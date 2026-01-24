from functools import cached_property

from django.db.models.functions import Coalesce

from wbcore import viewsets
from wbcore.contrib.color.models import TransparencyMixin
from wbcore.contrib.directory.models import (
    ClientManagerRelationship,
    Company,
    Entry,
    Person,
)
from wbcore.contrib.i18n.viewsets import ModelTranslateMixin
from wbcore.utils.views import MergeMixin

from ...authentication.models import UserActivity
from ..filters import CompanyFilter, EntryFilter, PersonFilter, UserIsManagerFilter
from ..serializers import (
    BankModelSerializer,
    CompanyModelListSerializer,
    CompanyModelSerializer,
    CompanyRepresentationSerializer,
    EntryModelSerializer,
    EntryRepresentationSerializer,
    NewPersonModelSerializer,
    PersonModelListSerializer,
    PersonModelSerializer,
    PersonRepresentationSerializer,
)
from .buttons.entries import (
    CompanyModelButtonConfig,
    EntryModelButtonConfig,
    PersonModelButtonConfig,
)
from .display.entries import (
    BankModelDisplay,
    CompanyModelDisplay,
    EntryModelDisplay,
    PersonModelDisplay,
    UserIsManagerDisplayConfig,
)
from .endpoints.entries import (
    CompanyModelEndpointConfig,
    CompanyRepresentationEndpointConfig,
    PersonModelEndpointConfig,
    PersonRepresentationEndpointConfig,
    UserIsManagerEndpointConfig,
)
from .mixins import EntryPermissionMixin
from .previews import EntryPreviewConfig
from .titles.entries import (
    CompanyModelTitleConfig,
    PersonModelTitleConfig,
    UserIsManagerTitleConfig,
)


class EntryRepresentationViewSet(EntryPermissionMixin, viewsets.RepresentationViewSet):
    min_rank = 0.25
    queryset = Entry.objects.annotate_all()
    serializer_class = EntryRepresentationSerializer
    filterset_class = EntryFilter
    ordering = ("entry_type", "id")
    ordering_fields = ("computed_str",)
    search_fields = ("computed_str", "slugify_computed_str", "emails__address")


class PersonRepresentationViewSet(EntryRepresentationViewSet):
    queryset = Person.objects.annotate_all()
    serializer_class = PersonRepresentationSerializer
    filterset_class = PersonFilter
    ONLY_READ_ONLY_ENDPOINT = False
    endpoint_config_class = PersonRepresentationEndpointConfig
    ordering_fields = ("last_name", "first_name")
    ordering = ("last_name", "first_name", "id")


class PersonInChargeRepresentationViewSet(PersonRepresentationViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(clients__isnull=False).distinct()


class CompanyRepresentationViewSet(EntryRepresentationViewSet):
    queryset = Company.objects.annotate_all()
    serializer_class = CompanyRepresentationSerializer
    ONLY_READ_ONLY_ENDPOINT = False
    endpoint_config_class = CompanyRepresentationEndpointConfig

    filterset_class = CompanyFilter
    ordering_fields = ("name",)
    ordering = ("name", "id")


class EntryModelViewSet(MergeMixin, EntryPermissionMixin, TransparencyMixin, viewsets.ModelViewSet):
    min_rank = 0.25
    search_fields = ("computed_str", "slugify_computed_str", "emails__address")
    ordering = ["computed_str", "id"]
    ordering_fields = (
        "computed_str",
        "primary_telephone",
        "primary_email",
        "primary_address",
    )
    preview_config_class = EntryPreviewConfig
    queryset = Entry.objects.annotate_all()
    serializer_class = EntryModelSerializer
    filterset_class = EntryFilter

    button_config_class = EntryModelButtonConfig
    display_config_class = EntryModelDisplay

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "addresses",
                "relationship_managers",
                "social_media",
            )
        )

    @cached_property
    def is_internal_user(self):
        return self.request.user.profile and self.request.user.profile.is_internal


class PersonModelViewSet(ModelTranslateMixin, EntryModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/person.md"
    button_config_class = PersonModelButtonConfig
    display_config_class = PersonModelDisplay
    endpoint_config_class = PersonModelEndpointConfig
    filterset_class = PersonFilter
    ordering = ["-activity_heat", "id"]
    ordering_fields = (
        "name",
        "primary_employer_repr",
        "customer_status",
        "position_in_company",
        "primary_telephone",
        "tier",
        "primary_manager_repr",
        "last_event",
        "last_event_period_endswith",
        "activity_heat",
    )

    queryset = Person.objects.annotate_all()
    serializer_class = PersonModelSerializer
    title_config_class = PersonModelTitleConfig

    def get_serializer_class(self):
        if self.get_action() in ["list", "list-metadata"]:
            return PersonModelListSerializer
        elif "pk" not in self.kwargs:
            return NewPersonModelSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if "pk" in self.kwargs:
            qs = qs.annotate(last_connection=Coalesce(UserActivity.get_latest_login_datetime_subquery(), None))
        return qs


class CompanyModelViewSet(EntryModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/company.md"
    button_config_class = CompanyModelButtonConfig
    display_config_class = CompanyModelDisplay
    endpoint_config_class = CompanyModelEndpointConfig
    filterset_class = CompanyFilter
    ordering_fields = (
        "name",
        "type",
        "tier",
        "customer_status",
        "relationship_managers",
        "last_event",
        "last_event_period_endswith",
        "activity_heat",
    )
    ordering = ["name", "id"]
    queryset = Company.objects.annotate_all().select_related("entry_ptr", "customer_status", "type")
    serializer_class = CompanyModelSerializer
    title_config_class = CompanyModelTitleConfig

    def get_serializer_class(self):
        if self.get_action() in ["list", "list-metadata"]:
            return CompanyModelListSerializer
        return super().get_serializer_class()


class BankModelViewSet(EntryModelViewSet):
    queryset = Company.objects.annotate_all()
    display_config_class = BankModelDisplay
    serializer_class = BankModelSerializer


class UserIsManagerViewSet(EntryModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/userismanager.md"
    display_config_class = UserIsManagerDisplayConfig
    title_config_class = UserIsManagerTitleConfig
    endpoint_config_class = UserIsManagerEndpointConfig
    search_fields = ("computed_str", "slugify_computed_str")
    filterset_class = UserIsManagerFilter

    def get_queryset(self):
        client_ids = ClientManagerRelationship.objects.filter(
            relationship_manager=self.request.user.profile.id,
            status__in=[ClientManagerRelationship.Status.APPROVED, ClientManagerRelationship.Status.PENDINGREMOVE],
        ).values_list("client_id", flat=True)
        return super().get_queryset().filter(id__in=client_ids)
