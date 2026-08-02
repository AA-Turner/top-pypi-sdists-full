import functools
import urllib2

from python_agent.common import constants
from python_agent.test_listener.state_tracker import StateTracker


class Urllib2Patcher(object):
    def __init__(self, config_data):
        self.config_data = config_data

    def patch(self):
        urllib2.Request.__init__ = self.handle_urllib2(urllib2.Request.__init__)

    def handle_urllib2(self, f):
        @functools.wraps(f)
        def inner_handle(self, *args, **kwargs):
            f(self, *args, **kwargs)
            if StateTracker().current_test_identifier:
                self.headers[constants.TEST_IDENTIFIER] = (
                    StateTracker().current_test_identifier
                )

        return inner_handle
