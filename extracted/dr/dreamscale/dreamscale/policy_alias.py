"""Between-episode hot-swap helper for living Policy addresses (``<org>/<policy>:live|staging``).

Active robots never swap weights mid-episode. Between episodes, ``PolicyTargetWatcher`` queries
``GET /v1/policies/{ref}/target`` and reports when the alias points to a newer deployment or
version so the robot loop can cleanly close the old session and reconnect to the new one.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass

POLICY_ALIASES = frozenset({"live", "staging"})


@dataclass(frozen=True)
class PolicyTarget:
    policy_id: str
    slug: str
    address: str
    alias: str
    version: int | None
    deployment_id: str | None
    experience_dataset_id: str | None = None
    updated_at: str | None = None


def split_policy_alias(model_ref: str) -> tuple[str, str | None]:
    """Split ``<org>/<policy>:live`` into ``(<org>/<policy>, 'live')``; plain refs yield None."""
    text = model_ref.strip()
    if ":" not in text:
        return text, None
    head, tail = text.rsplit(":", 1)
    if tail in POLICY_ALIASES:
        return head, tail
    return text, None


def is_policy_alias_ref(model_ref: str) -> bool:
    _, alias = split_policy_alias(model_ref)
    return alias is not None


class PolicyTargetWatcher:
    """Checks a Policy alias between episodes and signals when a hot-swap is available."""

    def __init__(
        self,
        model_ref: str,
        *,
        api_url: str,
        api_key: str,
        current_deployment_id: str | None = None,
        current_version: int | None = None,
        timeout_s: float = 5.0,
        fetcher: Callable[[str, dict[str, str], float], dict] | None = None,
    ) -> None:
        self.base_ref, alias = split_policy_alias(model_ref)
        self.alias = alias or "live"
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.current_deployment_id = current_deployment_id
        self.current_version = current_version
        self._fetcher = fetcher or self._http_get_json

    @staticmethod
    def _http_get_json(url: str, headers: dict[str, str], timeout_s: float) -> dict:
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310
            return json.loads(resp.read().decode("utf-8"))

    def fetch_target(self) -> PolicyTarget:
        quoted = urllib.parse.quote(self.base_ref, safe="/")
        url = f"{self.api_url}/v1/policies/{quoted}/target?alias={urllib.parse.quote(self.alias)}"
        payload = self._fetcher(
            url,
            {"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"},
            self.timeout_s,
        )
        return PolicyTarget(
            policy_id=str(payload["policy_id"]),
            slug=str(payload["slug"]),
            address=str(payload["address"]),
            alias=str(payload["alias"]),
            version=payload.get("version"),
            deployment_id=payload.get("deployment_id"),
            experience_dataset_id=payload.get("experience_dataset_id"),
            updated_at=payload.get("updated_at"),
        )

    def check_between_episodes(self) -> PolicyTarget | None:
        """Return the new ``PolicyTarget`` if the alias moved to another deployment, else None."""
        target = self.fetch_target()
        if not target.deployment_id:
            return None
        if self.current_deployment_id is None:
            self.current_deployment_id = target.deployment_id
            self.current_version = target.version
            return None
        if target.deployment_id != self.current_deployment_id:
            return target
        return None

    def mark_swapped(self, target: PolicyTarget) -> None:
        """Record that the robot has switched cleanly to ``target``."""
        self.current_deployment_id = target.deployment_id
        self.current_version = target.version
