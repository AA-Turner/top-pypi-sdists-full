"""OAuth provider definitions for codrninja."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from urllib.parse import urlencode, quote

import requests


@dataclass
class OAuthProviderBase:
    name: str
    auth_url: str
    token_url: str
    client_id: str
    scopes: list[str] = field(default_factory=list)
    experimental: bool = False
    extra_auth_params: Dict[str, Any] = field(default_factory=dict)
    extra_token_params: Dict[str, Any] = field(default_factory=dict)

    def build_authorization_url(self, redirect_uri: str, code_challenge: str, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "state": state,
        }
        params.update(self.extra_auth_params)
        return f"{self.auth_url}?{urlencode(params, quote_via=quote)}"

    def exchange_code(self, code: str, verifier: str, redirect_uri: str) -> Dict[str, Any]:
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": verifier,
        }
        payload.update(self.extra_token_params)
        response = requests.post(self.token_url, data=payload, timeout=30)
        response.raise_for_status()
        return self.normalize_tokens(response.json())

    def refresh_access_token(self, refresh_token: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": refresh_token,
        }
        payload.update(self.extra_token_params)
        response = requests.post(self.token_url, data=payload, timeout=30)
        response.raise_for_status()
        refreshed = self.normalize_tokens(response.json())
        if metadata:
            refreshed.setdefault("metadata", {}).update(metadata)
        return refreshed

    def normalize_tokens(self, data: Dict[str, Any]) -> Dict[str, Any]:
        expires_in = data.get("expires_in")
        expires_at = None
        if expires_in is not None:
            import time
            expires_at = time.time() + float(expires_in)
        return {
            "access_token": data.get("access_token"),
            "refresh_token": data.get("refresh_token"),
            "expires_at": expires_at,
            "scope": data.get("scope"),
            "token_type": data.get("token_type", "Bearer"),
            "metadata": {
                "experimental": self.experimental,
                "provider": self.name,
            },
        }


def _decode_jwt_payload(token: str) -> Dict[str, Any]:
    """Decode the payload section of a JWT without verification."""
    import base64, json as _json
    try:
        parts = token.split(".")
        if len(parts) >= 2:
            padded = parts[1] + "=" * (4 - len(parts[1]) % 4)
            return _json.loads(base64.urlsafe_b64decode(padded))
    except Exception:
        pass
    return {}


class OpenAIOAuth(OAuthProviderBase):
    CALLBACK_HOST = "localhost"
    CALLBACK_PORT = 1455
    CALLBACK_PATH = "/auth/callback"

    def __init__(self):
        super().__init__(
            name="openai",
            auth_url=os.environ.get(
                "CODRNINJA_OPENAI_AUTH_URL",
                "https://auth.openai.com/oauth/authorize",
            ),
            token_url=os.environ.get(
                "CODRNINJA_OPENAI_TOKEN_URL",
                "https://auth.openai.com/oauth/token",
            ),
            client_id=os.environ.get(
                "CODRNINJA_OPENAI_CLIENT_ID",
                "app_EMoamEEZ73f0CkXaXp7hrann",
            ),
            scopes=["openid", "profile", "email", "offline_access"],
            extra_auth_params={
                "codex_cli_simplified_flow": "true",
                "id_token_add_organizations": "true",
                "originator": "opencode",
            },
        )

    def normalize_tokens(self, data: Dict[str, Any]) -> Dict[str, Any]:
        tokens = super().normalize_tokens(data)
        # Extract account_id from id_token JWT (needed for ChatGPT-Account-Id header)
        id_token = data.get("id_token", "")
        if id_token:
            payload = _decode_jwt_payload(id_token)
            account_id = payload.get("account_id") or payload.get("sub") or ""
            if account_id:
                tokens["account_id"] = account_id
        return tokens


class AnthropicOAuth(OAuthProviderBase):
    def __init__(self):
        super().__init__(
            name="anthropic",
            auth_url=os.environ.get("CODRNINJA_ANTHROPIC_AUTH_URL", "https://anthropic.com/oauth/authorize"),
            token_url=os.environ.get("CODRNINJA_ANTHROPIC_TOKEN_URL", "https://anthropic.com/oauth/token"),
            client_id=os.environ.get("CODRNINJA_ANTHROPIC_CLIENT_ID", "codrninja"),
            scopes=["openid", "profile", "email", "offline_access"],
            experimental=True,
        )


def get_oauth_provider(name: str) -> OAuthProviderBase:
    normalized = name.lower()
    if normalized == "openai":
        return OpenAIOAuth()
    if normalized == "anthropic":
        return AnthropicOAuth()
    raise ValueError(f"Unsupported OAuth provider: {name}")
