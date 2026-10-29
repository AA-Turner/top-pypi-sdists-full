from django.apps import AppConfig


class DarklyThemeConfig(AppConfig):
    name = "allianceauth.theme.darkly"
    label = "darkly"
    version = "5.3.8"
    verbose_name = f"Bootswatch Darkly v{version}"

    def ready(self) -> None:
        pass
