"""
`seq benchmark cancel <name>`: the benchmark's registration in flight stops now.

Its check's machine, if its check began, ends at once, and what its machines ran until then is billed, as GCE and AWS
bill a machine stopped; the
version it was registering is marked failed (canceled), and an eval runs the version before it, when one passed its
check. Before it, the only stop
was `seq benchmark rm`, which deleted the benchmark - a version that passed its check too.

What it says is how far the registration got (the platform's `stage` and `check_started`): c-toy-cpu, canceled in its
image step, was told "its check's machine is ended and none of its check is billed" of a check that never began.

"""
from __future__ import annotations

from typing import Callable


def cancel(name: str, *, base_url: str | None = None, echo: Callable[[str], None] = print) -> dict:
    """Stop `name`'s registration in flight, printed."""
    from seq._eval_gateway import EvalGatewayClient

    out = EvalGatewayClient(base_url=base_url).cancel_benchmark(name)
    what = f"the registration of {out.get('name') or name} v{out.get('version')}"
    stage, started = out.get("stage"), out.get("check_started")
    if started:
        echo(f"canceled {what} in its check: its check's machine is ended, and what ran until now is billed")
    else:
        where = (", while its check waited for its card" if stage == "card" else
                 f", in its {stage} step" if stage else "")
        echo(f"canceled {what} before its check started{where}; what ran until now is billed")
    if out.get("runs") is not None:
        echo(f"  evals of {out.get('name') or name} run v{out['runs']}, the version before it")
    else:
        echo("  no version of it passed its check: register it again to run evals on it")
    return out
