package com.contoso.socialapp.service;

import com.contoso.socialapp.dto.LikeRequest;
import com.contoso.socialapp.dto.LikeResponse;
import com.contoso.socialapp.entity.Like;
import com.contoso.socialapp.exception.ResourceNotFoundException;
import com.contoso.socialapp.exception.ValidationException;
import com.contoso.socialapp.repository.LikeRepository;
import com.contoso.socialapp.repository.PostRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;

/**
 * Service for managing likes.
 */
@Service
@RequiredArgsConstructor
public class LikeService {

    private final LikeRepository likeRepository;
    private final PostRepository postRepository;

    /**
     * Add a like to a post.
     */
    @Transactional
    public LikeResponse likePost(String postId, LikeRequest request) {
        // Check if post exists
        if (!postRepository.existsById(postId)) {
            throw new ResourceNotFoundException("Post not found");
        }

        // Check if already liked
        if (likeRepository.existsByPostIdAndUsername(postId, request.getUsername())) {
            throw new ValidationException("Post already liked by this user");
        }

        Like like = new Like();
        like.setPostId(postId);
        like.setUsername(request.getUsername());
        like.setLikedAt(Instant.now().toString());

        likeRepository.save(like);

        long likesCount = likeRepository.countByPostId(postId);

        return LikeResponse.builder()
                .postId(postId)
                .username(request.getUsername())
                .likesCount(likesCount)
                .build();
    }

    /**
     * Remove a like from a post.
     */
    @Transactional
    public void unlikePost(String postId, String username) {
        if (!likeRepository.existsByPostIdAndUsername(postId, username)) {
            throw new ResourceNotFoundException("Like not found");
        }

        likeRepository.deleteByPostIdAndUsername(postId, username);
    }
}
