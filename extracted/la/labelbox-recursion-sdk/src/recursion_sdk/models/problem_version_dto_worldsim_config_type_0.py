from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_version_dto_worldsim_config_type_0_desktop_type import ProblemVersionDtoWorldsimConfigType0DesktopType
from ..models.problem_version_dto_worldsim_config_type_0_env_type import ProblemVersionDtoWorldsimConfigType0EnvType
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProblemVersionDtoWorldsimConfigType0")



@_attrs_define
class ProblemVersionDtoWorldsimConfigType0:
    """ Worldsim solver authoring payload as persisted on a locked version and returned in the problem-version DTO. Same
    shape as the authoring payload, with worldEffects as the normalized opaque JSON string.

        Attributes:
            simulated_time (None | str): ISO-8601 simulated wall-clock time for the run (WORLDSIM_SIMULATED_TIME). Null uses
                real time.
            mcp_servers (list[str]): Selected MCP service keys. Unless inheritSolverMcpTools is true, their tools form the
                mcp-tools.yaml allowlist, and an empty selection allows no tools.
            world_effects (str): Ordered list of startup MCP tool calls, as an opaque JSON string (a StartupCall[]).
                Duplicate tools are allowed (e.g. create five users). The calls run through the run's MCP tool allowlist, so
                unless inheritSolverMcpTools is true each call's tool must come from a server in mcpServers.
            inherit_solver_mcp_tools (bool | Unset): When true, each run keeps the resolved solver's own MCP tool allowlist
                (the tools file its WORLDSIM_MCP_TOOLS_FILE names, set on the run config or baked into the runner image, or
                every tool when it has none) and mcpServers is ignored.
            env_type (ProblemVersionDtoWorldsimConfigType0EnvType | Unset): Runtime environment type (mcp or computer). Maps
                to CUA_ENVIRONMENT_TYPE.
            desktop_type (ProblemVersionDtoWorldsimConfigType0DesktopType | Unset): Computer-use desktop flavor (chrome or
                full_desktop). Only meaningful when envType is "computer". Maps to CUA_DESKTOP_TYPE.
            api_allowed (bool | Unset): Whether the run may call the API. Maps to CUA_API_ALLOWED.
            allow_browser_api (bool | Unset): Whether the run may use the browser API. Maps to CUA_ALLOW_BROWSER_API.
            system_instructions (str | Unset): Free-text system instructions for the Worldsim harness in MCP or Computer
                environments. Maps to CUA_SYSTEM_INSTRUCTIONS. Supersedes cuaSystemInstructions.
            cua_system_instructions (str | Unset): Deprecated: use systemInstructions. Retained for locked-version
                compatibility. Maps to CUA_SYSTEM_INSTRUCTIONS.
     """

    simulated_time: None | str
    mcp_servers: list[str]
    world_effects: str
    inherit_solver_mcp_tools: bool | Unset = UNSET
    env_type: ProblemVersionDtoWorldsimConfigType0EnvType | Unset = UNSET
    desktop_type: ProblemVersionDtoWorldsimConfigType0DesktopType | Unset = UNSET
    api_allowed: bool | Unset = UNSET
    allow_browser_api: bool | Unset = UNSET
    system_instructions: str | Unset = UNSET
    cua_system_instructions: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        simulated_time: None | str
        simulated_time = self.simulated_time

        mcp_servers = self.mcp_servers



        world_effects = self.world_effects

        inherit_solver_mcp_tools = self.inherit_solver_mcp_tools

        env_type: str | Unset = UNSET
        if not isinstance(self.env_type, Unset):
            env_type = self.env_type.value


        desktop_type: str | Unset = UNSET
        if not isinstance(self.desktop_type, Unset):
            desktop_type = self.desktop_type.value


        api_allowed = self.api_allowed

        allow_browser_api = self.allow_browser_api

        system_instructions = self.system_instructions

        cua_system_instructions = self.cua_system_instructions


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "simulatedTime": simulated_time,
            "mcpServers": mcp_servers,
            "worldEffects": world_effects,
        })
        if inherit_solver_mcp_tools is not UNSET:
            field_dict["inheritSolverMcpTools"] = inherit_solver_mcp_tools
        if env_type is not UNSET:
            field_dict["envType"] = env_type
        if desktop_type is not UNSET:
            field_dict["desktopType"] = desktop_type
        if api_allowed is not UNSET:
            field_dict["apiAllowed"] = api_allowed
        if allow_browser_api is not UNSET:
            field_dict["allowBrowserApi"] = allow_browser_api
        if system_instructions is not UNSET:
            field_dict["systemInstructions"] = system_instructions
        if cua_system_instructions is not UNSET:
            field_dict["cuaSystemInstructions"] = cua_system_instructions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_simulated_time(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        simulated_time = _parse_simulated_time(d.pop("simulatedTime"))


        mcp_servers = cast(list[str], d.pop("mcpServers"))


        world_effects = d.pop("worldEffects")

        inherit_solver_mcp_tools = d.pop("inheritSolverMcpTools", UNSET)

        _env_type = d.pop("envType", UNSET)
        env_type: ProblemVersionDtoWorldsimConfigType0EnvType | Unset
        if isinstance(_env_type,  Unset):
            env_type = UNSET
        else:
            env_type = ProblemVersionDtoWorldsimConfigType0EnvType(_env_type)




        _desktop_type = d.pop("desktopType", UNSET)
        desktop_type: ProblemVersionDtoWorldsimConfigType0DesktopType | Unset
        if isinstance(_desktop_type,  Unset):
            desktop_type = UNSET
        else:
            desktop_type = ProblemVersionDtoWorldsimConfigType0DesktopType(_desktop_type)




        api_allowed = d.pop("apiAllowed", UNSET)

        allow_browser_api = d.pop("allowBrowserApi", UNSET)

        system_instructions = d.pop("systemInstructions", UNSET)

        cua_system_instructions = d.pop("cuaSystemInstructions", UNSET)

        problem_version_dto_worldsim_config_type_0 = cls(
            simulated_time=simulated_time,
            mcp_servers=mcp_servers,
            world_effects=world_effects,
            inherit_solver_mcp_tools=inherit_solver_mcp_tools,
            env_type=env_type,
            desktop_type=desktop_type,
            api_allowed=api_allowed,
            allow_browser_api=allow_browser_api,
            system_instructions=system_instructions,
            cua_system_instructions=cua_system_instructions,
        )

        return problem_version_dto_worldsim_config_type_0

