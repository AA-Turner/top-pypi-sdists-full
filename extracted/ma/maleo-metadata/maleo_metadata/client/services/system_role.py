from typing import Dict, Optional
from maleo_foundation.authorization import Authorization
from maleo_foundation.managers.client.maleo import MaleoClientService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.client.controllers import MaleoMetadataSystemRoleControllers
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.models.transfers.parameters.general.system_role \
    import MaleoMetadataSystemRoleGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.system_role \
    import MaleoMetadataSystemRoleClientParametersTransfers
from maleo_metadata.models.transfers.results.client.system_role \
    import MaleoMetadataSystemRoleClientResultsTransfers
from maleo_metadata.types.results.client.system_role \
    import MaleoMetadataSystemRoleClientResultsTypes

class MaleoMetadataSystemRoleClientService(MaleoClientService):
    def __init__(
        self,
        key,
        logger,
        service_manager,
        controllers:MaleoMetadataSystemRoleControllers
    ):
        super().__init__(key, logger, service_manager)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoMetadataSystemRoleControllers:
        raise self._controllers

    async def get_system_roles(
        self,
        parameters:MaleoMetadataSystemRoleClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP,
        authorization:Optional[Authorization] = None,
        headers:Optional[Dict[str, str]] = None
    ) -> MaleoMetadataSystemRoleClientResultsTypes.GetMultiple:
        """Retrieve system roles from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving system roles",
            logger=self._logger,
            fail_result_class=MaleoMetadataSystemRoleClientResultsTransfers.Fail
        )
        async def _impl(
            parameters:MaleoMetadataSystemRoleClientParametersTransfers.GetMultiple,
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
                return MaleoMetadataSystemRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve system roles using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_system_roles(
                        parameters=parameters,
                        authorization=authorization,
                        headers=headers
                    )
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataSystemRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataSystemRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoMetadataSystemRoleClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                    )
                else:
                    return (
                        MaleoMetadataSystemRoleClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type,
            authorization=authorization,
            headers=headers
        )

    async def get_system_role(
        self,
        parameters:MaleoMetadataSystemRoleGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP,
        authorization:Optional[Authorization] = None,
        headers:Optional[Dict[str, str]] = None
    ) -> MaleoMetadataSystemRoleClientResultsTypes.GetSingle:
        """Retrieve system role from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving system role",
            logger=self._logger,
            fail_result_class=MaleoMetadataSystemRoleClientResultsTransfers.Fail
        )
        async def _impl(
            parameters:MaleoMetadataSystemRoleGeneralParametersTransfers.GetSingle,
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
                return MaleoMetadataSystemRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve system role using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_system_role(
                        parameters=parameters,
                        authorization=authorization,
                        headers=headers
                    )
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataSystemRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataSystemRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                )
            else:
                return (
                    MaleoMetadataSystemRoleClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type,
            authorization=authorization,
            headers=headers
        )