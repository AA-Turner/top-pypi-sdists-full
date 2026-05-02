import random
from abc import ABC
from datetime import datetime, UTC
from time import sleep

from requests import Response

from lgt_jobs.lgt_common.enums.slack_errors import SlackErrors
from lgt_jobs.lgt_common.slack_client.slack_client import SlackClient
from lgt_jobs.lgt_data.models.people.people import SlackMemberInformation
from lgt_jobs.lgt_data.mongo_repository import DedicatedBotRepository, SlackContactUserRepository, \
    UserContactsRepository
import logging as log
from pydantic import BaseModel
from lgt_jobs.basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
Load Slack people by required bot
"""


class LoadSlackPeopleJobData(BaseBackgroundJobData, BaseModel):
    bot_id: str


class LoadSlackPeopleJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return LoadSlackPeopleJobData

    def exec(self, data: LoadSlackPeopleJobData):
        dedicated_bots_repo = DedicatedBotRepository()
        bot = dedicated_bots_repo.get_one(id=data.bot_id, include_deleted=True, include_paused=True)
        log.info(f'Start Scraping for [{str(bot.user_id)}:{bot.source.source_id}]')

        client = SlackClient(bot.token, bot.cookies)
        try:
            list_users_response = client.users_list()
        except:
            log.error(f'Error to get users [{str(bot.user_id)}:{bot.source.source_id}]')
            return

        members_count = 0
        while True:
            if not list_users_response["ok"] and list_users_response['error'] == SlackErrors.INVALID_AUTH:
                bot.invalid_creds = True
                dedicated_bots_repo.add_or_update(bot)
                log.error(f'Error during listing [{bot.source.source_name}:{bot.source.source_id}] '
                          f'members: {list_users_response["error"]}')
                return

            if not list_users_response.get('members', []):
                log.warning(f'No members in [{str(bot.user_id)}:{bot.source.source_id}]: {list_users_response}')
                return

            for member in list_users_response["members"]:
                sleep(random.uniform(0, 1))
                if not member.get("profile"):
                    continue

                if member.get("deleted", True) or member.get("id") == 'USLACKBOT':
                    continue

                member_info: SlackMemberInformation = SlackMemberInformation.from_slack_response(member, bot.source)
                members_count += 1
                presence_response: Response = None
                try:
                    for _ in range(3):
                        presence_response = client.get_presence(member_info.sender_id)
                        if presence_response.json():
                            break
                        sleep(1000)
                except:
                    log.error(f'Error to get user\'s presence [{member_info.sender_id}:{bot.source.source_id}]')
                    continue

                last_activity = None
                if presence_response.status_code == 200:
                    presence_data = presence_response.json()
                    if presence_data.get('ok'):
                        now = datetime.now(UTC)
                        online = presence_data.get('presence')
                        if presence_data.get('online'):
                            online = 'active'
                        last_activity = datetime.fromtimestamp(presence_data.get('last_activity'), tz=UTC) \
                            if presence_data.get('last_activity') else None
                        if online == 'active':
                            last_activity = now

                        member_info.online = online
                        member_info.online_updated_at = now

                member_info_dic = member_info.to_dic()
                member_info_dic.pop('created_at')
                if last_activity:
                    member_info_dic['last_activity'] = last_activity
                    UserContactsRepository().update_many(member_info.sender_id, last_activity=last_activity)
                SlackContactUserRepository().collection().update_one({"sender_id": member_info.sender_id},
                                                                     {"$set": member_info_dic}, upsert=True)

            next_cursor = list_users_response["response_metadata"].get("next_cursor", "")
            if next_cursor == "":
                log.info(f'[{str(bot.user_id)}:{bot.source.source_id}] loading done. {members_count} loaded')
                break

            try:
                for _ in range(3):
                    list_users_response = client.users_list(next_cursor)
                    if list_users_response:
                        break
                    sleep(1000)
            except:
                log.error(f'Error to get users [{str(bot.user_id)}:{bot.source.source_id}]')
                continue
