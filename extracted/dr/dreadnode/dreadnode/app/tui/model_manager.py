import asyncio
import contextlib
import hashlib
import json
import os
import tempfile
import time
import typing as t
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import httpx
from loguru import logger

from dreadnode.app.api.client import ApiClient
from dreadnode.app.config import Profile
from dreadnode.app.tui.error_handler import INSUFFICIENT_CREDITS_MESSAGE
from dreadnode.core.exceptions import InsufficientCreditsError

PLATFORM_MODELS_UNAVAILABLE_MESSAGE = "Platform-hosted models are not available"
DREADNODE_LLM_BASE_ENV = "DREADNODE_LLM_BASE"
DREADNODE_LLM_API_KEY_ENV = "DREADNODE_LLM_API_KEY"
LITELLM_REFRESH_WINDOW = timedelta(minutes=5)
PROXY_MODELS_CACHE_FILE = Path.home() / ".dreadnode" / "proxy-models.json"
MODEL_BROWSER_FEATURED_LIMIT = 12
MODEL_BROWSER_SEARCH_LIMIT = 50
DEFAULT_INFERENCE_CREDITS_PER_DOLLAR = 1000


@dataclass(slots=True)
class ModelCatalogState:
    platform_models: list[dict[str, t.Any]] = field(default_factory=list)
    user_model_ids: list[str] = field(default_factory=list)
    preference_platform_model_ids: list[str] = field(default_factory=list)
    inference_credits_per_dollar: int | None = None
    access_restricted: bool = False
    proxy_model_ids_synced: bool = False
    litellm_key_expires_at: datetime | None = None


class ModelCatalogContext(t.Protocol):
    def current_model(self) -> str: ...

    def is_authenticated(self) -> bool: ...

    def current_profile(self) -> Profile | None: ...

    def platform_client(self) -> tuple[ApiClient, Profile]: ...

    def current_org(self) -> str | None: ...

    def model_was_explicitly_selected(self) -> bool: ...


class ModelUiHost(t.Protocol):
    def model_browser_open(self) -> bool: ...

    def dismiss_pushed_screens(self) -> None: ...

    def open_model_browser(
        self,
        *,
        platform_models: list[dict[str, t.Any]],
        byok_models: list[dict[str, t.Any]],
        current_model: str,
        inference_credits_per_dollar: int | None,
        access_restricted: bool,
        search_models: t.Callable[..., t.Any],
        on_selected: t.Callable[[str | None], None],
    ) -> None: ...

    def refresh_model_browser(
        self,
        *,
        platform_models: list[dict[str, t.Any]],
        byok_models: list[dict[str, t.Any]],
        current_model: str,
        inference_credits_per_dollar: int | None,
        access_restricted: bool,
    ) -> None: ...


class BackgroundRunner(t.Protocol):
    def run_exclusive(self, coro: t.Awaitable[t.Any], *, group: str) -> None: ...


def parse_model_order(value: t.Any) -> int | None:
    """Parse a model's display-order hint, mirroring the model browser's sort."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and value >= 1:
        return value
    if isinstance(value, str) and value.strip():
        try:
            parsed = int(value)
        except ValueError:
            return None
        return parsed if parsed >= 1 else None
    return None


class ModelNotifier(t.Protocol):
    def flash_info(self, message: str) -> None: ...

    def flash_warning(self, message: str) -> None: ...


class ModelSelectionActions(t.Protocol):
    def apply_model(self, model_id: str) -> None: ...

    def persist_default_model_choice(self, model_id: str) -> None: ...

    def mark_model_explicitly_selected(self) -> None: ...


class ModelManager:
    """Owns runtime model catalog, proxy-model sync, and model browser flows."""

    def __init__(
        self,
        *,
        state: ModelCatalogState,
        context: ModelCatalogContext,
        ui_host: ModelUiHost,
        runner: BackgroundRunner,
        notifier: ModelNotifier,
        actions: ModelSelectionActions,
    ) -> None:
        self._state = state
        self._context = context
        self._ui_host = ui_host
        self._runner = runner
        self._notifier = notifier
        self._actions = actions
        self._tui_client_id = uuid4().hex

    def open_model_browser_screen(self) -> None:
        """Open the full-screen model browser (toggles closed if already open)."""
        if self._ui_host.model_browser_open():
            self._ui_host.dismiss_pushed_screens()
            return
        self._ui_host.dismiss_pushed_screens()

        if not self._state.platform_models:
            self._state.platform_models = self.load_cached_proxy_models()
        self._ui_host.open_model_browser(
            platform_models=list(self._state.platform_models),
            byok_models=self.browser_seed_models(),
            current_model=self._context.current_model(),
            inference_credits_per_dollar=self._state.inference_credits_per_dollar,
            access_restricted=self._state.access_restricted,
            search_models=self.search_model_browser_models,
            on_selected=self.apply_model_selection,
        )
        if self._context.is_authenticated() and not self._state.proxy_model_ids_synced:
            self.schedule_model_catalog_refresh()

    def apply_model_selection(self, model_id: str | None) -> None:
        """Apply a selected model from any picker surface.

        The selection applies to the active session only — we intentionally
        do not persist this as the profile default (CAP-1048). Other sessions
        keep whatever model they were already using, and the next new session
        still spawns with the saved profile default.
        """
        current_model = self._context.current_model()
        if not model_id or model_id == current_model:
            return
        self._actions.mark_model_explicitly_selected()
        self._actions.apply_model(model_id)
        self._notifier.flash_info(f"Model: {model_id}")

    def browser_seed_models(self) -> list[dict[str, t.Any]]:
        """Build the local seed set shown before the browser fetches featured results."""
        results: list[dict[str, t.Any]] = []
        seen: set[str] = set()
        current_model = self._context.current_model()

        for model_id in self._state.user_model_ids:
            if model_id.startswith("dn/") or model_id in seen:
                continue
            seen.add(model_id)
            results.append({"id": model_id})

        if not current_model.startswith("dn/") and current_model not in seen:
            results.insert(0, {"id": current_model})

        return results

    def schedule_model_catalog_refresh(self) -> None:
        """Refresh supported proxy models in the background for the model browser."""
        self._runner.run_exclusive(self.refresh_model_catalog(), group="model_catalog_fetch")

    async def refresh_model_catalog(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        """Fetch supported proxy model IDs for the model browser."""
        if self._state.proxy_model_ids_synced:
            return

        resolved_base_url = base_url or os.environ.get(DREADNODE_LLM_BASE_ENV, "").strip()
        resolved_api_key = api_key or os.environ.get(DREADNODE_LLM_API_KEY_ENV, "").strip()
        if not resolved_base_url or not resolved_api_key:
            return

        try:
            payload = await asyncio.to_thread(
                self.fetch_proxy_models,
                resolved_base_url,
                resolved_api_key,
            )
        except Exception as exc:
            logger.debug("Failed to fetch proxy models for picker: {}", exc)
            return

        model_ids = self.extract_proxy_model_ids(payload)
        accepted_model_ids = self.preference_model_ids_from_complete_proxy_snapshot(
            model_ids,
            preference_model_ids=self._state.preference_platform_model_ids,
        )
        if accepted_model_ids:
            self.write_cached_proxy_models(
                accepted_model_ids,
                preference_model_ids=self._state.preference_platform_model_ids,
                api_key=resolved_api_key,
            )
        self._state.proxy_model_ids_synced = True

        self._ui_host.refresh_model_browser(
            platform_models=list(self._state.platform_models),
            byok_models=self.browser_seed_models(),
            current_model=self._context.current_model(),
            inference_credits_per_dollar=self._state.inference_credits_per_dollar,
            access_restricted=self._state.access_restricted,
        )

    def platform_model_ids(self) -> list[str]:
        """Return enabled platform-hosted model IDs, ordered like the model browser.

        Sorted by each model's ``order`` hint (unordered models sort last),
        falling back to preference-list position — the same key
        ``screens/models.py`` uses to pick the browser's featured/first entry.
        """
        enabled = [m for m in self._state.platform_models if m.get("enabled", True)]
        keyed = [
            (self.parse_model_order(m.get("order")), index, m) for index, m in enumerate(enabled)
        ]
        keyed.sort(key=lambda item: (item[0] is None, item[0] or 0, item[1]))
        return [m["id"] for _order, _index, m in keyed]

    @staticmethod
    def parse_model_order(value: t.Any) -> int | None:
        """Parse a model's display-order hint, mirroring the model browser's sort."""
        return parse_model_order(value)

    def apply_default_platform_model_if_unset(self) -> None:
        """Default a fresh profile straight to a platform-hosted (dn/) model.

        Without this, a brand-new profile sits on the hardcoded BYOK
        fallback (``client.runtime_client.DEFAULT_MODEL``) until the user
        manually picks something — which fails outright for anyone without
        their own provider API key configured. Only fires when nothing has
        already made an explicit choice: no persisted profile default, no
        explicit ``--model`` flag or in-session pick this run (tracked via
        ``model_was_explicitly_selected``), and the app is still sitting on
        that hardcoded fallback.
        """
        profile = self._context.current_profile()
        if profile is not None and profile.default_model:
            return

        if self._context.model_was_explicitly_selected():
            return

        from dreadnode.app.client.runtime_client import DEFAULT_MODEL

        if self._context.current_model() != DEFAULT_MODEL:
            return

        allowed_model_ids = self.platform_model_ids()
        if not allowed_model_ids:
            return

        self._apply_and_persist_fallback_model(allowed_model_ids[0])

    def apply_restricted_current_model_fallback(self) -> None:
        """Switch away from a stale platform model no longer allowed by the org."""
        if not self._state.access_restricted:
            return
        current_model = self._context.current_model()
        if not current_model.startswith("dn/"):
            return

        allowed_model_ids = self.platform_model_ids()
        if current_model in allowed_model_ids or not allowed_model_ids:
            return

        self._apply_and_persist_fallback_model(allowed_model_ids[0])

    def _apply_and_persist_fallback_model(self, fallback_model: str) -> None:
        """Switch to `fallback_model` and persist it as the profile default."""
        self._actions.apply_model(fallback_model)
        self._actions.persist_default_model_choice(fallback_model)

    def clear_platform_proxy_state(self) -> None:
        """Clear provisioned proxy-model and LiteLLM key state."""
        self._state.platform_models = []
        self._state.user_model_ids = []
        self._state.preference_platform_model_ids = []
        self._state.inference_credits_per_dollar = None
        self._state.access_restricted = False
        self._state.proxy_model_ids_synced = False
        self._state.litellm_key_expires_at = None
        os.environ.pop(DREADNODE_LLM_BASE_ENV, None)
        os.environ.pop(DREADNODE_LLM_API_KEY_ENV, None)

    @staticmethod
    def parse_inference_credits_per_dollar(value: t.Any) -> int | None:
        if value is None:
            return DEFAULT_INFERENCE_CREDITS_PER_DOLLAR
        if isinstance(value, bool):
            return None
        if isinstance(value, int) and value > 0:
            return value
        if isinstance(value, float) and value > 0:
            return int(value)
        return None

    @staticmethod
    def normalize_platform_model_ids(model_ids: list[str] | None) -> list[str]:
        if not model_ids:
            return []
        return sorted(
            {
                model_id.strip()
                for model_id in model_ids
                if isinstance(model_id, str) and model_id.strip().startswith("dn/")
            }
        )

    @staticmethod
    def api_key_hash(api_key: str | None) -> str | None:
        if not isinstance(api_key, str) or not api_key:
            return None
        return hashlib.sha256(api_key.encode("utf-8")).hexdigest()

    @staticmethod
    def parse_expires_at(value: t.Any) -> datetime | None:
        if not isinstance(value, str) or not value.strip():
            return None
        candidate = value.strip()
        if candidate.endswith("Z"):
            candidate = f"{candidate[:-1]}+00:00"
        try:
            parsed = datetime.fromisoformat(candidate)
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed

    @staticmethod
    def extract_platform_models(payload: dict[str, t.Any]) -> list[dict[str, t.Any]]:
        models = payload.get("models") if isinstance(payload, dict) else None
        if isinstance(models, dict):
            entries: list[dict[str, t.Any]] = []
            for model_id, entry in models.items():
                if not isinstance(model_id, str):
                    continue
                if isinstance(entry, dict):
                    merged = dict(entry)
                    merged.setdefault("id", model_id)
                    entries.append(merged)
                else:
                    entries.append({"id": model_id})
        elif isinstance(models, list):
            entries = [entry for entry in models if isinstance(entry, dict)]
        else:
            return []

        results: list[dict[str, t.Any]] = []
        for entry in entries:
            model_id = entry.get("id")
            if not isinstance(model_id, str) or not model_id.startswith("dn/"):
                continue
            enabled = True
            status = entry.get("status")
            name = None
            if "enabled" in entry:
                enabled = bool(entry.get("enabled"))
            if isinstance(entry.get("name"), str):
                name = entry.get("name")
            result: dict[str, t.Any] = {"id": model_id, "enabled": enabled, "status": status}
            if name:
                result["name"] = name
            for extra_field in (
                "order",
                "cost",
                "limits",
                "cost_input",
                "cost_output",
                "context_window",
                "max_output",
                "capabilities",
                "modalities",
                "knowledge",
                "release_date",
                "open_weights",
            ):
                value = entry.get(extra_field)
                if value is not None:
                    result[extra_field] = value
            results.append(result)
        return results

    @staticmethod
    def extract_user_model_ids(payload: dict[str, t.Any]) -> list[str]:
        """Extract enabled non-platform model IDs from user preferences."""
        models = payload.get("models") if isinstance(payload, dict) else None
        if not isinstance(models, list):
            return []

        results: list[str] = []
        seen: set[str] = set()
        for entry in models:
            if not isinstance(entry, dict):
                continue
            model_id = entry.get("id")
            if not isinstance(model_id, str) or not model_id.strip():
                continue
            if model_id.startswith("dn/") or model_id in seen:
                continue
            seen.add(model_id)
            results.append(model_id)
        return results

    @staticmethod
    def extract_proxy_model_ids(payload: t.Any) -> list[str]:
        entries = payload
        if isinstance(payload, dict):
            entries = payload.get("data", payload.get("models"))
        if not isinstance(entries, list):
            return []

        results: list[str] = []
        seen: set[str] = set()
        for entry in entries:
            model_id: str | None
            if isinstance(entry, str):
                model_id = entry
            elif isinstance(entry, dict):
                raw_model_id = entry.get("id")
                model_id = raw_model_id if isinstance(raw_model_id, str) else None
            else:
                continue
            if not isinstance(model_id, str) or not model_id.strip():
                continue
            if not model_id.startswith("dn/") or model_id in seen:
                continue
            seen.add(model_id)
            results.append(model_id)
        return results

    @classmethod
    def preference_model_ids_from_complete_proxy_snapshot(
        cls,
        proxy_model_ids: list[str] | None,
        *,
        preference_model_ids: list[str] | None,
    ) -> list[str]:
        normalized_preference_model_ids = cls.normalize_platform_model_ids(preference_model_ids)
        if not normalized_preference_model_ids:
            return []

        proxy_model_id_set = set(cls.normalize_platform_model_ids(proxy_model_ids))
        if not proxy_model_id_set:
            return []

        missing_model_ids = [
            model_id
            for model_id in normalized_preference_model_ids
            if model_id not in proxy_model_id_set
        ]
        if missing_model_ids:
            logger.debug(
                "Ignoring incomplete proxy model snapshot; missing {} preference models",
                len(missing_model_ids),
            )
            return []

        # Keep preferences authoritative and intentionally drop proxy-only extras.
        return normalized_preference_model_ids

    @staticmethod
    def extract_catalog_models(payload: t.Any) -> list[dict[str, t.Any]]:
        entries = payload
        if isinstance(payload, dict):
            entries = payload.get("models", payload.get("data"))
        if not isinstance(entries, list):
            return []

        results: list[dict[str, t.Any]] = []
        seen: set[str] = set()
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            model_id = entry.get("id")
            if not isinstance(model_id, str) or not model_id.strip():
                continue
            if model_id.startswith("dn/") or model_id in seen:
                continue
            seen.add(model_id)

            model: dict[str, t.Any] = {"id": model_id}
            name = entry.get("name")
            provider = entry.get("provider")
            status = entry.get("status")
            cost = entry.get("cost")
            limits = entry.get("limits")
            capabilities = entry.get("capabilities")
            modalities = entry.get("modalities")
            knowledge = entry.get("knowledge")
            release_date = entry.get("release_date")
            open_weights = entry.get("open_weights")
            if isinstance(name, str) and name.strip():
                model["name"] = name
            if isinstance(provider, str) and provider.strip():
                model["provider"] = provider
            if isinstance(status, str) and status.strip():
                model["status"] = status
            if isinstance(cost, dict):
                model["cost"] = cost
            if isinstance(limits, dict):
                model["limits"] = limits
            if isinstance(capabilities, list):
                model["capabilities"] = [
                    capability
                    for capability in capabilities
                    if isinstance(capability, str) and capability.strip()
                ]
            if isinstance(modalities, dict):
                model["modalities"] = modalities
            if isinstance(knowledge, str) and knowledge.strip():
                model["knowledge"] = knowledge
            if isinstance(release_date, str) and release_date.strip():
                model["release_date"] = release_date
            if isinstance(open_weights, bool):
                model["open_weights"] = open_weights
            results.append(model)
        return results

    def load_cached_proxy_models(
        self,
        *,
        preference_model_ids: list[str] | None = None,
        api_key: str | None = None,
    ) -> list[dict[str, t.Any]]:
        """Read the last successful proxy model snapshot for the current server."""
        profile = self._context.current_profile()
        if profile is None or not PROXY_MODELS_CACHE_FILE.exists():
            return []

        try:
            payload = json.loads(PROXY_MODELS_CACHE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            logger.debug("Failed to read proxy model cache: {}", exc)
            return []

        if not isinstance(payload, dict):
            return []
        entry = payload.get(profile.url.rstrip("/"))
        if not isinstance(entry, dict):
            return []

        expected_model_ids = self.normalize_platform_model_ids(preference_model_ids)
        cached_preference_model_ids = self.normalize_platform_model_ids(
            t.cast("list[str] | None", entry.get("preference_model_ids"))
        )
        if expected_model_ids and cached_preference_model_ids != expected_model_ids:
            logger.debug("Invalidating proxy model cache: preference model set changed")
            self.invalidate_cached_proxy_models()
            return []

        expected_key_hash = self.api_key_hash(api_key)
        cached_key_hash = entry.get("api_key_hash")
        if expected_key_hash is not None and cached_key_hash != expected_key_hash:
            logger.debug("Invalidating proxy model cache: LiteLLM key changed")
            self.invalidate_cached_proxy_models()
            return []

        models = self.extract_proxy_model_ids(entry.get("models"))
        accepted_model_ids = self.preference_model_ids_from_complete_proxy_snapshot(
            models,
            preference_model_ids=expected_model_ids,
        )
        if expected_model_ids and not accepted_model_ids:
            logger.debug("Invalidating proxy model cache: cached models are incomplete")
            self.invalidate_cached_proxy_models()
            return []

        cached_model_ids = accepted_model_ids or models
        if cached_model_ids:
            logger.debug("Loaded {} cached proxy models for {}", len(cached_model_ids), profile.url)
        return self.platform_models_from_ids(cached_model_ids, current=[])

    def write_cached_proxy_models(
        self,
        model_ids: list[str],
        *,
        preference_model_ids: list[str] | None = None,
        api_key: str | None = None,
    ) -> None:
        """Persist the last successful proxy model snapshot for the current server."""
        profile = self._context.current_profile()
        if profile is None or not model_ids:
            return

        payload: dict[str, t.Any] = {}
        if PROXY_MODELS_CACHE_FILE.exists():
            try:
                existing = json.loads(PROXY_MODELS_CACHE_FILE.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                logger.debug("Failed to read existing proxy model cache: {}", exc)
            else:
                if isinstance(existing, dict):
                    payload = existing

        payload[profile.url.rstrip("/")] = {
            "models": model_ids,
            "cached_at": datetime.now(tz=UTC).isoformat(),
            "preference_model_ids": self.normalize_platform_model_ids(preference_model_ids),
            "api_key_hash": self.api_key_hash(api_key),
        }
        self.write_cache_file(PROXY_MODELS_CACHE_FILE, payload)

    def invalidate_cached_proxy_models(self) -> None:
        """Drop cached proxy models for the current profile URL."""
        profile = self._context.current_profile()
        if profile is None or not PROXY_MODELS_CACHE_FILE.exists():
            return

        try:
            payload = json.loads(PROXY_MODELS_CACHE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            logger.debug("Failed to read proxy model cache for invalidation: {}", exc)
            return
        if not isinstance(payload, dict):
            return

        removed = payload.pop(profile.url.rstrip("/"), None)
        if removed is None:
            return

        if payload:
            self.write_cache_file(PROXY_MODELS_CACHE_FILE, payload)
            return
        with contextlib.suppress(OSError):
            PROXY_MODELS_CACHE_FILE.unlink()

    @staticmethod
    def fetch_proxy_models(base_url: str, api_key: str) -> dict[str, t.Any]:
        """Fetch the supported model list from the provisioned LiteLLM proxy."""
        response = httpx.get(
            f"{base_url.rstrip('/')}/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10.0,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            return {}
        return payload

    @staticmethod
    def fetch_catalog_models(
        api: ApiClient,
        *,
        query: str | None,
        limit: int,
        provider: str | None,
        capabilities: list[str] | None,
        open_weights: bool | None,
        min_context: int | None,
        max_context: int | None,
        min_price: float | None,
        max_price: float | None,
        featured: bool,
    ) -> list[dict[str, t.Any]]:
        """Fetch featured or searched BYOK models for the full browser."""
        kwargs: dict[str, t.Any] = {
            "query": query,
            "limit": limit,
            "featured": featured,
        }
        kwargs.update(
            {
                key: value
                for key, value in {
                    "provider": provider,
                    "capabilities": capabilities,
                    "open_weights": open_weights,
                    "min_context": min_context,
                    "max_context": max_context,
                    "min_price": min_price,
                    "max_price": max_price,
                }.items()
                if value is not None and value != []
            }
        )
        return api.list_catalog_models(**kwargs)

    @staticmethod
    def platform_models_from_ids(
        model_ids: list[str],
        *,
        current: list[dict[str, t.Any]],
    ) -> list[dict[str, t.Any]]:
        """Build platform picker entries from supported proxy model IDs."""
        from dreadnode.app.model_catalog import display_name

        current_by_id = {
            model["id"]: model for model in current if isinstance(model.get("id"), str)
        }
        results: list[dict[str, t.Any]] = []
        for model_id in model_ids:
            existing = current_by_id.get(model_id, {})
            name = existing.get("name") if isinstance(existing.get("name"), str) else None
            status = existing.get("status")
            entry: dict[str, t.Any] = {
                "id": model_id,
                "enabled": True,
                "status": status,
                "name": name or display_name(model_id),
            }
            results.append(entry)
        return results

    @staticmethod
    def write_cache_file(path: Path, payload: dict[str, t.Any]) -> None:
        """Atomically write a small JSON cache file with restricted permissions."""
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as handle:
                json.dump(payload, handle, indent=2)
                handle.flush()
                os.fsync(handle.fileno())
            Path(tmp_path).chmod(0o600)
            Path(tmp_path).replace(path)
        except BaseException:
            with contextlib.suppress(OSError):
                Path(tmp_path).unlink()
            raise

    @staticmethod
    def is_litellm_service_unavailable(exc: Exception) -> bool:
        message = str(exc)
        if "503" in message:
            return True
        status_code = getattr(getattr(exc, "response", None), "status_code", None)
        return status_code == 503

    async def refresh_platform_models_and_key(self, api: ApiClient) -> None:
        self.clear_platform_proxy_state()
        try:
            t0 = time.monotonic()
            org = self._context.current_org()
            if not org:
                profile = self._context.current_profile()
                if profile is not None:
                    org = profile.default_organization
            preferences = await asyncio.to_thread(api.get_user_preferences, org=org)
            logger.debug(
                "Boot timing | get_user_preferences={:.0f}ms",
                (time.monotonic() - t0) * 1000,
            )
        except Exception as exc:
            logger.warning("Failed to fetch user preferences: {}", exc)
            return

        self._state.platform_models = self.extract_platform_models(preferences)
        self._state.user_model_ids = self.extract_user_model_ids(preferences)
        platform_model_ids: list[str] = []
        for model in self._state.platform_models:
            model_id = model.get("id")
            if isinstance(model_id, str):
                platform_model_ids.append(model_id)
        self._state.preference_platform_model_ids = self.normalize_platform_model_ids(
            platform_model_ids
        )
        self._state.inference_credits_per_dollar = self.parse_inference_credits_per_dollar(
            preferences.get("inference_credits_per_dollar")
        )
        self._state.access_restricted = bool(preferences.get("access_restricted"))
        self.apply_restricted_current_model_fallback()
        if not self._state.platform_models:
            return
        result = await self.provision_litellm_key(api)
        if result is None:
            return
        base_url = result.get("base_url") or result.get("url")
        api_key = result.get("api_key") or result.get("key")
        if not (isinstance(base_url, str) and isinstance(api_key, str)):
            return

        # Only default a fresh profile onto a platform model once we've
        # confirmed the proxy key actually provisions — otherwise a
        # zero-credit org or a transient LiteLLM outage would permanently
        # persist a default the user can never actually use.
        self.apply_default_platform_model_if_unset()

        # Validate cache freshness/integrity against current preferences
        # without replacing the preference-derived visible model list.
        self.load_cached_proxy_models(
            preference_model_ids=self._state.preference_platform_model_ids,
            api_key=api_key,
        )
        self._runner.run_exclusive(
            self.refresh_model_catalog(base_url=base_url, api_key=api_key),
            group="model_catalog_fetch",
        )

    async def provision_litellm_key(
        self,
        api: ApiClient | None = None,
    ) -> dict[str, t.Any] | None:
        if api is None and not self._context.is_authenticated():
            return None
        org = self._context.current_org()
        if api is None:
            try:
                api, profile = self._context.platform_client()
                if org is None:
                    org = profile.default_organization
            except Exception:
                logger.debug("Cannot provision LiteLLM key: no platform client available")
                return None
        if not org:
            logger.debug("Cannot provision LiteLLM key: no org context available")
            return None
        try:
            t0 = time.monotonic()
            result = await asyncio.to_thread(
                api.provision_inference_key,
                org,
                self._tui_client_id,
            )
            logger.debug(
                "LiteLLM key provisioned | elapsed={:.0f}ms",
                (time.monotonic() - t0) * 1000,
            )
        except InsufficientCreditsError as exc:
            logger.info("LiteLLM key provisioning blocked by insufficient credits: {}", exc)
            self._notifier.flash_warning(INSUFFICIENT_CREDITS_MESSAGE)
            self.clear_platform_proxy_state()
            return None
        except Exception as exc:
            if self.is_litellm_service_unavailable(exc):
                self._notifier.flash_info(PLATFORM_MODELS_UNAVAILABLE_MESSAGE)
                self.clear_platform_proxy_state()
                return None
            logger.warning("Failed to provision LiteLLM key: {}", exc)
            self._notifier.flash_warning("Failed to provision LiteLLM key")
            return None

        base_url = result.get("base_url") or result.get("url")
        api_key = result.get("api_key") or result.get("key")
        if isinstance(base_url, str) and isinstance(api_key, str):
            os.environ[DREADNODE_LLM_BASE_ENV] = base_url
            os.environ[DREADNODE_LLM_API_KEY_ENV] = api_key

        self._state.litellm_key_expires_at = self.parse_expires_at(
            result.get("expires_at") or result.get("expiresAt")
        )
        return result

    async def search_model_browser_models(
        self,
        query: str | None,
        *,
        filters: dict[str, t.Any] | None = None,
        api: ApiClient | None = None,
    ) -> list[dict[str, t.Any]]:
        """Fetch featured or searched BYOK models for the `/models` browser."""
        if api is None and not self._context.is_authenticated():
            return []
        if api is None:
            try:
                api, _profile = self._context.platform_client()
            except Exception:
                logger.debug("Cannot fetch browser models: no platform client available")
                return []

        normalized_query = query.strip() if isinstance(query, str) else None
        normalized_filters = {
            key: value
            for key, value in (filters or {}).items()
            if value is not None and value != []
        }
        featured = not normalized_query and not normalized_filters
        limit = MODEL_BROWSER_FEATURED_LIMIT if featured else MODEL_BROWSER_SEARCH_LIMIT

        try:
            payload = await asyncio.to_thread(
                self.fetch_catalog_models,
                api,
                query=normalized_query or None,
                limit=limit,
                provider=t.cast("str | None", normalized_filters.get("provider")),
                capabilities=t.cast("list[str] | None", normalized_filters.get("capabilities")),
                open_weights=t.cast("bool | None", normalized_filters.get("open_weights")),
                min_context=t.cast("int | None", normalized_filters.get("min_context")),
                max_context=t.cast("int | None", normalized_filters.get("max_context")),
                min_price=t.cast("float | None", normalized_filters.get("min_price")),
                max_price=t.cast("float | None", normalized_filters.get("max_price")),
                featured=featured,
            )
        except Exception as exc:
            logger.debug("Failed to fetch browser models: {}", exc)
            return []

        return self.extract_catalog_models(payload)

    async def ensure_litellm_key_fresh(self, *, now: datetime | None = None) -> None:
        if not self._context.is_authenticated():
            return
        if not self._state.platform_models:
            return
        current_time = now or datetime.now(UTC)
        expires_at = self._state.litellm_key_expires_at
        if expires_at is None:
            await self.provision_litellm_key()
            return
        if expires_at <= current_time + LITELLM_REFRESH_WINDOW:
            await self.provision_litellm_key()
