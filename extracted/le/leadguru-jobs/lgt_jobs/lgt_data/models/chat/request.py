from lgt_jobs.lgt_data.models.bots.dedicated_bot import DedicatedBotModel
from lgt_jobs.lgt_data.models.chat.message import ChatMessage


class MessageRequest(ChatMessage):
    hidden: bool

    def __init__(self):
        super().__init__()
        self.hidden = False

    @classmethod
    def from_slack_response(cls, bot: DedicatedBotModel, message_data: dict, sender_id: str):
        message = super().from_slack_response(bot, message_data, sender_id)
        return MessageRequest.from_dic(message.to_dic())

    @property
    def is_system_message(self) -> bool:
        return "joined Slack" in self.text or "accepted your invitation to join Slack" in self.text
