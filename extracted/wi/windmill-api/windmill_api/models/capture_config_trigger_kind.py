from enum import Enum


class CaptureConfigTriggerKind(str, Enum):
    EMAIL = "email"
    GCP = "gcp"
    HTTP = "http"
    KAFKA = "kafka"
    MQTT = "mqtt"
    NATS = "nats"
    POSTGRES = "postgres"
    SQS = "sqs"
    WEBHOOK = "webhook"
    WEBSOCKET = "websocket"

    def __str__(self) -> str:
        return str(self.value)
