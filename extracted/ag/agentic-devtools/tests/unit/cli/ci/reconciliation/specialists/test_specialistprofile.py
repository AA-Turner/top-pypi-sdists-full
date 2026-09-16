import pytest

from agentic_devtools.cli.ci.reconciliation.specialists import (
    SpecialistProfile,
    SpecialistRole,
    recovery_profile,
    route_specialist,
)


def test_profiles_enforce_models_and_footprints() -> None:
    profile = SpecialistProfile(SpecialistRole.CODE_REPAIR, file_footprint=("a.py",), test_footprint=("test_a.py",))
    assert not profile.is_recovery
    assert recovery_profile(SpecialistRole.CODE_REPAIR).is_recovery
    assert route_specialist(SpecialistRole.TEST_REPAIR).model == "gpt-5.6-luna"
    assert route_specialist(SpecialistRole.DOC_REPAIR, recovery=True).model == "gpt-6-astra"
    with pytest.raises(ValueError):
        SpecialistProfile(SpecialistRole.CODE_REPAIR, model="other")
    with pytest.raises(ValueError):
        SpecialistProfile(SpecialistRole.CODE_REPAIR, file_footprint=("a.py", "a.py"))
    with pytest.raises(TypeError):
        route_specialist("code_repair")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SpecialistProfile("code_repair")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SpecialistProfile(SpecialistRole.CODE_REPAIR, file_footprint=("",))
