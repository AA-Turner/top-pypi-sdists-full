import time
from abc import ABC
from random import randint
from typing import Optional, Any
from lgt_jobs.lgt_common.slack_client.web_client import SlackWebClient
from lgt_jobs.lgt_data.mongo_repository import DedicatedBotRepository
import logging as log
from pydantic import BaseModel
from lgt_jobs.basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
Send Slack Code
"""


class SendMassMessageSlackChannelJobData(BaseBackgroundJobData, BaseModel):
    text: str
    channel_ids: list[str]
    user_id: str
    files: Optional[list[Any]]
    source_id: str


class SendMassMessageSlackChannelJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return SendMassMessageSlackChannelJobData

    def exec(self, data: SendMassMessageSlackChannelJobData):
        bot = DedicatedBotRepository().get_one(user_id=data.user_id, source_id=data.source_id, only_valid=True)
        if not bot:
            log.warning(f"[SendMassMessageSlackChannelJob]: "
                        f"Bot not found or has invalid creds, source id:{data.source_id}")
            return

        slack_client = SlackWebClient(bot.token, bot.cookies)
        attempts = 0

        for channel in data.channel_ids:
            while attempts < 5:
                attempts += 1
                try:
                    post_message_response = slack_client.post_message(to=channel, text=data.text)
                    if not post_message_response['ok']:
                        log.warning(f"[SendMassMessageSlackChannelJob]: "
                                    f"Failed to post message. Attempt {attempts}, bot id {bot.id},"
                                    f" channel id {channel}. Details {post_message_response}")
                    attempts = 0
                    break
                except:
                    log.warning(f"[SendMassMessageSlackChannelJob]: "
                                f"Failed attempt to send message. Attempt {attempts}, bot id {bot.id}")
                    time.sleep(randint(1, 3))
