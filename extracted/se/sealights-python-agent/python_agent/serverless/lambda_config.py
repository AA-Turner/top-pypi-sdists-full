import json
import uuid
from typing import List, Dict


class LambdaConfig(object):
    def __init__(
        self,
        app_name: str,
        build_name: str,
        branch_name: str,
        build_session_id: str,
        collector_url: str,
        build_digest: Dict[str, Dict[str, List[int]]],
        token: str,
    ):
        self.appName = app_name
        self.buildName = build_name
        self.branchName = branch_name
        self.buildSessionId = build_session_id
        self.collectorUrl = collector_url
        self.agentId = uuid.uuid4().hex
        self.buildDigest: Dict[str, Dict[str, List[int]]] = build_digest
        self.token = token

    def to_dict(self):
        return {
            "appName": self.appName,
            "buildName": self.buildName,
            "branchName": self.branchName,
            "buildSessionId": self.buildSessionId,
            "collectorUrl": self.collectorUrl,
            "agentId": self.agentId,
            "buildDigest": self.buildDigest if self.buildDigest else {},
            "token": self.token,
        }

    # save config file to json with the workspace path
    def save_to_file(self, file_path):
        config_dict = self.to_dict()
        with open(file_path, "w") as f:
            json.dump(config_dict, f, indent=4)
