from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.update_problem_version_dto_allowed_domains_type_0_type_0_item import UpdateProblemVersionDtoAllowedDomainsType0Type0Item
from ..models.update_problem_version_dto_container_size_type_0 import UpdateProblemVersionDtoContainerSizeType0
from ..models.update_problem_version_dto_gpu_type_type_0 import UpdateProblemVersionDtoGpuTypeType0
from ..models.update_problem_version_dto_installed_package_managers_type_0_item import UpdateProblemVersionDtoInstalledPackageManagersType0Item
from ..models.update_problem_version_dto_tools_type_0_item import UpdateProblemVersionDtoToolsType0Item
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.grading_config_input_agentic import GradingConfigInputAgentic
  from ..models.grading_config_input_compute_exec import GradingConfigInputComputeExec
  from ..models.grading_config_input_max import GradingConfigInputMax
  from ..models.grading_config_input_mcp_tool_call import GradingConfigInputMcpToolCall
  from ..models.grading_config_input_none import GradingConfigInputNone
  from ..models.grading_config_input_programmatic import GradingConfigInputProgrammatic
  from ..models.grading_config_input_rubric import GradingConfigInputRubric
  from ..models.grading_config_input_weighted_sum import GradingConfigInputWeightedSum
  from ..models.update_problem_version_dto_tool_timeouts_type_0 import UpdateProblemVersionDtoToolTimeoutsType0





T = TypeVar("T", bound="UpdateProblemVersionDto")



@_attrs_define
class UpdateProblemVersionDto:
    """ Partial-update payload for a draft problem version, with cross-field validation that privileged containers require
    unrestricted network access.

        Example:
            {'prompt': 'You are a manufacturing QA agent. Inspect the metal panel image at /workspace/panel.png and identify
                every surface defect (scratch, dent, corrosion). Write a JSON report to /workspace/report.json with one entry
                per defect: { "type", "bbox": [x, y, w, h], "severity": "low" | "medium" | "high" }.', 'tools': ['Read',
                'Write', 'Bash'], 'containerSize': 'medium', 'timeoutSeconds': 7200, 'maxTurns': 50, 'gradingConfig': {'type':
                'rubric'}, 'singleAgentRubric': True}

        Attributes:
            prompt (str | Unset): Task prompt shown to the agent at run start.
            tools (list[UpdateProblemVersionDtoToolsType0Item] | None | Unset): Tool allowlist. Null means all known tools
                allowed; an empty list means no tools allowed.
            allowed_domains (list[str] | list[UpdateProblemVersionDtoAllowedDomainsType0Type0Item] | None | Unset): Outbound
                network allowlist. Null uses the legacy platform default, the unrestricted sentinel allows everything, and a
                non-empty list restricts access to those domains.
            installed_package_managers (list[UpdateProblemVersionDtoInstalledPackageManagersType0Item] | None | Unset):
                Package managers pre-installed in the container. Null means none.
            container_image (None | str | Unset): Container image reference for the agent runtime (e.g. "python:3.12"). Null
                falls back to the platform default.
            container_size (None | Unset | UpdateProblemVersionDtoContainerSizeType0): CPU/memory tier. Null falls back to
                the platform default.
            gpu_type (None | Unset | UpdateProblemVersionDtoGpuTypeType0): Optional GPU type. Null means no GPU.
            timeout_seconds (int | None | Unset): Wall-clock timeout for the agent run. Null falls back to the platform
                default.
            tool_timeouts (None | Unset | UpdateProblemVersionDtoToolTimeoutsType0): Sparse map of tool name to seconds.
                Include only tools whose timeout differs from the default. Null or omitted means all defaults apply.
            max_turns (int | None | Unset): Maximum agent turns. Null means unlimited, subject to the wall-clock timeout.
            grading_config (GradingConfigInputAgentic | GradingConfigInputComputeExec | GradingConfigInputMax |
                GradingConfigInputMcpToolCall | GradingConfigInputNone | GradingConfigInputProgrammatic |
                GradingConfigInputRubric | GradingConfigInputWeightedSum | Unset): Recursive grading configuration tree for a
                problem version: a leaf strategy (none, rubric, agentic, programmatic, mcp_tool_call, compute_exec) or a
                composition group (weighted-sum, max) of further configs. Tree depth must be ≤ 3.
            single_agent_rubric (bool | Unset): When true, a single agentic judge scores all rubric criteria together. When
                false, each criterion is judged independently.
            privileged (bool | Unset): Run the container privileged (Docker-in-Docker or kernel capabilities). Requires
                unrestricted outbound networking because privileged containers bypass egress enforcement.
            issue_template (None | str | Unset): Markdown template used to pre-populate the body of new global issues filed
                against this version. Overrides the environment-wide template when set; send null to clear.
            solver_run_config_version_id (None | Unset | UUID): Locked run-config version bound for solver invocations on
                this problem version. Null clears the binding so the environment-level fallback applies.
            grader_run_config_version_id (None | Unset | UUID): Locked run-config version bound for grader invocations on
                this problem version. Null clears the binding so the environment-level fallback applies.
            qa_run_config_version_id (None | Unset | UUID): Locked run-config version bound for QA invocations on this
                problem version. Null clears the binding so the environment-level fallback applies.
            synthesizer_run_config_version_id (None | Unset | UUID): Locked run-config version bound for synthesizer
                invocations on this problem version. Null clears the binding so the environment-level fallback applies.
     """

    prompt: str | Unset = UNSET
    tools: list[UpdateProblemVersionDtoToolsType0Item] | None | Unset = UNSET
    allowed_domains: list[str] | list[UpdateProblemVersionDtoAllowedDomainsType0Type0Item] | None | Unset = UNSET
    installed_package_managers: list[UpdateProblemVersionDtoInstalledPackageManagersType0Item] | None | Unset = UNSET
    container_image: None | str | Unset = UNSET
    container_size: None | Unset | UpdateProblemVersionDtoContainerSizeType0 = UNSET
    gpu_type: None | Unset | UpdateProblemVersionDtoGpuTypeType0 = UNSET
    timeout_seconds: int | None | Unset = UNSET
    tool_timeouts: None | Unset | UpdateProblemVersionDtoToolTimeoutsType0 = UNSET
    max_turns: int | None | Unset = UNSET
    grading_config: GradingConfigInputAgentic | GradingConfigInputComputeExec | GradingConfigInputMax | GradingConfigInputMcpToolCall | GradingConfigInputNone | GradingConfigInputProgrammatic | GradingConfigInputRubric | GradingConfigInputWeightedSum | Unset = UNSET
    single_agent_rubric: bool | Unset = UNSET
    privileged: bool | Unset = UNSET
    issue_template: None | str | Unset = UNSET
    solver_run_config_version_id: None | Unset | UUID = UNSET
    grader_run_config_version_id: None | Unset | UUID = UNSET
    qa_run_config_version_id: None | Unset | UUID = UNSET
    synthesizer_run_config_version_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.grading_config_input_agentic import GradingConfigInputAgentic # noqa: PLC0415
        from ..models.grading_config_input_compute_exec import GradingConfigInputComputeExec # noqa: PLC0415
        from ..models.grading_config_input_max import GradingConfigInputMax # noqa: PLC0415
        from ..models.grading_config_input_mcp_tool_call import GradingConfigInputMcpToolCall # noqa: PLC0415
        from ..models.grading_config_input_none import GradingConfigInputNone # noqa: PLC0415
        from ..models.grading_config_input_programmatic import GradingConfigInputProgrammatic # noqa: PLC0415
        from ..models.grading_config_input_rubric import GradingConfigInputRubric # noqa: PLC0415
        from ..models.grading_config_input_weighted_sum import GradingConfigInputWeightedSum # noqa: PLC0415
        from ..models.update_problem_version_dto_tool_timeouts_type_0 import UpdateProblemVersionDtoToolTimeoutsType0 # noqa: PLC0415
        prompt = self.prompt

        tools: list[str] | None | Unset
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.value
                tools.append(tools_type_0_item)


        else:
            tools = self.tools

        allowed_domains: list[str] | None | Unset
        if isinstance(self.allowed_domains, Unset):
            allowed_domains = UNSET
        elif isinstance(self.allowed_domains, list):
            allowed_domains = []
            for allowed_domains_type_0_type_0_item_data in self.allowed_domains:
                allowed_domains_type_0_type_0_item = allowed_domains_type_0_type_0_item_data.value
                allowed_domains.append(allowed_domains_type_0_type_0_item)


        elif isinstance(self.allowed_domains, list):
            allowed_domains = self.allowed_domains


        else:
            allowed_domains = self.allowed_domains

        installed_package_managers: list[str] | None | Unset
        if isinstance(self.installed_package_managers, Unset):
            installed_package_managers = UNSET
        elif isinstance(self.installed_package_managers, list):
            installed_package_managers = []
            for installed_package_managers_type_0_item_data in self.installed_package_managers:
                installed_package_managers_type_0_item = installed_package_managers_type_0_item_data.value
                installed_package_managers.append(installed_package_managers_type_0_item)


        else:
            installed_package_managers = self.installed_package_managers

        container_image: None | str | Unset
        if isinstance(self.container_image, Unset):
            container_image = UNSET
        else:
            container_image = self.container_image

        container_size: None | str | Unset
        if isinstance(self.container_size, Unset):
            container_size = UNSET
        elif isinstance(self.container_size, UpdateProblemVersionDtoContainerSizeType0):
            container_size = self.container_size.value
        else:
            container_size = self.container_size

        gpu_type: None | str | Unset
        if isinstance(self.gpu_type, Unset):
            gpu_type = UNSET
        elif isinstance(self.gpu_type, UpdateProblemVersionDtoGpuTypeType0):
            gpu_type = self.gpu_type.value
        else:
            gpu_type = self.gpu_type

        timeout_seconds: int | None | Unset
        if isinstance(self.timeout_seconds, Unset):
            timeout_seconds = UNSET
        else:
            timeout_seconds = self.timeout_seconds

        tool_timeouts: dict[str, Any] | None | Unset
        if isinstance(self.tool_timeouts, Unset):
            tool_timeouts = UNSET
        elif isinstance(self.tool_timeouts, UpdateProblemVersionDtoToolTimeoutsType0):
            tool_timeouts = self.tool_timeouts.to_dict()
        else:
            tool_timeouts = self.tool_timeouts

        max_turns: int | None | Unset
        if isinstance(self.max_turns, Unset):
            max_turns = UNSET
        else:
            max_turns = self.max_turns

        grading_config: dict[str, Any] | Unset
        if isinstance(self.grading_config, Unset):
            grading_config = UNSET
        elif isinstance(self.grading_config, GradingConfigInputNone):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigInputRubric):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigInputAgentic):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigInputProgrammatic):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigInputMcpToolCall):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigInputComputeExec):
            grading_config = self.grading_config.to_dict()
        elif isinstance(self.grading_config, GradingConfigInputWeightedSum):
            grading_config = self.grading_config.to_dict()
        else:
            grading_config = self.grading_config.to_dict()


        single_agent_rubric = self.single_agent_rubric

        privileged = self.privileged

        issue_template: None | str | Unset
        if isinstance(self.issue_template, Unset):
            issue_template = UNSET
        else:
            issue_template = self.issue_template

        solver_run_config_version_id: None | str | Unset
        if isinstance(self.solver_run_config_version_id, Unset):
            solver_run_config_version_id = UNSET
        elif isinstance(self.solver_run_config_version_id, UUID):
            solver_run_config_version_id = str(self.solver_run_config_version_id)
        else:
            solver_run_config_version_id = self.solver_run_config_version_id

        grader_run_config_version_id: None | str | Unset
        if isinstance(self.grader_run_config_version_id, Unset):
            grader_run_config_version_id = UNSET
        elif isinstance(self.grader_run_config_version_id, UUID):
            grader_run_config_version_id = str(self.grader_run_config_version_id)
        else:
            grader_run_config_version_id = self.grader_run_config_version_id

        qa_run_config_version_id: None | str | Unset
        if isinstance(self.qa_run_config_version_id, Unset):
            qa_run_config_version_id = UNSET
        elif isinstance(self.qa_run_config_version_id, UUID):
            qa_run_config_version_id = str(self.qa_run_config_version_id)
        else:
            qa_run_config_version_id = self.qa_run_config_version_id

        synthesizer_run_config_version_id: None | str | Unset
        if isinstance(self.synthesizer_run_config_version_id, Unset):
            synthesizer_run_config_version_id = UNSET
        elif isinstance(self.synthesizer_run_config_version_id, UUID):
            synthesizer_run_config_version_id = str(self.synthesizer_run_config_version_id)
        else:
            synthesizer_run_config_version_id = self.synthesizer_run_config_version_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if tools is not UNSET:
            field_dict["tools"] = tools
        if allowed_domains is not UNSET:
            field_dict["allowedDomains"] = allowed_domains
        if installed_package_managers is not UNSET:
            field_dict["installedPackageManagers"] = installed_package_managers
        if container_image is not UNSET:
            field_dict["containerImage"] = container_image
        if container_size is not UNSET:
            field_dict["containerSize"] = container_size
        if gpu_type is not UNSET:
            field_dict["gpuType"] = gpu_type
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if tool_timeouts is not UNSET:
            field_dict["toolTimeouts"] = tool_timeouts
        if max_turns is not UNSET:
            field_dict["maxTurns"] = max_turns
        if grading_config is not UNSET:
            field_dict["gradingConfig"] = grading_config
        if single_agent_rubric is not UNSET:
            field_dict["singleAgentRubric"] = single_agent_rubric
        if privileged is not UNSET:
            field_dict["privileged"] = privileged
        if issue_template is not UNSET:
            field_dict["issueTemplate"] = issue_template
        if solver_run_config_version_id is not UNSET:
            field_dict["solverRunConfigVersionId"] = solver_run_config_version_id
        if grader_run_config_version_id is not UNSET:
            field_dict["graderRunConfigVersionId"] = grader_run_config_version_id
        if qa_run_config_version_id is not UNSET:
            field_dict["qaRunConfigVersionId"] = qa_run_config_version_id
        if synthesizer_run_config_version_id is not UNSET:
            field_dict["synthesizerRunConfigVersionId"] = synthesizer_run_config_version_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grading_config_input_agentic import GradingConfigInputAgentic # noqa: PLC0415
        from ..models.grading_config_input_compute_exec import GradingConfigInputComputeExec # noqa: PLC0415
        from ..models.grading_config_input_max import GradingConfigInputMax # noqa: PLC0415
        from ..models.grading_config_input_mcp_tool_call import GradingConfigInputMcpToolCall # noqa: PLC0415
        from ..models.grading_config_input_none import GradingConfigInputNone # noqa: PLC0415
        from ..models.grading_config_input_programmatic import GradingConfigInputProgrammatic # noqa: PLC0415
        from ..models.grading_config_input_rubric import GradingConfigInputRubric # noqa: PLC0415
        from ..models.grading_config_input_weighted_sum import GradingConfigInputWeightedSum # noqa: PLC0415
        from ..models.update_problem_version_dto_tool_timeouts_type_0 import UpdateProblemVersionDtoToolTimeoutsType0 # noqa: PLC0415
        d = dict(src_dict)
        prompt = d.pop("prompt", UNSET)

        def _parse_tools(data: object) -> list[UpdateProblemVersionDtoToolsType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tools_type_0 = []
                _tools_type_0 = data
                for tools_type_0_item_data in (_tools_type_0):
                    tools_type_0_item = UpdateProblemVersionDtoToolsType0Item(tools_type_0_item_data)



                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UpdateProblemVersionDtoToolsType0Item] | None | Unset, data)

        tools = _parse_tools(d.pop("tools", UNSET))


        def _parse_allowed_domains(data: object) -> list[str] | list[UpdateProblemVersionDtoAllowedDomainsType0Type0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_domains_type_0_type_0 = []
                _allowed_domains_type_0_type_0 = data
                for allowed_domains_type_0_type_0_item_data in (_allowed_domains_type_0_type_0):
                    allowed_domains_type_0_type_0_item = UpdateProblemVersionDtoAllowedDomainsType0Type0Item(allowed_domains_type_0_type_0_item_data)



                    allowed_domains_type_0_type_0.append(allowed_domains_type_0_type_0_item)

                return allowed_domains_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_domains_type_0_type_1 = cast(list[str], data)

                return allowed_domains_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | list[UpdateProblemVersionDtoAllowedDomainsType0Type0Item] | None | Unset, data)

        allowed_domains = _parse_allowed_domains(d.pop("allowedDomains", UNSET))


        def _parse_installed_package_managers(data: object) -> list[UpdateProblemVersionDtoInstalledPackageManagersType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                installed_package_managers_type_0 = []
                _installed_package_managers_type_0 = data
                for installed_package_managers_type_0_item_data in (_installed_package_managers_type_0):
                    installed_package_managers_type_0_item = UpdateProblemVersionDtoInstalledPackageManagersType0Item(installed_package_managers_type_0_item_data)



                    installed_package_managers_type_0.append(installed_package_managers_type_0_item)

                return installed_package_managers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UpdateProblemVersionDtoInstalledPackageManagersType0Item] | None | Unset, data)

        installed_package_managers = _parse_installed_package_managers(d.pop("installedPackageManagers", UNSET))


        def _parse_container_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        container_image = _parse_container_image(d.pop("containerImage", UNSET))


        def _parse_container_size(data: object) -> None | Unset | UpdateProblemVersionDtoContainerSizeType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                container_size_type_0 = UpdateProblemVersionDtoContainerSizeType0(data)



                return container_size_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UpdateProblemVersionDtoContainerSizeType0, data)

        container_size = _parse_container_size(d.pop("containerSize", UNSET))


        def _parse_gpu_type(data: object) -> None | Unset | UpdateProblemVersionDtoGpuTypeType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                gpu_type_type_0 = UpdateProblemVersionDtoGpuTypeType0(data)



                return gpu_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UpdateProblemVersionDtoGpuTypeType0, data)

        gpu_type = _parse_gpu_type(d.pop("gpuType", UNSET))


        def _parse_timeout_seconds(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        timeout_seconds = _parse_timeout_seconds(d.pop("timeoutSeconds", UNSET))


        def _parse_tool_timeouts(data: object) -> None | Unset | UpdateProblemVersionDtoToolTimeoutsType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tool_timeouts_type_0 = UpdateProblemVersionDtoToolTimeoutsType0.from_dict(data)



                return tool_timeouts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UpdateProblemVersionDtoToolTimeoutsType0, data)

        tool_timeouts = _parse_tool_timeouts(d.pop("toolTimeouts", UNSET))


        def _parse_max_turns(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_turns = _parse_max_turns(d.pop("maxTurns", UNSET))


        def _parse_grading_config(data: object) -> GradingConfigInputAgentic | GradingConfigInputComputeExec | GradingConfigInputMax | GradingConfigInputMcpToolCall | GradingConfigInputNone | GradingConfigInputProgrammatic | GradingConfigInputRubric | GradingConfigInputWeightedSum | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_0 = GradingConfigInputNone.from_dict(data)



                return componentsschemas_grading_config_input_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_1 = GradingConfigInputRubric.from_dict(data)



                return componentsschemas_grading_config_input_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_2 = GradingConfigInputAgentic.from_dict(data)



                return componentsschemas_grading_config_input_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_3 = GradingConfigInputProgrammatic.from_dict(data)



                return componentsschemas_grading_config_input_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_4 = GradingConfigInputMcpToolCall.from_dict(data)



                return componentsschemas_grading_config_input_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_5 = GradingConfigInputComputeExec.from_dict(data)



                return componentsschemas_grading_config_input_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_6 = GradingConfigInputWeightedSum.from_dict(data)



                return componentsschemas_grading_config_input_type_6
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_grading_config_input_type_7 = GradingConfigInputMax.from_dict(data)



            return componentsschemas_grading_config_input_type_7

        grading_config = _parse_grading_config(d.pop("gradingConfig", UNSET))


        single_agent_rubric = d.pop("singleAgentRubric", UNSET)

        privileged = d.pop("privileged", UNSET)

        def _parse_issue_template(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        issue_template = _parse_issue_template(d.pop("issueTemplate", UNSET))


        def _parse_solver_run_config_version_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                solver_run_config_version_id_type_0 = UUID(data)



                return solver_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        solver_run_config_version_id = _parse_solver_run_config_version_id(d.pop("solverRunConfigVersionId", UNSET))


        def _parse_grader_run_config_version_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                grader_run_config_version_id_type_0 = UUID(data)



                return grader_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        grader_run_config_version_id = _parse_grader_run_config_version_id(d.pop("graderRunConfigVersionId", UNSET))


        def _parse_qa_run_config_version_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                qa_run_config_version_id_type_0 = UUID(data)



                return qa_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        qa_run_config_version_id = _parse_qa_run_config_version_id(d.pop("qaRunConfigVersionId", UNSET))


        def _parse_synthesizer_run_config_version_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                synthesizer_run_config_version_id_type_0 = UUID(data)



                return synthesizer_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        synthesizer_run_config_version_id = _parse_synthesizer_run_config_version_id(d.pop("synthesizerRunConfigVersionId", UNSET))


        update_problem_version_dto = cls(
            prompt=prompt,
            tools=tools,
            allowed_domains=allowed_domains,
            installed_package_managers=installed_package_managers,
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
        )


        update_problem_version_dto.additional_properties = d
        return update_problem_version_dto

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
