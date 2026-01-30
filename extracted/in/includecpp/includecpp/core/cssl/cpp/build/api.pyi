"""Auto-generated type stubs for IncludeCPP C++ bindings

This file describes the raw C++ module structure.
For VSCode autocomplete, see cpp_api_extensions.pyi
"""
from typing import Any, List, Dict, Optional, Union, overload, Sequence

class cssl_core:
    """Module: cssl_core

    Sources: include/cssl_core.cpp
    """

    class Lexer:
        """C++ class: Lexer"""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Initialize Lexer instance"""
            ...

        @staticmethod
        def Initialize(*args: Any, **kwargs: Any) -> "cssl_core.Lexer":
            """Create and initialize a new Lexer instance"""
            ...

        def tokenize(self) -> Any:
            """C++ method: tokenize"""
            ...

    class Token:
        """C++ class: Token"""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Initialize Token instance"""
            ...

        @staticmethod
        def Initialize(*args: Any, **kwargs: Any) -> "cssl_core.Token":
            """Create and initialize a new Token instance"""
            ...

        pass

    class Interpreter:
        """C++ class: Interpreter"""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Initialize Interpreter instance"""
            ...

        @staticmethod
        def Initialize(*args: Any, **kwargs: Any) -> "cssl_core.Interpreter":
            """Create and initialize a new Interpreter instance"""
            ...

        def run(self) -> Any:
            """C++ method: run"""
            ...

        def run_string(self) -> Any:
            """C++ method: run_string"""
            ...

    @staticmethod
    def run_cssl(source: str) -> str:
        """C++ function: run_cssl"""
        ...

    @staticmethod
    def version() -> str:
        """C++ function: version"""
        ...

    @staticmethod
    def is_keyword(word: str) -> bool:
        """C++ function: is_keyword"""
        ...

    @staticmethod
    def str_concat(a: str, b: str) -> str:
        """C++ function: str_concat"""
        ...

    @staticmethod
    def str_contains(s: str, sub: str) -> bool:
        """C++ function: str_contains"""
        ...

    @staticmethod
    def str_join(parts: List[str], delim: str) -> str:
        """C++ function: str_join"""
        ...

    @staticmethod
    def str_lower(s: str) -> str:
        """C++ function: str_lower"""
        ...

    @staticmethod
    def str_replace(s: str, from: str, to: str) -> str:
        """C++ function: str_replace"""
        ...

    @staticmethod
    def str_split(s: str, delim: str) -> List[str]:
        """C++ function: str_split"""
        ...

    @staticmethod
    def str_trim(s: str) -> str:
        """C++ function: str_trim"""
        ...

    @staticmethod
    def str_upper(s: str) -> str:
        """C++ function: str_upper"""
        ...

    @staticmethod
    def str_reverse(s: str) -> str:
        """C++ function: str_reverse"""
        ...

    @staticmethod
    def str_len(s: str) -> Any:
        """C++ function: str_len"""
        ...

    @staticmethod
    def str_repeat(s: str, count: Any) -> str:
        """C++ function: str_repeat"""
        ...

    @staticmethod
    def str_startswith(s: str, prefix: str) -> bool:
        """C++ function: str_startswith"""
        ...

    @staticmethod
    def str_endswith(s: str, suffix: str) -> bool:
        """C++ function: str_endswith"""
        ...

    @staticmethod
    def str_indexof(s: str, sub: str) -> Any:
        """C++ function: str_indexof"""
        ...

    @staticmethod
    def str_substr(s: str, start: Any, length: Any = -1) -> str:
        """C++ function: str_substr"""
        ...

    @staticmethod
    def str_cmp(a: str, b: str) -> int:
        """C++ function: str_cmp"""
        ...

    @staticmethod
    def math_clamp(value: float, min_val: float, max_val: float) -> float:
        """C++ function: math_clamp"""
        ...

    @staticmethod
    def math_ipow(base: Any, exp: Any) -> Any:
        """C++ function: math_ipow"""
        ...

    @staticmethod
    def math_pow(base: float, exp: float) -> float:
        """C++ function: math_pow"""
        ...

    @staticmethod
    def math_mod(a: Any, b: Any) -> Any:
        """C++ function: math_mod"""
        ...

    @staticmethod
    def math_abs(x: float) -> float:
        """C++ function: math_abs"""
        ...

    @staticmethod
    def math_min(a: float, b: float) -> float:
        """C++ function: math_min"""
        ...

    @staticmethod
    def math_max(a: float, b: float) -> float:
        """C++ function: math_max"""
        ...

    @staticmethod
    def math_floor(x: float) -> Any:
        """C++ function: math_floor"""
        ...

    @staticmethod
    def math_ceil(x: float) -> Any:
        """C++ function: math_ceil"""
        ...

    @staticmethod
    def array_sum(arr: List[float]) -> float:
        """C++ function: array_sum"""
        ...

    @staticmethod
    def array_isum(arr: List[Any]) -> Any:
        """C++ function: array_isum"""
        ...

    @staticmethod
    def array_avg(arr: List[float]) -> float:
        """C++ function: array_avg"""
        ...

    @staticmethod
    def array_min(arr: List[float]) -> float:
        """C++ function: array_min"""
        ...

    @staticmethod
    def array_max(arr: List[float]) -> float:
        """C++ function: array_max"""
        ...

    @staticmethod
    def range(start: Any, end: Any, step: Any = 1) -> List[Any]:
        """C++ function: range"""
        ...

    @staticmethod
    def loop_check_lt(i: Any, end: Any) -> bool:
        """C++ function: loop_check_lt"""
        ...

    @staticmethod
    def loop_check_le(i: Any, end: Any) -> bool:
        """C++ function: loop_check_le"""
        ...

    @staticmethod
    def loop_check_gt(i: Any, end: Any) -> bool:
        """C++ function: loop_check_gt"""
        ...

    @staticmethod
    def loop_check_ge(i: Any, end: Any) -> bool:
        """C++ function: loop_check_ge"""
        ...

    @staticmethod
    def num_cmp(a: float, b: float) -> int:
        """C++ function: num_cmp"""
        ...

    @staticmethod
    def eq_int(a: Any, b: Any) -> bool:
        """C++ function: eq_int"""
        ...

    @staticmethod
    def eq_float(a: float, b: float) -> bool:
        """C++ function: eq_float"""
        ...

    @staticmethod
    def eq_str(a: str, b: str) -> bool:
        """C++ function: eq_str"""
        ...


