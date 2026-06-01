"""노이즈 모델 (v0.4 stochastic trajectory).

panta-sim native fluent API 로 노이즈 채널을 회로 게이트에 매핑한다.
Trajectory 백엔드 — 각 shot 마다 회로 전체가 fresh 상태에서 재실행되며,
``ApplyNoise`` 명령에서 Kraus 연산자가 RNG 로 샘플링된다.

기본 사용법::

    from panta_sim import QuantumCircuit, NoiseModel

    noise = (
        NoiseModel()
        .add_bit_flip(p=0.01, qubits="all")
        .add_depolarizing(p=0.05, gates=["cx"], qubits=[(0, 1)])
        .add_amplitude_damping(gamma=0.02, qubits=[0])
    )

    qc = QuantumCircuit(2).h(0).cx(0, 1).measure_all()
    result = qc.run(shots=10000, noise_model=noise)

각 ``add_*`` 호출은 (channel, gate_filter, qubit_filter) 규칙을 누적 기록한다.
``qc.run(noise_model=...)`` 시점에 NoiseModel 이 _ops 를 walk 하며 매칭되는
규칙별로 ``ApplyNoise`` 명령을 게이트 *직후* 에 삽입한 새 Rust 회로를 만든다.

Density matrix 백엔드, 멀티-큐비트 채널, mid-circuit 동적 채널 적용은
v0.5 이후 마일스톤.
"""

from __future__ import annotations

from typing import Any, Iterable, List, Optional, Sequence, Tuple, Union

from .qsim_python import Circuit as _RustCircuit
from .qsim_python import NoiseChannel as _NoiseChannel

QubitSpec = Union[str, Sequence[int], Sequence[Tuple[int, ...]]]
GateSpec = Union[str, Sequence[str]]


class NoiseModel:
    """게이트 적용 후 삽입할 노이즈 채널의 모음.

    ``add_*`` fluent 메서드로 채널을 누적한 뒤 ``qc.run(noise_model=self)`` 에
    전달한다. 한 NoiseModel 은 여러 채널을 가질 수 있으며, 동일 게이트에 여러
    채널이 매칭되면 **추가된 순서대로** 모두 삽입된다.

    필터 규약 (게이트 / 큐비트):
        - ``gates`` 가 ``"all"`` 이거나 ``None`` 이면 모든 게이트 후 적용.
        - ``gates`` 가 리스트면 그 게이트 이름들에만 적용 (예: ``["cx", "cz"]``).
        - ``qubits`` 가 ``"all"`` 이면 게이트의 모든 큐비트 각각에 채널 1개씩 적용.
        - ``qubits`` 가 정수 리스트 (예: ``[0, 2]``) 면 그 큐비트들에만 적용 —
          단, 게이트가 그 큐비트를 *포함* 해야 매칭.
        - ``qubits`` 가 튜플 리스트 (예: ``[(0, 1), (1, 2)]``) 면 게이트의 큐비트
          시퀀스가 정확히 일치해야 매칭 (2큐비트 게이트의 (control, target) 쌍 등).
          이 경우 채널은 튜플의 각 큐비트에 적용된다.
    """

    def __init__(self) -> None:
        # 각 entry: (PyNoiseChannel, gate_filter | None, qubit_filter | None).
        # gate_filter: None 이면 모든 게이트, 그 외 set[str].
        # qubit_filter: None ("all"), List[int], 또는 List[Tuple[int, ...]].
        self._rules: List[Tuple[_NoiseChannel, Optional[set], Any]] = []

    # ------------------------------------------------------------------
    # Fluent builders
    # ------------------------------------------------------------------

    def add_bit_flip(
        self,
        p: float,
        *,
        gates: Optional[GateSpec] = None,
        qubits: QubitSpec = "all",
    ) -> "NoiseModel":
        """Bit-flip 채널 추가 (확률 ``p`` 로 X 게이트 적용)."""
        return self._add(_NoiseChannel.bit_flip(p), gates, qubits)

    def add_phase_flip(
        self,
        p: float,
        *,
        gates: Optional[GateSpec] = None,
        qubits: QubitSpec = "all",
    ) -> "NoiseModel":
        """Phase-flip 채널 추가 (확률 ``p`` 로 Z 게이트 적용)."""
        return self._add(_NoiseChannel.phase_flip(p), gates, qubits)

    def add_depolarizing(
        self,
        p: float,
        *,
        gates: Optional[GateSpec] = None,
        qubits: QubitSpec = "all",
    ) -> "NoiseModel":
        """Depolarizing 채널 추가 (확률 ``p`` 로 {X, Y, Z} 균등 적용)."""
        return self._add(_NoiseChannel.depolarizing(p), gates, qubits)

    def add_amplitude_damping(
        self,
        gamma: float,
        *,
        gates: Optional[GateSpec] = None,
        qubits: QubitSpec = "all",
    ) -> "NoiseModel":
        """Amplitude-damping 채널 추가 (T1 모델, γ ∈ [0, 1])."""
        return self._add(_NoiseChannel.amplitude_damping(gamma), gates, qubits)

    def _add(
        self,
        channel: _NoiseChannel,
        gates: Optional[GateSpec],
        qubits: QubitSpec,
    ) -> "NoiseModel":
        gate_filter = _normalize_gate_filter(gates)
        qubit_filter = _normalize_qubit_filter(qubits)
        self._rules.append((channel, gate_filter, qubit_filter))
        return self

    # ------------------------------------------------------------------
    # Apply
    # ------------------------------------------------------------------

    def apply_to(self, panta_circuit: Any) -> _RustCircuit:
        """``panta_circuit._ops`` 를 walk 하며 매칭되는 채널을 게이트 직후에
        삽입한 새 ``_RustCircuit`` 를 반환한다.

        global_phase 는 원본 회로에서 복사된다 (``unitary()`` 누적 phase 보존).

        Raises:
            ValueError: ``_ops`` 에 처리할 수 없는 op 이름 (방어적).
        """
        new_rust = _RustCircuit(panta_circuit.num_qubits)

        for op in panta_circuit._ops:
            _replay_op_to_rust(new_rust, op)
            name, qubits, _ = op
            if name in ("measure", "measure_all", "reset", "if_eq"):
                # 측정 / reset / classical control 자체에는 노이즈 적용 안 함
                # (Qiskit Aer 의 default 동작과 정합 — 사용자 게이트만 noisy).
                # if_eq 의 inner 게이트는 조건부 실행이라 trajectory 단계에서 결정되며,
                # 회로 빌드 시점에 noise 를 미리 붙이는 건 의미 모호해 v0.4.5 에선 skip.
                continue
            for channel, target in self._channels_for(name, qubits):
                new_rust.add_noise(channel, target)

        # 원본 회로의 global_phase 를 보존 (예: unitary() 분해 phase).
        new_rust.global_phase = panta_circuit.global_phase
        return new_rust

    def _channels_for(
        self, gate_name: str, gate_qubits: Tuple[int, ...]
    ) -> Iterable[Tuple[_NoiseChannel, int]]:
        """주어진 게이트에 매칭되는 (channel, target_qubit) 쌍을 yield."""
        for channel, gate_filter, qubit_filter in self._rules:
            if gate_filter is not None and gate_name not in gate_filter:
                continue
            for target in _resolve_targets(gate_qubits, qubit_filter):
                yield channel, target

    def __len__(self) -> int:
        return len(self._rules)

    def __repr__(self) -> str:
        return f"NoiseModel({len(self._rules)} rule{'s' if len(self._rules) != 1 else ''})"


# ----------------------------------------------------------------------
# 헬퍼
# ----------------------------------------------------------------------


def _normalize_gate_filter(gates: Optional[GateSpec]) -> Optional[set]:
    if gates is None or gates == "all":
        return None
    if isinstance(gates, str):
        return {gates}
    return set(gates)


def _normalize_qubit_filter(qubits: QubitSpec) -> Any:
    """qubits 인자를 내부 형태로 정규화.

    반환값은 다음 중 하나:
    - None (= 모든 큐비트, "all")
    - List[int] (= 이 큐비트들 각각)
    - List[Tuple[int, ...]] (= 정확히 매칭되는 큐비트 시퀀스 — 튜플의 모든
      큐비트에 채널 적용)
    """
    if qubits == "all":
        return None
    items = list(qubits)
    if not items:
        # 빈 리스트 = 어떤 게이트에도 매칭 안 됨 (effectively no-op).
        return []
    if all(isinstance(x, tuple) for x in items):
        return [tuple(int(q) for q in t) for t in items]
    if all(isinstance(x, int) for x in items):
        return [int(x) for x in items]
    raise ValueError(
        f"qubits 인자는 'all', List[int], 또는 List[Tuple[int,...]] 여야 합니다 (입력: {qubits!r})"
    )


def _resolve_targets(
    gate_qubits: Tuple[int, ...], qubit_filter: Any
) -> Iterable[int]:
    """게이트의 큐비트 시퀀스와 필터를 매칭해 노이즈 적용 큐비트를 yield."""
    if qubit_filter is None:
        # 모든 게이트 큐비트에 각각 채널 1 개씩 적용.
        yield from gate_qubits
        return
    if not qubit_filter:
        return
    if isinstance(qubit_filter[0], tuple):
        # 튜플 매칭: 정확히 일치하는 큐비트 시퀀스만.
        if tuple(gate_qubits) in qubit_filter:
            yield from gate_qubits
        return
    # List[int] — 게이트가 그 큐비트를 포함하면 *그 큐비트에만* 채널 적용.
    qubit_set = set(qubit_filter)
    for q in gate_qubits:
        if q in qubit_set:
            yield q


def _replay_op_to_rust(rust: _RustCircuit, op: Tuple[str, Tuple[int, ...], Tuple[Any, ...]]) -> None:
    """Python ``_ops`` 한 entry 를 새 Rust 회로에 다시 적용한다.

    이 dispatch 는 ``adapters.qiskit.to_qiskit`` 의 fluent 매핑과 동치 — 게이트
    이름별로 동명의 Rust 메서드를 호출한다. 신규 게이트 추가 시 양쪽 모두 갱신.
    """
    name, qubits, params = op

    if name == "h":
        rust.h(qubits[0])
    elif name == "x":
        rust.x(qubits[0])
    elif name == "y":
        rust.y(qubits[0])
    elif name == "z":
        rust.z(qubits[0])
    elif name == "s":
        rust.s(qubits[0])
    elif name == "sdg":
        rust.sdg(qubits[0])
    elif name == "t":
        rust.t(qubits[0])
    elif name == "tdg":
        rust.tdg(qubits[0])
    elif name == "sx":
        rust.sx(qubits[0])
    elif name == "sxdg":
        rust.sxdg(qubits[0])
    elif name == "id":
        rust.id(qubits[0])
    elif name == "rx":
        rust.rx(float(params[0]), qubits[0])
    elif name == "ry":
        rust.ry(float(params[0]), qubits[0])
    elif name == "rz":
        rust.rz(float(params[0]), qubits[0])
    elif name in ("p", "u1"):
        rust.p(float(params[0]), qubits[0])
    elif name == "u2":
        rust.u2(float(params[0]), float(params[1]), qubits[0])
    elif name == "u":
        # v0.4.6: Rust 가 native U(θ,φ,λ) 를 지원 — 직접 호출 (이전 unitary() 우회 제거).
        rust.u(float(params[0]), float(params[1]), float(params[2]), qubits[0])
    elif name == "cx":
        rust.cx(qubits[0], qubits[1])
    elif name == "cz":
        rust.cz(qubits[0], qubits[1])
    elif name == "swap":
        rust.swap(qubits[0], qubits[1])
    elif name == "cy":
        rust.cy(qubits[0], qubits[1])
    elif name == "ch":
        rust.ch(qubits[0], qubits[1])
    elif name == "crx":
        rust.crx(float(params[0]), qubits[0], qubits[1])
    elif name == "cry":
        rust.cry(float(params[0]), qubits[0], qubits[1])
    elif name == "crz":
        rust.crz(float(params[0]), qubits[0], qubits[1])
    elif name in ("cp", "cu1"):
        rust.cp(float(params[0]), qubits[0], qubits[1])
    elif name == "cu3":
        rust.cu3(
            float(params[0]),
            float(params[1]),
            float(params[2]),
            qubits[0],
            qubits[1],
        )
    elif name == "cu":
        rust.cu(
            float(params[0]),
            float(params[1]),
            float(params[2]),
            float(params[3]),
            qubits[0],
            qubits[1],
        )
    elif name == "ccx":
        rust.ccx(qubits[0], qubits[1], qubits[2])
    elif name == "cswap":
        rust.cswap(qubits[0], qubits[1], qubits[2])
    elif name == "unitary":
        if not params:
            rust.id(qubits[0])
        else:
            import numpy as np
            m = np.asarray(params[0], dtype=np.complex128)
            rust.unitary(m, qubits[0], True)
    elif name == "measure":
        cbit = int(params[0]) if params else 0
        rust.measure(qubits[0], cbit)
    elif name == "measure_all":
        rust.measure_all()
    elif name == "reset":
        rust.reset(qubits[0])
    elif name == "if_eq":
        # params slot = (cbits_tuple, value, inner_name, inner_params).
        # 먼저 inner 게이트를 push 한 뒤 c_if_last 로 in-place wrap.
        cbits_tuple, value, inner_name, inner_params = params
        inner_op = (inner_name, qubits, tuple(inner_params))
        _replay_op_to_rust(rust, inner_op)
        rust.c_if_last(list(cbits_tuple), int(value))
    else:  # pragma: no cover — defensive
        raise ValueError(f"NoiseModel.apply_to: 처리할 수 없는 op {name!r}")
