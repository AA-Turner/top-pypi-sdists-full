
package com.silabs.utf.QueueModels;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.processing.Generated;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import com.fasterxml.jackson.annotation.JsonValue;


/**
 * Tied to the table: testdatabase.appBuildResults
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "session_pk_id",
    "app_name",
    "app_description",
    "test_suite_name",
    "test_result_type",
    "executor_name",
    "feature_name",
    "module_name",
    "phy_name",
    "test_result",
    "engineer_name",
    "exception_msg",
    "iot_req_id",
    "tool_chain",
    "notes",
    "test_duration_sec",
    "package_info",
    "artifact_id",
    "app_version"
})
@Generated("jsonschema2pojo")
public class SqaAppBuildResult extends QueueRecord {

    /**
     * Logical FK to dbo.jobStatusTable.
     * Not creating the constraint in case this comes in before the session record.
     * (Required)
     * 
     */
    @JsonProperty("session_pk_id")
    @JsonPropertyDescription("Logical FK to dbo.jobStatusTable.\nNot creating the constraint in case this comes in before the session record.")
    @NotNull
    private String sessionPkId;
    /**
     * Name of the application
     * (Required)
     * 
     */
    @JsonProperty("app_name")
    @JsonPropertyDescription("Name of the application")
    @Size(max = 512)
    @NotNull
    private String appName;
    /**
     * Description of what the application does
     * 
     */
    @JsonProperty("app_description")
    @JsonPropertyDescription("Description of what the application does")
    @Size(max = 1024)
    private String appDescription;
    /**
     * Description of the grouping of applications
     * 
     */
    @JsonProperty("test_suite_name")
    @JsonPropertyDescription("Description of the grouping of applications")
    @Size(max = 512)
    private String testSuiteName;
    /**
     * Need table for validation created from the existing java enum
     * (Required)
     * 
     */
    @JsonProperty("test_result_type")
    @JsonPropertyDescription("Need table for validation created from the existing java enum")
    @Size(max = 256)
    @NotNull
    private String testResultType;
    /**
     * Where the application was built
     * 
     */
    @JsonProperty("executor_name")
    @JsonPropertyDescription("Where the application was built")
    @Size(max = 256)
    private String executorName;
    /**
     * Feature being tested by this test
     * 
     */
    @JsonProperty("feature_name")
    @JsonPropertyDescription("Feature being tested by this test")
    @Size(max = 256)
    private String featureName;
    /**
     * Description of the device type that the application runs on
     * 
     */
    @JsonProperty("module_name")
    @JsonPropertyDescription("Description of the device type that the application runs on")
    @Size(max = 256)
    private String moduleName;
    /**
     * Radio configuration used by the device
     * 
     */
    @JsonProperty("phy_name")
    @JsonPropertyDescription("Radio configuration used by the device")
    @Size(max = 256)
    private String phyName;
    /**
     * Did the application build
     * (Required)
     * 
     */
    @JsonProperty("test_result")
    @JsonPropertyDescription("Did the application build")
    @NotNull
    private SqaAppBuildResult.TestResult testResult;
    /**
     * Name of the engineer who created the test
     * 
     */
    @JsonProperty("engineer_name")
    @JsonPropertyDescription("Name of the engineer who created the test")
    @Size(max = 256)
    private String engineerName;
    /**
     * Stack dump exception message from build
     * 
     */
    @JsonProperty("exception_msg")
    @JsonPropertyDescription("Stack dump exception message from build")
    private String exceptionMsg;
    /**
     * JIRA IOT Req Number
     * 
     */
    @JsonProperty("iot_req_id")
    @JsonPropertyDescription("JIRA IOT Req Number")
    @Size(max = 256)
    private String iotReqId;
    /**
     * Need table for validation.
     * This is the tool and version used to build the application with colon separation
     * iar:7.80.1
     * 
     */
    @JsonProperty("tool_chain")
    @JsonPropertyDescription("Need table for validation.\nThis is the tool and version used to build the application with colon separation\niar:7.80.1")
    @Size(max = 256)
    private String toolChain;
    @JsonProperty("notes")
    @Size(max = 256)
    private String notes;
    /**
     * Length of time to build the application
     * (Required)
     * 
     */
    @JsonProperty("test_duration_sec")
    @JsonPropertyDescription("Length of time to build the application")
    @NotNull
    private Double testDurationSec;
    @JsonProperty("package_info")
    private String packageInfo;
    @JsonProperty("artifact_id")
    @Size(max = 36)
    private String artifactId;
    @JsonProperty("app_version")
    @Size(max = 50)
    private String appVersion;

    /**
     * Logical FK to dbo.jobStatusTable.
     * Not creating the constraint in case this comes in before the session record.
     * (Required)
     * 
     */
    @JsonProperty("session_pk_id")
    public String getSessionPkId() {
        return sessionPkId;
    }

    /**
     * Logical FK to dbo.jobStatusTable.
     * Not creating the constraint in case this comes in before the session record.
     * (Required)
     * 
     */
    @JsonProperty("session_pk_id")
    public void setSessionPkId(String sessionPkId) {
        this.sessionPkId = sessionPkId;
    }

    public SqaAppBuildResult withSessionPkId(String sessionPkId) {
        this.sessionPkId = sessionPkId;
        return this;
    }

    /**
     * Name of the application
     * (Required)
     * 
     */
    @JsonProperty("app_name")
    public String getAppName() {
        return appName;
    }

    /**
     * Name of the application
     * (Required)
     * 
     */
    @JsonProperty("app_name")
    public void setAppName(String appName) {
        this.appName = appName;
    }

    public SqaAppBuildResult withAppName(String appName) {
        this.appName = appName;
        return this;
    }

    /**
     * Description of what the application does
     * 
     */
    @JsonProperty("app_description")
    public String getAppDescription() {
        return appDescription;
    }

    /**
     * Description of what the application does
     * 
     */
    @JsonProperty("app_description")
    public void setAppDescription(String appDescription) {
        this.appDescription = appDescription;
    }

    public SqaAppBuildResult withAppDescription(String appDescription) {
        this.appDescription = appDescription;
        return this;
    }

    /**
     * Description of the grouping of applications
     * 
     */
    @JsonProperty("test_suite_name")
    public String getTestSuiteName() {
        return testSuiteName;
    }

    /**
     * Description of the grouping of applications
     * 
     */
    @JsonProperty("test_suite_name")
    public void setTestSuiteName(String testSuiteName) {
        this.testSuiteName = testSuiteName;
    }

    public SqaAppBuildResult withTestSuiteName(String testSuiteName) {
        this.testSuiteName = testSuiteName;
        return this;
    }

    /**
     * Need table for validation created from the existing java enum
     * (Required)
     * 
     */
    @JsonProperty("test_result_type")
    public String getTestResultType() {
        return testResultType;
    }

    /**
     * Need table for validation created from the existing java enum
     * (Required)
     * 
     */
    @JsonProperty("test_result_type")
    public void setTestResultType(String testResultType) {
        this.testResultType = testResultType;
    }

    public SqaAppBuildResult withTestResultType(String testResultType) {
        this.testResultType = testResultType;
        return this;
    }

    /**
     * Where the application was built
     * 
     */
    @JsonProperty("executor_name")
    public String getExecutorName() {
        return executorName;
    }

    /**
     * Where the application was built
     * 
     */
    @JsonProperty("executor_name")
    public void setExecutorName(String executorName) {
        this.executorName = executorName;
    }

    public SqaAppBuildResult withExecutorName(String executorName) {
        this.executorName = executorName;
        return this;
    }

    /**
     * Feature being tested by this test
     * 
     */
    @JsonProperty("feature_name")
    public String getFeatureName() {
        return featureName;
    }

    /**
     * Feature being tested by this test
     * 
     */
    @JsonProperty("feature_name")
    public void setFeatureName(String featureName) {
        this.featureName = featureName;
    }

    public SqaAppBuildResult withFeatureName(String featureName) {
        this.featureName = featureName;
        return this;
    }

    /**
     * Description of the device type that the application runs on
     * 
     */
    @JsonProperty("module_name")
    public String getModuleName() {
        return moduleName;
    }

    /**
     * Description of the device type that the application runs on
     * 
     */
    @JsonProperty("module_name")
    public void setModuleName(String moduleName) {
        this.moduleName = moduleName;
    }

    public SqaAppBuildResult withModuleName(String moduleName) {
        this.moduleName = moduleName;
        return this;
    }

    /**
     * Radio configuration used by the device
     * 
     */
    @JsonProperty("phy_name")
    public String getPhyName() {
        return phyName;
    }

    /**
     * Radio configuration used by the device
     * 
     */
    @JsonProperty("phy_name")
    public void setPhyName(String phyName) {
        this.phyName = phyName;
    }

    public SqaAppBuildResult withPhyName(String phyName) {
        this.phyName = phyName;
        return this;
    }

    /**
     * Did the application build
     * (Required)
     * 
     */
    @JsonProperty("test_result")
    public SqaAppBuildResult.TestResult getTestResult() {
        return testResult;
    }

    /**
     * Did the application build
     * (Required)
     * 
     */
    @JsonProperty("test_result")
    public void setTestResult(SqaAppBuildResult.TestResult testResult) {
        this.testResult = testResult;
    }

    public SqaAppBuildResult withTestResult(SqaAppBuildResult.TestResult testResult) {
        this.testResult = testResult;
        return this;
    }

    /**
     * Name of the engineer who created the test
     * 
     */
    @JsonProperty("engineer_name")
    public String getEngineerName() {
        return engineerName;
    }

    /**
     * Name of the engineer who created the test
     * 
     */
    @JsonProperty("engineer_name")
    public void setEngineerName(String engineerName) {
        this.engineerName = engineerName;
    }

    public SqaAppBuildResult withEngineerName(String engineerName) {
        this.engineerName = engineerName;
        return this;
    }

    /**
     * Stack dump exception message from build
     * 
     */
    @JsonProperty("exception_msg")
    public String getExceptionMsg() {
        return exceptionMsg;
    }

    /**
     * Stack dump exception message from build
     * 
     */
    @JsonProperty("exception_msg")
    public void setExceptionMsg(String exceptionMsg) {
        this.exceptionMsg = exceptionMsg;
    }

    public SqaAppBuildResult withExceptionMsg(String exceptionMsg) {
        this.exceptionMsg = exceptionMsg;
        return this;
    }

    /**
     * JIRA IOT Req Number
     * 
     */
    @JsonProperty("iot_req_id")
    public String getIotReqId() {
        return iotReqId;
    }

    /**
     * JIRA IOT Req Number
     * 
     */
    @JsonProperty("iot_req_id")
    public void setIotReqId(String iotReqId) {
        this.iotReqId = iotReqId;
    }

    public SqaAppBuildResult withIotReqId(String iotReqId) {
        this.iotReqId = iotReqId;
        return this;
    }

    /**
     * Need table for validation.
     * This is the tool and version used to build the application with colon separation
     * iar:7.80.1
     * 
     */
    @JsonProperty("tool_chain")
    public String getToolChain() {
        return toolChain;
    }

    /**
     * Need table for validation.
     * This is the tool and version used to build the application with colon separation
     * iar:7.80.1
     * 
     */
    @JsonProperty("tool_chain")
    public void setToolChain(String toolChain) {
        this.toolChain = toolChain;
    }

    public SqaAppBuildResult withToolChain(String toolChain) {
        this.toolChain = toolChain;
        return this;
    }

    @JsonProperty("notes")
    public String getNotes() {
        return notes;
    }

    @JsonProperty("notes")
    public void setNotes(String notes) {
        this.notes = notes;
    }

    public SqaAppBuildResult withNotes(String notes) {
        this.notes = notes;
        return this;
    }

    /**
     * Length of time to build the application
     * (Required)
     * 
     */
    @JsonProperty("test_duration_sec")
    public Double getTestDurationSec() {
        return testDurationSec;
    }

    /**
     * Length of time to build the application
     * (Required)
     * 
     */
    @JsonProperty("test_duration_sec")
    public void setTestDurationSec(Double testDurationSec) {
        this.testDurationSec = testDurationSec;
    }

    public SqaAppBuildResult withTestDurationSec(Double testDurationSec) {
        this.testDurationSec = testDurationSec;
        return this;
    }

    @JsonProperty("package_info")
    public String getPackageInfo() {
        return packageInfo;
    }

    @JsonProperty("package_info")
    public void setPackageInfo(String packageInfo) {
        this.packageInfo = packageInfo;
    }

    public SqaAppBuildResult withPackageInfo(String packageInfo) {
        this.packageInfo = packageInfo;
        return this;
    }

    @JsonProperty("artifact_id")
    public String getArtifactId() {
        return artifactId;
    }

    @JsonProperty("artifact_id")
    public void setArtifactId(String artifactId) {
        this.artifactId = artifactId;
    }

    public SqaAppBuildResult withArtifactId(String artifactId) {
        this.artifactId = artifactId;
        return this;
    }

    @JsonProperty("app_version")
    public String getAppVersion() {
        return appVersion;
    }

    @JsonProperty("app_version")
    public void setAppVersion(String appVersion) {
        this.appVersion = appVersion;
    }

    public SqaAppBuildResult withAppVersion(String appVersion) {
        this.appVersion = appVersion;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(SqaAppBuildResult.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("sessionPkId");
        sb.append('=');
        sb.append(((this.sessionPkId == null)?"<null>":this.sessionPkId));
        sb.append(',');
        sb.append("appName");
        sb.append('=');
        sb.append(((this.appName == null)?"<null>":this.appName));
        sb.append(',');
        sb.append("appDescription");
        sb.append('=');
        sb.append(((this.appDescription == null)?"<null>":this.appDescription));
        sb.append(',');
        sb.append("testSuiteName");
        sb.append('=');
        sb.append(((this.testSuiteName == null)?"<null>":this.testSuiteName));
        sb.append(',');
        sb.append("testResultType");
        sb.append('=');
        sb.append(((this.testResultType == null)?"<null>":this.testResultType));
        sb.append(',');
        sb.append("executorName");
        sb.append('=');
        sb.append(((this.executorName == null)?"<null>":this.executorName));
        sb.append(',');
        sb.append("featureName");
        sb.append('=');
        sb.append(((this.featureName == null)?"<null>":this.featureName));
        sb.append(',');
        sb.append("moduleName");
        sb.append('=');
        sb.append(((this.moduleName == null)?"<null>":this.moduleName));
        sb.append(',');
        sb.append("phyName");
        sb.append('=');
        sb.append(((this.phyName == null)?"<null>":this.phyName));
        sb.append(',');
        sb.append("testResult");
        sb.append('=');
        sb.append(((this.testResult == null)?"<null>":this.testResult));
        sb.append(',');
        sb.append("engineerName");
        sb.append('=');
        sb.append(((this.engineerName == null)?"<null>":this.engineerName));
        sb.append(',');
        sb.append("exceptionMsg");
        sb.append('=');
        sb.append(((this.exceptionMsg == null)?"<null>":this.exceptionMsg));
        sb.append(',');
        sb.append("iotReqId");
        sb.append('=');
        sb.append(((this.iotReqId == null)?"<null>":this.iotReqId));
        sb.append(',');
        sb.append("toolChain");
        sb.append('=');
        sb.append(((this.toolChain == null)?"<null>":this.toolChain));
        sb.append(',');
        sb.append("notes");
        sb.append('=');
        sb.append(((this.notes == null)?"<null>":this.notes));
        sb.append(',');
        sb.append("testDurationSec");
        sb.append('=');
        sb.append(((this.testDurationSec == null)?"<null>":this.testDurationSec));
        sb.append(',');
        sb.append("packageInfo");
        sb.append('=');
        sb.append(((this.packageInfo == null)?"<null>":this.packageInfo));
        sb.append(',');
        sb.append("artifactId");
        sb.append('=');
        sb.append(((this.artifactId == null)?"<null>":this.artifactId));
        sb.append(',');
        sb.append("appVersion");
        sb.append('=');
        sb.append(((this.appVersion == null)?"<null>":this.appVersion));
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
        result = ((result* 31)+((this.appVersion == null)? 0 :this.appVersion.hashCode()));
        result = ((result* 31)+((this.notes == null)? 0 :this.notes.hashCode()));
        result = ((result* 31)+((this.featureName == null)? 0 :this.featureName.hashCode()));
        result = ((result* 31)+((this.appName == null)? 0 :this.appName.hashCode()));
        result = ((result* 31)+((this.appDescription == null)? 0 :this.appDescription.hashCode()));
        result = ((result* 31)+((this.moduleName == null)? 0 :this.moduleName.hashCode()));
        result = ((result* 31)+((this.sessionPkId == null)? 0 :this.sessionPkId.hashCode()));
        result = ((result* 31)+((this.toolChain == null)? 0 :this.toolChain.hashCode()));
        result = ((result* 31)+((this.engineerName == null)? 0 :this.engineerName.hashCode()));
        result = ((result* 31)+((this.exceptionMsg == null)? 0 :this.exceptionMsg.hashCode()));
        result = ((result* 31)+((this.testResultType == null)? 0 :this.testResultType.hashCode()));
        result = ((result* 31)+((this.executorName == null)? 0 :this.executorName.hashCode()));
        result = ((result* 31)+((this.phyName == null)? 0 :this.phyName.hashCode()));
        result = ((result* 31)+((this.testSuiteName == null)? 0 :this.testSuiteName.hashCode()));
        result = ((result* 31)+((this.testDurationSec == null)? 0 :this.testDurationSec.hashCode()));
        result = ((result* 31)+((this.artifactId == null)? 0 :this.artifactId.hashCode()));
        result = ((result* 31)+((this.testResult == null)? 0 :this.testResult.hashCode()));
        result = ((result* 31)+((this.packageInfo == null)? 0 :this.packageInfo.hashCode()));
        result = ((result* 31)+((this.iotReqId == null)? 0 :this.iotReqId.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof SqaAppBuildResult) == false) {
            return false;
        }
        SqaAppBuildResult rhs = ((SqaAppBuildResult) other);
        return ((((((((((((((((((((this.appVersion == rhs.appVersion)||((this.appVersion!= null)&&this.appVersion.equals(rhs.appVersion)))&&((this.notes == rhs.notes)||((this.notes!= null)&&this.notes.equals(rhs.notes))))&&((this.featureName == rhs.featureName)||((this.featureName!= null)&&this.featureName.equals(rhs.featureName))))&&((this.appName == rhs.appName)||((this.appName!= null)&&this.appName.equals(rhs.appName))))&&((this.appDescription == rhs.appDescription)||((this.appDescription!= null)&&this.appDescription.equals(rhs.appDescription))))&&((this.moduleName == rhs.moduleName)||((this.moduleName!= null)&&this.moduleName.equals(rhs.moduleName))))&&((this.sessionPkId == rhs.sessionPkId)||((this.sessionPkId!= null)&&this.sessionPkId.equals(rhs.sessionPkId))))&&((this.toolChain == rhs.toolChain)||((this.toolChain!= null)&&this.toolChain.equals(rhs.toolChain))))&&((this.engineerName == rhs.engineerName)||((this.engineerName!= null)&&this.engineerName.equals(rhs.engineerName))))&&((this.exceptionMsg == rhs.exceptionMsg)||((this.exceptionMsg!= null)&&this.exceptionMsg.equals(rhs.exceptionMsg))))&&((this.testResultType == rhs.testResultType)||((this.testResultType!= null)&&this.testResultType.equals(rhs.testResultType))))&&((this.executorName == rhs.executorName)||((this.executorName!= null)&&this.executorName.equals(rhs.executorName))))&&((this.phyName == rhs.phyName)||((this.phyName!= null)&&this.phyName.equals(rhs.phyName))))&&((this.testSuiteName == rhs.testSuiteName)||((this.testSuiteName!= null)&&this.testSuiteName.equals(rhs.testSuiteName))))&&((this.testDurationSec == rhs.testDurationSec)||((this.testDurationSec!= null)&&this.testDurationSec.equals(rhs.testDurationSec))))&&((this.artifactId == rhs.artifactId)||((this.artifactId!= null)&&this.artifactId.equals(rhs.artifactId))))&&((this.testResult == rhs.testResult)||((this.testResult!= null)&&this.testResult.equals(rhs.testResult))))&&((this.packageInfo == rhs.packageInfo)||((this.packageInfo!= null)&&this.packageInfo.equals(rhs.packageInfo))))&&((this.iotReqId == rhs.iotReqId)||((this.iotReqId!= null)&&this.iotReqId.equals(rhs.iotReqId))));
    }


    /**
     * Did the application build
     * 
     */
    @Generated("jsonschema2pojo")
    public enum TestResult {

        FAIL("FAIL"),
        PASS("PASS"),
        BLOCK("block"),
        FAIL_("fail"),
        PASS_("pass"),
        SKIP("skip");
        private final String value;
        private final static Map<String, SqaAppBuildResult.TestResult> CONSTANTS = new HashMap<String, SqaAppBuildResult.TestResult>();

        static {
            for (SqaAppBuildResult.TestResult c: values()) {
                CONSTANTS.put(c.value, c);
            }
        }

        TestResult(String value) {
            this.value = value;
        }

        @Override
        public String toString() {
            return this.value;
        }

        @JsonValue
        public String value() {
            return this.value;
        }

        @JsonCreator
        public static SqaAppBuildResult.TestResult fromValue(String value) {
            SqaAppBuildResult.TestResult constant = CONSTANTS.get(value);
            if (constant == null) {
                throw new IllegalArgumentException(value);
            } else {
                return constant;
            }
        }

    }

}
