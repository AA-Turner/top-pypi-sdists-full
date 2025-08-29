from django.db.models import CharField, F, OuterRef, Q, Subquery, Value
from django.db.models.functions import Concat
from django.utils.functional import cached_property
from dynamic_preferences.registries import global_preferences_registry
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_fuzzysearch.search import RankedFuzzySearchFilter
from reversion.views import RevisionMixin

from wbcore.contrib.directory.models import (
    ClientManagerRelationship,
    EmailContact,
    EmployerEmployeeRelationship,
    Relationship,
    RelationshipType,
    TelephoneContact,
)
from wbcore.filters import DjangoFilterBackend
from wbcore.viewsets import ModelViewSet, ReadOnlyModelViewSet, RepresentationViewSet

from ..filters import ClientManagerFilter, RelationshipEntryFilter, RelationshipFilter
from ..permissions import IsClientManagerRelationshipAdmin
from ..serializers import (
    ClientManagerModelSerializer,
    ClientManagerRelationshipRepresentationSerializer,
    EmployerEmployeeRelationshipSerializer,
    RelationshipModelSerializer,
    RelationshipRepresentationSerializer,
    RelationshipTypeModelSerializer,
    RelationshipTypeRepresentationSerializer,
    UserIsClientModelSerializer,
)
from .buttons import ClientManagerRelationshipButtonConfig, EmployerEmployeeRelationshipButtonConfig
from .display import (
    ClientManagerModelDisplay,
    EmployeeEmployerDisplayConfig,
    EmployerEmployeeDisplayConfig,
    EmployerEmployeeRelationshipDisplayConfig,
    RelationshipDisplayConfig,
    RelationshipEntryDisplay,
    RelationshipTypeDisplayConfig,
    UserIsClientDisplayConfig,
)
from .endpoints import (
    ClientManagerEndpoint,
    EmployeeEmployerEndpointConfig,
    EmployerEmployeeEndpointConfig,
    RelationshipEntryModelEndpoint,
    UserIsClientEndpointConfig,
)
from .titles import (
    ClientManagerTitleConfig,
    EmployerEmployeeRelationshipTitleConfig,
    RelationshipEntryModelTitleConfig,
    RelationshipTypeModelTitleConfig,
    UserIsClientTitleConfig,
)


class RelationshipRepresentationViewSet(RepresentationViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipRepresentationSerializer


class RelationshipModelViewSet(RevisionMixin, ModelViewSet):
    queryset = Relationship.objects.select_related(
        "relationship_type",
        "from_entry",
        "to_entry",
    )
    serializer_class = RelationshipModelSerializer

    display_config_class = RelationshipDisplayConfig

    search_fields = ("computed_str",)
    filterset_class = RelationshipFilter
    ordering = ["relationship_type", "to_entry", "id"]


class RelationshipModelEntryViewSet(RelationshipModelViewSet):
    title_config_class = RelationshipEntryModelTitleConfig
    display_config_class = RelationshipEntryDisplay
    endpoint_config_class = RelationshipEntryModelEndpoint
    filterset_class = RelationshipEntryFilter

    def get_queryset(self):
        _id = self.kwargs["entry_id"]
        return super().get_queryset().filter(Q(from_entry=_id)).distinct()


class RelationshipTypeRepresentationViewSet(RepresentationViewSet):
    queryset = RelationshipType.objects.all()
    serializer_class = RelationshipTypeRepresentationSerializer

    search_fields = ("title",)


class RelationshipTypeModelViewSet(ModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/relationshiptype.md"
    title_config_class = RelationshipTypeModelTitleConfig

    display_config_class = RelationshipTypeDisplayConfig
    serializer_class = RelationshipTypeModelSerializer
    queryset = RelationshipType.objects.select_related("counter_relationship")
    ordering_fields = (
        "title",
        "counter_relationship",
    )
    ordering = ("title",)


class EmployerEmployeeRelationshipModelViewSet(ModelViewSet):
    serializer_class = EmployerEmployeeRelationshipSerializer

    display_config_class = EmployerEmployeeRelationshipDisplayConfig
    button_config_class = EmployerEmployeeRelationshipButtonConfig
    title_config_class = EmployerEmployeeRelationshipTitleConfig
    ordering_fields = ("primary", "position__title", "position_name")

    filterset_fields = {"position": ["exact"], "primary": ["exact"], "position_name": ["exact", "icontains"]}
    queryset = EmployerEmployeeRelationship.objects.all().prefetch_related("employee", "employer", "position")


class EmployeeEmployerModelViewSet(EmployerEmployeeRelationshipModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/employeecompany.md"

    endpoint_config_class = EmployeeEmployerEndpointConfig
    display_config_class = EmployeeEmployerDisplayConfig

    ordering = ["employee__computed_str", "id"]
    ordering_fields = ["employee__computed_str"]
    search_fields = ["employee__computed_str"]
    filterset_fields = {"employee": ["exact"]}

    def get_queryset(self):
        return super().get_queryset().filter(employer=self.kwargs["employer_id"])


class EmployerEmployeeModelViewSet(EmployerEmployeeRelationshipModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/employerperson.md"

    endpoint_config_class = EmployerEmployeeEndpointConfig
    display_config_class = EmployerEmployeeDisplayConfig

    ordering = ["employer__computed_str", "id"]
    ordering_fields = ["employer__computed_str"]
    search_fields = ["employer__computed_str"]
    filterset_fields = {"employer": ["exact"]}

    def get_queryset(self):
        return super().get_queryset().filter(employee=self.kwargs["employee_id"])


class SystemEmployeeModelViewSet(EmployeeEmployerModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/systememployee.md"

    def __init__(self, **kwargs):
        global_preferences = global_preferences_registry.manager()
        employer_id = global_preferences["directory__main_company"]
        self.kwargs["employer_id"] = employer_id
        super().__init__(**kwargs)


class ClientManagerRelationshipRepresentationViewSet(RepresentationViewSet):
    serializer_class = ClientManagerRelationshipRepresentationSerializer
    queryset = ClientManagerRelationship.objects.all()


class ClientManagerViewSet(RevisionMixin, ModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/clientmanagerrelationship.md"
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        RankedFuzzySearchFilter,
    )
    min_rank = 0.25
    search_fields = ("client__computed_str", "relationship_manager__computed_str")
    ordering_fields = ("client__computed_str", "created", "relationship_manager__computed_str")
    ordering = ("-created", "id")
    queryset = ClientManagerRelationship.objects.none()
    serializer_class = ClientManagerModelSerializer
    display_config_class = ClientManagerModelDisplay
    button_config_class = ClientManagerRelationshipButtonConfig
    endpoint_config_class = ClientManagerEndpoint
    filterset_class = ClientManagerFilter
    title_config_class = ClientManagerTitleConfig

    @cached_property
    def is_modifiable(self):
        if "pk" in self.kwargs and (obj := self.get_object()):
            return obj.status == ClientManagerRelationship.Status.DRAFT
        return self.new_mode

    def get_queryset(self):
        user = self.request.user
        profile = user.profile

        if user.is_superuser or profile.is_internal:  # TODO: Can TPM have access to this view?
            return ClientManagerRelationship.objects.select_related("client", "relationship_manager")
        return ClientManagerRelationship.objects.none()

    @action(detail=False, methods=["PATCH"], permission_classes=[IsClientManagerRelationshipAdmin])
    def approveallpendingrequests(self, *args, **kwargs):
        for request in ClientManagerRelationship.objects.filter(status=ClientManagerRelationship.Status.PENDINGADD):
            request.approve(by=self.request.user)
            request.save()
        for request in ClientManagerRelationship.objects.filter(status=ClientManagerRelationship.Status.PENDINGREMOVE):
            request.approveremoval(by=self.request.user)
            request.save()
        return Response({}, status=status.HTTP_200_OK)


class UserIsClientViewSet(ReadOnlyModelViewSet):
    queryset = ClientManagerRelationship.objects.all()
    LIST_DOCUMENTATION = "directory/markdown/documentation/userisclient.md"
    display_config_class = UserIsClientDisplayConfig
    title_config_class = UserIsClientTitleConfig
    endpoint_config_class = UserIsClientEndpointConfig
    serializer_class = UserIsClientModelSerializer
    ordering = ["-primary", "id"]
    ordering_fields = (
        "relationship_manager_name",
        "relationship_manager_email",
        "relationship_manager_phone_number",
    )

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                client_id=self.request.user.profile.id,
                status__in=[ClientManagerRelationship.Status.APPROVED, ClientManagerRelationship.Status.PENDINGREMOVE],
            )
            .annotate(
                relationship_manager_name=Concat(
                    F("relationship_manager__first_name"), Value(" "), F("relationship_manager__last_name")
                ),
                relationship_manager_email=Subquery(
                    EmailContact.objects.filter(primary=True, entry=OuterRef("relationship_manager")).values(
                        "address"
                    )[:1],
                    output_field=CharField(),
                ),
                relationship_manager_phone_number=Subquery(
                    TelephoneContact.objects.filter(primary=True, entry=OuterRef("relationship_manager")).values(
                        "number"
                    )[:1],
                    output_field=CharField(),
                ),
            )
        )
