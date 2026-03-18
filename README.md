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

* Request Body:
  * title: string
  * url: string
* Response: 201 Created, JSON object with the new bookmark

### PUT /bookmarks/{bookmark_id}
Updates a single bookmark by ID.

* Request Body:
  * title: optional string
  * url: optional string
* Response: JSON object with the updated bookmark

### DELETE /bookmarks/{bookmark_id}
Deletes a single bookmark by ID.

* Response: JSON object with a success message