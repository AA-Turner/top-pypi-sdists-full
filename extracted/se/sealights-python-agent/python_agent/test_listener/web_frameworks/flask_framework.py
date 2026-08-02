import functools
import logging

from python_agent import admin
from python_agent.common import constants
from python_agent.test_listener.state_tracker import StateTracker

log = logging.getLogger(__name__)


def bootstrap_init(init_method):
    @functools.wraps(init_method)
    def inner_bootstrap(self, *args, **kwargs):
        init_method(self, *args, **kwargs)
        try:
            admin.bootstrap()
        except SystemExit as e:
            if getattr(e, "code", 1) != 0:
                log.exception(
                    "Failed Initializing Agent. Error: %s" % getattr(e, "message", "")
                )
        self.before_request(before_request)

    return inner_bootstrap


def before_request():
    try:
        from flask import request

        test_identifier = request.headers.get(constants.TEST_IDENTIFIER)
        if test_identifier:
            StateTracker().set_current_test_identifier(test_identifier)
    except ImportError as e:
        log.warning("Failed To Import Flask request. Error: %s" % str(e))


def bootstrap():
    try:
        from flask import Flask

        Flask.__init__ = bootstrap_init(Flask.__init__)
        log.info("Bootstrapped Flask Init Method")
    except ImportError as e:
        log.warning("Failed To Import Flask. Error: %s" % str(e))
