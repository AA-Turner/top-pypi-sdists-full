import copy
from datetime import UTC, datetime
from typing import List, Optional

from bson import ObjectId

from lgt_jobs.lgt_data.enums import UserRole
from lgt_jobs.lgt_data.models.base import BaseModel
from lgt_jobs.lgt_data.models.external.discord.user import DiscordUser
from lgt_jobs.lgt_data.models.external.slack.user import SlackUser
from lgt_jobs.lgt_data.models.external.telegram.user import TelegramUser
from lgt_jobs.lgt_data.models.notifications.notification_settings import NotificationSettings
from lgt_jobs.lgt_data.models.people.profile import Profile
from lgt_jobs.lgt_data.models.user.general_settings import GeneralSettings
from lgt_jobs.lgt_data.models.user.typed_field import TypedField


class UserModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.email: Optional[str] = None
        self.password: Optional[str] = None
        self.google_id: Optional[str] = None
        self.google_session_id: Optional[str] = None
        self.roles: List[str] = []
        self.user_name: str = ''
        self.company: str = ''
        self.company_size: Optional[int] = None
        self.company_industries: Optional[List[str]] = None
        self.company_technologies: Optional[List[str]] = None
        self.company_locations: Optional[List[str]] = None
        self.company_web_site: str = ''
        self.company_description: str = ''
        self.position: str = ''
        self.leads_limit: Optional[int] = None
        self.leads_proceeded: Optional[int] = None
        self.leads_filtered: Optional[int] = None
        self.leads_limit_updated_at: Optional[int] = None
        self.paid_lead_price: int = 1
        self.state: int = 0
        self.credits_exceeded_at: Optional[datetime] = None
        self.unanswered_leads_period = None
        self.inactive = None
        self.slack_users: List[SlackUser] = []
        self.discord_users: List[DiscordUser] = []
        self.telegram_users: List[TelegramUser] = []
        self.verified: bool = False
        self.subscription_id: ObjectId | None = None
        self.subscription_expired_at: datetime | None = None
        self.balance: str | None = None
        self.subscription_name: str | None = None
        self.subscription_expiration_notified = False
        self.subscription_expiration_warning_notified = False
        self.notification_settings: NotificationSettings | None = None
        self.general_settings: GeneralSettings | None = None
        self.company_type: TypedField | None = None
        self.usage_purpose: list[TypedField] = []
        self.project_awareness: TypedField | None = None

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        model: UserModel = cls()
        for k, v in dic.items():
            setattr(model, k, v)

        if '_id' in dic:
            setattr(model, 'id', dic['_id'])

        model.slack_profile = Profile.from_dic(dic.get('slack_profile'))
        model.slack_users = [SlackUser.from_dic(user) for user in (dic.get('slack_users') or [])]
        model.discord_users = [DiscordUser.from_dic(user) for user in (dic.get('discord_users') or [])]
        model.telegram_users = [TelegramUser.from_dic(user) for user in (dic.get('telegram_users') or [])]
        model.usage_purpose = [TypedField.from_dic(purpose) for purpose in (dic.get('usage_purpose') or [])]
        model.company_type = TypedField.from_dic(dic.get('company_type'))
        model.project_awareness = TypedField.from_dic(dic.get('project_awareness'))
        model.notification_settings = NotificationSettings.from_dic(dic.get('notification_settings'))
        model.general_settings = GeneralSettings.from_dic(dic.get('general_settings'))
        return model

    def to_dic(self):
        result = copy.deepcopy(self.__dict__)

        if result.get('slack_profile'):
            result['slack_profile'] = result.get('slack_profile').__dict__
        if result.get('notification_settings'):
            result['notification_settings'] = NotificationSettings.to_dic(result.get('notification_settings'))
        if result.get('general_settings'):
            result['general_settings'] = GeneralSettings.to_dic(result.get('general_settings'))
        if result.get('company_type'):
            result['company_type'] = TypedField.to_dic(result.get('company_type'))
        if result.get('project_awareness'):
            result['project_awareness'] = TypedField.to_dic(result.get('project_awareness'))
        if result.get('usage_purpose'):
            result['usage_purpose'] = [TypedField.to_dic(purpose) for purpose in result.get('usage_purpose', [])]

        return result

    @property
    def is_admin(self):
        return UserRole.ADMIN in self.roles

    @property
    def subscription_expired(self):
        return self.subscription_expired_at.replace(tzinfo=UTC) < datetime.now(UTC)

    def get_slack_user(self, slack_email: str) -> SlackUser:
        return next(filter(lambda x: slack_email == x.email, self.slack_users), None)

    def get_discord_user(self, login: str) -> DiscordUser:
        return next(filter(lambda x: login == x.login, self.discord_users), None)

    def get_telegram_user(self, phone: str) -> TelegramUser:
        return next(filter(lambda x: phone == x.phone, self.telegram_users), None)
