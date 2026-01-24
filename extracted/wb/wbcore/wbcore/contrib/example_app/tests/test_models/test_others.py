import pytest
from django.db import IntegrityError
from wbcore.contrib.example_app.factories import (
    LeagueFactory,
    MatchFactory,
    PlayerFactory,
    RoleFactory,
    SportFactory,
    SportPersonFactory,
    StadiumFactory,
    TeamFactory,
    TeamResultsFactory,
)
from wbcore.contrib.example_app.models import League, Match, Player, SportPerson


@pytest.mark.django_db
class TestPerson:
    def test_str_full(self):
        person = SportPersonFactory.create(first_name="Test", last_name="Name")
        assert person.str_full() == "Test Name"

    def test_str_full_coach(self):
        person = SportPersonFactory.create(first_name="Test", last_name="Name")
        TeamFactory.create(coach=person, name="Test Team")
        assert person.str_full() == "Test Name (Coach of Test Team)"

    def test_str_full_commissioner(self):
        commissioner = SportPersonFactory.create(first_name="Test", last_name="Name")
        LeagueFactory.create(commissioner=commissioner, name="Test League")
        assert commissioner.str_full() == "Test Name (Commissioner of Test League)"

    def test_get_player_fail(self):
        person = SportPersonFactory.create()
        assert person.get_player() is None

    def test_get_player_sucess(self):
        player = PlayerFactory.create()
        person = SportPerson.objects.get(id=player.pk)
        assert person.get_player() == player


@pytest.mark.django_db
class TestPlayer:
    def test_str_full(self):
        player = PlayerFactory.create(first_name="Test", last_name="Name", current_team=None)
        assert player.str_full() == "Test Name"

    def test_str_full_team(self):
        player = PlayerFactory.create(
            current_team__name="Test Team", position=None, first_name="Test", last_name="Name"
        )
        assert player.str_full() == "Test Name (Test Team)"

    def test_str_full_team_position(self):
        player = PlayerFactory.create(
            current_team__name="Test Team", position="Test Position", first_name="Test", last_name="Name"
        )
        assert player.str_full() == "Test Name (Test Position at Test Team)"


@pytest.mark.django_db
class TestRole:
    def test_str(self):
        role = RoleFactory.create(title="Test Role")
        assert role.__str__() == "Test Role"


@pytest.mark.django_db
class TestSport:
    def test_str(self):
        sport = SportFactory.create(name="Test Sport")
        assert sport.__str__() == "Test Sport"

    def test_post_save(self):
        sport = SportFactory.create()
        league1 = LeagueFactory.create(sport=sport)
        old_name = sport.name
        new_name = "New Sport Name"
        sport.name = new_name
        sport.save()
        new_computed_str = League.objects.get(id=league1.pk).computed_str
        assert old_name not in new_computed_str
        assert new_name in new_computed_str


@pytest.mark.django_db
class TestLeague:
    def test_str(self):
        league = LeagueFactory(name="Test League", sport__name="Test Sport")
        assert league.__str__() == "Test League (Test Sport)"

    def test_unique_constraint(self):
        league = LeagueFactory.create()
        with pytest.raises(IntegrityError):
            LeagueFactory(name=league.name, sport=league.sport)

    def test_post_save(self):
        commissioner = SportPersonFactory.create()
        league = LeagueFactory(commissioner=commissioner)
        old_name = league.name
        new_name = "New League Name"
        league.name = new_name
        league.save()
        new_computed_str = SportPerson.objects.get(id=commissioner.pk).computed_str
        assert old_name not in new_computed_str
        assert new_name in new_computed_str


@pytest.mark.django_db
class TestTeamResults:
    def test_str(self):
        team_results = TeamResultsFactory(team__name="Test Team", league__name="Test League")
        assert team_results.__str__() == "Test Team in Test League"

    @pytest.mark.parametrize("points_for, points_against, difference", [(33, 91, -58), (252, 171, 81), (86, 86, 0)])
    def test_save(self, points_for, points_against, difference):
        team_results = TeamResultsFactory(match_points_for=points_for, match_points_against=points_against)
        assert team_results.match_point_difference == difference

    def test_unique_constraint(self):
        team_results = TeamResultsFactory.create()
        with pytest.raises(IntegrityError):
            TeamResultsFactory(team=team_results.team, league=team_results.league)


@pytest.mark.django_db
class TestStadium:
    def test_str(self):
        stadium = StadiumFactory(name="Test Stadium")
        assert stadium.__str__() == "Test Stadium"


@pytest.mark.django_db
class TestTeam:
    def test_str(self):
        team = TeamFactory(name="Test Team")
        assert team.__str__() == "Test Team"

    def test_post_save(self):
        team = TeamFactory.create()
        old_name = team.name
        player1 = PlayerFactory(current_team=team)
        player2 = PlayerFactory(current_team=team)
        player3 = PlayerFactory(current_team=team)
        match1 = MatchFactory(home=team)
        match2 = MatchFactory(away=team)
        new_name = "New Team Name"
        team.name = new_name
        team.save()
        for match in [match1, match2]:
            match_new_computed_str = Match.objects.get(id=match.pk).computed_str
            assert old_name not in match_new_computed_str
            assert new_name in match_new_computed_str
        for player in [player1, player2, player3]:
            player_new_computed_str = Player.objects.get(id=player.pk).computed_str
            assert old_name not in player_new_computed_str
            assert new_name in player_new_computed_str
        coach_new_computed_str = SportPerson.objects.get(id=team.coach.pk).computed_str
        assert old_name not in coach_new_computed_str
        assert new_name in coach_new_computed_str
