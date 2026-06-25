from datetime import datetime
from datetime import timezone as dt_timezone
from random import randint
from typing import TYPE_CHECKING

from allianceauth.eveonline.models import EveAllianceInfo, EveCorporationInfo
from allianceauth.services.hooks import get_extension_logger
from celery import group, shared_task
from celery_once import QueueOnce
from django.db import transaction
from django.utils import timezone
from esi.exceptions import HTTPNotModified
from esi.models import Token
from httpx import Response

from .app_settings import TASK_JITTER
from .models import (
    AllianceContact,
    AllianceContactLabel,
    AllianceToken,
    CorporationContact,
    CorporationContactLabel,
    CorporationToken,
)
from .providers import esi

if TYPE_CHECKING:
    from celery.result import AsyncResult
    from esi.stubs import (
        AlliancesAllianceIdContactsGet,
        AlliancesAllianceIdContactsLabelsGet,
        CorporationsCorporationIdContactsGet,
        CorporationsCorporationIdContactsLabelsGet,
    )

    # https://github.com/sbdchd/celery-types
    classes = [
        AsyncResult,
    ]

    for cls in classes:
        setattr(cls, "__class_getitem__", classmethod(lambda cls, *args, **kwargs: cls))  # noqa: ARG005, B010


logger = get_extension_logger(__name__)


@shared_task(base=QueueOnce, once={"graceful": True})
def load_alliance_contact_name(contact_pk: int) -> None:
    contact = AllianceContact.objects.get(pk=contact_pk)
    contact.contact_name  # noqa: B018


@shared_task(base=QueueOnce, once={"graceful": True})
def load_corporation_contact_name(contact_pk: int) -> None:
    contact = CorporationContact.objects.get(pk=contact_pk)
    contact.contact_name  # noqa: B018


class BaseContactUpdater:
    @classmethod
    def get_entity_object(cls, entity_id: int) -> EveCorporationInfo | EveAllianceInfo:
        raise NotImplementedError

    @classmethod
    def get_entity_token(
        cls, entity: EveCorporationInfo | EveAllianceInfo
    ) -> CorporationToken | AllianceToken:
        raise NotImplementedError

    @classmethod
    def get_labels_data(
        cls, entity_id: int, token: Token, last_modified: timezone.datetime | None
    ) -> tuple[
        "AlliancesAllianceIdContactsLabelsGet | CorporationsCorporationIdContactsLabelsGet",
        Response,
    ]:
        raise NotImplementedError

    @classmethod
    def get_contacts_data(
        cls, entity_id: int, token: Token, last_modified: timezone.datetime | None
    ) -> tuple[
        "AlliancesAllianceIdContactsGet | CorporationsCorporationIdContactsGet",
        Response,
    ]:
        raise NotImplementedError

    @classmethod
    def get_contacts_model(cls) -> type[AllianceContact] | type[CorporationContact]:
        raise NotImplementedError

    @classmethod
    def get_entity_selector(
        cls, entity: EveCorporationInfo | EveAllianceInfo
    ) -> dict[str, EveCorporationInfo | EveAllianceInfo]:
        raise NotImplementedError

    @classmethod
    def get_labels_model(
        cls,
    ) -> type[AllianceContactLabel] | type[CorporationContactLabel]:
        raise NotImplementedError

    @classmethod
    def get_labels_related_selector(cls, pks: list[int]) -> dict[str, list[int]]:
        raise NotImplementedError

    @classmethod
    def get_load_contact_name_task(cls):
        raise NotImplementedError

    @classmethod
    def update_contacts(cls, entity_id: int):
        contacts_to_load = []

        entity = cls.get_entity_object(entity_id)
        entity_token = cls.get_entity_token(entity)

        try:
            labels_data, labels_response = cls.get_labels_data(
                entity_id, entity_token.token, entity_token.last_modified_labels
            )
        except HTTPNotModified:
            update_labels = False
        else:
            labels = {label.label_id: label.label_name for label in labels_data}
            update_labels = True

        try:
            contacts_data, contacts_response = cls.get_contacts_data(
                entity_id, entity_token.token, entity_token.last_modified_contacts
            )
        except HTTPNotModified:
            update_contacts = False
        else:
            contact_ids = {
                contact.contact_id: {
                    "contact_type": contact.contact_type,
                    "label_ids": contact.label_ids or [],
                    "standing": contact.standing,
                }
                for contact in contacts_data
            }
            update_contacts = True

        with transaction.atomic():
            label_objects = {}

            if update_labels:
                entity_token.last_modified_labels = datetime.strptime(
                    labels_response.headers.get("Last-Modified"),
                    "%a, %d %b %Y %H:%M:%S GMT",
                ).replace(tzinfo=dt_timezone.utc)

                cls.get_labels_model().objects.filter(
                    **cls.get_entity_selector(entity),
                ).exclude(
                    label_id__in=labels.keys(),
                ).delete()

                for label_id, label_name in labels.items():
                    label, _ = cls.get_labels_model().objects.update_or_create(
                        **cls.get_entity_selector(entity),
                        label_id=label_id,
                        defaults={"label_name": label_name},
                    )

                    label_objects[label_id] = label
            elif update_contacts:
                existing_labels = cls.get_labels_model().objects.filter(
                    **cls.get_entity_selector(entity),
                )
                label_objects = {label.label_id: label for label in existing_labels}

            if update_contacts:
                entity_token.last_modified_contacts = datetime.strptime(
                    contacts_response.headers.get("Last-Modified"),
                    "%a, %d %b %Y %H:%M:%S GMT",
                ).replace(tzinfo=dt_timezone.utc)

                missing_contacts = (
                    cls.get_contacts_model()
                    .objects.filter(
                        **cls.get_entity_selector(entity),
                    )
                    .exclude(
                        contact_id__in=contact_ids.keys(),
                    )
                )

                missing_contacts.filter(notes="", server_links__isnull=True).delete()
                cls.get_contacts_model().labels.through.objects.filter(
                    **cls.get_labels_related_selector(missing_contacts.values("pk")),
                ).delete()
                missing_contacts.update(standing=0.0)

                for contact_id, contact_data in contact_ids.items():
                    contact, _ = cls.get_contacts_model().objects.update_or_create(
                        **cls.get_entity_selector(entity),
                        contact_id=contact_id,
                        defaults={
                            "contact_type": contact_data["contact_type"],
                            "standing": contact_data["standing"],
                        },
                    )

                    contact.labels.clear()
                    if contact_data["label_ids"] is not None:
                        contact.labels.set(
                            [
                                label_objects[label_id]
                                for label_id in contact_data["label_ids"]
                            ]
                        )

                    contacts_to_load.append(contact.pk)

            entity_token.last_update = timezone.now()
            entity_token.save()

        contacts_to_load = cls.get_contacts_model().filter_missing_contact_name(
            contacts_to_load
        )
        if len(contacts_to_load) > 0:
            group(
                cls.get_load_contact_name_task().si(pk) for pk in contacts_to_load
            ).delay()


class CorporationContactUpdater(BaseContactUpdater):
    @classmethod
    def get_entity_object(cls, entity_id: int) -> EveCorporationInfo:
        try:
            corporation = EveCorporationInfo.objects.get(corporation_id=entity_id)
        except EveCorporationInfo.DoesNotExist:
            corporation = EveCorporationInfo.objects.create_corporation(entity_id)

        return corporation

    @classmethod
    def get_entity_token(cls, entity: EveCorporationInfo) -> CorporationToken:
        try:
            return (
                CorporationToken.objects.with_valid_tokens()
                .select_related("token")
                .get(corporation=entity)
            )
        except CorporationToken.DoesNotExist as e:
            msg = f"No valid token found for corporation {entity}"
            raise ValueError(msg) from e

    @classmethod
    def get_labels_data(
        cls, entity_id: int, token: Token, last_modified: timezone.datetime | None
    ) -> tuple["CorporationsCorporationIdContactsLabelsGet", "Response"]:
        return esi.client.Contacts.GetCorporationsCorporationIdContactsLabels(
            corporation_id=entity_id,
            token=token,
        ).results(last_modified=last_modified, return_response=True)

    @classmethod
    def get_contacts_data(
        cls, entity_id: int, token: Token, last_modified: timezone.datetime | None
    ) -> tuple["CorporationsCorporationIdContactsGet", "Response"]:
        return esi.client.Contacts.GetCorporationsCorporationIdContacts(
            corporation_id=entity_id,
            token=token,
        ).results(last_modified=last_modified, return_response=True)

    @classmethod
    def get_contacts_model(cls):
        return CorporationContact

    @classmethod
    def get_entity_selector(
        cls, entity: EveCorporationInfo
    ) -> dict[str, EveCorporationInfo]:
        return {"corporation": entity}

    @classmethod
    def get_labels_model(cls):
        return CorporationContactLabel

    @classmethod
    def get_labels_related_selector(cls, pks: list[int]) -> dict[str, list[int]]:
        return {"corporationcontact_id__in": pks}

    @classmethod
    def get_load_contact_name_task(cls):
        return load_corporation_contact_name


class AllianceContactUpdater(BaseContactUpdater):
    @classmethod
    def get_entity_object(cls, entity_id: int) -> EveAllianceInfo:
        try:
            alliance = EveAllianceInfo.objects.get(alliance_id=entity_id)
        except EveAllianceInfo.DoesNotExist:
            alliance = EveAllianceInfo.objects.create_alliance(entity_id)

        return alliance

    @classmethod
    def get_entity_token(cls, entity: EveAllianceInfo) -> AllianceToken:
        try:
            return (
                AllianceToken.objects.with_valid_tokens()
                .select_related("token")
                .get(alliance=entity)
            )
        except AllianceToken.DoesNotExist as e:
            msg = f"No valid token found for alliance {entity}"
            raise ValueError(msg) from e

    @classmethod
    def get_labels_data(
        cls, entity_id: int, token: Token, last_modified: timezone.datetime | None
    ) -> tuple["AlliancesAllianceIdContactsLabelsGet", "Response"]:
        return esi.client.Contacts.GetAlliancesAllianceIdContactsLabels(
            alliance_id=entity_id,
            token=token,
        ).results(last_modified=last_modified, return_response=True)

    @classmethod
    def get_contacts_data(
        cls, entity_id: int, token: Token, last_modified: timezone.datetime | None
    ) -> tuple["AlliancesAllianceIdContactsGet", "Response"]:
        return esi.client.Contacts.GetAlliancesAllianceIdContacts(
            alliance_id=entity_id,
            token=token,
        ).results(last_modified=last_modified, return_response=True)

    @classmethod
    def get_contacts_model(cls):
        return AllianceContact

    @classmethod
    def get_entity_selector(cls, entity: EveAllianceInfo) -> dict[str, EveAllianceInfo]:
        return {"alliance": entity}

    @classmethod
    def get_labels_model(cls):
        return AllianceContactLabel

    @classmethod
    def get_labels_related_selector(cls, pks: list[int]) -> dict[str, list[int]]:
        return {"alliancecontact_id__in": pks}

    @classmethod
    def get_load_contact_name_task(cls):
        return load_alliance_contact_name


@shared_task(base=QueueOnce, once={"graceful": True})
def update_alliance_contacts(alliance_id: int):
    AllianceContactUpdater.update_contacts(alliance_id)


@shared_task(base=QueueOnce, once={"graceful": True})
def update_corporation_contacts(corporation_id: int):
    CorporationContactUpdater.update_contacts(corporation_id)


@shared_task
def update_all_alliances_contacts():
    group(
        update_alliance_contacts.si(alliance_token.alliance.alliance_id).set(
            countdown=randint(0, TASK_JITTER)
        )
        for alliance_token in AllianceToken.objects.with_valid_tokens().select_related(
            "alliance"
        )
    ).delay()


@shared_task
def update_all_corporations_contacts():
    group(
        update_corporation_contacts.si(
            corporation_token.corporation.corporation_id
        ).set(countdown=randint(0, TASK_JITTER))
        for corporation_token in CorporationToken.objects.with_valid_tokens().select_related(
            "corporation"
        )
    ).delay()


@shared_task
def update_all_contacts():
    update_all_alliances_contacts.delay()
    update_all_corporations_contacts.delay()
