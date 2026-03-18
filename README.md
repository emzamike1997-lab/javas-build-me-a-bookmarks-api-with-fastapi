# Bookmarks API with FastAPI

## Endpoints

### GET /
Returns a JSON object with the status of the service.

### GET /health
Returns a JSON object with the health status of the service.

### GET /bookmarks
Returns a list of all bookmarks.

### GET /bookmarks/{bookmark_id}
Returns a single bookmark by ID.

### POST /bookmarks
Creates a new bookmark.

### PUT /bookmarks/{bookmark_id}
Updates a single bookmark by ID.

### DELETE /bookmarks/{bookmark_id}
Deletes a single bookmark by ID.

## Request and Response Examples

### GET /
```json
GET / HTTP/1.1
Host: example.com

HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "ok",
  "service": "Bookmarks API with FastAPI",
  "docs": "/docs"
}
```

### GET /bookmarks
```json
GET /bookmarks HTTP/1.1
Host: example.com

HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": 1,
    "title": "Example Bookmark",
    "url": "https://example.com"
  }
]
```

### POST /bookmarks
```json
POST /bookmarks HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "title": "New Bookmark",
  "url": "https://new.example.com"
}

HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 2,
  "title": "New Bookmark",
  "url": "https://new.example.com"
}
```

### PUT /bookmarks/{bookmark_id}
```json
PUT /bookmarks/1 HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "title": "Updated Bookmark"
}

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "title": "Updated Bookmark",
  "url": "https://example.com"
}
```

### DELETE /bookmarks/{bookmark_id}
```json
DELETE /bookmarks/1 HTTP/1.1
Host: example.com

HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Bookmark deleted"
}
```