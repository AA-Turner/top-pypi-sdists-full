
package com.silabs.utf.QueueModels;

import java.util.ArrayList;
import java.util.List;
import javax.annotation.processing.Generated;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "test_key",
    "status",
    "test_info",
    "test_version",
    "start",
    "finish",
    "comment",
    "executed_by",
    "assignee",
    "steps",
    "iterations",
    "custom_fields"
})
@Generated("jsonschema2pojo")
public class XrayTestExecUpdate {

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_key")
    @NotNull
    private String testKey;
    /**
     * Status for the iteration (examples: PASS, FAIL, SKIP, BLOCK, BROKEN, REGRESSION)
     * (Required)
     * 
     */
    @JsonProperty("status")
    @JsonPropertyDescription("Status for the iteration (examples: PASS, FAIL, SKIP, BLOCK, BROKEN, REGRESSION)")
    @NotNull
    private String status;
    @JsonProperty("test_info")
    @Valid
    private XrayTestInfo testInfo;
    @JsonProperty("test_version")
    private String testVersion;
    @JsonProperty("start")
    private String start;
    @JsonProperty("finish")
    private String finish;
    @JsonProperty("comment")
    private String comment;
    @JsonProperty("executed_by")
    private String executedBy;
    @JsonProperty("assignee")
    private String assignee;
    @JsonProperty("steps")
    @Valid
    private List<XrayStep> steps = new ArrayList<XrayStep>();
    @JsonProperty("iterations")
    @Valid
    private List<XrayIteration> iterations = new ArrayList<XrayIteration>();
    @JsonProperty("custom_fields")
    @Valid
    private List<XrayCustomField> customFields = new ArrayList<XrayCustomField>();

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_key")
    public String getTestKey() {
        return testKey;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_key")
    public void setTestKey(String testKey) {
        this.testKey = testKey;
    }

    public XrayTestExecUpdate withTestKey(String testKey) {
        this.testKey = testKey;
        return this;
    }

    /**
     * Status for the iteration (examples: PASS, FAIL, SKIP, BLOCK, BROKEN, REGRESSION)
     * (Required)
     * 
     */
    @JsonProperty("status")
    public String getStatus() {
        return status;
    }

    /**
     * Status for the iteration (examples: PASS, FAIL, SKIP, BLOCK, BROKEN, REGRESSION)
     * (Required)
     * 
     */
    @JsonProperty("status")
    public void setStatus(String status) {
        this.status = status;
    }

    public XrayTestExecUpdate withStatus(String status) {
        this.status = status;
        return this;
    }

    @JsonProperty("test_info")
    public XrayTestInfo getTestInfo() {
        return testInfo;
    }

    @JsonProperty("test_info")
    public void setTestInfo(XrayTestInfo testInfo) {
        this.testInfo = testInfo;
    }

    public XrayTestExecUpdate withTestInfo(XrayTestInfo testInfo) {
        this.testInfo = testInfo;
        return this;
    }

    @JsonProperty("test_version")
    public String getTestVersion() {
        return testVersion;
    }

    @JsonProperty("test_version")
    public void setTestVersion(String testVersion) {
        this.testVersion = testVersion;
    }

    public XrayTestExecUpdate withTestVersion(String testVersion) {
        this.testVersion = testVersion;
        return this;
    }

    @JsonProperty("start")
    public String getStart() {
        return start;
    }

    @JsonProperty("start")
    public void setStart(String start) {
        this.start = start;
    }

    public XrayTestExecUpdate withStart(String start) {
        this.start = start;
        return this;
    }

    @JsonProperty("finish")
    public String getFinish() {
        return finish;
    }

    @JsonProperty("finish")
    public void setFinish(String finish) {
        this.finish = finish;
    }

    public XrayTestExecUpdate withFinish(String finish) {
        this.finish = finish;
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

    public XrayTestExecUpdate withComment(String comment) {
        this.comment = comment;
        return this;
    }

    @JsonProperty("executed_by")
    public String getExecutedBy() {
        return executedBy;
    }

    @JsonProperty("executed_by")
    public void setExecutedBy(String executedBy) {
        this.executedBy = executedBy;
    }

    public XrayTestExecUpdate withExecutedBy(String executedBy) {
        this.executedBy = executedBy;
        return this;
    }

    @JsonProperty("assignee")
    public String getAssignee() {
        return assignee;
    }

    @JsonProperty("assignee")
    public void setAssignee(String assignee) {
        this.assignee = assignee;
    }

    public XrayTestExecUpdate withAssignee(String assignee) {
        this.assignee = assignee;
        return this;
    }

    @JsonProperty("steps")
    public List<XrayStep> getSteps() {
        return steps;
    }

    @JsonProperty("steps")
    public void setSteps(List<XrayStep> steps) {
        this.steps = steps;
    }

    public XrayTestExecUpdate withSteps(List<XrayStep> steps) {
        this.steps = steps;
        return this;
    }

    @JsonProperty("iterations")
    public List<XrayIteration> getIterations() {
        return iterations;
    }

    @JsonProperty("iterations")
    public void setIterations(List<XrayIteration> iterations) {
        this.iterations = iterations;
    }

    public XrayTestExecUpdate withIterations(List<XrayIteration> iterations) {
        this.iterations = iterations;
        return this;
    }

    @JsonProperty("custom_fields")
    public List<XrayCustomField> getCustomFields() {
        return customFields;
    }

    @JsonProperty("custom_fields")
    public void setCustomFields(List<XrayCustomField> customFields) {
        this.customFields = customFields;
    }

    public XrayTestExecUpdate withCustomFields(List<XrayCustomField> customFields) {
        this.customFields = customFields;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(XrayTestExecUpdate.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("testKey");
        sb.append('=');
        sb.append(((this.testKey == null)?"<null>":this.testKey));
        sb.append(',');
        sb.append("status");
        sb.append('=');
        sb.append(((this.status == null)?"<null>":this.status));
        sb.append(',');
        sb.append("testInfo");
        sb.append('=');
        sb.append(((this.testInfo == null)?"<null>":this.testInfo));
        sb.append(',');
        sb.append("testVersion");
        sb.append('=');
        sb.append(((this.testVersion == null)?"<null>":this.testVersion));
        sb.append(',');
        sb.append("start");
        sb.append('=');
        sb.append(((this.start == null)?"<null>":this.start));
        sb.append(',');
        sb.append("finish");
        sb.append('=');
        sb.append(((this.finish == null)?"<null>":this.finish));
        sb.append(',');
        sb.append("comment");
        sb.append('=');
        sb.append(((this.comment == null)?"<null>":this.comment));
        sb.append(',');
        sb.append("executedBy");
        sb.append('=');
        sb.append(((this.executedBy == null)?"<null>":this.executedBy));
        sb.append(',');
        sb.append("assignee");
        sb.append('=');
        sb.append(((this.assignee == null)?"<null>":this.assignee));
        sb.append(',');
        sb.append("steps");
        sb.append('=');
        sb.append(((this.steps == null)?"<null>":this.steps));
        sb.append(',');
        sb.append("iterations");
        sb.append('=');
        sb.append(((this.iterations == null)?"<null>":this.iterations));
        sb.append(',');
        sb.append("customFields");
        sb.append('=');
        sb.append(((this.customFields == null)?"<null>":this.customFields));
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
        result = ((result* 31)+((this.testInfo == null)? 0 :this.testInfo.hashCode()));
        result = ((result* 31)+((this.executedBy == null)? 0 :this.executedBy.hashCode()));
        result = ((result* 31)+((this.customFields == null)? 0 :this.customFields.hashCode()));
        result = ((result* 31)+((this.testVersion == null)? 0 :this.testVersion.hashCode()));
        result = ((result* 31)+((this.start == null)? 0 :this.start.hashCode()));
        result = ((result* 31)+((this.finish == null)? 0 :this.finish.hashCode()));
        result = ((result* 31)+((this.comment == null)? 0 :this.comment.hashCode()));
        result = ((result* 31)+((this.testKey == null)? 0 :this.testKey.hashCode()));
        result = ((result* 31)+((this.assignee == null)? 0 :this.assignee.hashCode()));
        result = ((result* 31)+((this.steps == null)? 0 :this.steps.hashCode()));
        result = ((result* 31)+((this.iterations == null)? 0 :this.iterations.hashCode()));
        result = ((result* 31)+((this.status == null)? 0 :this.status.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof XrayTestExecUpdate) == false) {
            return false;
        }
        XrayTestExecUpdate rhs = ((XrayTestExecUpdate) other);
        return (((((((((((((this.testInfo == rhs.testInfo)||((this.testInfo!= null)&&this.testInfo.equals(rhs.testInfo)))&&((this.executedBy == rhs.executedBy)||((this.executedBy!= null)&&this.executedBy.equals(rhs.executedBy))))&&((this.customFields == rhs.customFields)||((this.customFields!= null)&&this.customFields.equals(rhs.customFields))))&&((this.testVersion == rhs.testVersion)||((this.testVersion!= null)&&this.testVersion.equals(rhs.testVersion))))&&((this.start == rhs.start)||((this.start!= null)&&this.start.equals(rhs.start))))&&((this.finish == rhs.finish)||((this.finish!= null)&&this.finish.equals(rhs.finish))))&&((this.comment == rhs.comment)||((this.comment!= null)&&this.comment.equals(rhs.comment))))&&((this.testKey == rhs.testKey)||((this.testKey!= null)&&this.testKey.equals(rhs.testKey))))&&((this.assignee == rhs.assignee)||((this.assignee!= null)&&this.assignee.equals(rhs.assignee))))&&((this.steps == rhs.steps)||((this.steps!= null)&&this.steps.equals(rhs.steps))))&&((this.iterations == rhs.iterations)||((this.iterations!= null)&&this.iterations.equals(rhs.iterations))))&&((this.status == rhs.status)||((this.status!= null)&&this.status.equals(rhs.status))));
    }

}
