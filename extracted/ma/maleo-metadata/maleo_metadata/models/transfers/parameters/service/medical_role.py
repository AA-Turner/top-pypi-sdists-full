from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_metadata.models.schemas.medical_role import MaleoMetadataMedicalRoleSchemas

class MaleoMetadataMedicalRoleServiceParametersTransfers:
    class GetMultipleSpecializationsQuery(
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfCodes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultipleQuery(
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfCodes,
        BaseGeneralSchemas.IsLeaf,
        BaseGeneralSchemas.IsChild,
        BaseGeneralSchemas.IsParent,
        BaseGeneralSchemas.IsRoot,
        MaleoMetadataMedicalRoleSchemas.OptionalListOfParentIds,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetStructuredMultipleQuery(
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfCodes,
        MaleoMetadataMedicalRoleSchemas.OptionalListOfParentIds,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultiple(
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfCodes,
        BaseGeneralSchemas.IsLeaf,
        BaseGeneralSchemas.IsChild,
        BaseGeneralSchemas.IsParent,
        BaseGeneralSchemas.IsRoot,
        MaleoMetadataMedicalRoleSchemas.OptionalListOfParentIds,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetStructuredMultiple(
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfCodes,
        MaleoMetadataMedicalRoleSchemas.OptionalListOfParentIds,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass