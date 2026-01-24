import threading

class ReaperForwardSession:
    is_forwarding = False
    stopping = threading.Event()
    schedules_ids_by_cluster: dict[str, list[str]] = {}