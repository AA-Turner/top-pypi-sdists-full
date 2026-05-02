import logging as log
import random
import time
from abc import ABC
from typing import Optional

from pydantic import BaseModel

from lgt_jobs.basejobs import BaseBackgroundJob, BaseBackgroundJobData
from lgt_jobs.lgt_common.discord_client.discord_client import DiscordClient
from lgt_jobs.lgt_common.enums.slack_errors import SlackErrors
from lgt_jobs.lgt_common.slack_client.web_client import SlackWebClient
from lgt_jobs.lgt_data.analytics import get_bots_aggregated_analytics
from lgt_jobs.lgt_data.enums import SourceType
from lgt_jobs.lgt_data.models.bots.dedicated_bot import Server, Channel, DedicatedBotModel
from lgt_jobs.lgt_data.models.external.discord.user import DiscordUser
from lgt_jobs.lgt_data.models.user.user import UserModel
from lgt_jobs.lgt_data.mongo_repository import (DedicatedBotRepository, UserMongoRepository, SlackContactUserRepository,
                                                LeadMongoRepository, UserLeadMongoRepository)

"""
Update bots statistics
"""


class BotStatsUpdateJobData(BaseBackgroundJobData, BaseModel):
    bot_id: Optional[str]


class BotStatsUpdateJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return BotStatsUpdateJobData

    def exec(self, data: BotStatsUpdateJobData):
        bots_rep = DedicatedBotRepository()
        users_rep = UserMongoRepository()
        bot = bots_rep.get_one(id=data.bot_id, include_deleted=True)
        user = users_rep.get(bot.user_id)
        received_messages, filtered_messages = get_bots_aggregated_analytics(bot_ids=[str(bot.id)])

        if bot.source.source_type == SourceType.DISCORD:
            client = DiscordClient(bot.token)
            servers_response = client.get_servers()

            if isinstance(servers_response, dict):
                if servers_response.get('message') == '401: Unauthorized':
                    BotStatsUpdateJob.__updated_invalid_creds_flag(bot, True, user)
                if servers_response.get('code') == 40002:
                    bot.two_factor_required = True
                    bots_rep.add_or_update(bot)
                log.warning(f"[BotStatsUpdateJob]: Servers response is not list: {servers_response}")
                return

            discord_servers = [Server.from_discord_response(server) for server in servers_response]
            discord_user: DiscordUser = user.get_discord_user(bot.user_name)
            available_channels_types = [0, 5, 15]
            if discord_user:
                discord_user.workspaces = discord_servers
                users_rep.set(user.id, discord_users=[user.to_dic() for user in user.discord_users])
            for discord_server in discord_servers:
                server = next(filter(lambda x: x.id == discord_server.id, bot.servers), None)
                if server:
                    discord_server.active = server.active
                    discord_server.deleted = server.deleted
                else:
                    discord_server.deleted = True
                channels = client.get_channels(discord_server.id)
                discord_channels = [Channel.from_dic(channel) for channel in channels
                                    if channel.get('type', 0) in available_channels_types]
                for discord_channel in discord_channels:
                    if server:
                        channel = next(filter(lambda x: x.id == discord_channel.id, server.channels), None)
                        if channel:
                            discord_channel.active = channel.active
                discord_server.channels = discord_channels
                if discord_server.icon:
                    discord_server.icon = (f'https://cdn.discordapp.com/icons/{discord_server.id}/'
                                           f'{discord_server.icon}.png')
                discord_server.messages_received = received_messages.get(discord_server.id)
                discord_server.messages_filtered = filtered_messages.get(discord_server.id)
                time.sleep(random.randint(1, 2))

            bot.servers = discord_servers
            bot.two_factor_required = False
            bot.invalid_creds = False
            bots_rep.add_or_update(bot)
            return

        client = SlackWebClient(bot.token, bot.cookies)
        auth_errors = [SlackErrors.INVALID_AUTH, SlackErrors.TWO_FACTOR_REQUIRED, SlackErrors.NOT_AUTHED]
        test_auth_response = client.test_auth()
        if not test_auth_response.status_code == 200:
            log.warning(f"[BotStatsUpdateJob]: Error to auth {data.bot_id}. {test_auth_response.content}")
            return

        if not bot.invalid_creds:
            error = test_auth_response.json().get("error")
            if error in auth_errors:
                BotStatsUpdateJob.__updated_invalid_creds_flag(bot, True, user)

        user = test_auth_response.json().get('user_id')
        bot.associated_user = user
        bots_rep.add_or_update(bot)
        team_info = {}
        try:
            team_info = client.get_team_info()
        except:
            log.warning(f"[BotStatsUpdateJob]: Error to get  team info of {data.bot_id}. {test_auth_response.content}")

        if team_info.get('ok'):
            bot_name = team_info['team']['domain']
            if bot.source.source_name != bot_name:
                log.info(f"[BotStatsUpdateJob]: Updated source {bot.source.source_id}. "
                         f"Was {bot.source.source_name}, now {bot_name}")
                if bot.servers:
                    bot.servers[0].name = bot_name
                bot.source.source_name = bot_name
                bot.slack_url = bot.registration_link = team_info['team']['url']
                bots_rep.add_or_update(bot)
                SlackContactUserRepository().update_source(bot.source.source_id, bot.source.__dict__)
                UserLeadMongoRepository().update_source(bot.source.source_id, bot.source.__dict__)
                LeadMongoRepository().update_source(bot.source.source_id, bot.source.__dict__)

            icons = team_info['team']['icon']
            icon = icons.get('image_88')
            bots_rep.collection().update_many({'source.source_id': bot.source.source_id, 'servers': {'$ne': []}}, {"$set": {"servers.$[].icon": icon, 'icon': icon}})

        try:
            channels_response = client.channels_list()
        except:
            log.warning(f"[BotStatsUpdateJob]: Error to get channels list for bot {bot.id}.")
            return

        if not channels_response['ok']:
            if channels_response.get("error") in auth_errors:
                BotStatsUpdateJob.__updated_invalid_creds_flag(bot, True, user)
            else:
                log.warning(f"[BotStatsUpdateJob]: Error during update bot {bot.id} stats. Error: {channels_response}")
            return

        channels = channels_response['channels']
        channels_users = {channel['id']: channel.get('num_members', 0) for channel in channels}
        max_users_count = 0
        if bot.servers:
            channels = [Channel.from_dic(channel_dict) for channel_dict in channels]
            for channel in channels:
                slack_channel: Channel = next(filter(lambda x: x.id == channel.id, bot.servers[0].channels), None)
                if slack_channel:
                    channel.active = slack_channel.active
                    channel.subscribers = channels_users.get(slack_channel.id, 0)
                else:
                    channel.active = channel.is_member
                if channel.subscribers > max_users_count:
                    max_users_count = channel.subscribers
            bot.servers[0].channels = channels
            bot.servers[0].subscribers = max_users_count
            bot.servers[0].messages_received = received_messages.get(bot.source.source_id, 0)
            bot.servers[0].messages_filtered = filtered_messages.get(bot.source.source_id, 0)

        bots_rep.add_or_update(bot)

    @staticmethod
    def __updated_invalid_creds_flag(bot: DedicatedBotModel, invalid_creds: bool, user: UserModel):
        if bot.invalid_creds != invalid_creds:
            bot.invalid_creds = invalid_creds
            DedicatedBotRepository().add_or_update(bot)
            if invalid_creds:
                user.notification_settings.source_deactivation.need_to_notify = True
                UserMongoRepository().set(user.id, notification_settings=user.notification_settings.to_dic())
