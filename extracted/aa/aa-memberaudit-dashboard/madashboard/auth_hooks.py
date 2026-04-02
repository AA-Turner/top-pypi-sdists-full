"""Hook into Alliance Auth"""

# Django
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth import hooks

from .views import dashboard_memberaudit_check


class MemberCheckDashboardHook(hooks.DashboardItemHook):
    def __init__(self):
        super().__init__(view_function=dashboard_memberaudit_check, order=5)


@hooks.register("dashboard_hook")
def register_membercheck_hook():
    return MemberCheckDashboardHook()
