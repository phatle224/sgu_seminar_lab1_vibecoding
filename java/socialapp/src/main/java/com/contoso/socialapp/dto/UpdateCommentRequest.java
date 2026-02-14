package com.contoso.socialapp.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request DTO for updating an existing comment.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class UpdateCommentRequest {

    @NotBlank(message = "Username is required")
    @Size(min = 1, max = 50, message = "Username must be between 1 and 50 characters")
    @JsonProperty("username")
    private String username;

    @NotBlank(message = "Content is required")
    @Size(min = 1, max = 500, message = "Content must be between 1 and 500 characters")
    @JsonProperty("content")
    private String content;
}
