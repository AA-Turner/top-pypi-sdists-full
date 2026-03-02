"""Setup & onboarding API — first run, setup wizard, onboarding flow."""

from salmalm.security.crypto import vault, log
import json
import os
from salmalm.constants import DATA_DIR, VAULT_FILE, TEST_MODELS
from salmalm.core import audit_log


def _ensure_vault_unlocked(vault) -> bool:
    """Ensure vault is unlocked (auto-create or unlock with empty password). Returns True if unlocked."""
    try:
        from salmalm.security.crypto import VAULT_FILE

        if not VAULT_FILE.exists():
            vault.create("", save_to_keychain=False)
        else:
            vault.unlock("")
    except Exception as e:
        log.debug(f"Suppressed: {e}")
    return vault.is_unlocked


class WebSetupMixin:
    GET_ROUTES = {
        "/api/onboarding": "_get_api_onboarding",
        "/setup": "_get_setup",
    }
    POST_ROUTES = {
        "/api/setup": "_post_api_setup",
        "/api/onboarding": "_post_api_onboarding",
        "/api/onboarding/preferences": "_post_api_onboarding_preferences",
    }

    """Mixin providing setup route handlers."""

    def _needs_onboarding(self) -> bool:
        """Check if first-run onboarding is needed (no API keys or Ollama configured)."""
        if not vault.is_unlocked:
            return False
        providers = [
            "anthropic_api_key",
            "openai_api_key",
            "xai_api_key",
            "google_api_key",
            "openrouter_api_key",
        ]
        has_api_key = any(vault.get(k) for k in providers)
        has_ollama = bool(vault.get("ollama_url"))
        return not (has_api_key or has_ollama)

    def _needs_first_run(self) -> bool:
        """True if vault file doesn't exist and no env password — brand new install."""
        if VAULT_FILE.exists():  # noqa: F405
            return False
        if os.environ.get("SALMALM_VAULT_PW", ""):
            return False
        # If .vault_auto exists, auto-create vault with that password
        try:
            _pw_hint_file = VAULT_FILE.parent / ".vault_auto"  # noqa: F405
            if _pw_hint_file.exists():
                _hint = _pw_hint_file.read_text(encoding="utf-8").strip()
                if _hint:
                    import base64
                    try:
                        _auto_pw = base64.b64decode(_hint).decode()
                    except Exception:
                        _auto_pw = _hint
                else:
                    _auto_pw = ""
                vault.create(_auto_pw)
                vault.unlock(_auto_pw, save_to_keychain=True)
                log.info("[SETUP] Vault auto-created from .vault_auto")
                return False
        except Exception as e:
            log.debug(f"vault_auto create failed: {e}")
        return True

    # ── Extracted GET handlers ────────────────────────────────

    def _get_setup(self):
        # Allow re-running the setup wizard anytime
        """Get setup."""
        from salmalm.web import templates as _tmpl

        self._html(_tmpl.ONBOARDING_HTML)

# ── FastAPI router ────────────────────────────────────────────────────────────
import asyncio as _asyncio
from fastapi import APIRouter as _APIRouter, Request as _Request, Depends as _Depends, Query as _Query
from fastapi.responses import JSONResponse as _JSON, Response as _Response, HTMLResponse as _HTML, StreamingResponse as _SR, RedirectResponse as _RR
from salmalm.web.fastapi_deps import require_auth as _auth, optional_auth as _optauth

router = _APIRouter()

@router.get("/api/onboarding")
async def get_onboarding():
    from salmalm.security.crypto import vault
    from salmalm.web.routes.web_setup import WebSetupMixin
    _result = {}
    class _H(WebSetupMixin):
        def _json(self, data, status=200): _result["d"] = data
    h = _H.__new__(_H)
    import types
    h._json = types.MethodType(_H._json, h)
    h._get_api_onboarding()
    return _JSON(content=_result.get("d", {}))

@router.get("/setup")
async def get_setup():
    from salmalm.web import templates as _tmpl
    return _HTML(content=_tmpl.ONBOARDING_HTML)

@router.post("/api/setup")
async def post_setup(request: _Request):
    import os, base64
    from salmalm.security.crypto import vault, log
    from salmalm.constants import VAULT_FILE
    from salmalm.core import audit_log
    body = await request.json()
    if VAULT_FILE.exists():
        return _JSON(content={"error": "Already set up"}, status_code=400)
    use_pw = body.get("use_password", False)
    pw = body.get("password", "")
    if use_pw and len(pw) < 4:
        return _JSON(content={"error": "Password must be at least 4 characters"}, status_code=400)
    if use_pw and len(pw) > 1024:
        return _JSON(content={"error": "Password too long (max 1024 characters)"}, status_code=400)
    try:
        _vault_pw = pw if use_pw else ""
        vault.create(_vault_pw)
        vault.unlock(_vault_pw, save_to_keychain=True)
        try:
            _pw_hint_file = VAULT_FILE.parent / ".vault_auto"
            if not use_pw:
                _pw_hint_file.write_text("", encoding="utf-8")
            else:
                _pw_hint_file.write_text(base64.b64encode(_vault_pw.encode()).decode(), encoding="utf-8")
            _pw_hint_file.chmod(0o600)
        except Exception as e:
            log.debug(f"Suppressed: {e}")
        audit_log("setup", f"vault created {'with' if use_pw else 'without'} password")
    except RuntimeError:
        log.warning("[SETUP] Vault unavailable (no cryptography). Proceeding without encryption.")
        audit_log("setup", "vault skipped — no cryptography package")
        vault._data = {}
        vault._password = ""
        vault._salt = b"\x00" * 16
        try:
            VAULT_FILE.parent.mkdir(parents=True, exist_ok=True)
            VAULT_FILE.write_bytes(b'{"no_crypto": true}')
        except Exception:
            pass
    return _JSON(content={"ok": True})

@router.post("/api/onboarding")
async def post_onboarding(request: _Request, _u=_Depends(_optauth)):
    import os as _os_onb
    import asyncio as _aio_onb
    # On external bind: reject unauthenticated onboarding API key writes
    _bind_onb = _os_onb.environ.get("SALMALM_BIND", "127.0.0.1")
    if _bind_onb not in ("127.0.0.1", "localhost", "::1") and not _u:
        return _JSON(content={"error": "Authentication required"}, status_code=401)
    from salmalm.web.routes.web_setup import WebSetupMixin, _ensure_vault_unlocked
    from salmalm.security.crypto import vault, log
    body = await request.json()
    _result = {}
    class _H(WebSetupMixin):
        @property
        def _body(self): return body
        def _json(self, data, status=200): _result["d"] = (data, status)
    h = _H.__new__(_H)
    import types
    h._json = types.MethodType(_H._json, h)
    h._body = body
    # Run in thread: _post_api_onboarding_inner() makes blocking HTTP calls (key tests)
    await _aio_onb.to_thread(h._post_api_onboarding_inner)
    data, status = _result.get("d", ({}, 200))
    return _JSON(content=data, status_code=status)

@router.post("/api/onboarding/preferences")
async def post_onboarding_preferences(request: _Request, _u=_Depends(_optauth)):
    import os
    from salmalm.security.crypto import vault, log
    from salmalm.constants import DATA_DIR
    from salmalm.core import audit_log
    # Require vault to be unlocked (= local session or authenticated user)
    if not vault.is_unlocked:
        return _JSON(content={"error": "Vault locked — unlock vault first"}, status_code=403)
    # On external bind: require authentication (no anonymous preference writes)
    _bind = os.environ.get("SALMALM_BIND", "127.0.0.1")
    _is_local_bind = _bind in ("127.0.0.1", "localhost", "::1")
    if not _is_local_bind and not _u:
        return _JSON(content={"error": "Authentication required"}, status_code=401)
    body = await request.json()
    model = body.get("model", "auto")
    persona = body.get("persona", "expert")
    if model and model != "auto":
        vault.set("default_model", model)
        try:
            from salmalm.core.core import router as _router
            _router.set_force_model(model)
        except Exception as e:
            log.warning(f"[SETUP] Failed to set router model: {e}")
    persona_templates = {
        "expert": "# SOUL.md\n\nYou are a professional AI expert. Be precise, detail-oriented, and thorough.",
        "friend": "# SOUL.md\n\nYou are a friendly and warm conversational partner. Be casual and engaging.",
        "assistant": "# SOUL.md\n\nYou are an efficient personal assistant. Be concise and task-focused.",
    }
    template = persona_templates.get(persona, persona_templates["expert"])
    try:
        soul_path = os.path.join(str(DATA_DIR), "SOUL.md")
        os.makedirs(os.path.dirname(soul_path), exist_ok=True)
        with open(soul_path, "w", encoding="utf-8") as f:
            f.write(template)
    except Exception as e:
        log.debug(f"Suppressed: {e}")
    audit_log("onboarding", f"preferences: model={model}, persona={persona}")
    return _JSON(content={"ok": True})
