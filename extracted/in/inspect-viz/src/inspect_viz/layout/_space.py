from inspect_viz._core import Component


def hspace(hspace: float | str = 10) -> Component:
    """Horizontal space to place between widgets.

    Args:
        hspace: Amount of space. Number values indicate screen pixels. String values may use CSS units (em, pt, px, etc).
    """
    return Component(config=dict(hspace=hspace))


def vspace(vspace: float | str = 10) -> Component:
    """Veritcal space to place between widgets.

    Args:
        vspace: Amount of space. Number values indicate screen pixels. String values may use CSS units (em, pt, px, etc).
    """
    return Component(config=dict(vspace=vspace))
