"""panta-sim: Rust 코어 양자 회로 시뮬레이터."""

from .adapters import (
    from_cirq,
    from_cirq_noise,
    from_pennylane_noise,
    from_qiskit,
    from_qiskit_noise_model,
    to_cirq,
    to_qiskit,
)
from .circuit import QuantumCircuit
from .noise import NoiseModel
from .qiskit_primitives import PantaEstimator, PantaSampler
from .result import SimulationResult
from .visualize import histogram_text, plot_bloch, plot_histogram

__version__ = "0.6.7"
__all__ = [
    "QuantumCircuit",
    "SimulationResult",
    "NoiseModel",
    "plot_histogram",
    "histogram_text",
    "plot_bloch",
    "from_qiskit",
    "to_qiskit",
    "from_qiskit_noise_model",
    "from_cirq",
    "to_cirq",
    "from_cirq_noise",
    "from_pennylane_noise",
    "PantaSampler",
    "PantaEstimator",
    "__version__",
]


def __getattr__(name: str):
    """``PantaDevice`` 는 PennyLane 미설치 환경에서도 panta-sim 자체 import 가
    깨지지 않도록 lazy 노출한다."""
    if name == "PantaDevice":
        from .pennylane_device import PantaDevice  # type: ignore

        return PantaDevice
    raise AttributeError(f"module 'panta_sim' has no attribute {name!r}")
