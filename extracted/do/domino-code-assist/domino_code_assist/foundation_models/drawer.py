import base64
import html
import json
import math
import os
import re
import sys
from functools import partial
from typing import Any, Callable, Dict, List, Optional, Union

import datasets
import humanize
import ipywidgets as widgets
import mlflow
import pandas as pd
import requests
import solara
from datasets import DatasetDict
from mlflow.utils.name_utils import _generate_random_name
from solara import Reactive, Result
from solara.components.code_highlight_css import CodeHighlightCss
from solara.hooks.misc import CancelledError
from solara.lab import Ref
from transformers import IntervalStrategy

from domino_code_assist.assistant import drawer, mixpanel
from domino_code_assist.df_select import DfSelect
from domino_code_assist.foundation_models.marked import Marked

from .. import util
from ..automl.drawer import bind_value
from ..automl.experiment_search import ExperimentSearch
from ..code import Code
from ..serialize import dumps
from ..util import bind_v_model, to_float, to_int
from . import store

view_task = solara.reactive("All tasks")


license_icon_str = b"""<svg class="ml-2 text-xs text-gray-900" width="1em" height="1em" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M1.46009 5.0945V6.88125C1.46009 7.25201 1.75937 7.55129 2.13012 7.55129C2.50087 7.55129 2.80016 7.25201 2.80016 6.88125V5.0945C2.80016 4.72375
2.50087 4.42446 2.13012 4.42446C1.75937 4.42446 1.46009 4.72375 1.46009 5.0945ZM4.14022 5.0945V6.88125C4.14022 7.25201 4.4395 7.55129 4.81026
7.55129C5.18101 7.55129 5.48029 7.25201 5.48029 6.88125V5.0945C5.48029 4.72375 5.18101 4.42446 4.81026 4.42446C4.4395 4.42446 4.14022 4.72375 4.14022
5.0945ZM1.23674 9.78473H8.38377C8.75452 9.78473 9.0538 9.48545 9.0538 9.1147C9.0538 8.74395 8.75452 8.44466 8.38377 8.44466H1.23674C0.865993 8.44466
0.566711 8.74395 0.566711 9.1147C0.566711 9.48545 0.865993 9.78473 1.23674 9.78473ZM6.82036 5.0945V6.88125C6.82036 7.25201 7.11964 7.55129 7.49039
7.55129C7.86114 7.55129 8.16042 7.25201 8.16042 6.88125V5.0945C8.16042 4.72375 7.86114 4.42446 7.49039 4.42446C7.11964 4.42446 6.82036 4.72375 6.82036
5.0945ZM4.39484 0.623142L0.865993 2.48137C0.682851 2.57517 0.566711 2.76725 0.566711 2.97273C0.566711 3.28094 0.816857 3.53109 1.12507
3.53109H8.49991C8.80365 3.53109 9.0538 3.28094 9.0538 2.97273C9.0538 2.76725 8.93766 2.57517 8.75452 2.48137L5.22568 0.623142C4.9666 0.484669
4.65391 0.484669 4.39484 0.623142V0.623142Z" fill="currentColor"></path></svg>"""

license_icon = "data:image/svg+xml;base64," + base64.b64encode(license_icon_str).decode("utf-8")


def generate_code(config: store.TuneConfig):
    file_name = os.path.join(os.path.dirname(__file__), "code/code.py")
    if config.task == "Text Classification":
        file_name = os.path.join(os.path.dirname(__file__), "code/code_text_classification.py")
    elif config.task == "Token Classification":
        file_name = os.path.join(os.path.dirname(__file__), "code/code_token_classification.py")
    elif config.task in ["Summarization"]:
        file_name = os.path.join(os.path.dirname(__file__), "code/code_summarization.py")
    elif config.task in ["Image Classification"]:
        file_name = os.path.join(os.path.dirname(__file__), "code/code_image_classification.py")
    elif config.task in ["Object Detection"]:
        file_name = os.path.join(os.path.dirname(__file__), "code/code_object_detection.py")
    elif config.task in ["Text Generation", "Conversational"]:
        file_name = os.path.join(os.path.dirname(__file__), "code/code_text_generation_and_conversational.py")
    with open(file_name) as f:
        code = f.read()
        template_delimiter = "# ___TEMPLATE_START___ #\n"
        code = code[code.index(template_delimiter) + len(template_delimiter) :]

        code = code.replace("___experiment_name___", config.experiment_name)  # type: ignore
        code = code.replace("___epochs___", config.epochs)  # type: ignore
        code = code.replace("___learning_rate___", config.learning_rate)  # type: ignore
        code = code.replace("___output_dir___", config.output_dir)  # type: ignore
        auto_ml_task = config.task
        if config.task == "Text Classification":
            auto_ml_task = "seq-classification"
        code = code.replace("___task___", auto_ml_task)  # type: ignore
        code = code.replace("___model_name___", config.model_name)  # type: ignore

        if config.use_huggingface_dataset:
            code = code.replace('ds_dict = datasets.DatasetDict({"train": dca.df_to_ds(___df_var_name___, text_col, label_col)})\n', "")
            code = code.replace('ds_dict = datasets.DatasetDict({"train": dca.df_to_ds_ner(___df_var_name___, "___output_col_name___")})\n', "")
            code = code.replace('ds_dict = datasets.DatasetDict({"train": dca.img_df_to_ds(___df_var_name___, LABEL_COL)})', "")
            code = code.replace("___hf_dataset_name___", config.hf_dataset_name)  # type: ignore

            if config.hf_dataset_config:
                code = code.replace("___hf_dataset_config___", config.hf_dataset_config)
            else:
                code = code.replace(', "___hf_dataset_config___"', "")
        else:
            code = code.replace('ds_dict = datasets.load_dataset("___hf_dataset_name___", "___hf_dataset_config___")\n', "")
            code = code.replace("___df_var_name___", config.df_var_name)  # type: ignore

        code = code.replace("___input_col_name___", config.input_col_name)  # type: ignore
        code = code.replace("___output_col_name___", config.output_col_name)  # type: ignore
        code = code.replace("___evaluation_strategy___", config.evaluation_strategy)  # type: ignore
        code = code.replace("___per_device_train_batch_size___", config.per_device_train_batch_size)  # type: ignore
        code = code.replace("___per_device_eval_batch_size___", config.per_device_eval_batch_size)  # type: ignore
        code = code.replace("___weight_decay___", config.weight_decay)  # type: ignore
        code = code.replace("___metric_for_best_model___", config.metric_for_best_model)  # type: ignore
        code = code.replace("___save_total_limit___", config.save_total_limit)  # type: ignore
        code = code.replace("___save_strategy___", config.save_strategy)  # type: ignore

        if config.task in ["Text Generation", "Summarization", "Conversational"]:
            code = code.replace("___max_input_length___", config.max_input_length)  # type: ignore
            code = code.replace("___max_output_length___", config.max_output_length)  # type: ignore
        if config.task in ["Text Generation"]:
            code = code.replace("___task_prefix___", "generate text: ")  # type: ignore
            code = code.replace("___prompt_prefix___", "Generate text from dialogue")  # type: ignore
        if config.task in ["Conversational"]:
            code = code.replace("___task_prefix___", "converse: ")  # type: ignore
            code = code.replace("___prompt_prefix___", "Converse with dialogue")  # type: ignore
        if config.task in ["Image Classification"]:
            code = code.replace("___gradient_accumulation_steps___", config.gradient_accumulation_steps)  # type: ignore
            code = code.replace("___warmup_ratio___", config.warmup_ratio)  # type: ignore
            code = code.replace("___logging_steps___", config.logging_steps)  # type: ignore
        if config.task in ["Object Detection"]:
            code = code.replace("___label_key___", str(config.label_key))  # type: ignore
            code = code.replace("___fp16___", str(config.fp16))  # type: ignore
            code = code.replace("___save_steps___", config.save_steps)  # type: ignore
            code = code.replace("___logging_steps___", config.logging_steps)  # type: ignore

    return code


@solara.memoize
def get_model_info(model: str):
    text = requests.get(url=f"https://huggingface.co/{model}").text
    res = re.findall(r'data-props="(.+apiUrl.+?)"', text)
    info = json.loads(html.unescape(res[0]))
    return info


@solara.memoize
def get_model_md(model: str):
    md = requests.get(url=f"https://huggingface.co/{model}/resolve/main/README.md").text
    return re.sub(r"\A\s*---\n(.|\n)*---\n", "", md or "")


@solara.memoize
def get_hf_datasets():
    return sorted(datasets.list_datasets(), key=str.lower)


@solara.memoize
def get_hf_datasets_by_task(task: Optional[str]):
    if not task:
        return []
    api_task = task.replace(" ", "-").lower()
    result = requests.get(url="https://huggingface.co/datasets-json", params={"task_categories": f"task_categories:{api_task}", "sort": "downloads"}).json()
    pages = math.floor(result["numTotalItems"] / result["numItemsPerPage"])

    all = [item["id"] for item in result["datasets"]]
    for p in range(1, pages):
        params: Dict[str, Union[int, str]] = {
            "task_categories": f"task_categories:{api_task}",
            "sort": "downloads",
            "p": p,
        }
        result = requests.get(url="https://huggingface.co/datasets-json", params=params).json()
        all.extend([item["id"] for item in result["datasets"]])
    return all


@solara.component
def RecommendendBadge(category: str, task: str, model: str):
    if store.is_recommended(category, task, model):
        with solara.v.Html(
            tag="div",
            style_=" border-radius: 8px; display: inline-block; border: 1px solid var(--jp-border-color2); padding: 4px 8px; margin-top:8px",
            class_="ml-2",
        ):
            solara.v.Img(
                src=util.logo_black,
                style_="height: 12px; width: 12px; display: inline-block; margin-right: 8px;",
            )
            solara.Text("Recommended")
    else:
        solara.Text("")


@solara.component
def ModelSubTitle(category: str, task: str, model: str):
    info_result = get_model_info.use_thread(model)

    if info_result.state == solara.ResultState.ERROR:
        text = "error getting model info"
    elif info_result.state != solara.ResultState.FINISHED:
        text = "loading model info..."
    elif info_result.value is None:
        text = "unknown model info"
    else:
        import datetime

        d = info_result.value.get("model", {}).get("lastModified", "")
        if d:
            date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            ago = humanize.naturaltime(datetime.datetime.now() - datetime.datetime.strptime(d, date_format))
        else:
            ago = "unknown"

        downloads_raw = info_result.value.get("model", {}).get("downloads")
        if downloads_raw is not None:
            downloads = humanize.metric(info_result.value["model"]["downloads"], unit="").replace(" ", "")
        else:
            downloads = "unknown"

        text = f"Updated {ago} • Downloads {downloads}"

    solara.v.ListItemSubtitle(
        children=[
            text,
            solara.v.Html(tag="br"),
            License(model),
            RecommendendBadge(category, task, model),
        ]
    )


@solara.component
def License(model: str):
    info_result = get_model_info.use_thread(model)

    if info_result.state == solara.ResultState.FINISHED and info_result.value is not None:
        with solara.v.Html(
            tag="div", style_=" border-radius: 8px; display: inline-block; border: 1px solid var(--jp-border-color2); padding: 4px 8px; margin-top:8px"
        ):
            solara.v.Img(
                src=license_icon,
                style_="height: 12px; width: 12px; display: inline-block; margin-right: 8px;",
            )
            solara.Text(info_result.value.get("model", {}).get("cardData", {}).get("license", "unknown"))
    else:
        solara.Text("")


@solara.component
def ModelCard(model: str):
    md_result = get_model_md.use_thread(model)

    with solara.Div(class_="px-8 py-4"):
        if md_result.state == solara.ResultState.ERROR:
            solara.Error(f"Error getting model info. Reason: {md_result.error.__repr__()}").key("error")
            return
        if md_result.state != solara.ResultState.FINISHED:
            solara.Text(f"Loading model card for {model} ...").key("loading")
            return

        Marked(md_result.value).key("markdown")


def get_extra_defaults(task: str):
    return (
        {
            "epochs": "10",
            "save_steps": "200",
            "logging_steps": "50",
            "weight_decay": "1e-4",
            "per_device_train_batch_size": "8",
        }
        if task == "Object Detection"
        else {}
    )


def get_metric(task: str):
    if task == "Summarization":
        return "rouge"
    elif task in ["Text Generation", "Conversational"]:
        return "perplexity"
    else:
        return "accuracy"


@solara.component
def Step0(tune_config=store.tune_config):
    def on_task(task: str):
        for category in store.categories():
            for task_ in store.tasks(category):
                if task_ == task:
                    tune_config.update(
                        category=category,
                        task=task_,
                        model_name=store.models(category, task_)[0],
                        metric_for_best_model=get_metric(task_),
                        **get_extra_defaults(task),
                    )
                    return

    with solara.Div(style_="height: 100%; display: flex; flex-direction: column;"):
        solara.v.Html(tag="h2", class_="ma-4", style_="font-size: 20px", children="Which tasks are you trying to achieve?")
        with solara.v.List(style_="padding-top: 0; flex-grow: 1; overflow-y: auto;"):
            with solara.v.ListItemGroup(v_model=None, on_v_model=on_task):
                for category in store.categories():
                    solara.v.Subheader(children=[category])
                    solara.v.Divider()
                    for task in store.tasks(category):
                        with solara.v.ListItem(value=task).key(task):
                            with solara.v.ListItemIcon():
                                solara.Image(os.path.join(os.path.dirname(__file__), f"icons/{task}.svg"), width="100px")
                            with solara.v.ListItemContent():
                                solara.v.ListItemTitle(style="font-size: 1.2rem;", children=task)
                                solara.v.ListItemSubtitle(
                                    children=[
                                        solara.v.Icon(small=True, class_="mr-1", children=["mdi-vector-triangle"]),
                                        f"{len(store.models(category, task))} models available",
                                    ]
                                )
                                solara.v.ListItemSubtitle(style_="white-space: unset; font-size: .750rem;", children=[store.description(category, task)])


@solara.component
def Main(tune_config=store.tune_config):
    def set_task(category, task):
        tune_config.update(
            task=task,
            model_name=store.models(category, task)[0],
            metric_for_best_model=get_metric(task),
            **get_extra_defaults(task),
        )
        mixpanel.api.track_with_defaults(
            "interaction",
            {"section": "foundational models", "type": "selected task", "task": task},
        )

    with solara.Div(style_="display: flex; flex-grow: 1; height: 100%"):
        with solara.Div(style_="width: 33%; overflow: hidden; display: flex; flex-direction: column;"):
            with solara.Row():
                with solara.v.Col():
                    solara.v.Select(
                        label="Task",
                        items=store.tasks(tune_config.value.category),
                        v_model=tune_config.value.task,
                        on_v_model=partial(set_task, tune_config.value.category),
                        hide_details=True,
                    )
            solara.Text("Model", style="margin-left: 12px; font-size: 12px;")
            with solara.Div(style_="overflow-y: auto;"):
                with solara.v.List(style_="padding-top: 0"):
                    with solara.v.ListItemGroup(**bind_v_model(tune_config.fields.model_name), mandatory=True):
                        for model_ in store.models(tune_config.value.category, tune_config.value.task):
                            with solara.v.ListItem(value=model_).key(model_):
                                with solara.v.ListItemContent():
                                    solara.v.ListItemTitle(children=model_)
                                    ModelSubTitle(tune_config.value.category, tune_config.value.task, model_)

        # Note: key needed to reset scroll position when changing model
        with solara.Div(style_="width: 67%; overflow: auto; background-color: var(--jp-border-color3); display: flex; flex-direction: column;").key(
            f"model-card-{tune_config.value.task}-{tune_config.value.model_name}"
        ):
            if tune_config.value.model_name:
                with solara.Div(style_="", class_="px-8 pt-4"):
                    with solara.Div(style_="display: flex"):
                        solara.v.Html(tag="h2", children=[tune_config.value.model_name or ""], class_="text-2xl font-bold mb-4")
                        solara.v.Spacer()
                        solara.Button(
                            href=f"https://huggingface.co/{tune_config.value.model_name}",
                            target="_blank",
                            color="primary",
                            text=True,
                            style_="text-transform: unset",
                            children=["Learn more"],
                        )
                        solara.Button("fine-tune", outlined=True, color="primary", on_click=lambda: Ref(store.tune_config.fields.model_selected).set(True))
                    solara.v.Divider()
                with solara.Div(style_="display: flex; flex-grow: 1; flex-direction: column; overflow: auto;"):
                    with solara.Div(class_="px-8 py-4"):
                        License(tune_config.value.model_name)
                        RecommendendBadge(tune_config.value.category, tune_config.value.task, tune_config.value.model_name)
                    ModelCard(tune_config.value.model_name)


def DataPreview(tune_config=store.tune_config):
    df: Optional[pd.DataFrame] = util.nb_locals[tune_config.value.df_var_name] if tune_config.value.df_var_name else None
    if df is None:
        return solara.Info("Please select a data frame")
    if not tune_config.value.input_col_name:
        return solara.Info("Please select an input column")
    if not tune_config.value.output_col_name:
        return solara.Info("Please select an output column")

    with solara.Div():
        with solara.v.Html(tag="table", class_="dcs-foundation-data-preview"):
            with solara.v.Html(tag="thead"):
                with solara.v.Html(tag="tr"):
                    if tune_config.value.input_col_name:
                        with solara.v.Html(tag="th").key("input"):
                            solara.Text(tune_config.value.input_col_name + " ")
                            solara.v.Chip(children=store.get_column_name(tune_config.value, "input"), small=True)
                    if tune_config.value.output_col_name:
                        with solara.v.Html(tag="th").key("output"):
                            solara.Text(tune_config.value.output_col_name + " ")
                            solara.v.Chip(children=store.get_column_name(tune_config.value, "output"), small=True)
            with solara.v.Html(tag="tbody"):
                for i in range(5):
                    with solara.v.Html(tag="tr").key(i):
                        if tune_config.value.input_col_name:
                            solara.v.Html(tag="td", children=[str(df[tune_config.value.input_col_name][i])]).key(f"{i}-input")
                        if tune_config.value.output_col_name:
                            solara.v.Html(tag="td", children=[str(df[tune_config.value.output_col_name][i])]).key(f"{i}-output")
                with solara.v.Html(tag="tr").key("eps"):
                    if tune_config.value.input_col_name:
                        with solara.v.Html(tag="td").key("eps-input"):
                            solara.Text("...")
                    if tune_config.value.output_col_name:
                        with solara.v.Html(tag="td").key("eps-output"):
                            solara.Text("...")


dataset_dict = solara.reactive(None)


def DataPreviewDs(tune_config=store.tune_config):
    if tune_config.value.hf_dataset_name is None:
        return solara.Info("Please select a dataset")
    if tune_config.value.hf_dataset_name and tune_config.value.hf_dataset_config_options and tune_config.value.hf_dataset_config is None:
        return solara.Info("Please select a config")
    if dataset_dict.value:
        ds_keys = list(dataset_dict.value.keys())
        first_ds_key = ds_keys[0]
        lines = dataset_dict.value[first_ds_key][:5]

        with solara.Div():
            with solara.v.Html(tag="table", class_="dcs-foundation-data-preview"):
                with solara.v.Html(tag="thead"):
                    with solara.v.Html(tag="tr"):
                        for col in lines.keys():
                            with solara.v.Html(tag="th"):
                                with solara.Div(style_="display: inline-block;"):
                                    solara.Text(col + " ")
                                    if col == tune_config.value.input_col_name:
                                        solara.v.Chip(children=store.get_column_name(tune_config.value, "input"), small=True)
                                    if col == tune_config.value.output_col_name:
                                        solara.v.Chip(children=store.get_column_name(tune_config.value, "output"), small=True)
                with solara.v.Html(tag="tbody"):
                    for line in list(zip(*lines.values())):
                        with solara.v.Html(tag="tr"):
                            for col in line:
                                solara.v.Html(tag="td", children=[str(col)])
                    with solara.v.Html(tag="tr").key("eps"):
                        for col in lines.keys():
                            solara.v.Html(tag="td", children=["..."])


@solara.component
def HfSearch(tune_config: Reactive[store.TuneConfig], dataset_dict=dataset_dict):
    task = tune_config.value.task
    value = tune_config.value.hf_dataset_name

    datasets_result = get_hf_datasets_by_task.use_thread(task)

    output_widget = solara.use_memo(widgets.Output, [])

    def load():
        if value:
            mixpanel.api.track_with_defaults(
                "interaction",
                {
                    "section": "foundational models",
                    "type": "attempt to load dataset",
                    "task_type": tune_config.value.task,
                    "model_type": tune_config.value.model_name,
                    "dataset": tune_config.value.hf_dataset_name,
                },
            )
            dataset_dict.value = None
            output_widget.clear_output()
            exception = None
            with output_widget:
                try:
                    dataset_dict.value = None
                    if tune_config.value.hf_dataset_config:
                        ds = datasets.load_dataset(value, tune_config.value.hf_dataset_config)
                    else:
                        configs = datasets.get_dataset_config_names(value)
                        if len(configs) > 1:
                            Ref(tune_config.fields.hf_dataset_config_options).set(configs)
                            return None
                        ds = datasets.load_dataset(value)
                    dataset_dict.value = ds
                    sys.stdout.flush()
                    sys.stderr.flush()
                    return ds
                except Exception as e:
                    exception = e
                except CancelledError:
                    mixpanel.api.track_with_defaults(
                        "interaction",
                        {
                            "section": "foundational models",
                            "type": "canceled load dataset",
                            "task_type": tune_config.value.task,
                            "model_type": tune_config.value.model_name,
                            "dataset": tune_config.value.hf_dataset_name,
                        },
                    )
                    if tune_config.value.hf_dataset_config_options:
                        Ref(tune_config.fields.hf_dataset_config).set(None)
                    else:
                        on_value(None)
            if exception:
                mixpanel.api.track_with_defaults(
                    "interaction",
                    {
                        "section": "foundational models",
                        "type": "failed to load dataset",
                        "task_type": tune_config.value.task,
                        "model_type": tune_config.value.model_name,
                        "dataset": tune_config.value.hf_dataset_name,
                        "exception": str(exception),
                    },
                )
                raise exception

    load_result: Result[Optional[DatasetDict]] = solara.use_thread(load, [value, tune_config.value.hf_dataset_config])

    def on_value(v: Optional[str]):
        tune_config.update(hf_dataset_name=v, hf_dataset_config_options=None, hf_dataset_config=None)

    if datasets_result.state == solara.ResultState.ERROR:
        solara.Warning(datasets_result.error.__repr__())
    elif datasets_result.state != solara.ResultState.FINISHED:
        solara.Div(children="Loading dataset list...")
        solara.v.ProgressLinear(indeterminate=True)
    else:
        solara.v.Autocomplete(label="Dataset", v_model=value, items=datasets_result.value, hide_details=True, on_v_model=on_value)
        if tune_config.value.hf_dataset_config_options:
            solara.v.Select(
                label="Config",
                items=tune_config.value.hf_dataset_config_options,
                hide_details=True,
                **bind_v_model(tune_config.fields.hf_dataset_config),
            )
        if value:
            if load_result.state == solara.ResultState.ERROR:
                solara.Error(load_result.error.__repr__())
            else:
                if load_result.state != solara.ResultState.FINISHED:
                    with solara.Div(style_="width: 118px;"):
                        solara.Button("cancel", color="primary", outlined=True, icon_name="mdi-close", on_click=load_result.cancel)
                        solara.v.ProgressLinear(indeterminate=True)
                    solara.Div(children=[output_widget])
                if load_result.state == solara.ResultState.FINISHED and load_result.value:
                    keys = load_result.value.keys()
                    rows = [load_result.value[k].num_rows for k in keys]
                    solara.Text(f"Datasets: {', '.join([str(t) for t in zip(keys, rows)])}")


def required(field):
    ref = Ref(field)
    if ref.value is None or ref.value == "":
        error_message = "required"
    else:
        error_message = None

    return {
        "v_model": ref.value,
        "on_v_model": ref.set,
        "error_messages": error_message,
        "hide_details": bool(not error_message),
    }


def required_num(fn: Callable[[str], Optional[Union[int, float]]], field):
    ref = Ref(field)
    if ref.value is None or ref.value == "":
        error_message = "required"
    elif fn(ref.value) is None:
        error_message = "invalid"
    else:
        error_message = None

    return {
        "v_model": ref.value,
        "on_v_model": ref.set,
        "error_messages": error_message,
        "hide_details": bool(not error_message),
    }


@solara.component
def FineTuneUI(dfs: List[str], expected_columns: List[str], is_visible: bool, edit: bool, on_load_own_data: Callable[[], None], tune_config=store.tune_config):
    expanded, set_expanded = solara.use_state([0])

    extended_dfs: List[Any] = dfs
    if not edit:
        extended_dfs = extended_dfs + [{"divider": True}, "Load more data"]

    df: Optional[pd.DataFrame] = util.nb_locals[tune_config.value.df_var_name] if tune_config.value.df_var_name else None
    available_columns: Optional[List[str]] = df.columns.tolist() if df is not None else None
    if tune_config.value.use_huggingface_dataset:
        if dataset_dict.value:
            available_columns = list(dataset_dict.value[list(dataset_dict.value.keys())[0]].features.keys())
        else:
            available_columns = None

    def update_df_var_name(df_var_name):
        if df_var_name == "Load more data":
            on_load_own_data()
            return
        tune_config.update(df_var_name=df_var_name, input_col_name=None, output_col_name=None)

        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "foundational models",
                "type": "selected dataframe",
                "task_type": tune_config.value.task,
                "model_type": tune_config.value.model_name,
            },
        )

    input_name = store.get_column_name(tune_config.value, "input")
    output_name = store.get_column_name(tune_config.value, "output")

    def reset_cols():
        if available_columns is not None:
            new_input = tune_config.value.input_col_name if tune_config.value.input_col_name in available_columns else None
            new_output = tune_config.value.output_col_name if tune_config.value.output_col_name in available_columns else None
            if not new_input and input_name in (available_columns or []):
                new_input = input_name
            if not new_output and output_name in (available_columns or []):
                new_output = output_name
            tune_config.update(input_col_name=new_input, output_col_name=new_output)

    solara.use_memo(reset_cols, [available_columns])

    with solara.Div(style_="height: 100%; overflow-y: auto; overflow-x: hidden; max-width: 100%;"):
        with solara.v.Row():
            with solara.v.Col():
                with solara.Div(style_="display: flex; ma-8"):
                    with solara.Button(icon=True, color="primary", on_click=lambda: Ref(tune_config.fields.model_selected).set(False)):
                        solara.v.Icon(children="mdi-chevron-left", large=True)
                    solara.v.Html(tag="h2", class_="text-2xl font-bold mb-4", children=[tune_config.value.model_name or ""])
                solara.v.Divider()
        with solara.v.Row(class_="dca-automl-config"):
            with solara.v.Col(style_="max-width: 800px"):
                with solara.v.ExpansionPanels(multiple=True, v_model=expanded, on_v_model=set_expanded, accordeon=True, style_="width: 800px"):
                    with solara.v.ExpansionPanel():
                        with solara.v.ExpansionPanelHeader():
                            with solara.Div(style_="min-width: 140px"):
                                solara.v.Html(tag="strong", children=["Dataset "])
                            solara.Text("Load dataset for training")
                        with solara.v.ExpansionPanelContent():
                            solara.Div(children=["Which data type would you like to use?"], style_="font-weight: bold;")
                            with solara.ToggleButtonsSingle(
                                value=0 if tune_config.value.use_huggingface_dataset else 1,
                                on_value=lambda index: Ref(tune_config.fields.use_huggingface_dataset).set(index == 0),
                            ):
                                solara.Button("Hugging Face", style_="text-transform: unset", value=0)
                                solara.Button("Dataframe", style_="text-transform: unset", value=1)
                            if tune_config.value.use_huggingface_dataset and is_visible:
                                with solara.Div():
                                    HfSearch(tune_config)
                            else:
                                with solara.Div():
                                    with solara.v.Row().key("df"):
                                        with solara.v.Col(class_="py-1"):
                                            DfSelect(
                                                value=tune_config.value.df_var_name,
                                                label="Data frame",
                                                on_value=update_df_var_name,
                                                items=extended_dfs or [],
                                                hide_details=True,
                                            )
                            if available_columns:
                                with solara.v.Row().key("cols"):
                                    with solara.v.Col(class_="py-5", style_="flex-grow: unset;"):
                                        solara.v.Chip(children=[input_name])
                                    with solara.v.Col(class_="py-1"):
                                        solara.v.Select(
                                            items=available_columns or [],
                                            label=f"{input_name.capitalize()} column",
                                            **bind_v_model(tune_config.fields.input_col_name),
                                            hide_details=True,
                                        )
                                    with solara.v.Col(class_="py-5", style_="flex-grow: unset;"):
                                        solara.v.Chip(children=[output_name])
                                    with solara.v.Col(class_="py-1"):
                                        solara.v.Select(
                                            items=available_columns or [],
                                            label=f"{output_name.capitalize()} column",
                                            **bind_v_model(tune_config.fields.output_col_name),
                                            hide_details=True,
                                        )
                    with solara.v.ExpansionPanel():
                        with solara.v.ExpansionPanelHeader():
                            with solara.Div(style_="min-width: 140px"):
                                solara.v.Html(tag="strong", children=["Training "])
                            solara.Text("An experiment will be created to log the optimizations")
                        with solara.v.ExpansionPanelContent():
                            with solara.v.Row():
                                with solara.v.Col(class_="py-1"):
                                    ExperimentSearch(**bind_value(tune_config.fields.experiment_name))
                            with solara.v.Row():
                                with solara.v.Col(class_="py-1"):
                                    solara.v.TextField(
                                        label="Epoch",
                                        clearable=True,
                                        **required_num(to_int, tune_config.fields.epochs),
                                    )
                                with solara.v.Col(class_="py-1"):
                                    solara.v.TextField(
                                        label="Learning rate",
                                        clearable=True,
                                        **required_num(to_float, tune_config.fields.learning_rate),
                                    )
                                with solara.v.Col(class_="py-1"):
                                    solara.v.TextField(
                                        label="Ouptut directory",
                                        **required(tune_config.fields.output_dir),
                                    )
                            with solara.v.Row():
                                with solara.v.Col():
                                    solara.v.Select(
                                        label="Evaluation strategy",
                                        items=[e.value for e in IntervalStrategy],
                                        **bind_v_model(tune_config.fields.evaluation_strategy),
                                    )
                                with solara.v.Col():
                                    metric_items = ["accuracy"]
                                    if tune_config.value.task == "Token Classification":
                                        metric_items = ["precision", "recall", "f1", "accuracy"]
                                    if tune_config.value.task in ["Summarization"]:
                                        metric_items = ["rouge", "bleu"]
                                    if tune_config.value.task in ["Conversational", "Text Generation"]:
                                        metric_items = ["perplexity"]
                                    solara.v.Select(
                                        label="Metric for best model",
                                        items=metric_items,
                                        **bind_v_model(tune_config.fields.metric_for_best_model),
                                    )
                                with solara.v.Col():
                                    solara.v.Select(
                                        label="Save strategy",
                                        items=[e.value for e in IntervalStrategy],
                                        **bind_v_model(tune_config.fields.save_strategy),
                                    )
                            with solara.v.Row():
                                with solara.v.Col():
                                    solara.v.TextField(
                                        label="Per device train batch size",
                                        **required_num(to_int, tune_config.fields.per_device_train_batch_size),
                                    )
                                with solara.v.Col():
                                    solara.v.TextField(
                                        label="Per device eval batch size",
                                        **required_num(to_int, tune_config.fields.per_device_eval_batch_size),
                                    )
                                with solara.v.Col():
                                    solara.v.TextField(
                                        label="Weight decay",
                                        **required_num(to_float, tune_config.fields.weight_decay),
                                    )
                                with solara.v.Col():
                                    solara.v.TextField(
                                        label="Save total limit",
                                        **required_num(to_int, tune_config.fields.save_total_limit),
                                    )
                    if tune_config.value.task in ["Summarization", "Conversational", "Text Generation"]:
                        with solara.v.ExpansionPanel().key("summarization/conversational/generation"):
                            with solara.v.ExpansionPanelHeader():
                                with solara.Div(style_="min-width: 140px"):
                                    solara.v.Html(tag="strong", children=[tune_config.value.task])
                                solara.Text(f"Settings specific to {tune_config.value.task}")
                            with solara.v.ExpansionPanelContent():
                                with solara.v.Row():
                                    with solara.v.Col(class_="py-1"):
                                        solara.v.TextField(
                                            label="Max input length",
                                            **required_num(to_int, tune_config.fields.max_input_length),
                                        )
                                    with solara.v.Col(class_="py-1"):
                                        solara.v.TextField(
                                            label="Max output length",
                                            **required_num(to_int, tune_config.fields.max_output_length),
                                        )
                    if tune_config.value.task in ["Image Classification"]:
                        with solara.v.ExpansionPanel().key("image_classification"):
                            with solara.v.ExpansionPanelHeader():
                                with solara.Div(style_="min-width: 140px"):
                                    solara.v.Html(tag="strong", children=[tune_config.value.task])
                                solara.Text(f"Settings specific to {tune_config.value.task}")
                            with solara.v.ExpansionPanelContent():
                                with solara.v.Row():
                                    with solara.v.Col(class_="py-1"):
                                        solara.v.TextField(
                                            label="Gradient accumulation steps",
                                            **required_num(to_int, tune_config.fields.gradient_accumulation_steps),
                                        )
                                    with solara.v.Col(class_="py-1"):
                                        solara.v.TextField(
                                            label="Warmup ratio",
                                            **required_num(to_float, tune_config.fields.warmup_ratio),
                                        )
                                    with solara.v.Col(class_="py-1"):
                                        solara.v.TextField(
                                            label="logging_steps",
                                            **required_num(to_int, tune_config.fields.logging_steps),
                                        )
                    if tune_config.value.task in ["Object Detection"]:
                        with solara.v.ExpansionPanel().key("object_detection"):
                            with solara.v.ExpansionPanelHeader():
                                with solara.Div(style_="min-width: 140px"):
                                    solara.v.Html(tag="strong", children=[tune_config.value.task])
                                solara.Text(f"Settings specific to {tune_config.value.task}")
                            with solara.v.ExpansionPanelContent():
                                with solara.v.Row():
                                    with solara.v.Col(class_="py-1"):
                                        solara.v.TextField(label="Label key", **required(tune_config.fields.label_key))
                                    with solara.v.Col(class_="py-1"):
                                        solara.v.Switch(
                                            label="fp16",
                                            messages=["Warning: high memory use when disabled"] if not tune_config.value.fp16 else None,
                                            **bind_v_model(tune_config.fields.fp16),
                                        )
                                    with solara.v.Col(class_="py-1"):
                                        solara.v.TextField(
                                            label="Save steps",
                                            **required_num(to_int, tune_config.fields.save_steps),
                                        )
                                    with solara.v.Col(class_="py-1"):
                                        solara.v.TextField(
                                            label="logging_steps",
                                            **required_num(to_int, tune_config.fields.logging_steps),
                                        )

            with solara.v.Col(style_="overflow: hidden"):
                if tune_config.value.use_huggingface_dataset:
                    DataPreviewDs()
                else:
                    DataPreview()
                if store.is_valid(tune_config.value):
                    with solara.Div(class_="dca-foundation__code mt-4"):
                        CodeHighlightCss()
                        Code(code_chunks=[generate_code(tune_config.value)], on_event=lambda x: None, error=None)


logo = solara.util.load_file_as_data_url(os.path.join(os.path.dirname(__file__), "hf-logo.png"), "image/png")


@solara.component
def FoundationDrawer(
    edit_data: Optional[Any],
    set_code: Callable[[Dict], None],
    dfs: List[str],
    is_open: bool,
    edit: bool,
    on_close: Callable[[], None],
    on_load_own_data: Callable[[], None],
    overwrite_warning=None,
):
    def init():
        if is_open and edit_data and edit:
            store.tune_config.set(edit_data)
        else:
            try:
                experiment_name = mlflow.get_experiment("0").name
            except Exception:
                experiment_name = _generate_random_name()
            store.tune_config.set(store.TuneConfig(experiment_name=experiment_name))

    solara.use_memo(init, [is_open])

    def on_apply():
        set_code(
            {
                "code": generate_code(store.tune_config.value),
                "meta": dumps(store.tune_config.value),
            }
        )
        mixpanel.api.track_with_defaults(
            "inserted code",
            {
                "section": "foundation_models",
                "task_type": store.tune_config.value.task,
                "model_type": store.tune_config.value.model_name,
                "input_col_name": store.tune_config.value.input_col_name,
                "output_col_name": store.tune_config.value.output_col_name,
                "experiment_name": store.tune_config.value.experiment_name,
                "use_huggingface_dataset": store.tune_config.value.use_huggingface_dataset,
                "hf_dataset_name": store.tune_config.value.hf_dataset_name,
                "hf_dataset_config": store.tune_config.value.hf_dataset_config,
                "epochs": store.tune_config.value.epochs,
                "learning_rate": store.tune_config.value.learning_rate,
                "evaluation_strategy": store.tune_config.value.evaluation_strategy,
                "per_device_train_batch_size": store.tune_config.value.per_device_train_batch_size,
                "per_device_eval_batch_size": store.tune_config.value.per_device_eval_batch_size,
                "weight_decay": store.tune_config.value.weight_decay,
                "metric_for_best_model": store.tune_config.value.metric_for_best_model,
                "save_total_limit": store.tune_config.value.save_total_limit,
                "save_strategy": store.tune_config.value.save_strategy,
                # Seq to seq specific
                "max_input_length": store.tune_config.value.max_input_length,
                "max_output_length": store.tune_config.value.max_output_length,
                # Image Classification specific
                "gradient_accumulation_steps": store.tune_config.value.gradient_accumulation_steps,
                "warmup_ratio": store.tune_config.value.warmup_ratio,
                "logging_steps": store.tune_config.value.logging_steps,
                # Object Detection specific
                "fp16": store.tune_config.value.fp16,
                "save_steps": store.tune_config.value.fp16,
                "label_key": store.tune_config.value.fp16,
            },
        )
        on_close()

    if store.tune_config.value.category is None:
        step = 0
    elif not store.tune_config.value.model_selected:
        step = 1
    else:
        step = 2

    with drawer.RightDrawer(
        open=is_open,
        on_open=lambda v: on_close() if not v else None,
        title="Foundation Models",
        edit=bool(edit),
        on_apply=on_apply,
        apply_disabled=not store.is_valid(store.tune_config.value),
        show_var_out=False,
        width="800px" if step == 0 else "100vw",
        warning_widget=overwrite_warning,
        class_="dca-foundation-drawer",
    ):
        if is_open:
            with solara.Div(style_="overflow: hidden; height: 100%"):
                solara.v.Img(
                    src=logo,
                    style_="height: 28px; max-width: 115px; border-radius: 14px; position: absolute; top: 19px; left: 213px;",
                )
                with solara.v.Stepper(v_model=step, elevation=0, class_="elevation-0 dca-foundation-drawer-content", style_="margin: 0"):
                    with solara.v.StepperItems():
                        with solara.v.StepperContent(step=0, style_="padding: 0"):
                            Step0()
                        with solara.v.StepperContent(step=1, style_="padding: 0"):
                            Main()
                        with solara.v.StepperContent(step=2):
                            FineTuneUI(
                                dfs, expected_columns=["input", "output"], is_visible=is_open and step == 2, edit=False, on_load_own_data=on_load_own_data
                            )
