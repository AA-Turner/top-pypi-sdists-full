import marimo
import mowidgets

from dlthub.data_quality._widgets.metrics_viewer import app as metrics_viewer


def render(app: marimo.App, *args, **kwargs):
    if not isinstance(app, marimo.App):
        raise ValueError("app must be an instance of marimo.App")

    if app is metrics_viewer:
        return metrics_viewer_widget(app, *args, **kwargs)
    else:
        raise ValueError("app must be either metrics_viewer")


def metrics_viewer_widget(app, pipeline_name: str, *args, **kwargs):
    return mowidgets.widgetize(app, data_access=True, inputs={"pipeline_name": pipeline_name})


__all__ = (
    "render",
    "metrics_viewer_widget",
)
