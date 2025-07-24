from uuid import UUID

import click

from montecarlodata.collector.validation import CollectorValidationService
from montecarlodata.common.echo_utils import echo_success_message
from montecarlodata.config import Config
from montecarlodata.errors import manage_errors, prompt_connection
from montecarlodata.integrations.onboarding.base import BaseOnboardingService
from montecarlodata.integrations.onboarding.fields import (
    CLICKHOUSE_DATABASE_TYPE,
    DREMIO_DATABASE_TYPE,
    MYSQL_DB_TYPE,
    ORACLE_DB_TYPE,
    SALESFORCE_CRM_DATABASE_TYPE,
    SALESFORCE_DATA_CLOUD_DATABASE_TYPE,
    TERADATA_DB_TYPE,
    TRANSACTIONAL_CONNECTION_TYPE,
    TRANSACTIONAL_WAREHOUSE_TYPE,
)


class TransactionalOnboardingService(CollectorValidationService, BaseOnboardingService):
    def __init__(self, config: Config, command_name: str, **kwargs):
        super().__init__(config, command_name=command_name, **kwargs)

    @manage_errors
    def onboard_transactional_db(self, **kwargs) -> None:
        """
        Onboard a Transactional DB connection by validating and adding a connection.
        """
        ssl_options = self.load_ssl_options(options=kwargs)
        if ssl_options:
            kwargs.setdefault("connection_settings", {})["ssl_options"] = ssl_options

        kwargs["connection_type"] = TRANSACTIONAL_CONNECTION_TYPE
        kwargs["warehouse_type"] = TRANSACTIONAL_WAREHOUSE_TYPE

        # These dbTypes have been promoted to their own connection type,
        # instead of being a 'transactional-db' connection type
        promoted_subtypes = [
            TERADATA_DB_TYPE,
            DREMIO_DATABASE_TYPE,
            ORACLE_DB_TYPE,
            MYSQL_DB_TYPE,
            SALESFORCE_CRM_DATABASE_TYPE,
            SALESFORCE_DATA_CLOUD_DATABASE_TYPE,
            CLICKHOUSE_DATABASE_TYPE,
        ]
        if kwargs.get("dbType") in promoted_subtypes:
            kwargs["connection_type"] = kwargs.get("dbType")
            kwargs["warehouse_type"] = kwargs.get("dbType")

        # Finds all v2 validations for this connection and runs each one.
        # If they all pass, return a temp credentials key
        # If the --skip-validations flag has been used, no validations are run and just a
        # temp key is returned
        key = self.test_new_credentials(**kwargs)

        # Add the connection
        if key:
            self.add_connection(key, **kwargs)
        else:
            click.Abort()

    @manage_errors
    def update_transactional_db(
        self,
        connection_id: UUID,
        skip_validation: bool,
        validate_only: bool,
        auto_yes: bool,
        connection_type: str,
        **kwargs,
    ) -> None:
        """
        Update a Transactional DB connection by validating and updating a connection.
        """
        ssl_options = self.load_ssl_options(options=kwargs)

        # Remove empty or null inputs. Also remove all ssl_* keys as these
        # will be passed under the 'ssl_options' dict.
        changes = {
            key: value
            for key, value in kwargs.items()
            if value is not None and value != {} and not key.startswith("ssl_")
        }

        if ssl_options:
            changes["ssl_options"] = ssl_options

        # Create a new temp credentials key for this connection with the changes
        key = self.create_update_credentials(
            changes=changes, connection_id=connection_id, connection_type=connection_type
        )

        # Run all validations for this connection using the new temp credentials key
        if not skip_validation:
            self.test_new_credentials_on_existing_connection(
                temp_key=key, connection_id=connection_id, connection_type=connection_type
            )

        # Update the connection with the new credentials key
        if not validate_only:
            prompt_connection(
                message="Validations passed! Would you like to continue?", skip_prompt=auto_yes
            )
            self.update_existing_connection(connection_id=connection_id, temp_key=key)
        else:
            echo_success_message(message="Validations passed!")
