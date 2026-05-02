from datetime import datetime
from typing import List

from lgt_jobs.lgt_data.enums import SourceType
from lgt_jobs.lgt_data.models.base import BaseModel, DictionaryModel


class Credentials(BaseModel):
    def __init__(self):
        super().__init__()
        self.token = None
        self.cookies = None
        self.invalid_creds = False


class Source(DictionaryModel):
    def __init__(self):
        self.source_type: SourceType | None = None
        self.source_name: str | None = None
        self.source_id = None


class BaseBotModel(Credentials):
    def __init__(self):
        super().__init__()
        self.created_by = None
        self.user_name = None
        self.slack_url = None
        self.registration_link = None
        self.channels = None
        self.connected_channels = None
        self.channels_users = None
        self.users_count = None
        self.recent_messages: List[str] = []
        self.icon = None
        self.active_channels = {}
        self.paused_channels = []
        self.source: Source | None = None
        self.two_factor_required: bool = False
        self.banned: bool = False
        self.associated_user = None
        self.type: SourceType | None = None
        self.deleted = False
        self.deactivated_at: datetime | None = None
        self.sync_chats: bool = False
