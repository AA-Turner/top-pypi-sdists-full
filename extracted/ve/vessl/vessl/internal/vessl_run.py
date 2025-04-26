import os
import re
import sys
import threading
import time
from typing import Any, Dict, List, Optional, Union

from urllib3.exceptions import MaxRetryError

from openapi_client.models.experiment_metric_entry import ExperimentMetricEntry
from openapi_client.models.experiment_metrics_update_api_input import (
    ExperimentMetricsUpdateAPIInput,
)
from openapi_client.models.response_experiment_info import ResponseExperimentInfo
from openapi_client.models.run_execution_metrics_update_api_input import (
    RunExecutionMetricsUpdateAPIInput,
)
from openapi_client.models.v1_plot_entry import V1PlotEntry
from vessl.internal.collector import (
    Collector,
    RunExecutionMetricCollector,
    UserMetricCollector,
)
from vessl.internal.progress_updater import ExecutionProgressUpdater, ProgressUpdater
from vessl.internal.vessl_hyperparameters import (
    HyperparametersController,
)
from vessl.util import constant, logger
from vessl.util.api import VesslApi
from vessl.util.audio import Audio
from vessl.util.constant import (
    VESSL_MEDIA_PATH,
    VESSL_PLOTS_FILETYPE_AUDIO,
    VESSL_PLOTS_FILETYPE_IMAGE,
)
from vessl.util.exception import (
    InvalidTypeError,
    VesslApiException,
    suppress_sdk_exception,
)
from vessl.util.file_watch import WatchJWT
from vessl.util.image import Image

MODE_TEST = "TEST"
MODE_NOT_STARTED = "NOT_STARTED"
MODE_MANAGED = "MANAGED"

SEND_INTERVAL_IN_SEC = 10

METRIC_KEY_REGEX = re.compile("^[a-zA-Z0-9/_-]+$")


class Sender(object):
    def __init__(self, api: VesslApi, experiment_id: int, collectors: List[Collector]):
        self._api = api
        self._experiment_id: int = experiment_id
        self._thread = threading.Thread(target=self._thread_body, daemon=True)
        self._exit = threading.Event()
        self._collectors = collectors

    def stop(self):
        for c in self._collectors:
            c.stop()

        self._exit.set()
        self._thread.join()

    def start(self):
        for c in self._collectors:
            c.start()
        self._thread.start()

    def _thread_body(self):
        while not self._exit.is_set():
            self._send()
            self._exit.wait(timeout=SEND_INTERVAL_IN_SEC)
        self._send()

    def _send(self):
        pairs = [(c, c.collect()) for c in self._collectors]
        for c, m in pairs:
            logger.debug(f"{c} / {m}", str(c), len(m))
        payload = [m for _, metrics in pairs for m in metrics]
        logger.debug(f"Sending {len(payload)} payloads")

        try:
            res = self._api.experiment_metrics_update_api(
                self._experiment_id,
                experiment_metrics_update_api_input=ExperimentMetricsUpdateAPIInput(
                    metrics=payload
                ),
            )
            if res.rejected:
                logger.warning(f"{res.rejected} payloads(s) were rejected.")

            for c, m in pairs:
                c.truncate(len(m))

        except (MaxRetryError, VesslApiException) as e:
            logger.exception("Failed to send metrics to server", exc_info=e)
        except Exception as e:
            logger.exception("Unexpected error", exc_info=e)


class VesslRun(object):
    class ExitHook(object):
        def __init__(self, orig_exit):
            self.orig_exit = orig_exit
            self.exit_code = 0

        def exit(self, code=0):
            self.exit_code = code
            self.orig_exit(code)

    __slots__ = [
        "api",
        "_mode",
        "_collectors",
        "_sender",
        "_progress_updater",
        "hyperparameters",
        "_experiment",
        "_execution",
        "_execution_volume_id",
        "_logger",
        "_user_metric_collector",
        "_run_execution_metric_collector",
        "_exit_hook",
        "_tensorboard_collector",
    ]

    def __init__(self) -> None:
        self.api = VesslApi()

        self._experiment = None
        self._execution = None

        if self.api.is_in_run_exec_context():
            self._execution = True
            self.hyperparameters = None
            self._mode = MODE_MANAGED
            self._set_plot_volume_id()
            self._run_execution_metric_collector = RunExecutionMetricCollector()

            w = WatchJWT(
                path=constant.VESSL_JWT_DIR, logger=logger, callback_function=self._update_jwt
            )
            t = threading.Thread(name="child process", target=w.run, daemon=True)
            t.start()
        else:
            self._experiment = self._get_experiment_from_environment()
            self.hyperparameters = HyperparametersController(self.api, self._experiment)
            self._mode = MODE_NOT_STARTED if self._experiment is None else MODE_MANAGED
            self._user_metric_collector = UserMetricCollector()

        self._exit_hook = self.ExitHook(sys.exit)

    def _set_plot_volume_id(self) -> bool:
        """
        also provides the plot volume id
        """
        try:
            self._execution_volume_id = self.api.run_execution_get_plot_volume_api().volume_id
            return True
        except:
            return False

    def _update_jwt(self, refreshed_token):
        logger.debug("update_jwt to", refreshed_token)
        self.api.reconfigure_access_token_on_jwt_refresh(refreshed_token)

    def _get_experiment_from_environment(self) -> Optional[ResponseExperimentInfo]:
        """Detect experiment from environment variables

        In a Vessl-managed experiment, these variables will be defined.
        """
        experiment_id = os.environ.get("VESSL_EXPERIMENT_ID", None)
        access_token = os.environ.get("VESSL_ACCESS_TOKEN", None)

        if experiment_id is None or access_token is None:
            return None

        self.api.configure_access_token(access_token)
        try:
            return self.api.experiment_read_by_idapi(experiment_id=experiment_id)
        except VesslApiException:
            return None

    def _signal_handler(self, signo, frames):
        sys.exit(130)  # job was terminated by the owner

    def _send_without_collector(self, payloads):
        """Send metrics without using the collector

        In a Vessl-managed experiment, metrics are sent immediately instead of being queued.
        """
        assert self._mode == MODE_MANAGED
        res = self.api.experiment_metrics_update_api(
            self._experiment.id,
            experiment_metrics_update_api_input=ExperimentMetricsUpdateAPIInput(metrics=payloads),
        )
        if res.rejected:
            logger.warning(f"{res.rejected} payloads(s) were rejected.")

    def _send_without_collector_execution(self, payloads):
        """Send metrics without using the collector

        In a Vessl-managed execution, metrics are sent immediately instead of being queued.
        """
        assert self._mode == MODE_MANAGED
        res = self.api.run_execution_metrics_update_api(
            run_execution_metrics_update_api_input=RunExecutionMetricsUpdateAPIInput(
                metrics=payloads
            ),
        )
        if res.rejected:
            logger.warning(f"{res.rejected} payloads(s) were rejected.")

    def init(
        self,
        message: str = None,
        hp: dict = None,
        **kwargs,
    ):
        """Main function to setup Vessl in a local setting

        If this is a Vessl-managed experiment or vessl.init has already been called,
        this will do nothing.

        Args:
            message (str): experiment message
            hp (dict): hyperparameters
        """
        logger.warning("vessl.init() will be deprecated. Use VESSL Run instead.")

        if self._execution:
            print("Connected to VESSL Run.")
            return

        if self._mode == MODE_MANAGED:
            if hp is not None:
                self.hyperparameters.update(hp)

            if message is not None and self._experiment.message != message:
                from vessl.experiment import update_experiment

                self._experiment = update_experiment(
                    self._experiment.number,
                    message=message,
                    organization_name=self._experiment.organization.name,
                    project_name=self._experiment.project.name,
                )
                logger.debug(f'Updated experiment.message to: "{message}"')
            else:
                logger.debug(
                    f'Connected to experiment #{self._experiment.number}. Message: "{self._experiment.message}"'
                )

    def finish(self):
        logger.warning("vessl.finish() will be deprecated. Use VESSL Run instead.")
        return

    @suppress_sdk_exception
    def log(
        self,
        payload: Dict[str, Any],
        step: Optional[int] = None,
        ts: Optional[float] = None,
    ):
        """Log metrics to Vessl

        Args:
            payload (Dict[str, Any]): to log a scalar, value should be a number. To
                log an image, pass a single image or a list of images (type `vessl.util.image.Image`).
            step (int): step.
        """
        if self._execution:
            if self._mode == MODE_NOT_STARTED:
                logger.warning("Invalid usage. This method is only available in VESSL managed environment.")
                return
            if ts is None:
                ts = time.time()

            log_dict = {}
            scalar_dict = {}
            media_dict = {}

            for k, v in payload.items():
                if isinstance(v, list):
                    if all(isinstance(i, Image) for i in v) or all(isinstance(i, Audio) for i in v):
                        media_dict[k] = v
                elif isinstance(v, Image) or isinstance(v, Audio):
                    media_dict[k] = [v]
                elif isinstance(v, int) or isinstance(v, float):
                    scalar_dict[k] = v
                elif isinstance(v, str):
                    log_dict[k] = v
                else:
                    try:
                        scalar_dict[k] = float(v)
                    except ValueError:
                        logger.error(
                            f"Could not convert '{type(v).__name__}' {v} to float. "
                            f"(allowed types: Image, Audio, int, float, str)"
                        )

            if scalar_dict or step is not None:
                self._run_execution_metric_collector.handle_step(step)

            if media_dict:
                self._update_media_execution(media_dict, ts, self._execution_volume_id, step)

            if scalar_dict:
                self._update_metrics_execution(scalar_dict, ts)

            if log_dict:
                self._update_logs_execution(log_dict, ts)

        if self._experiment is not None:
            if self._mode == MODE_NOT_STARTED:
                logger.warning("Invalid usage. This method is only available in VESSL managed environment.")
                return

            if ts is None:
                ts = time.time()

            scalar_dict = {}
            media_dict = {}

            for k, v in payload.items():
                if isinstance(v, list):
                    if all(isinstance(i, Image) for i in v) or all(isinstance(i, Audio) for i in v):
                        media_dict[k] = v
                elif isinstance(v, Image) or isinstance(v, Audio):
                    media_dict[k] = [v]
                elif isinstance(v, int) or isinstance(v, float):
                    scalar_dict[k] = v
                else:
                    try:
                        scalar_dict[k] = float(v)
                    except ValueError:
                        logger.error(
                            f"Could not convert '{type(v).__name__}' {v} to float. "
                            f"(allowed types: Image, Audio, int, float)"
                        )

            # Update step if step is specified. If a scalar is defined but step wasn't,
            # step will be autoincremented.
            if scalar_dict or step is not None:
                self._user_metric_collector.handle_step(step)

            if media_dict:
                self._update_media(media_dict, ts)

            if scalar_dict:
                self._update_metrics(scalar_dict, ts)

    # This should mirror app/influx/metric_schema.go > `isValidMetricKey`
    def _is_metric_key_valid(self, key: str):
        if not METRIC_KEY_REGEX.match(key):
            return False
        if key.startswith("/") or key.endswith("/"):
            return False
        for i in range(1, len(key)):
            if key[i] == "/" and key[i - 1] == "/":
                return False
        return True

    def _update_metrics(self, payload: Dict[str, Any], ts: float):
        invalid_keys = [k for k in payload.keys() if not self._is_metric_key_valid(k)]
        if invalid_keys:
            logger.warning(
                f"Invalid metric keys: {' '.join(invalid_keys)}. This payload will be rejected."
            )

        payloads = [self._user_metric_collector.build_metric_payload(payload, ts)]
        if self._mode == MODE_MANAGED:
            self._send_without_collector(payloads)
            return self._user_metric_collector.step
        return self._user_metric_collector.log_metrics(payloads)

    def _update_media(
        self,
        payload: Dict[str, Union[List[Image], List[Audio]]],
        ts: float,
    ):
        media_type, set_media_type = None, False
        path_to_caption = {}
        for media in payload.values():
            for medium in media:
                path = os.path.basename(medium.path)
                path_to_caption[path] = medium.caption
                if not set_media_type:
                    if not isinstance(medium, Image) and not isinstance(medium, Audio):
                        raise InvalidTypeError(f"Invalid payload type error: {type(medium)}")
                    else:
                        media_type = type(medium).__name__
                        set_media_type = True

        from vessl.volume import copy_volume_file

        files = copy_volume_file(
            source_volume_id=None,
            source_path=os.path.join(VESSL_MEDIA_PATH, "."),
            dest_volume_id=self._experiment.experiment_plot_volume,
            dest_path="/",
        )

        for media in payload.values():
            for medium in media:
                medium.flush()

        plot_files = []
        if files:
            plot_files = [
                {
                    "step": None,
                    "path": file.get("path"),
                    "caption": path_to_caption[file.get("path")],
                    "timestamp": ts,
                }
                for file in files
                if file.get("path") in path_to_caption
            ]

        payloads: List[ExperimentMetricEntry] = []
        for f in plot_files:
            payload = {}
            if media_type == Image.__name__:
                payload = {VESSL_PLOTS_FILETYPE_IMAGE: f}
            elif media_type == Audio.__name__:
                payload = {VESSL_PLOTS_FILETYPE_AUDIO: f}
            payloads.append(self._user_metric_collector.build_media_payload(payload, ts))

        if self._mode == MODE_MANAGED:
            self._send_without_collector(payloads)
        else:
            self._user_metric_collector.log_media(payloads)

    def _update_logs_execution(self, log_dict: Dict[str, Any], ts: float):
        payload = V1PlotEntry(
            measurement="log",
            ts=ts,
            tags=None,
            fields=log_dict,
        )
        payloads = [payload]
        self._send_without_collector_execution(payloads)

    def _update_metrics_execution(self, payload: Dict[str, Any], ts: float):
        invalid_keys = [k for k in payload.keys() if not self._is_metric_key_valid(k)]
        if invalid_keys:
            logger.warning(
                f"Invalid metric keys: {' '.join(invalid_keys)}. This payload will be rejected."
            )

        payloads = [self._run_execution_metric_collector.build_metric_payload(payload, ts)]
        if self._mode == MODE_MANAGED:
            self._send_without_collector_execution(payloads)
            return self._run_execution_metric_collector.step
        return self._run_execution_metric_collector.log_metrics(payloads)

    def _update_media_execution(
        self,
        payload: Dict[str, Union[List[Image], List[Audio]]],
        ts: float,
        volume_id: int,
        step: Optional[int] = None,
    ):
        media_type, set_media_type = None, False
        path_to_caption = {}
        for media in payload.values():
            for medium in media:
                if media_type is not None and media_type != type(medium).__name__:
                    raise InvalidTypeError(f"Invalid multiple payload type error: {type(medium)}")

                path = os.path.basename(medium.path)
                if medium.caption == "" or medium.caption is None:
                    path_to_caption[path] = path
                else:
                    path_to_caption[path] = medium.caption

                if not set_media_type:
                    if not isinstance(medium, Image) and not isinstance(medium, Audio):
                        raise InvalidTypeError(f"Invalid payload type error: {type(medium)}")
                    else:
                        media_type = type(medium).__name__
                        set_media_type = True

        from vessl.volume import copy_volume_file

        files = copy_volume_file(
            source_volume_id=None,
            source_path=os.path.join(VESSL_MEDIA_PATH, "."),
            dest_volume_id=volume_id,
            dest_path="/",
        )

        for media in payload.values():
            for medium in media:
                medium.flush()

        plot_files = []
        if files:
            plot_files = [
                {
                    "step": step,
                    "dest_path": file.get("path"),
                    "caption": path_to_caption[file.get("path")],
                }
                for file in files
                if file.get("path") in path_to_caption
            ]

        payloads: List[V1PlotEntry] = []
        for f in plot_files:
            payload = {}
            if media_type == Image.__name__:
                payload = {VESSL_PLOTS_FILETYPE_IMAGE: f}
            elif media_type == Audio.__name__:
                payload = {VESSL_PLOTS_FILETYPE_AUDIO: f}
            payloads.append(self._run_execution_metric_collector.build_media_payload(payload, ts))

        if self._mode == MODE_MANAGED:
            self._send_without_collector_execution(payloads)
        else:
            self._run_execution_metric_collector.log_media(payloads)

    @suppress_sdk_exception
    def progress(self, value: Union[float, int]):
        """Update experiment or execution progress

        Args:
            value (float): progress value as a decimal between 0 and 1
            value (int): progress value for execution between 0 and 1
        """
        if self._execution is None and self._experiment is None:
            logger.warning("Invalid usage. This method is only available in VESSL managed environment.")
            return

        if type(value) == float and not 0 < value <= 1:
            logger.warning(f"Invalid progress value {value}. (0 < value <= 1)")
            return
        if type(value) == int and not 0 < value <= 100:
            logger.warning(f"Invalid progress value {value}. (0 < value <= 100)")
            return

        # Do not initialize in init() since ProgressUpdater might not be used at all
        if self._execution:
            if not hasattr(self, "_progress_updater"):
                self._progress_updater = ExecutionProgressUpdater(self.api)
                self._progress_updater.start()

            if type(value) == float:
                value = int(value * 100)
            self._progress_updater.update(value)
            logger.debug(f"Run progress: {value}")

        if self._experiment is not None:
            if not hasattr(self, "_progress_updater"):
                self._progress_updater = ProgressUpdater(self.api, self._experiment.id)
                self._progress_updater.start()

            self._progress_updater.update(value)
            logger.debug(f"Experiment progress: {value}")
