"""The Reflex Enterprise component."""

from reflex.components.component import Component, NoSSRComponent

from reflex_enterprise.app import AppEnterprise


class ComponentEnterprise(Component):
    """The Reflex Enterprise component."""

    @classmethod
    def create(cls, *children, **props) -> Component:
        """Create the Reflex Enterprise component."""
        return super().create(*children, **props)

    def render(self, *children, **props) -> dict:
        """Render the Reflex Enterprise component."""
        from reflex.utils.prerequisites import get_app

        if not isinstance(get_app().app, AppEnterprise):
            raise TypeError(
                "Reflex Enterprise components can only be used in an Enterprise app. Use rxe.App() instead of rx.App()."
            )

        return super().render(*children, **props)


class NoSSRComponentEnterprise(NoSSRComponent):
    """The Reflex Enterprise component without SSR."""

    @classmethod
    def create(cls, *children, **props) -> Component:
        """Create the Reflex Enterprise component."""
        return super().create(*children, **props)

    def render(self, *children, **props) -> dict:
        """Render the Reflex Enterprise component."""
        from reflex.utils.prerequisites import get_app

        if not isinstance(get_app().app, AppEnterprise):
            raise TypeError(
                "Reflex Enterprise components can only be used in an Enterprise app. Use rxe.App() instead of rx.App()."
            )

        return super().render(*children, **props)
