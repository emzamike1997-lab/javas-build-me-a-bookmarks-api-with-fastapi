# Bookmarks API

## Endpoints

### GET /
Returns a JSON object with the status of the service.

### GET /health
Returns a JSON object with the health status of the service.

### GET /bookmarks
Returns a list of all bookmarks.

### GET /bookmarks/{bookmark_id}
Returns a single bookmark by id.

### POST /bookmarks
Creates a new bookmark.

### PUT /bookmarks/{bookmark_id}
Updates an existing bookmark.

### DELETE /bookmarks/{bookmark_id}
Deletes a bookmark.

## Example Use Cases

* Create a new bookmark: `curl -X POST -H "Content-Type: application/json" -d '{"title": "Example", "url": "https://example.com"}' http://localhost:8000/bookmarks`
* Get all bookmarks: `curl http://localhost:8000/bookmarks`
* Get a single bookmark: `curl http://localhost:8000/bookmarks/1`
* Update a bookmark: `curl -X PUT -H "Content-Type: application/json" -d '{"id": 1, "title": "Updated Example", "url": "https://updated.example.com"}' http://localhost:8000/bookmarks/1`
* Delete a bookmark: `curl -X DELETE http://localhost:8000/bookmarks/1`