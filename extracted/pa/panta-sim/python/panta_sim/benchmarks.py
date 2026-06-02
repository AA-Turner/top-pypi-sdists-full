"""Random Circuit Sampling (RCS) + Linear Cross-Entropy Benchmarking (XEB).

Google Sycamore-style supremacy 벤치마크 유틸 (v0.8).  random 회로 생성기와
linear XEB fidelity 측정을 제공한다.  XEB 는 양자 supremacy 의 표준 지표 —
이상적(noiseless) 회로면 `F_XEB ≈ 1` (Porter-Thomas), depolarizing noise 면
`F_XEB ≈ (1-p)^(게이트수)` 로 감소한다.

linear XEB:  ``F_XEB = 2^n · <p_ideal(x)>_samples − 1``
여기서 ``p_ideal(x) = |⟨x|C|0⟩|²``.  ideal 분포에서 뽑은 샘플이면 Porter-Thomas
(``E[2^n p] = 2``) 에 의해 ``F_XEB → 1``.  큰 N 에선 각 ``p_ideal(x)`` 를 Tensor
Network amplitude 로 계산한다 (Google 방식).
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from .circuit import QuantumCircuit


def random_circuit(
    n_qubits: int,
    depth: int,
    seed: Optional[int] = None,
    two_qubit: str = "cz",
    topology: str = "line",
    rows: Optional[int] = None,
    cols: Optional[int] = None,
) -> QuantumCircuit:
    """Random Circuit Sampling (RCS) 회로를 생성한다 (supremacy 벤치마크용).

    각 레이어 = 모든 큐비트에 random 단일 큐비트 게이트 (``√X``/``√Y``/``√W``
    아날로그로 random ``Rx, Rz``) + 얽힘 레이어 (``two_qubit`` 게이트를 brickwork
    패턴으로).  ``topology="grid"`` 면 2D 격자 (``rows×cols``, high treewidth),
    ``"line"`` 이면 1D 사슬.

    Args:
        n_qubits: 큐비트 수 (grid 면 ``rows*cols``).
        depth: 레이어 수.
        seed: RNG seed.
        two_qubit: 얽힘 게이트 — ``"cz"`` / ``"cx"`` / ``"iswap"``.
        topology: ``"line"`` 또는 ``"grid"`` (rows/cols 필요).

    Returns:
        ``QuantumCircuit``.
    """
    rng = np.random.default_rng(seed)
    if topology == "grid":
        if rows is None or cols is None:
            side = int(round(n_qubits**0.5))
            rows, cols = side, side
        n_qubits = rows * cols

        def qid(r, c):
            return r * cols + c

        h_pairs = [(qid(r, c), qid(r, c + 1)) for r in range(rows) for c in range(cols - 1)]
        v_pairs = [(qid(r, c), qid(r + 1, c)) for c in range(cols) for r in range(rows - 1)]
        layers = [h_pairs, v_pairs]
    else:
        even = [(q, q + 1) for q in range(0, n_qubits - 1, 2)]
        odd = [(q, q + 1) for q in range(1, n_qubits - 1, 2)]
        layers = [even, odd]

    qc = QuantumCircuit(n_qubits)

    def apply_2q(a, b):
        if two_qubit == "cx":
            qc.cx(a, b)
        elif two_qubit == "iswap":
            qc.iswap(a, b)
        else:
            qc.cz(a, b)

    for d in range(depth):
        # full SU(2) 단일 큐비트 게이트 (rz·rx·rz, 3 random angle) — Haar-random
        # 1q → Porter-Thomas scrambling (rx·rz 2-param 으론 부족).
        for q in range(n_qubits):
            qc.rz(float(rng.uniform(0, 2 * np.pi)), q)
            qc.rx(float(rng.uniform(0, 2 * np.pi)), q)
            qc.rz(float(rng.uniform(0, 2 * np.pi)), q)
        for a, b in layers[d % len(layers)]:
            apply_2q(a, b)
    return qc


def linear_xeb(circuit: QuantumCircuit, bitstrings, optimizer: str = "hyper") -> float:
    """주어진 측정 비트열들에 대한 linear XEB fidelity 를 계산한다.

    ``F_XEB = 2^n · mean_i p_ideal(x_i) − 1``.  각 ``p_ideal(x_i)`` 는 Tensor
    Network amplitude (``|⟨x_i|C|0⟩|²``) 로 계산하므로 **큰 N (statevector 불가)**
    에서도 동작한다 (Google supremacy 검증 방식).  ``bitstrings`` 가 ideal
    분포(또는 high-fidelity 디바이스)에서 나왔으면 ``F_XEB ≈ 1``.

    Args:
        circuit: 벤치마크 회로 (유니터리).
        bitstrings: 측정 비트열들 — 각각 str (Qiskit 표기) 또는 int 시퀀스.
        optimizer: TN contraction path 전략.

    Returns:
        linear XEB fidelity (float).
    """
    n = circuit.num_qubits
    dim = 1 << n
    # 배치 amplitude: path 1회 최적화 + 병렬 contraction (비트열마다 재계산 회피).
    amps = circuit.amplitudes(list(bitstrings), optimizer=optimizer)
    probs = [abs(a) ** 2 for a in amps]
    return dim * float(np.mean(probs)) - 1.0


def xeb_noisy(
    circuit: QuantumCircuit,
    p: float,
    shots: int = 4000,
    seed: Optional[int] = None,
) -> float:
    """**Depolarizing 노이즈** 하의 linear XEB fidelity (Sycamore supremacy 지표).

    회로를 확률 ``p`` 의 depolarizing 채널 (모든 게이트 후) 과 함께 trajectory
    샘플링하고, ideal 분포 ``p_ideal(x)=|⟨x|C|0⟩|²`` (정확 statevector) 에 대한
    ``F_XEB = 2ⁿ·mean_i p_ideal(xᵢ) − 1`` 를 계산한다.  noiseless (``p=0``) 면
    ``F_XEB≈1``, 노이즈가 커지면 (대략 ``(1−p)^{게이트수}`` 로) 0 으로 감쇠한다 —
    실제 양자 하드웨어의 XEB 충실도와 같은 척도.  작은 N (statevector) 용.

    Args:
        circuit: 벤치마크 회로 (유니터리).
        p: 게이트당 depolarizing 확률.
        shots: 샘플 수.
        seed: RNG seed.

    Returns:
        linear XEB fidelity (float).  ``p=0`` → ≈1, ``p`` 증가 → 감소.
    """
    from .noise import NoiseModel

    n = circuit.num_qubits
    dim = 1 << n
    ideal = np.abs(circuit.run(shots=0).statevector()) ** 2
    # 샘플링용 회로 (측정 추가) — 원본은 ideal statevector 계산에 그대로 둔다.
    meas = circuit.copy()
    meas.measure_all()
    if p <= 0.0:
        counts = meas.run(shots=shots, seed=seed).counts()
    else:
        nm = NoiseModel().add_depolarizing(float(p))
        counts = meas.run(shots=shots, seed=seed, noise_model=nm).counts()
    # counts 키는 MSB-first (왼쪽=큐비트 n-1) — statevector index 로 환산.
    total = 0
    acc = 0.0
    for bitstr, c in counts.items():
        idx = sum(((bitstr[n - 1 - q] == "1")) << q for q in range(n))
        acc += c * ideal[idx]
        total += c
    return dim * (acc / total) - 1.0


def xeb_ideal(
    circuit: QuantumCircuit,
    n_samples: int = 0,
    seed: Optional[int] = None,
    method: str = "statevector",
) -> dict:
    """이상적(noiseless) 회로의 XEB self-test (작은 N) — ``F_XEB ≈ 1`` 검증.

    전체 statevector 에서 ideal 분포를 얻어 ``n_samples`` 개 비트열을 ideal
    분포로 샘플하고 (또는 전체 분포로 정확히) linear XEB 를 계산한다.  random
    회로가 충분히 random 하면 Porter-Thomas 에 의해 ``F_XEB ≈ 1``, 분포의 정규화
    ``<2^n p> ≈ 1`` (uniform) / ``≈ 2`` (ideal 가중).

    Returns:
        ``{"xeb", "mean_2n_p", "porter_thomas_collision"}``.
        - ``xeb`` ≈ 1 (ideal).
        - ``mean_2n_p`` = ``2^n · mean_{ideal} p`` ≈ 2 (Porter-Thomas).
        - ``porter_thomas_collision`` = ``2^n · Σ p²`` ≈ 2 (random circuit).
    """
    n = circuit.num_qubits
    dim = 1 << n
    sv = circuit.run(shots=0, method=method).statevector()
    probs = np.abs(sv) ** 2
    probs = probs / probs.sum()
    # ideal 분포로 샘플 (n_samples=0 이면 전체 분포로 정확).
    if n_samples and n_samples > 0:
        rng = np.random.default_rng(seed)
        idx = rng.choice(dim, size=n_samples, p=probs)
        sampled_p = probs[idx]
        xeb = dim * float(np.mean(sampled_p)) - 1.0
        mean_2n_p = dim * float(np.mean(sampled_p))
    else:
        # 전체 분포 가중 평균 = Σ p·(2^n p) = 2^n Σ p².
        mean_2n_p = dim * float(np.sum(probs * probs))
        xeb = mean_2n_p - 1.0
    collision = dim * float(np.sum(probs * probs))
    return {"xeb": xeb, "mean_2n_p": mean_2n_p, "porter_thomas_collision": collision}
