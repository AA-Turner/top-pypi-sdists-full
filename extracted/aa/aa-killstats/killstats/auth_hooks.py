"""Hook into Alliance Auth"""

# Django
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# AA Killstats
from killstats import app_settings, urls


class KillstatsMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        super().__init__(
            f"{app_settings.KILLSTATS_APP_NAME}",
            "fas fa-star fa-fw",
            "killstats:index",
            navactive=["killstats:"],
        )

    def render(self, request):
        if request.user.has_perm("killstats.basic_access"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    """Register the menu item"""

    return KillstatsMenuItem()


@hooks.register("url_hook")
def register_urls():
    """Register app urls"""

    return UrlHook(urls, "killstats", r"^killstats/")


@hooks.register("charlink")
def register_charlink_hook():
    return "killstats.thirdparty.charlink_hook"
