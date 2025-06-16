from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers

class MaleoMetadataOrganizationTypeClientParametersTransfers:
    class GetMultiple(
        BaseClientParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultipleQuery(
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass