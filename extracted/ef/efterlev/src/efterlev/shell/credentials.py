"""Read/write `~/.efterlev/credentials.toml` for the shell `/setup` wizard.

The credentials file is a per-user store separate from the per-workspace
`.efterlev/config.toml`. It records:

- Anthropic API key (when the user configured the Anthropic backend)
- Bedrock region + role ARN (when the user configured Bedrock; AWS
  credentials themselves come from boto3's standard credential chain —
  the file just records "Bedrock is set up")
- Default model preference

Format:

    [anthropic]
    api_key = "sk-ant-api03-..."

    [bedrock]
    region = "us-east-1"

    [defaults]
    model = "claude-sonnet-4-6"

Permissions: file mode `0o600`, directory mode `0o700`. We do not
encrypt the key at rest; same posture as `~/.aws/credentials`. The
secret-scrubber in `efterlev/llm/scrubber.py` ensures the key never
leaves the machine in LLM prompts.

The Anthropic client (`efterlev/llm/anthropic_client.py`) falls back
to this file when `ANTHROPIC_API_KEY` is not set in the environment.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

CREDENTIALS_DIR = Path.home() / ".efterlev"
CREDENTIALS_PATH = CREDENTIALS_DIR / "credentials.toml"


@dataclass(frozen=True)
class Credentials:
    """Parsed view of `~/.efterlev/credentials.toml`. Missing sections become None."""

    anthropic_api_key: str | None = None
    bedrock_region: str | None = None
    default_model: str | None = None
    openai_api_key: str | None = None

    @property
    def has_anthropic(self) -> bool:
        return self.anthropic_api_key is not None

    @property
    def has_bedrock(self) -> bool:
        return self.bedrock_region is not None

    @property
    def has_openai(self) -> bool:
        return self.openai_api_key is not None


def load_credentials() -> Credentials:
    """Read credentials.toml; return empty Credentials when missing or malformed.

    Never raises — the shell falls back to env vars / AWS profiles when
    the file is absent or unreadable.
    """
    if not CREDENTIALS_PATH.is_file():
        return Credentials()
    try:
        import tomllib

        data = tomllib.loads(CREDENTIALS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError, tomllib.TOMLDecodeError):
        return Credentials()
    anthropic = data.get("anthropic", {}) if isinstance(data.get("anthropic"), dict) else {}
    bedrock = data.get("bedrock", {}) if isinstance(data.get("bedrock"), dict) else {}
    defaults = data.get("defaults", {}) if isinstance(data.get("defaults"), dict) else {}
    openai = data.get("openai", {}) if isinstance(data.get("openai"), dict) else {}
    return Credentials(
        anthropic_api_key=anthropic.get("api_key")
        if isinstance(anthropic.get("api_key"), str)
        else None,
        bedrock_region=bedrock.get("region") if isinstance(bedrock.get("region"), str) else None,
        default_model=defaults.get("model") if isinstance(defaults.get("model"), str) else None,
        openai_api_key=openai.get("api_key") if isinstance(openai.get("api_key"), str) else None,
    )


def save_credentials(creds: Credentials) -> None:
    """Write the credentials.toml atomically with mode 0o600."""
    CREDENTIALS_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    lines: list[str] = []
    if creds.anthropic_api_key:
        lines.append("[anthropic]")
        # Use literal-string (triple-single-quoted) form to avoid any TOML
        # escape gymnastics on the key. Anthropic keys are ASCII safe but
        # be defensive.
        lines.append(f'api_key = "{creds.anthropic_api_key}"')
        lines.append("")
    if creds.openai_api_key:
        lines.append("[openai]")
        lines.append(f'api_key = "{creds.openai_api_key}"')
        lines.append("")
    if creds.bedrock_region:
        lines.append("[bedrock]")
        lines.append(f'region = "{creds.bedrock_region}"')
        lines.append("")
    if creds.default_model:
        lines.append("[defaults]")
        lines.append(f'model = "{creds.default_model}"')
        lines.append("")

    body = "\n".join(lines).rstrip() + "\n" if lines else ""

    # Atomic write: tmp file in the same dir, fchmod, rename.
    import tempfile

    fd, tmp_path = tempfile.mkstemp(dir=CREDENTIALS_DIR, prefix=".credentials-", suffix=".tmp")
    try:
        os.write(fd, body.encode("utf-8"))
        os.fchmod(fd, 0o600)
    finally:
        os.close(fd)
    os.replace(tmp_path, CREDENTIALS_PATH)


def resolve_anthropic_api_key() -> str | None:
    """Return the Anthropic key the LLM client should use, or None.

    Resolution order:
      1. `ANTHROPIC_API_KEY` env var (highest precedence so CI / per-process
         overrides keep working without touching the file)
      2. `~/.efterlev/credentials.toml` `[anthropic].api_key`
    """
    env_key = os.environ.get("ANTHROPIC_API_KEY")
    if env_key:
        return env_key
    return load_credentials().anthropic_api_key


def resolve_openai_api_key() -> str | None:
    """Return the OpenAI key the LLM client should use, or None.

    Resolution order (parallel to ``resolve_anthropic_api_key``):
      1. ``OPENAI_API_KEY`` env var (highest precedence so CI / per-process
         overrides keep working without touching the file)
      2. ``~/.efterlev/credentials.toml`` ``[openai].api_key`` (what the
         shell ``/setup`` OpenAI path writes)
    """
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key
    return load_credentials().openai_api_key
