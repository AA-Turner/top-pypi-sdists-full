
package com.silabs.utf.QueueModels;

import java.util.ArrayList;
import java.util.List;
import javax.annotation.processing.Generated;
import javax.validation.Valid;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "project",
    "summary",
    "description",
    "version",
    "revision",
    "user",
    "start_date",
    "finish_date",
    "test_plan_key",
    "test_environments"
})
@Generated("jsonschema2pojo")
public class XrayInfo {

    @JsonProperty("project")
    private String project;
    @JsonProperty("summary")
    private String summary;
    @JsonProperty("description")
    private String description;
    @JsonProperty("version")
    private String version;
    @JsonProperty("revision")
    private String revision;
    @JsonProperty("user")
    private String user;
    @JsonProperty("start_date")
    private String startDate;
    @JsonProperty("finish_date")
    private String finishDate;
    @JsonProperty("test_plan_key")
    private String testPlanKey;
    @JsonProperty("test_environments")
    @Valid
    private List<String> testEnvironments = new ArrayList<String>();

    @JsonProperty("project")
    public String getProject() {
        return project;
    }

    @JsonProperty("project")
    public void setProject(String project) {
        this.project = project;
    }

    public XrayInfo withProject(String project) {
        this.project = project;
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

    public XrayInfo withSummary(String summary) {
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

    public XrayInfo withDescription(String description) {
        this.description = description;
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

    public XrayInfo withVersion(String version) {
        this.version = version;
        return this;
    }

    @JsonProperty("revision")
    public String getRevision() {
        return revision;
    }

    @JsonProperty("revision")
    public void setRevision(String revision) {
        this.revision = revision;
    }

    public XrayInfo withRevision(String revision) {
        this.revision = revision;
        return this;
    }

    @JsonProperty("user")
    public String getUser() {
        return user;
    }

    @JsonProperty("user")
    public void setUser(String user) {
        this.user = user;
    }

    public XrayInfo withUser(String user) {
        this.user = user;
        return this;
    }

    @JsonProperty("start_date")
    public String getStartDate() {
        return startDate;
    }

    @JsonProperty("start_date")
    public void setStartDate(String startDate) {
        this.startDate = startDate;
    }

    public XrayInfo withStartDate(String startDate) {
        this.startDate = startDate;
        return this;
    }

    @JsonProperty("finish_date")
    public String getFinishDate() {
        return finishDate;
    }

    @JsonProperty("finish_date")
    public void setFinishDate(String finishDate) {
        this.finishDate = finishDate;
    }

    public XrayInfo withFinishDate(String finishDate) {
        this.finishDate = finishDate;
        return this;
    }

    @JsonProperty("test_plan_key")
    public String getTestPlanKey() {
        return testPlanKey;
    }

    @JsonProperty("test_plan_key")
    public void setTestPlanKey(String testPlanKey) {
        this.testPlanKey = testPlanKey;
    }

    public XrayInfo withTestPlanKey(String testPlanKey) {
        this.testPlanKey = testPlanKey;
        return this;
    }

    @JsonProperty("test_environments")
    public List<String> getTestEnvironments() {
        return testEnvironments;
    }

    @JsonProperty("test_environments")
    public void setTestEnvironments(List<String> testEnvironments) {
        this.testEnvironments = testEnvironments;
    }

    public XrayInfo withTestEnvironments(List<String> testEnvironments) {
        this.testEnvironments = testEnvironments;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(XrayInfo.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("project");
        sb.append('=');
        sb.append(((this.project == null)?"<null>":this.project));
        sb.append(',');
        sb.append("summary");
        sb.append('=');
        sb.append(((this.summary == null)?"<null>":this.summary));
        sb.append(',');
        sb.append("description");
        sb.append('=');
        sb.append(((this.description == null)?"<null>":this.description));
        sb.append(',');
        sb.append("version");
        sb.append('=');
        sb.append(((this.version == null)?"<null>":this.version));
        sb.append(',');
        sb.append("revision");
        sb.append('=');
        sb.append(((this.revision == null)?"<null>":this.revision));
        sb.append(',');
        sb.append("user");
        sb.append('=');
        sb.append(((this.user == null)?"<null>":this.user));
        sb.append(',');
        sb.append("startDate");
        sb.append('=');
        sb.append(((this.startDate == null)?"<null>":this.startDate));
        sb.append(',');
        sb.append("finishDate");
        sb.append('=');
        sb.append(((this.finishDate == null)?"<null>":this.finishDate));
        sb.append(',');
        sb.append("testPlanKey");
        sb.append('=');
        sb.append(((this.testPlanKey == null)?"<null>":this.testPlanKey));
        sb.append(',');
        sb.append("testEnvironments");
        sb.append('=');
        sb.append(((this.testEnvironments == null)?"<null>":this.testEnvironments));
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
        result = ((result* 31)+((this.testEnvironments == null)? 0 :this.testEnvironments.hashCode()));
        result = ((result* 31)+((this.project == null)? 0 :this.project.hashCode()));
        result = ((result* 31)+((this.description == null)? 0 :this.description.hashCode()));
        result = ((result* 31)+((this.finishDate == null)? 0 :this.finishDate.hashCode()));
        result = ((result* 31)+((this.testPlanKey == null)? 0 :this.testPlanKey.hashCode()));
        result = ((result* 31)+((this.version == null)? 0 :this.version.hashCode()));
        result = ((result* 31)+((this.user == null)? 0 :this.user.hashCode()));
        result = ((result* 31)+((this.startDate == null)? 0 :this.startDate.hashCode()));
        result = ((result* 31)+((this.revision == null)? 0 :this.revision.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof XrayInfo) == false) {
            return false;
        }
        XrayInfo rhs = ((XrayInfo) other);
        return (((((((((((this.summary == rhs.summary)||((this.summary!= null)&&this.summary.equals(rhs.summary)))&&((this.testEnvironments == rhs.testEnvironments)||((this.testEnvironments!= null)&&this.testEnvironments.equals(rhs.testEnvironments))))&&((this.project == rhs.project)||((this.project!= null)&&this.project.equals(rhs.project))))&&((this.description == rhs.description)||((this.description!= null)&&this.description.equals(rhs.description))))&&((this.finishDate == rhs.finishDate)||((this.finishDate!= null)&&this.finishDate.equals(rhs.finishDate))))&&((this.testPlanKey == rhs.testPlanKey)||((this.testPlanKey!= null)&&this.testPlanKey.equals(rhs.testPlanKey))))&&((this.version == rhs.version)||((this.version!= null)&&this.version.equals(rhs.version))))&&((this.user == rhs.user)||((this.user!= null)&&this.user.equals(rhs.user))))&&((this.startDate == rhs.startDate)||((this.startDate!= null)&&this.startDate.equals(rhs.startDate))))&&((this.revision == rhs.revision)||((this.revision!= null)&&this.revision.equals(rhs.revision))));
    }

}
