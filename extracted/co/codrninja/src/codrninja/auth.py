"""OAuth helpers, PKCE flow, callback server, and encrypted token storage."""

from __future__ import annotations

import base64
import json
import os
import secrets
import stat
import threading
import time
import webbrowser
from dataclasses import dataclass
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import parse_qs, urlparse

import requests
from cryptography.fernet import Fernet, InvalidToken


AUTH_DIR = Path.home() / ".codrninja"
AUTH_FILE = AUTH_DIR / "auth.json"
KEY_FILE = AUTH_DIR / ".auth.key"
DEFAULT_CALLBACK_HOST = "127.0.0.1"
DEFAULT_CALLBACK_PORT = 8765
DEFAULT_CALLBACK_PATH = "/callback"
DEFAULT_TIMEOUT_SECONDS = 300


@dataclass
class OAuthCallbackResult:
    code: Optional[str] = None
    state: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None


class PKCEHandler:
    """Generates PKCE verifier/challenge pairs."""

    @staticmethod
    def generate_verifier() -> str:
        return secrets.token_urlsafe(48)

    @staticmethod
    def generate_challenge(verifier: str) -> str:
        digest = sha256(verifier.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")

    @staticmethod
    def generate_state() -> str:
        return secrets.token_urlsafe(24)


class TokenManager:
    """Stores provider OAuth tokens encrypted with Fernet."""

    def __init__(self, auth_file: Path = AUTH_FILE, key_file: Path = KEY_FILE):
        self.auth_file = Path(auth_file)
        self.key_file = Path(key_file)
        self.auth_file.parent.mkdir(parents=True, exist_ok=True)
        self._fernet = Fernet(self._load_or_create_key())
        self._chmod_private(self.auth_file.parent)

    def _load_or_create_key(self) -> bytes:
        if self.key_file.exists():
            key = self.key_file.read_bytes().strip()
        else:
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            self._chmod_private(self.key_file)
        return key

    def _chmod_private(self, path: Path):
        try:
            if path.is_dir():
                path.chmod(stat.S_IRWXU)
            else:
                path.chmod(stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass

    def _read_store(self) -> Dict[str, Any]:
        if not self.auth_file.exists():
            return {}
        try:
            encrypted = self.auth_file.read_bytes()
            if not encrypted:
                return {}
            data = self._fernet.decrypt(encrypted)
            return json.loads(data.decode("utf-8"))
        except (OSError, json.JSONDecodeError, InvalidToken):
            return {}

    def _write_store(self, data: Dict[str, Any]):
        payload = json.dumps(data, indent=2).encode("utf-8")
        encrypted = self._fernet.encrypt(payload)
        self.auth_file.write_bytes(encrypted)
        self._chmod_private(self.auth_file)

    def store_tokens(self, provider: str, tokens: Dict[str, Any]):
        data = self._read_store()
        data[provider] = tokens
        self._write_store(data)

    def get_tokens(self, provider: str) -> Optional[Dict[str, Any]]:
        return self._read_store().get(provider)

    def revoke(self, provider: str) -> bool:
        data = self._read_store()
        if provider not in data:
            return False
        del data[provider]
        self._write_store(data)
        return True

    def list_status(self) -> Dict[str, Any]:
        data = self._read_store()
        result: Dict[str, Any] = {}
        for provider, tokens in data.items():
            result[provider] = {
                "authenticated": True,
                "expires_at": tokens.get("expires_at"),
                "scope": tokens.get("scope"),
                "expired": self.is_token_expired(tokens),
                "token_type": tokens.get("token_type", "Bearer"),
                "metadata": tokens.get("metadata", {}),
            }
        return result

    def is_token_expired(self, tokens: Dict[str, Any], buffer_minutes: int = 5) -> bool:
        expires_at = tokens.get("expires_at")
        if not expires_at:
            return False
        try:
            return float(expires_at) <= (time.time() + buffer_minutes * 60)
        except (TypeError, ValueError):
            return True


class OAuthCallbackServer:
    """Local callback server for OAuth redirects."""

    def __init__(self, host: str = DEFAULT_CALLBACK_HOST, port: int = DEFAULT_CALLBACK_PORT, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS, callback_path: str = DEFAULT_CALLBACK_PATH):
        self.host = host
        self.port = port
        self.timeout_seconds = timeout_seconds
        self.callback_path = callback_path if callback_path.startswith("/") else "/" + callback_path
        self._result = OAuthCallbackResult()
        self._event = threading.Event()
        self._server: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    @property
    def callback_url(self) -> str:
        return f"http://{self.host}:{self.port}{self.callback_path}"

    @property
    def result(self) -> OAuthCallbackResult:
        return self._result

    def inject_callback(self, code: Optional[str] = None, state: Optional[str] = None, error: Optional[str] = None):
        self._result = OAuthCallbackResult(code=code, state=state, error=error)
        self._event.set()

    def start(self) -> str:
        server_self = self

        _callback_path = self.callback_path

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urlparse(self.path)
                if parsed.path != _callback_path:
                    self.send_response(404)
                    self.end_headers()
                    return
                query = parse_qs(parsed.query)
                server_self._result = OAuthCallbackResult(
                    code=(query.get("code") or [None])[0],
                    state=(query.get("state") or [None])[0],
                    error=(query.get("error") or [None])[0],
                    error_description=(query.get("error_description") or [None])[0],
                )
                message = "Authentication complete. You can close this window."
                if server_self._result.error:
                    message = f"Authentication failed: {server_self._result.error}"
                body = message.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                server_self._event.set()
                threading.Thread(target=server_self.shutdown, daemon=True).start()

            def log_message(self, format, *args):
                return

        for candidate_port in (self.port, self.port + 1, self.port + 2):
            try:
                self._server = HTTPServer((self.host, candidate_port), Handler)
                self.port = candidate_port
                break
            except OSError:
                continue
        if not self._server:
            raise OSError("No available callback port (tried 8765-8767)")

        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self.callback_url

    def wait_for_callback(self) -> OAuthCallbackResult:
        self._event.wait(timeout=self.timeout_seconds)
        if not self._event.is_set() and not self._result.error:
            self._result.error = "timeout"
            self._result.error_description = "Timed out waiting for OAuth callback"
        return self._result

    def shutdown(self):
        if self._server:
            try:
                self._server.shutdown()
                self._server.server_close()
            except OSError:
                pass
            self._server = None


class OAuthFlow:
    """Runs browser-based OAuth for a configured provider."""

    def __init__(self, provider_name: str, provider=None, token_manager: Optional[TokenManager] = None, callback_port: int = DEFAULT_CALLBACK_PORT, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS):
        self.provider_name = provider_name
        if provider is None:
            from .oauth_providers import get_oauth_provider
            provider = get_oauth_provider(provider_name)
        self.provider = provider
        self.token_manager = token_manager or TokenManager()
        self.callback_port = callback_port
        self.timeout_seconds = timeout_seconds

    def run(self, open_browser: bool = True) -> Tuple[bool, str]:
        callback_server = OAuthCallbackServer(port=self.callback_port, timeout_seconds=self.timeout_seconds)
        callback_url = callback_server.start()
        verifier = PKCEHandler.generate_verifier()
        challenge = PKCEHandler.generate_challenge(verifier)
        state = PKCEHandler.generate_state()

        auth_url = self.provider.build_authorization_url(
            redirect_uri=callback_url,
            code_challenge=challenge,
            state=state,
        )

        opened = False
        if open_browser:
            try:
                opened = webbrowser.open(auth_url)
            except Exception:
                opened = False

        result = callback_server.wait_for_callback()
        callback_server.shutdown()

        if result.error:
            if not opened:
                return False, f"Open this URL manually: {auth_url}\nOAuth error: {result.error}"
            return False, result.error_description or result.error
        if not result.code:
            return False, f"No authorization code received. Open this URL manually: {auth_url}"
        if result.state != state:
            return False, "OAuth state mismatch"

        tokens = self.provider.exchange_code(result.code, verifier, callback_url)
        self.token_manager.store_tokens(self.provider_name, tokens)
        manual_url = "" if opened else f" Opened failed; auth URL: {auth_url}"
        return True, f"Authenticated with {self.provider_name}.{manual_url}"

    def refresh(self, refresh_token: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.provider.refresh_access_token(refresh_token, metadata=metadata or {})
