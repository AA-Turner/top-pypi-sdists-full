from typing import overload
from enum import IntEnum
import abc
import datetime
import typing

import QuantConnect.Optimizer
import QuantConnect.Optimizer.Objectives
import QuantConnect.Optimizer.Parameters
import QuantConnect.Optimizer.Strategies
import QuantConnect.Packets
import QuantConnect.Statistics
import System
import System.Collections.Concurrent
import System.Collections.Generic

QuantConnect_Optimizer__EventContainer_Callable = typing.TypeVar("QuantConnect_Optimizer__EventContainer_Callable")
QuantConnect_Optimizer__EventContainer_ReturnType = typing.TypeVar("QuantConnect_Optimizer__EventContainer_ReturnType")


class SharpeSummary(System.Object):
    """Sharpe ratio statistics across all used backtests in an optimization."""

    @property
    def mean(self) -> float:
        """Arithmetic mean of Sharpe ratios."""
        ...

    @mean.setter
    def mean(self, value: float) -> None:
        ...

    @property
    def std_dev(self) -> float:
        """Sample standard deviation of Sharpe ratios."""
        ...

    @std_dev.setter
    def std_dev(self, value: float) -> None:
        ...

    @property
    def min(self) -> float:
        """Minimum Sharpe ratio observed."""
        ...

    @min.setter
    def min(self, value: float) -> None:
        ...

    @property
    def max(self) -> float:
        """Maximum Sharpe ratio observed."""
        ...

    @max.setter
    def max(self, value: float) -> None:
        ...

    @property
    def median(self) -> float:
        """Median Sharpe ratio."""
        ...

    @median.setter
    def median(self, value: float) -> None:
        ...


class BacktestSummary(System.Object):
    """Per-backtest identity + Sharpe ratio shared by all optimization-analysis records that describe one backtest."""

    @property
    def backtest_id(self) -> str:
        """The backtest id; kept for programmatic access but not serialized into the analysis JSON."""
        ...

    @backtest_id.setter
    def backtest_id(self, value: str) -> None:
        ...

    @property
    def parameters(self) -> typing.Dict[str, float]:
        """Parameter values the backtest was run with."""
        ...

    @parameters.setter
    def parameters(self, value: typing.Dict[str, float]) -> None:
        ...

    @property
    def sharpe_ratio(self) -> float:
        """The backtest's Sharpe ratio."""
        ...

    @sharpe_ratio.setter
    def sharpe_ratio(self, value: float) -> None:
        ...


class FailedBacktestSummary(System.Object):
    """Breakdown of backtests in an optimization that produced zero orders."""

    @property
    def zero_order_count(self) -> int:
        """Total number of backtests that produced zero orders."""
        ...

    @zero_order_count.setter
    def zero_order_count(self, value: int) -> None:
        ...

    @property
    def inspected_count(self) -> int:
        """Number of zero-order backtests inspected for analysis tags; may be smaller than zero_order_count."""
        ...

    @inspected_count.setter
    def inspected_count(self, value: int) -> None:
        ...

    @property
    def analysis_name_counts(self) -> typing.Dict[str, int]:
        """Map of analysis-tag name to the number of inspected backtests carrying that tag."""
        ...

    @analysis_name_counts.setter
    def analysis_name_counts(self, value: typing.Dict[str, int]) -> None:
        ...


class LinearSegment(System.Object):
    """One linear piece of a piecewise interpolant on <x_lo, x_hi>, evaluated as y(x) = A + B * (x - XLo)."""

    @property
    def x_lo(self) -> float:
        """Lower bound of this segment."""
        ...

    @x_lo.setter
    def x_lo(self, value: float) -> None:
        ...

    @property
    def x_hi(self) -> float:
        """Upper bound of this segment."""
        ...

    @x_hi.setter
    def x_hi(self, value: float) -> None:
        ...

    @property
    def a(self) -> float:
        """Sharpe ratio at x_lo."""
        ...

    @a.setter
    def a(self, value: float) -> None:
        ...

    @property
    def b(self) -> float:
        """Slope through the segment."""
        ...

    @b.setter
    def b(self, value: float) -> None:
        ...


class SliceFit(System.Object):
    """One-dimensional cross-section of the parameter space: one parameter varies while every other is held constant."""

    @property
    def fixed_parameters(self) -> typing.Dict[str, float]:
        """Values of the other parameters held constant for this slice."""
        ...

    @fixed_parameters.setter
    def fixed_parameters(self, value: typing.Dict[str, float]) -> None:
        ...

    @property
    def sharpe_range(self) -> float:
        """Max Sharpe minus min Sharpe across this slice."""
        ...

    @sharpe_range.setter
    def sharpe_range(self, value: float) -> None:
        ...

    @property
    def max_abs_derivative(self) -> float:
        """Maximum absolute slope across this slice's linear segments."""
        ...

    @max_abs_derivative.setter
    def max_abs_derivative(self, value: float) -> None:
        ...

    @property
    def segments(self) -> typing.Sequence[QuantConnect.Optimizer.LinearSegment]:
        """Piecewise linear pieces of the fit; one per adjacent pair of grid points."""
        ...

    @segments.setter
    def segments(self, value: typing.Sequence[QuantConnect.Optimizer.LinearSegment]) -> None:
        ...


class ParameterReport(System.Object):
    """Sensitivity report for a single optimized parameter."""

    @property
    def name(self) -> str:
        """Parameter name."""
        ...

    @name.setter
    def name(self, value: str) -> None:
        ...

    @property
    def searched_min(self) -> float:
        """Lower bound of the parameter sweep."""
        ...

    @searched_min.setter
    def searched_min(self, value: float) -> None:
        ...

    @property
    def searched_max(self) -> float:
        """Upper bound of the parameter sweep."""
        ...

    @searched_max.setter
    def searched_max(self, value: float) -> None:
        ...

    @property
    def step(self) -> typing.Optional[float]:
        """Sweep step size; null when not provided in the optimization configuration."""
        ...

    @step.setter
    def step(self, value: typing.Optional[float]) -> None:
        ...

    @property
    def mean_within_slice_sharpe_range(self) -> float:
        """Mean Sharpe range (max - min) across every 1-D slice."""
        ...

    @mean_within_slice_sharpe_range.setter
    def mean_within_slice_sharpe_range(self, value: float) -> None:
        ...

    @property
    def max_within_slice_sharpe_range(self) -> float:
        """Maximum Sharpe range (max - min) across every 1-D slice."""
        ...

    @max_within_slice_sharpe_range.setter
    def max_within_slice_sharpe_range(self, value: float) -> None:
        ...

    @property
    def max_abs_derivative_per_step(self) -> float:
        """Worst-case Sharpe change between two adjacent grid values, scaled by step."""
        ...

    @max_abs_derivative_per_step.setter
    def max_abs_derivative_per_step(self, value: float) -> None:
        ...

    @property
    def best_value(self) -> float:
        """This parameter's value at the best backtest."""
        ...

    @best_value.setter
    def best_value(self, value: float) -> None:
        ...

    @property
    def best_at_searched_edge(self) -> bool:
        """True when best_value lies within half a step of searched_min or searched_max."""
        ...

    @best_at_searched_edge.setter
    def best_at_searched_edge(self, value: bool) -> None:
        ...

    @property
    def slices(self) -> typing.Sequence[QuantConnect.Optimizer.SliceFit]:
        """One-dimensional slices used for the sensitivity analysis."""
        ...

    @slices.setter
    def slices(self, value: typing.Sequence[QuantConnect.Optimizer.SliceFit]) -> None:
        ...


class Cluster(System.Object):
    """One k-means cluster of backtests in standardized parameter space."""

    @property
    def centroid(self) -> typing.Dict[str, float]:
        """Cluster centroid in original parameter units."""
        ...

    @centroid.setter
    def centroid(self, value: typing.Dict[str, float]) -> None:
        ...

    @property
    def member_count(self) -> int:
        """Number of backtests assigned to this cluster."""
        ...

    @member_count.setter
    def member_count(self, value: int) -> None:
        ...

    @property
    def sharpe_mean(self) -> float:
        """Mean Sharpe ratio across the cluster's members."""
        ...

    @sharpe_mean.setter
    def sharpe_mean(self, value: float) -> None:
        ...

    @property
    def sharpe_std_dev(self) -> float:
        """Sample standard deviation of Sharpe ratios within this cluster."""
        ...

    @sharpe_std_dev.setter
    def sharpe_std_dev(self, value: float) -> None:
        ...

    @property
    def sharpe_min(self) -> float:
        """Minimum Sharpe ratio within this cluster."""
        ...

    @sharpe_min.setter
    def sharpe_min(self, value: float) -> None:
        ...

    @property
    def sharpe_max(self) -> float:
        """Maximum Sharpe ratio within this cluster."""
        ...

    @sharpe_max.setter
    def sharpe_max(self, value: float) -> None:
        ...


class Mode(QuantConnect.Optimizer.BacktestSummary):
    """A local maximum of the Sharpe surface on the parameter grid; strictly greater than every face-neighbor's Sharpe."""

    @property
    def neighbor_count(self) -> int:
        """Number of face-neighbors this backtest was compared against."""
        ...

    @neighbor_count.setter
    def neighbor_count(self, value: int) -> None:
        ...


class OptimizationAnalysis(System.Object):
    """Aggregate diagnostic produced by analyzing a completed optimization."""

    @property
    def interpretation(self) -> str:
        """Natural-language interpretation of the analysis produced by a downstream AI consumer; empty until populated."""
        ...

    @interpretation.setter
    def interpretation(self, value: str) -> None:
        ...

    @property
    def backtest_count_total(self) -> int:
        """Total number of backtests observed, including failures."""
        ...

    @backtest_count_total.setter
    def backtest_count_total(self, value: int) -> None:
        ...

    @property
    def backtest_count_used(self) -> int:
        """Number of backtests used in the analysis after filtering failures."""
        ...

    @backtest_count_used.setter
    def backtest_count_used(self, value: int) -> None:
        ...

    @property
    def overall_sharpe(self) -> QuantConnect.Optimizer.SharpeSummary:
        """Sharpe ratio statistics across all used backtests."""
        ...

    @overall_sharpe.setter
    def overall_sharpe(self, value: QuantConnect.Optimizer.SharpeSummary) -> None:
        ...

    @property
    def best(self) -> QuantConnect.Optimizer.BacktestSummary:
        """The best-performing backtest (argmax of Sharpe)."""
        ...

    @best.setter
    def best(self, value: QuantConnect.Optimizer.BacktestSummary) -> None:
        ...

    @property
    def parameters(self) -> typing.Sequence[QuantConnect.Optimizer.ParameterReport]:
        """Per-parameter sensitivity report; one entry per optimized parameter."""
        ...

    @parameters.setter
    def parameters(self, value: typing.Sequence[QuantConnect.Optimizer.ParameterReport]) -> None:
        ...

    @property
    def clusters(self) -> typing.Sequence[QuantConnect.Optimizer.Cluster]:
        """K-means clusters in standardized parameter space, ordered by mean Sharpe descending."""
        ...

    @clusters.setter
    def clusters(self, value: typing.Sequence[QuantConnect.Optimizer.Cluster]) -> None:
        ...

    @property
    def modes(self) -> typing.Sequence[QuantConnect.Optimizer.Mode]:
        """Local maxima of the Sharpe surface on the parameter grid, ordered by Sharpe descending."""
        ...

    @modes.setter
    def modes(self, value: typing.Sequence[QuantConnect.Optimizer.Mode]) -> None:
        ...

    @property
    def failed_backtests(self) -> QuantConnect.Optimizer.FailedBacktestSummary:
        """Breakdown of zero-order backtests; null when none exist."""
        ...

    @failed_backtests.setter
    def failed_backtests(self, value: QuantConnect.Optimizer.FailedBacktestSummary) -> None:
        ...


class OptimizationResult(System.Object):
    """Defines the result of Lean compute job"""

    INITIAL: QuantConnect.Optimizer.OptimizationResult = ...
    """Corresponds to initial result to drive the optimization strategy"""

    @property
    def backtest_id(self) -> str:
        """The backtest id that generated this result"""
        ...

    @property
    def id(self) -> int:
        """Parameter set Id"""
        ...

    @property
    def json_backtest_result(self) -> str:
        """Json Backtest result"""
        ...

    @property
    def parameter_set(self) -> QuantConnect.Optimizer.Parameters.ParameterSet:
        """The parameter set at which the result was achieved"""
        ...

    @property
    def analysis(self) -> QuantConnect.Optimizer.OptimizationAnalysis:
        """Aggregate diagnostic for the whole optimization; populated only on the final result fired via LeanOptimizer.ended."""
        ...

    @analysis.setter
    def analysis(self, value: QuantConnect.Optimizer.OptimizationAnalysis) -> None:
        ...

    def __init__(self, json_backtest_result: str, parameter_set: QuantConnect.Optimizer.Parameters.ParameterSet, backtest_id: str) -> None:
        """
        Create an instance of OptimizationResult
        
        :param json_backtest_result: Optimization target value for this backtest
        :param parameter_set: Parameter set used in compute job
        :param backtest_id: The backtest id that generated this result
        """
        ...


class OptimizationStatus(IntEnum):
    """The different optimization status"""

    NEW = 0
    """Just created and not running optimization (0)"""

    ABORTED = 1
    """We failed or we were aborted (1)"""

    RUNNING = 2
    """We are running (2)"""

    COMPLETED = 3
    """Optimization job has completed (3)"""


class OptimizationNodePacket(QuantConnect.Packets.Packet):
    """Provide a packet type containing information on the optimization compute job."""

    @property
    def name(self) -> str:
        """The optimization name"""
        ...

    @name.setter
    def name(self, value: str) -> None:
        ...

    @property
    def created(self) -> datetime.datetime:
        """The creation time"""
        ...

    @created.setter
    def created(self, value: datetime.datetime) -> None:
        ...

    @property
    def user_id(self) -> int:
        """User Id placing request"""
        ...

    @user_id.setter
    def user_id(self, value: int) -> None:
        ...

    @property
    def user_token(self) -> str:
        ...

    @user_token.setter
    def user_token(self, value: str) -> None:
        ...

    @property
    def project_id(self) -> int:
        """Project Id of the request"""
        ...

    @project_id.setter
    def project_id(self, value: int) -> None:
        ...

    @property
    def compile_id(self) -> str:
        """Unique compile id of this optimization"""
        ...

    @compile_id.setter
    def compile_id(self, value: str) -> None:
        ...

    @property
    def optimization_id(self) -> str:
        """The unique optimization Id of the request"""
        ...

    @optimization_id.setter
    def optimization_id(self, value: str) -> None:
        ...

    @property
    def organization_id(self) -> str:
        """Organization Id of the request"""
        ...

    @organization_id.setter
    def organization_id(self, value: str) -> None:
        ...

    @property
    def maximum_concurrent_backtests(self) -> int:
        """Limit for the amount of concurrent backtests being run"""
        ...

    @maximum_concurrent_backtests.setter
    def maximum_concurrent_backtests(self, value: int) -> None:
        ...

    @property
    def optimization_strategy(self) -> str:
        """Optimization strategy name"""
        ...

    @optimization_strategy.setter
    def optimization_strategy(self, value: str) -> None:
        ...

    @property
    def criterion(self) -> QuantConnect.Optimizer.Objectives.Target:
        """Objective settings"""
        ...

    @criterion.setter
    def criterion(self, value: QuantConnect.Optimizer.Objectives.Target) -> None:
        ...

    @property
    def constraints(self) -> typing.Sequence[QuantConnect.Optimizer.Objectives.Constraint]:
        """Optimization constraints"""
        ...

    @constraints.setter
    def constraints(self, value: typing.Sequence[QuantConnect.Optimizer.Objectives.Constraint]) -> None:
        ...

    @property
    def optimization_parameters(self) -> System.Collections.Generic.HashSet[QuantConnect.Optimizer.Parameters.OptimizationParameter]:
        """The user optimization parameters"""
        ...

    @optimization_parameters.setter
    def optimization_parameters(self, value: System.Collections.Generic.HashSet[QuantConnect.Optimizer.Parameters.OptimizationParameter]) -> None:
        ...

    @property
    def optimization_strategy_settings(self) -> QuantConnect.Optimizer.Strategies.OptimizationStrategySettings:
        """The user optimization parameters"""
        ...

    @optimization_strategy_settings.setter
    def optimization_strategy_settings(self, value: QuantConnect.Optimizer.Strategies.OptimizationStrategySettings) -> None:
        ...

    @property
    def out_of_sample_max_end_date(self) -> typing.Optional[datetime.datetime]:
        """Backtest out of sample maximum end date"""
        ...

    @out_of_sample_max_end_date.setter
    def out_of_sample_max_end_date(self, value: typing.Optional[datetime.datetime]) -> None:
        ...

    @property
    def out_of_sample_days(self) -> int:
        """The backtest out of sample day count"""
        ...

    @out_of_sample_days.setter
    def out_of_sample_days(self, value: int) -> None:
        ...

    @overload
    def __init__(self) -> None:
        """Creates a new instance"""
        ...

    @overload
    def __init__(self, packet_type: QuantConnect.Packets.PacketType) -> None:
        """
        Creates a new instance
        
        
        This Class is protected.
        """
        ...


class LeanOptimizer(System.Object, System.IDisposable, metaclass=abc.ABCMeta):
    """Base Lean optimizer class in charge of handling an optimization job packet"""

    @property
    def completed_backtests(self) -> int:
        """
        The total completed backtests count
        
        
        This Property is protected.
        """
        ...

    @property
    def status(self) -> QuantConnect.Optimizer.OptimizationStatus:
        """
        The current optimization status
        
        
        This Property is protected.
        """
        ...

    @property
    def optimization_target(self) -> QuantConnect.Optimizer.Objectives.Target:
        """
        The optimization target
        
        
        This Property is protected.
        """
        ...

    @property
    def running_parameter_set_for_backtest(self) -> System.Collections.Concurrent.ConcurrentDictionary[str, QuantConnect.Optimizer.Parameters.ParameterSet]:
        """
        Collection holding ParameterSet for each backtest id we are waiting to finish
        
        
        This Property is protected.
        """
        ...

    @property
    def pending_parameter_set(self) -> System.Collections.Concurrent.ConcurrentQueue[QuantConnect.Optimizer.Parameters.ParameterSet]:
        """
        Collection holding ParameterSet for each backtest id we are waiting to launch
        
        
        This Property is protected.
        """
        ...

    @property
    def strategy(self) -> QuantConnect.Optimizer.Strategies.IOptimizationStrategy:
        """
        The optimization strategy being used
        
        
        This Property is protected.
        """
        ...

    @property
    def node_packet(self) -> QuantConnect.Optimizer.OptimizationNodePacket:
        """
        The optimization packet
        
        
        This Property is protected.
        """
        ...

    @property
    def disposed(self) -> bool:
        """
        Indicates whether optimizer was disposed
        
        
        This Property is protected.
        """
        ...

    @property
    def ended(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.Optimizer.OptimizationResult], typing.Any], typing.Any]:
        """Event triggered when the optimization work ended"""
        ...

    @ended.setter
    def ended(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.Optimizer.OptimizationResult], typing.Any], typing.Any]) -> None:
        ...

    def __init__(self, node_packet: QuantConnect.Optimizer.OptimizationNodePacket) -> None:
        """
        Creates a new instance
        
        
        This Class is protected.
        
        :param node_packet: The optimization node packet to handle
        """
        ...

    def abort_lean(self, backtest_id: str) -> None:
        """
        Handles stopping Lean process
        
        
        This Class is protected.
        
        :param backtest_id: Specified backtest id
        """
        ...

    def dispose(self) -> None:
        """Disposes of any resources"""
        ...

    def get_backtest_name(self, parameter_set: QuantConnect.Optimizer.Parameters.ParameterSet) -> str:
        """
        Get's a new backtest name
        
        
        This Class is protected.
        """
        ...

    def get_current_estimate(self) -> int:
        """Returns the current optimization status and strategy estimates"""
        ...

    def get_log_details(self) -> str:
        """
        Helper method to have pretty more informative logs
        
        
        This Class is protected.
        """
        ...

    def get_runtime_statistics(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Get the current runtime statistics"""
        ...

    def new_result(self, json_backtest_result: str, backtest_id: str) -> None:
        """
        Handles a new backtest json result matching a requested backtest id
        
        
        This Class is protected.
        
        :param json_backtest_result: The backtest json result
        :param backtest_id: The associated backtest id
        """
        ...

    def run_lean(self, parameter_set: QuantConnect.Optimizer.Parameters.ParameterSet, backtest_name: str) -> str:
        """
        Handles starting Lean for a given parameter set
        
        
        This Class is protected.
        
        :param parameter_set: The parameter set for the backtest to run
        :param backtest_name: The backtest name to use
        :returns: The new unique backtest id.
        """
        ...

    def send_update(self) -> None:
        """
        Sends an update of the current optimization status to the user
        
        
        This Class is protected.
        """
        ...

    def set_optimization_status(self, optimization_status: QuantConnect.Optimizer.OptimizationStatus) -> None:
        """
        Sets the current optimization status
        
        
        This Class is protected.
        
        :param optimization_status: The new optimization status
        """
        ...

    def start(self) -> None:
        """Starts the optimization"""
        ...

    def trigger_on_end_event(self) -> None:
        """
        Triggers the optimization job end event
        
        
        This Class is protected.
        """
        ...


class OptimizationBacktestMetrics(QuantConnect.Optimizer.BacktestSummary):
    """Lightweight per-backtest record extracted at LeanOptimizer time to avoid retaining the full backtest JSON."""

    @property
    def total_performance(self) -> QuantConnect.Statistics.AlgorithmPerformance:
        """
        The backtest's total performance (wraps QuantConnect.Statistics.TradeStatistics,
        QuantConnect.Statistics.PortfolioStatistics, and QuantConnect.Statistics.Trade list); null when absent from the backtest result.
        """
        ...

    @total_performance.setter
    def total_performance(self, value: QuantConnect.Statistics.AlgorithmPerformance) -> None:
        ...

    @property
    def total_orders(self) -> int:
        """Number of orders the backtest produced."""
        ...

    @total_orders.setter
    def total_orders(self, value: int) -> None:
        ...

    @property
    def analysis_names(self) -> typing.Sequence[str]:
        """Names of the diagnostic QuantConnect.Analysis entries the backtest attached."""
        ...

    @analysis_names.setter
    def analysis_names(self, value: typing.Sequence[str]) -> None:
        ...

    @staticmethod
    def extract_from(backtest_id: str, parameter_set: QuantConnect.Optimizer.Parameters.ParameterSet, json_backtest_result: str) -> QuantConnect.Optimizer.OptimizationBacktestMetrics:
        """
        Extracts the fields the analyzer needs from a backtest result JSON; returns null when the parameter set is invalid.
        
        :param backtest_id: The backtest id.
        :param parameter_set: The parameter set the backtest was run with.
        :param json_backtest_result: The serialized backtest result JSON.
        """
        ...


class _EventContainer(typing.Generic[QuantConnect_Optimizer__EventContainer_Callable, QuantConnect_Optimizer__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> QuantConnect_Optimizer__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: QuantConnect_Optimizer__EventContainer_Callable) -> typing.Self:
        """Registers an event handler."""
        ...

    def __isub__(self, item: QuantConnect_Optimizer__EventContainer_Callable) -> typing.Self:
        """Unregisters an event handler."""
        ...


