
package com.silabs.utf.QueueModels;

import java.util.ArrayList;
import java.util.List;
import javax.annotation.processing.Generated;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "project_key",
    "summary",
    "description",
    "test_type",
    "requirement_keys",
    "labels",
    "steps"
})
@Generated("jsonschema2pojo")
public class XrayTestInfo {

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("project_key")
    @NotNull
    private String projectKey;
    @JsonProperty("summary")
    private String summary;
    @JsonProperty("description")
    private String description;
    @JsonProperty("test_type")
    private String testType;
    @JsonProperty("requirement_keys")
    @Valid
    private List<String> requirementKeys = new ArrayList<String>();
    @JsonProperty("labels")
    @Valid
    private List<String> labels = new ArrayList<String>();
    @JsonProperty("steps")
    @Valid
    private List<XrayStep> steps = new ArrayList<XrayStep>();

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("project_key")
    public String getProjectKey() {
        return projectKey;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("project_key")
    public void setProjectKey(String projectKey) {
        this.projectKey = projectKey;
    }

    public XrayTestInfo withProjectKey(String projectKey) {
        this.projectKey = projectKey;
        return this;
    }

    @JsonProperty("summary")
    public String getSummary() {
        return summary;
    }

    @JsonProperty("summary")
    public void setSummary(String summary) {
        this.summary = summary;
    }

    public XrayTestInfo withSummary(String summary) {
        this.summary = summary;
        return this;
    }

    @JsonProperty("description")
    public String getDescription() {
        return description;
    }

    @JsonProperty("description")
    public void setDescription(String description) {
        this.description = description;
    }

    public XrayTestInfo withDescription(String description) {
        this.description = description;
        return this;
    }

    @JsonProperty("test_type")
    public String getTestType() {
        return testType;
    }

    @JsonProperty("test_type")
    public void setTestType(String testType) {
        this.testType = testType;
    }

    public XrayTestInfo withTestType(String testType) {
        this.testType = testType;
        return this;
    }

    @JsonProperty("requirement_keys")
    public List<String> getRequirementKeys() {
        return requirementKeys;
    }

    @JsonProperty("requirement_keys")
    public void setRequirementKeys(List<String> requirementKeys) {
        this.requirementKeys = requirementKeys;
    }

    public XrayTestInfo withRequirementKeys(List<String> requirementKeys) {
        this.requirementKeys = requirementKeys;
        return this;
    }

    @JsonProperty("labels")
    public List<String> getLabels() {
        return labels;
    }

    @JsonProperty("labels")
    public void setLabels(List<String> labels) {
        this.labels = labels;
    }

    public XrayTestInfo withLabels(List<String> labels) {
        this.labels = labels;
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

    public XrayTestInfo withSteps(List<XrayStep> steps) {
        this.steps = steps;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(XrayTestInfo.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("projectKey");
        sb.append('=');
        sb.append(((this.projectKey == null)?"<null>":this.projectKey));
        sb.append(',');
        sb.append("summary");
        sb.append('=');
        sb.append(((this.summary == null)?"<null>":this.summary));
        sb.append(',');
        sb.append("description");
        sb.append('=');
        sb.append(((this.description == null)?"<null>":this.description));
        sb.append(',');
        sb.append("testType");
        sb.append('=');
        sb.append(((this.testType == null)?"<null>":this.testType));
        sb.append(',');
        sb.append("requirementKeys");
        sb.append('=');
        sb.append(((this.requirementKeys == null)?"<null>":this.requirementKeys));
        sb.append(',');
        sb.append("labels");
        sb.append('=');
        sb.append(((this.labels == null)?"<null>":this.labels));
        sb.append(',');
        sb.append("steps");
        sb.append('=');
        sb.append(((this.steps == null)?"<null>":this.steps));
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
        result = ((result* 31)+((this.summary == null)? 0 :this.summary.hashCode()));
        result = ((result* 31)+((this.projectKey == null)? 0 :this.projectKey.hashCode()));
        result = ((result* 31)+((this.description == null)? 0 :this.description.hashCode()));
        result = ((result* 31)+((this.testType == null)? 0 :this.testType.hashCode()));
        result = ((result* 31)+((this.requirementKeys == null)? 0 :this.requirementKeys.hashCode()));
        result = ((result* 31)+((this.steps == null)? 0 :this.steps.hashCode()));
        result = ((result* 31)+((this.labels == null)? 0 :this.labels.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof XrayTestInfo) == false) {
            return false;
        }
        XrayTestInfo rhs = ((XrayTestInfo) other);
        return ((((((((this.summary == rhs.summary)||((this.summary!= null)&&this.summary.equals(rhs.summary)))&&((this.projectKey == rhs.projectKey)||((this.projectKey!= null)&&this.projectKey.equals(rhs.projectKey))))&&((this.description == rhs.description)||((this.description!= null)&&this.description.equals(rhs.description))))&&((this.testType == rhs.testType)||((this.testType!= null)&&this.testType.equals(rhs.testType))))&&((this.requirementKeys == rhs.requirementKeys)||((this.requirementKeys!= null)&&this.requirementKeys.equals(rhs.requirementKeys))))&&((this.steps == rhs.steps)||((this.steps!= null)&&this.steps.equals(rhs.steps))))&&((this.labels == rhs.labels)||((this.labels!= null)&&this.labels.equals(rhs.labels))));
    }

}
