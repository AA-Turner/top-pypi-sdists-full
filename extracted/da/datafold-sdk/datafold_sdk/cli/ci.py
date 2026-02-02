import json
import logging
import sys
import os
import re
import subprocess
from typing import List

import click

from datafold_sdk.sdk.ci import run_diff, trigger_ci_run, CiDiff
from datafold_sdk import sdk_log

logger = logging.getLogger(__file__)
logger.addHandler(sdk_log.SDKLogHandler())


@click.group()
def manager():
    """Run datafold ci --help for general CI functionality."""


@manager.command()
@click.option('--ci-config-id',
              help="The ID of the CI config in Datafold (see CI settings screen)",
              type=int,
              required=True)
@click.option('--pr-num',
              help="The number of the Pull Request",
              type=int,
              required=True)
@click.option('--diffs',
              help='compose file to work with',
              type=click.File('r'),
              default=sys.stdin)
@click.pass_context
def submit(ctx: click.Context, ci_config_id: int, pr_num: int, diffs):
    """Submit some diffs for a CI run"""
    with diffs:
        diffs_json = diffs.read()
    diffs_dicts = json.loads(diffs_json)
    ci_diffs = [CiDiff(**d) for d in diffs_dicts]

    run_id = run_diff(
        host=ctx.obj.host,
        api_key=ctx.obj.api_key,
        ci_config_id=ci_config_id,
        pr_num=pr_num,
        diffs=ci_diffs
    )
    if run_id:
        logger.info(f"Successfully started a diff under Run ID {run_id}")
    else:
        logger.info("Could not find an active job for the pull request, is the CI set up correctly?")


@manager.command()
@click.option('--ci-config-id',
              help="The ID of the CI config in Datafold (see CI settings screen)",
              type=int,
              required=True)
@click.option('--pr-num',
              help="The number of the Pull Request",
              type=int,
              required=True)
@click.option('--base-branch',
              help="The branch name being merged into",
              type=str,
              required=True)
@click.option('--base-sha',
              help="The SHA of the common base",
              type=str,
              required=True)
@click.option('--pr-branch',
              help="The branch from which this PR is created",
              type=str,
              required=True)
@click.option('--pr-sha',
              help="The HEAD SHA of this branch",
              type=str,
              required=True)
@click.pass_context
def trigger(ctx: click.Context,
            ci_config_id: int,
            pr_num: int,
            base_branch: str,
            base_sha: str,
            pr_branch: str,
            pr_sha: str,
):
    """Trigger a CI run and let Datafold work out the diffs from the pull request."""
    _ = trigger_ci_run(
        host=ctx.obj.host,
        api_key=ctx.obj.api_key,
        ci_config_id=ci_config_id,
        pr_num=pr_num,
        base_sha=base_sha,
        base_branch=base_branch,
        pr_branch=pr_branch,
        pr_sha=pr_sha,
    )
    return 0


@click.group(help="Auto CI commands")
def auto_ci_manager():
    pass


manager.add_command(auto_ci_manager, "auto")


@auto_ci_manager.command(name="trigger", help="Automatically discover changes and trigger a CI run")
@click.option('--ci-config-id',
              help="The ID of the CI config in Datafold (see CI settings screen)",
              type=int,
              required=True)
@click.option('--pr-num',
              help="The PR number of the pull or merge request.",
              type=int,
              required=True)
@click.option('--base-sha',
              type=str,
              required=True)
@click.option('--base-branch',
              type=str,
              required=True)
@click.option('--pr-sha',
              type=str,
              required=True)
@click.option('--pr-branch',
              type=str,
              required=True)
@click.option('--pr-params',
              type=str,
              required=True)
@click.option('--reference-params',
              type=str,
              required=True)
@click.option('--root-path',
               type=str,
               default='./',
               required=True)
@click.pass_context
def trigger_auto_ci(
        ctx: click.Context,
        ci_config_id: int,
        pr_num: int,
        base_sha: str,
        base_branch: str,
        pr_sha: str,
        pr_branch: str,
        root_path: str,
        pr_params: str,
        reference_params: str):
    changed_file_names = subprocess.run(['git', 'diff', '--name-only', base_sha, pr_sha], capture_output=True,
                                        check=True, cwd=root_path)
    changed_files = [
        os.path.join(root_path, file_name)
        for file_name in changed_file_names.stdout.decode('utf-8').splitlines()
    ]
    tables = {}
    reference_params_values = json.loads(reference_params)
    pr_params_values = json.loads(pr_params)
    for file in changed_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                table_regex = r"create (or replace )?table\s+([^\s]+)\s"
                match = re.search(table_regex, content, re.IGNORECASE)
                if not match:
                    continue
                table_name = match.group(2)
                prod_table = table_name
                for key, value in reference_params_values.items():
                    prod_table = prod_table.replace(f'${{{key}}}', value)

                pr_table = table_name
                for key, value in pr_params_values.items():
                    pr_table = pr_table.replace(f'${{{key}}}', value)

                pk_regex = r'datafold:\spk=([^\s]+(,[^\s]+)*)'
                match = re.search(pk_regex, content, re.IGNORECASE)
                pk: List[str] = []
                if match:
                    pk = match.group(1).split(',')
                tables[table_name] = {
                    'table1': prod_table,
                    'table2': pr_table,
                    'pk': pk,
                }
        except (IOError, UnicodeDecodeError):
            continue

    diffs = []
    for payload in tables.values():
        diffs.append(
            CiDiff(
                prod=payload['table1'],
                pr=payload['table2'],
                pk=payload['pk'],
            )
        )
    if not diffs:
        return
    trigger_ci_run(host=ctx.obj.host,
                   api_key=ctx.obj.api_key,
                   ci_config_id=ci_config_id,
                   pr_num=pr_num,
                   pr_sha=pr_sha,
                   base_sha=base_sha,
                   pr_branch=pr_branch,
                   base_branch=base_branch)
    run_diff(
        host=ctx.obj.host,
        api_key=ctx.obj.api_key,
        ci_config_id=ci_config_id,
        pr_num=pr_num,
        diffs=diffs
    )
