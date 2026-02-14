package com.contoso.socialapp.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

/**
 * Like entity representing a like on a post.
 */
@Entity
@Table(name = "likes")
@IdClass(LikeId.class)
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Like {

    @Id
    @Column(name = "post_id", nullable = false)
    private String postId;

    @Id
    @Column(name = "username", nullable = false, length = 50)
    private String username;

    @Column(name = "liked_at", nullable = false)
    private String likedAt;

    /**
     * Set likedAt timestamp before persist.
     */
    @PrePersist
    public void prePersist() {
        if (likedAt == null) {
            likedAt = Instant.now().toString();
        }
    }
}
