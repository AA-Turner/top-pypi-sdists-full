from python_agent.common.agent_events.utils import get_utc_time_in_ms
from python_agent.common.constants import AGENT_EVENT_STOP


class AgentStopEvent(object):
    def __init__(self, config_data, agent_id):
        self.agentId = agent_id
        self.buildSessionId = config_data.buildSessionId
        self.appName = config_data.appName
        self.events = [
            {
                "type": AGENT_EVENT_STOP,
                "utcTimestamp_ms": get_utc_time_in_ms(),
            }
        ]

    @property
    def message_type(self):
        return AGENT_EVENT_STOP
