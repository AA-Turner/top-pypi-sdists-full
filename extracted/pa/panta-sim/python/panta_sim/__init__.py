"""panta-sim: Rust 코어 양자 회로 시뮬레이터."""

from .adapters import (
    from_braket,
    from_cirq,
    from_cirq_noise,
    from_pennylane_noise,
    from_qiskit,
    from_qiskit_noise_model,
    to_braket,
    to_cirq,
    to_qiskit,
)
from .circuit import QuantumCircuit
from . import benchmarks
from .benchmarks import linear_xeb, random_circuit, xeb_ideal, xeb_noisy
from . import distributed
from .distributed import (
    MpiReducer,
    SerialReducer,
    distributed_amplitude,
    simulate_cluster_amplitude,
)
from . import algorithms
from .algorithms import (
    bernstein_vazirani,
    deutsch_jozsa,
    draper_add_constant,
    draper_add_register,
    ghz_state,
    grover,
    grover_diffusion,
    grover_operator,
    amplitude_estimation,
    quantum_counting,
    inverse_qft,
    phase_oracle,
    qft,
    qft_circuit,
    quantum_phase_estimation,
    uniform_superposition,
    w_state,
)
from . import hamiltonians
from .hamiltonians import heisenberg_hamiltonian, ising_hamiltonian, tfim_hamiltonian
from . import evolution
from .evolution import pauli_evolution, trotter_circuit
from .noise import NoiseModel
from .parameter import Parameter, ParameterExpression
from . import quantum_info
from .qiskit_primitives import PantaEstimator, PantaSampler
from .result import SimulationResult
from . import synthesis
from .variational import (
    VQE,
    VQEResult,
    expectation,
    finite_difference_gradient,
    maxcut_hamiltonian,
    parameter_shift_gradient,
    qaoa_ansatz,
    qaoa_maxcut_ansatz,
)
from .visualize import histogram_text, plot_bloch, plot_histogram

__version__ = "0.8.22"
__all__ = [
    "QuantumCircuit",
    "SimulationResult",
    "NoiseModel",
    "Parameter",
    "ParameterExpression",
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
    "from_braket",
    "to_braket",
    "PantaSampler",
    "PantaEstimator",
    "VQE",
    "VQEResult",
    "expectation",
    "parameter_shift_gradient",
    "finite_difference_gradient",
    "maxcut_hamiltonian",
    "qaoa_maxcut_ansatz",
    "qaoa_ansatz",
    "hamiltonians",
    "ising_hamiltonian",
    "tfim_hamiltonian",
    "heisenberg_hamiltonian",
    "evolution",
    "pauli_evolution",
    "trotter_circuit",
    "quantum_info",
    "synthesis",
    "algorithms",
    "qft",
    "inverse_qft",
    "qft_circuit",
    "grover",
    "grover_diffusion",
    "grover_operator",
    "amplitude_estimation",
    "quantum_counting",
    "phase_oracle",
    "quantum_phase_estimation",
    "draper_add_constant",
    "draper_add_register",
    "bernstein_vazirani",
    "deutsch_jozsa",
    "ghz_state",
    "w_state",
    "uniform_superposition",
    "benchmarks",
    "random_circuit",
    "linear_xeb",
    "xeb_ideal",
    "xeb_noisy",
    "distributed",
    "distributed_amplitude",
    "simulate_cluster_amplitude",
    "SerialReducer",
    "MpiReducer",
    "__version__",
]


def __getattr__(name: str):
    """``PantaDevice`` 는 PennyLane 미설치 환경에서도 panta-sim 자체 import 가
    깨지지 않도록 lazy 노출한다."""
    if name == "PantaDevice":
        from .pennylane_device import PantaDevice  # type: ignore

        return PantaDevice
    raise AttributeError(f"module 'panta_sim' has no attribute {name!r}")
