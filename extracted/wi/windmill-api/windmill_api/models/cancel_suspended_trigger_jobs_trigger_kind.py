from enum import Enum


class CancelSuspendedTriggerJobsTriggerKind(str, Enum):
    AMQP = "amqp"
    APP = "app"
    ASSET = "asset"
    AZURE = "azure"
    DEFAULT_EMAIL = "default_email"
    EMAIL = "email"
    FRESHNESS = "freshness"
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
    UI = "ui"
    WEBHOOK = "webhook"
    WEBSOCKET = "websocket"

    def __str__(self) -> str:
        return str(self.value)
