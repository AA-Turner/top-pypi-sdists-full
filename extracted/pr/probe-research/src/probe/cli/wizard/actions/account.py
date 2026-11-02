"""the Account action: account maintenance flags and the legacy account details screen."""

from __future__ import annotations

import typer
from ....sdk.settings.device import OnboardingRequired


def _run_account_action(
    chosen_action,
    *,
    caps,
    base_now: str,
    yes: bool,
    sources: tuple[str, ...],
    telemetry=None,
) -> list[str] | None:
    """Account maintenance flags and the legacy account details screen.

    `sources` is ONLY about capture. The credential half of an account is
    device-wide -- one config file -- so this runs once per wizard pass however
    many coding agents are selected; the capture half is per agent, and that is
    what the list is for.
    """
    from probe.cli.wizard.actions import onboarding as actions_mod
    from probe.cli import wizard as wizard
    from probe import analytics as telemetry_mod
    from probe.cli.wizard import terminal as tui

    tel = telemetry_mod.null_context() if telemetry is None else telemetry
    saved = wizard.saved_accounts()
    choice = {
        actions_mod.Action.SIGN_IN: wizard.AccountAction.SIGN_IN,
        actions_mod.Action.SIGN_OUT: wizard.AccountAction.SIGN_OUT,
    }.get(chosen_action)

    if choice is None:
        if yes or not wizard.interactive():
            # A screen nobody can answer must not answer for them. Minting a
            # credential or clearing one unasked is the single thing this action
            # may never do on its own, so the flagless headless path REPORTS and
            # names the two flags that decide.
            return [
                "This device's account:",
                *wizard.describe_account(caps, saved=saved),
                "",
                "`probe wizard --action login` signs in; "
                "`probe wizard --action logout` clears the credentials saved here.",
            ]
        tui.clear()
        picked = wizard.run_account_menu(caps, saved=saved)
        if picked is None or picked is tui.BACK or picked is wizard.AccountAction.BACK:
            return None  # backed out: nothing happened, nothing to pause on
        choice = picked

    if choice is wizard.AccountAction.SWITCH:
        tui.clear()
        target = wizard.run_switch_menu(saved)
        if target is None or target is tui.BACK:
            return None
        return wizard.switch_account(target, sources)

    if choice is wizard.AccountAction.REMOVE:
        tui.clear()
        target = wizard.run_switch_menu(saved, removing=True)
        if target is None or target is tui.BACK:
            return None
        tui.clear()
        if wizard.confirm_remove_account(target) is not True:
            return None
        return wizard.remove_account(target)

    if choice is wizard.AccountAction.SIGN_OUT:
        if not yes and wizard.interactive():
            # A confirmation page first (Richard 2026-09-29); anything but a
            # yes is back to the menu with nothing changed.
            tui.clear()
            if wizard.confirm_sign_out(caps.logged_in_as if caps else None) is not True:
                return None
        # BEFORE the credential goes: `sign_out` revokes this device's token,
        # and an event resolved after that belongs to no person (`pin_identity`).
        tel.pin_identity()
        lines = wizard.sign_out(sources)
        # On a screen, what happened and the errors, not each step taken
        # (imports cleared, every agent's capture turned off, each token
        # revoked): the lines are what a script reads.
        cleared = not any(wizard.CREDENTIALS_NOT_CLEARED in line for line in lines)
        shown = lines if yes or not wizard.interactive() else wizard.result_page(
            ["Signed out of Probe on this device." if cleared else "Not signed out: the saved credentials remain.",
             "The plugins stay installed; Uninstall Probe removes them."],
            details=wizard.attention_lines(lines),
        )
        for line in shown:
            tui.say(line)
        _record_device_sign_in(wanted=False)
        tel.emit(
            telemetry_mod.EVENT_WIZARD_SIGNED_OUT,
            agent_count=len(sources),
            # Counts only, never the `! ...` lines themselves: they name paths.
            warnings=sum(1 for line in lines if line.startswith("!")),
        )
        raise typer.Exit(0)

    # SIGN IN. This one streams: the approval URL is only useful WHILE the flow
    # blocks on it, and everything else here returns its lines to be paged after
    # the fact.
    live = tui.interactive()
    heading = "Approve this device in the browser to sign in."

    def _prompt(prompt) -> None:
        details = [
            f"  visit: {prompt.verification_uri_complete}",
            f"  code:  {prompt.user_code}",
        ]
        if live:
            tui.page([heading, "", *details])
        else:
            for line in details:
                tui.say(line)

    if live:
        tui.page([heading, ""])
    else:
        tui.say(heading)
        tui.say()
    from probe.core import events as json_events

    json_events.step(json_events.Step.SIGN_IN, json_events.Status.STARTED, heading)
    try:
        result = wizard.sign_in(
            base_url=base_now,
            sources=sources,
            on_prompt=_prompt,
        )
    except OnboardingRequired as exc:
        json_events.step(json_events.Step.SIGN_IN, json_events.Status.FAILED, str(exc))
        _finish_website_onboarding(exc)
    json_events.step(
        json_events.Step.SIGN_IN,
        json_events.Status.DONE if result.ok else json_events.Status.FAILED,
        "\n".join(result.lines),
    )
    _record_device_sign_in(wanted=True, ok=result.ok, message="" if result.ok else "\n".join(result.lines))
    tel.emit(
        telemetry_mod.EVENT_WIZARD_SIGNED_IN,
        outcome=(
            telemetry_mod.SignInOutcome.SUCCESS if result.ok else telemetry_mod.SignInOutcome.FAILED
        ),
        via_account_menu=True,
    )
    if not result.ok and chosen_action is actions_mod.Action.SIGN_IN:
        # `--action login` is a SCRIPTED call, and a caller that cannot see the
        # exit status cannot tell an approved device from a refused one -- it
        # would go on to install plugins against a credential nobody minted.
        # The menu path deliberately does not exit: it returns to the menu,
        # where trying again is one keystroke.
        for line in result.lines:
            tui.say(line)
        raise typer.Exit(1)
    return result.lines
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.account.website_onboarding import _finish_website_onboarding  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.result_rows import _record_device_sign_in  # noqa: E402 -- pieces need each other; the front door loads this one first
