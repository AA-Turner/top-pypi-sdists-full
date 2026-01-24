import urllib
from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.urls import resolve
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from dynamic_preferences.models import global_preferences_registry
from rest_framework import exceptions
from rest_framework.authtoken.models import Token as DRFToken

from .users import User


class Token(DRFToken):
    """
    Short-Lived and short-usage Token to be used as DRF token
    """

    valid_until = models.DateTimeField(blank=True, null=True, verbose_name=_("Valid Until"))
    protected_view_name = models.CharField(
        blank=True,
        null=True,
        max_length=256,
        verbose_name="Protected View-Name",
        help_text="If specified, only view that revert to this viewname will accept this token",
    )
    number_usage_left = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("Number of allowed usage"))
    is_valid = models.BooleanField(default=True, verbose_name=_("Is Valid"))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="auth_tokens", on_delete=models.CASCADE, verbose_name=_("User")
    )

    def __str__(self):
        if self.key:
            return self.key
        return ""

    def check_validity_for_endpoint(self, view_name: str, current_time: datetime) -> True:
        """
        Handle the logic for token validity. Expect this method to be called from a request access
        Args:
            view_name: view name to check authentication against
            current_time: The time to check authentication validity

        Returns:
            True if the token is valid and authentication can be granted
        """
        if not current_time:
            current_time = timezone.now()
        if not self.is_valid:
            raise exceptions.AuthenticationFailed("Token is not valid anymore")
        if self.valid_until is not None and self.valid_until < current_time:
            raise exceptions.AuthenticationFailed("Token has expired")

        if self.protected_view_name and not view_name == self.protected_view_name:
            raise exceptions.AuthenticationFailed("Token has limited scope that doesn't match the requested endpoint")
        if self.number_usage_left is not None:
            if self.number_usage_left <= 0:
                raise exceptions.AuthenticationFailed("Token usage exhausted")
            self.number_usage_left -= 1
            self.save()
        return True

    @classmethod
    def generate_shareable_link(
        cls,
        endpoint: str,
        user: "User",
        creation_time: datetime | None = None,
        protected_view_name: str = None,
        token: str | None = None,
    ) -> str:
        """
        Given an endpoint and a user, generate a shorted live token valid from now to the default validity time and appends it to the base endpoint query parameters
        Args:
            endpoint: endpoint to append the token to
            user: token's owner
        Returns:
            an valid endpoint with the token as query parameter
        """
        if not creation_time:
            creation_time = timezone.now()
        global_preferences = global_preferences_registry.manager()
        valid_until = creation_time + timedelta(
            hours=global_preferences["authentication__default_token_validity_in_hours"]
        )

        parse_url = urllib.parse.urlsplit(urllib.parse.unquote(endpoint))
        endpoint = parse_url.path
        base_params = dict(urllib.parse.parse_qsl(parse_url.query))
        if not token:
            token = Token.generate_token_for_user(
                user,
                valid_until=valid_until,
                protected_view_name=resolve(endpoint).view_name if not protected_view_name else protected_view_name,
            ).key
        base_params["token"] = token

        if parse_url.scheme and parse_url.netloc:
            endpoint = parse_url.scheme + "://" + parse_url.netloc + endpoint
        params_repr = "&".join([f"{k}={v}" for k, v in base_params.items()])
        return endpoint + f"?{params_repr}"

    @classmethod
    def generate_token_for_user(
        cls,
        user: "User",
        valid_until: datetime | None = None,
        number_of_usages: int | None = None,
        protected_view_name: str | None = None,
    ):
        """
        Generate a token for a user. We assume uniqueness between user and protected_view_name to avoid crowding our table.
        Args:
            user: Token's owner
            valid_until: Token maximum datetime validity
            number_of_usages: Token maximum token usages
            protected_view_name: Token restricted view
        Returns:
            A valid Token
        """

        token, created = Token.objects.get_or_create(
            user=user,
            protected_view_name=protected_view_name,
            defaults={"valid_until": valid_until, "number_usage_left": number_of_usages},
        )
        if not created:
            token.number_usage_left = number_of_usages
            token.valid_until = valid_until
            token.is_valid = True
            token.save()
        return token

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")
        constraints = (models.UniqueConstraint(name="unique_token", fields=("user", "protected_view_name")),)
