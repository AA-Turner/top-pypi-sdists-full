from django.apps import AppConfig


class BootstrapThemeConfig(AppConfig):
    name = "allianceauth.theme.bootstrap"
    label = "bootstrap"
    version = "5.3.8"
    verbose_name = f"Bootstrap v{version}"

    def ready(self) -> None:
        pass
