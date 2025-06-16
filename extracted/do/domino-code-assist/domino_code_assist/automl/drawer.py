import os
from dataclasses import replace
from typing import Any, Callable, Dict, List, Optional, cast

import mlflow
import pandas as pd
import reacton.ipyvuetify as v
import solara
from mlflow.utils.name_utils import _generate_random_name
from reacton import use_effect
from reacton.ipyvue import use_event
from solara.components.input import _use_input_numeric
from solara.lab import Ref

from domino_code_assist import util
from domino_code_assist.assistant import drawer, mixpanel
from domino_code_assist.automl.experiment_search import ExperimentSearch
from domino_code_assist.automl.store import (
    AVAILABLE_TASKS,
    MLTask,
    TaskConfig,
    get_task_arg_for_name,
    ml_task,
    task_config_store,
)
from domino_code_assist.df_select import DfSelect
from domino_code_assist.serialize import dumps
from domino_code_assist.transform.column_description import ColumnDescription

from . import flaml_api, hyper_parameters
from .select_description import SelectDescription


def bind_value(field):
    ref = Ref(field)
    return {
        "value": ref.value,
        "on_value": ref.set,
    }


def generate_code(task: MLTask):
    if task.task_type in ["Classification", "Regression", "Forecasting", "Forecasting (classification)"] and task.task_config is not None:
        with open(os.path.join(os.path.dirname(__file__), "code.py")) as f:
            code = f.read()
            template_delimiter = "# ___TEMPLATE_START___ #\n"
            code = code[code.index(template_delimiter) + len(template_delimiter) :]

            config = task.task_config
            code = code.replace("___experiment_name___", config.experiment_name or "noname")

            if task.task_type.startswith("Forecasting"):
                if config.exclude_features:
                    code = code.replace("___exclude_features___", str(config.exclude_features).replace("'", '"'))
                else:
                    code = code.replace("exclude_features = ___exclude_features___\n", "")
                filter = (
                    f'[c for c in {config.df_var_name}.columns if c not in ["{config.time_column}", *exclude_features]]'
                    if config.exclude_features
                    else f'[c for c in {config.df_var_name}.columns if c != "{config.time_column}"]'
                )
                code = code.replace(".drop(exclude_features, axis=1)", f'[["{config.time_column}"] + {filter}]')
                if util.nb_locals[config.df_var_name][config.time_column].dtypes != "datetime64[ns]":
                    code = code.replace(".copy()", f'.dropna()\ndf_automl["{config.time_column}"] = pd.to_datetime(df_automl["{config.time_column}"])\n')
                else:
                    code = code.replace(".copy()", ".dropna()")
            else:
                if not config.exclude_features:
                    code = code.replace("exclude_features = ___exclude_features___\n", "").replace("drop(exclude_features, axis=1).", "")
                else:
                    code = code.replace("___exclude_features___", str(config.exclude_features).replace("'", '"'))

            if task.task_type and task.task_type.startswith("Forecasting"):
                code = code.replace("___period___", str(config.period) if config.period is not None else "None")
            else:
                code = code.replace(", period=___period___", "")
            assert config.df_var_name is not None
            code = code.replace("___df_var_name___", config.df_var_name)

            task_arg = get_task_arg_for_name(task.task_type)

            code = code.replace("___ml_task___", task_arg)
            factor = 0
            if config.time_unit == "Minutes":
                factor = 60
            elif config.time_unit == "Hours":
                factor = 3600

            code = code.replace("___time_budget___", str(config.max_time * factor) if config.max_time is not None else "None")
            code = code.replace("___max_iterations___", str(config.max_iterations) if config.max_iterations is not None else "None")
            code = code.replace("___optimization_metric___", config.optimization_metric)
            assert config.target is not None
            code = code.replace("___label___", config.target)

            if config.auto:
                code = code.replace(", tune", "")
                code = code.replace("estimator_list = ___estimator_list___\ncustom_hp = ___custom_hp___\n\n", "")
                code = code.replace(", custom_hp=custom_hp, estimator_list=estimator_list", "")
            else:
                code = code.replace("___estimator_list___", str(config.custom_learners_enabled).replace("'", '"'))
                code = code.replace(
                    "___custom_hp___", hyper_parameters.get_hyper_parameters_string(config.custom_learners or {}, config.custom_learners_enabled or [])
                )

            if config.resampling_strategy != "Auto":
                if config.resampling_strategy == "Holdout":
                    method = "holdout"
                    arg = f"split_ratio={config.split_ratio}"
                else:
                    method = "cv"
                    arg = f"n_splits={config.folds}"
                code = code.replace(", eval_method=None", f', eval_method="{method}", {arg}')
            else:
                code = code.replace(", eval_method=None", "")
    else:
        code = f"# TODO: insert {task.task_type} code. {task.task_config}"

    return code


@solara.component
def MlTaskTile(task_info, on_task_info):
    with solara.Div(
        style_=f"display: flex; align-items: center; padding: 16px 32px {'; cursor: unset' if task_info.soon else ''}", class_="domino-ml-model-type-button"
    ).meta(ref="TaskTile") as tile:
        with solara.Div(style_="margin-right: 16px"):
            solara.Image(os.path.join(os.path.dirname(__file__), task_info.image), width="120px")
        with solara.Div():
            solara.Div(children=task_info.name, style_="font-size: 20px")
            solara.Div(children=task_info.description, style_="font-size: 14px")
            if task_info.soon:
                v.Chip(children="Coming soon", color="green", small=True, style_="margin-top: 8px", dark=True)

    def on_click(*args):
        if not task_info.soon:
            on_task_info(task_info)
        mixpanel.api.track_with_defaults("interaction", {"section": "automl", "type": "select_task", "task": task_info.name})

    v.use_event(tile, "click", on_click)


@solara.component
def FixHorizontalScrollingInDialog(children):
    # See: https://github.com/vuetifyjs/vuetify/issues/3765
    assert len(children) == 1
    use_event(children[0], "wheel.stop", lambda *args: None)
    return children[0]


@solara.component
def MlTaskConfigUI(dfs: List[str], task_type, edit: bool, on_load_own_data: Callable[[], None], emphasize_errors: bool):
    ml_task.use()
    task_config_store.use()

    expanded, set_expanded = solara.use_state([0])
    column_menu_open, set_column_menu_open = solara.use_state(cast(Optional[str], None))

    extended_dfs: List[Any] = dfs
    if not edit:
        extended_dfs = extended_dfs + [{"divider": True}, "Load more data"]

    def set_df_var_name(value):
        if value == "Load more data":
            on_load_own_data()
            return
        Ref(task_config_store.fields.df_var_name).set(value)

    df: Optional[pd.DataFrame] = util.nb_locals[task_config_store.value.df_var_name] if task_config_store.value.df_var_name else None
    available_columns: Optional[List[str]] = df.columns.tolist() if df is not None else None
    features = task_config_store.get_features(available_columns)

    def find_date_time_columns():
        if available_columns is None or not task_type.startswith("Forecasting"):
            return None

        def is_date_time(col):
            if str(col.dtypes) == "datetime64[ns]":
                return True

            if str(col.dtypes) == "object":
                try:
                    pd.to_datetime(col.head())
                    return True
                except Exception:
                    pass
            return False

        return [col for col in available_columns if is_date_time(df[col])]  # type: ignore

    date_time_columns = solara.use_memo(find_date_time_columns, [available_columns, df])

    def pre_select_time_column():
        if not date_time_columns or task_config_store.value.time_column in date_time_columns:
            return None
        Ref(task_config_store.fields.time_column).set(date_time_columns[0])

    solara.use_memo(pre_select_time_column, [date_time_columns])

    int_period, set_int_period = solara.use_state(cast(Optional[int], task_config_store.value.period))
    period, set_period, period_error = _use_input_numeric(int, optional=True, value=int_period, on_value=set_int_period)

    def set_value():
        Ref(task_config_store.fields.period).set(period if not period_error else None)

    use_effect(set_value, [period, period_error])

    def available_items(used_items: Optional[List[Optional[str]]], used_description: str):
        if available_columns is None or df is None:
            return None
        return [
            {
                "text": col + (f" ({used_description})" if col in (used_items or []) else ""),
                "value": col,
                "disabled": col in (used_items or []),
            }
            for col in available_columns
        ]

    task = get_task_arg_for_name(task_type)

    with v.Row(class_="dca-automl-config"):
        with v.Col(style_="max-width: 800px"):
            with v.ExpansionPanels(multiple=True, v_model=expanded, on_v_model=set_expanded, accordeon=True, style_="width: 800px"):
                with v.ExpansionPanel():
                    with v.ExpansionPanelHeader():
                        with solara.Div(style_="display: flex; flex-direction: row; max-width: 100%; overflow: hidden;"):
                            with solara.Div(style_="min-width: 140px"):
                                v.Html(tag="strong", children=["Data & Features "])
                            if 0 in expanded or (
                                task_config_store.value.df_var_name is None
                                and task_config_store.value.target is None
                                and task_config_store.value.exclude_features is None
                            ):
                                solara.Text("Select the data you’d like to use and value to predict").meta(ref="DataFeaturesDescription")
                            else:
                                with solara.ColumnsResponsive([6, 6, 12], gutters=False, classes=["pa-0"]):
                                    with solara.Row(gap="8px"):
                                        solara.Text("Data frame:", style="font-weight: bold; color: var(--jp-border-color1);")
                                        solara.Text(task_config_store.value.df_var_name or "")
                                    with solara.Row(gap="8px"):
                                        solara.Text("Predict value:", style="font-weight: bold; color: var(--jp-border-color1);")
                                        solara.Text(task_config_store.value.target or "")
                                    with solara.Row(gap="8px", classes=["pt-2"], style="align-items: baseline;"):
                                        solara.Text("Features:", style="font-weight: bold; color: var(--jp-border-color1);")
                                        [v.Chip(small=True, children=[col]) for col in features or []]
                                    if task_type and task_type.startswith("Forecasting"):
                                        with solara.Row(gap="8px", classes=["pt-2"], style="align-items: baseline").key("bla"):
                                            solara.Text("Period:", style="font-weight: bold; color: var(--jp-border-color1);")
                                            solara.Text(str(task_config_store.value.period) if task_config_store.value.period is not None else "")
                    with v.ExpansionPanelContent():
                        with v.Row():
                            with v.Col(class_="py-1").key("df"):
                                DfSelect(
                                    value=task_config_store.value.df_var_name,
                                    label="Data frame",
                                    on_value=set_df_var_name,
                                    items=extended_dfs or [],
                                    hide_details=bool(task_config_store.value.df_var_name),
                                    error=emphasize_errors and not bool(task_config_store.value.df_var_name),
                                    messages=["required"] if not task_config_store.value.df_var_name else None,
                                )
                            if task_type and task_type.startswith("Forecasting"):
                                with v.Col(class_="py-1").key("time"):
                                    v.Select(
                                        label="Time column",
                                        items=date_time_columns,
                                        hide_details=bool(task_config_store.value.target),
                                        v_model=task_config_store.value.time_column,
                                        on_v_model=Ref(task_config_store.fields.time_column).set,
                                        error=emphasize_errors and not bool(task_config_store.value.time_column),
                                        messages=["required"] if not task_config_store.value.time_column else None,
                                        no_data_text="No date/time columns found",
                                    ).meta(ref="TimeColumnSelect")
                            with v.Col(class_="py-1").key("predict"):
                                v.Select(
                                    label="Predict value",
                                    items=available_columns,
                                    clearable=True,
                                    hide_details=bool(task_config_store.value.target),
                                    v_model=task_config_store.value.target,
                                    on_v_model=task_config_store.set_target,
                                    error=emphasize_errors and not bool(task_config_store.value.target),
                                    messages=["required"] if not task_config_store.value.target else None,
                                )
                        with v.Row():

                            def on_features(v: List[str]):
                                Ref(task_config_store.fields.exclude_features).set(
                                    [c for c in (available_columns or []) if c not in v and c != task_config_store.value.target]
                                )

                            with v.Col(class_="py-1"):
                                v.Select(
                                    label="Features",
                                    items=available_items([task_config_store.value.target], "Predict value"),
                                    multiple=True,
                                    chips=True,
                                    deletable_chips=True,
                                    hide_details=bool(features),
                                    error=emphasize_errors and not bool(features),
                                    messages=["required"] if not features else None,
                                    v_model=features,
                                    on_v_model=on_features,
                                )
                        if task_type and task_type.startswith("Forecasting"):
                            with v.Row():
                                with v.Col(class_="py-1", sm=2):
                                    period_error_message = None
                                    if period is None:
                                        period_error_message = "required"
                                    elif period_error:
                                        period_error_message = "invalid"

                                    v.TextField(
                                        label="Period",
                                        clearable=True,
                                        v_model=period,
                                        on_v_model=set_period,
                                        error=emphasize_errors and bool(period_error_message),
                                        messages=period_error_message,
                                        hide_details=bool(not period_error_message),
                                    )
                                with v.Col(class_="py-1", sm=2):
                                    with solara.ToggleButtonsSingle(
                                        value="regression" if ml_task.value.task_type == "Forecasting" else "classification",  # type: ignore
                                        on_value=lambda val: Ref(ml_task.fields.task_type).set(
                                            "Forecasting" if val == "regression" else "Forecasting (classification)"
                                        ),
                                    ):
                                        solara.Button("Regression", value="regression", small=True, classes=["mt-2"])
                                        solara.Button("Classification", value="classification", small=True, classes=["mt-2"])
                with v.ExpansionPanel():
                    with v.ExpansionPanelHeader():
                        with solara.Div(style_="display: flex; flex-direction: row;"):
                            with solara.Div(style_="min-width: 140px"):
                                v.Html(tag="strong", children=["Training"])
                            if 1 in expanded or (
                                task_config_store.value.experiment_name is None
                                and task_config_store.value.optimization_metric == "auto"
                                and task_config_store.value.max_iterations is None
                                and task_config_store.value.max_time is None
                            ):
                                solara.Text("Choose the metric to optimize and your time budget")
                            else:
                                with solara.ColumnsResponsive([12, 4, 4, 4], gutters=False, classes=["pa-0"]):
                                    with solara.Row(gap="8px"):
                                        solara.Text("Experiment name:", style="font-weight: bold; color: var(--jp-border-color1);")
                                        solara.Text(task_config_store.value.experiment_name or "")
                                    with solara.Row(gap="8px", classes=["pt-2"]):
                                        solara.Text("Optimize metric:", style="font-weight: bold; color: var(--jp-border-color1);")
                                        solara.Text(task_config_store.value.optimization_metric or "")
                                    with solara.Row(gap="8px", classes=["pt-2"]):
                                        solara.Text("Max iterations:", style="font-weight: bold; color: var(--jp-border-color1);")
                                        solara.Text(str(task_config_store.value.max_iterations) if task_config_store.value.max_iterations else "")
                                    with solara.Row(gap="8px", classes=["pt-2"]):
                                        solara.Text("Time budget:", style="font-weight: bold; color: var(--jp-border-color1);")
                                        solara.Text(
                                            (str(task_config_store.value.max_time) if task_config_store.value.max_time else "")
                                            + " "
                                            + task_config_store.value.time_unit
                                        ) if task_config_store.value.max_time else ""

                    with v.ExpansionPanelContent():
                        with v.Row():
                            with v.Col(class_="py-1"):
                                ExperimentSearch(**bind_value(task_config_store.fields.experiment_name))
                        with v.Row():
                            with v.Col(class_="py-1"):
                                metrics = (
                                    flaml_api.classification_forecasting_metric_options
                                    if task_type and task_type.startswith("Classification") or ml_task.value.task_type == "Forecasting (classification)"
                                    else flaml_api.regression_forecasting_metric_options
                                )
                                optimization_metric_options = [
                                    {
                                        "value": key,
                                        "text": key,
                                        "description": description,
                                    }
                                    for key, description in metrics
                                ]
                                SelectDescription(
                                    label="Optimize metric", items=optimization_metric_options, **bind_value(task_config_store.fields.optimization_metric)
                                )
                            with v.Col(class_="py-1"):
                                solara.InputInt(
                                    label="Max iterations",
                                    continuous_update=True,
                                    clearable=True,
                                    optional=True,
                                    **bind_value(task_config_store.fields.max_iterations),
                                )
                            with v.Col(class_="py-1"):
                                solara.InputInt(
                                    label="Time budget",
                                    continuous_update=True,
                                    clearable=True,
                                    optional=True,
                                    **bind_value(task_config_store.fields.max_time),
                                )
                            with v.Col(class_="py-1"):
                                v.Select(
                                    label="Unit",
                                    items=["Seconds", "Minutes", "Hours"],
                                    hide_details=True,
                                ).connect(Ref(task_config_store.fields.time_unit))
                hyper_parameters.Hyperparameters(task)
                with v.ExpansionPanel():
                    with v.ExpansionPanelHeader():
                        with solara.Div(style_="display: flex; flex-direction: row;"):
                            with solara.Div(style_="min-width: 140px"):
                                v.Html(tag="strong", children=["Resampling"])
                            if 3 in expanded or (task_config_store.value.resampling_strategy == "Auto"):
                                solara.Text("Customize the resampling method")
                            else:
                                with solara.ColumnsResponsive([6, 6], gutters=False, classes=["pa-0"]):
                                    with solara.Row(gap="8px"):
                                        solara.Text("Resampling strategy:", style="font-weight: bold; color: var(--jp-border-color1);")
                                        solara.Text(task_config_store.value.resampling_strategy)
                                    with solara.Row(gap="8px", classes=["pt-2"]):
                                        if task_config_store.value.resampling_strategy == "Holdout":
                                            solara.Text(
                                                "Split ratio:",
                                                style="font-weight: bold; color: var(--jp-border-color1);",
                                            )
                                            solara.Text(task_config_store.value.split_ratio)
                                        else:
                                            solara.Text(
                                                "Folds:",
                                                style="font-weight: bold; color: var(--jp-border-color1);",
                                            )
                                            solara.Text(task_config_store.value.folds)
                    with v.ExpansionPanelContent():
                        with v.Row():
                            with v.Col(class_="py-1"):
                                v.Select(label="Validation method", items=["Auto", "Holdout", "Cross validation"]).connect(
                                    Ref(task_config_store.fields.resampling_strategy)
                                )
                            with v.Col(class_="py-1"):
                                if task_config_store.value.resampling_strategy == "Holdout":
                                    messages = None
                                    if not task_config_store.value.split_ratio:
                                        messages = ["required"]
                                    elif util.to_float(task_config_store.value.split_ratio) is None:
                                        messages = ["invalid"]
                                    v.TextField(label="Split ratio", error_messages=messages).connect(Ref(task_config_store.fields.split_ratio)).key(
                                        "split_ratio"
                                    )
                                elif task_config_store.value.resampling_strategy == "Cross validation":
                                    messages = None
                                    if not task_config_store.value.folds:
                                        messages = ["required"]
                                    elif util.to_int(task_config_store.value.folds) is None:
                                        messages = ["invalid"]
                                    v.TextField(label="Folds", error=emphasize_errors and bool(messages), messages=messages).key("folds").connect(
                                        Ref(task_config_store.fields.folds)
                                    )
        with FixHorizontalScrollingInDialog():
            with v.Col(style_="overflow: hidden;"):
                if df is not None:
                    solara.DataFrame(
                        df,
                        items_per_page=10,
                        scrollable=True,
                        on_column_header_hover=set_column_menu_open,
                        column_header_info=ColumnDescription(df, column_menu_open),
                    )


# For remembering params when switching between forecasting tasks
hyper_param_scratchpad = solara.reactive(cast(Dict[str, Any], {}))


@solara.component
def AutoMlDrawer(
    edit_data: Optional[MLTask],
    set_code: Callable[[Dict], None],
    dfs: List[str],
    is_open: bool,
    edit: bool,
    on_close: Callable[[], None],
    on_load_own_data: Callable[[], None],
    overwrite_warning=None,
):
    ml_task.use()
    task_config_store.use()

    emphasize_errors, set_emphasize_errors = solara.use_state(False)

    def is_valid():
        return (
            ml_task.value.task_type in ["Regression", "Classification"]
            or (
                ml_task.value.task_type
                and ml_task.value.task_type.startswith("Forecasting")
                and task_config_store.value.period is not None
                and task_config_store.value.time_column is not None
            )
        ) and task_config_store.is_valid()

    def on_apply():
        if is_valid():
            complete_task = ml_task.value
            if complete_task.task_type in ["Classification", "Regression", "Forecasting", "Forecasting (classification)"]:
                task_config = replace(
                    task_config_store.value,
                    auto=hyper_parameters.auto.value,
                    custom_learners=hyper_parameters.learner_params.value,
                    custom_learners_enabled=hyper_parameters.selected_learners.value,
                )
                complete_task = replace(complete_task, task_config=task_config)
            set_code(
                {
                    "code": generate_code(complete_task),
                    "meta": dumps(complete_task),
                }
            )
            mixpanel.api.track_with_defaults("inserted code", {"section": "automl", "task_type": complete_task.task_type})
            on_close()
        else:
            set_emphasize_errors(True)

    def init():
        hyper_param_scratchpad.set({})
        set_emphasize_errors(False)
        if is_open and edit_data and edit:
            ml_task.set(edit_data)
            assert edit_data.task_config
            task_config_store.set(edit_data.task_config)

            assert edit_data.task_config
            hyper_parameters.auto.value = edit_data.task_config.auto
            hyper_parameters.learner_params.value = edit_data.task_config.custom_learners or {}
            hyper_parameters.selected_learners.value = edit_data.task_config.custom_learners_enabled or []
        else:
            ml_task.set(MLTask())
            try:
                experiment_name = mlflow.get_experiment("0").name
            except Exception:
                experiment_name = _generate_random_name()
            task_config_store.set(
                TaskConfig(df_var_name=dfs[0], experiment_name=experiment_name, max_iterations=50, max_time=5)
                if dfs
                else TaskConfig(experiment_name=experiment_name, max_iterations=50, max_time=5)
            )

            hyper_parameters.auto.value = True
            hyper_parameters.learner_params.value = {}
            hyper_parameters.selected_learners.value = None

    solara.use_memo(init, [is_open])

    last_task_type = solara.use_previous(ml_task.value.task_type, [ml_task.value.task_type])

    def on_ml_task():
        current = hyper_param_scratchpad.value
        if last_task_type:
            hyper_param_scratchpad.set(
                {
                    "auto": hyper_parameters.auto.value,
                    "learner_params": hyper_parameters.learner_params.value,
                    "selected_learners": hyper_parameters.selected_learners.value,
                }
            )
            if current:
                hyper_parameters.auto.value = current["auto"]
                hyper_parameters.learner_params.value = current["learner_params"]
                hyper_parameters.selected_learners.value = current["selected_learners"]
            else:
                hyper_parameters.auto.value = True
                hyper_parameters.learner_params.value = {}
                hyper_parameters.selected_learners.value = flaml_api.get_estimator_ids_for_task(get_task_arg_for_name(ml_task.value.task_type))

        if hyper_parameters.selected_learners.value is None and ml_task.value.task_type:
            hyper_parameters.selected_learners.value = flaml_api.get_estimator_ids_for_task(get_task_arg_for_name(ml_task.value.task_type))

    solara.use_effect(on_ml_task, [ml_task.value.task_type])

    def load_own_data():
        on_close()
        on_load_own_data()

    with drawer.RightDrawer(
        open=is_open,
        on_open=lambda v: on_close() if not v else None,
        title="AutoML" + (" - " + ml_task.value.task_type if ml_task.value.task_type else ""),
        edit=bool(edit),
        on_apply=on_apply,
        apply_disabled=not ml_task.value.task_type,
        show_var_out=False,
        width="1024px" if not ml_task.value.task_type else "100vw",
        warning_widget=overwrite_warning,
        class_="dca-ml-task-selection",
    ):
        with v.Stepper(v_model=1 if not ml_task.value.task_type else 2, elevation=0, class_="elevation-0", style_="margin: 0"):
            with v.StepperItems():
                with v.StepperContent(step=1):
                    v.Html(
                        tag="p",
                        style_="background-color: var(--jp-border-color3); padding:32px;",
                        children=[
                            "Choose what type of machine learning task you’d like to use with AutoML. ",
                            "For more on how to leverage the power of AutoML in Domino, ",
                            v.Html(
                                tag="a",
                                attributes={"href": "https://docs.dominodatalab.com/en/latest/user_guide/795e6f/domino-code-assist/", "target": "_blank"},
                                children=["check out the docs here"],
                            ),
                            ".",
                        ],
                    )
                    with solara.Div():
                        for task in [t for t in AVAILABLE_TASKS if t.name != "Forecasting (classification)"]:
                            MlTaskTile(task, on_task_info=lambda task_info: Ref(ml_task.fields.task_type).set(task_info.name) if task_info else None)
                with v.StepperContent(step=2):
                    v.Html(
                        tag="p",
                        style_="background-color: var(--jp-border-color3); padding: 32px; margin-bottom: 0;",
                        children=[
                            "Now configure the settings for how you’d like to run the AutoML. For more on how to leverage the power of AutoML in Domino, ",
                            v.Html(
                                tag="a",
                                attributes={"href": "https://docs.dominodatalab.com/en/latest/user_guide/795e6f/domino-code-assist/", "target": "_blank"},
                                children=["check out the docs here"],
                            ),
                            ".",
                        ],
                    )
                    with solara.Div(style_="padding: 32px"):
                        if ml_task.value.task_type:
                            if ml_task.value.task_type in ["Classification", "Regression", "Forecasting", "Forecasting (classification)"]:
                                MlTaskConfigUI(dfs, ml_task.value.task_type, edit, load_own_data, emphasize_errors)
                            else:
                                v.Chip(children=[ml_task.value.task_type])
