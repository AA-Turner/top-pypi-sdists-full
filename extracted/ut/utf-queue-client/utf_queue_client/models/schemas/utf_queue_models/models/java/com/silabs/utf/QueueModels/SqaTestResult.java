
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
 * Tied to the table: testdatabase.testResults_new
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "session_pk_id",
    "test_case_id",
    "test_case_version_num",
    "test_suite_name",
    "test_description",
    "test_result_type",
    "test_parametric_data",
    "test_case_name",
    "executor_name",
    "feature_name",
    "test_creation_date",
    "testbed_name",
    "module_name",
    "phy_name",
    "test_result",
    "engineer_name",
    "exception_msg",
    "iot_req_id",
    "tool_chain",
    "vendor_name",
    "vendor_build",
    "vendor_result",
    "notes",
    "portal_watch",
    "test_duration_sec",
    "test_bed_label",
    "req_id",
    "product_line",
    "product_type",
    "customer_type",
    "jenkins_test_case_results_url",
    "test_case_uuid"
})
@Generated("jsonschema2pojo")
public class SqaTestResult extends QueueRecord {

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
     * Passed in from the test executor.
     * From the test management system or git.
     * (Required)
     * 
     */
    @JsonProperty("test_case_id")
    @JsonPropertyDescription("Passed in from the test executor.\nFrom the test management system or git.")
    @Size(max = 512)
    @NotNull
    private String testCaseId;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_case_version_num")
    @NotNull
    private Integer testCaseVersionNum;
    /**
     * Named group of tests
     * 
     */
    @JsonProperty("test_suite_name")
    @JsonPropertyDescription("Named group of tests")
    @Size(max = 512)
    private String testSuiteName;
    /**
     * What does the test case actually do
     * 
     */
    @JsonProperty("test_description")
    @JsonPropertyDescription("What does the test case actually do")
    @Size(max = 1024)
    private String testDescription;
    /**
     * Need to create a table for verification of this field
     * (Required)
     * 
     */
    @JsonProperty("test_result_type")
    @JsonPropertyDescription("Need to create a table for verification of this field")
    @Size(max = 256)
    @NotNull
    private String testResultType;
    /**
     * Test Parametric Data
     * 
     */
    @JsonProperty("test_parametric_data")
    @JsonPropertyDescription("Test Parametric Data")
    private String testParametricData;
    /**
     * Human readable version of the test case ID
     * Short summary/description
     * (Required)
     * 
     */
    @JsonProperty("test_case_name")
    @JsonPropertyDescription("Human readable version of the test case ID\nShort summary/description")
    @Size(max = 512)
    @NotNull
    private String testCaseName;
    /**
     * Where the test actually ran
     * (Required)
     * 
     */
    @JsonProperty("executor_name")
    @JsonPropertyDescription("Where the test actually ran")
    @Size(max = 256)
    @NotNull
    private String executorName;
    /**
     * Feature being tested by this test
     * (Required)
     * 
     */
    @JsonProperty("feature_name")
    @JsonPropertyDescription("Feature being tested by this test")
    @Size(max = 256)
    @NotNull
    private String featureName;
    /**
     * Date the test was created
     * ISO-8601 format
     * (Required)
     * 
     */
    @JsonProperty("test_creation_date")
    @JsonPropertyDescription("Date the test was created\nISO-8601 format")
    @NotNull
    private String testCreationDate;
    /**
     * Grouping of all of the hardware used to execute the test
     * (Required)
     * 
     */
    @JsonProperty("testbed_name")
    @JsonPropertyDescription("Grouping of all of the hardware used to execute the test")
    @Size(max = 256)
    @NotNull
    private String testbedName;
    /**
     * Testbed component list
     * (Required)
     * 
     */
    @JsonProperty("module_name")
    @JsonPropertyDescription("Testbed component list")
    @Size(max = 256)
    @NotNull
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
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_result")
    @NotNull
    private SqaTestResult.TestResult testResult;
    /**
     * Name of the engineer who created the test
     * 
     */
    @JsonProperty("engineer_name")
    @JsonPropertyDescription("Name of the engineer who created the test")
    @Size(max = 256)
    private String engineerName;
    /**
     * If an error occurs, this is the message returned.
     * 
     */
    @JsonProperty("exception_msg")
    @JsonPropertyDescription("If an error occurs, this is the message returned.")
    private String exceptionMsg;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("iot_req_id")
    @Size(max = 256)
    @NotNull
    private String iotReqId;
    /**
     * Need table for validation.
     * This is the tool and version used to build the application with colon separation
     * iar:7.80.1
     * (Required)
     * 
     */
    @JsonProperty("tool_chain")
    @JsonPropertyDescription("Need table for validation.\nThis is the tool and version used to build the application with colon separation\niar:7.80.1")
    @Size(max = 256)
    @NotNull
    private String toolChain;
    @JsonProperty("vendor_name")
    @Size(max = 256)
    private String vendorName;
    @JsonProperty("vendor_build")
    @Size(max = 256)
    private String vendorBuild;
    @JsonProperty("vendor_result")
    @Size(max = 256)
    private String vendorResult;
    @JsonProperty("notes")
    @Size(max = 1024)
    private String notes;
    /**
     * Change this to boolean - default false
     * 
     */
    @JsonProperty("portal_watch")
    @JsonPropertyDescription("Change this to boolean - default false")
    private String portalWatch;
    /**
     * Test duration in seconds
     * (Required)
     * 
     */
    @JsonProperty("test_duration_sec")
    @JsonPropertyDescription("Test duration in seconds")
    @NotNull
    private Double testDurationSec;
    @JsonProperty("test_bed_label")
    @Size(max = 256)
    private String testBedLabel;
    @JsonProperty("req_id")
    @Size(max = 256)
    private String reqId;
    @JsonProperty("product_line")
    @Size(max = 256)
    private String productLine;
    @JsonProperty("product_type")
    @Size(max = 256)
    private String productType;
    @JsonProperty("customer_type")
    @Size(max = 256)
    private String customerType;
    @JsonProperty("jenkins_test_case_results_url")
    @Size(max = 1500)
    private String jenkinsTestCaseResultsUrl;
    /**
     * UUID generated by the client software
     * 
     */
    @JsonProperty("test_case_uuid")
    @JsonPropertyDescription("UUID generated by the client software")
    private String testCaseUuid;

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

    public SqaTestResult withSessionPkId(String sessionPkId) {
        this.sessionPkId = sessionPkId;
        return this;
    }

    /**
     * Passed in from the test executor.
     * From the test management system or git.
     * (Required)
     * 
     */
    @JsonProperty("test_case_id")
    public String getTestCaseId() {
        return testCaseId;
    }

    /**
     * Passed in from the test executor.
     * From the test management system or git.
     * (Required)
     * 
     */
    @JsonProperty("test_case_id")
    public void setTestCaseId(String testCaseId) {
        this.testCaseId = testCaseId;
    }

    public SqaTestResult withTestCaseId(String testCaseId) {
        this.testCaseId = testCaseId;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_case_version_num")
    public Integer getTestCaseVersionNum() {
        return testCaseVersionNum;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_case_version_num")
    public void setTestCaseVersionNum(Integer testCaseVersionNum) {
        this.testCaseVersionNum = testCaseVersionNum;
    }

    public SqaTestResult withTestCaseVersionNum(Integer testCaseVersionNum) {
        this.testCaseVersionNum = testCaseVersionNum;
        return this;
    }

    /**
     * Named group of tests
     * 
     */
    @JsonProperty("test_suite_name")
    public String getTestSuiteName() {
        return testSuiteName;
    }

    /**
     * Named group of tests
     * 
     */
    @JsonProperty("test_suite_name")
    public void setTestSuiteName(String testSuiteName) {
        this.testSuiteName = testSuiteName;
    }

    public SqaTestResult withTestSuiteName(String testSuiteName) {
        this.testSuiteName = testSuiteName;
        return this;
    }

    /**
     * What does the test case actually do
     * 
     */
    @JsonProperty("test_description")
    public String getTestDescription() {
        return testDescription;
    }

    /**
     * What does the test case actually do
     * 
     */
    @JsonProperty("test_description")
    public void setTestDescription(String testDescription) {
        this.testDescription = testDescription;
    }

    public SqaTestResult withTestDescription(String testDescription) {
        this.testDescription = testDescription;
        return this;
    }

    /**
     * Need to create a table for verification of this field
     * (Required)
     * 
     */
    @JsonProperty("test_result_type")
    public String getTestResultType() {
        return testResultType;
    }

    /**
     * Need to create a table for verification of this field
     * (Required)
     * 
     */
    @JsonProperty("test_result_type")
    public void setTestResultType(String testResultType) {
        this.testResultType = testResultType;
    }

    public SqaTestResult withTestResultType(String testResultType) {
        this.testResultType = testResultType;
        return this;
    }

    /**
     * Test Parametric Data
     * 
     */
    @JsonProperty("test_parametric_data")
    public String getTestParametricData() {
        return testParametricData;
    }

    /**
     * Test Parametric Data
     * 
     */
    @JsonProperty("test_parametric_data")
    public void setTestParametricData(String testParametricData) {
        this.testParametricData = testParametricData;
    }

    public SqaTestResult withTestParametricData(String testParametricData) {
        this.testParametricData = testParametricData;
        return this;
    }

    /**
     * Human readable version of the test case ID
     * Short summary/description
     * (Required)
     * 
     */
    @JsonProperty("test_case_name")
    public String getTestCaseName() {
        return testCaseName;
    }

    /**
     * Human readable version of the test case ID
     * Short summary/description
     * (Required)
     * 
     */
    @JsonProperty("test_case_name")
    public void setTestCaseName(String testCaseName) {
        this.testCaseName = testCaseName;
    }

    public SqaTestResult withTestCaseName(String testCaseName) {
        this.testCaseName = testCaseName;
        return this;
    }

    /**
     * Where the test actually ran
     * (Required)
     * 
     */
    @JsonProperty("executor_name")
    public String getExecutorName() {
        return executorName;
    }

    /**
     * Where the test actually ran
     * (Required)
     * 
     */
    @JsonProperty("executor_name")
    public void setExecutorName(String executorName) {
        this.executorName = executorName;
    }

    public SqaTestResult withExecutorName(String executorName) {
        this.executorName = executorName;
        return this;
    }

    /**
     * Feature being tested by this test
     * (Required)
     * 
     */
    @JsonProperty("feature_name")
    public String getFeatureName() {
        return featureName;
    }

    /**
     * Feature being tested by this test
     * (Required)
     * 
     */
    @JsonProperty("feature_name")
    public void setFeatureName(String featureName) {
        this.featureName = featureName;
    }

    public SqaTestResult withFeatureName(String featureName) {
        this.featureName = featureName;
        return this;
    }

    /**
     * Date the test was created
     * ISO-8601 format
     * (Required)
     * 
     */
    @JsonProperty("test_creation_date")
    public String getTestCreationDate() {
        return testCreationDate;
    }

    /**
     * Date the test was created
     * ISO-8601 format
     * (Required)
     * 
     */
    @JsonProperty("test_creation_date")
    public void setTestCreationDate(String testCreationDate) {
        this.testCreationDate = testCreationDate;
    }

    public SqaTestResult withTestCreationDate(String testCreationDate) {
        this.testCreationDate = testCreationDate;
        return this;
    }

    /**
     * Grouping of all of the hardware used to execute the test
     * (Required)
     * 
     */
    @JsonProperty("testbed_name")
    public String getTestbedName() {
        return testbedName;
    }

    /**
     * Grouping of all of the hardware used to execute the test
     * (Required)
     * 
     */
    @JsonProperty("testbed_name")
    public void setTestbedName(String testbedName) {
        this.testbedName = testbedName;
    }

    public SqaTestResult withTestbedName(String testbedName) {
        this.testbedName = testbedName;
        return this;
    }

    /**
     * Testbed component list
     * (Required)
     * 
     */
    @JsonProperty("module_name")
    public String getModuleName() {
        return moduleName;
    }

    /**
     * Testbed component list
     * (Required)
     * 
     */
    @JsonProperty("module_name")
    public void setModuleName(String moduleName) {
        this.moduleName = moduleName;
    }

    public SqaTestResult withModuleName(String moduleName) {
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

    public SqaTestResult withPhyName(String phyName) {
        this.phyName = phyName;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_result")
    public SqaTestResult.TestResult getTestResult() {
        return testResult;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_result")
    public void setTestResult(SqaTestResult.TestResult testResult) {
        this.testResult = testResult;
    }

    public SqaTestResult withTestResult(SqaTestResult.TestResult testResult) {
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

    public SqaTestResult withEngineerName(String engineerName) {
        this.engineerName = engineerName;
        return this;
    }

    /**
     * If an error occurs, this is the message returned.
     * 
     */
    @JsonProperty("exception_msg")
    public String getExceptionMsg() {
        return exceptionMsg;
    }

    /**
     * If an error occurs, this is the message returned.
     * 
     */
    @JsonProperty("exception_msg")
    public void setExceptionMsg(String exceptionMsg) {
        this.exceptionMsg = exceptionMsg;
    }

    public SqaTestResult withExceptionMsg(String exceptionMsg) {
        this.exceptionMsg = exceptionMsg;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("iot_req_id")
    public String getIotReqId() {
        return iotReqId;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("iot_req_id")
    public void setIotReqId(String iotReqId) {
        this.iotReqId = iotReqId;
    }

    public SqaTestResult withIotReqId(String iotReqId) {
        this.iotReqId = iotReqId;
        return this;
    }

    /**
     * Need table for validation.
     * This is the tool and version used to build the application with colon separation
     * iar:7.80.1
     * (Required)
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
     * (Required)
     * 
     */
    @JsonProperty("tool_chain")
    public void setToolChain(String toolChain) {
        this.toolChain = toolChain;
    }

    public SqaTestResult withToolChain(String toolChain) {
        this.toolChain = toolChain;
        return this;
    }

    @JsonProperty("vendor_name")
    public String getVendorName() {
        return vendorName;
    }

    @JsonProperty("vendor_name")
    public void setVendorName(String vendorName) {
        this.vendorName = vendorName;
    }

    public SqaTestResult withVendorName(String vendorName) {
        this.vendorName = vendorName;
        return this;
    }

    @JsonProperty("vendor_build")
    public String getVendorBuild() {
        return vendorBuild;
    }

    @JsonProperty("vendor_build")
    public void setVendorBuild(String vendorBuild) {
        this.vendorBuild = vendorBuild;
    }

    public SqaTestResult withVendorBuild(String vendorBuild) {
        this.vendorBuild = vendorBuild;
        return this;
    }

    @JsonProperty("vendor_result")
    public String getVendorResult() {
        return vendorResult;
    }

    @JsonProperty("vendor_result")
    public void setVendorResult(String vendorResult) {
        this.vendorResult = vendorResult;
    }

    public SqaTestResult withVendorResult(String vendorResult) {
        this.vendorResult = vendorResult;
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

    public SqaTestResult withNotes(String notes) {
        this.notes = notes;
        return this;
    }

    /**
     * Change this to boolean - default false
     * 
     */
    @JsonProperty("portal_watch")
    public String getPortalWatch() {
        return portalWatch;
    }

    /**
     * Change this to boolean - default false
     * 
     */
    @JsonProperty("portal_watch")
    public void setPortalWatch(String portalWatch) {
        this.portalWatch = portalWatch;
    }

    public SqaTestResult withPortalWatch(String portalWatch) {
        this.portalWatch = portalWatch;
        return this;
    }

    /**
     * Test duration in seconds
     * (Required)
     * 
     */
    @JsonProperty("test_duration_sec")
    public Double getTestDurationSec() {
        return testDurationSec;
    }

    /**
     * Test duration in seconds
     * (Required)
     * 
     */
    @JsonProperty("test_duration_sec")
    public void setTestDurationSec(Double testDurationSec) {
        this.testDurationSec = testDurationSec;
    }

    public SqaTestResult withTestDurationSec(Double testDurationSec) {
        this.testDurationSec = testDurationSec;
        return this;
    }

    @JsonProperty("test_bed_label")
    public String getTestBedLabel() {
        return testBedLabel;
    }

    @JsonProperty("test_bed_label")
    public void setTestBedLabel(String testBedLabel) {
        this.testBedLabel = testBedLabel;
    }

    public SqaTestResult withTestBedLabel(String testBedLabel) {
        this.testBedLabel = testBedLabel;
        return this;
    }

    @JsonProperty("req_id")
    public String getReqId() {
        return reqId;
    }

    @JsonProperty("req_id")
    public void setReqId(String reqId) {
        this.reqId = reqId;
    }

    public SqaTestResult withReqId(String reqId) {
        this.reqId = reqId;
        return this;
    }

    @JsonProperty("product_line")
    public String getProductLine() {
        return productLine;
    }

    @JsonProperty("product_line")
    public void setProductLine(String productLine) {
        this.productLine = productLine;
    }

    public SqaTestResult withProductLine(String productLine) {
        this.productLine = productLine;
        return this;
    }

    @JsonProperty("product_type")
    public String getProductType() {
        return productType;
    }

    @JsonProperty("product_type")
    public void setProductType(String productType) {
        this.productType = productType;
    }

    public SqaTestResult withProductType(String productType) {
        this.productType = productType;
        return this;
    }

    @JsonProperty("customer_type")
    public String getCustomerType() {
        return customerType;
    }

    @JsonProperty("customer_type")
    public void setCustomerType(String customerType) {
        this.customerType = customerType;
    }

    public SqaTestResult withCustomerType(String customerType) {
        this.customerType = customerType;
        return this;
    }

    @JsonProperty("jenkins_test_case_results_url")
    public String getJenkinsTestCaseResultsUrl() {
        return jenkinsTestCaseResultsUrl;
    }

    @JsonProperty("jenkins_test_case_results_url")
    public void setJenkinsTestCaseResultsUrl(String jenkinsTestCaseResultsUrl) {
        this.jenkinsTestCaseResultsUrl = jenkinsTestCaseResultsUrl;
    }

    public SqaTestResult withJenkinsTestCaseResultsUrl(String jenkinsTestCaseResultsUrl) {
        this.jenkinsTestCaseResultsUrl = jenkinsTestCaseResultsUrl;
        return this;
    }

    /**
     * UUID generated by the client software
     * 
     */
    @JsonProperty("test_case_uuid")
    public String getTestCaseUuid() {
        return testCaseUuid;
    }

    /**
     * UUID generated by the client software
     * 
     */
    @JsonProperty("test_case_uuid")
    public void setTestCaseUuid(String testCaseUuid) {
        this.testCaseUuid = testCaseUuid;
    }

    public SqaTestResult withTestCaseUuid(String testCaseUuid) {
        this.testCaseUuid = testCaseUuid;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(SqaTestResult.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("sessionPkId");
        sb.append('=');
        sb.append(((this.sessionPkId == null)?"<null>":this.sessionPkId));
        sb.append(',');
        sb.append("testCaseId");
        sb.append('=');
        sb.append(((this.testCaseId == null)?"<null>":this.testCaseId));
        sb.append(',');
        sb.append("testCaseVersionNum");
        sb.append('=');
        sb.append(((this.testCaseVersionNum == null)?"<null>":this.testCaseVersionNum));
        sb.append(',');
        sb.append("testSuiteName");
        sb.append('=');
        sb.append(((this.testSuiteName == null)?"<null>":this.testSuiteName));
        sb.append(',');
        sb.append("testDescription");
        sb.append('=');
        sb.append(((this.testDescription == null)?"<null>":this.testDescription));
        sb.append(',');
        sb.append("testResultType");
        sb.append('=');
        sb.append(((this.testResultType == null)?"<null>":this.testResultType));
        sb.append(',');
        sb.append("testParametricData");
        sb.append('=');
        sb.append(((this.testParametricData == null)?"<null>":this.testParametricData));
        sb.append(',');
        sb.append("testCaseName");
        sb.append('=');
        sb.append(((this.testCaseName == null)?"<null>":this.testCaseName));
        sb.append(',');
        sb.append("executorName");
        sb.append('=');
        sb.append(((this.executorName == null)?"<null>":this.executorName));
        sb.append(',');
        sb.append("featureName");
        sb.append('=');
        sb.append(((this.featureName == null)?"<null>":this.featureName));
        sb.append(',');
        sb.append("testCreationDate");
        sb.append('=');
        sb.append(((this.testCreationDate == null)?"<null>":this.testCreationDate));
        sb.append(',');
        sb.append("testbedName");
        sb.append('=');
        sb.append(((this.testbedName == null)?"<null>":this.testbedName));
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
        sb.append("vendorName");
        sb.append('=');
        sb.append(((this.vendorName == null)?"<null>":this.vendorName));
        sb.append(',');
        sb.append("vendorBuild");
        sb.append('=');
        sb.append(((this.vendorBuild == null)?"<null>":this.vendorBuild));
        sb.append(',');
        sb.append("vendorResult");
        sb.append('=');
        sb.append(((this.vendorResult == null)?"<null>":this.vendorResult));
        sb.append(',');
        sb.append("notes");
        sb.append('=');
        sb.append(((this.notes == null)?"<null>":this.notes));
        sb.append(',');
        sb.append("portalWatch");
        sb.append('=');
        sb.append(((this.portalWatch == null)?"<null>":this.portalWatch));
        sb.append(',');
        sb.append("testDurationSec");
        sb.append('=');
        sb.append(((this.testDurationSec == null)?"<null>":this.testDurationSec));
        sb.append(',');
        sb.append("testBedLabel");
        sb.append('=');
        sb.append(((this.testBedLabel == null)?"<null>":this.testBedLabel));
        sb.append(',');
        sb.append("reqId");
        sb.append('=');
        sb.append(((this.reqId == null)?"<null>":this.reqId));
        sb.append(',');
        sb.append("productLine");
        sb.append('=');
        sb.append(((this.productLine == null)?"<null>":this.productLine));
        sb.append(',');
        sb.append("productType");
        sb.append('=');
        sb.append(((this.productType == null)?"<null>":this.productType));
        sb.append(',');
        sb.append("customerType");
        sb.append('=');
        sb.append(((this.customerType == null)?"<null>":this.customerType));
        sb.append(',');
        sb.append("jenkinsTestCaseResultsUrl");
        sb.append('=');
        sb.append(((this.jenkinsTestCaseResultsUrl == null)?"<null>":this.jenkinsTestCaseResultsUrl));
        sb.append(',');
        sb.append("testCaseUuid");
        sb.append('=');
        sb.append(((this.testCaseUuid == null)?"<null>":this.testCaseUuid));
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
        result = ((result* 31)+((this.notes == null)? 0 :this.notes.hashCode()));
        result = ((result* 31)+((this.vendorResult == null)? 0 :this.vendorResult.hashCode()));
        result = ((result* 31)+((this.moduleName == null)? 0 :this.moduleName.hashCode()));
        result = ((result* 31)+((this.jenkinsTestCaseResultsUrl == null)? 0 :this.jenkinsTestCaseResultsUrl.hashCode()));
        result = ((result* 31)+((this.sessionPkId == null)? 0 :this.sessionPkId.hashCode()));
        result = ((result* 31)+((this.engineerName == null)? 0 :this.engineerName.hashCode()));
        result = ((result* 31)+((this.productLine == null)? 0 :this.productLine.hashCode()));
        result = ((result* 31)+((this.testParametricData == null)? 0 :this.testParametricData.hashCode()));
        result = ((result* 31)+((this.customerType == null)? 0 :this.customerType.hashCode()));
        result = ((result* 31)+((this.phyName == null)? 0 :this.phyName.hashCode()));
        result = ((result* 31)+((this.testSuiteName == null)? 0 :this.testSuiteName.hashCode()));
        result = ((result* 31)+((this.testbedName == null)? 0 :this.testbedName.hashCode()));
        result = ((result* 31)+((this.testDurationSec == null)? 0 :this.testDurationSec.hashCode()));
        result = ((result* 31)+((this.testCaseName == null)? 0 :this.testCaseName.hashCode()));
        result = ((result* 31)+((this.productType == null)? 0 :this.productType.hashCode()));
        result = ((result* 31)+((this.portalWatch == null)? 0 :this.portalWatch.hashCode()));
        result = ((result* 31)+((this.testCaseUuid == null)? 0 :this.testCaseUuid.hashCode()));
        result = ((result* 31)+((this.featureName == null)? 0 :this.featureName.hashCode()));
        result = ((result* 31)+((this.testCreationDate == null)? 0 :this.testCreationDate.hashCode()));
        result = ((result* 31)+((this.testDescription == null)? 0 :this.testDescription.hashCode()));
        result = ((result* 31)+((this.vendorName == null)? 0 :this.vendorName.hashCode()));
        result = ((result* 31)+((this.toolChain == null)? 0 :this.toolChain.hashCode()));
        result = ((result* 31)+((this.reqId == null)? 0 :this.reqId.hashCode()));
        result = ((result* 31)+((this.vendorBuild == null)? 0 :this.vendorBuild.hashCode()));
        result = ((result* 31)+((this.exceptionMsg == null)? 0 :this.exceptionMsg.hashCode()));
        result = ((result* 31)+((this.testResultType == null)? 0 :this.testResultType.hashCode()));
        result = ((result* 31)+((this.executorName == null)? 0 :this.executorName.hashCode()));
        result = ((result* 31)+((this.testCaseVersionNum == null)? 0 :this.testCaseVersionNum.hashCode()));
        result = ((result* 31)+((this.testBedLabel == null)? 0 :this.testBedLabel.hashCode()));
        result = ((result* 31)+((this.testResult == null)? 0 :this.testResult.hashCode()));
        result = ((result* 31)+((this.testCaseId == null)? 0 :this.testCaseId.hashCode()));
        result = ((result* 31)+((this.iotReqId == null)? 0 :this.iotReqId.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof SqaTestResult) == false) {
            return false;
        }
        SqaTestResult rhs = ((SqaTestResult) other);
        return (((((((((((((((((((((((((((((((((this.notes == rhs.notes)||((this.notes!= null)&&this.notes.equals(rhs.notes)))&&((this.vendorResult == rhs.vendorResult)||((this.vendorResult!= null)&&this.vendorResult.equals(rhs.vendorResult))))&&((this.moduleName == rhs.moduleName)||((this.moduleName!= null)&&this.moduleName.equals(rhs.moduleName))))&&((this.jenkinsTestCaseResultsUrl == rhs.jenkinsTestCaseResultsUrl)||((this.jenkinsTestCaseResultsUrl!= null)&&this.jenkinsTestCaseResultsUrl.equals(rhs.jenkinsTestCaseResultsUrl))))&&((this.sessionPkId == rhs.sessionPkId)||((this.sessionPkId!= null)&&this.sessionPkId.equals(rhs.sessionPkId))))&&((this.engineerName == rhs.engineerName)||((this.engineerName!= null)&&this.engineerName.equals(rhs.engineerName))))&&((this.productLine == rhs.productLine)||((this.productLine!= null)&&this.productLine.equals(rhs.productLine))))&&((this.testParametricData == rhs.testParametricData)||((this.testParametricData!= null)&&this.testParametricData.equals(rhs.testParametricData))))&&((this.customerType == rhs.customerType)||((this.customerType!= null)&&this.customerType.equals(rhs.customerType))))&&((this.phyName == rhs.phyName)||((this.phyName!= null)&&this.phyName.equals(rhs.phyName))))&&((this.testSuiteName == rhs.testSuiteName)||((this.testSuiteName!= null)&&this.testSuiteName.equals(rhs.testSuiteName))))&&((this.testbedName == rhs.testbedName)||((this.testbedName!= null)&&this.testbedName.equals(rhs.testbedName))))&&((this.testDurationSec == rhs.testDurationSec)||((this.testDurationSec!= null)&&this.testDurationSec.equals(rhs.testDurationSec))))&&((this.testCaseName == rhs.testCaseName)||((this.testCaseName!= null)&&this.testCaseName.equals(rhs.testCaseName))))&&((this.productType == rhs.productType)||((this.productType!= null)&&this.productType.equals(rhs.productType))))&&((this.portalWatch == rhs.portalWatch)||((this.portalWatch!= null)&&this.portalWatch.equals(rhs.portalWatch))))&&((this.testCaseUuid == rhs.testCaseUuid)||((this.testCaseUuid!= null)&&this.testCaseUuid.equals(rhs.testCaseUuid))))&&((this.featureName == rhs.featureName)||((this.featureName!= null)&&this.featureName.equals(rhs.featureName))))&&((this.testCreationDate == rhs.testCreationDate)||((this.testCreationDate!= null)&&this.testCreationDate.equals(rhs.testCreationDate))))&&((this.testDescription == rhs.testDescription)||((this.testDescription!= null)&&this.testDescription.equals(rhs.testDescription))))&&((this.vendorName == rhs.vendorName)||((this.vendorName!= null)&&this.vendorName.equals(rhs.vendorName))))&&((this.toolChain == rhs.toolChain)||((this.toolChain!= null)&&this.toolChain.equals(rhs.toolChain))))&&((this.reqId == rhs.reqId)||((this.reqId!= null)&&this.reqId.equals(rhs.reqId))))&&((this.vendorBuild == rhs.vendorBuild)||((this.vendorBuild!= null)&&this.vendorBuild.equals(rhs.vendorBuild))))&&((this.exceptionMsg == rhs.exceptionMsg)||((this.exceptionMsg!= null)&&this.exceptionMsg.equals(rhs.exceptionMsg))))&&((this.testResultType == rhs.testResultType)||((this.testResultType!= null)&&this.testResultType.equals(rhs.testResultType))))&&((this.executorName == rhs.executorName)||((this.executorName!= null)&&this.executorName.equals(rhs.executorName))))&&((this.testCaseVersionNum == rhs.testCaseVersionNum)||((this.testCaseVersionNum!= null)&&this.testCaseVersionNum.equals(rhs.testCaseVersionNum))))&&((this.testBedLabel == rhs.testBedLabel)||((this.testBedLabel!= null)&&this.testBedLabel.equals(rhs.testBedLabel))))&&((this.testResult == rhs.testResult)||((this.testResult!= null)&&this.testResult.equals(rhs.testResult))))&&((this.testCaseId == rhs.testCaseId)||((this.testCaseId!= null)&&this.testCaseId.equals(rhs.testCaseId))))&&((this.iotReqId == rhs.iotReqId)||((this.iotReqId!= null)&&this.iotReqId.equals(rhs.iotReqId))));
    }

    @Generated("jsonschema2pojo")
    public enum TestResult {

        BLOCK("block"),
        FAIL("fail"),
        METRICS("metrics"),
        PASS("pass"),
        SKIP("skip");
        private final String value;
        private final static Map<String, SqaTestResult.TestResult> CONSTANTS = new HashMap<String, SqaTestResult.TestResult>();

        static {
            for (SqaTestResult.TestResult c: values()) {
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
        public static SqaTestResult.TestResult fromValue(String value) {
            SqaTestResult.TestResult constant = CONSTANTS.get(value);
            if (constant == null) {
                throw new IllegalArgumentException(value);
            } else {
                return constant;
            }
        }

    }

}
