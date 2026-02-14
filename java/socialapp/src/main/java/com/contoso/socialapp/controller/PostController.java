package com.contoso.socialapp.controller;

import com.contoso.socialapp.dto.CreatePostRequest;
import com.contoso.socialapp.dto.PostResponse;
import com.contoso.socialapp.dto.UpdatePostRequest;
import com.contoso.socialapp.service.PostService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST controller for post management operations.
 */
@RestController
@RequestMapping("/api/posts")
@RequiredArgsConstructor
@Tag(name = "Posts", description = "Operations related to post management")
public class PostController {

    private final PostService postService;

    @GetMapping
    @Operation(summary = "List all posts", description = "Retrieve all recent posts to browse what others are sharing")
    public ResponseEntity<List<PostResponse>> getAllPosts() {
        return ResponseEntity.ok(postService.getAllPosts());
    }

    @PostMapping
    @Operation(summary = "Create a new post", description = "Create a new post to share content with others")
    public ResponseEntity<PostResponse> createPost(@Valid @RequestBody CreatePostRequest request) {
        PostResponse response = postService.createPost(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/{postId}")
    @Operation(summary = "Get a specific post", description = "Read a specific post in detail")
    public ResponseEntity<PostResponse> getPostById(@PathVariable String postId) {
        return ResponseEntity.ok(postService.getPostById(postId));
    }

    @PatchMapping("/{postId}")
    @Operation(summary = "Update a post", description = "Update an existing post to correct mistakes or add information")
    public ResponseEntity<PostResponse> updatePost(
            @PathVariable String postId,
            @Valid @RequestBody UpdatePostRequest request) {
        return ResponseEntity.ok(postService.updatePost(postId, request));
    }

    @DeleteMapping("/{postId}")
    @Operation(summary = "Delete a post", description = "Delete a post if you no longer want it shared")
    public ResponseEntity<Void> deletePost(@PathVariable String postId) {
        postService.deletePost(postId);
        return ResponseEntity.noContent().build();
    }
}
