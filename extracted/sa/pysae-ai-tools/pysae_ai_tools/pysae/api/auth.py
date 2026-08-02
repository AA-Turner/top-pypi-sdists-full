"""``pysae-ai-tools pysae api auth`` — manage Auth0 login for the Pysae API.

Commands:
    login      Interactive (browser PKCE) or device-code login; stores tokens.
    status     Show whether the local session is valid and when it expires.
    logout     Forget stored tokens for an environment.
    configure  Persist the Auth0 client id resolved at ``terraform apply`` time.
    oauth-config  Print the environment's public Auth0/OAuth2 settings as JSON.
"""

import json
import os
import sys
import urllib.parse
from typing import Annotated

import typer

from .common import oauth, tokens
from .common.config import OAUTH_SCOPE, get_env, resolve_client_id, set_client_id

app = typer.Typer(help="Authenticate against the Pysae API via Auth0.", no_args_is_help=True)

_ENV_OPT = typer.Option("--env", help="Target environment.")


def _err(msg: str) -> None:
    print(msg, file=sys.stderr)


@app.command()
def login(
    env: Annotated[str, _ENV_OPT] = "dev",
    client_id: Annotated[str | None, typer.Option("--client-id", help="Override the Auth0 client id.")] = None,
    device: Annotated[
        bool,
        typer.Option("--device", help="Use the device-code flow (no local browser; for headless/SSH)."),
    ] = False,
    timeout: Annotated[int, typer.Option("--timeout", help="Seconds to wait for the browser redirect.")] = 300,
) -> None:
    """Log in to ``env`` and store the resulting tokens locally."""
    auth0 = get_env(env)
    try:
        cid = resolve_client_id(auth0, client_id)
    except RuntimeError as e:
        _err(f"FAILED: {e}")
        raise typer.Exit(1) from None

    in_ci = bool(os.environ.get("CI"))
    use_device = device or in_ci

    try:
        if use_device:
            code = oauth.start_device_code(auth0, cid)
            target = code.verification_uri_complete or code.verification_uri
            _err(
                f"\nTo authorize, open:\n  {target}\n"
                f"and confirm this code: {code.user_code}\n\nWaiting for authorization..."
            )
            token_set = oauth.poll_device_code(auth0, cid, code)
        else:
            token_set = oauth.login_authorization_code(
                auth0,
                cid,
                timeout=timeout,
                on_url=lambda url: _err(f"Opening the Auth0 login page in your browser...\nIf it does not open: {url}"),
            )
    except oauth.OAuthError as e:
        _err(f"FAILED: {e}")
        raise typer.Exit(1) from None

    tokens.save(env, token_set)
    mins = token_set.seconds_remaining() // 60
    _err(f"OK: logged in to '{env}' — access token valid ~{mins} min, refresh token stored.")


@app.command()
def status(env: Annotated[str, _ENV_OPT] = "dev") -> None:
    """Report the local session state for ``env``."""
    get_env(env)  # validate name
    token_set = tokens.load(env)
    if token_set is None:
        print(f"{env}: not logged in")
        raise typer.Exit(1)
    remaining = token_set.seconds_remaining()
    state = "valid" if remaining > 0 else "expired"
    can_refresh = "yes" if token_set.refresh_token else "no"
    print(f"{env}: {state} (access token expires in {remaining}s, refreshable: {can_refresh})")


@app.command()
def logout(
    env: Annotated[
        str | None,
        typer.Option("--env", help="Environment to forget (omit with --all to clear everything)."),
    ] = "dev",
    all_envs: Annotated[bool, typer.Option("--all", help="Forget tokens for all environments.")] = False,
) -> None:
    """Forget stored tokens."""
    if all_envs:
        tokens.clear(None)
        print("OK: cleared all stored Pysae API tokens.")
        return
    if env is None:
        _err("FAILED: pass --env <name> or --all")
        raise typer.Exit(1)
    get_env(env)
    tokens.clear(env)
    print(f"OK: forgot tokens for '{env}'.")


@app.command()
def configure(
    client_id: Annotated[str, typer.Option("--client-id", help="Auth0 client id for this environment.")],
    env: Annotated[str, _ENV_OPT] = "dev",
) -> None:
    """Persist the Auth0 ``pysae-ai-tools`` client id for ``env``."""
    get_env(env)
    set_client_id(env, client_id)
    print(f"OK: stored Auth0 client id for '{env}'.")


@app.command("oauth-config")
def oauth_config(env: Annotated[str, _ENV_OPT] = "dev") -> None:
    """Print the environment's public Auth0/OAuth2 settings as JSON.

    Public values only (domain, audience, endpoints, PKCE client id) — no
    secret. Consumed by ``/openapi-to-postman`` to pre-fill the OAuth2 auth of a
    Postman environment against the Pysae API.
    """
    auth0 = get_env(env)
    payload = {
        "env": auth0.name,
        "api_base": auth0.api_base,
        "auth0_domain": auth0.auth0_domain,
        "audience": auth0.audience,
        "authorize_endpoint": auth0.authorize_endpoint,
        # Ready-to-use Postman "Auth URL": Auth0 needs `audience` on /authorize
        # to mint an API-scoped JWT (Postman adds client_id/scope/PKCE itself).
        "authorize_url": auth0.authorize_endpoint + "?" + urllib.parse.urlencode({"audience": auth0.audience}),
        "token_endpoint": auth0.token_endpoint,
        "client_id": resolve_client_id(auth0, None),
        "scope": OAUTH_SCOPE,
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    app()
