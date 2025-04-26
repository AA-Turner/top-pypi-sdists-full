from typing import TYPE_CHECKING, Any, Mapping, Optional, Union

from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.streams.base import StreamSource
from chalk.utils.duration import Duration

if TYPE_CHECKING:
    from pydantic import BaseModel
else:
    try:
        import pydantic.v1 as pydantic
        from pydantic.v1 import BaseModel
    except ImportError:
        import pydantic
        from pydantic import BaseModel

_KINESIS_STREAM_NAME_NAME = "KINESIS_STREAM_NAME"
_KINESIS_STREAM_ARN_NAME = "KINESIS_STREAM_ARN"
_KINESIS_REGION_NAME_NAME = "KINESIS_REGION_NAME"
_KINESIS_LATE_ARRIVAL_DEADLINE_NAME = "KINESIS_LATE_ARRIVAL_DEADLINE"
_KINESIS_DEAD_LETTER_QUEUE_STREAM_NAME_NAME = "KINESIS_DEAD_LETTER_QUEUE_STREAM_NAME"
_KINESIS_AWS_ACCESS_KEY_ID_NAME = "KINESIS_AWS_ACCESS_KEY_ID"
_KINESIS_AWS_SECRET_ACCESS_KEY_NAME = "KINESIS_AWS_SECRET_ACCESS_KEY"
_KINESIS_AWS_SESSION_TOKEN_NAME = "KINESIS_AWS_SESSION_TOKEN"
_KINESIS_ENDPOINT_URL_NAME = "KINESIS_ENDPOINT_URL"
_KINESIS_CONSUMER_ROLE_ARN_NAME = "KINESIS_CONSUMER_ROLE_ARN"


class KinesisSource(StreamSource, BaseModel, frozen=True):
    stream_name: Optional[str] = None
    """The name of your stream. Either this or the stream_arn must be specified"""

    stream_arn: Optional[str] = None
    """The ARN of your stream. Either this or the stream_name must be specified"""

    region_name: Optional[str] = None
    """
    AWS region string, e.g. "us-east-2"
    """

    name: Optional[str] = None
    """
    The name of the integration, as configured in your Chalk Dashboard.
    """

    late_arrival_deadline: Duration = "infinity"
    """
    Messages older than this deadline will not be processed.
    """

    dead_letter_queue_stream_name: Optional[str] = None
    """
    Kinesis stream name to send messages when message processing fails
    """

    aws_access_key_id: Optional[str] = None
    """
    AWS access key id credential
    """

    aws_secret_access_key: Optional[str] = None
    """
    AWS secret access key credential
    """

    aws_session_token: Optional[str] = None
    """
    AWS access key id credential
    """

    endpoint_url: Optional[str] = None
    """
    optional endpoint to hit Kinesis server
    """

    consumer_role_arn: Optional[str] = None
    """
    Optional role ARN for the consumer to assume
    """

    def __init__(
        self,
        *,
        region_name: Optional[str] = None,
        stream_name: Optional[str] = None,
        stream_arn: Optional[str] = None,
        late_arrival_deadline: Duration = "infinity",
        dead_letter_queue_stream_name: Optional[str] = None,
        name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        consumer_role_arn: Optional[str] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        super(KinesisSource, self).__init__(
            name=name,
            stream_name=stream_name
            or load_integration_variable(
                name=_KINESIS_STREAM_NAME_NAME, integration_name=name, override=integration_variable_override
            )
            or KinesisSource.__fields__["stream_name"].default,
            stream_arn=stream_arn
            or load_integration_variable(
                name=_KINESIS_STREAM_ARN_NAME, integration_name=name, override=integration_variable_override
            )
            or KinesisSource.__fields__["stream_arn"].default,
            late_arrival_deadline=late_arrival_deadline
            or load_integration_variable(
                name=_KINESIS_LATE_ARRIVAL_DEADLINE_NAME, integration_name=name, override=integration_variable_override
            )
            or KinesisSource.__fields__["late_arrival_deadline"].default,
            dead_letter_queue_stream_name=dead_letter_queue_stream_name
            or load_integration_variable(
                name=_KINESIS_DEAD_LETTER_QUEUE_STREAM_NAME_NAME,
                integration_name=name,
                override=integration_variable_override,
            )
            or KinesisSource.__fields__["dead_letter_queue_stream_name"].default,
            aws_access_key_id=aws_access_key_id
            or load_integration_variable(
                name=_KINESIS_AWS_ACCESS_KEY_ID_NAME, integration_name=name, override=integration_variable_override
            )
            or KinesisSource.__fields__["aws_access_key_id"].default,
            aws_secret_access_key=aws_secret_access_key
            or load_integration_variable(
                name=_KINESIS_AWS_SECRET_ACCESS_KEY_NAME, integration_name=name, override=integration_variable_override
            )
            or KinesisSource.__fields__["aws_secret_access_key"].default,
            aws_session_token=aws_session_token
            or load_integration_variable(
                name=_KINESIS_AWS_SESSION_TOKEN_NAME, integration_name=name, override=integration_variable_override
            )
            or KinesisSource.__fields__["aws_session_token"].default,
            region_name=region_name
            or load_integration_variable(
                name=_KINESIS_REGION_NAME_NAME, integration_name=name, override=integration_variable_override
            )
            or KinesisSource.__fields__["region_name"].default,
            endpoint_url=endpoint_url
            or load_integration_variable(
                name=_KINESIS_ENDPOINT_URL_NAME, integration_name=name, override=integration_variable_override
            )
            or KinesisSource.__fields__["endpoint_url"].default,
            consumer_role_arn=consumer_role_arn
            or load_integration_variable(
                name=_KINESIS_CONSUMER_ROLE_ARN_NAME, integration_name=name, override=integration_variable_override
            )
            or KinesisSource.__fields__["consumer_role_arn"].default,
        )
        self.registry.append(self)

    def config_to_json(self) -> Any:
        return self.json()

    @property
    def streaming_type(self) -> str:
        return "kinesis"

    @property
    def dlq_name(self) -> Union[str, None]:
        return self.dead_letter_queue_stream_name

    @property
    def stream_or_topic_name(self) -> str:
        assert self.stream_name is not None
        return self.stream_name

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_KINESIS_STREAM_NAME_NAME, self.name, self.stream_name),
                create_integration_variable(_KINESIS_STREAM_ARN_NAME, self.name, self.stream_arn),
                create_integration_variable(_KINESIS_REGION_NAME_NAME, self.name, self.region_name),
                create_integration_variable(_KINESIS_LATE_ARRIVAL_DEADLINE_NAME, self.name, self.late_arrival_deadline),
                create_integration_variable(
                    _KINESIS_DEAD_LETTER_QUEUE_STREAM_NAME_NAME, self.name, self.dead_letter_queue_stream_name
                ),
                create_integration_variable(_KINESIS_AWS_ACCESS_KEY_ID_NAME, self.name, self.aws_access_key_id),
                create_integration_variable(_KINESIS_AWS_SECRET_ACCESS_KEY_NAME, self.name, self.aws_secret_access_key),
                create_integration_variable(_KINESIS_AWS_SESSION_TOKEN_NAME, self.name, self.aws_session_token),
                create_integration_variable(_KINESIS_ENDPOINT_URL_NAME, self.name, self.endpoint_url),
                create_integration_variable(_KINESIS_CONSUMER_ROLE_ARN_NAME, self.name, self.consumer_role_arn),
            ]
            if v is not None
        }
