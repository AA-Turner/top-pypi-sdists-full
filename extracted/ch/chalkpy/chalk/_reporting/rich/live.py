from typing import Any

from rich import reconfigure
from rich.control import Control
from rich.live import Live

from chalk._reporting.rich.theme import CHALK_THEME
from chalk.utils.notebook import is_notebook


class ChalkLive(Live):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        reconfigure(
            force_jupyter=False,
            force_terminal=True,
            color_system="truecolor",
            theme=CHALK_THEME,
            # `self.console.width` is a width that is
            # wider than if `width` is not specified
            # at all. We want the wider width so that
            # long resolver names are not truncated.
            width=int(self.console.width),
        )

    def refresh(self) -> None:
        """
        Chalk's custom implementation of refresh, to achieve
        a dark background for certain IDEs.
        """
        with self._lock:
            self._live_render.set_renderable(self.renderable)
            if self.console.is_jupyter:  # pragma: no cover
                try:

                    from IPython.display import clear_output, display
                    from ipywidgets import Output
                except ImportError:
                    import warnings

                    warnings.warn('install "ipywidgets" for Jupyter support')
                else:
                    if self.ipy_widget is None:
                        self.ipy_widget = Output()
                        display(self.ipy_widget)
                    assert self.ipy_widget is not None
                    with self.ipy_widget:
                        self.ipy_widget.clear_output(wait=True)
                        self.console.print(self._live_render.renderable)
            elif self.console.is_terminal and not self.console.is_dumb_terminal:
                if is_notebook():
                    from IPython.display import clear_output

                    clear_output(wait=True)
                with self.console:
                    self.console.print(Control())
            elif (
                not self._started and not self.transient
            ):  # if it is finished allow files or dumb-terminals to see final result
                with self.console:
                    self.console.print(Control())
