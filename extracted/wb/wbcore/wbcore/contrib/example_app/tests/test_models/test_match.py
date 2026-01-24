from datetime import datetime
from unittest.mock import patch

import pytest
import pytz
from django.db import IntegrityError
from django.db.models import Q
from faker import Faker
from wbcore.contrib.authentication.factories import SuperUserFactory, UserFactory
from wbcore.contrib.directory.models import Person
from wbcore.contrib.example_app.factories import (
    LeagueFactory,
    MatchFactory,
    TeamFactory,
)
from wbcore.contrib.example_app.models import (
    Match,
    SportPerson,
    TeamResults,
    start_match,
)


@pytest.mark.django_db
class TestMatch:
    def test_has_permissions_superuser(self):
        user = SuperUserFactory.create()
        match = MatchFactory.create()
        assert match.has_permissions(user) is True

    # TODO This tests need some fixing
    # def test_has_permissions_custom_perm(self):
    #     match = MatchFactory.create()
    #     user = UserFactory.create(user_permissions=["wbcore.change_match_status"])
    #     assert match.has_permissions(user) is True

    def test_str(self):
        match = MatchFactory.create(home__name="Home Team", away__name="Away Team")
        assert match.__str__() == "Home Team vs. Away Team"

    @patch("wbcore.contrib.example_app.models.start_match.apply_async")
    @patch("wbcore.contrib.example_app.models.current_app.control.revoke")
    def test_reschedule_existing_task(self, mock_revoke, mock_start):
        user = UserFactory.create()
        # we just need an object with a .id method
        mock_start.return_value = user
        match = MatchFactory.create()
        old_task_id = match.task_id
        match.reschedule_task()
        assert mock_revoke.call_args.args == (old_task_id,)
        assert mock_revoke.call_args.kwargs == {"terminate": True}
        assert mock_start.call_args.kwargs == {
            "eta": match.date_time,
            "args": [match.pk],
        }
        assert match.task_id == user.pk

    @patch("wbcore.contrib.example_app.models.start_match.apply_async")
    @patch("wbcore.contrib.example_app.models.current_app.control.revoke")
    def test_reschedule_new_task(self, mock_revoke, mock_start):
        user = UserFactory.create()
        # we just need an object with a .id method
        mock_start.return_value = user
        match = MatchFactory.create()
        match.task_id = None
        match.reschedule_task()
        assert mock_revoke.call_count == 1
        assert mock_start.call_args.kwargs == {
            "eta": match.date_time,
            "args": [match.pk],
        }
        assert match.task_id == user.pk

    def test_save_calendar_item(self):
        match = MatchFactory.create(league__sport__match_duration=120, date_time=datetime(2023, 5, 20, 19, 15))

        home_sport_persons = SportPerson.objects.filter(
            Q(id__in=match.home.current_players.all()) | Q(coached_team=match.home)
        )
        away_sport_persons = SportPerson.objects.filter(
            Q(id__in=match.away.current_players.all()) | Q(coached_team=match.away)
        )
        referee = SportPerson.objects.filter(id=match.referee.id)
        match_persons = home_sport_persons.union(away_sport_persons, referee)

        persons = Person.objects.filter(id__in=match_persons.values_list("profile", flat=True))
        entities_id_list = list(persons.values_list("pk", flat=True))
        entities_id_list.extend([match.home.id, match.away.id])

        assert match.period.upper == datetime(2023, 5, 20, 21, 15)
        assert set(match.entities.values_list("id", flat=True)) == set(entities_id_list)

    @patch("wbcore.contrib.example_app.models.Match.reschedule_task")
    def test_save_trigger_rescheduling(self, mock_reschedule):
        match = MatchFactory.create()
        match.date_time = Faker().date_time(tzinfo=pytz.utc)
        match.save()
        assert mock_reschedule.call_count == 2

    @patch("wbcore.contrib.example_app.models.Match.reschedule_task")
    def test_save_no_rescheduling(self, mock_reschedule):
        match = MatchFactory.create()
        match.title = "Test"
        match.save()
        assert mock_reschedule.call_count == 1

    def test_save_update_teamresults(self):
        league = LeagueFactory.create(points_per_win=5, points_per_draw=2, points_per_loss=1)
        home_team = TeamFactory.create()
        away_team = TeamFactory.create()

        # Home win
        match1 = MatchFactory.create(
            home=home_team,
            away=away_team,
            status=Match.MatchStatus.FINISHED,
            score_home=3,
            score_away=1,
            league=league,
        )
        assert set(TeamResults.objects.values_list("team__name", flat=True)) == {
            home_team.name,
            away_team.name,
        }
        home_results = TeamResults.objects.get(team=home_team)
        away_results = TeamResults.objects.get(team=away_team)
        assert home_results.wins == 1
        assert home_results.draws == 0
        assert home_results.losses == 0
        assert home_results.form == "----W"
        assert home_results.points == 5
        assert home_results.match_points_for == 3
        assert home_results.match_points_against == 1
        assert away_results.wins == 0
        assert away_results.draws == 0
        assert away_results.losses == 1
        assert away_results.form == "----L"
        assert away_results.points == 1
        assert away_results.match_points_for == 1
        assert away_results.match_points_against == 3
        assert match1.task_id == ""

        # Home Loss
        match2 = MatchFactory.create(
            home=home_team,
            away=away_team,
            status=Match.MatchStatus.FINISHED,
            score_home=21,
            score_away=37,
            league=league,
        )
        home_results = TeamResults.objects.get(team=home_team)
        away_results = TeamResults.objects.get(team=away_team)
        assert home_results.wins == 1
        assert home_results.draws == 0
        assert home_results.losses == 1
        assert home_results.form == "---WL"
        assert home_results.points == 6
        assert home_results.match_points_for == 24
        assert home_results.match_points_against == 38
        assert away_results.wins == 1
        assert away_results.draws == 0
        assert away_results.losses == 1
        assert away_results.form == "---LW"
        assert away_results.points == 6
        assert away_results.match_points_for == 38
        assert away_results.match_points_against == 24
        assert match2.task_id == ""

        # Draw
        match3 = MatchFactory.create(
            home=home_team,
            away=away_team,
            status=Match.MatchStatus.FINISHED,
            score_home=2,
            score_away=2,
            league=league,
        )
        home_results = TeamResults.objects.get(team=home_team)
        away_results = TeamResults.objects.get(team=away_team)
        assert home_results.wins == 1
        assert home_results.draws == 1
        assert home_results.losses == 1
        assert home_results.form == "--WLD"
        assert home_results.points == 8
        assert home_results.match_points_for == 26
        assert home_results.match_points_against == 40
        assert away_results.wins == 1
        assert away_results.draws == 1
        assert away_results.losses == 1
        assert away_results.form == "--LWD"
        assert away_results.points == 8
        assert away_results.match_points_for == 40
        assert away_results.match_points_against == 26
        assert match3.task_id == ""

    @patch("wbcore.contrib.example_app.models.Match.reschedule_task")
    def test_save_no_task_id(self, mock_reschedule):
        MatchFactory.create(status=Match.MatchStatus.FINISHED, score_home=3, score_away=1, task_id="")
        assert not TeamResults.objects.exists()

    def test_unique_constraint(self):
        match = MatchFactory.create()
        with pytest.raises(IntegrityError):
            MatchFactory.create(home=match.home, away=match.away, date_time=match.date_time)

    def test_check_constraint(self):
        team = TeamFactory.create()
        with pytest.raises(IntegrityError):
            MatchFactory.create(home=team, away=team)

    def test_start_match_scheduled(self):
        match = MatchFactory(status=Match.MatchStatus.SCHEDULED)
        start_match(match.pk)
        assert Match.objects.get(id=match.pk).status == Match.MatchStatus.ONGOING

    def test_start_match_finished(self):
        match = MatchFactory(status=Match.MatchStatus.FINISHED)
        start_match(match.pk)
        assert Match.objects.get(id=match.pk).status != Match.MatchStatus.ONGOING
