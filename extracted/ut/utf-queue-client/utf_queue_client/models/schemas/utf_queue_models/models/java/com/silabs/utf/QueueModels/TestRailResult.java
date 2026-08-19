
package com.silabs.utf.QueueModels;

import javax.annotation.processing.Generated;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "id",
    "run_id",
    "status",
    "comment",
    "version",
    "defects",
    "assigned_to_id",
    "custom_props"
})
@Generated("jsonschema2pojo")
public class TestRailResult {

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("id")
    @NotNull
    private String id;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("run_id")
    @NotNull
    private Integer runId;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("status")
    @NotNull
    private String status;
    @JsonProperty("comment")
    private String comment;
    @JsonProperty("version")
    private String version;
    @JsonProperty("defects")
    private String defects;
    @JsonProperty("assigned_to_id")
    private Integer assignedToId;
    @JsonProperty("custom_props")
    @Valid
    private TestResultCustomProps customProps;

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("id")
    public String getId() {
        return id;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("id")
    public void setId(String id) {
        this.id = id;
    }

    public TestRailResult withId(String id) {
        this.id = id;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("run_id")
    public Integer getRunId() {
        return runId;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("run_id")
    public void setRunId(Integer runId) {
        this.runId = runId;
    }

    public TestRailResult withRunId(Integer runId) {
        this.runId = runId;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("status")
    public String getStatus() {
        return status;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("status")
    public void setStatus(String status) {
        this.status = status;
    }

    public TestRailResult withStatus(String status) {
        this.status = status;
        return this;
    }

    @JsonProperty("comment")
    public String getComment() {
        return comment;
    }

    @JsonProperty("comment")
    public void setComment(String comment) {
        this.comment = comment;
    }

    public TestRailResult withComment(String comment) {
        this.comment = comment;
        return this;
    }

    @JsonProperty("version")
    public String getVersion() {
        return version;
    }

    @JsonProperty("version")
    public void setVersion(String version) {
        this.version = version;
    }

    public TestRailResult withVersion(String version) {
        this.version = version;
        return this;
    }

    @JsonProperty("defects")
    public String getDefects() {
        return defects;
    }

    @JsonProperty("defects")
    public void setDefects(String defects) {
        this.defects = defects;
    }

    public TestRailResult withDefects(String defects) {
        this.defects = defects;
        return this;
    }

    @JsonProperty("assigned_to_id")
    public Integer getAssignedToId() {
        return assignedToId;
    }

    @JsonProperty("assigned_to_id")
    public void setAssignedToId(Integer assignedToId) {
        this.assignedToId = assignedToId;
    }

    public TestRailResult withAssignedToId(Integer assignedToId) {
        this.assignedToId = assignedToId;
        return this;
    }

    @JsonProperty("custom_props")
    public TestResultCustomProps getCustomProps() {
        return customProps;
    }

    @JsonProperty("custom_props")
    public void setCustomProps(TestResultCustomProps customProps) {
        this.customProps = customProps;
    }

    public TestRailResult withCustomProps(TestResultCustomProps customProps) {
        this.customProps = customProps;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(TestRailResult.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("id");
        sb.append('=');
        sb.append(((this.id == null)?"<null>":this.id));
        sb.append(',');
        sb.append("runId");
        sb.append('=');
        sb.append(((this.runId == null)?"<null>":this.runId));
        sb.append(',');
        sb.append("status");
        sb.append('=');
        sb.append(((this.status == null)?"<null>":this.status));
        sb.append(',');
        sb.append("comment");
        sb.append('=');
        sb.append(((this.comment == null)?"<null>":this.comment));
        sb.append(',');
        sb.append("version");
        sb.append('=');
        sb.append(((this.version == null)?"<null>":this.version));
        sb.append(',');
        sb.append("defects");
        sb.append('=');
        sb.append(((this.defects == null)?"<null>":this.defects));
        sb.append(',');
        sb.append("assignedToId");
        sb.append('=');
        sb.append(((this.assignedToId == null)?"<null>":this.assignedToId));
        sb.append(',');
        sb.append("customProps");
        sb.append('=');
        sb.append(((this.customProps == null)?"<null>":this.customProps));
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
        result = ((result* 31)+((this.assignedToId == null)? 0 :this.assignedToId.hashCode()));
        result = ((result* 31)+((this.defects == null)? 0 :this.defects.hashCode()));
        result = ((result* 31)+((this.customProps == null)? 0 :this.customProps.hashCode()));
        result = ((result* 31)+((this.comment == null)? 0 :this.comment.hashCode()));
        result = ((result* 31)+((this.id == null)? 0 :this.id.hashCode()));
        result = ((result* 31)+((this.runId == null)? 0 :this.runId.hashCode()));
        result = ((result* 31)+((this.version == null)? 0 :this.version.hashCode()));
        result = ((result* 31)+((this.status == null)? 0 :this.status.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof TestRailResult) == false) {
            return false;
        }
        TestRailResult rhs = ((TestRailResult) other);
        return (((((((((this.assignedToId == rhs.assignedToId)||((this.assignedToId!= null)&&this.assignedToId.equals(rhs.assignedToId)))&&((this.defects == rhs.defects)||((this.defects!= null)&&this.defects.equals(rhs.defects))))&&((this.customProps == rhs.customProps)||((this.customProps!= null)&&this.customProps.equals(rhs.customProps))))&&((this.comment == rhs.comment)||((this.comment!= null)&&this.comment.equals(rhs.comment))))&&((this.id == rhs.id)||((this.id!= null)&&this.id.equals(rhs.id))))&&((this.runId == rhs.runId)||((this.runId!= null)&&this.runId.equals(rhs.runId))))&&((this.version == rhs.version)||((this.version!= null)&&this.version.equals(rhs.version))))&&((this.status == rhs.status)||((this.status!= null)&&this.status.equals(rhs.status))));
    }

}
