### === test_bookmarks_api.py ===

```python
# Import necessary libraries
from fastapi.testclient import TestClient
from main import app

# Create a test client for the API
client = TestClient(app)

# Unit tests for the API
def test_bookmarks_api_root():
    """Test the root endpoint of the API"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bookmarks API"}

def test_bookmarks_api_create_bookmark():
    """Test creating a new bookmark"""
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]
    assert response.json()["url"] == data["url"]

def test_bookmarks_api_get_bookmark():
    """Test getting a bookmark by ID"""
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    bookmark_id = response.json()["id"]
    # Get the bookmark by ID
    response = client.get(f"/bookmarks/{bookmark_id}")
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["url"] == data["url"]

def test_bookmarks_api_update_bookmark():
    """Test updating a bookmark"""
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    bookmark_id = response.json()["id"]
    # Update the bookmark
    new_data = {"title": "Updated Test Bookmark", "url": "https://example.com/new"}
    response = client.put(f"/bookmarks/{bookmark_id}", json=new_data)
    assert response.status_code == 200
    assert response.json()["title"] == new_data["title"]
    assert response.json()["url"] == new_data["url"]

def test_bookmarks_api_delete_bookmark():
    """Test deleting a bookmark"""
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    bookmark_id = response.json()["id"]
    # Delete the bookmark
    response = client.delete(f"/bookmarks/{bookmark_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Bookmark deleted"

# Integration tests for the API
def test_bookmarks_api_create_bookmark_integration():
    """Test creating a new bookmark in an integration test"""
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]
    assert response.json()["url"] == data["url"]

def test_bookmarks_api_get_bookmark_integration():
    """Test getting a bookmark by ID in an integration test"""
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    bookmark_id = response.json()["id"]
    # Get the bookmark by ID
    response = client.get(f"/bookmarks/{bookmark_id}")
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["url"] == data["url"]

def test_bookmarks_api_update_bookmark_integration():
    """Test updating a bookmark in an integration test"""
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    bookmark_id = response.json()["id"]
    # Update the bookmark
    new_data = {"title": "Updated Test Bookmark", "url": "https://example.com/new"}
    response = client.put(f"/bookmarks/{bookmark_id}", json=new_data)
    assert response.status_code == 200
    assert response.json()["title"] == new_data["title"]
    assert response.json()["url"] == new_data["url"]

def test_bookmarks_api_delete_bookmark_integration():
    """Test deleting a bookmark in an integration test"""
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    bookmark_id = response.json()["id"]
    # Delete the bookmark
    response = client.delete(f"/bookmarks/{bookmark_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Bookmark deleted"
```

### === test_bookmarks_api_models.py ===

```python
# Import necessary libraries
from main import Bookmark, BookmarkDB
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a test database engine
engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

# Define a test model for the Bookmark
class TestBookmark(BaseModel):
    title: str
    url: str

# Define a test model for the BookmarkDB
class TestBookmarkDB(BookmarkDB):
    def __init__(self, session):
        self.session = session

    def get_bookmark(self, id):
        return self.session.query(Bookmark).get(id)

    def create_bookmark(self, title, url):
        bookmark = Bookmark(title=title, url=url)
        self.session.add(bookmark)
        self.session.commit()
        return bookmark

# Test the Bookmark model
def test_bookmark_model():
    """Test the Bookmark model"""
    bookmark = TestBookmark(title="Test Bookmark", url="https://example.com")
    assert bookmark.title == "Test Bookmark"
    assert bookmark.url == "https://example.com"

# Test the BookmarkDB model
def test_bookmark_db_model():
    """Test the BookmarkDB model"""
    session = Session()
    bookmark_db = TestBookmarkDB(session)
    bookmark = bookmark_db.create_bookmark("Test Bookmark", "https://example.com")
    assert bookmark.title == "Test Bookmark"
    assert bookmark.url == "https://example.com"
    session.close()
```

### === conftest.py ===

```python
# Import necessary libraries
import pytest
from main import app

# Create a test client for the API
@pytest.fixture
def client():
    """Create a test client for the API"""
    yield TestClient(app)

# Create a test database engine
@pytest.fixture
def db():
    """Create a test database engine"""
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    yield Session()
    engine.dispose()

# Create a test model for the Bookmark
@pytest.fixture
def bookmark_model():
    """Create a test model for the Bookmark"""
    yield TestBookmark

# Create a test model for the BookmarkDB
@pytest.fixture
def bookmark_db_model(db):
    """Create a test model for the BookmarkDB"""
    yield TestBookmarkDB(db)
```

### === main.py ===

```python
# Import necessary libraries
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the API application
app = FastAPI()

# Define the Bookmark model
class Bookmark(BaseModel):
    id: int
    title: str
    url: str

# Define the BookmarkDB model
class BookmarkDB:
    def __init__(self, session):
        self.session = session

    def get_bookmark(self, id):
        return self.session.query(Bookmark).get(id)

    def create_bookmark(self, title, url):
        bookmark = Bookmark(title=title, url=url)
        self.session.add(bookmark)
        self.session.commit()
        return bookmark

# Define the root endpoint of the API
@app.get("/")
async def read_root():
    """Return a message indicating that the API is working"""
    return {"message": "Bookmarks API"}

# Define the endpoint for creating a new bookmark
@app.post("/bookmarks")
async def create_bookmark(title: str, url: str):
    """Create a new bookmark"""
    session = create_engine("sqlite:///:memory:").connect()
    session.execute("CREATE TABLE bookmarks (id INTEGER PRIMARY KEY, title TEXT, url TEXT)")
    session.close()
    bookmark_db = BookmarkDB(session)
    bookmark = bookmark_db.create_bookmark(title, url)
    return {"id": bookmark.id, "title": bookmark.title, "url": bookmark.url}

# Define the endpoint for getting a bookmark by ID
@app.get("/bookmarks/{id}")
async def get_bookmark(id: int):
    """Get a bookmark by ID"""
    session = create_engine("sqlite:///:memory:").connect()
    session.execute("CREATE TABLE bookmarks (id INTEGER PRIMARY KEY, title TEXT, url TEXT)")
    session.close()
    bookmark_db = BookmarkDB(session)
    bookmark = bookmark_db.get_bookmark(id)
    if bookmark:
        return {"id": bookmark.id, "title": bookmark.title, "url": bookmark.url}
    else:
        return {"message": "Bookmark not found"}

# Define the endpoint for updating a bookmark
@app.put("/bookmarks/{id}")
async def update_bookmark(id: int, title: str, url: str):
    """Update a bookmark"""
    session = create_engine("sqlite:///:memory:").connect()
    session.execute("CREATE TABLE bookmarks (id INTEGER PRIMARY KEY, title TEXT, url TEXT)")
    session.close()
    bookmark_db = BookmarkDB(session)
    bookmark = bookmark_db.get_bookmark(id)
    if bookmark:
        bookmark.title = title
        bookmark.url = url
        session = create_engine("sqlite:///:memory:").connect()
        session.execute("CREATE TABLE bookmarks (id INTEGER PRIMARY KEY, title TEXT, url TEXT)")
        session.close()
        bookmark_db = BookmarkDB(session)
        bookmark_db.session.add(bookmark)
        bookmark_db.session.commit()
        return {"id": bookmark.id, "title": bookmark.title, "url": bookmark.url}
    else:
        return {"message": "Bookmark not found"}

# Define the endpoint for deleting a bookmark
@app.delete("/bookmarks/{id}")
async def delete_bookmark(id: int):
    """Delete a bookmark"""
    session = create_engine("sqlite:///:memory:").connect()
    session.execute("CREATE TABLE bookmarks (id INTEGER PRIMARY KEY, title TEXT, url TEXT)")
    session.close()
    bookmark_db = BookmarkDB(session)
    bookmark = bookmark_db.get_bookmark(id)
    if bookmark:
        bookmark_db.session.delete(bookmark)
        bookmark_db.session.commit()
        return {"message": "Bookmark deleted"}
    else:
        return {"message": "Bookmark not found"}
```