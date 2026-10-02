"""契約 `parameters_schema` / files・outputs の `schema`（JSON Schema v1 subset、00 §2）と安全な YAML/JSON parser。

subset: type ∈ object/array/string/boolean/integer/number、enum、required、additionalProperties=false、minLength/maxLength、
minimum/maximum、minItems/maxItems。ネスト最大 8、配列最大 100、schema 64KiB。外部 $ref / 実行式 / テンプレートは不可。
YAML は単一 document、独自 tag / 重複 key / alias・anchor / merge / 暗黙の日時 / YAML 1.1 の yes-no bool を拒否する
（front / executor と同じ規則。executer-marketplace `src/core/param_schema.py` と同等）。
"""
from __future__ import annotations

import json
import math
from typing import Any

MAX_DEPTH = 8
MAX_ITEMS = 100
MAX_SCHEMA_BYTES = 64 * 1024
_TYPES = ("object", "array", "string", "boolean", "integer", "number")
_ALLOWED_KEYS = frozenset({"type", "properties", "required", "additionalProperties", "items", "enum", "minLength",
                           "maxLength", "minimum", "maximum", "minItems", "maxItems", "description", "title", "default"})


class SchemaError(ValueError):
    pass


def validate_schema(schema: Any, _depth: int = 0) -> None:
    if _depth == 0 and len(json.dumps(schema, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) > MAX_SCHEMA_BYTES:
        raise SchemaError("schema exceeds 64KiB")
    if _depth > MAX_DEPTH:
        raise SchemaError("schema nesting exceeds 8")
    if not isinstance(schema, dict):
        raise SchemaError("schema must be an object")
    unknown = set(schema) - _ALLOWED_KEYS
    if unknown or "$ref" in schema:
        raise SchemaError(f"schema keyword not allowed: {sorted(unknown)}")
    t = schema.get("type")
    if t not in _TYPES:
        raise SchemaError(f"schema type must be one of {_TYPES}")
    if t == "object":
        if schema.get("additionalProperties", True) is not False:
            raise SchemaError("object schema must set additionalProperties=false")
        props = schema.get("properties") or {}
        if not isinstance(props, dict):
            raise SchemaError("properties must be an object")
        for k, sub in props.items():
            if not isinstance(k, str):
                raise SchemaError("property names must be strings")
            validate_schema(sub, _depth + 1)
        req = schema.get("required") or []
        if not isinstance(req, list) or any(r not in props for r in req):
            raise SchemaError("required must list declared properties")
    elif t == "array":
        if "items" not in schema:
            raise SchemaError("array schema must define items")
        validate_schema(schema["items"], _depth + 1)
        if int(schema.get("maxItems", MAX_ITEMS)) > MAX_ITEMS:
            raise SchemaError("maxItems exceeds 100")
    if "enum" in schema and (not isinstance(schema["enum"], list) or not schema["enum"]):
        raise SchemaError("enum must be a non-empty list")


def _type_ok(t: str, v: Any) -> bool:
    if t == "string":
        return isinstance(v, str)
    if t == "boolean":
        return isinstance(v, bool)
    if t == "integer":
        return (isinstance(v, int) and not isinstance(v, bool) and _representable(v)) \
            or (isinstance(v, float) and math.isfinite(v) and v.is_integer())
    if t == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool) and _representable(v)
    if t == "object":
        return isinstance(v, dict)
    if t == "array":
        return isinstance(v, list)
    return False


def _representable(v: Any) -> bool:
    """JSON number として扱える（float に収まる有限値）。巨大な整数は拒否（OverflowError を外へ出さない）。"""
    try:
        return math.isfinite(float(v))
    except (OverflowError, ValueError):
        return False


def json_equal(a: Any, b: Any) -> bool:
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if type(a) is not type(b):
        return False
    if isinstance(a, list):
        return len(a) == len(b) and all(json_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict):
        return set(a) == set(b) and all(json_equal(a[k], b[k]) for k in a)
    return a == b


def _validate_value(schema: dict, v: Any, path: str, depth: int) -> None:
    if depth > MAX_DEPTH:
        raise SchemaError(f"{path}: nesting exceeds 8")
    t = schema["type"]
    if not _type_ok(t, v):
        raise SchemaError(f"{path}: expected {t}")
    if "enum" in schema and not any(json_equal(v, e) for e in schema["enum"]):
        raise SchemaError(f"{path}: value not in enum")
    if t == "string":
        if "minLength" in schema and len(v) < int(schema["minLength"]):
            raise SchemaError(f"{path}: shorter than minLength")
        if "maxLength" in schema and len(v) > int(schema["maxLength"]):
            raise SchemaError(f"{path}: longer than maxLength")
    elif t in ("integer", "number"):
        if "minimum" in schema and v < schema["minimum"]:
            raise SchemaError(f"{path}: below minimum")
        if "maximum" in schema and v > schema["maximum"]:
            raise SchemaError(f"{path}: above maximum")
    elif t == "object":
        props = schema.get("properties") or {}
        extra = set(v) - set(props)
        if extra:
            raise SchemaError(f"{path}: {len(extra)} additional propert{'y' if len(extra) == 1 else 'ies'} not allowed")
        for r in schema.get("required") or []:
            if r not in v:
                raise SchemaError(f"{path}: missing required '{r}'")
        for k, sub in props.items():
            if k in v:
                _validate_value(sub, v[k], f"{path}.{k}", depth + 1)
    elif t == "array":
        if len(v) > int(schema.get("maxItems", MAX_ITEMS)):
            raise SchemaError(f"{path}: too many items")
        if len(v) < int(schema.get("minItems", 0)):
            raise SchemaError(f"{path}: too few items")
        for i, item in enumerate(v):
            _validate_value(schema["items"], item, f"{path}[{i}]", depth + 1)


def validate_value(schema: Any, value: Any) -> None:
    validate_schema(schema)
    _validate_value(schema, value, "$", 0)


MAX_DOCUMENT_DEPTH = 64


def _check_depth(value: Any, depth: int = 0) -> None:
    """parser が受け付けた document の深さを上限で拒否する（validate / digest / 比較の再帰を有界にする）。"""
    if depth > MAX_DOCUMENT_DEPTH:
        raise SchemaError("document nesting too deep")
    if isinstance(value, dict):
        for v in value.values():
            _check_depth(v, depth + 1)
    elif isinstance(value, list):
        for v in value:
            _check_depth(v, depth + 1)


# ---------------------------------------------------------------------------
# 安全な parser
# ---------------------------------------------------------------------------
def _reject_non_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise SchemaError("non-finite number")
    if isinstance(value, dict):
        for v in value.values():
            _reject_non_finite(v)
    elif isinstance(value, list):
        for v in value:
            _reject_non_finite(v)


def parse_json_strict(data: bytes) -> Any:
    def no_dup(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise SchemaError("duplicate key")
            d[k] = v
        return d
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=no_dup, parse_constant=lambda c: (_ for _ in ()).throw(SchemaError(c)))
    except (UnicodeDecodeError, ValueError) as e:
        raise SchemaError(f"invalid JSON: {type(e).__name__}")
    except RecursionError:
        raise SchemaError("document nesting too deep")
    _check_depth(value)
    _reject_non_finite(value)
    return value


def parse_yaml_strict(data: bytes) -> Any:
    """単一 document、alias / anchor / merge / 独自 tag / 重複 key / 暗黙の日時 / yes-no bool を拒否。JSON 表記の YAML も可。"""
    try:
        import yaml  # PyYAML（core 依存）
    except ImportError as e:  # pragma: no cover
        raise SchemaError("yaml parser unavailable") from e

    class StrictLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node, deep=False):
        keys = set()
        for key_node, _ in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                raise SchemaError("merge keys are not allowed")
            key = loader.construct_object(key_node, deep=True)
            if not isinstance(key, str):
                raise SchemaError("mapping keys must be strings")
            if key in keys:
                raise SchemaError("duplicate key")
            keys.add(key)
        return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)

    def reject(loader, node):
        raise SchemaError("tag not allowed")

    StrictLoader.add_constructor("tag:yaml.org,2002:map", construct_mapping)
    StrictLoader.add_constructor("tag:yaml.org,2002:timestamp", reject)
    StrictLoader.add_constructor("tag:yaml.org,2002:binary", reject)
    StrictLoader.add_constructor("tag:yaml.org,2002:set", reject)
    StrictLoader.add_constructor("tag:yaml.org,2002:omap", reject)
    StrictLoader.add_constructor("tag:yaml.org,2002:pairs", reject)
    StrictLoader.add_constructor(None, reject)
    # 暗黙 tag は YAML 1.2 core schema（front `contract.js parseYamlToJson` = eemeli/yaml schema 'core' と同じ）:
    # bool は true/True/TRUE/false/False/FALSE だけ（yes/no/on/off は文字列）、int は 10 進（1:20 の 60 進や 1_000 は文字列）、
    # float は 1e3 も数値、timestamp は解決しない。front と同じく plain の「先頭 0 + 数字/x/o/b」（01 / 0x1f / 0o7 / 0b1）は
    # 曖昧な数値として拒否、明示 tag（!!int 等）と anchor / alias も拒否
    import re
    _DROP = ("tag:yaml.org,2002:timestamp", "tag:yaml.org,2002:bool", "tag:yaml.org,2002:int", "tag:yaml.org,2002:float",
             "tag:yaml.org,2002:merge")   # core schema に merge は無い: `<<` は文字列（front と同じ）
    StrictLoader.yaml_implicit_resolvers = {
        k: [(tag, regexp) for tag, regexp in v if tag not in _DROP]
        for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }
    StrictLoader.add_implicit_resolver("tag:yaml.org,2002:bool", re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"), list("tTfF"))
    StrictLoader.add_implicit_resolver("tag:yaml.org,2002:int", re.compile(r"^[-+]?[0-9]+$"), list("-+0123456789"))
    StrictLoader.add_implicit_resolver(
        "tag:yaml.org,2002:float",
        re.compile(r"^(?:[-+]?(?:\.[0-9]+|[0-9]+(?:\.[0-9]*)?)(?:[eE][-+]?[0-9]+)?|[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN))$"),
        list("-+0123456789."))
    _AMBIGUOUS_NUMBER = re.compile(r"^[-+]?0[0-9xXoObB]")

    def construct_int(loader, node):
        return int(loader.construct_scalar(node))

    def construct_float(loader, node):
        v = loader.construct_scalar(node).lower()
        if v.endswith(".inf"):
            return float("-inf") if v.startswith("-") else float("inf")
        if v.endswith(".nan"):
            return float("nan")
        return float(v)

    StrictLoader.add_constructor("tag:yaml.org,2002:int", construct_int)
    StrictLoader.add_constructor("tag:yaml.org,2002:float", construct_float)

    class NoAliasComposer(StrictLoader):
        def process_directives(self):
            value = super().process_directives()
            # %YAML は 1.2 だけ（front の parser は 1.1 指定で yes/no を bool にするため、SDK は一致しない版を受けない）、%TAG は不可
            if self.yaml_version is not None and tuple(self.yaml_version) != (1, 2):
                raise SchemaError("unsupported YAML directive")
            if any(h not in ("!", "!!") for h in (self.tag_handles or {})):
                raise SchemaError("tag directives are not allowed")
            return value

        def compose_node(self, parent, index):
            if self.check_event(yaml.AliasEvent):
                raise SchemaError("aliases are not allowed")
            ev = self.peek_event()
            if getattr(ev, "anchor", None):
                raise SchemaError("anchors are not allowed")  # 未使用の anchor も不可（front と同じ document だけ受ける）
            if getattr(ev, "tag", None):
                raise SchemaError("tag not allowed")          # 明示 tag（!!int / !!str / !custom）は不可
            if isinstance(ev, yaml.ScalarEvent) and ev.style is None and _AMBIGUOUS_NUMBER.match(ev.value or ""):
                raise SchemaError("ambiguous number")         # 先頭 0 / 16 進 / 8 進 / 2 進の plain scalar
            return super().compose_node(parent, index)

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise SchemaError("invalid UTF-8")
    try:
        docs = list(yaml.load_all(text, Loader=NoAliasComposer))  # noqa: S506 — SafeLoader 派生
    except SchemaError:
        raise
    except yaml.YAMLError as e:
        raise SchemaError(f"invalid YAML: {type(e).__name__}")
    except (RecursionError, ValueError):
        raise SchemaError("document nesting too deep or invalid scalar")
    if len(docs) != 1:
        raise SchemaError("exactly one YAML document is required")
    value = docs[0]
    _check_depth(value)
    _reject_non_finite(value)
    return value


def parse_by_format(fmt: str, data: bytes) -> Any:
    if fmt == "json":
        return parse_json_strict(data)
    if fmt == "yaml":
        return parse_yaml_strict(data)
    raise SchemaError(f"format {fmt} has no structured parser")


def validate_file_content(fmt: str, data: bytes, schema: Any | None) -> None:
    """json / yaml は parse 可能であること、schema があれば subset で検証する（markdown / text / binary は対象外）。"""
    if fmt not in ("json", "yaml"):
        return
    value = parse_by_format(fmt, data)
    if schema is not None:
        try:
            validate_value(schema, value)
        except RecursionError:
            raise SchemaError("document nesting too deep")
        except (OverflowError, ValueError) as e:
            if isinstance(e, SchemaError):
                raise
            raise SchemaError("value not representable")
