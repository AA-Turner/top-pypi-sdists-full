from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class MateriaThemeHook(ThemeHook):
    """
    Bootswatch Materia Theme
    https://bootswatch.com/materia/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self,
            "Materia",
            "Material is the metaphor",
            html_tags={"data-theme": "materia"},
            css=[],
            js=[],
            css_template="theme/materia/css.html",
            js_template="bundles/bootstrap-js-bs5.html",
            header_padding="5.25em"
        )


@hooks.register('theme_hook')
def register_materia_hook() -> MateriaThemeHook:
    return MateriaThemeHook()
