from typing import List

from lgt_jobs.lgt_data.models.bots.bot_info import BotInfo
from lgt_jobs.lgt_data.models.chat.message import ChatMessage
from lgt_jobs.lgt_data.models.contacts.contact import UserContact
from lgt_jobs.lgt_data.models.leads.lead import LeadModel
from lgt_jobs.lgt_data.models.people.people import SlackMemberInformation
from lgt_jobs.lgt_data.models.user_leads.user_lead import UserLeadModel


class ExtendedLeadModel(LeadModel):
    def __init__(self):
        super().__init__()
        self.previous_publications = []
        self.last_conversation: List[ChatMessage] = []
        self.contact: SlackMemberInformation | None = None
        self.deleted = False
        self.user_lead: UserLeadModel | None = None
        self.dedicated: bool = False
        self.bots: List[BotInfo] = []
        self.user_contact: UserContact | None = None
        self.paid: bool = False
        self.hidden_by_user: bool = False

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        result: ExtendedLeadModel | None = LeadModel.from_dic(dic)
        if not result:
            return None

        result.contact = SlackMemberInformation.from_dic(dic.get('contact'))
        result.user_contact = UserContact.from_dic(dic.get('user_contact'))
        result.previous_publications = [LeadModel.from_dic(lead) for lead in dic.get('previous_publications', [])]
        result.user_lead = UserLeadModel.from_dic(dic.get('user_lead'))
        result.last_conversation = [ChatMessage.from_dic(message) for message in dic.get('last_conversation', [])]
        result.bots = [BotInfo.from_dic(bot) for bot in dic.get('bots', [])]
        return result

    def to_csv(self, board_name: str) -> List[str]:
        return [self.message.source, self.contact.real_name, self.contact.title, self.contact.email,
                self.notes, board_name, self.status,
                self.followup_date.strftime("%d.%m.%Y %H:%M") if self.followup_date else "",
                self.message.message.replace('\n', ' ').strip()]
