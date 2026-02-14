package com.contoso.socialapp.repository;

import com.contoso.socialapp.entity.Comment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * Repository interface for Comment entity.
 */
@Repository
public interface CommentRepository extends JpaRepository<Comment, String> {
    
    /**
     * Find all comments by post ID, ordered by creation date.
     */
    List<Comment> findByPostIdOrderByCreatedAtAsc(String postId);
    
    /**
     * Find a comment by ID and post ID.
     */
    Optional<Comment> findByIdAndPostId(String id, String postId);
    
    /**
     * Delete a comment by ID and post ID.
     */
    void deleteByIdAndPostId(String id, String postId);
    
    /**
     * Count comments by post ID.
     */
    long countByPostId(String postId);
}
