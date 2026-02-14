package com.contoso.socialapp.repository;

import com.contoso.socialapp.entity.Like;
import com.contoso.socialapp.entity.LikeId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Repository interface for Like entity.
 */
@Repository
public interface LikeRepository extends JpaRepository<Like, LikeId> {
    
    /**
     * Count likes by post ID.
     */
    long countByPostId(String postId);
    
    /**
     * Check if a like exists for a post by a user.
     */
    boolean existsByPostIdAndUsername(String postId, String username);
    
    /**
     * Delete a like by post ID and username.
     */
    void deleteByPostIdAndUsername(String postId, String username);
}
