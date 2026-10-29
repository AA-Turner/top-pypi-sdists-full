"""High-throughput docking workflow."""

from typing import Annotated, Any, TypeAlias

from pydantic import AfterValidator, ConfigDict, Field, NonNegativeInt, field_validator, model_validator

from ..pdb import PDB
from ..types import UUID, Vector3D, round_list
from .docking import Score, TurboDockSettings, VinaSettings
from .workflow import BatchSMILESWorkflow, ProteinStructureWorkflow

BatchDockingSettingsUnion: TypeAlias = Annotated[VinaSettings | TurboDockSettings, Field(discriminator="settings_type")]


class BatchDockingWorkflow(BatchSMILESWorkflow, ProteinStructureWorkflow):
    """Batch docking workflow.

    Attributes:
        initial_smiles_list: list of SMILES
        protein: PDB of the protein, or the UUID of the protein.

        target: PDB of the protein, or the UUID of the protein. DEPRECATED
        pocket: center (x, y, z) and size (x, y, z) of the pocket
        docking_settings: how to run each docking calculation
        num_poses_to_save: number of top-scoring compounds whose poses are saved. Zero disables saving
        run_mmgbsa: refine the saved poses with MM/GBSA when true (at most `num_poses_to_save`
            ligands). Ignored when `num_poses_to_save` is 0

        best_scores: best score for each SMILES string
        saved_poses: saved poses per input ligand, ordered by docking rank. Each selected
            ligand has up to `docking_settings.max_poses` entries; others have empty lists
        refined_scores: best pose and validity for the top `num_poses_to_save` compounds,
            parallel to `initial_smiles_list`; `None` otherwise. `score` is always the
            original docking score; `pose` is refined and `mmgbsa_score` set only if
            MM/GBSA succeeded, raw docked pose and `mmgbsa_score=None` otherwise
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    target: PDB | UUID
    pocket: tuple[Vector3D, Vector3D]

    docking_settings: BatchDockingSettingsUnion = VinaSettings()
    num_poses_to_save: NonNegativeInt = 0
    run_mmgbsa: bool = False

    best_scores: Annotated[list[float | None], AfterValidator(round_list(3))] = []
    refined_scores: list[Score | None] = []
    saved_poses: list[list[Score]] = []

    @model_validator(mode="before")
    def harmonize_target_and_protein(cls, data: Any) -> Any:  # noqa: N805
        """Syncs data between "target" and "protein" field.

        Args:
            data: input model data to normalize
        """
        protein = data.get("protein")
        target = data.get("target")

        if target and not protein:
            data["protein"] = target
        elif not target and protein:
            data["target"] = protein

        return data

    @field_validator("pocket", mode="after")
    def validate_pocket(cls, pocket: tuple[Vector3D, Vector3D]) -> tuple[Vector3D, Vector3D]:
        """Require positive pocket dimensions.

        Args:
            pocket: pocket center and dimensions

        Returns:
            validated pocket

        Raises:
            ValueError: any pocket dimension is nonpositive
        """
        _center, size = pocket
        if any(q <= 0 for q in size):
            raise ValueError(f"Pocket size must be positive, got: {size}")
        return pocket

    @field_validator("docking_settings", mode="before")
    @classmethod
    def default_docking_settings_type(cls, value: Any) -> Any:
        """Treat untagged settings dictionaries as Vina settings.

        Args:
            value: settings model or serialized settings

        Returns:
            Settings with the legacy Vina engine default applied
        """
        if isinstance(value, dict) and "settings_type" not in value:
            return value | {"settings_type": "vina"}
        return value
