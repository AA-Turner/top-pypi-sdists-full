from typing import overload
from enum import IntEnum
import datetime
import typing

import QuantConnect
import QuantConnect.Algorithm
import QuantConnect.Lean.Engine.Results.Analysis
import System
import System.Collections.Generic


class ResultsAnalyzer(System.Object):
    """Runs the full suite of backtest diagnostic tests against a single backtest."""

    def __init__(self, result: QuantConnect.Result, algorithm: QuantConnect.Algorithm.QCAlgorithm, language: QuantConnect.Language, logs: typing.Sequence[str]) -> None:
        """
        Initializes a new instance of the ResultsAnalyzer class.
        
        :param result: The backtest result to analyze.
        :param algorithm: The algorithm instance used for history requests and settings.
        :param language: The programming language the algorithm is written in.
        :param logs: The full list of log lines produced by the backtest.
        """
        ...

    def run(self, time_limit_seconds: int = 5, max_failed_analyses: int = 10) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Runs all registered diagnostic checks against the backtest in weight order,
        stopping early when the time limit or maximum failure count is reached.
        
        :param time_limit_seconds: Wall-clock seconds allowed for the full chain before early exit.
        :param max_failed_analyses: Maximum number of failing analyses to collect before stopping; also the max returned.
        :returns: Up to max_failed_analysesQuantConnect.Analysis entries with solutions, ranked by weight.
        """
        ...


class ResultsAnalysisRunParameters(System.Object):
    """
    Bundles all dependencies that a Analyses.BaseResultsAnalysis may need,
    so every analysis shares a single Run(ResultsAnalysisRunContext) entry point.
    """

    @property
    def result(self) -> QuantConnect.Result:
        """The backtest result being analysed."""
        ...

    @property
    def algorithm(self) -> QuantConnect.Algorithm.QCAlgorithm:
        """The algorithm instance used for history requests and API queries."""
        ...

    @property
    def language(self) -> QuantConnect.Language:
        """The programming language the algorithm is written in."""
        ...

    @property
    def logs(self) -> typing.Sequence[str]:
        """The full list of log lines produced by the backtest."""
        ...

    @property
    def equity_curve(self) -> System.Collections.Generic.SortedList[datetime.datetime, float]:
        """Daily equity values for the strategy, keyed by date."""
        ...

    @property
    def benchmark_equity_curve(self) -> System.Collections.Generic.SortedList[datetime.datetime, float]:
        """Daily equity values for the benchmark (SPY), keyed by date."""
        ...

    def __init__(self, result: QuantConnect.Result, algorithm: QuantConnect.Algorithm.QCAlgorithm, language: QuantConnect.Language, logs: typing.Sequence[str], equity_curve: System.Collections.Generic.SortedList[datetime.datetime, float], benchmark_equity_curve: System.Collections.Generic.SortedList[datetime.datetime, float]) -> None:
        """Initializes a new instance of the ResultsAnalysisRunParameters class with the specified dependencies."""
        ...


