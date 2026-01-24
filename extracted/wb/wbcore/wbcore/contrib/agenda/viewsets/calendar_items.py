from datetime import timedelta
from io import StringIO

from django.db.models import Case, Q, QuerySet, Value, When
from django.http import HttpResponse
from django.utils import timezone
from django.utils.functional import cached_property
from ics import Calendar
from psycopg.types.range import TimestamptzRange
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny

from wbcore import viewsets
from wbcore.contrib.authentication.authentication import QueryTokenAuthentication
from wbcore.contrib.directory.models import Person
from wbcore.utils.itertools import get_inheriting_subclasses

from ..filters import CalendarItemFilter
from ..models import CalendarItem
from ..serializers import (
    CalendarItemModelSerializer,
    CalendarItemRepresentationSerializer,
)
from ..signals import draggable_calendar_item_ids
from .display import CalendarItemDisplay
from .endpoints import CalendarItemEndpointConfig
from .titles import CalendarItemTitleConfig


class CalendarItemRepresentationViewSet(viewsets.RepresentationViewSet):
    queryset = CalendarItem.objects.all()
    serializer_class = CalendarItemRepresentationSerializer


class CalendarItemMetaClass(type(viewsets.ModelViewSet)):
    def __new__(cls, *args, **kwargs):
        _class = super().__new__(cls, *args, **kwargs)
        dependant_identifiers = []
        for subclass in get_inheriting_subclasses(_class):
            if identifier := getattr(subclass, "IDENTIFIER", None):
                dependant_identifiers.append(identifier)
        _class.DEPENDANT_IDENTIFIERS = dependant_identifiers
        return _class


class CalendarItemViewSet(viewsets.ModelViewSet, metaclass=CalendarItemMetaClass):
    display_config_class = CalendarItemDisplay
    endpoint_config_class = CalendarItemEndpointConfig
    filterset_class = CalendarItemFilter
    search_fields = ("title",)
    serializer_class = CalendarItemModelSerializer
    title_config_class = CalendarItemTitleConfig
    ordering = ("period__startswith", "id")
    queryset = CalendarItem.objects.all()

    @cached_property
    def request_profile(self):
        return getattr(self.request.user, "profile", None)

    @cached_property
    def draggable_calendar_item_ids(self) -> QuerySet[CalendarItem]:
        """
        Property to store the unioned queryset of draggable calendar items. Each module inheriting from CalendarItem are expected to define the signal receiver
        """
        qs = CalendarItem.objects.none()
        for _, union_qs in draggable_calendar_item_ids.send(CalendarItem, request=self.request):
            qs = qs.union(union_qs)
        return qs

    @cached_property
    def allowed_privates_calendar_item_ids(self) -> list[int]:
        if self.request_profile:
            return list(
                CalendarItem.objects.filter(
                    entities=self.request_profile, visibility=CalendarItem.Visibility.PRIVATE
                ).values_list("id", flat=True)
            )
        return list()

    @cached_property
    def has_user_administrate_permission(self) -> bool:
        return CalendarItem.has_user_administrate_permission(self.request.user)

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .annotate(
                is_draggable=Case(When(id__in=self.draggable_calendar_item_ids, then=True), default=False),
                is_private=Case(
                    When(
                        Q(visibility=CalendarItem.Visibility.PRIVATE)
                        & ~Q(id__in=self.allowed_privates_calendar_item_ids),
                        then=True,
                    ),
                    default=False,
                ),
            )
        )
        if self.has_user_administrate_permission:
            qs = qs.annotate(is_confidential=Value(False))
        else:
            qs = qs.annotate(
                is_confidential=Case(
                    When(visibility=CalendarItem.Visibility.CONFIDENTIAL, then=True),
                    default=False,
                )
            )
        return qs.prefetch_related("entities")


class InfiniteCalendarItemViewSet(CalendarItemViewSet):
    pagination_class = None


class OwnCalendarItemViewSet(CalendarItemViewSet):
    def get_queryset(self):
        if self.request_profile:
            return super().get_queryset().filter(is_cancelled=False, entities=self.request_profile)
        return super().get_queryset().none()


@api_view(["GET"])
@permission_classes([AllowAny])
@authentication_classes([QueryTokenAuthentication])
def get_ics(request):
    """
    API Calendar ICS request endpoint

    Return the ICS formatted calendar for the user with token
    """
    conference_room = request.GET.get("conference_room", "False") == "True"
    team = request.GET.get("team", "False") == "True"
    only_today = request.GET.get("only_today", "False") == "True"
    if profile := getattr(request.user, "profile", None):
        qs = CalendarItem.objects.exclude(is_cancelled=False)
        if conference_room:
            qs = qs.filter(conference_room=True).distinct()
        elif team:
            qs = CalendarItem.objects.filter(entities__in=Person.objects.filter_only_internal().values("id"))
        else:
            qs = CalendarItem.objects.filter(entities__id=profile.id)
        if only_today:
            minimum_date = timezone.now().date()
            maximum_date = minimum_date + timedelta(days=1)
        else:
            minimum_date = timezone.now() - timedelta(days=30)
            maximum_date = timezone.now() + timedelta(days=30)
        min_max_range = TimestamptzRange(minimum_date, maximum_date)
        gen = qs.filter(period__contained_by=min_max_range)

        ical = Calendar()
        for occurence in gen:
            start = occurence.period.lower
            end = occurence.period.upper
            activity = occurence
            event = activity.to_ics(start, end)
            if event:
                ical.events.add(event)
        data = StringIO(str(ical))
        response = HttpResponse(data, content_type="text/calendar")
        response["Content-Disposition"] = f'attachment; filename="{profile.computed_str}.ics"'
        return response
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
