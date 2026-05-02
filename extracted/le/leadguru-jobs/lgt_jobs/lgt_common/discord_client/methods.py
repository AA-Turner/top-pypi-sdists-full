from datetime import datetime
from enum import Enum


class DiscordMethods(str, Enum):
    USER_GUILDS = 'users/@me/guilds'
    USER_DMS = 'users/@me/channels'
    USER = 'users/@me'
    USER_PROFILE = 'users/@me/profile'
    LOGIN = 'auth/login'

    @staticmethod
    def guild_channels(guild_id: str):
        return f'guilds/{guild_id}/channels'

    @staticmethod
    def channel_messages(channel_id: str, date_to: datetime = None):
        path = f'channels/{channel_id}/messages?limit=100'
        if date_to:
            path += f'&before={DiscordMethods.timestamp_to_snowflake(date_to.timestamp())}'

        return path

    @staticmethod
    def guild_user(guild_id: str):
        return f'guilds/{guild_id}/members/@me'

    @staticmethod
    def guild_bio(guild_id: str):
        return f'guilds/{guild_id}/profile/@me'

    @staticmethod
    def channels_invites(channel_id: str):
        return f'channels/{channel_id}/invites'

    @staticmethod
    def timestamp_to_snowflake(timestamp: float):
        return (int(timestamp) * 1000 - 1420070400000) * 4194304
