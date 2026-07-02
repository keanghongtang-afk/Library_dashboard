from functools import wraps
from fastapi import HTTPException, status
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.services.bookservice import addBook, BorrowBook, ReturnBook
from app.services.loginService import Login, signup, Logout, verify_device
from app.basemodel.shcemas import BookSchema,BorrowSchema, UserSchema, LoginRequestSchema, SignInRequestSchema, VerifyDeviceRequestSchema
from app.db import session, Book, User, Borrow
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://keanghongtang-afk.github.io",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

""" Book Services """

@app.post("/books")
def add_book(book: BookSchema, user_email: str):
    user = session.query(User).filter(User.email == user_email).first()
    if not user or user.role != 'admin':
        return {"error": "Admin access required"}
    return addBook(book)

@app.get("/books")
def getBook(limit: int ):
    return session.query(Book).limit(limit=limit).all()

@app.put("/books/{book_id}")
def update_book_info(
    book: BookSchema,
    book_id: int,
    user_email: str
):
    try:
        user = session.query(User).filter(User.email == user_email).first()
        if not user or user.role != 'admin':
            return {"error": "Admin access required"}
        updateBook = session.query(Book).filter(Book.id == book_id).first()
        updateBook.title = book.title
        updateBook.author = book.author
        updateBook.genre = book.genre
        session.commit()
    finally: 
        session.close()
    return "successfully updated!"

@app.delete("/books/{book_id}")
def deleteBook(book_id: int, user_email: str):
    user = session.query(User).filter(User.email == user_email).first()
    if not user or user.role != 'admin':
        return {"error": "Admin access required"}
    session.query(Book).filter(Book.id == book_id).delete()
    session.commit()
    return {"Noti":"Delete successfully!"}

@app.post("/borrow")
def borrowBook(book: BorrowSchema):
    return BorrowBook(book=book)

@app.get("/borrow")
def getBorrowedBooks(limit: int):
    users = session.query(User).limit(limit=limit).all()
    whoBorrow = []
    for user in users:
        whoBorrow.append({
            "username": user.name,
            "Borrow": [
                book.title for book in user.borrow
            ]
        })
    return whoBorrow

@app.post("/return")
def returnBook(book: BorrowSchema):
    return ReturnBook(book=book)



"""Users Account Services"""

@app.post("/login")
def user_login(
    login: LoginRequestSchema
):
    return Login(LoginRequestSchema(email=login.email, password=login.password, device_id=login.device_id))

@app.post("/signin")
def Sign_in(
    signin: SignInRequestSchema
    ):
    return signup(SignInRequestSchema(name=signin.name, email=signin.email, password=signin.password, device_id=signin.device_id, role=signin.role))

@app.post("/verify-device")
def verify_device_endpoint(request: VerifyDeviceRequestSchema):
    return verify_device(request)

@app.post("/logout")
def user_logout(
    email:str = Form(...),
    device_id:str = Form(...)
    ):
    return Logout(email, device_id)

