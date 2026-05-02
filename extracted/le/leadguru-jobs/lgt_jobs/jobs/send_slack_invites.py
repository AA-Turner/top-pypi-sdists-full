from abc import ABC
from lgt_jobs.lgt_common.slack_client.web_client import SlackWebClient
from pydantic import BaseModel
from lgt_jobs.basejobs import BaseBackgroundJobData, BaseBackgroundJob
from lgt_jobs.lgt_data.enums import SourceType
from lgt_jobs.lgt_data.mongo_repository import DedicatedBotRepository, UserMongoRepository

"""
Send Slack Code
"""


class SendSlackInvitesJobData(BaseBackgroundJobData, BaseModel):
    emails: list[str]
    email_to_invite: str


class SendSlackInvitesJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return SendSlackInvitesJobData

    def exec(self, data: SendSlackInvitesJobData):
        print('[SendSlackInvitesJob]: Start...')
        users = UserMongoRepository().get_users(emails=data.emails)
        bots = DedicatedBotRepository().get_all(user_ids=[user.id for user in users],
                                                source_type=SourceType.SLACK,
                                                only_valid=True,
                                                include_paused=True,
                                                include_deleted=True)
        used_sources = {}
        count = 0
        for bot in bots:
            if not used_sources.get(bot.source.source_id):
                used_sources[bot.source.source_id] = None
                try:
                    client = SlackWebClient(bot.token, bot.cookies)
                    resp = client.send_slack_invite_to_workspace(data.email_to_invite)
                    print(f'Sent invite to {bot.source.source_name}. Count is {count}. Response: {resp.content}')
                    count += 1
                except:
                    print(f'Error to sent invite to {bot.source.source_name}')


        print(f'[SendSlackInvitesJob]: STOP...User were invited to {count} workspaces.')