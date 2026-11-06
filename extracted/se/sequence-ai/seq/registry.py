"""
Introspection → `PolicyRegistration`. Given a `@seq.policy`-decorated class, assemble its `PolicySpec`,
collect the `SeqFlags → method-name` bindings from the lifecycle decorators, validate the whole thing, and
produce the `PolicyRegistration` the harness loader introspects.

WHY the registration is built from the SHARED `sequence_base` types and nothing SDK-specific: a harness that
imports ONLY `sequence_base` (never any SDK authoring package) must be able to importlib-load the handler and
resolve every lifecycle entrypoint from a `PolicyRegistration` alone.



"""
from __future__ import annotations

import importlib.util
import inspect
import re
import sys
from typing import Any

from sequence_base.contract import (
    Concurrency,
    ImageSpec,
    InferParam,
    PolicyRegistration,
    PolicySpec,
    SecretRef,
    SeqFlags,
)
from sequence_base.by_name import INFER_PLATFORM, OBSERVE_PLATFORM, RESET_GONE
from sequence_base.constants.serving import MACHINE_CARDS, MAX_WARM_WORKERS

from seq._partial import Refused, hook, hooks_along, keeping, refused
from seq import named
from seq.errors import PolicyDefinitionError
from seq.image import Image
from seq.secret import Secret
from seq.weights import validate_weights_uri


_REG_ATTR = "__seq_registration__"


_RES_ATTR = "__seq_resources__"

_CTX_ATTR = "__seq_image_context__"

_LOCALS_ATTR = "__seq_image_locals__"


_IMAGE_DECLARED_ATTR = "__seq_image_declared__"

_MODELS_ATTR = "__seq_models__"

_MODEL_PREFIX = "accounts/sequences/models/"


def applied_by(frame: Any) -> tuple[str, dict] | None:
    """(its module's name, its globals) when `frame`, the caller of a decorator, is a module's top level - where
    `@seq.policy(...)` on a class, or `seq.policy(...)(Cls)` by hand, runs - else None (a function of the user's or the
    SDK's own applied it)."""
    if frame is None or frame.f_code.co_name != "<module>":
        return None
    name = frame.f_globals.get("__name__")
    return (name, frame.f_globals) if isinstance(name, str) else None


def build_registration(cls: type, policy_kwargs: dict[str, Any], *, applied: tuple[str, dict] | None = None) -> type:
    """The `@seq.policy` decorator body: validate + register `cls`, attach the `PolicyRegistration`, return. `applied`:
    the module that applied it (applied_by), when it applied it at its top level.

    Upstream trigger: `@seq.policy(...)` on a user class. Downstream: `registration(cls)` / a deploy step /
    the harness reads the attached `PolicyRegistration`.
    """



    bindings, plan_every_s = None, None
    try:



        if _REG_ATTR in cls.__dict__:
            raise PolicyDefinitionError(
                f"@seq.policy is applied more than once to {cls.__name__}; apply it exactly once"
            )


        bindings, plan_every_s = _collect_bindings(cls)
        return _register(cls, policy_kwargs, bindings, plan_every_s, applied)
    except PolicyDefinitionError as exc:
        if not keeping():
            raise
        return refused(cls, _REG_ATTR, exc, bindings, plan_every_s)


def _register(cls: type, policy_kwargs: dict[str, Any], bindings: dict[SeqFlags, str],
              plan_every_s: float | None, applied: tuple[str, dict] | None = None) -> type:
    """The registration of `cls` from its declaration and its bindings, attached; raises what it refuses."""




    if SeqFlags.RESET in bindings:
        raise PolicyDefinitionError(f"{cls.__name__}.{bindings[SeqFlags.RESET]}: {RESET_GONE}")




    constructor = named.constructor(cls, policy_kwargs)

    named.check(cls, bindings)

    if SeqFlags.PLAN in bindings:
        _check_plan(cls, bindings)



    spec = _assemble_spec(cls, policy_kwargs, bindings, episodes_of(cls, bindings))


    _validate(cls, spec, bindings)
    if SeqFlags.PLAN in bindings:
        why = plan_layout(spec.gpu)
        if why:
            raise PolicyDefinitionError(f"{cls.__name__}: {why}")





    handler_ref = _ref_kept(cls, applied)


    reg = PolicyRegistration(
        spec=spec, bindings=bindings, handler_ref=handler_ref, plan_every_s=plan_every_s, constructor=constructor
    )
    setattr(cls, _REG_ATTR, reg)
    return cls


def _check_plan(cls: type, bindings: dict[SeqFlags, str]) -> None:
    """The policy's @seq.plan, held to the words the worker says (sequence_base.by_name.plan_refused): `def plan(self,
    robot)`, plain or async, returning what it says, and an act function that takes `episode` to read the plans."""
    from sequence_base.by_name import plan_refused

    infer = bindings.get(SeqFlags.INFER)
    why = plan_refused(hook(cls, bindings[SeqFlags.PLAN]),
                       infer_takes_episode=infer is not None and _takes_episode(cls, infer))
    if why:
        raise PolicyDefinitionError(f"{cls.__name__}: {why}")


def registration(cls: type) -> PolicyRegistration:
    """Return the `PolicyRegistration` attached by `@seq.policy`.

    WHY it raises when absent: introspecting a class that was never `@seq.policy`-decorated (a bare class,
    or lifecycle decorators without the class decorator) has no registration to give — that is a user error
    and must be readable, not an `AttributeError`.

    """
    reg = cls.__dict__.get(_REG_ATTR)
    if reg is None:
        raise PolicyDefinitionError(
            f"{cls.__name__} is not a @seq.policy class (no registration); decorate it with @seq.policy(...)"
        )
    if isinstance(reg, Refused):
        reg.refuse()
    return reg


def _collect_bindings(cls: type) -> tuple[dict[SeqFlags, str], float | None]:
    """Every lifecycle hook of the class - its own decorated methods, and those it inherits from a policy or a mixin
    it is built on - as flag→method-name bindings, the raw functions restored. Returns (bindings, plan_every_s).

    WHY along the MRO (seq._partial.hooks_along), where only the class's own attributes were read: a subclass of a
    policy had none of its parent's hooks ("has no @seq.infer method"). Restoring raw functions still never mutates a
    shared base class: a base is read, `cls` alone is written. Two methods of one class claiming one flag are refused,
    as before.
    """
    return hooks_along(cls, _REG_ATTR, PolicyDefinitionError)




_OWN_STATE = (SeqFlags.ON_EPISODE, SeqFlags.OBSERVE)


def episodes_of(cls: type, bindings: dict[SeqFlags, str] | None) -> str | None:
    """How a policy keeps an episode's state, from how it is written (PolicySpec.episodes) - never declared:
    "shared" - its @seq.infer is @seq.concurrent, a batch's episodes handed to it as a list, with an @seq.observe or
    @seq.on_episode method or not (an episode's start and end hand it that episode's alone); else "own" - an
    @seq.observe method that does not take `episode`, whatever infer takes; else "shared" - its @seq.infer takes
    `episode`, the platform's seq.Episode, kept on the copy serving it - and its @seq.observe method too, when it has one:
    what they keep is in episode.state and episode.local; else "own" - an @seq.on_episode method beside an infer handed no
    episode keeps it on the class, so an episode holds a copy of its own; else None - it keeps none. A policy has no
    @seq.reset (_register refuses one): its @seq.on_episode runs as an episode begins, episode.phase "start".
    


"""
    bindings = bindings or {}
    infer = bindings.get(SeqFlags.INFER)
    if infer is not None:
        if getattr(hook(cls, infer), "__seq_concurrent__", None):
            return "shared"
        if SeqFlags.OBSERVE in bindings and not _takes_episode(cls, bindings[SeqFlags.OBSERVE]):
            return "own"
        if _takes_episode(cls, infer):
            return "shared"
    return "own" if any(f in bindings for f in _OWN_STATE) else None


def _takes_episode(cls: type, name: str) -> bool:
    """Whether the method `name` names `episode` among its arguments, which says its state is kept there: **kwargs,
    though the worker hands it one too, says nothing of where."""
    try:
        return "episode" in inspect.signature(hook(cls, name)).parameters
    except (TypeError, ValueError):
        return False



_CONTAINERS = ("list[", "List[", "Sequence[", "tuple[", "Tuple[", "Iterable[")


def _one_annotation(infer: Any, name: str, kind: str) -> str | None:
    """The annotation of infer's `name` as written, when it says one `kind` (seq.Episode) - a
    @seq.concurrent infer is handed a list of them - else None (no annotation, or a list of them)."""
    try:
        param = inspect.signature(infer).parameters.get(name)
    except (TypeError, ValueError):
        return None
    ann = None if param is None else param.annotation
    if ann is None or ann is inspect.Parameter.empty:
        return None
    text = (ann if isinstance(ann, str) else getattr(ann, "__qualname__", None) if isinstance(ann, type)
            else repr(ann)).replace(" ", "")
    if kind not in text or text.startswith(_CONTAINERS):
        return None
    return text


def _assemble_spec(cls: type, kw: dict[str, Any], bindings: dict[SeqFlags, str] | None = None,
                   episodes: str | None = None) -> PolicySpec:
    """Lower the `@seq.policy` kwargs (+ handles + concurrency) into the wire `PolicySpec`, verbatim/typed.

    WHY each value passes through unchanged: the goal requires "the values as the user wrote them" — a captured gpu
    list is the same list, a captured weights URI is the same string.

    """

    if "gpu" not in kw:


        raise PolicyDefinitionError('@seq.policy requires gpu=...: the one card it runs on, e.g. gpu="L4" '
                                    '("H100:2" is two of them), or "cpu"')
    gpu = kw["gpu"]
    if isinstance(gpu, (list, tuple)):


        first = str(gpu[0]) if gpu else "L4"
        raise PolicyDefinitionError(f'@seq.policy gpu= takes one card, not a list: write gpu="{first}", the card it runs '
                                    'on ("H100:2" is two of one type, "cpu" none)')









    weights_name, extra_weights = None, None
    if kw.get("weights") is None:

        weights = None
    elif isinstance(kw["weights"], dict):
        parts = dict(kw["weights"])
        if not parts:
            raise PolicyDefinitionError("@seq.policy(weights={...}) needs at least one named part")
        from sequence_base.contract.policy import check_weights_parts

        weights_name = next(iter(parts))
        try:
            check_weights_parts(weights_name, {n: None for n in list(parts)[1:]})
        except ValueError as exc:
            raise PolicyDefinitionError(f"@seq.policy(weights={{...}}): {exc}") from None
        weights = validate_weights_uri(parts[weights_name])
        extra_weights = {name: validate_weights_uri(uri) for name, uri in list(parts.items())[1:]} or None
    else:
        weights = validate_weights_uri(kw["weights"])




    image = kw.get("image")
    setattr(cls, _IMAGE_DECLARED_ATTR, "image=" if image is not None else None)
    if image is None:
        image_spec = Image.debian_slim()._spec()
    elif isinstance(image, Image):
        image_spec = image._spec()
    elif isinstance(image, ImageSpec):
        image_spec = image
    else:
        raise PolicyDefinitionError(
            f"image= must be a seq.Image, got {type(image).__name__}"
        )


    secrets: list[SecretRef] = []
    for sec in (kw.get("secrets") or []):
        if isinstance(sec, Secret):
            secrets.append(sec._ref())
        elif isinstance(sec, SecretRef):
            secrets.append(sec)
        else:
            raise PolicyDefinitionError(
                f"secrets entries must be seq.Secret.from_name(...), got {type(sec).__name__}"
            )










    cpu, cpu_limit = _size(kw, "cpu")
    memory_gb, memory_limit_gb = _size(kw, "memory")
    setattr(cls, _RES_ATTR, {"cpu": cpu, "cpu_limit": cpu_limit, "memory_gb": memory_gb,
                             "memory_limit_gb": memory_limit_gb})
    _check_scaling(kw)
    concurrency = _concurrency(cls, kw, bindings or {})
    _check_card_split(gpu, concurrency)
    setattr(cls, _CTX_ATTR, image.context if isinstance(image, Image) else None)
    setattr(cls, _LOCALS_ATTR, (image.local_files, image.python_sources) if isinstance(image, Image) else ((), ()))
    setattr(cls, _MODELS_ATTR, _models(kw))
    fields: dict[str, Any] = {
        "name": _name(kw, cls),
        "gpu": gpu,
        "image": image_spec,
        "weights": weights,
        "weights_name": weights_name,
        "extra_weights": extra_weights,
        "secrets": secrets,
        "concurrency": concurrency,
        "episodes": episodes,
    }


    for declared, field in (
        ("min_workers", "min_containers"), ("buffer_workers", "buffer_containers"), ("max_gpus", "max_gpus"),
        ("hz", "hz"), ("action_chunk_valid_len", "action_chunk_valid_len"),
        ("action_chunk_replan_at", "action_chunk_replan_at"), ("max_wait_for_batch", "max_wait_for_batch"),
    ):
        if declared in kw:
            fields[field] = kw[declared]
    try:
        return PolicySpec(**fields)
    except Exception as exc:
        raise PolicyDefinitionError(f"invalid @seq.policy declaration: {exc}") from exc








NEW_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}")
NAME_RULE = "name must be 1-64 letters, digits, '_' or '-', starting with a letter or digit"


def check_new_name(name: Any) -> str:
    """`name` when it is a deployment name the platform takes for a new one, else the platform's own words for why not -
    said here, where it is written, before anything is uploaded."""
    if not isinstance(name, str) or not NEW_NAME.fullmatch(name):
        raise PolicyDefinitionError(f"{NAME_RULE}, got {name!r}")
    return name


def _name(kw: dict[str, Any], cls: type) -> str:
    """name=: what robots connect to and the console lists — the platform's deployment-name rule (check_new_name),
    checked here so a bad one fails where it is written. Without it the class name, lower-case with hyphens (MyReacher
    → my-reacher, as pi05-droid is written), which `seq deploy --name` may still override, held to the same rule.
    """
    v = kw.get("name")
    if v is None:
        from seq.adapter import default_name

        return default_name(cls.__name__)
    return check_new_name(v)






_SIZE_RANGE = {"cpu": (0.125, 64.0, 64.0), "memory": (0.125, 336.0, 336.0)}


def _size(kw: dict[str, Any], name: str) -> tuple[float | None, float | None]:
    """cpu= (cores) / memory= (GiB) as (request, limit): a number is the request, `(request, limit)` adds a hard cap.

    Without a limit the worker may use more than it requested; either way CPU and memory are billed per second on the
    greater of the request and actual use. Undeclared → (None, None): the platform requests its minimum, 0.125 cores
    and 0.125 GiB — never a guessed 8 / 32 that every worker would pay for."""
    v = kw.get(name)
    if v is None:
        return None, None
    unit = "cores" if name == "cpu" else "GiB"
    low, top, limit_top = _SIZE_RANGE[name]
    if isinstance(v, (tuple, list)) and len(v) != 2:
        raise PolicyDefinitionError(f"{name}= is a number of {unit}, or (request, limit); got {v!r}")
    request, limit = (v[0], v[1]) if isinstance(v, (tuple, list)) else (v, None)
    for what, x, high in (("request", request, top), ("limit", limit, limit_top)):
        if what == "limit" and x is None:
            continue
        if isinstance(x, bool) or not isinstance(x, (int, float)) or not low <= x <= high:
            raise PolicyDefinitionError(f"{name}= {what} must be a number of {unit} from {low:g} to {high:g}, got {x!r}")
    if limit is not None and limit < request:
        raise PolicyDefinitionError(f"{name}=({request!r}, {limit!r}): the limit must be at least the request")
    return float(request), (float(limit) if limit is not None else None)


def _check_scaling(kw: dict[str, Any]) -> None:
    """max_gpus= / min_workers= / buffer_workers=, refused where they are written with what each means.
    """
    v = kw.get("max_gpus")


    if v is not None and (isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= 256):
        raise PolicyDefinitionError(f"max_gpus= is the most GPUs this deployment may hold at once (counted in cards), "
                                    f"a whole number from 1 up to your account's limit (`seq account` shows it), which "
                                    f"a GPU policy must declare; got {v!r}")



    for knob, what in (("min_workers", "warm workers kept running, robot or not"),
                       ("buffer_workers", "spare workers kept running while robots are connected")):
        if knob in kw:
            v = kw[knob]
            if isinstance(v, bool) or not isinstance(v, int) or not 0 <= v <= MAX_WARM_WORKERS:
                raise PolicyDefinitionError(f"{knob}= is the {what}, a whole number from 0 to {MAX_WARM_WORKERS}; "
                                            f"got {v!r}")


def _concurrency(cls: type, kw: dict[str, Any], bindings: dict[SeqFlags, str]) -> Concurrency | None:
    """How a worker serves robots, for the deploy request: `@seq.concurrent(sizes=[...])` from the infer method, and
    the layout of a worker of several cards from `@seq.policy(gpus_per_replica=..., replica_start=...)` - the wire
    keeps them in PolicySpec.concurrency. None when none is declared: one robot a copy, as ever.
    `@seq.concurrent` on any other method would be read by nothing, so it is refused.

    """
    infer = bindings.get(SeqFlags.INFER)
    for name, member in vars(cls).items():
        if name != infer and getattr(member, "__seq_concurrent__", None):
            raise PolicyDefinitionError(f"{cls.__name__}.{name}: @seq.concurrent goes on the @seq.infer method")
    declared = dict(getattr(vars(cls).get(infer), "__seq_concurrent__", None) or {}) if infer else {}

    declared.pop("collate", None)
    if "sizes" in declared:

        from seq.policy import policy_sizes

        declared["sizes"] = policy_sizes(declared["sizes"])
    per, start = kw.get("gpus_per_replica"), kw.get("replica_start")
    if per is not None and (isinstance(per, bool) or not isinstance(per, int) or per < 1):
        raise PolicyDefinitionError(f"@seq.policy(gpus_per_replica=...) must be a positive whole number, got {per!r}")
    if start is not None and start not in ("together", "one_by_one"):
        raise PolicyDefinitionError(f'@seq.policy(replica_start=...) is "together" or "one_by_one", got {start!r}')
    fields = {**declared, "gpus_per_replica": per, "replica_start": start}
    fields = {k: v for k, v in fields.items() if v is not None}
    if not fields:
        return None
    try:
        return Concurrency(**fields)
    except Exception as exc:
        raise PolicyDefinitionError(f"invalid concurrency declaration: {exc}") from exc






def _cards(gpu: Any) -> int:
    """The cards a worker holds: N of `gpu="TYPE:N"`, one for a single card or "cpu"."""
    _, sep, n = str(gpu).partition(":")
    return int(n) if sep and n.strip().isdigit() else 1


def _check_card_split(gpu: Any, concurrency: Any) -> None:
    """gpus_per_replica must divide a worker's cards (`gpu="TYPE:N"`): a worker splits its cards into groups of that
    size, one model copy per group."""
    per = getattr(concurrency, "gpus_per_replica", None)
    if not per or per == 1:
        return
    cards = _cards(gpu)
    if cards % per:
        raise PolicyDefinitionError(f"gpus_per_replica={per} does not divide {gpu!r}'s {cards} card(s): a worker "
                                    "splits its cards into groups of gpus_per_replica, one model copy per group")


def _models(kw: dict[str, Any]) -> tuple[str, ...]:
    """models=: the platform models the policy calls, each a catalogue name ("qwen3-8-27b") or full id, as full ids.
    Whether each exists is the platform's to say — `seq deploy` is refused with the list when one does not — so this
    only checks the shape: a list of names, each once."""
    v = kw.get("models")
    if v is None:
        return ()
    if isinstance(v, str) or not isinstance(v, (list, tuple)):
        raise PolicyDefinitionError(f'models= must be a list of model names, e.g. models=["qwen3-8-27b"], got {v!r}')
    out: list[str] = []
    for name in v:
        if not isinstance(name, str) or not name.strip() or name != name.strip():
            raise PolicyDefinitionError(f"models= entries are catalogue names like 'qwen3-8-27b', got {name!r}")
        full = name if "/" in name else _MODEL_PREFIX + name
        if full in out:
            raise PolicyDefinitionError(f"models= names {name!r} twice")
        out.append(full)
    return tuple(out)


def models_declared(cls: type) -> list[str] | None:
    """The full catalogue ids of the models the policy declared it calls, or None when it declared none."""
    return list(getattr(cls, _MODELS_ATTR, ()) or ()) or None


def resources_declared(cls: type) -> dict[str, Any]:
    """The worker size the policy declared ({"cpu", "cpu_limit", "memory_gb", "memory_limit_gb"}, None where it
    declared nothing)."""
    return {"cpu": None, "cpu_limit": None, "memory_gb": None, "memory_limit_gb": None,
            **(getattr(cls, _RES_ATTR, None) or {})}


def locals_declared(cls: type) -> tuple[tuple[tuple[str, str], ...], tuple[str, ...]]:
    """(local files, Python modules) the policy's image declared with seq.Image.add_local_*."""
    return getattr(cls, _LOCALS_ATTR, ((), ()))


def image_declared(cls: type) -> str | None:
    """"image=" when the policy wrote one, None when it did not."""
    return getattr(cls, _IMAGE_DECLARED_ATTR, None)


def context_declared(cls: type) -> str | None:
    """The Dockerfile's build context directory the policy's image declared, if any."""
    return getattr(cls, _CTX_ATTR, None)


def _validate(cls: type, spec: PolicySpec, bindings: dict[SeqFlags, str]) -> None:
    """Cross-cutting checks that need spec + bindings together: INFER presence/shape, and how the episodes it keeps meet
    @seq.concurrent. Raises a readable error rather than producing an unservable registration."""


    if SeqFlags.INFER not in bindings:
        raise PolicyDefinitionError(
            f"{cls.__name__} has no @seq.infer method; a policy needs a per-step entrypoint"
        )



    if SeqFlags.OBSERVE not in bindings:
        _check_infer_signature(cls, bindings[SeqFlags.INFER])




    if getattr(hook(cls, bindings[SeqFlags.INFER]), "__seq_concurrent__", None):
        for asked, name, kind, what in ((spec.episodes == "shared", "episode", "Episode", "episodes"),):
            written = _one_annotation(hook(cls, bindings[SeqFlags.INFER]), name, kind) if asked else None
            if written:
                raise PolicyDefinitionError(
                    f"{cls.__name__}: a @seq.concurrent infer is handed a batch's {what} as a list, one for each "
                    f"observation in order - annotate it `{name}: list[seq.{kind}]`, not `{name}: {written}`")



        if SeqFlags.SAMPLE not in bindings:
            raise PolicyDefinitionError(
                f"{cls.__name__}: @seq.concurrent needs @seq.sample - its build check times each listed batch size on "
                "the class's sample episode. Mark a method that returns one episode's calls in order, "
                "[(\"observe\", what a robot's observe() sends), (\"act\",), ...], with @seq.sample")



def _accepts_named(fn: Any, name: str) -> bool:
    """Whether `fn` takes an argument called `name`, by name or **kwargs - as the worker hands it one (its _accepts)."""
    try:
        params = inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return False
    return name in params or any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values())


def _check_infer_signature(cls: type, method_name: str) -> None:
    """Verify the infer method can receive an observation argument (beyond `self`)."""
    fn = hook(cls, method_name)

    sig = inspect.signature(fn)
    params = list(sig.parameters.values())

    rest = params[1:] if params else []

    can_take_obs = any(
        p.kind
        in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.VAR_POSITIONAL,
        )
        for p in rest
    )
    if not can_take_obs:
        raise PolicyDefinitionError(
            f"{cls.__name__}.{method_name} must accept an observation argument, e.g. "
            "def infer(self, obs, *, seed=None)"
        )


def plan_one_machine(card: str) -> str:
    """Why a policy with a @seq.plan does not run across several machines, `card` the type it declared: every machine
    of the copy has a `self` of its own and would plan its robots apart. The worker says the same
, and the gateway (deployments/validation.py plan_one_machine)."""
    return (f"a policy with a @seq.plan runs on one machine: across several, each machine would plan apart. Declare at "
            f'most {MACHINE_CARDS} cards (gpu="{card}:{MACHINE_CARDS}")')


def plan_layout(gpu: Any) -> str | None:
    """Why a policy with a @seq.plan cannot run as it declares, or None: its episode plans in the copy that holds it, so
    it runs on one machine (more cards than a machine holds is plan_one_machine). Several copies on one machine are
    fine: a robot's episode is on one of them. The gateway holds a deploy to the same rule (deployments/validation.py
    _check_plan), and the worker before its weights load."""
    if _cards(gpu) > MACHINE_CARDS:
        return plan_one_machine(str(gpu).partition(":")[0])
    return None


def infer_params(cls: type) -> dict[str, InferParam]:
    """The inference parameters a policy declares - its @seq.infer's and its @seq.observe's - `def infer(self, obs, *,
    seed=None, replan_steps: int = 5)` declares `replan_steps` - each with its type (the annotation, else its
    default's) and default. The deployment's defaults (`seq policy set`) or an eval may set them, never an act, which
    carries none; the worker passes each method only the ones it takes, cast to their type. The same rules as an
    adapter's and a benchmark's (seq/params.py). A method that takes its inputs by name declares none: each of its
    arguments is a key of the inputs; one that takes them whole declares those of its arguments with a default that can
    be one, the others keeping their defaults. A name both declare is declared the same by both, or refused.
    
"""
    declared = _infer_params(cls)
    reg = registration(cls)
    observe = reg.bindings.get(SeqFlags.OBSERVE)
    if observe is None:
        return declared
    from seq.params import keyword_params

    if named.inputs_by_name(cls, "observe", observe) is not None:
        return declared
    seen = keyword_params(hook(cls, observe), f"{cls.__name__}.{observe}", PolicyDefinitionError,
                          kind="inference parameter", skip=OBSERVE_PLATFORM, skip_first=True, loose=True)
    for name, param in seen.items():
        if name in declared and declared[name] != param:
            raise PolicyDefinitionError(
                f"{cls.__name__}: the inference parameter {name!r} is declared by both "
                f"{cls.__name__}.{reg.bindings[SeqFlags.INFER]} and {cls.__name__}.{observe}, differently "
                f"({declared[name].model_dump(exclude_none=True)} and {param.model_dump(exclude_none=True)}): "
                "declare it the same in both, or in one")
    return {**declared, **seen}


def _infer_params(cls: type) -> dict[str, InferParam]:
    """What its @seq.infer declares (infer_params)."""
    from seq.params import keyword_params

    reg = registration(cls)
    name = reg.bindings[SeqFlags.INFER]

    takes_input = SeqFlags.OBSERVE not in reg.bindings


    if takes_input and named.inputs_by_name(cls, "infer", name) is not None:
        return {}


    return keyword_params(hook(cls, name), f"{cls.__name__}.{name}", PolicyDefinitionError,
                          kind="inference parameter", skip=INFER_PLATFORM, skip_first=takes_input, loose=True)


def _handler_ref(cls: type, applied: tuple[str, dict] | None = None) -> str:
    """Build and validate the importable `module.path:ClassName` reference. `applied`: the module that applied the
    decorator at its top level (applied_by) - when that is not the class's own, the decorator applied there by hand to
    a class it imported (`from awomo.policy import Awomo` → `seq.policy(...)(Awomo)`, the one file that declares a
    class left as it is), the reference is that module's and the name it holds the class by: the worker imports that
    module, which applies the decorator, and finds the class there.


    WHY validate importability: the harness loads the class from this string with importlib; a class in `__main__`,
    a REPL, a function local, or an unloadable module yields a string that would only blow up at load time. Caught
    with a readable message - for a @seq.policy class where it is deployed (_ref_kept keeps it on the class;
    importable raises it), never where the class is written, which runs there as before the decorator.



    """
    module, qualname = _applied_name(cls, applied)
    _check_importable(module, qualname)
    return f"{module}:{qualname}"


def _applied_name(cls: type, applied: tuple[str, dict] | None) -> tuple[str, str]:
    """(module, qualname) the worker finds `cls` by: its own, or - the decorator applied by hand at the top of
    another module (_handler_ref) - that module's and the name it holds the class by. A declaring file that holds it by
    no name is refused where it is written, saying how to import it there: the fix is that file's, and nothing later
    would say it (`seq deploy` reads the folder and finds no class to deploy)."""
    module = cls.__module__
    qualname = cls.__qualname__
    if applied is not None and applied[0] != module:
        here, names = applied
        held = cls.__name__ if names.get(cls.__name__) is cls else next(
            (n for n, v in names.items() if v is cls and not n.startswith("__")), None)
        if held is None:
            raise PolicyDefinitionError(
                f"{qualname} is a class of {module}, decorated in {here}, which does not hold it by a name of its own; "
                f"import it there by name (from {module} import {cls.__name__}) and decorate that"
            )
        module, qualname = here, held
    return module, qualname


def _check_importable(module: str, qualname: str) -> None:
    """Refuse a reference no other process can import: a class in __main__ or a REPL, one defined inside a function,
    or one of a module that cannot be loaded."""

    if module == "__main__" or module is None:
        raise PolicyDefinitionError(
            f"{qualname} is defined in __main__/REPL and is not importable; put it in an importable module"
        )


    if "<locals>" in qualname:
        raise PolicyDefinitionError(
            f"{qualname} is defined inside a function/closure and is not importable; define it at module top level"
        )


    if module not in sys.modules:
        try:
            found = importlib.util.find_spec(module)
        except (ImportError, ValueError):
            found = None
        if found is None:
            raise PolicyDefinitionError(
                f"module {module!r} for {qualname} is not importable; the platform cannot load it"
            )




_UNIMPORTABLE_ATTR = "__seq_unimportable__"


def _ref_kept(cls: type, applied: tuple[str, dict] | None = None) -> str:
    """`cls`'s handler_ref (_handler_ref), for a @seq.policy, @seq.benchmark or @seq.adapter class -
    and, for one no other process can import (written in a script run as `python file.py` or in a notebook, __main__;
    inside a function; in a module that cannot be imported), its module:qualname as written, the refusal kept on the
    class (_UNIMPORTABLE_ATTR) and raised where the platform needs the import (importable: seq deploy and its dry run,
    seq adapter push). Where the class is written it runs as it did before the decorator: its methods are its author's.
    {/docs/policy/ "A class you already have": "THE CLASS KEEPS RUNNING LOCALLY AS BEFORE"}

"""
    module, qualname = _applied_name(cls, applied)
    try:
        _check_importable(module, qualname)
    except PolicyDefinitionError as exc:
        setattr(cls, _UNIMPORTABLE_ATTR, exc)
    return f"{module}:{qualname}"


def importable(cls: type) -> None:
    """Raise why another process cannot import `cls`, when its decorator kept a reason (_ref_kept): asked where its
    handler_ref is put to use - seq.deploy.deployment_request (`seq deploy`, its dry run, seq.deploy()), a
    benchmark's benchmark_request and an adapter's registration_body (`seq adapter push`). A class `seq deploy`
    imports from its file is that file's module, never __main__."""
    why = cls.__dict__.get(_UNIMPORTABLE_ATTR)
    if why is not None:
        raise why.with_traceback(None)
