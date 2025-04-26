from montecarlodata.config import Config
from montecarlodata.errors import manage_errors
from montecarlodata.integrations.onboarding.base import BaseOnboardingService
from montecarlodata.integrations.onboarding.fields import (
    EXPECTED_PRESTO_SQL_GQL_RESPONSE_FIELD,
    PRESTO_CERT_PREFIX,
    PRESTO_SQL_CONNECTION_TYPE,
)
from montecarlodata.queries.onboarding import (
    TEST_PRESTO_CRED_MUTATION,
)


class PrestoOnboardingService(BaseOnboardingService):
    def __init__(self, config: Config, command_name: str, **kwargs):
        super().__init__(config, command_name=command_name, **kwargs)

    @manage_errors
    def onboard_presto_sql(self, **kwargs) -> None:
        """
        Onboard a presto-sql connection by validating and adding a connection.
        Also, optionally uploads a certificate to the DC bucket.
        """
        self.handle_cert(cert_prefix=PRESTO_CERT_PREFIX, options=kwargs)
        self.onboard(
            validation_query=TEST_PRESTO_CRED_MUTATION,
            validation_response=EXPECTED_PRESTO_SQL_GQL_RESPONSE_FIELD,
            connection_type=PRESTO_SQL_CONNECTION_TYPE,
            **kwargs,
        )
