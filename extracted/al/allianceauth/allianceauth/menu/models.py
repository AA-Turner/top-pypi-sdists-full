from typing import ClassVar

from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from allianceauth.authentication.models import Permission, User
from allianceauth.menu.constants import DEFAULT_FOLDER_ICON_CLASSES

from .constants import DEFAULT_MENU_ITEM_ORDER
from .core.menu_item_hooks import MenuItemHookCustom
from .managers import MenuItemManager


class MenuItem(models.Model):
    """An item in the sidebar menu.

    Some of these objects are generated from `MenuItemHook` objects.
    To avoid confusion we are using the same same field names.user defined
    """

    class MenuItemType(models.TextChoices):
        """The type of a menu item."""

        APP = "app", _("app")
        FOLDER = "folder", _("folder")
        LINK = "link", _("link")

    class PermissionMode(models.TextChoices):
        """How multiple permissions on a menu item are combined."""

        ANY = "any", _("Any")
        ALL = "all", _("All")

    text = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name=_("text"),
        help_text=_("Text to show on menu"),
    )
    order = models.IntegerField(
        default=DEFAULT_MENU_ITEM_ORDER,
        db_index=True,
        verbose_name=_("order"),
        help_text=_("Order of the menu. Lowest First"),
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("folder"),
        help_text=_("Folder this item is in (optional)"),
    )
    is_hidden = models.BooleanField(
        default=False,
        verbose_name=_("is hidden"),
        help_text=_(
            "Hide this menu item."
            "If this item is a folder all items under it will be hidden too"
        ),
    )

    # app related properties
    hook_hash = models.CharField(
        max_length=64,
        default=None,
        null=True,
        unique=True,
        editable=False,
        help_text="hash of a menu item hook. Must be nullable for unique comparison.",
    )

    # user defined properties
    classes = models.CharField(
        max_length=150,
        default="",
        blank=True,
        verbose_name=_("icon classes"),
        help_text=_(
            "Font Awesome classes to show as icon on menu, "
            "e.g. <code>fa-solid fa-house</code>"
        ),
    )
    url = models.TextField(
        default="",
        verbose_name=_("url"),
        help_text=_("External URL this menu items will link to"),
    )
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        verbose_name=_("Permissions"),
        help_text=_(
            "Restrict this menu item to users with these permissions. "
            "When empty this item is visible to everyone. Affects only menu items that are created via admin site."
        ),
    )
    permission_mode = models.CharField(
        max_length=3,
        choices=PermissionMode.choices,
        default=PermissionMode.ANY,
        verbose_name=_("Permission mode"),
        help_text=_(
            "Whether a user needs any or all of the assigned permissions to see this menu item."
        ),
    )

    objects: ClassVar[MenuItemManager] = MenuItemManager()

    def __str__(self) -> str:
        return self.text

    def save(self, *args, **kwargs) -> None:
        if not self.hook_hash:
            self.hook_hash = None  # empty strings can create problems
        return super().save(*args, **kwargs)

    @property
    def item_type(self) -> MenuItemType:
        """Return the type of this menu item."""
        if self.hook_hash:
            return MenuItem.MenuItemType.APP

        if not self.url:
            return MenuItem.MenuItemType.FOLDER

        return MenuItem.MenuItemType.LINK

    @property
    def is_app_item(self) -> bool:
        """Return True if this is an app item, else False."""
        return self.item_type is MenuItem.MenuItemType.APP

    @property
    def is_child(self) -> bool:
        """Return True if this item is a child, else False."""
        return bool(self.parent_id)

    @property
    def is_folder(self) -> bool:
        """Return True if this item is a folder, else False."""
        return self.item_type is MenuItem.MenuItemType.FOLDER

    @property
    def is_link_item(self) -> bool:
        """Return True if this item is a link item, else False."""
        return self.item_type is MenuItem.MenuItemType.LINK

    @property
    def is_user_defined(self) -> bool:
        """Return True if this item is user defined."""
        return self.item_type is not MenuItem.MenuItemType.APP

    def user_has_access(self, user: User | AnonymousUser) -> bool:
        """Return True if the given user may see this menu item.

        Items with no assigned permissions are visible to everyone.
        """
        perms = [
            f"{perm.content_type.app_label}.{perm.codename}"
            for perm in self.permissions.all()
        ]
        if not perms:
            return True

        if self.permission_mode == MenuItem.PermissionMode.ALL:
            return user.has_perms(perms)

        return any(user.has_perm(perm) for perm in perms)

    def to_hook_obj(self) -> MenuItemHookCustom:
        """Convert to hook object for rendering."""
        if self.is_app_item:
            raise ValueError("The related hook objects should be used for app items.")

        hook_obj = MenuItemHookCustom(
            text=self.text, classes=self.classes, url_name="", order=self.order
        )
        hook_obj.navactive = []
        if self.is_folder and not self.classes:
            hook_obj.classes = DEFAULT_FOLDER_ICON_CLASSES

        hook_obj.url = self.url
        hook_obj.is_folder = self.is_folder
        hook_obj.html_id = f"id-folder-{self.pk}" if self.is_folder else ""
        return hook_obj
