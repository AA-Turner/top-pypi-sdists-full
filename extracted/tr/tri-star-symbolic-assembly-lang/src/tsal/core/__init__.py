"""Core TSAL functionality."""

from .rev_eng import Rev_Eng
from .phase_math import phase_match_enhanced, mesh_phase_sync
from .phi_math import (
    phi_wavefunction,
    phase_alignment_potential,
    corrected_energy,
    orbital_radius,
)
from .mesh_logger import log_event
from .intent_metric import calculate_idm
from .optimizer_utils import (
    SymbolicSignature,
    node_complexity,
    extract_signature,
)
from .spiral_fusion import SpiralFusionProtocol
from .state_vector import FourVector
from .opwords import OP_WORD_MAP, op_from_word
from .spark_translator import SPARK_TO_OPCODE, translate_spark_word
from .executor import MetaFlagProtocol, TSALExecutor
from .spiral_memory import SpiralMemory
from .madmonkey_handler import MadMonkeyHandler
from .connectivity import Node, verify_connectivity
from .logic_gate import DynamicLogicGate
from .module_registry import registry as module_registry, ModuleMeta
from .shadow import ShadowMemory
from .merge import merge_voxels
from .gradient import voxel_gradient
from .superpos import superpose
from .entangle import entangle
from .manifold import manifold_distance
from .reflection import ReflectionLog, mood_from_traits
from .meta_coherence import SpiralSignature, compute_spiral_signature
from .spin_algebra import SpinState, SpinInteraction, combine_spins
from .guardian_constants import (
    PERCEPTION_THRESHOLD,
    LEARNING_RATE,
    CONNECTION_DECAY,
    MAX_NODES,
    MAX_AGENTS,
    MAX_DIMENSIONS,
)

__all__ = [
    "Rev_Eng",
    "phase_match_enhanced",
    "mesh_phase_sync",
    "phi_wavefunction",
    "phase_alignment_potential",
    "corrected_energy",
    "orbital_radius",
    "log_event",
    "calculate_idm",
    "SymbolicSignature",
    "node_complexity",
    "extract_signature",
    "SpiralFusionProtocol",
    "FourVector",
    "OP_WORD_MAP",
    "op_from_word",
    "SPARK_TO_OPCODE",
    "translate_spark_word",
    "MetaFlagProtocol",
    "TSALExecutor",
    "SpiralMemory",
    "MadMonkeyHandler",
    "Node",
    "verify_connectivity",
    "DynamicLogicGate",
    "module_registry",
    "ModuleMeta",
    "ShadowMemory",
    "merge_voxels",
    "voxel_gradient",
    "superpose",
    "entangle",
    "manifold_distance",
    "ReflectionLog",
    "mood_from_traits",
    "PERCEPTION_THRESHOLD",
    "LEARNING_RATE",
    "CONNECTION_DECAY",
    "MAX_NODES",
    "MAX_AGENTS",
    "MAX_DIMENSIONS",
    "SpiralSignature",
    "compute_spiral_signature",
    "SpinState",
    "SpinInteraction",
    "combine_spins",
]
