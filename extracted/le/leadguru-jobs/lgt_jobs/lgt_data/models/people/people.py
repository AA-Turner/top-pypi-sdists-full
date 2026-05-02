import copy
from datetime import datetime
from typing import Optional

from lgt_jobs.lgt_data.models.base import BaseModel
from lgt_jobs.lgt_data.models.bots.base_bot import Source
from lgt_jobs.lgt_data.models.external.slack.timezone import SlackTimeZone
from lgt_jobs.lgt_data.models.people.profile import Profile


class SlackMemberInformation(BaseModel, Profile):
    workspace: str
    sender_id: str
    images: dict
    full_text: str
    deleted: bool = False
    is_bot: bool = False
    is_app_user: bool = False
    is_admin: bool = False
    is_owner: bool = False
    is_email_confirmed: bool = False
    online: Optional[str] = None
    online_updated_at: datetime = None
    timezone: SlackTimeZone = None
    source: Source = None

    @classmethod
    def from_dic(cls, dic: dict):
        model: SlackMemberInformation = cls()
        if not dic:
            return None

        for k, v in dic.items():
            setattr(model, k, v)

        model.online = dic.get('online', '') == "active"
        model: SlackMemberInformation | None = super().from_dic(dic)
        model.source = Source.from_dic(dic.get('source'))
        return model

    def to_dic(self):
        result = copy.deepcopy(self.__dict__)
        if result.get('source'):
            result['source'] = Source.to_dic(result.get('source'))
        return result

    @staticmethod
    def from_slack_response(slack_profile: dict, source: Source = None):
        member_info: SlackMemberInformation = SlackMemberInformation()
        member_info.source = source
        member_info.sender_id = slack_profile.get("id")
        member_info.display_name = slack_profile["profile"].get("display_name")
        member_info.real_name = slack_profile["profile"].get("real_name")
        member_info.title = slack_profile["profile"].get("title")
        member_info.phone = slack_profile["profile"].get("phone")
        member_info.skype = slack_profile["profile"].get("skype")
        member_info.email = slack_profile["profile"].get("email")
        member_info.images = {
            'image_24': slack_profile.get("profile", {}).get("image_24",
                                                             'https://a.slack-edge.com/80588/img/slackbot_24.png'),
            'image_32': slack_profile.get("profile", {}).get("image_32",
                                                             'https://a.slack-edge.com/80588/img/slackbot_32.png'),
            'image_48': slack_profile.get("profile", {}).get("image_48",
                                                             'https://a.slack-edge.com/80588/img/slackbot_48.png'),
            'image_72': slack_profile.get("profile", {}).get("image_72",
                                                             'https://a.slack-edge.com/80588/img/slackbot_72.png'),
            'image_192': slack_profile.get("profile", {}).get("image_192",
                                                              'https://a.slack-edge.com/80588/img/slackbot_192.png'),
            'image_512': slack_profile.get("profile", {}).get("image_512",
                                                              'https://a.slack-edge.com/80588/img/slackbot_512.png'),

        }
        member_info.timezone = {"tz": slack_profile.get("tz"), "tz_label": slack_profile.get("tz_label"),
                                "tz_offset": slack_profile.get("tz_offset")}
        return member_info
