from enum import Enum


class GetAssetsGraphResponse200TriggersItemType1TriggerKind(str, Enum):
    EMAIL = "email"
    GCP = "gcp"
    KAFKA = "kafka"
    MQTT = "mqtt"
    NATS = "nats"
    POSTGRES = "postgres"
    SCHEDULE = "schedule"
    SQS = "sqs"

    def __str__(self) -> str:
        return str(self.value)
