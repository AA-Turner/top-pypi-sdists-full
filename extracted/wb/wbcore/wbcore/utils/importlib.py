def parse_signal_received_for_module(receiver_response) -> tuple[str, any]:
    for receiver, response in receiver_response:
        if response:
            yield receiver.__module__.split(".", 1)[0], response
