import logging as log
from abc import ABC

from pydantic import BaseModel
from requests import exceptions

from lgt_jobs import BackgroundJobRunner
from lgt_jobs.basejobs import BaseBackgroundJob, BaseBackgroundJobData
from lgt_jobs.env import v3_background_job_topic
from lgt_jobs.lgt_common.slack_client.web_client import SlackWebClient
from lgt_jobs.lgt_data.models.bots.dedicated_bot import DedicatedBotModel
from lgt_jobs.lgt_data.models.chat.request import MessageRequest
from lgt_jobs.lgt_data.models.people.people import SlackMemberInformation
from lgt_jobs.lgt_data.models.user.user import UserModel
from lgt_jobs.lgt_data.mongo_repository import UserMongoRepository, DedicatedBotRepository, \
    SlackContactUserRepository, UserContactsRepository, MessageRequestsRepository

"""
Save inbox leads
"""


class InboxLeadsJobData(BaseBackgroundJobData, BaseModel):
    pass


class InboxLeadsJob(BaseBackgroundJob, ABC):

    @property
    def job_data_type(self) -> type:
        return InboxLeadsJobData

    def exec(self, _: InboxLeadsJobData):
        users = UserMongoRepository().get_users()
        for user in users:
            log.info(f'[InboxLeadsJob]: Loading chat for the: {user.email}')
            dedicated_bots = DedicatedBotRepository().get_all(only_valid=True, user_id=user.id)
            for dedicated_bot in dedicated_bots:
                self.create_inbox_leads(user, dedicated_bot)

    @classmethod
    def create_inbox_leads(cls, user: UserModel, dedicated_bot: DedicatedBotModel):
        slack_client = SlackWebClient(dedicated_bot.token, dedicated_bot.cookies)
        attempt = 0
        conversations_list = []
        while attempt < 3:
            try:
                conversations_list = slack_client.get_im_list().get('channels', [])
                break
            except exceptions.JSONDecodeError as er:
                log.info(f'[InboxLeadsJob]: Loading chat failed for the: {dedicated_bot.id}. '
                         f'Attempt: {attempt}. {str(er)}')
                attempt += 1

        log.info(f'[InboxLeadsJob]: Loading chat for the: {dedicated_bot.id}. '
                 f'Count of chats: {len(conversations_list)}')
        for conversation in conversations_list:
            sender_id = conversation.get('user')
            im_id = conversation.get('id')
            if sender_id == "USLACKBOT":
                continue

            history = {}
            while attempt < 3:
                try:
                    history = slack_client.chat_history(im_id)
                    break
                except exceptions.JSONDecodeError as er:
                    log.info(f'[InboxLeadsJob]: Loading chat failed for the: {dedicated_bot.id}. '
                             f'Attempt: {attempt}. {str(er)}')
                    attempt += 1

            if not history.get('ok', False):
                log.warning(f'Failed to load chat for the: {dedicated_bot.id}. ERROR: {history.get("error", "")}')
                continue

            messages = history.get('messages', [])
            messages = [msg for msg in messages if not cls.is_call_related_event(msg)]
            log.info(f'[InboxLeadsJob]: Count of messages: {len(messages)} with {sender_id}')
            if messages:
                user_contact = UserContactsRepository().find_one(user.id, sender_id=sender_id)
                if not user_contact:
                    people = SlackContactUserRepository().find_one(sender_id)
                    if not people:
                        slack_profile = slack_client.get_profile(sender_id).get('user')
                        InboxLeadsJob.create_people(slack_profile, dedicated_bot)
                    request = MessageRequest.from_slack_response(dedicated_bot, messages[0], sender_id)
                    if request.is_system_message:
                        continue
                    if cls._is_request_answered(messages, dedicated_bot.associated_user):
                        cls.detect_answer_in_requests(sender_id, dedicated_bot.source.source_id, user)
                    else:
                        cls.detect_unanswered_request(request, sender_id, user)

    @staticmethod
    def create_people(slack_profile: dict, dedicated_bot: DedicatedBotModel):
        member_info: SlackMemberInformation = SlackMemberInformation.from_slack_response(slack_profile,
                                                                                         dedicated_bot.source)
        SlackContactUserRepository().collection().update_one({"sender_id": member_info.sender_id,
                                                              "source.source_id": dedicated_bot.source.source_id},
                                                             {"$set": member_info.to_dic()}, upsert=True)
        return SlackContactUserRepository().find_one(member_info.sender_id)

    @staticmethod
    def _is_request_answered(messages: list[dict], associated_user: str):
        for msg in messages:
            if msg.get('user') == associated_user:
                return True
        return False

    @classmethod
    def detect_unanswered_request(cls, message, sender_id, user: UserModel):
        sender_request = MessageRequestsRepository().find(user.id, sender_id)
        if not sender_request:
            log.info(f"[InboxLeadsJob]: Unanswered message request from {sender_id} for user: {user.email}")
            MessageRequestsRepository().upsert(user.id, sender_id, message)
            user.notification_settings.inbox.need_to_notify = True
            UserMongoRepository().set(user.id, notification_settings=user.notification_settings.to_dic())

    @classmethod
    def detect_answer_in_requests(cls, sender_id: str, source_id: str, user: UserModel):
        sender_request = MessageRequestsRepository().find(user.id, sender_id)
        if sender_request:
            MessageRequestsRepository().delete(sender_request['_id'])
        log.info(f"[InboxLeadsJob]: Answered message request from {sender_id} for user: {user.email}")
        BackgroundJobRunner.submit_data({'job_name': "save_request", 'job_kwargs': {'sender_id': sender_id, "source_id": source_id, "user_email": user.email}},
                                        v3_background_job_topic)

    @staticmethod
    def is_call_related_event(event: dict) -> bool:
        """
        Return True if slack event is about call/huddle and should be ignored.
        """
        # 1) Explicit huddle / call subtype
        if event.get("subtype") in {"huddle_thread", "call"}:
            return True

        # 2) Messages that contain "room" object are call/huddle related
        if "room" in event:
            return True

        # 4) Explicit call-type events (in case you receive them отдельно)
        if event.get("type") in {"call", "call_ringing", "call_rejected", "call_ended"}:
            return True

        return False
