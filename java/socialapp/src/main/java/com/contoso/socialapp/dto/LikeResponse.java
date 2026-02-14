package com.contoso.socialapp.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Response DTO for Like operation.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LikeResponse {

    @JsonProperty("postId")
    private String postId;

    @JsonProperty("username")
    private String username;

    @JsonProperty("likesCount")
    private long likesCount;
}
