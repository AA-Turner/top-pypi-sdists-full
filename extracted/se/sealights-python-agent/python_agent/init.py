import sys
import threading

from python_agent import admin, utils
from python_agent.test_listener.managers.agent_manager import AgentManager


def init():
    try:
        admin.init()
    except SystemExit:
        if tuple(sys.version_info) >= (3, 0):
            threading.current_thread = utils.trace(
                threading.current_thread, AgentManager().get_trace_function()
            )
        else:
            threading.currentThread = utils.trace(
                threading.currentThread, AgentManager().get_trace_function()
            )


if "uwsgi" in sys.modules:
    import uwsgidecorators

    @uwsgidecorators.postfork
    def init_agent():
        init()


init()
