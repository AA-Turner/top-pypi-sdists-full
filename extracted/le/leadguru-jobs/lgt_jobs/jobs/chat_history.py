from datetime import datetime, UTC
from abc import ABC
from typing import Optional, List
import logging as log
from lgt_jobs.lgt_common.slack_client.web_client import SlackWebClient
from lgt_jobs.lgt_data.models.bots.dedicated_bot import DedicatedBotModel
from lgt_jobs.lgt_data.models.chat.message import ChatMessage
from lgt_jobs.lgt_data.models.contacts.contact import UserContact
from lgt_jobs.lgt_data.mongo_repository import UserMongoRepository, DedicatedBotRepository, UserContactsRepository, \
    ChatRepository, UserLeadMongoRepository
from pydantic import BaseModel
from lgt_jobs.lgt_data.enums import SourceType
from lgt_jobs.runner import BaseBackgroundJob, BaseBackgroundJobData

"""
Load slack chat history
"""


class LoadChatHistoryJobData(BaseBackgroundJobData, BaseModel):
    user_id: str
    template_path: str = 'lgt_jobs/templates/new_message.html'


class LoadChatHistoryJob(BaseBackgroundJob, ABC):
    chat_repo = ChatRepository()
    contacts_repo = UserContactsRepository()
    user_leads_repo = UserLeadMongoRepository()

    @property
    def job_data_type(self) -> type:
        return LoadChatHistoryJobData

    def exec(self, data: LoadChatHistoryJobData):
        user = UserMongoRepository().get(data.user_id)
        bots = DedicatedBotRepository().get_all(only_valid=True, user_id=user.id, source_type=SourceType.SLACK)
        if not bots:
            return
        last_message = None
        last_message_contact = None
        contacts_groups = self.contacts_repo.find_grouped_actual_contacts(user.id, spam=False, with_chat_only=False)
        for bot in bots:
            contacts = contacts_groups.get(bot.source.source_id)
            if not contacts:
                continue

            for contact in contacts:
                message = self._update_history(contact=contact, bot=bot)

                if not message:
                    continue

                if not last_message:
                    last_message = message
                    last_message_contact = contact

                if message.created_at > last_message.created_at and message.user == contact.sender_id:
                    last_message = message
                    last_message_contact = contact

        last_notification = user.notification_settings.incoming_messages.last_notification
        has_to_be_notified = (not last_notification or (last_message and last_message.created_at > last_notification))
        if last_message and has_to_be_notified and last_message.user == last_message_contact.sender_id:
            user.notification_settings.incoming_messages.need_to_notify = True
            UserMongoRepository().set(data.user_id, notification_settings=user.notification_settings.to_dic())

    def _get_new_messages(self, contact: UserContact, bot: DedicatedBotModel, slack_chat: List[ChatMessage]):
        messages = self.chat_repo.get_list(sender_id=contact.sender_id, bot_id=bot.id)
        new_messages = []
        for message in slack_chat:
            same_messages = [msg for msg in messages if msg.id == message.id]
            if not same_messages:
                new_messages.append(message)
        return new_messages

    def _update_history(self, contact: UserContact, bot: DedicatedBotModel) -> Optional[ChatMessage]:
        slack_client = SlackWebClient(bot.token, bot.cookies)
        try:
            chat_id = slack_client.im_open(contact.sender_id).get('channel', {}).get('id')
            history = slack_client.chat_history(chat_id)
        except Exception as ex:
            log.error(f'[LoadChatHistoryJob]: Failed to load chat for the contact: {contact.id}. ERROR: {str(ex)}')
            return

        if not history['ok']:
            log.error(f'[LoadChatHistoryJob]: Failed to load chat for the contact: {contact.id}. '
                      f'ERROR: {history.get("error", "")}')
            return

        messages = history.get('messages', [])
        if not messages:
            return

        messages = [ChatMessage.from_slack_response(bot, m, contact.sender_id) for m in messages]
        new_messages = self._get_new_messages(contact, bot, messages)
        chat_history = [message.to_dic() for message in new_messages]
        self.chat_repo.upsert_messages(chat_history)
        if bot.associated_user != contact.sender_id and new_messages:
            log.info(f'[LoadChatHistoryJob]: New message. Sender id: {contact.sender_id}, bot id: {bot.id}')
            now = datetime.now(UTC)
            self.contacts_repo.update(contact.user_id, contact.sender_id, contact.source_id, last_message_at=now)
            self.user_leads_repo.update_many_by_sender_id(contact.sender_id, last_action_at=now)
            return new_messages[-1]

        return
