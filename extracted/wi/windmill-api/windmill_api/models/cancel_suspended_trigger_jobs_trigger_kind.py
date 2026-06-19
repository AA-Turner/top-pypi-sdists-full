from enum import Enum


class CancelSuspendedTriggerJobsTriggerKind(str, Enum):
    ASSET = "asset"
    AZURE = "azure"
    DEFAULT_EMAIL = "default_email"
    EMAIL = "email"
    GCP = "gcp"
    GITHUB = "github"
    GOOGLE = "google"
    HTTP = "http"
    KAFKA = "kafka"
    MQTT = "mqtt"
    NATS = "nats"
    POSTGRES = "postgres"
    SCHEDULE = "schedule"
    SQS = "sqs"
    WEBHOOK = "webhook"
    WEBSOCKET = "websocket"

    def __str__(self) -> str:
        return str(self.value)
