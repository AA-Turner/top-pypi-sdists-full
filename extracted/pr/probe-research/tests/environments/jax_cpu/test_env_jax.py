"""JAX (CPU): a plain training loop logging jax arrays and numpy scalars.

What it simulates: a customer's hand-written JAX loop (jit + value_and_grad)
calling ``probe.log`` with the values as the loop produced them -- 0-d jax
arrays, numpy scalars, a value logged from inside ``jax.jit`` through
``jax.debug.callback`` -- then update_config, two artifacts (one > 64 MiB)
and finish. Real: JAX on the CPU backend, the released SDK, a real child
process. Simulated: the server (the fake, unless PROBE_BASE_URL is set).
"""

from __future__ import annotations

import math

from tests.environments import envkit

pytestmark = envkit.requires_env

TIMEOUT = 300


def _run(target, dirs) -> tuple[dict, envkit.Child]:
    envkit.requirement("jax")
    child = envkit.run_child(
        [envkit.PYTHON, envkit.script("jax_cpu", "jax_train.py")],
        env=envkit.child_env(target, dirs),
        cwd=dirs.work,
        timeout=TIMEOUT,
    )
    assert not child.timed_out and child.returncode == 0, child.tail()
    res = child.result("jax")
    assert res["backend"] == "cpu"
    raised = {k: v["raised"] for k, v in res["typed"].items() if v["raised"]}
    assert not raised, f"probe.log raised into the loop: {raised}"
    assert res["finish_raised"] is None and res["config_raised"] is None, res
    return res, child


def test_jax_loop_reconciles_and_closes_completed(target, dirs, started):
    res, child = _run(target, dirs)
    reader = target.reader()
    run_id = res["run_id"]
    status = envkit.wait_status(reader, run_id)
    assert status == "completed", (status, child.tail())

    # Every (step, key, value) the loop passed -- jax 0-d arrays, numpy
    # scalars, nested dicts -- exactly once.
    missing, wrong, _ = envkit.reconcile(reader, run_id, envkit.ledger_expected(res["ledger"]))
    assert not missing and not wrong, (missing[:5], wrong[:5])

    names = set(res["artifacts"])
    arts = envkit.wait_artifacts(reader, run_id, names)
    assert names <= set(arts), (names, sorted(arts))
    leases = envkit.lease_summary(envkit.writers(reader, run_id))
    assert leases == [("owner", None, True, "completed")], leases

    # update_config with a jax scalar and a numpy int: numbers, not reprs.
    config = reader.get_run(run_id).get("config") or {}
    assert isinstance(config.get("dim"), int), config
    assert isinstance(config.get("final_lr"), float), config.get("final_lr")

    assert envkit.leaked_files([run_id], started) == []
    print(
        f"sdk {res['sdk_version']} ({res['sdk_file']}) jax {res['jax_version']}: {len(res['ledger'])} points "
        f"reconciled, artifacts {sorted(names)}, {child.elapsed:.1f}s"
    )


def test_jax_and_numpy_value_types_are_stored_as_logged(target, dirs):
    """One step per value type. A one-element value (0-d, or size-1 like
    ``jnp.array([3.5])``) is a point equal to ``.item()``, as numpy's and
    torch's are; a several-element one is not a point (step record)."""
    res, _ = _run(target, dirs)
    reader = target.reader()
    run_id = res["run_id"]
    assert envkit.wait_status(reader, run_id) == "completed"
    envkit.reconcile(reader, run_id, envkit.ledger_expected(res["ledger"]))
    got = envkit.points(reader, run_id)
    stored, problems = {}, []
    for name, case in res["typed"].items():
        vals = got.get((case["step"], f"types/{name}"))
        stored[name] = vals
        want = case["expect"]
        if want is None:
            if vals is not None:
                problems.append(f"{name}: a multi-element value became a point {vals}")
        elif vals is None or len(vals) != 1:
            problems.append(f"{name}: logged {want!r}, stored as points {vals}")
        elif not envkit._close(vals[0], want):
            problems.append(f"{name}: stored {vals[0]!r}, logged {want!r}")
    print(f"types stored: {stored}\ntype warnings: {res['type_warnings']}")
    assert not problems, problems
    # NaN / inf survive as themselves (not dropped, not 0).
    assert math.isnan(stored["jax_nan"][0]) and stored["jax_inf"][0] == math.inf
