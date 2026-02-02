import sys

import yaml
import click

from datafold_sdk.sdk.utils import prepare_headers, prepare_api_url, post_data


@click.group()
def manager():
    """Monitors management."""


def _print_provisioning_result(provisioning_result: dict, dry_run: bool) -> bool:
    """
    Print provisioning results and return whether there were errors.

    Returns:
        True if there were errors, False otherwise.
    """
    errors = provisioning_result.get('errors', [])

    created = provisioning_result.get('created_monitors', [])
    updated = provisioning_result.get('updated_monitors', [])
    deleted = provisioning_result.get('deleted_monitors', [])
    paused = provisioning_result.get('paused_monitors', [])

    if dry_run:
        print("Dry run completed")
        print(f"Monitors to be created: {len(created)}")
        print(f"Monitors to be updated: {len(updated)}")
        print(f"Monitors to be deleted: {len(deleted)}")
        print(f"Monitors to be paused: {len(paused)}")
    else:
        print("Provisioning completed:")
        print(f"  created: {len(created)}")
        print(f"  updated: {len(updated)}")
        print(f"  deleted: {len(deleted)}")
        print(f"  paused: {len(paused)}")

    if errors:
        print(f"\nEncountered {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        return True

    return False


@manager.command()
@click.argument('yaml_file', type=click.Path(exists=True))
@click.option('--dangling-monitors-strategy', type=str, default='ignore',
              help="How to handle monitors not defined in the yaml file: ignore, delete, pause.")
@click.option('--dry-run', is_flag=True, help="Dry run the provisioning")
@click.pass_context
def provision(ctx: click.Context, yaml_file: str, dangling_monitors_strategy: str, dry_run: bool):
    """Provision monitors from a YAML configuration file."""
    with open(yaml_file, encoding='utf-8') as f:
        config = yaml.safe_load(f)
    headers = prepare_headers(ctx.obj.api_key)
    api_segment = "api/internal/monitors/provision"
    url = prepare_api_url(ctx.obj.host, api_segment)
    resp = post_data(url, json_data={
        'config': config,
        'dangling_monitors_strategy': dangling_monitors_strategy,
        'dry_run': dry_run
    }, headers=headers)
    if not resp.ok:
        print("Failed to provision monitors")
        print(resp.text)
        sys.exit(1)

    provisioning_result = resp.json()
    has_errors = _print_provisioning_result(provisioning_result, dry_run)

    if has_errors:
        sys.exit(1)
