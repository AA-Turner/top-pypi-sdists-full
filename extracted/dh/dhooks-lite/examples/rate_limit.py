import logging
import os
from time import sleep

from dhooks_lite import Webhook

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

if "DISCORD_WEBHOOK_URL" not in os.environ:
    raise ValueError('mandatory environment variable "DISCORD_WEBHOOK_URL" not set')
else:
    DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# bulk sending messages with rate limiting detection
hook = Webhook(DISCORD_WEBHOOK_URL)
max_runs = 20
for x in range(max_runs):
    response = hook.execute(
        "Hello, World! {} / {}".format(x + 1, max_runs), wait_for_response=True
    )
    if response.status_code == 429:
        retry_after = response.content["retry_after"] / 1000
        logging.warn("rate limited - retry after {}".format(retry_after))
        sleep(retry_after)
