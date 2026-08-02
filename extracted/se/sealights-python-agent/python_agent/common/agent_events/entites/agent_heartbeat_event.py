from python_agent.common.agent_events.utils import get_utc_time_in_ms
from python_agent.common.constants import AGENT_EVENT_HEARTBEAT


class AgentHeartbeatEvent(object):
    def __init__(self, config_data, agent_id, lab_id):
        self.agentId = agent_id
        self.buildSessionId = config_data.buildSessionId
        self.appName = config_data.appName
        self.events = [
            {
                "type": AGENT_EVENT_HEARTBEAT,
                "utcTimestamp_ms": get_utc_time_in_ms(),
                "data": {"agentInfo": {"labId": lab_id}, "labId": lab_id},
            }
        ]

    @property
    def message_type(self):
        return AGENT_EVENT_HEARTBEAT
