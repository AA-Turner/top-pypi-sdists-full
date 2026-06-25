from ninja import Router

from aa_contacts.api import common
from aa_contacts.api.schema import AllianceTokenSchema
from aa_contacts.models import AllianceToken

router = Router()


@router.get("/", response=list[AllianceTokenSchema])
def get_list(request):
    return AllianceToken.visible_for(request.user)


@router.get(
    "/{int:alliance_id}/", response={200: AllianceTokenSchema, 403: None, 404: None}
)
def get_single(request, alliance_id: int):
    return common.get_single_token(common.ALLIANCE, alliance_id, request.user)
