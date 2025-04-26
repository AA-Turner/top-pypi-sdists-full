from typing import TYPE_CHECKING, Any, List, Literal, Mapping, Optional, Union

from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sink._models import SinkIntegrationProtocol
from chalk.streams.base import StreamSource
from chalk.utils.duration import Duration
from chalk.utils.string import comma_join, comma_whitespace_split

if TYPE_CHECKING:
    import pydantic
    from pydantic import BaseModel
else:
    try:
        import pydantic.v1 as pydantic
        from pydantic.v1 import BaseModel
    except ImportError:
        import pydantic
        from pydantic import BaseModel


_KAFKA_BOOTSTRAP_SERVER_NAME = "KAFKA_BOOTSTRAP_SERVER"
_KAFKA_TOPIC_NAME = "KAFKA_TOPIC"
_KAFKA_SSL_KEYSTORE_LOCATION_NAME = "KAFKA_SSL_KEYSTORE_LOCATION"
_KAFKA_SSL_CA_FILE_NAME = "KAFKA_SSL_CA_FILE"
_KAFKA_CLIENT_ID_PREFIX_NAME = "KAFKA_CLIENT_ID_PREFIX"
_KAFKA_GROUP_ID_PREFIX_NAME = "KAFKA_GROUP_ID_PREFIX"
_KAFKA_SECURITY_PROTOCOL_NAME = "KAFKA_SECURITY_PROTOCOL"
_KAFKA_SASL_MECHANISM_NAME = "KAFKA_SASL_MECHANISM"
_KAFKA_SASL_USERNAME_NAME = "KAFKA_SASL_USERNAME"
_KAFKA_SASL_PASSWORD_NAME = "KAFKA_SASL_PASSWORD"


class KafkaSource(StreamSource, SinkIntegrationProtocol, BaseModel, frozen=True):
    bootstrap_server: Optional[Union[str, List[str]]] = None
    """The URL of one of your Kafka brokers from which to fetch initial metadata about your Kafka cluster"""

    topic: Optional[str] = None
    """The name of the topic to subscribe to."""

    ssl_keystore_location: Optional[str] = None
    """
    An S3 or GCS URI that points to the keystore file that should be
    used for brokers. You must configure the appropriate AWS or
    GCP integration in order for Chalk to be able to access these
    files.
    """

    ssl_ca_file: Optional[str] = None
    """
    An S3 or GCS URI that points to the certificate authority file that should be
    used to verify broker certificates. You must configure the appropriate AWS or
    GCP integration in order for Chalk to be able to access these files.
    """

    client_id_prefix: str = "chalk/"
    group_id_prefix: str = "chalk/"

    security_protocol: Literal["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"] = "PLAINTEXT"
    """
    Protocol used to communicate with brokers.
    Valid values are `"PLAINTEXT"`, `"SSL"`, `"SASL_PLAINTEXT"`, and `"SASL_SSL"`.
    Defaults to `"PLAINTEXT"`.
    """

    sasl_mechanism: Literal["PLAIN", "GSSAPI", "SCRAM-SHA-256", "SCRAM-SHA-512", "OAUTHBEARER"] = "PLAIN"
    """
    Authentication mechanism when `security_protocol`
    is configured for SASL_PLAINTEXT or SASL_SSL.
    Valid values are `"PLAIN"`, `"GSSAPI"`, `"SCRAM-SHA-256"`, `"SCRAM-SHA-512"`, `"OAUTHBEARER"`.
    Defaults to `"PLAIN"`.
    """

    sasl_username: Optional[str] = None
    """
    Username for SASL PLAIN, SCRAM-SHA-256, or SCRAM-SHA-512 authentication.
    """

    sasl_password: Optional[str] = pydantic.Field(default=None, repr=False)
    """
    Password for SASL PLAIN, SCRAM-SHA-256, or SCRAM-SHA-512 authentication.
    """

    name: Optional[str] = None
    """
    The name of the integration, as configured in your Chalk Dashboard.
    """

    late_arrival_deadline: Duration = "infinity"
    """
    Messages older than this deadline will not be processed.
    """

    dead_letter_queue_topic: Optional[str] = None
    """
    Kafka topic to send messages when message processing fails
    """

    def __init__(
        self,
        *,
        bootstrap_server: Optional[Union[str, List[str]]] = None,
        topic: Optional[str] = None,
        ssl_keystore_location: Optional[str] = None,
        ssl_ca_file: Optional[str] = None,
        client_id_prefix: Optional[str] = None,
        group_id_prefix: Optional[str] = None,
        security_protocol: Optional[str] = None,
        sasl_mechanism: Optional[Literal["PLAIN", "GSSAPI", "SCRAM-SHA-256", "SCRAM-SHA-512", "OAUTHBEARER"]] = None,
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
        name: Optional[str] = None,
        late_arrival_deadline: Duration = "infinity",
        dead_letter_queue_topic: Optional[str] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        super(KafkaSource, self).__init__(
            bootstrap_server=bootstrap_server
            or load_integration_variable(
                name=_KAFKA_BOOTSTRAP_SERVER_NAME,
                integration_name=name,
                parser=comma_whitespace_split,
                override=integration_variable_override,
            ),
            topic=topic
            or load_integration_variable(
                name=_KAFKA_TOPIC_NAME, integration_name=name, override=integration_variable_override
            ),
            ssl_keystore_location=ssl_keystore_location
            or load_integration_variable(
                name=_KAFKA_SSL_KEYSTORE_LOCATION_NAME, integration_name=name, override=integration_variable_override
            ),
            client_id_prefix=client_id_prefix
            or load_integration_variable(
                name=_KAFKA_CLIENT_ID_PREFIX_NAME, integration_name=name, override=integration_variable_override
            )
            or KafkaSource.__fields__["client_id_prefix"].default,
            group_id_prefix=group_id_prefix
            or load_integration_variable(
                name=_KAFKA_GROUP_ID_PREFIX_NAME, integration_name=name, override=integration_variable_override
            )
            or KafkaSource.__fields__["group_id_prefix"].default,
            security_protocol=security_protocol
            or load_integration_variable(
                name=_KAFKA_SECURITY_PROTOCOL_NAME, integration_name=name, override=integration_variable_override
            )
            or KafkaSource.__fields__["security_protocol"].default,
            sasl_mechanism=sasl_mechanism
            or load_integration_variable(
                name=_KAFKA_SASL_MECHANISM_NAME, integration_name=name, override=integration_variable_override
            )
            or KafkaSource.__fields__["sasl_mechanism"].default,
            sasl_username=sasl_username
            or load_integration_variable(
                name=_KAFKA_SASL_USERNAME_NAME, integration_name=name, override=integration_variable_override
            ),
            sasl_password=sasl_password
            or load_integration_variable(
                name=_KAFKA_SASL_PASSWORD_NAME, integration_name=name, override=integration_variable_override
            ),
            name=name,
            late_arrival_deadline=late_arrival_deadline,
            dead_letter_queue_topic=dead_letter_queue_topic,
            ssl_ca_file=ssl_ca_file
            or load_integration_variable(
                name=_KAFKA_SSL_CA_FILE_NAME, integration_name=name, override=integration_variable_override
            ),
        )
        self.registry.append(self)

    def config_to_json(self) -> Any:
        return self.json()

    @property
    def streaming_type(self) -> str:
        return "kafka"

    @property
    def dlq_name(self) -> Union[str, None]:
        return self.dead_letter_queue_topic

    @property
    def stream_or_topic_name(self):
        assert self.topic is not None
        return self.topic

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(
                    _KAFKA_BOOTSTRAP_SERVER_NAME, self.name, self.bootstrap_server, serializer=comma_join
                ),
                create_integration_variable(_KAFKA_TOPIC_NAME, self.name, self.topic),
                create_integration_variable(_KAFKA_SSL_KEYSTORE_LOCATION_NAME, self.name, self.ssl_keystore_location),
                create_integration_variable(_KAFKA_SSL_CA_FILE_NAME, self.name, self.ssl_ca_file),
                create_integration_variable(_KAFKA_CLIENT_ID_PREFIX_NAME, self.name, self.client_id_prefix),
                create_integration_variable(_KAFKA_GROUP_ID_PREFIX_NAME, self.name, self.group_id_prefix),
                create_integration_variable(_KAFKA_SECURITY_PROTOCOL_NAME, self.name, self.security_protocol),
                create_integration_variable(_KAFKA_SASL_MECHANISM_NAME, self.name, self.sasl_mechanism),
                create_integration_variable(_KAFKA_SASL_USERNAME_NAME, self.name, self.sasl_username),
                create_integration_variable(_KAFKA_SASL_PASSWORD_NAME, self.name, self.sasl_password),
            ]
            if v is not None
        }
