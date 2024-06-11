from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4

app = FastAPI()

class Book(BaseModel):
    id: Optional[UUID] = None
    name: str
    price: float
    kind: Optional[str] = None

books = [] 

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/books/", response_model=List[Book])
def read_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: UUID):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found.")

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: UUID, book_update: Book):
    for idx, book in enumerate(books):
        if book.id == book_id:
            updated_book = book.copy(update=book_update.dict(exclude_unset=True))
            books[idx] = update_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found. Cannot update.")

@app.post("/books/", response_model=Book)
async def create_book(book: Book):
    book.id = uuid4()
    books.append(book)
    return book

@app.delete("/books/{book_id}", response_model=Book)
async def delete_book(book_id: UUID):
    for idx, book in enumerate(books):
        if book.id == book_id:
            return books.pop(idx)
    raise HTTPException(status_code=404, detail="Book not found. Cannot delete.")