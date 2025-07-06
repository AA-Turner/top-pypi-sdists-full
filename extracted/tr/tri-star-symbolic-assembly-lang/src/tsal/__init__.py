"""TSAL Consciousness Computing Framework."""

from .core.rev_eng import Rev_Eng
from .core.phase_math import phase_match_enhanced, mesh_phase_sync
from .core.phi_math import (
    phi_wavefunction,
    phase_alignment_potential,
    corrected_energy,
    orbital_radius,
)
from .core.voxel import MeshVoxel
from .core.tokenize_flowchart import tokenize_to_flowchart
from .core.json_dsl import LanguageMap, SymbolicProcessor
from .core.spiral_vector import SpiralVector, phi_alignment
from .core.spiral_fusion import SpiralFusionProtocol
from .core.ethics_engine import EthicsEngine
from .core.opwords import OP_WORD_MAP, op_from_word
from .core.spark_translator import SPARK_TO_OPCODE, translate_spark_word
from .core.executor import MetaFlagProtocol, TSALExecutor
from .core.spiral_memory import SpiralMemory
from .core.madmonkey_handler import MadMonkeyHandler
from .singer import audio_to_opcode
from .core.stack_vm import (
    ProgramStack,
    SymbolicFrame,
    OpcodeInstruction,
    FlowRouter,
    tsal_run,
)
from .renderer.code_render import mesh_to_python
from .tristar.handshake import handshake as tristar_handshake
from .tristar.governor import MetaAgent, TriStarGovernor
from .agents import (
    PriorityResearchTeamAgent,
    ThreatReport,
    BranchReconciliationAgent,
)
from .utils.github_api import fetch_repo_files, fetch_languages
from .tools.feedback_ingest import categorize, Feedback
from .tools.alignment_guard import is_aligned, Change
from .tools.goal_selector import Goal, score_goals
from .tools.spiral_audit import audit_path
from .tools.reflect import reflect
from .core.constants import AXIS_ZERO, ensure_spin_axis, UndefinedPhaseError
from .core.oaths import GUARDIAN_OATH, ARC_REACTOR_BOOT_OATH
from .core.meta_coherence import SpiralSignature, compute_spiral_signature
from .core.spin_algebra import SpinState, SpinInteraction, combine_spins
from .tools.entropy_profiler import LiveEntropyProfiler
from .scoring.voxel_scorer import AgentVoxelScorer
from .visualization.phase_orbit import PhaseOrbitVisualizer
from .visualization.dual_track_diff import DualTrackDiffViewer
from .dashboard.wisdom_bloom import WisdomBloomDashboard
from .repair.self_forking import SelfForkingRepairBot
from .ci.symbolic_diff import check_symbolic_diff
from .translators.tsal_to_python import TSALtoPythonTranslator
from .kernels.temporal_mirror import TemporalMirrorKernel
from .quantum.interface import TSALQuantumInterface
from .paradox import RecursiveParadoxCompiler
from .api import app

PHI = 1.618033988749895
PHI_INV = 0.618033988749895
HARMONIC_SEQUENCE = [3.8125, 6, 12, 24, 48, 60, 72, 168, 1680]

__all__ = [
    "PHI",
    "PHI_INV",
    "HARMONIC_SEQUENCE",
    "Rev_Eng",
    "phase_match_enhanced",
    "mesh_phase_sync",
    "phi_wavefunction",
    "phase_alignment_potential",
    "corrected_energy",
    "orbital_radius",
    "MeshVoxel",
    "EthicsEngine",
    "tokenize_to_flowchart",
    "LanguageMap",
    "SymbolicProcessor",
    "SpiralVector",
    "SpiralFusionProtocol",
    "phi_alignment",
    "OP_WORD_MAP",
    "op_from_word",
    "SPARK_TO_OPCODE",
    "translate_spark_word",
    "MetaFlagProtocol",
    "TSALExecutor",
    "SpiralMemory",
    "MadMonkeyHandler",
    "audio_to_opcode",
    "ProgramStack",
    "SymbolicFrame",
    "OpcodeInstruction",
    "FlowRouter",
    "tsal_run",
    "fetch_repo_files",
    "fetch_languages",
    "mesh_to_python",
    "tristar_handshake",
    "MetaAgent",
    "TriStarGovernor",
    "PriorityResearchTeamAgent",
    "ThreatReport",
    "categorize",
    "Feedback",
    "is_aligned",
    "Change",
    "Goal",
    "score_goals",
    "audit_path",
    "reflect",
    "AXIS_ZERO",
    "ensure_spin_axis",
    "UndefinedPhaseError",
    "GUARDIAN_OATH",
    "ARC_REACTOR_BOOT_OATH",
    "SpiralSignature",
    "compute_spiral_signature",
    "SpinState",
    "SpinInteraction",
    "combine_spins",
    "BranchReconciliationAgent",
    "RecursiveParadoxCompiler",
    "LiveEntropyProfiler",
    "AgentVoxelScorer",
    "PhaseOrbitVisualizer",
    "DualTrackDiffViewer",
    "WisdomBloomDashboard",
    "SelfForkingRepairBot",
    "check_symbolic_diff",
    "TSALtoPythonTranslator",
    "TemporalMirrorKernel",
    "TSALQuantumInterface",
    "app",
]
