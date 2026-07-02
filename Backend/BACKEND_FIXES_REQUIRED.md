# Backend Fixes Required for Admin Role-Based Access Control

## Overview
The frontend has been updated to enforce role-based access control for the admin page. However, the backend needs to be updated to properly support this security model.

---

## 🔴 Critical Issue: Admin Account Creation

**Current Problem:**
- Anyone can create an admin account by setting `role="admin"` in the signup endpoint
- The frontend has been fixed to prevent this, but the backend still accepts it

**Solution:**
In `backend/app/services/loginService.py`, modify the `signup()` function:

```python
def signup(signup: SignInRequestSchema):
    try:
        existing_user = (
            session.query(User)
            .filter(User.email == signup.email)
            .first()
        )

        if existing_user:
            return {"message": "Email already exists"}

        # SECURITY FIX: Only allow 'user' role from frontend signup
        # Admin accounts should be created through a separate backend-only endpoint
        if signup.role not in ["user"]:  # Changed from ["admin", "user"]
            return {"error": "Invalid role. Only 'user' role is allowed."}
            
        # Rest of the function remains the same...
```

---

## 🔴 Issue 2: Login Doesn't Return User Role

**Current Problem:**
```python
return "Login Success!"  # Returns string, not user data
```

The frontend needs to know the user's role after login to determine page access.

**Solution:**
Modify the `Login()` function to return user data:

```python
def Login(request: LoginRequestSchema):
    user = session.query(User).filter(User.email == request.email).first()
    if not user:
        return "User not Found!"
    if user.password == request.password:
        if user.status:
            # Device detection logic...
            if request.device_id not in stored_device:
                # OTP required
                return {
                    "status": "otp_required",
                    "message": "A verification code has been sent to your email.",
                }
            else:
                # LOGIN SUCCESS - Return user data with role
                return {
                    "status": "success",
                    "message": "Login Success!",
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "role": user.role  # IMPORTANT: Include role
                    }
                }
        else:
            return "Account is not active"
    else:
        return "Incorrect Password"
```

---

## 🔴 Issue 3: Device Verification Doesn't Return User Role

**Current Problem:**
```python
return {"status": "success", "message": "Device verified. Login Success."}
```

Similar to login, this needs to include user role.

**Solution:**
Modify `verify_device()` to return user data:

```python
def verify_device(request: VerifyDeviceRequestSchema):
    # ... existing verification logic ...
    
    # After OTP verification success:
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
```

---

## 🔴 Issue 4: No Role-Based Access Control for Book Endpoints

**Current Problem:**
Any authenticated user can add, update, or delete books.

**Solution:**
Create a role-check middleware/decorator. Add to `app.py`:

```python
from functools import wraps
from fastapi import HTTPException, status

def require_admin(func):
    @wraps(func)
    async def wrapper(*args, user_email: str = None, **kwargs):
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        user = session.query(User).filter(User.email == user_email).first()
        if not user or user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        return await func(*args, **kwargs)
    return wrapper
```

Then protect book endpoints:

```python
@app.post("/books")
def add_book(book: BookSchema, user_email: str):  # Add user_email parameter
    # Check admin role
    user = session.query(User).filter(User.email == user_email).first()
    if not user or user.role != "admin":
        return {"error": "Admin access required"}
    
    return addBook(book)

@app.put("/books/{book_id}")
def update_book_info(book: BookSchema, book_id: int, user_email: str):
    # Check admin role
    user = session.query(User).filter(User.email == user_email).first()
    if not user or user.role != "admin":
        return {"error": "Admin access required"}
    # ... rest of function
```

---

## 📋 Implementation Checklist

- [X] Fix `signup()` to only allow `role="user"`
- [X] Modify `Login()` to return user object with role
- [X] Modify `verify_device()` to return user object with role
- [X] Add role-based access control to book endpoints (add, update, delete)
- [X] Create admin-only endpoints for admin operations
- [ ] Test login flow returns role correctly
- [ ] Test non-admin users cannot access book modification endpoints
- [ ] Test admin users can access admin panel

---

## Frontend Updates Already Complete ✅

1. **AuthContext.jsx** - Stores and tracks user role
2. **Signup.jsx** - Removed admin role option
3. **Login.jsx** - Ready to receive and store user role
4. **ProtectedAdminRoute.jsx** - Protects /admin route
5. **Admin.jsx** - Enhanced with user info and logout
6. **App.jsx** - Full routing with role-based access control

The frontend is now ready to properly handle admin authentication once the backend is updated.

---

## Testing Guide

### Test Admin Access:
1. Create admin account manually in database: `UPDATE users SET role='admin' WHERE email='admin@test.com'`
2. Login with admin account
3. Verify role is returned in login response
4. Verify redirect to /admin works
5. Verify logout functionality works

### Test Non-Admin Access:
1. Create regular user account
2. Login with user account
3. Verify role='user' is returned
4. Try to navigate to /admin - should redirect to /books
5. Try to call add_book endpoint - should get 403 error

---

## Security Notes

⚠️ **Current Status**: Frontend security is now in place. Backend still vulnerable until changes are implemented.

⚠️ **Do not rely on frontend role checks alone** - Backend must always verify roles.

⚠️ **Admin accounts should only be created via backend** - Never allow frontend signup to create admin accounts.

⚠️ **All sensitive operations must verify role** - Book add/update/delete, admin operations, user management, etc.
