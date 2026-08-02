"""Raw AWS Secrets Manager read/write.

Both ``read`` and ``write`` default to the caller's own per-user secret
``iam/<username>/private`` — a secret that exists by convention and is
readable/writable only by that IAM user. Pass ``--secret-id`` to target any
other secret. ``read-user`` reads the caller's themed per-user secret
``iam/<username>(/<env>)/<theme>``.

Usage:
    # Read a key from your private secret (or list all keys)
    pysae-ai-tools secrets read [<key>]

    # Read from another secret
    pysae-ai-tools secrets read --secret-id <secret-id> [<key>]

    # Write key=value pairs to your private secret
    pysae-ai-tools secrets write <key1>=<value1> [key2=$ENV_VAR] ...

    # Read the caller's themed per-user secret
    pysae-ai-tools secrets read-user <theme> [<key>] [--env <env>]

Values prefixed with $ are resolved from environment variables.
"""

import json
import os
import subprocess
import sys
from typing import Annotated

import typer

from ..common.paths import temp_path
from ..env import secret_store

app = typer.Typer(help="Read or write raw AWS Secrets Manager secrets (no environment notion)")

PRIVATE_THEME = "private"

SecretIdOption = Annotated[
    str | None,
    typer.Option(
        "--secret-id",
        "-s",
        help="AWS Secrets Manager secret ID. Default: your private secret iam/<username>/private.",
    ),
]


def _resolve_secret_id(secret_id: str | None) -> str:
    """Return ``secret_id`` if given, else the caller's private secret id."""
    if secret_id:
        return secret_id
    try:
        return secret_store.user_secret_id(PRIVATE_THEME)
    except secret_store.SecretError as e:
        print(f"FAILED: {e}", file=sys.stderr)
        raise typer.Exit(code=1) from None


def _read_and_print(secret_id: str, key: str | None, show_value: bool) -> None:
    """Fetch ``secret_id`` and print a key (or list all), masked unless show_value."""
    try:
        secrets = secret_store.fetch_secret(secret_id)
    except secret_store.SecretError as e:
        print(f"FAILED: {e}", file=sys.stderr)
        raise typer.Exit(code=1) from None

    if key:
        if key not in secrets:
            print(f"FAILED: key '{key}' not found in {secret_id}", file=sys.stderr)
            print(f"Available keys: {', '.join(sorted(secrets))}", file=sys.stderr)
            raise typer.Exit(code=1)
        if show_value:
            print(secrets[key])
        else:
            value = secrets[key]
            masked = value[:4] + "****" + value[-4:] if len(value) > 12 else "****"
            print(f"{key}={masked}")
    else:
        for k in sorted(secrets):
            if show_value:
                print(f"{k}={secrets[k]}")
            else:
                v = secrets[k]
                masked = v[:4] + "****" + v[-4:] if len(v) > 12 else "****"
                print(f"{k}={masked}")


@app.command()
def read(
    key: Annotated[str | None, typer.Argument(help="Key to read (omit to list all keys)")] = None,
    secret_id: SecretIdOption = None,
    show_value: Annotated[
        bool,
        typer.Option("--show-value", help="Print the actual value (default: masked)"),
    ] = False,
) -> None:
    """Read a key (or list all keys) from an AWS secret (default: your private secret)."""
    _read_and_print(_resolve_secret_id(secret_id), key, show_value)


@app.command(name="read-user")
def read_user(
    theme: Annotated[str, typer.Argument(help="Secret theme: datadog, atlas, mongo, argocd…")],
    key: Annotated[str | None, typer.Argument(help="Key to read (omit to list all keys)")] = None,
    env: Annotated[
        str | None,
        typer.Option("--env", help="Environment for per-env secrets (e.g. dev, prod). Omit for env-agnostic."),
    ] = None,
    show_value: Annotated[
        bool,
        typer.Option("--show-value", help="Print the actual value (default: masked)"),
    ] = False,
) -> None:
    """Read a key from the caller's own per-user secret iam/<username>(/<env>)/<theme>.

    The username comes from ``aws sts get-caller-identity``; the secret is
    readable only by that IAM user (see the infra-common self-read policy).
    """
    from ..env.aws import current_aws_username

    username = current_aws_username()
    if not username:
        print(
            "FAILED: could not determine the AWS username (`aws sts get-caller-identity` — check your credentials)",
            file=sys.stderr,
        )
        raise typer.Exit(code=1)
    secret_id = f"iam/{username}/{env}/{theme}" if env else f"iam/{username}/{theme}"
    _read_and_print(secret_id, key, show_value)


@app.command()
def write(
    pairs: Annotated[list[str], typer.Argument(help="key=value (or key=$ENV_VAR) pairs")],
    secret_id: SecretIdOption = None,
) -> None:
    """Update keys in an AWS secret (default: your private secret)."""
    if not pairs:
        print("FAILED: at least one key=value pair is required", file=sys.stderr)
        raise typer.Exit(code=1)

    resolved_id = _resolve_secret_id(secret_id)

    updates: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            print(f"FAILED: invalid pair '{pair}', expected key=value", file=sys.stderr)
            raise typer.Exit(code=1)
        key, value = pair.split("=", 1)
        if value.startswith("$"):
            env_var = value[1:]
            resolved = os.environ.get(env_var, "")
            if not resolved:
                print(f"FAILED: env var {env_var} is not set or empty", file=sys.stderr)
                raise typer.Exit(code=1)
            updates[key] = resolved
        else:
            updates[key] = value

    try:
        secrets = secret_store.fetch_secret(resolved_id)
    except secret_store.SecretError as e:
        print(f"FAILED: {e}", file=sys.stderr)
        raise typer.Exit(code=1) from None
    secrets.update(updates)

    tmp = str(temp_path("aws_secret_payload.json"))
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump(secrets, f)

        subprocess.run(
            [
                "aws",
                "secretsmanager",
                "update-secret",
                "--secret-id",
                resolved_id,
                "--secret-string",
                f"file://{tmp}",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        print("OK")
    except FileNotFoundError:
        print("FAILED: aws CLI not found — install it with `pysae-ai-tools tools install aws`", file=sys.stderr)
        raise typer.Exit(code=1) from None
    except subprocess.CalledProcessError as e:
        detail = (e.stderr or "").strip().splitlines()
        last = detail[-1] if detail else f"exit code {e.returncode}"
        print(f"FAILED: aws cli error — {last}", file=sys.stderr)
        raise typer.Exit(code=1) from None
    finally:
        try:
            os.remove(tmp)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    app()
