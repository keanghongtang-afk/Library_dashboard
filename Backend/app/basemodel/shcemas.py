from pydantic import BaseModel

class BookSchema(BaseModel):
    title: str
    author: str
    genre: str
    stock: int

class BorrowSchema(BaseModel):
    user_id: int
    title: str
    
class ContactSchema(BaseModel):
    email: str
    phone: str
    
class UserSchema(BaseModel):
    id: str
    name: str
    email: str
    password: str
    status: bool = True
    borrow: str
    device_id: str
    role: str
    
class LoginRequestSchema(BaseModel):
    email: str
    password: str
    device_id: str

class SignInRequestSchema(BaseModel):
    name: str
    email: str
    password: str
    device_id: str
    role: str = "user"

class VerifyDeviceRequestSchema(BaseModel):
    email: str
    otp: str
