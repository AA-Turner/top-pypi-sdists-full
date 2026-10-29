from django.apps import AppConfig


class MateriaThemeConfig(AppConfig):
    name = "allianceauth.theme.materia"
    label = "materia"
    version = "5.3.8"
    verbose_name = f"Bootswatch Materia v{version}"

    def ready(self) -> None:
        pass
