"""Qiskit Primitives V2 wrapper (v0.3.5 Cut 2).

panta-sim 을 Qiskit 의 ``BaseSamplerV2`` / ``BaseEstimatorV2`` 인터페이스로
노출하는 ``PantaSampler`` / ``PantaEstimator`` 를 제공한다. 사용자는 Qiskit
Runtime 코드의 ``StatevectorSampler()`` / ``StatevectorEstimator()`` 를
panta-sim 변형으로 한 줄만 갈아끼우면 된다.

지원 범위 (v0.3.5):
    - Sampler / Estimator 모두 broadcasting 없는 scalar pub (``shape=()``) 만 지원.
    - parameter binding 은 정수 / float key-value 또는 array-like.
    - Estimator 는 ``ObservablesArray`` 의 dict-of-Pauli-string 형식.

지원 안 함 (v0.3.5):
    - Multi-dimensional broadcasting (``BindingsArray.shape != ()``) — 단일 회로
      반복 호출로 대체.
    - non-Pauli observable — Qiskit 의 표준은 SparsePauliOp / Pauli 이므로 사실상
      문제 없음.

검증: Qiskit ``StatevectorSampler`` 와 동일 회로 + seed 에서 동일 BitArray
counts. ``StatevectorEstimator`` 와 expectation value 1e-10 (f64) 일치.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Optional

import numpy as np

from .adapters.qiskit import _lazy_import_qiskit, from_qiskit

if TYPE_CHECKING:  # pragma: no cover
    from qiskit.primitives.containers import (
        EstimatorPub,
        EstimatorPubLike,
        PrimitiveResult,
        SamplerPub,
        SamplerPubLike,
    )


_DEFAULT_SHOTS = 1024


def _check_no_unbound_parameters(qc: Any) -> None:
    if list(qc.parameters):
        raise ValueError(
            "circuit has unbound Parameters: "
            f"{list(qc.parameters)}. Pass parameter values via the pub tuple."
        )


def _bind_parameters(qc: Any, parameter_values: Any) -> Any:
    """``BindingsArray`` 가 비어있으면 그대로, 있으면 ``assign_parameters`` 호출."""
    # parameter_values 는 BindingsArray. shape () 이고 num_parameters 0 이면 no-op.
    if parameter_values is None:
        return qc
    if getattr(parameter_values, "num_parameters", 0) == 0:
        return qc
    if parameter_values.shape != ():
        raise NotImplementedError(
            "panta-sim Primitives 는 v0.3.5 에서 broadcasting (shape != ()) 을 "
            "지원하지 않는다. 회로별로 반복 호출하라."
        )
    # BindingsArray 의 element-wise 호출. as_array() 로 dict 화 후 bind.
    bindings = parameter_values.as_array(qc.parameters)  # type: ignore[arg-type]
    # bindings 는 1D numpy array (parameter 순서대로). assign_parameters 가 받음.
    return qc.assign_parameters(bindings)


def _expval_from_state(state: np.ndarray, observable_dict: dict[str, complex]) -> float:
    """SparsePauliOp 형식 dict ({Pauli string: coeff}) 의 ⟨ψ|H|ψ⟩ 계산.

    작은 큐비트 (state.size == 2^n, n ≤ 25) 에서 dense matmul 로 충분히 빠르다.
    """
    qiskit = _lazy_import_qiskit()
    SparsePauliOp = qiskit.quantum_info.SparsePauliOp

    op = SparsePauliOp.from_list(list(observable_dict.items()))
    matrix = op.to_matrix()
    # ⟨ψ|H|ψ⟩ — Hermitian 이라 실수.
    expval = np.vdot(state, matrix @ state)
    return float(np.real(expval))


def _make_primitive_job(callable_task: Any) -> Any:
    """Qiskit ``PrimitiveJob`` 을 만들고 즉시 ``_submit`` 한다 (synchronous)."""
    _lazy_import_qiskit()
    from qiskit.primitives.primitive_job import PrimitiveJob  # type: ignore

    job = PrimitiveJob(callable_task)
    job._submit()
    return job


def _project_counts_to_register(
    counts: dict[str, int],
    indices: list[int],
    total_clbits: int,
) -> dict[str, int]:
    """``counts`` (full-width MSB-first bit string) 을 ``indices`` 의 비트만
    추출한 register-local counts 로 project.

    panta-sim 의 ``SimulationResult.counts()`` 는 ``cbits.iter().rev()`` 로
    packing 한 MSB-first bit string (engine.rs).  string idx i 는 절대 clbit
    인덱스 ``total_clbits - 1 - i`` 를 의미한다.  이 함수는 register 안의 각
    clbit 의 절대 인덱스 (``indices``, LSB-first) 를 받아 register-local
    MSB-first substring 을 만든다.

    여러 outcome 이 같은 register substring 으로 collapse 될 수 있어 합산.

    Args:
        counts: 전체 회로 outcome counts (key 길이 = ``total_clbits``).
        indices: register 의 각 clbit 의 절대 회로 인덱스 (LSB-first).
        total_clbits: 회로 전체 classical bit 수.

    Returns:
        register-local counts. key 길이 = ``len(indices)``, MSB-first.
    """
    out: dict[str, int] = {}
    for full_key, n in counts.items():
        # full_key 길이가 total_clbits 와 다른 경우 (panta-sim 가 fast-path 에서
        # 다른 width 를 줄 수 있음) 정상화: leading 0 padding.
        padded = full_key.rjust(total_clbits, "0")
        # register substring: register MSB → LSB 순.
        chars = []
        for abs_idx in reversed(indices):
            # MSB-first 표기에서 string idx = total_clbits - 1 - abs_idx.
            chars.append(padded[total_clbits - 1 - abs_idx])
        sub = "".join(chars)
        out[sub] = out.get(sub, 0) + n
    return out


class PantaSampler:
    """Qiskit ``BaseSamplerV2`` 인터페이스를 panta-sim 백엔드로 구현한다.

    Args:
        default_shots: ``run(pubs)`` 호출 시 shots 가 명시되지 않은 pub 에
            적용되는 default. Qiskit 의 ``StatevectorSampler`` 와 동일하게
            ``1024`` 가 기본값.
        seed: ``panta_sim.QuantumCircuit.run`` 에 전달할 random seed
            (재현성). ``None`` 이면 매번 다른 결과.

    Example:
        >>> from qiskit import QuantumCircuit
        >>> from panta_sim.qiskit_primitives import PantaSampler
        >>> qc = QuantumCircuit(2)
        >>> qc.h(0); qc.cx(0, 1); qc.measure_all()
        >>> sampler = PantaSampler()
        >>> result = sampler.run([(qc,)], shots=1024).result()
        >>> bitarray = result[0].data.meas
        >>> bitarray.get_counts()  # {'00': ~512, '11': ~512}
    """

    def __init__(
        self,
        default_shots: int = _DEFAULT_SHOTS,
        seed: Optional[int] = None,
    ) -> None:
        self._default_shots = int(default_shots)
        self._seed = seed

    def run(
        self,
        pubs: "Iterable[SamplerPubLike]",
        *,
        shots: Optional[int] = None,
    ) -> Any:
        """Sampler 실행. Qiskit ``BaseSamplerV2.run`` 시그니처와 일치한다."""
        _lazy_import_qiskit()
        from qiskit.primitives.containers import (  # type: ignore
            DataBin,
            PrimitiveResult,
            SamplerPub,
            SamplerPubResult,
        )
        from qiskit.primitives.containers.bit_array import BitArray  # type: ignore

        coerced: list[Any] = [SamplerPub.coerce(p, shots) for p in pubs]
        default_shots = shots if shots is not None else self._default_shots

        def _task() -> Any:
            pub_results: list[Any] = []
            for pub in coerced:
                qc = _bind_parameters(pub.circuit, pub.parameter_values)
                _check_no_unbound_parameters(qc)
                n_shots = pub.shots if pub.shots is not None else default_shots

                panta_qc = from_qiskit(qc)
                sim_result = panta_qc.run(shots=int(n_shots), seed=self._seed)
                counts = sim_result.counts() or {"" * qc.num_qubits: int(n_shots)}

                # 회로의 ClassicalRegister 별로 BitArray 를 만들어야 표준 형식.
                # measure_all() 은 'meas' creg 자동 생성. measure(q,c) 만 쓰면
                # default 'c' creg.
                # v0.6.2 fix: 이전엔 모든 creg 에 동일 full-width counts 를 broadcast
                # 했음 — multi-creg 회로에서 각 register 가 자기 비트만 봐야 하는
                # Qiskit Primitive V2 spec 위반.  각 creg 의 절대 clbit index 를
                # find_bit 로 구해 counts substring 을 project 한다.
                data_fields: dict[str, Any] = {}
                total_clbits = qc.num_clbits
                for creg in qc.cregs:
                    # creg 의 각 clbit 의 회로 전역 인덱스 (LSB-first).
                    indices = [qc.find_bit(b).index for b in creg]
                    register_counts = _project_counts_to_register(
                        counts, indices, total_clbits
                    )
                    data_fields[creg.name] = BitArray.from_counts(
                        register_counts, num_bits=creg.size
                    )
                if not data_fields:
                    # measure 가 없는 회로 — Qiskit 도 빈 DataBin 반환이지만 통상
                    # 사용자는 measure 를 넣는다. 안전 fallback.
                    data_fields["meas"] = BitArray.from_counts(
                        counts, num_bits=qc.num_qubits
                    )

                data_bin = DataBin(**data_fields, shape=())
                pub_results.append(SamplerPubResult(data=data_bin, metadata={}))

            return PrimitiveResult(pub_results, metadata={})

        return _make_primitive_job(_task)


class PantaEstimator:
    """Qiskit ``BaseEstimatorV2`` 인터페이스를 panta-sim 백엔드로 구현한다.

    expectation value 는 panta-sim 의 statevector (shots=0) 에서 분석적으로
    계산되어, Qiskit ``StatevectorEstimator`` 와 1e-10 (f64) 일치한다.
    statistical noise 는 0 (shot-based estimation 이 아니므로).

    Example:
        >>> from qiskit import QuantumCircuit
        >>> from qiskit.quantum_info import SparsePauliOp
        >>> from panta_sim.qiskit_primitives import PantaEstimator
        >>> qc = QuantumCircuit(2); qc.h(0); qc.cx(0, 1)
        >>> obs = SparsePauliOp.from_list([("ZZ", 1.0), ("XX", 0.5)])
        >>> est = PantaEstimator()
        >>> result = est.run([(qc, obs)]).result()
        >>> result[0].data.evs  # Bell <ZZ + 0.5 XX> = 1 + 0.5 = 1.5
    """

    def __init__(self) -> None:
        pass

    def run(
        self,
        pubs: "Iterable[EstimatorPubLike]",
        *,
        precision: Optional[float] = None,
    ) -> Any:
        """Estimator 실행. ``precision`` 은 statevector path 에서 의미 없음."""
        _lazy_import_qiskit()
        from qiskit.primitives.containers import (  # type: ignore
            DataBin,
            EstimatorPub,
            PrimitiveResult,
            PubResult,
        )

        coerced: list[Any] = [EstimatorPub.coerce(p, precision) for p in pubs]

        def _task() -> Any:
            pub_results: list[Any] = []
            for pub in coerced:
                qc = _bind_parameters(pub.circuit, pub.parameter_values)
                _check_no_unbound_parameters(qc)

                # statevector mode (shots=0) 로 한 번 시뮬.
                panta_qc = from_qiskit(qc)
                state = panta_qc.run(shots=0).statevector().astype(np.complex128)

                obs_array = pub.observables
                if obs_array.shape != ():
                    raise NotImplementedError(
                        "panta-sim PantaEstimator 는 v0.3.5 에서 observable "
                        "broadcasting (shape != ()) 을 지원하지 않는다."
                    )
                # observables[()] → dict of Pauli string → coeff.
                obs_dict: dict[str, complex] = obs_array[()]
                expval = _expval_from_state(state, obs_dict)

                # numpy scalar 형태로 (Qiskit 도 0-d ndarray).
                evs = np.array(expval, dtype=float)
                stds = np.array(0.0, dtype=float)

                data_bin = DataBin(evs=evs, stds=stds, shape=())
                pub_results.append(PubResult(data=data_bin, metadata={}))

            return PrimitiveResult(pub_results, metadata={})

        return _make_primitive_job(_task)


__all__ = ["PantaSampler", "PantaEstimator"]
