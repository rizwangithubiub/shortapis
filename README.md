# URL Shortening Service

A RESTful API service for shortening URLs with full CRUD operations, statistics tracking, and a simple web interface.

## Features

- ✅ Create short URLs from long URLs
- ✅ Retrieve original URLs from short codes
- ✅ Update existing short URLs
- ✅ Delete short URLs
- ✅ Track and retrieve access statistics
- ✅ Automatic URL redirection
- ✅ Simple web interface
- ✅ Input validation and error handling
- ✅ Unique short code generation

## Tech Stack

- **Backend**: Python 3.8+
- **Framework**: Flask
- **Database**: SQLite (via SQLAlchemy)
- **Frontend**: HTML/CSS/JavaScript

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/yourname-innovaxel-lastname.git
   cd yourname-innovaxel-lastname
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - API Base URL: `http://localhost:5000`
   - Web Interface: `http://localhost:5000`

## API Endpoints

### 1. Create Short URL
```http
POST /shorten
Content-Type: application/json

{
  "url": "https://www.example.com/some/long/url"
}
```

**Response (201 Created):**
```json
{
  "id": "1",
  "url": "https://www.example.com/some/long/url",
  "shortCode": "abc123",
  "createdAt": "2021-09-01T12:00:00Z",
  "updatedAt": "2021-09-01T12:00:00Z"
}
```

### 2. Retrieve Original URL
```http
GET /shorten/{shortCode}
```

**Response (200 OK):**
```json
{
  "id": "1",
  "url": "https://www.example.com/some/long/url",
  "shortCode": "abc123",
  "createdAt": "2021-09-01T12:00:00Z",
  "updatedAt": "2021-09-01T12:00:00Z"
}
```

### 3. Update Short URL
```http
PUT /shorten/{shortCode}
Content-Type: application/json

{
  "url": "https://www.example.com/some/updated/url"
}
```

**Response (200 OK):**
```json
{
  "id": "1",
  "url": "https://www.example.com/some/updated/url",
  "shortCode": "abc123",
  "createdAt": "2021-09-01T12:00:00Z",
  "updatedAt": "2021-09-01T12:30:00Z"
}
```

### 4. Delete Short URL
```http
DELETE /shorten/{shortCode}
```

**Response (204 No Content)**

### 5. Get URL Statistics
```http
GET /shorten/{shortCode}/stats
```

**Response (200 OK):**
```json
{
  "id": "1",
  "url": "https://www.example.com/some/long/url",
  "shortCode": "abc123",
  "createdAt": "2021-09-01T12:00:00Z",
  "updatedAt": "2021-09-01T12:00:00Z",
  "accessCount": 10
}
```

### 6. URL Redirection
```http
GET /{shortCode}
```

**Response (302 Found):** Redirects to original URL and increments access count

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid URL format"
}
```

### 404 Not Found
```json
{
  "error": "Short URL not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Database Schema

The application uses SQLite with the following table structure:

```sql
CREATE TABLE url (
    id INTEGER PRIMARY KEY,
    url VARCHAR(2048) NOT NULL,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 0
);
```

## Testing the API

### Using curl

1. **Create a short URL:**
   ```bash
   curl -X POST http://localhost:5000/shorten \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.google.com"}'
   ```

2. **Get original URL:**
   ```bash
   curl http://localhost:5000/shorten/abc123
   ```

3. **Update URL:**
   ```bash
   curl -X PUT http://localhost:5000/shorten/abc123 \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.github.com"}'
   ```

4. **Get statistics:**
   ```bash
   curl http://localhost:5000/shorten/abc123/stats
   ```

5. **Delete URL:**
   ```bash
   curl -X DELETE http://localhost:5000/shorten/abc123
   ```

### Using the Web Interface

1. Visit `http://localhost:5000` in your browser
2. Use the form to create, retrieve, and get statistics for short URLs
3. Test redirection by clicking on generated short URLs

## Project Structure

```
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── url_shortener.db   # SQLite database (created automatically)
└── venv/              # Virtual environment (created during setup)
```

## Key Features Implemented

1. **URL Validation**: Validates URL format using urllib.parse
2. **Unique Short Code Generation**: Uses random string generation with collision detection
3. **Access Count Tracking**: Increments counter on each redirection
4. **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
5. **Input Validation**: Validates all API inputs with meaningful error messages
6. **Database Integration**: Uses SQLAlchemy ORM for database operations
7. **Web Interface**: Simple HTML/CSS/JavaScript frontend for testing
8. **RESTful Design**: Follows REST principles for all endpoints

## Development Notes

- The application uses SQLite for simplicity, but can be easily switched to PostgreSQL or MySQL
- Short codes are generated using a random combination of letters and numbers
- The access count is incremented only when someone visits the redirect URL (/{shortCode})
- All timestamps are stored in UTC format
- The application includes proper error handling and validation
- Database tables are created automatically on first run

## Future Enhancements

- Add user authentication and authorization
- Implement rate limiting
- Add custom short code functionality
- Add URL expiration dates
- Implement analytics dashboard
- Add bulk URL operations
- Add API documentation with Swagger/OpenAPI

## License

This project is created as part of a take-home assignment for Innovaxel.