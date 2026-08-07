from typing import overload
from enum import IntEnum
import datetime
import typing

import QuantConnect
import QuantConnect.Algorithm
import QuantConnect.Lean.Engine.Results
import QuantConnect.Lean.Engine.Results.Analysis
import QuantConnect.Lean.Engine.Results.Analysis.Analyses
import QuantConnect.Packets
import QuantConnect.Statistics
import QuantConnect.Util
import System
import System.Collections.Generic


class AlgorithmSpeedSample:
    """
    A point-in-time sample of the engine's cumulative speed counters, fed by the result handler
    into the AlgorithmSpeedTracker on each in-run analysis run.
    """

    @property
    def elapsed(self) -> datetime.timedelta:
        """The wall-clock time elapsed since the backtest started."""
        ...

    @property
    def data_points(self) -> int:
        """The cumulative data points processed by the main algorithm loop."""
        ...

    @property
    def history_data_points(self) -> int:
        """The cumulative data points served by the history provider."""
        ...

    @property
    def processed_days(self) -> int:
        """The calendar days the backtest has processed so far."""
        ...

    @property
    def total_days(self) -> int:
        """The total calendar days the backtest will run."""
        ...

    def __init__(self, elapsed: datetime.timedelta, data_points: int, history_data_points: int, processed_days: int, total_days: int) -> None:
        """
        Initializes a new instance of the AlgorithmSpeedSample struct.
        
        :param elapsed: Wall-clock time elapsed since the backtest started.
        :param data_points: Cumulative data points processed by the main algorithm loop.
        :param history_data_points: Cumulative data points served by the history provider.
        :param processed_days: Calendar days the backtest has processed so far.
        :param total_days: Total calendar days the backtest will run.
        """
        ...


class AlgorithmSpeedTracker(System.Object):
    """
    Accumulates periodic samples of the engine's speed counters (data points processed, history data points,
    backtest days processed) while a backtest runs, and computes the throughput and progress metrics consumed
    by the in-run Analyses.AlgorithmSpeedAnalysis.
    All rates are computed between samples, so setup time before the first sample is excluded.
    """

    RECENT_WINDOW_SAMPLES: int = 5
    """
    The number of trailing samples that make up the "recent" window used by the windowed rates.
    At the ~30 second in-run analysis cadence this spans roughly the last two minutes.
    """

    @property
    def sample_count(self) -> int:
        """The number of samples recorded so far."""
        ...

    @property
    def total_days(self) -> int:
        """The total number of calendar days the backtest will run."""
        ...

    @property
    def processed_days(self) -> int:
        """The number of calendar days the backtest has processed as of the latest sample."""
        ...

    @property
    def progress(self) -> float:
        """The backtest progress as of the latest sample, in the <0, 1> range."""
        ...

    @property
    def elapsed(self) -> datetime.timedelta:
        """The wall-clock time elapsed since the backtest started, as of the latest sample."""
        ...

    @property
    def sampled_span(self) -> datetime.timedelta:
        """
        The wall-clock time between the first and the latest sample, that is,
        the period the rates are measured over.
        """
        ...

    @property
    def has_data_point_counts(self) -> bool:
        """
        Whether the main loop data point counter is being fed. When the counter is not wired in
        (it reads zero), data-point-based rates are not meaningful and should not be used.
        """
        ...

    @property
    def data_points_per_second(self) -> typing.Optional[float]:
        """
        The average data points processed per second over the whole sampled span, including
        history data points to match the speed the engine reports on completion.
        Null when there are not enough samples to measure.
        """
        ...

    @property
    def initial_data_points_per_second(self) -> typing.Optional[float]:
        """
        The average data points processed per second over the first RECENT_WINDOW_SAMPLES samples,
        used as the early-run baseline for degradation detection. Null when there are not enough samples to measure.
        """
        ...

    def add_sample(self, sample: QuantConnect.Lean.Engine.Results.Analysis.AlgorithmSpeedSample) -> None:
        """
        Records a sample of the cumulative speed counters. Samples with a non-increasing
        elapsed time are ignored so rates are always computed over positive time deltas.
        
        :param sample: The sample of the cumulative speed counters.
        """
        ...

    def estimated_remaining_time(self, skip_last: int = 0) -> typing.Optional[datetime.timedelta]:
        """
        The estimated wall-clock time left for the backtest to complete, projecting the recent
        calendar-days-per-second pace over the remaining backtest days.
        
        :param skip_last: Number of trailing samples to skip, to evaluate the projection as of a previous run.
        :returns: The estimate, zero when the backtest already reached its end date, or null when the recent pace
        is zero or there are not enough samples to measure.
        """
        ...

    def recent_data_points_per_second(self, skip_last: int = 0) -> typing.Optional[float]:
        """
        The average data points processed per second over the recent window, including history data points.
        
        :param skip_last: Number of trailing samples to skip, to evaluate the window as of a previous run.
        :returns: The windowed rate, or null when there are not enough samples to measure.
        """
        ...

    def recent_days_per_second(self, skip_last: int = 0) -> typing.Optional[float]:
        """
        The average backtest calendar days processed per wall-clock second over the recent window.
        
        :param skip_last: Number of trailing samples to skip, to evaluate the window as of a previous run.
        :returns: The windowed rate, or null when there are not enough samples to measure.
        """
        ...

    def recent_history_data_points(self, skip_last: int = 0) -> int:
        """
        The number of history data points served over the recent window.
        
        :param skip_last: Number of trailing samples to skip, to evaluate the window as of a previous run.
        """
        ...

    def recent_history_data_points_share(self, skip_last: int = 0) -> typing.Optional[float]:
        """
        The share of the data points processed over the recent window that were served by the history
        provider, in the <0, 1> range.
        
        :param skip_last: Number of trailing samples to skip, to evaluate the window as of a previous run.
        :returns: The share, or null when there are not enough samples or no data points were processed in the window.
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

    @property
    def speed(self) -> QuantConnect.Lean.Engine.Results.Analysis.AlgorithmSpeedTracker:
        """
        The speed metrics tracked for the running backtest.
        Only available for in-run analysis; null on the final analysis.
        """
        ...

    def __init__(self, result: QuantConnect.Result, algorithm: QuantConnect.Algorithm.QCAlgorithm, language: QuantConnect.Language, logs: typing.Sequence[str], equity_curve: System.Collections.Generic.SortedList[datetime.datetime, float], benchmark_equity_curve: System.Collections.Generic.SortedList[datetime.datetime, float], speed: QuantConnect.Lean.Engine.Results.Analysis.AlgorithmSpeedTracker = None) -> None:
        """Initializes a new instance of the ResultsAnalysisRunParameters class with the specified dependencies."""
        ...


class ResultsAnalyzer(System.Object):
    """
    Runs the suite of backtest diagnostic tests against a single backtest, in one of two modes
    depending on how the instance is created:
    a final analysis instance is created with the completed result and logs, and runs the
    full analysis set once; an in-run analysis instance is created with the engine's
    speed counters, is kept alive for the duration of the backtest, and periodically runs the
    in-run capable analyses incrementally against the intermediate results and logs.
    """

    @property
    def is_in_run(self) -> bool:
        """
        Whether this instance was created for in-run analysis of a backtest still in progress
        (see create_for_in_run_analysis), as opposed to the final analysis of a
        completed backtest.
        
        
        This Property is protected.
        """
        ...

    @property
    def analyses(self) -> typing.Sequence[QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis]:
        """
        The diagnostic analyses to run, in execution order: descending by weight, so changing an
        analysis weight automatically reorders execution. Created once and reused across runs,
        since the analyses are stateless and their weights are constant. In-run instances filter
        the set to the analyses that declare they can run while the backtest is in progress
        (see BaseResultsAnalysis.runs_in_run).
        
        
        This Property is protected.
        """
        ...

    @property
    def requires_equity_curves(self) -> bool:
        """
        Whether the equity and benchmark curves should be built before running the analyses.
        Building them requires a benchmark history request, so in-run instances skip it:
        none of the in-run analyses read the curves, and building them would issue the
        history request on every run.
        
        
        This Property is protected.
        """
        ...

    @property
    def speed_tracker(self) -> QuantConnect.Lean.Engine.Results.Analysis.AlgorithmSpeedTracker:
        """
        The speed metrics tracked for the running backtest, made available to the analyses
        through ResultsAnalysisRunParameters.speed. An in-run instance owns its
        tracker and feeds it a sample on each run; the final analysis instance receives the same
        tracker so the speed analysis also runs against the full-run metrics. Null when speed is
        not tracked.
        
        
        This Property is protected.
        """
        ...

    @overload
    def __init__(self, result: QuantConnect.Result, algorithm: QuantConnect.Algorithm.QCAlgorithm, language: QuantConnect.Language, logs: typing.Sequence[str], speed_tracker: QuantConnect.Lean.Engine.Results.Analysis.AlgorithmSpeedTracker = None) -> None:
        """
        Initializes a new instance of the ResultsAnalyzer class for the final
        analysis of a completed backtest. Use create_for_final_analysis or
        create_for_in_run_analysis to create instances.
        
        
        This Class is protected.
        
        :param result: The backtest result to analyze.
        :param algorithm: The algorithm instance used for history requests and settings.
        :param language: The programming language the algorithm is written in.
        :param logs: The full list of log lines produced by the backtest.
        :param speed_tracker: The speed metrics tracked for the backtest, or null when speed is not tracked.
        """
        ...

    @overload
    def __init__(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, language: QuantConnect.Language, start_time: typing.Union[datetime.datetime, datetime.date], performance_tracking_tool: QuantConnect.Util.PerformanceTrackingTool, progress_monitor: QuantConnect.Lean.Engine.Results.BacktestProgressMonitor) -> None:
        """
        Initializes a new instance of the ResultsAnalyzer class for in-run analysis
        of a backtest still in progress. Use create_for_in_run_analysis to create instances.
        
        
        This Class is protected.
        
        :param algorithm: The algorithm instance used for history requests and settings.
        :param language: The programming language the algorithm is written in.
        :param start_time: The UTC time the backtest started, for the speed samples' elapsed time.
        :param performance_tracking_tool: The engine's data point counters, for the speed samples.
        :param progress_monitor: The backtest day-progress monitor, for the speed samples.
        """
        ...

    def complete_speed_tracking(self) -> QuantConnect.Lean.Engine.Results.Analysis.AlgorithmSpeedTracker:
        """
        Completes the speed metrics with one final sample so they cover the backtest through
        its end, and returns the tracker for the final analysis to reuse. The tracker is left
        untouched when no sample can be taken, like when the algorithm never left warm-up.
        """
        ...

    @staticmethod
    def create_for_final_analysis(result: QuantConnect.Result, algorithm: QuantConnect.Algorithm.QCAlgorithm, language: QuantConnect.Language, logs: typing.Sequence[str], speed_tracker: QuantConnect.Lean.Engine.Results.Analysis.AlgorithmSpeedTracker = None) -> QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalyzer:
        """
        Creates an analyzer for the final analysis of a completed backtest, running the full
        analysis set once through run(int, int).
        
        :param result: The backtest result to analyze.
        :param algorithm: The algorithm instance used for history requests and settings.
        :param language: The programming language the algorithm is written in.
        :param logs: The full list of log lines produced by the backtest.
        :param speed_tracker: The speed metrics tracked for the backtest, typically completed by the
        in-run analyzer through complete_speed_tracking, or null when speed is not tracked.
        :returns: The final analysis instance.
        """
        ...

    @staticmethod
    def create_for_in_run_analysis(algorithm: QuantConnect.Algorithm.QCAlgorithm, language: QuantConnect.Language, start_time: typing.Union[datetime.datetime, datetime.date], performance_tracking_tool: QuantConnect.Util.PerformanceTrackingTool, progress_monitor: QuantConnect.Lean.Engine.Results.BacktestProgressMonitor) -> QuantConnect.Lean.Engine.Results.Analysis.ResultsAnalyzer:
        """
        Creates an analyzer for in-run analysis of a backtest still in progress. The instance is
        expected to be kept alive for the duration of the backtest, sampling the given engine
        speed counters on each run(BacktestResult, IReadOnlyList{string}, AlgorithmPerformance, int, int) call.
        
        :param algorithm: The algorithm instance used for history requests and settings.
        :param language: The programming language the algorithm is written in.
        :param start_time: The UTC time the backtest started, for the speed samples' elapsed time.
        :param performance_tracking_tool: The engine's data point counters, for the speed samples.
        :param progress_monitor: The backtest day-progress monitor, for the speed samples.
        :returns: The in-run analysis instance.
        """
        ...

    def get_analyses(self) -> typing.Sequence[QuantConnect.Lean.Engine.Results.Analysis.Analyses.BaseResultsAnalysis]:
        """
        Creates the full set of diagnostic analyses to run against the backtest.
        Each analysis declares through BaseResultsAnalysis.runs_in_run whether it can
        also run while the backtest is in progress, which in-run instances filter this set by.
        
        
        This Class is protected.
        """
        ...

    @overload
    def run(self, time_limit_seconds: int = 5, max_failed_analyses: int = 10) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Runs all registered diagnostic checks against the backtest in weight order,
        stopping early when the time limit or maximum failure count is reached.
        
        :param time_limit_seconds: Wall-clock seconds allowed for the full chain before early exit.
        :param max_failed_analyses: Maximum number of failing analyses to collect before stopping; also the max returned.
        :returns: Up to max_failed_analysesQuantConnect.Analysis entries with solutions, ranked by weight.
        """
        ...

    @overload
    def run(self, result: QuantConnect.Packets.BacktestResult, logs: typing.Sequence[str], total_performance: QuantConnect.Statistics.AlgorithmPerformance, time_limit_seconds: int = 1, max_failed_analyses: int = 10) -> typing.Sequence[QuantConnect.Analysis]:
        """
        Runs the in-run analyses against the given intermediate backtest result and the log
        lines produced since the previous run. The returned findings are the merge of this
        run's findings into the ones accumulated by previous runs: findings from analyses
        scanning the order event and log streams are accumulated (first sample kept, counts
        totaled), while findings from state-based analyses are replaced on every run.
        
        :param result: The current intermediate backtest result. Its orders and order events
        are windows truncated to the most recent ones, so the in-run analyses can miss orders and
        events already evicted from them; the final analysis re-scans the complete data. Its charts
        are the handler's live ones, read without synchronization: a torn read while the algorithm
        thread updates them can fail a run, which the handler catches, and the next run retries.
        :param logs: The full list of log lines produced so far; the analyzer analyzes the
        lines past the ones consumed by previous runs.
        :param total_performance: The current total algorithm performance, for analyses that read
        portfolio statistics. Withheld from the analyses until the first equity sample exists, since
        the statistics are all-zero defaults before that.
        :param time_limit_seconds: Wall-clock seconds allowed for the full chain before early exit.
        The default is small because the analysis runs on the result handler thread, delaying message
        processing while it runs.
        :param max_failed_analyses: Maximum number of failing analyses to return.
        :returns: The accumulated findings, ranked by analysis weight.
        """
        ...

    def set_analysis_data(self, result: QuantConnect.Result, logs: typing.Sequence[str]) -> None:
        """
        Sets the backtest data to analyze. Used by in-run instances, which are kept alive
        and run multiple times against fresh data.
        
        
        This Class is protected.
        
        :param result: The backtest result to analyze.
        :param logs: The list of log lines to analyze.
        """
        ...

    def take_speed_sample(self) -> typing.Optional[QuantConnect.Lean.Engine.Results.Analysis.AlgorithmSpeedSample]:
        """
        Takes a sample of the engine speed counters for the algorithm speed analysis.
        Null while the algorithm warms up, since the warm-up pace would skew the speed metrics.
        
        
        This Class is protected.
        """
        ...


