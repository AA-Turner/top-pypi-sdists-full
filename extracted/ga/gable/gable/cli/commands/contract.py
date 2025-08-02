import re
from typing import Generator, List, Optional

import click
from click.core import Context as ClickContext
from gable.api.client import GableAPIClient
from gable.cli.helpers.contract import (
    contract_files_to_contract_inputs,
    contract_files_to_post_contract_request,
)
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.shell_output import shell_linkify_if_not_in_ci
from gable.cli.options import global_options
from gable.openapi import (
    ContractInput,
    ContractOutput,
    EnforcementLevel,
    PostContractRequest,
    PostContractResponse,
)
from gable.sdk.models import ContractPublishResponse
from loguru import logger

CONTRACT_VALIDATE_CHUNK_SIZE = 20


@click.group()
def contract():
    """Commands for contracts"""


@contract.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
    epilog="""Examples:

    gable contract publish contract1.yaml

    gable contract publish **/*.yaml""",
)
@click.argument(
    "contract_files",
    type=click.File(),
    nargs=-1,
)
@global_options()
@click.pass_context
def publish(ctx: ClickContext, contract_files: List[click.File]):
    """Publishes data contracts to Gable"""
    request = contract_files_to_contract_inputs(contract_files)
    response: ContractPublishResponse = ctx.obj.client.contracts.publish(request)
    if not response.success:
        raise click.ClickException(f"Publish failed: {response.message}")
    if len(response.updatedContractIds) == 0:
        logger.info("\u2705 No contracts published")
    else:
        updated_contracts = ", ".join(
            shell_linkify_if_not_in_ci(
                f"{ctx.obj.client.ui_endpoint}/contracts/{cid}",
                str(cid),
            )
            for cid in response.updatedContractIds
        )
        logger.info(f"\u2705 {len(response.updatedContractIds)} contract(s) published")
        logger.info(f"\t{updated_contracts}")


@contract.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
    epilog="""Examples:\n
\b
  gable contract validate contract1.yaml
  gable contract validate **/*.yaml""",
)
@click.argument("contract_files", type=click.File(), nargs=-1)
@global_options()
@click.pass_context
def validate(ctx: ClickContext, contract_files: List[click.File]):
    """Validates the configuration of the data contract files"""
    all_string_results = []
    overall_success = True

    for contract_file_chunk in _chunk_list(
        contract_files, CONTRACT_VALIDATE_CHUNK_SIZE
    ):
        string_results, success = _validate_contract_chunk(contract_file_chunk, ctx)
        all_string_results.append(string_results)
        if not success:
            overall_success = False

    final_string_results = "\n".join(all_string_results)
    if not overall_success:
        raise click.ClickException(f"\n{final_string_results}\nInvalid contract(s)")
    logger.info(final_string_results)
    logger.info("All contracts are valid")


def _chunk_list(
    input_list: List[click.File], chunk_size: int
) -> Generator[List[click.File], None, None]:
    """Splits a list into chunks of specified size."""
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i : i + chunk_size]


def _validate_contract_chunk(
    contract_file_chunk: List[click.File], ctx: ClickContext
) -> tuple[str, bool]:
    request = contract_files_to_post_contract_request(contract_file_chunk)
    response, success, _status_code = ctx.obj.client.post_contract_validate(request)
    logger.info(response["message"])
    data = response["message"].split("\n")
    # For each input file, zip up the emoji, file name, and result message into a tuple
    zipped_results = zip(
        [
            # Compute emoji based on whether the contract is valid
            EMOJI.GREEN_CHECK.value if m.strip() == "VALID" else EMOJI.RED_X.value
            for m in data
        ],
        contract_file_chunk,
        [m.replace("\n", "\n\t") for m in data],
    )
    string_results = "\n".join(
        [
            # For valid contracts, just print the check mark and name
            (
                f"{x[0]} {x[1].name}"
                if x[2].strip() == "VALID"
                # For invalid contracts, print the check mark, name, and error message
                else f"{x[0]} {x[1].name}:\n\t{x[2]}"
            )
            for x in zipped_results
        ]
    )
    return string_results, success


@contract.command(
    epilog="""Examples:\n
\b
  gable contract bulk-update-enforcement-levels BLOCK
  gable contract bulk-update-enforcement-levels ALERT data-asset-id-pattern 'postgres://*'""",
)
@click.option(
    "--enforcement-level",
    required=True,
    type=click.Choice([e.name for e in EnforcementLevel]),
    help="""The enforcement level to set for all contracts.
    """,
)
@click.option(
    "--data-asset-id-pattern",
    type=str,
    help="""Regex pattern to match data asset IDs. Only the contracts that have associated data assets that match the provided data asset id pattern will be updated.""",
)
@global_options()
@click.pass_context
def bulk_update_enforcement_levels(
    ctx: ClickContext, enforcement_level: str, data_asset_id_pattern: Optional[str]
):
    """
    Updates the enforcement level of all contracts to the given enforcement level.
    If a data asset id pattern is provided, only the contracts that have associated data assets that match the provided data asset id pattern will be updated.
    """
    # Get all contracts using getContracts
    client: GableAPIClient = ctx.obj.client

    enforcement_level = EnforcementLevel[enforcement_level]
    contracts = client.get_contracts()

    # Convert list of ContractOutputs to list of ContractInputs
    contract_inputs: list[ContractInput] = []
    for contract in contracts:
        # Skip if no data asset resource name
        if not contract.contractSpec.dataAssetResourceName:
            continue

        darn: str = contract.contractSpec.dataAssetResourceName.__root__
        if data_asset_id_pattern is None or re.match(data_asset_id_pattern, darn):
            # Only update the enforcement level if the data asset id matches the pattern (or when no pattern was provided)
            contract_input = _create_contract_input(contract, enforcement_level)
            contract_inputs.append(contract_input)

    # Call the postContract endpoint to update the contracts
    request = PostContractRequest(__root__=contract_inputs)
    response, _success, _status_code = client.post_contract(request)
    if isinstance(response, PostContractResponse):
        logger.info(f"Updated {len(response.contractIds)} contract(s)")
    else:
        logger.error(f"Failed to update contracts, error: {response}")


def _create_contract_input(
    contract: ContractOutput, enforcement_level: EnforcementLevel
):
    return ContractInput(
        id=contract.id,
        version=contract.version,
        status=contract.status,
        gitHash=contract.gitHash,
        gitRepo=contract.gitRepo,
        gitUser=contract.gitUser,
        reviewers=contract.reviewers,
        filePath=contract.filePath or "",
        mergedAt=contract.mergedAt,
        enforcementLevel=enforcement_level,
        contractSpec=contract.contractSpec,
        lastEditorUserId=contract.lastEditorUserId,
        lastEditorEmail=contract.lastEditorEmail,
        lastEditorFirstName=contract.lastEditorFirstName,
        lastEditorLastName=contract.lastEditorLastName,
        lastEditorGithubHandle=contract.lastEditorGithubHandle,
    )
