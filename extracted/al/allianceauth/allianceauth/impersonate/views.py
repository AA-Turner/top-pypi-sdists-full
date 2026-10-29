from hijack.views import AcquireUserView, ReleaseUserView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .permissions import can_impersonate

# Display preferences kept only in the session.
# MINIMIZE_SIDEBAR is not listed, UserSettingsMiddleware reloads it from the profile on every response.
PRESERVED_SESSION_KEYS = ("THEME", "NIGHT_MODE")


class PreserveDisplayPreferencesMixin:
    """Keep the person's display preferences when switching user.

    login() flushes the session when the user changes, which would drop
    them back to the default theme on both start and stop.
    """

    def post(self, request, *args, **kwargs):
        preserved = {key: request.session[key] for key in PRESERVED_SESSION_KEYS if key in request.session}
        response = super().post(request, *args, **kwargs)
        request.session.update(preserved)
        return response


class ImpersonateConfirmView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Explain what is about to happen before starting, so it is never a single stray click."""
    template_name = 'impersonate/confirm.html'
    raise_exception = True

    def get_target(self):
        return get_object_or_404(
            User.objects.select_related('profile__main_character', 'profile__state'),
            pk=self.kwargs['user_pk'],
        )

    def test_func(self):
        return can_impersonate(hijacker=self.request.user, hijacked=self.get_target())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target'] = self.get_target()
        return context


class ImpersonateStartView(PreserveDisplayPreferencesMixin, AcquireUserView):
    raise_exception = True
    success_url = reverse_lazy('authentication:dashboard')

    def test_func(self):
        return can_impersonate(hijacker=self.request.user, hijacked=self.get_object())


class ImpersonateStopView(PreserveDisplayPreferencesMixin, ReleaseUserView):
    success_url = reverse_lazy('authentication:dashboard')
