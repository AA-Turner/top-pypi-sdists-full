from datetime import datetime
from metaflow.decorators import StepDecorator
from ...profilers.gpu import GPUProfiler  # Fix import
from .deco_injector import CardDecoratorInjector
import threading


class GPUProfileDecorator(StepDecorator):
    name = "gpu_profile"

    defaults = {
        "include_artifacts": True,
        "artifact_prefix": "gpu_profile_",
        "interval": 1,
    }

    def step_init(
        self, flow, graph, step_name, decorators, environment, flow_datastore, logger
    ):
        self.deco_injector = CardDecoratorInjector()
        self.deco_injector.attach_card_decorator(
            flow,
            step_name,
            "gpu_profile",
            "blank",
            refresh_interval=self.attributes["interval"],
        )

    def task_pre_step(
        self,
        step_name,
        task_datastore,
        metadata,
        run_id,
        task_id,
        flow,
        graph,
        retry_count,
        max_user_code_retries,
        ubf_context,
        inputs,
    ):
        self._profiler = GPUProfiler(
            interval=self.attributes["interval"],
            artifact_name=self.attributes["artifact_prefix"] + "data",
        )

    def task_decorate(
        self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context
    ):
        from metaflow import current
        from metaflow.cards import Markdown

        if self.attributes["include_artifacts"]:
            setattr(
                flow,
                self.attributes["artifact_prefix"] + "num_gpus",
                len(self._profiler.devices),
            )

        current.card["gpu_profile"].append(
            Markdown("# GPU profile for `%s`" % current.pathspec)
        )
        current.card["gpu_profile"].append(
            Markdown(
                "_Started at: %s_"
                % datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S %z")
            )
        )
        self._profiler._setup_card()
        current.card["gpu_profile"].refresh()
        self._update_thread = threading.Thread(
            target=self._profiler._update_card, daemon=True
        )
        self._update_thread.start()

        def wrapped_step_func():
            try:
                step_func()
            finally:
                try:
                    results = self._profiler.finish()
                except:
                    results = {"error": "couldn't read profiler results"}
                if self.attributes["include_artifacts"]:
                    setattr(flow, self.attributes["artifact_prefix"] + "data", results)

        return wrapped_step_func
