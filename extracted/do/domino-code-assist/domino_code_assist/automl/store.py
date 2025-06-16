from dataclasses import asdict, dataclass
from typing import Dict, List, Optional

import solara
from solara.lab import Ref

from domino_code_assist import util


@dataclass(frozen=True)
class TaskInfo:
    name: str
    arg: str
    description: str
    image: str = "placeholder.png"
    soon: bool = False


AVAILABLE_TASKS = [
    TaskInfo(
        name="Classification",
        arg="classification",
        description="Tag and categorize any kind of data so that it can be better understood and analyzed.",
        image="icon_classification.svg",
    ),
    TaskInfo(
        name="Regression",
        arg="regression",
        description="Estimate the relationships between variables and output a numeric value.",
        image="icon_regression.svg",
    ),
    TaskInfo(
        name="Forecasting",
        arg="ts_forecast",
        description="Predict future conditions by considering historical data.",
        image="icon_forecasting.svg",
    ),
    TaskInfo(
        name="Forecasting (classification)",
        arg="ts_forecast_classification",
        description="Predict future conditions by considering historical data.",
        image="icon_forecasting.svg",
    ),
]


def get_task_arg_for_name(name):
    for task in AVAILABLE_TASKS:
        if task.name == name:
            return task.arg
    return None


@dataclass(frozen=True)
class TaskConfig:
    df_var_name: Optional[str] = None
    experiment_name: Optional[str] = None
    exclude_features: Optional[List[str]] = None
    target: Optional[str] = None
    optimization_metric: str = "log_loss"
    max_iterations: Optional[int] = None
    max_time: Optional[int] = None
    time_unit: str = "Minutes"
    period: Optional[int] = None
    auto: bool = True
    custom_learners: Optional[Dict] = None
    custom_learners_enabled: Optional[List[str]] = None
    time_column: Optional[str] = None
    resampling_strategy: str = "Auto"
    split_ratio: str = "0.1"
    folds: str = "5"


class ReactiveTaskConfig(solara.lab.Reactive[TaskConfig]):
    def is_valid(self):
        return bool(
            self.value.df_var_name
            and self.value.target
            and self.value.experiment_name
            and (
                self.value.resampling_strategy == "Auto"
                or (self.value.resampling_strategy == "Holdout" and util.to_float(self.value.split_ratio) is not None)
                or (self.value.resampling_strategy == "Cross validation" and util.to_int(self.value.folds) is not None)
            )
        )

    def get_features(self, all_columns):
        return [c for c in all_columns if c not in (self.value.exclude_features or []) and c != self.value.target] if all_columns is not None else None

    def set_target(self, target):
        if target in (self.value.exclude_features or []):
            Ref(self.fields.exclude_features).set([f for f in (self.value.exclude_features or []) if f != target])
        Ref(self.fields.target).set(target)


task_config_store = ReactiveTaskConfig(TaskConfig())


@dataclass(frozen=True)
class MLTask:
    task_type: Optional[str] = None
    task_config: Optional[TaskConfig] = None


class ReactiveMLTask(solara.lab.Reactive[MLTask]):
    pass


ml_task = ReactiveMLTask(MLTask())


def to_json(obj: MLTask):
    if isinstance(obj, MLTask):
        return {
            "type_ml": {
                "task_type": obj.task_type,
                "task_config": {"type": obj.task_config.__class__.__name__, "data": asdict(obj.task_config)} if obj.task_config else None,
            }
        }


def from_json(dct):
    if "type_ml" in dct:
        task_type = dct["type_ml"]["task_type"]
        task_config = dct["type_ml"]["task_config"]
        if task_config:
            task_config = globals()[task_config["type"]](**task_config["data"])
        res = MLTask(task_type=task_type, task_config=task_config)

        return res
