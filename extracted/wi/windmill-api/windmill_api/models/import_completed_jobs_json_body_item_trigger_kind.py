from enum import Enum


class ImportCompletedJobsJsonBodyItemTriggerKind(str, Enum):
    APP = "app"
    EMAIL = "email"
    GCP = "gcp"
    HTTP = "http"
    KAFKA = "kafka"
    NATS = "nats"
    POSTGRES = "postgres"
    SCHEDULE = "schedule"
    SQS = "sqs"
    UI = "ui"
    WEBHOOK = "webhook"
    WEBSOCKET = "websocket"

    def __str__(self) -> str:
        return str(self.value)
