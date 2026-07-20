"""
Tests for the ``scf`` control identifier (Vaillant iQconnect generation, e.g. VR_NEEXT).

iQconnect systems report ``controlIdentifier == "scf"`` from
``/systems/{id}/meta-info/control-identifier``. Before ``scf`` was a member of the
``ControlIdentifier`` enum, ``ControlIdentifier("scf")`` raised ``ValueError`` in
``get_control_identifier()`` and aborted the whole data fetch. These tests lock in that
``scf`` resolves and that the URL helpers treat it like the generic (non-tli) base.
"""

from ..api import get_api_base, get_system_api_base
from ..const import API_URL_BASE
from ..enums import ControlIdentifier


def test_scf_is_a_valid_control_identifier() -> None:
    assert ControlIdentifier("scf") is ControlIdentifier.SCF
    assert ControlIdentifier.SCF.value == "scf"


def test_is_scf_property() -> None:
    assert ControlIdentifier.SCF.is_scf
    assert not ControlIdentifier.TLI.is_scf
    assert not ControlIdentifier.VRC700.is_scf
    # scf is its own identifier, not a flavour of the others
    assert not ControlIdentifier.SCF.is_vrc700
    assert not ControlIdentifier.SCF.is_unsupported


def test_scf_has_a_base_url() -> None:
    assert "scf" in API_URL_BASE
    assert get_api_base(ControlIdentifier.SCF) == API_URL_BASE["scf"]
    assert get_api_base("scf") == API_URL_BASE["scf"]


def test_scf_system_api_base_uses_generic_shape() -> None:
    # scf falls into the generic ``case _`` branch (like vrc700): plain /systems/{id},
    # no /tli suffix.
    system_id = "00000000-0000-0000-0000-000000000000"
    assert get_system_api_base(system_id, ControlIdentifier.SCF) == (
        f"{API_URL_BASE['scf']}/systems/{system_id}"
    )
