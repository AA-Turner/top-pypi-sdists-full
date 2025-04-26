from pycarlo.core import Client

from montecarlodata.collector.validation import CollectorValidationService
from montecarlodata.config import Config
from montecarlodata.errors import manage_errors
from montecarlodata.integrations.onboarding.base import BaseOnboardingService
from montecarlodata.integrations.onboarding.fields import (
    EXPECTED_ADD_ETL_CONNECTION_RESPONSE_FIELD,
    INFORMATICA_CONNECTION_TYPE,
)
from montecarlodata.queries.onboarding import ADD_ETL_CONNECTION_MUTATION


class InformaticaOnboardingService(BaseOnboardingService):
    def __init__(self, config: Config, mc_client: Client, command_name: str, **kwargs):
        super().__init__(config, command_name, **kwargs)
        self._validation_service = CollectorValidationService(
            config=config,
            mc_client=mc_client,
            user_service=self._user_service,
            request_wrapper=self._request_wrapper,
            command_name=self._command_name,
        )

    @manage_errors
    def onboard(self, **kwargs) -> None:
        # run validations and store credentials (if passed)
        key = self._validation_service.test_new_credentials(
            connection_type=INFORMATICA_CONNECTION_TYPE,
            **kwargs,
        )
        if key:
            # create ETL connection
            self.add_connection(
                connection_type=INFORMATICA_CONNECTION_TYPE,
                connection_query=ADD_ETL_CONNECTION_MUTATION,
                connection_response=EXPECTED_ADD_ETL_CONNECTION_RESPONSE_FIELD,
                etl_name=kwargs.pop("name"),
                key=key,
                **kwargs,
            )
