from app.basemodel.shcemas import BookSchema, BorrowSchema
from app.db import session, Book, Borrow, User


def addBook(book: BookSchema):
    # store a serializable mapping instead of the Pydantic model
    SameBook = session.query(Book).filter(Book.title == book.title).first()
    if SameBook:
        SameBook.stock += book.stock
        session.commit()
        return {"Same Book":"Added to the existing book!"}
    try:
        addbook = Book(title= book.title, author=book.author,genre=book.genre,stock=book.stock)
        session.add(addbook)
        session.commit()
        session.refresh(addbook)
    finally: session.close()
    
    return f"Successfully added {book}"
    
def BorrowBook(book: BorrowSchema):
    try:
        borrow = Borrow(user_id= book.user_id, title= book.title)
        borrowBook = session.query(Book).filter(Book.title == book.title).first()
        borrowBook.stock -= 1
        session.add(borrowBook)
        session.add(borrow)
        session.commit()
        session.refresh(borrow)
    finally:
        session.close()
    return f"User No: {book.user_id} has borrow {book.title}"

def ReturnBook(book: BorrowSchema):
    returnedBook = Borrow(book.user_id,book.title)
    BookForm = session.query(Book).filter(Book.title == book.title).first()
    BookForm.stock += 1
    try:
        session.delete(returnedBook)
        session.commit()
    finally: session.close()
    
    return f"User No: {book.user_id} has return {book.title}"