"""해밀토니안 시간 진화 (Trotter-Suzuki) — v0.7.1.

Pauli-sum 해밀토니안 ``H = Σ cᵢ Pᵢ`` 의 시간 진화 ``e^{-iHt}`` 를 native
게이트로 분해한 Trotter 회로로 만든다.  양자 동역학 / 퀀치 / 시뮬레이션 연구의
핵심 도구.

각 항 ``e^{-iθ P}`` 는 표준 Pauli-evolution gadget (basis change → CNOT ladder
→ Rz(2θ) → uncompute) 로 정확히 구현한다 (전 백엔드 호환).  Identity 항은
전역 위상 (관측 불가) 이므로 생략한다.
"""

from __future__ import annotations

from typing import Dict, Optional

from .circuit import QuantumCircuit


def pauli_evolution(qc: QuantumCircuit, pauli: str, time: float) -> QuantumCircuit:
    """``qc`` 에 ``e^{-i·time·P}`` 를 추가한다 (in-place, P = Pauli string).

    Args:
        qc: 대상 회로.  ``pauli`` 길이 = ``qc.num_qubits``.
        pauli: Pauli string (오른쪽 끝 = 큐비트 0; 문자 ``I/X/Y/Z``).
        time: 진화 시간 (실수).  Identity (전부 ``I``) 면 no-op.

    Returns:
        ``qc`` (chaining).
    """
    pauli = str(pauli).upper()
    n = qc.num_qubits
    if len(pauli) != n:
        raise ValueError(f"pauli 길이 {len(pauli)} 가 큐비트 수 {n} 와 불일치")
    # 라벨 오른쪽 끝 = 큐비트 0.
    support = [(n - 1 - pos, ch) for pos, ch in enumerate(pauli) if ch != "I"]
    if not support:
        return qc  # 항등 — 전역 위상만 (생략).
    # 기저 변환: X→Z 는 H, Y→Z 는 S†·H.
    for q, ch in support:
        if ch == "X":
            qc.h(q)
        elif ch == "Y":
            qc.sdg(q)
            qc.h(q)
    qs = [q for q, _ in support]
    for i in range(len(qs) - 1):
        qc.cx(qs[i], qs[i + 1])
    qc.rz(2.0 * time, qs[-1])
    for i in reversed(range(len(qs) - 1)):
        qc.cx(qs[i], qs[i + 1])
    for q, ch in support:
        if ch == "X":
            qc.h(q)
        elif ch == "Y":
            qc.h(q)
            qc.s(q)
    return qc


def _num_qubits(hamiltonian: Dict[str, float]) -> int:
    lengths = {len(k) for k in hamiltonian}
    if len(lengths) != 1:
        raise ValueError(f"해밀토니안 Pauli string 길이가 일관되지 않습니다: {lengths}")
    return lengths.pop()


def _trotter_step1(qc: QuantumCircuit, terms: list, tau: float) -> None:
    """1차 Trotter step ``∏ e^{-iτcP}``."""
    for p, c in terms:
        pauli_evolution(qc, p, c * tau)


def _trotter_step2(qc: QuantumCircuit, terms: list, tau: float) -> None:
    """2차 대칭 (Strang) Trotter step."""
    for p, c in terms:
        pauli_evolution(qc, p, c * tau / 2.0)
    for p, c in reversed(terms):
        pauli_evolution(qc, p, c * tau / 2.0)


# 4차 Suzuki 분해 계수: S4(τ) = S2(pτ)² S2((1-4p)τ) S2(pτ)², p = 1/(4-4^{1/3}).
_SUZUKI_P = 1.0 / (4.0 - 4.0 ** (1.0 / 3.0))


def trotter_circuit(
    hamiltonian: Dict[str, float],
    time: float,
    steps: int = 1,
    *,
    order: int = 2,
    initial_circuit: Optional[QuantumCircuit] = None,
) -> QuantumCircuit:
    """``e^{-iHt}`` 의 Trotter-Suzuki 근사 회로를 만든다.

    Args:
        hamiltonian: Pauli string → 실수 계수 dict (``cᵢ``).
        time: 총 진화 시간 ``t``.
        steps: Trotter step 수 (클수록 정확, 오차 ``O((t/steps)^order)``).
        order: ``1`` (1차) / ``2`` (2차 대칭 Strang) / ``4`` (4차 Suzuki).
        initial_circuit: 초기 상태 준비 회로 (없으면 ``|0…0⟩``).  복사되어
            진화 게이트가 뒤에 붙는다.

    Returns:
        새 :class:`QuantumCircuit` (초기 회로 + Trotter 진화).
    """
    if order not in (1, 2, 4):
        raise ValueError(f"order 는 1 / 2 / 4 만 지원합니다 (입력 {order})")
    if steps < 1:
        raise ValueError(f"steps 는 1 이상이어야 합니다 (입력 {steps})")
    n = _num_qubits(hamiltonian)
    terms = [(p, float(c)) for p, c in hamiltonian.items() if set(p) != {"I"} and c != 0.0]

    qc = initial_circuit.copy() if initial_circuit is not None else QuantumCircuit(n)
    if qc.num_qubits != n:
        raise ValueError(
            f"initial_circuit 큐비트 수 {qc.num_qubits} 가 해밀토니안 {n} 와 불일치"
        )
    dt = time / steps
    for _ in range(steps):
        if order == 1:
            _trotter_step1(qc, terms, dt)
        elif order == 2:
            _trotter_step2(qc, terms, dt)
        else:  # 4차 Suzuki: 5 개의 2차 sub-step.
            p = _SUZUKI_P
            for tau in (p * dt, p * dt, (1.0 - 4.0 * p) * dt, p * dt, p * dt):
                _trotter_step2(qc, terms, tau)
    return qc
