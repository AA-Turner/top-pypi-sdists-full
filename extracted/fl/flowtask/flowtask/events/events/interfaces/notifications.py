from abc import ABC
from notify import Notify
from notify.providers.email import Email
from notify.providers.slack import Slack
from notify.providers.teams import Teams
from notify.models import Actor, Chat, Channel, TeamsChannel
from notify.conf import MS_TEAMS_DEFAULT_TEAMS_ID
from flowtask.conf import (
    EVENT_CHAT_ID,
    EVENT_CHAT_BOT,
    DEFAULT_RECIPIENT,
    EMAIL_USERNAME,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_HOST,
    SLACK_DEFAULT_CHANNEL,
    SLACK_DEFAULT_CHANNEL_NAME,
    MS_TEAMS_NAVIGATOR_CHANNEL,
    MS_TEAMS_NAVIGATOR_CHANNEL_ID,
)


class Notification(ABC):
    def get_notify(self, _type, **kwargs):
        if _type == "telegram":
            # defining the Default chat object:
            recipient = Chat(**{"chat_id": EVENT_CHAT_ID, "chat_name": "Navigator"})
            # send notifications to Telegram bot
            args = {"bot_token": EVENT_CHAT_BOT, **kwargs}
            ntf = Notify("telegram", **args)
        elif _type == "slack":
            recipient = Channel(
                channel_id=SLACK_DEFAULT_CHANNEL,
                channel_name=SLACK_DEFAULT_CHANNEL_NAME,
            )
            ntf = Slack()
        elif _type == "email":
            account = {
                "host": EMAIL_HOST,
                "port": EMAIL_PORT,
                "username": EMAIL_USERNAME,
                "password": EMAIL_PASSWORD,
                **kwargs,
            }
            recipient = Actor(**DEFAULT_RECIPIENT)
            ntf = Email(debug=True, **account)
        elif _type == "teams":
            ntf = Teams(as_user=True)
            recipient = TeamsChannel(
                name=MS_TEAMS_NAVIGATOR_CHANNEL,
                team_id=MS_TEAMS_DEFAULT_TEAMS_ID,
                channel_id=MS_TEAMS_NAVIGATOR_CHANNEL_ID,
            )
        else:
            # Any other Notify Provider:
            recipient = Actor(**DEFAULT_RECIPIENT)
            ntf = Notify(_type, **kwargs)
        return [ntf, recipient]
