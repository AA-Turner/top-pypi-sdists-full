"""
`seq serve [folder]`: a @seq.policy served from this machine's GPU - the class its folder declares, built as the platform
builds it, with its template's own weights read with your key - to robots that connect to this machine with
`sequence_ai.connect("http://<this machine>:8000")`.

In one sentence: the folder's class, found and imported as `seq deploy` finds it (seq.loading) → each of its weights
parts a folder here: an official template's fetched by weights_get, an hf:// repo downloaded by huggingface_hub, or the
folder `--weights` names → the class built by its init= as the platform builds it (sequence_base.construct.build) → its
@seq.infer served by sequence_ai.serve: a @seq.concurrent policy's acts stacked into one batch in its listed sizes and
its answer split back as the platform does it (_stack), one robot's act a call otherwise → @seq.shutdown when it stops.

WHY the platform's own building and stacking: one template runs on the platform or on a GPU of your own, and only
where the GPU is changes, so its code answers here as it does there.
"""
from __future__ import annotations

import inspect
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from seq.errors import PolicyDefinitionError


@dataclass
class Served:
    """What `seq serve` hands sequence_ai.serve: the call, its batch sizes (None: one act a call), an observation to warm
    it with, and what to run when it stops."""
    name: str
    call: Callable[[Any], Any]
    batch: list[int] | None
    example: Any
    shutdown: Callable[[], Any]


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
    """The folder's @seq.policy, built here as the platform builds it, and the call that serves it."""
    from sequence_base.contract import SeqFlags

    from seq.loading import load_folder
    from seq.registry import registration

    folder = Path(folder)
    _, cls = load_folder(folder, name)
    reg = registration(cls)
    spec = reg.spec
    if spec.planner is not None:
        raise PolicyDefinitionError(f"{spec.name} plans with a model of the platform: serve it on the platform")
    if SeqFlags.OBSERVE in reg.bindings or SeqFlags.ON_EPISODE in reg.bindings:
        raise PolicyDefinitionError(f"{spec.name} keeps each episode's state (@seq.observe or @seq.on_episode): serve "
                                    "it on the platform, which hands it each robot's episode")
    dirs = weights_dirs(spec, parse_weights(weights), api_key=api_key, base_url=base_url, say=say)
    if reg.constructor is None:
        instance = cls()
    else:
        from sequence_base.construct import build as construct

        instance = construct(cls, reg.constructor, base_dir=str(folder.resolve()), weights=dirs)
    infer =getattr(instance, reg.bindings[SeqFlags.INFER])
    declared = getattr(getattr(type(instance), reg.bindings[SeqFlags.INFER]), "__seq_concurrent__", None) or {}
    sizes = list(spec.concurrency.sizes) if spec.concurrency and spec.concurrency.sizes else None
    seeded = "seed" in inspect.signature(infer).parameters
    example = _example(instance, reg.bindings.get(SeqFlags.SAMPLE))
    shutdown = getattr(instance, reg.bindings[SeqFlags.SHUTDOWN]) if SeqFlags.SHUTDOWN in reg.bindings else _nothing
    return Served(spec.name, _call(infer, sizes, bool(declared.get("collate", True)), seeded), sizes, example,
                  shutdown)


def _call(infer: Callable, sizes: list[int] | None, collate: bool, seeded: bool) -> Callable[[Any], Any]:
    """What sequence_ai.serve calls: one act's observation in, its answer out; or, with batch sizes, the acts that run
    together - stacked into one batch the platform's way (collate), or as a list (collate=False) - their answers out
    one an act."""
    if sizes is None:
        return (lambda observation: infer(observation, seed=None)) if seeded else infer

    from seq import _stack

    def batch(observations: list) -> list:
        n = len(observations)
        kwargs = {"seed": [None] * n} if seeded else {}
        if collate:
            return _stack.unstack(infer(_stack.stack(observations), **kwargs), n)
        return list(infer(list(observations), **kwargs))

    return batch


def _example(instance: Any, sample: str | None) -> Any:
    """The first observation of the class's sample episode (@seq.sample): what the server warms on before it says it is
    ready. None for a class without one."""
    if not sample:
        return None
    for call in getattr(instance, sample)() or []:
        if isinstance(call, (list, tuple)) and len(call) >= 2 and call[0] == "observe":
            return call[1]
    return None


def _nothing() -> None:
    return None


def serve(folder: str | os.PathLike, name: str | None = None, *, host: str | None = None, port: int = 8000,
          weights: list[str] | None = None, token: str | None = None, api_key: str | None = None,
          base_url: str | None = None) -> int:
    """`seq serve`: build the folder's policy and serve it until stopped (Ctrl-C), then run its @seq.shutdown."""
    import sequence_ai

    served = build(folder, name, weights=weights, api_key=api_key, base_url=base_url)
    print(f"serving {served.name} on port {port}"
          + (f", in batches of {served.batch}" if served.batch else "")
          + f": a robot connects with sequence_ai.connect(\"http://<this machine>:{port}\")")
    try:
        sequence_ai.serve(served.call, host=host, port=port, batch=served.batch, example=served.example, token=token)
    finally:
        served.shutdown()
    return 0
