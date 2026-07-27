"""Publisher / distributor integrations for sage-generated games.

The build pipeline ends with a binary on disk. Getting that binary
into players' hands is a separate, publisher-specific step. This module
generates a `deploy/` directory inside the game's scaffold containing:

  - A shell script (or batch file) that runs the publisher's CLI.
  - A GitHub Actions workflow (if the user wants CI publishing).
  - A README documenting what credentials the user must supply.

Sage does NOT upload anything itself — that requires the user's API key
+ explicit run. We just scaffold the integration so users don't have to
hand-roll Steam pipelines from scratch.

Supported publishers (most-used first):
  - itch.io       (butler CLI, indie web + desktop)
  - Steam         (steamcmd / steampipe, PC desktop)
  - GitHub Pages  (gh-pages branch, free web hosting)
  - Google Play   (fastlane, Android)
  - App Store     (fastlane, iOS — Apple ID + provisioning required)
"""

from __future__ import annotations

from .base import PublisherAdapter, PublisherSpec
from .registry import REGISTRY, get_publisher


__all__ = [
    "PublisherAdapter", "PublisherSpec",
    "REGISTRY", "get_publisher",
]
