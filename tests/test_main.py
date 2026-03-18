Here's an example of how you can write comprehensive tests for the bookmarks API using Pytest.

### === test_bookmarks_api.py ===

```python
# test_bookmarks_api.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bookmarks API"}

def test_create_bookmark():
    """Test creating a new bookmark"""
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]
    assert response.json()["url"] == data["url"]

def test_get_bookmark():
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

def test_update_bookmark():
    """Test updating a bookmark"""
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    bookmark_id = response.json()["id"]

    # Update the bookmark
    new_data = {"title": "Updated Bookmark", "url": "https://example.com/new"}
    response = client.put(f"/bookmarks/{bookmark_id}", json=new_data)
    assert response.status_code == 200
    assert response.json()["title"] == new_data["title"]
    assert response.json()["url"] == new_data["url"]

def test_delete_bookmark():
    """Test deleting a bookmark"""
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    bookmark_id = response.json()["id"]

    # Delete the bookmark
    response = client.delete(f"/bookmarks/{bookmark_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Bookmark deleted"

def test_create_bookmark_invalid_data():
    """Test creating a new bookmark with invalid data"""
    data = {"title": "Test Bookmark"}
    response = client.post("/bookmarks", json=data)
    assert response.status_code == 422

def test_get_bookmark_non_existent():
    """Test getting a non-existent bookmark by ID"""
    response = client.get("/bookmarks/123")
    assert response.status_code == 404

def test_update_bookmark_non_existent():
    """Test updating a non-existent bookmark"""
    data = {"title": "Updated Bookmark", "url": "https://example.com/new"}
    response = client.put("/bookmarks/123", json=data)
    assert response.status_code == 404

def test_delete_bookmark_non_existent():
    """Test deleting a non-existent bookmark"""
    response = client.delete("/bookmarks/123")
    assert response.status_code == 404
```

### === test_bookmarks_api_integration.py ===

```python
# test_bookmarks_api_integration.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_bookmark_and_get_all():
    """Test creating a new bookmark and getting all bookmarks"""
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]
    assert response.json()["url"] == data["url"]

    response = client.get("/bookmarks")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == data["title"]
    assert response.json()[0]["url"] == data["url"]

def test_create_multiple_bookmarks_and_get_all():
    """Test creating multiple new bookmarks and getting all bookmarks"""
    data1 = {"title": "Test Bookmark 1", "url": "https://example.com/1"}
    data2 = {"title": "Test Bookmark 2", "url": "https://example.com/2"}
    response1 = client.post("/bookmarks", json=data1)
    response2 = client.post("/bookmarks", json=data2)

    assert response1.status_code == 201
    assert response1.json()["title"] == data1["title"]
    assert response1.json()["url"] == data1["url"]

    assert response2.status_code == 201
    assert response2.json()["title"] == data2["title"]
    assert response2.json()["url"] == data2["url"]

    response = client.get("/bookmarks")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == data1["title"]
    assert response.json()[0]["url"] == data1["url"]
    assert response.json()[1]["title"] == data2["title"]
    assert response.json()[1]["url"] == data2["url"]
```

### === test_bookmarks_api_db.py ===

```python
# test_bookmarks_api_db.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_bookmark_and_get_from_db():
    """Test creating a new bookmark and getting it from the database"""
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]
    assert response.json()["url"] == data["url"]

    # Get the bookmark from the database
    from main import db
    with db.sessionmaker() as session:
        bookmark = session.query(db.Bookmark).first()
        assert bookmark.title == data["title"]
        assert bookmark.url == data["url"]

def test_update_bookmark_and_get_from_db():
    """Test updating a bookmark and getting it from the database"""
    # Create a new bookmark
    data = {"title": "Test Bookmark", "url": "https://example.com"}
    response = client.post("/bookmarks", json=data)
    bookmark_id = response.json()["id"]

    # Update the bookmark
    new_data = {"title": "Updated Bookmark", "url": "https://example.com/new"}
    response = client.put(f"/bookmarks/{bookmark_id}", json=new_data)
    assert response.status_code == 200
    assert response.json()["title"] == new_data["title"]
    assert response.json()["url"] == new_data["url"]

    # Get the updated bookmark from the database
    from main import db
    with db.sessionmaker() as session:
        bookmark = session.query(db.Bookmark).first()
        assert bookmark.title == new_data["title"]
        assert bookmark.url == new_data["url"]
```

Note: The above tests assume that you have a `main.py` file that defines the FastAPI app and the database models. The tests also assume that you have a `db.py` file that defines the database session maker and the database models.

Also, note that the above tests are just examples and you may need to modify them to fit your specific use case. Additionally, you may want to add more tests to cover other scenarios and edge cases.