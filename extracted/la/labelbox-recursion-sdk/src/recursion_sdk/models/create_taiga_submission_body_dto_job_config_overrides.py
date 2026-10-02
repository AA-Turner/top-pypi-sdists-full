from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_taiga_submission_body_dto_job_config_overrides_iteration_order import CreateTaigaSubmissionBodyDtoJobConfigOverridesIterationOrder
from ..models.create_taiga_submission_body_dto_job_config_overrides_priority import CreateTaigaSubmissionBodyDtoJobConfigOverridesPriority
from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateTaigaSubmissionBodyDtoJobConfigOverrides")



@_attrs_define
class CreateTaigaSubmissionBodyDtoJobConfigOverrides:
    """ Per-submission overrides for Taiga job-level controls. Omitted fields fall back to the environment integration
    defaults.

        Attributes:
            api_model_name (str | Unset): Solver model identifier forwarded to Taiga (e.g. claude-sonnet-4-6).
            n_attempts_per_problem (int | Unset): Number of solver attempts per (problem × iteration). Defaults to 1.
                Default: 1.
            turn_limit (int | Unset): Per-attempt turn cap forwarded to Taiga. Omitted means use Taiga default.
            max_ctx (int | Unset): Per-attempt context-window cap forwarded to Taiga.
            priority (CreateTaigaSubmissionBodyDtoJobConfigOverridesPriority | Unset): Taiga job-level priority. Mothership
                defaults to "high".
            iteration_order (CreateTaigaSubmissionBodyDtoJobConfigOverridesIterationOrder | Unset): Taiga job iteration
                order over (problem × attempt) tuples.
            enable_memory (bool | Unset): Enable Taiga-side memory/persistence between turns.
            enable_autocompact (bool | Unset): Enable Taiga-side automatic transcript compaction when nearing context
                limits.
            auxiliary_model_api_name (str | Unset): Optional auxiliary model identifier for compaction / summarization
                passes.
     """

    api_model_name: str | Unset = UNSET
    n_attempts_per_problem: int | Unset = 1
    turn_limit: int | Unset = UNSET
    max_ctx: int | Unset = UNSET
    priority: CreateTaigaSubmissionBodyDtoJobConfigOverridesPriority | Unset = UNSET
    iteration_order: CreateTaigaSubmissionBodyDtoJobConfigOverridesIterationOrder | Unset = UNSET
    enable_memory: bool | Unset = UNSET
    enable_autocompact: bool | Unset = UNSET
    auxiliary_model_api_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        api_model_name = self.api_model_name

        n_attempts_per_problem = self.n_attempts_per_problem

        turn_limit = self.turn_limit

        max_ctx = self.max_ctx

        priority: str | Unset = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.value


        iteration_order: str | Unset = UNSET
        if not isinstance(self.iteration_order, Unset):
            iteration_order = self.iteration_order.value


        enable_memory = self.enable_memory

        enable_autocompact = self.enable_autocompact

        auxiliary_model_api_name = self.auxiliary_model_api_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if api_model_name is not UNSET:
            field_dict["apiModelName"] = api_model_name
        if n_attempts_per_problem is not UNSET:
            field_dict["nAttemptsPerProblem"] = n_attempts_per_problem
        if turn_limit is not UNSET:
            field_dict["turnLimit"] = turn_limit
        if max_ctx is not UNSET:
            field_dict["maxCtx"] = max_ctx
        if priority is not UNSET:
            field_dict["priority"] = priority
        if iteration_order is not UNSET:
            field_dict["iterationOrder"] = iteration_order
        if enable_memory is not UNSET:
            field_dict["enableMemory"] = enable_memory
        if enable_autocompact is not UNSET:
            field_dict["enableAutocompact"] = enable_autocompact
        if auxiliary_model_api_name is not UNSET:
            field_dict["auxiliaryModelApiName"] = auxiliary_model_api_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_model_name = d.pop("apiModelName", UNSET)

        n_attempts_per_problem = d.pop("nAttemptsPerProblem", UNSET)

        turn_limit = d.pop("turnLimit", UNSET)

        max_ctx = d.pop("maxCtx", UNSET)

        _priority = d.pop("priority", UNSET)
        priority: CreateTaigaSubmissionBodyDtoJobConfigOverridesPriority | Unset
        if isinstance(_priority,  Unset):
            priority = UNSET
        else:
            priority = CreateTaigaSubmissionBodyDtoJobConfigOverridesPriority(_priority)




        _iteration_order = d.pop("iterationOrder", UNSET)
        iteration_order: CreateTaigaSubmissionBodyDtoJobConfigOverridesIterationOrder | Unset
        if isinstance(_iteration_order,  Unset):
            iteration_order = UNSET
        else:
            iteration_order = CreateTaigaSubmissionBodyDtoJobConfigOverridesIterationOrder(_iteration_order)




        enable_memory = d.pop("enableMemory", UNSET)

        enable_autocompact = d.pop("enableAutocompact", UNSET)

        auxiliary_model_api_name = d.pop("auxiliaryModelApiName", UNSET)

        create_taiga_submission_body_dto_job_config_overrides = cls(
            api_model_name=api_model_name,
            n_attempts_per_problem=n_attempts_per_problem,
            turn_limit=turn_limit,
            max_ctx=max_ctx,
            priority=priority,
            iteration_order=iteration_order,
            enable_memory=enable_memory,
            enable_autocompact=enable_autocompact,
            auxiliary_model_api_name=auxiliary_model_api_name,
        )


        create_taiga_submission_body_dto_job_config_overrides.additional_properties = d
        return create_taiga_submission_body_dto_job_config_overrides

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
