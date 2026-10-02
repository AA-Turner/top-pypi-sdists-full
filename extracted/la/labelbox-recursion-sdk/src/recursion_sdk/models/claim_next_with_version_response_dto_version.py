from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.claim_next_with_version_response_dto_version_allowed_domains_type_0_item import ClaimNextWithVersionResponseDtoVersionAllowedDomainsType0Item
from ..models.claim_next_with_version_response_dto_version_container_size_type_0 import ClaimNextWithVersionResponseDtoVersionContainerSizeType0
from ..models.claim_next_with_version_response_dto_version_gpu_type_type_0 import ClaimNextWithVersionResponseDtoVersionGpuTypeType0
from ..models.claim_next_with_version_response_dto_version_installed_package_managers_item import ClaimNextWithVersionResponseDtoVersionInstalledPackageManagersItem
from ..models.claim_next_with_version_response_dto_version_tools_item import ClaimNextWithVersionResponseDtoVersionToolsItem
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.claim_next_with_version_response_dto_version_tool_timeouts_type_0 import ClaimNextWithVersionResponseDtoVersionToolTimeoutsType0
  from ..models.claim_next_with_version_response_dto_version_worldsim_config_type_0 import ClaimNextWithVersionResponseDtoVersionWorldsimConfigType0
  from ..models.grading_config_agentic import GradingConfigAgentic
  from ..models.grading_config_compute_exec import GradingConfigComputeExec
  from ..models.grading_config_max import GradingConfigMax
  from ..models.grading_config_mcp_tool_call import GradingConfigMcpToolCall
  from ..models.grading_config_none import GradingConfigNone
  from ..models.grading_config_programmatic import GradingConfigProgrammatic
  from ..models.grading_config_rubric import GradingConfigRubric
  from ..models.grading_config_weighted_sum import GradingConfigWeightedSum





T = TypeVar("T", bound="ClaimNextWithVersionResponseDtoVersion")



@_attrs_define
class ClaimNextWithVersionResponseDtoVersion:
    """ The initial version associated with the claimed problem.

        Attributes:
            id (UUID): Stable problem-version identifier (UUID). Each problem can have many versions; this points at one
                specific version.
            problem_id (UUID): Problem this version belongs to.
            environment_id (UUID): Environment the parent problem belongs to. Denormalized for scope checks.
            version (str): Sequential version label assigned at creation (e.g. "v1", "v2"). Example: v3.
            prompt (str): Task prompt shown to the agent at run start.
            container_image (None | str): Container image reference for the agent runtime (e.g. "python:3.12"). Null falls
                back to the platform default.
            container_size (ClaimNextWithVersionResponseDtoVersionContainerSizeType0 | None): CPU/memory tier for the run
                container. Null falls back to the platform default.
            gpu_type (ClaimNextWithVersionResponseDtoVersionGpuTypeType0 | None): Optional GPU type attached to the run.
                Null means no GPU is attached.
            timeout_seconds (int | None): Wall-clock timeout for the agent run, in seconds. Null falls back to the platform
                default. Example: 7200.
            tool_timeouts (ClaimNextWithVersionResponseDtoVersionToolTimeoutsType0 | None): Sparse map of tool name to
                seconds. Only tools with explicit overrides are present. Null means all defaults apply.
            max_turns (int | None): Maximum agent turns allowed for the run. Null means unlimited, subject to the wall-clock
                timeout. Example: 50.
            grading_config (GradingConfigAgentic | GradingConfigComputeExec | GradingConfigMax | GradingConfigMcpToolCall |
                GradingConfigNone | GradingConfigProgrammatic | GradingConfigRubric | GradingConfigWeightedSum): Recursive
                grading configuration tree for a problem version: a leaf strategy (none, rubric, agentic, programmatic,
                mcp_tool_call, compute_exec) or a composition group (weighted-sum, max) of further configs. Tree depth must be ≤
                3.
            single_agent_rubric (bool): When true, a single agentic judge scores all rubric criteria together. When false,
                each criterion is judged independently.
            privileged (bool): Run the container privileged (root on the host node). Only takes effect on the GKE launcher;
                requires unrestricted outbound networking because privileged containers bypass egress enforcement.
            issue_template (None | str): Markdown template that overrides the environment-wide global-issue template for
                issues filed against this version. Null inherits the environment template.
            solver_run_config_version_id (None | UUID): Locked run-config version bound for solver invocations on this
                problem version. Null falls back to the environment-level binding.
            grader_run_config_version_id (None | UUID): Locked run-config version bound for grader invocations on this
                problem version. Null falls back to the environment-level binding.
            qa_run_config_version_id (None | UUID): Locked run-config version bound for QA invocations on this problem
                version. Null falls back to the environment-level binding.
            synthesizer_run_config_version_id (None | UUID): Locked run-config version bound for synthesizer invocations on
                this problem version. Null falls back to the environment-level binding.
            worldsim_config (ClaimNextWithVersionResponseDtoVersionWorldsimConfigType0 | None): Raw worldsim authoring
                payload persisted at lock. Each run materializes the per-version solver run config from it; also used for
                export/import and re-authoring. Null when the version has no worldsim config.
            locked_at (datetime.datetime | None): Timestamp when this version was locked and made immutable (ISO-8601, UTC).
                Null while the version is still a draft.
            created_at (datetime.datetime): Timestamp when the problem version was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the problem version was last updated (ISO-8601, UTC).
            installed_package_managers (list[ClaimNextWithVersionResponseDtoVersionInstalledPackageManagersItem]): Package
                managers pre-installed in the container. An empty list means none are provisioned.
            tools (list[ClaimNextWithVersionResponseDtoVersionToolsItem] | Unset): Tool allowlist for the agent. Omitted
                means all known tools are allowed; an empty list means no tools are allowed.
            allowed_domains (list[ClaimNextWithVersionResponseDtoVersionAllowedDomainsType0Item] | list[str] | Unset):
                Outbound network allowlist. Omitted uses the platform default, the unrestricted sentinel allows everything, and
                a non-empty list restricts access to those domains.
     """

    id: UUID
    problem_id: UUID
    environment_id: UUID
    version: str
    prompt: str
    container_image: None | str
    container_size: ClaimNextWithVersionResponseDtoVersionContainerSizeType0 | None
    gpu_type: ClaimNextWithVersionResponseDtoVersionGpuTypeType0 | None
    timeout_seconds: int | None
    tool_timeouts: ClaimNextWithVersionResponseDtoVersionToolTimeoutsType0 | None
    max_turns: int | None
    grading_config: GradingConfigAgentic | GradingConfigComputeExec | GradingConfigMax | GradingConfigMcpToolCall | GradingConfigNone | GradingConfigProgrammatic | GradingConfigRubric | GradingConfigWeightedSum
    single_agent_rubric: bool
    privileged: bool
    issue_template: None | str
    solver_run_config_version_id: None | UUID
    grader_run_config_version_id: None | UUID
    qa_run_config_version_id: None | UUID
    synthesizer_run_config_version_id: None | UUID
    worldsim_config: ClaimNextWithVersionResponseDtoVersionWorldsimConfigType0 | None
    locked_at: datetime.datetime | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    installed_package_managers: list[ClaimNextWithVersionResponseDtoVersionInstalledPackageManagersItem]
    tools: list[ClaimNextWithVersionResponseDtoVersionToolsItem] | Unset = UNSET
    allowed_domains: list[ClaimNextWithVersionResponseDtoVersionAllowedDomainsType0Item] | list[str] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.claim_next_with_version_response_dto_version_tool_timeouts_type_0 import ClaimNextWithVersionResponseDtoVersionToolTimeoutsType0 # noqa: PLC0415
        from ..models.claim_next_with_version_response_dto_version_worldsim_config_type_0 import ClaimNextWithVersionResponseDtoVersionWorldsimConfigType0 # noqa: PLC0415
        from ..models.grading_config_agentic import GradingConfigAgentic # noqa: PLC0415
        from ..models.grading_config_compute_exec import GradingConfigComputeExec # noqa: PLC0415
        from ..models.grading_config_max import GradingConfigMax # noqa: PLC0415
        from ..models.grading_config_mcp_tool_call import GradingConfigMcpToolCall # noqa: PLC0415
        from ..models.grading_config_none import GradingConfigNone # noqa: PLC0415
        from ..models.grading_config_programmatic import GradingConfigProgrammatic # noqa: PLC0415
        from ..models.grading_config_rubric import GradingConfigRubric # noqa: PLC0415
        from ..models.grading_config_weighted_sum import GradingConfigWeightedSum # noqa: PLC0415
        id = str(self.id)

        problem_id = str(self.problem_id)

        environment_id = str(self.environment_id)

        version = self.version

        prompt = self.prompt

        container_image: None | str
        container_image = self.container_image

        container_size: None | str
        if isinstance(self.container_size, ClaimNextWithVersionResponseDtoVersionContainerSizeType0):
            container_size = self.container_size.value
        else:
            container_size = self.container_size

        gpu_type: None | str
        if isinstance(self.gpu_type, ClaimNextWithVersionResponseDtoVersionGpuTypeType0):
            gpu_type = self.gpu_type.value
        else:
            gpu_type = self.gpu_type

        timeout_seconds: int | None
        timeout_seconds = self.timeout_seconds

        tool_timeouts: dict[str, Any] | None
        if isinstance(self.tool_timeouts, ClaimNextWithVersionResponseDtoVersionToolTimeoutsType0):
            tool_timeouts = self.tool_timeouts.to_dict()
        else:
            tool_timeouts = self.tool_timeouts

        max_turns: int | None
        max_turns = self.max_turns

        grading_config: dict[str, Any]
        if isinstance(self.grading_config, GradingConfigNone):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigRubric):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigAgentic):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigProgrammatic):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigMcpToolCall):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigComputeExec):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigWeightedSum):
            grading_config = self.grading_config.to_dict()
        else:
            grading_config = self.grading_config.to_dict()


        single_agent_rubric = self.single_agent_rubric

        privileged = self.privileged

        issue_template: None | str
        issue_template = self.issue_template

        solver_run_config_version_id: None | str
        if isinstance(self.solver_run_config_version_id, UUID):
            solver_run_config_version_id = str(self.solver_run_config_version_id)
        else:
            solver_run_config_version_id = self.solver_run_config_version_id

        grader_run_config_version_id: None | str
        if isinstance(self.grader_run_config_version_id, UUID):
            grader_run_config_version_id = str(self.grader_run_config_version_id)
        else:
            grader_run_config_version_id = self.grader_run_config_version_id

        qa_run_config_version_id: None | str
        if isinstance(self.qa_run_config_version_id, UUID):
            qa_run_config_version_id = str(self.qa_run_config_version_id)
        else:
            qa_run_config_version_id = self.qa_run_config_version_id

        synthesizer_run_config_version_id: None | str
        if isinstance(self.synthesizer_run_config_version_id, UUID):
            synthesizer_run_config_version_id = str(self.synthesizer_run_config_version_id)
        else:
            synthesizer_run_config_version_id = self.synthesizer_run_config_version_id

        worldsim_config: dict[str, Any] | None
        if isinstance(self.worldsim_config, ClaimNextWithVersionResponseDtoVersionWorldsimConfigType0):
            worldsim_config = self.worldsim_config.to_dict()
        else:
            worldsim_config = self.worldsim_config

        locked_at: None | str
        if isinstance(self.locked_at, datetime.datetime):
            locked_at = self.locked_at.isoformat()
        else:
            locked_at = self.locked_at

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        installed_package_managers = []
        for installed_package_managers_item_data in self.installed_package_managers:
            installed_package_managers_item = installed_package_managers_item_data.value
            installed_package_managers.append(installed_package_managers_item)



        tools: list[str] | Unset = UNSET
        if not isinstance(self.tools, Unset):
            tools = []
            for tools_item_data in self.tools:
                tools_item = tools_item_data.value
                tools.append(tools_item)



        allowed_domains: list[str] | Unset
        if isinstance(self.allowed_domains, Unset):
            allowed_domains = UNSET
        elif isinstance(self.allowed_domains, list):
            allowed_domains = []
            for allowed_domains_type_0_item_data in self.allowed_domains:
                allowed_domains_type_0_item = allowed_domains_type_0_item_data.value
                allowed_domains.append(allowed_domains_type_0_item)


        else:
            allowed_domains = self.allowed_domains





        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "problemId": problem_id,
            "environmentId": environment_id,
            "version": version,
            "prompt": prompt,
            "containerImage": container_image,
            "containerSize": container_size,
            "gpuType": gpu_type,
            "timeoutSeconds": timeout_seconds,
            "toolTimeouts": tool_timeouts,
            "maxTurns": max_turns,
            "gradingConfig": grading_config,
            "singleAgentRubric": single_agent_rubric,
            "privileged": privileged,
            "issueTemplate": issue_template,
            "solverRunConfigVersionId": solver_run_config_version_id,
            "graderRunConfigVersionId": grader_run_config_version_id,
            "qaRunConfigVersionId": qa_run_config_version_id,
            "synthesizerRunConfigVersionId": synthesizer_run_config_version_id,
            "worldsimConfig": worldsim_config,
            "lockedAt": locked_at,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "installedPackageManagers": installed_package_managers,
        })
        if tools is not UNSET:
            field_dict["tools"] = tools
        if allowed_domains is not UNSET:
            field_dict["allowedDomains"] = allowed_domains

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.claim_next_with_version_response_dto_version_tool_timeouts_type_0 import ClaimNextWithVersionResponseDtoVersionToolTimeoutsType0 # noqa: PLC0415
        from ..models.claim_next_with_version_response_dto_version_worldsim_config_type_0 import ClaimNextWithVersionResponseDtoVersionWorldsimConfigType0 # noqa: PLC0415
        from ..models.grading_config_agentic import GradingConfigAgentic # noqa: PLC0415
        from ..models.grading_config_compute_exec import GradingConfigComputeExec # noqa: PLC0415
        from ..models.grading_config_max import GradingConfigMax # noqa: PLC0415
        from ..models.grading_config_mcp_tool_call import GradingConfigMcpToolCall # noqa: PLC0415
        from ..models.grading_config_none import GradingConfigNone # noqa: PLC0415
        from ..models.grading_config_programmatic import GradingConfigProgrammatic # noqa: PLC0415
        from ..models.grading_config_rubric import GradingConfigRubric # noqa: PLC0415
        from ..models.grading_config_weighted_sum import GradingConfigWeightedSum # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        problem_id = UUID(d.pop("problemId"))




        environment_id = UUID(d.pop("environmentId"))




        version = d.pop("version")

        prompt = d.pop("prompt")

        def _parse_container_image(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        container_image = _parse_container_image(d.pop("containerImage"))


        def _parse_container_size(data: object) -> ClaimNextWithVersionResponseDtoVersionContainerSizeType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                container_size_type_0 = ClaimNextWithVersionResponseDtoVersionContainerSizeType0(data)



                return container_size_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ClaimNextWithVersionResponseDtoVersionContainerSizeType0 | None, data)

        container_size = _parse_container_size(d.pop("containerSize"))


        def _parse_gpu_type(data: object) -> ClaimNextWithVersionResponseDtoVersionGpuTypeType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                gpu_type_type_0 = ClaimNextWithVersionResponseDtoVersionGpuTypeType0(data)



                return gpu_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ClaimNextWithVersionResponseDtoVersionGpuTypeType0 | None, data)

        gpu_type = _parse_gpu_type(d.pop("gpuType"))


        def _parse_timeout_seconds(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        timeout_seconds = _parse_timeout_seconds(d.pop("timeoutSeconds"))


        def _parse_tool_timeouts(data: object) -> ClaimNextWithVersionResponseDtoVersionToolTimeoutsType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tool_timeouts_type_0 = ClaimNextWithVersionResponseDtoVersionToolTimeoutsType0.from_dict(data)



                return tool_timeouts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ClaimNextWithVersionResponseDtoVersionToolTimeoutsType0 | None, data)

        tool_timeouts = _parse_tool_timeouts(d.pop("toolTimeouts"))


        def _parse_max_turns(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_turns = _parse_max_turns(d.pop("maxTurns"))


        def _parse_grading_config(data: object) -> GradingConfigAgentic | GradingConfigComputeExec | GradingConfigMax | GradingConfigMcpToolCall | GradingConfigNone | GradingConfigProgrammatic | GradingConfigRubric | GradingConfigWeightedSum:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_0 = GradingConfigNone.from_dict(data)



                return componentsschemas_grading_config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_1 = GradingConfigRubric.from_dict(data)



                return componentsschemas_grading_config_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_2 = GradingConfigAgentic.from_dict(data)



                return componentsschemas_grading_config_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_3 = GradingConfigProgrammatic.from_dict(data)



                return componentsschemas_grading_config_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_4 = GradingConfigMcpToolCall.from_dict(data)



                return componentsschemas_grading_config_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_5 = GradingConfigComputeExec.from_dict(data)



                return componentsschemas_grading_config_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_6 = GradingConfigWeightedSum.from_dict(data)



                return componentsschemas_grading_config_type_6
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_grading_config_type_7 = GradingConfigMax.from_dict(data)



            return componentsschemas_grading_config_type_7

        grading_config = _parse_grading_config(d.pop("gradingConfig"))


        single_agent_rubric = d.pop("singleAgentRubric")

        privileged = d.pop("privileged")

        def _parse_issue_template(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        issue_template = _parse_issue_template(d.pop("issueTemplate"))


        def _parse_solver_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                solver_run_config_version_id_type_0 = UUID(data)



                return solver_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        solver_run_config_version_id = _parse_solver_run_config_version_id(d.pop("solverRunConfigVersionId"))


        def _parse_grader_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                grader_run_config_version_id_type_0 = UUID(data)



                return grader_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        grader_run_config_version_id = _parse_grader_run_config_version_id(d.pop("graderRunConfigVersionId"))


        def _parse_qa_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                qa_run_config_version_id_type_0 = UUID(data)



                return qa_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        qa_run_config_version_id = _parse_qa_run_config_version_id(d.pop("qaRunConfigVersionId"))


        def _parse_synthesizer_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                synthesizer_run_config_version_id_type_0 = UUID(data)



                return synthesizer_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        synthesizer_run_config_version_id = _parse_synthesizer_run_config_version_id(d.pop("synthesizerRunConfigVersionId"))


        def _parse_worldsim_config(data: object) -> ClaimNextWithVersionResponseDtoVersionWorldsimConfigType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worldsim_config_type_0 = ClaimNextWithVersionResponseDtoVersionWorldsimConfigType0.from_dict(data)



                return worldsim_config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ClaimNextWithVersionResponseDtoVersionWorldsimConfigType0 | None, data)

        worldsim_config = _parse_worldsim_config(d.pop("worldsimConfig"))


        def _parse_locked_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                locked_at_type_0 = datetime.datetime.fromisoformat(data)



                return locked_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        locked_at = _parse_locked_at(d.pop("lockedAt"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        installed_package_managers = []
        _installed_package_managers = d.pop("installedPackageManagers")
        for installed_package_managers_item_data in (_installed_package_managers):
            installed_package_managers_item = ClaimNextWithVersionResponseDtoVersionInstalledPackageManagersItem(installed_package_managers_item_data)



            installed_package_managers.append(installed_package_managers_item)


        _tools = d.pop("tools", UNSET)
        tools: list[ClaimNextWithVersionResponseDtoVersionToolsItem] | Unset = UNSET
        if _tools is not UNSET:
            tools = []
            for tools_item_data in _tools:
                tools_item = ClaimNextWithVersionResponseDtoVersionToolsItem(tools_item_data)



                tools.append(tools_item)


        def _parse_allowed_domains(data: object) -> list[ClaimNextWithVersionResponseDtoVersionAllowedDomainsType0Item] | list[str] | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_domains_type_0 = []
                _allowed_domains_type_0 = data
                for allowed_domains_type_0_item_data in (_allowed_domains_type_0):
                    allowed_domains_type_0_item = ClaimNextWithVersionResponseDtoVersionAllowedDomainsType0Item(allowed_domains_type_0_item_data)



                    allowed_domains_type_0.append(allowed_domains_type_0_item)

                return allowed_domains_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, list):
                raise TypeError()
            allowed_domains_type_1 = cast(list[str], data)

            return allowed_domains_type_1

        allowed_domains = _parse_allowed_domains(d.pop("allowedDomains", UNSET))


        claim_next_with_version_response_dto_version = cls(
            id=id,
            problem_id=problem_id,
            environment_id=environment_id,
            version=version,
            prompt=prompt,
            container_image=container_image,
            container_size=container_size,
            gpu_type=gpu_type,
            timeout_seconds=timeout_seconds,
            tool_timeouts=tool_timeouts,
            max_turns=max_turns,
            grading_config=grading_config,
            single_agent_rubric=single_agent_rubric,
            privileged=privileged,
            issue_template=issue_template,
            solver_run_config_version_id=solver_run_config_version_id,
            grader_run_config_version_id=grader_run_config_version_id,
            qa_run_config_version_id=qa_run_config_version_id,
            synthesizer_run_config_version_id=synthesizer_run_config_version_id,
            worldsim_config=worldsim_config,
            locked_at=locked_at,
            created_at=created_at,
            updated_at=updated_at,
            installed_package_managers=installed_package_managers,
            tools=tools,
            allowed_domains=allowed_domains,
        )

        return claim_next_with_version_response_dto_version

