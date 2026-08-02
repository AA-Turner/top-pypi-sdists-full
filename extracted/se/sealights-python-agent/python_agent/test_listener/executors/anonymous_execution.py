import os

from python_agent.common import constants
from python_agent.common.http.backend_proxy import BackendProxy


class AnonymousExecution(object):
    def __init__(self, config_data, labid):
        self.config_data = config_data
        self.labid = self.resolve_lab_id(labid)
        self.config_data.labId = self.labid
        self.backend_proxy = BackendProxy(config_data)

    def resolve_lab_id(self, labid):
        if labid is not None:
            return labid
        labid_from_env = os.environ.get("SL_LAB_ID") or os.environ.get("SL_LABID")
        if labid_from_env is not None:
            return labid_from_env
        return (
            self.config_data.buildSessionId
            or self.config_data.appName
            or constants.DEFAULT_LAB_ID
        )
