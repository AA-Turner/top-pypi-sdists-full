"""Pauli propagation (Heisenberg) 기반 기댓값 추정 — 큰 N · 낮은 비-Clifford성.

관측량 ``O`` 를 회로 ``U`` 를 통해 역전파(Heisenberg)해 ``⟨0|U†OU|0⟩`` 를 추정한다.
상태를 weighted Pauli 합으로 표현하므로 **얽힘에 제약받지 않는다** (Tensor Network 의
보완재).  비-Clifford 게이트(Rz/Rx/Ry/T…)는 Pauli 항을 분기시키며, 계수 절댓값이
``threshold`` 미만인 항을 버려(truncation) 다항적으로 유지한다.  Monte-Carlo 변형
(`pauli_propagation_expectation_mc`)은 결정론적 truncation 대신 **무편향** 확률적
재표본으로 budget 을 유지한다.

참고: Angrisani et al., *Pauli Propagation* (arXiv:2505.21606, 2025).

정확성: truncation 없이는(threshold=0) exact statevector 기댓값과 일치한다 (검증).
각 게이트의 Pauli 켤레는 dense 행렬 분해로 유도해(부호 자동) 손계산 오류가 없다.

표현: Pauli 항 = ``(x_mask, z_mask) -> 복소계수``, 큐비트 q 의 라벨은
``I=(0,0) / X=(1,0) / Y=(1,1) / Z=(0,1)``.  ``⟨0|항|0⟩`` = (x_mask==0 이면 1).
"""

from __future__ import annotations

from functools import reduce
from itertools import product

import numpy as np

_I = np.eye(2, dtype=complex)
_X = np.array([[0, 1], [1, 0]], dtype=complex)
_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_PAULI = [_I, _X, _Y, _Z]
_LABEL_XZ = {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (0, 1)}  # I,X,Y,Z → (x,z)

_s = 1.0 / np.sqrt(2.0)


def _gate_matrix(name: str, params: tuple) -> tuple[np.ndarray, int]:
    """게이트 이름/파라미터 → (행렬, 큐비트수).  큐비트 순서: qubits[0]=MSB."""
    name = name.lower()
    one = {
        "h": np.array([[_s, _s], [_s, -_s]], dtype=complex),
        "x": _X, "y": _Y, "z": _Z, "id": _I,
        "s": np.array([[1, 0], [0, 1j]], dtype=complex),
        "sdg": np.array([[1, 0], [0, -1j]], dtype=complex),
        "t": np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex),
        "tdg": np.array([[1, 0], [0, np.exp(-1j * np.pi / 4)]], dtype=complex),
        "sx": 0.5 * np.array([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]], dtype=complex),
        "sxdg": 0.5 * np.array([[1 - 1j, 1 + 1j], [1 + 1j, 1 - 1j]], dtype=complex),
    }
    if name in one:
        return one[name], 1
    if name in ("rx", "ry", "rz", "p", "u1"):
        th = float(params[0])
        c, sn = np.cos(th / 2), np.sin(th / 2)
        if name == "rx":
            return np.array([[c, -1j * sn], [-1j * sn, c]], dtype=complex), 1
        if name == "ry":
            return np.array([[c, -sn], [sn, c]], dtype=complex), 1
        if name == "rz":
            return np.array([[np.exp(-1j * th / 2), 0], [0, np.exp(1j * th / 2)]], dtype=complex), 1
        return np.array([[1, 0], [0, np.exp(1j * th)]], dtype=complex), 1
    # 2-큐비트.
    if name in ("cx", "cnot"):
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex), 2
    if name == "cz":
        return np.diag([1, 1, 1, -1]).astype(complex), 2
    if name == "cy":
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1j], [0, 0, 1j, 0]], dtype=complex), 2
    if name == "swap":
        return np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex), 2
    if name == "iswap":
        return np.array([[1, 0, 0, 0], [0, 0, 1j, 0], [0, 1j, 0, 0], [0, 0, 0, 1]], dtype=complex), 2
    # 2q parametric Pauli-pair 회전 exp(-iθ/2 P⊗P) = cos(θ/2)·I − i·sin(θ/2)·(P⊗P)
    # (P⊗P 가 involutory ((P⊗P)²=I) 라 닫힌 형식; 대칭이라 큐비트 순서 무관).
    if name in ("rzz", "rxx", "ryy"):
        th = float(params[0])
        pp = {"rzz": np.kron(_Z, _Z), "rxx": np.kron(_X, _X), "ryy": np.kron(_Y, _Y)}[name]
        return np.cos(th / 2.0) * np.eye(4, dtype=complex) - 1j * np.sin(th / 2.0) * pp, 2
    # 3-큐비트 (permutation).
    if name in ("ccx", "toffoli"):
        m = np.eye(8, dtype=complex)
        m[[6, 7]] = m[[7, 6]]  # |110>↔|111>
        return m, 3
    if name in ("cswap", "fredkin"):
        m = np.eye(8, dtype=complex)
        m[[5, 6]] = m[[6, 5]]  # |101>↔|110>
        return m, 3
    raise ValueError(
        f"Pauli propagation 미지원 게이트: {name!r} "
        "(지원: 1q Clifford+rx/ry/rz/t/p, cx/cz/cy/swap/iswap, rzz/rxx/ryy, ccx/cswap)"
    )


def _decompose_kq(g: np.ndarray, k: int) -> dict:
    """g†·(P_0⊗…⊗P_{k-1})·g 를 k-큐비트 Pauli 기저로 분해.

    반환: ``{ ((x0,z0),…) : [ (((x0',z0'),…), coeff), … ] }`` (qubits[0]=MSB 순서).
    """
    gd = g.conj().T
    dim = 1 << k
    basis = []  # (label_tuple, matrix, xz_tuple)
    for labels in product(range(4), repeat=k):
        mat = reduce(np.kron, (_PAULI[lab] for lab in labels))
        xz = tuple(_LABEL_XZ[lab] for lab in labels)
        basis.append((xz, mat))
    out: dict = {}
    for xz_in, p in basis:
        m = gd @ p @ g
        terms = []
        for xz_out, q in basis:
            c = np.trace(q.conj().T @ m) / dim
            if abs(c) > 1e-12:
                terms.append((xz_out, complex(c)))
        out[xz_in] = terms
    return out


def _parse_observable(observable, n: int) -> dict:
    """관측량 → {(x_mask, z_mask): coeff}.  Pauli 라벨 Qiskit 규약(오른쪽=큐비트0)."""
    from .circuit import _normalize_pauli_terms

    terms = _normalize_pauli_terms(observable, n)
    out: dict[tuple[int, int], complex] = {}
    for ps, re, im in terms:
        x_mask = z_mask = 0
        for q in range(n):
            ch = ps[n - 1 - q]
            xz = {"I": (0, 0), "X": (1, 0), "Y": (1, 1), "Z": (0, 1)}[ch]
            if xz[0]:
                x_mask |= 1 << q
            if xz[1]:
                z_mask |= 1 << q
        out[(x_mask, z_mask)] = out.get((x_mask, z_mask), 0j) + complex(re, im)
    return out


def _iter_gates(circuit):
    """(matrix-map-key, qubits, name, params) 를 회로 순서로 yield (미지원 게이트는 raise)."""
    for name, qubits, params in circuit._ops:
        if name in ("measure", "measure_all", "reset", "barrier"):
            continue
        yield name, tuple(qubits), tuple(params)


def _apply_gate_map(terms, cmap, qubits, k):
    """terms (dict) 에 k-큐비트 켤레맵 cmap 를 qubits 에 적용한 새 terms."""
    bits = [1 << q for q in qubits]
    clear = 0
    for b in bits:
        clear |= b
    new_terms: dict[tuple[int, int], complex] = {}
    for (xm, zm), coeff in terms.items():
        key = tuple((1 if xm & bits[i] else 0, 1 if zm & bits[i] else 0) for i in range(k))
        base_x = xm & ~clear
        base_z = zm & ~clear
        for out_xz, c in cmap[key]:
            nx, nz = base_x, base_z
            for i in range(k):
                if out_xz[i][0]:
                    nx |= bits[i]
                if out_xz[i][1]:
                    nz |= bits[i]
            new_terms[(nx, nz)] = new_terms.get((nx, nz), 0j) + coeff * c
    return new_terms


def _apply_depolarizing(terms, qubits, p):
    """게이트가 닿는 큐비트마다 depolarizing(p) 의 Heisenberg 작용을 적용한다.

    convention: panta depolarizing Kraus = `I` w.p. (1-3p/4), `X/Y/Z` 각 p/4
    (`core::noise` 와 일치).  Pauli 채널은 Pauli 기저에서 대각 → 분기 없이 계수만
    스케일.  단일큐비트 traceless Pauli P 에 대해
    `D†(P) = (1-3p/4)P + (p/4)(XPX+YPY+ZPZ) = (1-3p/4 - p/4)P = (1-p)P`
    (`XPX+YPY+ZPZ = -P`).  즉 게이트가 닿는 큐비트 중 비-I 라벨마다 (1-p) 를 곱한다.
    """
    if p <= 0.0:
        return terms
    factor = 1.0 - p
    out: dict[tuple[int, int], complex] = {}
    for (xm, zm), coeff in terms.items():
        c = coeff
        for q in qubits:
            b = 1 << q
            if (xm & b) or (zm & b):  # 큐비트 q 가 X/Y/Z (비-I)
                c *= factor
        out[(xm, zm)] = out.get((xm, zm), 0j) + c
    return out


def pauli_propagation_expectation(
    circuit,
    observable,
    threshold: float = 1e-10,
    max_terms: int = 2_000_000,
    depolarizing: float = 0.0,
) -> complex:
    """``⟨0|U†OU|0⟩`` 를 Pauli 역전파로 추정한다 (결정론적 truncation).

    Args:
        circuit: ``QuantumCircuit`` (지원: 1q Clifford + rx/ry/rz/t/tdg/p,
            cx/cz/cy/swap/iswap, ccx/cswap).
        observable: ``dict`` / ``list[(str,coeff)]`` / SparsePauliOp (Qiskit 규약).
        threshold: 계수 절댓값 컷오프 (0 이면 정확).
        max_terms: 항 수 상한 (초과 시 ``ValueError``).
        depolarizing: 게이트당 depolarizing 확률 `p` (>0 이면 noisy 기댓값
            `Tr(ρH)`).  Pauli 채널은 Pauli 기저에서 대각이라 분기 없이 게이트가
            닿는 큐비트의 비-I 라벨마다 계수를 `(1-p)` 로 감쇠 → noiseless 와 동일
            비용 (core::noise 의 `K_0=√(1-3p/4) I, K_{1..3}=√(p/4) X/Y/Z` 규약에서
            `D†(P)=(1-p)P`).  density 백엔드 `Tr(ρH)` 와 1e-9 일치 (검증).

    Returns:
        기댓값 (복소; Hermitian observable 이면 허수부 ≈ 0).
    """
    n = circuit.num_qubits
    terms = _parse_observable(observable, n)
    cache: dict = {}
    gates = list(_iter_gates(circuit))
    for name, qubits, params in reversed(gates):
        g, k = _gate_matrix(name, params)
        key_gp = (name, params)
        if key_gp not in cache:
            cache[key_gp] = _decompose_kq(g, k)
        cmap = cache[key_gp]
        # 노이즈는 forward 에서 게이트 *직후* → Heisenberg 역전파에서는 게이트 켤레
        # *직전* 에 채널 adjoint 를 적용한다 (Λ = noise∘G → Λ† = G†∘noise†).
        terms = _apply_depolarizing(terms, qubits, depolarizing)
        new_terms = _apply_gate_map(terms, cmap, qubits, k)
        # truncation *이전* 의 항 수도 검사 — 고분기 게이트에서 truncation 이
        # 강해 post-count 는 작아도 new_terms 가 메모리를 폭발시킬 수 있어 더 일찍 차단.
        if len(new_terms) > max_terms:
            raise ValueError(
                f"Pauli 항 수 {len(new_terms)} > max_terms={max_terms} — threshold 를 키우세요."
            )
        if threshold > 0:
            terms = {key: v for key, v in new_terms.items() if abs(v) >= threshold}
        else:
            terms = {key: v for key, v in new_terms.items() if abs(v) > 1e-15}
    return sum((coeff for (xm, _zm), coeff in terms.items() if xm == 0), 0j)


def pauli_propagation_expectation_mc(
    circuit,
    observable,
    budget: int = 4096,
    shots: int = 16,
    seed: int | None = None,
) -> complex:
    """**Monte-Carlo (무편향) Pauli propagation** — 결정론적 truncation 대신,
    항 수가 ``budget`` 을 넘으면 계수 절댓값 ∝ 확률로 **재표본 + 재스케일** 한다.

    각 게이트 후 항이 budget 초과 시, ``|c_i|`` 에 비례해 budget 개를 (복원추출)
    뽑고 각 표본을 ``‖c‖₁ / budget`` 로 재스케일 → 기댓값이 **무편향**.  ``shots``
    회 독립 실행 평균으로 분산을 줄인다.  결정론적 truncation 의 편향이 문제되는
    회로에서 유용.

    Returns:
        기댓값 추정 (복소; ``shots`` 평균).
    """
    n = circuit.num_qubits
    base_terms = _parse_observable(observable, n)
    cache: dict = {}
    gates = list(reversed(list(_iter_gates(circuit))))
    rng = np.random.default_rng(seed)

    def one_run() -> complex:
        terms = dict(base_terms)
        for name, qubits, params in gates:
            g, k = _gate_matrix(name, params)
            key_gp = (name, params)
            if key_gp not in cache:
                cache[key_gp] = _decompose_kq(g, k)
            cmap = cache[key_gp]
            terms = _apply_gate_map(terms, cmap, qubits, k)
            terms = {key: v for key, v in terms.items() if abs(v) > 1e-15}
            if len(terms) > budget:
                keys = list(terms.keys())
                weights = np.array([abs(terms[key]) for key in keys])
                l1 = weights.sum()
                probs = weights / l1
                idx = rng.choice(len(keys), size=budget, p=probs)
                # 무편향 재표본: 표본별 기여 = sign(c)·‖c‖₁/budget, 동일 키 합산.
                resampled: dict[tuple[int, int], complex] = {}
                scale = l1 / budget
                for j in idx:
                    key = keys[j]
                    phase = terms[key] / abs(terms[key])
                    resampled[key] = resampled.get(key, 0j) + phase * scale
                terms = resampled
        return sum((coeff for (xm, _zm), coeff in terms.items() if xm == 0), 0j)

    return sum((one_run() for _ in range(max(1, shots))), 0j) / max(1, shots)
