import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="build me a bookmarks API with FastAPI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Bookmark(BaseModel):
    id: int
    title: str
    url: str

bookmarks = [
    Bookmark(id=1, title="Google", url="https://www.google.com"),
    Bookmark(id=2, title="Bing", url="https://www.bing.com"),
]

@app.get("/")
def root(): return {"status": "ok", "service": "build me a bookmarks API with FastAPI"}

@app.get("/health")
def health(): return {"status": "healthy"}

@app.get("/bookmarks")
def get_bookmarks():
    return bookmarks

@app.get("/bookmarks/{bookmark_id}")
def get_bookmark(bookmark_id: int):
    for bookmark in bookmarks:
        if bookmark.id == bookmark_id:
            return bookmark
    return {"error": "Bookmark not found"}

@app.post("/bookmarks")
def create_bookmark(new_bookmark: Bookmark):
    bookmarks.append(new_bookmark)
    return new_bookmark

@app.put("/bookmarks/{bookmark_id}")
def update_bookmark(bookmark_id: int, updated_bookmark: Bookmark):
    for i, bookmark in enumerate(bookmarks):
        if bookmark.id == bookmark_id:
            bookmarks[i] = updated_bookmark
            return updated_bookmark
    return {"error": "Bookmark not found"}

@app.delete("/bookmarks/{bookmark_id}")
def delete_bookmark(bookmark_id: int):
    for i, bookmark in enumerate(bookmarks):
        if bookmark.id == bookmark_id:
            del bookmarks[i]
            return {"message": "Bookmark deleted"}
    return {"error": "Bookmark not found"}

if __name__ == "__main__":
    print("🚀 FastAPI app starting...")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)