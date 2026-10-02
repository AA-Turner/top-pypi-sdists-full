"""統制ポリシーのモデルと判定 (ASTER 3.0 R-C1 / R-C2)。純 Python、I/O 無し。"""
from __future__ import annotations

import fnmatch
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Literal

Profile = Literal["open", "guarded", "strict"]
Mode = Literal["allow", "forbid"]
GateMode = Literal["notify_only", "blocking"]
OpClass = Literal["read", "write", "destructive"]

PROFILE_ORDER: tuple[str, ...] = ("open", "guarded", "strict")
GATE_MODE_ORDER: tuple[str, ...] = ("notify_only", "blocking")
OP_CLASSES: tuple[str, ...] = ("read", "write", "destructive")

#: policy 取得不能 (fail-closed) の理由コード
REASON_POLICY_UNAVAILABLE = "policy_unavailable"
REASON_FLOOR = "floor"
REASON_PROJECT_FORBID = "project_forbid"
REASON_UNEVALUABLE = "unevaluable_args"
REASON_UNKNOWN_TOOL = "unknown_tool"
REASON_DRY_RUN = "dry_run_read_only"
REASON_PROFILE = "profile"
REASON_ALLOWLIST = "strict_allowlist"
#: MCP のツールは実行ルール (profile / dry_run / 委譲 / 操作クラス) の対象外 = floor と明示の禁止規則に当たらなければ allow
#: (3.0req 指示書 28、PO 2026-09-22)
REASON_MCP_UNRESTRICTED = "mcp_unrestricted"
#: A2A 外部 Agent への送信も MCP と同じく実行ルールの対象外 = floor と明示の禁止規則 (connection_kind a2a + 接続 ID、
#: scope 無しの tool 名 glob) に当たらなければ allow (3.0req 指示書 30、PO 2026-09-23)
REASON_A2A_UNRESTRICTED = "a2a_unrestricted"

_SCHEMA_VERSION = 2  # 2 (1.0.0a3): l1_profile を追加 (project の allow が L1 の禁止クラスを解除しない = 許可集合の包含)
#: 3 (1.0.2、MT-A08 / MT-R06): scope 付き forbid (internal = 操作種別、external = 接続先 + メソッド名) を含む policy だけ
#: この版になる。scope 付きの規則が無ければ従来どおり 2 で保存する (既存 snapshot / digest / 旧 reader は不変)。
#: 旧 reader (1.0.1) は 3 を「未対応の版」として拒否する = policy 取得不能 = 全 forbid (禁止を黙って無視しない)
SCHEMA_VERSION_SCOPED = 3
#: 4 (3.0.4、3.0req 指示書 30): external 規則が接続の**種別** (`connection_kind` = mcp | a2a) を持つ。A2A 外部 Agent を接続 ID で
#: 禁止する規則 (`connection_kind: "a2a"`、tool 無し) を含む policy だけこの版になる。MCP 規則だけの policy は 3 のまま
#: (保存形に connection_kind を出さない = 既存 snapshot / digest / 旧 reader は不変)。旧 reader (≤ 3.0.3) は 4 を
#: 「未対応の版」として拒否する = policy 取得不能 = 全 forbid (A2A の禁止を黙って落として通さない)。
#: `connection_id` に "a2a:" を埋め込む案は、旧 reader が MCP 規則として読んで **黙って素通り** するので採らない。
SCHEMA_VERSION_TYPED_CONNECTION = 4
SUPPORTED_SCHEMA_VERSIONS: tuple[int, ...] = (_SCHEMA_VERSION, SCHEMA_VERSION_SCOPED, SCHEMA_VERSION_TYPED_CONNECTION)
SCOPES: tuple[str, ...] = ("internal", "external")
#: external 規則が指す接続の種別。mcp = `mcp_server_configurations.id`、a2a = `a2a_agent_configurations.id`。
#: どちらも整数 ID で別の表なので、**種別と ID の組**で照合する (指示書 30 決定 2)。
CONNECTION_KINDS: tuple[str, ...] = ("mcp", "a2a")
#: evaluate の `connection_id` に渡す「worker 内蔵の MCP (DB 登録の接続ではない)」の印。external 規則の対象外
#: (mcp_server_configurations.id は整数なので衝突しない)。None は「識別できない」= 判定不能 (forbid) で、これとは別
LOCAL_CONNECTION = "local"

from .internal_operations import (  # noqa: E402 - 定数の後に置く (循環無し)
    MAPPING_VERSION as INTERNAL_OPERATIONS_MAPPING_VERSION,
    is_supported_mapping_version,
    kind_tools,
)


def profile_rank(profile: str | None) -> int:
    p = (profile or "open").strip().lower()
    if p not in PROFILE_ORDER:
        raise ValueError(f"unknown profile: {profile!r}")
    return PROFILE_ORDER.index(p)


def tighten_profile(a: str | None, b: str | None) -> str:
    """2 つの profile の厳しい方（project は L1 を緩められない）。"""
    return PROFILE_ORDER[max(profile_rank(a), profile_rank(b))]


def _arg_text(value: Any) -> str:
    """引数値 / 条件値を同じ規則で文字列化する (bool → true/false、None → null、数値は JSON 表記、
    dict / list は canonical JSON)。条件側・実引数側で非対称にならないように必ずこれを通す。"""
    if isinstance(value, str):
        return value
    if value is None or isinstance(value, (bool, int, float)):
        return json.dumps(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def _norm_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


@dataclass(frozen=True)
class ForbidPattern:
    """forbid のパターン。`tool` は fnmatch glob（MCP は `mcp:<server>:<tool>` と `<tool>` の両方で照合）、
    `args` は引数名 → 値の glob（すべて一致したときだけ該当。条件値も実引数も `_arg_text` で同じ規則
    （bool → true/false、None → null、数値は JSON 表記、dict / list は canonical JSON）に文字列化し、
    完全一致 → glob の順で照合）。
    `op_class` を指定すると、そのクラスの操作だけに掛かる（例: {"tool": "*", "op_class": "destructive"}）。
    """
    tool: str
    args: dict[str, str] = field(default_factory=dict)
    op_class: str | None = None
    note: str | None = None
    #: MT-A08 / MT-R06 (schema 3): scope 無し = 従来 (candidates への glob 照合。意味を変えない)。
    #: internal = 組み込み tool の操作種別 (`kind` + `mapping_version`。同名の MCP メソッドには掛からない)。
    #: external = 顧客が設定した接続先 (`connection_id` = mcp_server_configurations の ID) のメソッド名 (`tool` = glob)。
    #: 照合は **接続の ID** (evaluate の `connection_id`) で行う。接続の名前は管理者が自由に付ける表示用の文字列で、
    #: 識別子には使わない (3.0req 指示書 26。3.0.1 までの `server` ラベル = 名前への束縛は廃止)。
    scope: str | None = None
    kind: str | None = None
    mapping_version: int | None = None
    connection_id: str | None = None
    #: external 規則の接続の種別 (CONNECTION_KINDS)。mcp = 従来 (メソッド glob あり)、a2a = A2A 外部 Agent (接続単位。tool 無し。
    #: 送信単位が message で skill を指定できない = tool 粒度の禁止は強制できないので持たない。指示書 30 決定 1)。
    #: internal / scope 無しは None
    connection_kind: str | None = None

    @classmethod
    def parse(cls, raw: Any) -> ForbidPattern:
        if isinstance(raw, str):
            text = raw.strip()
            if not text:
                raise ValueError("empty forbid pattern")
            return cls(tool=text)
        if isinstance(raw, dict):
            args = raw.get("args") or {}
            if not isinstance(args, dict):
                raise ValueError("forbid pattern 'args' must be an object")
            op_class = raw.get("op_class")
            if op_class is not None and op_class not in OP_CLASSES:
                raise ValueError(f"forbid pattern 'op_class' must be one of {OP_CLASSES}")
            note = str(raw["note"])[:200] if raw.get("note") else None
            norm_args = {str(k): _arg_text(v) for k, v in args.items()}
            scope = raw.get("scope")
            if scope is not None:
                if scope not in SCOPES:
                    raise ValueError(f"forbid pattern 'scope' must be one of {SCOPES}")
                if scope == "internal":
                    kind = str(raw.get("kind") or "").strip()
                    mv = raw.get("mapping_version", INTERNAL_OPERATIONS_MAPPING_VERSION)
                    if not is_supported_mapping_version(mv):
                        raise ValueError(f"unsupported internal operations mapping_version: {mv!r}")
                    try:
                        kind_tools(kind, mv)
                    except KeyError:
                        raise ValueError(f"unknown internal operation kind: {kind!r}") from None
                    if raw.get("connection_id") is not None or raw.get("server") is not None \
                            or raw.get("connection_kind") is not None:
                        raise ValueError("internal forbid pattern must not carry connection_id / connection_kind / server")
                    return cls(tool=f"internal:{kind}", args=norm_args, op_class=op_class, note=note,
                               scope="internal", kind=kind, mapping_version=int(mv))
                connection_id = str(raw.get("connection_id") or "").strip()
                connection_kind = str(raw.get("connection_kind") or "mcp").strip()
                if connection_kind not in CONNECTION_KINDS:
                    raise ValueError(f"external forbid pattern 'connection_kind' must be one of {CONNECTION_KINDS}")
                if not connection_id or ":" in connection_id:
                    raise ValueError("external forbid pattern requires 'connection_id'")
                if raw.get("kind") is not None:
                    raise ValueError("external forbid pattern must not carry kind")
                if connection_kind == "a2a":
                    # A2A は接続 (Agent) 単位。tool / method / op_class / args の **キーを持つ** 保存形は受理しない
                    # (A2A は分類せず引数条件も評価しないので、持たせると「受理されるが決して当たらない規則」= 禁止の錯覚になる。
                    # 指示書 30 決定 1)
                    for key in ("tool", "method", "op_class", "args"):
                        if key in raw:
                            raise ValueError(f"a2a forbid pattern must not carry '{key}' (connection-level only)")
                    return cls(tool=f"a2a:{connection_id}", note=note, scope="external",
                               connection_id=connection_id, connection_kind="a2a")
                tool = str(raw.get("tool") or raw.get("method") or "").strip()
                if not tool or ":" in tool:
                    raise ValueError("external forbid pattern requires a method name glob without ':'")
                # `server` (3.0.1 までの名前への束縛) は保存済み snapshot に残っていても読まない (照合は ID)
                return cls(tool=tool, args=norm_args, op_class=op_class, note=note, scope="external",
                           connection_id=connection_id, connection_kind="mcp")
            for key in ("kind", "connection_id", "connection_kind", "server", "mapping_version"):
                if raw.get(key) is not None:
                    raise ValueError(f"forbid pattern '{key}' requires 'scope'")
            tool = str(raw.get("tool") or raw.get("name") or "").strip()
            if not tool:
                raise ValueError("forbid pattern requires 'tool'")
            return cls(tool=tool, args=norm_args, op_class=op_class, note=note)
        raise ValueError(f"unsupported forbid pattern: {type(raw).__name__}")

    @property
    def scoped(self) -> bool:
        return self.scope is not None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"tool": self.tool}
        if self.scope == "internal":
            out = {"scope": "internal", "kind": self.kind, "mapping_version": self.mapping_version}
        elif self.scope == "external":
            if self.connection_kind == "a2a":
                out = {"scope": "external", "connection_kind": "a2a", "connection_id": self.connection_id}
            else:
                # mcp は connection_kind を出さない (3.0.3 までの保存形・digest と同一)
                out = {"scope": "external", "connection_id": self.connection_id, "tool": self.tool}
        if self.args:
            out["args"] = dict(sorted(self.args.items()))
        if self.op_class:
            out["op_class"] = self.op_class
        if self.note:
            out["note"] = self.note
        return out

    def _target_matches(self, candidates: list[str], tool_name: str | None, mcp_server: str | None,
                        connection_id: str | None, connection_kind: str | None = None) -> bool | None:
        """対象 (tool / 接続先) の一致。scope 無しは従来の candidates 照合そのまま。
        internal = 組み込み (mcp_server None) かつ種別の tool 名集合に完全一致。external = 呼び出しの接続 ID
        (`connection_id`) が規則の `connection_id` と一致し、メソッド名が glob に一致。external で MCP 呼び出しなのに
        接続 ID が無い (None = 識別できない)、または MCP のメソッド名に ':' を含む場合は None (= forbid)。
        worker 内蔵の MCP (DB 登録の接続ではない) は LOCAL_CONNECTION を渡す = external 規則の対象外。"""
        if self.scope is None:
            return any(fnmatch.fnmatchcase(c, self.tool) for c in candidates)
        if self.scope == "external" and self.connection_kind == "a2a":
            # A2A 規則: 呼び出しが A2A (connection_kind == "a2a") で接続 ID が一致したときだけ。組み込み / MCP には掛からない
            if connection_kind != "a2a":
                return False
            if connection_id is None:
                return None  # A2A 呼び出しなのに接続を識別できない = 判定できない → 呼び元は forbid (fail-open にしない)
            return connection_id == self.connection_id
        if connection_kind == "a2a":
            return False  # A2A 呼び出しに internal / MCP の external 規則は掛からない (scope 無しの glob は上で照合済み)
        name = (tool_name or "").strip()
        if not name or ":" in name:
            # 名前空間を含む名前 (詐称 / 不正な形): internal 規則の対象にはしない (組み込み tool には無い名前)。
            # external 規則で MCP 呼び出しがこの形なら判定できない = None (呼び元は forbid。fail-open にしない)
            return None if (self.scope == "external" and mcp_server is not None) else False
        if self.scope == "internal":
            if mcp_server is not None:
                return False  # 同名の MCP メソッドには掛からない
            return name in kind_tools(self.kind or "", self.mapping_version or INTERNAL_OPERATIONS_MAPPING_VERSION)
        # external
        if mcp_server is None:
            return False  # 組み込み tool には掛からない
        if connection_id is None:
            return None  # MCP 呼び出しなのに接続を識別できない = 判定できない → 呼び元は forbid (fail-open にしない)
        if connection_id == LOCAL_CONNECTION or connection_id != self.connection_id:
            return False
        return fnmatch.fnmatchcase(name, self.tool)

    def matches(self, candidates: list[str], op_class: str | None, args: dict | None, *,
                tool_name: str | None = None, mcp_server: str | None = None,
                connection_id: str | None = None, connection_kind: str | None = None) -> bool | None:
        """一致 = True、不一致 = False、args を解釈できない / 接続を識別できない = None（呼び元は forbid にする）。
        connection_kind = 呼び出しの接続の種別 (mcp / a2a / None = 組み込み)。"""
        hit = self._target_matches(candidates, tool_name, mcp_server, connection_id, connection_kind)
        if hit is not True:
            return hit
        if self.op_class and op_class != self.op_class:
            return False
        if not self.args:
            return True
        if args is None:
            # 引数を渡されていない呼び出し (引数不要の tool 等) には args 条件付きパターンは掛からない。
            # 「引数はあるが解釈できない」は呼び元が args_unparseable=True で明示する (→ forbid)
            return False
        if not isinstance(args, dict):
            return None  # 引数はあるが構造化されていない = 解釈不能 → 呼び元は forbid
        for key, pattern in self.args.items():
            if key not in args:
                return False
            text = _arg_text(args[key])
            # 完全一致を先に (JSON 化した list / dict は "[" "]" を含み fnmatch の文字クラスと衝突する)
            if text != pattern and not fnmatch.fnmatchcase(text, pattern):
                return False
        return True


@dataclass(frozen=True)
class L1Policy:
    """テナント統制ポリシー (`governance_policies` の active 行)。無い = open（既存テナント）。"""
    version: int
    default_profile: str = "open"
    floor: tuple[ForbidPattern, ...] = ()
    retain_rationale_body: bool = False

    @classmethod
    def from_row(cls, row: dict | None) -> L1Policy | None:
        if not row:
            return None
        floor_raw = row.get("floor") or {}
        if isinstance(floor_raw, str):
            floor_raw = json.loads(floor_raw)
        patterns = floor_raw.get("forbid", []) if isinstance(floor_raw, dict) else floor_raw
        return cls(
            version=int(row.get("version") or 0),
            default_profile=PROFILE_ORDER[profile_rank(row.get("default_profile"))],
            floor=tuple(ForbidPattern.parse(p) for p in _norm_list(patterns)),
            retain_rationale_body=bool(row.get("retain_rationale_body")),
        )


@dataclass(frozen=True)
class ProjectPolicy:
    """`projects.policy` JSON: {"profile": ..., "deny": [...], "allow": [...], "gate": {...}}。
    `deny` は forbid パターン、`allow` は strict の allowlist（tool glob）、`gate` は front の領分（透過）。
    """
    profile: str | None = None
    deny: tuple[ForbidPattern, ...] = ()
    allow: tuple[str, ...] = ()
    gate: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_json(cls, raw: Any) -> ProjectPolicy | None:
        if raw is None or raw == "":
            return None
        if isinstance(raw, str):
            raw = json.loads(raw)
        if not isinstance(raw, dict):
            raise ValueError("projects.policy must be an object")
        profile = raw.get("profile")
        if profile is not None:
            profile = PROFILE_ORDER[profile_rank(profile)]
        deny = tuple(ForbidPattern.parse(p) for p in _norm_list(raw.get("deny") or raw.get("forbid")))
        allow = tuple(str(a).strip() for a in _norm_list(raw.get("allow")) if str(a).strip())
        gate = raw.get("gate") if isinstance(raw.get("gate"), dict) else {}
        return cls(profile=profile, deny=deny, allow=allow, gate=dict(gate))


_REQUIRED_KEYS = ("schema_version", "policy_version", "profile", "l1_profile", "floor", "forbid", "allow")


def profile_permits(profile: str | None, op_class: str) -> bool:
    """profile が **単独で** (allowlist 抜きに) その操作クラスを許しうるか。open = write / destructive とも、
    guarded = write だけ、strict = allowlist で明示された write / destructive (= 両方が候補)。read は常に True。
    project の strict allowlist はこの範囲内でだけ効く (下位から緩和できない: RT-A1)。"""
    if op_class == "read":
        return True
    p = PROFILE_ORDER[profile_rank(profile)]
    if p == "guarded":
        return op_class == "write"
    return op_class in ("write", "destructive")


@dataclass(frozen=True)
class EffectivePolicy:
    """解決済みポリシー（executions の `effective_policy` 列に保存し、worker / read API はこれを読む）。

    floor = テナントの floor（誰も緩められない forbid）、forbid = プロジェクトの deny。
    evaluate は floor → forbid の順に照合する（保存形が壊れていて片方しか無くても floor が消えない）。
    l1_profile = L1 (テナント) の default_profile。project の strict allowlist は **L1 が profile で禁じない操作クラス**
    にだけ効く (guarded の destructive は project が strict + allow にしても解除できない)。
    保証 (RT-A1): 同じ allowlist に対して、project を重ねた許可集合 ⊆ L1 profile 単独の許可集合。allowlist は
    projects.policy だけが持つ (L1 に allowlist 列は無い) ので、「L1 単独」は allowlist を固定した L1 profile を指す。
    """
    profile: str
    floor: tuple[ForbidPattern, ...]
    forbid: tuple[ForbidPattern, ...]
    allow: tuple[str, ...]
    policy_version: int
    retain_rationale_body: bool = False
    gate: dict[str, Any] = field(default_factory=dict)
    project_id: str | None = None
    schema_version: int = _SCHEMA_VERSION
    l1_profile: str | None = None  # None (直接構築) = profile と同じ扱い。保存形 (from_dict) では必須

    def __post_init__(self) -> None:
        # schema_version は規則の内容から決まる (scope 付きがあれば 3)。構築経路 (tighten_merge / from_dict / replace) に
        # よらず属性と保存形を一致させる
        object.__setattr__(self, "schema_version", requires_schema(self.floor, self.forbid))

    @property
    def l1_bound(self) -> str:
        return self.l1_profile or self.profile

    @property
    def required_schema_version(self) -> int:
        """保存形の版: scope 付き規則 (floor / forbid のどちらか) があれば 3、無ければ 2 (既存の digest を変えない)。"""
        return requires_schema(self.floor, self.forbid)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.required_schema_version,
            "policy_version": self.policy_version,
            "profile": self.profile,
            "l1_profile": self.l1_bound,
            "floor": [p.to_dict() for p in self.floor],
            "forbid": [p.to_dict() for p in self.forbid],
            "allow": list(self.allow),
            "retain_rationale_body": self.retain_rationale_body,
            "gate": self.gate,
            "project_id": self.project_id,
        }

    @classmethod
    def from_dict(cls, raw: Any) -> EffectivePolicy:
        """保存形 (executions.effective_policy / policy API 応答) の読み戻し。

        不完全・未知の版・型違いは ValueError（呼び元は「policy 取得不能」= forbid にする。
        `{}` を open として受理しない = fail-open の穴を作らない）。
        """
        if isinstance(raw, str):
            raw = json.loads(raw)
        if not isinstance(raw, dict):
            raise ValueError("effective policy must be an object")
        missing = [k for k in _REQUIRED_KEYS if k not in raw]
        if missing:
            raise ValueError(f"effective policy is missing keys: {missing}")
        # 型は変換せずに検証する (schema_version=true / 1.9、profile=null / "" を open にしない)
        sv, pv, profile = raw["schema_version"], raw["policy_version"], raw["profile"]
        if isinstance(sv, bool) or not isinstance(sv, int) or sv not in SUPPORTED_SCHEMA_VERSIONS:
            raise ValueError(f"unsupported effective policy schema_version: {sv!r}")
        if isinstance(pv, bool) or not isinstance(pv, int) or pv < 0:
            raise ValueError(f"policy_version must be a non-negative integer: {pv!r}")
        if not isinstance(profile, str) or profile not in PROFILE_ORDER:
            raise ValueError(f"profile must be one of {PROFILE_ORDER}: {profile!r}")
        l1_profile = raw["l1_profile"]
        if not isinstance(l1_profile, str) or l1_profile not in PROFILE_ORDER:
            raise ValueError(f"l1_profile must be one of {PROFILE_ORDER}: {l1_profile!r}")
        if profile_rank(profile) < profile_rank(l1_profile):
            raise ValueError("profile must not be looser than l1_profile")
        if not isinstance(raw["floor"], list) or not isinstance(raw["forbid"], list) or not isinstance(raw["allow"], list):
            raise ValueError("floor / forbid / allow must be lists")
        floor = tuple(ForbidPattern.parse(p) for p in raw["floor"])
        forbid = tuple(ForbidPattern.parse(p) for p in raw["forbid"])
        needed = requires_schema(floor, forbid)
        if sv < needed:
            # schema 2 と名乗りながら scope 付き規則を持つ = 旧 writer が意味を落として保存した可能性 → 受理しない
            raise ValueError(f"effective policy carries scoped forbid patterns but schema_version={sv}")
        return cls(
            profile=profile,
            floor=floor,
            forbid=forbid,
            allow=tuple(str(a) for a in raw["allow"]),
            policy_version=pv,
            retain_rationale_body=bool(raw.get("retain_rationale_body")),
            gate=dict(raw.get("gate") or {}),
            project_id=raw.get("project_id"),
            schema_version=needed,
            l1_profile=l1_profile,
        )

    @property
    def digest(self) -> str:
        return policy_digest(self)


def requires_schema(floor: tuple[ForbidPattern, ...] | list, forbid: tuple[ForbidPattern, ...] | list) -> int:
    """floor / forbid に A2A の接続規則 (connection_kind a2a) があれば 4、scope 付き規則があれば 3、無ければ 2。"""
    patterns = (*floor, *forbid)
    if any(p.scope == "external" and p.connection_kind == "a2a" for p in patterns):
        return SCHEMA_VERSION_TYPED_CONNECTION
    return SCHEMA_VERSION_SCOPED if any(p.scoped for p in patterns) else _SCHEMA_VERSION


def verify_connections(policy: EffectivePolicy, connections: Any) -> EffectivePolicy:
    """external 規則が指す接続 (`connection_id`) が存在することを確かめる (resolver が snapshot の前に呼ぶ。executor の
    fire / cli-api の chat 解決 / MP の manifest 解決)。`connections` は種別ごとの対応表 `{"mcp": {id: name}, "a2a": {id: name}}`
    (指示書 30)、または従来の MCP だけの対応表 / ID の集合 (`mcp` として読む)。ID は整数。int / str どちらでも同じ接続を
    指す。a2a 規則があるのに `a2a` の表が無い / 規則が指す接続が無ければ ValueError
    (= 解決できない policy は使わない。禁止を黙って落として実行しない)。policy は書き換えない (照合は worker が
    接続 ID で行う。3.0.1 までの `bind_connections` = 名前への束縛は廃止。3.0req 指示書 26)。"""
    def _has(table: Any, connection_id: str) -> bool:
        try:
            if connection_id in table:
                return True
            return connection_id.isdigit() and int(connection_id) in table
        except (TypeError, ValueError):
            return False

    tables = _connection_tables(connections)
    for p in (*policy.floor, *policy.forbid):
        if p.scope != "external":
            continue
        kind = p.connection_kind or "mcp"
        table = tables.get(kind)
        if table is None:
            # 種別の対応表を渡されていない = その規則を確かめられない (解決できない policy は使わない)
            raise ValueError(f"no {kind} connection table to verify external forbid pattern {p.connection_id!r}")
        if not _has(table, str(p.connection_id)):
            raise ValueError(f"external forbid pattern refers to an unknown {kind} connection_id {p.connection_id!r}")
    return policy


def _connection_tables(connections: Any) -> dict[str, Any]:
    """verify_connections の `connections` を種別ごとの対応表にする。`{"mcp": {...}, "a2a": {...}}` (指示書 30) はそのまま、
    従来の平らな対応表 / 集合 (キーが MCP の ID) は `mcp` の表として読む (3.0.3 までの呼び元を変えない)。"""
    if isinstance(connections, dict) and connections and all(k in CONNECTION_KINDS for k in connections):
        return {k: v for k, v in connections.items() if v is not None}
    return {"mcp": connections}


def policy_digest(policy: EffectivePolicy) -> str:
    """annotation `agenticstar.io/policy-snapshot` と executions.policy_digest に載せる SHA-256。
    canonical JSON（sort_keys、区切り無し、ensure_ascii=False）。
    """
    canon = json.dumps(policy.to_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def tighten_merge(l1: L1Policy | None, project: ProjectPolicy | None, *,
                  project_id: str | None = None) -> EffectivePolicy:
    """`effective = tighten_merge(L1.default, L1.floor, projects.policy)`。

    - L1 無し = open・floor 無し（既存テナントのフォールバック）
    - project.profile は L1 より厳しい方だけ採用（緩める方向は無視）
    - floor = L1.floor、forbid = project.deny（evaluate は floor → forbid の順に照合）
    - l1_profile = L1 の default_profile（project の allowlist が解除できる範囲の上限。RT-A1）
    """
    base_profile = l1.default_profile if l1 else "open"
    profile = tighten_profile(base_profile, project.profile if project else None)
    floor = tuple(l1.floor) if l1 else ()
    forbid = tuple(project.deny) if project else ()
    return EffectivePolicy(
        profile=profile,
        floor=floor,
        forbid=forbid,
        allow=tuple(project.allow) if project else (),
        policy_version=l1.version if l1 else 0,
        retain_rationale_body=bool(l1.retain_rationale_body) if l1 else False,
        gate=dict(project.gate) if project else {},
        project_id=project_id,
        l1_profile=PROFILE_ORDER[profile_rank(base_profile)],
    )


@dataclass(frozen=True)
class Decision:
    mode: str                      # allow | forbid
    reason: str                    # 理由コード（自由文ではない）
    policy_version: int
    unregistered: bool = False     # 分類に無い tool を open / guarded で通した（監査に出す）
    matched: str | None = None  # 一致した forbid パターン (tool glob)

    @property
    def allowed(self) -> bool:
        return self.mode == "allow"


def _candidates(tool: str, mcp_server: str | None) -> list[str]:
    name = (tool or "").strip()
    if mcp_server:
        return [f"mcp:{mcp_server}:{name}", name]
    return [name]


def _with_aliases(cands: list[str], aliases: Any) -> list[str]:
    """候補名に別名を足す (重複・空は除く。順序は候補 → 別名)。"""
    if not aliases:
        return cands
    out = list(cands)
    for a in aliases:
        name = (str(a).strip() if a is not None else "")
        if name and name not in out:
            out.append(name)
    return out


def _match_forbid(policy: EffectivePolicy, cands: list[str], op_class: str | None, args: Any, *,
                  tool_name: str | None = None, mcp_server: str | None = None,
                  connection_id: str | None = None, connection_kind: str | None = None) -> Decision | None:
    """(2) floor → 明示 forbid の順に照合（分類の有無に関わらず。floor を先に見るので forbid 側が欠けても消えない）。

    一致 = その理由で forbid、引数を解釈できない = unevaluable_args で forbid、どれにも掛からない = None。
    """
    for reason, patterns in ((REASON_FLOOR, policy.floor), (REASON_PROJECT_FORBID, policy.forbid)):
        for pattern in patterns:
            hit = pattern.matches(cands, op_class, args, tool_name=tool_name, mcp_server=mcp_server,
                                  connection_id=connection_id, connection_kind=connection_kind)
            if hit is None:
                return Decision("forbid", REASON_UNEVALUABLE, policy.policy_version, matched=pattern.tool)
            if hit:
                return Decision("forbid", reason, policy.policy_version, matched=pattern.tool)
    return None


def _decide_unknown_tool(policy: EffectivePolicy, *, strict_like: bool) -> Decision:
    """(4) 分類に無い tool。strict 相当（strict / 委譲 / dry_run）は forbid、open / guarded は通す（監査に出す）。"""
    mode = "forbid" if strict_like else "allow"
    return Decision(mode, REASON_UNKNOWN_TOOL, policy.policy_version, unregistered=True)


def _decide_strict_allowlist(policy: EffectivePolicy, cands: list[str], op_class: str) -> Decision:
    """strict（委譲実行は strict 固定）: allowlist に明示された write / destructive だけ。

    ただし L1 が profile で禁じる操作クラス (guarded の destructive) は project の allow で解除できない
    (project を重ねた許可集合 ⊆ L1 単独の許可集合。RT-A1)。
    """
    if not any(fnmatch.fnmatchcase(c, a) for c in cands for a in policy.allow):
        return Decision("forbid", REASON_ALLOWLIST, policy.policy_version)
    if not profile_permits(policy.l1_bound, op_class):
        return Decision("forbid", REASON_PROFILE, policy.policy_version)
    return Decision("allow", REASON_ALLOWLIST, policy.policy_version)


def _decide_classified(policy: EffectivePolicy, cands: list[str], op_class: str, *,
                       dry_run: bool, delegated: bool) -> Decision:
    """(5) 分類あり (read / write / destructive)。read は常に allow、dry_run は read 以外 forbid、
    open / guarded は profile で決め（guarded は destructive だけ forbid）、strict と委譲は allowlist。"""
    if op_class == "read":
        return Decision("allow", REASON_PROFILE, policy.policy_version)
    if dry_run:
        return Decision("forbid", REASON_DRY_RUN, policy.policy_version)
    if not delegated and policy.profile in ("open", "guarded"):
        permitted = policy.profile == "open" or op_class == "write"
        return Decision("allow" if permitted else "forbid", REASON_PROFILE, policy.policy_version)
    return _decide_strict_allowlist(policy, cands, op_class)


def evaluate(
    policy: EffectivePolicy | None,
    tool: str,
    op_class: str | None,
    *,
    args: Any = None,
    args_unparseable: bool = False,
    dry_run: bool = False,
    delegated: bool = False,
    mcp_server: str | None = None,
    connection_id: str | None = None,
    mcp: bool | None = None,
    connection_kind: str | None = None,
    tool_aliases: Any = None,
) -> Decision:
    """interceptor の二値判定（instructions/00 §7 の優先順位そのまま）。

    op_class: tool_policies.yaml `operation_classes` の分類（read / write / destructive）。None = unknown。
    args_unparseable: 分類はあるが引数を解釈できなかった（caller が判定）→ forbid。
    mcp_server: MCP の接続の **表示名** (None = 組み込み tool)。candidates `mcp:<name>:<tool>` (allow / scope 無しの
        forbid の glob) に使う。識別には使わない。空 / 空白だけなら「MCP ではない」に正規化するが、`connection_id` が
        あれば MCP 由来として扱う (表示名で由来を消さない)。
    mcp: MCP 由来かを呼び元が明示する (True = MCP 呼び出し、False = 組み込み tool)。None = 上の推定 (名前か ID があれば MCP)。
        統制する側 (worker の interceptor) は必ず明示する: 表示名が空白だけで ID も無い遠隔の MCP 呼び出しを組み込みに
        見せない (external 規則があれば判定不能 = forbid)。
    connection_id: MCP の接続の **識別子** (`mcp_server_configurations.id` の文字列)。external 規則はこれで照合する。
        MCP なのに None = 接続を識別できない → external 規則があれば判定不能 (forbid)。worker 内蔵の MCP
        (DB 登録の接続ではない) は LOCAL_CONNECTION を渡す = external 規則の対象外 (3.0req 指示書 26)。

    優先順位: (1) policy 無し = forbid → (2) floor / forbid 照合 → (2') MCP は allow (下記) → (3) 評価不能 →
    (4) 未分類 → (5) 分類あり（profile / dry_run / allowlist）。各段は helper に分かれているが順序は不変で、
    どの段でも決まらない入力は無い（末尾で必ず Decision を返す = fail-closed の既定）。

    MCP (3.0req 指示書 28、PO 2026-09-22): MCP のツールは操作クラスで分類しない。実行ルール (profile の
    open / guarded / strict、dry_run、委譲) の対象外で、**floor と明示の禁止規則 (external の接続 ID + glob、
    scope 無しの `mcp:<name>:<tool>` glob) に当たらなければ allow**。呼び元が op_class を渡しても無視する
    (op_class 条件付きの禁止規則は MCP には掛からない)。接続を識別できない (external 規則あり + connection_id None)
    ときの forbid は従来どおり。

    connection_kind (3.0req 指示書 30、PO 2026-09-23): 呼び出しの接続の種別。`"a2a"` = A2A 外部 Agent への送信
    (`connection_id` = `a2a_agent_configurations.id` の文字列)。MCP と同じく実行ルールの対象外で、**floor / 明示の
    禁止規則 (connection_kind a2a + 接続 ID、scope 無しの tool 名 glob) に当たらなければ allow** (`a2a_unrestricted`)。
    a2a 規則があるのに接続を識別できない (connection_id None) = 判定不能 (forbid)。MCP の規則は A2A に、A2A の規則は
    MCP に掛からない (整数 ID は別の表)。`"mcp"` / None = 従来どおり (mcp の推定は上の規則)。未知の種別 = 判定不能 (forbid)。
    tool_aliases: scope 無しの禁止規則 (tool 名 glob) の照合に **追加**する候補名 (指示書 30)。A2A の判定名は入口 (React の
        FunctionTool / Claude 連携の共有入口) や生成文脈 (予約名との衝突回避 `_1`) で揺れうるので、呼び元は公開名に加えて
        基底名 (衝突回避前) と同じプロセスで割り当てた名前をここに渡す。候補のどれかに当たれば forbid (fail-closed の方向にだけ効く)。
        scope 付き規則 (internal / external) と strict の allowlist (許可) には効かない。
    """
    if policy is None:
        return Decision("forbid", REASON_POLICY_UNAVAILABLE, 0)
    kind = (str(connection_kind).strip().lower() or None) if connection_kind is not None else None
    if kind is not None and kind not in CONNECTION_KINDS:
        return Decision("forbid", REASON_UNEVALUABLE, policy.policy_version)
    if kind == "a2a":
        # A2A 外部 Agent: 分類しない・profile / dry_run / 委譲を見ない。禁止規則 (a2a の接続 ID、scope 無しの tool 名 glob) だけ
        cid = (str(connection_id).strip() or None) if connection_id is not None else None
        forbidden = _match_forbid(policy, _with_aliases(_candidates(tool, None), tool_aliases), None, args, tool_name=tool,
                                  mcp_server=None, connection_id=cid, connection_kind="a2a")
        if forbidden is not None:
            return forbidden
        return Decision("allow", REASON_A2A_UNRESTRICTED, policy.policy_version)
    # 表示名は candidates 用に正規化する (空 / 空白だけ = 名前なし)。MCP 由来は、呼び元が `mcp` で明示していればそれに従い
    # (統制する側の契約。空白だけの名前で ID も無い呼び出しを組み込みに見せない)、明示が無ければ従来の推定 (名前か ID があれば MCP)
    connection_id = (str(connection_id).strip() or None) if connection_id is not None else None
    mcp_name = (mcp_server or "").strip() or None
    if mcp is None:
        mcp = mcp_name is not None or connection_id is not None
    mcp_server = mcp_name if (mcp and mcp_name is not None) else ("" if mcp else None)
    if mcp:
        op_class = None  # MCP は分類しない (指示書 28)。呼び元の分類は使わない
    cands = _candidates(tool, mcp_name if mcp else None)
    # 別名は floor / forbid の照合 (禁止を増やす方向) にだけ足す。strict の allowlist (許可) には元の候補だけを渡す
    forbidden = _match_forbid(policy, _with_aliases(cands, tool_aliases), op_class, args, tool_name=tool, mcp_server=mcp_server,
                              connection_id=connection_id, connection_kind="mcp" if mcp else None)
    if forbidden is not None:
        return forbidden
    # (2') MCP: 禁止規則に当たらなければ allow。profile / dry_run / 委譲 / 未分類の段は通らない
    if mcp:
        return Decision("allow", REASON_MCP_UNRESTRICTED, policy.policy_version)
    # (3) 評価不能
    if op_class is not None and args_unparseable:
        return Decision("forbid", REASON_UNEVALUABLE, policy.policy_version)
    # (4) unknown
    if op_class is None:
        strict_like = policy.profile == "strict" or delegated or dry_run
        return _decide_unknown_tool(policy, strict_like=strict_like)
    if op_class not in OP_CLASSES:
        return Decision("forbid", REASON_UNEVALUABLE, policy.policy_version)
    # (5) 分類あり
    return _decide_classified(policy, cands, op_class, dry_run=dry_run, delegated=delegated)
