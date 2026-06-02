"""심볼릭 회로 파라미터 (v0.7.1) — Qiskit ``Parameter`` 호환.

파라메트릭 회로를 한 번 만들고 :meth:`QuantumCircuit.assign_parameters` 로
값을 대입하는 표준 변분(VQE/QAOA) 워크플로를 지원한다.

``Parameter("θ")`` 는 자유 변수이며, 스칼라/다른 파라미터와의 사칙연산은
:class:`ParameterExpression` 을 만든다.  ``expr.bind({p: value})`` 로 부분/완전
대입한다.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, FrozenSet, Union

Number = Union[int, float]


class ParameterExpression:
    """파라미터들의 식 (선형/곱/초월함수 포함).

    내부적으로 자유 파라미터 집합과 평가 함수 ``func(values: dict) -> float`` 를
    들고 다닌다.  사칙연산 및 ``sin/cos/...`` 연산자가 새 식을 합성한다.
    """

    __slots__ = ("_params", "_func")

    def __init__(self, params: FrozenSet["Parameter"], func: Callable[[Dict], float]) -> None:
        self._params = params
        self._func = func

    @property
    def parameters(self) -> FrozenSet["Parameter"]:
        """이 식에 등장하는 자유 파라미터 집합."""
        return self._params

    def bind(self, values: Dict["Parameter", Number]) -> Union[float, "ParameterExpression"]:
        """``values`` 의 파라미터를 대입한다.

        모든 자유 파라미터가 주어지면 ``float`` 을, 일부만 주어지면 (부분 대입)
        남은 파라미터를 가진 새 :class:`ParameterExpression` 를 반환한다.
        """
        remaining = self._params - set(values)
        if not remaining:
            return float(self._func(values))
        captured = dict(values)
        func = self._func
        return ParameterExpression(frozenset(remaining), lambda d: func({**captured, **d}))

    # ---- 사칙연산 (스칼라 또는 다른 식/파라미터) ----
    def _combine(self, other, op: Callable[[float, float], float]) -> "ParameterExpression":
        f = self._func
        if isinstance(other, ParameterExpression):
            g = other._func
            return ParameterExpression(self._params | other._params, lambda d: op(f(d), g(d)))
        c = float(other)
        return ParameterExpression(self._params, lambda d: op(f(d), c))

    def __add__(self, o):
        return self._combine(o, lambda a, b: a + b)

    def __radd__(self, o):
        return self._combine(o, lambda a, b: b + a)

    def __sub__(self, o):
        return self._combine(o, lambda a, b: a - b)

    def __rsub__(self, o):
        return self._combine(o, lambda a, b: b - a)

    def __mul__(self, o):
        return self._combine(o, lambda a, b: a * b)

    def __rmul__(self, o):
        return self._combine(o, lambda a, b: b * a)

    def __truediv__(self, o):
        return self._combine(o, lambda a, b: a / b)

    def __rtruediv__(self, o):
        return self._combine(o, lambda a, b: b / a)

    def __neg__(self):
        f = self._func
        return ParameterExpression(self._params, lambda d: -f(d))

    def sin(self) -> "ParameterExpression":
        f = self._func
        return ParameterExpression(self._params, lambda d: math.sin(f(d)))

    def cos(self) -> "ParameterExpression":
        f = self._func
        return ParameterExpression(self._params, lambda d: math.cos(f(d)))

    def __str__(self) -> str:
        names = "·".join(sorted(p.name for p in self._params))
        return f"f({names})"

    def __format__(self, spec: str) -> str:
        # draw() 등이 ``f"{angle:.3g}"`` 로 포맷해도 깨지지 않도록 spec 무시.
        return str(self)

    def __repr__(self) -> str:
        names = ", ".join(sorted(p.name for p in self._params))
        return f"ParameterExpression(free={{{names}}})"


class Parameter(ParameterExpression):
    """이름을 가진 자유 회로 파라미터 (Qiskit ``Parameter`` 호환).

    동일성은 객체 정체성으로 판단한다 (같은 이름의 별개 인스턴스는 서로 다른
    파라미터) — 사용자가 만든 객체를 그대로 ``assign_parameters`` 에 넘긴다.
    """

    __slots__ = ("name", "_uid")
    _counter = 0

    def __init__(self, name: str) -> None:
        self.name = str(name)
        Parameter._counter += 1
        self._uid = Parameter._counter
        super().__init__(frozenset({self}), lambda d: d[self])

    def __hash__(self) -> int:
        return hash(self._uid)

    def __eq__(self, other) -> bool:
        return self is other

    def __str__(self) -> str:
        return self.name

    def __format__(self, spec: str) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Parameter({self.name!r})"


def is_parameterlike(x) -> bool:
    """``x`` 가 :class:`Parameter` / :class:`ParameterExpression` 인지."""
    return isinstance(x, ParameterExpression)


def resolve_value(x, values: Dict["Parameter", Number]):
    """게이트 파라미터 슬롯 값을 대입한다 (심볼릭이면 bind, 아니면 그대로)."""
    if isinstance(x, ParameterExpression):
        return x.bind(values)
    return x
