"""the yes/no gates in front of irreversible steps: remove Probe or one agent, sign out, remove or switch an account, pending capture."""

from __future__ import annotations


def confirm_removal(agent_sources: tuple[str, ...] | list[str] | str = ("claude_code",), *, offline: bool = False):
    """The uninstall gate (`probe uninstall`). Returns None, tui.BACK, or a bool.

    A bare `typer.confirm` here was the one prompt in the wizard that printed
    at column 0 -- and it guarded the single destructive action, which is the
    worst place to look like a different program.

    The copy says what the uninstall does and nothing more: it used to claim
    every token was revoked while the daemon key was only wiped off the disk.
    A key another computer also holds is disconnected from this one, not
    revoked; offline, nothing is revoked and the dashboard is where it is done.
    """
    from probe.cli.wizard import terminal as tui

    agents = f"the {agent_label(agent_sources)} plugins, skills and rules" if agent_sources else "its plugins"
    keys = (
        "Nothing can be revoked offline: revoke this computer's keys in the dashboard afterwards."
        if offline else
        "This computer is retired from your account and its keys are revoked (the API and MCP tokens, the "
        "Probe daemon's key, every capture key); a key another computer also uses is only disconnected "
        "from this one."
    )
    return tui.review(
        "Remove Probe Research from this computer",
        tui.wrap(
            f"Stops every Probe process and removes the Probe CLI, {agents}, the status line, and "
            f"Probe's files for you on this computer. {keys} Your projects, .probe.config files and "
            "data already sent to your team stay."
        ),
        [("Keep Probe Research", False), ("Remove Probe Research", True)],
    )


def confirm_pending_capture(sources: tuple[str, ...] | list[str] | str):
    """Update's question for capture a sign-in left waiting (`AWAITING_CONFIRMATION`).
    Returns None, tui.BACK, or a bool.

    Turning it on is the first choice: the browser approval that left the lock
    is where session capture was granted and disclosed in full, and the
    person is in this wizard to set Probe up here. Saying no changes nothing.
    """
    from probe.cli.wizard import terminal as tui

    return tui.review(
        "Turn on session capture?",
        tui.wrap(
            f"You signed in on this device, but Install never confirmed session "
            f"capture, so {agent_label(sources)} sessions are not being sent to "
            "your team."
        ),
        [("Turn on session capture", True), ("Not now", False)],
    )


def confirm_agent_removal(agent_sources: tuple[str, ...] | list[str] | str):
    """`probe wizard --action uninstall --agent A`: Probe out of the named
    agents only. Keep first, like `confirm_removal`. None, tui.BACK or a bool."""
    from probe.cli.wizard import terminal as tui

    return tui.review(
        f"Remove Probe Research from {agent_label(agent_sources)}",
        tui.wrap(
            f"Removes Probe's plugins, hooks, skills and rules from {agent_label(agent_sources)} and stops its "
            "capture. The Probe CLI, this computer's sign-in and every other coding agent stay; "
            "`probe uninstall` removes all of Probe."
        ),
        [("Keep Probe Research", False), (f"Remove it from {agent_label(agent_sources)}", True)],
    )


def confirm_sign_out(account: "str | None" = None):
    """The sign-out gate (Richard 2026-09-29: "add a confirmation page to make
    sure a user doesnt accidentally sign themselves out"). Returns None,
    tui.BACK, or a bool. Staying signed in is listed first, so the cursor starts
    on the choice that costs nothing -- `confirm_removal`'s rule."""
    from probe.cli.wizard import terminal as tui

    who = f"Signed in as {account}. " if account else ""
    return tui.review(
        "Sign out of Probe on this device",
        tui.wrap(
            f"{who}Stops capture and imports, clears import history, and revokes this "
            "device's tokens. Data already sent to your team stays."
        ),
        [("Stay signed in", False), ("Sign out", True)],
    )


def run_confirm_account_switch(previous: str):
    """The gate in front of an install code on an already-signed-in device.
    Returns None (Ctrl-C), tui.BACK, or a bool.

    BEFORE THE EXCHANGE, and that ordering is the whole design. A website code
    carries its own identity: redeeming it binds this device to whoever
    generated it, and the exchange DETACHES the credentials that were bound
    here (see `revoke_replaced_token`, and the rotation block in the backend's
    device exchange). By the time we could name the new account, the old one is
    already gone from this device and there is nothing left to roll back to --
    so the only honest place to ask is here, where the only account we can name
    is the one being replaced.

    Defaulting to False for the same reason `confirm_removal` does: the
    keystroke that costs something is the one that must be typed, not the one
    that is already under the cursor.
    """
    import questionary

    from probe.cli.wizard import terminal as tui

    message = tui.framed(
        "This device is already signed in.",
        [
            *tui.wrap(f"Signed in as {previous}."),
            "",
            *tui.wrap("The website code signs in as whoever made it."),
            *tui.wrap(
                "Continuing replaces the account saved here and releases this "
                "device's credentials. Data already sent to your team stays."
            ),
        ],
        "Continue with the account from the website code?",
    )
    choices = [
        questionary.Choice("Keep current account", value=False),
        questionary.Separator(" "),
        questionary.Choice("Continue with website code", value=True),
    ]
    return tui.ask(
        tui.select(
            message,
            choices=choices,
            default=False,
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
            instruction=" ",
        ),
        height=tui.content_height(message, choices),
    )


def confirm_remove_account(name: str):
    """The gate before a saved account is deleted: keeping it is listed first,
    so the cursor starts on the choice that costs nothing. Returns None,
    tui.BACK, or a bool."""
    from probe.cli.wizard import terminal as tui

    return tui.review(
        f"Remove the account saved as “{name}”",
        tui.wrap(
            "Deletes it from this device. Your current account is not touched."
        ),
        [("Keep it", False), ("Remove it", True)],
    )
from probe.cli.wizard.agents import agent_label  # noqa: E402 -- pieces need each other; the front door loads this one first
