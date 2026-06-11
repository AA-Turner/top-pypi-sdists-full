"""사용자용 QuantumCircuit 클래스."""

from __future__ import annotations

import math
from typing import Any, Optional

import numpy as np

from .parameter import Parameter, ParameterExpression, is_parameterlike, resolve_value
from .qsim_python import Circuit as _RustCircuit
from .qsim_python import clifford_t_amplitude as _rust_clifford_t_amplitude
from .qsim_python import clifford_t_expectation as _rust_clifford_t_expectation
from .qsim_python import clifford_t_sample as _rust_clifford_t_sample
from .qsim_python import run as _rust_run
from .qsim_python import stabilizer_counts as _rust_stabilizer_counts
from .qsim_python import tensornet_amplitude as _rust_tn_amplitude
from .qsim_python import tensornet_amplitude_batch as _rust_tn_amplitude_batch
from .qsim_python import tensornet_amplitude_worker as _rust_tn_amplitude_worker
from .qsim_python import tensornet_contraction_cost as _rust_tn_cost
from .qsim_python import tensornet_expectation as _rust_tn_expectation
from .qsim_python import tensornet_plan as _rust_tn_plan
from .qsim_python import tensornet_run as _rust_tn_run
from .result import SimulationResult, _StabilizerRaw


def _ops_from_rust(
    rust_circuit: _RustCircuit,
) -> list[tuple[str, tuple[int, ...], tuple[Any, ...]]]:
    """Rust ``Circuit.instructions()`` → Python ``_ops`` 형식 변환.

    measure 의 cbit 은 f64 → int 로 cast (Python `_ops` 형 일치). 나머지 op 의
    params 는 그대로 float 유지.
    """
    ops: list[tuple[str, tuple[int, ...], tuple[Any, ...]]] = []
    for name, qubits, params in rust_circuit.instructions():
        q_tuple = tuple(qubits)
        if name == "measure":
            # cbit 만 들어 있음. f64 → int 복원.
            ops.append((name, q_tuple, (int(params[0]),)))
        else:
            ops.append((name, q_tuple, tuple(params)))
    return ops


# ----- 회로 조작 (copy / inverse / compose / power) 용 게이트 메타데이터 -----
# Hermitian (자기 자신이 역연산): U² = I.
_SELF_INVERSE_GATES = frozenset(
    {"h", "x", "y", "z", "cx", "cy", "cz", "ch", "swap", "ccx", "cswap", "id", "ecr"}
)
# adjoint 쌍 (S↔S†, T↔T†, √X↔√X†).
_ADJOINT_PAIR = {"s": "sdg", "sdg": "s", "t": "tdg", "tdg": "t", "sx": "sxdg", "sxdg": "sx"}
# 회전류: 같은 게이트에 모든 파라미터 부호 반전.
_PARAM_NEGATE_GATES = frozenset(
    {"rx", "ry", "rz", "rxx", "ryy", "rzz", "rzx", "crx", "cry", "crz",
     "p", "u1", "cp", "cu1", "xx_plus_yy", "xx_minus_yy"}
)
# 비-유니터리 (역연산 불가).
_NON_UNITARY_OPS = frozenset({"measure", "measure_all", "reset"})
# copy / compose 가 재생할 수 있는 모든 op 이름.
_REPLAYABLE_OPS = (
    _SELF_INVERSE_GATES
    | frozenset(_ADJOINT_PAIR)
    | _PARAM_NEGATE_GATES
    | _NON_UNITARY_OPS
    | frozenset({"u", "u2", "cu3", "cu", "iswap", "dcx", "unitary"})
)


def _replay_op(target: "QuantumCircuit", name: str, qubits: tuple, params: tuple) -> None:
    """단일 op 을 ``target`` 회로에 builder 메서드로 재생한다."""
    if name == "unitary":
        target.unitary(params[0], list(qubits))
    elif name == "measure":
        target.measure(qubits[0], int(params[0]))
    elif name == "measure_all":
        target.measure_all()
    elif name in _REPLAYABLE_OPS:
        # 모든 표준 게이트의 시그니처는 ``method(*params, *qubits)``.
        getattr(target, name)(*params, *qubits)
    else:
        raise NotImplementedError(
            f"회로 조작: 연산 {name!r} 은 재생 불가 (제어흐름 회로 미지원)"
        )


def _inverse_op(name: str, qubits: tuple, params: tuple) -> list:
    """단일 op 의 역연산을 (적용 순서대로) op 리스트로 반환한다."""
    import math as _math

    if name in _SELF_INVERSE_GATES:
        return [(name, qubits, params)]
    if name in _ADJOINT_PAIR:
        return [(_ADJOINT_PAIR[name], qubits, params)]
    if name in _PARAM_NEGATE_GATES:
        return [(name, qubits, tuple(-p for p in params))]
    if name == "u":  # u(θ,φ,λ)⁻¹ = u(-θ,-λ,-φ)
        th, ph, la = params
        return [("u", qubits, (-th, -la, -ph))]
    if name == "u2":  # u2(φ,λ)=u(π/2,φ,λ) → u(-π/2,-λ,-φ)
        ph, la = params
        return [("u", qubits, (-_math.pi / 2, -la, -ph))]
    if name == "cu3":  # cu3(θ,φ,λ)⁻¹ = cu3(-θ,-λ,-φ)
        th, ph, la = params
        return [("cu3", qubits, (-th, -la, -ph))]
    if name == "cu":  # cu(θ,φ,λ,γ)⁻¹ = cu(-θ,-λ,-φ,-γ)
        th, ph, la, ga = params
        return [("cu", qubits, (-th, -la, -ph, -ga))]
    if name == "iswap":  # iSWAP⁻¹ = iSWAP³ (iSWAP⁴ = I)
        return [("iswap", qubits, ())] * 3
    if name == "dcx":  # DCX(a,b)=CX(a,b);CX(b,a) → 역 = CX(b,a);CX(a,b)
        a, b = qubits
        return [("cx", (b, a), ()), ("cx", (a, b), ())]
    if name == "unitary":
        return [("unitary", qubits, (np.asarray(params[0]).conj().T,))]
    raise ValueError(
        f"inverse: 연산 {name!r} 의 역연산을 만들 수 없습니다 (측정/리셋/제어흐름 불가)"
    )


def _normalize_pauli_terms(observable, n_qubits: int) -> list:
    """observable → ``[(pauli_string, coeff_re, coeff_im), …]`` (TN expectation 용).

    ``dict`` / ``list[(str, coeff)]`` / Qiskit ``SparsePauliOp`` 를 받아 길이
    ``n_qubits`` 의 대문자 Pauli 라벨 (Qiskit 컨벤션) 로 정규화한다.
    """
    if hasattr(observable, "to_list") and not isinstance(observable, (list, tuple, dict)):
        items = list(observable.to_list())
    elif isinstance(observable, dict):
        items = list(observable.items())
    elif isinstance(observable, (list, tuple)):
        items = list(observable)
    else:
        raise TypeError(
            "observable 은 dict / list[(str, coeff)] / SparsePauliOp 여야 합니다 "
            f"(입력: {type(observable).__name__})"
        )
    terms = []
    for label, coeff in items:
        s = str(label).upper()
        if len(s) != n_qubits:
            raise ValueError(
                f"Pauli string 길이 {len(s)} != n_qubits {n_qubits} (label={label!r})"
            )
        for ch in s:
            if ch not in ("I", "X", "Y", "Z"):
                raise ValueError(f"잘못된 Pauli 문자 {ch!r} (I/X/Y/Z 만 허용)")
        c = complex(coeff)
        terms.append((s, float(c.real), float(c.imag)))
    return terms


class QuantumCircuit:
    """양자 회로를 구성하고 실행하는 메인 인터페이스.

    Args:
        n_qubits: 큐비트 수.

    Example:
        >>> qc = QuantumCircuit(2)
        >>> qc.h(0)
        >>> qc.cx(0, 1)
        >>> result = qc.run(shots=1024)
        >>> print(result.counts())
    """

    def __init__(self, n_qubits: int) -> None:
        if not isinstance(n_qubits, (int, np.integer)) or int(n_qubits) < 1:
            raise ValueError(
                f"n_qubits 는 1 이상의 정수여야 합니다 (입력: {n_qubits!r})"
            )
        self._raw_circuit = _RustCircuit(int(n_qubits))
        # OpRecord = (name, qubits, params). params 슬롯은 ``rx/ry/rz`` 의 회전 각도
        # (float) 외에도 ``unitary`` op 의 행렬 (np.ndarray) / ``measure`` op 의
        # cbit (int) 등을 보존한다 — to_qiskit / to_cirq 어댑터 (v0.3.5) 에서 활용.
        self._ops: list[tuple[str, tuple[int, ...], tuple[Any, ...]]] = []
        self._from_qasm: bool = False
        # v0.7.1: 심볼릭 Parameter 가 하나라도 쓰이면 True.  파라메트릭 회로는
        # _circuit (Rust) 가 불완전하므로 assign_parameters 로 바인딩 후 실행한다.
        self._parametric: bool = False
        # v0.6.2: ``with qc.if_test(...) as else_: ...`` then-only 패턴의 deferred
        # finalize.  __del__ (GC) 의존을 제거하기 위해 outer with 종료 시 pending
        # 으로 보관 후, 다음 회로 조작 (_circuit 접근) 시점에 flush.
        self._pending_builder: Optional[Any] = None

    @property
    def _circuit(self) -> _RustCircuit:
        # 회로를 건드리는 모든 메서드는 ``self._circuit.<x>(...)`` 패턴이므로
        # getter 진입에서 pending builder 를 flush 하면 결과적으로 deterministic
        # finalize 가 보장된다 (__del__ 의존 제거).
        self._flush_pending_builder()
        return self._raw_circuit

    @_circuit.setter
    def _circuit(self, value: _RustCircuit) -> None:
        # builder 들이 swap_in/swap_out 시 outer._circuit = nested 패턴으로 직접
        # 교체하므로 setter 는 단순 store 만 (여기서 flush 하면 swap 중 instruction
        # 이 잘못된 회로로 push 됨).
        self._raw_circuit = value

    def _flush_pending_builder(self) -> None:
        """``with qc.if_test(...) as else_: ...`` then-only 분기에서 outer with
        종료 시 보관된 pending builder 를 IfElse instruction 으로 flush.

        먼저 ``_pending_builder = None`` 으로 클리어한 뒤 ``_finalize()`` 를
        호출하므로 ``_finalize()`` 내부의 ``outer._circuit.add_if_else(...)`` 가
        property getter 를 다시 타도 무한 재귀하지 않는다.

        ``cls.__new__(cls)`` 우회 생성 (예: ``from_qasm``) 직후 _circuit setter
        호출 시 attribute 가 아직 없을 수 있어 ``getattr`` default."""
        pending = getattr(self, "_pending_builder", None)
        if pending is not None:
            self._pending_builder = None
            pending._finalize()

    @classmethod
    def from_qasm(cls, qasm: str) -> QuantumCircuit:
        """OpenQASM 2.0 또는 3.0 문자열로부터 회로를 구성한다.

        헤더 (``OPENQASM 2.0;`` 또는 ``OPENQASM 3.0;``) 가 버전을 결정한다. Qiskit /
        PennyLane 등이 emit 한 표준 회로를 그대로 import 할 수 있다.

        지원 게이트 (qelib1.inc / stdgates.inc): h/x/y/z/s/sdg/t/tdg/id, rx/ry/rz,
        u1/u2/u3/u/p, cx/CX/cy/cz/ch/swap, ccx/cswap, crx/cry/crz, cu1/cu3/cu/cp.

        지원 syntax: ``qreg q[N]`` / ``qubit[N] q``, ``creg c[N]`` / ``bit[N] c``,
        ``measure q[i] -> c[j]``, ``barrier`` (no-op), ``gate name(...) qubits {{ ... }}``
        user-defined gate (재귀 깊이 16 까지 inline).

        명시적 unsupported (명확한 ``ValueError`` + milestone 정보):
        ``if (c==N) ...`` / ``reset`` / ``opaque`` (v0.5),
        ``sx`` / ``sxdg`` / ``gphase`` (v0.3.1 transpiler 와 함께),
        3.0 의 ``for``/``while``/``box``/``def`` (v0.5).

        Args:
            qasm: OpenQASM 2.0 또는 3.0 소스 문자열.

        Returns:
            새 ``QuantumCircuit`` 객체.

        Raises:
            ValueError: 파싱 / lowering 실패 또는 unsupported feature.

        Example:
            >>> qc = QuantumCircuit.from_qasm('''
            ... OPENQASM 2.0;
            ... include "qelib1.inc";
            ... qreg q[2];
            ... h q[0];
            ... cx q[0], q[1];
            ... ''')
            >>> qc.num_qubits
            2
        """
        obj = cls.__new__(cls)
        obj._pending_builder = None
        obj._circuit = _RustCircuit.from_qasm(qasm)
        obj._ops = _ops_from_rust(obj._circuit)
        obj._from_qasm = True
        obj._parametric = False
        return obj

    def to_qasm(self, version: str = "2.0") -> str:
        """회로를 OpenQASM 문자열로 export 한다.

        Args:
            version: ``"2.0"`` (default) 또는 ``"3.0"``. 2.0 은 ``qreg``/``creg`` +
                ``include "qelib1.inc"``, 3.0 은 ``qubit[N]``/``bit[N]`` +
                ``include "stdgates.inc"`` 헤더를 emit. 게이트 매핑은 동일
                (``u3(θ,φ,λ)`` 형태).

        Returns:
            완성된 OpenQASM 문자열. ``qiskit.qasm2.loads()`` 또는
            ``qiskit.qasm3.loads()`` 가 직접 reparse 가능한 표준 형식.

        Raises:
            ValueError: ``version`` 이 ``"2.0"`` / ``"3.0"`` 가 아닐 때.

        Example:
            >>> qc = QuantumCircuit(2)
            >>> qc.h(0).cx(0, 1)
            >>> print(qc.to_qasm())
            OPENQASM 2.0;
            include "qelib1.inc";
            qreg q[2];
            h q[0];
            cx q[0],q[1];
        """
        self._ensure_bound("to_qasm")
        return self._circuit.to_qasm(version)

    @property
    def num_qubits(self) -> int:
        """큐비트 수를 반환한다."""
        return self._circuit.num_qubits()

    def size(self) -> int:
        """회로의 연산(게이트 + 측정) 총 개수를 반환한다 (Qiskit ``size()`` 호환).

        ``barrier`` 는 no-op 으로 기록되지 않으므로 제외된다.
        """
        return len(self._ops)

    def count_ops(self) -> dict[str, int]:
        """연산 이름별 개수를 반환한다 (Qiskit ``count_ops()`` 호환)."""
        counts: dict[str, int] = {}
        for name, _q, _p in self._ops:
            counts[name] = counts.get(name, 0) + 1
        return counts

    def depth(self) -> int:
        """회로 depth (per-qubit critical path 길이) 를 반환한다 (Qiskit ``depth()`` 호환).

        각 연산이 작용하는 큐비트들의 현재 layer 중 최대값 + 1 로 layer 를
        배정하고, 전체 최대 layer 를 depth 로 한다.  ``measure_all`` 은 모든
        큐비트를 touch.
        """
        n = self.num_qubits
        levels = [0] * n
        for name, qubits, _p in self._ops:
            touched = list(range(n)) if name == "measure_all" else [q for q in qubits if q < n]
            if not touched:
                continue
            new_level = max(levels[q] for q in touched) + 1
            for q in touched:
                levels[q] = new_level
        return max(levels) if levels else 0

    # ----- 심볼릭 파라미터 (v0.7.1) -----
    def _maybe_symbolic(self, name: str, qubits: tuple, params: tuple) -> bool:
        """파라미터 중 심볼릭이 있으면 op 을 기록 + 파라메트릭 표시 후 True 반환.

        게이트 메서드 상단에서 ``if self._maybe_symbolic(...): return self`` 로
        호출한다.  심볼릭 회로는 Rust ``_circuit`` 을 만들지 않고 ``_ops`` 만
        기록하며, :meth:`assign_parameters` 로 바인딩 후 실행한다.
        """
        if any(is_parameterlike(p) for p in params):
            self._parametric = True
            self._ops.append((name, qubits, params))
            return True
        return False

    @property
    def parameters(self) -> list[Parameter]:
        """회로에 등장하는 자유 파라미터 (이름 오름차순)."""
        seen: set = set()
        for _name, _q, params in self._ops:
            for p in params:
                if is_parameterlike(p):
                    seen |= set(p.parameters)
        return sorted(seen, key=lambda x: x.name)

    @property
    def num_parameters(self) -> int:
        """자유 파라미터 개수."""
        return len(self.parameters)

    def is_parameterized(self) -> bool:
        """자유 파라미터가 하나라도 있으면 True."""
        return self._parametric and len(self.parameters) > 0

    def assign_parameters(self, values, inplace: bool = False) -> QuantumCircuit:
        """파라미터에 값을 대입한 회로를 반환한다 (Qiskit ``assign_parameters`` 호환).

        Args:
            values: ``{Parameter: 값}`` dict, 또는 ``parameters`` (이름순) 에
                위치 대응하는 시퀀스.  부분 대입 가능 (남은 파라미터는 유지).
            inplace: ``True`` 면 self 를 대체하고 self 반환, ``False`` (기본) 면
                새 회로 반환.

        Returns:
            바인딩된 :class:`QuantumCircuit`.  모든 파라미터가 대입되면 concrete
            (실행 가능), 일부만 대입되면 여전히 파라메트릭.

        Raises:
            ValueError: dict 키가 회로 파라미터가 아니거나, 시퀀스 길이가
                파라미터 수와 불일치할 때.
        """
        free = self.parameters
        if isinstance(values, dict):
            bind_map = dict(values)
            unknown = set(bind_map) - set(free)
            if unknown:
                names = ", ".join(sorted(p.name for p in unknown))
                raise ValueError(f"assign_parameters: 회로에 없는 파라미터: {names}")
        else:
            seq = list(values)
            if len(seq) != len(free):
                raise ValueError(
                    f"assign_parameters: 값 개수 {len(seq)} 가 파라미터 수 "
                    f"{len(free)} 와 불일치 (순서: {[p.name for p in free]})"
                )
            bind_map = dict(zip(free, seq))

        new = QuantumCircuit(self.num_qubits)
        for name, qubits, params in self._ops:
            bound_params = tuple(resolve_value(p, bind_map) for p in params)
            _replay_op(new, name, qubits, bound_params)
        if inplace:
            self._raw_circuit = new._raw_circuit
            self._ops = new._ops
            self._parametric = new._parametric
            return self
        return new

    # 별칭 (Qiskit 구버전 호환).
    bind_parameters = assign_parameters

    def _ensure_bound(self, where: str) -> None:
        if self.is_parameterized():
            names = ", ".join(p.name for p in self.parameters)
            raise ValueError(
                f"{where}: 미바인딩 파라미터 ({names}) 가 있습니다. "
                f"assign_parameters() 로 값을 대입한 뒤 실행하세요."
            )

    # ----- 회로 조작 (v0.7.1) -----
    def copy(self) -> QuantumCircuit:
        """회로의 독립적인 사본을 반환한다 (Qiskit ``copy()`` 호환).

        모든 연산을 새 회로에 재생하므로 이후 변경이 서로 영향을 주지 않는다.
        제어흐름 (if/while/for/switch) 회로는 미지원 (``NotImplementedError``).
        """
        new = QuantumCircuit(self.num_qubits)
        for name, qubits, params in self._ops:
            _replay_op(new, name, qubits, params)
        return new

    def inverse(self) -> QuantumCircuit:
        """역회로 (adjoint) ``U†`` 를 새 회로로 반환한다 (Qiskit ``inverse()`` 호환).

        연산 순서를 뒤집고 각 게이트를 역연산으로 치환한다 (예: ``S→S†``,
        ``Rx(θ)→Rx(-θ)``, ``iSWAP→iSWAP³``, ``unitary→unitary†``).  uncompute
        / Hermitian 검증 / adjoint ansatz 에 쓰인다.

        Raises:
            ValueError: 측정 / 리셋 / 제어흐름 등 비-유니터리 연산이 있으면
                역회로를 정의할 수 없으므로 에러.
        """
        for name, _q, _p in self._ops:
            if name in _NON_UNITARY_OPS:
                raise ValueError(
                    f"inverse: 비-유니터리 연산 {name!r} 이 있어 역회로를 만들 수 없습니다"
                )
        new = QuantumCircuit(self.num_qubits)
        for name, qubits, params in reversed(self._ops):
            for iname, iq, ip in _inverse_op(name, qubits, params):
                _replay_op(new, iname, iq, ip)
        return new

    def compose(
        self, other: QuantumCircuit, qubits=None, inplace: bool = False
    ) -> QuantumCircuit:
        """다른 회로 ``other`` 를 이 회로 뒤에 이어붙인다 (Qiskit ``compose()`` 호환).

        Args:
            other: 이어붙일 회로.
            qubits: ``other`` 의 큐비트를 이 회로의 어느 큐비트에 매핑할지.
                ``None`` (기본) 이면 동일 인덱스 (``other`` 와 큐비트 수 동일 필요).
                길이 ``other.num_qubits`` 인 시퀀스면 ``other`` 의 큐비트 j 가
                ``qubits[j]`` 로 매핑된다.
            inplace: ``True`` 면 self 를 직접 수정하고 self 를 반환, ``False``
                (기본) 면 사본을 만들어 반환.

        Returns:
            합성된 회로.
        """
        if qubits is None:
            if other.num_qubits != self.num_qubits:
                raise ValueError(
                    f"compose: 큐비트 수 불일치 (self={self.num_qubits}, "
                    f"other={other.num_qubits}). qubits 매핑을 지정하세요"
                )
            mapping = list(range(other.num_qubits))
        else:
            mapping = [int(q) for q in qubits]
            if len(mapping) != other.num_qubits:
                raise ValueError(
                    f"compose: qubits 매핑 길이 {len(mapping)} 가 "
                    f"other.num_qubits {other.num_qubits} 와 불일치"
                )
            if any(q < 0 or q >= self.num_qubits for q in mapping):
                raise ValueError("compose: qubits 매핑이 self 범위를 벗어남")
        target = self if inplace else self.copy()
        for name, oqubits, params in other._ops:
            if name == "measure_all":
                raise NotImplementedError(
                    "compose: measure_all 은 미지원입니다 (measure(q, c) 를 사용하세요)"
                )
            mq = tuple(mapping[q] for q in oqubits)
            _replay_op(target, name, mq, params)
        return target

    def power(self, power: int) -> QuantumCircuit:
        """회로를 ``power`` 번 반복한 새 회로를 반환한다 (Qiskit ``power()`` 호환).

        ``power`` 가 음수면 역회로를 ``|power|`` 번 반복한다.  ``power == 0`` 은
        항등 회로 (빈 회로) 를 반환한다.  비-유니터리 연산이 있으면
        ``ValueError`` (``inverse`` 와 동일 제약).
        """
        n = int(power)
        if n == 0:
            return QuantumCircuit(self.num_qubits)
        # 양수 power 도 비-유니터리 op 검사 (inverse() 와 동일 제약 — docstring
        # 의 ValueError 약속을 모든 n != 0 에서 지킨다).
        for name, _q, _p in self._ops:
            if name in _NON_UNITARY_OPS:
                raise ValueError(
                    f"power: 비-유니터리 연산 {name!r} 이 있어 거듭제곱 회로를 "
                    f"만들 수 없습니다"
                )
        base = self if n > 0 else self.inverse()
        new = QuantumCircuit(self.num_qubits)
        for _ in range(abs(n)):
            for name, qubits, params in base._ops:
                _replay_op(new, name, qubits, params)
        return new

    def to_matrix(self) -> np.ndarray:
        """회로 전체의 유니터리 행렬 ``U ∈ ℂ^(2ⁿ × 2ⁿ)`` 를 반환한다 (Qiskit
        ``Operator(qc)`` 호환).

        각 계산 기저 상태 ``|j⟩`` 에 회로를 작용시켜 ``U`` 의 ``j`` 번째 열을
        얻는다 (statevector 백엔드).  게이트 항등식 검증 / 커스텀 유니터리
        추출 / 교육용.  ``U[i][j] = ⟨i|U|j⟩`` (little-endian, 큐비트 0 = LSB).

        Raises:
            ValueError: 측정 / 리셋 등 비-유니터리 연산이 있거나, 큐비트 수가
                12 를 초과 (메모리 ``O(4ⁿ)``) 할 때.
        """
        self._ensure_bound("to_matrix")
        for name, _q, _p in self._ops:
            if name in _NON_UNITARY_OPS:
                raise ValueError(
                    f"to_matrix: 비-유니터리 연산 {name!r} 이 있어 유니터리 행렬이 없습니다"
                )
        n = self.num_qubits
        if n > 12:
            raise ValueError(f"to_matrix: 큐비트 수 {n} > 12 (행렬 2^{n}² 메모리 과다)")
        dim = 1 << n
        mat = np.empty((dim, dim), dtype=np.complex128)
        for j in range(dim):
            col = QuantumCircuit(n)
            for q in range(n):
                if (j >> q) & 1:
                    col.x(q)
            for name, qubits, params in self._ops:
                _replay_op(col, name, qubits, params)
            mat[:, j] = np.asarray(col.run(shots=0).statevector(), dtype=np.complex128)
        return mat

    # 단일 큐비트 게이트
    def h(self, qubit: int) -> QuantumCircuit:
        """Hadamard 게이트를 적용한다."""
        self._circuit.h(qubit)
        self._ops.append(("h", (qubit,), ()))
        return self

    def x(self, qubit: int) -> QuantumCircuit:
        """Pauli-X (NOT) 게이트를 적용한다."""
        self._circuit.x(qubit)
        self._ops.append(("x", (qubit,), ()))
        return self

    def y(self, qubit: int) -> QuantumCircuit:
        """Pauli-Y 게이트를 적용한다."""
        self._circuit.y(qubit)
        self._ops.append(("y", (qubit,), ()))
        return self

    def z(self, qubit: int) -> QuantumCircuit:
        """Pauli-Z 게이트를 적용한다."""
        self._circuit.z(qubit)
        self._ops.append(("z", (qubit,), ()))
        return self

    def s(self, qubit: int) -> QuantumCircuit:
        """S (Phase) 게이트를 적용한다."""
        self._circuit.s(qubit)
        self._ops.append(("s", (qubit,), ()))
        return self

    def sdg(self, qubit: int) -> QuantumCircuit:
        """S† (S-dagger) 게이트를 적용한다."""
        self._circuit.sdg(qubit)
        self._ops.append(("sdg", (qubit,), ()))
        return self

    def t(self, qubit: int) -> QuantumCircuit:
        """T 게이트를 적용한다."""
        self._circuit.t(qubit)
        self._ops.append(("t", (qubit,), ()))
        return self

    def tdg(self, qubit: int) -> QuantumCircuit:
        """T† (T-dagger) 게이트를 적용한다."""
        self._circuit.tdg(qubit)
        self._ops.append(("tdg", (qubit,), ()))
        return self

    def sx(self, qubit: int) -> QuantumCircuit:
        """√X (Sx) 게이트를 적용한다 (v0.4.6).  IBM Falcon/Eagle hardware-native."""
        self._circuit.sx(qubit)
        self._ops.append(("sx", (qubit,), ()))
        return self

    def sxdg(self, qubit: int) -> QuantumCircuit:
        """√X† (Sxdg) 게이트를 적용한다 (v0.4.6)."""
        self._circuit.sxdg(qubit)
        self._ops.append(("sxdg", (qubit,), ()))
        return self

    def p(self, lambda_: float, qubit: int) -> QuantumCircuit:
        """Phase 게이트 ``P(λ) = diag(1, e^iλ)`` 를 적용한다 (v0.4.6).

        Qiskit ``p(λ)`` / ``u1(λ)`` 와 동일.  ``P(0)=I``, ``P(π/4)=T``,
        ``P(π/2)=S``, ``P(π)=Z`` 의 일반화.
        """
        if self._maybe_symbolic("p", (qubit,), (lambda_,)):
            return self
        self._circuit.p(float(lambda_), qubit)
        self._ops.append(("p", (qubit,), (float(lambda_),)))
        return self

    def u1(self, lambda_: float, qubit: int) -> QuantumCircuit:
        """``U1(λ)`` — ``P(λ)`` 의 Qiskit alias (v0.4.6).

        내부적으로 ``P(λ)`` 와 동일 회로를 만들지만 ``_ops`` 에는 ``"u1"`` 이름으로
        기록되어 ``draw()`` / ``to_qiskit()`` / ``to_qasm()`` 의 표기가 보존된다.
        """
        if self._maybe_symbolic("u1", (qubit,), (lambda_,)):
            return self
        self._circuit.p(float(lambda_), qubit)
        self._ops.append(("u1", (qubit,), (float(lambda_),)))
        return self

    def u2(self, phi: float, lambda_: float, qubit: int) -> QuantumCircuit:
        """``U2(φ, λ) = U(π/2, φ, λ)`` 게이트 (v0.4.6)."""
        if self._maybe_symbolic("u2", (qubit,), (phi, lambda_)):
            return self
        self._circuit.u2(float(phi), float(lambda_), qubit)
        self._ops.append(("u2", (qubit,), (float(phi), float(lambda_))))
        return self

    def u(self, theta: float, phi: float, lambda_: float, qubit: int) -> QuantumCircuit:
        """``U(θ, φ, λ)`` (= Qiskit ``u3``) 일반 1-큐비트 유니터리 (v0.4.6)."""
        if self._maybe_symbolic("u", (qubit,), (theta, phi, lambda_)):
            return self
        self._circuit.u(float(theta), float(phi), float(lambda_), qubit)
        self._ops.append(("u", (qubit,), (float(theta), float(phi), float(lambda_))))
        return self

    def rx(self, theta: float, qubit: int) -> QuantumCircuit:
        """X축 회전 게이트를 적용한다."""
        if self._maybe_symbolic("rx", (qubit,), (theta,)):
            return self
        self._circuit.rx(theta, qubit)
        self._ops.append(("rx", (qubit,), (float(theta),)))
        return self

    def ry(self, theta: float, qubit: int) -> QuantumCircuit:
        """Y축 회전 게이트를 적용한다."""
        if self._maybe_symbolic("ry", (qubit,), (theta,)):
            return self
        self._circuit.ry(theta, qubit)
        self._ops.append(("ry", (qubit,), (float(theta),)))
        return self

    def rz(self, theta: float, qubit: int) -> QuantumCircuit:
        """Z축 회전 게이트를 적용한다."""
        if self._maybe_symbolic("rz", (qubit,), (theta,)):
            return self
        self._circuit.rz(theta, qubit)
        self._ops.append(("rz", (qubit,), (float(theta),)))
        return self

    def id(self, qubit: int) -> QuantumCircuit:
        """Identity 게이트를 적용한다."""
        self._circuit.id(qubit)
        self._ops.append(("id", (qubit,), ()))
        return self

    # 2큐비트 게이트
    def cx(self, control: int, target: int) -> QuantumCircuit:
        """CNOT (Controlled-X) 게이트를 적용한다."""
        self._circuit.cx(control, target)
        self._ops.append(("cx", (control, target), ()))
        return self

    def cz(self, qubit0: int, qubit1: int) -> QuantumCircuit:
        """Controlled-Z 게이트를 적용한다."""
        self._circuit.cz(qubit0, qubit1)
        self._ops.append(("cz", (qubit0, qubit1), ()))
        return self

    def swap(self, qubit0: int, qubit1: int) -> QuantumCircuit:
        """SWAP 게이트를 적용한다."""
        self._circuit.swap(qubit0, qubit1)
        self._ops.append(("swap", (qubit0, qubit1), ()))
        return self

    def iswap(self, qubit0: int, qubit1: int) -> QuantumCircuit:
        """iSWAP 게이트를 적용한다 (v0.7)."""
        self._circuit.iswap(qubit0, qubit1)
        self._ops.append(("iswap", (qubit0, qubit1), ()))
        return self

    def rxx(self, theta: float, qubit0: int, qubit1: int) -> QuantumCircuit:
        """``RXX(θ) = exp(-iθ/2 X⊗X)`` 게이트를 적용한다 (v0.7)."""
        if self._maybe_symbolic("rxx", (qubit0, qubit1), (theta,)):
            return self
        self._circuit.rxx(theta, qubit0, qubit1)
        self._ops.append(("rxx", (qubit0, qubit1), (theta,)))
        return self

    def ryy(self, theta: float, qubit0: int, qubit1: int) -> QuantumCircuit:
        """``RYY(θ) = exp(-iθ/2 Y⊗Y)`` 게이트를 적용한다 (v0.7)."""
        if self._maybe_symbolic("ryy", (qubit0, qubit1), (theta,)):
            return self
        self._circuit.ryy(theta, qubit0, qubit1)
        self._ops.append(("ryy", (qubit0, qubit1), (theta,)))
        return self

    def rzz(self, theta: float, qubit0: int, qubit1: int) -> QuantumCircuit:
        """``RZZ(θ) = exp(-iθ/2 Z⊗Z)`` 게이트를 적용한다 (v0.7).  QAOA/Ising 기본."""
        if self._maybe_symbolic("rzz", (qubit0, qubit1), (theta,)):
            return self
        self._circuit.rzz(theta, qubit0, qubit1)
        self._ops.append(("rzz", (qubit0, qubit1), (theta,)))
        return self

    def dcx(self, qubit0: int, qubit1: int) -> QuantumCircuit:
        """DCX (double-CNOT) 게이트를 적용한다 (v0.7.1)."""
        self._circuit.dcx(qubit0, qubit1)
        self._ops.append(("dcx", (qubit0, qubit1), ()))
        return self

    def ecr(self, qubit0: int, qubit1: int) -> QuantumCircuit:
        """ECR (echoed cross-resonance) 게이트를 적용한다 (v0.7.1).  IBM native."""
        self._circuit.ecr(qubit0, qubit1)
        self._ops.append(("ecr", (qubit0, qubit1), ()))
        return self

    def rzx(self, theta: float, qubit0: int, qubit1: int) -> QuantumCircuit:
        """``RZX(θ) = exp(-iθ/2 Z⊗X)`` 게이트를 적용한다 (v0.7.1)."""
        if self._maybe_symbolic("rzx", (qubit0, qubit1), (theta,)):
            return self
        self._circuit.rzx(theta, qubit0, qubit1)
        self._ops.append(("rzx", (qubit0, qubit1), (theta,)))
        return self

    def xx_plus_yy(self, theta: float, qubit0: int, qubit1: int) -> QuantumCircuit:
        """``XXPlusYY(θ)`` excitation-preserving 게이트 (v0.7.1)."""
        if self._maybe_symbolic("xx_plus_yy", (qubit0, qubit1), (theta,)):
            return self
        self._circuit.xx_plus_yy(theta, qubit0, qubit1)
        self._ops.append(("xx_plus_yy", (qubit0, qubit1), (theta,)))
        return self

    def xx_minus_yy(self, theta: float, qubit0: int, qubit1: int) -> QuantumCircuit:
        """``XXMinusYY(θ)`` 게이트 (v0.7.1)."""
        if self._maybe_symbolic("xx_minus_yy", (qubit0, qubit1), (theta,)):
            return self
        self._circuit.xx_minus_yy(theta, qubit0, qubit1)
        self._ops.append(("xx_minus_yy", (qubit0, qubit1), (theta,)))
        return self

    def cy(self, control: int, target: int) -> QuantumCircuit:
        """Controlled-Y 게이트를 적용한다 (v0.4.6)."""
        self._circuit.cy(control, target)
        self._ops.append(("cy", (control, target), ()))
        return self

    def ch(self, control: int, target: int) -> QuantumCircuit:
        """Controlled-H 게이트를 적용한다 (v0.4.6)."""
        self._circuit.ch(control, target)
        self._ops.append(("ch", (control, target), ()))
        return self

    def crx(self, theta: float, control: int, target: int) -> QuantumCircuit:
        """Controlled-Rx(θ) 게이트를 적용한다 (v0.4.6)."""
        if self._maybe_symbolic("crx", (control, target), (theta,)):
            return self
        self._circuit.crx(float(theta), control, target)
        self._ops.append(("crx", (control, target), (float(theta),)))
        return self

    def cry(self, theta: float, control: int, target: int) -> QuantumCircuit:
        """Controlled-Ry(θ) 게이트를 적용한다 (v0.4.6)."""
        if self._maybe_symbolic("cry", (control, target), (theta,)):
            return self
        self._circuit.cry(float(theta), control, target)
        self._ops.append(("cry", (control, target), (float(theta),)))
        return self

    def crz(self, theta: float, control: int, target: int) -> QuantumCircuit:
        """Controlled-Rz(θ) 게이트를 적용한다 (v0.4.6)."""
        if self._maybe_symbolic("crz", (control, target), (theta,)):
            return self
        self._circuit.crz(float(theta), control, target)
        self._ops.append(("crz", (control, target), (float(theta),)))
        return self

    def cp(self, lambda_: float, control: int, target: int) -> QuantumCircuit:
        """Controlled-Phase(λ) 게이트를 적용한다 (v0.4.6).

        Qiskit ``cp(λ)`` / ``cu1(λ)`` 와 동일.
        """
        if self._maybe_symbolic("cp", (control, target), (lambda_,)):
            return self
        self._circuit.cp(float(lambda_), control, target)
        self._ops.append(("cp", (control, target), (float(lambda_),)))
        return self

    def cu1(self, lambda_: float, control: int, target: int) -> QuantumCircuit:
        """``cu1(λ)`` — ``cp(λ)`` 의 Qiskit alias (v0.4.6).

        내부적으로 ``CP(λ)`` 와 동일하지만 ``_ops`` 에 ``"cu1"`` 이름 보존.
        """
        if self._maybe_symbolic("cu1", (control, target), (lambda_,)):
            return self
        self._circuit.cp(float(lambda_), control, target)
        self._ops.append(("cu1", (control, target), (float(lambda_),)))
        return self

    def cu3(
        self, theta: float, phi: float, lambda_: float, control: int, target: int
    ) -> QuantumCircuit:
        """Controlled-U3(θ, φ, λ) 게이트를 적용한다 (v0.4.6)."""
        if self._maybe_symbolic("cu3", (control, target), (theta, phi, lambda_)):
            return self
        self._circuit.cu3(float(theta), float(phi), float(lambda_), control, target)
        self._ops.append(
            ("cu3", (control, target), (float(theta), float(phi), float(lambda_)))
        )
        return self

    def cu(
        self,
        theta: float,
        phi: float,
        lambda_: float,
        gamma: float,
        control: int,
        target: int,
    ) -> QuantumCircuit:
        """Controlled-U(θ, φ, λ, γ) 게이트 (v0.4.6).

        Qiskit ``cu(θ, φ, λ, γ)`` 와 동일.  ``γ`` 는 control activation phase.
        """
        if self._maybe_symbolic("cu", (control, target), (theta, phi, lambda_, gamma)):
            return self
        self._circuit.cu(
            float(theta), float(phi), float(lambda_), float(gamma), control, target
        )
        self._ops.append(
            (
                "cu",
                (control, target),
                (float(theta), float(phi), float(lambda_), float(gamma)),
            )
        )
        return self

    # 3큐비트 게이트
    def ccx(self, ctrl1: int, ctrl2: int, target: int) -> QuantumCircuit:
        """Toffoli (CCX) 게이트를 적용한다."""
        self._circuit.ccx(ctrl1, ctrl2, target)
        self._ops.append(("ccx", (ctrl1, ctrl2, target), ()))
        return self

    def cswap(self, control: int, target1: int, target2: int) -> QuantumCircuit:
        """Fredkin (CSWAP) 게이트를 적용한다."""
        self._circuit.cswap(control, target1, target2)
        self._ops.append(("cswap", (control, target1, target2), ()))
        return self

    # 다중 제어 게이트 (v0.7.1) — ancilla-free, native 게이트로 분해 (전 백엔드).
    def mcx(self, control_qubits, target: int) -> QuantumCircuit:
        """다중 제어 X (``Cⁿ(X)``) 게이트 (Qiskit ``mcx`` 호환).

        ``control_qubits`` 가 모두 ``|1⟩`` 일 때만 ``target`` 에 X 를 적용한다.
        ancilla 없이 native 게이트 (cx/ccx/h/cp) 로 정확히 분해 (Cⁿ(Z) =
        H·Cⁿ(X)·H, 위상 절반 재귀) — 모든 백엔드 + QASM + transpile 동작.
        Grover oracle / 산술 회로 등에 사용.  게이트 수 ``O(2ⁿ)``.

        Args:
            control_qubits: 제어 큐비트 인덱스 시퀀스 (또는 단일 int).
            target: 대상 큐비트.
        """
        controls = [int(control_qubits)] if isinstance(control_qubits, (int, np.integer)) else [int(q) for q in control_qubits]
        self._mcx(controls, int(target))
        return self

    def mcp(self, lam: float, control_qubits, target: int) -> QuantumCircuit:
        """다중 제어 위상 (``Cⁿ(P(λ))``) 게이트 (Qiskit ``mcp`` 호환).

        모든 제어 + target 이 ``|1⟩`` 인 기저상태에 위상 ``e^{iλ}`` 를 더한다
        (대각, 제어/타깃 대칭).  ancilla-free native 분해.
        """
        controls = [int(control_qubits)] if isinstance(control_qubits, (int, np.integer)) else [int(q) for q in control_qubits]
        # lam 은 심볼릭 가능 — 재귀의 cp/p 가 처리하므로 float() 강제 안 함.
        self._mcp(lam if is_parameterlike(lam) else float(lam), controls, int(target))
        return self

    def mcz(self, control_qubits, target: int) -> QuantumCircuit:
        """다중 제어 Z (``Cⁿ(Z)`` = ``Cⁿ(P(π))``) 게이트."""
        return self.mcp(math.pi, control_qubits, target)

    def mcrx(self, theta: float, control_qubits, target: int) -> QuantumCircuit:
        """다중 제어 Rx (``Cⁿ(Rx(θ))``) — 모든 제어가 ``|1⟩`` 일 때만 적용 (Qiskit `mcrx`)."""
        return self._mcr("x", theta if is_parameterlike(theta) else float(theta), control_qubits, int(target))

    def mcry(self, theta: float, control_qubits, target: int) -> QuantumCircuit:
        """다중 제어 Ry (``Cⁿ(Ry(θ))``) (Qiskit `mcry`)."""
        return self._mcr("y", theta if is_parameterlike(theta) else float(theta), control_qubits, int(target))

    def mcrz(self, theta: float, control_qubits, target: int) -> QuantumCircuit:
        """다중 제어 Rz (``Cⁿ(Rz(θ))``) (Qiskit `mcrz`)."""
        return self._mcr("z", theta if is_parameterlike(theta) else float(theta), control_qubits, int(target))

    def _mcr(self, axis: str, theta: float, control_qubits, target: int) -> QuantumCircuit:
        controls = [int(control_qubits)] if isinstance(control_qubits, (int, np.integer)) else [int(q) for q in control_qubits]
        self._mcr_rec(axis, theta, controls, target)
        return self

    def _mcr_rec(self, axis: str, theta: float, controls: list[int], target: int) -> None:
        cr = {"x": self.crx, "y": self.cry, "z": self.crz}[axis]
        if len(controls) == 0:
            {"x": self.rx, "y": self.ry, "z": self.rz}[axis](theta, target)
        elif len(controls) == 1:
            cr(theta, controls[0], target)
        else:
            c_last = controls[-1]
            rest = controls[:-1]
            cr(theta / 2, c_last, target)
            self._mcx(rest, c_last)
            cr(-theta / 2, c_last, target)
            self._mcx(rest, c_last)
            self._mcr_rec(axis, theta / 2, rest, target)

    def _mcx(self, controls: list[int], target: int) -> None:
        if len(controls) == 0:
            self.x(target)
        elif len(controls) == 1:
            self.cx(controls[0], target)
        elif len(controls) == 2:
            self.ccx(controls[0], controls[1], target)
        else:
            self.h(target)
            self._mcp(math.pi, controls, target)
            self.h(target)

    def _mcp(self, lam: float, controls: list[int], target: int) -> None:
        if len(controls) == 0:
            self.p(lam, target)
        elif len(controls) == 1:
            self.cp(lam, controls[0], target)
        else:
            c_last = controls[-1]
            rest = controls[:-1]
            self.cp(lam / 2, c_last, target)
            self._mcx(rest, c_last)
            self.cp(-lam / 2, c_last, target)
            self._mcx(rest, c_last)
            self._mcp(lam / 2, rest, target)

    # 임의 unitary + transpile
    def unitary(
        self,
        matrix,
        qubits,
        validate: bool = True,
        decompose=False,
    ) -> QuantumCircuit:
        """임의 k-큐비트 (k ≥ 1) unitary 행렬을 큐비트들에 적용한다.

        - **1-큐비트** (``qubits`` 가 int 이거나 길이 1): Z-Y-Z 분해
          (Nielsen-Chuang Thm 4.1) 로 native 게이트 ``Rz(δ); Ry(γ); Rz(β)``
          를 추가하고 글로벌 phase α 는 회로 메타데이터에 누적된다.  모든
          백엔드 (statevector / density / mps / gpu) 에서 동작.
        - **k ≥ 2 큐비트** (v0.6.8): 행렬을 그대로 보존해 statevector 백엔드
          에서 직접 적용한다 (``apply_multi_qubit_gate``).  density / mps /
          gpu 백엔드는 ``ValueError`` (``method='statevector'`` 사용).
        - **k ≥ 2 + ``decompose=True``** (v0.7.1): 2-큐비트는 KAK / Cartan,
          그 이상은 Quantum Shannon Decomposition 으로 단일 큐비트 게이트 +
          native ``RXX/RYY/RZZ`` / ``CX`` 의 곱으로 변환한다.  행렬을 보존하지
          않고 native 게이트만 추가하므로 **모든 백엔드** (mps / density / gpu)
          + QASM export + transpile 에서 동작한다.  (전역 위상까지 보존 —
          Qiskit ``Operator`` 와 일치.)  게이트 수 ``O(4^k)``.
        - **k ≥ 2 + ``decompose="cx"``** (v0.7.3): 하드웨어 basis (``CX`` + 단일
          큐비트) 타깃의 **CNOT-개수 최적** 분해.  2-큐비트는 Weyl chamber 정준
          좌표로 0/1/2/3-CNOT 을 판정해 최소 CNOT 회로를 emit (Qiskit
          ``TwoQubitBasisDecomposer(CXGate)`` 와 CNOT 개수 + 행렬 1e-9 일치),
          k≥3 은 QSD 의 2-큐비트 종료를 CX 기저로 한다.  실 하드웨어 transpile
          의 2-큐비트 게이트 수 최소화에 쓰인다.

        행렬의 sub-index 비트 ``j`` 가 ``qubits[j]`` 에 대응한다 (``qubits[0]``
        = LSB) — Qiskit 의 ``UnitaryGate`` 와 동일 컨벤션.

        Args:
            matrix: ``2^k × 2^k`` unitary. ``numpy.ndarray`` 또는
                list-of-list (자동 변환).
            qubits: 적용할 큐비트.  int (1-큐비트) 또는 정수 시퀀스.
            validate: ``True`` (default) 면 ``M·M† ≈ I`` (1e-10) 를 확인하고
                위반 시 ``ValueError``. ``False`` 면 검증 생략.
            decompose: ``True`` 면 k≥2 행렬을 native 게이트로 분해 (2-큐비트
                KAK, 그 이상 QSD; 전 백엔드 호환).  ``"cx"`` 면 하드웨어 basis
                (CX + 단일 큐비트) CNOT-개수 최적 분해.  k=1 은 항상 ZYZ (무시).

        Returns:
            ``self`` (fluent chaining 용).
        """
        import numpy as np

        arr = np.asarray(matrix, dtype=np.complex128)
        if isinstance(qubits, (int, np.integer)):
            qubit_tuple = (int(qubits),)
        else:
            qubit_tuple = tuple(int(q) for q in qubits)
        k = len(qubit_tuple)
        if k == 0:
            raise ValueError("unitary: qubits 는 비어 있을 수 없습니다")
        dim = 1 << k
        if arr.shape != (dim, dim):
            raise ValueError(
                f"unitary: matrix shape {arr.shape} 가 qubits 수 {k} "
                f"(2^k = {dim}) 와 불일치합니다"
            )
        if validate:
            # M·M† ≈ I (일반 k-큐비트 unitarity).
            ident = np.eye(dim, dtype=np.complex128)
            if not np.allclose(arr @ arr.conj().T, ident, atol=1e-10):
                raise ValueError(
                    "unitary: 입력 행렬이 unitary 가 아닙니다 (M·M† ≠ I, 1e-10)"
                )

        if decompose and k >= 2:
            basis = "cx" if decompose == "cx" else "native"
            self._apply_unitary_decomposed(arr, qubit_tuple, basis)
            return self

        if k == 1:
            # 1-큐비트는 ZYZ 분해 → native 게이트 (모든 백엔드 호환).
            self._circuit.unitary(arr, qubit_tuple[0], validate)
        else:
            # k ≥ 2 는 행렬 직접 적용 (statevector 전용).
            self._circuit.apply_unitary(arr, list(qubit_tuple))
        # to_qiskit / to_cirq 가 그대로 emit 할 수 있게 행렬을 params 슬롯에 보존.
        self._ops.append(("unitary", qubit_tuple, (arr,)))
        return self

    def _apply_unitary_decomposed(
        self, arr, qubit_tuple: tuple[int, ...], basis: str = "native"
    ) -> None:
        """임의 k-큐비트 (k≥2) unitary 를 QSD 로 native 게이트로 추가한다 (전 백엔드).

        2-큐비트는 KAK (``basis="native"``) 또는 CNOT-개수 최적 (``basis="cx"``),
        그 이상은 Quantum Shannon Decomposition.  1-큐비트 op 은 ``self.unitary``
        (ZYZ, 위상 추적) 로, 회전류는 native 게이트로 emit 하므로 전역 위상까지
        정확하고 copy/inverse/to_matrix 재생도 안전하다.
        """
        from .synthesis import quantum_shannon_decompose

        for op in quantum_shannon_decompose(arr, list(qubit_tuple), basis):
            kind = op[0]
            if kind == "u1":
                self.unitary(op[1], op[2])
            elif kind == "cx":
                self.cx(op[1], op[2])
            elif kind == "rx":
                self.rx(op[1], op[2])
            elif kind == "ry":
                self.ry(op[1], op[2])
            elif kind == "rz":
                self.rz(op[1], op[2])
            elif kind == "rxx":
                self.rxx(op[1], op[2], op[3])
            elif kind == "ryy":
                self.ryy(op[1], op[2], op[3])
            elif kind == "rzz":
                self.rzz(op[1], op[2], op[3])

    def initialize(self, state, qubits=None) -> QuantumCircuit:
        """큐비트를 임의의 상태로 초기화한다 (v0.7.1, Qiskit ``initialize`` 호환).

        대상 큐비트를 ``|0…0⟩`` 로 **reset** 한 뒤 목표 상태를 준비하는 게이트
        시퀀스를 추가한다 (Qiskit ``QuantumCircuit.initialize`` 와 동일 의미).
        진폭 인코딩 (QML), 화학/물리 초기 상태 준비 등 연구 워크플로에 쓰인다.

        ``state`` 는 세 형태를 허용한다:

        - **statevector** (1-D array-like, 길이 ``2^k``): 임의의 정규화된
          상태.  Möttönen uniformly-controlled rotation 으로 native RY/RZ +
          CNOT 준비 회로를 만들어 적용한다 (게이트 ``O(2^k)``, 전체 행렬을
          만들지 않음) — 모든 백엔드 (statevector / MPS / density / GPU) 에서
          동작한다.  ``state[i]`` 의 비트 ``j`` 가 ``qubits[j]`` 에 대응
          (little-endian, Qiskit 와 동일).
        - **정수** (``int``): 계산 기저 상태 ``|state⟩``.  큐비트별 ``X`` 만
          쓰므로 큰 레지스터에서도 ``O(k)``.
        - **라벨 문자열** (``str``, 문자 ``0 1 + - r l``): 곱 상태.  Qiskit
          컨벤션 — **가장 왼쪽 문자가 가장 높은 큐비트** (``qubits[-1]``).
          예) ``"01"`` → ``qubits[1]=|0⟩``, ``qubits[0]=|1⟩``.

        Args:
            state: 목표 상태 (statevector / int / 라벨 문자열).
            qubits: 초기화할 큐비트.  ``None`` (기본) → 전체 레지스터.  int
                (단일) 또는 정수 시퀀스.

        Returns:
            ``self`` (fluent chaining).

        Raises:
            ValueError: 길이/차원 불일치, statevector 가 정규화되지 않음
                (1e-8), 라벨 문자가 잘못됨.
        """
        import numpy as np

        if qubits is None:
            qubit_tuple = tuple(range(self.num_qubits))
        elif isinstance(qubits, (int, np.integer)):
            qubit_tuple = (int(qubits),)
        else:
            qubit_tuple = tuple(int(q) for q in qubits)
        k = len(qubit_tuple)
        if k == 0:
            raise ValueError("initialize: qubits 는 비어 있을 수 없습니다")

        # --- 정수 계산 기저 상태: 큐비트별 X (O(k)) ---
        if isinstance(state, (int, np.integer)):
            val = int(state)
            if val < 0 or val >= (1 << k):
                raise ValueError(f"initialize: 정수 {val} 가 0..2^{k}-1 범위를 벗어남")
            for j, q in enumerate(qubit_tuple):  # qubit_tuple[0] = LSB
                self.reset(q)
                if (val >> j) & 1:
                    self.x(q)
            return self

        # --- 라벨 문자열: 곱 상태 (O(k)) ---
        if isinstance(state, str):
            label = state.strip()
            if len(label) != k:
                raise ValueError(
                    f"initialize: 라벨 길이 {len(label)} 가 큐비트 수 {k} 와 불일치"
                )
            # Qiskit: 가장 왼쪽 문자 = 가장 높은 큐비트.  reversed → LSB 부터.
            for idx, ch in enumerate(reversed(label)):
                q = qubit_tuple[idx]
                self.reset(q)
                if ch == "0":
                    pass
                elif ch == "1":
                    self.x(q)
                elif ch == "+":
                    self.h(q)
                elif ch == "-":
                    self.x(q).h(q)
                elif ch == "r":  # |+i⟩ = (|0⟩+i|1⟩)/√2
                    self.h(q).s(q)
                elif ch == "l":  # |−i⟩ = (|0⟩−i|1⟩)/√2
                    self.h(q).sdg(q)
                else:
                    raise ValueError(
                        f"initialize: 잘못된 라벨 문자 {ch!r} (허용: 0 1 + - r l)"
                    )
            return self

        # --- 일반 statevector: reset + 준비 유니터리 ---
        arr = np.asarray(state, dtype=np.complex128).ravel()
        dim = 1 << k
        if arr.shape[0] != dim:
            raise ValueError(
                f"initialize: statevector 길이 {arr.shape[0]} 가 2^{k} = {dim} 와 불일치"
            )
        norm = float(np.linalg.norm(arr))
        if norm < 1e-12:
            raise ValueError("initialize: 영벡터는 초기화할 수 없습니다")
        if abs(norm - 1.0) > 1e-8:
            raise ValueError(
                f"initialize: statevector 가 정규화되지 않음 (‖ψ‖={norm:.6g}, 1e-8)"
            )
        # Möttönen uniformly-controlled rotation 으로 native (RY/RZ + CNOT)
        # 준비 회로를 만든다.  전체 2ⁿ×2ⁿ 행렬을 만들지 않고 (게이트 O(2ⁿ)),
        # 모든 백엔드 (statevector / MPS / density / GPU) 에서 동작한다.
        from .synthesis import state_preparation_gates

        for q in qubit_tuple:
            self.reset(q)
        gates, gphase = state_preparation_gates(arr)
        for g in gates:
            if g[0] == "cx":
                self.cx(qubit_tuple[g[1]], qubit_tuple[g[2]])
            elif g[0] == "ry":
                self.ry(g[1], qubit_tuple[g[2]])
            else:  # rz
                self.rz(g[1], qubit_tuple[g[2]])
        # 전역 위상 (초기화 회로는 reset 포함이라 관측 불가하지만 Qiskit
        # Statevector 와 정확히 일치시키기 위해 기록).
        self._circuit.global_phase = self._circuit.global_phase + gphase
        return self

    def expectation(
        self,
        observable,
        *,
        precision: str = "f64",
        shots: int | None = None,
        estimator_seed: int | None = None,
        **run_kwargs,
    ) -> float:
        """회로를 실행한 뒤 Pauli observable 의 기댓값 ``⟨ψ|H|ψ⟩`` 을 반환한다 (v0.7).

        ``self.run(shots=0, ...)`` 으로 statevector 를 얻어
        :meth:`SimulationResult.expectation` 을 호출하는 편의 메서드.  VQE /
        QAOA 의 비용 함수 평가에 사용한다.

        Args:
            observable: Pauli observable (dict / list / SparsePauliOp —
                :meth:`SimulationResult.expectation` 참조).
            precision: ``"f64"`` (기본) 또는 ``"f32"``.
            shots: ``None`` (기본) → 정확한 기댓값.  양의 정수 → shot-based
                추정 (NISQ 현실성, shot noise 포함; v0.7.1).
            estimator_seed: shot-based 추정 RNG seed.
            **run_kwargs: :meth:`run` 에 전달 (예: ``method``,
                ``max_bond_dim``).  회로 실행은 항상 ``shots=0``.
                ``method="pauli_propagation"`` 이면 전용 estimator
                (:func:`panta_sim.pauli_propagation.
                pauli_propagation_expectation`) 로 라우팅되며 ``shots`` /
                ``estimator_seed`` / ``precision`` 은 **무시** 된다 (해석적
                Heisenberg 역전파 — ``pp_threshold`` / ``pp_depolarizing``
                kwarg 로 제어).

        Returns:
            기댓값 (``float``).
        """
        # method="pauli_propagation": Heisenberg 역전파 경로 (큰 N·저 비-Clifford,
        # 얽힘 무관).  run/statevector 대신 전용 estimator 로 라우팅.
        if run_kwargs.get("method") == "pauli_propagation":
            from .pauli_propagation import pauli_propagation_expectation as _pp

            threshold = run_kwargs.get("pp_threshold", 1e-10)
            depolarizing = run_kwargs.get("pp_depolarizing", 0.0)
            return _pp(
                self, observable, threshold=threshold, depolarizing=depolarizing
            ).real
        result = self.run(shots=0, precision=precision, **run_kwargs)
        return result.expectation(observable, shots=shots, seed=estimator_seed)

    def variance(self, observable, *, precision: str = "f64", **run_kwargs) -> float:
        """회로 실행 후 Pauli observable 의 분산 ``⟨H²⟩ - ⟨H⟩²`` 를 반환한다 (v0.7.1).

        :meth:`SimulationResult.variance` 의 편의 래퍼.  VQE 에너지 오차 막대 /
        물리량 요동 측정용.

        Args:
            observable: Pauli observable (dict / list / SparsePauliOp).
            precision: ``"f64"`` (기본) 또는 ``"f32"``.
            **run_kwargs: :meth:`run` 에 전달 (예: ``method``, ``max_bond_dim``).
        """
        run_kwargs.pop("shots", None)
        return self.run(shots=0, precision=precision, **run_kwargs).variance(observable)

    def transpile(self, max_iters: int = 16) -> QuantumCircuit:
        """회로에 peephole 최적화 패스를 in-place 로 적용한다.

        v0.3.1 Cut B 단계에서는 stub (no-op). Cut C 에서 회전 합성, H·X·H = Z
        같은 항등식, trivial drop 패스가 활성화된다.

        Args:
            max_iters: fixed-point iteration 상한 (기본 16).

        Returns:
            ``self`` (fluent chaining 용).
        """
        self._circuit.transpile(max_iters)
        return self

    def transpile_to_basis(self, basis: str = "cx") -> QuantumCircuit:
        """회로를 하드웨어 basis gate set 으로 변환한 **새 회로** 를 반환한다 (v0.8.3+).

        지원 basis:
        - ``"cx"`` (default): **CX + 임의 1-큐비트** 게이트.  모든 2/3-큐비트
          게이트 (CZ/CY/SWAP/iSWAP/DCX/CRx/CRy/CRz/CP/CH/RXX/RYY/RZZ/RZX/Toffoli/
          Fredkin) 를 표준 항등식으로 CX + 1q 회전으로 분해한다.  대부분의 실
          하드웨어 (IBM/Google/IonQ) 의 2-큐비트 native gate 가 CX 동치이므로
          회로 레벨 transpile 의 핵심 단계다.
        - ``"ibm"`` (별칭 ``"rz_sx_x"``): **`rz` + `sx` + `x` + CX**.  CX-basis
          분해 후 모든 1q 게이트를 ZYZ 분해 + 항등식 `Ry(γ)=X·SX·Rz(γ)·SX` 로
          `{rz, sx, x}` 로 rebase 한다.  IBM Eagle/Heron 등 초전도 하드웨어의
          표준 1q basis (전역 위상 보존, 대각 게이트는 `rz` 하나로 접음).

        KAK 합성이 필요한 게이트 (CU/CU3/ECR/XXPlusYY/XXMinusYY) 를 만나면
        ``ValueError`` — 대신 ``unitary(M, qubits, decompose="cx")`` (KAK) 를
        사용하라는 안내를 포함한다.

        Args:
            basis: 타깃 basis — ``"cx"`` 또는 ``"ibm"`` (``"rz_sx_x"``).

        Returns:
            변환된 새 ``QuantumCircuit`` (원본은 불변).  ``"cx"`` 는
            ``is_cx_basis() == True``, ``"ibm"`` 은 ``is_zsx_basis() == True``.
        """
        if basis == "cx":
            new_raw = self._circuit.transpile_cx_basis()
        elif basis in ("ibm", "rz_sx_x"):
            new_raw = self._circuit.transpile_ibm_basis()
        else:
            raise ValueError(
                f"지원하는 basis 는 'cx' / 'ibm' 입니다 (입력: {basis!r})"
            )
        obj = QuantumCircuit.__new__(QuantumCircuit)
        obj._pending_builder = None
        obj._raw_circuit = new_raw
        obj._ops = _ops_from_rust(new_raw)
        obj._from_qasm = False
        obj._parametric = False
        return obj

    def is_cx_basis(self) -> bool:
        """회로의 모든 2/3-큐비트 게이트가 CX 인지 (CX-basis 인지) 검사한다."""
        return self._circuit.is_cx_basis()

    def is_zsx_basis(self) -> bool:
        """회로가 IBM basis (rz/sx/x 1q + CX 2q) 인지 검사한다."""
        return self._circuit.is_zsx_basis()

    @property
    def global_phase(self) -> float:
        """회로의 누적된 글로벌 phase (라디안)."""
        return self._circuit.global_phase

    def draw(self, style: str = "unicode") -> str:
        """회로의 텍스트 다이어그램을 반환한다.

        ``transpile()`` 호출 후에는 Rust 회로만 갱신되고 Python 측 ``_ops``
        는 그대로 남아 있으므로, ``draw()`` 는 항상 *transpile 전* 회로를
        표시한다. ``from_qasm()`` 으로 만든 회로도 v0.4 부터는 Rust
        ``Circuit::instructions()`` 에서 ``_ops`` 를 복원해 정상 다이어그램이
        출력된다.

        Args:
            style: ``"unicode"`` (default) — box-drawing 문자
                (``─ │ ┼ ┤ ├ ●``), 또는 ``"ascii"`` — 순수 ASCII
                (``- | + [ ] *``).

        Returns:
            줄 바꿈으로 join 된 다이어그램 문자열.

        Example:
            >>> qc = QuantumCircuit(2)
            >>> qc.h(0).cx(0, 1)
            >>> print(qc.draw())
            q0: ─┤H├──●──
            q1: ─────┤X├─
        """
        from .visualize import _draw_circuit_text

        return _draw_circuit_text(self._ops, self.num_qubits, style=style)

    def __repr__(self) -> str:
        return (
            f"QuantumCircuit({self.num_qubits} qubits, {len(self._ops)} ops)"
        )

    def __str__(self) -> str:
        return self.draw()

    # 측정
    def measure(self, qubit: int, cbit: int) -> QuantumCircuit:
        """특정 큐비트를 측정한다.

        v0.4.5 부터 회로 끝이 아닌 mid-circuit 위치에 두면 trajectory 모드로
        전환되어 즉시 collapse 후 cbit 갱신된다.
        """
        self._circuit.measure(qubit, cbit)
        # cbit 정보를 params 슬롯에 보존 (to_qiskit / to_cirq 에서 emit).
        self._ops.append(("measure", (qubit,), (int(cbit),)))
        return self

    def measure_all(self) -> QuantumCircuit:
        """모든 큐비트를 측정한다."""
        self._circuit.measure_all()
        self._ops.append(("measure_all", tuple(range(self.num_qubits)), ()))
        return self

    # Dynamic 회로 (v0.4.5)
    def reset(self, qubit: int) -> QuantumCircuit:
        """큐비트를 |0⟩ 상태로 리셋한다 (v0.4.5).

        측정 + 조건부 X 의 합성과 의미 동등하지만 cbit 을 소비하지 않는다.
        실행 시 trajectory 모드로 전환된다.
        """
        self._circuit.reset(qubit)
        self._ops.append(("reset", (qubit,), ()))
        return self

    def c_if(self, cbits, value: int) -> QuantumCircuit:
        """직전에 추가된 게이트를 classical-controlled 로 wrap 한다 (v0.4.5).

        Qiskit ``qc.x(0).c_if(c, 1)`` 와 동등 — 가장 최근에 추가된 단일 게이트
        op 을 ``IfEq`` 로 in-place 변환한다. ``cbits`` 의 cbit 들이 LSB-first
        packed 정수로 ``value`` 와 같을 때만 inner 게이트가 fire 한다.

        Args:
            cbits: 단일 cbit 인덱스 (``int``) 또는 cbit 인덱스 리스트
                (``list[int]`` / ``tuple[int, ...]``). LSB = ``cbits[0]``.
            value: 비교할 정수 값 (≥ 0). ``len(cbits) > 64`` 면 ValueError.

        Returns:
            self (fluent chaining 용).

        Raises:
            ValueError: 회로가 비어 있거나 마지막 op 이 단일 게이트가 아닐 때
                (예: ``measure`` / ``measure_all`` / ``unitary`` / ``reset``
                직후엔 c_if 불가 — Qiskit ``c_if`` 의미와 정합).
        """
        if isinstance(cbits, int):
            cbit_list = [int(cbits)]
        else:
            cbit_list = [int(b) for b in cbits]
        if not cbit_list:
            raise ValueError("c_if: cbits 가 비어 있을 수 없습니다")
        if any(b < 0 for b in cbit_list):
            raise ValueError(f"c_if: cbit 인덱스는 음수가 될 수 없습니다 ({cbit_list})")
        if len(cbit_list) > 64:
            raise ValueError(
                f"c_if: cbits 길이가 64 를 초과 ({len(cbit_list)}). u64 packing 한계."
            )
        v = int(value)
        if v < 0:
            raise ValueError(f"c_if: value 는 음수가 될 수 없습니다 ({v})")
        if v >= (1 << len(cbit_list)):
            raise ValueError(
                f"c_if: value={v} 가 cbits 폭 {len(cbit_list)} 비트로 표현할 수 있는 "
                f"최댓값 {(1 << len(cbit_list)) - 1} 을 초과합니다"
            )
        if not self._ops:
            raise ValueError("c_if: 회로가 비어 있어 wrap 할 게이트가 없습니다")
        last_name, last_qubits, last_params = self._ops[-1]
        # 단일 게이트 op 만 wrap 가능. unitary 는 Rust 측에서 Z-Y-Z 분해로 여러
        # ApplyGate 를 만들기 때문에 c_if 가 마지막 Rz 만 wrap 해 의미가 깨짐.
        _ALLOWED = {
            "h", "x", "y", "z", "s", "sdg", "t", "tdg", "sx", "sxdg", "id",
            "rx", "ry", "rz", "p", "u1", "u2", "u",
            "cx", "cz", "swap", "cy", "ch",
            "crx", "cry", "crz", "cp", "cu1", "cu3", "cu",
            "ccx", "cswap",
        }
        if last_name not in _ALLOWED:
            raise ValueError(
                f"c_if: 마지막 op 이 단일 게이트가 아닙니다 (got {last_name!r}). "
                f"단일 게이트 직후에만 c_if 호출 가능."
            )
        # Rust 측: 마지막 ApplyGate 를 IfEq 로 in-place wrap.
        self._circuit.c_if_last(cbit_list, v)
        # Python _ops: 마지막 op 을 IfEq 로 wrap.
        # params 슬롯 = (cbits_tuple, value, inner_name, inner_params).
        # to_qiskit / to_cirq 는 inner_name 으로 게이트를 재구성한다.
        self._ops.pop()
        self._ops.append(
            (
                "if_eq",
                last_qubits,
                (tuple(cbit_list), v, last_name, last_params),
            )
        )
        return self

    def c_if_last(self, cbits, value: int) -> "QuantumCircuit":
        """v0.5.21: Rust API 의 ``Circuit::c_if_last`` 와 이름 일치하는 alias.
        Python 측에서는 ``c_if`` (Qiskit 호환) 가 표준이지만, RX 6600 dispatch
        검증에서 사용자가 ``c_if_last`` 라고 호출 — Rust 이름 그대로 alias
        제공해 양쪽 호환.
        """
        return self.c_if(cbits, value)

    # ------------------------------------------------------------------
    # v0.4.7 — Block-form classical control flow (context manager API)
    # ------------------------------------------------------------------

    def if_test(self, condition) -> "_IfElseBuilder":
        """Block-form ``if (c == value):`` context manager (v0.4.7).

        Qiskit 의 ``with qc.if_test((cbit, value)):`` 패턴과 동일.

        Args:
            condition: ``(cbit_or_list, value)`` 튜플.  단일 ``int`` 인덱스 또는
                ``list[int]`` (LSB-first packed).

        Returns:
            ``_IfElseBuilder`` — context manager 로 사용. ``with`` 블록 안에서
            self-같은 ``QuantumCircuit`` 위에 게이트 / measure / reset / nested
            block control flow 를 모두 호출할 수 있다.  optional ``else_`` 메서드
            로 else branch.

        Example:
            >>> qc = QuantumCircuit(2, ...)
            >>> qc.measure(0, 0)
            >>> with qc.if_test((0, 1)) as else_:
            ...     qc.x(1)
            ... with else_:
            ...     qc.y(1)
        """
        cbits, value = _normalize_condition(condition)
        return _IfElseBuilder(self, cbits, value)

    def while_loop(self, condition, max_iters: int = 256) -> "_WhileLoopBuilder":
        """Block-form ``while (c == value):`` context manager (v0.4.7).

        Args:
            condition: ``(cbit_or_list, value)`` 튜플.
            max_iters: 안전 bound.  cbit 갱신이 body 안에서 일어나지 않으면
                무한 loop 방지를 위해 이 횟수 후 종료.  default 256.
        """
        cbits, value = _normalize_condition(condition)
        return _WhileLoopBuilder(self, cbits, value, max_iters)

    def for_loop(self, iterations: int) -> "_ForLoopBuilder":
        """Block-form ``for _ in range(iterations):`` context manager (v0.4.7).

        body 를 정확히 ``iterations`` 회 반복.  loop variable 은 panta-sim 에서
        직접 사용 불가 — body 안에서 i 가 게이트 인자로 쓰이는 회로는 사용자가
        Python 측에서 unroll 해야 한다.
        """
        if iterations < 0:
            raise ValueError(f"for_loop: iterations 는 음수 불가 ({iterations})")
        return _ForLoopBuilder(self, iterations)

    def switch(self, cbits) -> "_SwitchBuilder":
        """Block-form switch-case context manager (v0.4.7).

        Args:
            cbits: ``int`` 또는 ``list[int]`` (LSB-first packed).

        Example:
            >>> with qc.switch([0, 1]) as cases:
            ...     with cases.case(0):
            ...         qc.h(0)
            ...     with cases.case(1):
            ...         qc.x(0)
            ...     with cases.default:
            ...         qc.id(0)
        """
        if isinstance(cbits, int):
            cbit_list = [int(cbits)]
        else:
            cbit_list = [int(b) for b in cbits]
        if not cbit_list:
            raise ValueError("switch: cbits empty")
        return _SwitchBuilder(self, cbit_list)

    # 실행
    def _is_clifford_circuit(self) -> bool:
        """회로가 순수 Clifford (stabilizer 백엔드 적용 가능) 인지 검사한다.

        모든 op 이 Clifford 게이트 (H/X/Y/Z/S/Sdg/√X/√X†/CX/CY/CZ/SWAP/iSWAP/
        DCX/ECR) 이거나, π/2 의 배수 각도 회전 (rz/rx/p) / π 배수 rzz 인지 본다.
        측정/비동적 회로만 (mid-circuit reset / control-flow 는 제외).  파라메트릭
        회로는 ``False`` (바인딩 전).
        """
        if self._parametric:
            return False
        clifford_named = {
            "h", "x", "y", "z", "s", "sdg", "sx", "sxdg",
            "cx", "cy", "cz", "swap", "iswap", "dcx", "ecr", "id",
            "measure", "measure_all", "barrier",
        }
        half_pi_rot = {"rz", "rx", "p"}  # k·π/2
        for name, _q, params in self._ops:
            if name in clifford_named:
                continue
            if name in half_pi_rot and params:
                k = params[0] / (math.pi / 2)
                if abs(k - round(k)) > 1e-9:
                    return False
                continue
            if name == "ry" and params:
                # ry 는 0 / π 만 Clifford (±π/2 는 stabilizer 백엔드 미지원).
                k = params[0] / (math.pi / 2)
                if abs(k - round(k)) > 1e-9 or round(k) % 2 != 0:
                    return False
                continue
            if name == "rzz" and params:
                k = params[0] / math.pi
                if abs(k - round(k)) > 1e-9:
                    return False
                continue
            return False
        return True

    def _auto_method(self, shots: int, noise_model: Optional[Any]) -> str:
        """``method="auto"`` 의 백엔드 자동 선택 휴리스틱 (v0.8.5).

        회로 특성 (Clifford 여부 / 노이즈 / 큐비트 수) 을 보고 가장 적합한
        백엔드를 고른다:

        1. **노이즈** 있음 → ``density_matrix`` (N≤14) 또는 ``statevector``
           (trajectory).
        2. **순수 Clifford** (비-파라메트릭) → ``stabilizer`` (수천 큐비트
           다항시간).  단 작은 회로 (N≤24) 는 statevector 가 더 빠르고
           statevector() 도 제공하므로 statevector.
        3. **작은 회로** (N≤28) → ``statevector`` (정확·범용).
        4. **큰 회로** (N>28) → ``mps`` (저얽힘 가정, best-effort).
        """
        n = self.num_qubits
        if noise_model is not None:
            return "density_matrix" if n <= 14 else "statevector"
        # stabilizer 는 statevector 를 못 만들므로 shots>0 (샘플링) 일 때만.
        if shots > 0 and n > 24 and self._is_clifford_circuit():
            return "stabilizer"
        if n <= 28:
            return "statevector"
        # 큰 비-Clifford 회로: MPS (저얽힘 가정).  고얽힘이면 사용자가 tensornet
        # / amplitude 를 직접 선택해야 함.
        return "mps"

    def run(
        self,
        shots: int = 1024,
        seed: Optional[int] = None,
        precision: str = "f64",
        noise_model: Optional[Any] = None,
        method: str = "statevector",
        max_bond_dim: int = 64,
        trunc_threshold: float = 0.0,
        optimizer: str = "random-greedy",
        tn_gpu: bool = False,
        depolarizing: float = 0.0,
    ) -> SimulationResult:
        """회로를 실행하고 결과를 반환한다.

        Args:
            shots: 측정 횟수.
            seed: 재현 가능한 결과를 위한 랜덤 시드.
            precision: 시뮬레이션 정밀도. ``"f64"`` (default) 또는 ``"f32"``.
                ``"f32"`` 는 메모리를 약 50% 절감하고 SIMD 친화적이지만,
                statevector 정확도가 ~1e-6 수준으로 떨어진다 (Qiskit 비교 시).
                동일 RAM 에서 큐비트 1개 더 시뮬레이션 가능.
            noise_model: ``panta_sim.NoiseModel`` 인스턴스 (v0.4). 지정 시
                stochastic trajectory 모드 (statevector backend) 또는 결정적
                Kraus 적용 (density_matrix backend) 으로 실행.
                statevector + ``shots=0`` + noise: 단일 trajectory 만 실행되어
                mixed state 를 대표하지 못하므로 ``UserWarning`` 발생.
            method: 백엔드 선택 (v0.5.0).
                - ``"statevector"`` (default): 2ⁿ amplitude state vector.
                  noise 가 있으면 stochastic trajectory.
                - ``"density_matrix"``: 4ⁿ density matrix `ρ` 직접 진화.
                  noise 가 있어도 결정적 Kraus 적용 (Aer
                  ``method="density_matrix"`` 와 동일 의미).
                  메모리 4ⁿ × 16B (f64) → N≤14 권장.  N>14 면 ``UserWarning``.
                - ``"mps"`` (v0.6.1+): Matrix Product State 백엔드.
                  v0.6.1 부터 ``N > 20`` 도 지원 (sampling-via-MPS direct
                  contraction), v0.6.3 부터 ``N > 64`` 도 지원 (outcome
                  encoding 을 ``Vec<bool>`` 로 확장).  ``shots = 0`` 의 dense
                  statevector 접근은 ``N ≤ 20`` (``N > 20`` 은 MPS 가 보존돼
                  ``expectation()`` 가능, v0.7).  ``precision="f32"`` 지원
                  (v0.6.5).  noise / dynamic 회로 (reset / if / while / for /
                  switch) 는 trajectory 엔진으로 지원 (v0.6.5), 3-qubit gate
                  (Toffoli / Fredkin) 는 1q + CNOT 으로 자동 분해 (v0.6.8),
                  비인접 2q gate 는 SWAP chain 으로 자동 처리 (v0.6.3).
                  결과의 ``mps_max_bond_dim`` / ``mps_final_norm_sq`` /
                  ``mps_truncation_error_sum`` getter 로 truncation 메타
                  확인 가능.
                - ``"wgpu_mps"`` (v0.6.6): cross-platform GPU MPS — SVD
                  를 wgpu compute shader 로 offload.  ``"mps"`` 와 동일
                  의미이되 NVIDIA / AMD / Apple Metal / Intel 모두에서
                  GPU 가속.  ``f32`` only (wgpu storage f64 미지원) —
                  ``precision`` 인자는 무시되고 ``mps_trunc_threshold``
                  권장값은 ``1e-4``.  Cut 1 시점에서는 wiring 만 완료,
                  실제 GPU SVD 는 Cut 6 부터 통합 — 그 전까지는 CPU
                  MPS 와 동일 결과.
            max_bond_dim: MPS 백엔드의 χ_max (default 64, Qiskit Aer / MIMIQ 와
                동일).  비-MPS method 에서는 무시.
            trunc_threshold: MPS 백엔드의 singular-value cutoff (v0.6.5).
                기본 ``0.0`` (disabled) — ``max_bond_dim`` 만으로 truncation.
                양수면 SVD 결과의 ``s_i < trunc_threshold`` 인 mode 도 함께
                drop → adaptive bond dim.  ``max_bond_dim`` 과 동시에 지정시
                더 strict 한 쪽 적용 (Schollwöck 2011 §4.5.3).  ``f64`` 기준
                권장값 ``1e-10``, ``f32`` 기준 ``1e-4``.  비-MPS method 에서는
                무시.  결과의 ``mps_trunc_threshold`` / ``mps_observed_max_bond_dim``
                으로 실제 적용된 cutoff / 발생한 χ 확인 가능.
            optimizer: ``method="tensornet"`` 의 contraction path 전략
                (``"greedy"`` / ``"random-greedy"`` (default) / ``"sa"`` 등 —
                :meth:`amplitude` 참조).  다른 method 에서는 무시.
            tn_gpu: ``method="tensornet"`` 의 contraction 을 wgpu GPU 로 수행
                (v0.8).  다른 method 에서는 무시.
            depolarizing: ``method="stabilizer"`` 전용 — 게이트당 depolarizing
                확률 ``p`` (>0 이면 noisy Clifford trajectory, v0.8.16).
                다른 method 에서 양수를 지정하면 ``ValueError`` (조용한 무시
                방지) — 일반 백엔드의 노이즈는 ``noise_model=`` 을 사용.

        Returns:
            SimulationResult 객체. ``result.precision`` / ``result.backend`` 으로
            사용된 정밀도 / 백엔드 확인 가능.
            statevector + noise_model: ``statevector()`` 는 마지막 trajectory 의 상태
            (디버깅 용) — 사용자는 ``counts()`` 로 통계량을 본다.
            density_matrix: ``density_matrix()`` 로 ρ 직접 접근.
            mps: ``statevector()`` 는 회로 끝에서 contract 된 dense SV (truncation
            후 norm² < 1 일 수 있음).
        """
        self._ensure_bound("run")
        if not isinstance(shots, (int, np.integer)) or int(shots) < 0:
            raise ValueError(f"shots 는 0 이상의 정수여야 합니다 (입력: {shots!r})")
        if method not in (
            "statevector",
            "density_matrix",
            "density",
            "cpu",
            "wgpu",
            "wgpu_statevector",
            "wgpu_density_matrix",
            "wgpu_density",
            "cuda",
            "cuda_statevector",
            "custatevec",
            "mps",
            "mps_statevector",
            "wgpu_mps",
            "tensornet",
            "tn",
            "stabilizer",
            "clifford",
            "tableau",
            "auto",
        ):
            raise ValueError(
                f"method 는 'statevector' / 'density_matrix' / 'wgpu' / "
                f"'wgpu_density_matrix' / 'cuda' / 'mps' / 'wgpu_mps' / "
                f"'tensornet' / 'stabilizer' / 'auto' 여야 합니다 (입력: {method!r})"
            )

        # v0.8.5: 자동 백엔드 선택 — 회로를 분석해 최적 method 로 해소한다.
        if method == "auto":
            method = self._auto_method(int(shots), noise_model)

        # depolarizing= 는 stabilizer 전용 — 다른 method 에서 조용히 무시되면
        # 사용자가 noiseless 결과를 noisy 로 오인할 수 있어 명시적으로 거부.
        if float(depolarizing) > 0.0 and method not in (
            "stabilizer",
            "clifford",
            "tableau",
        ):
            raise ValueError(
                f"depolarizing= 인자는 method='stabilizer' 전용입니다 (해소된 "
                f"method: {method!r}).  일반 백엔드의 depolarizing 노이즈는 "
                f"NoiseModel().add_depolarizing(p) 를 noise_model= 로 전달하세요."
            )

        # v0.8.2: Stabilizer (Clifford) 백엔드 — Aaronson–Gottesman tableau.
        # Clifford 회로 (H/S/CNOT 군 + π/2 배수 회전) 를 다항시간으로 시뮬레이션해
        # 수천 큐비트까지 동작.  비-Clifford / noise / 동적 회로는 ValueError.
        if method in ("stabilizer", "clifford", "tableau"):
            if noise_model is not None:
                raise ValueError(
                    "method='stabilizer' 는 NoiseModel 을 지원하지 않습니다 — Pauli "
                    "노이즈는 depolarizing= 인자로 지정하세요 (Clifford 유지)."
                )
            # depolarizing>0 면 게이트별 depolarizing(p) trajectory (수천 큐비트
            # 노이즈 Clifford, QEC 코드 시뮬레이션).
            counts = _rust_stabilizer_counts(
                self._circuit, int(shots), seed, float(depolarizing)
            )
            return SimulationResult(_StabilizerRaw(counts))

        # v0.8: Tensor Network Contraction — deep / high-entanglement 회로
        # (MPS 가 못 하는 영역).  noise / 동적 회로 미지원.
        if method in ("tensornet", "tn"):
            if noise_model is not None:
                raise ValueError(
                    "method='tensornet' 은 노이즈 회로를 지원하지 않습니다 "
                    "(순수 유니터리 회로만)."
                )
            raw_result = _rust_tn_run(
                self._circuit,
                int(shots),
                seed,
                optimizer,
                32,
                200,
                4,
                bool(tn_gpu),
            )
            return SimulationResult(raw_result)
        if method in ("density_matrix", "density"):
            backend = "density_matrix"
        elif method in ("wgpu", "wgpu_statevector"):
            backend = "wgpu"
        elif method in ("wgpu_density_matrix", "wgpu_density"):
            backend = "wgpu_density_matrix"
        elif method in ("cuda", "cuda_statevector", "custatevec"):
            backend = "cuda"
        elif method in ("mps", "mps_statevector"):
            backend = "mps"
        elif method == "wgpu_mps":
            backend = "wgpu_mps"
        else:
            backend = "statevector"

        # v0.6.8: 임의 multi-qubit unitary (qc.unitary, k≥2) 는 statevector
        # 백엔드에서만 직접 적용된다.  1-큐비트 unitary 는 ZYZ 분해라 모든
        # 백엔드 호환.  Rust panic 전에 친화적인 ValueError 로 거부.
        if backend != "statevector":
            for op_name, qubits, _params in self._ops:
                if op_name == "unitary" and len(qubits) >= 2:
                    raise ValueError(
                        f"임의 multi-qubit unitary (qc.unitary, {len(qubits)}-큐비트) "
                        f"는 현재 method='statevector' 에서만 지원됩니다 "
                        f"(요청 backend={backend!r}).  단일 큐비트 unitary 는 "
                        f"모든 백엔드에서 동작합니다."
                    )

        if backend in ("density_matrix", "wgpu_density_matrix") and self.num_qubits > 14:
            import warnings

            bytes_per = 16 if backend == "density_matrix" else 8
            warnings.warn(
                f"{backend} backend 는 4ⁿ 메모리 (N={self.num_qubits} → "
                f"{4 ** self.num_qubits * bytes_per} bytes).  N≤14 권장.",
                UserWarning,
                stacklevel=2,
            )

        # v0.6.0/v0.6.1: MPS 백엔드의 사전 검증.  Rust panic 전에 친화적인 ValueError.
        # v0.6.5: precision='f32' MPS 지원 — 기존 f64-only 거부 제거.
        # v0.6.6 Cut 1: wgpu_mps 도 동일 사전 검증 (3-qubit gate / N constraint).
        if backend in ("mps", "wgpu_mps"):
            if int(max_bond_dim) < 1:
                raise ValueError(
                    f"max_bond_dim 은 1 이상이어야 합니다 (입력: {max_bond_dim!r})"
                )
            # v0.6.5: trunc_threshold 사전 검증 (음수 / NaN 거부).
            if (
                not isinstance(trunc_threshold, (int, float))
                or trunc_threshold != trunc_threshold  # NaN check
                or float(trunc_threshold) < 0.0
            ):
                raise ValueError(
                    "trunc_threshold 는 유한한 0 이상의 값이어야 합니다 "
                    f"(입력: {trunc_threshold!r})"
                )
            # v0.7: CpuMps shots=0 N>20 은 dense statevector 대신 MPS 를 보존해
            # observable expectation (expectation_pauli, O(N·χ³)) 에 쓸 수 있다.
            # 단 statevector() 는 여전히 N>20 에서 불가 (None).  wgpu_mps 는 호스트
            # MPS 가 없어 shots=0 N>20 이 무의미하므로 거부 유지.
            if backend == "wgpu_mps" and shots == 0 and self.num_qubits > 20:
                raise ValueError(
                    f"method='wgpu_mps' + shots=0 은 N ≤ 20 만 지원합니다 (dense "
                    f"statevector 가 필요). N={self.num_qubits} 에선 shots > 0 "
                    f"로 counts() 를 받거나 method='mps' 로 expectation() 을 쓰세요."
                )
            if self.num_qubits > 1000:
                import warnings

                warnings.warn(
                    f"method='mps' N={self.num_qubits} (>1000): 큰 N 은 χ × χ 좌측 "
                    f"환경 행렬 product 를 site 마다 계산 — χ_max 를 작게 (e.g. 16) "
                    f"유지해야 실용적입니다.",
                    UserWarning,
                    stacklevel=2,
                )
            # v0.6.5: MPS noise + dynamic ops via trajectory engine.
            # v0.6.8: 3-qubit gate (Toffoli / Fredkin) 도 엔진이 1q + CNOT 로
            # 자동 분해 — 더 이상 사전 거부하지 않는다.
            self._validate_mps_compatible_ops()

        # v0.5.8: wgpu backend 가 noise 회로를 자동 hybrid trajectory path 로 처리.
        # v0.5.9: wgpu 가 dynamic 회로 (reset / classical control) 도 처리.
        # v0.5.12: cuda backend 도 같은 hybrid trajectory path 진입 (사용자 NVIDIA PC 검증 대기).

        if noise_model is not None:
            if shots == 0 and backend == "statevector":
                import warnings

                warnings.warn(
                    "noise model with shots=0 (statevector) returns a single "
                    "trajectory, which is not representative of the mixed state. "
                    "Use method='density_matrix' for deterministic Kraus.",
                    UserWarning,
                    stacklevel=2,
                )
            runtime_circuit = noise_model.apply_to(self)
        else:
            runtime_circuit = self._circuit

        raw_result = _rust_run(
            runtime_circuit,
            shots,
            seed,
            precision,
            backend,
            int(max_bond_dim),
            float(trunc_threshold),
        )
        return SimulationResult(raw_result)

    def amplitude(
        self,
        bitstring,
        optimizer: str = "random-greedy",
        trials: int = 32,
        sa_iters: int = 200,
        sa_restarts: int = 4,
        seed: Optional[int] = None,
        gpu: bool = False,
        max_width: float = 0.0,
        max_slices: int = 30,
        mem_limit_gib: Optional[float] = None,
    ) -> complex:
        """단일 진폭 ``⟨bitstring|C|0…0⟩`` 를 Tensor Network Contraction 으로
        계산한다 (v0.8).

        전체 statevector 를 만들지 않으므로 MPS 가 못 다루는 **deep /
        high-entanglement** 회로 (예: random circuit, supremacy-style) 의 특정
        진폭을 큰 N 에서도 계산할 수 있다 (contraction width 가 허용하는 한).
        회로의 게이트를 tensor network 으로 표현하고 contraction path 를
        최적화해 수축한다 (Quantum Rings / cuTensorNet 영역).

        Args:
            bitstring: 길이 ``n_qubits`` 의 비트열.  ``str`` (``"0101"``, 가장
                왼쪽이 큐비트 ``n-1``, Qiskit 표기) 또는 큐비트 ``q`` 의 값을
                담은 정수 시퀀스 (``[b_0, b_1, …]``, ``b_q`` = 큐비트 ``q``).
            optimizer: contraction path 전략 — ``"greedy"`` / ``"random-greedy"``
                (기본) / ``"sa"`` (simulated annealing, 큰 회로).
            trials: random-greedy 시도 횟수.
            sa_iters / sa_restarts: simulated annealing 반복 / 재시작 횟수.
            seed: optimizer RNG seed.

        Returns:
            복소 진폭 ``⟨bitstring|C|0…0⟩``.
        """
        n = self.num_qubits
        if isinstance(bitstring, str):
            if len(bitstring) != n:
                raise ValueError(
                    f"bitstring 길이 {len(bitstring)} != n_qubits {n}"
                )
            # 가장 왼쪽 문자가 큐비트 n-1 (Qiskit 표기) → bits[q].
            bits = [1 if bitstring[n - 1 - q] == "1" else 0 for q in range(n)]
        else:
            bits = [int(b) & 1 for b in bitstring]
            if len(bits) != n:
                raise ValueError(f"bitstring 길이 {len(bits)} != n_qubits {n}")
        # v0.8.6: 메모리 예산 기반 자동 slicing.  mem_limit_gib 가 주어지면
        # intermediate 텐서 폭을 budget 안에 들도록 max_width 를 자동 산정한다
        # (complex128 = 2^w · 16B ≤ budget → w ≤ log2(budget/16)).  명시적
        # max_width 가 없을 때만 적용.
        if mem_limit_gib is not None and max_width <= 0.0:
            if mem_limit_gib <= 0:
                raise ValueError("mem_limit_gib 는 양수여야 합니다")
            max_width = math.log2(mem_limit_gib * (1 << 30) / 16.0)
        re, im = _rust_tn_amplitude(
            self._circuit,
            [int(b) for b in bits],
            optimizer,
            int(trials),
            int(sa_iters),
            int(sa_restarts),
            seed,
            bool(gpu),
            float(max_width),
            int(max_slices),
        )
        return complex(re, im)

    def clifford_t_amplitude(self, bitstring, low_rank: bool = False) -> complex:
        r"""near-Clifford (Clifford+T) 회로의 진폭 ``⟨bitstring|C|0…0⟩`` 를 정확히
        계산한다 (v0.8.7, low_rank v0.8.11).

        T 게이트를 stabilizer 항들의 간섭 합으로 분해해 **큰 N 에 T 게이트가 적은**
        회로의 진폭을 statevector 없이 **전역 위상까지 정확히** 계산한다 (Bravyi–
        Gosset stabilizer-rank).  TN 이 못 다루는 high-treewidth (깊은 2D Clifford
        + 소수 T) 영역을 큰 N 에서 처리하는 것이 핵심 가치다.

        회로는 Clifford (H/S/Sdg/√X/√X†/X/Y/Z/CX/CY/CZ/SWAP/iSWAP/DCX + π/2 배수
        회전) + ``T``/``Tdg`` (또는 ``p`` 의 π/4 배수) 만 허용한다.  그 외 게이트 ·
        noise · 동적 회로는 ``ValueError``.

        Args:
            bitstring: 길이 ``n_qubits`` 의 비트열 — ``str`` (Qiskit 표기) 또는
                큐비트 값 정수 시퀀스.
            low_rank: ``True`` 면 **Bravyi–Gosset rank-2 블록 분해** (gadget +
                χ(\|A²⟩)=2) 로 항 수를 ``2ᵗ → 2^{⌈t/2⌉}`` 로 줄인다 (T-count ≤ 50).
                큰 T-count 에서 유리.  ``False`` (기본) 는 직접 분해 (``2ᵗ``,
                T-count ≤ 30, 작은 T 에 빠름).  두 경로 결과 동일.

        Returns:
            복소 진폭 ``⟨bitstring|C|0…0⟩`` (전역 위상 포함).
        """
        self._ensure_bound("clifford_t_amplitude")
        n = self.num_qubits
        if isinstance(bitstring, str):
            if len(bitstring) != n:
                raise ValueError(f"bitstring 길이 {len(bitstring)} != n_qubits {n}")
            bits = [1 if bitstring[n - 1 - q] == "1" else 0 for q in range(n)]
        else:
            bits = [int(b) & 1 for b in bitstring]
            if len(bits) != n:
                raise ValueError(f"bitstring 길이 {len(bits)} != n_qubits {n}")
        re, im = _rust_clifford_t_amplitude(
            self._circuit, [int(b) for b in bits], bool(low_rank)
        )
        return complex(re, im)

    def clifford_t_expectation(self, observable) -> complex:
        """near-Clifford (Clifford+T) 회로의 Pauli-sum 기댓값 ``⟨ψ|H|ψ⟩`` 를
        정확히 계산한다 (v0.8.9).

        ``|ψ⟩ = Σ_k c_k P_{S_k}|Φ⟩`` (stabilizer-rank) 이므로
        ``⟨ψ|H|ψ⟩ = Σ_{j,k} c_j* c_k ⟨Φ|P_{S_j}† H_term P_{S_k}|Φ⟩``, 각 항은
        stabilizer 상태의 Pauli 기댓값 (전역 위상 무관).  큰 N · 적은 T 회로의
        noiseless 관측량 (VQE 등) — TN/statevector 가 못 다루는 영역.

        Clifford + T/Tdg 만 허용 (그 외 게이트/noise/동적 회로는 ``ValueError``).
        비용 ``O(#terms·2^{2t}·n²)`` 라 **T-count ≤ 16** 으로 제한된다.

        Args:
            observable: ``dict`` (``{"ZZI": 1.0, …}``) / ``list[(str, coeff)]`` /
                Qiskit ``SparsePauliOp``.  Pauli 라벨 Qiskit 컨벤션 (오른쪽=큐비트 0).

        Returns:
            기댓값 (복소; Hermitian observable 이면 허수부 ≈ 0).
        """
        self._ensure_bound("clifford_t_expectation")
        terms = _normalize_pauli_terms(observable, self.num_qubits)
        re, im = _rust_clifford_t_expectation(self._circuit, terms)
        return complex(re, im)

    def clifford_t_sample(
        self,
        shots: int = 1024,
        burn_in: int = 1000,
        thin: int = 2,
        chains: int = 4,
        seed: Optional[int] = None,
        return_diagnostic: bool = False,
    ):
        """near-Clifford (Clifford+T) 회로를 **다중 체인 Metropolis-Hastings
        MCMC** 로 근사 샘플링한다 (v0.8.17, 다중 체인+진단 v0.8.19).

        타깃 분포는 ``∝ |⟨x|ψ⟩|²`` 이며, 각 진폭 ``⟨x|ψ⟩`` 는 CH-form (QFE)
        기반으로 **정확히** 평가된다.  큰 N · 적은 T 회로에서 statevector 가
        담을 수 없는 측정 분포를 얻는 유일한 경로다.  단, exact marginal 은
        지수적이라 표본은 **근사** (MCMC) 이며, ``burn_in`` / ``thin`` 으로
        상관을 줄인다.

        ``chains`` 개의 독립 체인을 **병렬** 로 돌려 (각자 독립 시작점) 표본을
        모은다 → 다봉 분포에서 모드 누락 위험을 줄이고 병렬 가속을 얻는다.
        ``return_diagnostic=True`` 면 **Gelman-Rubin ``R̂``** (큐비트별 표본평균
        관측량의 체인간/체인내 분산비의 최댓값) 도 반환한다 — ``R̂ ≈ 1``
        (≲1.05) 이면 체인들이 같은 분포로 수렴했다는 신호, 크면 ``burn_in`` /
        ``shots`` 를 늘려야 한다.

        Clifford + T/Tdg 만 허용 (그 외 게이트/noise/동적 회로는 ``ValueError``).
        비용은 진폭 평가 ``O(n²)`` × MCMC 스텝 수.  **T-count ≤ 30** 제한.

        Args:
            shots: 수집할 총 표본 수 (체인들에 분배).
            burn_in: 체인마다 정상 분포 수렴 전 버릴 스텝 수.
            thin: 표본 간 간격 (자기상관 완화).
            chains: 병렬 독립 체인 수 (≥1).
            seed: 난수 시드 (재현성).
            return_diagnostic: ``True`` 면 ``(counts, r_hat)`` 반환.

        Returns:
            ``{"011": count, …}`` measure-all 카운트 dict (왼쪽=큐비트 n-1).
            ``return_diagnostic=True`` 면 ``(counts, r_hat)`` — ``r_hat`` 은
            ``float`` 또는 (체인 1개/표본 부족 시) ``None``.
        """
        self._ensure_bound("clifford_t_sample")
        counts, r_hat = _rust_clifford_t_sample(
            self._circuit, int(shots), int(burn_in), int(thin), int(chains), seed
        )
        if return_diagnostic:
            return counts, r_hat
        return counts

    def pauli_propagation_expectation(
        self,
        observable,
        threshold: float = 1e-10,
        max_terms: int = 2_000_000,
        depolarizing: float = 0.0,
    ) -> complex:
        """관측량 기댓값 ``⟨0|U†OU|0⟩`` 를 **Pauli 역전파(Heisenberg)** 로 추정한다
        (v1.1, arXiv:2505.21606).

        관측량을 weighted Pauli 합으로 회로를 통해 역전파하므로 **얽힘에 제약받지
        않는다** (Tensor Network 의 보완재).  비-Clifford 게이트가 Pauli 항을
        분기시키며, 계수 절댓값이 ``threshold`` 미만인 항을 버려 다항적으로 유지한다.
        Clifford 가 많고 비-Clifford 가 적은 큰 N 회로(VQE/동역학)에서 statevector·
        TN 이 못 미치는 영역 — 예: 100큐비트 TFIM Trotter 의 ``⟨Z⟩``.

        지원 게이트: 1q Clifford(h/s/sdg/x/y/z/sx/sxdg) + rx/ry/rz/t/tdg/p,
        2q cx/cz/cy/swap/iswap + rzz/rxx/ryy, 3q ccx/cswap.
        ``threshold=0`` 이면 exact statevector 기댓값과 일치(검증).

        Args:
            observable: ``dict`` / ``list[(str,coeff)]`` / SparsePauliOp (Qiskit 규약).
            threshold: 계수 절댓값 컷오프 (클수록 빠르고 덜 정확).
            max_terms: Pauli 항 수 상한 (초과 시 ``ValueError``).
            depolarizing: 게이트당 depolarizing 확률 ``p`` (>0 이면 noisy 기댓값
                ``Tr(ρH)``; density 백엔드와 1e-9 일치).

        Returns:
            기댓값 (복소; Hermitian observable 이면 허수부 ≈ 0).
        """
        from .pauli_propagation import pauli_propagation_expectation as _pp

        return _pp(
            self,
            observable,
            threshold=threshold,
            max_terms=max_terms,
            depolarizing=depolarizing,
        )

    def amplitudes(
        self,
        bitstrings,
        optimizer: str = "random-greedy",
        trials: int = 32,
        sa_iters: int = 200,
        sa_restarts: int = 4,
        seed: Optional[int] = None,
    ) -> list[complex]:
        """여러 비트열의 진폭 ``⟨xᵢ|C|0…0⟩`` 를 **배치** 로 계산한다 (v0.8.4).

        amplitude network 의 인덱스 구조는 비트열과 무관 (boundary projector 의
        값만 다름) 하므로 contraction path 를 **한 번만** 최적화하고 모든 비트열에
        재사용하며, 각 비트열 contraction 은 rayon 병렬로 수행한다.  ``amplitude``
        를 비트열마다 호출하는 것보다 (특히 ``optimizer="sa"/"hyper"`` 처럼 path
        탐색이 비싼 경우) 훨씬 빠르다 — XEB 등 다수 진폭 계산용.

        Args:
            bitstrings: 비트열들의 시퀀스.  각 원소는 ``str`` (Qiskit 표기) 또는
                큐비트 값 정수 시퀀스 (``amplitude`` 와 동일 규약).
            optimizer / trials / sa_iters / sa_restarts / seed: ``amplitude`` 참조.

        Returns:
            ``complex`` 진폭 리스트 (입력 순서 보존).
        """
        n = self.num_qubits

        def _to_bits(bs):
            if isinstance(bs, str):
                if len(bs) != n:
                    raise ValueError(f"bitstring 길이 {len(bs)} != n_qubits {n}")
                return [1 if bs[n - 1 - q] == "1" else 0 for q in range(n)]
            bits = [int(b) & 1 for b in bs]
            if len(bits) != n:
                raise ValueError(f"bitstring 길이 {len(bits)} != n_qubits {n}")
            return bits

        packed = [_to_bits(bs) for bs in bitstrings]
        pairs = _rust_tn_amplitude_batch(
            self._circuit,
            packed,
            optimizer,
            int(trials),
            int(sa_iters),
            int(sa_restarts),
            seed,
        )
        return [complex(re, im) for (re, im) in pairs]

    def expectation_tn(
        self,
        observable,
        optimizer: str = "random-greedy",
        trials: int = 32,
        sa_iters: int = 200,
        sa_restarts: int = 4,
        seed: Optional[int] = None,
    ) -> complex:
        """Pauli-sum observable 의 기댓값 ``⟨ψ|H|ψ⟩`` 를 Tensor Network
        Contraction 으로 계산한다 (v0.8).

        ``⟨0|C†HC|0⟩`` 를 doubled tensor network (``C + P + C†``) 의 amplitude
        로 수축하므로, dense statevector 없이 **deep / high-entanglement** 회로의
        VQE / 관측량을 큰 N 에서 계산할 수 있다 (contraction width 가 허용하는 한).

        Args:
            observable: ``dict`` (``{"ZZI": 1.0, …}``) / ``list[(str, coeff)]`` /
                Qiskit ``SparsePauliOp``.  Pauli 라벨은 Qiskit 컨벤션 (오른쪽 끝
                = 큐비트 0).
            optimizer / trials / sa_iters / sa_restarts / seed: contraction path
                전략 (``qc.amplitude`` 와 동일).

        Returns:
            기댓값 (복소; Hermitian observable 이면 허수부 ≈ 0).
        """
        terms = _normalize_pauli_terms(observable, self.num_qubits)
        re, im = _rust_tn_expectation(
            self._circuit,
            terms,
            optimizer,
            int(trials),
            int(sa_iters),
            int(sa_restarts),
            seed,
        )
        return complex(re, im)

    def slice_plan(
        self,
        optimizer: str = "hyper",
        trials: int = 32,
        sa_iters: int = 200,
        sa_restarts: int = 4,
        seed: Optional[int] = None,
        max_width: float = 27.0,
        max_slices: int = 40,
    ) -> dict:
        """**분산 슬라이싱 계획** 을 반환한다 (v0.8).

        contraction width 를 ``max_width`` 이하로 낮추기 위해 선택할 slice 개수와,
        그로 인해 생기는 독립 작업 단위 수 (``n_configs = 2^n_slices``) / worker
        당 peak 메모리 (``log2_width_per_worker``) 를 추정한다.  각 slice 는
        독립적이라 ``n_configs`` 를 worker/노드에 분배하고 부분합을 reduce 하면
        전체 amplitude 가 된다 (cuQuantum / cotengra distributed slicing 모델).

        Returns:
            ``{"n_slices", "n_configs", "log2_width_per_worker",
            "log10_total_flops"}``.  worker 당 메모리 ≈ ``2^log2_width_per_worker``
            복소수 (전체 큐비트 수 무관).
        """
        n_slices, n_configs, w, flops = _rust_tn_plan(
            self._circuit,
            optimizer,
            int(trials),
            int(sa_iters),
            int(sa_restarts),
            seed,
            float(max_width),
            int(max_slices),
        )
        return {
            "n_slices": n_slices,
            "n_configs": n_configs,
            "log2_width_per_worker": w,
            "log10_total_flops": flops,
        }

    def amplitude_distributed(
        self,
        bitstring,
        n_workers: int,
        worker_id: Optional[int] = None,
        optimizer: str = "hyper",
        trials: int = 32,
        sa_iters: int = 200,
        sa_restarts: int = 4,
        seed: Optional[int] = None,
        max_width: float = 27.0,
        max_slices: int = 40,
    ) -> complex:
        """**분산 슬라이싱** amplitude (v0.8).

        ``worker_id`` 가 주어지면 그 worker 의 **부분합** 만 계산한다 (멀티노드에서
        각 노드가 호출 — 부분합을 네트워크로 reduce).  ``worker_id=None`` 이면
        모든 worker 부분합을 로컬에서 더해 전체 amplitude 를 반환한다 (단일 머신
        시연/검증).  각 worker 의 peak 메모리는 ``slice_plan`` 의
        ``log2_width_per_worker`` (전체 N 무관) 라 큰 회로를 노드 RAM 한계 안에서
        분산 계산할 수 있다.

        Args:
            bitstring: 길이 ``n_qubits`` 비트열 (str 또는 int 시퀀스).
            n_workers: 전체 worker/노드 수 (slice 작업 분배 단위).
            worker_id: ``0..n_workers`` 의 worker 인덱스.  None 이면 전부 합산.
            optimizer / max_width / max_slices: ``amplitude`` / ``slice_plan`` 참조.

        Returns:
            ``worker_id`` 의 부분합 (또는 None 이면 전체 amplitude).
        """
        n = self.num_qubits
        if isinstance(bitstring, str):
            if len(bitstring) != n:
                raise ValueError(f"bitstring 길이 {len(bitstring)} != n_qubits {n}")
            bits = [1 if bitstring[n - 1 - q] == "1" else 0 for q in range(n)]
        else:
            bits = [int(b) & 1 for b in bitstring]
            if len(bits) != n:
                raise ValueError(f"bitstring 길이 {len(bits)} != n_qubits {n}")
        ints = [int(b) for b in bits]
        ids = range(n_workers) if worker_id is None else [int(worker_id)]
        total = 0j
        for w in ids:
            re, im = _rust_tn_amplitude_worker(
                self._circuit,
                ints,
                int(n_workers),
                int(w),
                optimizer,
                int(trials),
                int(sa_iters),
                int(sa_restarts),
                seed,
                float(max_width),
                int(max_slices),
            )
            total += complex(re, im)
        return total

    def contraction_cost(
        self,
        optimizer: str = "random-greedy",
        trials: int = 32,
        sa_iters: int = 200,
        sa_restarts: int = 4,
        seed: Optional[int] = None,
    ) -> dict:
        """Tensor Network contraction 의 비용을 추정한다 (실행 없이).

        회로가 TN contraction 으로 다룰 만한지 판단하는 데 쓴다.  ``log2_width``
        가 peak 중간 텐서의 큐비트 수 (메모리 ≈ ``2^width`` 복소수) — 이 값이
        작아야 (예 ≤ ~30) 실용적이다.

        Returns:
            ``{"log10_flops": float, "log2_width": float}``.
        """
        log10_flops, log2_width = _rust_tn_cost(
            self._circuit,
            optimizer,
            int(trials),
            int(sa_iters),
            int(sa_restarts),
            seed,
        )
        return {"log10_flops": log10_flops, "log2_width": log2_width}

    _MPS_DYNAMIC_OPS = ("reset", "if_eq", "if_else", "while_loop", "for_loop", "switch")
    _MPS_THREE_QUBIT_OPS = ("ccx", "cswap")

    def _validate_mps_compatible_ops(self) -> None:
        """v0.6.0: method='mps' 호출 시 회로의 instruction 집합을 사전 검증.

        v0.6.5 부터 dynamic 회로 (reset / if / while / for / switch) 와
        noise 채널은 MPS trajectory engine 으로 지원된다.  v0.6.8 부터
        3-큐비트 게이트 (Toffoli / Fredkin) 도 엔진이 1q + CNOT 표준 분해로
        처리하므로 더 이상 거부 항목이 없다 — 이 메서드는 현재 no-op 이며
        향후 제약이 생길 경우를 위한 hook 으로 남겨둔다.
        """
        # v0.6.3: 비인접 2-큐비트 게이트는 엔진이 internal SWAP chain
        # 으로 자동 처리.  v0.6.8: 3-큐비트 게이트는 1q + CNOT 로 자동 분해.
        # 둘 다 SVD 를 거치므로 chi_max 가 빠듯하면
        # `result.mps_truncation_error_sum` 이 누적된다.


# ============================================================================
# v0.4.7 — Block-form classical control flow builders (context managers)
# ============================================================================


def _normalize_condition(condition) -> tuple[list[int], int]:
    """``(cbit_or_list, value)`` → ``([cbit, ...], int(value))`` 정규화.

    Qiskit `if_test((Clbit, int))` / `if_test((ClassicalRegister, int))` 모두
    지원하기 위해 첫 원소가 list/tuple/int 모두 허용.
    """
    if not isinstance(condition, tuple) or len(condition) != 2:
        raise ValueError(
            f"condition 은 (cbit_or_list, value) 튜플이어야 합니다 (입력: {condition!r})"
        )
    cbits, value = condition
    if isinstance(cbits, int):
        cbit_list = [int(cbits)]
    else:
        cbit_list = [int(b) for b in cbits]
    if not cbit_list:
        raise ValueError("condition: cbits empty")
    if any(b < 0 for b in cbit_list):
        raise ValueError(f"condition: cbits 음수 ({cbit_list})")
    if len(cbit_list) > 64:
        raise ValueError(f"condition: cbits > 64 ({len(cbit_list)})")
    v = int(value)
    if v < 0:
        raise ValueError(f"condition: value 음수 ({v})")
    if v >= (1 << len(cbit_list)):
        raise ValueError(
            f"condition: value={v} 가 cbits 폭 {len(cbit_list)} 초과 "
            f"(max {(1 << len(cbit_list)) - 1})"
        )
    return cbit_list, v


class _IfElseBuilder:
    """``with qc.if_test((cbits, value)) as else_block:`` context manager.

    - 첫 번째 ``with`` 블록: then-body.
    - ``else_block`` 자체가 또 하나의 context manager — 옵셔널 ``with else_block:``
      안의 코드가 else-body 가 됨.  사용 안 하면 then-only block.
    - ``else_block`` 의 ``__exit__`` 시점에 outer 에 ``add_if_else`` push.
    - else 미사용 시에는 outer ``with`` 의 ``__exit__`` 에서 push.
    """

    def __init__(self, outer: QuantumCircuit, cbits: list[int], value: int) -> None:
        self._outer = outer
        self._cbits = cbits
        self._value = value
        self._then_circuit: Optional[_RustCircuit] = None
        self._then_ops: Optional[list] = None
        self._else_circuit: Optional[_RustCircuit] = None
        self._else_ops: Optional[list] = None
        self._saved_circuit: Optional[_RustCircuit] = None
        self._saved_ops: Optional[list] = None
        self._stage = "init"  # init → then → maybe-else → done
        self._finalized = False

    def _swap_in(self) -> None:
        self._saved_circuit = self._outer._circuit
        self._saved_ops = self._outer._ops
        nested = _RustCircuit(self._outer.num_qubits)
        nested_ops: list = []
        self._outer._circuit = nested
        self._outer._ops = nested_ops

    def _swap_out(self) -> tuple[_RustCircuit, list]:
        nested_circuit = self._outer._circuit
        nested_ops = self._outer._ops
        assert self._saved_circuit is not None
        assert self._saved_ops is not None
        self._outer._circuit = self._saved_circuit
        self._outer._ops = self._saved_ops
        self._saved_circuit = None
        self._saved_ops = None
        return nested_circuit, nested_ops

    # === outer with: then-body ===
    def __enter__(self) -> "_IfElseBuilder":
        if self._stage == "init":
            self._stage = "then"
            self._swap_in()
            return self
        if self._stage == "after_then":
            # ``with else_:`` 재진입.  v0.6.2: outer with 종료 시 pending 으로
            # 보관됐을 self 를 취소하고 else 분기로 진입.
            if self._finalized:
                # then-only 로 이미 finalize 된 뒤 (if_test 와 else_ 사이에
                # 회로 조작이 있었던 경우) else 진입을 허용하면 else-body 가
                # 조용히 버려진다 — 명시적 에러.
                raise RuntimeError(
                    "if_test 의 else 블록은 then 블록 직후에 열어야 합니다 — "
                    "`with qc.if_test(...) as else_:` 와 `with else_:` 사이에 "
                    "회로 조작이 있어 then-only 로 이미 확정되었습니다."
                )
            if self._outer._pending_builder is self:
                self._outer._pending_builder = None
            self._stage = "else"
            self._swap_in()
            return self
        raise RuntimeError(f"_IfElseBuilder: unexpected __enter__ at stage {self._stage}")

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._stage == "then":
            self._then_circuit, self._then_ops = self._swap_out()
            self._stage = "after_then"
            # v0.6.2 fix: outer with 종료 시 즉시 finalize 하지 않고 outer 의
            # ``_pending_builder`` 에 보관.  사용자가 곧이어 ``with else_:`` 로
            # 진입하면 __enter__ 에서 pending 을 취소하고 else 분기로 들어간다.
            # ``with else_:`` 가 없으면 다음 회로 조작 (outer._circuit getter)
            # 시 ``_flush_pending_builder`` 가 then-only IfElse 로 finalize 한다.
            # 이전 v0.4.7 은 GC 시점에 finalize → ``run()`` 호출 시점까지 instruction
            # 이 회로에 들어가지 않은 silent bug.
            self._outer._pending_builder = self
            return False
        if self._stage == "else":
            self._else_circuit, self._else_ops = self._swap_out()
            self._stage = "done"
            self._finalize()
            return False
        return False

    def __del__(self) -> None:
        # 안전망: 정상 경로에서는 _flush_pending_builder 가 먼저 finalize 하므로
        # __del__ 진입 시점에는 이미 _finalized=True.  reference 가 비정상적으로
        # 살아남은 코너 케이스 (예: 사용자가 else_ 변수만 들고 회로를 버린 경우)
        # 대비해 then-only finalize 시도.
        if not self._finalized and self._stage == "after_then":
            try:
                self._finalize()
            except Exception:
                pass

    def _finalize(self) -> None:
        if self._finalized:
            return
        # 무한 재귀 방지: outer._circuit getter 가 _flush_pending_builder 를
        # 다시 호출해도 pending 은 이미 None 이어야 한다.
        if self._outer._pending_builder is self:
            self._outer._pending_builder = None
        outer = self._outer
        rust = outer._circuit
        rust.add_if_else(
            self._cbits,
            self._value,
            self._then_circuit,
            self._else_circuit,
        )
        outer._ops.append(
            (
                "if_else",
                (),
                (
                    tuple(self._cbits),
                    self._value,
                    tuple(self._then_ops or []),
                    (tuple(self._else_ops) if self._else_ops is not None else None),
                ),
            )
        )
        self._finalized = True


class _WhileLoopBuilder:
    """``with qc.while_loop((cbits, value), max_iters):`` context manager."""

    def __init__(
        self,
        outer: QuantumCircuit,
        cbits: list[int],
        value: int,
        max_iters: int,
    ) -> None:
        self._outer = outer
        self._cbits = cbits
        self._value = value
        self._max_iters = max_iters
        self._saved_circuit: Optional[_RustCircuit] = None
        self._saved_ops: Optional[list] = None
        self._body_circuit: Optional[_RustCircuit] = None
        self._body_ops: Optional[list] = None

    def __enter__(self):
        self._saved_circuit = self._outer._circuit
        self._saved_ops = self._outer._ops
        self._body_circuit = _RustCircuit(self._outer.num_qubits)
        self._body_ops = []
        self._outer._circuit = self._body_circuit
        self._outer._ops = self._body_ops
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        nested_circuit = self._outer._circuit
        nested_ops = self._outer._ops
        assert self._saved_circuit is not None
        self._outer._circuit = self._saved_circuit
        self._outer._ops = self._saved_ops or []
        self._outer._circuit.add_while_loop(
            self._cbits, self._value, nested_circuit, self._max_iters
        )
        self._outer._ops.append(
            (
                "while_loop",
                (),
                (tuple(self._cbits), self._value, tuple(nested_ops), self._max_iters),
            )
        )
        return False


class _ForLoopBuilder:
    """``with qc.for_loop(N):`` context manager."""

    def __init__(self, outer: QuantumCircuit, iterations: int) -> None:
        self._outer = outer
        self._iterations = iterations
        self._saved_circuit: Optional[_RustCircuit] = None
        self._saved_ops: Optional[list] = None
        self._body_circuit: Optional[_RustCircuit] = None
        self._body_ops: Optional[list] = None

    def __enter__(self):
        self._saved_circuit = self._outer._circuit
        self._saved_ops = self._outer._ops
        self._body_circuit = _RustCircuit(self._outer.num_qubits)
        self._body_ops = []
        self._outer._circuit = self._body_circuit
        self._outer._ops = self._body_ops
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        nested_circuit = self._outer._circuit
        nested_ops = self._outer._ops
        assert self._saved_circuit is not None
        self._outer._circuit = self._saved_circuit
        self._outer._ops = self._saved_ops or []
        self._outer._circuit.add_for_loop(self._iterations, nested_circuit)
        self._outer._ops.append(
            (
                "for_loop",
                (),
                (self._iterations, tuple(nested_ops)),
            )
        )
        return False


class _SwitchBuilder:
    """``with qc.switch(cbits) as cases:`` context manager.

    ``cases`` 는 ``case(label) / default`` 메서드를 노출.  각 case 의 body 는
    별개의 context manager 로 진입.
    """

    def __init__(self, outer: QuantumCircuit, cbits: list[int]) -> None:
        self._outer = outer
        self._cbits = cbits
        self._cases: list[tuple[Optional[int], _RustCircuit, list]] = []

    def __enter__(self):
        return self

    def case(self, label: int) -> "_SwitchCaseBuilder":
        return _SwitchCaseBuilder(self, int(label))

    @property
    def default(self) -> "_SwitchCaseBuilder":
        return _SwitchCaseBuilder(self, None)

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # 모든 case body 가 누적된 후 outer 에 add_switch push.
        outer = self._outer
        rust_cases = []
        op_cases = []
        for label, sub_circuit, sub_ops in self._cases:
            rust_cases.append((label, sub_circuit))
            op_cases.append((label, tuple(sub_ops)))
        outer._circuit.add_switch(self._cbits, rust_cases)
        outer._ops.append(
            (
                "switch",
                (),
                (tuple(self._cbits), tuple(op_cases)),
            )
        )
        return False


class _SwitchCaseBuilder:
    """``with cases.case(N):`` / ``with cases.default:`` context manager."""

    def __init__(self, switch: _SwitchBuilder, label: Optional[int]) -> None:
        self._switch = switch
        self._label = label
        self._saved_circuit: Optional[_RustCircuit] = None
        self._saved_ops: Optional[list] = None
        self._body_circuit: Optional[_RustCircuit] = None
        self._body_ops: Optional[list] = None

    def __enter__(self):
        outer = self._switch._outer
        self._saved_circuit = outer._circuit
        self._saved_ops = outer._ops
        self._body_circuit = _RustCircuit(outer.num_qubits)
        self._body_ops = []
        outer._circuit = self._body_circuit
        outer._ops = self._body_ops
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        outer = self._switch._outer
        body_circuit = outer._circuit
        body_ops = outer._ops
        assert self._saved_circuit is not None
        outer._circuit = self._saved_circuit
        outer._ops = self._saved_ops or []
        self._switch._cases.append((self._label, body_circuit, body_ops))
        return False
