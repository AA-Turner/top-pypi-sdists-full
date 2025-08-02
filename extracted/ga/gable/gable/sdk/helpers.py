import datetime

from gable.openapi import ContractInput

from .models import ExternalContractInput


def external_to_internal_contract_input(
    input: ExternalContractInput,
) -> ContractInput:
    return ContractInput(
        id=input.contractSpec.id,
        gitHash=(input.gitMetadata.gitHash if input.gitMetadata else None),
        gitRepo=(input.gitMetadata.gitRepo if input.gitMetadata else None),  # type: ignore
        gitUser=input.gitMetadata.gitUser if input.gitMetadata else None,
        mergedAt=(
            input.gitMetadata.mergedAt
            if input.gitMetadata
            else datetime.datetime.now(datetime.timezone.utc)
        ),
        filePath=(input.gitMetadata.filePath if input.gitMetadata else None),
        version=input.version or "",
        status=input.status,
        enforcementLevel=input.enforcementLevel,
        contractSpec=input.contractSpec,
    )
