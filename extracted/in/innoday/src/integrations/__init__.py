"""
Integrations that make InnoDay a consumer of external packages.

Today this hosts ``InnoDayVersionStore`` -- InnoDay's implementation of
blastoff's ``VersionStore`` seam (see ``blastoff.stores.VersionStore``). It
lets the ``innoday release`` / ``innoday hotfix`` proxy commands drive
blastoff's release engine while reading version state from, and recording
releases into, the InnoDay DB (via the existing releases API) instead of a
local file.

The dependency arrow points one way only: InnoDay depends on ``blastoff`` and
implements its interface; ``blastoff`` imports nothing from InnoDay.
"""

from src.integrations.innoday_version_store import InnoDayVersionStore

__all__ = ["InnoDayVersionStore"]
