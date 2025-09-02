# utils_qt_apply.py
from ..imports import Any, Optional, QtCore, QtWidgets, enum

def _qmeta_key_to_value(meta_enum: QtCore.QMetaEnum, key: str) -> int:
    v = meta_enum.keyToValue(key)
    if isinstance(v, tuple):
        val, ok = v
        return val if ok else -1
    return v

def _qmeta_keys_to_value(meta_enum: QtCore.QMetaEnum, keys: str) -> int:
    v = meta_enum.keysToValue(keys)
    if isinstance(v, tuple):
        val, ok = v
        return val if ok else -1
    return v

def _meta_property(obj: QtCore.QObject, name: str) -> Optional[QtCore.QMetaProperty]:
    mo = obj.metaObject()
    for i in range(mo.propertyCount()):
        p = mo.property(i)
        if p.name() == name:
            return p
    return None

def _coerce_basic(value: Any, type_name: str) -> Any:
    t = (type_name or "").lower()
    if t in ("bool", "qbool"):
        if isinstance(value, bool): return value
        if isinstance(value, (int, float)): return bool(value)
        return str(value).strip().lower() in ("1","true","yes","on")
    if t in ("int", "qint", "qlonglong", "qulonglong"):
        return int(value)
    if t in ("double", "float", "qreal"):
        return float(value)
    if t in ("qstring", "str", "string"):
        return str(value)
    return value

def _find_python_enum_class(obj: QtCore.QObject, enum_name: str):
    for cls in type(obj).mro():
        py_enum_cls = getattr(cls, enum_name, None)
        if py_enum_cls is not None:
            return py_enum_cls
    return None

def _normalize_tokens(x) -> list[str]:
    if isinstance(x, (list, tuple, set)):
        return [str(t).strip() for t in x]
    if isinstance(x, str):
        return [t.strip() for t in x.replace(",", "|").split("|") if t.strip()]
    return [str(x).strip()]

def _coerce_enum_like(obj, prop: QtCore.QMetaProperty, value: Any) -> Any:
    meta_enum = prop.enumerator()
    enum_name = meta_enum.name()
    py_enum_cls = _find_python_enum_class(obj, enum_name)

    if py_enum_cls and isinstance(value, py_enum_cls):
        return value

    if isinstance(value, int):
        if py_enum_cls and issubclass(py_enum_cls, enum.Enum):
            try:
                return py_enum_cls(value)
            except Exception:
                return value
        return value

    if meta_enum.isFlag():
        joined = "|".join(_normalize_tokens(value))
        acc = _qmeta_keys_to_value(meta_enum, joined)
        if acc < 0:
            raise ValueError(f"Unknown flag token(s) '{joined}' for {type(obj).__name__}.{enum_name}")
        if py_enum_cls and issubclass(py_enum_cls, enum.IntFlag):
            try:
                return py_enum_cls(acc)
            except Exception:
                return acc
        return acc
    else:
        tok = _normalize_tokens(value)[0]
        iv = _qmeta_key_to_value(meta_enum, tok)
        if iv < 0:
            raise ValueError(f"Unknown enum '{tok}' for {type(obj).__name__}.{enum_name}")
        if py_enum_cls and issubclass(py_enum_cls, enum.Enum):
            try:
                return py_enum_cls(iv)
            except Exception:
                return iv
        return iv

def _apply_via_qproperty(obj: QtCore.QObject, name: str, value: Any):
    ok = bool(obj.setProperty(name, value))
    return ok, ("setProperty ok" if ok else "setProperty returned False")

def _apply_via_explicit_setter(obj: QtCore.QObject, setter: str, args: tuple[Any, ...]):
    meth = getattr(obj, setter, None)
    if not callable(meth):
        return False, f"no callable {setter}"
    try:
        meth(*args)
        return True, f"{setter}(*{args!r}) ok"
    except Exception as e:
        return False, f"{setter}(*{args!r}) error: {e!r}"

# ---- QSizePolicy helpers ----
def _to_policy(val) -> QtWidgets.QSizePolicy.Policy:
    if isinstance(val, QtWidgets.QSizePolicy.Policy):
        return val
    if isinstance(val, int):
        return QtWidgets.QSizePolicy.Policy(val)
    if isinstance(val, str):
        name = val.strip()
        # Accept 'Expanding', 'expanding', 'Policy.Expanding'
        name = name.split(".")[-1]
        try:
            return getattr(QtWidgets.QSizePolicy.Policy, name)
        except AttributeError:
            # allow numeric strings
            return QtWidgets.QSizePolicy.Policy(int(name))
    # last resort
    return QtWidgets.QSizePolicy.Policy.Expanding

def _coerce_size_policy(value):
    """
    Accepts:
      - (hPolicy, vPolicy)
      - {'horizontal': X, 'vertical': Y}
      - a QSizePolicy instance
    Returns a QSizePolicy instance or (hPolicy, vPolicy) tuple for 2-arg setter.
    """
    if isinstance(value, QtWidgets.QSizePolicy):
        return value
    if isinstance(value, dict):
        h = _to_policy(value.get("horizontal", "Expanding"))
        v = _to_policy(value.get("vertical", "Expanding"))
        return QtWidgets.QSizePolicy(h, v)
    if isinstance(value, (list, tuple)) and len(value) == 2:
        h = _to_policy(value[0]); v = _to_policy(value[1])
        return QtWidgets.QSizePolicy(h, v)
    # fallback: try to interpret single token
    p = _to_policy(value)
    return QtWidgets.QSizePolicy(p, p)

def _canonical_prop_and_setter(name: str) -> tuple[str, str]:
    """
    Accept both 'readOnly' and 'setReadOnly' (and similar).
    Return (prop_name, setter_name).
    """
    if name.startswith("set") and len(name) > 3 and name[3].isupper():
        prop = name[3].lower() + name[4:]  # setReadOnly -> readOnly
        return prop, name
    setter = "set" + name[0].upper() + name[1:]
    return name, setter

def resolve_attr_verbose(obj: QtCore.QObject, name: str, value: Any) -> tuple[bool, str]:
    """
    Try Q_PROPERTY first (with coercion), then explicit setter.
    Accepts both property names and setter names.
    Returns (ok, message).
    """
    prop_name, setter_name = _canonical_prop_and_setter(name)
    prop = _meta_property(obj, prop_name)
    coerced = value
    # Special-case complex types by property name
    if prop_name == "sizePolicy":
        sp = _coerce_size_policy(value)
        # try both shapes: either pass QSizePolicy (1 arg) or two policies
        ok, msg = _apply_via_explicit_setter(obj, setter_name, (sp,))
        if ok:
            return ok, f"{msg} (via QSizePolicy)"
        # try two-arg variant
        ok, msg = _apply_via_explicit_setter(obj, setter_name, (sp.horizontalPolicy(), sp.verticalPolicy()))
        if ok:
            return ok, f"{msg} (via two-arg Policy)"
        # last chance: property
        ok, msg = _apply_via_qproperty(obj, prop_name, sp)
        return ok, f"{msg} (via property QSizePolicy)"

    if prop is not None:
        if prop.isEnumType():
            try:
                coerced = _coerce_enum_like(obj, prop, value)
            except Exception as e:
                return False, f"enum coercion failed for {prop_name}: {e!r}"
        else:
            coerced = _coerce_basic(value, prop.typeName() or "")
        ok, msg = _apply_via_qproperty(obj, prop_name, coerced)
        if ok:
            return True, f"{msg} [{prop_name} <- {coerced!r}]"

    # explicit setter
    ok, msg = _apply_via_explicit_setter(obj, setter_name, (coerced,))
    if ok:
        return True, f"{msg} [{setter_name}]"

    # If you passed a setter name that *is* callable with a different arity,
    # try to help: e.g. setSizePolicy with 2 policies
    if setter_name == "setSizePolicy" and isinstance(value, (list, tuple)) and len(value) == 2:
        h = _to_policy(value[0]); v = _to_policy(value[1])
        ok, msg = _apply_via_explicit_setter(obj, setter_name, (h, v))
        if ok:
            return True, f"{msg} (coerced tuple->two-arg)"

    return False, f"no Q_PROPERTY '{prop_name}' accepted, and {msg}"

def apply_properties(obj: QtCore.QObject, props: dict[str, Any]) -> list[tuple[str, bool, str]]:
    """
    Apply dict of properties; return per-key diagnostics [(name, ok, message)].
    """
    report = []
    for name, val in props.items():
        ok, msg = resolve_attr_verbose(obj, name, val)
        report.append((name, ok, msg))
    return report
