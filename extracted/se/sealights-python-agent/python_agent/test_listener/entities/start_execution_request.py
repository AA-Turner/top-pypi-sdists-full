class StartExecutionRequest(object):
    def __init__(
        self,
        customer_id,
        app_name,
        branch_name,
        build_name,
        labid,
        test_stage,
        testgroupid,
        agentid,
    ):
        self.customerId = customer_id
        self.appName = app_name
        self.branchName = branch_name
        self.buildName = build_name
        self.environment = labid
        self.labId = labid
        self.newEnvironment = test_stage
        self.testStage = test_stage
        self.testGroupId = testgroupid
        self.agentId = agentid
