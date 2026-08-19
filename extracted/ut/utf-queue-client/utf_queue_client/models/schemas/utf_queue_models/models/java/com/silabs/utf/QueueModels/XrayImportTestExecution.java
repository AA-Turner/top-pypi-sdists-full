
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
    "test_execution_key",
    "tests",
    "test_map_field_name",
    "info",
    "add_tests_to_plan",
    "create_test_for_execution"
})
@Generated("jsonschema2pojo")
public class XrayImportTestExecution {

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_execution_key")
    @NotNull
    private String testExecutionKey;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("tests")
    @Valid
    @NotNull
    private List<XrayTestExecUpdate> tests = new ArrayList<XrayTestExecUpdate>();
    @JsonProperty("test_map_field_name")
    private String testMapFieldName;
    @JsonProperty("info")
    @Valid
    private XrayInfo info;
    @JsonProperty("add_tests_to_plan")
    private Boolean addTestsToPlan;
    @JsonProperty("create_test_for_execution")
    private Boolean createTestForExecution;

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_execution_key")
    public String getTestExecutionKey() {
        return testExecutionKey;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("test_execution_key")
    public void setTestExecutionKey(String testExecutionKey) {
        this.testExecutionKey = testExecutionKey;
    }

    public XrayImportTestExecution withTestExecutionKey(String testExecutionKey) {
        this.testExecutionKey = testExecutionKey;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("tests")
    public List<XrayTestExecUpdate> getTests() {
        return tests;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("tests")
    public void setTests(List<XrayTestExecUpdate> tests) {
        this.tests = tests;
    }

    public XrayImportTestExecution withTests(List<XrayTestExecUpdate> tests) {
        this.tests = tests;
        return this;
    }

    @JsonProperty("test_map_field_name")
    public String getTestMapFieldName() {
        return testMapFieldName;
    }

    @JsonProperty("test_map_field_name")
    public void setTestMapFieldName(String testMapFieldName) {
        this.testMapFieldName = testMapFieldName;
    }

    public XrayImportTestExecution withTestMapFieldName(String testMapFieldName) {
        this.testMapFieldName = testMapFieldName;
        return this;
    }

    @JsonProperty("info")
    public XrayInfo getInfo() {
        return info;
    }

    @JsonProperty("info")
    public void setInfo(XrayInfo info) {
        this.info = info;
    }

    public XrayImportTestExecution withInfo(XrayInfo info) {
        this.info = info;
        return this;
    }

    @JsonProperty("add_tests_to_plan")
    public Boolean getAddTestsToPlan() {
        return addTestsToPlan;
    }

    @JsonProperty("add_tests_to_plan")
    public void setAddTestsToPlan(Boolean addTestsToPlan) {
        this.addTestsToPlan = addTestsToPlan;
    }

    public XrayImportTestExecution withAddTestsToPlan(Boolean addTestsToPlan) {
        this.addTestsToPlan = addTestsToPlan;
        return this;
    }

    @JsonProperty("create_test_for_execution")
    public Boolean getCreateTestForExecution() {
        return createTestForExecution;
    }

    @JsonProperty("create_test_for_execution")
    public void setCreateTestForExecution(Boolean createTestForExecution) {
        this.createTestForExecution = createTestForExecution;
    }

    public XrayImportTestExecution withCreateTestForExecution(Boolean createTestForExecution) {
        this.createTestForExecution = createTestForExecution;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(XrayImportTestExecution.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("testExecutionKey");
        sb.append('=');
        sb.append(((this.testExecutionKey == null)?"<null>":this.testExecutionKey));
        sb.append(',');
        sb.append("tests");
        sb.append('=');
        sb.append(((this.tests == null)?"<null>":this.tests));
        sb.append(',');
        sb.append("testMapFieldName");
        sb.append('=');
        sb.append(((this.testMapFieldName == null)?"<null>":this.testMapFieldName));
        sb.append(',');
        sb.append("info");
        sb.append('=');
        sb.append(((this.info == null)?"<null>":this.info));
        sb.append(',');
        sb.append("addTestsToPlan");
        sb.append('=');
        sb.append(((this.addTestsToPlan == null)?"<null>":this.addTestsToPlan));
        sb.append(',');
        sb.append("createTestForExecution");
        sb.append('=');
        sb.append(((this.createTestForExecution == null)?"<null>":this.createTestForExecution));
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
        result = ((result* 31)+((this.addTestsToPlan == null)? 0 :this.addTestsToPlan.hashCode()));
        result = ((result* 31)+((this.testExecutionKey == null)? 0 :this.testExecutionKey.hashCode()));
        result = ((result* 31)+((this.testMapFieldName == null)? 0 :this.testMapFieldName.hashCode()));
        result = ((result* 31)+((this.tests == null)? 0 :this.tests.hashCode()));
        result = ((result* 31)+((this.createTestForExecution == null)? 0 :this.createTestForExecution.hashCode()));
        result = ((result* 31)+((this.info == null)? 0 :this.info.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof XrayImportTestExecution) == false) {
            return false;
        }
        XrayImportTestExecution rhs = ((XrayImportTestExecution) other);
        return (((((((this.addTestsToPlan == rhs.addTestsToPlan)||((this.addTestsToPlan!= null)&&this.addTestsToPlan.equals(rhs.addTestsToPlan)))&&((this.testExecutionKey == rhs.testExecutionKey)||((this.testExecutionKey!= null)&&this.testExecutionKey.equals(rhs.testExecutionKey))))&&((this.testMapFieldName == rhs.testMapFieldName)||((this.testMapFieldName!= null)&&this.testMapFieldName.equals(rhs.testMapFieldName))))&&((this.tests == rhs.tests)||((this.tests!= null)&&this.tests.equals(rhs.tests))))&&((this.createTestForExecution == rhs.createTestForExecution)||((this.createTestForExecution!= null)&&this.createTestForExecution.equals(rhs.createTestForExecution))))&&((this.info == rhs.info)||((this.info!= null)&&this.info.equals(rhs.info))));
    }

}
