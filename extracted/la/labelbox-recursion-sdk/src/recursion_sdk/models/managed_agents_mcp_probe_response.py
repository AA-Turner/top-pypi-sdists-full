from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_mcp_probe_response_credential_unopenable import ManagedAgentsMCPProbeResponseCredentialUnopenable
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_mcp_probe_tool import ManagedAgentsMCPProbeTool





T = TypeVar("T", bound="ManagedAgentsMCPProbeResponse")



@_attrs_define
class ManagedAgentsMCPProbeResponse:
    """ Response body of POST /v1/mcp/probe: the result of one live connection attempt to an MCP server, run through the
    same URL and vault resolution a real session uses. This envelope is a verdict rather than a resource: a server that
    is down is still HTTP 200 with ok=false, so a caller can distinguish "the server you configured is unreachable" from
    "this API is unreachable". Nothing is persisted by a probe.

        Example:
            {'credential_matched': True, 'credential_unopenable': 'external_reference', 'deployment_authorized': True,
                'error': 'example', 'ok': True, 'protocol_version': 'example', 'reachable': True, 'server_name': 'example',
                'tools': [{'description': 'example', 'name': 'example-name'}]}

        Attributes:
            credential_matched (bool): True when a credential from the named vaults was opened and attached to the request.
                It reports whether this attempt was authenticated, not whether a credential exists: a credential that matched
                the server URL but could not be opened reports false and sets credential_unopenable, because nothing was sent.
            deployment_authorized (bool): True when a deployment-owned access-token policy authorizes this endpoint for the
                organization and each request mints a token for the deployment's reader identity. Distinct from
                credential_matched: no vault credential is involved. For endpoints that answer discovery unauthenticated (Google
                hosted MCPs), a green tool list proves connectivity and discovery, not provider-side IAM — only a real tool call
                does.
            ok (bool): True when the server completed the handshake and returned a tool list.
            reachable (bool): True when the handshake succeeded, even if listing tools then failed.
            tools (list[ManagedAgentsMCPProbeTool] | None): Tools the server advertised on this attempt. Always an array and
                never null: empty means the handshake succeeded but the server offered no tools, or listing them failed, which
                is what ok=false plus reachable=true reports.
            credential_unopenable (ManagedAgentsMCPProbeResponseCredentialUnopenable | Unset): Set when a credential matched
                this server URL and could not be opened, so the request carried no auth header. external_reference means the
                material is held outside this service and must be re-entered here; material_missing means the credential row
                carries no stored value. Empty when none matched or the match was usable.
            error (str | Unset): Operator-facing diagnostic when the probe failed. Never contains credential material.
            protocol_version (str | Unset): The MCP protocol version used.
            server_name (str | Unset): What the server called itself during the handshake, which is how an operator confirms
                the URL reached the intended service.
     """

    credential_matched: bool
    deployment_authorized: bool
    ok: bool
    reachable: bool
    tools: list[ManagedAgentsMCPProbeTool] | None
    credential_unopenable: ManagedAgentsMCPProbeResponseCredentialUnopenable | Unset = UNSET
    error: str | Unset = UNSET
    protocol_version: str | Unset = UNSET
    server_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_mcp_probe_tool import ManagedAgentsMCPProbeTool # noqa: PLC0415
        credential_matched = self.credential_matched

        deployment_authorized = self.deployment_authorized

        ok = self.ok

        reachable = self.reachable

        tools: list[dict[str, Any]] | None
        if isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)


        else:
            tools = self.tools

        credential_unopenable: str | Unset = UNSET
        if not isinstance(self.credential_unopenable, Unset):
            credential_unopenable = self.credential_unopenable.value


        error = self.error

        protocol_version = self.protocol_version

        server_name = self.server_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "credential_matched": credential_matched,
            "deployment_authorized": deployment_authorized,
            "ok": ok,
            "reachable": reachable,
            "tools": tools,
        })
        if credential_unopenable is not UNSET:
            field_dict["credential_unopenable"] = credential_unopenable
        if error is not UNSET:
            field_dict["error"] = error
        if protocol_version is not UNSET:
            field_dict["protocol_version"] = protocol_version
        if server_name is not UNSET:
            field_dict["server_name"] = server_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_mcp_probe_tool import ManagedAgentsMCPProbeTool # noqa: PLC0415
        d = dict(src_dict)
        credential_matched = d.pop("credential_matched")

        deployment_authorized = d.pop("deployment_authorized")

        ok = d.pop("ok")

        reachable = d.pop("reachable")

        def _parse_tools(data: object) -> list[ManagedAgentsMCPProbeTool] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tools_type_0 = []
                _tools_type_0 = data
                for tools_type_0_item_data in (_tools_type_0):
                    tools_type_0_item = ManagedAgentsMCPProbeTool.from_dict(tools_type_0_item_data)



                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsMCPProbeTool] | None, data)

        tools = _parse_tools(d.pop("tools"))


        _credential_unopenable = d.pop("credential_unopenable", UNSET)
        credential_unopenable: ManagedAgentsMCPProbeResponseCredentialUnopenable | Unset
        if isinstance(_credential_unopenable,  Unset):
            credential_unopenable = UNSET
        else:
            credential_unopenable = ManagedAgentsMCPProbeResponseCredentialUnopenable(_credential_unopenable)




        error = d.pop("error", UNSET)

        protocol_version = d.pop("protocol_version", UNSET)

        server_name = d.pop("server_name", UNSET)

        managed_agents_mcp_probe_response = cls(
            credential_matched=credential_matched,
            deployment_authorized=deployment_authorized,
            ok=ok,
            reachable=reachable,
            tools=tools,
            credential_unopenable=credential_unopenable,
            error=error,
            protocol_version=protocol_version,
            server_name=server_name,
        )


        managed_agents_mcp_probe_response.additional_properties = d
        return managed_agents_mcp_probe_response

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
