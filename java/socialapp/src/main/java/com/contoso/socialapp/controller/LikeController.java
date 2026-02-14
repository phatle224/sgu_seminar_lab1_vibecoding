package com.contoso.socialapp.controller;

import com.contoso.socialapp.dto.LikeRequest;
import com.contoso.socialapp.dto.LikeResponse;
import com.contoso.socialapp.service.LikeService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * REST controller for like management operations.
 */
@RestController
@RequestMapping("/api/posts/{postId}/likes")
@RequiredArgsConstructor
@Tag(name = "Likes", description = "Operations related to post likes")
public class LikeController {

    private final LikeService likeService;

    @PostMapping
    @Operation(summary = "Like a post", description = "Like a post to show appreciation")
    public ResponseEntity<LikeResponse> likePost(
            @PathVariable String postId,
            @Valid @RequestBody LikeRequest request) {
        LikeResponse response = likeService.likePost(postId, request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @DeleteMapping
    @Operation(summary = "Unlike a post", description = "Remove your like if you change your mind")
    public ResponseEntity<Void> unlikePost(
            @PathVariable String postId,
            @RequestParam String username) {
        likeService.unlikePost(postId, username);
        return ResponseEntity.noContent().build();
    }
}
