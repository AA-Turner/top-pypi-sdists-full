from ninja import Router
from django.contrib.auth.models import User

from .schema import UserPermissionsSchema

router = Router(tags=["permissions"])


@router.get("/me", response=UserPermissionsSchema)
def get_me(request):
    user: User = request.user
    return {
        "can_manage_alliance_contacts": user.has_perm("aa_contacts.manage_alliance_contacts"),
        "can_manage_corporation_contacts": user.has_perm("aa_contacts.manage_corporation_contacts"),
    }
