"""A plain JAX (CPU) training loop logging through probe.log.

1. Linear regression by jax.value_and_grad for STEPS steps; every metric is a
   jax array or a numpy scalar, exactly as the loop produced it (no float()).
2. One step per value TYPE (jax 0-d / size-1 / vector / bfloat16 / int / NaN,
   numpy scalars, a value logged from inside jax.jit through
   jax.debug.callback), each in its own probe.log call, so one refusal cannot
   hide another. Exceptions are caught and reported: a raise here is a crash
   in the customer's loop.
3. update_config with jax / numpy values, two artifacts (one > 64 MiB), finish.
"""

from __future__ import annotations

import math
import os
import sys

import jax
import jax.numpy as jnp
import numpy as np

import envchild
import probe

STEPS = int(os.environ.get("JAX_STEPS", "30"))
TYPES_STEP = 1000

run = probe.init(project=envchild.PROJECT, name="jax-cpu-loop", config={"lr": 0.1, "dim": 3})
ledger = []  # [step, key, float value the customer passed]

key = jax.random.PRNGKey(0)
X = jax.random.normal(key, (64, 3))
true_w = jnp.array([1.0, -2.0, 0.5])
y = X @ true_w


def loss_fn(w):
    return jnp.mean((X @ w - y) ** 2)


grad = jax.jit(jax.value_and_grad(loss_fn))
w = jnp.zeros(3)
with envchild.Warned() as loop_warned:
    for step in range(STEPS):
        loss, g = grad(w)
        w = w - 0.1 * g
        wn = jnp.linalg.norm(w)
        gmax = np.float32(np.max(np.abs(np.asarray(g))))
        probe.log({"train": {"loss": loss, "grad_max": gmax}, "w_norm": wn}, step=step)
        ledger += [
            [step, "train/loss", float(loss)],
            [step, "train/grad_max", float(gmax)],
            [step, "w_norm", float(wn)],
        ]

# One step per value type. `expect`: the float the SDK should store, or None
# for "not a metric" (goes to the step record, never a point).
cases = {
    "jax_f32_0d": (jnp.float32(1.5), 1.5),
    "jax_array_0d": (jnp.array(2.25), 2.25),
    "jax_bf16": (jnp.array(0.1, dtype=jnp.bfloat16), float(jnp.array(0.1, dtype=jnp.bfloat16))),
    "jax_int32": (jnp.array(5, dtype=jnp.int32), 5.0),
    "jax_bool": (jnp.array(True), 1.0),
    "jax_size1_vec": (jnp.array([3.5]), 3.5),
    "jax_vec3": (jnp.array([1.0, 2.0, 3.0]), None),
    "jax_nan": (jnp.array(jnp.nan), math.nan),
    "jax_inf": (jnp.array(jnp.inf), math.inf),
    "np_float32": (np.float32(0.1), float(np.float32(0.1))),
    "np_float64": (np.float64(0.25), 0.25),
    "np_float16": (np.float16(0.1), float(np.float16(0.1))),
    "np_int64": (np.int64(7), 7.0),
    "np_int32": (np.int32(-3), -3.0),
    "np_bool": (np.bool_(True), 1.0),
    "np_vec2": (np.array([1.0, 2.0]), None),
    "np_nan32": (np.float32("nan"), math.nan),
}
typed = {}
with envchild.Warned() as types_warned:
    for i, (name, (val, expect)) in enumerate(cases.items()):
        step = TYPES_STEP + i
        try:
            probe.log({f"types/{name}": val}, step=step)
            typed[name] = {"step": step, "raised": None, "expect": expect}
        except BaseException as exc:  # noqa: BLE001 -- a raise is the finding
            typed[name] = {"step": step, "raised": f"{type(exc).__name__}: {exc}", "expect": expect}

    # Logged from INSIDE a jitted function: the callback receives numpy values.
    jit_step = TYPES_STEP + len(cases)

    @jax.jit
    def jitted(w):
        loss = loss_fn(w)
        jax.debug.callback(lambda v: probe.log({"types/jit_callback": v}, step=jit_step), loss)
        return loss

    try:
        jit_loss = float(jitted(w))
        jax.effects_barrier()
        typed["jit_callback"] = {"step": jit_step, "raised": None, "expect": jit_loss}
    except BaseException as exc:  # noqa: BLE001
        typed["jit_callback"] = {"step": jit_step, "raised": f"{type(exc).__name__}: {exc}", "expect": None}

config_raised = None
try:
    probe.update_config({"final_lr": jnp.float32(0.1), "dim": np.int64(3), "w_final": np.asarray(w).tolist()})
except BaseException as exc:  # noqa: BLE001
    config_raised = f"{type(exc).__name__}: {exc}"

names = []
for name, path in envchild.write_artifacts("jax", big=True).items():
    probe.log_artifact(name, path=path)
    names.append(name)

finish_raised = None
try:
    probe.finish()
except BaseException as exc:  # noqa: BLE001
    finish_raised = f"{type(exc).__name__}: {exc}"

envchild.result(
    "jax",
    run_id=str(run.id),
    ledger=ledger,
    typed=typed,
    config_raised=config_raised,
    finish_raised=finish_raised,
    artifacts=names,
    loop_warnings=loop_warned.texts(),
    type_warnings=types_warned.texts(),
    jax_version=jax.__version__,
    backend=jax.default_backend(),
    **envchild.sdk_info(),
)
sys.exit(0)
