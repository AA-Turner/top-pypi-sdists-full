interface QueueMessage {
    /**
     * Type of record
     */
    recordType: "UTF_TEST_EVENT" | "LOG_EVENT" | "EXCEPTION_EVENT" | "ARTIFACT_UPLOAD_REQUEST" | "OPENTELEMETRY_DATA" | "DATALAKE_DATA" | "TEST_RAIL_EVENT" | "XRAY_EVENT";
    /**
     * Subtype of record. Not all types have a subtype, but it is required when they have one.
     */
    recordSubType?: "TEST_RESULT" | "SESSION_START" | "SESSION_STOP" | "BUILD_RESULT" | "IMPORT_TEST_EXECUTION" | "TEST_RESULT_APP";
    /**
     * Unique string that identifies the app/group sending the message.
     * Forward looking to match the data lake infrastructure.
     */
     tenantKey: string;
    /**
     * UTC datetime.
     * Use ISO-8601 format with time zone
     * 2022-03-10T18:50:05Z
     */
    recordTimestamp: string;

    /**
     * Record Payload.
     * This is flexible to allow different fields for different record types and DB tables
     */
    payload: QueueRecord;

    /**
     * Unique client-generated UUID
     */
    messageId?: string;
}

// Older version of QueueMessage, for backwards compatibility
interface QueueMessageV1 {
    /**
     * Type of record
     */
    recordType: "UTF_TEST_EVENT" | "TEST_EVENT" | "LOG_EVENT" | "EXCEPTION_EVENT" | "ARTIFACT_UPLOAD_REQUEST";

    /**
     * Record Payload
     */
    payload: QueueRecord;

    /**
     * UTC Timestamp
     * Given in seconds since epoch (unix time)
     */
    timestamp: number;
}


interface QueueRecord {
    [key:string]: any;
}

interface DataLakeData extends QueueRecord {
    /*
    * Format of the data contained in the data field
    */ 
    dataFormat: "JSON" | "JSONSTR" | "PARQUET" | "CSV" | "NDJSON";

    /*
     * Object ID of the data payload
     * if this is not provided, a unique id will be generated
     */
    object_id?: string;
    
    /*
     * Data payload
     * if dataFormat is JSON, this is an object
     * if dataFormat is NDJSON, this is an array of objects
     * if dataFormat is JSONSTR, PARQUET or CSV, this is a base64 encoded string, with optional compression
     * as specified in the compression field
     */
    data: string | object | object[];

    /*
     * Compression format of the data field
     * if dataFormat is JSONSTR, PARQUET or CSV, this is required
     * if dataFormat is JSON or NDJSON, this is ignored
     */
    compression?: "GZIP" | "SNAPPY" | "NONE";
}

interface TelemetryData extends QueueRecord {
    dataType: "TRACES" | "LOGS" | "METRICS";
    base64ProtobufData: string;
    compression?: string;
}

interface ArtifactUploadRequest extends QueueRecord{
    name: string;
    extension: string;
    metadata: ArtifactMetadata | ArtifactBuildMetadata;
    base64Content: string;
    validateMetadata: boolean;
}

interface ArtifactMetadata {
    [key:string]: string;
}

interface ArtifactBuildMetadata {
    branch?: string;
    stack?: string;
    build_number?: string;
    target?: string;
    studio?: string;
    compiler?: string;
    app_name?: string;
    test_suite?: string;
    chip_id?: string;
    studio_build_version?: string;
    compiler_build_version?: string;
}


/**
 * Tied to the table: testdatabase.appBuildResults
 */
interface SqaAppBuildResult extends QueueRecord{

    /**
     * Logical FK to dbo.jobStatusTable.
     * Not creating the constraint in case this comes in before the session record.
     */
    session_pk_id: string;

    /**
     * Name of the application
     * @maxLength 512
     */
    app_name: string;

    /**
     * Description of what the application does
     * @maxLength 1024
     */
    app_description?: string;

    /**
     * Description of the grouping of applications
     * @maxLength 512
     */
    test_suite_name?: string;

    /**
     * Need table for validation created from the existing java enum
     * @maxLength 256
     */
    test_result_type: string;

    /**
     * Where the application was built
     * @maxLength 256
     */
    executor_name?: string;

    /**
     * Feature being tested by this test
     * @maxLength 256
     */
    feature_name?: string;

    /**
     * Description of the device type that the application runs on
     * @maxLength 256
     */
    module_name?: string;

    /**
     * Radio configuration used by the device
     * @maxLength 256
     */
    phy_name?: string;

    /**
     * Did the application build
     */
    test_result: "pass" | "fail" | "skip" | "block" | "PASS" | "FAIL";

    /**
     * Name of the engineer who created the test
     * @maxLength 256
     */
    engineer_name?: string;

    /**
     * Stack dump exception message from build
     */
    exception_msg?: string;

    /**
     * JIRA IOT Req Number
     * @maxLength 256
     */
    iot_req_id?: string;

    /**
     * Need table for validation.
     * This is the tool and version used to build the application with colon separation
     * iar:7.80.1
     * @maxLength 256
     */
    tool_chain?: string;

    /**
     * @maxLength 256
     */
    notes?: string;

    /**
     * Length of time to build the application
     */
    test_duration_sec: number;

    package_info?: string;

    /**
     * @maxLength 36
     */
    artifact_id?: string;

    /**
     * @maxLength 50
     */
    app_version?: string;
}


/**
 * Tied to the table: testdatabase.testResults_new
 */
interface SqaTestResult extends QueueRecord {

    /**
     * Logical FK to dbo.jobStatusTable.
     * Not creating the constraint in case this comes in before the session record.
     */
    session_pk_id: string;

    /**
     * Passed in from the test executor.
     * From the test management system or git.
     * @maxLength 512
     */
    test_case_id: string;

    /**
     * @TJS-type integer
     */
    test_case_version_num: number;

    /**
     * Named group of tests
     * @maxLength 512
     */
    test_suite_name?: string;

    /**
     * What does the test case actually do
     * @maxLength 1024
     */
    test_description?: string;

    /**
     * Need to create a table for verification of this field
     * @maxLength 256
     */
    test_result_type: string
    /**
     * Test Parametric Data
     */
    test_parametric_data?: string;

    /**
     * Human readable version of the test case ID
     * Short summary/description
     * @maxLength 512
     */
    test_case_name: string;

    /**
     * Where the test actually ran
     * @maxLength 256
     */
    executor_name: string;

    /**
     * Feature being tested by this test
     * @maxLength 256
     */
    feature_name: string;

    /**
     * Date the test was created
     * ISO-8601 format
     */
    test_creation_date: string;

    /**
     * Grouping of all of the hardware used to execute the test
     * @maxLength 256
     */
    testbed_name: string; 

    /**
     * Testbed component list
     * @maxLength 256
     */
    module_name: string;

    /**
     * Radio configuration used by the device
     * @maxLength 256
     */
    phy_name?: string;

    /**
     * 
     */
    test_result: "pass" | "fail" | "skip" | "block" | "metrics";

    /**
     * Name of the engineer who created the test
     * @maxLength 256
     */
    engineer_name?: string;

    /**
     * If an error occurs, this is the message returned.
     */
    exception_msg?: string;

    /**
     * @maxLength 256
     */
    iot_req_id: string;

    /**
     * Need table for validation.
     * This is the tool and version used to build the application with colon separation
     * iar:7.80.1
     * @maxLength 256
     */
    tool_chain: string;

    /**
     * @maxLength 256
     */
    vendor_name?: string;
    
    /**
     * @maxLength 256
     */
    vendor_build?: string;
    
    /**
     * @maxLength 256
     */
    vendor_result?: string;
    
    /**
     * @maxLength 1024
     */
    notes?: string;
    
    /**
     * Change this to boolean - default false
     */
    portal_watch?: string;
    
    /**
     * Test duration in seconds
     */
    test_duration_sec: number;
    
    /**
     * @maxLength 256
     */
    test_bed_label?: string;

    /**
     * @maxLength 256
     */
    req_id?: string;

    /**
     * @maxLength 256
     */
    product_line?: string;

    /**
     * @maxLength 256
     */
    product_type?: string;

    /**
     * @maxLength 256
     */
    customer_type?: string;

    /**
     * @maxLength 1500
     */
    jenkins_test_case_results_url?: string;

    /**
     * UUID generated by the client software
     */
    test_case_uuid?: string;
}


/**
 * Tied to the table: dbo.jobStatusTable
 */
interface SqaTestSession extends QueueRecord {
    
    /**
     * UUID generated by the Jenkins client software
     */
    PK_ID: string;
    
    /**
     * ISO-8601 Datetime
     */
    startTime: string;
    
    /**
     * ISO-8601 datetime
     */
    stopTime?: string;
    
    /**
     * Status of the Jenkins job
     */
    jenkinsJobStatus: "COMPLETE" | "IN PROGRESS" | "FAIL"
    
    /**
     * Elapsed number of seconds for the Jenkins job.
     * Should be close to stop time - start time.
     * Change the data type in the DB to integer.
     * @TJS-type integer
     */
    duration?: number;
    /**
     * Type of Jenkins job
     * @maxLength 256
     */
    jobType?: string
    
    /**
     * @maxLength 256
     */
    releaseName: string;
    
    /**
     * @maxLength 256
     */
    branchName: string;
    
    /**
     * @maxLength 256
     */
    stackName: string;

    /**
     * @TJS-type number
     */
    SDKBuildNum: number;
    
    /**
     * @maxLength 1500
     */
    SDKUrl?: string;
    
    /**
     * @maxLength 1500
     */
    studioUrl?: string;

    /**
     * @TJS-type integer
     */
    totalTests?: number;

    /**
     * @TJS-type integer
     */
    PASS_cnt?: number;

    /**
     * @TJS-type integer
     */
    FAIL_cnt?: number;

    /**
     * @TJS-type integer
     */
    SKIP_cnt?: number;

    /**
     * @TJS-type integer
     */
    BLOCK_cnt?: number;
    
    /**
     * @maxLength 256
     */
    jenkinsServerName: string;

    /**
     * @TJS-type integer
     */
    jenkinRunNum: number;
    
    /**
     * @maxLength 1500
     */
    jenkinsJobName: string;
    
    /**
     * @maxLength 1500
     */
    jenkinsTestResultsUrl: string;
    
    /**
     * @maxLength 500
     */
    traceId?: string;

    /**
     * @maxLength 256
     */
    testFramework?: string;

    /**
     * @maxLength 256
     */
    SDKVersion?: string;

    /**
     * @maxLength 256
     */
    test_run_by?: string;

    /**
     * @maxLength 500
     */
    package_name?: string;

    /**
     * @maxLength 50
     */
    package_version?: string;

    /**
     * ISO-8601 Datetime
     */
    package_datetime?: string;

    /**
     * Branch from which the test originated
     * @maxLength 250
     */
    from_branch_name?: string;

    /**
     * Build number from which the test originated
     * @TJS-type number
     */
    from_build_num?: number;

    /**
     * Test Framework version on which the test ran
     * @maxLength 250
     */
    testFrameworkVersion?: string;

    /**
     * Substack name for the multiprotocol stack
     * @maxLength 50
     */
    subStackName?: string;

}

interface LogEvent extends QueueRecord {

}

interface ExceptionEvent extends QueueRecord {

}

interface TestRailResult extends QueueRecord{
    id: string;

    /**
     * @TJS-type integer
     */
    run_id: number;

    status: string;

    comment?: string;

    version?: string;

    defects?: string;

    /**
     * @TJS-type integer
     */
    assigned_to_id?: number;

    custom_props?: TestResultCustomProps;
}

interface TestResultCustomProps {
    [key:string]: string;
}

interface XrayInfo extends QueueRecord {
    project?: string; // The project key where the test execution will be created
    summary?: string; // The summary for the test execution issue
    description?: string; // The description for the test execution issue
    version?: string; // The version name for the Fix Version field
    revision?: string; // A revision for the revision custom field
    user?: string; // The username for the Jira user who executed the tests
    start_date?: string; // The start date for the test execution issue
    finish_date?: string; // The finish date for the test execution issue
    test_plan_key?: string; // The test plan key for associating the test execution issue
    test_environments?: string[]; // The test environments for the test execution issue
}

interface XrayStep extends QueueRecord {
    action: string; // The step action
    data: string; // The step data
    result: string; // The step expected result
}

interface XrayParameter extends QueueRecord {
    name: string; // The parameter name
    value: string; // The parameter value
}

interface XrayCustomField extends QueueRecord {
    name: string; // Name of custom field ID
    /**
     * @TJS-type integer
    */
    id?: string; // The test run custom field ID
    value: string; // The test run custom field value
}

interface XrayIteration extends QueueRecord {
    name?: string; // The iteration name
    /**
     * @TJS-type integer
     */
    id?: number,
    parameters: XrayParameter[]; // The parameters for the iteration
    /**
     * Status for the iteration (examples: PASS, FAIL, SKIP, BLOCK, BROKEN, REGRESSION)
     */
    status: string;
}

interface XrayTestInfo extends QueueRecord {
    project_key: string; // The project key where the test issue will be created
    summary?: string; // The summary for the test issue
    description?: string; // The description of the test issue
    test_type?: string; // The test type (e.g., Manual, Cucumber, Generic)
    requirement_keys?: string[]; // An array of requirement issue keys to associate with the test
    labels?: string[]; // The test issue labels
    steps?: XrayStep[]; // An array of steps for the test issue
}

interface XrayTestExecUpdate extends QueueRecord {
    test_key: string; // The test issue key
    /**
     * Status for the iteration (examples: PASS, FAIL, SKIP, BLOCK, BROKEN, REGRESSION)
     */
    status: string;
    test_info?: XrayTestInfo; // Information about the test
    test_version?: string; // The Test Version to import the result
    start?: string; // The start date for the test run
    finish?: string; // The finish date for the test run
    comment?: string; // The comment for the test run
    executed_by?: string; // The user ID who executed the test run
    assignee?: string; // The user ID for the assignee of the test run
    steps?: XrayStep[]; // An array of steps for the test run
    iterations?: XrayIteration[]; // An array of iterations for the test run
    custom_fields?: XrayCustomField[]; // An array of custom fields for the test run
}

interface XrayImportTestExecution extends QueueRecord {
    test_execution_key: string; // The test execution key where to import the execution results
    tests: XrayTestExecUpdate[]; // An array of test execution updates
    test_map_field_name?: string;
    info?: XrayInfo; // Additional information for the test execution
    add_tests_to_plan?: boolean; // Whether the tests must be added to the Test Plan
    create_test_for_execution?: boolean // whether to create new tests for test execution
}

interface SqaTestResultApps extends QueueRecord {
    /**
     * @maxLength 36
     */
    test_case_uuid: string; // unique test case uuid
    /**
     * @maxLength 36
     */
    artifact_id: string; // artifact uuid
   
}