"""forbid を決めた規則の層 (Decision.layer、3.1req 指示書 29)。

worker はこれで Agent への拒否の文言を出し分ける: project = プロジェクトの設定で変えられる、tenant / floor = 管理者の規則
(プロジェクトの設定では変えられない)、system = 規則ではなく判定できない。allow の layer は None。
判定 (mode / reason) そのものは変えない (test_evaluate_decision_table.py が固定)。
"""
import pytest

from agenticstar_platform.policy import (
    LAYER_FLOOR,
    LAYER_PROJECT,
    LAYER_SYSTEM,
    LAYER_TENANT,
    L1Policy,
    ProjectPolicy,
    evaluate,
    tighten_merge,
)


def _l1(profile, floor=()):
    return L1Policy.from_row({"version": 3, "default_profile": profile, "floor": {"forbid": list(floor)}})


def _eff(l1_profile, project=None, floor=()):
    return tighten_merge(_l1(l1_profile, floor), ProjectPolicy.from_json(project) if project is not None else None)


FLOOR = [{"tool": "wipe", "op_class": "destructive", "args": {"target": "prod*"}}, {"tool": "mcp:kintone:delete_record"}]


@pytest.mark.parametrize("policy, call, expected", [
    # policy 無し / 判定できない = system
    (None, dict(tool="read", op_class="read"), (LAYER_SYSTEM, "policy_unavailable")),
    (_eff("open"), dict(tool="edit", op_class="write", args_unparseable=True), (LAYER_SYSTEM, "unevaluable_args")),
    (_eff("open"), dict(tool="t", op_class="write", connection_kind="weird"), (LAYER_SYSTEM, "unevaluable_args")),
    # floor (テナントの誰も緩められない規則) = floor。floor の規則で引数を解釈できない も floor
    (_eff("open", floor=FLOOR), dict(tool="delete_record", op_class=None, mcp_server="kintone"), (LAYER_FLOOR, "floor")),
    (_eff("open", floor=FLOOR), dict(tool="wipe", op_class="destructive", args={"target": "prod-1"}), (LAYER_FLOOR, "floor")),
    (_eff("open", floor=FLOOR), dict(tool="wipe", op_class="destructive", args="not-a-dict"),
     (LAYER_FLOOR, "unevaluable_args")),
    # プロジェクトの禁止規則 = project
    (_eff("open", {"deny": ["vendor_delete*"]}), dict(tool="vendor_delete_all", op_class=None), (LAYER_PROJECT, "project_forbid")),
    # プロジェクトの禁止規則に当たったが、外しても下の段で止まる = その層 (reason / matched は project の規則のまま)
    (_eff("guarded", {"deny": ["edit"]}), dict(tool="edit", op_class="destructive"), (LAYER_TENANT, "project_forbid")),
    (_eff("strict", {"deny": ["edit"]}), dict(tool="edit", op_class=None), (LAYER_TENANT, "project_forbid")),
    (_eff("open", {"deny": ["edit"]}), dict(tool="edit", op_class="write", args_unparseable=True), (LAYER_SYSTEM, "project_forbid")),
    (_eff("open", {"deny": ["edit"]}), dict(tool="edit", op_class="bogus"), (LAYER_SYSTEM, "project_forbid")),
    (_eff("guarded", {"deny": [{"tool": "edit", "args": {"target": "prod*"}}]}),
     dict(tool="edit", op_class="destructive", args="bad-json"), (LAYER_TENANT, "unevaluable_args")),
    # 外しても project の設定 (allowlist / dry_run) で止まるだけなら project のまま
    (_eff("strict", {"deny": ["edit"]}), dict(tool="edit", op_class="write"), (LAYER_PROJECT, "project_forbid")),
    (_eff("open", {"deny": ["edit"]}), dict(tool="edit", op_class="write", dry_run=True), (LAYER_PROJECT, "project_forbid")),
    # guarded の destructive: L1 が guarded ならテナント、L1 は open で project が guarded にしたならプロジェクト
    (_eff("guarded"), dict(tool="rm", op_class="destructive"), (LAYER_TENANT, "profile")),
    (_eff("open", {"profile": "guarded"}), dict(tool="rm", op_class="destructive"), (LAYER_PROJECT, "profile")),
    # strict の allowlist に無い = project (allowlist に足せば通る)
    (_eff("strict"), dict(tool="edit", op_class="write"), (LAYER_PROJECT, "strict_allowlist")),
    (_eff("open", {"profile": "strict"}), dict(tool="rm_all", op_class="destructive"), (LAYER_PROJECT, "strict_allowlist")),
    # allowlist に無いが、足しても L1 (guarded) が destructive を禁じる = tenant (「プロジェクトで変えられる」と言わない)
    (_eff("guarded", {"profile": "strict"}), dict(tool="rm_all", op_class="destructive"), (LAYER_TENANT, "strict_allowlist")),
    (_eff("guarded"), dict(tool="rm_all", op_class="destructive", delegated=True), (LAYER_TENANT, "strict_allowlist")),
    # allowlist にあっても L1 (guarded) が destructive を禁じる = tenant (RT-A1)
    (_eff("guarded", {"profile": "strict", "allow": ["rm_*"]}), dict(tool="rm_all", op_class="destructive"),
     (LAYER_TENANT, "profile")),
    # dry_run = 実行の設定 = project。L1 が禁じる操作クラスは dry_run を外しても止まるので tenant
    (_eff("open"), dict(tool="edit", op_class="write", dry_run=True), (LAYER_PROJECT, "dry_run_read_only")),
    (_eff("guarded"), dict(tool="rm", op_class="destructive", dry_run=True), (LAYER_TENANT, "dry_run_read_only")),
    # 外部の MCP / A2A の禁止規則: プロジェクトの deny = project、floor = floor
    (_eff("open", {"deny": [{"scope": "external", "connection_id": "7", "tool": "create_*"}]}),
     dict(tool="create_issue", op_class=None, mcp_server="gitlab", connection_id="7", mcp=True), (LAYER_PROJECT, "project_forbid")),
    (_eff("open", floor=[{"tool": "mcp:kintone:delete_*"}]),
     dict(tool="delete_app", op_class=None, mcp_server="kintone", mcp=True), (LAYER_FLOOR, "floor")),
    (_eff("open", {"deny": [{"scope": "external", "connection_kind": "a2a", "connection_id": "3"}]}),
     dict(tool="ask", op_class=None, connection_id="3", connection_kind="a2a"), (LAYER_PROJECT, "project_forbid")),
    # 未分類の tool を strict 相当で止めた: strict を決めた側 (L1 strict = tenant / project strict = project)、委譲・dry_run = project
    (_eff("strict"), dict(tool="mystery", op_class=None), (LAYER_TENANT, "unknown_tool")),
    (_eff("open", {"profile": "strict"}), dict(tool="mystery", op_class=None), (LAYER_PROJECT, "unknown_tool")),
    (_eff("open"), dict(tool="mystery", op_class=None, delegated=True), (LAYER_PROJECT, "unknown_tool")),
    (_eff("open"), dict(tool="mystery", op_class=None, dry_run=True), (LAYER_PROJECT, "unknown_tool")),
])
def test_forbid_carries_the_rule_layer(policy, call, expected):
    tool = call.pop("tool")
    op_class = call.pop("op_class")
    d = evaluate(policy, tool, op_class, **call)
    assert d.mode == "forbid"
    assert (d.layer, d.reason) == expected


@pytest.mark.parametrize("policy, call", [
    (_eff("open"), dict(tool="edit", op_class="write")),
    (_eff("guarded"), dict(tool="edit", op_class="write")),
    (_eff("strict", {"allow": ["edit"]}), dict(tool="edit", op_class="write")),
    (_eff("open"), dict(tool="mystery", op_class=None)),
    (_eff("strict"), dict(tool="post", op_class=None, mcp_server="slack", mcp=True)),
])
def test_allow_has_no_layer(policy, call):
    tool = call.pop("tool")
    op_class = call.pop("op_class")
    d = evaluate(policy, tool, op_class, **call)
    assert d.mode == "allow" and d.layer is None
