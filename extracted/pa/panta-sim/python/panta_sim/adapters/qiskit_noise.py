"""Qiskit Aer ``NoiseModel`` → panta-sim ``NoiseModel`` 자동 어댑터 (v0.4.1).

Aer 의 등록된 quantum error 들을 walk 하며 4 가지 표준 1-qubit 채널
(BitFlip / PhaseFlip / Depolarizing / AmplitudeDamping) 으로 식별 가능한
패턴을 panta-sim 의 ``NoiseModel`` 규칙으로 변환한다.

대응 패턴:

- **1-qubit Pauli error** (``[X, I]``, ``[Z, I]``, 또는 ``[I, X, Y, Z]``):
  → BitFlip / PhaseFlip / Depolarizing
- **1-qubit Kraus error** (단일 branch with ``kraus`` instruction):
  → AmplitudeDamping (행렬 모양 매칭으로 검출)
- **2-qubit `err1q.tensor(err1q)` 패턴** (typical Aer 의 cx 적용 방식):
  - Pauli: N² 개 branch 의 outer product → 1q 채널로 unfold (panta 가 cx 의
    양쪽 큐비트에 자동 적용)
  - Kraus: 단일 branch 에 두 개의 kraus instruction (양쪽 큐비트) →
    1q AmplitudeDamping 으로 unfold
- **그 외**: ``NotImplementedError`` (사용자가 직접 panta NoiseModel 작성 권장)

이 어댑터는 ``qiskit-aer`` 가 설치되어 있을 때만 동작 — 미설치 시 ImportError.
"""

from __future__ import annotations

from typing import Any, Iterable, List, Optional, Tuple

import numpy as np

from ..noise import NoiseModel

_AER_INSTALL_HINT = (
    "qiskit-aer is required for from_qiskit_noise_model — install with: "
    "pip install qiskit-aer"
)

# 행렬 / 확률 비교 허용오차. Aer 의 부동소수 누적 (예: depolarizing 의 1-3p/4) 과
# panta 의 식별 사이의 ULP 차이를 흡수.
_ATOL = 1e-9


def _lazy_import_aer() -> Any:
    """qiskit-aer 를 lazy import (미설치 시 친절 ImportError)."""
    try:
        import qiskit_aer  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover
        raise ImportError(_AER_INSTALL_HINT) from exc
    return qiskit_aer


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------


def from_qiskit_noise_model(aer_model: Any) -> NoiseModel:
    """Aer ``NoiseModel`` 을 panta-sim ``NoiseModel`` 로 변환한다.

    Aer 의 ``_default_quantum_errors`` (모든 큐비트 등록) 와
    ``_local_quantum_errors`` (특정 큐비트 등록) 양쪽을 walk 하며 각 error 를
    1-qubit 표준 채널로 식별 → panta NoiseModel 규칙으로 추가.

    Args:
        aer_model: ``qiskit_aer.noise.NoiseModel`` 인스턴스.

    Returns:
        panta-sim ``NoiseModel``. 동일 회로 + 동일 noise 적용 시 Aer 와 통계적
        으로 일치 (TVD < 0.02 at shots=10000, v0.4 cross-check 와 동일 기준).

    Raises:
        ImportError: ``qiskit-aer`` 미설치.
        NotImplementedError: Aer error 가 4 가지 표준 채널 패턴이 아님 (예:
            non-unitary 일반 Kraus, 3-qubit error, asymmetric 2-qubit error 등).
            메시지에 어느 게이트의 어떤 error 가 문제인지 명시.

    Example:
        >>> from qiskit_aer.noise import NoiseModel as AerNM
        >>> from qiskit_aer.noise import depolarizing_error
        >>> from panta_sim import from_qiskit_noise_model
        >>>
        >>> aer = AerNM()
        >>> aer.add_all_qubit_quantum_error(depolarizing_error(0.05, 1), ['h'])
        >>> panta = from_qiskit_noise_model(aer)
        >>> # panta 는 Depolarizing(0.05) on 'h' / qubits='all' 규칙 1 개를 가짐
    """
    _lazy_import_aer()  # 친절 ImportError early

    panta = NoiseModel()

    # 1. _default_quantum_errors : {gate_name: QuantumError} — 모든 큐비트 적용.
    default_errors = getattr(aer_model, "_default_quantum_errors", {})
    for gate_name, error in default_errors.items():
        _add_decoded_rule(panta, error, gate_name, qubits_arg="all")

    # 2. _local_quantum_errors : {gate_name: {qubit_tuple: QuantumError}} — 특정 큐비트.
    local_errors = getattr(aer_model, "_local_quantum_errors", {})
    for gate_name, qubit_dict in local_errors.items():
        for qubit_tuple, error in qubit_dict.items():
            qubits_arg = _qubit_arg_from_tuple(qubit_tuple, error.num_qubits)
            _add_decoded_rule(panta, error, gate_name, qubits_arg=qubits_arg)

    return panta


# ----------------------------------------------------------------------
# Decoding internals
# ----------------------------------------------------------------------


def _add_decoded_rule(
    panta: NoiseModel,
    error: Any,
    gate_name: str,
    qubits_arg: Any,
) -> None:
    """Aer error 하나를 decode 해 panta NoiseModel 에 추가한다."""
    decoded = _decode_error(error, gate_name)
    kind, param = decoded
    if kind == "bit_flip":
        panta.add_bit_flip(param, gates=[gate_name], qubits=qubits_arg)
    elif kind == "phase_flip":
        panta.add_phase_flip(param, gates=[gate_name], qubits=qubits_arg)
    elif kind == "depolarizing":
        panta.add_depolarizing(param, gates=[gate_name], qubits=qubits_arg)
    elif kind == "amplitude_damping":
        panta.add_amplitude_damping(param, gates=[gate_name], qubits=qubits_arg)
    else:  # pragma: no cover — defensive
        raise NotImplementedError(f"unknown channel kind {kind!r}")


def _decode_error(error: Any, gate_name: str) -> Tuple[str, float]:
    """Aer QuantumError 를 (channel_kind, param) 으로 decode.

    실패 시 ``NotImplementedError`` (사용자에게 정확한 위치/원인 보고).
    """
    d = error.to_dict()
    instructions = d["instructions"]
    probs = [float(p) for p in d["probabilities"]]
    nq = error.num_qubits

    if nq == 1:
        result = _decode_1q(instructions, probs)
        if result is None:
            raise NotImplementedError(
                f"Aer 1-qubit error on gate {gate_name!r} 가 4 가지 표준 채널 "
                "(BitFlip / PhaseFlip / Depolarizing / AmplitudeDamping) "
                "패턴이 아니다. v0.4.1 어댑터는 표준 패턴만 지원한다 — "
                "panta NoiseModel 을 직접 작성해야 한다."
            )
        return result

    if nq == 2:
        result = _decode_2q_tensor(instructions, probs)
        if result is None:
            raise NotImplementedError(
                f"Aer 2-qubit error on gate {gate_name!r} 가 1-qubit 채널의 "
                "tensor(err, err) 패턴이 아니다. v0.4.1 어댑터는 "
                "``err1q.tensor(err1q)`` 형태만 지원한다."
            )
        return result

    raise NotImplementedError(
        f"Aer {nq}-qubit error on gate {gate_name!r}: panta-sim 어댑터는 "
        "1-qubit / 2-qubit (tensor) 만 지원한다."
    )


def _decode_1q(
    instructions: List[List[dict]],
    probs: List[float],
) -> Optional[Tuple[str, float]]:
    """1-qubit error → (kind, param). 매칭 실패 시 None."""
    # 단일 branch — Kraus matrix 형태 (amplitude_damping)
    if len(probs) == 1:
        seq = instructions[0]
        if len(seq) == 1 and seq[0].get("name") == "kraus":
            kraus_list = _coerce_kraus_params(seq[0].get("params", []))
            return _identify_kraus_1q(kraus_list)
        return None

    # 다중 branch — Pauli sequence 형태
    # 각 branch 가 단일 1-qubit named gate 인지 확인.
    pauli_dist: dict[str, float] = {}
    for seq, p in zip(instructions, probs):
        if len(seq) != 1:
            return None
        op = seq[0]
        # qubit 인덱스가 0 이어야 (1q error 의 standard form).
        if op.get("qubits") != [0]:
            return None
        name = op.get("name")
        if name not in ("i", "id", "x", "y", "z"):
            return None
        canonical = "id" if name in ("i", "id") else name
        pauli_dist[canonical] = pauli_dist.get(canonical, 0.0) + p

    return _identify_pauli_dist(pauli_dist)


def _identify_pauli_dist(dist: dict) -> Optional[Tuple[str, float]]:
    """Pauli 분포 ``{op_name: prob}`` 를 4 채널 중 하나로 식별."""
    # 정규화 (Aer 가 가끔 0 prob 항을 누락).
    p_id = dist.get("id", 0.0)
    p_x = dist.get("x", 0.0)
    p_y = dist.get("y", 0.0)
    p_z = dist.get("z", 0.0)

    total = p_id + p_x + p_y + p_z
    if abs(total - 1.0) > _ATOL:
        return None

    # BitFlip(p): X@p, I@(1-p)
    if p_y == 0 and p_z == 0:
        return ("bit_flip", p_x) if p_x > 0 else ("bit_flip", 0.0)

    # PhaseFlip(p): Z@p, I@(1-p)
    if p_x == 0 and p_y == 0:
        return ("phase_flip", p_z) if p_z > 0 else ("phase_flip", 0.0)

    # Depolarizing(p): I@(1-3p/4), X@(p/4), Y@(p/4), Z@(p/4)
    # → p_x == p_y == p_z 이어야.
    if abs(p_x - p_y) < _ATOL and abs(p_y - p_z) < _ATOL and p_x > 0:
        p = 4 * p_x  # p/4 = p_x → p = 4p_x
        if 0.0 <= p <= 1.0 + _ATOL:
            return ("depolarizing", min(p, 1.0))

    return None


def _identify_kraus_1q(kraus_list: List[np.ndarray]) -> Optional[Tuple[str, float]]:
    """1-qubit Kraus 행렬 리스트 → AmplitudeDamping 식별 (γ).

    AD form (global phase ±1 무시):
        K_0 = diag(1, √(1-γ)),   K_1 = √γ |0⟩⟨1|
    절대값으로 비교: |K_0[0,0]| ≈ 1, |K_0[1,1]| ≈ √(1-γ), 그 외 0.
                    |K_1[0,1]| ≈ √γ, 그 외 0.
    """
    if len(kraus_list) != 2:
        return None
    k0, k1 = kraus_list
    abs0 = np.abs(k0)
    abs1 = np.abs(k1)

    # K_0 가 diag(1, √(1-γ)) 모양인가
    if not (abs0[0, 1] < _ATOL and abs0[1, 0] < _ATOL):
        return None
    if abs(abs0[0, 0] - 1.0) > _ATOL:
        return None
    sqrt_one_minus_g = abs0[1, 1]
    if not (0.0 <= sqrt_one_minus_g <= 1.0 + _ATOL):
        return None

    # K_1 가 √γ |0⟩⟨1| 모양인가
    if not (
        abs1[0, 0] < _ATOL
        and abs1[1, 0] < _ATOL
        and abs1[1, 1] < _ATOL
    ):
        return None
    sqrt_g = abs1[0, 1]

    # γ = 1 - (sqrt_one_minus_g)² == (sqrt_g)² 이어야.
    g_from_k0 = max(0.0, 1.0 - sqrt_one_minus_g ** 2)
    g_from_k1 = sqrt_g ** 2
    if abs(g_from_k0 - g_from_k1) > 1e-6:
        return None
    gamma = g_from_k0
    if not (0.0 <= gamma <= 1.0 + _ATOL):
        return None
    return ("amplitude_damping", min(gamma, 1.0))


def _decode_2q_tensor(
    instructions: List[List[dict]],
    probs: List[float],
) -> Optional[Tuple[str, float]]:
    """2-qubit error 가 ``err1q.tensor(err1q)`` 패턴인지 확인 후 1q 채널 추출."""
    # Case A: 단일 branch + 두 개의 kraus instruction (양쪽 큐비트).
    if len(probs) == 1 and abs(probs[0] - 1.0) < _ATOL:
        seq = instructions[0]
        if len(seq) == 2:
            ops_by_qubit: dict[int, dict] = {}
            for op in seq:
                qs = op.get("qubits", [])
                if len(qs) == 1 and op.get("name") == "kraus":
                    ops_by_qubit[qs[0]] = op
            if set(ops_by_qubit.keys()) == {0, 1}:
                k0 = _coerce_kraus_params(ops_by_qubit[0].get("params", []))
                k1 = _coerce_kraus_params(ops_by_qubit[1].get("params", []))
                if _kraus_lists_close(k0, k1):
                    return _identify_kraus_1q(k0)
        return None

    # Case B: N² Pauli outer product. 각 branch 는 [op@q0, op@q1] 형태.
    return _decode_pauli_tensor_2q(instructions, probs)


def _decode_pauli_tensor_2q(
    instructions: List[List[dict]],
    probs: List[float],
) -> Optional[Tuple[str, float]]:
    """2-qubit Pauli error 의 outer product 분해."""
    n = len(probs)
    if n < 4:  # 최소 2² = BitFlip ⊗ BitFlip
        return None

    # 각 branch 는 두 op (q0, q1) 짝.
    q0_dist: dict[str, float] = {}
    q1_dist: dict[str, float] = {}
    cross: dict[Tuple[str, str], float] = {}

    for seq, prob in zip(instructions, probs):
        if len(seq) != 2:
            return None
        ops_by_qubit: dict[int, str] = {}
        for op in seq:
            qs = op.get("qubits", [])
            name = op.get("name", "")
            if len(qs) != 1 or qs[0] not in (0, 1):
                return None
            if name not in ("i", "id", "x", "y", "z"):
                return None
            canonical = "id" if name in ("i", "id") else name
            ops_by_qubit[qs[0]] = canonical
        if set(ops_by_qubit.keys()) != {0, 1}:
            return None
        a, b = ops_by_qubit[0], ops_by_qubit[1]
        q0_dist[a] = q0_dist.get(a, 0.0) + prob
        q1_dist[b] = q1_dist.get(b, 0.0) + prob
        cross[(a, b)] = cross.get((a, b), 0.0) + prob

    # Marginal 이 동일해야 (대칭 tensor 만 지원).
    if not _dicts_close(q0_dist, q1_dist):
        return None

    # Outer product 검증: cross[(a, b)] ≈ q0_dist[a] * q0_dist[b].
    for (a, b), p_ab in cross.items():
        expected = q0_dist[a] * q0_dist[b]
        if abs(p_ab - expected) > 1e-6:
            return None

    # 1q 분포로 식별.
    return _identify_pauli_dist(q0_dist)


# ----------------------------------------------------------------------
# 헬퍼
# ----------------------------------------------------------------------


def _coerce_kraus_params(params: Iterable) -> List[np.ndarray]:
    """Aer to_dict() 의 kraus params 가 numpy array / repr 문자열 / list 일
    수 있어 일관된 ``np.ndarray`` 리스트로 변환."""
    out: List[np.ndarray] = []
    for p in params:
        if isinstance(p, np.ndarray):
            out.append(np.asarray(p, dtype=np.complex128))
        elif isinstance(p, (list, tuple)):
            out.append(np.asarray(p, dtype=np.complex128))
        elif isinstance(p, str):
            # "[[1+0j 0+0j] [0+0j 1+0j]]" 같은 repr — eval 보다는 split 으로 안전 파싱은
            # 구현 비용이 높아 unsupported 로 처리. (Aer 의 새 to_dict 는 ndarray 반환).
            return []
    return out


def _kraus_lists_close(a: List[np.ndarray], b: List[np.ndarray]) -> bool:
    """두 Kraus 리스트가 (절대값 기준) 동일한지. global phase 무시."""
    if len(a) != len(b):
        return False
    for ma, mb in zip(a, b):
        if ma.shape != mb.shape:
            return False
        if not np.allclose(np.abs(ma), np.abs(mb), atol=_ATOL):
            return False
    return True


def _dicts_close(a: dict, b: dict) -> bool:
    """확률 분포 dict 두 개가 거의 같은지."""
    keys = set(a) | set(b)
    return all(abs(a.get(k, 0.0) - b.get(k, 0.0)) < _ATOL for k in keys)


def _qubit_arg_from_tuple(qubit_tuple: tuple, n_qubits: int) -> Any:
    """Aer 의 (1,) / (0, 1) 같은 큐비트 튜플을 panta-sim 의 qubits_arg 로 변환."""
    if n_qubits == 1:
        # 1-qubit error → qubits=[q] (게이트 큐비트 중 q 만 매칭).
        return [int(qubit_tuple[0])]
    # 2-qubit error → qubits=[(q0, q1)] (정확히 일치하는 큐비트 시퀀스만).
    return [tuple(int(q) for q in qubit_tuple)]
