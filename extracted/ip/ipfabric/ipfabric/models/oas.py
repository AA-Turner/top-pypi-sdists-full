import json
from collections import defaultdict
from functools import cached_property
from importlib.resources import files
from typing import Optional, Any, Union
from urllib.parse import quote_plus

from httpx import URL
from pydantic import BaseModel, PrivateAttr, TypeAdapter, Field, FilePath

from ipfabric.tools.shared import raise_for_status

OAS_DIR = files("ipfabric.oas")
CONTENT_TYPE = "application/json"
LOGIN_IP_COLS = ["loginIp", "loginIpv4", "loginIpv6"]


class NestedColumn(BaseModel):
    parent: str
    child: str


class Column(BaseModel):
    name: str
    filter: Optional[str] = None
    deprecated: Optional[bool] = False


class Scan(BaseModel):
    columns: Optional[list[Union[Column, NestedColumn]]] = Field(default_factory=list)
    full_scan: bool = True


class ComplexColumn(BaseModel):
    filter: Optional[str] = None
    array: Optional[bool] = Field(False)
    children: list[Column] = Field(default_factory=list)

    @property
    def children_by_name(self) -> dict[str, Column]:
        return {_.name: _ for _ in self.children}

    @property
    def children_by_filters(self) -> dict[str, list[Column]]:
        tmp = defaultdict(list)
        [tmp[_.filter].append(_) for _ in self.children]
        return dict(tmp)


class Endpoint(BaseModel):
    full_api_endpoint: str
    web_endpoint: Optional[str] = None
    columns: Optional[list[str]] = None
    nested_columns: Optional[dict[str, ComplexColumn]] = Field(default_factory=dict)
    array_columns: Optional[dict[str, ComplexColumn]] = Field(default_factory=dict)
    deprecated_columns: Optional[set[str]] = Field(default_factory=set)
    summary: Optional[str] = None
    title: Optional[str] = None
    tags: Optional[list[str]] = Field(default_factory=list)
    tag_groups: Optional[list[str]] = Field(default_factory=list)
    method: str
    ui_columns: Optional[list[str]] = None
    api_scope_id: Optional[str] = None
    description: Optional[str] = None
    ipv4: Optional[Scan] = Field(default_factory=Scan)
    ipv6: Optional[Scan] = Field(default_factory=Scan)
    mac: Optional[Scan] = Field(default_factory=Scan)
    deprecated: Optional[bool] = False
    device_filters: list[str] = Field(default_factory=list)
    device_attribute_filters: bool = False
    attribute_filters: bool = False

    def __repr__(self):
        return f"({self.method}, {self.api_endpoint})"

    @property
    def api_endpoint(self):
        return self.full_api_endpoint[1:]

    @property
    def web_menu(self):
        return f"{self.tag_groups[0]} — {self.tags[0]}" if self.tag_groups and self.tags else None

    def filter_url(self, filters: Union[str, dict], base_url: Union[URL, str]) -> Union[None, str]:
        if not self.web_endpoint:
            return None
        filters = json.loads(filters) if isinstance(filters, str) else filters
        filters = filters if "filters" in filters else {"filters": filters}
        url = base_url.join(self.web_endpoint) if isinstance(base_url, URL) else URL(base_url).join(self.web_endpoint)
        return f"{url}?options=" + quote_plus(json.dumps(filters, separators=(",", ":")))


class Methods(BaseModel):
    full_api_endpoint: str
    get: Optional[Endpoint] = None
    put: Optional[Endpoint] = None
    patch: Optional[Endpoint] = None
    post: Optional[Endpoint] = None
    delete: Optional[Endpoint] = None

    @property
    def api_endpoint(self):
        return self.full_api_endpoint[1:]


class OAS(BaseModel):
    client: Any = Field(exclude=True)
    local_oas: bool = True
    local_oas_file: Optional[Union[FilePath, dict]] = None
    _oas: dict[str, Methods] = PrivateAttr(default_factory=dict)

    def model_post_init(self, __context) -> None:
        self._oas = self._get_oas()

    @property
    def oas(self) -> dict[str, Methods]:
        return self._oas

    def _get_oas(self) -> dict[str, Methods]:
        if not self.local_oas or (self.local_oas_file and self.local_oas):
            return self._parse_oas()
        try:
            min_oas = OAS_DIR.joinpath(self.client.api_version + ".json").read_text(encoding="UTF-8")
            oas = TypeAdapter(dict[str, Methods]).validate_json(min_oas)
            return oas
        except FileNotFoundError:
            return self._parse_oas()

    @cached_property
    def web_to_api(self) -> dict[str, Endpoint]:
        return {m.post.web_endpoint: m.post for m in self._oas.values() if m.post and m.post.web_endpoint}

    @cached_property
    def scope_to_api(self) -> dict[str, Endpoint]:
        _ = dict()
        for methods in self._oas.values():
            for method in ["get", "put", "post", "patch", "delete"]:
                m = getattr(methods, method, None)
                if m and m.api_scope_id:
                    _[m.api_scope_id] = m
        return _

    def _complex_columns(self, data: Endpoint, spec: dict) -> Endpoint:  # NOSONAR
        x_columns = {_["key"]: _ for _ in spec.get("x-table", {}).get("columns", [])}

        try:
            columns = spec["responses"]["200"]["content"][CONTENT_TYPE]["schema"]["properties"]["data"]["items"][
                "properties"
            ]
            for k, v in columns.items():
                col_type = v.get("type", None)
                children = list()
                if k in x_columns and isinstance(x_columns[k].get("filter", None), dict):
                    children = [
                        Column(
                            name=c["field"],
                            filter=c["filter"]["type"] if isinstance(c["filter"], dict) else c["filter"],
                            deprecated=c.get("deprecated", False),
                        )
                        for c in x_columns[k]["filter"]["children"]
                    ]
                if col_type == "array":
                    filters = v["filter"] if isinstance(v.get("filter", None), str) else None
                    data.array_columns[k] = ComplexColumn(array=True, children=children, filter=filters)
                    if v.get("items", {}).get("type", None) == "object":
                        data.nested_columns[k] = data.array_columns[k]
                elif col_type == "object":
                    data.nested_columns[k] = ComplexColumn(children=children)
        except KeyError:
            pass
        return self._global_search(data, spec)

    def _post_logic(self, data: Endpoint, spec: dict):
        data.web_endpoint = spec.get("x-table", {}).get("webPath")
        data.title = spec.get("x-table", {}).get("title")
        data.ui_columns = [_["key"] for _ in spec.get("x-table", {}).get("columns", [])]
        columns = set(
            spec.get("requestBody", {})
            .get("content", {})
            .get(CONTENT_TYPE, {})
            .get("schema", {})
            .get("properties", {})
            .get("columns", {})
            .get("items", {})
            .get("enum", [])
        )
        data.columns = list(columns)
        return self._complex_columns(data, spec)

    def _complex_global_search(self, data: Endpoint) -> Endpoint:
        for cname, column in data.nested_columns.items():
            data.ipv4.columns.extend(
                [NestedColumn(parent=cname, child=_.name) for _ in column.children_by_filters.get("ip", [])]
            )
            data.ipv6.columns.extend(
                [NestedColumn(parent=cname, child=_.name) for _ in column.children_by_filters.get("ipv6", [])]
            )
            data.mac.columns.extend(
                [
                    NestedColumn(parent=cname, child=_.name)
                    for _ in column.children
                    if self._check_mac(_.name, data.full_api_endpoint)
                ]
            )
        return data

    @staticmethod
    def _check_mac(mac: str, endpoint: str) -> bool:
        return (
            "mac" in mac
            and mac not in ["macVerification", "macFlags", "macCount"]
            and endpoint not in ["/tables/inventory/devices"]
        )

    def _global_search(self, data: Endpoint, spec: dict) -> Endpoint:
        if not data.api_endpoint.startswith("tables"):
            return data
        columns = spec.get("x-table", {}).get("columns", [])
        for column in columns:
            key, filter_type = column["key"], column.get("filter", "text")
            if (
                filter_type in ["ip", "routing"]
                and (
                    key not in LOGIN_IP_COLS
                    or (key in LOGIN_IP_COLS and data.full_api_endpoint == "/tables/inventory/devices")
                )
                and data.full_api_endpoint not in ["/tables/routing/protocols/ospf-v3/neighbors"]
            ):
                data.ipv4.columns.append(Column(name=key, filter=filter_type))
            elif filter_type in ["ipv6", "routingIpv6"]:
                data.ipv6.columns.append(Column(name=key, filter=filter_type))
            elif self._check_mac(key, data.full_api_endpoint):
                data.mac.columns.append(Column(name=key, filter=filter_type))
        return self._complex_global_search(data)

    def _parse_oas(self) -> dict[str, Methods]:
        if not self.local_oas or not self.local_oas_file:
            url = self.client.base_url.join("/api/static/oas/openapi-internal.json")
            oas = raise_for_status(self.client.get(url, follow_redirects=True)).json()
        elif isinstance(self.local_oas_file, dict):
            oas = self.local_oas_file
        else:
            with open(self.local_oas_file, "r") as f:
                oas = json.load(f)

        endpoints = dict()
        for endpoint, methods in oas["paths"].items():
            methods_obj = Methods(full_api_endpoint=endpoint)
            for method, spec in methods.items():
                r_props = (
                    spec.get("requestBody", {})
                    .get("content", {})
                    .get(CONTENT_TYPE, {})
                    .get("schema", {})
                    .get("properties", {})
                )
                filters = r_props.get("filters", {}).get("properties", {})
                data = Endpoint(
                    full_api_endpoint=endpoint,
                    method=method,
                    api_scope_id=spec.get("x-apiScopeId", None),
                    summary=spec.get("summary", None),
                    description=spec.get("description", None),
                    tags=spec.get("tags", None),
                    tag_groups=spec.get("x-tagGroups", None),
                    deprecated=spec.get("deprecated", False),
                    deprecated_columns={
                        _["key"] for _ in spec.get("x-table", {}).get("columns", []) if _.get("deprecated", False)
                    },
                    device_filters=[_ for _ in filters if _.startswith("device.")],
                    device_attribute_filters="device.attributes" in filters,
                    attribute_filters="attributeFilters" in r_props,
                )
                if method == "post":
                    data = self._post_logic(data, spec)
                setattr(methods_obj, method, data)
            endpoints[endpoint[1:]] = methods_obj
        return endpoints
