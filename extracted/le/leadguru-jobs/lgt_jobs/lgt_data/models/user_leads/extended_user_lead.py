from typing import List

from lgt_jobs.lgt_data.models.bots.bot_info import BotInfo
from lgt_jobs.lgt_data.models.leads.lead import LeadModel
from lgt_jobs.lgt_data.models.people.people import SlackMemberInformation
from lgt_jobs.lgt_data.models.user_leads.user_lead import UserLeadModel


class ExtendedUserLeadModel(UserLeadModel):
    pass

    def __init__(self):
        super().__init__()
        self.contact: SlackMemberInformation | None = None
        self.previous_publications = []
        self.bots: List[BotInfo] = []
        self.user_email: str | None = None

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        result: ExtendedUserLeadModel | None = super().from_dic(dic)
        if not result:
            return None

        result.contact = SlackMemberInformation.from_dic(dic.get('contact'))
        result.previous_publications = [LeadModel.from_dic(lead) for lead in dic.get('previous_publications', [])]
        return result

    def to_dic(self):
        result = super().to_dic()
        result["contact"] = self.contact.to_dic()
        return result

    def to_csv(self, board_name: str) -> List[str]:
        return [self.message.source, self.contact.real_name, self.contact.title, self.contact.email,
                self.notes, board_name, self.status,
                self.followup_date.strftime("%d.%m.%Y %H:%M") if self.followup_date else "",
                self.message.message.replace('\n', ' ').strip()]
