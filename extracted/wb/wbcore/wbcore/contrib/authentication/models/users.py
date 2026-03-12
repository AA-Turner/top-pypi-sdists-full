# -*- encoding: utf-8 -*-
import unicodedata
import uuid
from contextlib import suppress

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group as DjangoBaseGroup
from django.contrib.auth.models import Permission as DjangoBasePermission
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from wbcore.signals import pre_merge
from wbcore.utils.models import MergeError


class UserQuerySet(models.QuerySet):
    def filter_internal(self):
        return self.filter(is_internal=True)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_queryset(self) -> UserQuerySet:
        return UserQuerySet(self.model, using=self._db)

    def filter_internal(self):
        return self.get_queryset().filter_internal()

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize("NFKC", force_str(username))

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError(gettext("No E-Mail provided"))
        email = self.normalize_email(email)
        if not username:
            raise ValueError(gettext("No Username provided"))
        username = UserManager.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_register", True)
        return self._create_user(username, email.lower(), password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_register", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_("E-Mail"), unique=True)
    username = models.CharField(_("username"), max_length=255, unique=True)
    profile = models.OneToOneField("directory.Person", on_delete=models.PROTECT, related_name="user_account")
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Specifies whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Specifies whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    is_register = models.BooleanField(
        _("register"), default=True, help_text=_("Specifies whether this user has registered its email. ")
    )
    is_internal = models.BooleanField(
        _("Internal"),
        default=False,
        help_text="If true, define this user as internal which grants specific permissions.",
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    metadata = models.JSONField(default=dict, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = "AUTH_USER_MODEL"
        permissions = [("administrate_user", "Administrate Users"), ("is_internal_user", "Internal User")]

    def get_full_name(self):
        full_name = "%s %s" % (self.profile.first_name, self.profile.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.profile.first_name

    def save(self, *args, **kwargs):
        from wbcore.contrib.directory.models.entries import Person

        self.username = self.username.lower()  # make sure username is lower case
        self.profile = Person.get_or_create_with_user(self)
        super().save(*args, **kwargs)

    def reset_password(self, request=None):
        """
        Create the Reset Password email including the new password to be used for the next login
        """
        from django.contrib.auth.forms import PasswordResetForm

        reset_password_form = PasswordResetForm(data={"email": self.email})
        if reset_password_form.is_valid():
            reset_password_form.save(
                request=request,
                email_template_name="authentication/email/password_reset_email.html",
                html_email_template_name="authentication/email/password_reset_email_html.html",
            )

    def generate_temporary_token(self):
        return PasswordResetTokenGenerator().make_token(self)

    def verify_temporary_token(self, token):
        return PasswordResetTokenGenerator().check_token(self, token)

    @classmethod
    def generate_username(cls, *names) -> str:
        username = "-".join(map(lambda x: x.lower(), names))
        similar = User.objects.filter(username__iregex=f"^({username}(-[0-9]*)*)$").count()
        return username if similar == 0 else f"{username}-{similar + 1}"

    @classmethod
    def create_with_attributes(cls, email, password, username=None, first_name=None, last_name=None):
        if not username and first_name and last_name:
            username = cls.generate_username(first_name, last_name)
        if not username:
            raise ValueError(gettext("You need to specify a username or a pair of first and last name"))
        return cls.objects.create_user(
            username, email, password, is_staff=False, is_superuser=False, is_active=False, is_register=False
        )

    @property
    def generic_auth_token_key(self) -> str | None:
        """
        Return generic valid useable token
        """
        token = self.auth_tokens.get_or_create(
            valid_until__isnull=True,
            protected_view_name__isnull=True,
            number_usage_left__isnull=True,
            defaults={
                "is_valid": True,
            },
        )[0]
        return token.key

    @property
    def first_name(self):
        return self.profile.first_name

    @property
    def last_name(self):
        return self.profile.last_name

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:authentication:user"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:authentication:userrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{computed_str}}"


class Group(DjangoBaseGroup):
    class Meta:
        proxy = True

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:authentication:group"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:authentication:grouprepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{name}}"


class Permission(DjangoBasePermission):
    class Meta:
        proxy = True

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:authentication:permission"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:authentication:permissionrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{name}}"


@receiver(pre_merge, sender="directory.Person")
def pre_merge_person_user(sender: models.Model, merged_object, main_object, **kwargs):
    with suppress(User.DoesNotExist):
        user = User.objects.get(profile=merged_object)
        if User.objects.filter(profile=main_object).exists():
            raise MergeError(
                f"we cannot safely merge person {merged_object} into {main_object}: A user profile already exists for {main_object}"
            )
        else:
            user.profile = main_object
            user.save()
