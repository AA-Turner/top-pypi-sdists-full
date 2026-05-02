# ======================================== IMPORTS ========================================
from types import UnionType
from typing import Tuple, get_args, get_origin, Union, Literal
from numbers import Real

# ======================================== TYPE CHECK ========================================
def typename(t: type):
    """
    Renvoie le str du type

    Args:
        t(type): type à vérifier
    """
    return getattr(t, "__name__", str(t))


def expect(value: object, types: type | Tuple[type, ...]):
    """
    Vérifie la valeur contre un type supporté :
        T type simple
        (T1, T2, T3) multi-types
        T1 | T2 union
        list[T] liste typée
        set[T] set typé
        tuple[T] tuple broadcast
        tuple[T1, T2, T3] tuple positionnel
        dict[K, V] dictionnaire typé

    Args:
        value: valeur à vérifier
        types: types à vérifier

    Returns:
        value: si valide
    
    Raises:
        TypeError: si la valeur n'est pas conforme
    """
    # (T1, T2, T3)
    if isinstance(types, tuple):
        types = tuple(type(None) if t is None else t for t in types)
        if not isinstance(value, types):
            readable = " | ".join(typename(t) for t in types)
            raise TypeError(f"expected ({readable}), got ({typename(value)})")
        return value

    # T
    origin = get_origin(types)
    if origin is None:
        types = type(None) if types is None else types
        if not isinstance(value, types):
            raise TypeError(f"expected ({typename(types)}), got ({typename(value)})")
        return value
    
    # T1 |T2
    args = get_args(types)
    if origin in (UnionType, Union):
        for t in args:
            try:
                return expect(value, t)
            except TypeError:
                continue
        readable = " | ".join(typename(t) for t in args)
        raise TypeError(f"expected ({readable}), got ({typename(value)})")

    # list[T] / set[T] / frozenset[T]
    if origin in (list, set, frozenset):
        if not isinstance(value, origin):
            raise TypeError(f"expected ({typename(origin)}), got ({typename(value)})")
        inner = args[0]
        if get_origin(inner) is None:
            for i, v in enumerate(value):
                if not isinstance(v, inner):
                    raise TypeError(f"at index {i}: expected ({typename(inner)}), got ({typename(v)})")
        else:
            for i, v in enumerate(value):
                try:
                    expect(v, inner)
                except TypeError as e:
                    raise TypeError(f"at index {i}: {e}") from e
        return value

    # tuple[T] / tuple[T1, T2, T3]
    if origin is tuple:
        if not isinstance(value, tuple):
            raise TypeError(f"expected (tuple), got ({typename(value)})")
        if len(args) == 1 or len(args) == 2 and args[1] is Ellipsis:
            inner = args[0]
            if get_origin(inner) is None:
                for i, v in enumerate(value):
                    if not isinstance(v, inner):
                        raise TypeError(f"at index {i}: expected ({typename(inner)}), got ({typename(v)})")
            else:
                for i, v in enumerate(value):
                    try:
                        expect(v, inner)
                    except TypeError as e:
                        raise TypeError(f"at index {i}: {e}") from e
        else:
            if len(value) != len(args):
                raise TypeError(f"expected (tuple) of len {len(args)}, got {len(value)}")
            for i, (v, t) in enumerate(zip(value, args)):
                if get_origin(t) is None:
                    if not isinstance(v, t):
                        raise TypeError(f"at index {i}: expected ({typename(t)}), got ({typename(v)})")
                else:
                    try:
                        expect(v, t)
                    except TypeError as e:
                        raise TypeError(f"at index {i}: {e}") from e
        return value

    # dict[K, V]
    if origin is dict:
        if not isinstance(value, dict):
            raise TypeError(f"expected (dict), got ({typename(value)})")
        kt, vt = args
        kt_simple = get_origin(kt) is None
        vt_simple = get_origin(vt) is None
        for k, v in value.items():
            if kt_simple:
                if not isinstance(k, kt):
                    raise TypeError(f"at key {k!r}: invalid key: expected ({typename(kt)}), got ({typename(k)})")
            else:
                try:
                    expect(k, kt)
                except TypeError as e:
                    raise TypeError(f"at key {k!r}: invalid key: {e}") from e
            if vt_simple:
                if not isinstance(v, vt):
                    raise TypeError(f"at key {k!r}: expected ({typename(vt)}), got ({typename(v)})")
            else:
                try:
                    expect(v, vt)
                except TypeError as e:
                    raise TypeError(f"at key {k!r}: {e}") from e
        return value
    
    # Literal[T1, T2, ...]
    if origin is Literal:
        if value not in args:
            readable = " | ".join(repr(a) for a in args)
            raise TypeError(f"expected Literal[{readable}], got ({value!r})")
        return value

    raise TypeError(f"unsupported type annotation: {types!r}")

def expect_callable(value: object, include_none: bool = False, arg: str = "Argument") -> object:
    """Vérifie que l'objet soit appelable

    Args:
        value: objet à vérifier
        include_none: accepte que la valeur soit ``None``
        arg: nom de l'argument
    """
    if callable(value):
        return value
    if include_none and value is None:
        return value
    raise TypeError(f"{arg} ({value}) must be a callable{' or None' if include_none else ''}")
    
# ======================================== VALUE CHECK ========================================
def not_null(value: object, arg: str = "Argument"):
    """
    Vérifie que la valeur ne soit pas nulle

    Args:
        value(object): valeur à vérifier
        arg(str): nom de l'argument à vérifier
    """
    # None
    if value is None:
        raise ValueError(f"{arg} cannot be None")

    # Nombre
    if isinstance(value, Real):
        if value == 0:
            raise ValueError(f"{arg} cannot be None")
        return value
    
    # Types composés
    if isinstance(value, (str, list, tuple, set, dict, frozenset)):
        if len(value) == 0:
            raise ValueError(f"{arg} cannot be empty")
        return value
        
    # Objet possédant une méthode __len__
    if hasattr(value, "__len__"):
        if len(value) == 0:
            raise ValueError(f"{arg} cannot be empty")
        return value
    
    # Objet custom
    return value

def not_in(value: object, forbidden: object | tuple[object], arg: str = "Argument"):
    """
    Vérifie que la valeur ne soit pas parmi les valeurs interdites

    Args:
        value(object): valeur à vérifier
        forbidden(object | tuple[object]): valeur(s) interdite(s)
        arg(str): nom de l'argument à vérifier
    """
    forbidden = forbidden if isinstance(forbidden, tuple) else (forbidden,)
    if value in forbidden:
        readable = " | ".join(repr(f) for f in forbidden)
        raise ValueError(f"{arg} cannot be {readable}, got {value!r}")
    return value

# ======================================== NUMBER CHECK ========================================
def positive(value: Real, arg: str = "Argument"):
    """Vérifie que la valeur soit positive

    Args:
        value: valeur à vérifier
        arg: nom de l'argument à vérifier
    """
    if value < 0:
        raise ValueError(f"{arg} cannot be negative")
    return value
    
def over(value: Real, threshold: Real, include: bool = True, arg: str = "Argument"):
    """Vérifie que la valeur soit supérieure à un seuil

    Args:
        value: valeur à vérifier
        threshold: seuil minimum exclu
        arg: nom de l'argument à vérifier
    """
    if (value < threshold if include else value <= threshold):
        raise ValueError(f"{arg} must be over {threshold}")
    return value

def under(value: Real, threshold: Real, include: bool = True, arg: str = "Argument"):
    """Vérifie que la valeur soit inférieure à un seuil

    Args:
        value: valeur à vérifier
        threshold: seuil maximum exclu
        arg: nom de l'argument à vérifier
    """
    if (value > threshold if include else value >= threshold):
        raise ValueError(f"{arg} must be under {threshold}")
    return value

def clamped(value: Real, min: Real = 0.0, max: Real = 1.0, include_min: bool = True, include_max: bool = True, arg: str = "Argument"):
    """Vérifie que la valeur soit comprise entre min et max

    Args:
        value: valeur à vérifier
        min: valeur minimale autorisée
        max: valeur maximale autorisée
        arg: nom de l'argument à vérifier
    """    
    if (value < min if include_min else value <= min) or (value > max if include_max else value >= max):
        raise ValueError(f"{arg} must be between {min} {'included' if include_min else 'excluded'} and {max} {'included' if include_max else 'excluded'}")
    return value

def inferior_to(value: Real, threshold: Real, include: bool = True, arg: str = "Argument"):
    """Vérifie que la valeur soit inférieure à un seuil

    Args:
        value: valeur à vérifier
        threshold: seuil maximum
        include: inclure le seuil
        arg: nom de l'argument à vérifier
    """
    if (value > threshold if include else value >= threshold):
        raise ValueError(f"{arg} must be inferior to {threshold}")
    return value


def superior_to(value: Real, threshold: Real, include: bool = True, arg: str = "Argument"):
    """Vérifie que la valeur soit supérieure à un seuil

    Args:
        value: valeur à vérifier
        threshold: seuil minimum
        include: inclure le seuil
        arg: nom de l'argument à vérifier
    """
    if (value < threshold if include else value <= threshold):
        raise ValueError(f"{arg} must be superior to {threshold}")
    return value


def equal_to(value: Real, target: object, arg: str = "Argument"):
    """Vérifie que la valeur soit égale à une cible

    Args:
        value: valeur à vérifier
        target: valeur attendue
        arg: nom de l'argument à vérifier
    """
    if value != target:
        raise ValueError(f"{arg} must be equal to {target!r}, got {value!r}")
    return value

def different_from(value: Real, target: object, arg: str = "Argument"):
    """Vérifie que la valeur soit différente à une cible

    Args:
        value: valeur à vérifier
        target: valeur interdite
        arg: nom de l'argument à vérifier
    """
    if value == target:
        raise ValueError(f"{arg} must be different from {target!r}")
    return value

# ======================================== EXPORTS ========================================
__all__ = [
    "expect",
    "expect_callable",

    "not_null",
    "not_in",

    "positive",
    "over",
    "under",
    "clamped",
    "inferior_to",
    "superior_to",
    "equal_to",
    "different_from",
]