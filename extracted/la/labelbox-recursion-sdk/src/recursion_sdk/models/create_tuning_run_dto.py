from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_tuning_run_dto_eval_template import CreateTuningRunDtoEvalTemplate
  from ..models.create_tuning_run_dto_properties_cadence_every_n_steps import CreateTuningRunDtoPropertiesCadenceEveryNSteps
  from ..models.create_tuning_run_dto_properties_cadence_steps import CreateTuningRunDtoPropertiesCadenceSteps
  from ..models.create_tuning_run_dto_trainer_config import CreateTuningRunDtoTrainerConfig
  from ..models.create_tuning_run_dto_training_template import CreateTuningRunDtoTrainingTemplate





T = TypeVar("T", bound="CreateTuningRunDto")



@_attrs_define
class CreateTuningRunDto:
    """ Create-request body for a tuning session: trainer run-config, per-checkpoint eval template, training problem set,
    cadence, and eval-concurrency cap (organizationId is stamped from the route).

        Example:
            {'runName': 'llama-grpo-session', 'trainerRunConfigVersionId': '11111111-1111-4111-8111-111111111111',
                'trainerConfig': {}, 'evalTemplate': {'environmentId': '11111111-1111-4111-8111-111111111111',
                'solverRunConfigVersionId': '11111111-1111-4111-8111-111111111111', 'graderRunConfigVersionId':
                '11111111-1111-4111-8111-111111111111', 'problems': [{'problemId': '11111111-1111-4111-8111-111111111111',
                'problemVersionId': '11111111-1111-4111-8111-111111111111', 'environmentId':
                '11111111-1111-4111-8111-111111111111'}]}, 'trainingTemplate': {'environmentId':
                '11111111-1111-4111-8111-111111111111', 'problems': [{'problemId': '11111111-1111-4111-8111-111111111111',
                'problemVersionId': '11111111-1111-4111-8111-111111111111', 'environmentId':
                '11111111-1111-4111-8111-111111111111'}]}, 'cadence': {'type': 'every_n_steps', 'n': 5}, 'evalConcurrencyCap':
                4}

        Attributes:
            run_name (str): Human-readable label for the session and its spawned children.
            trainer_run_config_version_id (UUID): Locked, agent-harness run-config version for the trainer container.
            trainer_config (CreateTuningRunDtoTrainerConfig): Opaque trainer config blob -- never inspected by the platform
                (B7).
            eval_template (CreateTuningRunDtoEvalTemplate): Template for the per-checkpoint evaluations a tuning_run spawns.
            cadence (CreateTuningRunDtoPropertiesCadenceEveryNSteps | CreateTuningRunDtoPropertiesCadenceSteps): Which
                trainer checkpoint steps to evaluate. Step 0 (the untrained base model) is always included regardless of this
                cadence.
            eval_concurrency_cap (int): Maximum number of per-checkpoint evaluations in flight at once (1-10).
            training_template (CreateTuningRunDtoTrainingTemplate | Unset): The training problem set a tuning_run
                materializes into the trainer dataset_ref.
     """

    run_name: str
    trainer_run_config_version_id: UUID
    trainer_config: CreateTuningRunDtoTrainerConfig
    eval_template: CreateTuningRunDtoEvalTemplate
    cadence: CreateTuningRunDtoPropertiesCadenceEveryNSteps | CreateTuningRunDtoPropertiesCadenceSteps
    eval_concurrency_cap: int
    training_template: CreateTuningRunDtoTrainingTemplate | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_tuning_run_dto_eval_template import CreateTuningRunDtoEvalTemplate # noqa: PLC0415
        from ..models.create_tuning_run_dto_properties_cadence_every_n_steps import CreateTuningRunDtoPropertiesCadenceEveryNSteps # noqa: PLC0415
        from ..models.create_tuning_run_dto_properties_cadence_steps import CreateTuningRunDtoPropertiesCadenceSteps # noqa: PLC0415
        from ..models.create_tuning_run_dto_trainer_config import CreateTuningRunDtoTrainerConfig # noqa: PLC0415
        from ..models.create_tuning_run_dto_training_template import CreateTuningRunDtoTrainingTemplate # noqa: PLC0415
        run_name = self.run_name

        trainer_run_config_version_id = str(self.trainer_run_config_version_id)

        trainer_config = self.trainer_config.to_dict()

        eval_template = self.eval_template.to_dict()

        cadence: dict[str, Any]
        if isinstance(self.cadence, CreateTuningRunDtoPropertiesCadenceEveryNSteps):
            cadence = self.cadence.to_dict()
        else:
            cadence = self.cadence.to_dict()


        eval_concurrency_cap = self.eval_concurrency_cap

        training_template: dict[str, Any] | Unset = UNSET
        if not isinstance(self.training_template, Unset):
            training_template = self.training_template.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "runName": run_name,
            "trainerRunConfigVersionId": trainer_run_config_version_id,
            "trainerConfig": trainer_config,
            "evalTemplate": eval_template,
            "cadence": cadence,
            "evalConcurrencyCap": eval_concurrency_cap,
        })
        if training_template is not UNSET:
            field_dict["trainingTemplate"] = training_template

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_tuning_run_dto_eval_template import CreateTuningRunDtoEvalTemplate # noqa: PLC0415
        from ..models.create_tuning_run_dto_properties_cadence_every_n_steps import CreateTuningRunDtoPropertiesCadenceEveryNSteps # noqa: PLC0415
        from ..models.create_tuning_run_dto_properties_cadence_steps import CreateTuningRunDtoPropertiesCadenceSteps # noqa: PLC0415
        from ..models.create_tuning_run_dto_trainer_config import CreateTuningRunDtoTrainerConfig # noqa: PLC0415
        from ..models.create_tuning_run_dto_training_template import CreateTuningRunDtoTrainingTemplate # noqa: PLC0415
        d = dict(src_dict)
        run_name = d.pop("runName")

        trainer_run_config_version_id = UUID(d.pop("trainerRunConfigVersionId"))




        trainer_config = CreateTuningRunDtoTrainerConfig.from_dict(d.pop("trainerConfig"))




        eval_template = CreateTuningRunDtoEvalTemplate.from_dict(d.pop("evalTemplate"))




        def _parse_cadence(data: object) -> CreateTuningRunDtoPropertiesCadenceEveryNSteps | CreateTuningRunDtoPropertiesCadenceSteps:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cadence_type_0 = CreateTuningRunDtoPropertiesCadenceEveryNSteps.from_dict(data)



                return cadence_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            cadence_type_1 = CreateTuningRunDtoPropertiesCadenceSteps.from_dict(data)



            return cadence_type_1

        cadence = _parse_cadence(d.pop("cadence"))


        eval_concurrency_cap = d.pop("evalConcurrencyCap")

        _training_template = d.pop("trainingTemplate", UNSET)
        training_template: CreateTuningRunDtoTrainingTemplate | Unset
        if isinstance(_training_template,  Unset):
            training_template = UNSET
        else:
            training_template = CreateTuningRunDtoTrainingTemplate.from_dict(_training_template)




        create_tuning_run_dto = cls(
            run_name=run_name,
            trainer_run_config_version_id=trainer_run_config_version_id,
            trainer_config=trainer_config,
            eval_template=eval_template,
            cadence=cadence,
            eval_concurrency_cap=eval_concurrency_cap,
            training_template=training_template,
        )

        return create_tuning_run_dto

