"""Configuration management for codrninja."""

import json
import os
from dataclasses import dataclass, field
from typing import Literal, Optional, Dict, Any, List


@dataclass
class Config:
    """Configuration for codrninja."""
    
    # Provider settings — empty until user completes onboarding
    default_provider: str = field(default_factory=lambda: os.environ.get("CODRNINJA_PROVIDER", ""))
    default_model: str = field(default_factory=lambda: os.environ.get("CODRNINJA_MODEL", ""))
    
    # Ollama
    ollama_url: str = field(default_factory=lambda: os.environ.get("OLLAMA_URL", "http://localhost:11434"))
    ollama_configured: bool = False  # True only after user explicitly runs /providers/ollama/configure
    ollama_api_key: str = field(default_factory=lambda: os.environ.get("OLLAMA_API_KEY", ""))
    
    # OpenAI
    openai_api_key: str = field(default_factory=lambda: os.environ.get("OPENAI_API_KEY", ""))
    
    # Anthropic
    anthropic_api_key: str = field(default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY", ""))
    
    # OpenRouter
    openrouter_api_key: str = field(default_factory=lambda: os.environ.get("OPENROUTER_API_KEY", ""))
    
    # Reasoning level
    reasoning_level: Literal["none", "low", "medium", "high"] = field(
        default_factory=lambda: os.environ.get("CODRNINJA_REASONING_LEVEL", "medium")
    )
    
    # Database
    db_path: str = field(default_factory=lambda: os.path.expanduser("~/.codrninja/sessions.db"))

    # OAuth / TUI
    oauth_callback_port: int = field(default_factory=lambda: int(os.environ.get("CODRNINJA_OAUTH_CALLBACK_PORT", "8765")))
    oauth_timeout_seconds: int = field(default_factory=lambda: int(os.environ.get("CODRNINJA_OAUTH_TIMEOUT_SECONDS", "300")))
    oauth_auto_refresh: bool = field(default_factory=lambda: os.environ.get("CODRNINJA_OAUTH_AUTO_REFRESH", "true").lower() not in {"0", "false", "no"})
    oauth_refresh_buffer_minutes: int = field(default_factory=lambda: int(os.environ.get("CODRNINJA_OAUTH_REFRESH_BUFFER_MINUTES", "5")))
    tui_colors: Dict[str, str] = field(default_factory=lambda: {
        "user": "blue",
        "assistant": "green",
        "system": "grey50",
    })

    # Permissions
    permissions_mode: Literal["none", "ask", "auto", "strict", "relaxed", "custom"] = field(
        default_factory=lambda: os.environ.get("CODRNINJA_PERMISSIONS_MODE", "ask")
    )

    # Model preferences — maps provider → list of enabled model IDs (empty = all enabled)
    model_prefs: Dict[str, List[str]] = field(default_factory=dict)

    # Auto-LSP: run lsp_diagnostics after write_file/edit_file and inject errors into context
    auto_lsp_check: bool = field(default_factory=lambda: os.environ.get("CODRNINJA_AUTO_LSP", "true").lower() not in {"0", "false", "no"})

    # Web tools
    web_search: bool = field(default_factory=lambda: os.environ.get("CODRNINJA_WEB_SEARCH", "true").lower() not in {"0", "false", "no"})
    web_fetch: bool = field(default_factory=lambda: os.environ.get("CODRNINJA_WEB_FETCH", "true").lower() not in {"0", "false", "no"})
    
    # Prompt
    system_prompt: str = """You are an expert software engineer. You help write, review, and modify code.
When asked to create or modify files, respond with the file content in a code block.
Always specify the file path in the response.
Be concise and practical.
You can fetch web pages and search the internet for up-to-date information."""
    
    def get_provider_config(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """Get configuration for a specific provider."""
        p = provider or self.default_provider
        
        configs = {
            "ollama": {
                "url": self.ollama_url,
                "model": self.default_model,
                "reasoning_level": self.reasoning_level,
                "api_key": self.ollama_api_key,
            },
            "openai": {
                "api_key": self.openai_api_key,
                "model": self.default_model,
                "reasoning_level": self.reasoning_level
            },
            "anthropic": {
                "api_key": self.anthropic_api_key,
                "model": self.default_model,
                "reasoning_level": self.reasoning_level
            },
            "openrouter": {
                "api_key": self.openrouter_api_key,
                "model": self.default_model,
                "reasoning_level": self.reasoning_level
            },
            "claude-cli": {
                "model": self.default_model,
            },
        }

        return configs.get(p, configs["ollama"])
    
    def update_provider_config(self):
        """Sync provider manager with current config."""
        from .providers import ProviderManager
        self.provider_manager = ProviderManager({
            "provider": self.default_provider,
            "providers": {
                "ollama": self.get_provider_config("ollama"),
                "openai": self.get_provider_config("openai"),
                "anthropic": self.get_provider_config("anthropic"),
                "openrouter": self.get_provider_config("openrouter"),
                "claude-cli": self.get_provider_config("claude-cli"),
            }
        })
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables and config file."""
        config = cls()

        # Candidate paths in priority order: XDG standard, then legacy location.
        _candidates = [
            os.path.expanduser("~/.config/codrninja/config.json"),
            os.path.expanduser("~/.codrninja/config.json"),
        ]

        for config_file in _candidates:
            if not os.path.exists(config_file):
                continue
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)

                if data.get('provider'):
                    config.default_provider = data['provider']
                # Accept both "model" (canonical) and "default_model" (legacy key).
                model_val = data.get('model') or data.get('default_model')
                if model_val:
                    config.default_model = model_val
                if data.get('ollama_url'):
                    config.ollama_url = data['ollama_url']
                if data.get('ollama_configured'):
                    config.ollama_configured = bool(data['ollama_configured'])
                if data.get('ollama_api_key'):
                    config.ollama_api_key = data['ollama_api_key']
                if data.get('reasoning_level'):
                    config.reasoning_level = data['reasoning_level']
                if data.get('permissions_mode'):
                    config.permissions_mode = data['permissions_mode']
                api_keys = data.get('api_keys', {}) or {}
                if api_keys.get('openai'):
                    config.openai_api_key = api_keys['openai']
                if api_keys.get('anthropic'):
                    config.anthropic_api_key = api_keys['anthropic']
                if api_keys.get('openrouter'):
                    config.openrouter_api_key = api_keys['openrouter']
                oauth = data.get('oauth', {}) or {}
                if 'callback_port' in oauth:
                    config.oauth_callback_port = int(oauth['callback_port'])
                if 'callback_timeout_seconds' in oauth:
                    config.oauth_timeout_seconds = int(oauth['callback_timeout_seconds'])
                if 'auto_refresh' in oauth:
                    config.oauth_auto_refresh = bool(oauth['auto_refresh'])
                if 'refresh_buffer_minutes' in oauth:
                    config.oauth_refresh_buffer_minutes = int(oauth['refresh_buffer_minutes'])
                tui = data.get('tui', {}) or {}
                colors = tui.get('colors')
                if isinstance(colors, dict):
                    config.tui_colors.update(colors)
                if isinstance(data.get('model_prefs'), dict):
                    config.model_prefs = data['model_prefs']
                break  # Stop at first loadable file
            except Exception:
                pass  # Try next candidate

        return config

    def to_config_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            'provider': self.default_provider,
            'model': self.default_model,
            'ollama_url': self.ollama_url,
            'ollama_configured': self.ollama_configured,
            'ollama_api_key': self.ollama_api_key,
            'reasoning_level': self.reasoning_level,
            'permissions_mode': self.permissions_mode,
            'oauth': {
                'callback_port': self.oauth_callback_port,
                'callback_timeout_seconds': self.oauth_timeout_seconds,
                'auto_refresh': self.oauth_auto_refresh,
                'refresh_buffer_minutes': self.oauth_refresh_buffer_minutes,
            },
            'tui': {
                'colors': self.tui_colors,
            },
        }
        # Preserve API keys so save() never silently deletes them
        api_keys: Dict[str, str] = {}
        if self.openai_api_key:
            api_keys['openai'] = self.openai_api_key
        if self.anthropic_api_key:
            api_keys['anthropic'] = self.anthropic_api_key
        if self.openrouter_api_key:
            api_keys['openrouter'] = self.openrouter_api_key
        if api_keys:
            d['api_keys'] = api_keys
        if self.model_prefs:
            d['model_prefs'] = self.model_prefs
        return d

    def save(self, path: Optional[str] = None):
        config_file = os.path.expanduser(path or '~/.config/codrninja/config.json')
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(self.to_config_dict(), f, indent=2)
    
    def ensure_db_dir(self):
        """Ensure database directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
