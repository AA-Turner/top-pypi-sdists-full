from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers

class MaleoMetadataGenderServiceParametersTransfers:
    class GetMultipleQuery(
        BaseServiceParametersTransfers.GetUnpaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultiple(
        BaseServiceParametersTransfers.GetUnpaginatedMultiple,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass