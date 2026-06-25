from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from allianceauth.authentication.models import CharacterOwnership

from aa_contacts.models import (
    AllianceContact,
    AllianceToken,
    CorporationContact,
    CorporationToken,
)
from aa_contacts.tasks import update_alliance_contacts, update_corporation_contacts

if TYPE_CHECKING:
    from celery import Task
    from django.contrib.auth.models import User
    from django.db.models import QuerySet

    from aa_contacts.api.schema import ServerLinkInputSchema, UpdateContactSchema
    from aa_contacts.models import Contact, ContactServerLink, ContactToken


@dataclass(frozen=True)
class ContactApiConfig:
    contact_model: type[Contact]
    token_model: type[CorporationToken | AllianceToken]
    owner_type: str  # "alliance" | "corporation"
    update_task: Task


ALLIANCE = ContactApiConfig(
    AllianceContact, AllianceToken, "alliance", update_alliance_contacts
)
CORPORATION = ContactApiConfig(
    CorporationContact,
    CorporationToken,
    "corporation",
    update_corporation_contacts,
)


def _owner_filter(cfg: ContactApiConfig, owner_id: int) -> dict[str, int]:
    return {f"{cfg.owner_type}__{cfg.owner_type}_id": owner_id}


def _manage_perm(cfg: ContactApiConfig) -> str:
    return f"aa_contacts.manage_{cfg.owner_type}_contacts"


def _view_notes_perm(cfg: ContactApiConfig) -> str:
    return f"aa_contacts.view_{cfg.owner_type}_notes"


def _is_member(user: User, cfg: ContactApiConfig, owner_id: int) -> bool:
    return (
        user.is_superuser
        or CharacterOwnership.objects.filter(
            user=user, **{f"character__{cfg.owner_type}_id": owner_id}
        ).exists()
    )


def _has_contact_token(user: User, cfg: ContactApiConfig, owner_id: int) -> bool:
    return (
        cfg.token_model.visible_for(user)
        .filter(**_owner_filter(cfg, owner_id))
        .exists()
    )


def list_contacts(
    cfg: ContactApiConfig, owner_id: int, user: User
) -> tuple[int, QuerySet[Contact] | None]:
    if not _is_member(user, cfg, owner_id):
        return 403, None

    if not _has_contact_token(user, cfg, owner_id):
        return 404, None

    contacts = (
        cfg.contact_model.objects.with_contact_name()
        .filter(**_owner_filter(cfg, owner_id))
        .prefetch_related("labels", "server_links")
    )

    return 200, contacts


def update_contacts(
    cfg: ContactApiConfig, owner_id: int, user: User
) -> tuple[int, None]:
    if not _is_member(user, cfg, owner_id) or not user.has_perm(_manage_perm(cfg)):
        return 403, None

    if not _has_contact_token(user, cfg, owner_id):
        return 404, None

    cfg.update_task.delay(owner_id)

    return 200, None


def edit_contact(
    cfg: ContactApiConfig,
    owner_id: int,
    contact_pk: int,
    data: UpdateContactSchema,
    user: User,
) -> tuple[int, None]:
    if not _is_member(user, cfg, owner_id) or not user.has_perms(
        [_manage_perm(cfg), _view_notes_perm(cfg)]
    ):
        return 403, None

    if not _has_contact_token(user, cfg, owner_id):
        return 404, None

    try:
        contact: Contact = cfg.contact_model.objects.get(
            pk=contact_pk, **_owner_filter(cfg, owner_id)
        )
    except cfg.contact_model.DoesNotExist:
        return 404, None

    contact.notes = data.notes
    contact.save(update_fields=["notes"])

    return 200, None


def get_managed_contact(
    cfg: ContactApiConfig, owner_id: int, contact_pk: int, user: User
) -> Contact | int:
    if not _is_member(user, cfg, owner_id) or not user.has_perm(_manage_perm(cfg)):
        return 403

    if not _has_contact_token(user, cfg, owner_id):
        return 404

    try:
        return cfg.contact_model.objects.get(
            pk=contact_pk, **_owner_filter(cfg, owner_id)
        )
    except cfg.contact_model.DoesNotExist:
        return 404


def create_server_link(
    cfg: ContactApiConfig,
    owner_id: int,
    contact_pk: int,
    data: ServerLinkInputSchema,
    user: User,
) -> tuple[int, ContactServerLink | None]:
    contact = get_managed_contact(cfg, owner_id, contact_pk, user)
    if isinstance(contact, int):
        return contact, None

    link = contact.server_links.create(**data.dict())

    return 200, link


def update_server_link(  # noqa: PLR0913
    cfg: ContactApiConfig,
    owner_id: int,
    contact_pk: int,
    link_pk: int,
    data: ServerLinkInputSchema,
    user: User,
) -> tuple[int, ContactServerLink | None]:
    contact = get_managed_contact(cfg, owner_id, contact_pk, user)
    if isinstance(contact, int):
        return contact, None

    if not contact.server_links.filter(pk=link_pk).exists():
        return 404, None

    contact.server_links.filter(pk=link_pk).update(**data.dict())
    link = contact.server_links.get(pk=link_pk)

    return 200, link


def delete_server_link(
    cfg: ContactApiConfig, owner_id: int, contact_pk: int, link_pk: int, user: User
) -> tuple[int, None]:
    contact = get_managed_contact(cfg, owner_id, contact_pk, user)
    if isinstance(contact, int):
        return contact, None

    deletes = contact.server_links.filter(pk=link_pk).delete()

    if deletes[0] == 0:
        return 404, None
    return 200, None


def get_single_token(
    cfg: ContactApiConfig, owner_id: int, user: User
) -> tuple[int, ContactToken | None]:
    if not _is_member(user, cfg, owner_id):
        return 403, None

    try:
        token = cfg.token_model.visible_for(user).get(**_owner_filter(cfg, owner_id))
    except cfg.token_model.DoesNotExist:
        return 404, None

    return 200, token
