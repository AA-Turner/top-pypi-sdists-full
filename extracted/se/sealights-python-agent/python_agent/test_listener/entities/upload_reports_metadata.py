from python_agent.build_scanner.entities.environment_data import EnvironmentData


class UploadReportsAgentData(object):
    def __init__(self, config_data, labid, source, report_type, has_more_requests):
        self.source = source
        self.type = report_type
        self.customerId = config_data.customerId
        self.appName = config_data.appName
        self.branchName = config_data.branchName
        self.buildName = config_data.buildName
        self.hasMoreRequests = has_more_requests
        self.environment = EnvironmentData(labid, None, "")
        self.environment.environmentName = labid
