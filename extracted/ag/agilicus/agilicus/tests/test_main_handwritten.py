"""Unit tests for hand-written code in agilicus/main.py."""

import json
import os
import tempfile
from datetime import datetime, date
from unittest.mock import patch, MagicMock

import click
import pytest
from click.testing import CliRunner
from prettytable import PrettyTable

from agilicus.main import (
    Config,
    json_serial,
    get_org_id_by_name_or_use_given,
    get_connector_id_from_id_or_name,
    get_saved_orgs,
    get_data_dir,
    get_saved_orgs_path,
    _format_subtable,
    _format_flat_list,
    convert_condition_value,
    override_replace,
    vnc_pw_valid,
    format_signup_as_text,
    output_environment_entries,
)
from agilicus import main as main_module


# ---------------------------------------------------------------------------
# json_serial
# ---------------------------------------------------------------------------
def test_json_serial_datetime():
    dt = datetime(2024, 1, 15, 10, 30, 0)
    assert json_serial(dt) == "2024-01-15T10:30:00"


def test_json_serial_date():
    d = date(2024, 1, 15)
    assert json_serial(d) == "2024-01-15"


def test_json_serial_raises_on_unknown_type():
    with pytest.raises(TypeError, match="not serializable"):
        json_serial(object())


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
def test_config_init():
    cfg = Config()
    assert cfg.path == os.getcwd()
    assert cfg.aliases == {}


def test_config_add_alias():
    cfg = Config()
    cfg.add_alias("foo", "bar")
    assert cfg.aliases == {"foo": "bar"}


def test_config_write_and_read():
    cfg = Config()
    cfg.add_alias("ls", "list-orgs")
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".ini", delete=False) as f:
        f.write("[aliases]\nls = list-orgs\n")
        f.flush()
        path = f.name
    try:
        cfg2 = Config()
        cfg2.read_config(path)
        assert cfg2.aliases == {"ls": "list-orgs"}
    finally:
        os.unlink(path)


def test_config_read_nonexistent_file():
    cfg = Config()
    cfg.read_config("/nonexistent/path/config.ini")
    assert cfg.aliases == {}


# ---------------------------------------------------------------------------
# get_org_id_by_name_or_use_given
# ---------------------------------------------------------------------------
def test_get_org_id_by_name_or_use_given_uses_org_id():
    org_id = get_org_id_by_name_or_use_given({}, org_id="my-id")
    assert org_id == "my-id"


def test_get_org_id_by_name_or_use_given_looks_up_by_name():
    org_by_name = {"myorg": {"id": "found-id"}}
    org_id = get_org_id_by_name_or_use_given(org_by_name, org_name="myorg")
    assert org_id == "found-id"


def test_get_org_id_by_name_or_use_given_none_found_raises():
    with pytest.raises(Exception, match="No such organisation found"):
        get_org_id_by_name_or_use_given({}, org_name="nonexistent")


def test_get_org_id_by_name_or_use_given_returns_none_when_neither():
    assert get_org_id_by_name_or_use_given({}) is None


# ---------------------------------------------------------------------------
# get_connector_id_from_id_or_name
# ---------------------------------------------------------------------------
def test_get_connector_id_from_id_or_name_by_id():
    ctx = MagicMock()
    connector_id = "a" * 22
    result = get_connector_id_from_id_or_name(ctx, connector_id)
    assert result == connector_id


def test_get_connector_id_from_id_or_name_by_name():
    ctx = MagicMock()
    with patch(
        "agilicus.main.connectors.query", return_value=[{"metadata": {"id": "conn-123"}}]
    ):
        result = get_connector_id_from_id_or_name(ctx, "my-connector")
        assert result == "conn-123"


def test_get_connector_id_from_id_or_name_not_found():
    ctx = MagicMock()
    with patch("agilicus.main.connectors.query", return_value=[]):
        result = get_connector_id_from_id_or_name(ctx, "missing-connector")
        assert result is None


# ---------------------------------------------------------------------------
# get_saved_orgs / get_data_dir / get_saved_orgs_path
# ---------------------------------------------------------------------------
def test_get_data_dir_creates_if_needed(monkeypatch, tmp_path):
    data_dir = tmp_path / "agilicus-cli" / "agilicus"
    monkeypatch.setattr("agilicus.main.user_data_dir", lambda *a, **kw: str(data_dir))
    result = get_data_dir()
    assert result == str(data_dir)
    assert os.path.isdir(result)


def test_get_saved_orgs_path(monkeypatch, tmp_path):
    data_dir = tmp_path / "cli-data"
    data_dir.mkdir(parents=True)
    monkeypatch.setattr("agilicus.main.user_data_dir", lambda *a, **kw: str(data_dir))
    result = get_saved_orgs_path()
    assert result.endswith("saved-orgs")


def test_get_saved_orgs_empty_when_no_file(monkeypatch, tmp_path):
    data_dir = tmp_path / "empty-data"
    data_dir.mkdir(parents=True)
    monkeypatch.setattr("agilicus.main.user_data_dir", lambda *a, **kw: str(data_dir))
    assert get_saved_orgs() == []


def test_get_saved_orgs_returns_data(monkeypatch, tmp_path):
    data_dir = tmp_path / "with-data"
    data_dir.mkdir(parents=True)
    monkeypatch.setattr("agilicus.main.user_data_dir", lambda *a, **kw: str(data_dir))
    orgs_file = data_dir / "saved-orgs"
    orgs_file.write_text(json.dumps([{"id": "o1", "org": "Org1"}]))
    assert get_saved_orgs() == [{"id": "o1", "org": "Org1"}]


# ---------------------------------------------------------------------------
# vnc_pw_valid
# ---------------------------------------------------------------------------
def test_vnc_pw_valid_ok():
    ctx = MagicMock()
    param = MagicMock()
    assert vnc_pw_valid(ctx, param, "short") == "short"
    assert vnc_pw_valid(ctx, param, None) is None


def test_vnc_pw_valid_too_long():
    ctx = MagicMock()
    param = MagicMock()
    with pytest.raises(click.BadParameter):
        vnc_pw_valid(ctx, param, "x" * 257)


# ---------------------------------------------------------------------------
# convert_condition_value
# ---------------------------------------------------------------------------
def test_convert_condition_value_bool_true():
    assert convert_condition_value("bool", ["true"]) == "true"


def test_convert_condition_value_bool_false():
    assert convert_condition_value("bool", ["false"]) == "false"


def test_convert_condition_value_int():
    assert convert_condition_value("int", ["42"]) == "42"


def test_convert_condition_value_str():
    assert convert_condition_value("str", ["hello"]) == '"hello"'


def test_convert_condition_value_list():
    result = json.loads(convert_condition_value("list", ["a", "b", "c"]))
    assert result == ["a", "b", "c"]


def test_convert_condition_value_unknown_type():
    with pytest.raises(ValueError, match="not known"):
        convert_condition_value("unknown", ["x"])


# ---------------------------------------------------------------------------
# override_replace
# ---------------------------------------------------------------------------
def test_override_replace_add_new_metric():
    result = override_replace("active_users", [], 5, 100, 10, False)
    assert len(result) == 1
    assert result[0] == {
        "metric": "active_users",
        "min_quantity": 5,
        "max_quantity": 100,
        "step_size": 10,
    }


def test_override_replace_updates_existing():
    existing = [
        {"metric": "active_users", "min_quantity": 1, "max_quantity": 10, "step_size": 1}
    ]
    result = override_replace("active_users", existing, 5, 100, 10, False)
    assert len(result) == 1
    assert result[0] == {
        "metric": "active_users",
        "min_quantity": 5,
        "max_quantity": 100,
        "step_size": 10,
    }


def test_override_replace_with_group_by_org():
    result = override_replace("users", [], 1, 50, 5, True)
    assert result[0]["group_by_org"] is True


def test_override_replace_minimal():
    result = override_replace("sessions", [], None, None, None, False)
    assert result == []


def test_override_replace_only_min():
    result = override_replace("connectors", [], 1, None, None, False)
    assert result == [{"metric": "connectors", "min_quantity": 1}]


# ---------------------------------------------------------------------------
# _format_subtable
# ---------------------------------------------------------------------------
def test_format_subtable_empty():
    result = _format_subtable([])
    assert result is None


def test_format_subtable_non_empty():
    rows = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    result = _format_subtable(rows)
    assert isinstance(result, PrettyTable)
    assert "Alice" in result.get_string()
    assert "Bob" in result.get_string()
    assert "Alice" in result.get_string()


# ---------------------------------------------------------------------------
# _format_flat_list
# ---------------------------------------------------------------------------
def test_format_flat_list():
    assert _format_flat_list([1, 2, 3]) == [1, 2, 3]
    assert _format_flat_list([]) == []
    assert _format_flat_list(["a"]) == ["a"]


# ---------------------------------------------------------------------------
# format_signup_as_text
# ---------------------------------------------------------------------------
def test_format_signup_as_text():
    records = [
        {
            "time": datetime(2024, 1, 15, 10, 0, 0),
            "first_name": "John",
            "last_name": "Doe",
            "user_id": "u1",
            "email": "john@example.com",
            "ip": "1.2.3.4",
            "org_name": "Example Corp",
            "org_id": "org1",
            "country": "US",
            "city": "New York",
        }
    ]
    table = format_signup_as_text(records)
    assert isinstance(table, PrettyTable)
    output = table.get_string()
    assert "John" in output
    assert "Doe" in output
    assert "john@example.com" in output
    assert "Example Corp" in output


def test_format_signup_as_text_multiple_rows():
    records = [
        {
            "time": datetime(2024, 1, 15, 10, 0, 0),
            "first_name": "John",
            "last_name": "Doe",
            "user_id": "u1",
            "email": "john@example.com",
            "ip": "1.2.3.4",
            "org_name": "Example Corp",
            "org_id": "org1",
            "country": "US",
            "city": "New York",
        },
        {
            "time": datetime(2024, 2, 20, 14, 0, 0),
            "first_name": "Jane",
            "last_name": "Smith",
            "user_id": "u2",
            "email": "jane@example.com",
            "ip": "5.6.7.8",
            "org_name": "Other Corp",
            "org_id": "org2",
            "country": "CA",
            "city": "Toronto",
        },
    ]
    table = format_signup_as_text(records)
    output = table.get_string()
    assert "John" in output
    assert "Jane" in output


# ---------------------------------------------------------------------------
# output_environment_entries
# ---------------------------------------------------------------------------
def test_output_environment_entries_json(capsys):
    ctx = MagicMock()
    ctx.obj = {"output_format": "json"}
    entry = {"name": "env1", "status": "active"}
    with patch("agilicus.main.output_json") as mock_output:
        output_environment_entries(ctx, entry)
        mock_output.assert_called_once_with(ctx, entry)


def test_output_environment_entries_table(capsys):
    ctx = MagicMock()
    ctx.obj = {"output_format": "table"}
    entry = {"name": "env1", "status": "active"}
    output_environment_entries(ctx, entry)
    captured = capsys.readouterr()
    assert "env1" in captured.out
    assert "active" in captured.out


# ---------------------------------------------------------------------------
# output_tokens_list (table path)
# ---------------------------------------------------------------------------
def test_output_tokens_list_table(capsys):
    from agilicus.main import output_tokens_list

    ctx = MagicMock()
    ctx.obj = {"output_format": "table"}
    tokens_list = [
        {
            "jti": "jti-1",
            "roles": ["admin"],
            "iat": 1234567890,
            "exp": 1234567890,
            "aud": ["aud1"],
            "sub": "user1",
            "session": "sess1",
            "revoked": False,
            "scopes": ["openid"],
            "updated": "2024-01-01",
            "masquerading": "---",
        }
    ]
    output_tokens_list(ctx, tokens_list)
    captured = capsys.readouterr()
    assert "jti-1" in captured.out
    assert "user1" in captured.out


def test_output_tokens_list_json(capsys):
    from agilicus.main import output_tokens_list

    ctx = MagicMock()
    ctx.obj = {"output_format": "json"}
    tokens_list = [{"jti": "jti-1"}]
    with patch("agilicus.main.output_json") as mock_output:
        output_tokens_list(ctx, tokens_list)
        mock_output.assert_called_once_with(ctx, tokens_list)


# ---------------------------------------------------------------------------
# output_list_orgs
# ---------------------------------------------------------------------------
def test_output_list_orgs_table(capsys):
    from agilicus.main import output_list_orgs

    ctx = MagicMock()
    ctx.obj = {"output_format": "table"}
    orgs_list = [
        {
            "id": "org1",
            "organisation": "Example Corp",
            "created": datetime(2024, 1, 1),
            "admin_state": "active",
            "contact_email": "admin@example.com",
            "issuer": "issuer1",
            "subdomain": "example",
        }
    ]
    output_list_orgs(ctx, orgs_list)
    captured = capsys.readouterr()
    assert "Example Corp" in captured.out


def test_output_list_orgs_json():
    from agilicus.main import output_list_orgs

    ctx = MagicMock()
    ctx.obj = {"output_format": "json"}
    with patch("agilicus.main.output_json") as mock_output:
        output_list_orgs(ctx, [])
        mock_output.assert_called_once_with(ctx, [])


def test_output_list_orgs_handles_missing_subdomain(capsys):
    from agilicus.main import output_list_orgs

    ctx = MagicMock()
    ctx.obj = {"output_format": "table"}
    orgs_list = [
        {"id": "org1", "organisation": "No Subdomain", "created": datetime(2024, 1, 1)}
    ]
    output_list_orgs(ctx, orgs_list)
    captured = capsys.readouterr()
    assert "No Subdomain" in captured.out


# ---------------------------------------------------------------------------
# output_list_groups
# ---------------------------------------------------------------------------
def test_output_list_groups_table(capsys):
    from agilicus.main import output_list_groups

    ctx = MagicMock()
    ctx.obj = {"output_format": "table"}
    groups = [
        {
            "id": "g1",
            "email": "group@example.com",
            "members": [{"email": "user@example.com"}],
        }
    ]
    output_list_groups(ctx, groups, hide_members=False)
    captured = capsys.readouterr()
    assert "group@example.com" in captured.out


def test_output_list_groups_hide_members(capsys):
    from agilicus.main import output_list_groups

    ctx = MagicMock()
    ctx.obj = {"output_format": "table"}
    groups = [
        {
            "id": "g1",
            "email": "group@example.com",
            "members": [{"email": "user@example.com"}],
        }
    ]
    output_list_groups(ctx, groups, hide_members=True)
    captured = capsys.readouterr()
    assert "group@example.com" in captured.out


def test_output_list_groups_json():
    from agilicus.main import output_list_groups

    ctx = MagicMock()
    ctx.obj = {"output_format": "json"}
    with patch("agilicus.main.output_json") as mock_output:
        output_list_groups(ctx, [], hide_members=False)
        mock_output.assert_called_once_with(ctx, [])


# ---------------------------------------------------------------------------
# output_list_apps
# ---------------------------------------------------------------------------
def test_output_list_apps_table(capsys):
    from agilicus.main import output_list_apps

    ctx = MagicMock()
    ctx.obj = {"output_format": "table"}
    orgs_by_id = {"org1": {"organisation": "Example Corp"}}
    AppEntry = MagicMock()
    AppEntry.id = "app1"
    AppEntry.name = "MyApp"
    AppEntry.org_id = "org1"
    apps_list = [AppEntry]
    output_list_apps(ctx, orgs_by_id, apps_list)
    captured = capsys.readouterr()
    assert "MyApp" in captured.out
    assert "Example Corp" in captured.out


def test_output_list_apps_no_org(capsys):
    from agilicus.main import output_list_apps

    ctx = MagicMock()
    ctx.obj = {"output_format": "table"}
    orgs_by_id = {}
    AppEntry = MagicMock()
    AppEntry.id = "app1"
    AppEntry.name = "MyApp"
    AppEntry.org_id = "org1"
    apps_list = [AppEntry]
    output_list_apps(ctx, orgs_by_id, apps_list)
    captured = capsys.readouterr()
    assert "MyApp" in captured.out
    assert "none" in captured.out


def test_output_list_apps_json():
    from agilicus.main import output_list_apps

    ctx = MagicMock()
    ctx.obj = {"output_format": "json"}
    with patch("agilicus.main.output_json") as mock_output:
        AppEntry = MagicMock()
        AppEntry.to_dict.return_value = {"id": "app1"}
        output_list_apps(ctx, {}, [AppEntry])
        mock_output.assert_called_once()


# ---------------------------------------------------------------------------
# _format_subtable_objs (uses objects with .to_dict())
# ---------------------------------------------------------------------------
def test_format_subtable_objs_none():
    from agilicus.main import _format_subtable_objs

    assert _format_subtable_objs(None) is None


def test_format_subtable_objs_with_objects():
    from agilicus.main import _format_subtable_objs

    obj = MagicMock()
    obj.to_dict.return_value = {"key": "value"}
    result = _format_subtable_objs([obj])
    assert isinstance(result, PrettyTable)
    assert "value" in result.get_string()


# ---------------------------------------------------------------------------
# main function - verifies subcommand groups are attached
# ---------------------------------------------------------------------------
def test_main_adds_all_subcommands():
    with patch.object(main_module, "trusted_certs_main") as mock_tc, patch.object(
        main_module, "hosts_main"
    ) as mock_hosts, patch.object(
        main_module, "labels_main"
    ) as mock_labels, patch.object(
        main_module, "rules_main"
    ) as mock_rules, patch.object(
        main_module, "policy_main"
    ) as mock_policy, patch.object(
        main_module, "products_main"
    ) as mock_products, patch.object(
        main_module, "credentials_main"
    ) as mock_creds, patch.object(
        main_module, "features_main"
    ) as mock_features, patch.object(
        main_module, "files_main"
    ) as mock_files, patch.object(
        main_module, "policy_config_main"
    ) as mock_pcfg, patch.object(
        main_module, "messages_main"
    ) as mock_msgs, patch.object(
        main_module, "databases"
    ) as mock_dbs, patch.object(
        main_module, "licensing_main"
    ) as mock_lic, patch.object(
        main_module, "deployments_main"
    ) as mock_deps, patch.object(
        main_module, "cli"
    ) as mock_cli:

        main_module.main()

        # Verify each subcommand group's add_commands was called with cli
        mock_tc.add_commands.assert_called_once_with(main_module.cli)
        mock_hosts.add_commands.assert_called_once_with(main_module.cli)
        mock_labels.add_commands.assert_called_once_with(main_module.cli)
        mock_rules.add_commands.assert_called_once_with(main_module.cli)
        mock_policy.add_commands.assert_called_once_with(main_module.cli)
        mock_products.add_commands.assert_called_once_with(main_module.cli)
        mock_creds.add_commands.assert_called_once_with(main_module.cli)
        mock_features.add_commands.assert_called_once_with(main_module.cli)
        mock_files.add_commands.assert_called_once_with(main_module.cli)
        mock_pcfg.add_commands.assert_called_once_with(main_module.cli)
        mock_msgs.add_commands.assert_called_once_with(main_module.cli)
        mock_dbs.add_commands.assert_called_once_with(main_module.cli)
        mock_lic.add_commands.assert_called_once_with(main_module.cli)
        mock_deps.add_commands.assert_called_once_with(main_module.cli)

        # Verify cli was called with envvar prefix
        mock_cli.assert_called_once_with(auto_envvar_prefix="AGILICUS")


# ---------------------------------------------------------------------------
# cli function - context setup via CliRunner
# The cli callback always creates a RefreshableAccessToken which reads from
# keyring; CI environments lack a keyring session so we mock it out.
# ---------------------------------------------------------------------------
def _cli_auth_mocks():
    return (
        patch("agilicus.main.tokens.RefreshableAccessToken", return_value=MagicMock()),
        patch("agilicus.main.tokens.RefreshableServiceToken", return_value=MagicMock()),
        patch("agilicus.main.context.save_refreshable_token"),
        patch("agilicus.main.context.save"),
    )


def test_cli_root_sets_context():
    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(main_module.cli, ["--help"], catch_exceptions=False)
        assert result.exit_code == 0
        assert "Usage:" in result.output


def test_cli_root_with_token():
    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli,
            ["--token", "test-token", "--help"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0


def test_cli_root_with_admin_flag():
    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli,
            ["--admin", "--help"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# prompt function
# ---------------------------------------------------------------------------
def test_prompt_without_org(monkeypatch):
    from agilicus.main import prompt

    ctx = MagicMock()
    monkeypatch.setattr(
        "agilicus.main.context.get_issuer", lambda c: "https://auth.example.com/"
    )
    monkeypatch.setattr("agilicus.main.context.get_org", lambda c: None)
    result = prompt(ctx)
    assert "example.com" in result


def test_prompt_without_org_auth_prefix(monkeypatch):
    from agilicus.main import prompt

    ctx = MagicMock()
    monkeypatch.setattr(
        "agilicus.main.context.get_issuer", lambda c: "https://auth.acme.com/"
    )
    monkeypatch.setattr("agilicus.main.context.get_org", lambda c: None)
    result = prompt(ctx)
    assert "acme.com" in result


def test_prompt_with_org(monkeypatch):
    from agilicus.main import prompt

    ctx = MagicMock()
    monkeypatch.setattr(
        "agilicus.main.context.get_issuer", lambda c: "https://auth.example.com/"
    )
    monkeypatch.setattr(
        "agilicus.main.context.get_org", lambda c: {"subdomain": "mysub"}
    )
    result = prompt(ctx)
    assert "mysub" in result


# ---------------------------------------------------------------------------
# read_config callback
# ---------------------------------------------------------------------------
def test_read_config_loads_file(monkeypatch):
    from agilicus.main import read_config

    cfg_content = "[aliases]\nls = list-orgs\n"
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".ini", delete=False) as f:
        f.write(cfg_content)
        f.flush()
        path = f.name
    try:
        ctx = MagicMock()
        cfg = Config()
        ctx.ensure_object.return_value = cfg
        result = read_config(ctx, None, path)
        assert result == path
        assert cfg.aliases == {"ls": "list-orgs"}
    finally:
        os.unlink(path)


def test_read_config_uses_default(monkeypatch, tmp_path):
    from agilicus.main import read_config

    ctx = MagicMock()
    cfg = Config()
    ctx.ensure_object.return_value = cfg
    result = read_config(ctx, None, None)
    assert result is not None


# ---------------------------------------------------------------------------
# get_user_id_from_email
# ---------------------------------------------------------------------------
def test_get_user_id_from_email_found():
    from agilicus.main import get_user_id_from_email

    ctx = MagicMock()
    with patch(
        "agilicus.main.users.query",
        return_value=[{"id": "u1", "email": "user@example.com"}],
    ):
        result = get_user_id_from_email(ctx, "user@example.com")
        assert result == {"id": "u1", "email": "user@example.com"}


def test_get_user_id_from_email_not_found():
    from agilicus.main import get_user_id_from_email

    ctx = MagicMock()
    with patch("agilicus.main.users.query", return_value=[]):
        result = get_user_id_from_email(ctx, "missing@example.com")
        assert result == {}


def test_get_user_id_from_email_multiple_found():
    from agilicus.main import get_user_id_from_email

    ctx = MagicMock()
    with patch("agilicus.main.users.query", return_value=[{"id": "u1"}, {"id": "u2"}]):
        result = get_user_id_from_email(ctx, "dup@example.com")
        assert result == {}


# ---------------------------------------------------------------------------
# get_user_from_email_or_id
# ---------------------------------------------------------------------------
def test_get_user_from_email_or_id_by_email():
    from agilicus.main import get_user_from_email_or_id

    ctx = MagicMock()
    with patch(
        "agilicus.main.input_helpers.get_user_id_from_input_or_ctx",
        return_value="user@example.com",
    ), patch(
        "agilicus.main.get_user_id_from_email",
        return_value={"id": "u1", "email": "user@example.com"},
    ):
        result = get_user_from_email_or_id(ctx, user_id_or_email="user@example.com")
        assert result == {"id": "u1", "email": "user@example.com"}


def test_get_user_from_email_or_id_by_id():
    from agilicus.main import get_user_from_email_or_id

    ctx = MagicMock()
    with patch(
        "agilicus.main.input_helpers.get_user_id_from_input_or_ctx",
        return_value="user-id-123",
    ), patch("agilicus.main.get_user_id_from_email", return_value={}), patch(
        "agilicus.main.users.get_user",
        return_value={"id": "user-id-123", "email": "x@y.com"},
    ):
        result = get_user_from_email_or_id(ctx, user_id_or_email="user-id-123")
        assert result == {"id": "user-id-123", "email": "x@y.com"}


def test_get_user_from_email_or_id_not_found():
    from agilicus.main import get_user_from_email_or_id

    ctx = MagicMock()
    with patch(
        "agilicus.main.input_helpers.get_user_id_from_input_or_ctx",
        return_value="unknown@bad.com",
    ), patch("agilicus.main.get_user_id_from_email", return_value={}), patch(
        "agilicus.main.users.get_user", return_value=None
    ):
        result = get_user_from_email_or_id(ctx, user_id_or_email="unknown@bad.com")
        assert result is None


# ---------------------------------------------------------------------------
# user_id_or_id_from_email
# ---------------------------------------------------------------------------
def test_user_id_or_id_from_email_found():
    from agilicus.main import user_id_or_id_from_email

    ctx = MagicMock()
    with patch("agilicus.main.get_user_from_email_or_id", return_value={"id": "u1"}):
        result = user_id_or_id_from_email(ctx, user_id_or_email="user@example.com")
        assert result == "u1"


def test_user_id_or_id_from_email_not_found():
    from agilicus.main import user_id_or_id_from_email

    ctx = MagicMock()
    with patch("agilicus.main.get_user_from_email_or_id", return_value=None):
        result = user_id_or_id_from_email(ctx, user_id_or_email="unknown")
        assert result is None


# ---------------------------------------------------------------------------
# get_org_id
# ---------------------------------------------------------------------------
def test_get_org_id_by_name():
    from agilicus.main import get_org_id

    ctx = MagicMock()
    org_by_name = {"myorg": {"id": "org-found"}}
    with patch(
        "agilicus.main.orgs.get_org_by_dictionary", return_value=(None, org_by_name)
    ):
        result = get_org_id(ctx, org_name="myorg")
        assert result == "org-found"


def test_get_org_id_by_id_direct():
    from agilicus.main import get_org_id

    ctx = MagicMock()
    with patch("agilicus.main.orgs.get_org_by_dictionary", return_value=(None, {})):
        result = get_org_id(ctx, org_id="direct-id")
        assert result == "direct-id"


# ---------------------------------------------------------------------------
# output_gw_audit_list
# ---------------------------------------------------------------------------
def test_output_gw_audit_list_table(capsys):
    from agilicus.main import output_gw_audit_list

    ctx = MagicMock()
    ctx.obj = {"output_format": "table"}
    audit_list = [
        {"time": "2024-01-01", "authority": "auth1", "token_id": "tok1"},
        {"time": "2024-01-02", "authority": "auth2", "token_id": "tok2"},
    ]
    output_gw_audit_list(ctx, audit_list)
    captured = capsys.readouterr()
    assert "auth1" in captured.out
    assert "tok2" in captured.out


def test_output_gw_audit_list_json():
    from agilicus.main import output_gw_audit_list

    ctx = MagicMock()
    ctx.obj = {"output_format": "json"}
    with patch("agilicus.main.output_json") as mock_output:
        output_gw_audit_list(ctx, [])
        mock_output.assert_called_once()


# ---------------------------------------------------------------------------
# _format_roles
# ---------------------------------------------------------------------------
def test_format_roles_table():
    from agilicus.main import _format_roles

    roles = MagicMock()
    roles.to_dict.return_value = {"myapp": ["admin", "user"], "other": ["read"]}
    result = _format_roles(roles)
    assert isinstance(result, PrettyTable)
    output = result.get_string()
    assert "myapp" in output
    assert "admin" in output


# ---------------------------------------------------------------------------
# _get_app helper
# ---------------------------------------------------------------------------
def test_get_app_found():
    from agilicus.main import _get_app

    ctx = MagicMock()
    with patch("agilicus.main.apps.get_app", return_value={"id": "a1", "name": "myapp"}):
        result = _get_app(ctx, "myapp")
        assert result == {"id": "a1", "name": "myapp"}


def test_get_app_not_found(capsys):
    from agilicus.main import _get_app

    ctx = MagicMock()
    with patch("agilicus.main.apps.get_app", return_value=None):
        result = _get_app(ctx, "missing")
        assert result is None
        captured = capsys.readouterr()
        assert "not found" in captured.out


# ---------------------------------------------------------------------------
# switch_org
# ---------------------------------------------------------------------------
def test_switch_org():
    from agilicus.main import switch_org

    ctx = MagicMock()
    ctx.obj = {}
    org = {"id": "org-123", "organisation": "Test Org"}
    with patch("agilicus.main.click.get_current_context", return_value=ctx), patch(
        "agilicus.main.context.save_refreshable_token"
    ), patch("agilicus.main.orgs.get", return_value=org), patch(
        "agilicus.main.context.save"
    ):
        switch_org(org)
        assert ctx.obj["ORG_ID"] == "org-123"
        assert ctx.obj["ORGANISATION"] == org


# ---------------------------------------------------------------------------
# completion functions (verify they call the correct APIs)
# ---------------------------------------------------------------------------
def test_connector_completion():
    from agilicus.main import connector_completion

    ctx = MagicMock()
    with patch(
        "agilicus.main.connectors.query",
        return_value=[
            {"spec": {"name": "conn-abc"}},
            {"spec": {"name": "conn-xyz"}},
            {"spec": {"name": "other"}},
        ],
    ):
        results = connector_completion(ctx, [], "conn")
        assert results == ["conn-abc", "conn-xyz"]


def test_app_completion():
    from agilicus.main import app_completion

    ctx = MagicMock()
    with patch(
        "agilicus.main.apps.query",
        return_value=[
            {"name": "myapp"},
            {"name": "myotherapp"},
            {"name": "other"},
        ],
    ):
        results = app_completion(ctx, [], "my")
        assert results == ["myapp", "myotherapp"]


def test_user_completion():
    from agilicus.main import user_completion

    ctx = MagicMock()
    with patch(
        "agilicus.main.users.query",
        return_value=[
            {"email": "alice@example.com"},
            {"email": "bob@example.com"},
        ],
    ):
        results = user_completion(ctx, [], "")
        assert "alice@example.com" in results
        assert "bob@example.com" in results


def test_sub_org_completion():
    from agilicus.main import sub_org_completion

    ctx = MagicMock()
    with patch(
        "agilicus.main.orgs.query_suborgs",
        return_value=[
            {"organisation": "SubOrg-A"},
            {"organisation": "SubOrg-B"},
            {"organisation": "Other"},
        ],
    ):
        results = sub_org_completion(ctx, [], "Sub")
        assert results == ["SubOrg-A", "SubOrg-B"]


# ---------------------------------------------------------------------------
# cli subcommands smoke - ensure commands exist
# In CI, the cli callback tries to read from keyring / do auth which can hang.
# Patch out the token refresh so these are safe to run without a keyring session.
# ---------------------------------------------------------------------------
def test_cli_list_users_command_help():
    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli, ["list-users", "--help"], catch_exceptions=False
        )
        assert result.exit_code == 0
        assert "--org-id" in result.output


def test_cli_whoami_help():
    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli, ["whoami", "--help"], catch_exceptions=False
        )
        assert result.exit_code == 0


def test_cli_list_orgs_help():
    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli, ["list-orgs", "--help"], catch_exceptions=False
        )
        assert result.exit_code == 0


def test_cli_show_user_help():
    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli, ["show-user", "--help"], catch_exceptions=False
        )
        assert result.exit_code == 0


def test_cli_version_command():
    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(main_module.cli, ["version"], catch_exceptions=False)
        assert result.exit_code == 0
        assert result.output.strip() != ""
