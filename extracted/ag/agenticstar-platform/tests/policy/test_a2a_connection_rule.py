"""3.0req 指示書 30 (2026-09-23): A2A 外部 Agent を接続 ID で禁止する (schema 4、`connection_kind`)。

- external 規則は接続の種別 `connection_kind` (mcp | a2a) を持つ。省略 = mcp (3.0.3 までの保存形・digest と同一)
- a2a 規則は接続 (Agent) 単位。tool / method を持たない (送信単位が message で skill を指定できない = 強制できない粒度を作らない)
- a2a 規則を含む policy は schema 4。旧 reader は 4 を拒否 = policy 取得不能 = 全 forbid。mcp 規則だけなら 3 のまま
- evaluate(connection_kind="a2a"): MCP と同じく実行ルールの対象外。floor / 明示 deny (a2a の接続 ID、scope 無しの tool 名 glob)
  に当たらなければ allow (`a2a_unrestricted`)。接続を識別できない (connection_id None) + a2a 規則あり = 判定不能 (forbid)
- MCP の規則は A2A に、A2A の規則は MCP に掛からない (同じ整数 ID でも別の表)
- verify_connections は `{"mcp": {...}, "a2a": {...}}` を受ける。a2a 規則があるのに a2a の表が無い / 接続が無い = ValueError
"""
import json

import pytest

from agenticstar_platform.policy import (
    CONNECTION_KINDS,
    SCHEMA_VERSION_SCOPED,
    SCHEMA_VERSION_TYPED_CONNECTION,
    SUPPORTED_SCHEMA_VERSIONS,
    EffectivePolicy,
    ForbidPattern,
    L1Policy,
    ProjectPolicy,
    evaluate,
    policy_digest,
    requires_schema,
    tighten_merge,
    verify_connections,
)


def _l1(profile="open", floor=(), version=5):
    return L1Policy.from_row({"version": version, "default_profile": profile, "floor": {"forbid": list(floor)}})


A2A_17 = {"scope": "external", "connection_kind": "a2a", "connection_id": "17"}
MCP_17 = {"scope": "external", "connection_id": "17", "tool": "*"}


def test_constants_and_parse_forms():
    assert CONNECTION_KINDS == ("mcp", "a2a")
    assert SCHEMA_VERSION_TYPED_CONNECTION == 4 and 4 in SUPPORTED_SCHEMA_VERSIONS and SCHEMA_VERSION_SCOPED == 3
    a2a = ForbidPattern.parse(A2A_17)
    assert a2a.scope == "external" and a2a.connection_kind == "a2a" and a2a.connection_id == "17"
    assert a2a.tool == "a2a:17" and a2a.to_dict() == A2A_17  # tool は保存形に出ない
    mcp = ForbidPattern.parse(MCP_17)
    assert mcp.connection_kind == "mcp" and mcp.to_dict() == MCP_17  # mcp は connection_kind を出さない (digest 不変)
    assert ForbidPattern.parse({**MCP_17, "connection_kind": "mcp"}).to_dict() == MCP_17
    for bad in ({**A2A_17, "tool": "*"}, {**A2A_17, "method": "x"},  # a2a は tool を持てない
                {**A2A_17, "tool": None}, {**A2A_17, "method": None},  # 値が null でもキーがあれば拒否 (指示書 30 §4.1)
                {**A2A_17, "op_class": "write"}, {**A2A_17, "args": {"message": "*"}},  # 分類も引数条件も評価しない = 持たせない
                {"scope": "external", "connection_kind": "smtp", "connection_id": "1"},  # 未知の種別
                {"connection_kind": "a2a", "connection_id": "1"},  # scope 無しに種別だけ
                {"scope": "external", "connection_kind": "a2a"},  # 接続 ID 無し
                {"scope": "internal", "kind": "text_write", "connection_kind": "a2a"}):
        with pytest.raises(ValueError):
            ForbidPattern.parse(bad)


def test_schema_version_is_4_only_with_a2a_rules_and_old_forms_are_rejected():
    with_a2a = tighten_merge(_l1("open", [A2A_17]), None)
    mcp_only = tighten_merge(_l1("open", [MCP_17]), None)
    legacy = tighten_merge(_l1("open", ["write"]), None)
    assert with_a2a.schema_version == 4 and mcp_only.schema_version == 3 and legacy.schema_version == 2
    assert requires_schema(with_a2a.floor, ()) == 4
    body = with_a2a.to_dict()
    assert body["schema_version"] == 4 and body["floor"] == [A2A_17]
    back = EffectivePolicy.from_dict(json.loads(json.dumps(body)))
    assert back.to_dict() == body and policy_digest(back) == policy_digest(with_a2a)
    # schema 3 と名乗りながら a2a 規則を持つ保存形は拒否 (旧 writer が意味を落とした可能性)
    with pytest.raises(ValueError):
        EffectivePolicy.from_dict({**body, "schema_version": 3})
    # mcp だけの policy の保存形は 3.0.3 と同じ (connection_kind は出ない)
    assert "connection_kind" not in json.dumps(mcp_only.to_dict())


def test_a2a_call_is_forbidden_only_by_a2a_rule_with_same_connection_id():
    floor = tighten_merge(_l1("open", [A2A_17]), None)
    deny = evaluate(floor, "afmr_discovery_agent", None, connection_kind="a2a", connection_id="17")
    assert deny.mode == "forbid" and deny.reason == "floor" and deny.matched == "a2a:17"
    other = evaluate(floor, "afmr_discovery_agent", None, connection_kind="a2a", connection_id="18")
    assert other.mode == "allow" and other.reason == "a2a_unrestricted"
    # project の deny でも同じ。int / str の ID は同じ接続
    prj = tighten_merge(_l1("open"), ProjectPolicy.from_json({"deny": [{**A2A_17, "connection_id": 17}]}))
    assert evaluate(prj, "x", None, connection_kind="a2a", connection_id="17").reason == "project_forbid"
    # 同じ整数 ID の MCP 規則は A2A に掛からない / A2A 規則は MCP に掛からない / 組み込みにも掛からない
    mcp_only = tighten_merge(_l1("open", [MCP_17]), None)
    assert evaluate(mcp_only, "afmr_discovery_agent", None, connection_kind="a2a", connection_id="17").mode == "allow"
    assert evaluate(floor, "merge", None, mcp_server="gitlab", connection_id="17", mcp=True).reason == "mcp_unrestricted"
    assert evaluate(floor, "write", "write").mode == "allow"
    # 同名の tool 名 glob (scope 無し) は従来どおり A2A にも掛かる (改名で外れる従来の手段は残す)
    legacy = tighten_merge(_l1("open", ["afmr_*"]), None)
    assert evaluate(legacy, "afmr_discovery_agent", None, connection_kind="a2a", connection_id="3").mode == "forbid"


def test_a2a_is_outside_profile_rules_like_mcp_and_unidentified_connection_is_fail_closed():
    strict = tighten_merge(_l1("strict"), ProjectPolicy.from_json({"profile": "strict", "allow": []}))
    for kw in ({}, {"dry_run": True}, {"delegated": True}):
        d = evaluate(strict, "afmr_discovery_agent", None, connection_kind="a2a", connection_id="17", **kw)
        assert d.mode == "allow" and d.reason == "a2a_unrestricted" and not d.unregistered
    # 呼び元が op_class を渡しても無視する (A2A は分類しない)
    assert evaluate(strict, "x", "destructive", connection_kind="a2a", connection_id="17").mode == "allow"
    # a2a 規則があるのに接続を識別できない = 判定不能 → forbid
    floor = tighten_merge(_l1("open", [A2A_17]), None)
    assert evaluate(floor, "x", None, connection_kind="a2a", connection_id=None).reason == "unevaluable_args"
    assert evaluate(floor, "x", None, connection_kind="a2a", connection_id="  ").reason == "unevaluable_args"
    # a2a 規則が無ければ識別できなくても allow (MCP の連携先が無いテナントと同じ)
    assert evaluate(strict, "x", None, connection_kind="a2a", connection_id=None).mode == "allow"
    # 未知の種別 = 判定不能 (fail-closed)。policy 無しは従来どおり
    assert evaluate(strict, "x", None, connection_kind="smtp", connection_id="1").mode == "forbid"
    assert evaluate(None, "x", None, connection_kind="a2a", connection_id="1").reason == "policy_unavailable"
    # 種別 mcp を明示した呼び出しは従来の MCP 判定と同じ
    mcp_only = tighten_merge(_l1("open", [MCP_17]), None)
    assert evaluate(mcp_only, "merge", None, mcp_server="gitlab", connection_id="17", connection_kind="mcp").reason == "floor"


def test_verify_connections_takes_tables_per_kind_and_fails_closed():
    pol = tighten_merge(_l1("open", [A2A_17, MCP_17]), None)
    assert verify_connections(pol, {"mcp": {17: "gitlab"}, "a2a": {"17": "AFMR"}}) is pol
    assert verify_connections(pol, {"mcp": {"17": ""}, "a2a": {17}}) is pol
    for conns in ({"mcp": {17: "gitlab"}},  # a2a の表が無い
                  {"mcp": {17: "gitlab"}, "a2a": {}},  # a2a の接続が無い
                  {"mcp": {}, "a2a": {17: "AFMR"}},  # mcp の接続が無い
                  {17: "gitlab"}):  # 従来の平らな表は mcp としてだけ読む → a2a を確かめられない
        with pytest.raises(ValueError):
            verify_connections(pol, conns)
    # mcp 規則だけなら従来の平らな表 / 集合でよい (3.0.3 の呼び元を変えない)
    mcp_only = tighten_merge(_l1("open", [MCP_17]), None)
    assert verify_connections(mcp_only, {17: "gitlab"}) is mcp_only and verify_connections(mcp_only, {"17"}) is mcp_only
    assert verify_connections(mcp_only, {"mcp": {"17": "gitlab"}}) is mcp_only


def test_tool_aliases_extend_legacy_glob_candidates_only():
    """tool_aliases (指示書 30): scope 無しの tool 名 glob の候補に別名を足す (どれかに当たれば forbid)。scope 付き規則
    (a2a の接続 ID / mcp の external) には効かない。MCP / 組み込みにも同じ意味で使える (呼び元が渡した場合だけ)。"""
    legacy = tighten_merge(_l1("open", ["map_view_*"]), None)
    d = evaluate(legacy, "map_view", None, connection_kind="a2a", connection_id="17", tool_aliases=("map_view_1",))
    assert d.mode == "forbid" and d.matched == "map_view_*"
    assert evaluate(legacy, "map_view", None, connection_kind="a2a", connection_id="17").mode == "allow"
    assert evaluate(legacy, "x", None, connection_kind="a2a", connection_id="17", tool_aliases=("", None, "map_view_2")).mode == "forbid"
    # scope 付き規則は別名で当たらない (接続 ID / mcp_server で照合)
    scoped = tighten_merge(_l1("open", [A2A_17, MCP_17]), None)
    assert evaluate(scoped, "x", None, connection_kind="a2a", connection_id="18", tool_aliases=("a2a:17",)).mode == "allow"
    assert evaluate(scoped, "write", "write", tool_aliases=("merge",)).mode == "allow"
    # 組み込み: 別名が glob に当たれば forbid、無ければ従来どおり
    assert evaluate(legacy, "write", "write", tool_aliases=("map_view_9",)).mode == "forbid"
    assert evaluate(legacy, "write", "write").mode == "allow"
    # 別名は許可 (strict の allowlist) を広げない: allow=["edit"] の strict で write を edit の別名付きで呼んでも forbid のまま
    strict = tighten_merge(_l1("open"), ProjectPolicy.from_json({"profile": "strict", "allow": ["edit"]}))
    assert evaluate(strict, "write", "write").mode == "forbid"
    assert evaluate(strict, "write", "write", tool_aliases=("edit",)).mode == "forbid"
    assert evaluate(strict, "write", "write", delegated=True, tool_aliases=("edit",)).mode == "forbid"
    assert evaluate(strict, "edit", "write").mode == "allow"  # 本来の候補は従来どおり
