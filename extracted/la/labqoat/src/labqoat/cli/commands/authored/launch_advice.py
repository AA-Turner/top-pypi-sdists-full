"""Hints, printed before a launch, about declarations that commonly cost a failed or wasteful run."""

import inspect
import re
from pathlib import Path
from types import ModuleType
from typing import ClassVar

import click

from labqoat.compute.function import Function
from labqoat.compute.images.app_source import AppSource


class LaunchAdvice:
    """Read each remote function's own source; advise, never block, and never guess beyond what the text shows."""

    hub = re.compile(r"\b(load_dataset|from_pretrained|hf_hub_download|snapshot_download|HfApi)\s*\(")
    children = re.compile(r"\.(spawn|spawn_async|spawn_map|spawn_map_async|map|map_async|starmap|starmap_async)\(")
    gathered = re.compile(r"\bgather\(")
    token: ClassVar[str] = "HF_TOKEN"

    @classmethod
    def hints(cls, module: ModuleType) -> list[str]:
        """One line per finding, in declaration order."""
        functions = [value for value in vars(module).values() if isinstance(value, Function)]
        remote = {function.local.__name__ for function in functions}
        found = [hint for function in functions for hint in [*cls.inspect(function, remote), *cls.placement(function)]]
        return [*found, *cls.left_out(module)]

    @staticmethod
    def placement(function: Function[..., object]) -> list[str]:
        """GPU requests that trade the user's money or the run's patience for being placed sooner."""
        name = function.local.__name__
        hints = []
        if function.gpu == "any":
            hints.append(
                f'`{name}` asks for gpu="any": it takes whichever card with enough memory frees first, H100s '
                "included. Name the model the work needs unless any card is fine with the user."
            )
        gpu = function.gpu is not None or bool(function.gpu_count)
        if gpu and function.queue_timeout is not None and function.queue_timeout < 3600:
            hints.append(
                f"`{name}` gives up after {function.queue_timeout} s without a GPU; waits of hours are normal. Leave "
                "queue_timeout unset (24 h for GPU work) unless the user set a deadline."
            )
        return hints

    @staticmethod
    def left_out(module: ModuleType) -> list[str]:
        """Name the files beside the code that are too large to travel with it."""
        source = getattr(module, "__file__", None)
        if source is None:
            return []
        try:
            names = AppSource.data(AppSource.root(Path(source), module.__name__))[1]
        except ValueError:
            return []
        if not names:
            return []
        shown = ", ".join(names[:3]) + (f" and {len(names) - 3} more" if len(names) > 3 else "")
        return [
            f"{len(names)} file(s) beside the code stay on this machine: {shown} (over 1 MiB each, or past 16 MiB "
            "or 1,000 files in all). Add what the run reads with Image.add_local_dir, or keep it in a volume or dataset."
        ]

    @classmethod
    def inspect(cls, function: Function[..., object], remote: set[str]) -> list[str]:
        """Check one function: Hugging Face access, recoverable fan-out and tolerant gathering."""
        name = function.local.__name__
        try:
            source = inspect.getsource(function.local)
        except (OSError, TypeError):
            return []
        hints = []
        if cls.hub.search(source) and cls.token not in {secret.name for secret in function.secrets}:
            hints.append(
                f"`{name}` downloads from Hugging Face without the {cls.token} secret; anonymous downloads are rate "
                f'limited (HTTP 429). Declare secrets=[Secret.from_name("{cls.token}")] on it.'
            )
        named = any(re.search(rf"\b{re.escape(child)}\.", source) for child in remote)
        fans_out = named and cls.children.search(source) is not None
        if fans_out and not function.workflow_replay:
            hints.append(
                f"`{name}` starts child runs but is not declared with `.with_workflow_replay()`, so "
                "`lab run recover --failed-descendants` cannot reuse the children that finished."
            )
        if fans_out and cls.gathered.search(source) and "return_exceptions=True" not in source:
            hints.append(
                f"`{name}` gathers child results without `return_exceptions=True`; the first failed child ends the "
                "parent and cancels its healthy siblings."
            )
        return hints

    @classmethod
    def announce(cls, module: ModuleType | None) -> None:
        """Write hints to stderr so machine-readable stdout stays a single receipt."""
        for hint in cls.hints(module) if module is not None else []:
            click.echo(f"hint {hint}", err=True)
