from enum import Enum


class GetGranularAclsKind(str, Enum):
    APP = "app"
    EMAIL_TRIGGER = "email_trigger"
    FLOW = "flow"
    FOLDER = "folder"
    GCP_TRIGGER = "gcp_trigger"
    GROUP = "group_"
    HTTP_TRIGGER = "http_trigger"
    KAFKA_TRIGGER = "kafka_trigger"
    MQTT_TRIGGER = "mqtt_trigger"
    NATS_TRIGGER = "nats_trigger"
    POSTGRES_TRIGGER = "postgres_trigger"
    RAW_APP = "raw_app"
    RESOURCE = "resource"
    SCHEDULE = "schedule"
    SCRIPT = "script"
    SQS_TRIGGER = "sqs_trigger"
    VARIABLE = "variable"
    WEBSOCKET_TRIGGER = "websocket_trigger"

    def __str__(self) -> str:
        return str(self.value)
