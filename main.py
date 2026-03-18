import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import List

app = FastAPI(title="build me a bookmarks API with FastAPI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Bookmark(BaseModel):
    id: int
    title: str
    url: str

class BookmarkRequest(BaseModel):
    title: str
    url: str

bookmarks = [
    Bookmark(id=1, title="Google", url="https://www.google.com"),
    Bookmark(id=2, title="Bing", url="https://www.bing.com"),
]

@app.get("/")
def root(): 
    return {"status": "ok", "service": "build me a bookmarks API with FastAPI"}

@app.get("/health")
def health(): 
    return {"status": "healthy"}

@app.get("/bookmarks")
def get_bookmarks():
    return bookmarks

@app.get("/bookmarks/{bookmark_id}")
def get_bookmark(bookmark_id: int):
    for bookmark in bookmarks:
        if bookmark.id == bookmark_id:
            return bookmark
    raise HTTPException(status_code=404, detail="Bookmark not found")

@app.post("/bookmarks")
def create_bookmark(bookmark: BookmarkRequest):
    new_bookmark = Bookmark(id=len(bookmarks) + 1, title=bookmark.title, url=bookmark.url)
    bookmarks.append(new_bookmark)
    return new_bookmark

@app.put("/bookmarks/{bookmark_id}")
def update_bookmark(bookmark_id: int, bookmark: BookmarkRequest):
    for existing_bookmark in bookmarks:
        if existing_bookmark.id == bookmark_id:
            existing_bookmark.title = bookmark.title
            existing_bookmark.url = bookmark.url
            return existing_bookmark
    raise HTTPException(status_code=404, detail="Bookmark not found")

@app.delete("/bookmarks/{bookmark_id}")
def delete_bookmark(bookmark_id: int):
    for bookmark in bookmarks:
        if bookmark.id == bookmark_id:
            bookmarks.remove(bookmark)
            return {"message": "Bookmark deleted"}
    raise HTTPException(status_code=404, detail="Bookmark not found")

if __name__ == "__main__":
    print(" FastAPI app starting...")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)