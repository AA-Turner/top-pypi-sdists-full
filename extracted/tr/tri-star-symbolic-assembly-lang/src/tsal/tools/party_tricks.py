from __future__ import annotations

"""Interactive demo runner for Brian party tricks."""

import argparse
import inspect
import random
from typing import Callable, Dict, Tuple, Any

from tsal.core.phi_math import (
    corrected_energy,
    phi_wavefunction,
    phase_alignment_potential,
    orbital_radius,
)
from tsal.core.intent_metric import calculate_idm
from tsal.core.spiral_vector import phi_alignment
from tsal.core.symbols import get_symbol


def orbital_trick(n: int = 1, phi: float = 0.0) -> float:
    """Return corrected orbital energy."""
    return corrected_energy(n, phi)


def phi_trick(complexity: float = 0.5, coherence: float = 0.5) -> float:
    """Return phi alignment score."""
    return phi_alignment(complexity, coherence)


def symbol_trick(symbol: str = "PHI") -> tuple:
    """Lookup a TSAL symbol by name or hex code."""
    try:
        code = int(symbol, 16)
    except ValueError:
        code = None
    if code is None:
        for k, v in get_symbol.__globals__["TSAL_SYMBOLS"].items():
            if v[1] == symbol:
                code = k
                break
    return get_symbol(code) if code is not None else ("?", symbol, "Unknown")


def wavefunction_trick(
    phi: float = 0.0, phi_vacuum: float = 0.0, lam: float = 1.0
) -> float:
    """Return φ wavefunction value."""
    return phi_wavefunction(phi, phi_vacuum, lam)


def potential_trick(
    phi: float = 0.0, phi_vacuum: float = 0.0, lam: float = 1.0
) -> float:
    """Return phase alignment potential."""
    return phase_alignment_potential(phi, phi_vacuum, lam)


def radius_trick(n: int = 1, phi: float = 0.0) -> float:
    """Return orbital radius."""
    return orbital_radius(n, phi)


def idm_trick(
    info_quality: float = 1.0,
    info_quantity: float = 1.0,
    accuracy: float = 1.0,
    complexity: float = 1.0,
    time_taken: float = 1.0,
) -> float:
    """Return Intent-Driven Metric score."""
    return calculate_idm(
        info_quality, info_quantity, accuracy, complexity, time_taken
    )


Func_yTown: Dict[str, Tuple[Callable[..., Any], str]] = {
    "orbital": (orbital_trick, "Calculate orbital energy"),
    "phi-align": (phi_trick, "Phi alignment score"),
    "symbol": (symbol_trick, "TSAL symbol lookup"),
    "wavefunction": (wavefunction_trick, "φ wavefunction"),
    "potential": (potential_trick, "Phase alignment potential"),
    "radius": (radius_trick, "Orbital radius"),
    "idm": (idm_trick, "Intent metric"),
}


def run_trick(name: str, **kwargs: Any) -> Any:
    if name not in Func_yTown:
        raise KeyError(name)
    func = Func_yTown[name][0]
    sig = inspect.signature(func)
    bound = sig.bind_partial(**kwargs)
    bound.apply_defaults()
    return func(*bound.args, **bound.kwargs)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run a Brian party trick")
    parser.add_argument("name", nargs="?", help="trick name")
    parser.add_argument("args", nargs=argparse.REMAINDER)
    parser.add_argument("--list", action="store_true", dest="list_tricks")
    args = parser.parse_args(argv)

    if args.list_tricks or not args.name:
        for key, (_, help_text) in Func_yTown.items():
            print(f"{key}: {help_text}")
        return

    func = Func_yTown.get(args.name)
    if not func:
        raise SystemExit(f"Unknown trick: {args.name}")

    func_obj = func[0]
    sig = inspect.signature(func_obj)
    params = {}
    for param in sig.parameters.values():
        if args.args:
            value = args.args.pop(0)
        else:
            value = input(f"{param.name} [{param.default}]: ") or param.default
        params[param.name] = type(param.default)(value)
    result = func_obj(**params)
    print(result)


if __name__ == "__main__":
    main()
