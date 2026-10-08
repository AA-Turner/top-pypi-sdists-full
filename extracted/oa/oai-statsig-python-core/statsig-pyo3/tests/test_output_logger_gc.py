import gc
import weakref

from statsig_python_core import (
    OutputLoggerProvider,
    SpecAdapterConfig,
    Statsig,
    StatsigOptions,
)


class CollectingLogger(OutputLoggerProvider):
    def __init__(self):
        super().__init__()
        self.collect_on_warning = False
        self.in_warning = False
        self.collected = None
        self.shutdowns = 0
        self.shutdown_during_warning = False

    def warn(self, tag, message):
        if not self.collect_on_warning:
            return
        self.collect_on_warning = False
        self.in_warning = True
        try:
            self.collected = gc.collect()
        finally:
            self.in_warning = False

    def shutdown(self):
        self.shutdowns += 1
        self.shutdown_during_warning |= self.in_warning


def test_collecting_retired_sdk_in_logger_callback_completes_shutdown():
    gc.collect()
    automatic_gc = gc.isenabled()
    gc.disable()
    logger = CollectingLogger()
    options = StatsigOptions(
        disable_network=True,
        disable_all_logging=True,
        output_log_level="warn",
        output_logger_provider=logger,
        spec_adapter_configs=[
            SpecAdapterConfig("network_http", specs_url="http://127.0.0.1:1/specs")
        ],
    )
    current = None
    try:
        retired = Statsig("secret-offline-logger-test", options)
        retired.shutdown().wait()
        retired_ref = weakref.ref(retired)
        # Model an SDK retained by a Python cycle until the next logger callback.
        cycle = [retired]
        cycle.append(cycle)
        del retired, cycle

        current = Statsig("secret-offline-logger-test", options)
        shutdowns_before_warning = logger.shutdowns
        logger.collect_on_warning = True
        current.initialize_with_details().result()

        assert logger.collected is not None and logger.collected > 0
        assert retired_ref() is None
        assert logger.shutdowns == shutdowns_before_warning + 1
        assert not logger.shutdown_during_warning
    finally:
        if current is not None:
            current.shutdown().wait()
            del current
        gc.collect()
        if automatic_gc:
            gc.enable()
