from urllib.parse import urlencode

from higgsfield_client.types_ import (
    AnyJSON, Cancelled, Completed, Failed, InProgress, NSFW, Queued, Status, StatusEnum,
)

STATUS_MAPPER = {
    StatusEnum.QUEUED: Queued,
    StatusEnum.IN_PROGRESS: InProgress,
    StatusEnum.COMPLETED: Completed,
    StatusEnum.FAILED: Failed,
    StatusEnum.NSFW: NSFW,
    StatusEnum.CANCELED: Cancelled,
}


def get_status(data: AnyJSON) -> Status:
    try:
        status_value = data['status']
        status_enum = StatusEnum(status_value)
        status_class = STATUS_MAPPER[status_enum]
        return status_class()
    except (KeyError, ValueError):
        raise ValueError(
            f"Unknown status: {data.get('status', 'MISSING')}"
        )


def get_url(application: str, webhook_url: str) -> str:
    url = application

    if webhook_url is not None:
        url += '?' + urlencode({'hf_webhook': webhook_url})

    return url
