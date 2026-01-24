# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from datetime import datetime
import json
import uuid
import pathlib
from os import path
from contrast.reporting.teamserver_messages import BaseTsMessage
from requests.models import Response

from contrast_vendor import structlog as logging
from contrast.utils.decorators import fail_quietly

logger = logging.getLogger("contrast")


def get_message_body(msg):
    if isinstance(msg, BaseTsMessage):
        return msg.body
    if isinstance(msg, Response) and msg.status_code == 200:
        return msg.json()

    return {}


class RequestAudit:
    SUB_DIRS = ("requests", "responses")

    def __init__(self, config):
        self.config = config
        self.messages_path = ""

    @fail_quietly("Unable to prepare request_audit dirs")
    def prepare_dirs(self):
        # grab config request audit path, or the default, write /messages dir
        # create requests/response subdirs under message
        parent_path = self.config.get("api.request_audit.path")

        if "messages" in parent_path:
            self.messages_path = parent_path
        else:
            self.messages_path = path.join(parent_path, "messages")

        for sub_dir in self.SUB_DIRS:
            sub_path = path.join(self.messages_path, sub_dir)
            pathlib.Path(sub_path).mkdir(parents=True, exist_ok=True)

        logger.debug("Created request_audit dirs in %s", self.messages_path)

    def audit(self, msg, response):
        uid = uuid.uuid4().hex[:8]
        if self.config.get("api.request_audit.requests"):
            self.write_data(msg, "requests", msg.name, uid)

        if self.config.get("api.request_audit.responses"):
            self.write_data(response, "responses", msg.name, uid)

    @fail_quietly("Unable to write request audit data")
    def write_data(self, msg, msg_type, msg_name, uid):
        now = datetime.now()
        epoch = now.timestamp()
        day = now.strftime("%Y%m%d")
        time = f"{day}-{epoch}"

        file_name = f"{time}-{uid}-{msg_name}-teamserver.json"
        file_path = path.join(self.messages_path, msg_type, file_name)

        data = get_message_body(msg)

        # In the future, we'd like to somehow include status code + headers
        with pathlib.Path(file_path).open("w", encoding="UTF-8") as target:
            json.dump(data, target, indent=1)
