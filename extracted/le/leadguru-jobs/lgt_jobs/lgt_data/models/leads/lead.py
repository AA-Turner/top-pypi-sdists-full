import copy
from datetime import datetime
from typing import Optional

from lgt_jobs.lgt_data.models.base import BaseModel
from lgt_jobs.lgt_data.models.leads.message import MessageModel


class LeadModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.status = ''
        self.notes = ''
        self.archived = False
        self.message: Optional[MessageModel] = None
        self.hidden = False
        self.followup_date = None
        self.score = 0
        self.board_id = None
        self.linkedin_urls = []
        self.likes = 0
        self.reactions = 0
        self.replies = []
        self.last_action_at: Optional[datetime] = None
        self.slack_channel = None

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        model: LeadModel = cls()
        for k, v in dic.items():
            setattr(model, k, v)

        if dic.get('message'):
            model.message = MessageModel.from_dic(dic['message'])

        if not model.last_action_at:
            model.last_action_at = model.created_at

        return model

    def to_dic(self):
        result = copy.deepcopy(self.__dict__)
        result["message"] = self.message.to_dic()
        result['archived'] = self.archived
        return result
