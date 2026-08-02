import datetime
import os
import platform
import socket
import sys

from python_agent import __version__ as VERSION
from python_agent.common.agent_events.env_vars import get_agent_env_vars, redact_argv
from python_agent.common.agent_events.utils import get_utc_time_in_ms
from python_agent.common.constants import AGENT_EVENT_START


def python_version():
    version = sys.version_info
    return f"python-{version.major}.{version.minor}.{version.micro}"


class AgentStartEvent(object):
    def __init__(
        self, config_data, agent_id, lab_id, agent_type, test_stage, agent_config=None
    ):
        self.agentId = agent_id
        self.buildSessionId = config_data.buildSessionId
        self.appName = config_data.appName
        self.agentType = agent_type
        self.labId = lab_id
        try:
            ip_address = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip_address = "127.0.0.1"
        try:
            cwd = os.getcwd()
        except Exception:
            cwd = ""
        self.events = [
            {
                "type": AGENT_EVENT_START,
                "utcTimestamp_ms": get_utc_time_in_ms(),
                "data": {
                    "agentInfo": {
                        "technology": "python",
                        "agentVersion": VERSION,
                        "agentType": agent_type,
                        "testStage": test_stage,
                        "labId": lab_id,
                        "sendsPing": True,
                        "cwd": cwd,
                        "argv": redact_argv(sys.argv[1:]),
                        "envVars": get_agent_env_vars(),
                        "tags": [python_version()],
                        "agentConfig": agent_config or {},
                        "buildSessionId": self.buildSessionId,
                    },
                    "machineInfo": {
                        "machineName": socket.gethostname(),
                        "arch": platform.machine(),
                        "os": platform.system(),
                        "localDateTime": datetime.datetime.now().isoformat(),
                        "localDateTimeUnix_s": int(datetime.datetime.now().timestamp()),
                        "ipAddress": [ip_address],
                    },
                },
            }
        ]

    @property
    def message_type(self):
        return AGENT_EVENT_START
