from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_metadata.models.schemas.medical_role import MaleoMetadataMedicalRoleSchemas

class MaleoMetadataMedicalRoleClientParametersTransfers:
    class GetMultiple(
        BaseClientParametersTransfers.GetPaginatedMultiple,
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

    class GetMultipleRootSpecializations(
        BaseClientParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfCodes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultipleSpecializations(
        GetMultipleRootSpecializations,
        MaleoMetadataMedicalRoleSchemas.MedicaRoleId
    ): pass

    class GetStructuredMultiple(
        BaseClientParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfCodes,
        MaleoMetadataMedicalRoleSchemas.OptionalListOfParentIds,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultipleQuery(
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
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

    class GetMultipleSpecializationsQuery(
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfCodes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetStructuredMultipleQuery(
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfNames,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseParameterSchemas.OptionalListOfCodes,
        MaleoMetadataMedicalRoleSchemas.OptionalListOfParentIds,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass