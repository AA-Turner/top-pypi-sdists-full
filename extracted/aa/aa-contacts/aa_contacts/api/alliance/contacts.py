from django.contrib.auth.models import User

from ninja import Router, Path

from allianceauth.authentication.models import CharacterOwnership
from aa_contacts.models import AllianceToken, AllianceContact
from aa_contacts.tasks import update_alliance_contacts
from ..schema import ContactSchema, UpdateContactSchema

router = Router()


@router.get("/", response={200: list[ContactSchema], 403: None, 404: None})
def list_contacts(request, alliance_id: int = Path(...)):
    user: User = request.user

    ownerships = CharacterOwnership.objects.filter(user=user)
    if not user.is_superuser and not ownerships.filter(character__alliance_id=alliance_id).exists():
        return 403, None

    token = AllianceToken.visible_for(user).filter(alliance__alliance_id=alliance_id)
    if not token.exists():
        return 404, None

    contacts = (
        AllianceContact.objects
        .with_contact_name()
        .filter(alliance__alliance_id=alliance_id)
        .prefetch_related('labels')
    )

    return 200, contacts


@router.post("/update", response={200: None, 403: None, 404: None})
def update_contacts(request, alliance_id: int = Path(...)):
    user: User = request.user

    ownerships = CharacterOwnership.objects.filter(user=user)
    if not user.is_superuser and not ownerships.filter(character__alliance_id=alliance_id).exists():
        return 403, None

    token = (
        AllianceToken.visible_for(user)
        .filter(alliance__alliance_id=alliance_id)
    )
    if not token.exists():
        return 404, None

    update_alliance_contacts.delay(alliance_id)

    return 200, None


@router.patch("/{int:contact_pk}", response={200: None, 403: None, 404: None})
def edit_contact(request, data: UpdateContactSchema, contact_pk: int, alliance_id: int = Path(...)):
    user: User = request.user

    ownerships = CharacterOwnership.objects.filter(user=user)
    if (
        (not user.is_superuser and not ownerships.filter(character__alliance_id=alliance_id).exists())
        or
        (not user.has_perms(['aa_contacts.manage_alliance_contacts', 'aa_contacts.view_alliance_notes']))
    ):
        return 403, None

    token = (
        AllianceToken.visible_for(user)
        .filter(alliance__alliance_id=alliance_id)
    )
    if not token.exists():
        return 404, None

    try:
        contact: AllianceContact = AllianceContact.objects.get(pk=contact_pk, alliance__alliance_id=alliance_id)
    except AllianceContact.DoesNotExist:
        return 404, None

    contact.notes = data.notes
    contact.save(update_fields=['notes'])

    return 200, None
