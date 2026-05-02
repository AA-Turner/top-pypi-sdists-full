from abc import ABC
from lgt_jobs.lgt_common.slack_client.slack_client import SlackClient
from lgt_jobs.lgt_data.models.people.people import SlackMemberInformation
from lgt_jobs.lgt_data.mongo_repository import DedicatedBotRepository, SlackContactUserRepository
from pydantic import BaseModel
from lgt_jobs.basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
Load required Slack users by required bot
"""


class LoadSlackUsersJobData(BaseBackgroundJobData, BaseModel):
    bot_id: str
    users: list[str]


class LoadSlackUsersJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return LoadSlackUsersJobData

    def exec(self, data: LoadSlackUsersJobData):
        dedicated_bots_repo = DedicatedBotRepository()
        bot = dedicated_bots_repo.get_one(id=data.bot_id, include_deleted=True, include_paused=True)
        for user in data.users:
            client = SlackClient(bot.token, bot.cookies)
            profile = client.get_profile(user)
            if profile['ok']:
                profile['id'] = user
                member_info: SlackMemberInformation = SlackMemberInformation.from_slack_response(profile, bot.source)
                SlackContactUserRepository().collection().update_one({"sender_id": member_info.sender_id},
                                                                     {"$set": member_info.to_dic()}, upsert=True)
