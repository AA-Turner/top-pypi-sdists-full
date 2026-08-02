"""Helpers around the standard AWS CLI config files (default profile).

Reads and writes ``~/.aws/credentials`` and ``~/.aws/config`` directly
(``configparser``-format files), so the helpers work whether the ``aws``
binary is installed or not. The ``AWS_SHARED_CREDENTIALS_FILE`` and
``AWS_CONFIG_FILE`` env vars are honoured to match the AWS SDK
convention.

The interactive prompt has two paths:
- ``aws`` is on PATH → delegate to ``aws configure`` (full 4-prompt UX).
- ``aws`` is missing → manual prompt for access key + secret, written
  directly to ``~/.aws/credentials``. Region is pre-seeded to
  :data:`DEFAULT_REGION` in both paths.

This module deliberately does **not** manage AWS profiles: every command
runs against the user's default profile (whatever ``aws configure`` would
pick when invoked without ``--profile``). If callers need profile
isolation, they set ``AWS_PROFILE`` themselves before invoking us.
"""

import configparser
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import typer

DEFAULT_REGION = "eu-west-3"
"""Pysae uses Paris (eu-west-3) — pre-seeded into ~/.aws/config when missing."""


def aws_cli_available() -> bool:
    """True when the ``aws`` binary is on PATH."""
    return shutil.which("aws") is not None


def _credentials_path() -> Path:
    """``~/.aws/credentials`` (or whatever ``AWS_SHARED_CREDENTIALS_FILE`` says)."""
    custom = os.environ.get("AWS_SHARED_CREDENTIALS_FILE")
    if custom:
        return Path(custom).expanduser()
    return Path.home() / ".aws" / "credentials"


def _config_path() -> Path:
    """``~/.aws/config`` (or whatever ``AWS_CONFIG_FILE`` says)."""
    custom = os.environ.get("AWS_CONFIG_FILE")
    if custom:
        return Path(custom).expanduser()
    return Path.home() / ".aws" / "config"


# Map field names to their canonical home: credentials file vs. config file.
_KEY_FILE: dict[str, str] = {
    "aws_access_key_id": "credentials",
    "aws_secret_access_key": "credentials",
    "aws_session_token": "credentials",
    "region": "config",
    "output": "config",
}


def _path_for_key(key: str) -> Path | None:
    location = _KEY_FILE.get(key)
    if location == "credentials":
        return _credentials_path()
    if location == "config":
        return _config_path()
    return None


def _read_parser(path: Path) -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    if path.exists():
        parser.read(path)
    return parser


def _write_parser(path: Path, parser: configparser.ConfigParser) -> None:
    """Atomically write ``parser`` to ``path`` with 0600 perms."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        parser.write(f)


def aws_configure_get(key: str) -> str | None:
    """Read ``key`` from the ``[default]`` section of the relevant AWS file.

    Returns the value or None when the file / section / key is missing.
    Works without the ``aws`` binary — reads ``~/.aws/credentials`` and
    ``~/.aws/config`` directly.
    """
    path = _path_for_key(key)
    if path is None or not path.exists():
        return None
    parser = _read_parser(path)
    if "default" not in parser:
        return None
    value = parser["default"].get(key, "").strip()
    return value or None


def aws_configure_set(key: str, value: str) -> bool:
    """Persist ``key=value`` to the ``[default]`` section of the relevant AWS file."""
    path = _path_for_key(key)
    if path is None:
        return False
    parser = _read_parser(path)
    if "default" not in parser:
        parser["default"] = {}
    parser["default"][key] = value
    _write_parser(path, parser)
    return True


# Per-process memo: avoid re-prompting for the credentials pair when the
# user has already declined or already filled it once during this run.
# Cleared at process exit; not persisted across invocations.
_credentials_prompt_outcome: str = ""  # "" | "declined" | "completed"


def prompt_aws_credentials() -> bool:
    """Prompt for the access key + secret pair and persist them.

    Two paths:
    - When ``aws`` is on PATH, delegate to ``aws configure`` so the user
      sees the canonical 4-prompt flow (access key, secret, region,
      output format). The region is pre-seeded to :data:`DEFAULT_REGION`.
    - Otherwise, prompt manually for access key + secret and write them
      to ``~/.aws/credentials`` directly. The region is also written to
      ``~/.aws/config`` so the AWS SDK / CLI (once installed) finds it.

    Returns True when both keys end up populated, False when the user
    cancels (empty input) or persistence fails. Memoised per process.
    """
    global _credentials_prompt_outcome
    if _credentials_prompt_outcome == "completed":
        return True
    if _credentials_prompt_outcome == "declined":
        return False

    # Pre-seed the region so it shows as the default in either flow.
    if not aws_configure_get("region"):
        aws_configure_set("region", DEFAULT_REGION)

    if aws_cli_available():
        ok = _prompt_via_aws_configure()
    else:
        ok = _prompt_manually()
    _credentials_prompt_outcome = "completed" if ok else "declined"
    return ok


def _prompt_via_aws_configure() -> bool:
    """Delegate to ``aws configure`` — the standard 4-prompt AWS flow."""
    typer.echo("", err=True)
    typer.secho("  ┌─ Configuration AWS CLI ────────────────────────────────────", fg=typer.colors.CYAN, err=True)
    typer.secho("  │ Création de la clé d'accès :", fg=typer.colors.CYAN, err=True)
    typer.secho(
        "  │   AWS Console → IAM → Users → <toi> → Security credentials",
        fg=typer.colors.BRIGHT_BLACK,
        err=True,
    )
    typer.secho(
        "  │   → Access keys → Create access key → Command Line Interface (CLI)",
        fg=typer.colors.BRIGHT_BLACK,
        err=True,
    )
    typer.secho("  │", fg=typer.colors.CYAN, err=True)
    typer.secho("  │ Réponses aux 4 prompts qui suivent :", fg=typer.colors.CYAN, err=True)
    typer.secho(
        "  │   • AWS Access Key ID       → colle la clé créée (commence par AKIA…)",
        fg=typer.colors.BRIGHT_BLACK,
        err=True,
    )
    typer.secho(
        "  │   • AWS Secret Access Key   → colle le secret (saisie masquée)",
        fg=typer.colors.BRIGHT_BLACK,
        err=True,
    )
    typer.secho(
        f"  │   • Default region name     → Entrée pour garder « {DEFAULT_REGION} » (Paris)",
        fg=typer.colors.BRIGHT_BLACK,
        err=True,
    )
    typer.secho(
        "  │   • Default output format   → Entrée (json par défaut, ou tape `yaml`/`text`)",
        fg=typer.colors.BRIGHT_BLACK,
        err=True,
    )
    typer.secho("  │", fg=typer.colors.CYAN, err=True)
    typer.secho(
        "  │ Ctrl-C pour annuler. Les valeurs sont écrites dans ~/.aws/.",
        fg=typer.colors.BRIGHT_BLACK,
        err=True,
    )
    typer.secho("  └────────────────────────────────────────────────────────────", fg=typer.colors.CYAN, err=True)
    typer.echo("", err=True)

    try:
        r = subprocess.run(["aws", "configure"])
    except (OSError, KeyboardInterrupt):
        return False
    if r.returncode != 0:
        return False

    # ``aws configure`` keeps existing values when the user just hits Enter,
    # so an empty profile after a clean exit means the user actually skipped.
    return bool(aws_configure_get("aws_access_key_id") and aws_configure_get("aws_secret_access_key"))


def _prompt_manually() -> bool:
    """Manual fallback when ``aws`` CLI is not on PATH.

    Writes directly to ``~/.aws/credentials`` so the AWS CLI / SDK finds
    them once installed.
    """
    typer.echo("", err=True)
    typer.secho(
        "  ┌─ Configuration AWS — saisie manuelle (aws CLI absent) ─────",
        fg=typer.colors.CYAN,
        err=True,
    )
    typer.secho("  │ Création de la clé d'accès :", fg=typer.colors.CYAN, err=True)
    typer.secho(
        "  │   AWS Console → IAM → Users → <toi> → Security credentials",
        fg=typer.colors.BRIGHT_BLACK,
        err=True,
    )
    typer.secho(
        "  │   → Access keys → Create access key → Command Line Interface (CLI)",
        fg=typer.colors.BRIGHT_BLACK,
        err=True,
    )
    typer.secho("  │", fg=typer.colors.CYAN, err=True)
    typer.secho(
        f"  │ Région pré-remplie : {DEFAULT_REGION} (Paris). Output par défaut : json.",
        fg=typer.colors.BRIGHT_BLACK,
        err=True,
    )
    typer.secho(
        "  │ Les valeurs sont écrites dans ~/.aws/credentials et ~/.aws/config.",
        fg=typer.colors.BRIGHT_BLACK,
        err=True,
    )
    typer.secho(
        "  │ Laisse vide pour annuler.",
        fg=typer.colors.BRIGHT_BLACK,
        err=True,
    )
    typer.secho(
        "  └────────────────────────────────────────────────────────────",
        fg=typer.colors.CYAN,
        err=True,
    )
    typer.echo("", err=True)

    access_key_raw: str = typer.prompt("  AWS Access Key ID", default="", show_default=False)
    access_key = access_key_raw.strip()
    if not access_key:
        return False
    secret_raw: str = typer.prompt(
        "  AWS Secret Access Key",
        default="",
        show_default=False,
        hide_input=True,
    )
    secret = secret_raw.strip()
    if not secret:
        return False

    if not aws_configure_set("aws_access_key_id", access_key):
        typer.secho("  ✗ écriture dans ~/.aws/credentials a échoué", fg=typer.colors.RED, err=True)
        return False
    if not aws_configure_set("aws_secret_access_key", secret):
        typer.secho("  ✗ écriture dans ~/.aws/credentials a échoué", fg=typer.colors.RED, err=True)
        return False
    typer.secho("  ✓ Identifiants écrits dans ~/.aws/credentials [default]", fg=typer.colors.GREEN, err=True)
    return True


def stdin_is_tty() -> bool:
    """True when stdin is interactive — required for typer.prompt to work."""
    try:
        return sys.stdin.isatty()
    except (AttributeError, ValueError):
        return False


_username_resolved = False
_username_cache: str | None = None


def _username_cache_key() -> str:
    """Cache key for the resolved username, scoped to the active access key.

    Reading the access-key id is cheap (env var, or ``~/.aws/credentials`` —
    no subprocess), so changing credentials naturally invalidates the cached
    username. Falls back to a constant key when no access-key id is available
    (e.g. session-token / SSO creds)."""
    akid = os.environ.get("AWS_ACCESS_KEY_ID") or aws_configure_get("aws_access_key_id") or ""
    return f"__aws_username__:{akid}" if akid else "__aws_username__"


def current_aws_username() -> str | None:
    """Return the IAM username of the caller (``aws sts get-caller-identity``).

    Parses the user ARN (``arn:aws:iam::<acct>:user/<name>``) and returns
    ``<name>`` (last path segment), which matches the ``${aws:username}`` IAM
    variable and the per-user secret namespace ``iam/<name>/…``. Returns None
    when ``aws`` is missing, the call fails, or the caller is not an IAM user
    (e.g. an assumed role).

    Memoised per process, and cached on disk (``env-cache.json``, keyed by the
    access-key id) so the many separate ``secrets read-user`` subprocesses
    spawned by ``env resolve`` don't each pay an STS round-trip.
    """
    global _username_resolved, _username_cache
    if _username_resolved:
        return _username_cache

    from . import cache

    cache_key = _username_cache_key()
    if cached := cache.read(cache_key):
        _username_resolved = True
        _username_cache = cached
        return cached

    from ..common import winpath

    winpath.refresh_process_path_from_registry(force=True)
    try:
        result = subprocess.run(
            ["aws", "sts", "get-caller-identity", "--query", "Arn", "--output", "text"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        # Transient (e.g. aws not installed *yet* during a long `install all`
        # run): do NOT memoise, so a later call retries once aws is on PATH.
        return None
    if result.returncode != 0:
        return None
    # STS answered: memoise this definitive result (even a None for a non-user
    # identity) to avoid re-querying within the process.
    arn = (result.stdout or "").strip()
    m = re.search(r":user/(.+)$", arn)
    _username_resolved = True
    _username_cache = m.group(1).split("/")[-1] if m else None
    if _username_cache:
        cache.write(cache_key, _username_cache)
    return _username_cache
