class BuildSessionData(object):
    def __init__(
        self,
        app_name,
        build_name,
        branch_name,
        build_session_id,
        additional_params=None,
        pull_request_params=None,
    ):
        self.appName = app_name
        self.buildName = build_name
        self.branchName = branch_name
        self.buildSessionId = build_session_id
        self.additionalParams = additional_params or {}
        self.pullRequestParams = pull_request_params or {}
