"""PennyLane device plugin: ``qml.device("panta-sim", wires=N)`` (v0.3.5 Cut 3).

PennyLane 의 ``Device`` 신 API (``pennylane.devices.Device``) 를 panta-sim
백엔드로 구현한다. analytic statevector, sampling, expectation value,
probabilities, counts 측정을 지원한다.

**parameter-shift autodiff (v0.7)**: 디바이스 자체는 forward-only 지만,
QNode 의 ``diff_method="parameter-shift"`` 변환이 shifted tape 를 디바이스에
실행시켜 gradient 를 계산하므로 ``qml.grad`` / ``qml.jacobian`` /
``GradientDescentOptimizer`` 가 그대로 동작한다 (회전 게이트 각도가 0-dim 또는
1-element trainable ndarray 로 전달되는 경우 [`_scalar_param`] 가 스칼라로
변환).

Wire convention:
    PennyLane 의 statevector index 는 wire 0 = MSB (big-endian) 인 반면,
    panta-sim 은 qubit 0 = LSB (little-endian). 동일한 statevector 가
    나오도록 ``wire k`` 를 panta-sim 의 ``qubit (n-1-k)`` 로 매핑한다.
    이 매핑이 일관되게 적용되면 ``PennyLane.MeasurementProcess.process_state``
    가 변환 없이 그대로 panta-sim statevector 를 받아도 정확하다.

지원 PennyLane 게이트 (직접 매핑):
    Hadamard, PauliX/Y/Z, S, T, Adjoint(S/T) (= sdg/tdg), Identity,
    RX/Y/Z, CNOT, CZ, SWAP, Toffoli, CSWAP, QubitUnitary (1qubit).

미지원 게이트는 PennyLane 의 ``op.decomposition()`` 으로 풀어 recurse.
``QubitUnitary`` 멀티큐비트는 v0.4 (Rust ``Circuit::instructions()`` 노출 후)
또는 사용자가 미리 ``qml.transforms.decompose`` 로 분해할 것을 권장한다.

지원 측정 (PennyLane MeasurementProcess):
    state(), expval(obs), probs(wires), counts(wires), sample(wires).

v0.4.5 부터 지원:
    - mid-circuit measurement (``qml.measure`` 의 ``MidMeasureMP``) — 위치별
      panta-sim ``measure(q, cbit)`` 로 자동 매핑. cbit 인덱스는 발견 순서.

미지원 (v0.4.6+ 또는 그 이후):
    - ``qml.cond`` (PennyLane classical control / ``Conditional`` op) →
      명시적 ``NotImplementedError``. 대안: Qiskit 어댑터 (``qc.x(0).c_if(c, 1)``).
    - var / purity / vn_entropy measurement.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Sequence, Union

import numpy as np

from .circuit import QuantumCircuit as PantaCircuit

if TYPE_CHECKING:  # pragma: no cover
    from pennylane.devices import ExecutionConfig
    from pennylane.tape import QuantumScript


_PENNYLANE_INSTALL_HINT = (
    "pennylane is required for this device — install with: "
    "pip install panta-sim[pennylane]"
)


def _scalar_param(x: Any) -> float:
    """게이트 각도 파라미터를 float 로 변환한다.

    PennyLane 의 parameter-shift autodiff (v0.7) 는 게이트 각도를 0-dim 또는
    1-element ndarray (qml.numpy trainable) 로 넘길 수 있다.  numpy 2.x 에서는
    1-element 배열에 ``float()`` 이 실패하므로 ravel 후 첫 원소를 취한다.
    """
    import numpy as _np

    arr = _np.asarray(x)
    if arr.ndim == 0:
        return float(arr)
    return float(arr.ravel()[0])


def _lazy_import_pennylane() -> Any:
    try:
        import pennylane as qml  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover
        raise ImportError(_PENNYLANE_INSTALL_HINT) from exc
    return qml


# PennyLane gate name → panta-sim QuantumCircuit method name.
_DIRECT_GATE_MAP: dict[str, str] = {
    "Hadamard": "h",
    "PauliX": "x",
    "PauliY": "y",
    "PauliZ": "z",
    "S": "s",
    "T": "t",
    "Identity": "id",
    "RX": "rx",
    "RY": "ry",
    "RZ": "rz",
    "CNOT": "cx",
    "CZ": "cz",
    "SWAP": "swap",
    "Toffoli": "ccx",
    "CSWAP": "cswap",
    # PennyLane 의 표기 alternates
    "I": "id",
    "X": "x",
    "Y": "y",
    "Z": "z",
    "H": "h",
}


def _try_import_device():
    qml = _lazy_import_pennylane()
    try:
        from pennylane.devices import Device  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            f"pennylane.devices.Device not found — pennylane>=0.35 required ({exc})"
        ) from exc
    return qml, Device


def _package_version() -> str:
    """panta_sim 패키지의 ``__version__`` 을 읽는다 (``PantaDevice.version`` 동기화).

    plugin entry point 등 부분 초기화 코너 케이스에서도 import 가 깨지지 않도록
    실패 시 ``"unknown"`` 으로 폴백한다.
    """
    try:
        from panta_sim import __version__

        return __version__
    except ImportError:  # pragma: no cover — 부분 초기화 방어
        return "unknown"


class PantaDevice:
    """``qml.device("panta-sim", wires=N)`` 의 backend.

    이 클래스는 import 시점에 PennyLane 을 요구하지 않는다 — 인스턴스 생성
    시점에만 lazy import. PennyLane plugin entry point 에 등록되어 사용자
    코드에선 ``qml.device("panta-sim", wires=N, shots=None)`` 한 줄로
    instantiate.

    Args:
        wires: 큐비트 수 (int) 또는 wire labels (sequence).
        shots: ``None`` 이면 analytic statevector mode. 정수 ``N`` 이면 N shots
            sampling. 혼합 (``None`` + sample measurement) 은 PennyLane 측에서
            거부.
        seed: ``qml.sample`` / ``qml.counts`` 샘플링 RNG seed (재현성).
            ``None`` (기본) 이면 비결정적.

    Example:
        >>> import pennylane as qml
        >>> dev = qml.device("panta-sim", wires=2)
        >>> @qml.qnode(dev)
        ... def circuit():
        ...     qml.Hadamard(wires=0)
        ...     qml.CNOT(wires=[0, 1])
        ...     return qml.expval(qml.PauliZ(0))
        >>> circuit()  # 0.0 (Bell state)
    """

    name = "panta-sim"
    short_name = "panta-sim"
    pennylane_requires = ">=0.35"
    version = _package_version()
    author = "quantumfia"

    def __new__(cls, *args, **kwargs):
        # PennyLane Device 의 신 API base class 를 lazy import 후 동적으로
        # 상속한다 — pennylane 미설치 환경에서도 모듈 import 가 깨지지 않도록.
        _, Device = _try_import_device()
        if Device not in cls.__mro__:
            new_cls = type(cls.__name__, (cls, Device), {})
            return Device.__new__(new_cls)
        return Device.__new__(cls)  # type: ignore[arg-type]

    def __init__(
        self,
        wires: Union[int, Sequence[Any]],
        shots: Optional[int] = None,
        *,
        seed: Optional[int] = None,
    ) -> None:
        qml, Device = _try_import_device()
        Device.__init__(self, wires=wires, shots=shots)
        # sample/counts 샘플링용 RNG seed (None 이면 비결정적).
        self._seed = seed

    def execute(
        self,
        circuits: Union["QuantumScript", Sequence["QuantumScript"]],
        execution_config: Optional["ExecutionConfig"] = None,
    ) -> Union[Any, Sequence[Any]]:
        """PennyLane 의 ``Device.execute`` 진입점."""
        qml = _lazy_import_pennylane()

        # Single tape 인 경우 단일 결과, 시퀀스인 경우 리스트.
        is_single = not isinstance(circuits, (list, tuple))
        tapes = [circuits] if is_single else list(circuits)

        results = [self._execute_tape(tape) for tape in tapes]
        return results[0] if is_single else tuple(results)

    # ------------------------------------------------------------------
    # internal
    # ------------------------------------------------------------------

    def _wire_to_qubit(self, wire: Any, n: int) -> int:
        """PennyLane wire label → panta-sim qubit index. wire 0 → qubit (n-1)."""
        idx = self.wires.index(wire)  # type: ignore[attr-defined]
        return n - 1 - idx

    def _process_op(
        self,
        op: Any,
        panta_qc: PantaCircuit,
        n: int,
        cbit_counter: Optional[list] = None,
    ) -> None:
        """단일 PennyLane op 을 panta-sim 회로에 추가. 미지원이면 분해 후 recurse.

        ``cbit_counter`` 는 mid-circuit ``MidMeasureMP`` 마다 cbit 인덱스를 할당
        하는 용도의 가변 카운터 (``[int]`` shape). ``_build_circuit`` 이 ``[0]``
        으로 초기화하고 매 mid-measure 마다 1 증가시킨다 (None 이면 저장 안 함).
        """
        qml = _lazy_import_pennylane()
        op_name = op.name

        # qml.cond 결과 (Conditional op) → v0.4.5 거부.
        if op_name == "Conditional" or op_name.startswith("Cond("):
            raise NotImplementedError(
                "PennyLane qml.cond (Conditional op) is not supported by "
                "panta-sim (deferred to v0.4.6+). Use the Qiskit adapter "
                "(qc.x(0).c_if(c, 1)) for classical-control circuits."
            )

        # qml.measure 의 결과 (MidMeasureMP) — mid-circuit measurement.
        # PennyLane 의 MeasurementProcess 류 중 'measure' 카테고리지만
        # tape.operations 에 들어간다 (gate 와 동일 위치 처리 필요).
        if hasattr(qml, "measurements") and isinstance(
            op, qml.measurements.MidMeasureMP
        ):
            wire = op.wires[0]
            qubit_idx = self._wire_to_qubit(wire, n)
            cbit = (cbit_counter[0] if cbit_counter is not None else 0)
            panta_qc.measure(qubit_idx, cbit)
            if cbit_counter is not None:
                cbit_counter[0] += 1
            return

        # Adjoint(S) / Adjoint(T) → sdg / tdg.
        if op_name == "Adjoint(S)":
            panta_qc.sdg(self._wire_to_qubit(op.wires[0], n))
            return
        if op_name == "Adjoint(T)":
            panta_qc.tdg(self._wire_to_qubit(op.wires[0], n))
            return

        if op_name in _DIRECT_GATE_MAP:
            method_name = _DIRECT_GATE_MAP[op_name]
            qubits = [self._wire_to_qubit(w, n) for w in op.wires]

            if method_name in ("rx", "ry", "rz"):
                theta = _scalar_param(op.parameters[0])
                getattr(panta_qc, method_name)(theta, qubits[0])
            else:
                getattr(panta_qc, method_name)(*qubits)
            return

        if op_name == "GlobalPhase":
            # GlobalPhase(φ) = e^{-iφ} · I. panta-sim 의 unitary 가 Z-Y-Z 분해
            # 시 α = -φ 만 누적하므로 어떤 qubit 에 적용해도 회로 전체 phase 동일.
            phi = _scalar_param(op.parameters[0])
            matrix = np.exp(-1j * phi) * np.eye(2, dtype=complex)
            panta_qc.unitary(matrix, 0)
            return

        if op_name == "QubitUnitary":
            matrix = np.asarray(op.matrix(), dtype=np.complex128)
            if matrix.shape == (2, 2):
                panta_qc.unitary(matrix, self._wire_to_qubit(op.wires[0], n))
                return
            # 다큐빗 unitary → decomposition 으로 풀어주길 시도.

        # 분해 시도.
        if op.has_decomposition:
            for sub_op in op.decomposition():
                self._process_op(sub_op, panta_qc, n, cbit_counter)
            return

        raise ValueError(
            f"PennyLane op {op_name!r} is not supported by panta-sim and "
            "has no decomposition. Try qml.transforms.decompose first."
        )

    def _build_circuit(self, tape: Any) -> PantaCircuit:
        n = len(self.wires)  # type: ignore[attr-defined]
        panta_qc = PantaCircuit(n)
        cbit_counter = [0]  # mid-circuit measure 마다 cbit 인덱스 할당.
        for op in tape.operations:
            self._process_op(op, panta_qc, n, cbit_counter)
        return panta_qc

    def _execute_tape(self, tape: Any) -> Any:
        """단일 tape 실행: panta-sim 으로 statevector 산출 후 PennyLane 측정 함수에 위임.

        PennyLane 의 ``pennylane.devices.qubit.measure`` / ``measure_with_samples``
        가 expval / probs / state / var / sample / counts 를 모두 정확히
        처리하므로, 우리는 ``(2,)*n`` shape 의 statevector ndarray 만
        제공하면 된다 (default.qubit 가 사용하는 표준 형식).
        """
        _lazy_import_pennylane()
        from pennylane.devices.qubit import (  # type: ignore
            measure as pl_measure,
        )
        from pennylane.devices.qubit import (
            measure_with_samples as pl_measure_with_samples,
        )
        from pennylane.measurements import CountsMP, SampleMP  # type: ignore

        n = len(self.wires)  # type: ignore[attr-defined]
        panta_qc = self._build_circuit(tape)

        # shots 결정.
        shots_obj = getattr(tape, "shots", None)
        if shots_obj is None or getattr(shots_obj, "total_shots", None) is None:
            shots_obj = getattr(self, "shots", None)  # type: ignore[attr-defined]

        # Statevector 한 번 산출 후 (2,)^n 으로 reshape — PennyLane 의
        # multi-dim state convention. wire k 가 axis k 로 매핑된다 (panta-sim
        # 의 qubit (n-1-k) → wire k 매핑이 numpy C-order reshape 와 일치).
        state_flat = panta_qc.run(shots=0).statevector().astype(np.complex128)
        state_md = state_flat.reshape((2,) * n) if n > 0 else state_flat

        # Sample / Counts 분리 처리.
        sample_mps = [
            mp for mp in tape.measurements if isinstance(mp, (SampleMP, CountsMP))
        ]
        state_mps = [
            mp for mp in tape.measurements
            if not isinstance(mp, (SampleMP, CountsMP))
        ]

        results_by_idx: dict[int, Any] = {}

        for idx, mp in enumerate(tape.measurements):
            if mp in state_mps:
                results_by_idx[idx] = pl_measure(mp, state_md)

        if sample_mps:
            if shots_obj is None or getattr(shots_obj, "total_shots", None) is None:
                raise ValueError(
                    "qml.sample / qml.counts requires shots — pass shots=N to "
                    "qml.device('panta-sim', wires=..., shots=N) or to the QNode."
                )
            rng = np.random.default_rng(getattr(self, "_seed", None))
            sampled = pl_measure_with_samples(
                sample_mps, state_md, shots_obj, rng=rng
            )
            sample_iter = iter(sampled)
            for idx, mp in enumerate(tape.measurements):
                if mp in sample_mps:
                    results_by_idx[idx] = next(sample_iter)

        results = [results_by_idx[i] for i in range(len(tape.measurements))]
        return results[0] if len(results) == 1 else tuple(results)


__all__ = ["PantaDevice"]
