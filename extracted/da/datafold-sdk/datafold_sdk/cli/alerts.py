import logging
import time
import sys
from typing import Optional

from datetime import datetime
import click

from datafold_sdk.sdk.utils import prepare_api_url, prepare_headers, post_data, get_data
from datafold_sdk import sdk_log

logger = logging.getLogger(__file__)
logger.addHandler(sdk_log.SDKLogHandler())

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
# Docs: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
# %Y – Year with century as a decimal number.
# %m – Month as a zero-padded decimal number.
# %d – Day of the month as a zero-padded decimal number.
# %H – Hour (24-hour clock) as a zero-padded decimal number.
# %M – Minute as a zero-padded decimal number.
# %S – Second as a zero-padded decimal number.
# %f – Microsecond as a decimal number, zero-padded on the left.
# %z – UTC offset in the form +HH:MM or -HH:MM (empty string if the the object is naive).


@click.group()
def manager():
    """Run datafold queries --help for Alerts/Monitors management."""


@manager.command()
@click.option('--id', 'alert_id', type=int, required=True)
@click.option('--wait', type=int, default=None,
              help="How long to wait for the alert (seconds).")
@click.option('--interval', type=click.IntRange(1, 60), default=3,
              help="How often to poll for the alert result (seconds).")
@click.pass_context
def run(ctx: click.Context, alert_id: int, wait: Optional[int], interval: int):
    """ Run the alert query, trigger the notifications. """
    headers = prepare_headers(ctx.obj.api_key)

    api_segment = f"api/v1/alerts/{alert_id}/checks"
    url = prepare_api_url(ctx.obj.host, api_segment)
    resp = post_data(url, json_data={}, headers=headers)
    data = resp.json()
    result_id = data['id']
    logger.debug(f"API response={data!r}")

    started = time.monotonic()
    last_status: Optional[str] = None
    while wait and time.monotonic() < started + wait:
        # Sleep first, as it is never done immediately on creation.
        remaining_time = started + wait - time.monotonic()
        time.sleep(min(float(interval), remaining_time))

        api_segment = f"api/v1/alerts/{alert_id}/results/{result_id}"
        url = prepare_api_url(ctx.obj.host, api_segment)
        resp = get_data(url, headers=headers)
        data = resp.json()
        last_status = data['status']
        logger.debug(f"API response={data!r}")

        if last_status in ["done", "failed"]:
            break

    if last_status in ["done", "failed"]:
        logger.info(f"Finished a run {result_id} for the alert {alert_id}: status={last_status}")

        if wait and last_status == 'done':
            api_result = f"api/v1/alerts/{alert_id}"
            url = prepare_api_url(ctx.obj.host, api_result)
            resp = get_data(url, headers=headers)
            data = resp.json()
            logger.debug(f"API response={data!r}")
            # If there is no trigger, then last_triggered will be null
            if data['last_triggered']:
                last_triggered = datetime.strptime(data['last_triggered']['value'], DATE_FORMAT)
                last_run = datetime.strptime(data['last_run']['value'], DATE_FORMAT)
                if last_triggered >= last_run:
                    # The alert triggered, so we should error
                    logger.warning(f"The alert triggered, check for details: {ctx.obj.host}/query_alerts/{alert_id}")
                    sys.exit(22)

        if last_status == 'failed':
            sys.exit(22)

    elif wait:
        logger.warning(f"Timed out waiting for a run {result_id} for the alert {alert_id}. "
                       "It is still running, but we do not wait.")
    else:
        logger.warning(f"Started a run {result_id} for the alert {alert_id}.")
