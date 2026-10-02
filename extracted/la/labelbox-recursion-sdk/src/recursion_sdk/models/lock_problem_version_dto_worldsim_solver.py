from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lock_problem_version_dto_worldsim_solver_desktop_type import LockProblemVersionDtoWorldsimSolverDesktopType
from ..models.lock_problem_version_dto_worldsim_solver_env_type import LockProblemVersionDtoWorldsimSolverEnvType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.lock_problem_version_dto_worldsim_solver_world_effects_type_2 import LockProblemVersionDtoWorldsimSolverWorldEffectsType2





T = TypeVar("T", bound="LockProblemVersionDtoWorldsimSolver")



@_attrs_define
class LockProblemVersionDtoWorldsimSolver:
    """ Worldsim solver authoring payload (MCP servers, world effects, simulated time, CUA env-config). When present, it is
    persisted on the locked version; each run forks a per-version solver child from the solver the environment resolves
    at that time.

        Attributes:
            simulated_time (None | str): ISO-8601 simulated wall-clock time for the run (WORLDSIM_SIMULATED_TIME). Null uses
                real time.
            mcp_servers (list[str]): Selected MCP service keys. Unless inheritSolverMcpTools is true, their tools form the
                mcp-tools.yaml allowlist, and an empty selection allows no tools.
            world_effects (list[Any] | LockProblemVersionDtoWorldsimSolverWorldEffectsType2 | str): Ordered list of startup
                MCP tool calls, as an opaque JSON string (a StartupCall[]). Duplicate tools are allowed (e.g. create five
                users). The calls run through the run's MCP tool allowlist, so unless inheritSolverMcpTools is true each call's
                tool must come from a server in mcpServers.
            inherit_solver_mcp_tools (bool | Unset): When true, each run keeps the resolved solver's own MCP tool allowlist
                (the tools file its WORLDSIM_MCP_TOOLS_FILE names, set on the run config or baked into the runner image, or
                every tool when it has none) and mcpServers is ignored.
            env_type (LockProblemVersionDtoWorldsimSolverEnvType | Unset): Runtime environment type (mcp or computer). Maps
                to CUA_ENVIRONMENT_TYPE.
            desktop_type (LockProblemVersionDtoWorldsimSolverDesktopType | Unset): Computer-use desktop flavor (chrome or
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
    world_effects: list[Any] | LockProblemVersionDtoWorldsimSolverWorldEffectsType2 | str
    inherit_solver_mcp_tools: bool | Unset = UNSET
    env_type: LockProblemVersionDtoWorldsimSolverEnvType | Unset = UNSET
    desktop_type: LockProblemVersionDtoWorldsimSolverDesktopType | Unset = UNSET
    api_allowed: bool | Unset = UNSET
    allow_browser_api: bool | Unset = UNSET
    system_instructions: str | Unset = UNSET
    cua_system_instructions: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lock_problem_version_dto_worldsim_solver_world_effects_type_2 import LockProblemVersionDtoWorldsimSolverWorldEffectsType2 # noqa: PLC0415
        simulated_time: None | str
        simulated_time = self.simulated_time

        mcp_servers = self.mcp_servers



        world_effects: dict[str, Any] | list[Any] | str
        if isinstance(self.world_effects, list):
            world_effects = self.world_effects


        elif isinstance(self.world_effects, LockProblemVersionDtoWorldsimSolverWorldEffectsType2):
            world_effects = self.world_effects.to_dict()
        else:
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
        field_dict.update(self.additional_properties)
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
        from ..models.lock_problem_version_dto_worldsim_solver_world_effects_type_2 import LockProblemVersionDtoWorldsimSolverWorldEffectsType2 # noqa: PLC0415
        d = dict(src_dict)
        def _parse_simulated_time(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        simulated_time = _parse_simulated_time(d.pop("simulatedTime"))


        mcp_servers = cast(list[str], d.pop("mcpServers"))


        def _parse_world_effects(data: object) -> list[Any] | LockProblemVersionDtoWorldsimSolverWorldEffectsType2 | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                world_effects_type_1 = cast(list[Any], data)

                return world_effects_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                world_effects_type_2 = LockProblemVersionDtoWorldsimSolverWorldEffectsType2.from_dict(data)



                return world_effects_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Any] | LockProblemVersionDtoWorldsimSolverWorldEffectsType2 | str, data)

        world_effects = _parse_world_effects(d.pop("worldEffects"))


        inherit_solver_mcp_tools = d.pop("inheritSolverMcpTools", UNSET)

        _env_type = d.pop("envType", UNSET)
        env_type: LockProblemVersionDtoWorldsimSolverEnvType | Unset
        if isinstance(_env_type,  Unset):
            env_type = UNSET
        else:
            env_type = LockProblemVersionDtoWorldsimSolverEnvType(_env_type)




        _desktop_type = d.pop("desktopType", UNSET)
        desktop_type: LockProblemVersionDtoWorldsimSolverDesktopType | Unset
        if isinstance(_desktop_type,  Unset):
            desktop_type = UNSET
        else:
            desktop_type = LockProblemVersionDtoWorldsimSolverDesktopType(_desktop_type)




        api_allowed = d.pop("apiAllowed", UNSET)

        allow_browser_api = d.pop("allowBrowserApi", UNSET)

        system_instructions = d.pop("systemInstructions", UNSET)

        cua_system_instructions = d.pop("cuaSystemInstructions", UNSET)

        lock_problem_version_dto_worldsim_solver = cls(
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


        lock_problem_version_dto_worldsim_solver.additional_properties = d
        return lock_problem_version_dto_worldsim_solver

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
