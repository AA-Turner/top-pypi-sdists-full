from django.contrib.auth.models import User

from ninja import Router, Path

from allianceauth.authentication.models import CharacterOwnership

from aa_contacts.models import CorporationToken, CorporationContact
from aa_contacts.tasks import update_corporation_contacts
from ..schema import ContactSchema, UpdateContactSchema

router = Router()


@router.get("/", response={200: list[ContactSchema], 403: None, 404: None})
def list_contacts(request, corporation_id: int = Path(...)):
    user: User = request.user

    ownerships = CharacterOwnership.objects.filter(user=user)
    if not user.is_superuser and not ownerships.filter(character__corporation_id=corporation_id).exists():
        return 403, None

    token = CorporationToken.visible_for(user).filter(corporation__corporation_id=corporation_id)
    if not token.exists():
        return 404, None

    contacts = (
        CorporationContact.objects
        .with_contact_name()
        .filter(corporation__corporation_id=corporation_id)
        .prefetch_related('labels')
    )

    return 200, contacts


@router.post("/update", response={200: None, 403: None, 404: None})
def update_contacts(request, corporation_id: int = Path(...)):
    user: User = request.user

    ownerships = CharacterOwnership.objects.filter(user=user)
    if not user.is_superuser and not ownerships.filter(character__corporation_id=corporation_id).exists():
        return 403, None

    token = (
        CorporationToken.visible_for(user)
        .filter(corporation__corporation_id=corporation_id)
    )
    if not token.exists():
        return 404, None

    update_corporation_contacts.delay(corporation_id)

    return 200, None


@router.patch("/{int:contact_pk}", response={200: None, 403: None, 404: None})
def edit_contact(request, data: UpdateContactSchema, contact_pk: int, corporation_id: int = Path(...)):
    user: User = request.user

    ownerships = CharacterOwnership.objects.filter(user=user)
    if (
        (not user.is_superuser and not ownerships.filter(character__corporation_id=corporation_id).exists())
        or
        (not user.has_perms(['aa_contacts.manage_corporation_contacts', 'aa_contacts.view_corporation_notes']))
    ):
        return 403, None

    token = (
        CorporationToken.visible_for(user)
        .filter(corporation__corporation_id=corporation_id)
    )
    if not token.exists():
        return 404, None

    try:
        contact: CorporationContact = CorporationContact.objects.get(pk=contact_pk, corporation__corporation_id=corporation_id)
    except CorporationContact.DoesNotExist:
        return 404, None

    contact.notes = data.notes
    contact.save(update_fields=['notes'])

    return 200, None
