"""변분 양자 알고리즘 (VQE / QAOA) + 자동 미분 (v0.7).

panta-sim 의 네이티브 Pauli 기댓값 (:meth:`SimulationResult.expectation`,
v0.7 Cut 1) 위에 parameter-shift gradient 와 VQE/QAOA 드라이버를 올린다.

ansatz 는 **callable** ``ansatz(params) -> QuantumCircuit`` 형태 — PennyLane /
Qiskit 의 변분 패턴과 동일하며 심볼릭 파라미터 인프라가 필요 없다.

핵심 함수:
- :func:`expectation` — `⟨ψ(θ)|H|ψ(θ)⟩`.
- :func:`parameter_shift_gradient` — Pauli-rotation 게이트 (Rx/Ry/Rz/CRx/CRy/
  CRz) 에 대해 해석적 gradient `∂⟨H⟩/∂θⱼ = ½[f(θ+π/2·eⱼ) − f(θ−π/2·eⱼ)]`.
- :func:`finite_difference_gradient` — 임의 게이트용 수치 gradient (fallback).
- :class:`VQE` — 비용 = `⟨H⟩` 최소화 (scipy.optimize 또는 내장 gradient descent).
- :func:`qaoa_maxcut_ansatz` / :func:`maxcut_hamiltonian` — QAOA MaxCut 템플릿.
"""

from __future__ import annotations

import math
from typing import Callable, Optional, Sequence

import numpy as np

from .circuit import QuantumCircuit

Ansatz = Callable[[Sequence[float]], QuantumCircuit]


def _bind_ansatz(ansatz, params) -> QuantumCircuit:
    """ansatz 를 회로로 바인딩한다.

    - **callable**: ``ansatz(list(params))`` 호출 (기존 방식).
    - **파라메트릭 QuantumCircuit**: ``assign_parameters(params)`` (이름 오름차순
      위치 대응) — 표준 Qiskit Parameter 워크플로.
    """
    if isinstance(ansatz, QuantumCircuit):
        return ansatz.assign_parameters(list(params))
    return ansatz(list(params))


def expectation(
    ansatz: Ansatz,
    params: Sequence[float],
    observable,
    **run_kwargs,
) -> float:
    """`⟨ψ(params)|H|ψ(params)⟩` 를 계산한다.

    Args:
        ansatz: ``params -> QuantumCircuit`` callable, 또는 심볼릭
            :class:`Parameter` 를 가진 파라메트릭 :class:`QuantumCircuit`
            (이름 오름차순으로 ``params`` 와 위치 대응).
        params: 파라미터 벡터.
        observable: Pauli observable (dict / list / SparsePauliOp).
        **run_kwargs: :meth:`QuantumCircuit.expectation` 에 전달 (예: ``method``).
    """
    qc = _bind_ansatz(ansatz, params)
    return qc.expectation(observable, **run_kwargs)


def parameter_shift_gradient(
    ansatz: Ansatz,
    params: Sequence[float],
    observable,
    *,
    shift: float = math.pi / 2,
    **run_kwargs,
) -> np.ndarray:
    """Parameter-shift rule 로 `∇_θ ⟨H⟩` 를 계산한다.

    각 파라미터가 Pauli-rotation 게이트 (생성자 고유값 ±½, 예: Rx/Ry/Rz/
    CRx/CRy/CRz) 의 각도로 **정확히 한 번** 들어갈 때 해석적으로 정확하다:

        ∂⟨H⟩/∂θⱼ = ½ [ f(θ + (π/2)·eⱼ) − f(θ − (π/2)·eⱼ) ].

    일반 게이트 (P, U 등) 나 파라미터 공유가 있으면
    :func:`finite_difference_gradient` 를 사용하라.

    Returns:
        ``numpy.ndarray`` shape ``(len(params),)``.
    """
    params = np.asarray(params, dtype=float)
    grad = np.zeros(len(params))
    factor = 1.0 / (2.0 * math.sin(shift))  # shift=π/2 → ½.
    for j in range(len(params)):
        p_plus = params.copy()
        p_minus = params.copy()
        p_plus[j] += shift
        p_minus[j] -= shift
        e_plus = expectation(ansatz, p_plus, observable, **run_kwargs)
        e_minus = expectation(ansatz, p_minus, observable, **run_kwargs)
        grad[j] = factor * (e_plus - e_minus)
    return grad


def finite_difference_gradient(
    ansatz: Ansatz,
    params: Sequence[float],
    observable,
    *,
    eps: float = 1e-6,
    **run_kwargs,
) -> np.ndarray:
    """중심 차분 수치 gradient (임의 게이트 ansatz 용 fallback)."""
    params = np.asarray(params, dtype=float)
    grad = np.zeros(len(params))
    for j in range(len(params)):
        p_plus = params.copy()
        p_minus = params.copy()
        p_plus[j] += eps
        p_minus[j] -= eps
        e_plus = expectation(ansatz, p_plus, observable, **run_kwargs)
        e_minus = expectation(ansatz, p_minus, observable, **run_kwargs)
        grad[j] = (e_plus - e_minus) / (2.0 * eps)
    return grad


class VQEResult:
    """:class:`VQE` 의 최적화 결과."""

    def __init__(
        self,
        optimal_params: np.ndarray,
        optimal_value: float,
        history: list[float],
        nit: int,
        success: bool,
    ) -> None:
        self.optimal_params = optimal_params
        self.optimal_value = optimal_value
        self.history = history
        self.nit = nit
        self.success = success

    def __repr__(self) -> str:
        return (
            f"VQEResult(optimal_value={self.optimal_value:.8f}, "
            f"nit={self.nit}, success={self.success})"
        )


class VQE:
    """Variational Quantum Eigensolver.

    비용 함수 `E(θ) = ⟨ψ(θ)|H|ψ(θ)⟩` 를 최소화해 Hamiltonian ``H`` 의
    바닥상태 에너지 근사치를 찾는다.

    Args:
        ansatz: ``params -> QuantumCircuit`` callable.
        hamiltonian: Pauli observable (dict / list / SparsePauliOp).
        optimizer: ``"gradient-descent"`` (내장) 또는 scipy.optimize method
            이름 (``"COBYLA"``, ``"L-BFGS-B"``, ``"BFGS"`` 등 — scipy 필요).
        gradient: ``"parameter-shift"`` (기본) / ``"finite-difference"`` /
            ``None`` (gradient-free).  gradient-based optimizer 에만 영향.
        maxiter: 최대 반복 횟수.
        learning_rate: gradient-descent 학습률.
        run_kwargs: 각 회로 실행에 전달 (예: ``method="statevector"``).
    """

    def __init__(
        self,
        ansatz: Ansatz,
        hamiltonian,
        *,
        optimizer: str = "gradient-descent",
        gradient: str | None = "parameter-shift",
        maxiter: int = 200,
        learning_rate: float = 0.1,
        tol: float = 1e-8,
        spsa_a: float = 1.0,
        spsa_c: float = 0.1,
        spsa_seed: int | None = None,
        **run_kwargs,
    ) -> None:
        self.ansatz = ansatz
        self.hamiltonian = hamiltonian
        self.optimizer = optimizer
        self.gradient = gradient
        self.maxiter = maxiter
        self.learning_rate = learning_rate
        self.tol = tol
        self.spsa_a = spsa_a
        self.spsa_c = spsa_c
        self.spsa_seed = spsa_seed
        self.run_kwargs = run_kwargs

    def energy(self, params: Sequence[float]) -> float:
        """주어진 파라미터에서의 에너지 `⟨H⟩`."""
        return expectation(self.ansatz, params, self.hamiltonian, **self.run_kwargs)

    def _grad(self, params: Sequence[float]) -> np.ndarray:
        if self.gradient == "parameter-shift":
            return parameter_shift_gradient(
                self.ansatz, params, self.hamiltonian, **self.run_kwargs
            )
        if self.gradient == "finite-difference":
            return finite_difference_gradient(
                self.ansatz, params, self.hamiltonian, **self.run_kwargs
            )
        raise ValueError(f"gradient {self.gradient!r} 는 gradient 벡터를 제공하지 않습니다")

    def run(self, initial_params: Sequence[float]) -> VQEResult:
        """최적화를 실행해 :class:`VQEResult` 를 반환한다."""
        x0 = np.asarray(initial_params, dtype=float)
        history: list[float] = []

        def cost(p):
            e = self.energy(p)
            history.append(float(e))
            return e

        if self.optimizer == "gradient-descent":
            return self._run_gradient_descent(x0, cost, history)
        if self.optimizer == "spsa":
            return self._run_spsa(x0, cost, history)
        return self._run_scipy(x0, cost, history)

    def _run_spsa(self, x0, cost, history) -> VQEResult:
        """SPSA (Simultaneous Perturbation Stochastic Approximation).

        shot-noise / NISQ VQE 의 표준 최적화기 — 매 iteration 당 cost 평가 2회
        (gradient 평가 없이) 로 모든 파라미터를 동시 섭동해 추정 gradient 로
        업데이트한다.  Spall (1998) 표준 gain 스케줄.
        """
        rng = np.random.default_rng(self.spsa_seed)
        x = x0.copy()
        a, c = self.spsa_a, self.spsa_c
        A = 0.1 * self.maxiter
        alpha, gamma = 0.602, 0.101
        best_x, best_f = x.copy(), float(cost(x))
        for k in range(self.maxiter):
            ak = a / (k + 1 + A) ** alpha
            ck = c / (k + 1) ** gamma
            delta = rng.choice([-1.0, 1.0], size=len(x))
            fp = cost(x + ck * delta)
            fm = cost(x - ck * delta)
            ghat = (fp - fm) / (2.0 * ck) * delta
            x = x - ak * ghat
            fx = float(cost(x))
            if fx < best_f:
                best_f, best_x = fx, x.copy()
        return VQEResult(best_x, best_f, history, self.maxiter, True)

    def _run_gradient_descent(self, x0, cost, history) -> VQEResult:
        x = x0.copy()
        prev = cost(x)
        for it in range(self.maxiter):
            g = self._grad(x)
            x = x - self.learning_rate * g
            cur = cost(x)
            if abs(cur - prev) < self.tol:
                return VQEResult(x, cur, history, it + 1, True)
            prev = cur
        return VQEResult(x, prev, history, self.maxiter, True)

    def _run_scipy(self, x0, cost, history) -> VQEResult:
        try:
            from scipy.optimize import minimize
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "scipy optimizer 를 쓰려면 scipy 가 필요합니다 "
                "(pip install scipy) 또는 optimizer='gradient-descent' 사용"
            ) from exc

        gradient_methods = {"BFGS", "L-BFGS-B", "CG", "TNC", "SLSQP"}
        jac = None
        if self.gradient is not None and self.optimizer in gradient_methods:
            jac = lambda p: self._grad(p)  # noqa: E731

        res = minimize(
            cost,
            x0,
            method=self.optimizer,
            jac=jac,
            options={"maxiter": self.maxiter},
            tol=self.tol,
        )
        return VQEResult(
            np.asarray(res.x),
            float(res.fun),
            history,
            int(getattr(res, "nit", len(history))),
            bool(res.success),
        )


# ----------------------------------------------------------------------------
# QAOA MaxCut 템플릿
# ----------------------------------------------------------------------------


def maxcut_hamiltonian(edges: Sequence[tuple[int, int]], n_qubits: int) -> dict[str, float]:
    """MaxCut cost Hamiltonian `H_C = Σ_{(i,j)∈E} ½(Zᵢ Zⱼ − I)`.

    최소화하면 (= 바닥상태) 최대 cut 에 해당한다.  상수항 `−|E|/2` 는 생략하고
    `Σ ½ Zᵢ Zⱼ` 항만 반환해도 argmin 은 동일하지만, 에너지 절대값을 MaxCut
    값과 맞추기 위해 상수 포함 형태 (`½ ZZ − ½ I`) 로 돌려준다.

    Returns:
        Pauli string → coeff dict (``QuantumCircuit.expectation`` 형식).
    """
    terms: dict[str, float] = {}
    ident = "I" * n_qubits
    for i, j in edges:
        label = ["I"] * n_qubits
        # 라벨 오른쪽 끝 = 큐비트 0.
        label[n_qubits - 1 - i] = "Z"
        label[n_qubits - 1 - j] = "Z"
        key = "".join(label)
        terms[key] = terms.get(key, 0.0) + 0.5
        terms[ident] = terms.get(ident, 0.0) - 0.5
    return terms


def qaoa_maxcut_ansatz(
    edges: Sequence[tuple[int, int]], n_qubits: int, p: int = 1
) -> Ansatz:
    """QAOA MaxCut ansatz callable 을 반환한다 (depth ``p``).

    파라미터 벡터는 길이 ``2p``: ``[γ₀, β₀, γ₁, β₁, ...]``.  표준 QAOA:
    `|ψ⟩ = ∏_l e^{-iβ_l H_M} e^{-iγ_l H_C} H^{⊗n}|0⟩`, `H_M = Σ Xᵢ`,
    `H_C = Σ_{(i,j)} ½ Zᵢ Zⱼ`.  cost-layer `e^{-iγ ½ ZᵢZⱼ}` 는 CX·Rz(γ)·CX.
    """

    def ansatz(params: Sequence[float]) -> QuantumCircuit:
        if len(params) != 2 * p:
            raise ValueError(f"QAOA p={p} 는 파라미터 {2 * p} 개가 필요합니다 (입력 {len(params)})")
        qc = QuantumCircuit(n_qubits)
        for q in range(n_qubits):
            qc.h(q)
        for layer in range(p):
            gamma = params[2 * layer]
            beta = params[2 * layer + 1]
            # cost layer: e^{-i γ ½ Z_i Z_j} = CX(i,j) Rz(γ) CX(i,j) (target j).
            for i, j in edges:
                qc.cx(i, j)
                qc.rz(gamma, j)
                qc.cx(i, j)
            # mixer layer: e^{-i β X_q} = Rx(2β).
            for q in range(n_qubits):
                qc.rx(2.0 * beta, q)
        return qc

    return ansatz


def qaoa_ansatz(cost_hamiltonian: dict, p: int = 1, n_qubits: Optional[int] = None) -> Ansatz:
    """임의 cost 해밀토니안에 대한 QAOA ansatz callable 을 반환한다 (v0.7.1).

    ``qaoa_maxcut_ansatz`` 의 일반화 — MaxCut 뿐 아니라 가중 그래프 / Ising /
    number partitioning 등 임의의 (대각이 아니어도 되는) Pauli cost
    해밀토니안 ``H_C`` 에 대해 cost layer ``e^{-iγ H_C}`` 를
    :func:`panta_sim.evolution.pauli_evolution` gadget 으로 정확히 구현한다.

    ``|ψ⟩ = ∏_l e^{-iβ_l H_M} e^{-iγ_l H_C} · H^{⊗n}|0⟩``, mixer
    ``H_M = Σ Xᵢ`` (``e^{-iβ H_M} = ∏ Rx(2β)``).

    Args:
        cost_hamiltonian: Pauli string → 계수 dict.
        p: QAOA depth (layer 수).
        n_qubits: 큐비트 수 (생략 시 Pauli string 길이에서 추론).

    Returns:
        ``params -> QuantumCircuit`` callable.  파라미터 벡터 길이 ``2p``:
        ``[γ₀, β₀, γ₁, β₁, ...]`` (``qaoa_maxcut_ansatz`` 와 동일 컨벤션).
    """
    from .evolution import pauli_evolution

    lengths = {len(k) for k in cost_hamiltonian}
    if len(lengths) != 1:
        raise ValueError(f"cost_hamiltonian Pauli string 길이 불일치: {lengths}")
    n = n_qubits if n_qubits is not None else lengths.pop()
    terms = [(s, float(c)) for s, c in cost_hamiltonian.items() if set(s) != {"I"} and c != 0.0]

    def ansatz(params: Sequence[float]) -> QuantumCircuit:
        if len(params) != 2 * p:
            raise ValueError(f"QAOA p={p} 는 파라미터 {2 * p} 개가 필요합니다 (입력 {len(params)})")
        qc = QuantumCircuit(n)
        for q in range(n):
            qc.h(q)
        for layer in range(p):
            gamma = params[2 * layer]
            beta = params[2 * layer + 1]
            for pauli, c in terms:  # e^{-iγ H_C} = ∏ e^{-iγc P}
                pauli_evolution(qc, pauli, gamma * c)
            for q in range(n):
                qc.rx(2.0 * beta, q)
        return qc

    return ansatz
