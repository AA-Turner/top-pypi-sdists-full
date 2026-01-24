import factory

from wbcore.contrib.example_app.models import Player, SportPerson


class SportPersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SportPerson
        skip_postgeneration_save = True

    profile = factory.SubFactory("wbcore.contrib.directory.factories.PersonFactory")
    profile_image = factory.django.ImageField(filename="image_profile.jpeg")
    first_name = factory.SelfAttribute("profile.first_name")
    last_name = factory.SelfAttribute("profile.last_name")

    @factory.post_generation
    def roles(self, create, extracted, **kwargs):
        if extracted:
            for role in extracted:
                self.roles.add(role)


class PlayerFactory(SportPersonFactory):
    position = factory.Faker("text", max_nb_chars=15)
    current_team = factory.SubFactory("wbcore.contrib.example_app.factories.TeamFactory")

    @factory.post_generation
    def former_teams(self, create, extracted, **kwargs):
        if extracted:
            for team in extracted:
                self.former_teams.add(team)

    class Meta:
        model = Player
