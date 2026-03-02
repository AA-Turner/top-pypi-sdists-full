"""Cli for licensing"""

import os
from typing import List
import argparse

from dlt.common.configuration.container import Container
from dlt.common.configuration.specs import PluggableRunContext
from dlt._workspace.cli import echo as fmt, SupportsCliCommand

from dlthub.common.license.exceptions import DltUnknownScopeException

from .license import (
    DltLicense,
    DltLicenseNotFoundException,
    TLicenseType,
    create_self_signed_license,
    decode_license,
    discover_license,
    discover_private_key,
    create_license,
    ensure_feature_scope,
    get_known_features,
    get_known_scopes,
    prettify_license,
    validate_license,
    DltPrivateKeyNotFoundException,
)


def _get_private_key() -> str:
    try:
        return discover_private_key()
    except DltPrivateKeyNotFoundException:
        return None


def print_license() -> None:
    """
    Print the found license
    """
    fmt.echo("Searching dlt license in environment or secrets toml")
    encoded_license = discover_license()
    fmt.echo("License found")
    # decode license type
    validate_license(encoded_license)
    fmt.echo(prettify_license(encoded_license, with_license=False))


def issue_license(
    licensee_name: str, license_type: TLicenseType, days_valid: int, scopes: List[str]
) -> None:
    """
    Issue a new license
    """
    if license_type not in ["trial", "commercial"]:
        fmt.error("License type must be trial or commercial")
        exit(0)
    if not _get_private_key():
        exit(0)

    fmt.echo(f"Generating license for {licensee_name}, valid for {days_valid} days.")
    license = create_license(
        private_key=_get_private_key(),
        days_valid=days_valid,
        licensee_name=licensee_name,
        license_type=license_type,
        scope=" ".join(scopes),  # space delimited scopes
    )
    fmt.echo("License generated")
    fmt.echo(prettify_license(license, with_license=True))


def self_issue_trial_license(scopes: List[str]) -> None:
    """Issue a self-signed trial license for selected feature scopes and install it.

    This command helps you evaluate dltHub Features without a commercial key. It:
    - Validates the provided feature scopes.
    - Merges them with any already installed self-issued trial license scopes.
    - Generates a new self-signed trial license.
    - Writes it to your global secrets.toml so it is picked up automatically.
    - Sends a single anonymous telemetry event with the selected scopes.

    By using this command you accept the dltHub EULA and agree to the above telemetry:
    https://dlthub.com/docs/hub/EULA

    Args:
        scopes: A list of feature scope names to include in the trial license. Scopes must
            refer to individual features (package or wildcard scopes are not allowed).

    Raises:
        DltUnknownScopeException: If any of the provided scopes are not recognized.

    Side Effects:
        - Prints license details and guidance to the console.
        - Writes/updates [runtime].license in your global secrets.toml.
        - Reloads configuration providers and the license context.
        - Sends an anonymous telemetry event with the selected scopes.

    Example:
        >>> self_issue_trial_license(["dlthub.transformation"])
    """
    # read current license in order to merge scopes
    existing_scopes: str = ""
    existing_license: DltLicense = None
    try:
        encoded_existing = discover_license()
        existing_license = decode_license(encoded_existing)
        if existing_license["license_type"] == "self-issued-trial":
            # scopes are space delimited
            existing_scopes = existing_license["scope"]
    except DltLicenseNotFoundException:
        encoded_existing = None

    # must be feature scope, package or wildcard scopes not allowed
    for scope in scopes:
        ensure_feature_scope(scope)

    all_scopes = set(scopes)
    if existing_scopes:
        all_scopes.update(existing_scopes.split(" "))

    fmt.echo("You are self issuing a trial license for the following scopes:")
    for scope in all_scopes:
        if scope_info := get_known_features().get(scope):
            fmt.echo(fmt.bold(f"{scope} - {scope_info[0]} {scope_info[1]}"))
        else:
            raise DltUnknownScopeException(scope)
    fmt.echo("")
    fmt.echo("Please read our EULA: https://dlthub.com/docs/hub/EULA")
    fmt.echo(
        "If you are interested in production license or support during trial, contact us at: "
        "https://info.dlthub.com/waiting-list"
    )
    fmt.echo(
        "Please note that we will send an anonymous telemetry event with the license scope you "
        "selected."
    )
    fmt.echo("")
    with fmt.maybe_no_stdin():
        confirmed = fmt.confirm("I agree to dltHub EULA and to send telemetry event", default=True)
    if confirmed:
        new_license_encoded = create_self_signed_license(" ".join(all_scopes))
        fmt.echo("New license details:")
        fmt.echo(prettify_license(new_license_encoded))

        # non self-signed license exist
        if encoded_existing and not existing_scopes:
            fmt.warning(
                "A license that is not self-signed already exists. Auto-installation will not be "
                "possible."
            )
            fmt.echo("Please paste the toml snipped below into your global secrets.toml")
            fmt.echo(f'[runtime]\nlicense="{new_license_encoded}"')
        else:
            from dlt.common.runtime import run_context
            from dlt.common.configuration.providers import SecretsTomlProvider
            from dlt._workspace.cli.config_toml_writer import WritableConfigValue, write_values

            run_ctx = run_context.active()
            # write global config
            global_path = run_ctx.global_dir
            os.makedirs(global_path, exist_ok=True)
            secrets = SecretsTomlProvider(settings_dir=global_path)
            telemetry_value = [
                WritableConfigValue("license", str, new_license_encoded, ("runtime",))
            ]
            write_values(secrets._config_toml, telemetry_value, overwrite_existing=True)
            secrets.write_toml()
            Container()[PluggableRunContext].reload_providers()

            # reset licenses
            from .license import LicenseContext

            Container()[LicenseContext].reload()
            fmt.echo("")
            fmt.echo(f"License saved to {secrets.locations[0]}")

        # set mandatory telemetry event
        from dlt.common.runtime.anon_tracker import always_track, track

        with always_track():
            track(
                "command",
                "issue-license",
                {"scopes": scopes, "license-category": "self-issued-trial"},
            )


class LicenseCommand(SupportsCliCommand):
    command = "license"
    help_string = "View dlthub license status"

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser

        subparsers = parser.add_subparsers(
            title="Available subcommands", dest="license_command", required=True
        )
        subparsers.add_parser("info", help="Show the installed license")
        subparsers.add_parser("scopes", help="Show available scopes")

        known_scopes = get_known_scopes()
        if _get_private_key():
            issue_parser = subparsers.add_parser(
                "issue", help="Issue a new license", description="Issue a new license"
            )
            issue_parser.add_argument("licensee_name", help="Name of the licensee")
            issue_parser.add_argument(
                "days_valid",
                nargs="?",
                help="Amount of days the license will be valid",
                default=30,
                type=int,
            )
            issue_parser.add_argument(
                "license_type",
                nargs="?",
                help="Type of license, can be trial or commercial",
                choices=["trial", "commercial"],
                default="trial",
            )
            issue_parser.add_argument(
                "scope",
                nargs="?",
                help=f"Scope of the license, a comma separated list of the scopes: {known_scopes}",
                default="*",
            )
        else:
            # scopes that are features with docs pages
            known_scopes = [scope for scope, info in get_known_features().items() if info[1]]
            issue_parser = subparsers.add_parser(
                "issue",
                help="Issues a self-signed trial license that may be used for development, testing "
                "and for ci ops.",
                description="Issue a new self-signed trial license",
            )
            issue_parser.add_argument(
                "scope",
                help=f"Scope of the license, a comma separated list of the scopes: {known_scopes}",
            )

    def execute(self, args: argparse.Namespace) -> None:
        if args.license_command == "info":
            print_license()
        elif args.license_command == "issue":
            if args.scope:
                scopes = [scope.strip() for scope in args.scope.split(",")]
            else:
                scopes = []

            # verify if scopes are known
            all_scopes = get_known_scopes()
            for scope in scopes:
                if scope not in all_scopes:
                    raise DltUnknownScopeException(scope)

            if _get_private_key():
                issue_license(args.licensee_name, args.license_type, int(args.days_valid), scopes)
            else:
                self_issue_trial_license(scopes)
        elif args.license_command == "scopes":
            fmt.echo("Known scopes:")
            for scope, info in get_known_features().items():
                fmt.echo("%s - %s %s" % (fmt.bold(scope), *info))
