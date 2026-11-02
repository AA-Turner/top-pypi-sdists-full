from letschatty.models.messages.meta_message_model.meta_base_notification_json import Contact
from letschatty.models.chat.client import Client
from letschatty.services.chat.client_service import ClientService
from letschatty.models.company.empresa import EmpresaModel
from letschatty.models.messages.message_templates.filled_data_from_frontend import FilledTemplateData
from datetime import datetime
from zoneinfo import ZoneInfo
from letschatty.models.utils.types import StrObjectId
from letschatty.models.whatsapp.portfolio_bsuid import PortfolioBsuid
from typing import Optional

class ClientFactory:

    @staticmethod
    def from_json(client_json: dict) -> Client:
        return Client(**client_json)

    @staticmethod
    def from_meta_contact(
        meta_contact: Contact, empresa: EmpresaModel, portfolio_id: Optional[str] = None, is_default_account: bool = True,
    ) -> Client:
        # Captura BSUID/username al crear el chat. Phase 2: `waid` puede ser None (contacto
        # sin teléfono, username-adopter fuera de ventana) → cliente sin teléfono, identificado
        # por user_id. `find_country_with_phone(None)` devuelve "Unknown" sin crashear.
        # With the portfolio of the receiving account, the BSUID is also recorded per portfolio.
        # `user_id` (the legacy scalar older readers send to) is the DEFAULT account's BSUID. A
        # person first met on another account keeps that BSUID only in `bsuids`, unless there is
        # no portfolio to file it under (then the scalar is the only identity there is).
        user_id = meta_contact.get_user_id()
        parent = meta_contact.get_parent_user_id()
        legacy_user_id = user_id if is_default_account or not portfolio_id else None
        return Client(
            bsuids=[PortfolioBsuid(portfolio_id=portfolio_id, bsuid=user_id)] if portfolio_id and user_id else [],
            parent_bsuids=[parent] if parent else [],
            name=meta_contact.get_name(),
            waid=meta_contact.get_wa_id(),
            user_id=legacy_user_id,
            user_id_parent=parent if legacy_user_id else None,
            username=meta_contact.get_username(),
            company_id=empresa.id,
            country=ClientService.find_country_with_phone(meta_contact.get_wa_id()),
            created_at=datetime.now(ZoneInfo("UTC")),
            updated_at=datetime.now(ZoneInfo("UTC")),
        )

    @staticmethod
    def from_phone_number_and_name(phone_number:str, new_contact_name:str, company_id: StrObjectId) -> Client:
        country = ClientService.find_country_with_phone(phone_number)
        client : Client = Client(
            waid = phone_number,
            name = new_contact_name,
            country = country,
            created_at=datetime.now(ZoneInfo("UTC")),
            updated_at=datetime.now(ZoneInfo("UTC")),
            company_id=company_id,
        )
        return client