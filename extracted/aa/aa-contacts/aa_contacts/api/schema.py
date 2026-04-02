from datetime import datetime
from typing import Optional
from ninja import Schema, ModelSchema

from django.contrib.auth.models import User

from allianceauth.eveonline.models import EveCorporationInfo, EveAllianceInfo

from aa_contacts.models import Contact

from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)


class UserPermissionsSchema(Schema):
    can_manage_alliance_contacts: bool
    can_manage_corporation_contacts: bool


class EveAllianceSchema(ModelSchema):
    logo_url: str

    class Meta:
        model = EveAllianceInfo
        fields = ["alliance_id", "alliance_name"]

    @staticmethod
    def resolve_logo_url(obj: EveAllianceInfo) -> str:
        return obj.logo_url_32.split('?')[0]


class EveCorporationSchema(ModelSchema):
    alliance: Optional[EveAllianceSchema] = None
    logo_url: str

    class Meta:
        model = EveCorporationInfo
        fields = ["corporation_id", "corporation_name"]

    @staticmethod
    def resolve_logo_url(obj: EveCorporationInfo) -> str:
        return obj.logo_url_32.split('?')[0]


class TokenSchema(Schema):
    last_update: datetime


class AllianceTokenSchema(TokenSchema):
    alliance: EveAllianceSchema


class CorporationTokenSchema(TokenSchema):
    corporation: EveCorporationSchema


class ContactLabelSchema(Schema):
    label_name: str


class ContactSchema(Schema):
    id: int
    contact_id: int
    contact_type: Contact.ContactTypeOptions
    contact_logo_url: str
    contact_name: str
    standing: float
    notes: Optional[str] = None
    can_edit_notes: bool
    labels: list[ContactLabelSchema] = []

    @staticmethod
    def resolve_notes(obj: Contact, context) -> Optional[str]:
        user: User = context['request'].user
        if obj.can_view_notes(user):
            return obj.notes

    @staticmethod
    def resolve_contact_logo_url(obj: Contact) -> str:
        return obj.image_src.split('?')[0]

    @staticmethod
    def resolve_can_edit_notes(obj: Contact, context) -> bool:
        user: User = context['request'].user
        return obj.can_edit_notes(user)


class UpdateContactSchema(Schema):
    notes: str
