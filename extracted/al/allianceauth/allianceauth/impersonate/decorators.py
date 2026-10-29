from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from .utils import is_impersonating


def not_while_impersonating(view_func):
    """Refuse a view while the user is being impersonated.

    Use on views that would attach the real person's identities (EVE characters,
    ESI tokens, external service accounts) to the impersonated user.
    Safe to use whether or not ``allianceauth.impersonate`` is installed.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if is_impersonating(request):
            messages.error(request, _('This action is not available while impersonating another user.'))
            return redirect('authentication:dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
