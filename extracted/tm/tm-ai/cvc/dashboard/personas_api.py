"""Personas layer — composer-bar persona switcher backend.

Personas live as YAML files under ``~/.cvc/personas/{id}.yaml``. Each file
declares a system prompt, a default model+provider, and a list of skill ids.

The dashboard composer-bar uses these endpoints to:

* enumerate available personas (`GET /api/personas`)
* fetch full detail incl. system prompt + skills (`GET /api/personas/{id}`)
* fetch just the skills list (`GET /api/personas/{id}/skills`)
* read & write the active persona for the current workspace
  (`GET /api/personas/active`, `POST /api/personas/active`)

Active persona is persisted under the workspace's settings file
(``<workspace>/.cvc/settings.local.json``) under key ``active_persona``.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

PERSONAS_DIR = Path.home() / ".cvc" / "personas"

# ── Seed personas (used to bootstrap an empty ~/.cvc/personas/ dir) ──
_SEED_PERSONAS: List[Dict[str, Any]] = [
    {
        "id": "default",
        "name": "Default",
        "description": "General-purpose CVC assistant — balanced, helpful, conservative.",
        "default_model": "claude-opus-4.7",
        "default_provider": "copilot",
        "system_prompt": (
            "You are CVC, a focused AI coding assistant. Be concise, accurate, and "
            "prefer using tools to verify before answering. Respect workspace boundaries.\n"
        ),
        "skills": ["read_file", "search_files", "patch", "terminal"],
    },
]
# NOTE: Only the "default" persona is seeded. Additional personas are
# created by the user via POST /api/personas — never auto-seeded.
# Historical team-named seeds (ajay/jha/robin/samantha/tina) were
# removed 2026-05-11; existing user YAMLs in ~/.cvc/personas/ continue
# to load normally via _all_personas().
_LEGACY_SEEDS_REMOVED: List[Dict[str, Any]] = [
    {
        "id": "_legacy_ajay",
        "name": "Ajay",
        "description": "Pragmatic principal engineer — ships fast, optimises later.",
        "default_model": "claude-opus-4.7",
        "default_provider": "copilot",
        "system_prompt": (
            "You are Ajay, a pragmatic principal engineer. Bias toward shipping "
            "working code over perfect code. Prefer small diffs. Explain trade-offs briefly.\n"
        ),
        "skills": ["read_file", "search_files", "patch", "terminal", "cvc_commit"],
    },
    {
        "id": "jha",
        "name": "Jha",
        "description": "Systems architect — long-horizon design, careful refactors.",
        "default_model": "claude-opus-4.7",
        "default_provider": "copilot",
        "system_prompt": (
            "You are Jha, a systems architect. Think before you type. Diagram in "
            "text when useful. Prefer interfaces and contracts over implementations.\n"
        ),
        "skills": ["read_file", "search_files", "patch", "cvc_recall", "cvc_commit"],
    },
    {
        "id": "robin",
        "name": "Robin",
        "description": "Business & scalability CTO — deployment, infra, growth.",
        "default_model": "claude-opus-4.7",
        "default_provider": "copilot",
        "system_prompt": (
            "You are Robin, a business-minded CTO. Always weigh cost, latency, "
            "and scale. Push back on premature complexity. Recommend boring tech.\n"
        ),
        "skills": ["read_file", "search_files", "terminal", "cvc_status"],
    },
    {
        "id": "samantha",
        "name": "Samantha",
        "description": "AI researcher & scientist — rigorous, curious, citation-driven.",
        "default_model": "claude-opus-4.7",
        "default_provider": "copilot",
        "system_prompt": (
            "You are Samantha, an AI researcher. Cite sources. State assumptions. "
            "Quantify when possible. Distinguish what is known from what is guessed.\n"
        ),
        "skills": ["read_file", "search_files", "cvc_recall", "cvc_smart_search"],
    },
    {
        "id": "tina",
        "name": "Tina",
        "description": "Main developer — fast hands-on coding, tests, small commits.",
        "default_model": "claude-opus-4.7",
        "default_provider": "copilot",
        "system_prompt": (
            "You are Tina, the main developer. Write code, run tests, commit often. "
            "Prefer the smallest change that works. Always verify with tests.\n"
        ),
        "skills": [
            "read_file", "search_files", "patch", "terminal",
            "cvc_commit", "cvc_status",
        ],
    },
]


# ── Pydantic models ─────────────────────────────────────────────────────

class PersonaSummary(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    default_model: str
    default_provider: str
    skills_count: int
    system_prompt_path: Optional[str] = None


class PersonaDetail(PersonaSummary):
    system_prompt: str
    skills: List[str]


class PersonaActive(BaseModel):
    workspace_id: str
    persona_id: str


class PersonaCreate(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    default_model: str = "claude-opus-4.7"
    default_provider: str = "copilot"
    system_prompt: str = ""
    skills: List[str] = []


class PersonaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    default_model: Optional[str] = None
    default_provider: Optional[str] = None
    system_prompt: Optional[str] = None
    skills: Optional[List[str]] = None


# ── YAML helpers ────────────────────────────────────────────────────────


def _ensure_seeded() -> None:
    """Create ``~/.cvc/personas/`` and seed starter YAMLs if missing."""
    try:
        PERSONAS_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not create personas dir %s: %s", PERSONAS_DIR, exc)
        return
    for spec in _SEED_PERSONAS:
        path = PERSONAS_DIR / f"{spec['id']}.yaml"
        if path.exists():
            continue
        try:
            import yaml  # type: ignore
            path.write_text(yaml.safe_dump(spec, sort_keys=False), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not seed persona %s: %s", spec["id"], exc)


def _load_yaml(path: Path) -> Optional[Dict[str, Any]]:
    try:
        import yaml  # type: ignore
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text) or {}
        if not isinstance(data, dict):
            return None
        return data
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to load persona %s: %s", path, exc)
        return None


def _persona_from_yaml(path: Path) -> Optional[Dict[str, Any]]:
    data = _load_yaml(path)
    if data is None:
        return None
    pid = data.get("id") or path.stem
    skills = data.get("skills") or []
    if not isinstance(skills, list):
        skills = []
    return {
        "id": pid,
        "name": data.get("name") or pid.title(),
        "description": data.get("description"),
        "default_model": data.get("default_model", "claude-opus-4.7"),
        "default_provider": data.get("default_provider", "copilot"),
        "system_prompt": data.get("system_prompt", ""),
        "skills": [str(s) for s in skills],
        "system_prompt_path": str(path),
    }


def _all_personas() -> List[Dict[str, Any]]:
    _ensure_seeded()
    out: List[Dict[str, Any]] = []
    if not PERSONAS_DIR.exists():
        return out
    for path in sorted(PERSONAS_DIR.glob("*.yaml")):
        p = _persona_from_yaml(path)
        if p:
            out.append(p)
    return out


def _get_persona(persona_id: str) -> Optional[Dict[str, Any]]:
    path = PERSONAS_DIR / f"{persona_id}.yaml"
    if not path.exists():
        return None
    return _persona_from_yaml(path)


def _summary(p: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": p["id"],
        "name": p["name"],
        "description": p.get("description"),
        "default_model": p["default_model"],
        "default_provider": p["default_provider"],
        "skills_count": len(p.get("skills") or []),
        "system_prompt_path": p.get("system_prompt_path"),
    }


# ── Active persona persistence (per workspace settings) ─────────────────


def _settings_path(workspace_path: Path) -> Path:
    return workspace_path / ".cvc" / "settings.local.json"


def get_active_persona_id(workspace_path: Path, default: str = "default") -> str:
    """Read active persona id from workspace settings.local.json."""
    import json
    path = _settings_path(workspace_path)
    if not path.exists():
        return default
    try:
        data = json.loads(path.read_text(encoding="utf-8") or "{}")
        return str(data.get("active_persona") or default)
    except Exception:  # noqa: BLE001
        return default


def set_active_persona_id(workspace_path: Path, persona_id: str) -> None:
    """Write active persona id into workspace settings.local.json (merge)."""
    import json
    path = _settings_path(workspace_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data: Dict[str, Any] = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8") or "{}") or {}
        except Exception:  # noqa: BLE001
            data = {}
    data["active_persona"] = persona_id
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _current_workspace_path() -> Path:
    """Resolve the current workspace path via cvc.gateway state."""
    from cvc import gateway as gw  # type: ignore
    if gw._workspace_mgr and gw._workspace_mgr.current:
        return Path(gw._workspace_mgr.current.path)
    if gw._project_root:
        return Path(gw._project_root)
    return Path.cwd()


def _workspace_id_for(path: Path) -> str:
    import hashlib
    return hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:12]


# ── Route registration ──────────────────────────────────────────────────


def register_personas_routes(app: FastAPI) -> None:
    """Mount /api/personas routes."""

    @app.get("/api/personas")
    async def get_personas() -> Dict[str, Any]:
        personas = [_summary(p) for p in _all_personas()]
        return {"personas": personas, "total": len(personas)}

    @app.get("/api/personas/active")
    async def get_active_persona() -> Dict[str, Any]:
        ws_path = _current_workspace_path()
        pid = get_active_persona_id(ws_path)
        # Validate; fall back to "default" if id unknown
        if _get_persona(pid) is None:
            pid = "default"
        return {
            "workspace_id": _workspace_id_for(ws_path),
            "persona_id": pid,
        }

    @app.post("/api/personas/active")
    async def post_active_persona(body: PersonaActive) -> Dict[str, Any]:
        if _get_persona(body.persona_id) is None:
            raise HTTPException(404, f"Persona not found: {body.persona_id}")
        ws_path = _current_workspace_path()
        # workspace_id is informational; we always write to the *active* workspace
        set_active_persona_id(ws_path, body.persona_id)
        return {
            "workspace_id": _workspace_id_for(ws_path),
            "persona_id": body.persona_id,
        }

    @app.get("/api/personas/{persona_id}")
    async def get_persona(persona_id: str) -> Dict[str, Any]:
        p = _get_persona(persona_id)
        if p is None:
            raise HTTPException(404, f"Persona not found: {persona_id}")
        out = _summary(p)
        out["system_prompt"] = p.get("system_prompt", "")
        out["skills"] = p.get("skills") or []
        return out

    @app.get("/api/personas/{persona_id}/skills")
    async def get_persona_skills(persona_id: str) -> Dict[str, Any]:
        p = _get_persona(persona_id)
        if p is None:
            raise HTTPException(404, f"Persona not found: {persona_id}")
        skills = p.get("skills") or []
        return {"persona_id": persona_id, "skills": skills, "count": len(skills)}

    @app.post("/api/personas")
    async def create_persona(body: PersonaCreate) -> Dict[str, Any]:
        import re
        import yaml  # type: ignore
        pid = re.sub(r"[^a-z0-9_-]+", "-", body.id.strip().lower()).strip("-")
        if not pid:
            raise HTTPException(400, "Invalid persona id")
        path = PERSONAS_DIR / f"{pid}.yaml"
        if path.exists():
            raise HTTPException(409, f"Persona already exists: {pid}")
        PERSONAS_DIR.mkdir(parents=True, exist_ok=True)
        spec = {
            "id": pid,
            "name": body.name,
            "description": body.description,
            "default_model": body.default_model,
            "default_provider": body.default_provider,
            "system_prompt": body.system_prompt,
            "skills": [str(s) for s in body.skills],
        }
        path.write_text(yaml.safe_dump(spec, sort_keys=False), encoding="utf-8")
        p = _get_persona(pid)
        if p is None:
            raise HTTPException(500, "Persona write succeeded but reload failed")
        out = _summary(p)
        out["system_prompt"] = p.get("system_prompt", "")
        out["skills"] = p.get("skills") or []
        return out

    @app.put("/api/personas/{persona_id}")
    async def update_persona(persona_id: str, body: PersonaUpdate) -> Dict[str, Any]:
        import yaml  # type: ignore
        path = PERSONAS_DIR / f"{persona_id}.yaml"
        if not path.exists():
            raise HTTPException(404, f"Persona not found: {persona_id}")
        data = _load_yaml(path) or {}
        upd = body.model_dump(exclude_unset=True)
        if "skills" in upd and upd["skills"] is not None:
            upd["skills"] = [str(s) for s in upd["skills"]]
        data.update(upd)
        data["id"] = persona_id
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        p = _get_persona(persona_id)
        if p is None:
            raise HTTPException(500, "Persona update succeeded but reload failed")
        out = _summary(p)
        out["system_prompt"] = p.get("system_prompt", "")
        out["skills"] = p.get("skills") or []
        return out

    @app.delete("/api/personas/{persona_id}")
    async def delete_persona(persona_id: str) -> Dict[str, Any]:
        if persona_id == "default":
            raise HTTPException(400, "Cannot delete the default persona")
        path = PERSONAS_DIR / f"{persona_id}.yaml"
        if not path.exists():
            raise HTTPException(404, f"Persona not found: {persona_id}")
        path.unlink()
        return {"deleted": persona_id}
