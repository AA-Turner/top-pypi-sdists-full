from enum import Enum


class ListMqttTriggersResponse200ItemSubscribeTopicsItemQos(str, Enum):
    QOS0 = "qos0"
    QOS1 = "qos1"
    QOS2 = "qos2"

    def __str__(self) -> str:
        return str(self.value)
