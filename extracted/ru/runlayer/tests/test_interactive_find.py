from runlayer_cli.api import PluginDetail, SkillDetail
from runlayer_cli.commands.interactive_find import format_choice


def test_format_choice_renders_name_namespace_and_description() -> None:
    plugin = PluginDetail(
        id="plugin-1",
        name="review-suite",
        namespace="Org/Repo",
        description="Review plugin",
    )
    skill = SkillDetail(
        id="skill-1",
        name="review-skill",
        namespace="Org/Repo",
        description="Review skill",
    )

    assert format_choice(plugin) == "review-suite  (Org/Repo)  - Review plugin"
    assert format_choice(skill) == "review-skill  (Org/Repo)  - Review skill"
