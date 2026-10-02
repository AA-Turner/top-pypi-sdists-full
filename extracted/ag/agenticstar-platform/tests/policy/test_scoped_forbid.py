"""MT-A08 / MT-R06 (2026-09-14): 禁止操作の「内部操作種別」と「外部 (接続先 + MCP メソッド名)」の分離 (schema 3)。

- internal: 組み込み tool を種別 (kind + mapping_version) で禁止。同名の MCP メソッドには掛からない
- external: connection_id (mcp_server_configurations.id) で接続を識別する。worker は呼び出しの接続 ID (`connection_id`) を
  渡し、名前では照合しない (3.0req 指示書 26。3.0.1 までの bind_connections = 名前への束縛は廃止)。MCP 呼び出しなのに
  接続 ID が無ければ判定不能 = forbid (禁止を黙って落とさない)。組み込み tool と worker 内蔵の MCP (LOCAL_CONNECTION)
  には掛からない。resolver は verify_connections で規則が指す接続の存在だけ確かめる
- 旧 (scope 無し) の規則は従来どおり candidates への glob 照合 (意味を変えない)
- scope 付き規則が無い policy は schema 2 のまま (既存 digest / 旧 reader 不変)。ある policy は schema 3。
  schema 2 と名乗りつつ scope 付き規則を持つ保存形は拒否 (旧 writer が意味を落とした可能性)
"""
import json

import pytest

from agenticstar_platform.policy import (
    INTERNAL_OPERATIONS_MAPPING_VERSION,
    SCHEMA_VERSION_SCOPED,
    SUPPORTED_SCHEMA_VERSIONS,
    EffectivePolicy,
    ForbidPattern,
    L1Policy,
    ProjectPolicy,
    LOCAL_CONNECTION,
    evaluate,
    internal_operation_kinds,
    internal_operation_mapping,
    kind_tools,
    requires_schema,
    tighten_merge,
    verify_connections,
)


def _l1(profile="open", floor=(), version=5):
    return L1Policy.from_row({"version": version, "default_profile": profile, "floor": {"forbid": list(floor)}})


INTERNAL_WRITE = {"scope": "internal", "kind": "text_write"}
EXTERNAL_MERGE = {"scope": "external", "connection_id": "17", "tool": "merge_*"}


def test_parse_shapes_and_rejections():
    p = ForbidPattern.parse(INTERNAL_WRITE)
    assert p.scope == "internal" and p.kind == "text_write" and p.mapping_version == INTERNAL_OPERATIONS_MAPPING_VERSION
    assert p.to_dict() == {"scope": "internal", "kind": "text_write", "mapping_version": INTERNAL_OPERATIONS_MAPPING_VERSION}
    e = ForbidPattern.parse(EXTERNAL_MERGE)
    assert e.scope == "external" and e.connection_id == "17" and e.tool == "merge_*"
    assert e.to_dict() == {"scope": "external", "connection_id": "17", "tool": "merge_*"}
    # 3.0.1 までの保存形 (名前に束縛した `server`) は読み捨てる = 保存形・digest は ID だけの形に揃う
    assert ForbidPattern.parse({**EXTERNAL_MERGE, "server": "gitlab"}).to_dict() == e.to_dict()
    assert not hasattr(e, "server")
    legacy = ForbidPattern.parse({"tool": "write"})
    assert legacy.scope is None and legacy.to_dict() == {"tool": "write"}
    for bad in ({"scope": "internal"}, {"scope": "internal", "kind": "nope"},
                {"scope": "internal", "kind": "text_write", "mapping_version": 99},
                {"scope": "internal", "kind": "text_write", "connection_id": "1"},
                {"scope": "external", "tool": "x"}, {"scope": "external", "connection_id": "1"},
                {"scope": "external", "connection_id": "1", "tool": "mcp:x"},
                {"scope": "external", "connection_id": "1", "tool": "x", "kind": "text_write"},
                {"scope": "other", "tool": "x"}, {"tool": "x", "kind": "text_write"}, {"tool": "x", "connection_id": "1"}):
        with pytest.raises(ValueError):
            ForbidPattern.parse(bad)


def test_internal_kind_forbids_native_tools_but_not_same_named_mcp_methods():
    pol = tighten_merge(_l1("open", [INTERNAL_WRITE]), None)
    assert evaluate(pol, "write", "write").mode == "forbid" and evaluate(pol, "write", "write").reason == "floor"
    assert evaluate(pol, "edit", "write").mode == "forbid"
    assert evaluate(pol, "bash", "write").mode == "allow", "bash は『コマンド実行』の種別 = text_write では止まらない"
    assert evaluate(pol, "read", "read").mode == "allow"
    assert evaluate(pol, "write", "write", mcp_server="gitlab").mode == "allow", "同名の MCP メソッドには掛からない"
    assert evaluate(pol, "native:write", "write").mode == "allow", "名前空間を含む名前は scoped 規則の対象外"
    for empty in ("", "  "):  # 空の server 名は「組み込み」として扱う (従来の candidates と同じ)
        assert evaluate(pol, "write", "write", mcp_server=empty).reason == "floor"
    assert "bash" in kind_tools("command_exec") and "bash" not in kind_tools("text_write")
    assert {"lsp", "diagnostics"} <= kind_tools("file_read")


def test_external_rule_matches_by_connection_id_and_never_native():
    pol = tighten_merge(_l1("open", [EXTERNAL_MERGE]), None)
    ev = lambda tool, cls, **kw: evaluate(pol, tool, cls, **kw)  # noqa: E731
    # 接続を識別できない MCP 呼び出し (connection_id 無し) は判定不能 = forbid。組み込みは影響なし
    d = ev("merge_merge_request", "destructive", mcp_server="gitlab")
    assert d.mode == "forbid" and d.reason == "unevaluable_args"
    assert ev("merge_merge_request", "destructive").mode == "allow"
    # 照合は接続 ID。名前は何でもよい (空白付き / 別名 / `__` 入り) し、別 ID の同名接続には掛からない
    for name in ("gitlab", "gitlab ", " GitLab", "crm__prod", "autonomous-tools"):
        assert ev("merge_merge_request", "destructive", mcp_server=name, connection_id="17").reason == "floor", name
    assert ev("merge_merge_request", "destructive", mcp_server="gitlab", connection_id=17).reason == "floor", "整数の ID も同じ接続"
    assert ev("merge_merge_request", "destructive", mcp_server="gitlab", connection_id="18").mode == "allow", "別接続の同名メソッドには掛からない"
    assert ev("create_merge_request", "write", mcp_server="gitlab", connection_id="17").mode == "allow"
    # worker 内蔵の MCP (DB 登録の接続ではない) には掛からない。接続と同じ名前でも
    assert ev("merge_merge_request", "destructive", mcp_server="gitlab", connection_id=LOCAL_CONNECTION).mode == "allow"
    assert ev("merge_x", "write", mcp_server="git:lab", connection_id="17").reason == "floor", "名前に ':' があっても ID で照合する"
    # 表示名が空 / 空白だけでも、接続 ID が付いていれば MCP 由来 (名前で由来を消さない)。ID も無ければ従来どおり組み込み扱い
    for blank in ("", "   ", None):
        assert ev("merge_x", "write", mcp_server=blank, connection_id="17").reason == "floor", repr(blank)
        assert ev("merge_x", "write", mcp_server=blank, connection_id="18").mode == "allow", repr(blank)
    assert ev("merge_x", "write", mcp_server="   ").mode == "allow"
    # 統制する側は MCP 由来を明示する: 名前が空白だけで ID も無い遠隔 MCP 呼び出しは「識別できない MCP」= forbid (組み込みに見せない)
    for blank in ("", "   ", None):
        assert ev("merge_x", "write", mcp_server=blank, mcp=True).reason == "unevaluable_args", repr(blank)
        assert ev("merge_x", "write", mcp_server=blank, connection_id="17", mcp=True).reason == "floor", repr(blank)
    assert ev("merge_x", "write", mcp_server="gitlab", mcp=False).mode == "allow", "明示の False は組み込み = external 規則の対象外"
    internal = tighten_merge(_l1("open", [INTERNAL_WRITE]), None)
    assert evaluate(internal, "write", "write", mcp_server="", mcp=True).mode == "allow", "MCP 由来を明示すれば internal 規則は掛からない"
    assert evaluate(internal, "write", "write", mcp_server="").reason == "floor", "明示が無ければ従来の推定 (空の名前 = 組み込み)"
    # メソッド名に ':' を含む MCP 呼び出しは external 規則では判定できない = forbid (fail-open にしない)。internal は対象外
    assert ev("native:write", None, mcp_server="gitlab", connection_id="17").reason == "unevaluable_args"
    assert ev("native:write", None, mcp_server="gitlab").reason == "unevaluable_args"
    assert pol.schema_version == 3 and tighten_merge(_l1("open", ["write"]), None).schema_version == 2  # 属性は保存形と同じ
    # resolver は規則が指す接続の存在だけ確かめる (policy は書き換えない)
    assert verify_connections(pol, {"17": "gitlab"}) is pol
    assert verify_connections(pol, {17: "gitlab"}) is pol and verify_connections(pol, {17}) is pol
    for conns in ({}, {"18": "gitlab"}, None, {"1", "7"}):
        with pytest.raises(ValueError):
            verify_connections(pol, conns)
    legacy_only = tighten_merge(_l1("open", ["write"]), None)
    assert verify_connections(legacy_only, {}) is legacy_only


def test_legacy_bare_and_glob_rules_keep_their_meaning():
    pol = tighten_merge(_l1("open", ["write", "mcp:kintone:delete_*"]), ProjectPolicy.from_json({"deny": ["vendor_*"]}))
    assert evaluate(pol, "write", "write").reason == "floor"
    assert evaluate(pol, "write", "write", mcp_server="gitlab").reason == "floor", "旧 bare 規則は今までどおり MCP も巻き込む"
    assert evaluate(pol, "delete_record", "destructive", mcp_server="kintone").reason == "floor"
    assert evaluate(pol, "vendor_delete", "destructive").reason == "project_forbid"
    assert pol.to_dict()["schema_version"] == 2 and "scope" not in json.dumps(pol.to_dict())


def test_schema_version_is_3_only_with_scoped_rules_and_round_trips():
    plain = tighten_merge(_l1("guarded", ["write"]), None)
    scoped = tighten_merge(_l1("guarded", [INTERNAL_WRITE]), ProjectPolicy.from_json({"deny": [EXTERNAL_MERGE]}))
    assert plain.to_dict()["schema_version"] == 2 and scoped.to_dict()["schema_version"] == SCHEMA_VERSION_SCOPED
    assert requires_schema(plain.floor, plain.forbid) == 2 and requires_schema(scoped.floor, scoped.forbid) == 3
    assert SUPPORTED_SCHEMA_VERSIONS == (2, 3, 4)  # 4 = a2a の接続規則 (3.0.4、指示書 30)
    back = EffectivePolicy.from_dict(json.dumps(scoped.to_dict()))
    assert back.to_dict() == scoped.to_dict() and back.digest == scoped.digest
    assert back.floor[0].kind == "text_write" and back.forbid[0].connection_id == "17"
    # 旧 writer が schema 2 と書きながら scoped 規則を含めた保存形は受理しない
    lying = dict(scoped.to_dict(), schema_version=2)
    with pytest.raises(ValueError):
        EffectivePolicy.from_dict(lying)
    with pytest.raises(ValueError):
        EffectivePolicy.from_dict(dict(scoped.to_dict(), schema_version=99))  # 未対応の版 (4 は 3.0.4 で a2a 規則の版になった)
    # 3.0.1 までの snapshot (名前に束縛した `server` 入り) を読んでも、保存形と digest は ID だけの形に揃う
    legacy = json.loads(json.dumps(scoped.to_dict()))
    legacy["forbid"][0]["server"] = "gitlab"
    back2 = EffectivePolicy.from_dict(legacy)
    assert back2.to_dict() == scoped.to_dict() and back2.digest == scoped.digest


def test_rt_a1_project_cannot_loosen_scoped_floor_and_conditions_are_conjunctive():
    l1 = _l1("guarded", [INTERNAL_WRITE, EXTERNAL_MERGE])
    pol = tighten_merge(l1, ProjectPolicy.from_json({"profile": "strict", "allow": ["write", "mcp:gitlab:merge_*"]}), project_id="p1")
    assert evaluate(pol, "write", "write").reason == "floor"
    assert evaluate(pol, "merge_merge_request", "destructive", mcp_server="gitlab", connection_id="17").reason == "floor"
    cond = ForbidPattern.parse({**INTERNAL_WRITE, "op_class": "write", "args": {"file_path": "/etc/*"}})
    polc = tighten_merge(_l1("open", [cond.to_dict()]), None)
    assert evaluate(polc, "write", "write", args={"file_path": "/etc/passwd"}).reason == "floor"
    assert evaluate(polc, "write", "write", args={"file_path": "/w/a"}).mode == "allow"
    assert evaluate(polc, "write", "destructive", args={"file_path": "/etc/passwd"}).mode == "allow"  # op_class 条件も conjunctive


def test_public_kinds_do_not_expose_tool_names():
    public = internal_operation_kinds()
    full_names = sorted({t for tools in internal_operation_mapping()["kinds"].values() for t in tools}, key=len, reverse=True)
    full_names = [n for n in full_names if len(n) >= 3 and n not in ("read", "edit", "write", "upload", "download", "browser")]  # 説明文で普通に使う英単語だけ除外 (grep / glob / lsp 等は tool 名として露出になる)
    assert public["mapping_version"] == INTERNAL_OPERATIONS_MAPPING_VERSION
    ids = [k["id"] for k in public["kinds"]]
    assert ids == ["text_write", "file_read", "file_transfer", "command_exec", "browser", "desktop"]
    text = json.dumps(public, ensure_ascii=False)
    for name in ("bash", "write", "macos_applescript", "box_upload"):
        assert f'"{name}"' not in text
    # RRC-04: 説明文にも内部 tool 名を書かない (公開 DTO は操作の表現だけ)
    for kind in public["kinds"]:
        blob = (kind["description_ja"] + kind["description_en"] + kind["label_ja"] + kind["label_en"]).lower()
        for name in full_names:
            assert name not in blob, (kind["id"], name)
    full = internal_operation_mapping()
    assert full["kinds"]["command_exec"] == ["bash"] and "macos_applescript" in full["kinds"]["desktop"]
    all_tools = [t for tools in full["kinds"].values() for t in tools]
    assert len(all_tools) == len(set(all_tools)), "1 つの tool は 1 種別だけに入る"
