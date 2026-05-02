from datetime import datetime, UTC

from bson import ObjectId

from lgt_jobs.lgt_data.models.leads.lead import LeadModel


class UserLeadModel(LeadModel):
    pass

    def __init__(self):
        super().__init__()
        self.order: int = 0
        self.followup_date: datetime | None = None
        self.user_id: ObjectId | None = None
        self.chat_viewed_at: datetime | None = None
        self.board_id: ObjectId | None = None

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        result: UserLeadModel | None = super().from_dic(dic)
        if not result:
            return None

        if result.followup_date:
            result.followup_date.replace(tzinfo=UTC)

        result.chat_viewed_at = dic.get('chat_viewed_at')
        return result
    