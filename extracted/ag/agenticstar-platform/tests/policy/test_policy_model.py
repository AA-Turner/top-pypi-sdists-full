"""agenticstar_platform.policy — R-C1 / R-C2 の 2 層解決と二値判定（instructions/00 §7）。"""
import json
import pytest

from agenticstar_platform.policy import (
    Decision,
    EffectivePolicy,
    ForbidPattern,
    L1Policy,
    ProjectPolicy,
    evaluate,
    policy_digest,
    tighten_merge,
    profile_permits,
    tighten_profile,
)


def _l1(profile="open", floor=(), version=1):
    return L1Policy.from_row({"version": version, "default_profile": profile,
                              "floor": {"forbid": list(floor)}, "retain_rationale_body": False})


def test_tighten_profile_only_tightens():
    assert tighten_profile("open", "guarded") == "guarded"
    assert tighten_profile("strict", "open") == "strict"
    assert tighten_profile(None, None) == "open"
    with pytest.raises(ValueError):
        tighten_profile("open", "lenient")


def test_tighten_merge_keeps_floor_first_and_l1_none_is_open():
    eff = tighten_merge(None, None)
    assert eff.profile == "open" and eff.forbid == () and eff.policy_version == 0
    l1 = _l1("guarded", floor=[{"tool": "mcp:kintone:delete_*"}], version=7)
    prj = ProjectPolicy.from_json({"profile": "open", "deny": ["bash"], "allow": ["gitlab.create_*"],
                                   "gate": {"mode": "blocking"}})
    eff = tighten_merge(l1, prj, project_id="p1")
    assert eff.profile == "guarded"                  # project は緩められない
    assert [f.tool for f in eff.floor] == ["mcp:kintone:delete_*"] and [f.tool for f in eff.forbid] == ["bash"]
    assert eff.allow == ("gitlab.create_*",)
    assert eff.policy_version == 7 and eff.gate == {"mode": "blocking"} and eff.project_id == "p1"
    again = EffectivePolicy.from_dict(eff.to_dict())   # executions.effective_policy 往復
    assert again == eff and policy_digest(again) == eff.digest and len(eff.digest) == 64


def test_project_policy_accepts_front_shape_and_rejects_garbage():
    assert ProjectPolicy.from_json('{"deny": [], "profile": "open"}').profile == "open"  # sbtest の実データ形
    assert ProjectPolicy.from_json(None) is None
    with pytest.raises(ValueError):
        ProjectPolicy.from_json({"profile": "root"})
    with pytest.raises(ValueError):
        ForbidPattern.parse({"args": {"x": "1"}})  # tool 必須


def test_evaluate_priority_order():
    l1 = _l1("open", floor=[{"tool": "*", "op_class": "destructive", "args": {"target": "prod*"}},
                            {"tool": "mcp:kintone:delete_record"}])
    eff = tighten_merge(l1, ProjectPolicy.from_json({"deny": ["vendor_delete*"]}))
    assert evaluate(None, "read", "read") == Decision("forbid", "policy_unavailable", 0)
    d = evaluate(eff, "delete_record", "destructive", mcp_server="kintone")
    assert d.mode == "forbid" and d.reason == "floor" and d.matched == "mcp:kintone:delete_record"
    d = evaluate(eff, "wipe", "destructive", args={"target": "prod-db"})
    assert (d.mode, d.reason) == ("forbid", "floor")
    assert evaluate(eff, "wipe", "destructive", args={"target": "dev-db"}).mode == "allow"   # open
    assert evaluate(eff, "wipe", "destructive", args="not-a-dict").reason == "unevaluable_args"
    d = evaluate(eff, "vendor_delete_all", None)
    assert (d.mode, d.reason) == ("forbid", "project_forbid")                       # 未分類でも止まる
    assert evaluate(eff, "edit", "write", args_unparseable=True).reason == "unevaluable_args"
    d = evaluate(eff, "mystery", None)
    assert d.mode == "allow" and d.unregistered is True and d.reason == "unknown_tool"
    assert evaluate(eff, "mystery", None, dry_run=True).mode == "forbid"
    assert evaluate(eff, "mystery", None, delegated=True).mode == "forbid"


def test_profile_matrix_and_dry_run():
    open_ = tighten_merge(_l1("open"), None)
    guarded = tighten_merge(_l1("guarded"), None)
    strict = tighten_merge(_l1("strict"), ProjectPolicy.from_json({"allow": ["rm_*"]}))
    for cls in ("read", "write", "destructive"):
        assert evaluate(open_, "t", cls).mode == "allow"
    assert evaluate(guarded, "t", "read").mode == "allow"
    assert evaluate(guarded, "t", "write").mode == "allow"
    assert evaluate(guarded, "rm_tree", "destructive").mode == "forbid"
    # 指示書 28: MCP は profile 表の対象外 (guarded の destructive 禁止も掛からない)
    assert evaluate(guarded, "merge_merge_request", "destructive", mcp_server="gitlab").reason == "mcp_unrestricted"
    assert evaluate(strict, "t", "read").mode == "allow"
    assert evaluate(strict, "edit", "write").mode == "forbid"                               # allowlist 外
    assert evaluate(strict, "rm_tree", "destructive").mode == "allow"                        # allowlist
    assert evaluate(strict, "create_issue", "write", mcp_server="gitlab").reason == "mcp_unrestricted"  # MCP は allowlist 不要 (28)
    assert evaluate(open_, "edit", "write", dry_run=True).reason == "dry_run_read_only"
    assert evaluate(open_, "read", "read", dry_run=True).mode == "allow"
    assert evaluate(open_, "edit", "write", delegated=True).mode == "forbid"                # 委譲は strict 固定
    assert evaluate(open_, "t", "unknown_class").reason == "unevaluable_args"


def test_project_allow_never_widens_l1_permission_set():
    """RT-A1: project を重ねた許可集合 ⊆ **同じ allowlist を持つ L1 profile** の許可集合。

    00 §7 では allowlist は projects.policy だけが持つ (L1 に allowlist は無い) ので、「L1 単独」の許可集合は
    allowlist を固定して比べる。project が変えられるのは profile / deny / allow で、profile を上げる (guarded→strict)
    ことで allowlist が guarded の禁止クラス (destructive) を解除する経路が唯一の広がり = ここを塞ぐ。
    delegated (strict 固定) / dry_run / unknown / floor / deny は締める方向しかないことも同じ比較で確認する。"""
    allow = ["mcp:gitlab:*", "rm_*", "x"]
    cases = (("create_issue", "gitlab", "write"), ("merge_merge_request", "gitlab", "destructive"),
             ("rm_tree", None, "destructive"), ("x", None, "write"), ("x", None, "destructive"),
             ("edit", None, "write"), ("read", None, "read"), ("vendor_tool", None, None))
    floor = ProjectPolicy.from_json({"deny": ["*delete*"]})  # L1 floor の代用 (下で L1 側に載せる)
    for l1_profile in ("open", "guarded", "strict"):
        l1 = L1Policy(version=3, default_profile=l1_profile, floor=floor.deny)
        baseline = tighten_merge(l1, ProjectPolicy.from_json({"allow": allow}))  # L1 profile + 同じ allowlist
        for project in ({"profile": "strict", "allow": allow}, {"profile": "guarded", "allow": allow},
                        {"profile": "strict", "allow": allow, "deny": ["rm_*"]}):
            merged = tighten_merge(l1, ProjectPolicy.from_json(project))
            assert merged.l1_profile == l1_profile
            for tool, server, cls in cases:
                for flags in ({}, {"delegated": True}, {"dry_run": True}):
                    base = evaluate(baseline, tool, cls, mcp_server=server, **flags).mode
                    got = evaluate(merged, tool, cls, mcp_server=server, **flags).mode
                    assert not (base == "forbid" and got == "allow"), (l1_profile, project, tool, cls, flags)
    # 再現ケース: L1=guarded (destructive forbid) + project strict/allow → destructive は forbid (理由 profile) のまま
    merged = tighten_merge(_l1("guarded"), ProjectPolicy.from_json({"profile": "strict", "allow": allow}))
    got = evaluate(merged, "x", "destructive")
    assert got.mode == "forbid" and got.reason == "profile"
    assert evaluate(merged, "x", "write").reason == "strict_allowlist"  # write は範囲内
    # MCP は profile / allowlist の対象外 (28): L1=guarded でも禁止規則に当たらなければ allow
    assert evaluate(merged, "merge_merge_request", "destructive", mcp_server="gitlab").reason == "mcp_unrestricted"
    assert evaluate(merged, "x", "destructive", delegated=True).mode == "forbid"  # 委譲でも解除しない
    # L1=open / strict では allowlist が write / destructive とも効く (allowlist は strict の機構そのもの)
    for l1_profile in ("open", "strict"):
        m = tighten_merge(_l1(l1_profile), ProjectPolicy.from_json({"profile": "strict", "allow": allow}))
        assert evaluate(m, "rm_tree", "destructive").reason == "strict_allowlist"
    # 保存 → 読み戻しで同じ判定 / digest
    again = EffectivePolicy.from_dict(json.loads(json.dumps(merged.to_dict())))
    assert again.to_dict() == merged.to_dict() and again.digest == merged.digest
    assert evaluate(again, "x", "destructive").mode == "forbid"
    # 保存形の検証: l1_profile 欠落 / profile が l1_profile より緩い → 読めない (fail-closed)
    for bad in ({k: v for k, v in merged.to_dict().items() if k != "l1_profile"},
                {**merged.to_dict(), "profile": "open"}, {**merged.to_dict(), "l1_profile": "loose"}):
        with pytest.raises(ValueError):
            EffectivePolicy.from_dict(bad)
    # 直接構築 (l1_profile 省略) は profile を上限とみなす
    direct = EffectivePolicy(profile="strict", floor=(), forbid=(), allow=("x",), policy_version=1)
    assert direct.l1_bound == "strict" and direct.to_dict()["l1_profile"] == "strict"
    assert profile_permits("guarded", "destructive") is False and profile_permits("guarded", "write") is True
    assert profile_permits("open", "destructive") is True and profile_permits("strict", "destructive") is True


def test_from_dict_is_fail_closed_and_args_normalization_is_symmetric():
    import pytest as _pytest
    base = tighten_merge(None, None).to_dict()
    for bad in ({}, {"profile": "open"}, {**base, "schema_version": 99}, {**base, "floor": "nope"},
                {**base, "profile": None}, {**base, "profile": False}, {**base, "profile": ""},
                {**base, "schema_version": True}, {**base, "schema_version": 1.9}, {**base, "policy_version": True},
                {**base, "policy_version": "7"}):
        with _pytest.raises(ValueError):
            EffectivePolicy.from_dict(bad)
    # floor だけで forbid が空でも floor は効く (evaluate は floor → forbid の順)
    eff = EffectivePolicy.from_dict({**tighten_merge(None, None).to_dict(), "floor": [{"tool": "rm"}], "forbid": []})
    assert evaluate(eff, "rm", "destructive").reason == "floor"
    # 条件値 false と実引数 False が同じ規則で正規化される
    pat = ForbidPattern.parse({"tool": "deploy", "args": {"force": False, "count": 3, "tags": ["a", "b"]}})
    eff = EffectivePolicy.from_dict({**tighten_merge(None, None).to_dict(), "forbid": [pat.to_dict()]})
    assert evaluate(eff, "deploy", "write", args={"force": False, "count": 3, "tags": ["a", "b"]}).reason == "project_forbid"
    assert evaluate(eff, "deploy", "write", args={"force": True, "count": 3, "tags": ["a", "b"]}).mode == "allow"
