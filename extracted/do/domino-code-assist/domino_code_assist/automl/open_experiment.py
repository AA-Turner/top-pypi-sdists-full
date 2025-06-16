import threading
import time

import ipyvuetify as v
import solara
import traitlets
from ipywidgets import widget_serialization

from domino_code_assist.domino_api import get_domino_api
from domino_code_assist.settings import settings


class AboveOutputWidget(v.VuetifyTemplate):
    template_file = (__file__, "above_output.vue")
    children = traitlets.List().tag(sync=True, **widget_serialization)


@solara.component
def OpenExperiment(name: str):
    def get_experiments(cancel: threading.Event):
        for i in range(10):
            if cancel.is_set():
                raise Exception("Cancelled")
            found = [e for e in get_domino_api().get_experiments() if e["name"] == name]
            if cancel.is_set():
                raise Exception("Cancelled")
            if found:
                return found[0]
            time.sleep(1)
        raise Exception(f"Experiment {name} not found")

    experiments_result: solara.Result = solara.use_thread(get_experiments, [name])

    with AboveOutputWidget.element():
        if experiments_result.state == solara.ResultState.ERROR:
            solara.Error(f"Error getting link to experiment. Reason: {experiments_result.error.__repr__()}").key("error")
        else:
            finished = experiments_result.state == solara.ResultState.FINISHED

            if not experiments_result.value:
                solara.Error("Could not find experiment.")
            else:
                with solara.Div().key("found"):
                    href = (
                        f"/experiments/{settings.domino_project_owner}/{settings.domino_project_name}/{experiments_result.value['experiment_id']}"
                        if finished
                        else ""
                    )
                    solara.Button(
                        f"open experiment: {name}",
                        disabled=not finished,
                        color="primary",
                        icon_name="mdi-open-in-new",
                        href=href,
                        target="_blank",
                        style_="text-transform: unset",
                    )
