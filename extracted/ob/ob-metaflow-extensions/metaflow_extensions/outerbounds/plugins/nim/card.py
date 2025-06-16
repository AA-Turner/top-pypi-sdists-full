from metaflow.cards import Markdown, Table
from metaflow.metaflow_current import current

from .utils import get_storage_path
from ..card_utilities.async_cards import CardRefresher
from ..card_utilities.extra_components import BarPlot, ViolinPlot


class NimMetricsRefresher(CardRefresher):
    CARD_ID = "nim_metrics"

    def __init__(self) -> None:
        self._metrics_charts = {}
        self._last_updated_on = None
        self._already_rendered = False
        self._file_name = get_storage_path(current.task_id)

    def sqlite_fetch_func(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT error, success, status_code, prompt_tokens, completion_tokens, e2e_time, model FROM metrics"
            )
            rows = cursor.fetchall()
            data = {
                "error": 0,
                "success": 0,
                "status_code": [],
                "prompt_tokens": [],
                "completion_tokens": [],
                "e2e_time": [],
                "model": [],
            }
            for row in rows:
                data["error"] += row[0]
                data["success"] += row[1]
                data["status_code"].append(row[2])
                data["prompt_tokens"].append(row[3])
                data["completion_tokens"].append(row[4])
                data["e2e_time"].append(row[5])
                data["model"].append(row[6])
            return data
        finally:
            conn.close()

    def render_card_fresh(self, current_card, data):
        self._already_rendered = True
        current_card.clear()
        current_card.append(Markdown("## Metrics"))

        self._metrics_charts["request_success"] = BarPlot(
            title="Request success",
            category_name="category",
            value_name="amount",
            orientation="horizontal",
        )
        self._metrics_charts["latency_distribution"] = ViolinPlot(
            title="Latency distribution (s)",
            category_col_name="model",
            value_col_name="e2e_time",
        )

        current_card.append(
            Table(
                data=[
                    [
                        self._metrics_charts["request_success"],
                    ],
                    [self._metrics_charts["latency_distribution"]],
                ]
            )
        )
        current_card.refresh()

    def on_startup(self, current_card):
        current_card.append(Markdown("# Task-level NIM API metrics"))
        current_card.append(
            Markdown(
                "_waiting for data to appear_",
            )
        )
        current_card.refresh()

    def on_error(self, current_card, error_message):
        if isinstance(error_message, FileNotFoundError):
            return

        if not self._already_rendered:
            current_card.clear()
            current_card.append(
                Markdown(
                    f"## Error: {str(error_message)}",
                )
            )
            current_card.refresh()

    def update_only_components(self, current_card, data_object):
        # update request success data
        self._metrics_charts["request_success"].spec["data"][0]["values"] = [
            {
                "category": "Successful requests",
                "amount": data_object["metrics"]["success"],
            },
            {"category": "Errors", "amount": data_object["metrics"]["error"]},
        ]

        latency_data = []
        times = []
        for m, e in zip(
            data_object["metrics"]["model"], data_object["metrics"]["e2e_time"]
        ):
            latency_data.append({"model": m, "e2e_time": e})
            times.append(e)

        # update latency data
        self._metrics_charts["latency_distribution"].spec["data"][0][
            "values"
        ] = latency_data

        # update domain for latency plot
        min_time = min(times)
        max_time = max(times)
        for scale in self._metrics_charts["latency_distribution"].spec["scales"]:
            if scale["name"] == "xscale":
                scale["domain"] = [min_time - max_time * 0.1, max_time + max_time * 0.1]

        current_card.refresh()

    def on_update(self, current_card, data_object):
        data_object_keys = set(data_object.keys())
        if len(data_object_keys) == 0:
            return
        if len(self._metrics_charts) == 0:
            self.render_card_fresh(current_card, data_object)
            return
        elif len(data_object["metrics"]["status_code"]) == 0:
            return
        else:
            self.update_only_components(current_card, data_object)
            return
