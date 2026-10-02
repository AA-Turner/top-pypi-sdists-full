from typing import Annotated, Any, Self

from pydantic import AfterValidator, AliasChoices, Field, NonNegativeFloat, NonNegativeInt, PositiveFloat, PositiveInt, model_validator

from ..base import Base, UniqueList, round_float
from ..method import FFMethod, Method, ProteinForceField, WaterForceField
from ..pdb import PDB
from ..trajectory_clustering import TrajectoryClustering
from ..types import UUID, NonPolymerResidueMapping, ProteinMDTrajectory, round_list, round_vector3d
from .workflow import ProteinStructureWorkflow, SMILESWorkflow


class BindingPoseContact(Base):
    """
    A single protein–ligand contact from an MD trajectory.

    :param protein_atom_index: index of protein atom
    :param ligand_atom_index: index of ligand atom
    :param occupancy: the probability of seeing this interaction in a frame, between 0 and 1
    """

    protein_atom_index: int
    ligand_atom_index: int
    occupancy: Annotated[float, AfterValidator(round_float(3))]


class BindingPoseTrajectory(ProteinMDTrajectory):
    """
    Represents a single trajectory looking at a binding pose.

    Inherited:
    :param uuid: UUID of the DCD trajectory file in S3 storage
    :param cluster_centroid_indices: indices of frames corresponding to cluster centroids
    :param cluster_indices_by_frame: cluster that each frame belongs to
    :param isotropic_radius_of_gyration: per-frame protein Rg (all polymer chains including
        binder; excludes small molecules, waters, and solvent ions), in Å
    :param sasa: per-frame total solvent-accessible surface area of the receptor only
        (excludes binder chains, small molecules, waters, and solvent ions), in Å²
    :param polar_sasa: per-frame polar (non-H, non-C) solvent-accessible surface area of
        the receptor only (excludes binder chains, small molecules, waters, and solvent ions), in Å²
    :param protein_rmsd: per-frame all-Cα RMSD (receptor + protein binder chains), in Å
    :param rmsf: per-Cα RMSF (receptor + protein binder chains), in Å
    :param potential_energy: potential energy per frame, in Hartree
    :param mean_structure_uuid: UUID of saved PDB for coordinate-averaged (mean) structure
    :param median_structure_frame_index: index of medoid frame (minimum total RMSD to all other frames)

    New:
    :param binder_rmsd: per-frame binder RMSD vs starting pose, in Å; populated only when
        the binder is a single component (one small molecule → heavy-atom RMSD; one
        binder chain → backbone N/CA/C/O RMSD). Empty for protein-only, multi-molecule,
        multi-chain, or combined chain+molecule binders
    :param contacts: currently always empty
    :param mmgbsa_scores: per-frame MM/GBSA binding-side interaction energy in kcal/mol
        (receptor vs the entire binder side); length n_frames; None at unsampled frames,
        float at analysis_interval_ps-strided frames; empty if analysis not requested
    """

    binder_rmsd: Annotated[list[NonNegativeFloat], AfterValidator(round_list(3))] = Field(
        default=[], validation_alias=AliasChoices("binder_rmsd", "ligand_rmsd")
    )
    contacts: list[BindingPoseContact] = []
    mmgbsa_scores: Annotated[list[float | None], AfterValidator(round_list(3))] = []


class HydrationBridgeResidue(Base):
    """
    Protein residue participating in a water bridge at a hydration site.

    :param residue_index: 0-based index of residue in the protein structure
    :param bridge_occ: fraction of frames in which this residue forms a water bridge, between 0 and 1
    """

    residue_index: NonNegativeInt
    bridge_occ: Annotated[float, AfterValidator(round_float(3))]


class HydrationSite(Base):
    """
    Hydration site with occupancy and water-mediated interaction statistics.

    :param centroid: position of site centroid, in Å
    :param abs_occ: fraction of frames in which a water occupies the site, between 0 and 1
    :param num_unique_waters: number of distinct water molecules ever occupying the site; None if not computed
    :param bridge_abs_occ: fraction of frames in which the site water bridges binder and receptor
    :param binder_only_abs_occ: fraction of frames in which the site water contacts only the binder
    :param prot_only_abs_occ: fraction of frames in which the site water contacts only the receptor
    :param bridge_residues: protein residues involved in water bridges, sorted by descending bridge_occ
    """

    centroid: Annotated[tuple[float, float, float], AfterValidator(round_vector3d(3))]
    abs_occ: Annotated[float, AfterValidator(round_float(3))]
    num_unique_waters: PositiveInt | None = None
    bridge_abs_occ: Annotated[float, AfterValidator(round_float(3))] = 0.0
    binder_only_abs_occ: Annotated[float, AfterValidator(round_float(3))] = Field(
        default=0.0, validation_alias=AliasChoices("binder_only_abs_occ", "lig_only_abs_occ")
    )
    prot_only_abs_occ: Annotated[float, AfterValidator(round_float(3))] = 0.0
    bridge_residues: list[HydrationBridgeResidue] = []


class Binder(Base):
    """
    Specification of the binder within a protein complex.

    A binder may consist of protein/peptide chains, small molecules, or both together.
    At least one of chain_ids or small_molecule_residues must be set.

    :param chain_ids: chain IDs of the protein/peptide binder chains within the complex
    :param small_molecule_residues: residue names or 0-based non-polymer residue indices
        identifying which small molecules are part of the binder
    """

    chain_ids: UniqueList[str] | None = None
    small_molecule_residues: UniqueList[str | NonNegativeInt] | None = None

    @model_validator(mode="after")
    def validate_components(self) -> Self:
        """
        Confirm at least one component is specified.

        :raises ValueError: if neither chain_ids nor small_molecule_residues is set
        """
        if self.chain_ids is None and self.small_molecule_residues is None:
            raise ValueError("at least one of chain_ids or small_molecule_residues must be set")
        return self


class ProteinMDSettingsMixin(Base):
    """
    Mix-in for various settings used in running protein MD.

    :param small_molecule_ff: forcefield used for small molecules
    :param protein_ff: forcefield used for proteins
    :param water_ff: forcefield used for water and ions
    :param equilibration_time_ns: how long to equilibrate trajectories for, in ns
    :param simulation_time_ns: how long to run trajectories for, in ns
    :param temperature: temperature, in K
    :param pressure_atm: pressure, in atm
    :param langevin_timescale_ps: timescale for the Langevin integrator, in ps⁻¹
    :param timestep_fs: timestep, in femtoseconds
    :param hydrogen_mass: mass of hydrogen atoms, in amu
    :param constrain_hydrogens: whether or not to use SHAKE to freeze bonds to hydrogen
    :param nonbonded_cutoff: nonbonded cutoff for particle-mesh Ewald, in Å
    :param ionic_strength_M: ionic strength of the solution, in M (molar)
    :param water_buffer: amount of water to add around the protein, in Å
    :param frame_save_interval_ps: how often to save frames to the trajectory, in ps
    :param clustering: clustering method and parameters; `None` disables clustering
    :param analysis_interval_ps: interval between frames at which to compute expensive per-frame
        quantities (SASA, polar SASA), in ps; `None` disables those analyses
    """

    small_molecule_ff: FFMethod = Method.OFF_SAGE_2_3_0
    protein_ff: ProteinForceField = ProteinForceField.FF14SB
    water_ff: WaterForceField = WaterForceField.TIP3P

    equilibration_time_ns: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 0.5
    simulation_time_ns: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 10

    temperature: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 300
    pressure_atm: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 1.0
    langevin_timescale_ps: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 1.0

    timestep_fs: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 4
    hydrogen_mass: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 3
    constrain_hydrogens: bool = True
    nonbonded_cutoff: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 8.0

    ionic_strength_M: Annotated[NonNegativeFloat, AfterValidator(round_float(3))] = 0.0
    water_buffer: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 8.0

    frame_save_interval_ps: Annotated[PositiveFloat, AfterValidator(round_float(1))] = 10.0

    clustering: TrajectoryClustering | None = None
    analysis_interval_ps: PositiveFloat | None = None

    @model_validator(mode="after")
    def validate_frame_save_interval(self) -> Self:
        """Confirm frame_save_interval_ps is an integer multiple of timestep_fs."""
        interval_fs = round(self.frame_save_interval_ps * 1000)
        if interval_fs % self.timestep_fs != 0:
            raise ValueError(f"frame_save_interval_ps ({self.frame_save_interval_ps} ps) must be an integer multiple of timestep_fs ({self.timestep_fs} fs)")
        return self


class ProteinMolecularDynamicsWorkflow(ProteinMDSettingsMixin, ProteinStructureWorkflow):
    """
    Protein molecular dynamics workflow.

    Inherited:
    :param protein: PDB or UUID of the (holo) protein.
    :param equilibration_time_ns: how long to equilibrate trajectories for, in ns
    :param simulation_time_ns: how long to run trajectories for, in ns
    :param temperature: temperature, in K
    :param pressure_atm: pressure, in atm
    :param langevin_timescale_ps: timescale for Langevin integrator, in ps⁻¹
    :param timestep_fs: timestep, in femtoseconds
    :param constrain_hydrogens: whether to use SHAKE to freeze bonds to hydrogen
    :param nonbonded_cutoff: nonbonded cutoff for particle-mesh Ewald, in Å
    :param ionic_strength_M: ionic strength of solution, in M (molar)
    :param water_buffer: amount of water to add around protein, in Å
    :param frame_save_interval_ps: how often to save frames to the trajectory, in ps
    :param clustering: clustering method and parameters; `None` disables clustering
    :param analysis_interval_ps: interval between frames at which to compute expensive per-frame
        quantities (SASA, polar SASA), in ps; `None` disables those analyses

    New:
    :param num_trajectories: number of trajectories to run
    :param save_solvent: whether solvent should be saved
    :param num_solvent_to_save: saves this many solvent molecules nearest the binder, or all if None;
        only meaningful when save_solvent is True and a binder is present
    :param small_molecules: small molecules requiring force-field parameterization, keyed by
        residue name or 0-based residue index; values are SMILES strings, or None for known
        ions and structural waters; residues in `binder.small_molecule_residues` are the binder,
        all others are cofactors
    :param binder: optional binder specification; when set, per-frame binder RMSD (aligned on
        receptor Cα) and MM/GBSA scores are computed; contacts and hydration sites are populated
        only when `small_molecule_residues` is set on the binder
    :param protein_restraint_cutoff: cutoff distance from the binder past which
        Cα atoms are harmonically restrained, in Å; None disables restraints
    :param protein_restraint_constant: force constant for Cα backbone restraints, in kcal/mol/Å²

    Results:
    :param minimized_protein_uuid: UUID of final system PDB
    :param bonds: which atoms are bonded to which other atoms
    :param trajectories: UUID and analysis results per replicate; `protein_rmsd` and `rmsf`
        cover all protein Cα (receptor + binder chains); `binder_rmsd` holds per-frame binder
        RMSD only when the binder is a single component (one small molecule → heavy atoms;
        one binder chain → backbone N/CA/C/O); `mmgbsa_scores` holds MM/GBSA scores when a
        binder is present; `contacts` is currently never populated.
    :param hydration_sites: hydration sites aggregated across all replicates; populated only when
        a small-molecule binder is present
    """

    num_trajectories: PositiveInt = 1
    save_solvent: bool = False
    num_solvent_to_save: PositiveInt | None = None

    small_molecules: NonPolymerResidueMapping | None = None
    binder: Binder | None = None

    protein_restraint_cutoff: Annotated[PositiveFloat, AfterValidator(round_float(3))] | None = None
    protein_restraint_constant: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 100

    minimized_protein_uuid: UUID | None = None
    bonds: list[tuple[int, int]] = []
    trajectories: list[BindingPoseTrajectory] = []
    hydration_sites: list[HydrationSite] = []

    @model_validator(mode="after")
    def validate_binder(self) -> Self:
        """
        Validate binder chain IDs against the inlined PDB when available.

        :raises ValueError: if any chain_ids entry is absent from the first model of the PDB
        :raises ValueError: if chain_ids covers every polymer chain, leaving no receptor

        Note: chain-existence check is skipped when `protein` is a UUID; the runner
        re-validates after resolution.
        """
        if self.binder is None or not self.binder.chain_ids:
            return self
        if not isinstance(self.protein, PDB):
            return self
        if not self.protein.models:
            raise ValueError("PDB has no models; cannot validate binder chain_ids")
        chains = self.protein.models[0].polymer
        missing = [c for c in self.binder.chain_ids if c not in chains]
        if missing:
            raise ValueError(f"binder chain_ids {missing!r} not found in PDB (available chains: {sorted(chains.keys())})")
        if set(self.binder.chain_ids) >= set(chains):
            raise ValueError(f"binder chain_ids covers every polymer chain ({sorted(chains.keys())}); no receptor would remain")
        return self


class PoseAnalysisMolecularDynamicsWorkflow(ProteinMDSettingsMixin, ProteinStructureWorkflow, SMILESWorkflow):
    """
    Pose-analysis molecular dynamics workflow.

    Inherited:
    :param initial_smiles: ligand's SMILES
    :param protein: PDB or UUID of the (holo) protein.
    :param equilibration_time_ns: how long to equilibrate trajectories for, in ns
    :param simulation_time_ns: how long to run trajectories for, in ns
    :param temperature: temperature, in K
    :param pressure_atm: pressure, in atm
    :param langevin_timescale_ps: timescale for the Langevin integrator, in ps⁻¹
    :param timestep_fs: timestep, in femtoseconds
    :param constrain_hydrogens: whether or not to use SHAKE to freeze bonds to hydrogen
    :param nonbonded_cutoff: nonbonded cutoff for particle-mesh Ewald, in Å
    :param ionic_strength_M: ionic strength of the solution, in M (molar)
    :param water_buffer: amount of water to add around the protein, in Å
    :param frame_save_interval_ps: how often to save frames to the trajectory, in ps
    :param clustering: clustering method and parameters; `None` disables clustering
    :param analysis_interval_ps: interval between frames at which to compute expensive per-frame
        quantities (SASA, polar SASA), in ps; `None` disables those analyses

    New:
    :param protein_uuid: UUID of the (holo) protein. DEPRECATED.
    :param ligand_residue_name: ligand's residue name
    :param num_trajectories: number of trajectories to run
    :param save_solvent: whether any solvent should be saved
    :param num_solvent_to_save: saves this many solvent molecules, or all solvent molecules if None
    :param protein_restraint_cutoff: cutoff past which alpha-carbons will be constrained, in Å
    :param protein_restraint_constant: force constant for backbone restraints, in kcal/mol/Å²

    Results:
    :param minimized_protein_uuid: UUID of final system PDB
    :param bonds: which atoms are bonded to which other atoms
    :param trajectories: for each replicate, a UUID and the corresponding analysis results
    :param hydration_sites: hydration sites aggregated across all replicates, with occupancy and H-bond statistics
    """

    protein_uuid: UUID | None = None
    ligand_residue_name: str = "LIG"

    num_trajectories: PositiveInt = 1
    save_solvent: bool = False
    num_solvent_to_save: PositiveInt | None = None

    protein_restraint_cutoff: Annotated[PositiveFloat, AfterValidator(round_float(3))] | None = None
    protein_restraint_constant: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 100

    minimized_protein_uuid: UUID | None = None
    bonds: list[tuple[int, int]] = []
    trajectories: list[BindingPoseTrajectory] = []
    hydration_sites: list[HydrationSite] = []

    @model_validator(mode="before")
    def harmonize_protein_uuid(cls, data: Any) -> Any:  # noqa: N805
        """
        Syncs data between "protein_uuid" and "protein" field.
        """
        if "protein_uuid" in data:
            data["protein"] = data["protein_uuid"]

        return data
