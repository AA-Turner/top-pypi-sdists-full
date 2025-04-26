import typing as t

from connector.generated import (
    BasicCredential,
    StandardCapabilityName,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
    ValidatedCredentials,
)
from connector.oai.integration import DescriptionData, Integration
from connector.oai.modules.base_module import BaseIntegrationModule

Case: t.TypeAlias = tuple[
    Integration,
    BaseIntegrationModule,
]


def case_add_module() -> Case:
    integration = Integration(
        app_id="test",
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[],
        description_data=DescriptionData(
            user_friendly_name="test_modules_cases.py",
            categories=[],
        ),
    )

    class TestModule(BaseIntegrationModule):
        def register(self, integration: Integration):
            print("registered module")

    return integration, TestModule()


def case_register_module_capabilities() -> Case:
    integration = Integration(
        app_id="test",
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[],
        description_data=DescriptionData(
            user_friendly_name="test_modules_cases.py",
            categories=[],
        ),
    )

    class TestModuleWithCapabilities(BaseIntegrationModule):
        def register(self, integration: Integration):
            self.integration = integration
            self.register_capability()
            self.add_capability(StandardCapabilityName.VALIDATE_CREDENTIALS)

        def register_capability(self):
            @self.integration.register_capability(StandardCapabilityName.VALIDATE_CREDENTIALS)
            async def validate_credentials(
                args: ValidateCredentialsRequest,
            ) -> ValidateCredentialsResponse:
                return ValidateCredentialsResponse(
                    response=ValidatedCredentials(
                        valid=True,
                        unique_tenant_id="test",
                    )
                )

    return integration, TestModuleWithCapabilities()
