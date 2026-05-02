import copy
from datetime import datetime

from bson import ObjectId

from lgt_jobs.lgt_data.models.base import DictionaryModel
from lgt_jobs.lgt_data.models.bots.dedicated_bot import DedicatedBotModel
from lgt_jobs.lgt_data.models.chat.file import LeadGuruFile


class ChatMessage(DictionaryModel):
    bot_id: ObjectId
    user_id: ObjectId
    sender_id: str
    text: str
    user: str
    id: str
    viewed: bool
    files: list
    attachments: list[dict] | None
    created_at: datetime | None
    source_id: str | None

    def __init__(self):
        self.viewed = False
        self.text: str = ''
        self.created_at: datetime
        self.user = ''
        self.id = ''
        self.files = []
        self.attachments = []

    def to_dic(self):
        result = copy.deepcopy(self.__dict__)
        result['files'] = [x.to_dic() for x in result.get('files', []) if not isinstance(x, dict)]
        return result

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None
        model = cls()
        for k, v in dic.items():
            setattr(model, k, v)

        if dic.get('files'):
            model.files = [LeadGuruFile.from_dic(x) for x in dic.get('files', [])]
        return model

    @classmethod
    def from_slack_response(cls, bot: DedicatedBotModel, message_data: dict, sender_id: str):
        model = cls()
        model.sender_id = sender_id
        model.bot_id = bot.id
        model.text = message_data.get('text', '')
        model.user = message_data.get('user', '')
        model.id = message_data.get('ts', '')
        model.attachments = message_data.get('attachments', [])
        model.files = []
        model.user_id = bot.user_id
        model.source_id = bot.source.source_id
        if 'files' in message_data:
            for file in message_data.get('files'):
                if file.get('mode') != "tombstone" and file.get('url_private_download'):
                    leadguru_file = LeadGuruFile()
                    leadguru_file.id = file['id']
                    leadguru_file.content_type = file['mimetype']
                    leadguru_file.file_name = file['name']
                    leadguru_file.blob_path = f'slack_files/{bot.user_name}/slack_files/{file["id"]}'
                    model.files.append(leadguru_file)

        js_ticks = int(model.id.split('.')[0] + model.id.split('.')[1][3:])
        model.created_at = datetime.fromtimestamp(js_ticks / 1000.0)
        return model

