from __future__ import annotations

import contextlib
import os
import pathlib
import subprocess
import sys
import time

import importlib_metadata
import rich
import rich.panel
from rich import box
from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.rule import Rule
from rich.syntax import Syntax

import coiled
from coiled.pypi_conda_map import PYPI_TO_CONDA
from coiled.utils import error_info_for_tracking

PRIMARY_COLOR = "rgb(0,95,255)"
console = Console(width=80)


class Panel(rich.panel.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "padding" not in kwargs:
            self.padding = (1, 2)


@contextlib.contextmanager
def log_interactions(action):
    success = True
    exception = None
    info = {}
    try:
        yield info
    except (Exception, KeyboardInterrupt) as e:
        # TODO: Better error when something goes wrong in example
        success = False
        exception = e
        raise e
    finally:
        coiled.add_interaction(
            f"cli-hello:{action}",
            success=success,
            **error_info_for_tracking(exception),
            **info,
        )


def live_panel_print(*renderables, delay=0.5, panel_kwargs=None):
    panel_kwargs = panel_kwargs or {}
    renderables = [r for r in renderables if r is not None]
    with Live(Panel(renderables[0], **panel_kwargs), console=console, auto_refresh=False) as live:
        for idx in range(len(renderables)):
            time.sleep(delay)
            live.update(Panel(Group(*renderables[: idx + 1]), **panel_kwargs), refresh=True)


def has_macos_system_python():
    system_python_mac = sys.platform == "darwin" and "Python3.framework" in sys.exec_prefix
    return system_python_mac


def missing_dependencies_message(dependencies):
    missing = []
    for dep in dependencies:
        try:
            importlib_metadata.distribution(dep)
        except ModuleNotFoundError:
            missing.append(dep)
    coiled.add_interaction("cli-hello:missing-deps", success=True, missing=missing)

    msg = ""
    if missing:
        if len(missing) == 1:
            missing_formatted = f"`{missing[0]}`"
        elif len(missing) == 2:
            missing_formatted = f"`{missing[0]}` and `{missing[1]}`"
        else:
            missing_formatted = ", ".join([f"`{p}`" for p in missing[:-1]])
            missing_formatted += f", and `{missing[-1]}`"

        plural = len(missing) > 1
        msg = Markdown(
            f"""
Your current software environment is missing the
{"libraries" if plural else "library"} {missing_formatted}
which {"are" if plural else "is"} needed for this example.
We'll install {"them" if plural else "it"} for you with `pip` before
running the example.  

<br>
"""  # noqa
        )
    return msg, missing


def ask_and_run_example(name, missing, dependencies, filename) -> bool | None:
    if missing:
        prompt = "Install packages and run example?"
    else:
        prompt = "Run example?"

    try:
        choice = Prompt.ask(
            prompt,
            choices=["y", "n"],
            default="y",
            show_choices=True,
        )
    except KeyboardInterrupt:
        coiled.add_interaction(action="cli-hello:KeyboardInterrupt", success=False)
        return False

    coiled.add_interaction("cli-hello:install-and-run", success=True, choice=choice)
    if choice == "y":
        if missing:
            with log_interactions("install-missing-deps"):
                with console.status(f"Installing {', '.join(missing)}"):
                    subprocess.run(
                        [sys.executable or "python", "-m", "pip", "install", *missing], capture_output=True, check=True
                    )
        # Run example
        with log_interactions(f"example-{name}") as info:
            clusters_before = set(i["id"] for i in coiled.list_clusters(max_pages=1, just_mine=True))
            fill = pathlib.Path(__file__).parent / "scripts" / "fill_ipython.py"
            subprocess.run(
                [sys.executable or "python", "-m", "IPython", "-i", fill, str(filename)],
                env={
                    **os.environ,
                    **{
                        "DASK_COILED__TAGS": f'{{"coiled-hello": "{name}"}}',
                        "DASK_DISTRIBUTED__SCHEDULER__IDLE_TIMEOUT": "5 minutes",
                        "DASK_COILED___INTERNAL__PACKAGE_SYNC_ONLY": f"{dependencies}",
                    },
                },
                check=True,
            )
            clusters_after = set(i["id"] for i in coiled.list_clusters(max_pages=1, just_mine=True))
            cluster_ids = clusters_after - clusters_before
            info["cluster_id"] = None
            if len(cluster_ids) == 1:
                info["cluster_id"] = next(iter(cluster_ids))
    else:
        return None

    return True


def render_example(name: str, dependencies, msg_start) -> bool | None:
    script_path = pathlib.Path(__file__).parent / "scripts" / f"{name.replace('-', '_')}.py"
    # Don't display IPython usage tip here (only when users are put into IPython)
    lines = pathlib.Path(script_path).read_text().split("\n")
    line_range = None
    for idx, line in enumerate(lines):
        if line.startswith("# Tip: "):
            line_range = (1, idx)
            break
    msg_code = Syntax.from_path(str(script_path), line_range=line_range)
    msg_ipython = """
Next we'll drop you into an IPython terminal to run this code yourself.
""".strip()

    msg_macos_system_python = macos_system_python_message()
    msg_missing, missing = missing_dependencies_message(dependencies)
    if msg_macos_system_python:
        msg_end = """
I recommend quitting this wizard (Ctrl-C) and running the commands above.
    """.strip()

        live_panel_print(msg_start, Rule(style="grey"), msg_code, Rule(style="grey"), msg_macos_system_python, msg_end)
        try:
            choice = Prompt.ask(
                "Proceed anyway?",
                choices=["y", "n"],
                default="n",
                show_choices=True,
            )
        except KeyboardInterrupt:
            coiled.add_interaction(action="cli-hello:KeyboardInterrupt", success=False)
            return False

        coiled.add_interaction("cli-hello:messy-software-continue", success=True, choice=choice)
        if choice == "y":
            if msg_missing:
                live_panel_print(msg_missing, msg_ipython, panel_kwargs={"box": box.SIMPLE})
            else:
                live_panel_print(msg_ipython)
            result = ask_and_run_example(name=name, missing=missing, dependencies=dependencies, filename=script_path)
            return result
        else:
            console.print("See you in a minute with that new software environment :wave:")
            return True
    else:
        live_panel_print(msg_start, Rule(style="grey"), msg_code, Rule(style="grey"), msg_missing, msg_ipython)
        result = ask_and_run_example(name=name, missing=missing, dependencies=dependencies, filename=script_path)

    return result


def get_conda_dependencies(deps):
    if "dask" in deps:
        # These are included with `dask` on conda-forge
        deps = [d for d in deps if d not in ("pandas", "bokeh", "pyarrow")]
    deps = [PYPI_TO_CONDA.get(p, p) if p not in ("dask", "matplotlib") else p for p in deps]
    return deps


def macos_system_python_message():
    msg = ""
    if has_macos_system_python():
        msg = Panel(
            Group(
                Markdown(
                    f"""
We're about to run a fun Python example on the cloud.  
Normally, Coiled copies your local software environment to
cloud machines automatically (no Docker!)
However this doesn't work well when using the macOS system Python.

We recommend creating a local environment that uses a different
Python installation. One easy option is to make a new environment
with conda:

```bash
curl -L -O \\
    "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
conda create -n coiled -c conda-forge -y coiled
conda activate coiled
coiled quickstart
```
""".strip()  # noqa
                ),
            ),
            title=f"[{PRIMARY_COLOR}]MacOS System Python[/{PRIMARY_COLOR}]",
        )

    return msg
