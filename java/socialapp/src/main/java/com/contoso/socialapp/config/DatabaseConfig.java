package com.contoso.socialapp.config;

import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;

/**
 * Configuration for database initialization.
 */
@Configuration
@RequiredArgsConstructor
public class DatabaseConfig {

    private final JdbcTemplate jdbcTemplate;

    /**
     * Initialize database tables on application startup.
     * This ensures the database is always initialized when starting the app.
     */
    @PostConstruct
    public void initializeDatabase() {
        // Drop existing tables to ensure fresh start
        jdbcTemplate.execute("DROP TABLE IF EXISTS likes");
        jdbcTemplate.execute("DROP TABLE IF EXISTS comments");
        jdbcTemplate.execute("DROP TABLE IF EXISTS posts");

        // Create posts table
        jdbcTemplate.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """);

        // Create comments table
        jdbcTemplate.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
            )
        """);

        // Create likes table
        jdbcTemplate.execute("""
            CREATE TABLE IF NOT EXISTS likes (
                post_id TEXT NOT NULL,
                username TEXT NOT NULL,
                liked_at TEXT NOT NULL,
                PRIMARY KEY (post_id, username),
                FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
            )
        """);
    }
}
