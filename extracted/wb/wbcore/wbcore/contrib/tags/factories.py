import factory

from .models import Tag, TagGroup


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        skip_postgeneration_save = True

    title = factory.Faker("name")
    description = factory.Faker("paragraph")

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)


class TagGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TagGroup

    title = factory.Faker("name")
