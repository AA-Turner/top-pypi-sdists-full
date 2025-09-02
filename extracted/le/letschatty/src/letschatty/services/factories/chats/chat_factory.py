from letschatty.models.chat.chat import Chat
from letschatty.models.chat.client import Client
from letschatty.models.company.empresa import EmpresaModel
from datetime import datetime
from zoneinfo import ZoneInfo
from ..messages.chatty_message_factory import from_message_json
from letschatty.models.chat.flow_link_state import FlowStateAssignedToChat

class ChatFactory:
    @staticmethod
    def from_json(chat_json: dict) -> Chat:
        chat_json["messages"] = [from_message_json(message) for message in chat_json["messages"]]
        chat_json["flow_states"] = [FlowStateAssignedToChat.from_json(state) for state in chat_json["flow_states"]]
        return Chat(**chat_json)

    @staticmethod
    def from_client(client: Client, empresa: EmpresaModel, channel_id: str) -> Chat:
        return Chat(
            client=client,
            channel_id=channel_id,
            company_id=empresa.id,
            created_at=datetime.now(ZoneInfo("UTC")),
            updated_at=datetime.now(ZoneInfo("UTC"))
        )