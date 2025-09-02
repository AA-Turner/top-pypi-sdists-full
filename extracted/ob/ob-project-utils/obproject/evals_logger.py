import sys
import json
from metaflow import current
from .assets import Asset

MAGIC_PREFIX = "usm0jrb3"


class EvalsLogger:
    def __init__(self, project=None, branch=None):
        asset = Asset(project=project, branch=branch)
        self.project = project
        self.branch = branch
        self.meta = asset.meta

    def log(self, message: str):
        jsonmsg = json.dumps(self.meta | {"content": message})
        print(f"{MAGIC_PREFIX} {self.project} {self.branch} evals {jsonmsg}")
