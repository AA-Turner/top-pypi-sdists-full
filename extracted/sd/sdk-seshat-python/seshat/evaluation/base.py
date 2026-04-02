import os
from typing import List, Callable

from seshat.data_class import SFrame
from seshat.evaluation.evaluator import Evaluator
from seshat.general.exceptions import InvalidArgumentsError


class Evaluation:
    evaluators: List[Evaluator]
    test_sf: SFrame
    prediction_sf: SFrame
    model_func: Callable
    report_path: str

    def __init__(self, evaluators, report_path):
        self.evaluators = evaluators
        self.report_path = report_path

    def __call__(self, test_sf, model_func=None, **prediction_kwargs):
        if not prediction_kwargs and not model_func:
            raise InvalidArgumentsError(
                "Must provide either prediction_kwargs or mode_func"
            )
        elif not prediction_kwargs:
            prediction_kwargs = model_func(test_sf)

        report = {}
        for evaluator in self.evaluators:
            report |= evaluator(test_sf=test_sf, **prediction_kwargs)
        self.write_report(report, self.report_path)
        return report

    @staticmethod
    def write_report(report, report_path):
        report_content = ""
        for metric, result in report.items():
            report_content += f"Metric {metric}: {result}\n"
        directory = os.path.dirname(report_path)
        os.makedirs(directory, exist_ok=True)
        with open(report_path, "w") as file:
            file.write(report_content)
