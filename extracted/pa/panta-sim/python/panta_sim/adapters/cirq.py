"""Cirq ↔ panta-sim 회로 변환 어댑터 (v0.3.5 Cut 4).

``from_cirq`` 는 ``cirq.Circuit`` 을 panta-sim ``QuantumCircuit`` 으로 변환,
``to_cirq`` 은 그 역방향을 수행한다.

Wire convention:
    Cirq 의 statevector index 는 qubit 0 = MSB (PennyLane 과 동일), panta-sim
    은 qubit 0 = LSB. 일관성 유지를 위해 cirq 의 sorted qubit ``k`` (0..n-1)
    를 panta-sim 의 ``qubit (n-1-k)`` 로 매핑한다. 결과 statevector 는
    panta-sim convention 으로 산출되어, cirq 와 직접 statevector 비교 시
    bit-reversed 인덱스로 일치한다 (테스트가 검증).

게이트 매핑 (직접):
    cirq.H, X, Y, Z, S (S**-1=sdg), T (T**-1=tdg), I → 동명/단순 매핑.
    cirq.rx, ry, rz (theta-radian) → 동명.
    cirq.CNOT, CZ, SWAP, TOFFOLI (=ccx), CSWAP (=cswap) → 동명.

매핑 표 외 1qubit gate: ``cirq.unitary(op)`` 로 행렬 추출 후
``panta_qc.unitary()`` (Z-Y-Z 분해). 다큐빗 미지원 gate 는
``cirq.decompose_once(op)`` 로 풀어 recurse — Cirq 의 표준 분해가
대부분 native gate 까지 풀어준다.

v0.4.5 부터 지원:
    - mid-circuit measurement (Cirq ``MeasurementGate`` 가 회로 중간에 있어도 OK).
    - ``cirq.reset(q)`` / ``cirq.ResetChannel`` → panta-sim ``qc.reset(q)``.

지원 안 함:
    - ``cirq.ClassicallyControlledOperation`` (cirq 의 classical control) —
      v0.4.6+ 으로 deferred. ``NotImplementedError`` 로 명시 거부.
    - parametric circuits with sympy expressions — 미리 numeric 으로 resolve.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from ..circuit import QuantumCircuit as PantaCircuit

if TYPE_CHECKING:  # pragma: no cover
    import cirq as _cirq_typing  # noqa: F401


_CIRQ_INSTALL_HINT = (
    "cirq is required for this function — install with: "
    "pip install panta-sim[cirq]"
)


def _lazy_import_cirq() -> Any:
    try:
        import cirq  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover
        raise ImportError(_CIRQ_INSTALL_HINT) from exc
    return cirq


def _wire_to_qubit(wire_idx: int, n: int) -> int:
    """cirq wire k → panta-sim qubit (n-1-k) (PennyLane 과 동일 방식)."""
    return n - 1 - wire_idx


def _process_op(op: Any, panta_qc: PantaCircuit, qubit_to_idx: dict, n: int, depth: int = 0) -> None:
    """단일 cirq operation 을 panta-sim 회로에 적용. 미지원이면 분해 후 recurse.

    무한 분해 방지를 위해 ``depth`` 상한 (16) 을 둔다.
    """
    cirq = _lazy_import_cirq()

    if depth > 16:
        raise ValueError(
            f"cirq op {op!r} decomposition exceeded depth 16 — "
            "circuit may have non-trivial gates not supported by panta-sim."
        )

    gate = op.gate
    qubits = op.qubits
    qubit_idxs = [_wire_to_qubit(qubit_to_idx[q], n) for q in qubits]

    # Cirq classical control — v0.4.5 거부 (v0.4.6+ deferred).
    if isinstance(op, cirq.ClassicallyControlledOperation):
        raise NotImplementedError(
            "cirq ClassicallyControlledOperation is not supported by panta-sim "
            "(v0.4.6+). Use Qiskit adapter (qc.x(0).c_if(c, 1)) for classical "
            "control circuits."
        )

    # Identity / no-op gates.
    if isinstance(gate, cirq.IdentityGate):
        for q in qubit_idxs:
            panta_qc.id(q)
        return

    # Measurement (v0.4.5 부터 mid-circuit 위치도 정상 처리).
    if isinstance(gate, cirq.MeasurementGate):
        for q, qi in zip(qubits, qubit_idxs):
            # cbit index = wire_idx (cirq wire 인덱스 그대로).
            panta_qc.measure(qi, qubit_to_idx[q])
        return

    # Reset — cirq 의 ResetChannel 또는 cirq.reset(q) 매핑 (v0.4.5).
    if isinstance(gate, cirq.ResetChannel):
        for q in qubit_idxs:
            panta_qc.reset(q)
        return

    # 표준 single-qubit no-param gates.
    if gate == cirq.H:
        panta_qc.h(qubit_idxs[0])
        return
    if gate == cirq.X:
        panta_qc.x(qubit_idxs[0])
        return
    if gate == cirq.Y:
        panta_qc.y(qubit_idxs[0])
        return
    if gate == cirq.Z:
        panta_qc.z(qubit_idxs[0])
        return
    if gate == cirq.S:
        panta_qc.s(qubit_idxs[0])
        return
    if gate == cirq.S**-1:
        panta_qc.sdg(qubit_idxs[0])
        return
    if gate == cirq.T:
        panta_qc.t(qubit_idxs[0])
        return
    if gate == cirq.T**-1:
        panta_qc.tdg(qubit_idxs[0])
        return

    # Parametric rotations.
    if isinstance(gate, cirq.Rx):
        # Cirq Rx(theta) 의 exponent = theta/π. panta-sim rx 는 theta 라디안 받음.
        theta = float(gate.exponent) * np.pi
        panta_qc.rx(theta, qubit_idxs[0])
        return
    if isinstance(gate, cirq.Ry):
        theta = float(gate.exponent) * np.pi
        panta_qc.ry(theta, qubit_idxs[0])
        return
    if isinstance(gate, cirq.Rz):
        theta = float(gate.exponent) * np.pi
        panta_qc.rz(theta, qubit_idxs[0])
        return

    # Two/three-qubit standard gates.
    if gate == cirq.CNOT:
        panta_qc.cx(qubit_idxs[0], qubit_idxs[1])
        return
    if gate == cirq.CZ:
        panta_qc.cz(qubit_idxs[0], qubit_idxs[1])
        return
    if gate == cirq.SWAP:
        panta_qc.swap(qubit_idxs[0], qubit_idxs[1])
        return
    if gate == cirq.TOFFOLI:
        panta_qc.ccx(qubit_idxs[0], qubit_idxs[1], qubit_idxs[2])
        return
    if gate == cirq.CSWAP:
        panta_qc.cswap(qubit_idxs[0], qubit_idxs[1], qubit_idxs[2])
        return

    # 1qubit fallback: dense unitary 추출.
    if len(qubit_idxs) == 1:
        try:
            matrix = cirq.unitary(op)
        except (TypeError, ValueError):
            matrix = None
        if matrix is not None and matrix.shape == (2, 2):
            panta_qc.unitary(np.asarray(matrix, dtype=np.complex128), qubit_idxs[0])
            return

    # 다큐빗 미지원 → cirq 의 decomposition 시도.
    decomposed = cirq.decompose_once(op, default=None)
    missing_phase = 0.0  # KAK 분해 시 SU(4) 로 정규화돼 누락되는 global phase.

    # decompose_once 가 풀어주지 못하면 (CZPowGate 등 native pow gates),
    # 4x4 unitary matrix 를 KAK decomposition 으로 1qubit + CZ 로 변환.
    if decomposed is None and len(qubits) == 2:
        try:
            matrix4 = cirq.unitary(op)
            decomposed = list(
                cirq.two_qubit_matrix_to_cz_operations(
                    qubits[0], qubits[1], matrix4, allow_partial_czs=False
                )
            )
            # ``two_qubit_matrix_to_cz_operations`` 는 ``M_orig`` 에 대해
            # ``M_decomposed = e^{-i·φ} · M_orig`` 형태 (global phase 차이)
            # 의 회로를 만든다. φ 를 panta-sim 회로에 누적해 보정한다.
            # ``M_orig · M_decomposed^†`` ≈ ``e^{iφ}·I`` 이므로 trace/4 의
            # arg 가 정확히 φ.
            decomposed_circ = cirq.Circuit(decomposed)
            m_decomp = cirq.unitary(decomposed_circ)
            ratio_matrix = matrix4 @ m_decomp.conj().T
            missing_phase = float(np.angle(np.trace(ratio_matrix) / 4.0))
        except (TypeError, ValueError, AssertionError) as exc:  # pragma: no cover
            raise ValueError(
                f"cirq op {op!r} could not be decomposed via 4x4 KAK: {exc}"
            ) from exc

    if decomposed is None:
        raise ValueError(
            f"cirq op {op!r} (gate {type(gate).__name__}) is not supported "
            f"by panta-sim and has no decomposition. Try cirq's compiler "
            f"to decompose first."
        )

    for sub_op in decomposed:
        _process_op(sub_op, panta_qc, qubit_to_idx, n, depth + 1)

    if abs(missing_phase) > 1e-15:
        # ``e^{i·missing_phase} · I`` 를 첫 qubit 에 적용 — panta-sim unitary()
        # 가 Z-Y-Z 분해 후 global_phase 를 ``missing_phase`` 만큼 누적 (회전
        # 자체는 zero matrix 라 statevector 는 변화 없음).
        ph_matrix = np.exp(1j * missing_phase) * np.eye(2, dtype=complex)
        panta_qc.unitary(ph_matrix, qubit_idxs[0])


def from_cirq(cirq_circuit: Any) -> PantaCircuit:
    """Cirq ``Circuit`` 을 panta-sim ``QuantumCircuit`` 으로 변환한다.

    cirq qubit 은 sorted order 로 panta-sim qubit (n-1-k) 매핑. 이 매핑은
    PennyLane plugin (``PantaDevice``) 와 동일하며, 그 결과 cirq simulator 의
    ``final_state_vector`` 와 panta-sim ``run().statevector()`` 가 동일 인덱스
    (no reverse 필요) 에서 일치한다. cirq.Simulator 는 내부적으로 ``complex64``
    를 사용하므로 비교 시 ~1e-7 ~ 1e-8 정밀도가 한계 (panta-sim f64 자체는
    1e-15 일관).

    Args:
        cirq_circuit: ``cirq.Circuit`` 인스턴스.

    Returns:
        panta-sim ``QuantumCircuit``.

    Raises:
        ImportError: ``cirq`` 미설치.
        ValueError: 변환 불가 op (mid-circuit measurement, sympy parameter 등).

    Example:
        >>> import cirq
        >>> from panta_sim import from_cirq
        >>> q0, q1 = cirq.LineQubit.range(2)
        >>> c = cirq.Circuit([cirq.H(q0), cirq.CNOT(q0, q1)])
        >>> panta = from_cirq(c)
    """
    _lazy_import_cirq()

    qubits_sorted = sorted(cirq_circuit.all_qubits())
    n = len(qubits_sorted)
    qubit_to_idx = {q: i for i, q in enumerate(qubits_sorted)}

    panta_qc = PantaCircuit(n)
    for op in cirq_circuit.all_operations():
        _process_op(op, panta_qc, qubit_to_idx, n)

    return panta_qc


def to_cirq(panta_circuit: PantaCircuit) -> Any:
    """panta-sim ``QuantumCircuit`` 을 Cirq ``Circuit`` 으로 변환한다.

    panta-sim qubit ``k`` 는 cirq ``LineQubit(n-1-k)`` 로 역매핑된다 (즉
    cirq qubit 0 = MSB convention 과 일치). v0.4 부터 ``from_qasm()`` 으로
    만든 회로의 ``_ops`` 는 Rust ``Circuit::instructions()`` 에서 복원되므로
    별도 우회 없이 직접 매핑된다.

    Args:
        panta_circuit: panta-sim ``QuantumCircuit``.

    Returns:
        ``cirq.Circuit``.

    Raises:
        ImportError: ``cirq`` 미설치.
        ValueError: 처리할 수 없는 op 이름 (방어적), 또는 미바인딩 파라미터.
    """
    if getattr(panta_circuit, "is_parameterized", lambda: False)():
        raise ValueError(
            "to_cirq: 미바인딩 파라미터가 있는 회로는 변환할 수 없습니다. "
            "assign_parameters() 로 값을 대입한 뒤 변환하세요."
        )
    cirq = _lazy_import_cirq()

    n = panta_circuit.num_qubits
    # panta qubit k → cirq LineQubit (n-1-k).
    cirq_qubits = [cirq.LineQubit(n - 1 - k) for k in range(n)]

    ops_list = []
    for name, qubits, params in panta_circuit._ops:
        c_qubits = [cirq_qubits[k] for k in qubits]

        if name == "h":
            ops_list.append(cirq.H(c_qubits[0]))
        elif name == "x":
            ops_list.append(cirq.X(c_qubits[0]))
        elif name == "y":
            ops_list.append(cirq.Y(c_qubits[0]))
        elif name == "z":
            ops_list.append(cirq.Z(c_qubits[0]))
        elif name == "s":
            ops_list.append(cirq.S(c_qubits[0]))
        elif name == "sdg":
            ops_list.append((cirq.S**-1)(c_qubits[0]))
        elif name == "t":
            ops_list.append(cirq.T(c_qubits[0]))
        elif name == "tdg":
            ops_list.append((cirq.T**-1)(c_qubits[0]))
        elif name == "id":
            ops_list.append(cirq.I(c_qubits[0]))
        elif name == "rx":
            ops_list.append(cirq.rx(float(params[0])).on(c_qubits[0]))
        elif name == "ry":
            ops_list.append(cirq.ry(float(params[0])).on(c_qubits[0]))
        elif name == "rz":
            ops_list.append(cirq.rz(float(params[0])).on(c_qubits[0]))
        elif name == "u":
            # OpenQASM U(θ,φ,λ) — Cirq 에 직접 매핑 게이트는 없으므로
            # 행렬을 빌드해서 MatrixGate 로 적용. Qiskit u3 정의:
            # [[cos(θ/2), -e^(iλ)sin(θ/2)], [e^(iφ)sin(θ/2), e^(i(φ+λ))cos(θ/2)]]
            theta, phi, lam = float(params[0]), float(params[1]), float(params[2])
            c = np.cos(theta / 2.0)
            s = np.sin(theta / 2.0)
            m = np.array(
                [
                    [c, -np.exp(1j * lam) * s],
                    [np.exp(1j * phi) * s, np.exp(1j * (phi + lam)) * c],
                ],
                dtype=np.complex128,
            )
            ops_list.append(cirq.MatrixGate(m).on(c_qubits[0]))
        elif name == "cx":
            ops_list.append(cirq.CNOT(c_qubits[0], c_qubits[1]))
        elif name == "cz":
            ops_list.append(cirq.CZ(c_qubits[0], c_qubits[1]))
        elif name == "swap":
            ops_list.append(cirq.SWAP(c_qubits[0], c_qubits[1]))
        elif name == "ccx":
            ops_list.append(cirq.TOFFOLI(c_qubits[0], c_qubits[1], c_qubits[2]))
        elif name == "cswap":
            ops_list.append(cirq.CSWAP(c_qubits[0], c_qubits[1], c_qubits[2]))
        elif name == "unitary":
            if not params:
                ops_list.append(cirq.I(c_qubits[0]))
            else:
                m = np.asarray(params[0], dtype=np.complex128)
                ops_list.append(
                    cirq.MatrixGate(m).on(c_qubits[0])
                )
        elif name == "measure":
            cbit = int(params[0]) if params else 0
            ops_list.append(
                cirq.measure(c_qubits[0], key=f"c{cbit}")
            )
        elif name == "measure_all":
            ops_list.append(cirq.measure(*c_qubits, key="meas"))
        elif name == "reset":
            ops_list.append(cirq.reset(c_qubits[0]))
        elif name == "if_eq":
            # Cirq 의 classical control (ClassicallyControlledOperation) 은
            # 표현 모델이 다르고 (KeyCondition 기반), Qiskit c_if 와 1:1 매핑이 어려움.
            # v0.4.5 에선 거부하고 사용자에게 명시.
            raise NotImplementedError(
                "to_cirq: c_if (if_eq) op 변환은 v0.4.6+ 으로 deferred. "
                "panta-sim 회로의 classical control 을 cirq 로 가져갈 수 없음."
            )
        else:  # pragma: no cover — unhandled op name (방어적)
            raise ValueError(f"unsupported op name {name!r} in to_cirq")

    return cirq.Circuit(ops_list)
