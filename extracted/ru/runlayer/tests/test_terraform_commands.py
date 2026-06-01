from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from runlayer_cli.main import app
from runlayer_cli.terraform_export import (
    ExportEntry,
    build_export_sections,
    render_tfvars,
)

runner = CliRunner()


def test_build_export_sections_normalizes_and_sorts_keys():
    sections = build_export_sections(
        users=[
            ExportEntry(key_source="zoe+ops@runlayer.com", resource_id="user-2"),
            ExportEntry(key_source="marcin@runlayer.com", resource_id="user-1"),
        ],
        groups=[
            ExportEntry(key_source="Data Science", resource_id="group-2"),
            ExportEntry(key_source="Engineers", resource_id="group-1"),
        ],
        roles=[
            ExportEntry(key_source="super_admin", resource_id="role-2"),
            ExportEntry(key_source="admin", resource_id="role-1"),
        ],
        selected_sections=("users", "groups", "roles"),
    )

    assert list(sections["users"].keys()) == [
        "marcin_at_runlayer_com",
        "zoe_ops_at_runlayer_com",
    ]
    assert list(sections["groups"].keys()) == ["data_science", "engineers"]
    assert list(sections["roles"].keys()) == ["admin", "super_admin"]


def test_build_export_sections_resolves_collisions_with_stable_suffix():
    sections = build_export_sections(
        users=[
            ExportEntry(
                key_source="marcin@runlayer.com",
                resource_id="11111111-1111-1111-1111-111111111111",
            ),
            ExportEntry(
                key_source="marcin+test@runlayer.com",
                resource_id="22222222-2222-2222-2222-222222222222",
            ),
            ExportEntry(
                key_source="123@example.com",
                resource_id="33333333-3333-3333-3333-333333333333",
            ),
        ],
        groups=[],
        roles=[],
        selected_sections=("users",),
    )

    assert list(sections["users"].keys()) == [
        "_123_at_example_com",
        "marcin_at_runlayer_com",
        "marcin_test_at_runlayer_com",
    ]

    collided = build_export_sections(
        users=[
            ExportEntry(
                key_source="marcin-test@runlayer.com",
                resource_id="11111111-1111-1111-1111-111111111111",
            ),
            ExportEntry(
                key_source="marcin_test@runlayer.com",
                resource_id="22222222-2222-2222-2222-222222222222",
            ),
        ],
        groups=[],
        roles=[],
        selected_sections=("users",),
    )

    assert list(collided["users"].keys()) == [
        "marcin_test_at_runlayer_com",
        "marcin_test_at_runlayer_com_22222222",
    ]


def test_build_export_sections_does_not_overwrite_on_suffix_collision():
    sections = build_export_sections(
        users=[
            ExportEntry(
                key_source="same@example.com",
                resource_id="aaaaaaaa-1111-1111-1111-111111111111",
            ),
            ExportEntry(
                key_source="same+one@example.com",
                resource_id="bbbbbbbb-1111-1111-1111-111111111111",
            ),
        ],
        groups=[
            ExportEntry(
                key_source="same_one_example_com_bbbbbbbb",
                resource_id="group-1",
            )
        ],
        roles=[],
        selected_sections=("users", "groups"),
    )

    assert sections["users"] == {
        "same_at_example_com": "aaaaaaaa-1111-1111-1111-111111111111",
        "same_one_at_example_com": "bbbbbbbb-1111-1111-1111-111111111111",
    }
    assert sections["groups"] == {
        "same_one_example_com_bbbbbbbb": "group-1",
    }


def test_render_tfvars_keeps_section_order_and_blank_lines():
    rendered = render_tfvars(
        {
            "users": {"marcin_at_runlayer_com": "user-1"},
            "groups": {"engineers": "group-1"},
            "roles": {"admin": "role-1"},
        }
    )

    assert rendered == (
        'users = {\n'
        '  marcin_at_runlayer_com = "user-1"\n'
        "}\n\n"
        'groups = {\n'
        '  engineers = "group-1"\n'
        "}\n\n"
        'roles = {\n'
        '  admin = "role-1"\n'
        "}\n"
    )


def test_export_command_writes_requested_sections(tmp_path: Path):
    output_path = tmp_path / "vars.tfvars"

    with (
        patch(
            "runlayer_cli.commands.terraform.resolve_credentials",
            return_value={"secret": "rl_secret", "host": "https://example.com"},
        ),
        patch("runlayer_cli.commands.terraform.set_credentials_in_context"),
        patch("runlayer_cli.commands.terraform.RunlayerClient") as client_class,
        patch("runlayer_cli.commands.terraform.list_users_for_terraform") as list_users,
        patch("runlayer_cli.commands.terraform.list_groups_for_terraform") as list_groups,
        patch("runlayer_cli.commands.terraform.list_roles_for_terraform") as list_roles,
    ):
        client = client_class.return_value
        list_users.return_value = [
            ExportEntry(
                key_source="marcin@runlayer.com",
                resource_id="11111111-1111-1111-1111-111111111111",
            )
        ]
        list_groups.return_value = [ExportEntry(key_source="Engineers", resource_id="group-1")]
        list_roles.return_value = [ExportEntry(key_source="admin", resource_id="role-1")]

        result = runner.invoke(
            app,
            [
                "terraform",
                "export",
                "--output",
                str(output_path),
                "--only",
                "users",
                "--only",
                "groups",
            ],
        )

    assert result.exit_code == 0
    assert "Exported users, groups to" in result.output
    assert output_path.read_text() == (
        'users = {\n'
        '  marcin_at_runlayer_com = "11111111-1111-1111-1111-111111111111"\n'
        "}\n\n"
        'groups = {\n'
        '  engineers = "group-1"\n'
        "}\n"
    )
    list_users.assert_called_once_with(client)
    list_groups.assert_called_once_with(client)
    list_roles.assert_not_called()


def test_export_command_uses_default_output_path(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with (
        patch(
            "runlayer_cli.commands.terraform.resolve_credentials",
            return_value={"secret": "rl_secret", "host": "https://example.com"},
        ),
        patch("runlayer_cli.commands.terraform.set_credentials_in_context"),
        patch("runlayer_cli.commands.terraform.RunlayerClient"),
        patch("runlayer_cli.commands.terraform.list_users_for_terraform", return_value=[]),
        patch("runlayer_cli.commands.terraform.list_groups_for_terraform", return_value=[]),
        patch("runlayer_cli.commands.terraform.list_roles_for_terraform", return_value=[]),
    ):
        result = runner.invoke(app, ["terraform", "export"])

    assert result.exit_code == 0
    output_path = tmp_path / "runlayer.auto.tfvars"
    assert output_path.exists()
    assert output_path.read_text() == "users = {\n}\n\ngroups = {\n}\n\nroles = {\n}\n"
    assert "runlayer.auto.tfvars" in result.output
