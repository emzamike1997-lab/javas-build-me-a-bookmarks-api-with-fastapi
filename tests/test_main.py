### === test_bookmarks_api.py ===

```python
# Import necessary libraries
from fastapi.testclient import TestClient
from main import app
import pytest
from pydantic import BaseModel
from typing import List

# Define a Pydantic model for the Bookmark
class Bookmark(BaseModel):
    id: int
    title: str
    url: str

# Define a client instance for the API
client = TestClient(app)

# Unit tests
def test_create_bookmark():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks/", json=data)
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]
    assert response.json()["url"] == data["url"]

def test_get_bookmark():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    client.post("/bookmarks/", json=data)
    # Get the bookmark
    response = client.get("/bookmarks/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == data["title"]
    assert response.json()[0]["url"] == data["url"]

def test_get_bookmark_by_id():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    client.post("/bookmarks/", json=data)
    # Get the bookmark by ID
    response = client.get("/bookmarks/1")
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["url"] == data["url"]

def test_update_bookmark():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    client.post("/bookmarks/", json=data)
    # Update the bookmark
    new_data = {"title": "Updated Bookmark", "url": "https://updated.com"}
    response = client.put("/bookmarks/1", json=new_data)
    assert response.status_code == 200
    assert response.json()["title"] == new_data["title"]
    assert response.json()["url"] == new_data["url"]

def test_delete_bookmark():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    client.post("/bookmarks/", json=data)
    # Delete the bookmark
    response = client.delete("/bookmarks/1")
    assert response.status_code == 200

# Integration tests
def test_create_bookmark_with_invalid_data():
    # Create a new bookmark with invalid data
    data = {"title": "Test Bookmark"}
    response = client.post("/bookmarks/", json=data)
    assert response.status_code == 422

def test_get_bookmark_by_non_existent_id():
    # Get a bookmark by non-existent ID
    response = client.get("/bookmarks/100")
    assert response.status_code == 404

def test_update_bookmark_with_invalid_data():
    # Update a bookmark with invalid data
    data = {"title": "Updated Bookmark"}
    response = client.put("/bookmarks/1", json=data)
    assert response.status_code == 422

def test_delete_bookmark_with_invalid_id():
    # Delete a bookmark with invalid ID
    response = client.delete("/bookmarks/100")
    assert response.status_code == 404
```

### === test_bookmarks_api_integration.py ===

```python
# Import necessary libraries
from fastapi.testclient import TestClient
from main import app
import pytest
from pydantic import BaseModel
from typing import List

# Define a Pydantic model for the Bookmark
class Bookmark(BaseModel):
    id: int
    title: str
    url: str

# Define a client instance for the API
client = TestClient(app)

# Integration tests
def test_create_bookmark_and_get_all_bookmarks():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    client.post("/bookmarks/", json=data)
    # Get all bookmarks
    response = client.get("/bookmarks/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == data["title"]
    assert response.json()[0]["url"] == data["url"]

def test_create_bookmark_and_get_bookmark_by_id():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    client.post("/bookmarks/", json=data)
    # Get the bookmark by ID
    response = client.get("/bookmarks/1")
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["url"] == data["url"]

def test_create_bookmark_and_update_bookmark():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    client.post("/bookmarks/", json=data)
    # Update the bookmark
    new_data = {"title": "Updated Bookmark", "url": "https://updated.com"}
    response = client.put("/bookmarks/1", json=new_data)
    assert response.status_code == 200
    assert response.json()["title"] == new_data["title"]
    assert response.json()["url"] == new_data["url"]

def test_create_bookmark_and_delete_bookmark():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    client.post("/bookmarks/", json=data)
    # Delete the bookmark
    response = client.delete("/bookmarks/1")
    assert response.status_code == 200
```

### === test_bookmarks_api_db.py ===

```python
# Import necessary libraries
from fastapi.testclient import TestClient
from main import app
import pytest
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define a Pydantic model for the Bookmark
class Bookmark(BaseModel):
    id: int
    title: str
    url: str

# Define a client instance for the API
client = TestClient(app)

# Define a test database engine
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Integration tests
def test_create_bookmark_and_get_all_bookmarks_db():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    client.post("/bookmarks/", json=data)
    # Get all bookmarks
    response = client.get("/bookmarks/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == data["title"]
    assert response.json()[0]["url"] == data["url"]

def test_create_bookmark_and_get_bookmark_by_id_db():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    client.post("/bookmarks/", json=data)
    # Get the bookmark by ID
    response = client.get("/bookmarks/1")
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["url"] == data["url"]

def test_create_bookmark_and_update_bookmark_db():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    client.post("/bookmarks/", json=data)
    # Update the bookmark
    new_data = {"title": "Updated Bookmark", "url": "https://updated.com"}
    response = client.put("/bookmarks/1", json=new_data)
    assert response.status_code == 200
    assert response.json()["title"] == new_data["title"]
    assert response.json()["url"] == new_data["url"]

def test_create_bookmark_and_delete_bookmark_db():
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    client.post("/bookmarks/", json=data)
    # Delete the bookmark
    response = client.delete("/bookmarks/1")
    assert response.status_code == 200
```