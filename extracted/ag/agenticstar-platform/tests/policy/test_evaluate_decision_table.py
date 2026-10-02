"""evaluate() の allow / forbid 境界を table-driven で固定する (automationhub#303 / Sonar CC 分割の挙動保存)。

instructions/00 §7 の優先順位 (1) policy 無し → (2) floor / forbid → (3) 評価不能 → (4) 未分類 → (5) 分類あり
を、各段の代表入力と理由コードで 1 行ずつ固定する。分割後も表の各行が同じ Decision を返すことが契約。
"""
import pytest

from agenticstar_platform.policy import (
    Decision,
    EffectivePolicy,
    L1Policy,
    ProjectPolicy,
    evaluate,
    tighten_merge,
)


def _l1(profile, floor=(), version=3):
    return L1Policy.from_row({"version": version, "default_profile": profile, "floor": {"forbid": list(floor)}})


FLOOR = [{"tool": "*", "op_class": "destructive", "args": {"target": "prod*"}}, {"tool": "mcp:kintone:delete_record"}]
ALLOW = ["mcp:gitlab:create_*", "rm_*"]

POLICIES = {
    "open": tighten_merge(_l1("open", FLOOR), ProjectPolicy.from_json({"deny": ["vendor_delete*"]})),
    "guarded": tighten_merge(_l1("guarded"), None),
    "strict": tighten_merge(_l1("strict"), ProjectPolicy.from_json({"allow": ALLOW})),
    # L1=guarded の上に project が strict + allowlist を重ねる (RT-A1: destructive は解除できない)
    "guarded_l1_strict_project": tighten_merge(_l1("guarded"), ProjectPolicy.from_json({"profile": "strict", "allow": ALLOW})),
    # 保存形の読み戻しで forbid が空でも floor は生きる
    "floor_only_from_dict": EffectivePolicy.from_dict({**tighten_merge(None, None).to_dict(), "floor": [{"tool": "rm"}], "forbid": []}),
    # 同じ tool が floor と project deny の両方に掛かる
    "floor_and_deny_overlap": tighten_merge(_l1("open", [{"tool": "mcp:kintone:delete_record"}]),
                                            ProjectPolicy.from_json({"deny": ["mcp:kintone:delete_*"]})),
    # 指示書 28: MCP は external の禁止規則 (接続 ID + glob) だけで止める。strict でも profile 表は通らない
    "strict_external_deny": tighten_merge(_l1("strict"), ProjectPolicy.from_json(
        {"deny": [{"scope": "external", "connection_id": "7", "tool": "create_*"}]})),
}

# (policy, tool, mcp_server, op_class, kwargs) → (mode, reason, matched, unregistered)
TABLE = [
    # (1) policy 取得不能 = fail-closed
    ("none", "read", None, "read", {}, ("forbid", "policy_unavailable", None, False)),
    # (2) floor → forbid (分類の有無に関わらず)
    ("open", "delete_record", "kintone", "destructive", {}, ("forbid", "floor", "mcp:kintone:delete_record", False)),
    ("open", "wipe", None, "destructive", {"args": {"target": "prod-db"}}, ("forbid", "floor", "*", False)),
    ("open", "wipe", None, "destructive", {"args": {"target": "dev-db"}}, ("allow", "profile", None, False)),
    ("open", "wipe", None, "destructive", {"args": "not-a-dict"}, ("forbid", "unevaluable_args", "*", False)),
    ("open", "vendor_delete_all", None, None, {}, ("forbid", "project_forbid", "vendor_delete*", False)),
    ("floor_only_from_dict", "rm", None, "destructive", {}, ("forbid", "floor", "rm", False)),
    # (3) 分類はあるが引数を解釈できない
    ("open", "edit", None, "write", {"args_unparseable": True}, ("forbid", "unevaluable_args", None, False)),
    # (4) 未分類: open / guarded は通す (監査に出す)、strict 相当 (strict / dry_run / delegated) は forbid
    ("open", "mystery", None, None, {}, ("allow", "unknown_tool", None, True)),
    ("guarded", "mystery", None, None, {}, ("allow", "unknown_tool", None, True)),
    ("strict", "mystery", None, None, {}, ("forbid", "unknown_tool", None, True)),
    ("open", "mystery", None, None, {"dry_run": True}, ("forbid", "unknown_tool", None, True)),
    ("open", "mystery", None, None, {"delegated": True}, ("forbid", "unknown_tool", None, True)),
    # 分類語彙外は評価不能
    ("open", "t", None, "unknown_class", {}, ("forbid", "unevaluable_args", None, False)),
    # (5) read は常に allow (dry_run でも)
    ("strict", "t", None, "read", {}, ("allow", "profile", None, False)),
    ("open", "read", None, "read", {"dry_run": True}, ("allow", "profile", None, False)),
    # (5) dry_run は read 以外 forbid
    ("open", "edit", None, "write", {"dry_run": True}, ("forbid", "dry_run_read_only", None, False)),
    # (5) open / guarded の profile 判定
    ("open", "t", None, "write", {}, ("allow", "profile", None, False)),
    ("open", "t", None, "destructive", {}, ("allow", "profile", None, False)),
    ("guarded", "t", None, "write", {}, ("allow", "profile", None, False)),
    # 指示書 28: MCP は profile 表を通らない (呼び元が分類を渡しても無視)
    ("guarded", "merge_merge_request", "gitlab", "destructive", {}, ("allow", "mcp_unrestricted", None, False)),
    # (5) strict / 委譲は allowlist
    ("strict", "edit", None, "write", {}, ("forbid", "strict_allowlist", None, False)),
    ("strict", "create_issue", "gitlab", "write", {}, ("allow", "mcp_unrestricted", None, False)),
    ("strict", "rm_tree", None, "destructive", {}, ("allow", "strict_allowlist", None, False)),
    ("open", "edit", None, "write", {"delegated": True}, ("forbid", "strict_allowlist", None, False)),
    ("guarded", "t", None, "write", {"delegated": True}, ("forbid", "strict_allowlist", None, False)),
    # (5) RT-A1: L1=guarded の禁止クラス (destructive) は project の allowlist で解除できない
    ("guarded_l1_strict_project", "create_issue", "gitlab", "write", {}, ("allow", "mcp_unrestricted", None, False)),
    ("guarded_l1_strict_project", "rm_tree", None, "destructive", {}, ("forbid", "profile", None, False)),
    ("guarded_l1_strict_project", "rm_tree", None, "destructive", {"delegated": True}, ("forbid", "profile", None, False)),
    # フラグの組合せ: dry_run は allowlist / 委譲より先に効く (allowlist 内の write / destructive も forbid)
    ("strict", "create_issue", "gitlab", "write", {"dry_run": True}, ("allow", "mcp_unrestricted", None, False)),  # MCP は dry_run の対象外 (28)
    ("strict", "rm_tree", None, "destructive", {"dry_run": True, "delegated": True}, ("forbid", "dry_run_read_only", None, False)),
    ("open", "t", None, "write", {"dry_run": True, "delegated": True}, ("forbid", "dry_run_read_only", None, False)),
    ("strict", "t", None, "read", {"dry_run": True, "delegated": True}, ("allow", "profile", None, False)),
    # 委譲 + allowlist 内: strict として allowlist が効く (open でも)
    ("strict", "create_issue", "gitlab", "write", {"delegated": True}, ("allow", "mcp_unrestricted", None, False)),
    ("strict", "rm_tree", None, "destructive", {"delegated": True}, ("allow", "strict_allowlist", None, False)),
    ("open", "wipe", None, "destructive", {"delegated": True}, ("forbid", "strict_allowlist", None, False)),
    # 未分類 + args_unparseable は unknown の段で決まる (評価不能の段は分類ありのみ)
    ("open", "mystery", None, None, {"args_unparseable": True}, ("allow", "unknown_tool", None, True)),
    ("strict", "mystery", None, None, {"args_unparseable": True}, ("forbid", "unknown_tool", None, True)),
    # floor と project forbid の両方に掛かる tool は floor が勝つ (照合順)
    ("floor_and_deny_overlap", "delete_record", "kintone", "destructive", {}, ("forbid", "floor", "mcp:kintone:delete_record", False)),
    ("floor_and_deny_overlap", "delete_record", "kintone", "write", {}, ("forbid", "floor", "mcp:kintone:delete_record", False)),
    ("floor_and_deny_overlap", "delete_row", "kintone", "write", {}, ("forbid", "project_forbid", "mcp:kintone:delete_*", False)),
    # forbid 照合は評価不能 / dry_run / 委譲より先 (どのフラグでも floor が理由)
    ("open", "delete_record", "kintone", "destructive", {"dry_run": True, "delegated": True, "args_unparseable": True},
     ("forbid", "floor", "mcp:kintone:delete_record", False)),
    # 指示書 28 (PO 2026-09-22): MCP は実行ルールの対象外。禁止規則に当たらなければ strict / dry_run / 委譲でも allow、
    # 分類なしでも unregistered は立てない。禁止は floor / external の禁止規則 (接続 ID + glob) だけ
    ("strict", "slack_search_channels", "Slack MCP", None, {}, ("allow", "mcp_unrestricted", None, False)),
    ("strict", "slack_send_message", "Slack MCP", None, {"dry_run": True, "delegated": True}, ("allow", "mcp_unrestricted", None, False)),
    ("guarded", "slack_send_message", "Slack MCP", None, {"args_unparseable": True}, ("allow", "mcp_unrestricted", None, False)),
    ("strict_external_deny", "create_issue", "gitlab", None, {"connection_id": "7"}, ("forbid", "project_forbid", "create_*", False)),
    ("strict_external_deny", "list_issues", "gitlab", None, {"connection_id": "7"}, ("allow", "mcp_unrestricted", None, False)),
    ("strict_external_deny", "create_issue", "gitlab", None, {"connection_id": "8"}, ("allow", "mcp_unrestricted", None, False)),
    # external 規則があるのに接続を識別できない MCP 呼び出しは従来どおり forbid (fail-open にしない)
    ("strict_external_deny", "create_issue", "gitlab", None, {}, ("forbid", "unevaluable_args", "create_*", False)),
    # 名前が空白だけでも `mcp=True` の明示で MCP として扱う (組み込みの profile 表に落ちない)
    ("strict", "mystery", "  ", None, {"mcp": True, "connection_id": "9"}, ("allow", "mcp_unrestricted", None, False)),
    # op_class 条件付きの floor (`*` destructive + args) は MCP には掛からない (分類しないため)
    ("open", "wipe", "ops-mcp", "destructive", {"args": {"target": "prod-db"}, "connection_id": "3"}, ("allow", "mcp_unrestricted", None, False)),
]


@pytest.mark.parametrize(("policy_key", "tool", "server", "op_class", "kwargs", "expected"), TABLE,
                         ids=[f"{r[0]}:{r[1]}:{r[3]}:{'/'.join(sorted(r[4])) or '-'}" for r in TABLE])
def test_evaluate_decision_table(policy_key, tool, server, op_class, kwargs, expected):
    policy = None if policy_key == "none" else POLICIES[policy_key]
    d = evaluate(policy, tool, op_class, mcp_server=server, **kwargs)
    assert isinstance(d, Decision)
    assert (d.mode, d.reason, d.matched, d.unregistered) == expected
    assert d.policy_version == (0 if policy is None else policy.policy_version)


def test_every_input_yields_a_binary_decision_without_raising():
    """どの段でも決まらない入力は無い (末尾で必ず Decision)。mode は allow / forbid の二値。"""
    import itertools
    reasons = {"policy_unavailable", "floor", "project_forbid", "unevaluable_args", "unknown_tool",
               "dry_run_read_only", "profile", "strict_allowlist", "mcp_unrestricted"}
    for pk, (tool, srv), oc, args, (au, dr, de) in itertools.product(
        list(POLICIES) + ["none"], [("t", None), ("delete_record", "kintone"), ("rm_x", None), ("", None)],
        [None, "read", "write", "destructive", "weird"], [None, {"target": "prod-1"}, "raw", ["l"]],
        itertools.product([False, True], repeat=3),
    ):
        d = evaluate(None if pk == "none" else POLICIES[pk], tool, oc, args=args, args_unparseable=au,
                     dry_run=dr, delegated=de, mcp_server=srv)
        assert d.mode in ("allow", "forbid") and d.reason in reasons, (pk, tool, oc, args, au, dr, de)
        if pk == "none" or (oc == "weird" and srv is None):
            assert d.mode == "forbid"
        if srv is not None and d.mode == "allow":
            # MCP は実行ルールの対象外 (28): allow の理由は常に mcp_unrestricted で、unregistered は立てない
            assert d.reason == "mcp_unrestricted" and not d.unregistered, (pk, tool, oc, args, au, dr, de)
            continue
        if d.mode == "allow":
            # 締める方向のフラグは allow を作らない: dry_run は read 以外を通さない、委譲は allowlist / read 以外を通さない、
            # 分類ありで引数解釈不能は通さない
            assert not (dr and oc != "read"), (pk, tool, oc, args, au, dr, de)
            assert not (de and oc not in ("read", None) and d.reason != "strict_allowlist"), (pk, tool, oc, dr, de)
            assert not (au and oc is not None), (pk, tool, oc, au)
