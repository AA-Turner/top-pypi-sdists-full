# coding=utf-8
# Copyright 2024 HuggingFace Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
import types
from textwrap import dedent

import pytest

from smolagents.local_python_executor import (
    InterpreterError,
    YieldException,
    evaluate_python_code,
    evaluate_yield,
)


class TestEvaluateYield:
    def test_evaluate_yield_simple(self):
        """Test basic yield evaluation."""
        yield_node = ast.parse("yield 42").body[0].value
        state = {}

        with pytest.raises(YieldException) as exc_info:
            evaluate_yield(yield_node, state, {}, {}, [])

        assert exc_info.value.value == 42

    def test_evaluate_yield_none(self):
        """Test yield with no value."""
        yield_node = ast.parse("yield").body[0].value
        state = {}

        with pytest.raises(YieldException) as exc_info:
            evaluate_yield(yield_node, state, {}, {}, [])

        assert exc_info.value.value is None

    def test_evaluate_yield_expression(self):
        """Test yield with expression."""
        yield_node = ast.parse("yield x + 1").body[0].value
        state = {"x": 5}

        with pytest.raises(YieldException) as exc_info:
            evaluate_yield(yield_node, state, {}, {}, [])

        assert exc_info.value.value == 6

    def test_evaluate_yield_from(self):
        """Test yield from evaluation."""
        yield_from_node = ast.parse("yield from [1, 2, 3]").body[0].value
        state = {}

        with pytest.raises(YieldException) as exc_info:
            evaluate_yield(yield_from_node, state, {}, {}, [])

        assert exc_info.value.value == [1, 2, 3]

    def test_evaluate_yield_from_generator(self):
        """Test yield from with generator expression."""
        yield_from_node = ast.parse("yield from (x for x in range(3))").body[0].value
        state = {}

        with pytest.raises(YieldException) as exc_info:
            evaluate_yield(yield_from_node, state, {"range": range}, {}, [])

        # The value should be a generator
        assert hasattr(exc_info.value.value, "__iter__")


class TestGeneratorFunctions:
    def test_simple_generator_function(self):
        """Test a simple generator function."""
        code = dedent("""
            def simple_gen():
                yield 1
                yield 2
                yield 3

            gen = simple_gen()
            result = list(gen)
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"list": list}, state=state)

        assert result == [1, 2, 3]
        assert isinstance(state["gen"], types.GeneratorType)

    def test_generator_with_return(self):
        """Test generator function with return statement."""
        code = dedent("""
            def gen_with_return():
                yield 1
                yield 2
                return "done"

            gen = gen_with_return()
            values = []
            try:
                while True:
                    values.append(next(gen))
            except StopIteration as e:
                return_value = e.value

            result = (values, return_value)
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"list": list, "next": next}, state=state)

        assert result == ([1, 2], "done")

    def test_generator_with_for_loop(self):
        """Test generator function with loop."""
        code = dedent("""
            def count_up_to(max_val):
                for count in range(1, max_val + 1):
                    yield count

            gen = count_up_to(5)
            result = list(gen)
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"list": list, "range": range}, state=state)

        assert result == [1, 2, 3, 4, 5]

    def test_generator_with_while_loop(self):
        """Test generator function with loop."""
        code = dedent("""
            def count_up_to(max_val):
                count = 1
                while count <= max_val:
                    yield count
                    count += 1

            gen = count_up_to(5)
            result = list(gen)
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"list": list}, state=state)

        assert result == [1, 2, 3, 4, 5]

    def test_generator_with_conditional_yield(self):
        """Test generator with conditional yield."""
        code = dedent("""
            def even_numbers(max_val):
                for i in range(max_val):
                    if i % 2 == 0:
                        yield i

            gen = even_numbers(10)
            result = list(gen)
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"list": list, "range": range}, state=state)

        assert result == [0, 2, 4, 6, 8]

    def test_generator_fibonacci(self):
        """Test Fibonacci generator."""
        code = dedent("""
            def fibonacci(n):
                a, b = 0, 1
                count = 0
                while count < n:
                    yield a
                    a, b = b, a + b
                    count += 1

            gen = fibonacci(7)
            result = list(gen)
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"list": list}, state=state)

        assert result == [0, 1, 1, 2, 3, 5, 8]

    def test_yield_from_generator(self):
        """Test yield from with another generator."""
        code = dedent("""
            def inner_gen():
                yield 1
                yield 2
                yield 3

            def outer_gen():
                yield from inner_gen()
                yield 4
                yield 5

            gen = outer_gen()
            result = list(gen)
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"list": list}, state=state)

        assert result == [1, 2, 3, 4, 5]

    def test_yield_from_iterable(self):
        """Test yield from with iterable."""
        code = dedent("""
            def delegate_to_list():
                yield from [1, 2, 3]
                yield from "abc"

            gen = delegate_to_list()
            result = list(gen)
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"list": list}, state=state)

        assert result == [1, 2, 3, "a", "b", "c"]

    def test_generator_expression_vs_function(self):
        """Test difference between generator expression and generator function."""
        code = dedent("""
            # Generator expression
            gen_expr = (x * 2 for x in range(5))

            # Generator function
            def gen_func():
                for x in range(5):
                    yield x * 2

            gen_from_func = gen_func()

            result_expr = list(gen_expr)
            result_func = list(gen_from_func)
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"list": list, "range": range}, state=state)

        assert state["result_expr"] == [0, 2, 4, 6, 8]
        assert state["result_func"] == [0, 2, 4, 6, 8]
        assert isinstance(state["gen_expr"], types.GeneratorType)
        assert isinstance(state["gen_from_func"], types.GeneratorType)

    def test_nested_generator_functions(self):
        """Test nested generator functions."""
        code = dedent("""
            def outer_generator():
                def inner_generator():
                    yield "inner1"
                    yield "inner2"

                yield "outer1"
                yield from inner_generator()
                yield "outer2"

            gen = outer_generator()
            result = list(gen)
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"list": list}, state=state)

        assert result == ["outer1", "inner1", "inner2", "outer2"]


class TestYieldErrorHandling:
    def test_yield_outside_function_raises_error(self):
        """Test that yield outside function raises error."""
        code = "yield 42"

        with pytest.raises(InterpreterError, match="Yield statements are only allowed inside generator functions"):
            evaluate_python_code(code)

    def test_yield_from_outside_function_raises_error(self):
        """Test that yield from outside function raises error."""
        code = "yield from [1, 2, 3]"

        with pytest.raises(InterpreterError, match="Yield statements are only allowed inside generator functions"):
            evaluate_python_code(code)

    def test_regular_function_with_no_yield(self):
        """Test that regular functions still work normally."""
        code = dedent("""
            def regular_function(x):
                return x * 2

            result = regular_function(21)
        """)

        state = {}
        result, _ = evaluate_python_code(code, state=state)

        assert result == 42
        assert not isinstance(state["regular_function"](), types.GeneratorType)


class TestYieldIntegration:
    def test_generator_in_list_comprehension(self):
        """Test using generator in list comprehension."""
        code = dedent("""
            def squares(n):
                for i in range(n):
                    yield i * i

            result = [x for x in squares(5)]
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"range": range}, state=state)

        assert result == [0, 1, 4, 9, 16]

    def test_generator_with_exception_handling(self):
        """Test generator with exception handling."""
        code = dedent("""
            def safe_generator():
                try:
                    yield 1
                    yield 2
                    raise ValueError("test error")
                    yield 3  # This should not be reached
                except ValueError:
                    yield "error handled"
                finally:
                    yield "cleanup"

            gen = safe_generator()
            result = list(gen)
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"list": list}, state=state)

        assert result == [1, 2, "error handled", "cleanup"]

    def test_generator_state_preservation(self):
        """Test that generator preserves state between yields."""
        code = dedent("""
            def stateful_generator():
                state = 0
                while state < 3:
                    state += 1
                    yield state

            gen = stateful_generator()
            first = next(gen)
            second = next(gen)
            third = next(gen)

            result = [first, second, third]
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"next": next}, state=state)

        assert result == [1, 2, 3]

    def test_multiple_generators(self):
        """Test multiple independent generators."""
        code = dedent("""
            def counter(start, end):
                current = start
                while current < end:
                    yield current
                    current += 1

            gen1 = counter(0, 3)
            gen2 = counter(10, 13)

            result1 = list(gen1)
            result2 = list(gen2)

            result = (result1, result2)
        """)

        state = {}
        result, _ = evaluate_python_code(code, {"list": list}, state=state)

        assert result == ([0, 1, 2], [10, 11, 12])
