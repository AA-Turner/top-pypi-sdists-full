"""``databaas`` console script: login, logout, whoami, token, profile, dag.

Kept to argparse and this package's existing dependencies (requests) —
``databaas-utils`` core does not otherwise carry a CLI framework, and adding
one just for this would ripple through every extra's dependency footprint.
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import replace
from typing import TYPE_CHECKING

from databaas_utils.errors import LakehouseError
from databaas_utils.profiles import (
    DEFAULT_REGION,
    DEFAULT_WAREHOUSE,
    Profile,
    default_profile_name,
    delete_profile,
    discover,
    endpoints_from_base_url,
    list_profiles,
    load_profile,
    save_profile,
)
from databaas_utils.tokenstore import MacKeychainStore
from databaas_utils.userauth import UserLogin

if TYPE_CHECKING:
    from databaas_utils.dags.config import DagsConfig
    from databaas_utils.dags.s3 import DagBucket

_REGISTER_TIMEOUT = 15
_OK_STATUSES = (200, 201, 409)


def main(argv: list[str] | None = None) -> int:
    """The ``databaas`` console script.

    Args:
        argv: Arguments to parse instead of ``sys.argv[1:]``.

    Returns:
        The process exit status: ``0`` on success, ``1`` on a handled error.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except LakehouseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="databaas",
        description="Log in to a Databaas lakehouse and deploy DAGs to it.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    login = sub.add_parser("login", help="log in interactively and cache the session")
    login.add_argument(
        "portal_url",
        nargs="?",
        help="the environment's base URL, e.g. https://next.dev.databaas.app; "
        "the auth. and catalog. addresses are derived from it",
    )
    login.add_argument("--profile", help="profile name to save (default: from the host)")
    login.add_argument("--device", action="store_true", help="use the device-code flow")
    login.add_argument("--issuer", help="Zitadel issuer (default: derived from the URL)")
    login.add_argument("--client-id")
    login.add_argument("--project-id")
    login.add_argument(
        "--catalog-url",
        help="Lakekeeper root URL, not the /catalog path (default: derived from the URL)",
    )
    login.add_argument("--warehouse", help=f"default: {DEFAULT_WAREHOUSE}")
    login.add_argument("--region")
    login.set_defaults(handler=_cmd_login)

    logout = sub.add_parser("logout", help="revoke and forget the cached login")
    logout.add_argument("--profile")
    logout.add_argument("--all", action="store_true", help="log out of every profile")
    logout.set_defaults(handler=_cmd_logout)

    whoami = sub.add_parser("whoami", help="show the signed-in identity")
    whoami.add_argument("--profile")
    whoami.set_defaults(handler=_cmd_whoami)

    token = sub.add_parser("token", help="print a fresh access token")
    token.add_argument("--profile")
    token.set_defaults(handler=_cmd_token)

    profile = sub.add_parser("profile", help="manage saved profiles")
    profile_sub = profile.add_subparsers(dest="profile_command", required=True)
    profile_sub.add_parser("list").set_defaults(handler=_cmd_profile_list)
    profile_use = profile_sub.add_parser("use")
    profile_use.add_argument("name")
    profile_use.set_defaults(handler=_cmd_profile_use)
    profile_delete = profile_sub.add_parser(
        "delete", help="log out and remove the profile from this machine"
    )
    profile_delete.add_argument("name")
    profile_delete.set_defaults(handler=_cmd_profile_delete)

    _add_dag_parser(sub)
    return parser


_LOGIN_FLAGS = ("--issuer", "--client-id", "--catalog-url")


def _cmd_login(args: argparse.Namespace) -> int:
    profile = _resolve_login_profile(args)
    if profile is None:
        return 1
    login = UserLogin.from_profile(profile, flow="device" if args.device else "auto")
    login.login()
    save_profile(profile, make_default=True)
    _register_with_lakekeeper(profile, login)
    claims = login.claims()
    identity = _email(login) or claims.get("sub") or "?"
    print(f"Signed in as {identity} — profile {profile.name!r} saved.")
    return 0


def _resolve_login_profile(args: argparse.Namespace) -> Profile | None:
    if args.portal_url:
        return _profile_from_base_url(args)
    given = {
        "--issuer": args.issuer,
        "--client-id": args.client_id,
        "--catalog-url": args.catalog_url,
    }
    missing = [flag for flag, value in given.items() if not value]
    if missing:
        print(
            "error: supply the environment's base URL with --client-id, or all "
            "of: " + ", ".join(_LOGIN_FLAGS),
            file=sys.stderr,
        )
        return None
    name = args.profile or args.issuer.split("//")[-1].split(".")[0]
    return Profile(
        name=name,
        issuer=args.issuer,
        client_id=args.client_id,
        project_id=args.project_id or "",
        catalog_url=args.catalog_url,
        warehouse=args.warehouse or DEFAULT_WAREHOUSE,
        region=args.region or DEFAULT_REGION,
    )


def _profile_from_base_url(args: argparse.Namespace) -> Profile | None:
    """Derive the profile from the base URL; ask the portal only without a client id."""
    import requests

    url = args.portal_url
    if args.client_id:
        issuer, catalog_url = endpoints_from_base_url(url)
        profile = Profile(
            name=args.profile or default_profile_name(url),
            issuer=issuer,
            client_id=args.client_id,
            project_id=args.project_id or "",
            catalog_url=catalog_url,
        )
    else:
        try:
            profile = discover(url, name=args.profile)
        except requests.RequestException:
            print(
                f"error: {url} serves no /.well-known/databaas-client.json; "
                "pass --client-id",
                file=sys.stderr,
            )
            return None
    overrides = {
        "issuer": args.issuer,
        "client_id": args.client_id,
        "project_id": args.project_id,
        "catalog_url": args.catalog_url,
        "warehouse": args.warehouse,
        "region": args.region,
    }
    return replace(profile, **{k: v for k, v in overrides.items() if v})


def _register_with_lakekeeper(profile: Profile, login: UserLogin) -> None:
    """Best-effort ``POST /management/v1/user`` so an admin has something to grant on.

    Zitadel's user-provisioned webhook (which is meant to do this ahead of
    time) is known broken on the current Zitadel version — see
    databaas-charts/docs/lakekeeper-design.md. Registering here fills that gap
    for whoever logs in this way, regardless of the webhook.
    """
    import requests

    url = f"{profile.catalog_url.rstrip('/')}/management/v1/user"
    try:
        response = requests.post(
            url,
            headers={"Authorization": login.auth_header()},
            json={"update-if-exists": True},
            timeout=_REGISTER_TIMEOUT,
        )
        if response.status_code not in _OK_STATUSES:
            print(
                f"warning: could not register with Lakekeeper "
                f"({response.status_code}): {response.text}",
                file=sys.stderr,
            )
    except requests.RequestException as exc:
        print(f"warning: could not register with Lakekeeper: {exc}", file=sys.stderr)


def _cmd_logout(args: argparse.Namespace) -> int:
    if args.all:
        for name, profile in list_profiles().items():
            UserLogin.from_profile(profile).logout()
            print(f"logged out of {name!r}")
        return 0
    profile = load_profile(args.profile)
    UserLogin.from_profile(profile).logout()
    print(f"logged out of {profile.name!r}")
    return 0


def _email(login: UserLogin) -> str | None:
    """The user's email for display, from userinfo; ``None`` if unavailable."""
    import requests

    try:
        email = login.userinfo().get("email")
    except (requests.RequestException, ValueError):
        return None
    return str(email) if email else None


def _cmd_whoami(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    login = UserLogin.from_profile(profile, interactive=False)
    claims = login.claims()
    sub = claims.get("sub", "?")
    print(f"profile:            {profile.name}")
    print(f"issuer:             {profile.issuer}")
    print(f"user:               {_email(login) or '?'} ({sub})")
    print(f"lakekeeper user id: oidc~{sub}")
    print(f"warehouse:          {profile.warehouse}")
    return 0


def _cmd_token(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    login = UserLogin.from_profile(profile, interactive=False)
    print(login.auth_header().removeprefix("Bearer "))
    return 0


def _cmd_profile_list(args: argparse.Namespace) -> int:
    profiles = list_profiles()
    if not profiles:
        print("no profiles saved — run `databaas login` first")
        return 0
    for name, profile in sorted(profiles.items()):
        print(f"{name}\t{profile.issuer}\t{profile.catalog_url}")
    return 0


def _cmd_profile_use(args: argparse.Namespace) -> int:
    profile = load_profile(args.name)
    save_profile(profile, make_default=True)
    print(f"default profile set to {profile.name!r}")
    return 0


def _cmd_profile_delete(args: argparse.Namespace) -> int:
    profile = load_profile(args.name)
    login = UserLogin.from_profile(profile)
    login.logout()
    was_default = delete_profile(profile.name)
    print(f"deleted profile {profile.name!r}")
    store = login.store
    if isinstance(store, MacKeychainStore) and store.has_legacy_entry(login.store_key):
        print(
            f"warning: an older login for {login.store_key!r} is still in the macOS "
            "Keychain and only the Python installation that saved it may remove it. "
            "Delete the 'databaas-utils' entry for it in Keychain Access.",
            file=sys.stderr,
        )
    remaining = list_profiles()
    if was_default and remaining:
        print(
            "no default profile now — pick one with "
            f"`databaas profile use NAME` ({', '.join(sorted(remaining))})"
        )
    return 0


def _add_dag_parser(sub: argparse._SubParsersAction) -> None:
    dag = sub.add_parser(
        "dag", help="validate and deploy Airflow DAG code from databaas.yml"
    )
    actions = dag.add_subparsers(dest="dag_command", required=True)
    for name, help_text, handler in (
        (
            "validate",
            "parse the target's DAGs with Airflow, as they would be deployed",
            _cmd_dag_validate,
        ),
        ("deploy", "upload artifacts.dags to the target's prefix", _cmd_dag_deploy),
        ("destroy", "delete everything under the target's prefix", _cmd_dag_destroy),
    ):
        action = actions.add_parser(name, help=help_text)
        action.add_argument("-t", "--target", help="target from databaas.yml")
        action.add_argument(
            "--dev-key", help="dev deploy name (default: the branch, as a slug)"
        )
        action.add_argument("--config", help="path to databaas.yml (default: search up)")
        action.set_defaults(handler=handler)
        if name == "validate":
            action.add_argument(
                "-v", "--verbose", action="store_true", help="show Airflow's output"
            )
            continue
        action.add_argument("--bucket", help="default: $DATABAAS_DAGS_BUCKET")
        action.add_argument("--endpoint-url", help="default: $AWS_ENDPOINT_URL")
        if name == "deploy":
            action.add_argument(
                "--dry-run", action="store_true", help="show what would change"
            )
            action.add_argument("-v", "--verbose", action="store_true")
        else:
            action.add_argument(
                "--force", action="store_true", help="allow destroying production"
            )


def _dag_config(args: argparse.Namespace) -> DagsConfig:
    from pathlib import Path

    from databaas_utils.dags.config import load_config

    return load_config(Path(args.config) if args.config else None)


def _dag_context(args: argparse.Namespace) -> tuple[DagsConfig, DagBucket]:
    from databaas_utils.dags.s3 import DagBucket

    bucket = DagBucket.from_env(bucket=args.bucket, endpoint_url=args.endpoint_url)
    return _dag_config(args), bucket


def _describe(dev_key: str) -> str:
    return f"dev deploy {dev_key!r}" if dev_key else "production"


def _cmd_dag_validate(args: argparse.Namespace) -> int:
    from databaas_utils.dags.validate import validate

    config = _dag_config(args)
    result = validate(config, args.target, dev_key=args.dev_key)
    if args.verbose and result.output:
        print(result.output.rstrip())
    annotate = os.environ.get("GITHUB_ACTIONS") == "true"
    for problem in result.problems:
        where = f"{problem.file}: " if problem.file else ""
        print(f"{where}{problem.message}", file=sys.stderr)
        if annotate:
            title = problem.message.strip().splitlines()[-1].replace("%", "%25")
            location = f" file={problem.file}" if problem.file else ""
            print(f"::error{location}::{title}")
    what = _describe(result.resolved.dev_key)
    if not result.ok:
        print(
            f"error: {len(result.problems)} problem(s) in {config.name} ({what})",
            file=sys.stderr,
        )
        return 1
    print(
        f"Validated {config.name} ({what}): {len(result.dag_ids)} DAG(s): "
        + ", ".join(result.dag_ids)
    )
    return 0


def _cmd_dag_deploy(args: argparse.Namespace) -> int:
    from databaas_utils.dags.deploy import deploy

    config, bucket = _dag_context(args)
    result = deploy(
        config,
        args.target,
        bucket,
        dev_key=args.dev_key,
        dry_run=args.dry_run,
        log=print if args.verbose else lambda _: None,
    )
    if args.dry_run:
        for key in result.uploaded:
            print(f"would upload {key}")
        for key in result.deleted:
            print(f"would delete {key}")
    what = _describe(result.resolved.dev_key)
    verb = "Would deploy" if args.dry_run else "Deployed"
    print(
        f"{verb} {config.name} ({what}) to {result.url}: {len(result.uploaded)} "
        f"uploaded, {len(result.unchanged)} unchanged, {len(result.deleted)} deleted"
    )
    if result.renamed:
        print(
            "namespaced: " + ", ".join(f"{k} -> {v}" for k, v in result.renamed.items())
        )
    return 0


def _cmd_dag_destroy(args: argparse.Namespace) -> int:
    from databaas_utils.dags.deploy import destroy

    config, bucket = _dag_context(args)
    resolved, count = destroy(
        config, args.target, bucket, dev_key=args.dev_key, force=args.force
    )
    print(f"Deleted {count} object(s) under s3://{bucket.bucket}/{resolved.prefix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
