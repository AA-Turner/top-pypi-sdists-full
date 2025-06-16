from functools import partial
from typing import Dict, List, Optional, Union, cast

import reacton.ipyvuetify as v
import solara

from domino_code_assist.automl import flaml_api

auto = solara.reactive(cast(bool, True))
learner_params = solara.reactive(cast(Dict[str, Dict], {}))
selected_learners = solara.reactive(cast(Optional[List[str]], []))


@solara.component
def Hyperparameters(task: str, auto=auto, learner_params=learner_params, selected_learners=selected_learners):
    all_learners = flaml_api.get_estimator_ids_for_task(task)

    def compute_select_all():
        if len(selected_learners.value or []) == 0:
            return False
        elif len(selected_learners.value) == len(all_learners):
            return True
        else:
            return None

    select_all = compute_select_all()

    opened_estimator, set_opened_estimator = solara.use_state(cast(Optional[Dict], None))

    def on_select_learner(learner: str, on: bool):
        if on:
            learners = selected_learners.value + [learner]
        else:
            learners = [sl for sl in selected_learners.value if sl != learner]
        selected_learners.set(learners)

    def on_select_all(on: bool):
        selected_learners.set([*all_learners] if on else [])

    def on_open_params(estimator: Dict):
        params = learner_params.value.get(estimator["id"], {})
        params_selected.value = params.get("selected", [])
        params_lower.value = params.get("lower", {})
        params_upper.value = params.get("upper", {})
        set_opened_estimator(estimator)

    def on_save():
        if opened_estimator:
            learner_params.value = {
                **learner_params.value,
                opened_estimator["id"]: {
                    "selected": params_selected.value,
                    "lower": params_lower.value,
                    "upper": params_upper.value,
                },
            }
            set_opened_estimator(None)

    def get_enabled_hyper_params(estimator: Dict) -> List[str]:
        return learner_params.value.get(estimator["id"], {}).get("selected", [])

    with v.ExpansionPanel(class_="dca-hyperparameters"):
        with v.ExpansionPanelHeader().key("header"):
            with solara.Div(style_="display: flex; flex-direction: row; max-width: 100%; overflow: hidden;"):
                with solara.Div(style_="min-width: 140px"):
                    v.Html(tag="strong", children=["Advanced "])
                with solara.Div():
                    solara.Text("Hyperparameter search space: ", style="font-weight: bold; color: var(--jp-border-color1);")
                    solara.Text("auto" if auto.value else "custom")
        with v.ExpansionPanelContent().key("content"):
            solara.Text("Hyperparameter Search Space")
            v.Switch(v_model=auto.value, on_v_model=auto.set, label="Auto (recommended) Domino will auto-tune hyperparameters")
            with solara.Div(class_=f"dca-hyperparameters-list {'dca-hyperparameters-list-off' if auto.value else ''}"):
                with solara.Div():
                    v.Checkbox(label="Select all", v_model=select_all, on_v_model=on_select_all, indeterminate=select_all is None)
                for estimator in [item for item in flaml_api.hyperparameters if task in item["tasks"]]:
                    with solara.ColumnsResponsive([6, 5, 1], gutters=False, classes=["pa-0"], style="line-height: 2.2"):
                        with solara.Row():
                            v.Checkbox(
                                v_model=estimator["id"] in (selected_learners.value or []),
                                on_v_model=partial(on_select_learner, estimator["id"]),
                                class_="dca-hyperparameters-checkbox",
                                hide_details=True,
                            )
                            solara.Text("Learner: ", style="color: var(--jp-border-color1); margin-left: -12px;")
                            solara.Text(estimator.get("readable_name", estimator["id"]))
                        with solara.Row():
                            solara.Text("Hyper-parameters: ", style="color: var(--jp-border-color1);")
                            solara.Text(
                                f" {len(get_enabled_hyper_params(estimator))}/{len(flaml_api.get_hyper_parameters_for_task(estimator, task))} configured"
                            )
                        with solara.Row():
                            solara.Button(icon_name="mdi-pencil", icon=True, on_click=lambda estimator=estimator: on_open_params(estimator))
        if opened_estimator:
            with v.Dialog(v_model=bool(opened_estimator), on_v_model=lambda on: set_opened_estimator(None) if not on else None, max_width="800px").key(
                "dialog"
            ):
                with v.Card(class_="dca-hyperparameters-dialog"):
                    with v.CardTitle():
                        solara.Text("Edit hyper-parameters for ", style="white-space: pre;")
                        solara.Text(opened_estimator.get("readable_name", opened_estimator["id"]), style="font-weight: bold;")
                    with v.CardText():
                        HyperParametersPanel(task, opened_estimator["id"])
                    with v.CardActions():
                        solara.Button(color="primary", text=True, children=["Save"], on_click=on_save)
                        solara.Button(color="primary", text=True, children=["Cancel"], on_click=lambda: set_opened_estimator(None))


params_selected = solara.reactive(cast(List[str], []))
params_lower = solara.reactive(cast(Dict[str, Union[str, List]], {}))
params_upper = solara.reactive(cast(Dict[str, str], {}))


@solara.component
def HyperParametersPanel(
    task: str,
    estimator_id: str,
    selected=params_selected,
    upper=params_upper,
    lower=params_lower,
):
    estimator = [item for item in flaml_api.hyperparameters if item["id"] == estimator_id][0]

    available_params = flaml_api.get_hyper_parameters_for_task(estimator, task)

    def compute_select_all():
        if len(selected.value) == 0:
            return False
        elif len(selected.value) == len(available_params):
            return True
        else:
            return None

    select_all = compute_select_all()

    def on_select_param(param: str, on: bool):
        if on:
            params = selected.value + [param]
        else:
            params = [sl for sl in selected.value if sl != param]
        selected.set(params)

    def on_select_all(on: bool):
        selected.set(available_params if on else [])

    def on_param(param, prop, value):
        if prop == "lower":
            lower.value = {**lower.value, param: value}
        if prop == "upper":
            upper.value = {**upper.value, param: value}

    with solara.Div():
        with solara.Div():
            v.Checkbox(label="Select all", v_model=select_all, on_v_model=on_select_all, indeterminate=select_all is None)
        for param in available_params:
            with solara.ColumnsResponsive([4, 4, 4], gutters=False, classes=["pa-0"], style="line-height: 2.2"):
                type_ = estimator["hyper-parameters"][param]["type"]  # type: ignore
                with solara.Row(classes=["pt-4"]):
                    v.Checkbox(
                        v_model=param in selected.value,
                        on_v_model=partial(on_select_param, param),
                        class_="dca-hyperparameters-checkbox",
                        hide_details=True,
                    )
                    solara.Text("Parameter: ", style="color: var(--jp-border-color1); margin-left: -12px;")
                    solara.Text(param)
                if isinstance(type_, List):
                    with solara.Row().key("choice1"):
                        v.Select(
                            label="choice",
                            items=[{"text": str(choice), "value": choice} for choice in type_],
                            multiple=True,
                            v_model=lower.value.get(param),
                            on_v_model=partial(on_param, param, "lower"),
                            class_="ml-4",
                        )
                    solara.Row().key("choice2")
                else:
                    with solara.Row().key("other1"):
                        v.TextField(
                            label="lower",
                            v_model=lower.value.get(param),
                            on_v_model=partial(on_param, param, "lower"),
                            class_="ml-4",
                        )
                    with solara.Row().key("other2"):
                        v.TextField(
                            label="upper",
                            v_model=upper.value.get(param),
                            on_v_model=partial(on_param, param, "upper"),
                            class_="ml-4",
                        )


def get_hyper_parameters_string(custom_learners: Dict, custom_learners_enabled: List[str]):
    def to_domain(type_: Union[str, List], lower: Union[str, List], upper: str):
        if type_ == "int":
            return {
                "domain": f"tune.lograndint(lower={lower}, upper={upper})",
            }
        if type_ == "float":
            return {
                "domain": f"tune.loguniform(lower={lower}, upper={upper})",
            }
        if isinstance(type_, List):
            return {
                "domain": f"tune.choice({ [None if e == 'None' else e for e in lower]})",
            }

    def learner(k, learner_dict):
        estimator = [e for e in flaml_api.hyperparameters if e["id"] == k][0]

        def get_type(param) -> Union[str, List]:
            return estimator["hyper-parameters"][param]["type"]  # type: ignore

        return {param: to_domain(get_type(param), learner_dict["lower"][param], learner_dict.get("upper", {}).get(param)) for param in learner_dict["selected"]}

    cv_learners = {k: learner(k, v) for k, v in custom_learners.items() if k in custom_learners_enabled}

    def dict_to_string(d, indent=0):
        output = []
        for key, value in d.items():
            if isinstance(value, dict):
                output.append(f"""{' ' * indent}"{key}": {{""")
                output.append(dict_to_string(value, indent + 4))
                output.append(f"{' ' * indent}}},")
            else:
                output.append(f"""{' ' * indent}"{key}": {value}""")
        return "\n".join(output)

    return "{\n" + dict_to_string(cv_learners, 4) + "\n}"
