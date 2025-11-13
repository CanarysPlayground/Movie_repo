# App.py Documentation

## Overview
`app.py` is the main Flask application file for the Movie Website. It provides a RESTful API for managing movies and playlists, along with a web interface for users to interact with the application.

## Dependencies
- **Flask**: Web framework for building the application
- **sqlite3**: Database interface for SQLite
- **os**: File path operations
- **math.ceil**: Pagination calculations

## Database Configuration
- **Database Path**: `movies.db` (in the same directory as app.py)
- **Database Factory**: Uses Flask's `g` object for connection management
- **Schema**: Defined in `schema.sql`

---

## Core Components

### 1. Database Utilities

#### `get_db()`
Returns a database connection stored in Flask's `g` object.

**Returns**: 
- `sqlite3.Connection` with `row_factory` set to `sqlite3.Row`

**Features**:
- Connection pooling per request context
- Row factory enabled for dict-like row access

#### `init_db()`
Initializes the database using the `schema.sql` file.

**Usage**: 
- Automatically called on first run if `movies.db` doesn't exist
- Can be manually invoked to reset the database

---

### 2. Pagination Helpers

#### `get_pagination_params(request, default_per_page=10, max_per_page=100)`
Extracts and validates pagination parameters from HTTP request.

**Parameters**:
- `request`: Flask request object
- `default_per_page`: Default items per page (default: 10)
- `max_per_page`: Maximum allowed items per page (default: 100)

**Returns**: 
- `tuple`: (page, per_page) both as integers

**Validation**:
- Ensures page is at least 1
- Limits per_page between 1 and max_per_page
- Handles invalid input gracefully (returns defaults)

#### `calculate_pagination_metadata(page, per_page, total_items)`
Calculates pagination metadata for API responses.

**Parameters**:
- `page`: Current page number
- `per_page`: Items per page
- `total_items`: Total number of items in dataset

**Returns**: 
- `dict` containing:
  - `page`: Current page number
  - `per_page`: Items per page
  - `total_items`: Total number of items
  - `total_pages`: Total number of pages
  - `has_next`: Boolean indicating if next page exists
  - `has_prev`: Boolean indicating if previous page exists
  - `offset`: SQL OFFSET value for query

#### `create_paginated_response(items, page, per_page, total_items)`
Creates a standardized paginated API response.

**Parameters**:
- `items`: List of items for current page
- `page`: Current page number
- `per_page`: Items per page
- `total_items`: Total number of items

**Returns**: 
- `dict` with structure:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_items": 50,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

---

### 3. Flask Application Setup

#### Application Initialization
```python
app = Flask(__name__)
```

#### Database Initialization
- Checks if `movies.db` exists
- Automatically initializes database on first run

#### Request Teardown
**`close_connection(exception)`**: Closes database connection at the end of each request to prevent connection leaks.

---

## API Endpoints

### 1. GET `/`
**Description**: Renders the main HTML page.

**Response**: 
- HTML page (`templates/index.html`)

---

### 2. GET `/api/movies`
**Description**: List all movies with pagination support.

**Query Parameters**:
| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `page` | int | 1 | - | Page number |
| `per_page` | int | 10 | 100 | Items per page |

**Response**: 
```json
{
  "data": [
    {
      "id": 1,
      "title": "Movie Title",
      "year": 2020,
      "genre": "Action",
      "synopsis": "Movie description"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_items": 50,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

**Status Codes**:
- `200 OK`: Success

---

### 3. GET `/api/movies/<movie_id>`
**Description**: Get details for a specific movie.

**URL Parameters**:
- `movie_id` (int): Movie ID

**Response**: 
```json
{
  "id": 1,
  "title": "Movie Title",
  "year": 2020,
  "genre": "Action",
  "synopsis": "Movie description"
}
```

**Status Codes**:
- `200 OK`: Movie found
- `404 Not Found`: Movie doesn't exist

**Error Response**:
```json
{
  "error": "Movie not found"
}
```

---

### 4. POST `/api/playlist`
**Description**: Add a movie to the playlist.

**Request Body**:
```json
{
  "movie_id": 1
}
```

**Response**: 
```json
{
  "status": "added",
  "movie_id": 1
}
```

**Status Codes**:
- `200 OK`: Movie added to playlist
- `400 Bad Request`: Missing movie_id
- `404 Not Found`: Movie doesn't exist
- `500 Internal Server Error`: Database error

**Error Responses**:
```json
{
  "error": "movie_id required"
}
```
```json
{
  "error": "movie not found"
}
```

---

### 5. GET `/api/playlist`
**Description**: Get all movies in the playlist.

**Response**: 
```json
[
  {
    "playlist_id": 1,
    "movie_id": 5,
    "title": "Movie Title",
    "year": 2020,
    "genre": "Action"
  }
]
```

**Status Codes**:
- `200 OK`: Success (returns empty array if playlist is empty)

---

## Database Schema

The application expects the following tables (defined in `schema.sql`):

### `movies` Table
- `id`: INTEGER PRIMARY KEY
- `title`: TEXT
- `year`: INTEGER
- `genre`: TEXT
- `synopsis`: TEXT

### `playlist` Table
- `id`: INTEGER PRIMARY KEY
- `movie_id`: INTEGER (foreign key to movies.id)

---

## Error Handling

### Input Validation
- Pagination parameters are validated and constrained
- Missing or invalid parameters default to safe values
- Invalid movie IDs return 404 errors

### Database Errors
- SQLite errors are caught and returned as 500 errors
- Connection management prevents leaks

---

## Running the Application

### Development Mode
```bash
python app.py
```

The application will start in debug mode on `http://127.0.0.1:5000/`

### Production Considerations
1. **Debug Mode**: Set `debug=False` in production
2. **Database Path**: Consider using environment variables
3. **Security**: Implement authentication for API endpoints
4. **WSGI Server**: Use production-grade server (Gunicorn, uWSGI)
5. **Database**: Consider PostgreSQL or MySQL for production

---

## Architecture

### Design Patterns
- **Factory Pattern**: Database connection management via `get_db()`
- **Separation of Concerns**: Utilities separated from routes
- **RESTful API**: Standard HTTP methods and status codes

### Request Flow
1. Client makes HTTP request
2. Flask routes request to appropriate handler
3. Handler gets database connection via `get_db()`
4. Data is queried/modified
5. Response is formatted (JSON or HTML)
6. Database connection is closed via teardown

---

## Future Enhancements

Based on the requirements document, the following features should be implemented:

1. **User Authentication**
   - Registration and login endpoints
   - Password hashing (bcrypt recommended)
   - Session management

2. **Movie Management**
   - POST `/api/movies` - Add new movie
   - PUT `/api/movies/<id>` - Edit movie
   - DELETE `/api/movies/<id>` - Delete movie

3. **Playlist Management**
   - DELETE `/api/playlist/<id>` - Remove from playlist
   - Named playlists support

4. **Search Functionality**
   - GET `/api/movies/search` - Search by title, genre, year

5. **Authorization**
   - API key or JWT tokens
   - User-specific collections

6. **Additional Validation**
   - Input sanitization
   - Schema validation (e.g., using marshmallow)

---

## Testing

### Manual Testing
Use tools like:
- **cURL**: Command-line testing
- **Postman**: GUI-based API testing
- **Browser DevTools**: Frontend testing

### Example cURL Commands
```bash
# List movies
curl http://127.0.0.1:5000/api/movies

# Get specific movie
curl http://127.0.0.1:5000/api/movies/1

# Add to playlist
curl -X POST http://127.0.0.1:5000/api/playlist \
  -H "Content-Type: application/json" \
  -d '{"movie_id": 1}'

# Get playlist
curl http://127.0.0.1:5000/api/playlist
```

---

## Troubleshooting

### Common Issues

**Issue**: Database not found
- **Solution**: Ensure `schema.sql` exists in the same directory

**Issue**: Port already in use
- **Solution**: Change port: `app.run(port=5001)`

**Issue**: Database locked
- **Solution**: Only one write operation at a time; consider connection pooling

**Issue**: CORS errors (frontend on different port)
- **Solution**: Install and configure Flask-CORS

---

## Version History
- **v1.0**: Initial implementation with basic CRUD operations and pagination

---

## License & Credits
Part of the Movie Website project.
