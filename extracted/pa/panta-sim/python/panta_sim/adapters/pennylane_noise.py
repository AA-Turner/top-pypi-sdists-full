"""PennyLane noise channels → panta-sim ``NoiseModel`` 어댑터 (v0.5.4).

PennyLane 의 4 표준 1-qubit noise channel (``qml.BitFlip`` / ``qml.PhaseFlip``
/ ``qml.DepolarizingChannel`` / ``qml.AmplitudeDamping``) 인스턴스 리스트를
panta-sim 의 ``NoiseModel`` 로 변환한다.  사용자가 PennyLane 에서 noise op
들을 정의하고 panta-sim 으로 마이그레이션 시 마찰 0.

PennyLane 은 Aer 처럼 "noise model 객체에 자동 attach" 시스템이 표준화되어
있지 않고 (PennyLane 0.36+ 의 ``qml.NoiseModel`` 은 condition / channel
mapping 모델로 별개), 사용자가 noise op 를 회로에 직접 넣거나 별도로 channel
인스턴스를 들고 다니는 패턴이 흔하다.  이 어댑터는 후자 패턴 — channel
인스턴스 리스트를 panta NoiseModel 로 변환.

동등성: 같은 noise + 같은 회로를 PennyLane (default.mixed) 와 panta-sim 에서
실행하면 통계적으로 일치 (TVD < 0.02 at shots=10000) 또는 density backend
에서 ‖ρ‖ < 1e-10 일치.
"""

from __future__ import annotations

from typing import Any, List, Tuple, Union

from ..noise import NoiseModel

_PL_INSTALL_HINT = (
    "PennyLane is required for from_pennylane_noise — install with: "
    "pip install pennylane"
)


def _lazy_import_pennylane() -> Any:
    """PennyLane 을 lazy import (미설치 시 친절 ImportError)."""
    try:
        import pennylane as qml  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover
        raise ImportError(_PL_INSTALL_HINT) from exc
    return qml


def from_pennylane_noise(
    noise_ops: List[Any],
    gates: Union[str, List[str]] = "all",
    qubits: Any = "all",
) -> NoiseModel:
    """PennyLane noise op 인스턴스 리스트를 panta-sim ``NoiseModel`` 로 변환.

    Args:
        noise_ops: ``qml.BitFlip(p, wires=...)``, ``qml.PhaseFlip(p, ...)``,
            ``qml.DepolarizingChannel(p, ...)``, ``qml.AmplitudeDamping(γ, ...)``
            인스턴스 리스트.  ``wires`` 는 무시 — panta NoiseModel 은 gate-level
            필터 (``gates``, ``qubits``) 를 사용하므로 사용자가 별도 지정.
        gates: panta NoiseModel 의 gates 필터 — 어느 게이트 직후 noise 적용.
            ``"all"`` (default) / 단일 gate name (str) / list of gate names.
        qubits: panta NoiseModel 의 qubits 필터.  ``"all"`` (default) / qubit
            인덱스 list / 정확한 (qubit_tuple,) 매칭.

    Returns:
        panta-sim ``NoiseModel``.  입력 noise op 모두 같은 gates/qubits 필터로
        등록 (각 op 별 다른 필터가 필요하면 ``from_pennylane_noise`` 를 여러
        번 호출하거나 panta NoiseModel 직접 작성).

    Raises:
        ImportError: ``pennylane`` 미설치.
        NotImplementedError: 4 표준 채널 외 (예: ``qml.GeneralizedAmplitudeDamping``,
            ``qml.PauliError``, ``qml.QubitChannel`` 등).  panta-sim 의 noise
            모델은 BitFlip / PhaseFlip / Depolarizing / AmplitudeDamping 4 종만
            지원.

    Example:
        >>> import pennylane as qml
        >>> from panta_sim import from_pennylane_noise, QuantumCircuit
        >>>
        >>> # PennyLane 측에서 noise channel 인스턴스 정의
        >>> pl_noise = [qml.BitFlip(0.05, wires=0), qml.PhaseFlip(0.02, wires=0)]
        >>>
        >>> # panta-sim NoiseModel 으로 변환 (h gate 직후 적용)
        >>> nm = from_pennylane_noise(pl_noise, gates=["h"])
        >>>
        >>> qc = QuantumCircuit(1); qc.h(0); qc.measure_all()
        >>> result = qc.run(shots=10000, noise_model=nm, seed=42)
    """
    qml = _lazy_import_pennylane()
    panta = NoiseModel()
    for op in noise_ops:
        kind, param = _decode_pennylane_op(op, qml)
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


def _decode_pennylane_op(op: Any, qml: Any) -> Tuple[str, float]:
    """PennyLane noise op 인스턴스를 (channel_kind, param) 으로 decode.

    PennyLane 의 channel parameter 는 ``op.parameters[0]`` (BitFlip / PhaseFlip
    / DepolarizingChannel 의 ``p``, AmplitudeDamping 의 ``γ``).  파라미터화
    된 channel 만 — non-parametric 이거나 multi-parameter (예:
    GeneralizedAmplitudeDamping) 는 거부.
    """
    name = type(op).__name__

    if isinstance(op, qml.BitFlip):
        return ("bit_flip", float(op.parameters[0]))
    if isinstance(op, qml.PhaseFlip):
        return ("phase_flip", float(op.parameters[0]))
    if isinstance(op, qml.DepolarizingChannel):
        # 컨벤션 변환: PennyLane DepolarizingChannel(p) 는 각 Pauli p/3
        # (총 오류율 p).  panta/Aer 의 Depolarizing(λ) 는 각 Pauli λ/4 —
        # 동일 채널은 λ = 4p/3 (그대로 넘기면 25% 약한 노이즈).
        p = float(op.parameters[0])
        if p > 0.75:
            raise ValueError(
                f"DepolarizingChannel(p={p}) 는 panta 의 λ = 4p/3 = {4 * p / 3:.4f} > 1 — "
                "panta-sim Depolarizing 표현 범위 (λ ≤ 1, p ≤ 0.75) 를 벗어납니다."
            )
        return ("depolarizing", 4.0 * p / 3.0)
    if isinstance(op, qml.AmplitudeDamping):
        return ("amplitude_damping", float(op.parameters[0]))

    # 흔한 unsupported PennyLane channels — 친화적 메시지.
    unsupported = {
        "GeneralizedAmplitudeDamping": "GeneralizedAmplitudeDamping 은 "
        "AmplitudeDamping 의 thermal-bath 일반화 — panta-sim 의 4 표준 채널 외.",
        "PhaseDamping": "PhaseDamping 은 panta-sim 미지원 — PhaseFlip 으로 "
        "근사 (정확한 모델은 v0.5.x patch).",
        "PauliError": "PauliError 는 임의 Pauli string error — panta-sim 의 "
        "1-qubit Pauli 4 종 (BitFlip / PhaseFlip / Depolarizing) 외.",
        "QubitChannel": "QubitChannel 은 임의 Kraus operator — panta-sim 의 "
        "표준 4 채널 외.  panta NoiseModel 직접 작성 권장.",
    }
    hint = unsupported.get(name, "")
    raise NotImplementedError(
        f"PennyLane noise op {name} 은 panta-sim 의 4 표준 채널 (BitFlip / "
        f"PhaseFlip / DepolarizingChannel / AmplitudeDamping) 외.{' ' + hint if hint else ''}\n"
        f"panta NoiseModel 의 fluent API (add_bit_flip / add_phase_flip / "
        f"add_depolarizing / add_amplitude_damping) 로 직접 작성하세요."
    )
