from typing import Dict, Optional
from maleo_foundation.authorization import Authorization
from maleo_foundation.managers.client.maleo import MaleoClientService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.client.controllers import MaleoMetadataGenderControllers
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.models.transfers.parameters.general.gender \
    import MaleoMetadataGenderGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.gender \
    import MaleoMetadataGenderClientParametersTransfers
from maleo_metadata.models.transfers.results.client.gender \
    import MaleoMetadataGenderClientResultsTransfers
from maleo_metadata.types.results.client.gender \
    import MaleoMetadataGenderClientResultsTypes

class MaleoMetadataGenderClientService(MaleoClientService):
    def __init__(
        self,
        key,
        logger,
        service_manager,
        controllers:MaleoMetadataGenderControllers
    ):
        super().__init__(key, logger, service_manager)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoMetadataGenderControllers:
        raise self._controllers

    async def get_genders(
        self,
        parameters:MaleoMetadataGenderClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP,
        authorization:Optional[Authorization] = None,
        headers:Optional[Dict[str, str]] = None
    ) -> MaleoMetadataGenderClientResultsTypes.GetMultiple:
        """Retrieve genders from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving genders",
            logger=self._logger,
            fail_result_class=MaleoMetadataGenderClientResultsTransfers.Fail
        )
        async def _impl(
            parameters:MaleoMetadataGenderClientParametersTransfers.GetMultiple,
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
                return MaleoMetadataGenderClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve genders using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_genders(
                        parameters=parameters,
                        authorization=authorization,
                        headers=headers
                    )
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataGenderClientResultsTransfers.Fail(
                    message=message,
                    description=description,
                    authorization=authorization,
                    headers=headers
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataGenderClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoMetadataGenderClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                    )
                else:
                    return (
                        MaleoMetadataGenderClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type,
            authorization=authorization,
            headers=headers
        )

    async def get_gender(
        self,
        parameters:MaleoMetadataGenderGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP,
        authorization:Optional[Authorization] = None,
        headers:Optional[Dict[str, str]] = None
    ) -> MaleoMetadataGenderClientResultsTypes.GetSingle:
        """Retrieve gender from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving gender",
            logger=self._logger,
            fail_result_class=MaleoMetadataGenderClientResultsTransfers.Fail
        )
        async def _impl(
            parameters:MaleoMetadataGenderGeneralParametersTransfers.GetSingle,
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
                return MaleoMetadataGenderClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve gender using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_gender(
                        parameters=parameters,
                        authorization=authorization,
                        headers=headers
                    )
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataGenderClientResultsTransfers.Fail(
                    message=message,
                    description=description,
                    authorization=authorization,
                    headers=headers
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataGenderClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                )
            else:
                return (
                    MaleoMetadataGenderClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type,
            authorization=authorization,
            headers=headers
        )