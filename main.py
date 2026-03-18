import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Bookmarks API with FastAPI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Bookmark(BaseModel):
    id: Optional[int]
    title: str
    url: str

class BookmarkUpdate(BaseModel):
    title: Optional[str]
    url: Optional[str]

bookmarks = {}

@app.get("/")
def root():
    return {"status": "ok", "service": "Bookmarks API with FastAPI", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/bookmarks")
def get_bookmarks():
    return list(bookmarks.values())

@app.get("/bookmarks/{bookmark_id}")
def get_bookmark(bookmark_id: int):
    if bookmark_id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmarks[bookmark_id]

@app.post("/bookmarks")
def create_bookmark(bookmark: Bookmark):
    if bookmark.id is not None and bookmark.id in bookmarks:
        raise HTTPException(status_code=422, detail="Bookmark with this ID already exists")
    new_id = max(bookmarks.keys(), default=-1) + 1
    bookmarks[new_id] = bookmark.dict()
    bookmarks[new_id]["id"] = new_id
    return bookmarks[new_id], 201

@app.put("/bookmarks/{bookmark_id}")
def update_bookmark(bookmark_id: int, bookmark: BookmarkUpdate):
    if bookmark_id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    for key, value in bookmark.dict(exclude_unset=True).items():
        bookmarks[bookmark_id][key] = value
    return bookmarks[bookmark_id]

@app.delete("/bookmarks/{bookmark_id}")
def delete_bookmark(bookmark_id: int):
    if bookmark_id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    del bookmarks[bookmark_id]
    return {"message": "Bookmark deleted"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)