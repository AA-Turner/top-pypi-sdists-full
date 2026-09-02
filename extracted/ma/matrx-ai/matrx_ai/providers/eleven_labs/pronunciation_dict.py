"""ElevenLabs pronunciation-dictionary REST wrapper + rule mapping.

A thin, SDK-version-proof client over the three pronunciation-dictionary
endpoints, plus the canonical mapping from our `DictionaryEntry` shape to
ElevenLabs rule objects and a stable hash for idempotent sync.

This module is pure provider plumbing — NO database, NO org/user context. The
host (aidream) owns rollup resolution, the publication ledger, and which
dictionary to publish; it calls these functions with already-resolved entries.

ElevenLabs rule model (official):
  alias:   {"string_to_replace": str, "type": "alias",   "alias": str}
  phoneme: {"string_to_replace": str, "type": "phoneme", "phoneme": str, "alphabet": "ipa"|"cmu-arpabet"}
Matching is case-sensitive, checked start→end, first match wins. Phoneme rules
only take effect on eleven_flash_v2 / eleven_monolingual_v1 (English); every
other model silently ignores them — never an error.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

import httpx

_BASE = "https://api.elevenlabs.io/v1/pronunciation-dictionaries"
_TIMEOUT = 60.0


def _api_key() -> str:
    from matrx_ai.providers.keys import resolve_api_key

    key = resolve_api_key("ELEVENLABS_API_KEY") or ""
    if not key:
        raise RuntimeError(
            "ELEVENLABS_API_KEY is not set — cannot publish pronunciation dictionaries."
        )
    return key


def _headers() -> dict[str, str]:
    return {"xi-api-key": _api_key(), "Content-Type": "application/json"}


# ── rule mapping ─────────────────────────────────────────────────────────────
def entries_to_rules(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Map resolved dictionary entries → ElevenLabs rule objects.

    For each entry: one alias rule per spoken form (`term` + each `sounds_like`)
    when `pronunciation` is set, and one phoneme rule from `ipa` when present.
    De-duplicates by `string_to_replace` (first wins — matches ElevenLabs'
    own first-match semantics). Deterministic order → stable hash.
    """
    rules: list[dict[str, Any]] = []
    seen: set[str] = set()

    def _add(rule: dict[str, Any]) -> None:
        s = rule["string_to_replace"].strip()
        if not s or s in seen:
            return
        seen.add(s)
        rule["string_to_replace"] = s
        rules.append(rule)

    for e in entries:
        say_as = (e.get("pronunciation") or "").strip()
        ipa = (e.get("ipa") or "").strip()
        forms = [e.get("term") or "", *(e.get("sounds_like") or [])]
        for form in forms:
            form = (form or "").strip()
            if not form:
                continue
            if say_as:
                _add({"string_to_replace": form, "type": "alias", "alias": say_as})
            elif ipa:
                _add(
                    {
                        "string_to_replace": form,
                        "type": "phoneme",
                        "phoneme": ipa,
                        "alphabet": "ipa",
                    }
                )
    # Sort by string_to_replace for a byte-stable canonical form.
    rules.sort(key=lambda r: r["string_to_replace"])
    return rules


def rule_strings(rules: list[dict[str, Any]]) -> list[str]:
    return [r["string_to_replace"] for r in rules]


def canonical_hash(rules: list[dict[str, Any]]) -> str:
    payload = json.dumps(rules, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ── REST calls ───────────────────────────────────────────────────────────────
async def create_from_rules(name: str, rules: list[dict[str, Any]]) -> dict[str, str]:
    async with httpx.AsyncClient(timeout=_TIMEOUT) as http:
        resp = await http.post(
            f"{_BASE}/add-from-rules",
            headers=_headers(),
            json={"name": name, "rules": rules},
        )
        resp.raise_for_status()
        data = resp.json()
    return {"id": data["id"], "version_id": data["version_id"]}


async def add_rules(dictionary_id: str, rules: list[dict[str, Any]]) -> dict[str, str]:
    async with httpx.AsyncClient(timeout=_TIMEOUT) as http:
        resp = await http.post(
            f"{_BASE}/{dictionary_id}/add-rules",
            headers=_headers(),
            json={"rules": rules},
        )
        resp.raise_for_status()
        data = resp.json()
    return {"id": data.get("id", dictionary_id), "version_id": data["version_id"]}


async def remove_rules(dictionary_id: str, strings: list[str]) -> dict[str, str]:
    async with httpx.AsyncClient(timeout=_TIMEOUT) as http:
        resp = await http.post(
            f"{_BASE}/{dictionary_id}/remove-rules",
            headers=_headers(),
            json={"rule_strings": strings},
        )
        resp.raise_for_status()
        data = resp.json()
    return {"id": data.get("id", dictionary_id), "version_id": data["version_id"]}
