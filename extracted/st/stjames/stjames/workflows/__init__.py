# ruff: noqa: F405

from typing import Literal

from .admet import *
from .basic_calculation import *
from .batch_docking import *
from .batch_protein_cofolding import *
from .bde import *
from .binding_affinity import *
from .conformer import *
from .conformer_search import *
from .covalent_inhibitor_scan import *
from .descriptors import *
from .docking import *
from .double_ended_ts_search import DoubleEndedTSSearchWorkflow
from .electronic_properties import *
from .fukui import *
from .hydrogen_bond_basicity import *
from .interaction_energy_decomposition import (
    EnergyDecompositionMethod,
    EnergyDecompositionSettings,
    InteractionEnergyDecompositionWorkflow,
    SAPT0Result,
)
from .ion_mobility import *
from .irc import *
from .ligand_parameterization import LigandParameterizationWorkflow
from .logp import *
from .macropka import *
from .membrane_permeability import *
from .molecular_dynamics import *
from .msa import *
from .multistage_opt import *
from .nmr import *
from .phonons import *
from .pka import *
from .pocket_detection import Pocket, PocketDetectionWorkflow
from .protein_binder_design import *
from .protein_cofolding import *
from .protein_md import *
from .protein_preparation import *
from .redox_potential import *
from .relative_binding_free_energy_perturbation import (
    ChargeMethod,
    RBFEEdgeTopology,
    RBFEGraphWorkflow,
    RBFEReceptorAnchorAtom,
    RBFESeparatedTopologyAnchors,
    RBFESeparatedTopologyMetadata,
    RBFESeparatedTopologyTetherAtoms,
    RelativeBindingFreeEnergyPerturbationWorkflow,
    TMDRBFESettings,
    TMDSeparatedTopologyAnchorEquilibrationSettings,
    TMDSeparatedTopologyRestraintSettings,
    TMDSeparatedTopologySettings,
)
from .scan import *
from .solubility import *
from .solvent_dependent_conformers import *
from .spin_states import *
from .strain import *
from .surface_energy import *
from .tautomer import *
from .workflow import *

WORKFLOW_NAME = Literal[
    "admet",
    "analogue_docking",
    "basic_calculation",
    "batch_docking",
    "batch_protein_cofolding",
    "bde",
    "binding_affinity",
    "membrane_permeability",
    "conformers",
    "conformer_search",
    "covalent_inhibitor_scan",
    "descriptors",
    "docking",
    "double_ended_ts_search",
    "electronic_properties",
    "relative_binding_free_energy_perturbation",
    "fukui",
    "hydrogen_bond_basicity",
    "interaction_energy_decomposition",
    "ion_mobility",
    "irc",
    "logp",
    "ligand_parameterization",
    "macropka",
    "molecular_dynamics",
    "msa",
    "multistage_opt",
    "nmr",
    "phonons",
    "pka",
    "pocket_detection",
    "pose_analysis_md",
    "protein_cofolding",
    "protein_binder_design",
    "protein_md",
    "protein_preparation",
    "rbfe_graph",
    "redox_potential",
    "scan",
    "solubility",
    "solvent_dependent_conformers",
    "spin_states",
    "strain",
    "surface_energy",
    "tautomers",
]

WORKFLOW_MAPPING: dict[WORKFLOW_NAME, type[Workflow]] = {
    "admet": ADMETWorkflow,
    "analogue_docking": AnalogueDockingWorkflow,
    "basic_calculation": BasicCalculationWorkflow,
    "batch_docking": BatchDockingWorkflow,
    "batch_protein_cofolding": BatchProteinCofoldingWorkflow,
    "bde": BDEWorkflow,
    "binding_affinity": BindingAffinityWorkflow,
    "membrane_permeability": MembranePermeabilityWorkflow,
    "conformers": ConformerWorkflow,
    "conformer_search": ConformerSearchWorkflow,
    "covalent_inhibitor_scan": CovalentInhibitorScanWorkflow,
    "descriptors": DescriptorsWorkflow,
    "docking": DockingWorkflow,
    "double_ended_ts_search": DoubleEndedTSSearchWorkflow,
    "electronic_properties": ElectronicPropertiesWorkflow,
    "fukui": FukuiIndexWorkflow,
    "hydrogen_bond_basicity": HydrogenBondBasicityWorkflow,
    "interaction_energy_decomposition": InteractionEnergyDecompositionWorkflow,
    "ion_mobility": IonMobilityWorkflow,
    "irc": IRCWorkflow,
    "logp": LogPWorkflow,
    "ligand_parameterization": LigandParameterizationWorkflow,
    "macropka": MacropKaWorkflow,
    "molecular_dynamics": MolecularDynamicsWorkflow,
    "multistage_opt": MultiStageOptWorkflow,
    "msa": MSAWorkflow,
    "nmr": NMRSpectroscopyWorkflow,
    "phonons": PhononWorkflow,
    "pka": pKaWorkflow,
    "pocket_detection": PocketDetectionWorkflow,
    "pose_analysis_md": PoseAnalysisMolecularDynamicsWorkflow,
    "protein_cofolding": ProteinCofoldingWorkflow,
    "protein_binder_design": ProteinBinderDesignWorkflow,
    "protein_md": ProteinMolecularDynamicsWorkflow,
    "protein_preparation": ProteinPreparationWorkflow,
    "rbfe_graph": RBFEGraphWorkflow,
    "redox_potential": RedoxPotentialWorkflow,
    "relative_binding_free_energy_perturbation": RelativeBindingFreeEnergyPerturbationWorkflow,
    "scan": ScanWorkflow,
    "solubility": SolubilityWorkflow,
    "solvent_dependent_conformers": SolventDependentConformersWorkflow,
    "spin_states": SpinStatesWorkflow,
    "strain": StrainWorkflow,
    "surface_energy": SurfaceEnergyWorkflow,
    "tautomers": TautomerWorkflow,
}
