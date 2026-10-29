__lazy_modules__ = ["allianceauth.authentication.models", "allianceauth.services.modules.mumble.models"]

import logging
from typing import TYPE_CHECKING

from django.utils.crypto import get_random_string
from passlib.hash import bcrypt_sha256

from django.db import models

if TYPE_CHECKING:
    from allianceauth.authentication.models import User

    from .models import MumbleUser

logger = logging.getLogger(__name__)


class MumbleManager(models.Manager["MumbleUser"]):
    @staticmethod
    def get_username(user: "User") -> str:
        return user.profile.main_character.character_name  # main character as the user.username may be incorrect

    @staticmethod
    def sanitise_username(username: str) -> str:
        return username.replace(" ", "_")

    @staticmethod
    def gen_pwhash(password: str) -> str:
        return bcrypt_sha256.encrypt(password.encode('utf-8'))

    def create(self, user: "User") -> "MumbleUser | bool":
        try:
            username = self.get_username(user)
            logger.debug(f"Creating mumble user with username {username}")
            username_clean = self.sanitise_username(username)
            password = get_random_string(length=20)
            pwhash = self.gen_pwhash(password)
            logger.debug("Proceeding with mumble user creation: clean username {}, pwhash starts with {}".format(
                username_clean, pwhash[0:5]))
            logger.info(f"Creating mumble user {username_clean}")

            result = super().create(user=user, username=username_clean, pwhash=pwhash)
            result.credentials.update({'username': result.username, 'password': password})
            return result
        except AttributeError:  # No Main or similar errors
            return False
