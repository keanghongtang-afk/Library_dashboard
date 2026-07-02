import random
import threading
from datetime import datetime, timedelta
import bcrypt

from app.basemodel.shcemas import LoginRequestSchema, SignInRequestSchema, UserSchema, VerifyDeviceRequestSchema
from app.db import session, User, Device, Verification_Pending
from app.filepath import VERIFYPATH, getVerifications, save
from app.services.emailService import send_new_device_alert, send_otp_email

from sqlalchemy.exc import IntegrityError

OTP_EXPIRY_MINUTES = 5

def _generate_otp() -> str:
    """Generate a random 6-digit OTP."""
    return str(random.randint(100000, 999999))


def Login(request: LoginRequestSchema):
    user = session.query(User).filter(User.email == request.email).first()
    if not user:
        return "User not Found!"
    if bcrypt.checkpw(password=request.password.encode('utf-8'), hashed_password=user.password):
        if user.status:
            # ── Device detection ──────────────────────────────────────
            stored_device = []
            for device in user.devices:
                stored_device.append(device.device_id)
            if request.device_id not in stored_device:
                # New/different device — send OTP and block device_id update
                user_email = user.email
                user_name  = user.name
                otp = _generate_otp()
                expires_at = (
                    datetime.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
                ).isoformat()
                # Persist the pending verification
                verify_otp = Verification_Pending(
                    user_email=request.email,
                    otp=otp,
                    new_device_id=request.device_id,
                    expires_at=expires_at
                )
                session.add(verify_otp)
                session.commit()
                session.refresh()
                # Send OTP email asynchronously
                threading.Thread(
                    target=send_otp_email,
                    args=(user_email, user_name, otp),
                    daemon=True,
                ).start()
                return {
                    "status": "otp_required",
                    "message": "A verification code has been sent to your email. "
                               "Please verify to continue.",
                }
            else:
                return {
                    "status": "success",
                    "message": "Login Success!",
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "role": user.role
                    }
                }
            # ─────────────────────────────────────────────────────────
        else:
            return "Account is not active"
    else:
        return "Incorrect Password"


def verify_device(request: VerifyDeviceRequestSchema):
    """
    Verify the OTP sent to the user's email and, if valid, commit the new device_id.
    """
    record = session.query(Verification_Pending).filter(Verification_Pending.user_email == request.email).first()
    
    if not record:
        return {"status": "error", "message": "No pending verification for this email."}

    # Check expiry
    expires_at = datetime.fromisoformat(record.expires_at)
    if datetime.now() > expires_at:
        # Clean up expired record
        session.delete(record)
        session.commit()
        session.refresh(record)
        return {"status": "error", "message": "OTP has expired. Please log in again."}

    # Check OTP
    if record.otp != request.otp:
        return {"status": "error", "message": "Incorrect OTP. Please try again."}

    # OTP valid — update device_id in users
    new_device_id = record.new_device_id
    user = session.query(User).filter(User.email == request.email).first()
    if not user:
        return "User not found!"
    
    exist_devise= session.query(Device).filter(Device.user_id == user.id).all()
    if new_device_id in exist_devise:
        return "Device already exit!"
    device = Device(
        user_id= user.id,
        device_id =new_device_id
    )
    
    session.add(device)
    session.commit()
    session.refresh(device)

    # Remove the used verification record
    session.delete(record)
    session.commit()
    session.close()

    return {
        "status": "success", 
        "message": "Device verified. Login Success.",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role  # IMPORTANT: Include role
        }
    }


def Logout(
    email: str,
    device_id: str,
):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return "User Not Found!"
    user_devices = []
    for device in user.devices:
        user_devices.append(device.device_id)
    if not user:
        return "User Not Found"
    
    if user.status:
        if device_id in user_devices:
            device = session.query(Device).filter(Device.device_id == device_id).first()
            if not device:
                return "Device Not Found"
            session.delete(device)
            session.commit()
            return "Logout Success"
        else:
            return "Device not match"
    else:
        return "Account is not active"


def signup(signup: SignInRequestSchema):
    try:
        existing_user = (
            session.query(User)
            .filter(User.email == signup.email)
            .first()
        )

        if existing_user:
            return {"message": "Email already exists"}

        if signup.role not in ["user"]:
            return {"error": "Invalid role. Only 'user' role is allowed."}
        password_byte = signup.password.encode("utf-8")
        hash_pass = bcrypt.hashpw(password_byte, bcrypt.gensalt())
        user = User(
            name=signup.name,
            email=signup.email,
            password=hash_pass,
            status=True,
            role=signup.role
        )

        session.add(user)
        session.flush()  # gets user.id without commit

        device = Device(
            user_id=user.id,
            device_id=signup.device_id
        )

        session.add(device)

        session.commit()
        session.refresh(user)

        return {"message": "Successfully signed up!"}

    except IntegrityError:
        session.rollback()
        return {"error": "Database integrity error"}

    except Exception as e:
        session.rollback()
        return {"error": str(e)}

    finally:
        session.close()
