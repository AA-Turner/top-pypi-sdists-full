"""Core reflects the Wrapper's telemetry; it does not derive its own view of a worker's resources
(operator 2026-11-16: "core needs to be reflecting the wrappers telemetry … it should have no reason to
derive its own aggregation of its resources"). The worker record Core builds must carry the Wrapper's
live /v1/telemetry/resources report — residents, transfers, gpu_state, cards, host/cpu state — intact,
so the console renders Serving rows and the GPU card straight from the Wrapper's own facts."""
from hugpy_core.intake.service import presence


def test_the_wrappers_resources_report_reaches_the_worker_record_intact():
    worker = {"name": "w1", "url": "http://w1:9000"}
    state = {}
    resources = {
        "residents": [
            {"key": "org/nine::q4.gguf", "pid": 11, "vram_bytes": 14, "ram_bytes": 0,
             "healthy": True, "busy": True, "loading": False, "device_id": 0},
            {"key": "org/coder::q4.gguf", "pid": 12, "vram_bytes": 0, "ram_bytes": 38,
             "healthy": False, "busy": False, "loading": True, "device_id": None},
        ],
        # A central->worker copy a CALL brought in: not assigned, still shown downloading.
        "transfers": [
            {"key": "org/brought::q8.gguf", "repo": "org/brought", "variation": "q8.gguf",
             "state": "copying", "done_bytes": 3, "total_bytes": 10,
             "started_at": 100.0, "updated_at": 105.0, "error": None},
            {"key": "org/done::q8.gguf", "repo": "org/done", "variation": "q8.gguf",
             "state": "done", "done_bytes": 10, "total_bytes": 10,
             "started_at": 90.0, "updated_at": 95.0, "error": None},
        ],
        "gpu_state": [{"device": 0, "used": 15, "total": 24}],
        "cards": [{"device": 0}],
        "host_state": [{"mem_total": 64, "mem_available": 30}],
        "cpu_state": [{"busy": 0.2}],
        "queue": [{"id": "q1"}],
        "sampled_at": 123.0,
    }
    payload = presence(worker, state, models=[], storage=None, resources=resources)

    res = payload["resources"]
    # Every field the Wrapper reported is carried through byte-for-byte — Core adds nothing and drops
    # none of the live facts the console renders from.
    assert res["residents"] == resources["residents"]
    assert res["transfers"] == resources["transfers"]
    assert res["gpu_state"] == resources["gpu_state"]
    assert res["cards"] == resources["cards"]
    assert res["host_state"] == resources["host_state"]
    assert res["sampled_at"] == 123.0
    # The still-copying transfer (and only it) is what the console shows as downloading; Core does not
    # pre-filter — the ended "done" copy is present too, labelled by the Wrapper's own state.
    states = {t["key"]: t["state"] for t in res["transfers"]}
    assert states == {"org/brought::q8.gguf": "copying", "org/done::q8.gguf": "done"}
    # Core builds no parallel aggregation of its own.
    assert "pid_registry" not in payload
    assert "provisioning" not in payload and "provision_progress" not in payload
