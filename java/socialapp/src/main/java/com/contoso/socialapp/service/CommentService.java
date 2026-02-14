package com.contoso.socialapp.service;

import com.contoso.socialapp.dto.CommentResponse;
import com.contoso.socialapp.dto.CreateCommentRequest;
import com.contoso.socialapp.dto.UpdateCommentRequest;
import com.contoso.socialapp.entity.Comment;
import com.contoso.socialapp.exception.ResourceNotFoundException;
import com.contoso.socialapp.repository.CommentRepository;
import com.contoso.socialapp.repository.PostRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * Service for managing comments.
 */
@Service
@RequiredArgsConstructor
public class CommentService {

    private final CommentRepository commentRepository;
    private final PostRepository postRepository;

    /**
     * Get all comments for a post.
     */
    @Transactional(readOnly = true)
    public List<CommentResponse> getCommentsByPostId(String postId) {
        // Check if post exists
        if (!postRepository.existsById(postId)) {
            throw new ResourceNotFoundException("Post not found");
        }

        return commentRepository.findByPostIdOrderByCreatedAtAsc(postId).stream()
                .map(this::toCommentResponse)
                .collect(Collectors.toList());
    }

    /**
     * Get a specific comment by ID.
     */
    @Transactional(readOnly = true)
    public CommentResponse getCommentById(String postId, String commentId) {
        Comment comment = commentRepository.findByIdAndPostId(commentId, postId)
                .orElseThrow(() -> new ResourceNotFoundException("Comment not found"));
        return toCommentResponse(comment);
    }

    /**
     * Create a new comment.
     */
    @Transactional
    public CommentResponse createComment(String postId, CreateCommentRequest request) {
        // Check if post exists
        if (!postRepository.existsById(postId)) {
            throw new ResourceNotFoundException("Post not found");
        }

        Comment comment = new Comment();
        comment.setId(UUID.randomUUID().toString());
        comment.setPostId(postId);
        comment.setUsername(request.getUsername());
        comment.setContent(request.getContent());
        String now = Instant.now().toString();
        comment.setCreatedAt(now);
        comment.setUpdatedAt(now);

        comment = commentRepository.save(comment);
        return toCommentResponse(comment);
    }

    /**
     * Update an existing comment.
     */
    @Transactional
    public CommentResponse updateComment(String postId, String commentId, UpdateCommentRequest request) {
        Comment comment = commentRepository.findByIdAndPostId(commentId, postId)
                .orElseThrow(() -> new ResourceNotFoundException("Comment not found or you don't have permission to update it"));

        // Verify username matches (simple authorization)
        if (!comment.getUsername().equals(request.getUsername())) {
            throw new ResourceNotFoundException("Comment not found or you don't have permission to update it");
        }

        comment.setContent(request.getContent());
        comment.setUpdatedAt(Instant.now().toString());

        comment = commentRepository.save(comment);
        return toCommentResponse(comment);
    }

    /**
     * Delete a comment.
     */
    @Transactional
    public void deleteComment(String postId, String commentId) {
        Comment comment = commentRepository.findByIdAndPostId(commentId, postId)
                .orElseThrow(() -> new ResourceNotFoundException("Comment not found"));

        commentRepository.deleteById(commentId);
    }

    /**
     * Convert Comment entity to CommentResponse DTO.
     */
    private CommentResponse toCommentResponse(Comment comment) {
        return CommentResponse.builder()
                .id(comment.getId())
                .postId(comment.getPostId())
                .username(comment.getUsername())
                .content(comment.getContent())
                .createdAt(comment.getCreatedAt())
                .updatedAt(comment.getUpdatedAt())
                .build();
    }
}
