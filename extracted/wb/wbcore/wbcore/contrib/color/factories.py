import factory

from wbcore.contrib.color.models import ColorGradient


class ColorGradientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ColorGradient

    title = factory.Sequence(lambda n: f"Color Gradient {n}")
    colors = factory.List([factory.Faker("color") for _ in range(10)])
