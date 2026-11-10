"""
Introspection → `BenchmarkRegistration`, symmetric to `registry.py` for policies.

In one sentence: `@seq.benchmark(...)` on a class → its marked methods are collected (@seq.reset / @seq.step - its
own and those it inherits) and each held to what the platform hands it, @seq.concurrent(sizes=[N]) on its step read as
how many worlds one call steps → init= held to its constructor (seq.named.constructor: "{num_worlds}" for a vectorized env,
"{policy.<field>}") → its tasks, seeds and time limit checked → the wire `BenchmarkSpec` built and kept, with the
parameters its constructor declares beside what init= hands it, as the `BenchmarkRegistration` an eval's machine
imports the class by, builds it from after the snapshot and runs it from.

WHY the signatures are checked here: the platform calls each method with what it hands it, so a method that cannot
take it would fail on the eval's machine, after cards were paid for; here it fails where it is written.
"""
from __future__ import annotations

import inspect
import re
from dataclasses import dataclass
from typing import Any

from seq import named
from seq._partial import Refused, hook, hooks_along, keeping, refused
from seq.errors import BenchmarkDefinitionError
from seq.image import Image
from seq.registry import _CTX_ATTR, _ref_kept, importable
from seq.secret import Secret
from seq.volume import Volume


from sequence_base.constants.cards import BENCHMARK_CPU as CPU
from sequence_base.constants.cards import BENCHMARK_GPUS, DEFAULT_BENCHMARK_GPU

from sequence_base.constants.limits import DEFAULT_CPU_CORES, MAX_CPU_CORES, MAX_ENVS
from sequence_base.contract import (
    BenchmarkRegisterRequest,
    BenchmarkSpec,
    ImageSpec,
    InferParam,
    ReplaySpec,
    SecretRef,
    SeqFlags,
    VolumeRef,
)
from sequence_base.contract.flags import BENCHMARK_BINDABLE



_ASSETS_MOUNT = "/assets"

_BENCH_ATTR = "__seq_benchmark__"

DEFAULT_GB_PER_CORE = 2

@dataclass
class BenchmarkRegistration:
    """Everything an eval needs to run a benchmark, introspected from the decorated class: the wire `spec`, and the
    parameters its constructor declares with a default beside what init= hands it (`params`, each with its type and
    default, settable per eval as --param benchmark.NAME=VALUE). Everything else is read off the spec:

    - `bindings`: RESET / STEP → the method's name;
    - `constructor`: how its class is built after the machine's snapshot (init=), None for `cls()`;
    - `tasks`: {name: description}, "" for a task with none; `seeds`: a list; `max_seconds`: one number of seconds or
      {task: seconds} naming every task - `max_seconds_of(task)` reads either;
    - `worlds`: how many worlds one call of a vectorized env's step takes (@seq.concurrent(sizes=[N])), None for an env
      that steps one world at a time;
    - `replay`, `engine`, `gpu`, `cpu`, `memory_gb`, `secrets`, `assets`, `handler_ref`, `name`."""

    spec: BenchmarkSpec
    params: dict[str, InferParam]

    @property
    def name(self) -> str:
        return self.spec.name

    @property
    def bindings(self) -> dict[SeqFlags, str]:
        return self.spec.bindings

    @property
    def handler_ref(self) -> str:
        return self.spec.handler_ref

    @property
    def tasks(self) -> dict[str, str]:
        return self.spec.tasks

    @property
    def seeds(self) -> list[int]:
        return self.spec.seeds

    @property
    def max_seconds(self) -> float | dict[str, float]:
        return self.spec.max_seconds

    @property
    def worlds(self) -> int | None:
        return self.spec.worlds

    @property
    def constructor(self) -> Any:
        return self.spec.constructor

    @property
    def replay(self) -> ReplaySpec | None:
        return self.spec.replay

    @property
    def engine(self) -> str | None:
        return self.spec.engine

    @property
    def gpu(self) -> str | None:
        return self.spec.gpu

    @property
    def cpu(self) -> int | None:
        return self.spec.cpu

    @property
    def memory_gb(self) -> int | None:
        return self.spec.memory_gb

    @property
    def secrets(self) -> list[SecretRef]:
        return self.spec.secrets

    @property
    def assets(self) -> list[VolumeRef]:
        return self.spec.assets

    def max_seconds_of(self, task: str) -> float:
        """How long an episode of `task` may run, in seconds on the robot's clock: the benchmark's one limit, or the
        task's own. A name that is none of its tasks raises KeyError naming them."""
        if task not in self.spec.tasks:
            raise KeyError(f"{task!r} is not a task of {self.name}: {', '.join(self.spec.tasks)}")
        limit = self.spec.max_seconds
        return float(limit[task] if isinstance(limit, dict) else limit)


def build_benchmark_registration(cls: type, kwargs: dict[str, Any]) -> type:
    """The `@seq.benchmark` decorator body: validate + register `cls`, attach the registration, return. A declaration it
    refuses is raised here, or - while seq imports the file, and on the platform (seq._partial.keeping) - kept on the
    class (Refused) and raised where the class is used, so the other classes of its file still import."""
    bindings = None
    try:
        if _BENCH_ATTR in cls.__dict__:
            raise BenchmarkDefinitionError(
                f"@seq.benchmark is applied more than once to {cls.__name__}; apply it exactly once"
            )

        bindings = _collect_benchmark_bindings(cls)
        return _register(cls, kwargs, bindings)
    except BenchmarkDefinitionError as exc:
        if not keeping():
            raise
        return refused(cls, _BENCH_ATTR, exc, bindings)


def _register(cls: type, kwargs: dict[str, Any], bindings: dict[SeqFlags, str]) -> type:
    """The registration of `cls` from its declaration and its bindings, attached; raises what it refuses."""
    from seq.params import _first_error




    worlds = _validate_bindings(cls, bindings)
    constructor = named.constructor(cls, kwargs, benchmark=True, worlds=worlds, error=BenchmarkDefinitionError)
    params = _init_params(cls, constructor)

    gpu = _resolve_gpu(kwargs.get("gpu"))
    driver = _resolve_driver(kwargs.get("driver"), gpu)


    cpu, memory_gb = kwargs.get("cpu"), kwargs.get("memory")
    if gpu == CPU:
        cpu, memory_gb = _cpu_sizes(cpu, memory_gb)
    name = kwargs.get("name") or cls.__name__

    from sequence_base.contract.deployments import _NAME
    if not isinstance(name, str) or not _NAME.fullmatch(name):
        raise BenchmarkDefinitionError(f"@seq.benchmark name= must be 1-64 letters, digits, '.', '_' or '-', starting "
                                       f"with a letter or digit, got {name!r}")
    tasks = _resolve_tasks(kwargs.get("tasks"))
    seeds = _resolve_seeds(kwargs.get("seeds"))
    max_seconds = _resolve_max_seconds(kwargs.get("max_seconds"), tasks)
    image_spec = _resolve_image(kwargs.get("image"))
    replay = _resolve_replay(kwargs.get("replay"), cls)


    handler_ref = _ref_kept(cls)
    try:
        spec = BenchmarkSpec(
            name=name,
            image=image_spec,
            tasks=tasks,
            seeds=seeds,
            max_seconds=max_seconds,
            handler_ref=handler_ref,
            bindings=bindings,
            worlds=worlds,
            gpu=gpu,
            assets=_resolve_assets(kwargs.get("assets")),
            replay=replay,
            cpu=cpu,
            memory_gb=memory_gb,
            secrets=_resolve_secrets(kwargs.get("secrets")),

            **({"constructor": constructor} if constructor is not None else {}),

            **({"driver": driver} if driver is not None else {}),
        )
        spec = spec.model_copy(update={"replay": _replay_engine(replay)})
    except BenchmarkDefinitionError:
        raise
    except Exception as exc:
        raise BenchmarkDefinitionError(f"invalid @seq.benchmark declaration: {_first_error(exc)}") from None

    setattr(cls, _BENCH_ATTR, BenchmarkRegistration(spec=spec, params=params))

    image = kwargs.get("image")
    setattr(cls, "__seq_image_locals__",
            (image.local_files, image.python_sources) if isinstance(image, Image) else ((), ()))

    setattr(cls, _CTX_ATTR, image.context if isinstance(image, Image) else None)
    return cls


def benchmark_registration(cls: type) -> BenchmarkRegistration:
    """Return the `BenchmarkRegistration` `@seq.benchmark` attached, or raise if never decorated."""
    reg = cls.__dict__.get(_BENCH_ATTR)
    if reg is None:
        raise BenchmarkDefinitionError(
            f"{cls.__name__} is not a @seq.benchmark class; decorate it with @seq.benchmark(...)"
        )
    if isinstance(reg, Refused):
        reg.refuse()
    return reg


def benchmark_request(cls: type, *, name: str | None = None,
                      snapshots: list | None = None) -> BenchmarkRegisterRequest:
    """The `POST /v1/benchmarks` body for a `@seq.benchmark` class: its declaration - tasks, seeds, time limit, worlds -
    its source (the folder it was imported from, whole, plus what its image declared with seq.Image.add_local_* -
    seq.code_bundle.pack, appended to `snapshots` when given) and the parameters its constructor declares beside what
    init= hands it. `name` (from `seq deploy --name`) replaces the declared name, as it does for a policy."""
    from seq.code_bundle import pack, pack_dir, with_sources
    from seq.project_deps import image_for

    reg = benchmark_registration(cls)
    importable(cls)
    spec = reg.spec
    snap = pack(spec.handler_ref, local_files=getattr(cls, "__seq_image_locals__", ((), ()))[0],
                python_sources=getattr(cls, "__seq_image_locals__", ((), ()))[1])
    if snapshots is not None:
        snapshots.append(snap)
    context = cls.__dict__.get(_CTX_ATTR)


    image = image_for(with_sources(spec.image, snap.src_map), snap, handler_ref=spec.handler_ref,
                      kind="benchmark", declared=None)
    return BenchmarkRegisterRequest(
        name=name or spec.name, image=image,
        tasks=dict(spec.tasks), seeds=list(spec.seeds),
        max_seconds=dict(spec.max_seconds) if isinstance(spec.max_seconds, dict) else spec.max_seconds,
        handler_ref=spec.handler_ref, worlds=spec.worlds, assets=spec.assets, replay=spec.replay, cpu=spec.cpu,
        memory_gb=spec.memory_gb,
        code=snap.bundle,



        image_context=pack_dir(context) if context else None,

        secrets=list(spec.secrets),

        gpu=spec.gpu,


        params=dict(reg.params) or None,

        **({"driver": spec.driver} if spec.driver is not None else {}))




_NOT_A_BENCHMARKS = {
    SeqFlags.OBSERVE: "an observation is what a benchmark's @seq.step returns, (observation, done, success): "
                      "@seq.observation turns one into the policy's input on a @seq.adapter, and @seq.observe is a "
                      "policy's",
    SeqFlags.ACTION: "@seq.action is an adapter's (@seq.adapter): it turns the policy's answer into the actions a "
                     "benchmark's @seq.step plays",
}


def _collect_benchmark_bindings(cls: type) -> dict[SeqFlags, str]:
    """Bind each benchmark flag to its method - the class's own, or one it inherits from a benchmark or a mixin it is
    built on (seq._partial.hooks_along) - and restore raw fns. What sequence-base binds on a benchmark is
    BENCHMARK_BINDABLE (RESET / STEP); any other mark on one is refused, saying where it belongs."""
    bindings, _ = hooks_along(cls, _BENCH_ATTR, BenchmarkDefinitionError, "benchmark lifecycle")
    for member, attr_name in bindings.items():
        if member not in BENCHMARK_BINDABLE:
            said = _NOT_A_BENCHMARKS.get(member) or (
                f"@seq.{(member.name or str(member.value)).lower()} is not a benchmark's: a benchmark marks "
                "@seq.reset and @seq.step")
            raise BenchmarkDefinitionError(f"{cls.__name__}.{attr_name}: {said}")
    return bindings


def _validate_bindings(cls: type, bindings: dict[SeqFlags, str]) -> int | None:
    """@seq.reset and @seq.step are required, each held to what the platform hands it - a vectorized env's
    (@seq.concurrent(sizes=[N]) on its step) the worlds it is handed with them. Returns how many worlds one step call
    takes: N, or None for an env that steps one world at a time."""
    if SeqFlags.RESET not in bindings:
        raise BenchmarkDefinitionError(
            f"{cls.__name__} has no @seq.reset method: a benchmark marks the method that starts an episode of a task at "
            "a seed and returns its first observation - @seq.reset def reset(self, task, seed)")
    if SeqFlags.STEP not in bindings:
        raise BenchmarkDefinitionError(
            f"{cls.__name__} has no @seq.step method: a benchmark marks the method that plays one action and returns "
            "(observation, done, success) - @seq.step def step(self, action)")
    worlds = _worlds(cls, bindings[SeqFlags.STEP])
    reset, step = bindings[SeqFlags.RESET], bindings[SeqFlags.STEP]
    if worlds is None:
        _takes(cls, reset, 2, "@seq.reset", "a task and a seed", f"def {reset}(self, task, seed)")
        _takes(cls, step, 1, "@seq.step", "one action", f"def {step}(self, action)")
    else:
        _takes(cls, reset, 3, "@seq.reset", "the worlds to restart and each one's task and seed",
               f"def {reset}(self, worlds, tasks, seeds)")
        _takes(cls, step, 2, "@seq.step", "the worlds to step and one action for each - returning one (observation, "
               "done, success) a world", f"def {step}(self, worlds, actions)")
    return worlds


def _worlds(cls: type, step: str) -> int | None:
    """How many worlds one call of the step takes: N of @seq.concurrent(sizes=[N]) on it - one size, the most a machine
    runs at once - or None without it. @seq.concurrent on another method, or in a policy's form, is refused.
    
"""
    for name, member in vars(cls).items():
        if name != step and getattr(member, "__seq_concurrent__", None):
            raise BenchmarkDefinitionError(f"{cls.__name__}.{name}: @seq.concurrent goes on the @seq.step method - "
                                           "@seq.concurrent(sizes=[N]), N the most worlds one call steps")
    declared = getattr(hook(cls, step), "__seq_concurrent__", None)
    if not declared:
        return None
    listed = list(declared["sizes"])
    if len(listed) != 1:
        raise BenchmarkDefinitionError(
            f"@seq.concurrent(sizes={listed!r}) on {cls.__name__}.{step}: a benchmark's step takes one size, the most "
            f"worlds one call steps - @seq.concurrent(sizes=[{max(listed)}]); an eval builds as many as it needs, at "
            "most that")
    if listed[0] > MAX_ENVS:
        raise BenchmarkDefinitionError(f"@seq.concurrent(sizes={listed!r}) on {cls.__name__}.{step}: the size is a whole "
                                       f"number of worlds from 1 to {MAX_ENVS}")
    return listed[0]


def _takes(cls: type, method: str, n: int, mark: str, what: str, example: str) -> None:
    """The method takes exactly the `n` arguments the platform hands it, by position: at least n positional parameters
    (or *args), no more than n without a default, and no keyword-only one without a default."""
    try:
        params = list(inspect.signature(hook(cls, method)).parameters.values())[1:]
    except (TypeError, ValueError):
        return
    positional = (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    pos = [p for p in params if p.kind in positional]
    star = any(p.kind is inspect.Parameter.VAR_POSITIONAL for p in params)
    required = [p for p in pos if p.default is inspect.Parameter.empty]
    keyword_required = [p for p in params
                        if p.kind is inspect.Parameter.KEYWORD_ONLY and p.default is inspect.Parameter.empty]
    if (len(pos) < n and not star) or len(required) > n or keyword_required:
        raise BenchmarkDefinitionError(f"{cls.__name__}.{method} is the {mark} method: the platform hands it {what}, "
                                       f"in that order - {example}")


def _init_params(cls: type, constructor: Any) -> dict[str, InferParam]:
    """The parameters its constructor declares with a default beside what init= hands it - `def __init__(self, worlds,
    *, noise_std: float = 0.02)` with init={"worlds": "{num_worlds}"} - which an eval may set (`--param
    benchmark.noise_std=0`), every benchmark machine's constructor handed them. Its class's constructor as it is
    written: one of a type no --param sets keeps its default, set by nothing (keyword_params' loose). {} for a class
    without a constructor of its own.
"""
    from seq.params import keyword_params

    init = getattr(cls, "__init__", object.__init__)
    if init is object.__init__ or not inspect.isfunction(init):
        return {}
    given = set(constructor.kwargs) if constructor is not None else set()
    if constructor is not None and constructor.args:
        positional = [p.name for p in list(inspect.signature(init).parameters.values())[1:]
                      if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)]
        given |= set(positional[:len(constructor.args)])
    return keyword_params(init, f"{cls.__name__}.__init__", BenchmarkDefinitionError, kind="benchmark parameter",
                          skip=frozenset(given), loose=True)


def _resolve_tasks(given: Any) -> dict[str, str]:
    """tasks= as declared: {name: description}, each name a str and each description a str ("" for none). The names'
    form and the descriptions' length are the platform's rule (sequence_base's BenchmarkSpec checks both)."""
    how = 'tasks={"open_drawer": "open the top drawer"} - "" for a task with no description'
    if given is None:
        raise BenchmarkDefinitionError(f"@seq.benchmark needs tasks=: each task an episode can be of, by the name "
                                       f"@seq.reset is handed and an eval chooses it by, with what it asks - {how}")
    if not isinstance(given, dict):
        names = [t for t in given if isinstance(t, str)][:2] if isinstance(given, (list, tuple, set)) else []
        example = ("{" + ", ".join(f'"{t}": ""' for t in names) + "}") if names else None
        raise BenchmarkDefinitionError(f"@seq.benchmark tasks= is {{name: description}}, not a "
                                       f"{type(given).__name__}: " + (f"tasks={example}" if example else how))
    for task, text in given.items():
        if not isinstance(task, str):
            raise BenchmarkDefinitionError(f"@seq.benchmark tasks= names each task by a str, not {task!r}")
        if not isinstance(text, str):
            raise BenchmarkDefinitionError(f"tasks[{task!r}] is its description, a str (\"\" for none), not {text!r}")
    return dict(given)


def _resolve_seeds(given: Any) -> list[int]:
    """seeds= as declared: the seeds an episode starts at - a list of whole numbers, range(50) included."""
    if given is None:
        raise BenchmarkDefinitionError("@seq.benchmark needs seeds=: the seeds an episode starts at, e.g. "
                                       "seeds=range(50); trial k of a task runs seeds[k % len(seeds)]")
    if isinstance(given, (str, bytes, dict)) or not hasattr(given, "__iter__"):
        raise BenchmarkDefinitionError(f"@seq.benchmark seeds= is a list of whole numbers, e.g. seeds=range(50), not "
                                       f"{given!r}")
    seeds = list(given)
    for s in seeds:
        if isinstance(s, bool) or not isinstance(s, int):
            raise BenchmarkDefinitionError(f"@seq.benchmark seeds= holds whole numbers, not {s!r}")
    return seeds


def _resolve_max_seconds(given: Any, tasks: dict[str, str]) -> float | dict[str, float]:
    """max_seconds= as declared: how long an episode may run on the robot's clock - one number of seconds for every
    task, or {task: seconds} naming each.
"""
    def seconds(value: Any, where: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise BenchmarkDefinitionError(f"@seq.benchmark {where} is a number of seconds, not {value!r}")
        return float(value)

    if given is None:
        raise BenchmarkDefinitionError("@seq.benchmark needs max_seconds=: how long an episode may run on the robot's "
                                       "clock, in seconds - max_seconds=15.0, or {task: seconds}")
    if not isinstance(given, dict):
        return seconds(given, "max_seconds=")
    unknown = [t for t in given if t not in tasks]
    if unknown:
        raise BenchmarkDefinitionError(f"max_seconds= names {unknown[0]!r}, which is not one of its tasks: "
                                       f"{', '.join(tasks)}")
    missing = [t for t in tasks if t not in given]
    if missing:
        raise BenchmarkDefinitionError(f"max_seconds= gives no limit for {', '.join(repr(t) for t in missing[:3])}"
                                       + (f" and {len(missing) - 3} more" if len(missing) > 3 else "")
                                       + ": one number of seconds for every task, or {task: seconds} naming each")
    return {t: seconds(v, f"max_seconds[{t!r}]") for t, v in given.items()}


def _resolve_driver(driver: Any, gpu: str) -> str | None:
    """driver= as declared: the NVIDIA driver's major version its card must have ("580"), None when it names none; a
    driver beside gpu="cpu", or anything but three digits, is refused while authoring."""
    from sequence_base.constants.cards import DRIVER, check_driver

    if driver is None:
        return None
    if not isinstance(driver, str) or not re.fullmatch(DRIVER, driver):
        raise BenchmarkDefinitionError(f"@seq.benchmark driver= is the NVIDIA driver's major version its card must have, "
                                       f"three digits as a string: driver=\"580\", not {driver!r}")
    try:
        check_driver(driver, gpu)
    except ValueError as exc:
        raise BenchmarkDefinitionError(f"@seq.benchmark {exc}") from None
    return driver


def _resolve_gpu(gpu: Any) -> str:
    """The benchmark's card: one of BENCHMARK_GPUS, or nothing (DEFAULT_BENCHMARK_GPU) — or "cpu", for a simulation
    that runs on the CPU.
    Any other card, or a list, is refused here, before anything is registered: a benchmark's machines run on one card
    (a list was a preference order, its first card the one they ran on)."""
    if gpu is None:
        return DEFAULT_BENCHMARK_GPU
    if isinstance(gpu, (list, tuple)):
        first = str(gpu[0]).strip() if gpu else ""
        one = CPU if first.lower() == CPU else first if first in BENCHMARK_GPUS else DEFAULT_BENCHMARK_GPU
        raise BenchmarkDefinitionError(f'@seq.benchmark gpu= takes one card, not a list: write gpu="{one}" '
                                       f'({_one_of(BENCHMARK_GPUS)}, or "cpu" for a simulation that runs on the CPU)')
    if isinstance(gpu, str) and gpu.strip().lower() == CPU:
        return CPU
    if gpu not in BENCHMARK_GPUS:
        raise BenchmarkDefinitionError(
            f"@seq.benchmark gpu= is {_one_of(BENCHMARK_GPUS)}, or \"cpu\" for a simulation that runs on the CPU; "
            f"not {gpu!r}")
    return gpu


def _one_of(names) -> str:
    """"L4 or RTX-PRO-6000": the cards said as a sentence offers them."""
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} or {names[-1]}"


def _cpu_sizes(cpu: Any, memory_gb: Any) -> tuple[int, Any]:
    """A CPU benchmark machine: `cpu` cores - a copy of its env on each - and `memory` GB for all of them
    (DEFAULT_GB_PER_CORE a core when not given)."""
    cores = DEFAULT_CPU_CORES if cpu is None else cpu
    if not isinstance(cores, int) or isinstance(cores, bool) or not 1 <= cores <= MAX_CPU_CORES:
        raise BenchmarkDefinitionError(
            f"@seq.benchmark(gpu=\"cpu\") cpu= is the cores one benchmark machine holds: an int from 1 to "
            f"{MAX_CPU_CORES}, not {cpu!r}")
    return cores, DEFAULT_GB_PER_CORE * cores if memory_gb is None else memory_gb


def _resolve_image(image: Any) -> ImageSpec:
    if image is None:


        return Image.debian_slim()._spec()
    if isinstance(image, Image):
        return image._spec()
    if isinstance(image, ImageSpec):
        return image
    raise BenchmarkDefinitionError(f"image= must be a seq.Image, got {type(image).__name__}")


def _resolve_secrets(secrets: Any) -> list[SecretRef]:
    out: list[SecretRef] = []
    for sec in secrets or []:
        if isinstance(sec, Secret):
            out.append(sec._ref())
        elif isinstance(sec, SecretRef):
            out.append(sec)
        else:
            raise BenchmarkDefinitionError(
                f"secrets entries must be seq.Secret.from_name(...), got {type(sec).__name__}"
            )
    return out


def _resolve_assets(assets: Any) -> list[VolumeRef]:
    """Lower `assets=` (a `seq.Volume`, or a list of them) to versioned `VolumeRef`s mounted at `/assets`. A single
    volume mounts at `/assets`; several are namespaced under `/assets/<name>` so they do not collide on one mount
    point."""
    if assets is None:
        return []
    vols = list(assets) if isinstance(assets, (list, tuple)) else [assets]
    out: list[VolumeRef] = []
    for vol in vols:
        if not isinstance(vol, Volume):
            raise BenchmarkDefinitionError(
                f"assets= entries must be seq.Volume.from_name(...), got {type(vol).__name__}"
            )
        mount = _ASSETS_MOUNT if len(vols) == 1 else f"{_ASSETS_MOUNT}/{vol.name}"
        out.append(vol._ref(mount))
    return out


def _resolve_replay(replay: Any, cls: type) -> ReplaySpec | None:
    """`replay=seq.Replay(engine=..., state=..., looks=...)` → the wire `ReplaySpec`: the eval's 3D replay. The methods
    it names must be the benchmark's own, and an adapter that reads the simulation ("mujoco", "sapien") needs `state`,
    the method it asks for an env's engine state; "own" hands its frames through seq.replay and names none.
    """
    if replay is None:
        return None
    if not isinstance(replay, ReplaySpec):
        raise BenchmarkDefinitionError(
            f"replay= must be a seq.Replay(engine=..., state=...), got {type(replay).__name__}")
    for role in ("state", "looks"):
        method = getattr(replay, role)
        if method is not None and not callable(getattr(cls, method, None)):
            raise BenchmarkDefinitionError(
                f"seq.Replay({role}={method!r}): {cls.__name__} has no method {method!r}")
    return replay




REPLAY_ADAPTERS = ("mujoco", "sapien", "isaac")


def _replay_engine(replay: ReplaySpec | None) -> ReplaySpec | None:
    """`replay` with its adapter said: the one it names, else "own". An adapter needs state=, the method that returns an
    env's engine state for the platform to read each step."""
    if replay is None:
        return None
    resolved = replay.engine or "own"
    if resolved in REPLAY_ADAPTERS and replay.state is None:
        raise BenchmarkDefinitionError(
            f"seq.Replay(engine={resolved!r}) needs state=, the method that returns an env's {resolved} state for "
            "the platform to read each step")
    return replay if resolved == replay.engine else replay.model_copy(update={"engine": resolved})
