# FastAPI Social Media API

A simple social networking service API built with FastAPI that allows users to create, retrieve, update, and delete posts; add comments; and like/unlike posts.

## Features

- **Post Management**: Create, read, update, delete posts
- **Comment System**: Add, view, update, delete comments on posts  
- **Like System**: Like and unlike posts
- **SQLite Database**: Persistent storage with automatic initialization
- **OpenAPI Documentation**: Swagger UI and ReDoc interfaces
- **CORS Support**: Enabled for all origins

## Project Structure

```
python/
├── main.py           # FastAPI application with all endpoints
├── models.py         # Pydantic models for request/response validation
├── database.py       # SQLite database operations and CRUD functions
├── requirements.txt  # Python dependencies
├── sns_api.db       # SQLite database (created automatically)
└── .venv/           # Python virtual environment
```

## Installation & Setup

1. **Create and activate virtual environment**:
   ```bash
   cd python
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### Posts
- `GET /api/posts` - List all posts
- `POST /api/posts` - Create a new post
- `GET /api/posts/{postId}` - Get a specific post
- `PATCH /api/posts/{postId}` - Update a post
- `DELETE /api/posts/{postId}` - Delete a post

### Comments
- `GET /api/posts/{postId}/comments` - List comments for a post
- `POST /api/posts/{postId}/comments` - Create a comment
- `GET /api/posts/{postId}/comments/{commentId}` - Get a specific comment
- `PATCH /api/posts/{postId}/comments/{commentId}` - Update a comment
- `DELETE /api/posts/{postId}/comments/{commentId}` - Delete a comment

### Likes
- `POST /api/posts/{postId}/likes` - Like a post
- `DELETE /api/posts/{postId}/likes` - Unlike a post

## API Documentation

FastAPI automatically generates interactive API documentation in multiple formats:

### 1. Swagger UI - `/docs`
**URL**: `http://localhost:8000/docs`

Swagger UI is an **interactive documentation interface** that allows you to:
- 📖 Browse all available API endpoints
- 🧪 **Test API calls directly from your browser** (Try it out!)
- 📝 View request/response schemas and examples
- 🔍 See detailed parameter descriptions
- ✅ Execute API calls and see real responses

**Use Case**: Perfect for developers who want to quickly test and explore the API without writing code.

### 2. ReDoc - `/redoc`
**URL**: `http://localhost:8000/redoc`

ReDoc is a **clean, reading-focused documentation interface** that provides:
- 📚 A more polished, professional documentation layout
- 📊 Better for sharing with non-technical stakeholders
- 🎨 Clean, three-panel layout for easy navigation
- 📖 Optimized for reading and understanding the API structure
- 🖨️ Print-friendly documentation

**Use Case**: Ideal for creating user-facing documentation or sharing API specifications with clients/teams.

### 3. OpenAPI JSON - `/openapi.json`
**URL**: `http://localhost:8000/openapi.json`

The OpenAPI specification in JSON format:
- 🔧 **Machine-readable API specification** (OpenAPI 3.0.1 standard)
- 🤖 Used by tools to generate client SDKs, tests, and documentation
- 📋 Contains complete API contract: endpoints, schemas, responses, examples
- 🔄 Can be imported into tools like Postman, Insomnia, or API testing frameworks
- ✅ This endpoint serves the **exact same specification** as defined in `openapi.yaml`

**Use Case**: For programmatic access, code generation tools, API testing tools, or importing into other documentation platforms.

---

**Quick Comparison**:
| Feature | Swagger UI (`/docs`) | ReDoc (`/redoc`) | OpenAPI JSON (`/openapi.json`) |
|---------|---------------------|------------------|-------------------------------|
| Interactive Testing | ✅ Yes | ❌ No | ❌ No |
| Clean UI | ✅ Good | ✅ Excellent | N/A |
| Machine Readable | ❌ No | ❌ No | ✅ Yes |
| Best For | Testing & Exploration | Reading & Sharing | Tools & Integration |

## Example Usage

### Create a Post
```bash
curl -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "content": "Hello, World!"}'
```

### Get All Posts  
```bash
curl http://localhost:8000/api/posts
```

### Add a Comment
```bash  
curl -X POST http://localhost:8000/api/posts/1/comments \
  -H "Content-Type: application/json" \
  -d '{"username": "jane_smith", "content": "Great post!"}'
```

### Like a Post
```bash
curl -X POST http://localhost:8000/api/posts/1/likes \
  -H "Content-Type: application/json" \  
  -d '{"username": "alice"}' 
```

## Key Features Implemented

✅ **FastAPI Framework**: High-performance web framework  
✅ **SQLite Database**: Lightweight, file-based database with automatic initialization  
✅ **Exact OpenAPI Compliance**: Serves the exact OpenAPI 3.0.1 specification from `openapi.yaml`
✅ **CORS Enabled**: Configured to allow all origins for development
✅ **Port 8000**: Application runs on the specified port
✅ **Pydantic Validation**: Request/response validation with detailed error messages
✅ **Database Relationships**: Foreign keys and referential integrity  
✅ **Automatic Counts**: Post like_count and comment_count updated automatically
✅ **Error Handling**: Comprehensive error responses with proper HTTP status codes
✅ **Clean Architecture**: Separated concerns with models, database operations, and API routes
