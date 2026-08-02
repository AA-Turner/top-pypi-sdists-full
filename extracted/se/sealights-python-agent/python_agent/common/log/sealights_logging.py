import logging
import sys
import traceback

from python_agent.build_scanner.entities.environment_data import EnvironmentData
from python_agent.common import constants
from python_agent.common.http.backend_proxy import BackendProxy
from python_agent.common.schduler.scheduler import SchedulerManager
from python_agent.test_listener.entities.logs_request import LogsRequest


class SealightsHTTPHandler(logging.Handler):
    def __init__(self, config_data, capacity=50):
        logging.Handler.__init__(self)
        self.capacity = capacity
        self.buffer = []
        self.backend_proxy = BackendProxy(config_data)
        self.config_data = config_data
        self.environment = EnvironmentData(
            config_data.labId, config_data.testStage, config_data.testGroupId
        )
        self.environment.environmentName = config_data.labId
        self.watchdog = SchedulerManager()
        self.watchdog.add_job(self.flush, constants.INTERVAL_IN_SECONDS)
        self.watchdog.start()

    def build_request(self, records):
        log = "\n".join(map(lambda record: self.format(record), records))
        return LogsRequest(
            self.config_data.customerId,
            self.config_data.appName,
            self.config_data.branchName,
            self.config_data.buildName,
            self.environment,
            log,
        )

    def should_flush(self, record):
        """
        Should the handler flush its buffer?

        Returns true if the buffer is up to capacity. This method can be
        overridden to implement custom flushing strategies.
        """
        return len(self.buffer) >= self.capacity

    def flush(self):
        """
        Override to implement custom flushing behaviour.

        This version just zaps the buffer to empty.
        """
        self.acquire()
        try:
            logs_request = self.build_request(self.buffer)
            self.backend_proxy.submit_logs(self.config_data, logs_request)
        except Exception:
            self.handle_exception()
        finally:
            self.buffer = []
            self.release()

    def emit(self, record):
        try:
            self.buffer.append(record)
        except Exception:
            self.handleError(record)

    def close(self):
        try:
            self.flush()
            self.watchdog.shutdown()
        except Exception:
            self.handle_exception()
        finally:
            logging.Handler.close(self)

    def handle_exception(self):
        if logging.raiseExceptions and sys.stderr:  # see issue 13807
            ei = sys.exc_info()
            try:
                traceback.print_exception(ei[0], ei[1], ei[2], None, sys.stderr)
                sys.stderr.write("Failed Sending Logs to Server")
            except IOError:
                pass
            finally:
                del ei
