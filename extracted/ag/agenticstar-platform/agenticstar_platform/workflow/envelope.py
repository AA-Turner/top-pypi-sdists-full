"""completion_envelope (version 2) と effect tally（marketplace-3.0 00 §7、03 §4。3.0req 指示書 25）。

- outcome は「どう終わったか」の 7 値: completed / incomplete / failed / timeout / stopped / denied / skipped。
  **成否 = Agent が完遂したか**。Agent の関数が正常に戻れば `completed`。write の失敗・未観測の効果・tool 記録が無いことは
  outcome を下げない（Agent が完遂できなかったなら、Agent が例外で終わる）。何を書いたかは `counts` / `tools` / `had_mutating_success` の側に残す
- tally は runner が保存済み（ack 済み）監査から数える
- mutating な tool.invoked は **呼出し（invoked event_id）単位** で effect の status を対応付け、成功 / 失敗 / 不明を区別する
  （`action_ref` は外部の冪等キーで、集計キーではない = 同じ action_ref を共有する 2 回の呼出しが結果を共有しない）
- **再実行してよいかは outcome ではなく「効果が不明か」で決まる**: `had_mutating_success` は 成功を観測 = true / 効果なしと確定 = false /
  **不明 = null**（監査の保存失敗、effect が無い・status が unknown の write、runner の再起動・停止・cleanup 未完）。
  front は null の不成功を自動 retry せず人へ回す（重複 write を避ける）。既発生の成功（true）はどの outcome でも消さない
- 拒否（tool.denied）は成功 / 必須 output より優先して `denied`。permitted skip は front と同じ理由（`SKIP_REASONS`）、
  `policy_unavailable` は外部行為前の再照合用
- tally は runner の state file に journal し、再起動後も観測を 0 に戻さない
- front の completion 保存 API は `version: 2` を要求し、SaaS / executor の保存形は `envelope_version: 2`。両方を載せる
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Optional

ENVELOPE_VERSION = 2
OUTCOMES = ("completed", "incomplete", "failed", "timeout", "stopped", "denied", "skipped")
MUTATING_EFFECT_KINDS = ("write", "create", "update", "delete", "send", "mutate")
SUCCESS_STATUSES = ("ok", "success", "succeeded")
FAILED_STATUSES = ("error", "failed", "failure", "rejected")
# front `completion.js` PROCEED_SKIP_REASONS: これだけ次工程へ進める skip 理由
SKIP_REASONS = ("no_target", "not_applicable", "nothing_to_do")
# 外部行為の **前** に policy を照合できなかった: front は budget 内で再照合（retryOrHold）する。次工程へは進めない
PRE_ACTION_SKIP_REASONS = ("policy_unavailable",)
_REASON_RE = re.compile(r"^[a-z][a-z0-9_]{0,31}$")


def reason_code(value: Any, default: str) -> str:
    v = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    return v if _REASON_RE.match(v) else default


@dataclass
class EffectTally:
    """保存済み（ack 済み）監査から集計する。ack されていない event は数えない。"""
    invoked: dict[str, dict[str, Any]] = field(default_factory=dict)   # invoked event_id -> metadata
    effects: dict[str, dict[str, Any]] = field(default_factory=dict)   # invoked event_id -> effect metadata（成功は sticky）
    effect_conflicts: int = 0                                          # 成功観測の後に届いた別 status（成功を消さない）
    orphan_effects: int = 0                                            # 対応する invoked が無い effect = 帰属不明の効果（hold）
    denials: list[str] = field(default_factory=list)                   # reason codes
    persist_failures: int = 0                                          # 必須監査（manifest / invoked / effect / denied）の保存失敗
    skip_reason: Optional[str] = None                                  # Agent が宣言した skip 理由（SKIP_REASONS / PRE_ACTION）

    def record(self, event_type: str, event_id: str, metadata: dict[str, Any], reason: Optional[str] = None) -> None:
        if event_type == "tool.invoked":
            self.invoked[event_id] = dict(metadata)
        elif event_type == "tool.effect":
            ref = str(metadata.get("invoked_event_id") or "")
            if ref and ref in self.invoked:
                prev = self.effects.get(ref)
                if prev is not None and self._status_of(prev) == "ok":
                    self.effect_conflicts += 1   # 既に観測した成功は後の報告で消さない（sticky）
                else:
                    self.effects[ref] = dict(metadata)
            else:
                self.orphan_effects += 1         # どの呼出しの効果か確定できない → 効果不明として hold
        elif event_type == "tool.denied":
            self.denials.append(reason_code(metadata.get("reason_code") or reason, "tool_denied"))

    # ----- journal（再起動後に観測を失わない） -----
    def to_dict(self) -> dict[str, Any]:
        return {"invoked": self.invoked, "effects": self.effects, "orphan_effects": self.orphan_effects,
                "effect_conflicts": self.effect_conflicts, "denials": list(self.denials),
                "persist_failures": self.persist_failures, "skip_reason": self.skip_reason}

    @classmethod
    def from_dict(cls, data: Any) -> "EffectTally":
        t = cls()
        if not isinstance(data, dict):
            return t
        inv = data.get("invoked")
        eff = data.get("effects")
        t.invoked = {str(k): dict(v) for k, v in inv.items() if isinstance(v, dict)} if isinstance(inv, dict) else {}
        t.effects = {str(k): dict(v) for k, v in eff.items() if isinstance(v, dict)} if isinstance(eff, dict) else {}
        t.orphan_effects = int(data.get("orphan_effects") or 0)
        t.effect_conflicts = int(data.get("effect_conflicts") or 0)
        t.denials = [reason_code(d, "tool_denied") for d in (data.get("denials") or []) if isinstance(d, str)]
        t.persist_failures = int(data.get("persist_failures") or 0)
        sr = data.get("skip_reason")
        t.skip_reason = sr if sr in SKIP_REASONS + PRE_ACTION_SKIP_REASONS else None
        return t

    @property
    def mutating_invoked(self) -> list[str]:
        return [eid for eid, m in self.invoked.items() if str(m.get("effect_kind") or "") in MUTATING_EFFECT_KINDS]

    @staticmethod
    def _status_of(eff: dict[str, Any]) -> str:
        s = str(eff.get("status") or "ok").lower()
        if s in SUCCESS_STATUSES:
            return "ok"
        if s in FAILED_STATUSES:
            return "failed"
        return "unknown"

    def _status(self, eid: str) -> str:
        eff = self.effects.get(eid)
        if eff is None:
            return "unobserved"
        return self._status_of(eff)

    @property
    def mutating_success(self) -> int:
        return sum(1 for e in self.mutating_invoked if self._status(e) == "ok")

    @property
    def mutating_failed(self) -> int:
        return sum(1 for e in self.mutating_invoked if self._status(e) == "failed")

    @property
    def mutating_unresolved(self) -> int:
        """effect が無い（未観測）または不明 = 効果不明。帰属不明の effect（orphan）も 1 件ずつ数える。"""
        return sum(1 for e in self.mutating_invoked if self._status(e) in ("unobserved", "unknown")) + self.orphan_effects

    @property
    def observed_reads(self) -> int:
        return sum(1 for m in self.invoked.values() if str(m.get("effect_kind") or "") not in MUTATING_EFFECT_KINDS)

    @property
    def denied(self) -> int:
        return len(self.denials)

    def counts(self) -> dict[str, int]:
        return {
            # tool_calls / read_calls / mutating_success / mutating_failed は SaaS の worker と同じキー (front / admin / executor の
            # 実行記録とエクスポートが共通に読む)。それ以外は SDK が呼出し単位で観測したもの
            "tool_calls": len(self.invoked),
            "read_calls": self.observed_reads,
            "mutating_invoked": len(self.mutating_invoked),
            "mutating_success": self.mutating_success,
            "mutating_failed": self.mutating_failed,
            "mutating_unresolved": self.mutating_unresolved,
            "orphan_effects": self.orphan_effects,
            "effect_conflicts": self.effect_conflicts,
            "denied": self.denied,
            "audit_persist_failures": self.persist_failures,
        }

    def tools(self) -> list[dict[str, Any]]:
        out = []
        for eid, m in list(self.invoked.items())[:100]:
            out.append({"tool": str(m.get("tool") or m.get("tool_name") or "")[:200], "effect_kind": str(m.get("effect_kind") or ""),
                        "status": self._status(eid)})
        return out


def decide_outcome(*, tally: EffectTally, agent_error: Optional[str], stop_reason: Optional[str],
                   outputs_collected: int, required_missing: list[str], effect_mode: str,
                   collection_failed: bool = False, effects_uncertain: bool = False) -> tuple[str, str, Optional[bool]]:
    """(outcome, outcome_reason_code, had_mutating_success)。優先順位（00 §7 / 03 §4）:
    監査保存失敗 → 取消 → 期限 → 他所終端 → runner 停止 → 拒否 → 例外
    → 回収失敗（宣言 output が不正 / 読めない。skip でも隠さない）→ skip（成功が無い場合。skip = 成果物を作らないので
    必須 output の **欠落** より先）→ 必須 output 欠落 → 完遂。

    write の失敗・未観測の効果・観測 0 件は outcome を決めない（成否 = Agent が完遂したか）。それらは
    `had_mutating_success`（true / false / **None = 不明**）と counts に残り、front はそこから再実行の可否を決める。
    `effects_uncertain`: runner が Agent の結果を観測し切れていない（再起動 / cleanup 未完）ことを呼び出し側が渡す。"""
    succeeded = tally.mutating_success > 0
    unknown = bool(tally.persist_failures or tally.mutating_unresolved or effects_uncertain
                   or stop_reason in ("terminal", "stopped"))
    had: Optional[bool] = True if succeeded else (None if unknown else False)
    if tally.persist_failures:
        return "failed", "audit_persist_failed", had
    if stop_reason == "cancel":
        return "stopped", "cancelled", had
    if stop_reason == "deadline":
        return "timeout", "execution_timeout", had
    if stop_reason == "terminal":
        return "stopped", "terminal_elsewhere", had
    if stop_reason == "stopped":
        # runner 自身が停止 signal（K8s の Pod 停止）で止まった: 実行環境の異常。Agent の結果を観測し切れていないので効果は不明
        return "failed", "runner_stopped", had
    if tally.denied:
        return "denied", tally.denials[0], had        # 成功 / 必須 output より優先（front は hold / on_denied）
    if agent_error:
        return "failed", "agent_error", had
    if collection_failed:
        return "failed", "output_invalid", had        # 宣言 output の検証 / 読取失敗は skip / 成功で隠さない
    if tally.skip_reason in PRE_ACTION_SKIP_REASONS and tally.mutating_invoked:
        # 「外部行為の前に policy を照合できなかった」は、write を 1 件でも呼んだ後には成り立たない (その write が成功していても
        # 同じ)。skipped/policy_unavailable は front が認定に関わらず再照合 (再実行) するので名乗らせず、完遂にもしない
        return "failed", "skip_after_effect", had
    if tally.skip_reason and not succeeded:
        return "skipped", tally.skip_reason, had
    if required_missing:
        return "failed", "required_output_missing", had
    return "completed", "completed", had


def build_envelope(*, outcome: str, reason: str, had_mutating_success: Optional[bool], tally: EffectTally,
                   error_class: Optional[str] = None, runner: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """`runner`: runner 自身の終わり方（停止理由 / 再起動 / cleanup 未完）。Agent の成否ではなく実行環境の記録。"""
    if outcome not in OUTCOMES:
        raise ValueError(f"unknown outcome {outcome}")
    return {
        "version": ENVELOPE_VERSION,
        "envelope_version": ENVELOPE_VERSION,
        "outcome": outcome,
        "outcome_reason_code": reason,
        "had_mutating_success": had_mutating_success if had_mutating_success is None else bool(had_mutating_success),
        "counts": tally.counts(),
        "tools": tally.tools(),
        "resumed": False,
        "error_class": error_class,
        "runner": runner,
        "written_by": "agenticstar-platform-sdk",
    }
