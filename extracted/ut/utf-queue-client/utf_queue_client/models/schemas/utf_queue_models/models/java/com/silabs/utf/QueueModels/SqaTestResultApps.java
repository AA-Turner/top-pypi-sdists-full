
package com.silabs.utf.QueueModels;

import javax.annotation.processing.Generated;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "test_case_uuid",
    "artifact_id"
})
@Generated("jsonschema2pojo")
public class SqaTestResultApps extends QueueRecord {

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_case_uuid")
    @Size(max = 36)
    @NotNull
    private String testCaseUuid;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("artifact_id")
    @Size(max = 36)
    @NotNull
    private String artifactId;

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_case_uuid")
    public String getTestCaseUuid() {
        return testCaseUuid;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_case_uuid")
    public void setTestCaseUuid(String testCaseUuid) {
        this.testCaseUuid = testCaseUuid;
    }

    public SqaTestResultApps withTestCaseUuid(String testCaseUuid) {
        this.testCaseUuid = testCaseUuid;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("artifact_id")
    public String getArtifactId() {
        return artifactId;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("artifact_id")
    public void setArtifactId(String artifactId) {
        this.artifactId = artifactId;
    }

    public SqaTestResultApps withArtifactId(String artifactId) {
        this.artifactId = artifactId;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(SqaTestResultApps.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("testCaseUuid");
        sb.append('=');
        sb.append(((this.testCaseUuid == null)?"<null>":this.testCaseUuid));
        sb.append(',');
        sb.append("artifactId");
        sb.append('=');
        sb.append(((this.artifactId == null)?"<null>":this.artifactId));
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
        result = ((result* 31)+((this.testCaseUuid == null)? 0 :this.testCaseUuid.hashCode()));
        result = ((result* 31)+((this.artifactId == null)? 0 :this.artifactId.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof SqaTestResultApps) == false) {
            return false;
        }
        SqaTestResultApps rhs = ((SqaTestResultApps) other);
        return (((this.testCaseUuid == rhs.testCaseUuid)||((this.testCaseUuid!= null)&&this.testCaseUuid.equals(rhs.testCaseUuid)))&&((this.artifactId == rhs.artifactId)||((this.artifactId!= null)&&this.artifactId.equals(rhs.artifactId))));
    }

}
