from ninja import Router

from django.contrib.auth.models import User

from allianceauth.authentication.models import CharacterOwnership
from aa_contacts.models import CorporationToken

from ..schema import CorporationTokenSchema


router = Router()


@router.get("/", response=list[CorporationTokenSchema])
def get_list(request):
    return CorporationToken.visible_for(request.user)


@router.get("/{int:corporation_id}/", response={200: CorporationTokenSchema, 403: None, 404: None})
def get_single(request, corporation_id: int):
    user: User = request.user

    ownerships = CharacterOwnership.objects.filter(user=user)
    if not user.is_superuser and not ownerships.filter(character__corporation_id=corporation_id).exists():
        return 403, None

    try:
        token = CorporationToken.visible_for(user).get(corporation__corporation_id=corporation_id)
    except CorporationToken.DoesNotExist:
        return 404, None

    return 200, token
