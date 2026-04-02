from ninja import Router

from django.contrib.auth.models import User

from allianceauth.authentication.models import CharacterOwnership
from aa_contacts.models import AllianceToken

from ..schema import AllianceTokenSchema


router = Router()


@router.get("/", response=list[AllianceTokenSchema])
def get_list(request):
    return AllianceToken.visible_for(request.user)


@router.get("/{int:alliance_id}/", response={200: AllianceTokenSchema, 403: None, 404: None})
def get_single(request, alliance_id: int):
    user: User = request.user

    ownerships = CharacterOwnership.objects.filter(user=user)
    if not user.is_superuser and not ownerships.filter(character__alliance_id=alliance_id).exists():
        return 403, None

    try:
        token = AllianceToken.visible_for(user).get(alliance__alliance_id=alliance_id)
    except AllianceToken.DoesNotExist:
        return 404, None

    return 200, token
