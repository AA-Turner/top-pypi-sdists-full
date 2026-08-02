from python_agent.test_listener.managers.agent_manager import AgentManager


class SeaLightsAPI:
    @staticmethod
    def create_execution_id():
        return AgentManager().create_execution_id()

    @staticmethod
    def start_execution(execution_id):
        AgentManager().start_execution(execution_id)

    @staticmethod
    def end_execution(execution_id):
        AgentManager().end_execution(execution_id)

    @staticmethod
    def create_test_id(execution_id, test_name):
        if not execution_id or not test_name:
            return ""
        return execution_id + "/" + test_name

    @staticmethod
    def push_event(event):
        AgentManager().push_event(event)

    @staticmethod
    def set_current_test_identifier(test_identifier):
        AgentManager().state_tracker.set_current_test_identifier(test_identifier)

    @staticmethod
    def get_current_test_identifier():
        return AgentManager().state_tracker.current_test_identifier

    @staticmethod
    def notify_test_start(execution_id, test_name, external_id=""):
        test_identifier = SeaLightsAPI.create_test_id(execution_id, test_name)
        if AgentManager().config_data.perTest:
            SeaLightsAPI.set_current_test_identifier(test_identifier)
        event = {
            "type": "testStart",
            "externalId": external_id,
            "testName": test_name,
            "testPath": None,
            "executionId": execution_id,
        }
        SeaLightsAPI.push_event(event)

    @staticmethod
    def notify_test_end(execution_id, test_name, duration, result, external_id=""):
        event = {
            "type": "testEnd",
            "testName": test_name,
            "testPath": None,
            "executionId": execution_id,
            "result": result,
            "externalId": external_id,
            "duration": duration * 1000,  # TODO maybe remove "* 1000"
        }
        SeaLightsAPI.push_event(event)

    @staticmethod
    def send_all():
        AgentManager().send_all()

    @staticmethod
    def get_excluded_tests():
        return AgentManager().get_excluded_tests()
