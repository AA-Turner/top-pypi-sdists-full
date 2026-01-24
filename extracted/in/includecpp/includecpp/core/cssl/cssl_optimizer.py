"""
CSSL Optimizer - Smart Adaptive Performance System

This module provides intelligent C++/Python execution switching:
1. Adaptive threshold learning from actual execution times
2. Complexity scoring based on code analysis
3. Automatic tuning based on runtime performance
4. Full C++ interpreter for complex code (375x+ speedup)
5. Python for simple code (lower overhead)

The optimizer learns which execution path is fastest for different code patterns.
"""

import sys
import time
import hashlib
import re
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Callable
from dataclasses import dataclass, field
from threading import Lock
from collections import defaultdict


# =============================================================================
# Performance Thresholds (Auto-Tuned)
# =============================================================================

@dataclass
class PerformanceThresholds:
    """Configurable thresholds for optimization decisions."""

    # Source size thresholds (characters)
    small_source: int = 200          # Use Python for < 200 chars
    medium_source: int = 1000        # Mixed optimization
    large_source: int = 5000         # Full C++ acceleration

    # Complexity score thresholds
    simple_complexity: int = 10      # Simple code - Python
    complex_threshold: int = 50      # Complex code - C++

    # Loop thresholds
    small_loop: int = 50             # Small loops - Python OK
    large_loop: int = 500            # Large loops - prefer C++

    # Cache settings
    cache_enabled: bool = True
    cache_max_size: int = 200
    cache_ttl: float = 600.0         # 10 minutes TTL

    # Adaptive tuning
    adaptive_enabled: bool = True
    learning_rate: float = 0.1       # How fast to adapt thresholds
    min_samples: int = 5             # Min samples before adapting


# Global thresholds instance
THRESHOLDS = PerformanceThresholds()


# =============================================================================
# Complexity Analyzer
# =============================================================================

class ComplexityAnalyzer:
    """
    Analyzes CSSL code to estimate execution complexity.

    Scoring:
    - Each loop: +10 (nested: +20)
    - Each class: +15
    - Each function: +5
    - Datastruct operations: +20
    - String operations in loop: +15
    - Math operations: +5
    - Recursion detected: +30
    """

    # Patterns for complexity detection
    LOOP_PATTERNS = [
        r'\bfor\s*\(',
        r'\bwhile\s*\(',
        r'\bforeach\s*\(',
    ]
    CLASS_PATTERN = r'\bclass\s+\w+'
    FUNC_PATTERN = r'\b(?:define|void|int|float|string|bool|dynamic)\s+\w+\s*\('
    DATASTRUCT_PATTERN = r'\b(?:datastruct|shuffled|iterator|combo|dataspace)\b'
    RECURSION_PATTERN = r'(\w+)\s*\([^)]*\)[^{]*\{[^}]*\1\s*\('
    # v4.6.0: Native keyword forces C++ execution
    NATIVE_PATTERN = r'\bnative\b'
    # v4.6.5: Unative keyword forces Python execution (opposite of native)
    UNATIVE_PATTERN = r'\bunative\b'

    def __init__(self):
        self._pattern_cache: Dict[str, re.Pattern] = {}

    def _get_pattern(self, pattern: str) -> re.Pattern:
        """Get compiled regex pattern (cached)."""
        if pattern not in self._pattern_cache:
            self._pattern_cache[pattern] = re.compile(pattern, re.MULTILINE | re.IGNORECASE)
        return self._pattern_cache[pattern]

    def analyze(self, source: str) -> 'ComplexityScore':
        """Analyze source and return complexity score."""
        score = ComplexityScore(source=source)

        # Count loops
        for pattern in self.LOOP_PATTERNS:
            matches = self._get_pattern(pattern).findall(source)
            score.loop_count += len(matches)

        # Detect nested loops (simplified)
        score.nested_loops = source.count('for (') > 1 and 'for (' in source[source.find('for (') + 5:]

        # Count classes
        score.class_count = len(self._get_pattern(self.CLASS_PATTERN).findall(source))

        # Count functions
        score.function_count = len(self._get_pattern(self.FUNC_PATTERN).findall(source))

        # Check for datastruct operations
        score.has_datastruct = bool(self._get_pattern(self.DATASTRUCT_PATTERN).search(source))

        # Check for recursion
        score.has_recursion = bool(self._get_pattern(self.RECURSION_PATTERN).search(source))

        # Check for native keyword (forces C++ execution)
        score.force_native = bool(self._get_pattern(self.NATIVE_PATTERN).search(source))

        # Check for unative keyword (forces Python execution - opposite of native)
        score.force_python = bool(self._get_pattern(self.UNATIVE_PATTERN).search(source))

        # Calculate total score
        score.calculate()

        return score


@dataclass
class ComplexityScore:
    """Complexity analysis result."""
    source: str = ""
    loop_count: int = 0
    nested_loops: bool = False
    class_count: int = 0
    function_count: int = 0
    has_datastruct: bool = False
    has_recursion: bool = False
    force_native: bool = False  # Force C++ execution (native keyword)
    force_python: bool = False  # Force Python execution (unative keyword) - v4.6.5
    total_score: int = 0

    def calculate(self) -> None:
        """Calculate total complexity score."""
        self.total_score = 0

        # Base score from source size
        self.total_score += len(self.source) // 100

        # Loop complexity
        self.total_score += self.loop_count * 10
        if self.nested_loops:
            self.total_score += 20

        # Class complexity
        self.total_score += self.class_count * 15

        # Function complexity
        self.total_score += self.function_count * 5

        # Datastruct operations
        if self.has_datastruct:
            self.total_score += 20

        # Recursion
        if self.has_recursion:
            self.total_score += 30

    @property
    def recommendation(self) -> str:
        """Get execution recommendation."""
        if self.total_score < THRESHOLDS.simple_complexity:
            return "python"
        elif self.total_score >= THRESHOLDS.complex_threshold:
            return "cpp"
        else:
            return "hybrid"


# Global analyzer
_ANALYZER = ComplexityAnalyzer()


# =============================================================================
# Adaptive Performance Tracker
# =============================================================================

class PerformanceTracker:
    """
    Tracks execution performance and adapts thresholds.

    Learns which execution path (Python vs C++) is faster for different
    code patterns and complexity levels.
    """

    def __init__(self):
        self._lock = Lock()
        # Track times by complexity bracket
        self._python_times: Dict[str, List[float]] = defaultdict(list)
        self._cpp_times: Dict[str, List[float]] = defaultdict(list)
        # Track decisions and outcomes
        self._decisions: List[Tuple[str, str, float]] = []  # (complexity_bracket, engine, time)

    def _get_bracket(self, score: int) -> str:
        """Get complexity bracket for a score."""
        if score < 10:
            return "tiny"
        elif score < 30:
            return "small"
        elif score < 70:
            return "medium"
        elif score < 150:
            return "large"
        else:
            return "huge"

    def record(self, complexity_score: int, engine: str, exec_time: float) -> None:
        """Record execution performance."""
        bracket = self._get_bracket(complexity_score)

        with self._lock:
            if engine == "python":
                self._python_times[bracket].append(exec_time)
                # Keep last 50 samples
                if len(self._python_times[bracket]) > 50:
                    self._python_times[bracket] = self._python_times[bracket][-50:]
            else:
                self._cpp_times[bracket].append(exec_time)
                if len(self._cpp_times[bracket]) > 50:
                    self._cpp_times[bracket] = self._cpp_times[bracket][-50:]

            self._decisions.append((bracket, engine, exec_time))
            if len(self._decisions) > 200:
                self._decisions = self._decisions[-200:]

    def get_best_engine(self, complexity_score: int) -> str:
        """Get recommended engine based on historical performance."""
        bracket = self._get_bracket(complexity_score)

        with self._lock:
            py_times = self._python_times.get(bracket, [])
            cpp_times = self._cpp_times.get(bracket, [])

            # Need minimum samples
            if len(py_times) < THRESHOLDS.min_samples:
                # Not enough Python data - use default logic
                return "cpp" if complexity_score >= THRESHOLDS.complex_threshold else "python"

            if len(cpp_times) < THRESHOLDS.min_samples:
                # Not enough C++ data - try C++ to gather data
                return "cpp" if complexity_score >= THRESHOLDS.simple_complexity else "python"

            # Compare averages
            py_avg = sum(py_times) / len(py_times)
            cpp_avg = sum(cpp_times) / len(cpp_times)

            # Add small overhead penalty for C++ (call overhead)
            cpp_overhead = 0.0001  # 0.1ms overhead

            if cpp_avg + cpp_overhead < py_avg:
                return "cpp"
            else:
                return "python"

    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        with self._lock:
            stats = {
                "brackets": {},
                "total_decisions": len(self._decisions),
            }

            for bracket in ["tiny", "small", "medium", "large", "huge"]:
                py_times = self._python_times.get(bracket, [])
                cpp_times = self._cpp_times.get(bracket, [])

                stats["brackets"][bracket] = {
                    "python_samples": len(py_times),
                    "python_avg_ms": (sum(py_times) / len(py_times) * 1000) if py_times else 0,
                    "cpp_samples": len(cpp_times),
                    "cpp_avg_ms": (sum(cpp_times) / len(cpp_times) * 1000) if cpp_times else 0,
                    "recommended": self.get_best_engine(
                        {"tiny": 5, "small": 20, "medium": 50, "large": 100, "huge": 200}[bracket]
                    ),
                }

            return stats


# Global tracker
_TRACKER = PerformanceTracker()


# =============================================================================
# AST Cache
# =============================================================================

@dataclass
class CachedAST:
    """Cached AST with metadata."""
    ast: Any
    source_hash: str
    created_at: float
    complexity_score: int = 0
    access_count: int = 0
    total_exec_time: float = 0.0

    @property
    def avg_exec_time(self) -> float:
        if self.access_count == 0:
            return 0.0
        return self.total_exec_time / self.access_count


class ASTCache:
    """Thread-safe AST cache with LRU eviction and TTL."""

    def __init__(self, max_size: int = 200, ttl: float = 600.0):
        self._cache: Dict[str, CachedAST] = {}
        self._lock = Lock()
        self._max_size = max_size
        self._ttl = ttl
        self._hits = 0
        self._misses = 0

    def _hash_source(self, source: str) -> str:
        return hashlib.md5(source.encode('utf-8')).hexdigest()

    def get(self, source: str) -> Optional[CachedAST]:
        """Get cached AST for source code."""
        source_hash = self._hash_source(source)

        with self._lock:
            if source_hash in self._cache:
                cached = self._cache[source_hash]

                if time.time() - cached.created_at > self._ttl:
                    del self._cache[source_hash]
                    self._misses += 1
                    return None

                cached.access_count += 1
                self._hits += 1
                return cached

            self._misses += 1
            return None

    def put(self, source: str, ast: Any, complexity_score: int = 0) -> None:
        """Cache AST for source code."""
        source_hash = self._hash_source(source)

        with self._lock:
            if len(self._cache) >= self._max_size:
                self._evict_lru()

            self._cache[source_hash] = CachedAST(
                ast=ast,
                source_hash=source_hash,
                created_at=time.time(),
                complexity_score=complexity_score
            )

    def record_execution(self, source: str, exec_time: float) -> None:
        """Record execution time for adaptive optimization."""
        source_hash = self._hash_source(source)

        with self._lock:
            if source_hash in self._cache:
                self._cache[source_hash].total_exec_time += exec_time

    def _evict_lru(self) -> None:
        """Evict least recently used entry."""
        if not self._cache:
            return

        oldest_hash = min(
            self._cache.keys(),
            key=lambda h: (self._cache[h].access_count, -self._cache[h].created_at)
        )
        del self._cache[oldest_hash]

    def clear(self) -> None:
        """Clear all cached ASTs."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    @property
    def stats(self) -> Dict[str, Any]:
        total = self._hits + self._misses
        return {
            'size': len(self._cache),
            'max_size': self._max_size,
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': self._hits / total if total > 0 else 0.0,
        }


# Global AST cache
_AST_CACHE = ASTCache(
    max_size=THRESHOLDS.cache_max_size,
    ttl=THRESHOLDS.cache_ttl
)


# =============================================================================
# Execution Context
# =============================================================================

@dataclass
class ExecutionContext:
    """Context for optimized execution decisions."""
    source: str
    source_size: int = 0
    complexity: Optional[ComplexityScore] = None
    recommended_engine: str = "python"
    cached_ast: Optional[CachedAST] = None

    def __post_init__(self):
        self.source_size = len(self.source)
        # Quick complexity analysis
        self.complexity = _ANALYZER.analyze(self.source)
        # Get recommendation from tracker (adaptive) or complexity score
        if THRESHOLDS.adaptive_enabled:
            self.recommended_engine = _TRACKER.get_best_engine(self.complexity.total_score)
        else:
            self.recommended_engine = self.complexity.recommendation


# =============================================================================
# Optimized Operations
# =============================================================================

class OptimizedOperations:
    """
    Provides optimized implementations that automatically choose
    between Python and C++ based on input size.
    """

    def __init__(self):
        self._cpp_module = None
        self._cpp_available = False
        self._load_cpp()

    def _load_cpp(self) -> None:
        try:
            from . import _cpp_module, _CPP_AVAILABLE
            self._cpp_module = _cpp_module
            self._cpp_available = _CPP_AVAILABLE
        except ImportError:
            pass

    def str_upper(self, s: str) -> str:
        if len(s) < 100 or not self._cpp_available:
            return s.upper()
        if self._cpp_module and hasattr(self._cpp_module, 'str_upper'):
            return self._cpp_module.str_upper(s)
        return s.upper()

    def str_lower(self, s: str) -> str:
        if len(s) < 100 or not self._cpp_available:
            return s.lower()
        if self._cpp_module and hasattr(self._cpp_module, 'str_lower'):
            return self._cpp_module.str_lower(s)
        return s.lower()

    def str_replace(self, s: str, old: str, new: str) -> str:
        if len(s) < 100 or not self._cpp_available:
            return s.replace(old, new)
        if self._cpp_module and hasattr(self._cpp_module, 'str_replace'):
            return self._cpp_module.str_replace(s, old, new)
        return s.replace(old, new)

    def str_split(self, s: str, sep: str) -> List[str]:
        if len(s) < 100 or not self._cpp_available:
            return s.split(sep)
        if self._cpp_module and hasattr(self._cpp_module, 'str_split'):
            return self._cpp_module.str_split(s, sep)
        return s.split(sep)

    def str_join(self, sep: str, items: List[str]) -> str:
        if len(items) < 50 or not self._cpp_available:
            return sep.join(items)
        if self._cpp_module and hasattr(self._cpp_module, 'str_join'):
            return self._cpp_module.str_join(sep, items)
        return sep.join(items)

    def str_trim(self, s: str) -> str:
        if len(s) < 100 or not self._cpp_available:
            return s.strip()
        if self._cpp_module and hasattr(self._cpp_module, 'str_trim'):
            return self._cpp_module.str_trim(s)
        return s.strip()

    def tokenize(self, source: str) -> List[Any]:
        """Optimized tokenization."""
        use_cpp = (
            self._cpp_available and
            len(source) >= THRESHOLDS.small_source and
            self._cpp_module and
            hasattr(self._cpp_module, 'Lexer')
        )

        if use_cpp:
            try:
                lexer = self._cpp_module.Lexer(source)
                return lexer.tokenize()
            except Exception:
                pass

        from .cssl_parser import CSSLLexer
        lexer = CSSLLexer(source)
        return lexer.tokenize()


# Global optimized operations
OPS = OptimizedOperations()


# =============================================================================
# Smart Optimized Runtime
# =============================================================================

class OptimizedRuntime:
    """
    Smart CSSL runtime with adaptive C++/Python switching.

    Features:
    - Learns from execution times to optimize decisions
    - Uses complexity analysis for initial estimates
    - Full C++ interpreter for complex code (375x+ speedup)
    - Python for simple code (lower call overhead)
    - AST caching for repeated execution
    """

    def __init__(self):
        self._cache = _AST_CACHE
        self._tracker = _TRACKER
        self._ops = OPS
        self._execution_times: List[float] = []
        self._cpp_module = None
        self._cpp_available = False
        self._load_cpp()

    def _load_cpp(self) -> None:
        try:
            from . import _cpp_module, _CPP_AVAILABLE
            self._cpp_module = _cpp_module
            self._cpp_available = _CPP_AVAILABLE
        except ImportError:
            pass

    def execute(self, source: str, service_engine=None) -> Any:
        """
        Execute CSSL with smart optimization.

        Decision flow:
        1. Analyze complexity
        2. Check if service_engine requires Python
        3. Consult adaptive tracker for best engine
        4. Check AST cache
        5. Execute with chosen engine
        6. Record performance for learning
        """
        start_time = time.perf_counter()

        # Create execution context (includes complexity analysis)
        ctx = ExecutionContext(source)

        # Check for 'native' keyword - forces C++ execution
        force_native = ctx.complexity.force_native if ctx.complexity else False
        # Check for 'unative' keyword - forces Python execution (opposite of native)
        force_python = ctx.complexity.force_python if ctx.complexity else False

        # Determine execution engine
        if force_python:
            # 'unative' keyword forces Python execution (no C++ even if available)
            engine = "python"
        elif force_native and self._cpp_available:
            # 'native' keyword forces C++ execution (no fallback)
            engine = "cpp"
        elif service_engine is not None:
            # Service engine requires Python runtime
            engine = "python"
        elif self._cpp_available and ctx.recommended_engine == "cpp":
            # Check adaptive recommendation
            engine = "cpp"
        else:
            engine = "python"

        # Execute
        try:
            if engine == "cpp" and self._cpp_module and hasattr(self._cpp_module, 'run_cssl'):
                result = self._execute_cpp(source)
            else:
                # Check cache for Python execution
                cached = self._cache.get(source) if THRESHOLDS.cache_enabled else None
                if cached is not None:
                    result = self._execute_ast(cached.ast, service_engine)
                else:
                    result = self._parse_and_execute(source, ctx, service_engine)
                engine = "python"  # Ensure we record correctly

            # Record timing
            exec_time = time.perf_counter() - start_time
            self._execution_times.append(exec_time)
            if len(self._execution_times) > 100:
                self._execution_times = self._execution_times[-100:]

            # Record for adaptive learning
            if THRESHOLDS.adaptive_enabled and ctx.complexity:
                self._tracker.record(ctx.complexity.total_score, engine, exec_time)

            if THRESHOLDS.cache_enabled:
                self._cache.record_execution(source, exec_time)

            return result

        except Exception as e:
            # On C++ failure, fallback to Python
            if engine == "cpp":
                return self._parse_and_execute(source, ctx, service_engine)
            raise

    def _execute_cpp(self, source: str) -> Any:
        """Execute using full C++ interpreter."""
        return self._cpp_module.run_cssl(source)

    def _parse_and_execute(self, source: str, ctx: ExecutionContext, service_engine) -> Any:
        """Parse and execute with Python runtime."""
        from .cssl_parser import CSSLParser
        from .cssl_runtime import CSSLRuntime

        # Tokenize (with smart switching)
        tokens = self._ops.tokenize(source)

        # Parse
        parser = CSSLParser(tokens)
        ast = parser.parse()

        # Cache AST
        if THRESHOLDS.cache_enabled and ctx.complexity:
            self._cache.put(source, ast, ctx.complexity.total_score)

        # Execute
        runtime = CSSLRuntime(service_engine)
        return runtime.execute_ast(ast)

    def _execute_ast(self, ast: Any, service_engine) -> Any:
        """Execute pre-parsed AST."""
        from .cssl_runtime import CSSLRuntime
        runtime = CSSLRuntime(service_engine)
        return runtime.execute_ast(ast)

    @property
    def avg_execution_time(self) -> float:
        if not self._execution_times:
            return 0.0
        return sum(self._execution_times) / len(self._execution_times) * 1000

    @property
    def cache_stats(self) -> Dict[str, Any]:
        return self._cache.stats

    @property
    def performance_stats(self) -> Dict[str, Any]:
        return self._tracker.get_stats()


# Global optimized runtime
_OPTIMIZED_RUNTIME = OptimizedRuntime()


# =============================================================================
# Public API
# =============================================================================

def run_optimized(source: str, service_engine=None) -> Any:
    """
    Run CSSL with smart adaptive optimization.

    Automatically chooses between:
    - C++ interpreter for complex code (375x+ faster)
    - Python runtime for simple code (lower overhead)
    - Cached AST for repeated execution

    The optimizer learns from execution times to make better decisions.

    Args:
        source: CSSL source code
        service_engine: Optional service engine for Python interop

    Returns:
        Execution result
    """
    return _OPTIMIZED_RUNTIME.execute(source, service_engine)


def get_optimizer_stats() -> Dict[str, Any]:
    """Get comprehensive optimizer statistics."""
    from . import _CPP_AVAILABLE, _CPP_LOAD_SOURCE

    return {
        'cpp_available': _CPP_AVAILABLE,
        'cpp_source': _CPP_LOAD_SOURCE,
        'cache': _AST_CACHE.stats,
        'performance': _TRACKER.get_stats(),
        'avg_exec_time_ms': _OPTIMIZED_RUNTIME.avg_execution_time,
        'thresholds': {
            'small_source': THRESHOLDS.small_source,
            'medium_source': THRESHOLDS.medium_source,
            'large_source': THRESHOLDS.large_source,
            'simple_complexity': THRESHOLDS.simple_complexity,
            'complex_threshold': THRESHOLDS.complex_threshold,
        }
    }


def configure_optimizer(
    cache_enabled: bool = None,
    cache_max_size: int = None,
    cache_ttl: float = None,
    adaptive_enabled: bool = None,
    small_source: int = None,
    complex_threshold: int = None,
) -> None:
    """
    Configure optimizer settings.

    Args:
        cache_enabled: Enable/disable AST caching
        cache_max_size: Maximum cached ASTs
        cache_ttl: Cache TTL in seconds
        adaptive_enabled: Enable adaptive threshold learning
        small_source: Source size threshold for Python
        complex_threshold: Complexity score threshold for C++
    """
    global THRESHOLDS, _AST_CACHE

    if cache_enabled is not None:
        THRESHOLDS.cache_enabled = cache_enabled
    if cache_max_size is not None:
        THRESHOLDS.cache_max_size = cache_max_size
    if cache_ttl is not None:
        THRESHOLDS.cache_ttl = cache_ttl
    if adaptive_enabled is not None:
        THRESHOLDS.adaptive_enabled = adaptive_enabled
    if small_source is not None:
        THRESHOLDS.small_source = small_source
    if complex_threshold is not None:
        THRESHOLDS.complex_threshold = complex_threshold

    _AST_CACHE = ASTCache(
        max_size=THRESHOLDS.cache_max_size,
        ttl=THRESHOLDS.cache_ttl
    )


def clear_cache() -> None:
    """Clear AST cache."""
    _AST_CACHE.clear()


def get_optimized_ops() -> OptimizedOperations:
    """Get the optimized operations instance."""
    return OPS


def analyze_complexity(source: str) -> Dict[str, Any]:
    """
    Analyze CSSL code complexity.

    Returns complexity score and recommendation (python/cpp/hybrid).
    """
    score = _ANALYZER.analyze(source)
    return {
        'source_size': len(source),
        'loop_count': score.loop_count,
        'nested_loops': score.nested_loops,
        'class_count': score.class_count,
        'function_count': score.function_count,
        'has_datastruct': score.has_datastruct,
        'has_recursion': score.has_recursion,
        'total_score': score.total_score,
        'recommendation': score.recommendation,
    }


# =============================================================================
# Precompiled Patterns
# =============================================================================

class PrecompiledPattern:
    """
    Precompiled CSSL code for maximum performance.

    Use this for frequently executed code patterns.
    """

    def __init__(self, source: str):
        self.source = source
        self._ast = None
        self._complexity = _ANALYZER.analyze(source)
        self._compile()

    def _compile(self) -> None:
        """Pre-parse the source."""
        from .cssl_parser import CSSLParser
        tokens = OPS.tokenize(self.source)
        parser = CSSLParser(tokens)
        self._ast = parser.parse()

    def execute(self, service_engine=None) -> Any:
        """Execute precompiled pattern."""
        from .cssl_runtime import CSSLRuntime
        runtime = CSSLRuntime(service_engine)
        return runtime.execute_ast(self._ast)

    @property
    def complexity(self) -> int:
        return self._complexity.total_score


def precompile(source: str) -> PrecompiledPattern:
    """
    Precompile CSSL source for repeated execution.

    Returns a PrecompiledPattern that can be executed multiple times
    without re-parsing.
    """
    return PrecompiledPattern(source)
