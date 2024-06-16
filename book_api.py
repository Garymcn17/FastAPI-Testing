from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4
import sqlite3
import json

connection = sqlite3.connect("books.db", check_same_thread=False)
cur = connection.cursor()
#cur.execute("CREATE TABLE Books(id, title, price, kind)")

#res = cur.execute("SELECT * FROM books WHERE ID = '1f5b0bb7-f5e2-404c-b9ae-10fc2af8dc12'")
#test = res.fetchone()
#print(test)

# cur.execute("""
#     INSERT INTO books VALUES
#         ('Prophet Song', 1975, 8.2),
#         ('And Now for Something Completely Different', 1971, 7.5)
# """)

app = FastAPI()

class Book(BaseModel):
    id: Optional[UUID] = None
    kind: Optional[str] = None
    title: str
    price: float

books = [] 

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/books/", response_model=List[Book])
def read_books():
    res = cur.execute("SELECT * FROM books")
    book_list = res.fetchall()
    json_str = jsonable_encoder(book_list)
    #json_str = json.dumps(book_list)
    print(json_str)
    return JSONResponse(content=json_str)
    #return books

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: UUID):
    # for book in books:
    #     if book.id == book_id:
    #         return book
    res = cur.execute(f"SELECT * FROM books WHERE ID = '{book_id}'")
    #print(res.fetchone())
    book_list = res.fetchone()
    if book_list:
        json_str = jsonable_encoder(book_list)
        return JSONResponse(content=json_str)
    else:
        raise HTTPException(status_code=404, detail="Book not found.")

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: UUID, book_update: Book):
    res = cur.execute(f"UPDATE books SET price = {book_update.price} WHERE id = '{book_id}'")
    if res.rowcount > 0:
        connection.commit()
        return book_update
    else:
        raise HTTPException(status_code=404, detail="Could not update book.")
    # for idx, book in enumerate(books):
    #     if book.id == book_id:
    #         updated_book = book.copy(update=book_update.dict(exclude_unset=True))
    #         books[idx] = update_book
    #         return updated_book
    # raise HTTPException(status_code=404, detail="Book not found. Cannot update.")

@app.post("/books/", response_model=Book)
async def create_book(book: Book):
    book.id = uuid4()
    books.append(book)
    cur.execute(f"INSERT INTO books VALUES ('{book.id}','{book.title}', {book.price}, '{book.kind}') ")
    connection.commit()
    return book

@app.delete("/books/{book_id}", response_model=Book)
async def delete_book(book_id: UUID):
    #for idx, book in enumerate(books):
    #    if book.id == book_id:
    res = cur.execute(f"DELETE FROM books WHERE id = '{book_id}'")
    print(res.rowcount)
    if(res.rowcount > 0):
        connection.commit()
        return JSONResponse(status_code=200, content="Book successfully deleted.")  
    else:
        raise HTTPException(status_code=404, detail="Book not found. Cannot delete.")
    
    #return "Book"
    #        return books.pop(idx)
    #raise HTTPException(status_code=404, detail="Book not found. Cannot delete.")