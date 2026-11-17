"""A test fire calls only what the worker already holds on its own drives, and
makes NO concurrency decision of its own (operator 2026-11-16: "all testfire
should have to do is make all calls in sequential order and the job should take
care of itself" — the Wrapper's queue plans concurrency; "for now it needs to
just use the models on the worker drives")."""
from hugpy_core.testfire.testfire import on_worker_drive, parse_start_body, worker_drive_models


def test_only_models_on_the_workers_own_drives_are_served_in_place():
    worker = {"storage": {"models": [
        dict(model_key="org/nine", role="worker", complete=True, variations=["nine.Q4_K_M.gguf"]),
        dict(model_key="org/coder/q4", role="immutable", complete=True, variations=["coder-q4-*.gguf"]),
        dict(model_key="org/cold", role="central", complete=True, variations=["cold.gguf"]),
        dict(model_key="org/half", role="worker", complete=False, variations=["half.gguf"])]}}
    on_drive = worker_drive_models(worker)
    assert on_worker_drive("org/nine", on_drive) and on_worker_drive("org/nine::nine.Q4_K_M.gguf", on_drive)
    assert on_worker_drive("org/coder/q4::coder-q4-*.gguf", on_drive)                    # a split model, served in place
    assert not on_worker_drive("org/nine::nine.Q8_0.gguf", on_drive)                    # another quant: not here
    assert not on_worker_drive("org/cold", on_drive) and not on_worker_drive("org/half", on_drive)


def test_start_options_carry_no_concurrency_knob():
    opts = parse_start_body({})
    assert opts["worker_drive_only"] is True and opts["grade"] is True and opts["rounds"] == 1
    assert "concurrency" not in opts and "chaos" not in opts        # the job paces nothing
    assert parse_start_body({"grade": False, "rounds": 3})["rounds"] == 3
