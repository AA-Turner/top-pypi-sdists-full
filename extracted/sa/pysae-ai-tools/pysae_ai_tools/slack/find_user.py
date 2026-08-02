"""Find a Slack user by name or email.

Usage:
    pysae-ai-tools slack find-user "Rémi Alvergnat"
    pysae-ai-tools slack find-user remi.alvergnat@pysae.com

Matching rules (case-insensitive):
1. If the query looks like an email → ``users.lookupByEmail`` (fast, exact).
2. Otherwise → ``users.list``, paginated, matching the query as a substring
   of ``real_name``, ``display_name``, ``name`` (handle), or ``email``.

The first match wins — for multiple hits, refine the query.

Output (JSON, one line):
    {"found": true, "id": "U123", "name": "handle", "real_name": "Jane Doe", "email": "jane@…"}
    {"found": false}
"""

import json
from typing import Annotated

import typer

from .client import SlackApiError, slack_get, slack_paginate
from .common import get_slack_token

PAGE_LIMIT = 200


def _format(user: dict[str, object]) -> dict[str, object]:
    profile = user.get("profile") if isinstance(user.get("profile"), dict) else {}
    assert isinstance(profile, dict)
    return {
        "found": True,
        "id": user.get("id"),
        "name": user.get("name"),
        "real_name": profile.get("real_name") or user.get("real_name"),
        "email": profile.get("email"),
    }


def _matches(user: dict[str, object], needle: str) -> bool:
    needle = needle.lower()
    profile = user.get("profile") if isinstance(user.get("profile"), dict) else {}
    assert isinstance(profile, dict)
    haystacks = [
        str(user.get("name", "")),
        str(user.get("real_name", "")),
        str(profile.get("real_name", "")),
        str(profile.get("display_name", "")),
        str(profile.get("email", "")),
    ]
    return any(needle in h.lower() for h in haystacks if h)


cli = typer.Typer()


@cli.command()
def main(
    query: Annotated[str, typer.Argument(help="Name, handle, or email to match.")],
) -> None:
    """Find a Slack user by name or email."""
    token = get_slack_token()
    if not token:
        print(json.dumps({"found": False, "error": "no Slack token available"}))
        raise typer.Exit(code=1)

    # 1. Email fast-path.
    if "@" in query and "." in query.split("@", 1)[1]:
        try:
            data = slack_get(token, "users.lookupByEmail", {"email": query})
        except SlackApiError:
            data = None
        if data is not None:
            user = data.get("user")
            if isinstance(user, dict):
                print(json.dumps(_format(user)))
                return

    # 2. Paginated users.list fallback.
    try:
        for user in slack_paginate(token, "users.list", {"limit": str(PAGE_LIMIT)}, items_key="members"):
            if _matches(user, query):
                print(json.dumps(_format(user)))
                return
    except SlackApiError as e:
        print(json.dumps({"found": False, "error": str(e)}))
        raise typer.Exit(code=1) from None

    print(json.dumps({"found": False}))
    raise typer.Exit(code=1)


if __name__ == "__main__":
    cli()
