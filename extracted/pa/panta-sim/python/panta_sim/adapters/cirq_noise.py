"""Cirq noise channels → panta-sim ``NoiseModel`` 어댑터 (v0.5.4).

Cirq 의 4 표준 1-qubit noise channel (``cirq.BitFlipChannel`` /
``cirq.PhaseFlipChannel`` / ``cirq.DepolarizingChannel`` /
``cirq.AmplitudeDampingChannel``) 인스턴스 리스트를 panta-sim 의
``NoiseModel`` 로 변환한다.

Cirq 에서 noise channel 은 gate-like 객체 (``cirq.bit_flip(p)`` 같은 factory
함수가 channel 인스턴스 반환).  사용자가 회로에 ``.on(qubit)`` 으로 적용하거나
별도로 channel 인스턴스를 들고 다님.  이 어댑터는 후자 — channel 인스턴스
리스트를 panta NoiseModel 로 변환.

동등성: 같은 noise + 같은 회로를 ``cirq.DensityMatrixSimulator`` 와
panta-sim ``method="density_matrix"`` 에서 실행 시 ‖ρ‖ < 1e-10 (f64) 또는
1e-6 (cirq complex64 한계) 일치.
"""

from __future__ import annotations

from typing import Any, List, Tuple, Union

from ..noise import NoiseModel

_CIRQ_INSTALL_HINT = (
    "cirq-core is required for from_cirq_noise — install with: pip install cirq-core"
)


def _lazy_import_cirq() -> Any:
    """Cirq 를 lazy import (미설치 시 친절 ImportError)."""
    try:
        import cirq  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover
        raise ImportError(_CIRQ_INSTALL_HINT) from exc
    return cirq


def from_cirq_noise(
    noise_channels: List[Any],
    gates: Union[str, List[str]] = "all",
    qubits: Any = "all",
) -> NoiseModel:
    """Cirq noise channel 인스턴스 리스트를 panta-sim ``NoiseModel`` 로 변환.

    Args:
        noise_channels: ``cirq.bit_flip(p)`` (= ``cirq.BitFlipChannel``),
            ``cirq.phase_flip(p)``, ``cirq.depolarize(p)``,
            ``cirq.amplitude_damp(γ)`` 인스턴스 리스트.
        gates: panta NoiseModel 의 gates 필터.  ``"all"`` (default) / 단일
            gate name / list.
        qubits: panta NoiseModel 의 qubits 필터.

    Returns:
        panta-sim ``NoiseModel`` — 입력 channel 모두 같은 gates/qubits 필터로
        등록.

    Raises:
        ImportError: ``cirq-core`` 미설치.
        NotImplementedError: 4 표준 채널 외 (예: ``cirq.AsymmetricDepolarizingChannel``,
            ``cirq.PhaseDampingChannel``, ``cirq.GeneralizedAmplitudeDampingChannel``,
            ``cirq.MixedUnitaryChannel``, ``cirq.KrausChannel``).

    Example:
        >>> import cirq
        >>> from panta_sim import from_cirq_noise, QuantumCircuit
        >>>
        >>> ch_list = [cirq.depolarize(0.05), cirq.amplitude_damp(0.02)]
        >>> nm = from_cirq_noise(ch_list, gates=["h", "cx"])
        >>>
        >>> qc = QuantumCircuit(2); qc.h(0); qc.cx(0, 1); qc.measure_all()
        >>> result = qc.run(shots=10000, noise_model=nm, seed=42)
    """
    cirq = _lazy_import_cirq()
    panta = NoiseModel()
    for ch in noise_channels:
        kind, param = _decode_cirq_channel(ch, cirq)
        if kind == "bit_flip":
            panta.add_bit_flip(param, gates=gates, qubits=qubits)
        elif kind == "phase_flip":
            panta.add_phase_flip(param, gates=gates, qubits=qubits)
        elif kind == "depolarizing":
            panta.add_depolarizing(param, gates=gates, qubits=qubits)
        elif kind == "amplitude_damping":
            panta.add_amplitude_damping(param, gates=gates, qubits=qubits)
        else:  # pragma: no cover — defensive
            raise NotImplementedError(f"unknown channel kind {kind!r}")
    return panta


def _decode_cirq_channel(ch: Any, cirq: Any) -> Tuple[str, float]:
    """Cirq channel 인스턴스를 (channel_kind, param) 으로 decode.

    - BitFlipChannel: ``ch.p`` = bit-flip 확률
    - PhaseFlipChannel: ``ch.p`` = phase-flip 확률
    - DepolarizingChannel: ``ch.p`` = 총 Pauli 오류율 (각 Pauli p/3) →
      panta 의 λ = 4p/3 으로 변환 (panta/Aer 는 각 Pauli λ/4 컨벤션)
    - AmplitudeDampingChannel: ``ch.gamma`` = γ
    """
    name = type(ch).__name__

    if isinstance(ch, cirq.BitFlipChannel):
        return ("bit_flip", float(ch.p))
    if isinstance(ch, cirq.PhaseFlipChannel):
        return ("phase_flip", float(ch.p))
    if isinstance(ch, cirq.DepolarizingChannel):
        # 컨벤션 변환: cirq.depolarize(p) 는 각 Pauli 를 p/3 로 적용
        # (Λ = (1-p)ρ + (p/3)Σ PρP, 총 오류율 p).  panta / Aer 의
        # Depolarizing(λ) 는 각 Pauli 를 λ/4 로 적용 (Λ = (1-λ)ρ + λ·I/2,
        # 총 오류율 3λ/4).  동일 채널이 되려면 λ = 4p/3 — 그대로 넘기면
        # 25% 약한 노이즈가 된다.
        # cirq 1.x 에서 single-qubit channel 의 num_qubits == 1 검증.
        if getattr(ch, "num_qubits", lambda: 1)() != 1:
            raise NotImplementedError(
                f"Cirq DepolarizingChannel num_qubits={ch.num_qubits()} — "
                "panta-sim 의 1-qubit channel 외, multi-qubit depolarizing 미지원."
            )
        p = float(ch.p)
        if p > 0.75:
            raise ValueError(
                f"cirq.depolarize(p={p}) 는 panta 의 λ = 4p/3 = {4 * p / 3:.4f} > 1 — "
                "panta-sim Depolarizing 표현 범위 (λ ≤ 1, p ≤ 0.75) 를 벗어납니다."
            )
        return ("depolarizing", 4.0 * p / 3.0)
    if isinstance(ch, cirq.AmplitudeDampingChannel):
        return ("amplitude_damping", float(ch.gamma))

    # 흔한 unsupported Cirq channels — 친화적 메시지.
    unsupported = {
        "AsymmetricDepolarizingChannel": "AsymmetricDepolarizingChannel 은 "
        "X / Y / Z 별 다른 확률 — panta 의 균등 Depolarizing 외.",
        "PhaseDampingChannel": "PhaseDampingChannel 은 panta-sim 미지원 — "
        "PhaseFlip 으로 근사 (정확한 모델은 v0.5.x patch).",
        "GeneralizedAmplitudeDampingChannel": "GeneralizedAmplitudeDampingChannel "
        "은 thermal-bath 일반화 — panta-sim 의 4 표준 채널 외.",
        "MixedUnitaryChannel": "MixedUnitaryChannel 은 임의 unitary 혼합 — "
        "panta-sim 의 표준 4 채널 외.",
        "KrausChannel": "KrausChannel 은 임의 Kraus operator — panta-sim 의 "
        "표준 4 채널 외.  panta NoiseModel 직접 작성 권장.",
        "ResetChannel": "ResetChannel 은 noise 가 아닌 reset op — "
        "panta_sim.from_cirq 의 reset 매핑 사용 (회로 변환 시 자동 처리).",
    }
    hint = unsupported.get(name, "")
    raise NotImplementedError(
        f"Cirq noise channel {name} 은 panta-sim 의 4 표준 채널 (BitFlip / "
        f"PhaseFlip / Depolarizing / AmplitudeDamping) 외.{' ' + hint if hint else ''}\n"
        f"panta NoiseModel 의 fluent API (add_bit_flip / add_phase_flip / "
        f"add_depolarizing / add_amplitude_damping) 로 직접 작성하세요."
    )
