"""양자 정보 분석 유틸리티 (v0.7).

statevector / density matrix 로부터 fidelity, purity, partial trace, von
Neumann / entanglement entropy, trace distance 를 계산한다.  panta-sim 의
little-endian 컨벤션 (큐비트 0 = LSB, statevector index bit 0) 을 따른다 —
Qiskit ``quantum_info`` 와 동일하므로 결과가 1e-10 수준에서 일치한다.

모든 함수는 numpy 배열 (``result.statevector()`` / ``result.density_matrix()``)
또는 1-D / 2-D array-like 를 받는다.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def _as_density(state: npt.ArrayLike) -> np.ndarray:
    """statevector (1-D) 또는 density matrix (2-D) → density matrix."""
    arr = np.asarray(state, dtype=np.complex128)
    if arr.ndim == 1:
        return np.outer(arr, arr.conj())
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        return arr
    raise ValueError(f"state 는 1-D statevector 또는 정방 2-D density 여야 합니다 (shape={arr.shape})")


def _num_qubits(dim: int) -> int:
    n = int(round(np.log2(dim)))
    if 2**n != dim:
        raise ValueError(f"차원 {dim} 이 2의 거듭제곱이 아닙니다")
    return n


def state_fidelity(a: npt.ArrayLike, b: npt.ArrayLike) -> float:
    """두 상태의 fidelity.

    - 둘 다 순수 상태 (statevector): ``|⟨a|b⟩|²``.
    - 하나라도 mixed (density): Uhlmann fidelity
      ``(Tr√(√ρ σ √ρ))²`` (Jozsa 정의, Qiskit ``state_fidelity`` 와 일치).
    """
    aa = np.asarray(a, dtype=np.complex128)
    bb = np.asarray(b, dtype=np.complex128)
    if aa.ndim == 1 and bb.ndim == 1:
        return float(np.abs(np.vdot(aa, bb)) ** 2)
    rho = _as_density(aa)
    sigma = _as_density(bb)
    # √ρ.
    evals, evecs = np.linalg.eigh(rho)
    evals = np.clip(evals.real, 0.0, None)
    sqrt_rho = (evecs * np.sqrt(evals)) @ evecs.conj().T
    inner = sqrt_rho @ sigma @ sqrt_rho
    inner_evals = np.clip(np.linalg.eigvalsh(inner).real, 0.0, None)
    f = float(np.sum(np.sqrt(inner_evals)) ** 2)
    return min(max(f, 0.0), 1.0)


def purity(state: npt.ArrayLike) -> float:
    """``Tr(ρ²)`` — 순수 상태면 1, 최대 혼합이면 1/2ⁿ."""
    rho = _as_density(state)
    return float(np.real(np.trace(rho @ rho)))


def partial_trace(state: npt.ArrayLike, keep: list[int], num_qubits: int | None = None) -> np.ndarray:
    """``keep`` 큐비트만 남기고 나머지를 trace out 한 reduced density matrix.

    Args:
        state: statevector (1-D) 또는 density matrix (2-D).
        keep: 보존할 큐비트 인덱스 리스트 (little-endian, 큐비트 0 = LSB).
        num_qubits: 총 큐비트 수 (생략 시 차원에서 추론).

    Returns:
        ``2^|keep| × 2^|keep|`` reduced density matrix.  ``keep`` 오름차순
        기준으로 결과 인덱스의 비트 0 = ``keep`` 의 최소 큐비트.
    """
    arr = np.asarray(state, dtype=np.complex128)
    # v0.7.1: statevector (1-D) 는 전체 2ⁿ×2ⁿ density 를 만들지 않고 (메모리
    # O(4ⁿ) → N≥14 에서 수십 GiB 크래시) reshape + M·M† 로 reduced density 를
    # 직접 계산한다 (메모리 O(2ⁿ + 4^|keep|)).  대규모 순수상태 entanglement
    # entropy (퀀치 동역학 / area-law 연구) 에 필수.
    if arr.ndim == 1:
        dim = arr.shape[0]
        n = num_qubits if num_qubits is not None else _num_qubits(dim)
        if dim != 2**n:
            raise ValueError(f"state 차원 {dim} 이 num_qubits {n} 과 불일치")
        keep_sorted = sorted(keep)
        k = len(keep_sorted)
        # tensor 축 a ↔ 큐비트 (n-1-a) (reshape 는 axis 0 = MSB).  kept 큐비트를
        # 내림차순 (큰 큐비트 = MSB = 앞 축) 으로, traced 를 뒤로 transpose.
        t = arr.reshape([2] * n)
        keep_axes = [n - 1 - q for q in reversed(keep_sorted)]
        trace_axes = [n - 1 - q for q in range(n) if q not in keep_sorted]
        m = np.transpose(t, keep_axes + trace_axes).reshape(2**k, 2 ** (n - k))
        return m @ m.conj().T

    rho = _as_density(arr)
    dim = rho.shape[0]
    n = num_qubits if num_qubits is not None else _num_qubits(dim)
    if dim != 2**n:
        raise ValueError(f"state 차원 {dim} 이 num_qubits {n} 과 불일치")
    keep_sorted = sorted(keep)
    trace_out = [q for q in range(n) if q not in keep_sorted]
    # reshape into 2*n axes: little-endian → axis ordering must map qubit q
    # to tensor axis. statevector index bit q (value 1<<q) ↔ qubit q.
    # numpy reshape with shape (2,)*n gives axis 0 = MSB (bit n-1).  So
    # qubit q ↔ axis (n-1-q) for the row indices, and (2n-1-q) for columns.
    rho_t = rho.reshape([2] * (2 * n))
    # trace out each qubit in trace_out (row axis = n-1-q, col axis = 2n-1-q).
    # Perform einsum by pairing the corresponding row/col axes.
    row_axis = {q: n - 1 - q for q in range(n)}
    col_axis = {q: 2 * n - 1 - q for q in range(n)}
    # Build einsum subscripts.
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if 2 * n > len(letters):
        raise ValueError("partial_trace: 큐비트 수가 너무 많습니다 (numpy einsum 한계)")
    subs = [""] * (2 * n)
    idx = 0
    # assign distinct letters to all axes first.
    for ax in range(2 * n):
        subs[ax] = letters[ax]
    # for traced qubits, force row axis letter == col axis letter (contract).
    for q in trace_out:
        subs[col_axis[q]] = subs[row_axis[q]]
    in_sub = "".join(subs)
    # output: keep qubits' row axes then col axes.  numpy reshape maps the
    # FIRST axis to the MSB, so to make the smallest kept qubit the LSB
    # (little-endian, matching panta / Qiskit) the axes are emitted in
    # DESCENDING qubit order (largest kept qubit = MSB = first axis).
    keep_desc = list(reversed(keep_sorted))
    out_rows = "".join(subs[row_axis[q]] for q in keep_desc)
    out_cols = "".join(subs[col_axis[q]] for q in keep_desc)
    out_sub = out_rows + out_cols
    reduced = np.einsum(f"{in_sub}->{out_sub}", rho_t)
    k = len(keep_sorted)
    return reduced.reshape(2**k, 2**k)


def von_neumann_entropy(state: npt.ArrayLike, base: float = 2.0) -> float:
    """von Neumann entropy ``S(ρ) = -Tr(ρ log ρ)`` (기본 밑 2, 단위 bit)."""
    rho = _as_density(state)
    evals = np.clip(np.linalg.eigvalsh(rho).real, 0.0, None)
    nz = evals[evals > 1e-12]
    if nz.size == 0:
        return 0.0
    s = -float(np.sum(nz * np.log(nz)))
    return s / float(np.log(base))


def entanglement_entropy(
    statevector: npt.ArrayLike, subsystem: list[int], num_qubits: int | None = None, base: float = 2.0
) -> float:
    """순수 상태의 bipartite entanglement entropy = ``subsystem`` reduced
    density matrix 의 von Neumann entropy."""
    reduced = partial_trace(statevector, subsystem, num_qubits)
    return von_neumann_entropy(reduced, base=base)


def trace_distance(a: npt.ArrayLike, b: npt.ArrayLike) -> float:
    """Trace distance ``½ Tr|ρ-σ|`` = ½ Σ|eigenvalues(ρ-σ)|."""
    rho = _as_density(a)
    sigma = _as_density(b)
    diff = rho - sigma
    evals = np.linalg.eigvalsh(diff).real
    return float(0.5 * np.sum(np.abs(evals)))
