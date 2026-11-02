"""family update_rejected: a switch-back the guard recorded lately."""

from __future__ import annotations
from probe.service.watch.incident import Family
from probe.service.watch.settings import GUARD_FRESH_S


class GuardCheckMixin:
    """Part of Watch: its methods run with `self` the Watch; compose() folds them into Watch."""

    def _guard(self, record: dict | None) -> None:
        """A switch-back the guard recorded lately (`guard.json` `ok: false`):
        one `update_rejected`, once per rejected version."""
        if not isinstance(record, dict) or record.get("ok") is not False:
            return
        rejected, at = record.get("to"), record.get("at")
        if not isinstance(rejected, str) or not isinstance(at, (int, float)) or self.clock() - at > GUARD_FRESH_S:
            return
        facts = {"rejected_version": rejected, **{k: record.get(k) for k in ("from", "reason", "rollback", "active",
                                                                            "answering", "at")}}
        self.note(Family.UPDATE_REJECTED, "switched_back", None, facts, once=f"update_rejected:{rejected}")
