"""
FastAPI Social Media API
A simple social networking service API for posts, comments, and likes.
"""
import yaml
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import (
    Post, Comment, Like, Error,
    CreatePostRequest, UpdatePostRequest,
    CreateCommentRequest, UpdateCommentRequest,
    LikeRequest, UnlikeRequest
)
from database import (
    init_database, get_db_connection, update_post_counts,
    get_all_posts, get_post_by_id, create_post, update_post, delete_post, post_exists,
    get_comments_by_post_id, get_comment_by_id, create_comment, update_comment, delete_comment, comment_exists,
    get_like, create_like, delete_like, like_exists
)


# Load the OpenAPI specification
def load_openapi_spec():
    """Load the OpenAPI specification from the yaml file"""
    with open("/workspaces/github-copilot-vibe-coding-workshop/openapi.yaml", "r") as file:
        return yaml.safe_load(file)


# Lifespan event for database initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_database()
    yield
    # Shutdown - nothing to clean up


# FastAPI app with custom OpenAPI configuration
app = FastAPI(
    lifespan=lifespan,
    title="Simple Social Media API",
    description="A basic Social Networking Service API that allows users to create, retrieve, update, and delete posts; add comments; and like/unlike posts.",
    version="1.0.0",
    contact={
        "name": "Contoso Team",
        "email": "team@contoso.com"
    },
    servers=[{"url": "http://localhost:8000/api", "description": "Local development server"}],
    docs_url="/docs",
    redoc_url="/redoc"
)

# Override the default OpenAPI schema with our custom one
def custom_openapi():
    """Override FastAPI's default OpenAPI generation"""
    if app.openapi_schema:
        return app.openapi_schema
    
    # Load and return the exact OpenAPI specification from the YAML file
    openapi_schema = load_openapi_spec()
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# API Endpoints
@app.get("/api/posts", response_model=List[Post])
async def list_posts():
    """List all posts"""
    try:
        conn = get_db_connection()
        posts = get_all_posts(conn)
        conn.close()
        
        return [
            Post(
                id=post["id"],
                username=post["username"],
                content=post["content"],
                created_at=post["created_at"],
                updated_at=post["updated_at"],
                like_count=post["like_count"],
                comment_count=post["comment_count"]
            )
            for post in posts
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})


@app.post("/api/posts", response_model=Post, status_code=201)
async def create_post_endpoint(request: CreatePostRequest):
    """Create a new post"""
    try:
        conn = get_db_connection()
        post_id = create_post(request.username, request.content, conn)
        conn.commit()
        
        # Fetch the created post
        post = get_post_by_id(post_id, conn)
        conn.close()
        
        return Post(
            id=post["id"],
            username=post["username"],
            content=post["content"],
            created_at=post["created_at"],
            updated_at=post["updated_at"],
            like_count=post["like_count"],
            comment_count=post["comment_count"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})


@app.get("/api/posts/{post_id}", response_model=Post)
async def get_post(post_id: int):
    """Get a specific post"""
    try:
        conn = get_db_connection()
        post = get_post_by_id(post_id, conn)
        conn.close()
        
        if not post:
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Post not found"})
        
        return Post(
            id=post["id"],
            username=post["username"],
            content=post["content"],
            created_at=post["created_at"],
            updated_at=post["updated_at"],
            like_count=post["like_count"],
            comment_count=post["comment_count"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})


@app.patch("/api/posts/{post_id}", response_model=Post)
async def update_post_endpoint(post_id: int, request: UpdatePostRequest):
    """Update a post"""
    try:
        conn = get_db_connection()
        
        # Check if post exists
        if not post_exists(post_id, conn):
            conn.close()
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Post not found"})
        
        # Update the post
        update_post(post_id, request.username, request.content, conn)
        conn.commit()
        
        # Fetch the updated post
        post = get_post_by_id(post_id, conn)
        conn.close()
        
        return Post(
            id=post["id"],
            username=post["username"],
            content=post["content"],
            created_at=post["created_at"],
            updated_at=post["updated_at"],
            like_count=post["like_count"],
            comment_count=post["comment_count"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})


@app.delete("/api/posts/{post_id}", status_code=204)
async def delete_post_endpoint(post_id: int):
    """Delete a post"""
    try:
        conn = get_db_connection()
        
        # Check if post exists
        if not post_exists(post_id, conn):
            conn.close()
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Post not found"})
        
        # Delete the post and related data
        delete_post(post_id, conn)
        conn.commit()
        conn.close()
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})


@app.get("/api/posts/{post_id}/comments", response_model=List[Comment])
async def list_comments(post_id: int):
    """List comments for a post"""
    try:
        conn = get_db_connection()
        
        # Check if post exists
        if not post_exists(post_id, conn):
            conn.close()
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Post not found"})
        
        # Get comments
        comments = get_comments_by_post_id(post_id, conn)
        conn.close()
        
        return [
            Comment(
                id=comment["id"],
                post_id=comment["post_id"],
                username=comment["username"],
                content=comment["content"],
                created_at=comment["created_at"],
                updated_at=comment["updated_at"]
            )
            for comment in comments
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})


@app.post("/api/posts/{post_id}/comments", response_model=Comment, status_code=201)
async def create_comment_endpoint(post_id: int, request: CreateCommentRequest):
    """Create a comment"""
    try:
        conn = get_db_connection()
        
        # Check if post exists
        if not post_exists(post_id, conn):
            conn.close()
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Post not found"})
        
        # Create comment
        comment_id = create_comment(post_id, request.username, request.content, conn)
        
        # Update post comment count
        update_post_counts(post_id, conn)
        conn.commit()
        
        # Fetch the created comment
        comment = get_comment_by_id(comment_id, post_id, conn)
        conn.close()
        
        return Comment(
            id=comment["id"],
            post_id=comment["post_id"],
            username=comment["username"],
            content=comment["content"],
            created_at=comment["created_at"],
            updated_at=comment["updated_at"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})


@app.get("/api/posts/{post_id}/comments/{comment_id}", response_model=Comment)
async def get_comment(post_id: int, comment_id: int):
    """Get a specific comment"""
    try:
        conn = get_db_connection()
        
        # Check if post exists
        if not post_exists(post_id, conn):
            conn.close()
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Post not found"})
        
        # Get comment
        comment = get_comment_by_id(comment_id, post_id, conn)
        conn.close()
        
        if not comment:
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Comment not found"})
        
        return Comment(
            id=comment["id"],
            post_id=comment["post_id"],
            username=comment["username"],
            content=comment["content"],
            created_at=comment["created_at"],
            updated_at=comment["updated_at"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})


@app.patch("/api/posts/{post_id}/comments/{comment_id}", response_model=Comment)
async def update_comment_endpoint(post_id: int, comment_id: int, request: UpdateCommentRequest):
    """Update a comment"""
    try:
        conn = get_db_connection()
        
        # Check if post exists
        if not post_exists(post_id, conn):
            conn.close()
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Post not found"})
        
        # Check if comment exists
        if not comment_exists(comment_id, post_id, conn):
            conn.close()
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Comment not found"})
        
        # Update the comment
        update_comment(comment_id, post_id, request.username, request.content, conn)
        conn.commit()
        
        # Fetch the updated comment
        comment = get_comment_by_id(comment_id, post_id, conn)
        conn.close()
        
        return Comment(
            id=comment["id"],
            post_id=comment["post_id"],
            username=comment["username"],
            content=comment["content"],
            created_at=comment["created_at"],
            updated_at=comment["updated_at"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})


@app.delete("/api/posts/{post_id}/comments/{comment_id}", status_code=204)
async def delete_comment_endpoint(post_id: int, comment_id: int):
    """Delete a comment"""
    try:
        conn = get_db_connection()
        
        # Check if post exists
        if not post_exists(post_id, conn):
            conn.close()
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Post not found"})
        
        # Check if comment exists
        if not comment_exists(comment_id, post_id, conn):
            conn.close()
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Comment not found"})
        
        # Delete the comment
        delete_comment(comment_id, post_id, conn)
        
        # Update post comment count
        update_post_counts(post_id, conn)
        conn.commit()
        conn.close()
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})


@app.post("/api/posts/{post_id}/likes", response_model=Like, status_code=201)
async def like_post(post_id: int, request: LikeRequest):
    """Like a post"""
    try:
        conn = get_db_connection()
        
        # Check if post exists
        if not post_exists(post_id, conn):
            conn.close()
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Post not found"})
        
        # Check if user already liked this post
        if like_exists(post_id, request.username, conn):
            conn.close()
            raise HTTPException(status_code=400, detail={"error": "ValidationError", "message": "Post already liked by user"})
        
        # Create like
        like_id = create_like(post_id, request.username, conn)
        
        # Update post like count
        update_post_counts(post_id, conn)
        conn.commit()
        
        # Fetch the created like
        like = get_like(post_id, request.username, conn)
        conn.close()
        
        return Like(
            id=like["id"],
            post_id=like["post_id"],
            username=like["username"],
            created_at=like["created_at"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})


@app.delete("/api/posts/{post_id}/likes", status_code=204)
async def unlike_post(post_id: int, request: UnlikeRequest):
    """Unlike a post"""
    try:
        conn = get_db_connection()
        
        # Check if post exists
        if not post_exists(post_id, conn):
            conn.close()
            raise HTTPException(status_code=404, detail={"error": "NotFound", "message": "Post not found"})
        
        # Check if user has liked this post
        if not like_exists(post_id, request.username, conn):
            conn.close()
            raise HTTPException(status_code=400, detail={"error": "ValidationError", "message": "Post not currently liked by user"})
        
        # Delete the like
        delete_like(post_id, request.username, conn)
        
        # Update post like count
        update_post_counts(post_id, conn)
        conn.commit()
        conn.close()
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "InternalServerError", "message": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)