from csrd.message import Acknowledgement, Message


def test_message_defaults() -> None:
    msg = Message(topic="orders.created", payload={"id": "o-1"})

    assert msg.topic == "orders.created"
    assert msg.payload["id"] == "o-1"
    assert msg.headers == {}
    assert msg.timestamp is not None


def test_ack_values() -> None:
    assert Acknowledgement.ACK.value == "ack"
    assert Acknowledgement.RETRY.value == "retry"
    assert Acknowledgement.REJECT.value == "reject"
