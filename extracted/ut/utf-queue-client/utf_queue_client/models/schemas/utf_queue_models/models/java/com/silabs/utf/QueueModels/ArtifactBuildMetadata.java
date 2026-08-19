
package com.silabs.utf.QueueModels;

import javax.annotation.processing.Generated;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "branch",
    "stack",
    "build_number",
    "target",
    "studio",
    "compiler",
    "app_name",
    "test_suite",
    "chip_id",
    "studio_build_version",
    "compiler_build_version"
})
@Generated("jsonschema2pojo")
public class ArtifactBuildMetadata {

    @JsonProperty("branch")
    private String branch;
    @JsonProperty("stack")
    private String stack;
    @JsonProperty("build_number")
    private String buildNumber;
    @JsonProperty("target")
    private String target;
    @JsonProperty("studio")
    private String studio;
    @JsonProperty("compiler")
    private String compiler;
    @JsonProperty("app_name")
    private String appName;
    @JsonProperty("test_suite")
    private String testSuite;
    @JsonProperty("chip_id")
    private String chipId;
    @JsonProperty("studio_build_version")
    private String studioBuildVersion;
    @JsonProperty("compiler_build_version")
    private String compilerBuildVersion;

    @JsonProperty("branch")
    public String getBranch() {
        return branch;
    }

    @JsonProperty("branch")
    public void setBranch(String branch) {
        this.branch = branch;
    }

    public ArtifactBuildMetadata withBranch(String branch) {
        this.branch = branch;
        return this;
    }

    @JsonProperty("stack")
    public String getStack() {
        return stack;
    }

    @JsonProperty("stack")
    public void setStack(String stack) {
        this.stack = stack;
    }

    public ArtifactBuildMetadata withStack(String stack) {
        this.stack = stack;
        return this;
    }

    @JsonProperty("build_number")
    public String getBuildNumber() {
        return buildNumber;
    }

    @JsonProperty("build_number")
    public void setBuildNumber(String buildNumber) {
        this.buildNumber = buildNumber;
    }

    public ArtifactBuildMetadata withBuildNumber(String buildNumber) {
        this.buildNumber = buildNumber;
        return this;
    }

    @JsonProperty("target")
    public String getTarget() {
        return target;
    }

    @JsonProperty("target")
    public void setTarget(String target) {
        this.target = target;
    }

    public ArtifactBuildMetadata withTarget(String target) {
        this.target = target;
        return this;
    }

    @JsonProperty("studio")
    public String getStudio() {
        return studio;
    }

    @JsonProperty("studio")
    public void setStudio(String studio) {
        this.studio = studio;
    }

    public ArtifactBuildMetadata withStudio(String studio) {
        this.studio = studio;
        return this;
    }

    @JsonProperty("compiler")
    public String getCompiler() {
        return compiler;
    }

    @JsonProperty("compiler")
    public void setCompiler(String compiler) {
        this.compiler = compiler;
    }

    public ArtifactBuildMetadata withCompiler(String compiler) {
        this.compiler = compiler;
        return this;
    }

    @JsonProperty("app_name")
    public String getAppName() {
        return appName;
    }

    @JsonProperty("app_name")
    public void setAppName(String appName) {
        this.appName = appName;
    }

    public ArtifactBuildMetadata withAppName(String appName) {
        this.appName = appName;
        return this;
    }

    @JsonProperty("test_suite")
    public String getTestSuite() {
        return testSuite;
    }

    @JsonProperty("test_suite")
    public void setTestSuite(String testSuite) {
        this.testSuite = testSuite;
    }

    public ArtifactBuildMetadata withTestSuite(String testSuite) {
        this.testSuite = testSuite;
        return this;
    }

    @JsonProperty("chip_id")
    public String getChipId() {
        return chipId;
    }

    @JsonProperty("chip_id")
    public void setChipId(String chipId) {
        this.chipId = chipId;
    }

    public ArtifactBuildMetadata withChipId(String chipId) {
        this.chipId = chipId;
        return this;
    }

    @JsonProperty("studio_build_version")
    public String getStudioBuildVersion() {
        return studioBuildVersion;
    }

    @JsonProperty("studio_build_version")
    public void setStudioBuildVersion(String studioBuildVersion) {
        this.studioBuildVersion = studioBuildVersion;
    }

    public ArtifactBuildMetadata withStudioBuildVersion(String studioBuildVersion) {
        this.studioBuildVersion = studioBuildVersion;
        return this;
    }

    @JsonProperty("compiler_build_version")
    public String getCompilerBuildVersion() {
        return compilerBuildVersion;
    }

    @JsonProperty("compiler_build_version")
    public void setCompilerBuildVersion(String compilerBuildVersion) {
        this.compilerBuildVersion = compilerBuildVersion;
    }

    public ArtifactBuildMetadata withCompilerBuildVersion(String compilerBuildVersion) {
        this.compilerBuildVersion = compilerBuildVersion;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(ArtifactBuildMetadata.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("branch");
        sb.append('=');
        sb.append(((this.branch == null)?"<null>":this.branch));
        sb.append(',');
        sb.append("stack");
        sb.append('=');
        sb.append(((this.stack == null)?"<null>":this.stack));
        sb.append(',');
        sb.append("buildNumber");
        sb.append('=');
        sb.append(((this.buildNumber == null)?"<null>":this.buildNumber));
        sb.append(',');
        sb.append("target");
        sb.append('=');
        sb.append(((this.target == null)?"<null>":this.target));
        sb.append(',');
        sb.append("studio");
        sb.append('=');
        sb.append(((this.studio == null)?"<null>":this.studio));
        sb.append(',');
        sb.append("compiler");
        sb.append('=');
        sb.append(((this.compiler == null)?"<null>":this.compiler));
        sb.append(',');
        sb.append("appName");
        sb.append('=');
        sb.append(((this.appName == null)?"<null>":this.appName));
        sb.append(',');
        sb.append("testSuite");
        sb.append('=');
        sb.append(((this.testSuite == null)?"<null>":this.testSuite));
        sb.append(',');
        sb.append("chipId");
        sb.append('=');
        sb.append(((this.chipId == null)?"<null>":this.chipId));
        sb.append(',');
        sb.append("studioBuildVersion");
        sb.append('=');
        sb.append(((this.studioBuildVersion == null)?"<null>":this.studioBuildVersion));
        sb.append(',');
        sb.append("compilerBuildVersion");
        sb.append('=');
        sb.append(((this.compilerBuildVersion == null)?"<null>":this.compilerBuildVersion));
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
        result = ((result* 31)+((this.studio == null)? 0 :this.studio.hashCode()));
        result = ((result* 31)+((this.stack == null)? 0 :this.stack.hashCode()));
        result = ((result* 31)+((this.appName == null)? 0 :this.appName.hashCode()));
        result = ((result* 31)+((this.testSuite == null)? 0 :this.testSuite.hashCode()));
        result = ((result* 31)+((this.compiler == null)? 0 :this.compiler.hashCode()));
        result = ((result* 31)+((this.studioBuildVersion == null)? 0 :this.studioBuildVersion.hashCode()));
        result = ((result* 31)+((this.branch == null)? 0 :this.branch.hashCode()));
        result = ((result* 31)+((this.buildNumber == null)? 0 :this.buildNumber.hashCode()));
        result = ((result* 31)+((this.chipId == null)? 0 :this.chipId.hashCode()));
        result = ((result* 31)+((this.target == null)? 0 :this.target.hashCode()));
        result = ((result* 31)+((this.compilerBuildVersion == null)? 0 :this.compilerBuildVersion.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof ArtifactBuildMetadata) == false) {
            return false;
        }
        ArtifactBuildMetadata rhs = ((ArtifactBuildMetadata) other);
        return ((((((((((((this.studio == rhs.studio)||((this.studio!= null)&&this.studio.equals(rhs.studio)))&&((this.stack == rhs.stack)||((this.stack!= null)&&this.stack.equals(rhs.stack))))&&((this.appName == rhs.appName)||((this.appName!= null)&&this.appName.equals(rhs.appName))))&&((this.testSuite == rhs.testSuite)||((this.testSuite!= null)&&this.testSuite.equals(rhs.testSuite))))&&((this.compiler == rhs.compiler)||((this.compiler!= null)&&this.compiler.equals(rhs.compiler))))&&((this.studioBuildVersion == rhs.studioBuildVersion)||((this.studioBuildVersion!= null)&&this.studioBuildVersion.equals(rhs.studioBuildVersion))))&&((this.branch == rhs.branch)||((this.branch!= null)&&this.branch.equals(rhs.branch))))&&((this.buildNumber == rhs.buildNumber)||((this.buildNumber!= null)&&this.buildNumber.equals(rhs.buildNumber))))&&((this.chipId == rhs.chipId)||((this.chipId!= null)&&this.chipId.equals(rhs.chipId))))&&((this.target == rhs.target)||((this.target!= null)&&this.target.equals(rhs.target))))&&((this.compilerBuildVersion == rhs.compilerBuildVersion)||((this.compilerBuildVersion!= null)&&this.compilerBuildVersion.equals(rhs.compilerBuildVersion))));
    }

}
