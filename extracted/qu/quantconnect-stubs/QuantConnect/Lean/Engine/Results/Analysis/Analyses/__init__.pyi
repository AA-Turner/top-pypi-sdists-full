from typing import overload
from enum import IntEnum
import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Algorithm
import QuantConnect.Lean.Engine.Results.Analysis
import QuantConnect.Lean.Engine.Results.Analysis.Analyses
import QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages
import QuantConnect.Orders
import System
import System.Collections.Generic
import System.Text.RegularExpressions


class BaseResultsAnalysis(System.Object, metaclass=abc.ABCMeta):
    """Abstract base class for all backtest diagnostic tests."""

    @property
    @abc.abstractmethod
    def issue(self) -> str:
        """Gets a short (3–8 word) description of why the analysis was triggered."""
        ...

    @property
    @abc.abstractmethod
    def weight(self) -> int:
        """Gets the severity/impact weight (0–100). Higher values run first and rank higher in results."""
        ...

    @property
    def runs_in_run(self) -> bool:
        """
        Whether this analysis can also run while the backtest is still in progress, against a
        snapshot of the intermediate results. Most analyses read only the result snapshot, so
        this defaults to true. Analyses that need the completed run (runtime errors, equity
        curves, final statistics, completion logs) or that read algorithm state that is not
        safe to access while it runs override this to leave them to the final analysis only.
        """
        ...

    @property
    def is_state_based(self) -> bool:
        """
        Whether this analysis reads the current backtest state (statistics, orders, charts)
        instead of scanning the append-only order event and log streams. When run in-run, it
        runs against the full current state on every run and its findings replace the
        previous ones instead of accumulating.
        """
        ...

    def create_aggregated_response(self, responses: typing.List[QuantConnect.Analysis]) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Filters responses to those with solutions,
        prefixes the class name, and returns a flat list.
        
        
        This Class is protected.
        """
        ...

    @staticmethod
    def format_code(code: str, language: QuantConnect.Language) -> str:
        """
        Formats the specified code string according to the conventions of the given programming language.
        
        
        This Class is protected.
        """
        ...

    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the analysis against all backtest data provided in parameters."""
        ...

    @overload
    def single_response(self, sample: typing.Any, solutions: typing.Sequence[str] = None) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Wraps a single QuantConnect.Analysis in a one-element read-only list.
        
        
        This Class is protected.
        """
        ...

    @overload
    def single_response(self, sample: typing.Any, count: typing.Optional[int], solutions: typing.Sequence[str] = None) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Wraps a single QuantConnect.Analysis in a one-element read-only list.
        
        
        This Class is protected.
        """
        ...


class PerformanceRelativeToBenchmarkAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """Compares the full-period Sharpe ratio of the strategy to the benchmark."""

    @property
    def runs_in_run(self) -> bool:
        """This analysis compares the equity and benchmark curves, which are only built for the final analysis."""
        ...

    @property
    def issue(self) -> str:
        """Gets the description of the underperformance relative to benchmark issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the severity weight for the benchmark comparison analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the performance relative to benchmark analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, backtest_equity: System.Collections.Generic.SortedList[datetime.datetime, float], benchmark_equity: System.Collections.Generic.SortedList[datetime.datetime, float]) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Calculates the Sharpe ratio of the strategy over the full backtest period and compares it to the benchmark.
        
        :param algorithm: The algorithm instance used to obtain the risk-free rate model.
        :param backtest_equity: Daily equity values for the strategy, keyed by date.
        :param benchmark_equity: Daily equity values for the benchmark (SPY), keyed by date.
        :returns: Analysis results when the strategy's Sharpe ratio is lower than the benchmark's.
        """
        ...


class ParameterCountAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """Warns when too many numeric parameters are detected in the algorithm."""

    @property
    def runs_in_run(self) -> bool:
        """
        This analysis reads the algorithm's parameters, and its overfitting-risk warning is only
        meaningful for the completed run.
        """
        ...

    @property
    def issue(self) -> str:
        """Gets the description of the excessive parameter count issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the severity weight for the parameter count analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the parameter count analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, language: QuantConnect.Language) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Counts the algorithm's parameters and flags the backtest when more than 10 are detected.
        
        :param algorithm: The algorithm instance whose parameters are inspected.
        :param language: The programming language the algorithm is written in.
        :returns: Analysis results when the parameter count exceeds the threshold.
        """
        ...


class PortfolioValueIsNotPositiveAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """Flags backtests whose ending equity is zero or negative."""

    @property
    def is_state_based(self) -> bool:
        """
        This analysis reads the current portfolio statistics instead of scanning the order event
        and log streams, so its in-run findings are replaced on every run.
        """
        ...

    @property
    def issue(self) -> str:
        """Gets the description of the non-positive portfolio equity issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the severity weight for this portfolio value analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the portfolio value positivity analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, result: QuantConnect.Result) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Checks whether the backtest's ending equity is positive.
        
        :param result: The backtest result containing portfolio statistics.
        :returns: Analysis results flagging the issue when ending equity is zero or negative.
        """
        ...


class StaleOrderFillsAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """Detects orders filled at stale (outdated) prices."""

    @property
    def issue(self) -> str:
        """Gets the description of the stale order fill issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the severity weight for this stale fills analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the stale order fills analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, order_events: typing.Sequence[QuantConnect.Orders.OrderEvent], language: QuantConnect.Language) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Searches order events for fill messages that contain a stale-price warning.
        
        :param order_events: The list of order events from the backtest result.
        :param language: The programming language the algorithm is written in.
        :returns: Analysis results when stale fill events are detected.
        """
        ...


class FlatEquityCurveAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """Detects prolonged flat (zero-change) segments in the equity curve."""

    @property
    def runs_in_run(self) -> bool:
        """This analysis scans the equity curve, which is only built for the final analysis."""
        ...

    @property
    def issue(self) -> str:
        """Gets the description of the flat equity curve issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the severity weight for the flat equity curve analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the flat equity curve analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, equity_curve: System.Collections.Generic.SortedList[datetime.datetime, float]) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Scans the equity curve for consecutive flat (unchanged) segments.
        
        :param equity_curve: Daily equity values from the backtest, keyed by date.
        :returns: Analysis results describing any detected flat segments.
        """
        ...


class TakeProfitAndStopLossOrdersAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    Detects TP/SL order pairs where both filled, or where the surviving leg
    was not cancelled when the other filled.
    """

    @property
    def is_state_based(self) -> bool:
        """
        This analysis reads the current orders collection instead of scanning the order event
        and log streams, so its in-run findings are replaced on every run.
        """
        ...

    @property
    def issue(self) -> str:
        """Gets the description of the TP/SL order handling issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the severity weight for this TP/SL orders analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the take-profit and stop-loss orders analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, orders: System.Collections.Generic.ICollection[QuantConnect.Orders.Order], language: QuantConnect.Language) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Groups orders into TP/SL pairs by symbol, quantity, and creation time, then
        delegates to sub-analyses that check for both-filled and dangling-order scenarios.
        
        :param orders: All orders from the backtest result.
        :param language: The programming language the algorithm is written in.
        :returns: Aggregated analysis results from all sub-analyses that detected issues.
        """
        ...


class InsightsEmittedForDelistedSecuritiesAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects the QC warning about emitting insights for delisted securities."""

    @property
    def issue(self) -> str:
        """Description of the delisted-security insight emission issue detected by this analysis."""
        ...

    @property
    def weight(self) -> int:
        """Relative weight indicating the severity of emitting insights for delisted securities."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Log messages indicating that insights were emitted for delisted securities.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Returns suggested solutions for avoiding insight emissions on delisted securities.
        
        
        This Class is protected.
        """
        ...


class StatisticalSignificanceOfDailyReturnsAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    One-sample t-test: tests whether the strategy's excess daily returns
    (over benchmark) have a mean significantly greater than zero.
    Mirrors tests/statistical_significance_of_daily_returns.py.
    """

    @property
    def runs_in_run(self) -> bool:
        """This analysis compares the equity and benchmark curves, which are only built for the final analysis."""
        ...

    @property
    def issue(self) -> str:
        """Gets the description of the statistical insignificance issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the severity weight for this statistical significance analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the statistical significance of daily returns analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, backtest_equity: System.Collections.Generic.SortedList[datetime.datetime, float], benchmark_equity: System.Collections.Generic.SortedList[datetime.datetime, float]) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Computes excess daily returns (strategy minus benchmark) and applies a one-tailed
        one-sample t-test at the 5 % significance level.
        
        :param backtest_equity: Daily equity values for the strategy, keyed by date.
        :param benchmark_equity: Daily equity values for the benchmark (SPY), keyed by date.
        :returns: Analysis results when the strategy's excess returns are not statistically significant.
        """
        ...


class OrderFillsDuringExtendedMarketHoursAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """Detects order fills that occurred outside regular market hours."""

    @property
    def runs_in_run(self) -> bool:
        """This analysis reads the algorithm's securities, which are not safe to access while it runs."""
        ...

    @property
    def issue(self) -> str:
        """Gets the description of the extended market hours fill issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the severity weight for the extended market hours analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the extended market hours order fill analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, order_events: typing.Sequence[QuantConnect.Orders.OrderEvent], language: QuantConnect.Language) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Iterates filled order events and flags those that occurred when the exchange was not open.
        
        :param algorithm: The algorithm instance used to check market-open status at the fill time.
        :param order_events: The list of order events from the backtest result.
        :param language: The programming language the algorithm is written in.
        :returns: Analysis results when fills outside regular hours are detected.
        """
        ...


class MonteCarloPercentileAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    Block-bootstrap Monte Carlo test: flags strategies whose total return
    is in the top 10 % of simulated outcomes (potentially lucky).
    """

    @property
    def runs_in_run(self) -> bool:
        """This analysis runs simulations over the equity curve, which is only built for the final analysis."""
        ...

    @property
    def issue(self) -> str:
        """Gets the description of the overly optimistic equity curve issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the severity weight for the Monte Carlo percentile analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the Monte Carlo percentile analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, backtest_equity: System.Collections.Generic.SortedList[datetime.datetime, float]) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Runs the Monte Carlo percentile test against the given equity curve.
        
        :param backtest_equity: Daily equity values from the backtest, keyed by date.
        :returns: Analysis results indicating whether the strategy's return is suspiciously high.
        """
        ...


class MarginCallsAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects margin-call events in the backtest logs."""

    @property
    def issue(self) -> str:
        """Description of the margin-call issue detected by this analysis."""
        ...

    @property
    def weight(self) -> int:
        """Relative weight indicating the severity of margin-call events."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Log messages indicating that a margin-call order was executed.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Returns suggested solutions for preventing or handling margin calls.
        
        
        This Class is protected.
        """
        ...


class PortfolioMarginUsageAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    Detects periods where the portfolio under-utilises available margin
    (3-day SMA of margin usage drops below 50 %).
    """

    @property
    def is_state_based(self) -> bool:
        """
        This analysis reads the current margin chart instead of scanning the order event
        and log streams, so its in-run findings are replaced on every run.
        """
        ...

    @property
    def issue(self) -> str:
        """Gets the description of the detected margin under-utilisation issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the severity weight for this margin usage analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the portfolio margin usage analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, backtest_result: QuantConnect.Result) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Reads the "Portfolio Margin" chart from the backtest result and counts trading days
        where the 3-day SMA of total margin usage drops below 50%.
        
        :param backtest_result: The backtest result whose charts are inspected.
        :returns: Analysis results when any such days are detected.
        """
        ...


class CrisisEventsAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    Compares the strategy's Sharpe ratio to the benchmark's across known
    crisis / market-stress periods.
    Source: https://github.com/QuantConnect/Lean/blob/master/Report/Crisis.cs
    """

    @property
    def runs_in_run(self) -> bool:
        """This analysis compares the equity and benchmark curves, which are only built for the final analysis."""
        ...

    @property
    def issue(self) -> str:
        """Gets the description indicating that the strategy underperformed the benchmark during crisis events."""
        ...

    @property
    def weight(self) -> int:
        """Gets the severity weight for crisis event underperformance analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the crisis events analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, backtest_equity: System.Collections.Generic.SortedList[datetime.datetime, float], benchmark_equity: System.Collections.Generic.SortedList[datetime.datetime, float]) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Compares the strategy's Sharpe ratio to the benchmark's across all crisis events
        that fall entirely within the backtest period.
        
        :param algorithm: The algorithm instance used to obtain the risk-free rate model.
        :param backtest_equity: Daily equity values for the strategy, keyed by date.
        :param benchmark_equity: Daily equity values for the benchmark (SPY), keyed by date.
        :returns: Analysis results listing crisis periods where the strategy underperformed the benchmark.
        """
        ...


class SingleTimeLoopTimeoutRuntimeErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    Detects algorithms terminated by an Isolator time limit, inspecting the error
    message for known text fragments. The runtime error is read from the result state, falling
    back to the "Runtime Error:" log line for results that carry no state. It covers a single
    time loop exceeding the per-loop limit ("Algorithm took longer than N minutes on a single
    time loop"), the whole run outliving the maximum allowed wall-clock time ("Execution
    Security Error: Operation timed out - N minutes max", "Failed to complete algorithm within
    N seconds"), and code still running once the shutdown grace period expires after a stop
    request ("Operation was canceled").
    """

    @property
    def runs_in_run(self) -> bool:
        """A timeout runtime error terminates the backtest, so there is no in-progress run to analyze."""
        ...

    @property
    def issue(self) -> str:
        """Gets the description of the timeout issue."""
        ...

    @property
    def weight(self) -> int:
        """
        Gets the severity weight for this analysis. A timeout is a fatal error that terminated
        the run, so it ranks above every non-fatal finding.
        """
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the runtime error analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, state: System.Collections.Generic.IDictionary[str, str], logs: typing.Sequence[str], language: QuantConnect.Language) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Runs the runtime error analysis against the algorithm state and logs.
        
        :param state: The algorithm state of the result, holding the runtime error message if any.
        :param logs: The full list of log lines produced by the backtest.
        :param language: The programming language the algorithm is written in.
        :returns: A single response with the matched error message and solutions, or without them when the error is not found.
        """
        ...


class AlgorithmSpeedAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    Tracks the algorithm's execution speed from the throughput and progress metrics accumulated
    by AlgorithmSpeedTracker, reporting slow processing speed, a long projected
    remaining runtime, degrading throughput, and history-request-dominated data loads.
    It runs periodically while the backtest is in progress, so the user can decide to stop a
    slow backtest early, and again on the final analysis against the whole run's metrics.
    When the tracked metrics cannot measure the processing speed, the engine's completion log
    line is parsed for the whole-run average rate as a fallback; the line only exists once the
    backtest ends, so the fallback can only fire on the final analysis.
    Benchmark speeds: https://www.quantconnect.com/performance
    """

    SLOW_DATA_POINTS_PER_SECOND: int = ...
    """The data points per second under which execution is reported as slow, from the platform benchmarks."""

    MINIMUM_COMPLETED_RUNTIME_SECONDS: int = 10
    """
    The minimum runtime a completed backtest must have for its whole-run average rate,
    parsed from the completion log line, to be worth reporting as slow.
    """

    DEGRADATION_RATIO: float = 0.5
    """The recent-to-initial throughput ratio under which throughput is reported as degrading."""

    HIGH_HISTORY_DATA_POINTS_SHARE: float = 0.5
    """
    The share of recently processed data points served by the history provider
    over which the data load is reported as history-request dominated.
    """

    MINIMUM_RECENT_HISTORY_DATA_POINTS: int = ...
    """
    The minimum number of history data points in the recent window for the
    history-request load to be worth reporting.
    """

    MINIMUM_SAMPLED_SPAN: datetime.timedelta = ...
    """
    The minimum wall-clock span the metrics must cover before any finding is reported,
    so early warm-up noise doesn't produce false positives.
    """

    LONG_PROJECTED_REMAINING_TIME: datetime.timedelta = ...
    """The projected remaining runtime over which the backtest is reported as long-running."""

    SLOW_EXECUTION_NAME: str = "SlowExecution"
    """The name of the slow execution sub-finding."""

    LONG_PROJECTED_RUNTIME_NAME: str = "LongProjectedRuntime"
    """The name of the long projected runtime sub-finding."""

    THROUGHPUT_DEGRADATION_NAME: str = "ThroughputDegradation"
    """The name of the degrading throughput sub-finding."""

    HISTORY_REQUEST_LOAD_NAME: str = "HistoryRequestLoad"
    """The name of the history-request load sub-finding."""

    @property
    def is_state_based(self) -> bool:
        """
        This analysis reads the current speed metrics instead of scanning the order event
        and log streams, so its in-run findings are replaced on every run.
        """
        ...

    @property
    def issue(self) -> str:
        """Gets the description of the slow algorithm issue."""
        ...

    @property
    def weight(self) -> int:
        """
        Gets the severity weight for the algorithm speed analysis. High enough to run before the
        order-response error analyses in the in-run chain: this analysis drives the user's decision
        to stop a slow backtest, and it is one of the cheapest in the set, so it should not be the
        one skipped when the time limit or the failed-analyses cap truncates a run.
        """
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Runs the algorithm speed analysis against the speed metrics tracked for the backtest,
        falling back to the completion log line when they cannot measure the speed.
        """
        ...

    @overload
    def run(self, speed: QuantConnect.Lean.Engine.Results.Analysis.AlgorithmSpeedTracker, logs: typing.Sequence[str] = None) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Runs the algorithm speed analysis against the given speed metrics.
        Each detected condition is reported as its own sub-finding. Every condition must hold for
        both the current recent window and the window as of the previous run, so a single noisy
        sample doesn't flag or clear a finding.
        When the metrics cannot measure the processing speed — the tracker isn't wired in, the
        backtest finished before it got enough samples, or the data point counters aren't fed —
        the completion log line's whole-run average is used to detect slow execution instead.
        
        :param speed: The speed metrics tracked for the running backtest, or null when not tracked.
        :param logs: The log lines to search for the completion line, or null when not available.
        :returns: The failed sub-findings, or empty when no speed condition failed or none could be measured.
        """
        ...


class OrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis, metaclass=abc.ABCMeta):
    """
    Abstract base class for analyses that detect specific order-response errors
    by inspecting invalid order events for known message text fragments.
    """

    def get_matching_order_events_messages(self, order_events: typing.List[QuantConnect.Orders.OrderEvent]) -> typing.Sequence[str]:
        """
        Filters order_events to those with OrderStatus.INVALID status
        whose message contains all MessageAnalysis.expected_message_text fragments.
        
        
        This Class is protected.
        
        :param order_events: The order events to inspect.
        :returns: An enumerable of matching message strings.
        """
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        ...

    @overload
    def run(self, order_events: typing.List[QuantConnect.Orders.OrderEvent], language: QuantConnect.Language) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Runs the analysis against a list of order events, extracting matching invalid-event messages
        and delegating to the message-based MessageAnalysis.run(IReadOnlyList{string}, Language) overload.
        
        :param order_events: The order events from the backtest result.
        :param language: The programming language the algorithm is written in.
        :returns: Analysis results when any matching order response errors are found.
        """
        ...


class BrokerageModelRefusedToUpdateOrderOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.OrderResponseErrorAnalysis):
    """Detects brokerage-model-refused-to-update-order errors."""

    @property
    def issue(self) -> str:
        """Gets a description of the brokerage-refused-to-update-order issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragment that identifies a brokerage update-order refusal.
        
        
        This Property is protected.
        """
        ...

    def run(self, order_events: typing.List[QuantConnect.Orders.OrderEvent], language: QuantConnect.Language) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Filters order events for brokerage-refused-to-update errors and dispatches the matched
        messages to each per-brokerage sub-analysis to surface specific solutions.
        
        :param order_events: The order events from the backtest result.
        :param language: The programming language the algorithm is written in.
        :returns: Aggregated analysis results from all sub-analyses that detected a matching message.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Returns an empty list because solutions are provided by the per-brokerage sub-analyses.
        
        
        This Class is protected.
        """
        ...


class OrderQuantityZeroOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects zero-quantity order errors."""

    @property
    def issue(self) -> str:
        """Gets a description of the zero order quantity issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragments that identify a zero-quantity order error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions for ensuring non-zero order quantities or increasing starting cash.
        
        
        This Class is protected.
        """
        ...


class AlgorithmWarmingUpOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """
    Detects orders placed during the algorithm warm-up period.
    Error code: OrderResponseErrorCode.ALGORITHM_WARMING_UP (-24)
    """

    @property
    def issue(self) -> str:
        """Gets a description of the warm-up period ordering violation."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_pattern(self) -> System.Text.RegularExpressions.Regex:
        """
        Gets the pattern that identifies a warm-up period order error. The method names are
        language-formatted in the message (OnWarmupFinished for C#, on_warmup_finished for
        Python), so a pattern is used instead of text fragments to match both.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions suggesting moving orders out of the warm-up period.
        
        
        This Class is protected.
        """
        ...


class SecurityPriceZeroOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects orders placed when the security price is zero."""

    @property
    def issue(self) -> str:
        """Gets a description of the zero security price ordering issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragment that identifies a zero security price error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions for seeding initial prices or investigating missing data.
        
        
        This Class is protected.
        """
        ...


class OrderQuantityLessThanLotSizeOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects orders with quantity below the security's lot size."""

    @property
    def issue(self) -> str:
        """Gets a description of the order quantity below lot size issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragments that identify a quantity-less-than-lot-size error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions for validating order quantity against the lot size.
        
        
        This Class is protected.
        """
        ...


class MarketOnOpenNotAllowedDuringRegularHoursOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects MarketOnOpen orders submitted during regular trading hours."""

    @property
    def issue(self) -> str:
        """Gets a description of the market-on-open during regular hours issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragment that identifies a market-on-open during regular hours error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions for placing market-on-open orders outside regular hours.
        
        
        This Class is protected.
        """
        ...


class ExceededMaximumOrdersOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects the "exceeded maximum orders" error."""

    @property
    def issue(self) -> str:
        """Gets a description of the exceeded maximum orders issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragments that identify the exceeded-maximum-orders error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions for upgrading the account tier or reducing order count.
        
        
        This Class is protected.
        """
        ...


class ExchangeNotOpenOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    Detects "exchange not open" order response errors.
    Returns the first sub-test that fires.
    """

    @property
    def issue(self) -> str:
        """Gets a description of the exchange-not-open ordering issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the exchange not open analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, logs: typing.Sequence[str], language: QuantConnect.Language) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Runs the first sub-analysis that produces a match, covering exercise-while-closed
        and MOC-on-Futures scenarios.
        
        :param logs: The log lines produced by the backtest.
        :param language: The programming language the algorithm is written in.
        :returns: The results of the first matching sub-analysis, or a single empty response when none match.
        """
        ...


class InsufficientBuyingPowerOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.OrderResponseErrorAnalysis):
    """Detects insufficient-buying-power order rejections."""

    @property
    def issue(self) -> str:
        """Gets a description of the insufficient buying power issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragment that identifies an insufficient buying power error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions for ensuring sufficient margin or adjusting the buying power buffer.
        
        
        This Class is protected.
        """
        ...


class NonTradableSecurityOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects orders placed for non-tradable securities."""

    @property
    def issue(self) -> str:
        """Gets a description of the non-tradable security ordering issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragments that identify a non-tradable security error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions for checking the IsTradable flag before placing orders.
        
        
        This Class is protected.
        """
        ...


class UnsupportedOptionExerciseQuantityAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects attempts to exercise more Option contracts than are currently held in the portfolio."""

    @property
    def issue(self) -> str:
        """Gets a description of the excess-quantity option exercise issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragments that identify an excess-quantity option exercise error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions for capping the exercise quantity to what is actually held.
        
        
        This Class is protected.
        """
        ...


class ForexConversionRateZeroOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects zero Forex conversion rate errors."""

    @property
    def issue(self) -> str:
        """Gets a description of the zero Forex conversion rate issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragments that identify a zero conversion rate error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions suggesting investigation of missing data.
        
        
        This Class is protected.
        """
        ...


class ExceedsShortableQuantityOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """Detects orders rejected because they exceed the available shortable quantity."""

    @property
    def issue(self) -> str:
        """Gets a description of the exceeded shortable quantity issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the exceeds shortable quantity analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, order_events: typing.Sequence[QuantConnect.Orders.OrderEvent], language: QuantConnect.Language) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Searches order events for exceeds-shortable-quantity rejection messages.
        
        :param order_events: The order events from the backtest result.
        :param language: The programming language the algorithm is written in.
        :returns: Analysis results when shortable quantity violations are detected.
        """
        ...


class EuropeanOptionNotExpiredOnExerciseOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """
    Detects attempts to exercise a European option before expiry.
    Error code: OrderResponseErrorCode.EUROPEAN_OPTION_NOT_EXPIRED_ON_EXERCISE (-33)
    """

    @property
    def issue(self) -> str:
        """Gets a description of the premature European option exercise issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragments that identify a European option early exercise error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions for verifying option style and expiry before exercising.
        
        
        This Class is protected.
        """
        ...


class MarketOnCloseOrderTooLateOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects MarketOnClose orders submitted too early in the day."""

    @property
    def issue(self) -> str:
        """Gets a description of the MOC order submitted too late issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragments that identify a MOC order timing error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions for adjusting MOC order timing or the submission time buffer.
        
        
        This Class is protected.
        """
        ...


class BrokerageModelRefusedToSubmitOrderOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.OrderResponseErrorAnalysis):
    """
    Detects brokerage-model-refused-to-submit-order errors and dispatches to
    per-message sub-tests to surface specific solutions.
    """

    @property
    def issue(self) -> str:
        """Gets a description of the brokerage-refused-to-submit-order issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragment that identifies a brokerage submit-order refusal.
        
        
        This Property is protected.
        """
        ...

    def run(self, order_events: typing.List[QuantConnect.Orders.OrderEvent], language: QuantConnect.Language) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Filters order events for brokerage-refused-to-submit errors and dispatches the matched
        messages to each per-brokerage sub-analysis to surface specific solutions.
        
        :param order_events: The order events from the backtest result.
        :param language: The programming language the algorithm is written in.
        :returns: Aggregated analysis results from all sub-analyses that detected a matching message.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Returns an empty list because solutions are provided by the per-brokerage sub-analyses.
        
        
        This Class is protected.
        """
        ...


class OptionOrderOnStockSplitOrderResponseErrorAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects Option orders placed when the underlying stock had a split."""

    @property
    def issue(self) -> str:
        """Gets a description of the option order during stock split issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragment that identifies an option-order-on-stock-split error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions for checking underlying split events before placing option orders.
        
        
        This Class is protected.
        """
        ...


class UnsupportedOptionShortPositionExerciseAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.Messages.MessageAnalysis):
    """Detects attempts to exercise an Option contract while holding a short position."""

    @property
    def issue(self) -> str:
        """Gets a description of the short-position option exercise issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the priority weight for this analysis."""
        ...

    @property
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragments that identify a short-position option exercise error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions for verifying the position direction before exercising an Option contract.
        
        
        This Class is protected.
        """
        ...


