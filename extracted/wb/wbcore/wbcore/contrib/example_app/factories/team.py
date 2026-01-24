import factory

from wbcore.contrib.directory.factories import CompanyFactory
from wbcore.contrib.example_app.models import Team, TeamResults


class TeamFactory(CompanyFactory):
    coach = factory.SubFactory("wbcore.contrib.example_app.factories.SportPersonFactory")
    home_stadium = factory.SubFactory("wbcore.contrib.example_app.factories.StadiumFactory")
    founded_date = factory.Faker("date_object")
    # city = factory.SubFactory("wbcore.contrib.geography.factories.CityFactory")

    @factory.post_generation
    def opponents(self, create, extracted, **kwargs):
        if extracted:
            for team in extracted:
                self.opponents.add(team)

    class Meta:
        model = Team
        skip_postgeneration_save = True


class TeamResultsFactory(factory.django.DjangoModelFactory):
    team = factory.SubFactory(TeamFactory)
    league = factory.SubFactory("wbcore.contrib.example_app.factories.LeagueFactory")
    points = factory.Faker("pyint")
    match_points_for = factory.Faker("pyint")
    match_points_against = factory.Faker("pyint")
    match_point_difference = factory.Faker("pyint", min_value=-500)
    wins = factory.Faker("pyint")
    draws = factory.Faker("pyint")
    losses = factory.Faker("pyint")
    form = factory.Faker("text", max_nb_chars=5)

    class Meta:
        model = TeamResults
