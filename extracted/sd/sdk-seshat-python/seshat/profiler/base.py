import cProfile
import inspect
import logging
import os
import pathlib
import pstats
import time
from dataclasses import dataclass, field
from io import StringIO
from pstats import Stats
from typing import Callable, List
from typing import Literal

from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.transport import HttpTransport
from memory_profiler import profile as mem_profile, memory_usage

from seshat.profiler.decorator import track
from seshat.utils.logger.cloudwatch_handler import CloudWatchHandler
from seshat.profiler.format import log_format, ConsoleFormatter, UTCFormatter
from seshat.transformer import Transformer
from seshat.utils.patching import patch

LogLevel = Literal[
    logging.INFO, logging.DEBUG, logging.WARNING, logging.ERROR, logging.CRITICAL
]


@dataclass
class MemProfileConfig:
    log_path: str | None
    enable: bool = True


@dataclass
class CProfileConfig:
    log_path: str | None
    enable: bool = True


@dataclass
class LogstashConfig:
    host: str = None
    port: int = None
    username: str = None
    password: str = None
    enable: bool = False
    ssl_enable: bool = True


@dataclass
class ProfileConfig:
    log_level: LogLevel
    log_dir: str = "./logs"
    job_id: str = "unknown"
    show_in_console: bool = True
    default_tracking: bool = True
    logstash_conf: LogstashConfig = field(
        default_factory=lambda: LogstashConfig(enable=False)
    )
    mem_profile_conf: MemProfileConfig = field(
        default_factory=lambda: MemProfileConfig(log_path=None, enable=False)
    )
    cprofile_conf: CProfileConfig = field(
        default_factory=lambda: CProfileConfig(log_path=None, enable=False)
    )


class Profiler:
    config: ProfileConfig

    _cprofile = None
    _logger: logging.Logger
    _mem_logs = StringIO()
    _tracked: List[Callable] = []
    _is_setup: bool = False

    def run(self, func: Callable, *args, **kwargs):
        if not self._is_setup:
            return func(*args, **kwargs)
        self._tracked.append(func)
        method_log = func.__qualname__
        try:
            self.log("info", msg=f"start {method_log}", method=func)
            if self.config.mem_profile_conf.enable:
                func = mem_profile(func, stream=self._mem_logs)

            init_mem_usage = memory_usage()[0]
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            final_mem_usage = memory_usage()[0]

            # Temporarily disable the cProfile profiler to extract data for
            # the specified function. Keeping the profiler enabled during stats
            # extraction can cause incomplete results, missing some function calls.
            self._cprofile.disable()
            time_spent = self.get_spent_time(func, self._cprofile)
            self._cprofile.enable()

            self.log(
                "info",
                msg=f"finish {method_log}",
                mem_changes=final_mem_usage - init_mem_usage,
                time_spent=time_spent,
                cumulative_time_spent=end - start,
                method=func,
            )
            return result

        except Exception as exc:
            self.log(
                "error", msg=f"error in {method_log}: {exc}", method=func, exc_info=True
            )
            self.tear_down()
            raise

    def tear_down(self):
        self._cprofile.disable()
        if not hasattr(self, "config"):
            return
        if self.config.mem_profile_conf.enable:
            self.save_mem_log()
        if self.config.cprofile_conf.enable:
            self.save_profile_log()

    def save_mem_log(self):
        self._mem_logs.seek(0)
        log_path = self.get_log_path(self.config.mem_profile_conf.log_path)
        # Ensure the directory exists
        self.ensure_dir_exists(os.path.dirname(log_path))
        with open(log_path, "w") as mem_file:
            mem_file.write(self._mem_logs.read())

    def save_profile_log(self):
        log_path = self.get_log_path(self.config.cprofile_conf.log_path)
        # Ensure the directory exists
        self.ensure_dir_exists(os.path.dirname(log_path))
        with open(log_path, "w") as stream:
            stats = Stats(self._cprofile)
            self.strip_cprofile(stats)
            stats.stream = stream
            stats.sort_stats("time").print_stats()

    def strip_cprofile(self, stats):
        tracked_functions = {
            self.get_func_path(f, with_number=True) for f in self._tracked
        }
        for key in list(stats.stats.keys()):
            func_name, line, func = key
            if f"{func_name}:{line}" in tracked_functions:
                new_key = (func_name.replace(self.seshat_path, ""), line, func)
                stats.stats[new_key] = stats.stats.pop(key)
            else:
                stats.stats.pop(key)

    def log(
        self,
        level,
        msg,
        method=None,
        exc_info=False,
        **extra,
    ):
        if not self._is_setup:
            return
        logger = getattr(self._logger, level, None)
        extra.setdefault("method_path", "")
        extra.setdefault("error", "")
        extra.setdefault("mem_changes", "")
        extra.setdefault("time_spent", "")
        extra.setdefault("cumulative_time_spent", "")
        extra.setdefault("log_source", self.config.job_id)
        extra.setdefault("tokens_out", "")
        extra.setdefault("tokens_in", "")
        if method:
            extra["method_path"] = self.get_func_path(method)
        return logger(msg=msg, extra=extra, exc_info=exc_info)

    @property
    def seshat_path(self):
        here = os.path.abspath(__file__)
        return os.path.dirname(os.path.dirname(here))

    def get_spent_time(self, func, cprofile):
        stat = pstats.Stats(cprofile)
        method = self.get_func_path(func, with_number=False)
        for k, info in stat.stats.items():
            if k[0] == method:
                return info[2]
        return None, None

    @staticmethod
    def get_func_path(func, with_number=True):
        source_path = inspect.getsourcefile(func)
        line_number = inspect.getsourcelines(func)[1]
        return f"{source_path}:{line_number}" if with_number else source_path

    @classmethod
    def setup_logging(cls, config: ProfileConfig):
        if getattr(cls, "_logger", None):
            return

        logger = logging.getLogger("seshat")
        logger.setLevel(config.log_level)

        run_in_container = (
            os.getenv("RUN_IN_CONTAINER", default="false").lower() == "true"
        )
        if run_in_container:
            config.show_in_console = False
            config.job_id = os.getenv("JOB_ID")
            config.logstash_conf = LogstashConfig(
                os.getenv("LOGSTASH_URL"),
                int(os.getenv("LOGSTASH_PORT", default=443)),
                os.getenv("LOGSTASH_USERNAME"),
                os.getenv("LOGSTASH_PASSWORD"),
                enable=True,
            )
        else:
            file_handler = logging.FileHandler(cls.get_log_path("event.txt"))
            file_handler.setFormatter(UTCFormatter(log_format))
            logger.addHandler(file_handler)

        if config.show_in_console:
            console = logging.StreamHandler()
            console.setLevel(level=config.log_level)
            console.setFormatter(ConsoleFormatter())
            logging.getLogger(__name__).addHandler(console)

        if config.logstash_conf.enable:
            transport = HttpTransport(
                host=config.logstash_conf.host,
                port=config.logstash_conf.port,
                ssl_enable=config.logstash_conf.ssl_enable,
                username=config.logstash_conf.username,
                password=config.logstash_conf.password,
            )
            logstash = AsynchronousLogstashHandler(
                host=config.logstash_conf.host,
                port=config.logstash_conf.port,
                transport=transport,
                database_path="/tmp/logstash.db",
            )
            logstash.setFormatter(UTCFormatter(log_format))
            logging.getLogger(__name__).addHandler(logstash)

        # AWS CloudWatch Logs handler
        if os.getenv("AWS_LOGGING", "false").lower() == "true":
            try:
                pipeline_name = os.getenv("HEISENBERG_JOB_NAME", "unknown")

                cloudwatch_handler = CloudWatchHandler(
                    log_group=f"/heisenberg/pipelines/{pipeline_name}",
                    region=os.getenv("AWS_REGION", "us-east-1"),
                    retention_days=int(os.getenv("AWS_LOG_RETENTION_DAYS", "7")),
                )
                cloudwatch_handler.setFormatter(UTCFormatter(log_format))
                logging.getLogger(__name__).addHandler(cloudwatch_handler)
            except Exception as e:
                print(f"Failed to initialize CloudWatch handler: {e}")

        cls._logger = logging.getLogger(__name__)

    @classmethod
    def track_default_methods(cls):
        seshat_directory = pathlib.Path(__file__).parent.parent.resolve()
        cls.track_method(
            f"{seshat_directory}/transformer",
            "seshat.transformer.",
            {"__call__"},
            lambda klass, attr_name: issubclass(klass, Transformer)
            and attr_name.startswith(klass.HANDLER_NAME),
        )
        cls.track_method(
            f"{seshat_directory}/source",
            "seshat.source.",
            {"fetch", "save", "insert", "update", "copy", "create_table"},
        )
        cls.track_method(
            f"{seshat_directory}/data_class", "seshat.data_class.", {"convert"}
        )

    @classmethod
    def setup(cls, config: ProfileConfig):
        if config.log_dir:
            cls.ensure_dir_exists(config.log_dir)
        if config.default_tracking:
            cls.track_default_methods()
        cls.config = config
        cls.setup_logging(config)
        cls._cprofile = cProfile.Profile()
        cls._cprofile.enable()
        cls._is_setup = True

    @staticmethod
    def ensure_dir_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @classmethod
    def get_log_path(cls, filename):
        return os.path.join(cls.config.log_dir, filename)

    @staticmethod
    def track_method(dirname, prefix, to_track, condition: Callable = lambda *_: False):
        return patch(track, **locals())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tear_down()


profiler = Profiler()
