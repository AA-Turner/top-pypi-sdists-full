
package com.silabs.utf.QueueModels;

import javax.annotation.processing.Generated;
import javax.validation.constraints.NotNull;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "name",
    "extension",
    "metadata",
    "base64Content",
    "validateMetadata"
})
@Generated("jsonschema2pojo")
public class ArtifactUploadRequest {

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("name")
    @NotNull
    private String name;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("extension")
    @NotNull
    private String extension;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("metadata")
    @NotNull
    private Object metadata;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("base64Content")
    @NotNull
    private String base64Content;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("validateMetadata")
    @NotNull
    private Boolean validateMetadata;

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("name")
    public String getName() {
        return name;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("name")
    public void setName(String name) {
        this.name = name;
    }

    public ArtifactUploadRequest withName(String name) {
        this.name = name;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("extension")
    public String getExtension() {
        return extension;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("extension")
    public void setExtension(String extension) {
        this.extension = extension;
    }

    public ArtifactUploadRequest withExtension(String extension) {
        this.extension = extension;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("metadata")
    public Object getMetadata() {
        return metadata;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("metadata")
    public void setMetadata(Object metadata) {
        this.metadata = metadata;
    }

    public ArtifactUploadRequest withMetadata(Object metadata) {
        this.metadata = metadata;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("base64Content")
    public String getBase64Content() {
        return base64Content;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("base64Content")
    public void setBase64Content(String base64Content) {
        this.base64Content = base64Content;
    }

    public ArtifactUploadRequest withBase64Content(String base64Content) {
        this.base64Content = base64Content;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("validateMetadata")
    public Boolean getValidateMetadata() {
        return validateMetadata;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("validateMetadata")
    public void setValidateMetadata(Boolean validateMetadata) {
        this.validateMetadata = validateMetadata;
    }

    public ArtifactUploadRequest withValidateMetadata(Boolean validateMetadata) {
        this.validateMetadata = validateMetadata;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(ArtifactUploadRequest.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("name");
        sb.append('=');
        sb.append(((this.name == null)?"<null>":this.name));
        sb.append(',');
        sb.append("extension");
        sb.append('=');
        sb.append(((this.extension == null)?"<null>":this.extension));
        sb.append(',');
        sb.append("metadata");
        sb.append('=');
        sb.append(((this.metadata == null)?"<null>":this.metadata));
        sb.append(',');
        sb.append("base64Content");
        sb.append('=');
        sb.append(((this.base64Content == null)?"<null>":this.base64Content));
        sb.append(',');
        sb.append("validateMetadata");
        sb.append('=');
        sb.append(((this.validateMetadata == null)?"<null>":this.validateMetadata));
        sb.append(',');
        if (sb.charAt((sb.length()- 1)) == ',') {
            sb.setCharAt((sb.length()- 1), ']');
        } else {
            sb.append(']');
        }
        return sb.toString();
    }

    @Override
    public int hashCode() {
        int result = 1;
        result = ((result* 31)+((this.name == null)? 0 :this.name.hashCode()));
        result = ((result* 31)+((this.base64Content == null)? 0 :this.base64Content.hashCode()));
        result = ((result* 31)+((this.extension == null)? 0 :this.extension.hashCode()));
        result = ((result* 31)+((this.metadata == null)? 0 :this.metadata.hashCode()));
        result = ((result* 31)+((this.validateMetadata == null)? 0 :this.validateMetadata.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof ArtifactUploadRequest) == false) {
            return false;
        }
        ArtifactUploadRequest rhs = ((ArtifactUploadRequest) other);
        return ((((((this.name == rhs.name)||((this.name!= null)&&this.name.equals(rhs.name)))&&((this.base64Content == rhs.base64Content)||((this.base64Content!= null)&&this.base64Content.equals(rhs.base64Content))))&&((this.extension == rhs.extension)||((this.extension!= null)&&this.extension.equals(rhs.extension))))&&((this.metadata == rhs.metadata)||((this.metadata!= null)&&this.metadata.equals(rhs.metadata))))&&((this.validateMetadata == rhs.validateMetadata)||((this.validateMetadata!= null)&&this.validateMetadata.equals(rhs.validateMetadata))));
    }

}
