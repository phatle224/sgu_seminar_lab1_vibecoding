"""
Pydantic models for the FastAPI Social Media API
These models match the OpenAPI specification exactly.
"""
from typing import Optional
from pydantic import BaseModel


class Post(BaseModel):
    """Post model matching the OpenAPI specification"""
    id: int
    username: str
    content: str
    created_at: str
    updated_at: str
    like_count: int
    comment_count: int

    class Config:
        from_attributes = True


class Comment(BaseModel):
    """Comment model matching the OpenAPI specification"""
    id: int
    post_id: int
    username: str
    content: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class Like(BaseModel):
    """Like model matching the OpenAPI specification"""
    id: int
    post_id: int
    username: str
    created_at: str

    class Config:
        from_attributes = True


# Request models
class CreatePostRequest(BaseModel):
    """Request model for creating a new post"""
    username: str
    content: str


class UpdatePostRequest(BaseModel):
    """Request model for updating an existing post"""
    username: str
    content: str


class CreateCommentRequest(BaseModel):
    """Request model for creating a new comment"""
    username: str
    content: str


class UpdateCommentRequest(BaseModel):
    """Request model for updating an existing comment"""
    username: str
    content: str


class LikeRequest(BaseModel):
    """Request model for liking a post"""
    username: str


class UnlikeRequest(BaseModel):
    """Request model for unliking a post"""
    username: str


# Error response model
class Error(BaseModel):
    """Error response model matching the OpenAPI specification"""
    error: str
    message: str
    details: Optional[dict] = None