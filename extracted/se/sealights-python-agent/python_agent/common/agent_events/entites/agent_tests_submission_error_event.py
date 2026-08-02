from python_agent.common.agent_events.utils import get_utc_time_in_ms
from python_agent.common.config_data import ConfigData
from python_agent.common.constants import AGENT_EVENT_TEST_SUBMIT_ERROR


class AgentTestsSubmissionErrorEvent(object):
    def __init__(self, config_data: ConfigData, agent_id: str, err: Exception):
        self.agentId = agent_id
        self.buildSessionId = config_data.buildSessionId
        self.appName = config_data.appName
        self.events = [
            {
                "type": AGENT_EVENT_TEST_SUBMIT_ERROR,
                "utcTimestamp_ms": get_utc_time_in_ms(),
                "data": str(err),
            }
        ]

    @property
    def message_type(self):
        return AGENT_EVENT_TEST_SUBMIT_ERROR
