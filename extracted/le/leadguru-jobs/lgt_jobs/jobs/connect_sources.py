from abc import ABC
from typing import List
import logging as log

from lgt_jobs.jobs.load_slack_people import LoadSlackPeopleJob, LoadSlackPeopleJobData
from lgt_jobs.basejobs import BaseBackgroundJob, BaseBackgroundJobData
from lgt_jobs.jobs.bot_stats_update import BotStatsUpdateJob, BotStatsUpdateJobData
from lgt_jobs.lgt_data.models.base import BaseModel
from lgt_jobs.lgt_data.models.bots.base_bot import Source
from lgt_jobs.lgt_data.models.bots.dedicated_bot import DedicatedBotModel, Server
from lgt_jobs.lgt_data.models.external.slack.user import SlackUser
from lgt_jobs.runner import BackgroundJobRunner
from lgt_jobs.lgt_data.engine import UserTrackAction
from lgt_jobs.lgt_data.enums import SourceType, UserAction, StatusConnection
from lgt_jobs.lgt_data.mongo_repository import DedicatedBotRepository, UserMongoRepository


class ConnectSourceJobData(BaseBackgroundJobData, BaseModel):
    slack_email: str
    sources_ids: List[str]
    action_user_email: str
    user_email: str


class ConnectSourceJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return ConnectSourceJobData

    def exec(self, data: ConnectSourceJobData):
        users_repository = UserMongoRepository()
        bots_repository = DedicatedBotRepository()
        action_user = users_repository.get_by_email(data.action_user_email)
        user = users_repository.get_by_email(data.user_email)
        if not action_user:
            log.info(f'[ConnectSourceJobData]: Unable to find user with email: {data.action_user_email}')
            return

        slack_user: SlackUser = action_user.get_slack_user(data.slack_email)
        if not slack_user:
            log.info(f"[ConnectSourceJobData]: You have no credentials for {data.slack_email}. Try to login to Slack.")
            slack_user.status = StatusConnection.COMPLETE
            users_repository.set(action_user.id, slack_users=[user.to_dic() for user in action_user.slack_users])
            return
        bots = []
        for ws in slack_user.workspaces:
            try:
                if ws.id in data.sources_ids:
                    active_bot = bots_repository.get_one(user_id=action_user.id, active_server_id=ws.id)
                    bot = bots_repository.get_one(user_id=action_user.id, server_id=ws.id, include_deleted=True,
                                                  user_name=data.slack_email)
                    if active_bot:
                        continue
                    if not bot:
                        bot = DedicatedBotModel()
                        bot.servers = [Server()]

                    bot.user_name = slack_user.email
                    bot.slack_url = ws.url
                    bot.user_id = action_user.id
                    bot.created_by = user.email
                    bot.registration_link = ws.url
                    bot.token = ws.token
                    bot.cookies = slack_user.cookies
                    bot.deleted = False
                    bot.paused = False
                    bot.invalid_creds = False
                    bot.banned = False
                    bot.two_factor_required = ws.two_factor_required
                    source = Source()

                    for server in bot.servers:
                        server.id = ws.id
                        server.name = ws.domain
                        server.deleted = False
                        server.active = True
                        server.icon = ws.icon
                        server.subscribers = int(ws.active_users)

                    source.source_id = ws.id
                    source.source_name = ws.domain
                    bot.type = source.source_type = SourceType.SLACK
                    bot.icon = ws.icon
                    bot.source = source
                    bots_repository.add_or_update(bot)
                    UserTrackAction.track(action_user.id, UserAction.START_SOURCE, ws.id)
                    bot = bots_repository.get_one(user_id=action_user.id, server_id=ws.id, user_name=slack_user.email)
                    bots.append(bot)
                    BackgroundJobRunner.submit(BotStatsUpdateJob, BotStatsUpdateJobData(bot_id=str(bot.id)))
                    workspace_bots = DedicatedBotRepository().get_all(source_id=ws.id, include_deleted=True,
                                                                      only_valid=False, include_paused=True)
                    if len(workspace_bots) == 1:
                        BackgroundJobRunner.submit(LoadSlackPeopleJob,
                                                   LoadSlackPeopleJobData(bot_id=workspace_bots[0].id))
            except Exception:
                import traceback
                log.exception(f"[ConnectSourceJobData]: Error to connect {ws.id}")
                traceback.print_exc()
        slack_user.status = StatusConnection.COMPLETE
        users_repository.set(action_user.id, slack_users=[user.to_dic() for user in action_user.slack_users])
        return bots
