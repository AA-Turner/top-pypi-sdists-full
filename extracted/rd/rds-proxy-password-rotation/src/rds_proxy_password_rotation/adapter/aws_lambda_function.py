from dependency_injector.wiring import inject, Provide

from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.typing import LambdaContext

from rds_proxy_password_rotation.adapter.aws_lambda_function_model import AwsSecretManagerRotationEvent
from rds_proxy_password_rotation.adapter.container import Container
from rds_proxy_password_rotation.password_rotation_application import PasswordRotationApplication


container = None

@event_parser(model=AwsSecretManagerRotationEvent)
def lambda_handler(event: AwsSecretManagerRotationEvent, context: LambdaContext) -> None:
    global container

    if container is None:
        container = Container()
        container.wire(modules=[__name__])

    __call_application(event)

@inject
def __call_application(event: AwsSecretManagerRotationEvent, application: PasswordRotationApplication = Provide[Container.password_rotation_application]) -> None:
    application.rotate_secret(event.step.to_rotation_step(), event.secret_id, event.client_request_token)
