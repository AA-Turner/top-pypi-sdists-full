"""Filesystem profile loader.

Canonical personal-AI state lives in structured rows and ledgers. The profile
root carries local prompt sources such as ``profile.json`` and ``AEGIS.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import quote

from packages.contracts.runtime import ProfileState
from .files import (
    AEGIS_FILENAME,
    PROFILE_BUNDLES_DIRNAME,
    PROFILE_MANIFEST_FILENAME,
    profile_bundle_has_content,
    profile_manifest_path,
    write_profile_manifest_file,
)
from .policy import (
    CompanionSettings,
    infer_personality_preset_id,
    is_companion_mode,
    normalize_profile_mode,
    resolve_personality_preset,
)


@dataclass(frozen=True, slots=True)
class LoadedProfile:
    state: ProfileState
    companion: CompanionSettings | None
    profile_dir: str
    manifest_path: str | None
    clone_text: str | None = None
    user_profile_text: str | None = None
    aegis_path: str | None = None
    user_profile_path: str | None = None
    manifest: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ProfileLoader:
    profile_dir: Path

    def load(
        self,
        *,
        profile_id: str | None = None,
        display_name: str | None = None,
        mode: str | None = None,
    ) -> LoadedProfile:
        bundle_dir = resolve_profile_bundle_dir(self.profile_dir, profile_id)
        manifest_path = profile_manifest_path(bundle_dir)
        manifest = self._load_manifest(manifest_path)
        resolved_profile_id = profile_id or str(manifest.get("profile_id") or bundle_dir.name)
        resolved_display_name = (
            display_name
            or str(manifest.get("display_name") or resolved_profile_id.replace("-", " ").title())
        )
        if mode is not None:
            resolved_mode = normalize_profile_mode(mode)
        elif manifest.get("mode") is not None:
            resolved_mode = normalize_profile_mode(str(manifest["mode"]))
        elif _contains_companion_settings(manifest):
            resolved_mode = "companion"
        else:
            resolved_mode = "default"
        preferences = self._normalize_sequence(manifest.get("preferences", ()))
        enabled_capabilities = self._normalize_sequence(
            manifest.get("enabled_capabilities", ())
        )
        companion_payload = _companion_payload_from_manifest(manifest)
        companion = self._load_companion_settings(companion_payload, resolved_mode)

        state = ProfileState(
            profile_id=resolved_profile_id,
            display_name=resolved_display_name,
            mode=resolved_mode,
            clone_path=None,
            preferences=preferences,
            enabled_capabilities=enabled_capabilities,
        )
        return LoadedProfile(
            state=state,
            companion=companion,
            profile_dir=str(bundle_dir),
            manifest_path=str(manifest_path) if manifest_path.exists() else None,
            aegis_path=str(profile_aegis_path(self.profile_dir)),
            manifest=dict(manifest),
        )

    def load_state(
        self,
        *,
        profile_id: str | None = None,
        display_name: str | None = None,
        mode: str | None = None,
    ) -> ProfileState:
        return self.load(
            profile_id=profile_id,
            display_name=display_name,
            mode=mode,
        ).state

    def _load_manifest(self, manifest_path: Path) -> dict[str, Any]:
        if not manifest_path.exists():
            return {}
        with manifest_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if not isinstance(payload, dict):
            raise ValueError(f"{manifest_path} must contain a JSON object")
        return payload

    def _normalize_sequence(self, value: Any) -> tuple[str, ...]:
        if value is None:
            return ()
        if isinstance(value, str):
            return (value,)
        if not isinstance(value, (list, tuple)):
            raise ValueError("profile manifest sequence values must be arrays or strings")
        return tuple(str(item) for item in value)

    def _load_companion_settings(self, value: Any, resolved_mode: str) -> CompanionSettings | None:
        if value is None and not is_companion_mode(resolved_mode):
            return None
        payload = value or {}
        if not isinstance(payload, dict):
            raise ValueError("companion manifest value must be a JSON object")
        raw_preset = str(payload.get("personality_preset") or "").strip() or None
        personality = self._normalize_sequence(payload.get("personality"))
        if personality:
            personality_preset = raw_preset or infer_personality_preset_id(personality, mode=resolved_mode)
        else:
            preset = resolve_personality_preset(raw_preset, mode=resolved_mode)
            personality_preset = preset.preset_id
            personality = preset.traits
        notes = self._normalize_sequence(payload.get("notes", ()))
        return CompanionSettings(
            text_first=bool(payload.get("text_first", True)),
            personality_preset=personality_preset,
            personality=personality,
            initiative=str(payload.get("initiative", "gentle")),
            preserve_relationship_timeline=bool(payload.get("preserve_relationship_timeline", True)),
            preserve_preferences=bool(payload.get("preserve_preferences", True)),
            preserve_corrections=bool(payload.get("preserve_corrections", True)),
            preserve_emotional_context=bool(payload.get("preserve_emotional_context", True)),
            allow_voice_extension=bool(payload.get("allow_voice_extension", False)),
            notes=notes,
        )


def companion_manifest_payload(companion: CompanionSettings | None) -> dict[str, Any] | None:
    if companion is None:
        return None
    return {
        "text_first": companion.text_first,
        "personality_preset": companion.personality_preset,
        "personality": list(companion.personality),
        "initiative": companion.initiative,
        "preserve_relationship_timeline": companion.preserve_relationship_timeline,
        "preserve_preferences": companion.preserve_preferences,
        "preserve_corrections": companion.preserve_corrections,
        "preserve_emotional_context": companion.preserve_emotional_context,
        "allow_voice_extension": companion.allow_voice_extension,
        "notes": list(companion.notes),
    }

def profile_manifest_payload(
    loaded_profile: LoadedProfile,
    *,
    existing_manifest: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    manifest = dict(existing_manifest or {})
    manifest["profile_id"] = loaded_profile.state.profile_id
    manifest["display_name"] = loaded_profile.state.display_name
    manifest["mode"] = normalize_profile_mode(loaded_profile.state.mode)
    manifest["preferences"] = list(loaded_profile.state.preferences)
    manifest["enabled_capabilities"] = list(loaded_profile.state.enabled_capabilities)
    companion_payload = companion_manifest_payload(loaded_profile.companion)
    if companion_payload is None:
        manifest.pop("companion", None)
    else:
        manifest["companion"] = companion_payload
    return manifest


def _contains_companion_settings(manifest: Mapping[str, Any]) -> bool:
    return manifest.get("companion") is not None


def _companion_payload_from_manifest(manifest: Mapping[str, Any]) -> Any:
    return manifest.get("companion")


def profile_bundle_dir(profile_root: Path, profile_id: str) -> Path:
    key = quote(profile_id, safe="")
    return profile_root / PROFILE_BUNDLES_DIRNAME / key


def resolve_profile_bundle_dir(profile_root: Path, profile_id: str | None) -> Path:
    if profile_id is None:
        return profile_root
    candidate = profile_bundle_dir(profile_root, profile_id)
    if profile_bundle_has_content(candidate):
        return candidate
    return profile_root


def write_profile_manifest(profile_dir: Path, manifest: Mapping[str, Any]) -> Path:
    return write_profile_manifest_file(profile_dir, manifest)


def profile_aegis_path(profile_root: Path) -> Path:
    return profile_root / AEGIS_FILENAME


def ensure_profile_aegis_file(profile_root: Path) -> Path:
    path = profile_aegis_path(profile_root)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(load_packaged_aegis_text().rstrip() + "\n", encoding="utf-8")
    return path


def packaged_aegis_path() -> Path:
    return Path(__file__).with_name(AEGIS_FILENAME)


def load_packaged_aegis_text() -> str:
    path = packaged_aegis_path()
    if not path.exists():
        raise FileNotFoundError(f"missing packaged AEGIS charter: {path}")
    return path.read_text(encoding="utf-8")
