import os
import time
from metaflow import current
from .utils import get_storage_path, NIM_MONITOR_LOCAL_STORAGE_ROOT
from .nim_manager import NimManager
from metaflow.decorators import StepDecorator
from .card import NimMetricsRefresher
from ..card_utilities.injector import CardDecoratorInjector
from ..card_utilities.async_cards import AsyncPeriodicRefresher


class NimDecorator(StepDecorator, CardDecoratorInjector):
    name = "nim"

    defaults = {
        "models": [],
        "monitor": True,
        "persist_db": False,
    }

    # Refer https://github.com/Netflix/metaflow/blob/master/docs/lifecycle.png
    # to understand where these functions are invoked in the lifecycle of a
    # Metaflow flow.
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        if self.attributes["monitor"]:
            self.attach_card_decorator(
                flow,
                step,
                NimMetricsRefresher.CARD_ID,
                "blank",
                refresh_interval=4.0,
            )

        current._update_env(
            {
                "nim": NimManager(
                    models=self.attributes["models"],
                    flow=flow,
                    step_name=step,
                    monitor=self.attributes["monitor"],
                )
            }
        )

    def task_decorate(
        self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context
    ):
        if self.attributes["monitor"]:
            import sqlite3

            file_path = get_storage_path(current.task_id)
            if os.path.exists(file_path):
                os.remove(file_path)
            os.makedirs(NIM_MONITOR_LOCAL_STORAGE_ROOT, exist_ok=True)
            conn = sqlite3.connect(file_path)

            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE metrics (
                    error INTEGER,
                    success INTEGER,
                    status_code INTEGER,
                    prompt_tokens INTEGER,
                    completion_tokens INTEGER,
                    e2e_time NUMERIC,
                    model TEXT
                )
                """
            )

            def _wrapped_step_func(*args, **kwargs):
                async_refresher_metrics = AsyncPeriodicRefresher(
                    NimMetricsRefresher(),
                    updater_interval=4.0,
                    collector_interval=2.0,
                    file_name=file_path,
                )
                try:
                    async_refresher_metrics.start()
                    return step_func(*args, **kwargs)
                finally:
                    time.sleep(5.0)  # buffer for the last update to synchronize
                    async_refresher_metrics.stop()

            return _wrapped_step_func
        else:
            return step_func

    def task_post_step(
        self, step_name, flow, graph, retry_count, max_user_code_retries
    ):
        if not self.attributes["persist_db"]:
            import shutil

            file_path = get_storage_path(current.task_id)
            if os.path.exists(file_path):
                os.remove(file_path)
            # if this task is the last one, delete the whole enchilada.
            if not os.listdir(NIM_MONITOR_LOCAL_STORAGE_ROOT):
                shutil.rmtree(NIM_MONITOR_LOCAL_STORAGE_ROOT, ignore_errors=True)
