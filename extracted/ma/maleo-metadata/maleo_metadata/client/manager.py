from __future__ import annotations
from maleo_foundation.managers.client.maleo import MaleoClientManager
from maleo_foundation.managers.service import ServiceManager
from maleo_metadata.client.controllers.http.blood_type \
    import MaleoMetadataBloodTypeHTTPController
from maleo_metadata.client.controllers.http.gender \
    import MaleoMetadataGenderHTTPController
from maleo_metadata.client.controllers.http.medical_role \
    import MaleoMetadataMedicalRoleHTTPController
from maleo_metadata.client.controllers.http.organization_type \
    import MaleoMetadataOrganizationTypeHTTPController
from maleo_metadata.client.controllers.http.service \
    import MaleoMetadataServiceHTTPController
from maleo_metadata.client.controllers.http.system_role \
    import MaleoMetadataSystemRoleHTTPController
from maleo_metadata.client.controllers.http.user_type \
    import MaleoMetadataUserTypeHTTPController
from maleo_metadata.client.controllers import (
    MaleoMetadataBloodTypeControllers,
    MaleoMetadataGenderControllers,
    MaleoMetadataMedicalRoleHTTPControllers,
    MaleoMetadataOrganizationTypeControllers,
    MaleoMetadataServiceControllers,
    MaleoMetadataSystemRoleControllers,
    MaleoMetadataUserTypeControllers,
    MaleoMetadataControllers
)
from maleo_metadata.client.services import (
    MaleoMetadataBloodTypeClientService,
    MaleoMetadataGenderClientService,
    MaleoMetadataMedicalRoleClientService,
    MaleoMetadataOrganizationTypeClientService,
    MaleoMetadataServiceClientService,
    MaleoMetadataSystemRoleClientService,
    MaleoMetadataUserTypeClientService,
    MaleoMetadataServices
)

class MaleoMetadataClientManager(MaleoClientManager):
    def __init__(self, service_manager:ServiceManager):
        key = service_manager.configs.client.maleo.metadata.key
        name = service_manager.configs.client.maleo.metadata.name
        url = service_manager.configs.client.maleo.metadata.url
        super().__init__(key, name, url, service_manager)
        self._initialize_controllers()
        self._initialize_services()
        self._logger.info("Client manager initialized successfully")

    def _initialize_controllers(self):
        super()._initialize_controllers()
        #* Blood type controllers
        blood_type_http_controller = MaleoMetadataBloodTypeHTTPController(
            service_manager=self.service_manager,
            manager=self._controller_managers.http
        )
        blood_type_controllers = MaleoMetadataBloodTypeControllers(
            http=blood_type_http_controller
        )
        #* Gender controllers
        gender_http_controller = MaleoMetadataGenderHTTPController(
            service_manager=self.service_manager,
            manager=self._controller_managers.http
        )
        gender_controllers = MaleoMetadataGenderControllers(
            http=gender_http_controller
        )
        #* Medical role controllers
        medical_role_http_controller = MaleoMetadataMedicalRoleHTTPController(
            service_manager=self.service_manager,
            manager=self._controller_managers.http
        )
        medical_role_controllers = MaleoMetadataMedicalRoleHTTPControllers(
            http=medical_role_http_controller
        )
        #* Organization type controllers
        organization_type_http_controller = MaleoMetadataOrganizationTypeHTTPController(
            service_manager=self.service_manager,
            manager=self._controller_managers.http
        )
        organization_type_controllers = MaleoMetadataOrganizationTypeControllers(
            http=organization_type_http_controller
        )
        #* Service controllers
        service_http_controller = MaleoMetadataServiceHTTPController(
            service_manager=self.service_manager,
            manager=self._controller_managers.http
        )
        service_controllers = MaleoMetadataServiceControllers(
            http=service_http_controller
        )
        #* System role controllers
        system_role_http_controller = MaleoMetadataSystemRoleHTTPController(
            service_manager=self.service_manager,
            manager=self._controller_managers.http
        )
        system_role_controllers = MaleoMetadataSystemRoleControllers(
            http=system_role_http_controller
        )
        #* User type controllers
        user_type_http_controller = MaleoMetadataUserTypeHTTPController(
            service_manager=self.service_manager,
            manager=self._controller_managers.http
        )
        user_type_controllers = MaleoMetadataUserTypeControllers(
            http=user_type_http_controller
        )
        #* All controllers
        self._controllers = MaleoMetadataControllers(
            blood_type=blood_type_controllers,
            gender=gender_controllers,
            medical_role=medical_role_controllers,
            organization_type=organization_type_controllers,
            service=service_controllers,
            system_role=system_role_controllers,
            user_type=user_type_controllers
        )

    @property
    def controllers(self) -> MaleoMetadataControllers:
        return self._controllers

    def _initialize_services(self):
        super()._initialize_services()
        blood_type_service = MaleoMetadataBloodTypeClientService(
            key=self._key,
            logger=self._logger,
            service_manager=self.service_manager,
            controllers=self._controllers.blood_type
        )
        gender_service = MaleoMetadataGenderClientService(
            key=self._key,
            logger=self._logger,
            service_manager=self.service_manager,
            controllers=self._controllers.gender
        )
        medical_role = MaleoMetadataMedicalRoleClientService(
            key=self._key,
            logger=self._logger,
            service_manager=self.service_manager,
            controllers=self._controllers.medical_role
        )
        organization_type_service = MaleoMetadataOrganizationTypeClientService(
            key=self._key,
            logger=self._logger,
            service_manager=self.service_manager,
            controllers=self._controllers.organization_type
        )
        service_service = MaleoMetadataServiceClientService(
            key=self._key,
            logger=self._logger,
            service_manager=self.service_manager,
            controllers=self._controllers.service
        )
        system_role_service = MaleoMetadataSystemRoleClientService(
            key=self._key,
            logger=self._logger,
            service_manager=self.service_manager,
            controllers=self._controllers.system_role
        )
        user_type_service = MaleoMetadataUserTypeClientService(
            key=self._key,
            logger=self._logger,
            service_manager=self.service_manager,
            controllers=self._controllers.user_type
        )
        self._services = MaleoMetadataServices(
            blood_type=blood_type_service,
            gender=gender_service,
            medical_role=medical_role,
            organization_type=organization_type_service,
            service=service_service,
            system_role=system_role_service,
            user_type=user_type_service
        )

    @property
    def services(self) -> MaleoMetadataServices:
        return self._services