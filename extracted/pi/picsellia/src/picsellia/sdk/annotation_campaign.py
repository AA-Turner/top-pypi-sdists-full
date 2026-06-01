import logging
import os
from datetime import date
from typing import Literal
from uuid import UUID

from beartype import beartype
from deprecation import deprecated

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.annotation_campaign_assignment import AnnotationCampaignAssignment
from picsellia.sdk.annotation_campaign_step import AnnotationCampaignStep
from picsellia.sdk.campaign.abstract_campaign import AbstractCampaign
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.job import Job
from picsellia.services.lister.assignment_lister import (
    AnnotationCampaignAssignmentLister,
)
from picsellia.types.enums import CampaignStepType, ObjectDataType, WorkerType
from picsellia.types.schemas import AnnotationCampaignSchema

logger = logging.getLogger("picsellia")


class AnnotationCampaign(
    AbstractCampaign[AnnotationCampaignStep, AnnotationCampaignAssignment]
):
    _base_path = "/api/campaigns/annotation"
    _allowed_step_types = [CampaignStepType.ANNOTATION, CampaignStepType.REVIEW]
    _worker_type = WorkerType.DATASET

    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)

    def __str__(self):
        return f"{Colors.GREEN}Annotation Campaign {Colors.ENDC} for dataset version {self.dataset_version_id} (id: {self.id})"

    @property
    def dataset_version_id(self) -> UUID:
        """UUID of the (DatasetVersion) of this campaign"""
        return self._dataset_version_id

    @property
    def name(self) -> str:
        """Deprecated property"""
        return f"Campaign {self._id}"

    @exception_handler
    @beartype
    def refresh(self, data: dict):
        schema = AnnotationCampaignSchema(**data)
        self._dataset_version_id = schema.dataset_version_id
        return schema

    @exception_handler
    @beartype
    def update(
        self,
        name: str | None = None,
        description: str | None = None,
        instructions_object_name: str | None = None,
        instructions_text: str | None = None,
        end_date: date | None = None,
        auto_add_new_assets: bool | None = None,
        auto_close_on_completion: bool | None = None,
        default_entry_step: AnnotationCampaignStep | None = None,
        annotated_entry_step: AnnotationCampaignStep | Literal["DONE"] | None = None,
    ) -> None:
        """Update this campaign parameters

        Examples:
            ```python
            foo_campaign.update(description="Yet another campaign")
            ```

        Arguments:
            name (str, optional): deprecated.
            description (str, optional): Description of the campaign. Defaults to None.
            instructions_object_name (str, optional): Instructions file object name stored on S3. Defaults to None.
            instructions_text (str, optional): Instructions text. Defaults to None.
            end_date (date, optional): End date of the campaign. Defaults to None.
            auto_add_new_assets (bool, optional):
                If true, new assets of this dataset will be added as a task in the campaign.  Defaults to None.
            auto_close_on_completion (bool, optional):
                If true, campaign will be close when all tasks will be done. Defaults to None.
            default_entry_step (Step, optional): Step where tasks will be created for items that have no annotations.
            annotated_entry_step (Step, optional): Step where tasks will be created for items already containing annotations
        """
        if name is not None:
            logging.warning(
                "'name' parameter is deprecated and will be removed in future versions. "
                "You cannot set a name to a Campaign anymore."
            )
        return self._update(
            description,
            instructions_object_name,
            instructions_text,
            end_date,
            auto_add_new_assets,
            auto_close_on_completion,
            default_entry_step,
            annotated_entry_step,
        )

    @exception_handler
    @beartype
    def upload_instructions_file(self, path: str) -> None:
        """Upload instructions for this campaign

        Examples:
            ```python
            foo_campaign.upload_instructions_file("/path/to/file.pdf")
            ```

        Arguments:
            path (str): Path of instructions file

        """
        instruction_file_name = os.path.basename(path)
        object_name = self.connection.generate_dataset_version_object_name(
            instruction_file_name,
            ObjectDataType.CAMPAIGN_FILE,
            dataset_version_id=self.dataset_version_id,
        )
        self.connection.upload_file(object_name, path)
        self.update(instructions_object_name=object_name)

    def _build_step(self, data: dict):
        return AnnotationCampaignStep(self.connection, data, self._id)

    @exception_handler
    @beartype
    @deprecated(
        deprecated_in="6.20.0",
        details="This method has been renamed into sync_assets",
    )
    def launch(self, existing_annotations_step_id: str | UUID | None = None) -> Job:
        """This method is deprecated. self.sync_assets() should be used instead
        Launch this campaign, creating assignments on steps you have created before.

        Examples:
            ```python
            workers = foo_dataset.list_workers()
            foo_campaign = foo_dataset_version.create_campaign()
            foo_campaign.add_step(
                name="annotation-step",
                type="ANNOTATION",
                assignees=[(workers[0], 1.0), (workers[1], 2.0)]
            )
            review_step = foo_campaign.add_step(
                name="review-step",
                type="REVIEW",
                assignees=[(workers[2], 1)]
            )
            foo_campaign.launch(existing_annotations_step_id=review_step["id"])
            ```

        Arguments:
            existing_annotations_step_id (UUID or str, optional):
                If given, will create assignments for existing annotations on given step_id.
                You also can give "DONE" in this field, it will create assignments in DONE last step. Defaults to None.

        Returns:
            a Job, that you can wait for.
        """
        return self.sync_assets(
            existing_annotations_step_id=existing_annotations_step_id
        )

    @exception_handler
    @beartype
    def sync_assets(
        self, existing_annotations_step_id: str | UUID | None = None
    ) -> Job:
        """This will create tasks and assignments for assets that are not in the campaign yet.

        By default, your already annotated assets will be synced to the annotated_entry_step in your campaign settings.
        Using existing_annotations_step_id here will override this setting once.

        Arguments:
            existing_annotations_step_id (UUID or str, optional):
                If given, will create assignments for existing annotations on given step_id.
                You also can give "DONE" in this field, it will create assignments in DONE last step. Defaults to None.

        Returns:
            a Job, that you can wait for.
        """
        return self._sync_assets(existing_annotations_step_id)

    def _get_assignment_lister(self):
        return AnnotationCampaignAssignmentLister(self.connection, self.id)
