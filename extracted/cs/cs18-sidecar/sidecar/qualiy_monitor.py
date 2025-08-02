import datetime
import threading
from logging import Logger
from timeit import default_timer as timer
from time import sleep

from retrying import retry

from sidecar.app_instance_service import IAppInstanceService
from sidecar.status_maintainer import StatusMaintainer


class QualiyMonitor:
    SAMPLE_INTERVAL = 10

    def __init__(self,
                 status_maintainer: StatusMaintainer,
                 app_instance_service: IAppInstanceService,
                 logger: Logger):
        self._status_maintainer = status_maintainer
        self._app_instance_service = app_instance_service
        self._logger = logger
        self._lock = threading.RLock()
        self._thread = None

    def start(self):
        with self._lock:
            if not self._thread or not self._thread.is_alive():
                self._thread = threading.Thread(target=self.sampling_loop, daemon=True)
                self._thread.start()
            else:
                self._logger.warning('Sampling loop is already running')

    def sampling_loop(self):
        self._logger.info(f'Waiting for qualiy to be turned off ({self.SAMPLE_INTERVAL} sec intervals)')
        start = timer()
        iterations = 0
        while not self.is_qualiy_off():
            iterations += 1
            sleep(self.SAMPLE_INTERVAL)

        duration = datetime.timedelta(seconds=timer()-start)
        self._logger.info(f'Qualiy is off (took {duration}, and {iterations} valid iterations)')
        try:
            self._status_maintainer.update_qualiy_status('off')
        except:
            self._logger.exception('Failed to set qualiy status "off"')

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=1000*60*30)  # Exponential Backoff, starts from 1 sec to 30 min
    def is_qualiy_off(self) -> bool:
        try:
            return self._app_instance_service.is_qualiy_off()
        except:
            self._logger.warning('Failed to get qualiy instance power status', exc_info=True)
            raise
