from abc import ABC
from typing import Optional
import logging as log
from lgt_jobs.lgt_common.slack_client.web_client import SlackWebClient
from lgt_jobs.lgt_data.models.chat.message import ChatMessage
from lgt_jobs.lgt_data.mongo_repository import DedicatedBotRepository, ChatRepository
from pydantic import BaseModel
from lgt_jobs.basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
Send Slack Message
"""


class SendSlackMessageJobData(BaseBackgroundJobData, BaseModel):
    sender_id: str
    bot_id: str
    text: Optional[str]
    files_ids: Optional[list] = []


class SendSlackMessageJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return SendSlackMessageJobData

    def exec(self, data: SendSlackMessageJobData):
        bot = DedicatedBotRepository().get_one(id=data.bot_id)
        if not bot:
            return

        slack_client = SlackWebClient(bot.token, bot.cookies)
        im = slack_client.im_open(data.sender_id)
        if not im['ok']:
            log.warning(f"Unable to open im with user: {data.sender_id}")
            return

        channel_id = im['channel']['id']
        if data.files_ids:
            resp = slack_client.share_files(data.files_ids, channel_id, data.text)
        else:
            resp = slack_client.post_message(channel_id, data.text)

        message = resp.get('message') if 'message' in resp \
            else slack_client.conversation_replies(channel_id, resp['file_msg_ts'])['messages'][0]

        message_model: ChatMessage = ChatMessage().from_slack_response(bot, message, data.sender_id)
        message_model.viewed = True
        ChatRepository().upsert_messages([message_model.to_dic()])
