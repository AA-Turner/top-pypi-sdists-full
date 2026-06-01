from dataclasses import dataclass

from runlayer_cli.skills.names import skill_install_name


@dataclass
class _Skill:
    name: str
    install_name: str | None = None


def test_skill_install_name_prefers_api_install_name() -> None:
    assert skill_install_name(_Skill(name="Display Name", install_name="display-name")) == "display-name"


def test_skill_install_name_falls_back_to_display_name() -> None:
    assert skill_install_name(_Skill(name="legacy-name")) == "legacy-name"
