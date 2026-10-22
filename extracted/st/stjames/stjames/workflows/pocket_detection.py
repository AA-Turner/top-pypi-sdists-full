"""Define protein pocket detection settings and results."""

from math import isclose
from typing import Annotated, Any, Literal, Self

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, NonNegativeFloat, NonNegativeInt, PositiveFloat, model_validator

from ..base import Base, round_float
from ..method import Method
from ..solvent import Solvent
from ..types import UUID, ProteinUUID, Vector3D
from .protein_md import ProteinMDSimulationSettings
from .workflow import ProteinStructureWorkflow


class PocketeerSettings(BaseModel):
    """Configure geometric pocket detection.

    Attributes:
        merge_distance: distance for merging pocket spheres, in Å
    """

    settings_type: Literal["pocketeer"] = "pocketeer"
    merge_distance: Annotated[NonNegativeFloat, AfterValidator(round_float(3))] = 1.75


class MixMDSettings(ProteinMDSimulationSettings):
    """Configure unbiased mixed-solvent screening for probe-enriched pockets.

    Inherits force fields and simulation controls from `ProteinMDSimulationSettings`.

    Attributes:
        probe: neutral cosolvent species
        probe_volume_fraction: nominal probe fraction by liquid volume
        num_trajectories: number of independently prepared replicas
        grid_spacing: occupancy grid spacing, in Å
        enrichment_threshold: minimum density relative to bulk solvent
        min_cluster_volume: minimum enriched cluster volume, in Å³
        surface_distance: maximum protein distance for pocket voxels, in Å

    Overridden attributes:
        small_molecule_ff: Sage force field for probes; molecule-specific Mango parameters are unsupported
        simulation_time_ns: production duration per replica, in ns
        equilibration_time_ns: equilibration duration per replica, in ns
        temperature: thermostat temperature between 250 and 350 K
        ionic_strength_M: salt concentration, in M
        water_buffer: solvent padding of at least 10 Å
        timestep_fs: integration timestep of at most 2 fs
        hydrogen_mass: hydrogen mass, defaulting to 1.008 amu
        frame_save_interval_ps: interval between saved frames, in ps
        analysis_interval_ps: interval between analyzed frames, in ps; `None` analyzes every saved frame
    """

    model_config = ConfigDict(allow_inf_nan=False)

    settings_type: Literal["mixmd"] = "mixmd"
    small_molecule_ff: Literal[Method.OFF_SAGE_2_0_0, Method.OFF_SAGE_2_2_1, Method.OFF_SAGE_2_3_0] = Method.OFF_SAGE_2_3_0
    probe: Literal[Solvent.ACETONITRILE, Solvent.ISOPROPANOL] = Solvent.ACETONITRILE
    probe_volume_fraction: Annotated[float, Field(gt=0, le=0.1)] = 0.05
    num_trajectories: Annotated[int, Field(ge=1, le=20)] = 3
    simulation_time_ns: PositiveFloat = 15
    equilibration_time_ns: PositiveFloat = 5
    temperature: Annotated[float, Field(ge=250, le=350)] = 300
    ionic_strength_M: NonNegativeFloat = 0.15
    water_buffer: Annotated[float, Field(ge=10)] = 15
    timestep_fs: Annotated[float, Field(gt=0, le=2)] = 2
    hydrogen_mass: PositiveFloat = 1.008
    frame_save_interval_ps: PositiveFloat = 10
    grid_spacing: PositiveFloat = 0.5
    enrichment_threshold: Annotated[float, Field(gt=1)] = 5
    min_cluster_volume: PositiveFloat = 8
    surface_distance: PositiveFloat = 5

    @model_validator(mode="after")
    def validate_analysis_window(self) -> Self:
        """Require a saved-frame analysis cadence and at least two sampled frames."""
        interval = self.analysis_interval_ps or self.frame_save_interval_ps
        stride = interval / self.frame_save_interval_ps
        if interval < self.frame_save_interval_ps or not isclose(stride, round(stride)):
            raise ValueError("analysis_interval_ps must be a positive integer multiple of frame_save_interval_ps")
        if 2 * interval > 1000 * self.simulation_time_ns:
            raise ValueError("analysis window must contain at least two sampled frames")
        if self.frame_save_interval_ps * 1000 < self.timestep_fs:
            raise ValueError("frame_save_interval_ps must be at least one integration timestep")
        return self


PocketDetectionSettings = Annotated[PocketeerSettings | MixMDSettings, Field(discriminator="settings_type")]


class MixMDPocketDiagnostics(Base):
    """Describe probe enrichment for one pocket.

    Attributes:
        density_center: density-weighted position, in Å
        peak_enrichment: maximum voxel density relative to bulk solvent
        integrated_excess_density: excess probe count integrated over the pocket
    """

    density_center: Vector3D
    peak_enrichment: NonNegativeFloat
    integrated_excess_density: NonNegativeFloat


class MixMDReplicaDiagnostics(Base):
    """Record replica sampling, solvent quality, and stored artifacts.

    Attributes:
        index: zero-based replica index
        seed: replica random seed
        num_frames: analyzed frames
        num_probes: probe molecules in the simulation
        largest_probe_cluster_fraction: mean fraction of probes in the largest cluster
        trajectory_uuid: stored probe-containing trajectory
        topology_uuid: stored trajectory topology
        density_map_uuid: stored probe number-density map
    """

    index: NonNegativeInt
    seed: NonNegativeInt
    num_frames: NonNegativeInt = 0
    num_probes: NonNegativeInt = 0
    largest_probe_cluster_fraction: Annotated[float, Field(ge=0, le=1)] | None = None
    trajectory_uuid: UUID | None = None
    topology_uuid: ProteinUUID | None = None
    density_map_uuid: UUID | None = None


class MixMDResults(Base):
    """Store consensus maps, aligned reference, and replica diagnostics.

    Attributes:
        reference_uuid: protein reference defining pocket and map coordinates
        density_map_uuid: equally weighted consensus number-density map, in Å⁻³
        replicas: replica results, including failures
    """

    reference_uuid: ProteinUUID | None = None
    density_map_uuid: UUID | None = None
    replicas: list[MixMDReplicaDiagnostics] = []


class Pocket(Base):
    """Represent a detected pocket.

    Attributes:
        sphere_centers: centers of detected spheres, in Å
        sphere_radii: radii of detected spheres, in Å
        volume: volume, in Å³
        score: method-specific ranking score, with larger scores preferred
        pocket_center: center of bounding box, in Å
        pocket_sides: side lengths of bounding box, in Å
        residue_numbers: indices of residues on pocket
        mixmd: probe-density and replica-consistency diagnostics
    """

    sphere_centers: list[Vector3D]
    sphere_radii: list[float]
    volume: Annotated[float, AfterValidator(round_float(3))]
    score: Annotated[float, AfterValidator(round_float(3))]
    pocket_center: Vector3D
    pocket_sides: Vector3D
    residue_numbers: list[NonNegativeInt]
    mixmd: MixMDPocketDiagnostics | None = None


class PocketDetectionWorkflow(ProteinStructureWorkflow):
    """Detect potential binding sites geometrically or with cosolvent MD.

    The inherited `protein` supplies the prepared structure.

    Attributes:
        settings: pocket detection method and parameters
        merge_distance: deprecated Pocketeer sphere-merging distance, in Å
        pockets: detected pockets in descending score order
        mixmd: maps and replica diagnostics
    """

    settings: PocketDetectionSettings = PocketeerSettings()
    merge_distance: Annotated[float, AfterValidator(round_float(3))] = Field(default=1.75, deprecated=True)
    pockets: list[Pocket] = []
    mixmd: MixMDResults | None = None

    @model_validator(mode="before")
    @classmethod
    def migrate_merge_distance(cls, data: Any) -> Any:
        """Use legacy merge distance when Pocketeer settings leave it unspecified."""
        if not isinstance(data, dict) or "merge_distance" not in data:
            return data
        settings = data.get("settings", {"settings_type": "pocketeer"})
        if isinstance(settings, PocketeerSettings):
            settings = settings.model_dump(exclude_unset=True) | {"settings_type": "pocketeer"}
        if isinstance(settings, dict) and settings.get("settings_type") == "pocketeer":
            return data | {"settings": {"merge_distance": data["merge_distance"]} | settings}
        return data
