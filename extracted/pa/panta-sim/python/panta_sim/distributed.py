"""멀티노드 분산 transport 추상화 (v0.8) — distributed slicing 의 reduce 레이어.

Tensor Network 분산 슬라이싱은 각 slice 가 독립적이라 worker/노드가 서로 다른
slice 범위를 계산하고 **부분합을 all-reduce (sum)** 하면 전체 amplitude 가 된다.
이 모듈은 그 reduce 를 추상화한다:

- [`Reducer`] 프로토콜: ``size`` / ``rank`` / ``allreduce_sum(value)``.
- [`MpiReducer`]: ``mpi4py`` 의 ``COMM_WORLD`` 래퍼 (실 클러스터).  각 MPI rank 가
  같은 스크립트를 실행하고, 자기 worker 부분합을 계산한 뒤 ``allreduce_sum`` 으로
  네트워크 reduce → 모든 rank 가 전체 amplitude 를 얻는다.
- [`simulate_cluster_amplitude`]: 단일 프로세스에서 ``n_ranks`` 를 순차 모사 —
  분산 결과의 정확성을 in-sandbox 로 검증 (실 transport 없이).

실 MPI 사용 패턴::

    # mpirun -n 16 python my_xeb.py
    from panta_sim.distributed import MpiReducer, distributed_amplitude
    reducer = MpiReducer()
    amp = distributed_amplitude(qc, bitstring, reducer, max_width=27)
    # 모든 rank 가 동일한 전체 amplitude 를 보유 (allreduce 후).
"""

from __future__ import annotations

from typing import Optional, Protocol

from .circuit import QuantumCircuit


class Reducer(Protocol):
    """분산 all-reduce 추상 인터페이스.  worker 부분합 (복소수) 을 모든 rank
    합산해 전체 값을 돌려준다."""

    @property
    def size(self) -> int:
        """전체 rank (노드) 수."""
        ...

    @property
    def rank(self) -> int:
        """이 프로세스의 rank (``0..size``)."""
        ...

    def allreduce_sum(self, value: complex) -> complex:
        """모든 rank 의 ``value`` 를 합산해 (모든 rank 에) 반환."""
        ...


class SerialReducer:
    """단일 rank (size=1) — 비분산 fallback.  ``allreduce_sum`` 은 항등."""

    @property
    def size(self) -> int:
        return 1

    @property
    def rank(self) -> int:
        return 0

    def allreduce_sum(self, value: complex) -> complex:
        return value


class MpiReducer:
    """``mpi4py`` ``COMM_WORLD`` 기반 분산 reducer (실 클러스터).

    ``mpi4py`` 미설치 시 ``ImportError``.  ``mpirun -n W python script.py`` 로
    실행하면 각 프로세스가 자기 rank/size 를 얻고, ``allreduce_sum`` 이
    ``MPI.SUM`` all-reduce 를 수행한다.
    """

    def __init__(self) -> None:
        from mpi4py import MPI  # lazy: 미설치 환경 안전

        self._MPI = MPI
        self._comm = MPI.COMM_WORLD

    @property
    def size(self) -> int:
        return int(self._comm.Get_size())

    @property
    def rank(self) -> int:
        return int(self._comm.Get_rank())

    def allreduce_sum(self, value: complex) -> complex:
        return complex(self._comm.allreduce(value, op=self._MPI.SUM))


def distributed_amplitude(
    circuit: QuantumCircuit,
    bitstring,
    reducer: Reducer,
    optimizer: str = "hyper",
    max_width: float = 27.0,
    max_slices: int = 40,
    seed: Optional[int] = None,
) -> complex:
    """분산 슬라이싱 amplitude — 이 rank 의 부분합을 계산하고 all-reduce 한다.

    각 rank 가 동일 (결정론적) slice plan 을 독립 재구성하고 자기 slice 범위만
    수축 (``amplitude_distributed(worker_id=rank, n_workers=size)``) 한 뒤
    ``reducer.allreduce_sum`` 으로 전체 amplitude 를 얻는다.  worker 당 peak
    메모리는 sliced contraction width (전체 N 무관) 라 노드 RAM 에 맞춰
    ``max_width`` 로 제어한다.

    Returns:
        전체 amplitude ``⟨bitstring|C|0…0⟩`` (모든 rank 동일).
    """
    partial = circuit.amplitude_distributed(
        bitstring,
        n_workers=reducer.size,
        worker_id=reducer.rank,
        optimizer=optimizer,
        max_width=max_width,
        max_slices=max_slices,
        seed=seed,
    )
    return reducer.allreduce_sum(partial)


def simulate_cluster_amplitude(
    circuit: QuantumCircuit,
    bitstring,
    n_ranks: int,
    optimizer: str = "hyper",
    max_width: float = 27.0,
    max_slices: int = 40,
    seed: Optional[int] = None,
) -> complex:
    """``n_ranks`` 노드 클러스터를 단일 프로세스에서 모사 — 각 rank 의 부분합을
    계산해 합산 (실 transport 없는 정확성 검증/단일 머신 실행).  결과는
    비분산 ``amplitude`` 와 동일.

    Returns:
        전체 amplitude (모든 rank 부분합의 합).
    """
    total = 0j
    for r in range(n_ranks):
        total += circuit.amplitude_distributed(
            bitstring,
            n_workers=n_ranks,
            worker_id=r,
            optimizer=optimizer,
            max_width=max_width,
            max_slices=max_slices,
            seed=seed,
        )
    return total
