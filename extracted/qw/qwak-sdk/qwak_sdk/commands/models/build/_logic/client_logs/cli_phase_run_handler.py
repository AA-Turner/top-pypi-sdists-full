from contextlib import contextmanager
from logging import Logger
from pathlib import Path

from qwak.inner.build_logic.interface.build_phase import BuildPhase
from qwak.inner.build_logic.interface.phase_run_handler import PhaseRunHandler
from qwak.inner.build_logic.phases.phases_pipeline import PhasesPipeline
from yaspin import yaspin

from qwak_sdk.tools.colors import Color
from .cli_trigger_build_logger import CliTriggerBuildLogger
from .messages import (
    FAILED_CONTACT_QWAK_SUPPORT,
)
from .utils import zip_logs


class CLIPhaseRunHandler(PhaseRunHandler):
    BUILD_IN_PROGRESS_FORMAT = "Build phase in progress: {}"
    BUILD_FINISHED_FORMAT = "Phase successfully finished: {} after {} seconds"
    KEYBOARD_INTERRUPT_FORMAT = "\n{color}Stopping Qwak build (ctrl-c)"
    BUILD_FAILURE_FORMAT = "Build phase failed: {} after {} seconds"
    PIPELINE_ERROR = "\n{color}{ex}"
    SPINNER_FINISH = "✅"
    SPINNER_FAIL = "💥"
    SPINNER_OK = "‼️"

    def __init__(self, python_logger: Logger, log_path: Path, verbose: int, json_logs: bool):
        self.sp = None
        self.build_logger = None
        self.log_path = str(log_path)
        self.python_logger = python_logger
        self.json_logs = json_logs
        self.verbose = verbose

    @contextmanager
    def handle_current_phase(self, phase: PhasesPipeline):
        build_logger = CliTriggerBuildLogger(
            self.python_logger,
            prefix="" if self.json_logs else phase.build_phase.description,
            build_phase=phase.build_phase,
        )
        show = (self.verbose == 0 and not self.json_logs)
        text = phase.build_phase.description
        if show:
            with yaspin(text=text, color="blue", timer=True).bold as sp:
                self.sp = sp
                build_logger.set_spinner(sp)
                self.build_logger = build_logger
                yield
        else:
            self.build_logger = build_logger
            yield

    def handle_phase_in_progress(self, build_phase: BuildPhase):
        logger = self.build_logger or self.python_logger
        logger.debug(
            self.BUILD_IN_PROGRESS_FORMAT.format(build_phase.name)
        )

    def handle_phase_finished_successfully(
        self, build_phase: BuildPhase, duration_in_seconds: int
    ):
        if self.sp:
            self.sp.ok(self.SPINNER_FINISH)

        logger = self.build_logger or self.python_logger
        logger.debug(
            self.BUILD_FINISHED_FORMAT.format(build_phase.name, duration_in_seconds))

    def _report_failure(self, build_phase: BuildPhase, duration_in_seconds: int):
        logger = self.build_logger or self.python_logger
        logger.debug(
            self.BUILD_FAILURE_FORMAT.format(build_phase.name, duration_in_seconds))

    def handle_contact_support_error(
        self, build_id: str, build_phase: BuildPhase, ex: BaseException, duration_in_seconds: int
    ):
        print(f"\n{ex}\n{FAILED_CONTACT_QWAK_SUPPORT.format(build_id=build_id, log_file=Path(self.log_path).parent / build_id)}")
        zip_logs(log_path=self.log_path, build_id=build_id)
        self._report_failure(build_phase, duration_in_seconds)
        exit(1)

    def handle_remote_build_error(
        self, build_id: str, build_phase: BuildPhase, ex: BaseException, duration_in_seconds: int
    ):
        if self.sp:
            self.sp.fail(self.SPINNER_FAIL)
            print(self.PIPELINE_ERROR.format(color=Color.RED, ex=ex))
        else:
            print(f"\n{ex}")
        self._report_failure(build_phase, duration_in_seconds)
        exit(1)

    def handle_keyboard_interrupt(
        self, build_id: str, build_phase: BuildPhase, duration_in_seconds: int
    ):
        print(self.KEYBOARD_INTERRUPT_FORMAT.format(color=Color.RED))
        zip_logs(log_path=self.log_path, build_id=build_id)
        self._report_failure(build_phase, duration_in_seconds)
        exit(1)

    def handle_pipeline_exception(
        self, build_id: str, build_phase: BuildPhase, ex: BaseException, duration_in_seconds: int
    ):
        if self.sp:
            self.sp.fail("💥")
            print(f"\n{Color.RED}{ex}")
        zip_logs(
            log_path=self.log_path,
            build_id=build_id,
        )
        self._report_failure(build_phase, duration_in_seconds)
        exit(1)

    def handle_pipeline_quiet_exception(
        self, build_id: str, build_phase: BuildPhase, ex: BaseException, duration_in_seconds: int
    ):
        if self.sp:
            self.sp.ok(self.SPINNER_OK)
            print(self.PIPELINE_ERROR.format(color=Color.RED, ex=ex))
        self._report_failure(build_phase, duration_in_seconds)
        exit(1)
