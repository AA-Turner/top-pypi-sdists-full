import datetime
from typing import Callable, List, Optional

import humanize
import ipyvuetify as v
import mlflow
import solara
import traitlets

from ..settings import settings


class SearchAndNewWidget(v.VuetifyTemplate):
    template_file = (__file__, "experiment_search.vue")

    search = traitlets.Unicode(allow_none=True).tag(sync=True)
    selected = traitlets.Any().tag(sync=True)
    items = traitlets.List().tag(sync=True)
    loading = traitlets.Bool(default_value=False).tag(sync=True)
    opened = traitlets.Bool(default_value=False).tag(sync=True)
    error = traitlets.Unicode(allow_none=True).tag(sync=True)


@solara.component
def SearchAndNew(
    search: Optional[str],
    selected: Optional[str],
    items: List[str],
    loading: bool,
    opened: bool,
    error: Optional[str],
    on_search: Callable[[str], None],
    on_selected: Callable[[str], None],
    on_opened: Callable[[bool], None],
):
    return SearchAndNewWidget.element(
        search=search,
        selected=selected,
        items=items,
        loading=loading,
        opened=opened,
        error=error,
        on_search=on_search,
        on_selected=on_selected,
        on_opened=on_opened,
    )


def date(time_in_millis):
    natural_time = humanize.naturaltime(datetime.datetime.now() - datetime.datetime.fromtimestamp(time_in_millis / 1000))
    return f"last updated {natural_time}"


@solara.component
def ExperimentSearch(value: Optional[str], on_value: Callable[[str], None]):
    search, set_search = solara.use_state("")
    opened, set_opened = solara.use_state(False)

    def get_experiments(_cancel):
        return mlflow.search_experiments(filter_string="tags.mlflow.domino.project_id = '{}'".format(settings.domino_project_id))

    experiment_list_result: solara.Result = solara.use_thread(get_experiments, [])

    def get_all_items():
        items = (
            [
                {
                    "name": item.name,
                    "time": item.last_update_time,
                    "description": date(item.last_update_time),
                }
                for item in experiment_list_result.value
            ]
            if experiment_list_result.value
            else []
        )

        return sorted(items, key=lambda item: item["time"], reverse=True)

    all_items = solara.use_memo(get_all_items, [experiment_list_result.value])

    loading = experiment_list_result.state == solara.ResultState.RUNNING

    def filter_items():
        if search is None or search == "":
            return all_items
        else:
            return [item for item in all_items if search.lower() in item["name"].lower()]

    filtered_items = solara.use_memo(filter_items, [all_items, search])

    def on_selected(selected: str):
        set_opened(False)
        set_search("")
        on_value(selected)

    return SearchAndNew(
        search=search,
        selected=value,
        items=filtered_items,
        loading=loading,
        opened=opened,
        error=experiment_list_result.error.__repr__() if experiment_list_result.state == solara.ResultState.ERROR else None,
        on_search=set_search,
        on_selected=on_selected,
        on_opened=set_opened,
    )
