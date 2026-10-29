"""The agent goals of `plato vault`: one Markdown template per goal, in this package.

A template states the goal, where the data is, the checks that prove it is done,
the page facts seen in live runs, and the secret limits. It does not give a click
order. Slots are ``$name`` (:class:`string.Template`), so the ``@@VAULT {json}``
lines need no brace escapes. A slot that the caller does not fill raises ``KeyError``.
"""

from __future__ import annotations

from enum import StrEnum
from functools import cache
from importlib import resources
from string import Template


class GoalTemplate(StrEnum):
    """Every template file in this package. A recipe names its goals by these values."""

    # Shared rules, filled into the goals as $no_files and $screen_rule.
    no_files = "no_files.md"
    pi_screen = "pi_screen.md"
    # Canva (VendorRecipe): the portal agent and the consent agent, ego-browser and Pi.
    canva_portal = "canva_portal.md"
    canva_consent = "canva_consent.md"
    canva_pi_portal = "canva_pi_portal.md"
    canva_pi_consent = "canva_pi_consent.md"
    # Canva (TotpRecipe): the authenticator-app setup agent, ego-browser and Pi.
    canva_totp = "canva_totp.md"
    canva_pi_totp = "canva_pi_totp.md"
    # Any vendor (app_mint): the OAuth app and consent agent on the Pi, with web search.
    mint_pi = "mint_pi.md"
    # Any vendor (mint_docs): the docs model that reads the developer docs before the walk.
    mint_docs = "mint_docs.md"


@cache
def load_prompt(name: GoalTemplate) -> str:
    """The raw template text from the installed package, without the end newline."""
    return resources.files(__name__).joinpath(name.value).read_text(encoding="utf-8").strip()


def render_prompt(name: GoalTemplate, **slots: object) -> str:
    return Template(load_prompt(name)).substitute(slots)


__all__ = ["GoalTemplate", "load_prompt", "render_prompt"]
