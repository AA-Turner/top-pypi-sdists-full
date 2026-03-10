"""
gpu_card_process.py — isolated subprocess entry point for GPU card live updates.

Spawned by _gpu_profile_wrapper. Receives a JSON config blob via --config.
Runs GPUMonitor + writes data.json to CardDatastore on a fixed card_interval.
Zero communication back to the parent process.
"""

import argparse
import json
import os
import signal
import sys
import threading
import time

# Ensure sibling modules are importable regardless of cwd.
# This script runs as a standalone subprocess.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

_DEBUG = os.environ.get("METAFLOW_GPU_PROFILE_DEBUG", "") != ""


def _debug(msg):
    if _DEBUG:
        print("[gpu_card_process] %s" % msg, file=sys.stderr, flush=True)


def run(config: dict):
    from gpu import GPUMonitor
    from gpu_card_utils import make_card_datastore
    from gpu_card_writer import build_data_json

    sample_interval = config.get("sample_interval", 1)
    card_interval = config.get("card_interval", 5)
    max_samples_per_gpu = config.get("max_samples_per_gpu")

    monitor = GPUMonitor(
        interval=sample_interval,
        max_samples_per_gpu=max_samples_per_gpu,
    )
    monitor_thread = threading.Thread(
        target=monitor._monitor_update_thread, daemon=True
    )
    monitor_thread.start()

    card_ds = make_card_datastore(config)
    readings_path = config.get("readings_path")
    display_max_points = config.get("display_max_points", 2400)

    if max_samples_per_gpu:
        window_hrs = (max_samples_per_gpu * sample_interval) / 3600.0
        _debug(
            "started. interval=%ds card_interval=%ds max_samples=%d (%.1f hr window)"
            % (sample_interval, card_interval, max_samples_per_gpu, window_hrs)
        )
    else:
        _debug(
            "started. interval=%ds card_interval=%ds (unbounded memory)"
            % (sample_interval, card_interval)
        )

    def _write_update():
        chart_readings = monitor.read(max_points=display_max_points)
        payload = build_data_json(chart_readings, config)
        card_ds.save_data(
            config["card_uuid"],
            config["card_type"],
            payload,
            card_id=config["card_id"],
        )
        if readings_path:
            full_readings = monitor.read()
            tmp = readings_path + ".tmp"
            with open(tmp, "w") as f:
                f.write(json.dumps(full_readings))
            os.replace(tmp, readings_path)

    _stop = threading.Event()

    def _handle_signal(signum, frame):
        _stop.set()

    signal.signal(signal.SIGTERM, _handle_signal)

    try:
        while not _stop.wait(card_interval):
            try:
                _write_update()
            except Exception as e:
                _debug("write error: %s" % e)
    except KeyboardInterrupt:
        pass
    finally:
        monitor.cleanup()
        try:
            _write_update()
        except Exception:
            pass
        _debug("stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GPU card live-update subprocess")
    parser.add_argument("--config", required=True, help="JSON config string")
    args = parser.parse_args()

    config = json.loads(args.config)
    run(config)
