"""
agenticstar_platform.policy — tool 呼び出しの統制ポリシー (純計算。I/O もフレームワーク依存も無い)。

「この tool 呼び出しを許すか」を、2 層のポリシーを合成した結果 (EffectivePolicy) に対して二値で判定する。

- 2 層: **テナント層** (L1Policy: 既定の profile、誰も緩められない floor、根拠本文の保持可否、version) と
  **プロジェクト層** (ProjectPolicy: profile、deny / allow のパターン、gate の設定)。
  tighten_merge が保証するのは 2 つ: **floor はプロジェクトで外せない**、**profile はテナントの既定より緩く
  できない** (rank は下がらない)。注意: strict の allowlist はプロジェクトが明示した write / destructive を
  許すので、テナントが guarded で禁止していた destructive を、プロジェクトが strict + allow で許すことはできる
  (floor に入っていないもの)。テナントとして必ず禁止したいものは floor に入れる。
- profile は `open < guarded < strict` の順に厳しい。open = 全て allow、guarded = destructive を forbid、
  strict = allowlist (read は allow、write / destructive はプロジェクトの allow に明示されたものだけ)。
- 判定 (evaluate) の順: (1) policy が無い → forbid (2) floor / 明示 deny のパターン一致 → forbid
  (3) 分類はあるが引数を解釈できない → forbid (4) 分類に無い tool (unknown) → open / guarded は allow
  (`unregistered=True` を立てる)、strict / 委譲 / dry_run は forbid (5) 分類あり → profile の表。
  `dry_run=True` は profile によらず read 以外を forbid する (読むだけの実行)。
- **MCP のツールは (2) の後で allow** (`mcp_unrestricted`)。操作クラスで分類せず、profile / dry_run / 委譲の
  対象外。禁止は floor と明示の禁止規則 (external の接続 ID + glob) だけ (3.0req 指示書 28、PO 2026-09-22)。
- **A2A 外部 Agent への送信も (2) の後で allow** (`a2a_unrestricted`)。`evaluate(..., connection_kind="a2a",
  connection_id=<a2a_agent_configurations.id>)`。禁止は floor / 明示の禁止規則の **接続 (Agent) 単位**
  (`{scope: external, connection_kind: a2a, connection_id}`。tool 無し) と scope 無しの tool 名 glob だけ。
  MCP の規則と A2A の規則は互いに掛からない (整数 ID は別の表 = 種別と ID の組で照合)。A2A 規則を含む policy は
  schema 4 (3.0req 指示書 30、PO 2026-09-23)。
- 解決結果 (EffectivePolicy) は `to_dict()` / `from_dict()` で保存・復元でき、`digest` (SHA-256) で
  「どの設定で判定したか」を後から突き合わせられる。

公開 API:
    Profile / Mode / GateMode        列挙と順序 (`profile_rank` / `tighten_profile`)
    L1Policy / ProjectPolicy         入力 (DB 行 / JSON からの from_* 付き)
    EffectivePolicy                  解決結果 (`to_dict()` / `digest` / `from_dict()`)
    tighten_merge(l1, project)       2 層の解決
    evaluate(policy, tool, op_class, args=..., dry_run=..., delegated=..., mcp_server=...)
    Decision                         mode (allow | forbid) / reason / policy_version / unregistered
    policy_digest(effective)         EffectivePolicy の SHA-256 (snapshot の照合用)

op_class は呼び出し側が tool を read / write / destructive に分類して渡す (分類表は SDK の外)。
mcp_server を渡すと `mcp:<server>:<tool>` と `<tool>` の 2 通りでパターンに照合する。

設計の出典 (ASTER 内部): devdocs docs/3.0req/instructions/00_shared_contracts.md §7。
"""
from .internal_operations import (
    MAPPING_VERSION as INTERNAL_OPERATIONS_MAPPING_VERSION,
    internal_operation_kinds,
    internal_operation_mapping,
    kind_tools,
)
from .model import (
    SCHEMA_VERSION_SCOPED,
    SCHEMA_VERSION_TYPED_CONNECTION,
    SUPPORTED_SCHEMA_VERSIONS,
    CONNECTION_KINDS,
    LOCAL_CONNECTION,
    verify_connections,
    requires_schema,
    PROFILE_ORDER,
    Decision,
    EffectivePolicy,
    ForbidPattern,
    GateMode,
    L1Policy,
    Mode,
    Profile,
    ProjectPolicy,
    evaluate,
    policy_digest,
    profile_rank,
    tighten_merge,
    profile_permits,
    tighten_profile,
)

__all__ = [
    "PROFILE_ORDER", "Decision", "EffectivePolicy", "ForbidPattern", "GateMode", "L1Policy",
    "Mode", "Profile", "ProjectPolicy", "evaluate", "policy_digest", "profile_rank",
    "tighten_merge", "tighten_profile",
    "profile_permits",
    "SCHEMA_VERSION_SCOPED", "SCHEMA_VERSION_TYPED_CONNECTION", "SUPPORTED_SCHEMA_VERSIONS", "CONNECTION_KINDS",
    "verify_connections", "LOCAL_CONNECTION", "requires_schema",
    "INTERNAL_OPERATIONS_MAPPING_VERSION", "internal_operation_kinds", "internal_operation_mapping", "kind_tools",
]
