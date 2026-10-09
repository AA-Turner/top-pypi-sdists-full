"""High-throughput docking workflow."""

from typing import Annotated, Any

from pydantic import AfterValidator, ConfigDict, NonNegativeInt, field_validator, model_validator

from ..pdb import PDB
from ..types import UUID, Vector3D, round_list
from .docking import Score, VinaSettings
from .workflow import BatchSMILESWorkflow, ProteinStructureWorkflow


class BatchDockingWorkflow(BatchSMILESWorkflow, ProteinStructureWorkflow):
    """Batch docking workflow.

    Attributes:
        initial_smiles_list: list of SMILES
        protein: PDB of the protein, or the UUID of the protein.

        target: PDB of the protein, or the UUID of the protein. DEPRECATED
        pocket: center (x, y, z) and size (x, y, z) of the pocket
        docking_settings: how to run each docking calculation
        num_poses_to_save: number of top-scoring compounds to save; 0 disables saving
        run_mmgbsa: refine the saved poses with MM/GBSA when true (at most `num_poses_to_save`
            of them); ignored when `num_poses_to_save` is 0

        best_scores: best score for each SMILES string
        refined_scores: pose and validity for the top `num_poses_to_save` compounds,
            parallel to `initial_smiles_list`; `None` otherwise. `score` is always the
            original Vina score; `pose` is refined and `mmgbsa_score` set only if
            MM/GBSA succeeded, raw pose and `mmgbsa_score=None` otherwise
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    target: PDB | UUID
    pocket: tuple[Vector3D, Vector3D]

    docking_settings: VinaSettings = VinaSettings()
    num_poses_to_save: NonNegativeInt = 0
    run_mmgbsa: bool = False

    best_scores: Annotated[list[float | None], AfterValidator(round_list(3))] = []
    refined_scores: list[Score | None] = []

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
