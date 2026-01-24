from __future__ import annotations

from typing import Dict, Any


def parse_teal_signals(teal_code: str) -> Dict[str, Any]:
    """Parse TEAL code (as string) and extract signals for P0 rule checks."""
    lines = [ln.strip().lower() for ln in teal_code.splitlines()]

    def any_contains(substr: str) -> bool:
        return any(substr in ln for ln in lines)

    return {
        "has_delete_application": any_contains("deleteapplication"),
        "has_update_application": any_contains("updateapplication"),
        "has_global_put": any_contains("app_global_put"),
        "has_global_del": any_contains("app_global_del"),
        "has_local_put": any_contains("app_local_put"),
        "has_box_ops": any(any_contains(k) for k in ["box_put", "box_replace", "box_create"]),
        "has_assert": any_contains("assert"),
        "has_inner_txn": any_contains("inner_txn") or any_contains("itxn"),
        "has_fee_check": any_contains("txn fee") and any_contains("<=") and any_contains("assert"),
        "has_sender_check": any_contains("txn sender") and any_contains("==") and any_contains("assert"),
        "has_rekey_to_check": any_contains("txn rekeyto") and any_contains("global zeroaddress") and any_contains("=="),
        "has_close_check": any_contains("txn closeremainderto") and any_contains("global zeroaddress") and any_contains("=="),
        "has_arg_validation": any_contains("txn numappargs") or any_contains("txna applicationargs"),
    }


def parse_teal_file(file_path: str) -> Dict[str, Any]:
    """Very small TEAL signal parser for P0.
    We scan for key opcodes/keywords to power rule checks.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    return parse_teal_signals(code)
