import io
import json


class UploadReportsRequest(object):
    def __init__(self, agent_data, report_file):
        self.agentData = io.StringIO(
            str(json.dumps(agent_data, default=lambda m: m.__dict__))
        )
        self.report = report_file
