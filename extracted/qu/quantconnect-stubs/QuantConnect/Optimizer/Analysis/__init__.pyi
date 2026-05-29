from typing import overload
from enum import IntEnum
import typing

import QuantConnect.Optimizer
import QuantConnect.Optimizer.Analysis
import QuantConnect.Optimizer.Parameters
import System


class OptimizationAnalysisRunParameters(System.Object):
    """Bundles the inputs to the optimization analyzer: per-backtest metrics and the parameter grid spec."""

    @property
    def completed_backtests(self) -> typing.Sequence[QuantConnect.Optimizer.OptimizationBacktestMetrics]:
        """Completed backtests from the optimization, already reduced to the metrics the analyzer reads."""
        ...

    @property
    def optimization_parameters(self) -> typing.Sequence[QuantConnect.Optimizer.Parameters.OptimizationParameter]:
        """The optimization parameter grid spec."""
        ...

    def __init__(self, completed_backtests: typing.Sequence[QuantConnect.Optimizer.OptimizationBacktestMetrics], optimization_parameters: typing.Sequence[QuantConnect.Optimizer.Parameters.OptimizationParameter]) -> None:
        """
        Initializes a new instance of the OptimizationAnalysisRunParameters class.
        
        :param completed_backtests: The completed backtest metrics.
        :param optimization_parameters: The parameter grid spec.
        """
        ...


class OptimizationAnalyzer(System.Object):
    """Builds an aggregate OptimizationAnalysis from a completed optimization's per-backtest metrics; optimization-side analogue of the Engine ResultsAnalyzer."""

    def run(self, parameters: QuantConnect.Optimizer.Analysis.OptimizationAnalysisRunParameters) -> QuantConnect.Optimizer.OptimizationAnalysis:
        """
        Runs the full optimization-analysis pipeline.
        
        :param parameters: Completed backtest metrics plus the parameter grid spec.
        :returns: The populated OptimizationAnalysis, or null when no usable backtests remain.
        """
        ...


