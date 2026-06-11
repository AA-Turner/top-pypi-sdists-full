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


class MonteCarloPercentileAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    Block-bootstrap Monte Carlo test: flags strategies whose total return
    is in the top 10 % of simulated outcomes (potentially lucky).
    """

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


class FlatEquityCurveAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """Detects prolonged flat (zero-change) segments in the equity curve."""

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


class PortfolioValueIsNotPositiveAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """Flags backtests whose ending equity is zero or negative."""

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


class PortfolioMarginUsageAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    Detects periods where the portfolio under-utilises available margin
    (3-day SMA of margin usage drops below 50 %).
    """

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


class OrderFillsDuringExtendedMarketHoursAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """Detects order fills that occurred outside regular market hours."""

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


class PerformanceRelativeToBenchmarkAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """Compares the full-period Sharpe ratio of the strategy to the benchmark."""

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


class ExecutionSpeedAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    Detects slow execution by parsing the last log line.
    Benchmark speeds: https://www.quantconnect.com/performance
    """

    @property
    def issue(self) -> str:
        """Gets the description of the slow execution issue."""
        ...

    @property
    def weight(self) -> int:
        """Gets the severity weight for the execution speed analysis."""
        ...

    @overload
    def run(self, parameters: QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalysisRunParameters) -> typing.Sequence[QuantConnect.Analysis]:
        """Runs the execution speed analysis against the provided backtest parameters."""
        ...

    @overload
    def run(self, logs: typing.Sequence[str]) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Parses the backtest logs to determine execution speed and flags backtests that ran slowly.
        
        :param logs: The full list of log lines produced by the backtest.
        :returns: Analysis results flagging slow execution when below 40k data points per second and runtime is at least 10 seconds.
        """
        ...


class ParameterCountAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """Warns when too many numeric parameters are detected in the algorithm."""

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


class StatisticalSignificanceOfDailyReturnsAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    One-sample t-test: tests whether the strategy's excess daily returns
    (over benchmark) have a mean significantly greater than zero.
    Mirrors tests/statistical_significance_of_daily_returns.py.
    """

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


class TakeProfitAndStopLossOrdersAnalysis(QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis):
    """
    Detects TP/SL order pairs where both filled, or where the surviving leg
    was not cancelled when the other filled.
    """

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
    def expected_message_text(self) -> typing.List[str]:
        """
        Gets the message fragments that identify a warm-up period order error.
        
        
        This Property is protected.
        """
        ...

    def solutions(self, language: QuantConnect.Language) -> typing.List[str]:
        """
        Gets solutions suggesting moving orders out of the warm-up period.
        
        
        This Class is protected.
        """
        ...


