from logging import Logger

from sidecar.app_instance_identifier import AppInstanceIdentifier
from sidecar.app_instance_identifier_creator import IAppInstanceIdentifierCreator


class AwsAppInstanceIdentifierCreator(IAppInstanceIdentifierCreator):
    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)

    def create(self, app_name: str, instance_id: str) -> AppInstanceIdentifier:
        return AppInstanceIdentifier(name=app_name, infra_id=instance_id)
