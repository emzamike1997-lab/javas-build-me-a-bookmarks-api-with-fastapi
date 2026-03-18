from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Enable CORS for all origins
from fastapi.middleware.cors import CORSMiddleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
bookmarks = {}

class Bookmark(BaseModel):
    id: int
    title: str
    url: str

class BookmarkRequest(BaseModel):
    title: str
    url: str

# GET /health endpoint
@app.get("/health")
def get_health():
    return {"status": "healthy"}

# GET / endpoint
@app.get("/")
def get_api_info():
    return {"info": "Bookmarks API"}

# GET /bookmarks endpoint
@app.get("/bookmarks", response_model=List[Bookmark])
def get_bookmarks():
    return list(bookmarks.values())

# GET /bookmarks/{id} endpoint
@app.get("/bookmarks/{id}", response_model=Bookmark)
def get_bookmark(id: int):
    if id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmarks[id]

# POST /bookmarks endpoint
@app.post("/bookmarks", response_model=Bookmark)
def create_bookmark(request: BookmarkRequest):
    new_id = max(bookmarks.keys(), default=0) + 1
    new_bookmark = Bookmark(id=new_id, title=request.title, url=request.url)
    bookmarks[new_id] = new_bookmark
    return new_bookmark

# PUT /bookmarks/{id} endpoint
@app.put("/bookmarks/{id}", response_model=Bookmark)
def update_bookmark(id: int, request: BookmarkRequest):
    if id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    updated_bookmark = Bookmark(id=id, title=request.title, url=request.url)
    bookmarks[id] = updated_bookmark
    return updated_bookmark

# DELETE /bookmarks/{id} endpoint
@app.delete("/bookmarks/{id}")
def delete_bookmark(id: int):
    if id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    del bookmarks[id]
    return {"message": "Bookmark deleted"}