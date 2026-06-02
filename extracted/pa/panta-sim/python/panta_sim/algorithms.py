"""표준 양자 알고리즘 빌딩블록 (v0.8.14).

자주 쓰이는 알고리즘 서브루틴을 native 게이트로 구성한 ``QuantumCircuit`` 빌더.
모든 함수는 Qiskit 교차검증되어 있고 전 백엔드 (statevector / MPS / TN /
stabilizer / GPU) 에서 동작한다.

- [`qft`] / [`inverse_qft`] : Quantum Fourier Transform.
- [`grover_diffusion`] : Grover 확산 연산자 (inversion about mean).
- [`grover`] : 마킹된 기저상태 검색 (oracle + diffusion 반복).
- [`quantum_phase_estimation`] : 위상 추정 (controlled-U^{2^k} + inverse QFT).

큐비트 규약: Qiskit 과 동일 (오른쪽 끝 = 큐비트 0).
"""

from __future__ import annotations

import math
from typing import Callable, Optional, Sequence

from .circuit import QuantumCircuit


def qft(
    qc: QuantumCircuit,
    qubits: Optional[Sequence[int]] = None,
    do_swaps: bool = True,
    inverse: bool = False,
) -> QuantumCircuit:
    """``qubits`` 에 Quantum Fourier Transform 을 추가한다 (in-place).

    Qiskit ``QFT`` 와 동일한 변환:  ``|j⟩ → (1/√N) Σ_k e^{2πi jk/N} |k⟩``
    (``do_swaps=True`` 면 끝에서 비트 reverse).  ``inverse=True`` 면 역변환.

    Args:
        qc: 대상 회로.
        qubits: 적용할 큐비트 (기본 전체).  ``qubits[0]`` 이 최하위 비트.
        do_swaps: 마지막 비트 reverse swap 포함 여부.
        inverse: 역 QFT.

    Returns:
        ``qc`` (chaining).
    """
    qs = list(range(qc.num_qubits)) if qubits is None else list(qubits)
    n = len(qs)
    if not inverse:
        for j in range(n - 1, -1, -1):
            qc.h(qs[j])
            for k in range(j - 1, -1, -1):
                qc.cp(math.pi / (2 ** (j - k)), qs[k], qs[j])
        if do_swaps:
            for i in range(n // 2):
                qc.swap(qs[i], qs[n - 1 - i])
    else:
        if do_swaps:
            for i in range(n // 2):
                qc.swap(qs[i], qs[n - 1 - i])
        for j in range(n):
            for k in range(j):
                qc.cp(-math.pi / (2 ** (j - k)), qs[k], qs[j])
            qc.h(qs[j])
    return qc


def inverse_qft(
    qc: QuantumCircuit,
    qubits: Optional[Sequence[int]] = None,
    do_swaps: bool = True,
) -> QuantumCircuit:
    """역 Quantum Fourier Transform ([`qft`] ``inverse=True``)."""
    return qft(qc, qubits, do_swaps=do_swaps, inverse=True)


def qft_circuit(n: int, do_swaps: bool = True, inverse: bool = False) -> QuantumCircuit:
    """``n`` 큐비트 QFT 만 담은 새 회로를 반환한다."""
    qc = QuantumCircuit(n)
    qft(qc, do_swaps=do_swaps, inverse=inverse)
    return qc


def grover_diffusion(
    qc: QuantumCircuit, qubits: Optional[Sequence[int]] = None
) -> QuantumCircuit:
    """Grover 확산 연산자 ``2|s⟩⟨s| − I`` 를 추가한다 (in-place).

    ``H^⊗n · (2|0⟩⟨0|−I) · H^⊗n`` — 평균 중심 반사 (inversion about the mean).
    ``2|0⟩⟨0|−I`` 는 다중제어 Z 로 구현 (전역 위상 무시).
    """
    qs = list(range(qc.num_qubits)) if qubits is None else list(qubits)
    n = len(qs)
    for q in qs:
        qc.h(q)
        qc.x(q)
    # 다중제어 Z = H·MCX·H on target.
    if n == 1:
        qc.z(qs[0])
    else:
        ctrls = qs[:-1]
        tgt = qs[-1]
        qc.h(tgt)
        qc.mcx(ctrls, tgt)
        qc.h(tgt)
    for q in qs:
        qc.x(q)
        qc.h(q)
    return qc


def grover(
    n: int,
    oracle: Callable[[QuantumCircuit], None],
    iterations: Optional[int] = None,
    num_solutions: int = 1,
    measure: bool = True,
) -> QuantumCircuit:
    """Grover 검색 회로를 만든다 (균등 중첩 → oracle + 확산 반복).

    Args:
        n: 검색공간 큐비트 수 (``N = 2ⁿ``).
        oracle: 마킹된 상태에 ``−1`` 위상을 거는 함수 (in-place, 회로 받음).
            예: 단일 마킹 상태 ``m`` → ``mcz``-스타일 phase flip.
        iterations: Grover 반복 횟수 (기본 ``⌊(π/4)√(N/M)⌋``, M=해 수).
        num_solutions: 해의 개수 ``M`` (반복 횟수 자동계산용).
        measure: ``True`` (기본) 면 끝에 ``measure_all`` 추가 (샘플링용).
            statevector 분석엔 ``False``.

    Returns:
        ``QuantumCircuit`` (``measure=True`` 면 측정 포함).
    """
    if iterations is None:
        N = 2**n
        iterations = max(1, int(math.floor((math.pi / 4) * math.sqrt(N / num_solutions))))
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
    for _ in range(iterations):
        oracle(qc)
        grover_diffusion(qc)
    if measure:
        qc.measure_all()
    return qc


def phase_oracle(n: int, marked: Sequence[int]) -> Callable[[QuantumCircuit], None]:
    """마킹된 기저상태들에 ``−1`` 위상을 거는 oracle 을 만든다 (Grover 용).

    Args:
        n: 큐비트 수.
        marked: 마킹할 기저상태 인덱스들 (정수).

    Returns:
        ``oracle(qc)`` 함수.
    """
    marked = list(marked)

    def oracle(qc: QuantumCircuit) -> None:
        for m in marked:
            # |m⟩ 에만 −1: X 로 0-비트를 1 로 만든 뒤 다중제어 Z, 복원.
            zeros = [q for q in range(n) if not ((m >> q) & 1)]
            for q in zeros:
                qc.x(q)
            if n == 1:
                qc.z(0)
            else:
                qc.h(n - 1)
                qc.mcx(list(range(n - 1)), n - 1)
                qc.h(n - 1)
            for q in zeros:
                qc.x(q)

    return oracle


def quantum_phase_estimation(
    n_counting: int,
    n_state: int,
    apply_controlled_unitary: Callable[[QuantumCircuit, int, int], None],
    state_prep: Optional[Callable[[QuantumCircuit, Sequence[int]], None]] = None,
    measure: bool = True,
) -> QuantumCircuit:
    """Quantum Phase Estimation 회로를 만든다.

    counting 레지스터 (``n_counting`` 큐비트, 인덱스 ``0..n_counting−1``) + state
    레지스터 (``n_state`` 큐비트).  ``U|ψ⟩ = e^{2πiφ}|ψ⟩`` 의 위상 ``φ`` 를 추정.

    Args:
        n_counting: counting 큐비트 수 (정밀도).
        n_state: eigenstate 레지스터 큐비트 수.
        apply_controlled_unitary: ``(qc, control, power)`` → controlled-``U^{2^power}``
            를 추가하는 함수.  state 레지스터는 ``n_counting..n_counting+n_state−1``.
        state_prep: ``(qc, state_qubits)`` → eigenstate 준비 (기본 |0…0⟩).

    Returns:
        QPE ``QuantumCircuit`` (counting 레지스터 측정 → ``φ ≈ (읽은 정수)/2^{n_counting}``).
    """
    total = n_counting + n_state
    qc = QuantumCircuit(total)
    state_qubits = list(range(n_counting, total))
    if state_prep is not None:
        state_prep(qc, state_qubits)
    for q in range(n_counting):
        qc.h(q)
    for q in range(n_counting):
        # counting 큐비트 q 가 U^{2^q} 를 제어.
        apply_controlled_unitary(qc, q, q)
    inverse_qft(qc, list(range(n_counting)), do_swaps=True)
    if measure:
        qc.measure_all()
    return qc


def ghz_state(n: int, measure: bool = False) -> QuantumCircuit:
    """``n`` 큐비트 GHZ 상태 ``(|0…0⟩ + |1…1⟩)/√2`` 회로."""
    qc = QuantumCircuit(n)
    qc.h(0)
    for q in range(n - 1):
        qc.cx(q, q + 1)
    if measure:
        qc.measure_all()
    return qc


def uniform_superposition(n: int) -> QuantumCircuit:
    """``n`` 큐비트 균등 중첩 ``H^⊗n|0⟩`` 회로."""
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
    return qc


def w_state(n: int) -> QuantumCircuit:
    """``n`` 큐비트 W 상태 ``(|10…0⟩+|01…0⟩+…+|0…01⟩)/√n`` 회로.

    표준 구성: 첫 큐비트에 `Ry` 로 진폭을 분배하고 controlled-`Ry` 사슬 + CNOT 로
    한 개의 여기(excitation) 를 펼친다.  (큐비트 ``q`` 가 비트 ``q``.)
    """
    if n < 1:
        raise ValueError("n ≥ 1")
    qc = QuantumCircuit(n)
    qc.x(n - 1)
    # 위에서 아래로 excitation 을 controlled-Ry + CX 로 분배.
    for i in range(n - 1, 0, -1):
        theta = 2.0 * math.acos(math.sqrt(1.0 / (i + 1)))
        qc.cry(theta, i, i - 1)
        qc.cx(i - 1, i)
    return qc


def draper_add_constant(
    qc: QuantumCircuit, a: int, qubits: Optional[Sequence[int]] = None
) -> QuantumCircuit:
    """QFT 기반 Draper 덧셈기: ``|x⟩ → |(x+a) mod 2ⁿ⟩`` (in-place).

    Fourier 기저에서 위상 회전만으로 정수 덧셈을 수행 (ancilla-free, 모듈러).
    ``qubits[0]`` = 최하위 비트.

    Args:
        qc: 대상 회로.
        a: 더할 정수 (음수면 뺄셈, mod 2ⁿ).
        qubits: 대상 레지스터 (기본 전체).
    """
    qs = list(range(qc.num_qubits)) if qubits is None else list(qubits)
    n = len(qs)
    qft(qc, qs, do_swaps=False)
    for j in range(n):
        # Fourier 기저에서 qubit j 에 위상 2π a 2^{n-1-j} / 2^n.
        qc.p(2.0 * math.pi * a * (2 ** (n - 1 - j)) / (2**n), qs[j])
    inverse_qft(qc, qs, do_swaps=False)
    return qc


def draper_add_register(
    qc: QuantumCircuit, reg_a: Sequence[int], reg_b: Sequence[int]
) -> QuantumCircuit:
    """QFT 기반 레지스터 덧셈: ``|a⟩|b⟩ → |a⟩|(a+b) mod 2ⁿ⟩`` (in-place).

    ``reg_b`` 에 ``reg_a`` 를 더한다 (``reg_a`` 불변).  두 레지스터 길이 동일,
    각 ``reg[0]`` = 최하위 비트.  Shor / 모듈러 산술의 빌딩블록.
    """
    a = list(reg_a)
    b = list(reg_b)
    n = len(b)
    if len(a) != n:
        raise ValueError("두 레지스터 길이가 같아야 합니다")
    qft(qc, b, do_swaps=False)
    for j in range(n):
        for k in range(n):
            # 상수 덧셈기의 a_k=1 기여를 a[k] 로 제어.
            angle = 2.0 * math.pi * (2**k) * (2 ** (n - 1 - j)) / (2**n)
            qc.cp(angle, a[k], b[j])
    inverse_qft(qc, b, do_swaps=False)
    return qc


def grover_operator(state_prep: QuantumCircuit, marked: Sequence[int]) -> QuantumCircuit:
    """Grover/진폭증폭 연산자 ``Q = A·(2|0⟩⟨0|−I)·A†·S_f`` 회로를 만든다.

    ``A = state_prep`` (``|ψ⟩=A|0⟩``), ``S_f`` 는 ``marked`` 기저상태 위상반전.
    ``Q^m A|0⟩`` 을 측정해 marked 에 들 확률은 ``sin²((2m+1)θ)`` (``a=sin²θ=
    P(marked|ψ)``) — amplitude estimation 의 핵심.

    Returns:
        ``Q`` (``state_prep.num_qubits`` 큐비트, 측정 미포함).
    """
    n = state_prep.num_qubits
    oracle = phase_oracle(n, marked)
    q = QuantumCircuit(n)
    # S_f: marked 위상반전.
    oracle(q)
    # A (2|0⟩⟨0|−I) A† = A · Z0-reflection · A†.
    a_inv = state_prep.inverse()
    q.compose(a_inv, inplace=True)
    # 2|0⟩⟨0|−I  (전역부호 무시: |0> 제외 위상반전 = X^n·mcz·X^n).
    for i in range(n):
        q.x(i)
    if n == 1:
        q.z(0)
    else:
        q.h(n - 1)
        q.mcx(list(range(n - 1)), n - 1)
        q.h(n - 1)
    for i in range(n):
        q.x(i)
    q.compose(state_prep, inplace=True)
    return q


def amplitude_estimation(
    state_prep: QuantumCircuit,
    marked: Sequence[int],
    powers: Optional[Sequence[int]] = None,
    shots: int = 2048,
    seed: Optional[int] = None,
) -> float:
    """Maximum-Likelihood Amplitude Estimation (controlled-Q 불필요).

    ``a = P(marked | A|0⟩)`` 를 추정한다.  각 power ``m`` 에 대해 ``Q^m A|0⟩`` 을
    측정해 marked 빈도를 세고, 우도 ``∏ sin²((2m+1)θ)^{h} cos²(·)^{N−h}`` 를
    ``θ∈[0,π/2]`` 에서 최대화 (격자 + 세분).  ``a = sin²θ`` 반환.

    Args:
        state_prep: ``A`` (``|ψ⟩ = A|0⟩``).
        marked: "good" 기저상태 인덱스들.
        powers: Grover power schedule (기본 ``[0,1,2,4,8]``).
        shots / seed: power 당 측정 수 / RNG seed.

    Returns:
        추정 진폭 ``a ∈ [0,1]``.
    """
    import numpy as np

    n = state_prep.num_qubits
    marked_set = set(int(m) for m in marked)
    if powers is None:
        powers = [0, 1, 2, 4, 8]
    q_op = grover_operator(state_prep, marked)
    data = []  # (m, hits, shots)
    for idx, m in enumerate(powers):
        qc = QuantumCircuit(n)
        qc.compose(state_prep, inplace=True)
        for _ in range(m):
            qc.compose(q_op, inplace=True)
        qc.measure_all()
        sd = None if seed is None else seed + idx
        counts = qc.run(shots=shots, seed=sd).counts()
        hits = sum(v for k, v in counts.items() if int(k, 2) in marked_set)
        data.append((m, hits, shots))

    # MLAE: θ 격자 + 세분.
    def neg_loglik(theta):
        ll = 0.0
        for m, h, N in data:
            p = math.sin((2 * m + 1) * theta) ** 2
            p = min(max(p, 1e-12), 1 - 1e-12)
            ll += h * math.log(p) + (N - h) * math.log(1 - p)
        return -ll

    lo, hi = 0.0, math.pi / 2
    best = lo
    for _ in range(6):  # 반복 세분
        grid = np.linspace(lo, hi, 200)
        vals = [neg_loglik(t) for t in grid]
        bi = int(np.argmin(vals))
        best = grid[bi]
        step = (hi - lo) / 200
        lo, hi = max(0.0, best - step), min(math.pi / 2, best + step)
    return float(math.sin(best) ** 2)


def quantum_counting(
    n: int,
    marked: Sequence[int],
    powers: Optional[Sequence[int]] = None,
    shots: int = 4096,
    seed: Optional[int] = None,
) -> float:
    """마킹된 기저상태 개수 `M` 을 추정한다 (amplitude estimation 기반).

    균등 중첩 `A = H^⊗n` 에서 `a = M/2ⁿ` 를 [`amplitude_estimation`] (MLAE) 으로
    추정하고 `M = a·2ⁿ` 반환.  Grover 검색의 해 개수를 모를 때 사용.

    Args:
        n: 큐비트 수 (`N = 2ⁿ`).
        marked: "good" 기저상태 인덱스들.
        powers / shots / seed: amplitude estimation 파라미터.

    Returns:
        추정 해 개수 `M` (실수; 반올림하면 정수 추정).
    """
    a = amplitude_estimation(
        uniform_superposition(n), marked, powers=powers, shots=shots, seed=seed
    )
    return a * (2**n)


def bernstein_vazirani(secret: Sequence[int]) -> QuantumCircuit:
    """Bernstein–Vazirani 회로: 단일 쿼리로 비밀 문자열 ``s`` 를 복원한다.

    오라클 ``f(x) = s·x mod 2`` 를 phase 로 구현 (s_i=1 인 큐비트에 CX → ancilla).
    측정 결과 = ``s`` (반전 비트열).

    Args:
        secret: 비밀 비트열 (``s[0]`` = 큐비트 0).

    Returns:
        측정 포함 ``QuantumCircuit`` (n+1 큐비트, 마지막은 phase ancilla).
    """
    s = [int(b) & 1 for b in secret]
    n = len(s)
    qc = QuantumCircuit(n + 1)
    qc.x(n)  # ancilla |1⟩
    for q in range(n + 1):
        qc.h(q)
    for i in range(n):
        if s[i]:
            qc.cx(i, n)  # phase kickback: f(x)=s·x
    for q in range(n):
        qc.h(q)
    for q in range(n):
        qc.measure(q, q)
    return qc


def deutsch_jozsa(n: int, oracle: Callable[[QuantumCircuit], None]) -> QuantumCircuit:
    """Deutsch–Jozsa 회로: ``f`` 가 상수면 측정 ``0…0``, balanced 면 비-0.

    Args:
        n: 입력 큐비트 수 (회로는 n+1 큐비트, 마지막은 phase ancilla).
        oracle: ``f`` 를 phase 로 거는 함수 (입력 큐비트 0..n-1, ancilla n).

    Returns:
        측정 포함 ``QuantumCircuit``.
    """
    qc = QuantumCircuit(n + 1)
    qc.x(n)
    for q in range(n + 1):
        qc.h(q)
    oracle(qc)
    for q in range(n):
        qc.h(q)
    for q in range(n):
        qc.measure(q, q)
    return qc
