import time


class LogsRequest(object):
    def __init__(
        self, customer_id, app_name, branch_name, build_name, environment, log
    ):
        self.customerId = customer_id
        self.appName = app_name
        self.branch = branch_name
        self.build = build_name
        self.environment = environment
        self.log = log
        self.creationTime = int(round(time.time() * 1000))
