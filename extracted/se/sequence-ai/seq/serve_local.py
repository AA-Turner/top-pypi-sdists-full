"""
`seq serve [folder]`: a @seq.policy served from this machine's GPU - the class its folder declares, built as the platform
builds it, with its template's own weights read with your key - to robots that connect to this machine with
`sequence_ai.connect("http://<this machine>:8000")`.

In one sentence: the folder's class, found and imported as `seq deploy` finds it (seq.loading) → each of its weights
parts a folder here: an official template's fetched by weights_get, an hf:// repo downloaded by huggingface_hub, or the
folder `--weights` names → the class built and run by the platform worker's own adapter, the public
sequence_ai.engine.adapter.RegisteredAdapter: its init= filled, its @seq.infer, @seq.observe, @seq.on_episode and
@seq.plan as a deployment runs them, a @seq.concurrent policy's acts stacked into one batch → served by
the engine's serve() with that adapter as the copy each robot's stream goes to (sequence_ai.engine.episodes.PolicyCopy):
each episode's frames in order, its acts, its end, its plans on their clock; each robot's acts held for a batch and its
robots seated by how the policy declares its answers play (hz, action_chunk_valid_len, action_chunk_replan_at,
max_wait_for_batch), as the platform's workers hold and seat them - the speed-ups that keep its answers the same tried
first on its sample episode's observations (sequence_ai.engine.optimize) → @seq.shutdown when it stops.

WHY the platform's own adapter: one template runs on the platform or on a GPU of your own, and only where the GPU is
changes, so its code answers here as it does there, decorator for decorator.
WHY a plan runs here only when it declares no models=: a model of the platform is called with the credential a
deployment's machine is handed for the models it declared, which a machine of your own is never handed; a plan that
declares none calls a model service of its own with sequence_ai.chat(server=...) from anywhere.
"""
from __future__ import annotations

import errno
import inspect
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from seq.errors import PolicyDefinitionError


@dataclass
class Served:
    """What `seq serve` hands the engine's serve(): the call, its batch sizes (None: one act a call), an observation to warm
    it with, what to run when it stops, the copy each robot's stream goes to (its adapter: episodes, observe,
    on_episode, plans), the observations its speed-ups are checked on (its sample episode's), and how its answers play
    on its robots as serve() takes it (hz, action_chunk_valid_len, action_chunk_replan_at, max_wait_for_batch; empty
    where it declares too little to hold or seat its robots by)."""
    name: str
    call: Callable[[Any], Any]
    batch: list[int] | None
    example: Any
    shutdown: Callable[[], Any]
    copy: Any = None
    examples: list = field(default_factory=list)
    plays: dict | None = None


def parse_weights(given: list[str] | None) -> dict[str | None, str]:
    """`--weights DIR` (a policy's one part) and `--weights PART=DIR` (a named part), as {part or None: folder}."""
    out: dict[str | None, str] = {}
    for item in given or []:
        part, eq, folder = item.partition("=")
        if eq and part and not os.path.isdir(item):
            out[part] = folder
        else:
            out[None] = item
    return out


def weights_dirs(spec: Any, given: dict[str | None, str], *, api_key: str | None, base_url: str | None,
                 say: Callable[[str], Any]) -> Any:
    """Each weights part of `spec` (a PolicySpec) as a folder here, in the form the class's init= is filled with: the
    folder, for weights in one part; {part: folder} for named parts; None for none."""
    parts: dict[str | None, str] = {}
    if spec.weights:
        parts[spec.weights_name] = spec.weights
    parts.update({str(n): uri for n, uri in (spec.extra_weights or {}).items()})
    if not parts:
        return None
    folders = {}
    for part, uri in parts.items():
        named = given.get(part) or (given.get(None) if len(parts) == 1 else None)
        folders[part] = named if named is not None else _local(uri, part, api_key=api_key, base_url=base_url, say=say)
    if list(folders) == [None]:
        return folders[None]
    return folders


def _local(uri: str, part: str | None, *, api_key: str | None, base_url: str | None,
           say: Callable[[str], Any]) -> str:
    """One weights URI as a folder of this machine."""
    from sequence_base.contract.templates import TEMPLATE_SCHEME, parse_template

    flag = f"--weights {part}=<folder>" if part else "--weights <folder>"
    if uri.startswith(TEMPLATE_SCHEME):
        from seq import weights_get

        name, version = parse_template(uri)
        return str(weights_get.fetch(name, version, api_key=api_key, base_url=base_url, say=say))
    if uri.startswith("hf://"):
        try:
            from huggingface_hub import snapshot_download
        except ImportError:
            raise PolicyDefinitionError(f"{uri} is a Hugging Face repo: pip install huggingface_hub, or download it "
                                        f"and name its folder with {flag}") from None
        repo, _, revision = uri[len("hf://"):].strip("/").partition("@")
        say(f"downloading {repo}{'@' + revision if revision else ''} from Hugging Face")
        return snapshot_download(repo, revision=revision or None)
    raise PolicyDefinitionError(f"{uri} is kept on the platform: download it and name its folder with {flag}")


def build(folder: str | os.PathLike, name: str | None = None, *, weights: list[str] | None = None,
          api_key: str | None = None, base_url: str | None = None, say: Callable[[str], Any] = print) -> Served:
    """The folder's @seq.policy, built here as the platform builds it - by the platform worker's own adapter - the copy
    and call that serve it, and the call its speed-ups are tried on, as the platform tries a version's
    (checked_call)."""
    from types import SimpleNamespace

    from sequence_base.contract import SeqFlags

    from seq.loading import load_folder
    from seq.registry import models_declared, registration
    from sequence_ai.engine.adapter import RegisteredAdapter
    from sequence_ai.engine.episodes import PolicyCopy

    folder = Path(folder)
    _, cls = load_folder(folder, name, verb="serve")
    reg = registration(cls)
    spec = reg.spec





    models = models_declared(cls)
    if SeqFlags.PLAN in reg.bindings and models:
        raise PolicyDefinitionError(f"{spec.name}'s plan declares models={_names(models)}, models seq serve cannot "
                                    "call: have its plan call a model with your own key - sequence_ai.chat(model, "
                                    'messages, server="openrouter") - and drop models=')


    if spec.secrets:
        say(f"{spec.name} declares secrets {', '.join(ref.name for ref in spec.secrets)}: seq serve puts nothing in its "
            "environment - set the variables they hold yourself before it serves")
    dirs = weights_dirs(spec, parse_weights(weights), api_key=api_key, base_url=base_url, say=say)



    adapter = RegisteredAdapter(cls, SimpleNamespace(registration=reg, cls=cls))
    adapter.load(dirs)






    copy = PolicyCopy(adapter, checked=_checked(adapter._inst)[0])
    examples = _observed(adapter.sample())
    return Served(spec.name, copy.call, copy.batch, examples[0] if examples else None, adapter.shutdown, copy,
                  examples, _plays(spec))


def _plays(spec: Any) -> dict:
    """How the policy's answers play on its robots, as serve() takes it, from what it declares: its hz, with its
    action_chunk_valid_len or action_chunk_replan_at, and its max_wait_for_batch where set; empty where it declares no
    hz or neither number, whose robots the platform holds for no batch."""
    hz, valid, replan = spec.hz, spec.action_chunk_valid_len, spec.action_chunk_replan_at
    if not hz or (valid is None and replan is None):
        return {}
    plays = {"hz": hz, "action_chunk_valid_len": valid, "action_chunk_replan_at": replan,
             "max_wait_for_batch": spec.max_wait_for_batch}
    return {key: value for key, value in plays.items() if value is not None}


def _names(models: list[str]) -> list[str]:
    """Catalogue ids as the policy names them: accounts/sequences/models/qwen3-8-27b as qwen3-8-27b."""
    return [m.rsplit("/", 1)[-1] for m in models]


def _observed(sample: list | None) -> list:
    """The observations of the class's sample episode (@seq.sample), in its order: the first is what the server warms
    on before it says it is ready, and all of them what its speed-ups are checked on. [] for a class without one."""
    return [call[1] for call in sample or [] if isinstance(call, (list, tuple)) and len(call) >= 2 and call[0] == "observe"]


def checked_call(instance: Any) -> tuple[Callable[[Any], Any], list[int] | None, list]:
    """What an instance of a @seq.policy class is served and checked by: the call (one act's observation in, its answer
    out; with batch sizes, a batch's acts), its batch sizes (None: one act a call), and its sample episode's
    observations - the call and the observations sequence_ai.engine.optimize checks its speed-ups with, alike under
    `seq serve` and on the platform, where a hosted version's check runs it in its worker and each worker of the version
    applies what it kept (sequence_ai.engine.optimize.apply) to the call built the same way."""
    from sequence_base.contract import SeqFlags

    from seq.registry import registration

    call, sizes = _checked(instance)
    return call, sizes, _examples(instance, registration(type(instance)).bindings.get(SeqFlags.SAMPLE))


def _checked(instance: Any) -> tuple[Callable[[Any], Any], list[int] | None]:
    """checked_call's call and batch sizes, its sample episode left unread: seq serve's copy is handed the call
    (PolicyCopy's `checked`), and has read its observations through its adapter already."""
    from sequence_base.contract import SeqFlags

    from seq.registry import registration

    reg = registration(type(instance))
    spec = reg.spec
    infer = getattr(instance, reg.bindings[SeqFlags.INFER])
    declared = getattr(getattr(type(instance), reg.bindings[SeqFlags.INFER]), "__seq_concurrent__", None) or {}
    sizes = list(spec.concurrency.sizes) if spec.concurrency and spec.concurrency.sizes else None
    parameters = inspect.signature(infer).parameters
    call = _call(infer, sizes, bool(declared.get("collate", True)), "seed" in parameters, "episode" in parameters)
    return call, sizes


def _call(infer: Callable, sizes: list[int] | None, collate: bool, seeded: bool,
          episodic: bool = False) -> Callable[[Any], Any]:
    """What serve() calls (sequence_ai.engine.serve): one act's observation in, its answer out; or, with batch sizes,
    the acts that run together - stacked into one batch the platform's way (collate), or as a list (collate=False) -
    their answers out one an act. A robot's act has no seed, as on the platform; a policy whose infer takes one is also
    given `seed=` when sequence_ai.engine.optimize checks its speed-ups, so its noise is the same from one run to the
    next. A policy whose infer takes `episode` is given none - None, or None for each act - since an act served here
    belongs to no episode the platform keeps.

"""
    extra = {"episode": None} if episodic else {}
    if sizes is None:
        if not seeded and not episodic:
            return infer
        if not seeded:
            def bare(observation: Any) -> Any:
                return infer(observation, **extra)

            return bare

        def one(observation: Any, seed: int | None = None) -> Any:
            return infer(observation, seed=seed, **extra)

        return one

    from seq import _stack

    def batch(observations: list, seed: list | None = None) -> list:
        n = len(observations)
        kwargs = {"seed": list(seed) if seed is not None else [None] * n} if seeded else {}
        if episodic:
            kwargs["episode"] = [None] * n
        if collate:
            return _stack.unstack(infer(_stack.stack(observations), **kwargs), n)
        return list(infer(list(observations), **kwargs))

    return batch


def _examples(instance: Any, sample: str | None) -> list:
    """The observations of the class's sample episode (@seq.sample), in its order: the first is what the server warms
    on before it says it is ready, and all of them what its speed-ups are checked on. None for a class without one."""
    if not sample:
        return []
    return [call[1] for call in getattr(instance, sample)() or []
            if isinstance(call, (list, tuple)) and len(call) >= 2 and call[0] == "observe"]


def serve(folder: str | os.PathLike, name: str | None = None, *, host: str | None = None, port: int = 8000,
          weights: list[str] | None = None, token: str | None = None, api_key: str | None = None,
          base_url: str | None = None, cuda_graphs: bool | None = None, whole_graph: bool | None = None,
          torch_compile: bool = False, fused_kernels: bool = False, tensorrt: bool = False,
          precision: str | None = None, tolerance: Any = None, cfg_parallel: bool = False,
          pipeline_parallel: bool = False) -> int:
    """`seq serve`: build the folder's policy and serve it until stopped (Ctrl-C), then run its @seq.shutdown. Before it
    says it is ready, the speed-ups that keep its answers the same are tried on its sample episode's observations and
    kept where they are faster (sequence_ai.engine.optimize); `cuda_graphs`, `whole_graph` False leave one untried.
    torch_compile, fused_kernels, tensorrt, precision, cfg_parallel (two processes, torchrun --nproc-per-node 2) and
    pipeline_parallel (two or more) change the answers, and are tried only with `tolerance`."""
    from sequence_ai.engine.optimize import check_switches
    from sequence_ai.engine import ranks as _ranks
    from sequence_ai.engine.serve import answered_at, serve as engine_serve
    from sequence_ai.errors import Conflict

    check_switches(cuda_graphs=cuda_graphs, whole_graph=whole_graph, torch_compile=torch_compile,
                   fused_kernels=fused_kernels, tensorrt=tensorrt, precision=precision, tolerance=tolerance,
                   cfg_parallel=cfg_parallel, pipeline_parallel=pipeline_parallel)




    group = _ranks.from_env()
    if group is not None:
        _ranks.own_card()
    if group is None or group.leads:
        try:
            answered_at(host, port)
        except OSError as taken:
            raise Conflict(taken.strerror or str(taken)) from None
    served = build(folder, name, weights=weights, api_key=api_key, base_url=base_url)
    plays = served.plays or {}
    if plays and served.example is None:
        print(f"{served.name} declares how its answers play, and has no @seq.sample to time its batches on: its robots "
              "are not held or seated by their time")
        plays = {}
    print(f"serving {served.name} on port {port}"
          + (f", in batches of {served.batch}" if served.batch else "")
          + (f", planning each episode every {served.copy.plan_every_s:g} s"
             if served.copy is not None and served.copy.plan_every_s else "")
          + (f", each robot held and seated by its time at {plays['hz']:g} Hz" if plays else "")
          + f": a robot connects with sequence_ai.connect(\"http://<this machine>:{port}\")")
    try:
        engine_serve(served.call, host=host, port=port, batch=served.batch, example=served.example, token=token,
                     examples=served.examples, cuda_graphs=cuda_graphs, whole_graph=whole_graph,
                     torch_compile=torch_compile, fused_kernels=fused_kernels, tensorrt=tensorrt,
                     precision=precision, tolerance=tolerance, cfg_parallel=cfg_parallel,
                     pipeline_parallel=pipeline_parallel, copy=served.copy, **plays)
    except OSError as failed:
        if failed.errno != errno.EADDRINUSE:
            raise
        raise Conflict(failed.strerror or str(failed)) from None
    finally:
        served.shutdown()
    return 0
