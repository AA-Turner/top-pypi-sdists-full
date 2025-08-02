import json
from typing import List, Literal

import click
from gable.api.client import GableAPIClient
from gable.cli.commands.asset_plugins.baseclass import (
    AssetPluginAbstract,
    ExtractedAsset,
)
from gable.cli.helpers.data_asset import (
    darn_to_string,
    determine_should_block,
    format_check_data_assets_json_output,
    format_check_data_assets_text_output,
)
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.repo_interactions import get_pr_link
from gable.cli.helpers.sca_exceptions import ScaException
from gable.cli.options import global_options
from gable.openapi import (
    CheckDataAssetCommentMarkdownResponse,
    DataAssetsCheckComplianceRequest,
    ErrorResponse,
    ResolvedDataAsset,
    ResponseType,
    SourceType,
)
from loguru import logger

output_format_to_response_type = {
    "text": ResponseType.DETAILED,
    "json": ResponseType.DETAILED,
    "markdown": ResponseType.COMMENT_MARKDOWN,
}


def extracted_assets_to_check_assets_request(
    source_type: SourceType,
    extracted_assets: List[ExtractedAsset],
    output_format: Literal["text", "json", "markdown"],
    include_unchanged_assets: bool,
) -> DataAssetsCheckComplianceRequest:

    return DataAssetsCheckComplianceRequest(
        assets=[
            ResolvedDataAsset(
                source_type=source_type,
                data_asset_resource_name=asset.darn,
                schema={
                    "type": "struct",
                    "fields": asset.fields,
                },
            )
            for asset in extracted_assets
        ],
        includeUnchangedAssets=include_unchanged_assets,
        responseType=output_format_to_response_type[output_format],
        prLink=get_pr_link(),
    )


def check_click_command_for_asset_plugin(asset_plugin: AssetPluginAbstract):

    @click.command(
        name=asset_plugin.source_type(),
        help=f"Check a {asset_plugin.source_type()} data asset against contracts",
        short_help=f"Check a {asset_plugin.source_type()} data asset against contracts",
    )
    @click.option(
        "--include-unchanged-assets",
        type=bool,
        default=False,
        help="""Include assets that are the same as Gable's registered version of the asset. This is useful for checking the current state of an asset but should not be used for automated checks on branches.""",
    )
    @click.option(
        "-o",
        "--output",
        type=click.Choice(["text", "json", "markdown"]),
        default="text",
        help="Format of the output. Options are: text (default), json, or markdown which is intended to be used as a PR comment",
    )
    @global_options()
    @click.pass_context
    @asset_plugin.click_options_decorator()
    def implementation(
        ctx: click.Context,
        include_unchanged_assets: bool,
        output: Literal["text", "json", "markdown"],
        *args,
        **kwargs,
    ):
        allowed_args = set(asset_plugin.click_options_keys())
        received_args = set(kwargs.keys())
        if not received_args.issubset(allowed_args):
            raise ValueError(f"Extra fields found: {received_args - allowed_args}")

        asset_plugin.pre_validation(kwargs)
        plugin_check(asset_plugin, output, include_unchanged_assets, kwargs, ctx)

    return implementation


def plugin_check(
    asset_plugin: AssetPluginAbstract,
    output: Literal["text", "json", "markdown"],
    include_unchanged_assets: bool,
    kwargs: dict,
    ctx: click.Context,
):
    client: GableAPIClient = ctx.obj.client
    try:
        extracted_assets = asset_plugin.extract_assets(client, kwargs)
    except ScaException as e:
        if output == "markdown":
            # Log to stdout so the markdown is displayed in the PR comment
            logger.info(e.markdown)
        raise click.ClickException("Error running Gable SCA: \n" + str(e))
    if not extracted_assets:
        raise click.ClickException(
            f"Error checking data assets: No data assets found to check! You can use the --debug or --trace flags for more details."
        )

    for asset in extracted_assets:
        darn_str = darn_to_string(asset.darn)
        logger.trace(
            f"- {darn_str} schema: {json.dumps([field.json() for field in asset.fields], indent=2)}"
        )

    check_assets_request = extracted_assets_to_check_assets_request(
        asset_plugin.source_type(),
        extracted_assets,
        output,
        include_unchanged_assets,
    )

    response = client.post_data_assets_check_compliance(check_assets_request)

    if isinstance(response, ErrorResponse):
        raise click.ClickException(
            f"Error checking data assets: {response.title}: {response.message}"
        )
    elif isinstance(response, CheckDataAssetCommentMarkdownResponse):
        if response.markdown and response.markdown != "":
            # Print markdown to stdout, so our cicd github action/users' integrations can read it
            # separately from the error output to determine if we should comment on a PR
            logger.info(response.markdown)

        if response.shouldBlock:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Contract violations found, maximum enforcement level was 'BLOCK'"
            )
        elif response.shouldAlert:
            logger.error(
                f"{EMOJI.YELLOW_WARNING.value} Contract violations found, maximum enforcement level was 'ALERT'"
            )

        if response.errors:
            errors_string = "\n".join([error.json() for error in response.errors])
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Contract checking failed for some data assets:\n{errors_string}"
            )
    else:
        should_block = determine_should_block(response)
        if output == "markdown":
            raise click.ClickException(
                "Markdown response not received from backend although requested"
            )
        elif output == "json":
            output_string = format_check_data_assets_json_output(response)
        else:
            output_string = format_check_data_assets_text_output(response)
        logger.info(output_string)
        if should_block:
            raise click.ClickException("Contract violation(s) found")
