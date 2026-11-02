from letschatty.models.chat.chat import Chat
from letschatty.models.chat.client import Client
from letschatty.models.company.empresa import EmpresaModel
from letschatty.models.whatsapp.account_context import AccountContext
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo


class ChatFactory:
    @staticmethod
    def from_json(chat_json: dict) -> Chat:
        """Un chat desde su documento de `chats`. Llega sin mensajes ni estados de workflow:
        esos los carga `ChatLoader` cuando hacen falta."""
        if isinstance(chat_json, Chat):
            return chat_json
        return Chat(**chat_json)

    @staticmethod
    def from_client(client: Client, empresa: EmpresaModel, channel_id: str, account: Optional[AccountContext] = None) -> Chat:
        """Un chat nuevo de esta persona, con la persona cargada: al crearlo, `ChatAssetService.create`
        la busca en `clients` por su identidad y, si no existe, la da de alta. Sin mensajes:
        arranca con el resumen vacío.

        With `account`, the chat belongs to that account: its `channel_id` is the account's number
        and its `bsuid` the person's BSUID in the account's portfolio."""
        now = datetime.now(ZoneInfo("UTC"))
        chat = Chat(
            client_id=client.id,
            client=client.preview(),
            channel_id=account.channel_id if account else channel_id,
            account_id=account.account_id if account else None,
            bsuid=client.bsuid_for(account.portfolio_id) if account else None,
            company_id=empresa.id,
            created_at=now,
            updated_at=now,
        )
        chat.load_person(client)
        chat.load_messages([])
        chat.load_flow_states([])
        return chat
