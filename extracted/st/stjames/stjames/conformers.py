"""Define conformer generation and clustering settings."""

from abc import ABC
from typing import Annotated, Literal, Self, Sequence

from pydantic import AfterValidator, BaseModel, Field, NonNegativeFloat, PositiveFloat, PositiveInt, field_validator, model_validator

from .base import LowercaseStrEnum, round_float, round_optional_float
from .constraint import Constraint
from .method import Method, XTBMethod
from .mode import Mode
from .settings import Settings
from .solvent import SolventModel, SolventSettings
from .types import FloatPerAtom, round_list, round_optional_float_per_atom
from .workflows.multistage_opt import MultiStageOptMixin


class ConformerProperties(BaseModel):
    """Properties of a conformer or of a population-weighted conformer ensemble.

    Attributes:
        solvent_accessible_surface_area: SASA (Å²); ensemble: averaged
        polar_solvent_accessible_surface_area: SASA of non-C/H atoms (Å²); ensemble: averaged
        radius_of_gyration: radius of gyration (Å); ensemble: averaged
        dipole: dipole magnitude about the center of mass (Debye); ensemble: root-mean-square
        mulliken_charges: partial atomic charges (e); ensemble only: averaged per atom
        excitation_energies: excitation energies (Hartree); ensemble only: every conformer's, unweighted
        oscillator_strengths: oscillator strengths, parallel to `excitation_energies`; ensemble only: each weighted
        rotatory_strengths: ECD rotatory strengths (10⁻⁴⁰ esu²·cm²), parallel to `excitation_energies`; ensemble only: each weighted
        vibrational_frequencies: real vibrational frequencies (cm⁻¹); ensemble only: every conformer's, unweighted
        ir_intensities: IR intensities (km/mol), parallel to `vibrational_frequencies`; ensemble only: each weighted
    """

    solvent_accessible_surface_area: Annotated[PositiveFloat | None, AfterValidator(round_optional_float(3))] = None
    polar_solvent_accessible_surface_area: Annotated[NonNegativeFloat | None, AfterValidator(round_optional_float(3))] = None
    radius_of_gyration: Annotated[PositiveFloat | None, AfterValidator(round_optional_float(3))] = None
    dipole: Annotated[NonNegativeFloat | None, AfterValidator(round_optional_float(3))] = None
    mulliken_charges: Annotated[FloatPerAtom | None, AfterValidator(round_optional_float_per_atom(6))] = None

    excitation_energies: Annotated[list[float] | None, AfterValidator(round_list(6))] = None
    oscillator_strengths: Annotated[list[float] | None, AfterValidator(round_list(6))] = None
    rotatory_strengths: Annotated[list[float] | None, AfterValidator(round_list(4))] = None

    vibrational_frequencies: Annotated[list[float] | None, AfterValidator(round_list(3))] = None
    ir_intensities: Annotated[list[float] | None, AfterValidator(round_list(3))] = None

    @model_validator(mode="after")
    def check_spectrum_lengths(self) -> Self:
        """Require spectral intensities to be parallel to their line positions.

        Raises:
            ValueError: intensities lack positions or differ from them in length
        """
        spectra = {
            "excitation_energies": (
                self.excitation_energies,
                {"oscillator_strengths": self.oscillator_strengths, "rotatory_strengths": self.rotatory_strengths},
            ),
            "vibrational_frequencies": (self.vibrational_frequencies, {"ir_intensities": self.ir_intensities}),
        }
        for positions_name, (positions, intensities) in spectra.items():
            for name, values in intensities.items():
                if values is None:
                    continue
                if positions is None:
                    raise ValueError(f"{name} requires {positions_name}")
                if len(values) != len(positions):
                    raise ValueError(f"{positions_name} ({len(positions)}) and {name} ({len(values)}) must have the same length")

        return self


class ConformerClusteringDescriptor(LowercaseStrEnum):
    """Potential descriptors to employ in conformer clustering."""

    SOLVENT_ACCESSIBLE_SURFACE_AREA = "solvent_accessible_surface_area"
    POLAR_SOLVENT_ACCESSIBLE_SURACE_AREA = "polar_solvent_accessible_surface_area"
    RADIUS_OF_GYRATION = "radius_of_gyration"
    PLANE_OF_BEST_FIT = "plane_of_best_fit"
    NORMALIZED_PRINCIPAL_MOMENT_RATIO_1 = "normalized_principal_moment_ratio_1"
    NORMALIZED_PRINCIPAL_MOMENT_RATIO_2 = "normalized_principal_moment_ratio_2"


class ConformerClusteringSettings(BaseModel):
    """Settings for clustering conformers based on their three-dimensional properties.

    The properties used for clustering by default are:
    - Solvent-accessible surface area
    - Polar solvent-accessible surface area
    - Radius of gyration
    - Plane of best fit
    - Normalized principal moment ratios 1 and 2

    Rowan uses k-means clustering to identify representative conformers.
    This loosely follows Wilcken and co-workers (10.1007/s10822-020-00337-7).

    Attributes:
        num_clusters: number of clusters to include
        conformers_per_cluster: number of conformers to pick from each cluster
        descriptors: conformer properties used for clustering
    """

    descriptors: list[ConformerClusteringDescriptor] = [
        ConformerClusteringDescriptor.SOLVENT_ACCESSIBLE_SURFACE_AREA,
        ConformerClusteringDescriptor.POLAR_SOLVENT_ACCESSIBLE_SURACE_AREA,
        ConformerClusteringDescriptor.RADIUS_OF_GYRATION,
        ConformerClusteringDescriptor.PLANE_OF_BEST_FIT,
        ConformerClusteringDescriptor.NORMALIZED_PRINCIPAL_MOMENT_RATIO_1,
        ConformerClusteringDescriptor.NORMALIZED_PRINCIPAL_MOMENT_RATIO_2,
    ]

    num_clusters: PositiveInt = 5
    conformers_per_cluster: PositiveInt = 3


class ConformerGenSettings(BaseModel):
    """Conformer generation settings.

    Conformers are generated and an initial screening is performed to remove duplicates and high-energy conformers.

    Attributes:
        constraints: constraints for conformer generation
        nci: add a constraining potential for non-covalent interactions
        max_confs: maximum number of conformers to keep
    """

    constraints: Sequence[Constraint] = ()
    nci: bool = False
    max_confs: PositiveInt | None = None

    def __str__(self) -> str:
        """Return a string representation of the ConformerGenSettings."""
        return repr(self)

    def __repr__(self) -> str:
        """Return a string representation of the ConformerGenSettings."""
        extra = ""
        if self.constraints:
            extra += f" constraints={len(self.constraints)}"
        if self.nci:
            extra += " nci "
        if self.max_confs:
            extra += f" max_confs={self.max_confs}"

        return f"<{type(self).__name__} {extra}>"


class ETKDGSettings(ConformerGenSettings):
    """Settings for ETKDG conformer generation.

    Attributes:
        constraints: frozen atoms, bond distances (Angstrom), angles and dihedrals
            (degrees); omitted values preserve the input geometry

        nci: add a constraining potential for non-covalent interactions (not supported in ETKDG)
        max_confs: maximum number of conformers to keep

        num_initial_confs: number of initial conformers to generate
        num_confs_considered: number of conformers to consider for optimization
        max_mmff_energy: MMFF energy cutoff
        max_mmff_iterations: MMFF optimization iterations
    """

    num_initial_confs: int = 300
    num_confs_considered: int = 100
    max_mmff_iterations: int = 500
    max_mmff_energy: float | None = 30
    settings_type: Literal["etkdg"] = "etkdg"

    @field_validator("constraints")
    def check_constraints(cls, constraints: Sequence[Constraint]) -> Sequence[Constraint]:
        """Convert ETKDG constraints to an immutable sequence.

        Args:
            constraints: geometric constraints

        Returns:
            constraints as a tuple
        """
        return tuple(constraints)

    @field_validator("nci")
    def check_nci(cls, nci: bool) -> Literal[False]:
        """Reject NCI potentials for ETKDG.

        Args:
            nci: indicates that an NCI potential was requested

        Returns:
            disabled NCI setting

        Raises:
            ValueError: NCI is enabled
        """
        if nci:
            raise ValueError("ETKDG does not support NCI")

        return nci

    @classmethod
    def from_mode(cls, mode: Mode) -> Self:
        """Build ETKDG settings for an effort mode.

        Args:
            mode: effort mode to apply

        Returns:
            settings with mode-specific defaults
        """
        match mode:
            case Mode.RECKLESS:
                num_initial_confs = 200
                num_confs_considered = 50
                max_mmff_iterations = 500
                max_mmff_energy = 30
                max_confs = 20
                max_mmff_energy = 20
            case Mode.RAPID:
                num_initial_confs = 300
                num_confs_considered = 100
                max_mmff_iterations = 500
                max_mmff_energy = 30
                max_confs = 50
                max_mmff_energy = 30
            case _:
                raise NotImplementedError(f"Unsupported mode: {mode}")

        return cls(
            num_initial_confs=num_initial_confs,
            num_confs_considered=num_confs_considered,
            max_mmff_iterations=max_mmff_iterations,
            max_mmff_energy=max_mmff_energy,
            max_confs=max_confs,
        )


class iMTDSpeeds(LowercaseStrEnum):
    """Select the speed preset for iMTD conformer generation."""

    MEGAQUICK = "megaquick"
    SUPERQUICK = "superquick"
    QUICK = "quick"
    NORMAL = "normal"
    EXTENSIVE = "extensive"


class iMTDSettings(ConformerGenSettings, ABC):
    """Settings for iMTD style conformer generation.

    See https://github.com/crest-lab/crest/blob/5ca82feb2ec4df30a0129db957163c934f085952/src/choose_settings.f90#L202
    and https://github.com/crest-lab/crest/blob/5ca82feb2ec4df30a0129db957163c934f085952/src/confparse.f90#L825
    for how quick, superquick, and megaquick are defined.

    See build_imtd_setings(mode) for sensible defaults.

    Attributes:
        constraints: constraints to add
        nci: add an ellipsoide potential around the input structure
        max_confs: maximum number of conformers to keep

        mtd_method: method for the metadynamics
        mtd_runtype: algorithm used
        speed: speed of the calculations (CREST specific setting)
        reopt: re-optimize conformers (corrects for the lack of rotamer metadynamics and GC)
        free_energy_weights: calculate frequencies and re-weight based on free energies
        energy_window: energy window used, in kcal/mol (CREST specific setting). if set, overrides default from speed
        solvent_settings: solvent to use, if any
    """

    settings_type: Literal["imtd"] = "imtd"

    mtd_method: XTBMethod = Method.GFN_FF
    mtd_runtype: str = "imtd-gc"
    speed: iMTDSpeeds = iMTDSpeeds.QUICK
    reopt: bool = False
    free_energy_weights: bool = False
    energy_window: Annotated[PositiveFloat, AfterValidator(round_float(1))] | None = None
    solvent_settings: SolventSettings | None = None

    @model_validator(mode="after")
    def validate_and_build_imtdgc_settings(self) -> Self:
        """Require a supported solvent model for iMTD.

        Returns:
            validated settings

        Raises:
            ValueError: solvent model is unsupported
        """
        if self.solvent_settings and self.solvent_settings.model not in {SolventModel.ALPB, SolventModel.GBSA}:
            raise ValueError("Only ALPB or GBSA solvent models supported for iMTD conformer search!")

        return self

    @classmethod
    def from_mode(cls, mode: Mode) -> Self:
        """Settings for iMTD style conformer generation.

        RECKLESS:
            - GFN-FF//MTD(GFN-FF)
            - Megaquick
                - No GC
                - No rotamer metadynamics
                - Energy window = 5.0
                - Run scaling factor = 0.5
                - 6 MTD runs
        RAPID:
            - GFN0//MTD(GFN-FF)
            - Superquick
                - No GC
                - No rotamer metadynamics
                - Energy window = 5.0
                - Run scaling factor = 0.5
                - 6 MTD runs
        CAREFUL:
            - GFN2//MTD(GFN-FF)
            - Quick
                - GC (for iMTD-GC)
                - Rotamer metadynamics (for iMTD-GC)
                - Energy window = 5.0
                - Run scaling factor = 0.5
                - 6 MTD runs
        METICULOUS:
            - GFN2//MTD(GFN2)
            - "Normal"
                - GC (for iMTD-GC)
                - Rotamer metadynamics (for iMTD-GC)
                - Energy window = 6.0
                - Run scaling factor = 1
                - 14 MTD runs (2 with extreme values)

        Args:
            mode: effort mode to apply
        """
        match mode:
            case Mode.RECKLESS:  # GFN-FF//MTD(GFN-FF)
                mtd_method = Method.GFN_FF
                speed = iMTDSpeeds.MEGAQUICK
                reopt = True
                max_confs: int | None = 20
            case Mode.RAPID:  # GFN0//MTD(GFN-FF)
                mtd_method = Method.GFN_FF
                speed = iMTDSpeeds.SUPERQUICK
                reopt = True
                max_confs = 50
            case Mode.CAREFUL:  # GFN2//MTD(GFN-FF)
                mtd_method = Method.GFN_FF
                speed = iMTDSpeeds.QUICK
                reopt = False
                max_confs = None
            case Mode.METICULOUS:  # GFN2//MTD(GFN2)
                mtd_method = Method.GFN2_XTB
                speed = iMTDSpeeds.NORMAL
                reopt = False
                max_confs = None
            case _:
                raise NotImplementedError(f"Unsupported mode: {mode}")

        return cls(
            mtd_method=mtd_method,
            speed=speed,
            reopt=reopt,
            max_confs=max_confs,
        )


class iMTDGCSettings(iMTDSettings):
    """Configure iMTD with genetic crossing.

    Attributes:
        run_type: iMTD run type sent to the conformer generator
    """

    run_type: str = "imtdgc"


class iMTDsMTDSettings(iMTDSettings):
    """Configure iMTD with static metadynamics.

    Attributes:
        run_type: iMTD run type sent to the conformer generator
    """

    run_type: str = "imtd-smtd"


class LyrebirdSettings(ConformerGenSettings):
    """Settings for Lyrebird-based conformer generation.

    Attributes:
        constraints: constraints for conformer generation (not supported)
        nci: add a constraining potential for non-covalent interactions (not supported)
        max_confs: maximum number of conformers to keep

        num_initial_confs: number of initial conformers to generate
    """

    num_initial_confs: int = 300
    settings_type: Literal["lyrebird"] = "lyrebird"

    @field_validator("constraints")
    def check_constraints(cls, constraints: Sequence[Constraint]) -> Sequence[Constraint]:
        """Reject geometric constraints for Lyrebird.

        Args:
            constraints: geometric constraints

        Returns:
            empty constraint tuple

        Raises:
            ValueError: constraints were provided
        """
        if constraints:
            raise ValueError("Lyrebird does not support constraints")

        return tuple(constraints)

    @field_validator("nci")
    def check_nci(cls, nci: bool) -> Literal[False]:
        """Reject NCI potentials for Lyrebird.

        Args:
            nci: indicates that an NCI potential was requested

        Returns:
            disabled NCI setting

        Raises:
            ValueError: NCI is enabled
        """
        if nci:
            raise ValueError("Lyrebird does not support NCI")

        return nci


class MonteCarloMultipleMinimumSettings(ConformerGenSettings):
    """Settings for Monte-Carlo-multiple-minimum-based conformer generation.

    Default values recommended by Nick Casetti.

    Attributes:
        constraints: constraints for conformer generation (not supported)
        nci: add a constraining potential for non-covalent interactions (not supported)
        max_confs: maximum number of conformers to keep

        num_monte_carlo_iterations: number of Monte Carlo iterations to run
        rmsd_threshold: threshold to determine if MCMM output structures are identical
        energy_window: maximum energy window above the minimum-energy conformer above which to retain (kcal/mol)
        energy_settings: energy computation method for Monte Carlo steps
    """

    energy_settings: Settings = Settings(method=Method.AIMNET2_WB97MD3)

    num_monte_carlo_iterations: int = 250
    rmsd_threshold: float = 0.5
    energy_window: float = 20

    settings_type: Literal["monte_carlo_multiple_minimum"] = "monte_carlo_multiple_minimum"

    @field_validator("constraints")
    def check_constraints(cls, constraints: Sequence[Constraint]) -> Sequence[Constraint]:
        """Reject geometric constraints for Monte Carlo conformer generation.

        Args:
            constraints: geometric constraints

        Returns:
            empty constraint tuple

        Raises:
            ValueError: constraints were provided
        """
        if constraints:
            raise ValueError("MCMM does not support constraints")

        return tuple(constraints)

    @field_validator("nci")
    def check_nci(cls, nci: bool) -> Literal[False]:
        """Reject NCI potentials for Monte Carlo conformer generation.

        Args:
            nci: indicates that an NCI potential was requested

        Returns:
            disabled NCI setting

        Raises:
            ValueError: NCI is enabled
        """
        if nci:
            raise ValueError("MCMM does not support NCI")

        return nci


class OpenConfSettings(ConformerGenSettings):
    """Settings for OpenConf-based conformer generation.

    OpenConf uses a hybrid ETKDG seeding + MCMM torsion-walk exploration
    strategy with PRISM deduplication.

    Attributes:
        constraints: frozen atoms, bond distances (Angstrom), angles and dihedrals
            (degrees); omitted values preserve the input geometry

        nci: not supported
        max_confs: maximum number of conformers to return

        n_steps: number of MCMM exploration steps (primary quality/speed lever)
        energy_window_kcal: energy window for keeping conformers (kcal/mol)
        parent_strategy: how to select parent conformers for mutation
            - "softmax": energy-biased; favors low-energy basins (good for NMR/property prediction)
            - "uniform": random; maximizes diversity (good for docking)
            - "best": always mutate the lowest-energy conformer; fastest but least diverse

        final_select: how the final conformer set is selected
            - "diverse": k-means clustering on 3D shape descriptors; one conformer per cluster
            - "energy": lowest-energy conformers only (best for Boltzmann-weighted applications)

        do_final_refine: run full MMFF minimization on final set (slower but more accurate geometries)
    """

    n_steps: PositiveInt = 200
    energy_window_kcal: PositiveFloat = 10.0
    parent_strategy: Literal["softmax", "uniform", "best"] = "softmax"
    final_select: Literal["energy", "diverse"] = "diverse"
    do_final_refine: bool = True

    settings_type: Literal["openconf"] = "openconf"

    @field_validator("constraints")
    def check_constraints(cls, constraints: Sequence[Constraint]) -> Sequence[Constraint]:
        """Convert OpenConf constraints to an immutable sequence.

        Args:
            constraints: geometric constraints

        Returns:
            constraints as a tuple
        """
        return tuple(constraints)

    @field_validator("nci")
    def check_nci(cls, nci: bool) -> Literal[False]:
        """Reject NCI potentials for OpenConf.

        Args:
            nci: indicates that an NCI potential was requested

        Returns:
            disabled NCI setting

        Raises:
            ValueError: NCI is enabled
        """
        if nci:
            raise ValueError("OpenConf does not support NCI potentials")
        return nci


ConformerGenSettingsUnion = Annotated[
    ETKDGSettings | iMTDSettings | LyrebirdSettings | MonteCarloMultipleMinimumSettings | OpenConfSettings, Field(discriminator="settings_type")
]


class ConformerGenMixin(BaseModel):
    """Mixin for classes need conformer generation.

    Attributes:
        conf_gen_settings: settings for conformer generation
        max_confs: maximum number of conformers to keep
        conformer_clustering_settings: how to cluster the conformers (if at all)
    """

    conf_gen_settings: ConformerGenSettingsUnion | None
    max_confs: int | None = None

    conformer_clustering_settings: ConformerClusteringSettings | None = None


class ConformerSearchMixin(ConformerGenMixin, MultiStageOptMixin):
    """Mixin for classes need conformer search—a combination of conformer generation and optimization.

    Inherited (ConformerGenMixin):

    Attributes:
        conf_gen_settings: settings for conformer generation

    Inherited (MultiStageOptMixin):

        multistage_opt_settings: settings for the optimization
    """

    def __str__(self) -> str:
        """Return a string representation of the ConformerSearch workflow."""
        return repr(self)
