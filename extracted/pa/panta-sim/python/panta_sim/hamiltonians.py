"""표준 물리 해밀토니안 빌더 (v0.7.1).

자주 손으로 작성하는 Ising / TFIM / Heisenberg 해밀토니안을 Pauli string dict
(``QuantumCircuit.expectation`` / ``VQE`` 형식) 으로 생성한다.  큐비트 0 = LSB
(라벨 오른쪽 끝) 컨벤션을 따른다.

Example:
    >>> from panta_sim import QuantumCircuit
    >>> from panta_sim.hamiltonians import tfim_hamiltonian
    >>> H = tfim_hamiltonian(4, J=1.0, h=0.5)
    >>> qc = QuantumCircuit(4); [qc.h(i) for i in range(4)]
    >>> qc.expectation(H)
"""

from __future__ import annotations

from typing import Dict, List, Tuple


def _pauli_label(n: int, ops: List[Tuple[int, str]]) -> str:
    """``ops`` (``[(qubit, 'X'|'Y'|'Z'), ...]``) → 길이 ``n`` Pauli 라벨 (오른쪽 끝 = q0)."""
    label = ["I"] * n
    for q, p in ops:
        if not 0 <= q < n:
            raise ValueError(f"큐비트 인덱스 {q} 가 [0, {n}) 범위를 벗어남")
        label[n - 1 - q] = p
    return "".join(label)


def _bonds(n: int, periodic: bool) -> List[Tuple[int, int]]:
    bonds = [(i, i + 1) for i in range(n - 1)]
    if periodic and n > 2:
        bonds.append((n - 1, 0))
    return bonds


def _add(terms: Dict[str, float], key: str, coeff: float) -> None:
    terms[key] = terms.get(key, 0.0) + coeff


def ising_hamiltonian(
    n: int, J: float = 1.0, h: float = 0.0, *, periodic: bool = False
) -> Dict[str, float]:
    """1D 고전 Ising 모델 ``H = -J Σ⟨i,j⟩ ZᵢZⱼ - h Σᵢ Zᵢ`` (종방향 장).

    Args:
        n: 큐비트 수 (≥ 1).
        J: 결합 상수 (이웃 ZZ).
        h: 종방향 자기장 (Z).
        periodic: 주기 경계 조건 (마지막-처음 결합 추가).
    """
    if n < 1:
        raise ValueError(f"n 은 1 이상이어야 합니다 (입력 {n})")
    terms: Dict[str, float] = {}
    for i, j in _bonds(n, periodic):
        _add(terms, _pauli_label(n, [(i, "Z"), (j, "Z")]), -J)
    if h != 0.0:
        for q in range(n):
            _add(terms, _pauli_label(n, [(q, "Z")]), -h)
    return terms


def tfim_hamiltonian(
    n: int, J: float = 1.0, h: float = 1.0, *, periodic: bool = False
) -> Dict[str, float]:
    """횡자기장 Ising 모델 (TFIM) ``H = -J Σ⟨i,j⟩ ZᵢZⱼ - h Σᵢ Xᵢ``.

    양자 상전이 (`h/J = 1`) / 퀀치 동역학 연구의 표준 모델.
    """
    if n < 1:
        raise ValueError(f"n 은 1 이상이어야 합니다 (입력 {n})")
    terms: Dict[str, float] = {}
    for i, j in _bonds(n, periodic):
        _add(terms, _pauli_label(n, [(i, "Z"), (j, "Z")]), -J)
    if h != 0.0:
        for q in range(n):
            _add(terms, _pauli_label(n, [(q, "X")]), -h)
    return terms


def heisenberg_hamiltonian(
    n: int,
    Jx: float = 1.0,
    Jy: float = 1.0,
    Jz: float = 1.0,
    h: float = 0.0,
    *,
    periodic: bool = False,
) -> Dict[str, float]:
    """1D Heisenberg (XYZ) 모델
    ``H = Σ⟨i,j⟩ (Jx XᵢXⱼ + Jy YᵢYⱼ + Jz ZᵢZⱼ) + h Σᵢ Zᵢ``.

    ``Jx=Jy=Jz`` 면 XXX (등방성), ``Jx=Jy`` 면 XXZ.  ``h`` 는 종방향 장.
    """
    if n < 1:
        raise ValueError(f"n 은 1 이상이어야 합니다 (입력 {n})")
    terms: Dict[str, float] = {}
    for i, j in _bonds(n, periodic):
        for axis, jc in (("X", Jx), ("Y", Jy), ("Z", Jz)):
            if jc != 0.0:
                _add(terms, _pauli_label(n, [(i, axis), (j, axis)]), jc)
    if h != 0.0:
        for q in range(n):
            _add(terms, _pauli_label(n, [(q, "Z")]), h)
    return terms
