"""the account screen: saved accounts, who is signed in, switch to or remove a saved one."""

from __future__ import annotations
from dataclasses import dataclass
from probe.foundation.compat.compat import StrEnum
from probe.cli.wizard.state.state import (
    Capabilities,
    TokenSource)
from probe.cli.wizard.state.capture_credentials import capture_token_sources


# -- accounts ---------------------------------------------------------------
#
# The credentials on this device belong to ONE account, and until now the wizard
# could only ever mint them (Install) or destroy the whole installation
# (Uninstall). Anyone who signed in with the wrong account, joined a second
# team, or handed the laptop on had to be told to leave the wizard and run
# `probe login` / `probe logout` -- two commands the wizard names exactly once,
# in a message printed after removing a plugin. So the wizard managed everything
# about this device except whose data it writes to.
#
# What makes this a screen of its own rather than a fifth checkbox: the
# capability menu is about what Probe DOES here, and every row of it is the same
# answer under a different account. Switching who you are is not another
# capability, it is the thing all of them hang off.


class AccountAction(StrEnum):
    """A row on the account screen. Not a `Capability` -- see the note above."""

    SIGN_IN = "sign_in"
    SWITCH = "switch"
    #: Forget ANOTHER saved account; the active one leaves by SIGN_OUT (R4).
    REMOVE = "remove"
    SIGN_OUT = "sign_out"
    BACK = "back"


#: Row copy for the account screen. Module-level, like MENU_COPY and
#: ACTION_COPY, so the narrow-terminal guard can MEASURE it -- a detail wider
#: than the block wraps mid-word and undoes the separation between rows.
ACCOUNT_COPY: dict[AccountAction, tuple[str, str]] = {
    AccountAction.SIGN_IN: (
        "Sign in",
        "Approve this device in the browser; the credentials are saved here.",
    ),
    AccountAction.SWITCH: (
        "Switch to an account saved here",
        "Use an account saved here. No browser.",
    ),
    AccountAction.REMOVE: (
        "Remove a saved account",
        "Delete another account saved here.",
    ),
    AccountAction.SIGN_OUT: (
        "Sign out",
        "Revoke this device's token and clear it.",
    ),
    AccountAction.BACK: (
        "Back",
        "Return to the main menu. Nothing changes.",
    ),
}

#: What the sign-in row says on a device that already holds a credential. Same
#: action, different sentence: "Sign in" there reads as a no-op, which is how
#: someone stuck on the wrong account concludes the wizard cannot help them.
SIGN_IN_AGAIN_TITLE = "Sign in as a different account"


@dataclass(frozen=True)
class SavedAccount:
    """One named context in the CLI config, as the account screen shows it."""

    name: str
    base_url: str | None
    has_token: bool
    active: bool

    def describe(self) -> str:
        """The endpoint, and whether this one can actually authenticate."""
        where = self.base_url or "no endpoint saved"
        return where if self.has_token else f"{where} — no credential saved"


def saved_accounts() -> list[SavedAccount]:
    """Every account saved on this device. Read-only and fail-soft.

    `load_file` already degrades an unreadable config to `{}` for readers, which
    is the right answer here: a menu must render something, and "no saved
    accounts" is recoverable by signing in. (WRITERS take the strict path -- see
    config.load_file -- because for them the same shrug would overwrite the
    file.)
    """
    from probe.sdk.settings.settings import DEFAULT_CONTEXT, load_file

    data = load_file()
    contexts = data.get("contexts")
    if not isinstance(contexts, dict):
        return []
    active = data.get("current_context") or DEFAULT_CONTEXT
    return [
        SavedAccount(
            name=name,
            base_url=(context.get("base_url") if isinstance(context, dict) else None),
            has_token=bool(isinstance(context, dict) and context.get("token")),
            active=name == active,
        )
        for name, context in sorted(contexts.items())
    ]


def account_email(base_url: str | None = None) -> str | None:
    """Who the resolved credential belongs to, or None.

    One network call, and failure is not an error: after a sign-in the answer is
    nice to have, never load-bearing, and an offline laptop must still be able
    to finish the flow.
    """
    from probe.sdk.client.client import Client
    from probe.foundation.request_identity.surface import Surface
    from probe.sdk.settings.settings import resolve

    settings = resolve(base_url=base_url)
    if not settings.token:
        return None
    try:
        with Client(
            settings=settings, async_writes=False, surface=Surface.CLI.value
        ) as client:
            return str(client.me().get("email") or "") or None
    except Exception:  # noqa: BLE001 - an unreachable endpoint is not an identity
        return None


def describe_account(caps: Capabilities, *, saved: list[SavedAccount] | None = None) -> list[str]:
    """The account state, for the header above the account screen."""
    saved = saved_accounts() if saved is None else saved
    active = next((account for account in saved if account.active), None)
    # THREE states, not two. `logged_in_as` is an email the API confirmed, so it
    # is empty both for a device with no credential AND for one whose endpoint
    # could not be reached -- and telling an offline researcher "not signed in"
    # invites them to re-approve a device that was never signed out.
    if caps.logged_in_as:
        who = caps.logged_in_as
    elif active is not None and active.has_token:
        who = "a saved credential — could not reach the endpoint to confirm whose"
    else:
        who = "not signed in"
    lines = [
        f"  {'Signed in as':<28} {who}",
        f"  {'Endpoint':<28} {caps.base_url or 'unknown'}",
    ]
    if active is not None:
        others = len(saved) - 1
        suffix = f"  (+{others} other saved here)" if others > 0 else ""
        lines.append(f"  {'Saved account':<28} {active.name}{suffix}")
    return lines


def can_sign_out(caps: Capabilities, saved: list[SavedAccount]) -> bool:
    """Whether there is anything here to sign out OF.

    Deliberately not just `caps.logged_in_as`: that is a verified email, so it
    is None on a laptop with no network -- and offering no way out of an account
    because the machine is offline is exactly when someone needs one.
    """
    active = next((account for account in saved if account.active), None)
    return bool(caps.logged_in_as) or bool(active and active.has_token)


def run_account_menu(caps: Capabilities, *, saved: list[SavedAccount] | None = None):
    """The account screen. Returns None (quit), tui.BACK, or an AccountAction.

    Retained for `--action account`. Account changes start by signing out;
    opening the wizard again performs a fresh sign-in before the main menu.
    """
    import questionary

    from probe.cli.wizard import terminal as tui

    saved = saved_accounts() if saved is None else saved
    body = tui.body_indent()
    choices: list = [questionary.Separator(" ")]

    def row(action: AccountAction, *, title: str | None = None) -> None:
        if len(choices) > 1:
            choices.append(questionary.Separator(" "))
        default_title, detail = ACCOUNT_COPY[action]
        choices.append(
            questionary.Choice(title=f"{title or default_title}\n{body}  {detail}", value=action)
        )

    # Switching and removing act on the OTHER saved accounts, so neither row
    # shows on a device that holds only the active one.
    if any(not account.active for account in saved):
        row(AccountAction.SWITCH)
        row(AccountAction.REMOVE)
    if can_sign_out(caps, saved):
        row(AccountAction.SIGN_OUT)
    row(AccountAction.BACK)

    message = tui.framed(
        "This device's account:", describe_account(caps, saved=saved), "What do you want to do?"
    )
    return tui.ask(
        tui.select(
            message,
            choices=choices,
            instruction="(arrow keys, enter to choose)",
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        ),
        height=tui.content_height(message, choices),
    )


def run_switch_menu(saved: list[SavedAccount], *, removing: bool = False):
    """Pick one of the saved accounts that is NOT active: to make it active, or
    (`removing`) to delete it. Returns None, tui.BACK, or a name."""
    import questionary

    from probe.cli.wizard import terminal as tui

    body = tui.body_indent()
    choices: list = [questionary.Separator(" ")]
    for index, account in enumerate([a for a in saved if not a.active]):
        if index:
            choices.append(questionary.Separator(" "))
        choices.append(
            questionary.Choice(
                title=f"{account.name}\n{body}  {account.describe()}", value=account.name
            )
        )
    choices.append(questionary.Separator(" "))
    choices.append(questionary.Choice(title="Back", value=tui.BACK))

    message = tui.framed(
        "Accounts already saved on this device.",
        tui.wrap(
            "Deletes it from this device. Its token stays valid until you revoke it "
            "in the dashboard."
            if removing
            else "Switching is local. Nothing is sent."
        ),
        "Which one should be removed?" if removing else "Which one should this device use?",
    )
    return tui.ask(
        tui.select(
            message,
            choices=choices,
            instruction="(arrow keys, enter to choose)",
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        ),
        height=tui.content_height(message, choices),
    )


def remove_account(name: str) -> list[str]:
    """Delete a saved account that is NOT the active one (`probe context delete`
    before it was removed). The active one leaves by Sign out, which also
    revokes its token and stops capture."""
    from probe.sdk.settings.settings import delete_context

    if next((a for a in saved_accounts() if a.name == name and not a.active), None) is None:
        return [f"No other account is saved as “{name}”; nothing was removed."]
    delete_context(name)
    return [f"Removed the account saved as “{name}”."]


def switch_account(
    name: str, sources: tuple[str, ...] | list[str] | str = ("claude_code",)
) -> list[str]:
    """Make one of the accounts already saved here the active one.

    Purely local: nothing is minted, revoked, or sent. That is what makes it
    worth having beside sign-in -- someone who works across two teams should not
    need a browser round trip to move between credentials this machine already
    holds.
    """
    from probe.sdk.settings.settings import DEFAULT_BASE_URL, load_context, resolve, use_context

    use_context(name)
    stored = load_context(name)
    endpoint = str(stored.get("base_url") or resolve().base_url)
    if not stored.get("token"):
        lines = [
            f"Now using the account saved as “{name}” ({endpoint}).",
            f"It holds no credential yet — `probe wizard --action login --context {name}` signs in to it.",
        ]
    else:
        # Who it is, in one line: the server only when it is not Probe's own.
        email = account_email(endpoint)
        who = [part for part in (email, endpoint if endpoint.rstrip("/") != DEFAULT_BASE_URL else None) if part]
        lines = [f"Now using “{name}”" + (f" ({' at '.join(who)})." if who else ".")]

    # `ingest_token` lives INSIDE the context, so it follows the switch. A
    # paired device token does not: it is one file per agent, minted by whoever
    # approved it, and it keeps uploading there. Switching accounts silently
    # would send this device's transcripts to the team just switched away from.
    # One line naming them all, not the same sentence per agent.
    normalized = (sources,) if isinstance(sources, str) else tuple(sources)
    paired = [source for source in normalized if TokenSource.PAIRED_FILE in capture_token_sources(source)]
    if paired:
        lines.append(
            f"! Session capture for {spoken_list([agent_label(source) for source in paired])} still "
            "uploads to the account that paired it. `probe wizard --action login` re-pairs it to this one."
        )
    return lines
from probe.cli.wizard.agents import agent_label, spoken_list  # noqa: E402 -- pieces need each other; the front door loads this one first
