"""finish the website onboarding once this device signed in."""

from __future__ import annotations

import typer
from ....sdk.settings.device import OnboardingRequired


# -- auth -------------------------------------------------------------------
def _finish_website_onboarding(exc: OnboardingRequired) -> None:
    from probe.core import events as json_events
    from probe.cli.wizard import terminal as tui

    json_events.onboarding_required(exc.onboarding_url)
    # Through `tui.final`: this is the run's last word, and inside the
    # wizard's window a plain print would close with the window.
    if exc.onboarding_url:
        tui.final(f"Complete onboarding on {exc.onboarding_url} first.")
    else:
        tui.final(str(exc))
    tui.final("Then run the install command shown there.")
    raise typer.Exit(0)
