from enum import StrEnum

class LiveTranscriptEnvelopeDtoEventsItemEventType(StrEnum):
    DONE = "done"
    ERROR = "error"
    EVENT = "event"
    INPUT_DELIVERED = "input_delivered"
    LAUNCHED = "launched"
    OBSERVATION = "observation"
    PROCESS_EXITED = "process_exited"
    SETUP_COMPLETED = "setup_completed"
    SETUP_STARTED = "setup_started"
    SNAPSHOTTING = "snapshotting"
    STARTED = "started"
    STDERR = "stderr"
    STDOUT = "stdout"

    def __str__(self) -> str:
        return str(self.value)
