"""
writer.py — payload builder for GpuCardProcess.

Pure function: readings (from monitor.read()) + config → data.json dict.
No I/O. Metaflow card objects are NOT used here — we build the serialized
JSON directly, matching what Table/VegaChart/Markdown produce via .render().

Component layout written to data.json per device:
  "ts_{safe_id}"           → markdown  (time range string)
  "charts_table_{safe_id}" → table     (2 rows: GPU util chart | mem chart)
  "max_util_table"         → markdown  (summary table, all devices)
"""

import re
import time
from datetime import datetime

MEM_COLOR = "#0c64d6"
GPU_COLOR = "#ff69b4"
_TS_FORMAT = "%Y/%m/%d %H:%M:%S"


# -----------------------------------------------------------------------
# Public entry point
# -----------------------------------------------------------------------


def build_data_json(readings: dict, config: dict) -> dict:
    comp_ids = config["comp_ids"]
    data = {}

    data[comp_ids["max_util_table"]] = _build_max_util_table(
        readings, comp_ids["max_util_table"]
    )

    for device_id, device_comps in comp_ids["devices"].items():
        dev_data = readings.get(device_id, {})
        data[device_comps["ts_range"]] = _build_ts_range(
            dev_data, device_comps["ts_range"]
        )
        data[device_comps["charts_table"]] = _build_charts_table(
            device_id, dev_data, device_comps["charts_table"]
        )

    return {
        "reload_token": config["reload_token"],
        "created_on": time.time(),
        "data": data,
    }


# -----------------------------------------------------------------------
# Component builders
# -----------------------------------------------------------------------


def _build_max_util_table(readings: dict, comp_id: str) -> dict:
    """Markdown table: Device ID | Max GPU % | Max memory."""
    if not readings:
        return {
            "type": "markdown",
            "id": comp_id,
            "source": "_Waiting for first reading..._",
        }

    lines = [
        "| Device ID | Max GPU % | Max memory |",
        "|-----------|-----------|------------|",
    ]
    for gpu_id, data in readings.items():
        util_vals = data.get("gpu_utilization", [])
        mem_used = data.get("memory_used", [])
        max_util = ("%.1f%%" % max(map(float, util_vals))) if util_vals else "—"
        peak_mem = ("%d MiB" % int(max(map(float, mem_used)))) if mem_used else "—"
        lines.append("| `%s` | %s | %s |" % (gpu_id, max_util, peak_mem))

    return {"type": "markdown", "id": comp_id, "source": "\n".join(lines)}


def _build_ts_range(data: dict, comp_id: str) -> dict:
    """Markdown: time range covered by the readings."""
    ts_raw = data.get("timestamp", [])
    if len(ts_raw) < 2:
        source = "*No readings available*"
    else:
        try:
            parsed = [datetime.strptime(t, _TS_FORMAT) for t in ts_raw]
            source = "*Time range of charts: %s to %s*" % (
                min(parsed).strftime(_TS_FORMAT),
                max(parsed).strftime(_TS_FORMAT),
            )
        except ValueError:
            source = "*No readings available*"
    return {"type": "markdown", "id": comp_id, "source": source}


def _build_charts_table(device_id: str, data: dict, comp_id: str) -> dict:
    """
    Table component JSON (matching Metaflow Table.render() format):
        Row 0: ["GPU Utilization",  <pink GPU util VegaChart>]
        Row 1: ["Memory usage",     <blue mem %   VegaChart>]
    """
    safe = _safe_id(device_id)
    gpu_spec = _build_gpu_spec(data)
    mem_spec = _build_mem_spec(data)

    return {
        "type": "table",
        "columns": [],
        "vertical": False,
        "id": comp_id,
        "data": [
            [
                {
                    "type": "markdown",
                    "source": "GPU Utilization",
                    "id": "md_gpu_%s" % safe,
                },
                {
                    "type": "vegaChart",
                    "id": "vc_gpu_%s" % safe,
                    "spec": gpu_spec or _placeholder_spec(),
                    "options": {"actions": False},
                },
            ],
            [
                {
                    "type": "markdown",
                    "source": "Memory usage",
                    "id": "md_mem_%s" % safe,
                },
                {
                    "type": "vegaChart",
                    "id": "vc_mem_%s" % safe,
                    "spec": mem_spec or _placeholder_spec(),
                    "options": {"actions": False},
                },
            ],
        ],
    }


# -----------------------------------------------------------------------
# Spec builders (also used directly by wrapper.py for final in-process update)
# -----------------------------------------------------------------------


def _build_gpu_spec(data: dict):
    """VegaLite spec — GPU utilization % — pink. Returns None if no data."""
    ts_raw = data.get("timestamp", [])
    util_raw = data.get("gpu_utilization", [])
    if not ts_raw:
        return None
    values = []
    for t_str, u_str in zip(ts_raw, util_raw):
        try:
            values.append(
                {
                    "tstamps": str(datetime.strptime(t_str, _TS_FORMAT)),
                    "vals": float(u_str) / 100.0,
                }
            )
        except (ValueError, IndexError):
            continue
    if not values:
        return None
    return _vegalite_line(
        values, "GPU utilization", "GPU utilization", GPU_COLOR, percentage_format=True
    )


def _build_mem_spec(data: dict):
    """VegaLite spec — memory % — blue. Returns None if no data."""
    ts_raw = data.get("timestamp", [])
    mem_used_raw = data.get("memory_used", [])
    mem_total_raw = data.get("memory_total", [])
    if not ts_raw:
        return None
    values = []
    for t_str, used, total in zip(ts_raw, mem_used_raw, mem_total_raw):
        try:
            val = float(used) / float(total) if float(total) > 0 else 0.0
            values.append(
                {"tstamps": str(datetime.strptime(t_str, _TS_FORMAT)), "vals": val}
            )
        except (ValueError, IndexError, ZeroDivisionError):
            continue
    if not values:
        return None
    return _vegalite_line(
        values,
        "Percentage Memory utilization",
        "Percentage Memory utilization",
        MEM_COLOR,
        percentage_format=True,
    )


# -----------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------


def _safe_id(device_id: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]", "_", device_id)


def _vegalite_line(values, description, y_label, line_color, percentage_format):
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": description,
        "data": {"values": values},
        "width": 600,
        "height": 400,
        "encoding": {
            "x": {"field": "tstamps", "type": "temporal", "axis": {"title": "Time"}},
            "y": {
                "field": "vals",
                "type": "quantitative",
                "axis": {
                    "title": y_label,
                    **({"format": "%"} if percentage_format else {}),
                },
            },
        },
        "layer": [
            {
                "mark": {"type": "line", "color": line_color, "tooltip": True},
                "encoding": {"tooltip": [{"field": "tstamps"}, {"field": "vals"}]},
            }
        ],
    }


def _placeholder_spec():
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "Waiting for GPU readings...",
        "data": {"values": []},
        "width": 600,
        "height": 400,
        "mark": "line",
        "encoding": {
            "x": {"field": "tstamps", "type": "temporal"},
            "y": {"field": "vals", "type": "quantitative"},
        },
    }
