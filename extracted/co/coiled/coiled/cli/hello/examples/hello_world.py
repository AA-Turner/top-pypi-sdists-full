from __future__ import annotations

import os
import subprocess
import time

import dask.config
from dask.utils import format_time
from rich import box
from rich.console import Group
from rich.markdown import Markdown
from rich.prompt import Prompt

import coiled

from ..utils import PRIMARY_COLOR, Panel, console, log_interactions

NTASKS = 10

# Ensure subprocesses use utf-8 encoding.
# Some Windows systems raise encoding errors without this.
os.environ["PYTHONIOENCODING"] = "utf-8"


def hello_world(first_time=False):
    panel_kwargs = {}
    if first_time:
        panel_kwargs = {
            "title": "[white]Step 2: Hello world[/white]",
            "border_style": PRIMARY_COLOR,
        }
    console.print(
        Panel(
            Markdown(
                f"""
{"## Example: Hello world" if not first_time else ""}

Coiled makes it easy to run your code on the cloud.  

This could be _any_ code, but let's start simple by running  
`echo 'Hello world'` on {NTASKS} cloud VMs.

We'll launch all {NTASKS} jobs from this machine with this command:

```bash
$ coiled batch run \\             # Submit 10 'Hello world' jobs
    --container ubuntu:latest \\
    --n-tasks {NTASKS} \\
    echo Hello world
```

I'll run this for you here, but you can do this yourself any time.
""".strip()  # noqa: W291
            ),
            **panel_kwargs,
        ),
    )

    try:
        choice = Prompt.ask(
            "Ready to launch some cloud instances?",
            choices=["y", "n"],
            default="y",
            show_choices=True,
            show_default=True,
        )
        coiled.add_interaction("cli-hello:run-hello-world", success=True, choice=choice)
    except KeyboardInterrupt:
        coiled.add_interaction("cli-hello:KeyboardInterrupt", success=False)
        return False

    if choice == "y":
        with log_interactions("example-hello-world") as interaction_info:
            info = coiled.batch.run(
                ["echo", "Hello world"], container="ubuntu:latest", ntasks=NTASKS, tag={"coiled-hello": "hello-world"}
            )
            interaction_info["cluster_id"] = info["cluster_id"]
            link = f"{dask.config.get('coiled.server')}/clusters/{info['cluster_id']}"
            console.print(
                Panel(
                    f"""
You've just launched your first jobs with Coiled :rocket:
We're spinning up cloud VMs right now.

Go check them out at [link={link}]{link}[/link].
You'll see logs, the state of each VM, and hardware metrics.

Be sure to come back here after exploring the Coiled UI.
This job takes less than a minute to run.
""",
                    title="[white]First cloud jobs[/white]",
                    border_style="green",
                )
            )
            output = None
            with console.status("Running jobs..."):
                t_start = time.monotonic()
                subprocess.run(["coiled", "batch", "wait", str(info["cluster_id"])], check=True, capture_output=True)
                t_end = time.monotonic()
                # Sometimes it takes a while for all logs to show up.
                # Let's try a few times if they're not there initially.
                count = 0
                while count <= 3:
                    logs = subprocess.run(
                        ["coiled", "logs", "--no-color", "--filter", "Hello world", str(info["cluster_id"])],
                        check=True,
                        capture_output=True,
                    )
                    if b"Hello" in logs.stdout:
                        lines = logs.stdout.decode().strip().split("\n")
                        if len(lines) - 2 == NTASKS:
                            # Accounting for two header lines in the `coiled logs` output
                            output = "\n".join(lines[2:])
                            break
                    # Either no, or not all, "Hello world" logs have arrived yet, so try again
                    time.sleep(0.5)
                    count += 1
            if output:
                console.print(
                    Panel(
                        Group(
                            f"""Jobs are finished :white_check_mark:
It took {format_time(t_end - t_start)} to run on 10 cloud VMs.
""",
                            Markdown(f"""
We can see the results from this job by looking through VM logs with this command:

```bash
$ coiled logs --filter "Hello world"  # Grep through logs
```

which outputs

```terminal
{output}
```
"""),
                        ),
                        box=box.SIMPLE,
                    )
                )

        return True
    else:
        console.print("On to bigger examples then! :rocket:")
        return None
