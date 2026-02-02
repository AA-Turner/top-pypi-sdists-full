"""
DSLighting Benchmark System

Provides lightweight benchmarking capabilities, including:
1. BaseBenchmark (pure DSLighting)
2. MLELiteBenchmark (MLE-Bench + DSLighting)
3. CustomBenchmark (fully custom)
4. BenchmarkFactory (create from config)
5. Evaluator (grading helper)

Example:
    >>> from dslighting.benchmark import MLELiteBenchmark, BenchmarkFactory, Evaluator
    >>>
    >>> # Option 1: create directly
    >>> benchmark = MLELiteBenchmark()
    >>> results = await benchmark.run_evaluation(eval_fn)
    >>>
    >>> # Option 2: create from config
    >>> factory = BenchmarkFactory.from_config_file("config.yaml")
    >>> benchmark = factory.create("mle-lite")
    >>> results = await benchmark.run_evaluation(eval_fn)
    >>>
    >>> # Option 3: use evaluator directly
    >>> evaluator = Evaluator.from_registry(...)
    >>> score = evaluator.evaluate_sync(submission_path)
"""

# DSLighting benchmark exports.
from dslighting.benchmark.core import (
    BaseBenchmark,
    CustomBenchmark,
    MLELiteBenchmark,
    BaseBenchmarkEvaluator,
)
from dslighting.benchmark.factory import BenchmarkFactory
from dslighting.benchmark.grading import Evaluator

# Compatibility aliases.
UniversalEvaluator = Evaluator
KaggleEvaluator = Evaluator

# Re-export DSAT benchmarks for compatibility.
try:
    from dsat.benchmark.benchmark import BaseBenchmark as DSATBaseBenchmark
    from dsat.benchmark.mle import MLEBenchmark
    from dsat.benchmark.sciencebench import ScienceBenchBenchmark

    __all__ = [
        # DSLighting benchmarks
        "BaseBenchmark",
        "CustomBenchmark",
        "MLELiteBenchmark",
        "BenchmarkFactory",
        "Evaluator",
        "UniversalEvaluator",  # Alias for Evaluator
        "KaggleEvaluator",     # Alias for Evaluator
        "BaseBenchmarkEvaluator",
        # DSAT benchmarks
        "DSATBaseBenchmark",
        "DSATMLEBenchmark",
        "DSATScienceBenchBenchmark",
    ]

except ImportError:
    # If DSAT is unavailable, export DSLighting only.
    __all__ = [
        "BaseBenchmark",
        "CustomBenchmark",
        "MLELiteBenchmark",
        "BenchmarkFactory",
        "Evaluator",
        "UniversalEvaluator",  # Alias for Evaluator
        "KaggleEvaluator",     # Alias for Evaluator
        "BaseBenchmarkEvaluator",
    ]
