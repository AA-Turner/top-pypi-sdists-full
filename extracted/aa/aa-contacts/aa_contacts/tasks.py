from random import randint

from celery import shared_task, group
from celery_once import QueueOnce

from django.db import transaction
from django.utils import timezone

from allianceauth.eveonline.models import EveAllianceInfo, EveCorporationInfo
from allianceauth.services.hooks import get_extension_logger

from esi.models import Token
from esi.exceptions import HTTPNotModified

from .app_settings import TASK_JITTER
from .models import AllianceContact, AllianceContactLabel, AllianceToken, CorporationToken, CorporationContact, CorporationContactLabel
from .providers import esi

logger = get_extension_logger(__name__)


@shared_task(base=QueueOnce, once={'graceful': True})
def load_alliance_contact_name(contact_pk: int):
    contact = AllianceContact.objects.get(pk=contact_pk)
    contact.contact_name


@shared_task(base=QueueOnce, once={'graceful': True})
def load_corporation_contact_name(contact_pk: int):
    contact = CorporationContact.objects.get(pk=contact_pk)
    contact.contact_name


class BaseContactUpdater:

    @classmethod
    def get_entity_object(cls, entity_id: int) -> EveCorporationInfo | EveAllianceInfo:
        raise NotImplementedError

    @classmethod
    def get_entity_token(cls, entity: EveCorporationInfo | EveAllianceInfo) -> CorporationToken | AllianceToken:
        raise NotImplementedError

    @classmethod
    def get_labels_data(cls, entity_id: int, token: Token):
        raise NotImplementedError

    @classmethod
    def get_contacts_data(cls, entity_id: int, token: Token):
        raise NotImplementedError

    @classmethod
    def get_contacts_model(cls):
        raise NotImplementedError

    @classmethod
    def get_entity_selector(cls, entity: EveCorporationInfo | EveAllianceInfo) -> dict[str, EveCorporationInfo | EveAllianceInfo]:
        raise NotImplementedError

    @classmethod
    def get_labels_model(cls):
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
            labels_data = cls.get_labels_data(entity_id, entity_token.token)
        except HTTPNotModified:
            update_labels = False
        else:
            labels = {label.label_id: label.label_name for label in labels_data}
            update_labels = True

        try:
            contacts_data = cls.get_contacts_data(entity_id, entity_token.token)
        except HTTPNotModified:
            update_contacts = False
        else:
            contact_ids = {
                contact.contact_id: {
                    'contact_type': contact.contact_type,
                    'label_ids': contact.label_ids or [],
                    'standing': contact.standing
                } for contact in contacts_data
            }
            update_contacts = True

        with transaction.atomic():
            label_objects = {}

            if update_labels:
                cls.get_labels_model().objects.filter(
                    **cls.get_entity_selector(entity)
                ).exclude(
                    label_id__in=labels.keys()
                ).delete()

                for label_id, label_name in labels.items():
                    label, _ = cls.get_labels_model().objects.update_or_create(
                        **cls.get_entity_selector(entity),
                        label_id=label_id,
                        defaults={'label_name': label_name}
                    )

                    label_objects[label_id] = label
            elif update_contacts:
                existing_labels = cls.get_labels_model().objects.filter(
                    **cls.get_entity_selector(entity)
                )
                label_objects = {label.label_id: label for label in existing_labels}

            if update_contacts:
                missing_contacts = cls.get_contacts_model().objects.filter(
                    **cls.get_entity_selector(entity)
                ).exclude(
                    contact_id__in=contact_ids.keys()
                )

                missing_contacts.filter(notes='').delete()
                cls.get_contacts_model().labels.through.objects.filter(
                    **cls.get_labels_related_selector(missing_contacts.values('pk'))
                ).delete()
                missing_contacts.update(standing=0.0)

                for contact_id, contact_data in contact_ids.items():
                    contact, _ = cls.get_contacts_model().objects.update_or_create(
                        **cls.get_entity_selector(entity),
                        contact_id=contact_id,
                        defaults={
                            'contact_type': contact_data['contact_type'],
                            'standing': contact_data['standing']
                        }
                    )

                    contact.labels.clear()
                    if contact_data['label_ids'] is not None:
                        contact.labels.set([label_objects[label_id] for label_id in contact_data['label_ids']])

                    contacts_to_load.append(contact.pk)

            entity_token.last_update = timezone.now()
            entity_token.save()

        contacts_to_load = cls.get_contacts_model().filter_missing_contact_name(contacts_to_load)
        if len(contacts_to_load) > 0:
            group(cls.get_load_contact_name_task().si(pk) for pk in contacts_to_load).delay()


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
            return CorporationToken.objects.with_valid_tokens().select_related('token').get(corporation=entity)
        except CorporationToken.DoesNotExist:
            raise ValueError(f"No valid token found for corporation {entity}")

    @classmethod
    def get_labels_data(cls, entity_id: int, token: Token):
        return (
            esi.client
            .Contacts
            .GetCorporationsCorporationIdContactsLabels(
                corporation_id=entity_id,
                token=token
            )
            .results()
        )

    @classmethod
    def get_contacts_data(cls, entity_id: int, token: Token):
        return (
            esi.client
            .Contacts
            .GetCorporationsCorporationIdContacts(
                corporation_id=entity_id,
                token=token
            )
            .results()
        )

    @classmethod
    def get_contacts_model(cls):
        return CorporationContact

    @classmethod
    def get_entity_selector(cls, entity: EveCorporationInfo) -> dict[str, EveCorporationInfo]:
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
            return AllianceToken.objects.with_valid_tokens().select_related('token').get(alliance=entity)
        except AllianceToken.DoesNotExist:
            raise ValueError(f"No valid token found for alliance {entity}")

    @classmethod
    def get_labels_data(cls, entity_id: int, token: Token):
        return (
            esi.client
            .Contacts
            .GetAlliancesAllianceIdContactsLabels(
                alliance_id=entity_id,
                token=token
            ).results()
        )

    @classmethod
    def get_contacts_data(cls, entity_id: int, token: Token):
        return (
            esi.client
            .Contacts
            .GetAlliancesAllianceIdContacts(
                alliance_id=entity_id,
                token=token
            ).results()
        )

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


@shared_task(base=QueueOnce, once={'graceful': True})
def update_alliance_contacts(alliance_id: int):
    AllianceContactUpdater.update_contacts(alliance_id)


@shared_task(base=QueueOnce, once={'graceful': True})
def update_corporation_contacts(corporation_id: int):
    CorporationContactUpdater.update_contacts(corporation_id)


@shared_task
def update_all_alliances_contacts():
    group(
        update_alliance_contacts.si(alliance_token.alliance.alliance_id).set(countdown=randint(0, TASK_JITTER))
        for alliance_token in AllianceToken.objects.with_valid_tokens().select_related('alliance')
    ).delay()


@shared_task
def update_all_corporations_contacts():
    group(
        update_corporation_contacts.si(corporation_token.corporation.corporation_id).set(countdown=randint(0, TASK_JITTER))
        for corporation_token in CorporationToken.objects.with_valid_tokens().select_related('corporation')
    ).delay()


@shared_task
def update_all_contacts():
    update_all_alliances_contacts.delay()
    update_all_corporations_contacts.delay()
