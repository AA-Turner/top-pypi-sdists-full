"""사용자용 QuantumCircuit 클래스."""

from __future__ import annotations

from typing import Any, Optional

from .qsim_python import Circuit as _RustCircuit
from .qsim_python import run as _rust_run
from .result import SimulationResult


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
        self._raw_circuit = _RustCircuit(n_qubits)
        # OpRecord = (name, qubits, params). params 슬롯은 ``rx/ry/rz`` 의 회전 각도
        # (float) 외에도 ``unitary`` op 의 행렬 (np.ndarray) / ``measure`` op 의
        # cbit (int) 등을 보존한다 — to_qiskit / to_cirq 어댑터 (v0.3.5) 에서 활용.
        self._ops: list[tuple[str, tuple[int, ...], tuple[Any, ...]]] = []
        self._from_qasm: bool = False
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
        return self._circuit.to_qasm(version)

    @property
    def num_qubits(self) -> int:
        """큐비트 수를 반환한다."""
        return self._circuit.num_qubits()

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
        self._circuit.p(float(lambda_), qubit)
        self._ops.append(("p", (qubit,), (float(lambda_),)))
        return self

    def u1(self, lambda_: float, qubit: int) -> QuantumCircuit:
        """``U1(λ)`` — ``P(λ)`` 의 Qiskit alias (v0.4.6).

        내부적으로 ``P(λ)`` 와 동일 회로를 만들지만 ``_ops`` 에는 ``"u1"`` 이름으로
        기록되어 ``draw()`` / ``to_qiskit()`` / ``to_qasm()`` 의 표기가 보존된다.
        """
        self._circuit.p(float(lambda_), qubit)
        self._ops.append(("u1", (qubit,), (float(lambda_),)))
        return self

    def u2(self, phi: float, lambda_: float, qubit: int) -> QuantumCircuit:
        """``U2(φ, λ) = U(π/2, φ, λ)`` 게이트 (v0.4.6)."""
        self._circuit.u2(float(phi), float(lambda_), qubit)
        self._ops.append(("u2", (qubit,), (float(phi), float(lambda_))))
        return self

    def u(self, theta: float, phi: float, lambda_: float, qubit: int) -> QuantumCircuit:
        """``U(θ, φ, λ)`` (= Qiskit ``u3``) 일반 1-큐비트 유니터리 (v0.4.6)."""
        self._circuit.u(float(theta), float(phi), float(lambda_), qubit)
        self._ops.append(("u", (qubit,), (float(theta), float(phi), float(lambda_))))
        return self

    def rx(self, theta: float, qubit: int) -> QuantumCircuit:
        """X축 회전 게이트를 적용한다."""
        self._circuit.rx(theta, qubit)
        self._ops.append(("rx", (qubit,), (float(theta),)))
        return self

    def ry(self, theta: float, qubit: int) -> QuantumCircuit:
        """Y축 회전 게이트를 적용한다."""
        self._circuit.ry(theta, qubit)
        self._ops.append(("ry", (qubit,), (float(theta),)))
        return self

    def rz(self, theta: float, qubit: int) -> QuantumCircuit:
        """Z축 회전 게이트를 적용한다."""
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
        self._circuit.crx(float(theta), control, target)
        self._ops.append(("crx", (control, target), (float(theta),)))
        return self

    def cry(self, theta: float, control: int, target: int) -> QuantumCircuit:
        """Controlled-Ry(θ) 게이트를 적용한다 (v0.4.6)."""
        self._circuit.cry(float(theta), control, target)
        self._ops.append(("cry", (control, target), (float(theta),)))
        return self

    def crz(self, theta: float, control: int, target: int) -> QuantumCircuit:
        """Controlled-Rz(θ) 게이트를 적용한다 (v0.4.6)."""
        self._circuit.crz(float(theta), control, target)
        self._ops.append(("crz", (control, target), (float(theta),)))
        return self

    def cp(self, lambda_: float, control: int, target: int) -> QuantumCircuit:
        """Controlled-Phase(λ) 게이트를 적용한다 (v0.4.6).

        Qiskit ``cp(λ)`` / ``cu1(λ)`` 와 동일.
        """
        self._circuit.cp(float(lambda_), control, target)
        self._ops.append(("cp", (control, target), (float(lambda_),)))
        return self

    def cu1(self, lambda_: float, control: int, target: int) -> QuantumCircuit:
        """``cu1(λ)`` — ``cp(λ)`` 의 Qiskit alias (v0.4.6).

        내부적으로 ``CP(λ)`` 와 동일하지만 ``_ops`` 에 ``"cu1"`` 이름 보존.
        """
        self._circuit.cp(float(lambda_), control, target)
        self._ops.append(("cu1", (control, target), (float(lambda_),)))
        return self

    def cu3(
        self, theta: float, phi: float, lambda_: float, control: int, target: int
    ) -> QuantumCircuit:
        """Controlled-U3(θ, φ, λ) 게이트를 적용한다 (v0.4.6)."""
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

    # 임의 unitary + transpile
    def unitary(
        self,
        matrix,
        qubit: int,
        validate: bool = True,
    ) -> QuantumCircuit:
        """임의 2×2 unitary 행렬을 ``qubit`` 번째 큐비트에 적용한다.

        내부적으로 Z-Y-Z 분해 (Nielsen-Chuang Thm 4.1) 로 native 게이트
        ``Rz(δ); Ry(γ); Rz(β)`` 를 추가하고 글로벌 phase α 는 회로 메타데이터에
        누적된다. Qiskit 의 ``Statevector`` 가 ``global_phase`` 를 포함하므로
        결과 비교 시 1e-10 수준에서 일치한다.

        Args:
            matrix: 2×2 unitary. ``numpy.ndarray`` 또는 list-of-list (자동 변환).
            qubit: 적용할 큐비트 인덱스.
            validate: ``True`` (default) 면 ``M·M† ≈ I`` (1e-10) 를 확인하고
                위반 시 ``ValueError``. ``False`` 면 검증 생략.

        Returns:
            ``self`` (fluent chaining 용).
        """
        import numpy as np

        arr = np.asarray(matrix, dtype=np.complex128)
        self._circuit.unitary(arr, qubit, validate)
        # to_qiskit / to_cirq 가 그대로 emit 할 수 있게 행렬을 params 슬롯에 보존.
        self._ops.append(("unitary", (qubit,), (arr,)))
        return self

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

    def while_loop(self, condition, max_iters: int = 256) -> "_BlockBuilder":
        """Block-form ``while (c == value):`` context manager (v0.4.7).

        Args:
            condition: ``(cbit_or_list, value)`` 튜플.
            max_iters: 안전 bound.  cbit 갱신이 body 안에서 일어나지 않으면
                무한 loop 방지를 위해 이 횟수 후 종료.  default 256.
        """
        cbits, value = _normalize_condition(condition)
        return _WhileLoopBuilder(self, cbits, value, max_iters)

    def for_loop(self, iterations: int) -> "_BlockBuilder":
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
    def run(
        self,
        shots: int = 1024,
        seed: Optional[int] = None,
        precision: str = "f64",
        noise_model: Optional[Any] = None,
        method: str = "statevector",
        max_bond_dim: int = 64,
        trunc_threshold: float = 0.0,
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
                - ``"mps"`` (v0.6.1 / v0.6.3): Matrix Product State 백엔드.
                  v0.6.1 부터 ``N > 20`` 도 지원 (sampling-via-MPS direct
                  contraction).  v0.6.3 부터 ``N > 64`` 도 지원
                  (outcome encoding 을 ``Vec<bool>`` 로 확장).  ``shots = 0``
                  은 dense statevector 접근을 위해 ``N ≤ 20`` 유지.  여전히
                  noise / dynamic / non-adjacent 2q / 3q gate 미지원.
                  ``f64`` 만 지원.  결과의 ``mps_max_bond_dim`` /
                  ``mps_final_norm_sq`` / ``mps_truncation_error_sum``
                  getter 로 truncation 메타 확인 가능.
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

        Returns:
            SimulationResult 객체. ``result.precision`` / ``result.backend`` 으로
            사용된 정밀도 / 백엔드 확인 가능.
            statevector + noise_model: ``statevector()`` 는 마지막 trajectory 의 상태
            (디버깅 용) — 사용자는 ``counts()`` 로 통계량을 본다.
            density_matrix: ``density_matrix()`` 로 ρ 직접 접근.
            mps: ``statevector()`` 는 회로 끝에서 contract 된 dense SV (truncation
            후 norm² < 1 일 수 있음).
        """
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
        ):
            raise ValueError(
                f"method 는 'statevector' / 'density_matrix' / 'wgpu' / "
                f"'wgpu_density_matrix' / 'cuda' / 'mps' / 'wgpu_mps' 여야 합니다 "
                f"(입력: {method!r})"
            )
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
            if shots == 0 and self.num_qubits > 20:
                raise ValueError(
                    f"method='mps' + shots=0 은 N ≤ 20 만 지원합니다 (dense "
                    f"statevector 가 필요). N={self.num_qubits} 에선 shots > 0 "
                    f"로 실행해 counts() 만 받거나, N 을 줄여야 합니다."
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
            # 3-qubit gate (Toffoli / Fredkin) 은 여전히 사전 거부.
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

    _MPS_DYNAMIC_OPS = ("reset", "if_eq", "if_else", "while_loop", "for_loop", "switch")
    _MPS_THREE_QUBIT_OPS = ("ccx", "cswap")

    def _validate_mps_compatible_ops(self) -> None:
        """v0.6.0: method='mps' 호출 시 회로의 instruction 집합을 사전 검증.

        v0.6.5 부터 dynamic 회로 (reset / if / while / for / switch) 와
        noise 채널은 MPS trajectory engine 으로 지원된다.  남는 거부 항목은
        3-큐비트 게이트 (Toffoli / Fredkin) 뿐 — 여전히 deferred.
        """
        for op_name, qubits, _params in self._ops:
            if op_name in self._MPS_THREE_QUBIT_OPS or len(qubits) == 3:
                raise ValueError(
                    f"method='mps' 는 3-큐비트 게이트를 지원하지 않습니다 "
                    f"(instruction={op_name!r}).  Toffoli / Fredkin 는 "
                    f"method='statevector' 또는 transpile 후 1q+2q 로 분해 (v0.6.x deferred)."
                )
            # v0.6.3: 비인접 2-큐비트 게이트는 엔진이 internal SWAP chain
            # 으로 자동 처리 (was v0.6.4 deferred).  사용자가 신경쓸 필요
            # 없음 — 다만 SWAP 도 SVD 를 거치므로 chi_max 가 빠듯하면
            # `result.mps_truncation_error_sum` 이 누적된다.
            # v0.6.5: dynamic ops 도 trajectory engine 으로 dispatch.


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


class _BlockBuilder:
    """Block control flow 의 base context manager.

    `__enter__` 시 outer ``QuantumCircuit`` 의 ``_circuit`` / ``_ops`` 를 잠시
    nested 빌더로 가리고, ``__exit__`` 에서 nested 의 instructions 를 추출해
    block instruction (IfElse / While / For / Switch) 으로 outer 에 push.

    nested 빌더의 큐비트/cbit 폭은 outer 와 동일 — 사용자 코드는 outer 에 대한
    참조 (``qc``) 를 그대로 사용하면 nested 에 push 된다.
    """

    def __init__(self, outer: QuantumCircuit) -> None:
        self._outer = outer
        # 진입 시 보관 + 새 nested 로 swap.  __exit__ 에서 복구 후 block push.
        self._saved_circuit: Optional[_RustCircuit] = None
        self._saved_ops: Optional[list] = None
        self._nested_circuit: Optional[_RustCircuit] = None
        self._nested_ops: Optional[list] = None

    def _swap_in_nested(self) -> None:
        self._saved_circuit = self._outer._circuit
        self._saved_ops = self._outer._ops
        self._nested_circuit = _RustCircuit(self._outer.num_qubits)
        self._nested_ops = []
        self._outer._circuit = self._nested_circuit
        self._outer._ops = self._nested_ops

    def _swap_back(self) -> tuple[_RustCircuit, list]:
        nested_circuit = self._outer._circuit
        nested_ops = self._outer._ops
        assert self._saved_circuit is not None
        assert self._saved_ops is not None
        self._outer._circuit = self._saved_circuit
        self._outer._ops = self._saved_ops
        return nested_circuit, nested_ops


class _IfElseBuilder(_BlockBuilder):
    """``with qc.if_test((cbits, value)) as else_:`` context manager."""

    def __init__(self, outer: QuantumCircuit, cbits: list[int], value: int) -> None:
        super().__init__(outer)
        self._cbits = cbits
        self._value = value
        self._then_circuit: Optional[_RustCircuit] = None
        self._then_ops: Optional[list] = None
        self._has_else = False
        self._else_circuit: Optional[_RustCircuit] = None
        self._else_ops: Optional[list] = None
        self._stage = "init"  # init → then → else → done

    def __enter__(self):
        self._stage = "then"
        self._swap_in_nested()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._stage == "then":
            self._then_circuit, self._then_ops = self._swap_back()
            self._stage = "after_then"
        elif self._stage == "else":
            self._else_circuit, self._else_ops = self._swap_back()
            self._stage = "done"
            self._finalize()
        if exc_type is None and self._stage == "after_then":
            # else 가 호출 안 되면 finalize. else 가 호출되면 그 __exit__ 에서.
            # else 호출은 사용자가 ``with else_:`` 한 시점에 진입.
            # 다만 with else_: 안 쓰면 finalize 누락 — 안전하게 여기서 finalize.
            self._finalize()
            self._stage = "done"
        return False

    # `with else_:` syntax — Qiskit 호환.
    def __enter_else__(self) -> None:
        # else 진입 — re-swap.
        self._stage = "else"
        self._swap_in_nested()

    # else_ 자체가 context manager 로 다시 사용되는 패턴: ``with else_:``.
    # 이걸 가능하게 하려면 ``__enter__`` / ``__exit__`` 가 stage 별로 다르게.
    # 위 __exit__ 가 already 처리 — 사용자는 단순히 ``with else_:`` 호출.

    def _finalize(self) -> None:
        # nested instructions 가 outer 에 push 되도록 add_if_else 호출.
        outer = self._outer
        rust = outer._circuit
        rust.add_if_else(
            self._cbits,
            self._value,
            self._then_circuit,
            self._else_circuit,
        )
        # _ops 마커: ("if_else", qubits=(), params=(cbits_tuple, value, then_ops, else_ops))
        outer._ops.append(
            (
                "if_else",
                (),
                (
                    tuple(self._cbits),
                    self._value,
                    tuple(self._then_ops or []),
                    tuple(self._else_ops or []) if self._has_else else None,
                ),
            )
        )

    def __iter__(self):
        # ``as else_:`` 의 unpacking 우회 — Qiskit 패턴은 ``as else_`` 단일 변수.
        raise TypeError("if_test result is not iterable; use ``as else_``")

    # else 가 호출됐다는 마킹 — context manager 재진입 처리.
    @property
    def has_else(self) -> bool:
        return self._has_else

    # ``with else_:`` 호출 시
    #   1. else_ 에 첫 번째 with 가 끝나며 self._stage = "after_then" 으로 전이됐고
    #      _finalize() 가 발동해 buffered.  근데 else 를 받아야 하니 부분 재구성.
    # 더 단순한 방법: ``with else_:`` 진입 시 stage 가 "after_then" 이면 다시
    # nested 모드로 전환하고 stage="else".  __exit__ 에서 stage=="else" → else_circuit 저장
    # → finalize.  근데 이미 _finalize() 했을 가능성 있어 그건 첫 with 종료 시점에
    # 자동 호출 안 하게 막아야.
    #
    # 위 구현은 with else_: 가 안 쓰일 때만 _finalize() 자동 호출이라 부정확.
    # 다시 정리: 사용자가 with 끝낼 때 else 안 쓰면 finalize, 쓰면 그 시점에서 finalize.
    # 처음 with 끝(after_then) 에서 자동 finalize 막고, _IfElseBuilder 의 __del__ 또는 명시
    # `.finalize()` 가 필요.  Python 의 GC 에 의존하면 비결정적.
    #
    # 가장 간단: `as else_:` 를 명시 syntax 로, else 사용 안 할 거면 명시적
    # `qc.if_test(...)` 만 사용 (with 한 번).  with 끝났을 때 finalize.
    # else 사용할 거면 `with qc.if_test(...) as else_:` 후 사용자가 수동 `else_.use()`
    # 같은 거 호출... 너무 복잡.

# 결론: Qiskit 의 패턴은 with-statement 의 `__exit__` 시점에 `as else_` 변수가
# 두 번째 context manager 가 되는 nested 패턴.  이걸 정확히 모방하려면 stage
# tracking + delayed finalize.  아래 _IfElseBuilder2 가 더 깔끔한 구현:

# 위 _IfElseBuilder 를 폐기하고 새로 작성.
del _IfElseBuilder


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
