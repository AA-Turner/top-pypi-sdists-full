from lgt_jobs.lgt_data.models.base import DictionaryModel
from lgt_jobs.lgt_data.models.leads.extended_lead import ExtendedLeadModel
from lgt_jobs.lgt_data.models.notifications.notification_settings import NotificationSettings


class UserFollowUps(DictionaryModel):
    actual_follow_ups: list[ExtendedLeadModel] = []
    overdue_follow_ups: list[ExtendedLeadModel] = []
    email: str | None = None
    notification_settings: NotificationSettings | None = None

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None
        model: UserFollowUps | None = super().from_dic(dic)
        model.actual_follow_ups = [ExtendedLeadModel.from_dic(lead) for lead in dic.get('actual_follow_ups', [])]
        model.overdue_follow_ups = [ExtendedLeadModel.from_dic(lead) for lead in dic.get('overdue_follow_ups', [])]
        model.notification_settings = NotificationSettings.from_dic(dic.get('notification_settings'))
        return model
