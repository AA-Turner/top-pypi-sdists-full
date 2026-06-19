from enum import Enum


class ListDraftsResponse200ItemKind(str, Enum):
    APP = "app"
    DATA_PIPELINE = "data_pipeline"
    FLOW = "flow"
    RAW_APP = "raw_app"
    RESOURCE = "resource"
    SCRIPT = "script"
    TRIGGER_AZURE = "trigger_azure"
    TRIGGER_CLI = "trigger_cli"
    TRIGGER_DEFAULT_EMAIL = "trigger_default_email"
    TRIGGER_EMAIL = "trigger_email"
    TRIGGER_GCP = "trigger_gcp"
    TRIGGER_GITHUB = "trigger_github"
    TRIGGER_GOOGLE = "trigger_google"
    TRIGGER_HTTP = "trigger_http"
    TRIGGER_KAFKA = "trigger_kafka"
    TRIGGER_MQTT = "trigger_mqtt"
    TRIGGER_NATS = "trigger_nats"
    TRIGGER_NEXTCLOUD = "trigger_nextcloud"
    TRIGGER_POLL = "trigger_poll"
    TRIGGER_POSTGRES = "trigger_postgres"
    TRIGGER_SCHEDULE = "trigger_schedule"
    TRIGGER_SQS = "trigger_sqs"
    TRIGGER_WEBHOOK = "trigger_webhook"
    TRIGGER_WEBSOCKET = "trigger_websocket"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return str(self.value)
