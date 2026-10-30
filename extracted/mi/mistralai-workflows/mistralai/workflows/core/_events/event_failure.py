from temporalio.exceptions import ApplicationError

from mistralai.workflows.core.config.config import config


def event_failure_message(error: BaseException | None) -> str:
    """Message to put in a failure event.

    A failure event's message is not a payload, so the event encoder does not encrypt it, and error
    messages often contain the data being processed. With full encryption, only the error type is reported.
    """
    if error is None or not config.worker.encrypts_payloads_fully:
        return str(error)
    if isinstance(error, ApplicationError) and error.type:
        return error.type
    return type(error).__name__
