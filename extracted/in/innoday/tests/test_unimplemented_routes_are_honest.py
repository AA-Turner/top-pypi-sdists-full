"""An unbuilt endpoint must say so, not fake a result.

`container_execution.py` had this right from the start -- every route raises 501
and names the issue. Three other routers did not, and the difference matters more
than it sounds: a 501 tells a caller to stop building on this, while a fabricated
200 tells them it worked. Anything written against the second is wrong in a way
that surfaces much later, in someone else's code.

The worst offender was `GET /integrations/{service}/sync-status`, which reported
`last_sync_status: "success"` with `last_sync` stamped to the moment of the call.
A service that had never synced looked healthy, and looked *more* healthy the more
recently you asked.

This is a guard, not a wish: when one of these is genuinely implemented, it comes
off the list in the same commit that implements it.
"""

import re
from pathlib import Path

ROUTERS = Path(__file__).resolve().parents[1] / "src" / "routers"

UNIMPLEMENTED = {
    "container_execution.py": [
        "execute_container",
        "list_executions",
        "get_execution_status",
        "cancel_execution",
        "delete_execution",
        "get_execution_logs",
    ],
    "integrations.py": [
        "get_service_webhooks",
        "create_service_webhook",
        "delete_service_webhook",
        "get_sync_status",
        "update_service_config",
    ],
    "search.py": ["search_similar", "refresh_embeddings", "get_missing_embeddings"],
}


def test_every_unimplemented_route_raises_501_and_returns_nothing():
    """One test, every handler, all failures at once.

    Reported together rather than as 14 parametrized cases: these fail as a group
    when someone reintroduces the pattern, and fourteen near-identical red lines
    say less than one list.
    """
    problems = []
    for filename, handlers in UNIMPLEMENTED.items():
        text = (ROUTERS / filename).read_text()
        for name in handlers:
            m = re.search(
                rf"^(?:async )?def {name}\(.*?(?=^(?:@|class |def |async def )|\Z)",
                text,
                re.S | re.M,
            )
            if not m:
                problems.append(f"{filename}:{name} not found -- renamed?")
                continue
            source = m.group(0)
            body = source.split('"""')[-1] if '"""' in source else source
            if "501" not in source:
                problems.append(
                    f"{filename}:{name} does not raise 501. If it is now "
                    f"implemented, remove it from UNIMPLEMENTED in the same "
                    f"commit that implemented it."
                )
            # A `return` in an unbuilt handler is the exact failure this file
            # exists for: some path still hands the caller a shape.
            elif re.search(r"^\s+return\b", body, re.M):
                problems.append(
                    f"{filename}:{name} raises 501 but still returns on some path."
                )
    assert not problems, "\n  " + "\n  ".join(problems)


def test_the_list_has_not_silently_grown():
    """Adding a stub should mean editing this number and saying why."""
    total = sum(len(v) for v in UNIMPLEMENTED.values())
    assert total == 14, f"{total} unimplemented endpoints, expected 14."
