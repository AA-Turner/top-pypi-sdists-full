from typing import Dict, Optional
from maleo_foundation.authorization import Authorization
from maleo_foundation.managers.client.maleo import MaleoClientService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.client.controllers import MaleoMetadataOrganizationTypeControllers
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.models.transfers.parameters.general.organization_type \
    import MaleoMetadataOrganizationTypeGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.organization_type \
    import MaleoMetadataOrganizationTypeClientParametersTransfers
from maleo_metadata.models.transfers.results.client.organization_type \
    import MaleoMetadataOrganizationTypeClientResultsTransfers
from maleo_metadata.types.results.client.organization_type \
    import MaleoMetadataOrganizationTypeClientResultsTypes

class MaleoMetadataOrganizationTypeClientService(MaleoClientService):
    def __init__(
        self,
        key,
        logger,
        service_manager,
        controllers:MaleoMetadataOrganizationTypeControllers
    ):
        super().__init__(key, logger, service_manager)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoMetadataOrganizationTypeControllers:
        raise self._controllers

    async def get_organization_types(
        self,
        parameters:MaleoMetadataOrganizationTypeClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP,
        authorization:Optional[Authorization] = None,
        headers:Optional[Dict[str, str]] = None
    ) -> MaleoMetadataOrganizationTypeClientResultsTypes.GetMultiple:
        """Retrieve organization types from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving organization types",
            logger=self._logger,
            fail_result_class=MaleoMetadataOrganizationTypeClientResultsTransfers.Fail
        )
        async def _impl(
            parameters:MaleoMetadataOrganizationTypeClientParametersTransfers.GetMultiple,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP,
            authorization:Optional[Authorization] = None,
            headers:Optional[Dict[str, str]] = None
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataOrganizationTypeClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve organization types using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_organization_types(
                        parameters=parameters,
                        authorization=authorization,
                        headers=headers
                    )
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataOrganizationTypeClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataOrganizationTypeClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoMetadataOrganizationTypeClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                    )
                else:
                    return (
                        MaleoMetadataOrganizationTypeClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type,
            authorization=authorization,
            headers=headers
        )

    async def get_organization_type(
        self,
        parameters:MaleoMetadataOrganizationTypeGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP,
        authorization:Optional[Authorization] = None,
        headers:Optional[Dict[str, str]] = None
    ) -> MaleoMetadataOrganizationTypeClientResultsTypes.GetSingle:
        """Retrieve organization type from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving organization type",
            logger=self._logger,
            fail_result_class=MaleoMetadataOrganizationTypeClientResultsTransfers.Fail
        )
        async def _impl(
            parameters:MaleoMetadataOrganizationTypeGeneralParametersTransfers.GetSingle,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP,
            authorization:Optional[Authorization] = None,
            headers:Optional[Dict[str, str]] = None
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataOrganizationTypeClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve organization type using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_organization_type(
                        parameters=parameters,
                        authorization=authorization,
                        headers=headers
                    )
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataOrganizationTypeClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataOrganizationTypeClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                )
            else:
                return (
                    MaleoMetadataOrganizationTypeClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type,
            authorization=authorization,
            headers=headers
        )