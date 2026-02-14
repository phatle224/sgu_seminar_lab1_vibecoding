package com.contoso.socialapp.service;

import com.contoso.socialapp.dto.CreatePostRequest;
import com.contoso.socialapp.dto.PostResponse;
import com.contoso.socialapp.dto.UpdatePostRequest;
import com.contoso.socialapp.entity.Post;
import com.contoso.socialapp.exception.ResourceNotFoundException;
import com.contoso.socialapp.repository.CommentRepository;
import com.contoso.socialapp.repository.LikeRepository;
import com.contoso.socialapp.repository.PostRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * Service for managing posts.
 */
@Service
@RequiredArgsConstructor
public class PostService {

    private final PostRepository postRepository;
    private final LikeRepository likeRepository;

    /**
     * Get all posts ordered by creation date descending.
     */
    @Transactional(readOnly = true)
    public List<PostResponse> getAllPosts() {
        return postRepository.findAll().stream()
                .map(this::toPostResponse)
                .sorted((p1, p2) -> p2.getCreatedAt().compareTo(p1.getCreatedAt()))
                .collect(Collectors.toList());
    }

    /**
     * Get a post by ID.
     */
    @Transactional(readOnly = true)
    public PostResponse getPostById(String postId) {
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ResourceNotFoundException("Post not found"));
        return toPostResponse(post);
    }

    /**
     * Create a new post.
     */
    @Transactional
    public PostResponse createPost(CreatePostRequest request) {
        Post post = new Post();
        post.setId(UUID.randomUUID().toString());
        post.setUsername(request.getUsername());
        post.setContent(request.getContent());
        String now = Instant.now().toString();
        post.setCreatedAt(now);
        post.setUpdatedAt(now);

        post = postRepository.save(post);
        return toPostResponse(post);
    }

    /**
     * Update an existing post.
     */
    @Transactional
    public PostResponse updatePost(String postId, UpdatePostRequest request) {
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ResourceNotFoundException("Post not found or you don't have permission to update it"));

        // Verify username matches (simple authorization)
        if (!post.getUsername().equals(request.getUsername())) {
            throw new ResourceNotFoundException("Post not found or you don't have permission to update it");
        }

        post.setContent(request.getContent());
        post.setUpdatedAt(Instant.now().toString());

        post = postRepository.save(post);
        return toPostResponse(post);
    }

    /**
     * Delete a post by ID.
     */
    @Transactional
    public void deletePost(String postId) {
        if (!postRepository.existsById(postId)) {
            throw new ResourceNotFoundException("Post not found");
        }
        postRepository.deleteById(postId);
    }

    /**
     * Convert Post entity to PostResponse DTO.
     */
    private PostResponse toPostResponse(Post post) {
        long likesCount = likeRepository.countByPostId(post.getId());

        return PostResponse.builder()
                .id(post.getId())
                .username(post.getUsername())
                .content(post.getContent())
                .createdAt(post.getCreatedAt())
                .updatedAt(post.getUpdatedAt())
                .likesCount(likesCount)
                .build();
    }
}
