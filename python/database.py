"""
Database operations for the FastAPI Social Media API
Handles SQLite database initialization and CRUD operations.
"""
import sqlite3
from datetime import datetime
from typing import List, Optional


DATABASE_URL = "sns_api.db"


def get_db_connection():
    """Get a database connection with row factory for dict-like access"""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    return conn


def init_database():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Create posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            like_count INTEGER DEFAULT 0,
            comment_count INTEGER DEFAULT 0
        )
    """)
    
    # Create comments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    """)
    
    # Create likes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            UNIQUE(post_id, username),
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    """)
    
    conn.commit()
    conn.close()


def get_post_like_count(post_id: int, conn: sqlite3.Connection) -> int:
    """Get the like count for a post"""
    cursor = conn.execute("SELECT COUNT(*) FROM likes WHERE post_id = ?", (post_id,))
    return cursor.fetchone()[0]


def get_post_comment_count(post_id: int, conn: sqlite3.Connection) -> int:
    """Get the comment count for a post"""
    cursor = conn.execute("SELECT COUNT(*) FROM comments WHERE post_id = ?", (post_id,))
    return cursor.fetchone()[0]


def update_post_counts(post_id: int, conn: sqlite3.Connection):
    """Update like_count and comment_count for a post"""
    like_count = get_post_like_count(post_id, conn)
    comment_count = get_post_comment_count(post_id, conn)
    conn.execute(
        "UPDATE posts SET like_count = ?, comment_count = ? WHERE id = ?",
        (like_count, comment_count, post_id)
    )


# Post operations
def get_all_posts(conn: sqlite3.Connection) -> List[sqlite3.Row]:
    """Get all posts ordered by creation date"""
    cursor = conn.execute("""
        SELECT id, username, content, created_at, updated_at, like_count, comment_count
        FROM posts ORDER BY created_at DESC
    """)
    return cursor.fetchall()


def get_post_by_id(post_id: int, conn: sqlite3.Connection) -> Optional[sqlite3.Row]:
    """Get a post by its ID"""
    cursor = conn.execute("""
        SELECT id, username, content, created_at, updated_at, like_count, comment_count
        FROM posts WHERE id = ?
    """, (post_id,))
    return cursor.fetchone()


def create_post(username: str, content: str, conn: sqlite3.Connection) -> int:
    """Create a new post and return its ID"""
    now = datetime.utcnow().isoformat() + "Z"
    cursor = conn.execute("""
        INSERT INTO posts (username, content, created_at, updated_at, like_count, comment_count)
        VALUES (?, ?, ?, ?, 0, 0)
    """, (username, content, now, now))
    return cursor.lastrowid


def update_post(post_id: int, username: str, content: str, conn: sqlite3.Connection):
    """Update an existing post"""
    now = datetime.utcnow().isoformat() + "Z"
    conn.execute("""
        UPDATE posts SET username = ?, content = ?, updated_at = ? WHERE id = ?
    """, (username, content, now, post_id))


def delete_post(post_id: int, conn: sqlite3.Connection):
    """Delete a post and its related comments and likes"""
    # Delete related likes and comments first
    conn.execute("DELETE FROM likes WHERE post_id = ?", (post_id,))
    conn.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
    # Delete the post
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))


def post_exists(post_id: int, conn: sqlite3.Connection) -> bool:
    """Check if a post exists"""
    cursor = conn.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
    return cursor.fetchone() is not None


# Comment operations
def get_comments_by_post_id(post_id: int, conn: sqlite3.Connection) -> List[sqlite3.Row]:
    """Get all comments for a post"""
    cursor = conn.execute("""
        SELECT id, post_id, username, content, created_at, updated_at
        FROM comments WHERE post_id = ? ORDER BY created_at DESC
    """, (post_id,))
    return cursor.fetchall()


def get_comment_by_id(comment_id: int, post_id: int, conn: sqlite3.Connection) -> Optional[sqlite3.Row]:
    """Get a comment by its ID and post ID"""
    cursor = conn.execute("""
        SELECT id, post_id, username, content, created_at, updated_at
        FROM comments WHERE id = ? AND post_id = ?
    """, (comment_id, post_id))
    return cursor.fetchone()


def create_comment(post_id: int, username: str, content: str, conn: sqlite3.Connection) -> int:
    """Create a new comment and return its ID"""
    now = datetime.utcnow().isoformat() + "Z"
    cursor = conn.execute("""
        INSERT INTO comments (post_id, username, content, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, (post_id, username, content, now, now))
    return cursor.lastrowid


def update_comment(comment_id: int, post_id: int, username: str, content: str, conn: sqlite3.Connection):
    """Update an existing comment"""
    now = datetime.utcnow().isoformat() + "Z"
    conn.execute("""
        UPDATE comments SET username = ?, content = ?, updated_at = ? WHERE id = ? AND post_id = ?
    """, (username, content, now, comment_id, post_id))


def delete_comment(comment_id: int, post_id: int, conn: sqlite3.Connection):
    """Delete a comment"""
    conn.execute("DELETE FROM comments WHERE id = ? AND post_id = ?", (comment_id, post_id))


def comment_exists(comment_id: int, post_id: int, conn: sqlite3.Connection) -> bool:
    """Check if a comment exists"""
    cursor = conn.execute("SELECT id FROM comments WHERE id = ? AND post_id = ?", (comment_id, post_id))
    return cursor.fetchone() is not None


# Like operations
def get_like(post_id: int, username: str, conn: sqlite3.Connection) -> Optional[sqlite3.Row]:
    """Get a like by post ID and username"""
    cursor = conn.execute("""
        SELECT id, post_id, username, created_at
        FROM likes WHERE post_id = ? AND username = ?
    """, (post_id, username))
    return cursor.fetchone()


def create_like(post_id: int, username: str, conn: sqlite3.Connection) -> int:
    """Create a new like and return its ID"""
    now = datetime.utcnow().isoformat() + "Z"
    cursor = conn.execute("""
        INSERT INTO likes (post_id, username, created_at)
        VALUES (?, ?, ?)
    """, (post_id, username, now))
    return cursor.lastrowid


def delete_like(post_id: int, username: str, conn: sqlite3.Connection):
    """Delete a like"""
    conn.execute("DELETE FROM likes WHERE post_id = ? AND username = ?", (post_id, username))


def like_exists(post_id: int, username: str, conn: sqlite3.Connection) -> bool:
    """Check if a like exists"""
    cursor = conn.execute("SELECT id FROM likes WHERE post_id = ? AND username = ?", (post_id, username))
    return cursor.fetchone() is not None