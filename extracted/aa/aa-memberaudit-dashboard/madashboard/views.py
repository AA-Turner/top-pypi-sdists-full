# Third Party
from memberaudit.app_settings import MEMBERAUDIT_APP_NAME
from memberaudit.models import CharacterUpdateStatus

# Django
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.translation import gettext as _

# Alliance Auth
from allianceauth.authentication.models import CharacterOwnership
from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)


def dashboard_memberaudit_check(request):
    unregistered = CharacterOwnership.objects.filter(
        user=request.user, character__memberaudit_character__isnull=True
    )

    registred = CharacterOwnership.objects.filter(user=request.user).values_list(
        "character__memberaudit_character", flat=True
    )

    issues = CharacterUpdateStatus.objects.filter(character__in=registred, is_success=0)

    chars = {}

    if unregistered or issues:
        for char in unregistered:
            title = _("Character Registration Issue")
            msg = f"<span class='text-danger'><i class='fas fa-times-circle' data-bs-tooltip='aa-memberaudit-dashboard' title='{title}'></i></span>"
            chars[char.character.character_id] = {
                "id": char.character.character_id,
                "name": char.character.character_name,
                "issues": _(
                    "Character is not registered in {memberaudit_app_name}."
                ).format(memberaudit_app_name=MEMBERAUDIT_APP_NAME),
                "icon": format_html(msg),
            }

    if issues:
        for issue in issues:
            if issue.character.eve_character.character_id not in chars:
                title = _("Character Update Issue")
                msg = f"<span class='text-warning'><i class='fas fa-triangle-exclamation' data-bs-tooltip='aa-memberaudit-dashboard' title='{title}'></i></span>"
                chars[issue.character.eve_character.character_id] = {
                    "id": issue.character.eve_character.character_id,
                    "name": issue.character.eve_character.character_name,
                    "issues": _(
                        "Please re-register this character, as there was an issue with the last update."
                    ),
                    "icon": format_html(msg),
                }

    context = {
        "chars": chars if chars else None,
        "memberaudit_app_name": MEMBERAUDIT_APP_NAME,
    }
    return render_to_string(
        "madashboard/dashboard.html", context=context, request=request
    )
