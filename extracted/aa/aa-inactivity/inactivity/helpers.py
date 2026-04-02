"""Helpers for Inactivity."""

from typing import NamedTuple, Optional

from allianceauth.authentication.models import User
from allianceauth.eveonline.models import EveCharacter
from app_utils.views import bootstrap_icon_plus_name_html


class UserForDisplay(NamedTuple):
    """User with additional information for display."""

    character: Optional[EveCharacter]
    html: str
    icon_url: str
    name: str
    name_with_ticker: str
    user: User

    def has_main(self) -> bool:
        """Return True when this user has a main."""
        return bool(self.character)


def main_or_username(user: User) -> str:
    """Safe way to get the main's character name or fallback to the username."""
    try:
        return user.profile.main_character.character_name
    except AttributeError:
        return user.username


def user_for_display(user: User) -> UserForDisplay:
    """Prepare user for display.

    Use main character as default or fallback to username if user has no main.
    """
    character: EveCharacter = user.profile.main_character
    if not character:
        name = name_with_ticker = user.username
        icon_url = EveCharacter.generic_portrait_url(1)  # empty portrait
    else:
        name = character.character_name
        name_with_ticker = f"{name} [{character.corporation_ticker}]"
        icon_url = character.portrait_url()
    html = bootstrap_icon_plus_name_html(icon_url, name_with_ticker, avatar=True)
    return UserForDisplay(
        name_with_ticker=name_with_ticker,
        name=name,
        html=html,
        character=character,
        icon_url=icon_url,
        user=user,
    )
