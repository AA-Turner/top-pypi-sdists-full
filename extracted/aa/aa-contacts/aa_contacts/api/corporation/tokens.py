from ninja import Router

from aa_contacts.api import common
from aa_contacts.api.schema import CorporationTokenSchema
from aa_contacts.models import CorporationToken

router = Router()


@router.get("/", response=list[CorporationTokenSchema])
def get_list(request):
    return CorporationToken.visible_for(request.user)


@router.get(
    "/{int:corporation_id}/",
    response={200: CorporationTokenSchema, 403: None, 404: None},
)
def get_single(request, corporation_id: int):
    return common.get_single_token(common.CORPORATION, corporation_id, request.user)
