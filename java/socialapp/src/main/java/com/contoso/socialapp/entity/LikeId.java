package com.contoso.socialapp.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * Composite primary key for Like entity.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class LikeId implements Serializable {
    
    private String postId;
    private String username;
}
