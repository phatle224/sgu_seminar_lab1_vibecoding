package com.contoso.socialapp.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.UUID;

/**
 * Post entity representing a social media post.
 */
@Entity
@Table(name = "posts")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Post {

    @Id
    @Column(name = "id", nullable = false)
    private String id;

    @Column(name = "username", nullable = false, length = 50)
    private String username;

    @Column(name = "content", nullable = false, length = 1000)
    private String content;

    @Column(name = "created_at", nullable = false)
    private String createdAt;

    @Column(name = "updated_at", nullable = false)
    private String updatedAt;

    /**
     * Generate a new Post with UUID and timestamps.
     */
    @PrePersist
    public void prePersist() {
        if (id == null) {
            id = UUID.randomUUID().toString();
        }
        String now = Instant.now().toString();
        if (createdAt == null) {
            createdAt = now;
        }
        updatedAt = now;
    }

    /**
     * Update timestamp before update.
     */
    @PreUpdate
    public void preUpdate() {
        updatedAt = Instant.now().toString();
    }
}
