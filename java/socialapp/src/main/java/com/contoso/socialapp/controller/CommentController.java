package com.contoso.socialapp.controller;

import com.contoso.socialapp.dto.CommentResponse;
import com.contoso.socialapp.dto.CreateCommentRequest;
import com.contoso.socialapp.dto.UpdateCommentRequest;
import com.contoso.socialapp.service.CommentService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST controller for comment management operations.
 */
@RestController
@RequestMapping("/api/posts/{postId}/comments")
@RequiredArgsConstructor
@Tag(name = "Comments", description = "Operations related to comment management")
public class CommentController {

    private final CommentService commentService;

    @GetMapping
    @Operation(summary = "List all comments for a post", description = "Read all the comments on a specific post")
    public ResponseEntity<List<CommentResponse>> getCommentsByPostId(@PathVariable String postId) {
        return ResponseEntity.ok(commentService.getCommentsByPostId(postId));
    }

    @PostMapping
    @Operation(summary = "Create a comment on a post", description = "Comment on a post to share your thoughts")
    public ResponseEntity<CommentResponse> createComment(
            @PathVariable String postId,
            @Valid @RequestBody CreateCommentRequest request) {
        CommentResponse response = commentService.createComment(postId, request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/{commentId}")
    @Operation(summary = "Get a specific comment", description = "See a specific comment in detail")
    public ResponseEntity<CommentResponse> getCommentById(
            @PathVariable String postId,
            @PathVariable String commentId) {
        return ResponseEntity.ok(commentService.getCommentById(postId, commentId));
    }

    @PatchMapping("/{commentId}")
    @Operation(summary = "Update a comment", description = "Correct or revise your comment")
    public ResponseEntity<CommentResponse> updateComment(
            @PathVariable String postId,
            @PathVariable String commentId,
            @Valid @RequestBody UpdateCommentRequest request) {
        return ResponseEntity.ok(commentService.updateComment(postId, commentId, request));
    }

    @DeleteMapping("/{commentId}")
    @Operation(summary = "Delete a comment", description = "Delete your comment if necessary")
    public ResponseEntity<Void> deleteComment(
            @PathVariable String postId,
            @PathVariable String commentId) {
        commentService.deleteComment(postId, commentId);
        return ResponseEntity.noContent().build();
    }
}
