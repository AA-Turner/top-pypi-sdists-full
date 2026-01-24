import logging
from datetime import date, timedelta

import pandas as pd
import plotly.graph_objects as go
from django.db.models import (
    DurationField,
    ExpressionWrapper,
    F,
    OuterRef,
    Subquery,
    Sum,
    Value,
)
from django.db.models.fields import FloatField
from django.db.models.functions import Coalesce, Concat, ExtractMinute
from django.utils.translation import gettext as _
from rest_framework import filters

from wbcore import viewsets
from wbcore.filters import DjangoFilterBackend

from .. import serializers
from ..filters import UserActivityChartFilter
from ..models import User, UserActivity
from ..serializers import UserActivityTableSerializer
from .display.user_activities import (
    UserActivityModelDisplay,
    UserActivityModelUserDisplay,
    UserActivityTableDisplayConfig,
)
from .endpoints.user_activities import (
    UserActivityModelEndpointConfig,
    UserActivityTableEndpointConfig,
    UserActivityUserModelEndpointConfig,
)
from .titles.user_activities import (
    UserActivityChartTitleConfig,
    UserActivityModelTitleConfig,
    UserActivityTableTitleConfig,
    UserActivityUserChartTitleConfig,
    UserActivityUserModelTitleConfig,
)

logger = logging.getLogger()


class UserActivityModelViewSet(viewsets.ModelViewSet):
    filterset_fields = {
        "IP": ["exact", "icontains"],
        "user": ["exact"],
        "date": ["gte", "exact", "lte"],
        "latest_refresh": ["gte", "exact", "lte"],
        "user_agent_info": ["exact", "icontains"],
    }

    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    search_fields = ("user__email", "user_agent_info")
    ordering_fields = ("date", "latest_refresh", "time_online_minute")
    ordering = ["-date"]

    queryset = UserActivity.objects.all()
    serializer_class = serializers.UserActivitySerializer

    display_config_class = UserActivityModelDisplay
    endpoint_config_class = UserActivityModelEndpointConfig
    title_config_class = UserActivityModelTitleConfig

    def get_queryset(self):
        expression = ExpressionWrapper(F("latest_refresh") - F("date"), output_field=DurationField())
        return UserActivity.objects.annotate(time_online_minute=ExtractMinute(expression))


class UserActivityUserModelViewSet(UserActivityModelViewSet):
    display_config_class = UserActivityModelUserDisplay
    endpoint_config_class = UserActivityUserModelEndpointConfig
    title_config_class = UserActivityUserModelTitleConfig

    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = {
        "IP": ["exact"],
        "date": ["gte", "exact", "lte"],
        "latest_refresh": ["gte", "exact", "lte"],
        "user_agent_info": ["exact", "icontains"],
    }

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs["user_id"])
        return super().get_queryset().filter(user=user)


class UserActivityTable(viewsets.ModelViewSet):
    queryset = UserActivity.objects.all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serializer_class = UserActivityTableSerializer
    ordering_fields = ["user_repr", "today_activity", "yesterday_activity", "beforeyesterday_activity"]
    ordering = ["-today_activity"]
    search_fields = ["user_repr"]

    endpoint_config_class = UserActivityTableEndpointConfig
    title_config_class = UserActivityTableTitleConfig
    display_config_class = UserActivityTableDisplayConfig

    def get_queryset(self):
        expression = ExpressionWrapper(F("latest_refresh") - F("date"), output_field=DurationField())

        def get_time_day(day):
            return Coalesce(
                Subquery(
                    UserActivity.objects.filter(user__id=OuterRef("pk"), date__date=day)
                    .annotate(_time_online_minute=ExtractMinute(expression))
                    .values("user")
                    .annotate(total_time=Sum("_time_online_minute"))
                    .values("total_time")[:1],
                    output_field=FloatField(),
                ),
                0.0,
            )

        today = date.today()
        qs = User.objects.annotate(
            beforeyesterday_activity=get_time_day(today - timedelta(days=2)),
            today_activity=get_time_day(today),
            yesterday_activity=get_time_day(today - timedelta(days=1)),
            user_repr=F("profile__computed_str"),
        )
        return qs


class UserActivityChart(viewsets.ChartViewSet):
    queryset = UserActivity.objects.all()
    title_config_class = UserActivityChartTitleConfig
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserActivityChartFilter

    def get_queryset(self):
        return UserActivity.objects.all().annotate(
            username=Concat(F("user__profile__first_name"), Value(" "), F("user__profile__last_name"))
        )

    def get_plotly(self, queryset):
        fig = go.Figure()
        if queryset.count() > 0:
            df = pd.DataFrame(queryset.order_by("-date").values("latest_refresh", "date", "username"))

            df.date = pd.to_datetime(df.date).dt.round("Min")
            df.latest_refresh = pd.to_datetime(df.latest_refresh).dt.round("Min")
            min_date = df.date.min()
            max_date = df.latest_refresh.max()
            freq = "H"
            if (max_date - min_date).total_seconds() < 86400:
                freq = "D"
            min_date = min_date.floor(freq)
            max_date = max_date.ceil(freq)

            for username, dff in df.groupby("username"):
                cum_times = pd.Series(
                    dt
                    for group in [
                        pd.date_range(start, end, freq="Min")
                        for start, end in zip(dff.date, dff.latest_refresh, strict=False)
                    ]
                    for dt in group
                ).value_counts()
                fig.add_trace(
                    go.Histogram(
                        histfunc="sum",
                        xbins=dict(start=min_date, end=max_date, size=3600000),  # bins used for histogram
                        y=cum_times.values,
                        x=cum_times.index,
                        bingroup=1,
                        name=username,
                    ),
                )
            fig.update_layout(
                barmode="stack",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                title=_("<b>User Activity</b>"),
                xaxis=dict(title=_("Time"), type="date", range=[min_date, max_date]),
                yaxis=dict(title=_("Cummulative time"), type="linear"),
                updatemenus=[
                    dict(
                        buttons=[
                            # dict(
                            #     args = ['xbins.size', 60000],
                            #     label = 'Minute',
                            #     method = 'restyle',
                            # ),
                            dict(
                                args=["xbins.size", 3600000],
                                label=_("Hour"),
                                method="restyle",
                            ),
                            dict(
                                args=["xbins.size", 86400000],
                                label=_("Day"),
                                method="restyle",
                            ),
                            dict(
                                args=["xbins.size", 604800000],
                                label=_("Week"),
                                method="restyle",
                            ),
                            dict(
                                args=["xbins.size", "M1"],
                                label=_("Month"),
                                method="restyle",
                            ),
                        ]
                    )
                ],
                autosize=True,
            )

        return fig


class UserActivityUserChart(UserActivityChart):
    title_config_class = UserActivityUserChartTitleConfig

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs["user_id"])
        return super().get_queryset().filter(user=user)
