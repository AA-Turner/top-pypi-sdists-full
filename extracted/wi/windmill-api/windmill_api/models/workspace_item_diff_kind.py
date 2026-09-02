from enum import Enum


class WorkspaceItemDiffKind(str, Enum):
    AMQP_TRIGGER = "amqp_trigger"
    APP = "app"
    AZURE_TRIGGER = "azure_trigger"
    EMAIL_TRIGGER = "email_trigger"
    FLOW = "flow"
    FOLDER = "folder"
    GCP_TRIGGER = "gcp_trigger"
    HTTP_TRIGGER = "http_trigger"
    KAFKA_TRIGGER = "kafka_trigger"
    MQTT_TRIGGER = "mqtt_trigger"
    NATS_TRIGGER = "nats_trigger"
    POSTGRES_TRIGGER = "postgres_trigger"
    RAW_APP = "raw_app"
    RESOURCE = "resource"
    RESOURCE_TYPE = "resource_type"
    SCHEDULE = "schedule"
    SCRIPT = "script"
    SQS_TRIGGER = "sqs_trigger"
    VARIABLE = "variable"
    WEBSOCKET_TRIGGER = "websocket_trigger"

    def __str__(self) -> str:
        return str(self.value)
