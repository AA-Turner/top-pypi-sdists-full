import json
from logging import Logger

import requests


def send_slack_message(
    message: str,
    webhook_url: str | None = None,
    logger: Logger | None = None,
    post_timout: int = 30,
    raise_on_error: bool = True,
) -> None:
    """
    Send slack message via slack webhook url.

    Args:
        message (str): message to send.
        webhook_url (str): slack webhook url.
        logger (Logger): logger to use, if not passed no logs will be displayed.
        post_timout (int): Timeout in seconds to send to request.post.
        raise_on_error (bool): Raise exception if error.
    """
    try:
        if webhook_url:
            slack_data = {"text": message}
            if logger:
                logger.info(f"Sending message to slack: {message}")

            response = requests.post(
                webhook_url,
                data=json.dumps(slack_data),
                headers={"Content-Type": "application/json"},
                timeout=post_timout,
            )
            if response.status_code != 200 and logger:
                logger.error(
                    f"Request to slack returned an error {response.status_code} with the following message: {response.text}"
                )
    except Exception as ex:
        if logger:
            logger.error(f"Failed to send slack message. error: {ex}")

        if raise_on_error:
            raise
