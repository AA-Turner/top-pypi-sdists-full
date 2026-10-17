"""Skill text that ships in the CLI wheel before its plugin copies, when it does.

Plan writer-owns-summary, D29: PR D1 (the CLI) changed `skills/track-work` and
added `skills/write-summary` and `skills/overview-visuals`; their copies in
`plugins/**` (the main agent's, the inline agent's, pi's, the tap's) were PR D2,
merged once that CLI was on PyPI: a push to main that touches
`agent/plugins/**` reaches users at once (`mirror-public.yml`), and a skill
naming a command their CLI lacks would arrive first.

While a hold is on, the sync guards xfail(strict=True) on the held skills, so
the plugin release's `make sync-plugin` must empty this file in the same change
(a held copy that is still in sync fails), and the coverage guards refuse a
held new skill the plugins already carry. Both sets are empty now (D2 landed).
Use it again only for a plugin release that must trail a CLI release: name the
skills here, keep the plugin copies as they were, and let the next change run
`make sync-plugin` and empty the sets.
"""

from __future__ import annotations

#: Skills whose plugin, pi and tap copies trail the canonical text (D2).
HELD_SKILLS: frozenset[str] = frozenset()
#: New skills that no plugin carries yet (D2 adds them to every copy).
HELD_NEW_SKILLS: frozenset[str] = frozenset()

REASON = "plan writer-owns-summary D29: the plugin copy is PR D2, after the CLI release"
