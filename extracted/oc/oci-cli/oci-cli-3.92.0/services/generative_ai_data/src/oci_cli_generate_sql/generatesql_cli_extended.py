# coding: utf-8
# Copyright (c) 2016, 2026, Oracle and/or its affiliates.  All rights reserved.

import click
from oci_cli import cli_util
from oci_cli import json_skeleton_utils
from services.generative_ai_data.src.oci_cli_generate_sql.generated import generatesql_cli
from services.generative_ai_data.src.oci_cli_generative_ai_data.generated import generative_ai_data_service_cli


cli_util.rename_command(
    generatesql_cli,
    generative_ai_data_service_cli.generative_ai_data_service_group,
    generatesql_cli.generate_sql_root_group,
    "generate-sql-jobs"
)

generatesql_cli.generate_sql_root_group.commands.pop(generatesql_cli.generate_sql_from_nl_job_group.name)
generatesql_cli.generate_sql_root_group.add_command(generatesql_cli.generate_sql_from_nl)
generatesql_cli.generate_sql_root_group.add_command(generatesql_cli.get_generate_sql_from_nl_job)

cli_util.rename_command(generatesql_cli, generatesql_cli.generate_sql_root_group, generatesql_cli.generate_sql_from_nl, "generate")


@cli_util.copy_params_from_generated_command(generatesql_cli.generate_sql_from_nl, params_to_exclude=['input_natural_language_query'])
@generatesql_cli.generate_sql_root_group.command(name=generatesql_cli.generate_sql_from_nl.name, help=generatesql_cli.generate_sql_from_nl.help)
@cli_util.option('--nl-query', required=True, help=u"""A user-provided query or instruction written in plain, conversational language.""")
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'freeform-tags': {'module': 'generative_ai_data', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'generative_ai_data', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'generative_ai_data', 'class': 'GenerateSqlFromNlJob'})
def generate_sql_from_nl_extended(ctx, **kwargs):
    kwargs['input_natural_language_query'] = kwargs.pop('nl_query')
    ctx.obj.pop('missing_required_parameters', None)
    ctx.invoke(generatesql_cli.generate_sql_from_nl, **kwargs)


@cli_util.copy_params_from_generated_command(generatesql_cli.get_generate_sql_from_nl_job, params_to_exclude=['generate_sql_from_nl_job_id'])
@generatesql_cli.generate_sql_root_group.command(name=generatesql_cli.get_generate_sql_from_nl_job.name, help=generatesql_cli.get_generate_sql_from_nl_job.help)
@cli_util.option('--job-id', required=True, help=u"""The OCID of the GenerateSqlFromNl job.""")
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'generative_ai_data', 'class': 'GenerateSqlFromNlJob'})
def get_generate_sql_from_nl_job_extended(ctx, **kwargs):
    kwargs['generate_sql_from_nl_job_id'] = kwargs.pop('job_id')
    ctx.obj.pop('missing_required_parameters', None)
    ctx.invoke(generatesql_cli.get_generate_sql_from_nl_job, **kwargs)


def _normalize_choice_params(command):
    for param in getattr(command, 'params', []):
        choices = getattr(getattr(param, 'type', None), 'choices', None)
        if isinstance(choices, tuple):
            param.type.choices = list(choices)

    for child in getattr(command, 'commands', {}).values():
        _normalize_choice_params(child)


_normalize_choice_params(generatesql_cli.generate_sql_root_group)
