from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone
from psycopg.types.range import DateRange
from rest_framework.test import APIRequestFactory

from wbcore.contrib.example_app.factories import (
    EventFactory,
    MatchFactory,
    PlayerFactory,
    SportPersonFactory,
    TeamFactory,
)
from wbcore.contrib.example_app.viewsets import (
    PlayerStatisticsChartModelViewSet,
    SportPersonRepresentationViewSet,
)
from wbcore.filters.defaults import current_year_date_range
from wbcore.test.utils import get_or_create_superuser


@pytest.mark.django_db
class TestEvent:
    @patch("wbcore.contrib.example_app.models.Match.reschedule_task")
    def test_filter_by_period(self, mock_reschedule):
        event = EventFactory.create(match__date_time=timezone.now())
        before_event = DateRange((timezone.now() - timedelta(7)).date(), (timezone.now() - timedelta(1)).date())
        after_event = DateRange((timezone.now() + timedelta(1)).date(), (timezone.now() + timedelta(7)).date())
        mvs = PlayerStatisticsChartModelViewSet(kwargs={"player_id": event.person})
        request = APIRequestFactory().get("")
        request.user = get_or_create_superuser()
        qs = mvs.get_queryset()
        assert len(mvs.filterset_class(request=request).filter_by_period(qs, "", current_year_date_range())) == 1
        assert (
            mvs.filterset_class(request=request).filter_by_period(qs, "", current_year_date_range()).first() == event
        )
        assert not mvs.filterset_class(request=request).filter_by_period(qs, "", before_event).exists()
        assert not mvs.filterset_class(request=request).filter_by_period(qs, "", after_event).exists()


@pytest.mark.django_db
class TestPerson:
    @patch("wbcore.contrib.example_app.models.Match.reschedule_task")
    def test_filter_by_match(self, mock_reschedule):
        ref1 = SportPersonFactory.create()
        match1 = MatchFactory.create(referee=ref1, home__coach=None, away__coach=None)
        ref2 = SportPersonFactory.create()
        home_coach = SportPersonFactory.create()
        away_coach = SportPersonFactory.create()
        home_team = TeamFactory.create(coach=home_coach)
        away_team = TeamFactory.create(coach=away_coach)
        home_player = PlayerFactory.create(current_team=home_team)
        away_player = PlayerFactory.create(current_team=away_team)
        match2 = MatchFactory.create(
            home=home_team,
            away=away_team,
            referee=ref2,
        )
        SportPersonFactory.create()
        PlayerFactory.create()
        mvs = SportPersonRepresentationViewSet()
        request = APIRequestFactory().get("")
        request.user = get_or_create_superuser()
        qs = mvs.get_queryset()
        assert len(mvs.filterset_class(request=request).filter_by_match(qs, "", match1)) == 1
        assert mvs.filterset_class(request=request).filter_by_match(qs, "", match1).first() == ref1
        assert set(
            mvs.filterset_class(request=request).filter_by_match(qs, "", match2).values_list("id", flat=True)
        ) == {ref2.pk, home_coach.pk, away_coach.pk, home_player.pk, away_player.pk}
