"""외부 양자 프레임워크 호환 어댑터 (v0.3.5+).

이 패키지는 panta-sim 회로 ↔ 외부 프레임워크 회로 변환 함수를 제공한다.
모든 어댑터는 lazy import 패턴 — 외부 라이브러리는 함수 호출 시점에만
로드되며, 미설치 시 친절한 ``ImportError`` 가 발생한다.

지원 프레임워크 (v0.3.5):
    - Qiskit: ``from_qiskit`` / ``to_qiskit`` (이 모듈은 v0.3.5 Cut 1)
    - Cirq:   ``from_cirq`` / ``to_cirq``  (v0.3.5 Cut 4)
    - PennyLane: ``panta_sim.pennylane_device.PantaDevice`` (v0.3.5 Cut 3)

호환 패턴:
    >>> from qiskit import QuantumCircuit as QC
    >>> from panta_sim import from_qiskit
    >>> qc = QC(2); qc.h(0); qc.cx(0, 1)
    >>> panta_qc = from_qiskit(qc)
    >>> result = panta_qc.run(shots=1024)
"""

from __future__ import annotations

from .cirq import from_cirq, to_cirq
from .cirq_noise import from_cirq_noise
from .pennylane_noise import from_pennylane_noise
from .qiskit import from_qiskit, to_qiskit
from .qiskit_noise import from_qiskit_noise_model

__all__ = [
    "from_qiskit",
    "to_qiskit",
    "from_qiskit_noise_model",
    "from_cirq",
    "to_cirq",
    "from_cirq_noise",
    "from_pennylane_noise",
]
