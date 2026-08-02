import json
import os
import sys
from typing import List, Optional

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "libs"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent"))
import requests

from .agent_config import AgentConfig
from .logging import debug, error


class TechSpecificInfo:
    # Assuming the structure of TechSpecificInfo, since it wasn't provided
    pass


class AgentInfo:
    # Assuming the structure of AgentInfo, since it wasn't provided
    pass


class MachineInfo:
    # Assuming the structure of MachineInfo, since it wasn't provided
    pass


class AgentMetadata:
    def __init__(
        self,
        tech_specific_info: Optional[TechSpecificInfo] = None,
        agent_info: Optional[AgentInfo] = None,
        machine_info: Optional[MachineInfo] = None,
    ):
        self.tech_specific_info = tech_specific_info
        self.agent_info = agent_info
        self.machine_info = machine_info


class Intervals:
    def __init__(self, timed_footprints_collection_interval_seconds: int):
        self.timed_footprints_collection_interval_seconds = (
            timed_footprints_collection_interval_seconds
        )


class FootprintMeta:
    def __init__(self, agent_config: AgentConfig):
        self.agentMetadata = {}
        self.agentConfig = agent_config
        self.agentId = agent_config.agentId
        self.labId = agent_config.labId
        self.intervals = {"timedFootprintsCollectionIntervalSeconds": 10}


class FootprintExecutionHit(object):
    def __init__(
        self,
        methods: List[int],
        method_lines: dict[str, List[int]],
        start_time: int,
        end_time: int,
    ):
        self.start = start_time
        self.end = end_time
        self.methods = methods
        self.methodLines = method_lines


class FootprintExecution(object):
    def __init__(
        self,
        indexes: List[int],
        method_lines: dict[str, List[int]],
        start_time: int,
        end_time: int,
    ):
        self.executionId = ""
        self.hits = []
        self.hits.append(
            FootprintExecutionHit(indexes, method_lines, start_time, end_time)
        )


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(
            obj,
            (
                FootprintExecutionHit,
                FootprintExecution,
                FootprintModel,
                FootprintMeta,
                AgentConfig,
            ),
        ):
            return obj.__dict__
        return super().default(obj)


class FootprintModel(object):
    def __init__(
        self,
        agent_config: AgentConfig,
        methods: dict[str, List[int]],
        start_time: int,
        end_time: int,
    ):
        self.formatVersion = "6.0"
        self.methods = []
        self.executions = []
        self.meta = FootprintMeta(agent_config)
        self.methods.extend(list(methods.keys()))
        method_lines: dict[str, List[int]] = {
            index: value for index, (key, value) in enumerate(methods.items())
        }
        indexes = [index for index, _ in enumerate(list(methods.keys()))]
        self.executions.append(
            FootprintExecution(indexes, method_lines, start_time, end_time)
        )

    def send_collector(
        self,
        agent_config: AgentConfig,
        proxy: Optional[str] = None,
        token: Optional[str] = None,
    ):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        url = "%s/api/v6/agents/%s/footprints" % (
            agent_config.collectorUrl,
            agent_config.buildSessionId,
        )
        proxies = {
            "http": proxy,  # For HTTP requests
            "https": proxy,  # For HTTPS requests
        }
        try:
            data_json = json.dumps(self, cls=CustomEncoder, indent=4)
            debug(f"Footprints JSON: {data_json}")
            response = requests.post(
                url, data=data_json, headers=headers, proxies=proxies
            )
            response.raise_for_status()
        except requests.HTTPError as http_err:
            error(f"HTTP error occurred: {http_err}")
        except requests.ConnectionError as conn_err:
            error(f"Connection error occurred: {conn_err}")
        except requests.Timeout as timeout_err:
            error(f"Timeout error occurred: {timeout_err}")
        except requests.RequestException as req_err:
            error(f"An error occurred during the request: {req_err}")
        except json.JSONDecodeError:
            error("Failed to decode JSON response from server.")
        except Exception as e:
            error(f"An unexpected error occurred: {e}")
            raise e
