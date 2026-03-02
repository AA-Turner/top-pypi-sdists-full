import builtins
import json
import os
from pathlib import Path

import pytest
import yaml

import tmo.tmo_cli as tmo_cli
from types import SimpleNamespace


def test_bash_escape_handles_backslashes_and_none():
    assert tmo_cli.bash_escape(r"C:\path\to\file") == r"C:\\path\\to\\file"
    assert tmo_cli.bash_escape("") == ""
    assert tmo_cli.bash_escape(None) is None


def test_print_underscored_outputs_message_and_underline(capsys):
    tmo_cli.print_underscored("Hello")
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    assert lines[0] == "Hello"
    assert lines[1] == "-" * len("Hello")


def test_yes_or_no_returns_true_and_false(monkeypatch):
    # simulate answering 'y'
    monkeypatch.setattr(builtins, "input", lambda prompt="": "y")
    assert tmo_cli.yes_or_no("question") is True

    # simulate answering 'n'
    monkeypatch.setattr(builtins, "input", lambda prompt="": "n")
    assert tmo_cli.yes_or_no("question") is False


def test_set_cwd_nonexistent_path_exits(monkeypatch):
    # Force os.path.exists to return False inside module
    monkeypatch.setattr(tmo_cli.os.path, "exists", lambda path: False)
    with pytest.raises(SystemExit) as exc:
        tmo_cli.set_cwd("/nonexistent/path")
    assert exc.value.code == 1


def test_handle_generic_error_debug_true_logs_exception(caplog):
    caplog.clear()
    # debug True should call logging.exception and not exit
    tmo_cli.handle_generic_error(Exception("boom"), debug=True)
    assert any(
        "An error occurred, printing stack trace output." in r.getMessage()
        or "An error occurred" in r.getMessage()
        for r in caplog.records
    )


def test_handle_generic_error_debug_false_exits_and_logs(caplog):
    caplog.clear()
    with pytest.raises(SystemExit) as exc:
        tmo_cli.handle_generic_error(Exception("boom"), debug=False)
    assert exc.value.code == 1
    assert any("An error occurred" in r.getMessage() for r in caplog.records)


def test_link_repo_calls_write_repo_config(monkeypatch, capsys):
    # Prepare a fake project returned by the selection function
    monkeypatch.setattr(
        tmo_cli,
        "list_and_select_projects",
        lambda _repo_manager, tmo_client, a, b: {"id": "proj-123"},
    )

    class DummyRepoManager:
        def __init__(self):
            self.written = None

        def write_repo_config(self, config, path=None):
            # mirror behavior: accept optional path param
            self.written = (config, path)

    repo_manager = DummyRepoManager()
    # call link_repo and capture stdout
    tmo_cli.link_repo(repo_manager, None)
    out, _ = capsys.readouterr()
    assert repo_manager.written == (
        {"project_id": "proj-123"},
    ) or repo_manager.written == ({"project_id": "proj-123"}, None)
    assert "Repo linked to Project." in out


def test_input_string_required_retry(monkeypatch, capsys):
    calls = {"count": 0}

    def fake_input(prompt=""):
        calls["count"] += 1
        if calls["count"] == 1:
            return ""
        return "value"

    monkeypatch.setattr("builtins.input", fake_input)
    val = tmo_cli.input_string("name", required=True)
    assert val == "value"


def test_input_string_password_getpass(monkeypatch):
    monkeypatch.setattr("getpass.getpass", lambda prompt=None: "secret")
    val = tmo_cli.input_string(
        "pwd", required=True, password=True, is_called_from_test=False
    )
    assert val == "secret"


def test_input_select_default_and_invalid(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    values = ["a", "b"]
    res = tmo_cli.input_select("item", values, default="a")
    assert res == "a"
    # test invalid selection then valid
    seq = iter(["", "2", "1"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(seq))
    res2 = tmo_cli.input_select("item", values)
    assert res2 == "b"


def test_list_connections_no_file(tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    args = SimpleNamespace(cwd=None)
    with pytest.raises(SystemExit):
        tmo_cli.list_connections(args)


def test_add_connections_writes_file(tmp_path, monkeypatch):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    args = SimpleNamespace(
        cwd=None,
        name="conn1",
        username="u",
        password="p",
        host="h",
        database="db",
        val_db="VAL",
        byom_db="MLDB",
        logmech="TDNEGO",
        parent_parser=None,
    )
    monkeypatch.setattr(tmo_cli.crypto, "td_encrypt_password", lambda **kwargs: "ENC")
    tmo_cli.add_connections(args)
    f = Path(tmo_cli.config_dir) / "connections.yaml"
    assert f.exists()
    assert "connections" in yaml.safe_load(open(f))


def test_remove_connections_no_file(tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    args = SimpleNamespace(cwd=None, connection=None)
    with pytest.raises(SystemExit) as exc:
        tmo_cli.remove_connections(args)
    assert exc.value.code == 0


def test_remove_connections_not_exists(tmp_path, monkeypatch):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)
    con = {
        "connections": [{
            "id": "abc",
            "name": "n",
            "username": "u",
            "password": "p",
            "host": "h",
            "logmech": "TDNEGO",
        }]
    }
    yaml.safe_dump(con, open(Path(tmo_cli.config_dir) / "connections.yaml", "w+"))
    args = SimpleNamespace(cwd=None, connection="notfound")
    with pytest.raises(SystemExit) as exc:
        tmo_cli.remove_connections(args)
    assert exc.value.code == 1


def test_remove_connections_success(tmp_path, monkeypatch):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)
    conn_id = "c1"
    con = {
        "connections": [{
            "id": conn_id,
            "name": "n",
            "username": "u",
            "password": "p",
            "host": "h",
            "logmech": "TDNEGO",
        }]
    }
    yaml.safe_dump(con, open(Path(tmo_cli.config_dir) / "connections.yaml", "w+"))
    Path(tmo_cli.config_dir, f"{conn_id}.key").write_text("k")
    Path(tmo_cli.config_dir, f"{conn_id}.pass").write_text("p")
    args = SimpleNamespace(cwd=None, connection=None)
    monkeypatch.setattr(tmo_cli, "input_select", lambda *a, **k: "n")
    tmo_cli.remove_connections(args)
    data = yaml.safe_load(open(Path(tmo_cli.config_dir) / "connections.yaml"))
    assert data.get("connections", []) == []
    assert not Path(tmo_cli.config_dir, f"{conn_id}.key").exists()


def test_export_connection_prints(tmp_path, monkeypatch, capsys):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)
    connection = {
        "id": "c1",
        "name": "n",
        "username": "u",
        "password": "p",
        "host": "h",
        "logmech": "TDNEGO",
        "database": "db",
        "val_db": "VAL",
        "byom_db": "BYOM",
    }
    yaml.safe_dump(
        {"connections": [connection]},
        open(Path(tmo_cli.config_dir) / "connections.yaml", "w+"),
    )
    args = SimpleNamespace(cwd=None, connection=None)
    monkeypatch.setattr(tmo_cli, "input_select", lambda *a, **k: "n")
    tmo_cli.export_connection(args)


def test_activate_connection_sets_env_and_returns(tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)
    connection = {
        "id": "c1",
        "name": "n",
        "username": "u",
        "password": "p",
        "host": "h",
        "logmech": "TDNEGO",
        "database": "db",
    }
    yaml.safe_dump(
        {"connections": [connection]},
        open(Path(tmo_cli.config_dir) / "connections.yaml", "w+"),
    )
    args = SimpleNamespace(cwd=None, connection="c1")
    ret = tmo_cli.activate_connection(args)
    assert ret == "c1"
    assert os.environ.get("VMO_CONN_USERNAME") == "u"


def test_activate_connection_auto_select(monkeypatch, tmp_path, capsys):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)
    connection = {
        "id": "c1",
        "name": "n",
        "username": "u",
        "password": "p",
        "host": "h",
        "logmech": "TDNEGO",
        "database": "db",
    }
    yaml.safe_dump(
        {"connections": [connection]},
        open(Path(tmo_cli.config_dir) / "connections.yaml", "w+"),
    )
    args = SimpleNamespace(cwd=None, connection=None)
    ret = tmo_cli.activate_connection(args)
    assert ret == "c1"


def test_test_connection_success(monkeypatch, tmp_path, capsys):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)
    connection = {
        "id": "c1",
        "name": "n",
        "username": "u",
        "password": "p",
        "host": "h",
        "logmech": "TDNEGO",
    }
    yaml.safe_dump(
        {"connections": [connection]},
        open(Path(tmo_cli.config_dir) / "connections.yaml", "w+"),
    )
    import tmo

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)

    class R:
        def fetchall(self):
            return [("ver1",)]

    monkeypatch.setattr(tmo, "execute_sql", lambda q: R())
    args = SimpleNamespace(cwd=None, connection="c1")
    tmo_cli.test_connection(args)


def test_test_connection_failure(monkeypatch, tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)
    connection = {
        "id": "c1",
        "name": "n",
        "username": "u",
        "password": "p",
        "host": "h",
        "logmech": "TDNEGO",
    }
    yaml.safe_dump(
        {"connections": [connection]},
        open(Path(tmo_cli.config_dir) / "connections.yaml", "w+"),
    )
    import tmo

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)
    monkeypatch.setattr(
        tmo, "execute_sql", lambda q: (_ for _ in ()).throw(Exception("fail"))
    )
    args = SimpleNamespace(cwd=None, connection="c1")
    with pytest.raises(SystemExit):
        tmo_cli.test_connection(args)


def test_create_byom_table_no_execute(tmp_path):
    args = SimpleNamespace(cwd=None, name="tbl", execute_ddl=False)
    tmo_cli.create_byom_table(args)


def test_create_byom_table_execute_error(monkeypatch, tmp_path):
    args = SimpleNamespace(cwd=None, name="tbl", execute_ddl=True)
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)
    monkeypatch.setattr(
        tmo, "execute_sql", lambda q: (_ for _ in ()).throw(Exception("boom"))
    )
    with pytest.raises(tmo_cli.EntityCreationError):
        tmo_cli.create_byom_table(args)


def test_set_cwd_success(tmp_path):
    d = tmp_path / "repo"
    d.mkdir()
    tmo_cli.set_cwd(str(d))
    assert tmo_cli.base_path == str(d.resolve())
    assert tmo_cli.model_catalog.endswith(tmo_cli.MODEL_CATALOG_PATH + "/")


def test_print_help_shows_version(capsys):
    ns = SimpleNamespace(version=True)
    tmo_cli.print_help(ns, parent_parser=None)
    out, _ = capsys.readouterr()
    from tmo import __version__

    assert __version__ in out


def test_list_and_select_projects_as_list(monkeypatch, capsys):
    monkeypatch.setattr("tmo.ProjectApi", lambda tmo_client, show_archived=False: [])
    ret = tmo_cli.list_and_select_projects(None, None, as_list=True, check_config=False)
    assert ret is None


def test_get_current_project_found(monkeypatch):
    class RM:
        def read_repo_config(self):
            return {"project_id": "p1"}

    class PApi:
        def __init__(self, tmo_client, show_archived=False):
            pass

        def find_by_id(self, pid):
            return {"id": pid, "name": "proj"}

    monkeypatch.setattr("tmo.ProjectApi", PApi)
    monkeypatch.setattr(tmo_cli, "validate_model_catalog_cwd_valid", lambda: True)
    res = tmo_cli.get_current_project(RM(), None, check_repo_conf=False)
    assert res["id"] == "p1"


def test_validate_model_and_fe_tasks_cwd_valid(tmp_path, monkeypatch):
    d_model = tmp_path / "models"
    d_model.mkdir(parents=True)
    tmo_cli.model_catalog = str(d_model) + "/"
    assert tmo_cli.validate_model_catalog_cwd_valid() is True
    d_model.rmdir()
    assert tmo_cli.validate_model_catalog_cwd_valid() is False

    d_tasks = tmp_path / "fe_tasks"
    d_tasks.mkdir(parents=True)
    tmo_cli.fe_tasks_catalog = str(d_tasks) + "/"
    assert tmo_cli.validate_fe_tasks_cwd_valid() is True
    d_tasks.rmdir()
    assert tmo_cli.validate_fe_tasks_cwd_valid() is False


def test_init_model_directory_calls_link_when_no_repo_config(monkeypatch):
    class RM:
        def __init__(self):
            self.inited = False

        def init_model_directory(self):
            self.inited = True

        def repo_config_exists(self):
            return False

    repo_manager = RM()
    called = {"link": False}
    monkeypatch.setattr(
        tmo_cli,
        "link_repo",
        lambda repo_manager, tmo_client: called.update({"link": True}),
    )
    args = type("A", (), {"cwd": None})()
    tmo_cli.init_model_directory(args, repo_manager, None)
    assert repo_manager.inited is True
    assert called["link"] is True


def test_add_model_templates_empty_exits(monkeypatch, tmp_path):
    args = type("A", (), {"cwd": None, "template_url": "u", "branch": "b"})()

    class RM:
        def clone_repository(self, url, path, branch):
            return None

        def get_templates(self, entity_type=None, source_path=None):
            return {}

        def repo_config_exists(self):
            return True

    monkeypatch.setattr(tmo_cli, "validate_model_catalog_cwd_valid", lambda: True)
    with pytest.raises(SystemExit):
        tmo_cli.add_model(args, RM())


def test_run_model_no_models_exits(monkeypatch):
    args = type(
        "A",
        (),
        {
            "cwd": None,
            "model_id": None,
            "mode": None,
            "local_dataset": None,
            "local_dataset_template": None,
            "dataset_id": None,
            "dataset_template_id": None,
            "connection": None,
        },
    )()
    monkeypatch.setattr(
        tmo_cli,
        "get_current_project",
        lambda repo_manager, tmo_client, check: {"id": "p1"},
    )
    import tmo

    class Client:
        def set_project_id(self, pid):
            pass

    monkeypatch.setattr(tmo.TrainModel, "get_model_ids", lambda catalog, arg: {})
    with pytest.raises(SystemExit):
        tmo_cli.run_model(args, None, Client())


def test_list_resources_invalid_selection_calls_help_and_exits(monkeypatch):
    args = type(
        "A",
        (),
        {
            "cwd": None,
            "projects": False,
            "models": False,
            "local_models": False,
            "templates": False,
            "datasets": False,
            "connections": False,
        },
    )()
    parent = type("P", (), {"print_help": lambda self: None})()
    with pytest.raises(SystemExit):
        tmo_cli.list_resources(args, None, None, parent_parser=parent)


def test_input_select_empty_values_returns_none():
    result = tmo_cli.input_select("test", [])
    assert result is None


def test_input_select_numeric_validation(monkeypatch):
    seq = iter(["abc", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(seq))
    values = ["option1", "option2"]
    result = tmo_cli.input_select("item", values)
    assert result == "option1"


def test_yes_or_no_invalid_input_retry(monkeypatch):
    seq = iter(["maybe", "x", "y"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(seq))
    result = tmo_cli.yes_or_no("question")
    assert result is True


def test_bash_escape_with_multiple_backslashes():
    assert tmo_cli.bash_escape(r"C:\path\to\file\dir") == r"C:\\path\\to\\file\\dir"


def test_input_string_empty_not_required():
    import builtins
    import tmo.tmo_cli

    original_input = builtins.input
    builtins.input = lambda prompt="": ""
    result = tmo_cli.input_string("test", required=False)
    builtins.input = original_input
    assert result == ""


def test_input_string_tooltip_displays(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "value")
    tmo_cli.input_string("test", tooltip="This is a tooltip")
    out, _ = capsys.readouterr()
    assert "This is a tooltip" in out


def test_set_cwd_updates_global_paths(tmp_path):
    test_dir = tmp_path / "test_repo"
    test_dir.mkdir()
    tmo_cli.set_cwd(str(test_dir))
    assert tmo_cli.base_path == str(test_dir.resolve())
    assert tmo_cli.model_catalog == str(test_dir.resolve()) + "/model_definitions/"
    assert (
        tmo_cli.fe_tasks_catalog
        == str(test_dir.resolve()) + "/feature_engineering_tasks/"
    )


def test_list_connections_with_data(tmp_path, capsys):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)
    connections = {
        "connections": [
            {
                "id": "c1",
                "name": "conn1",
                "username": "user1",
                "host": "host1",
                "database": "db1",
            },
            {
                "id": "c2",
                "name": "conn2",
                "username": "user2",
                "host": "host2",
            },
        ]
    }
    yaml.safe_dump(
        connections, open(Path(tmo_cli.config_dir) / "connections.yaml", "w+")
    )
    args = SimpleNamespace(cwd=None)
    tmo_cli.list_connections(args)
    out, _ = capsys.readouterr()
    assert "conn1" in out
    assert "conn2" in out


def test_add_connections_without_args_prompts_user(monkeypatch, tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)

    inputs = iter(["testconn", "testuser", "testhost", "BYOM", "VAL", "testdb", "TD2"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr("getpass.getpass", lambda prompt="": "testpass")
    monkeypatch.setattr(
        tmo_cli.crypto, "td_encrypt_password", lambda **kwargs: "ENCRYPTED"
    )

    args = SimpleNamespace(
        cwd=None,
        name=None,
        username=None,
        password=None,
        host=None,
        database=None,
        val_db=None,
        byom_db=None,
        logmech=None,
        parent_parser=None,
    )

    tmo_cli.add_connections(args)

    f = Path(tmo_cli.config_dir) / "connections.yaml"
    assert f.exists()
    data = yaml.safe_load(open(f))
    assert len(data["connections"]) == 1
    assert data["connections"][0]["name"] == "testconn"


def test_add_connections_partial_args_exits(tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)

    args = SimpleNamespace(
        cwd=None,
        name="test",
        username=None,
        password=None,
        host=None,
        database=None,
        val_db=None,
        byom_db=None,
        logmech=None,
        parent_parser=type("P", (), {"print_help": lambda self: None})(),
    )

    with pytest.raises(SystemExit):
        tmo_cli.add_connections(args)


def test_add_connections_existing_file_appends(monkeypatch, tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)

    existing = {"connections": [{"id": "old", "name": "old_conn"}]}
    yaml.safe_dump(existing, open(Path(tmo_cli.config_dir) / "connections.yaml", "w+"))

    monkeypatch.setattr(tmo_cli.crypto, "td_encrypt_password", lambda **kwargs: "ENC")

    args = SimpleNamespace(
        cwd=None,
        name="new_conn",
        username="u",
        password="p",
        host="h",
        database="db",
        val_db="VAL",
        byom_db="BYOM",
        logmech="TD2",
        parent_parser=None,
    )

    tmo_cli.add_connections(args)

    data = yaml.safe_load(open(Path(tmo_cli.config_dir) / "connections.yaml"))
    assert len(data["connections"]) == 2


def test_remove_connections_with_args(tmp_path, monkeypatch):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)

    conn_id = "c1"
    connections = {
        "connections": [{
            "id": conn_id,
            "name": "conn1",
            "username": "u",
            "password": "p",
            "host": "h",
            "logmech": "TD2",
        }]
    }
    yaml.safe_dump(
        connections, open(Path(tmo_cli.config_dir) / "connections.yaml", "w+")
    )

    args = SimpleNamespace(cwd=None, connection=conn_id)
    tmo_cli.remove_connections(args)

    data = yaml.safe_load(open(Path(tmo_cli.config_dir) / "connections.yaml"))
    assert len(data.get("connections", [])) == 0


def test_remove_connections_with_select(tmp_path, monkeypatch):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)

    conn_id = "c1"
    connections = {
        "connections": [{
            "id": conn_id,
            "name": "conn1",
            "username": "u",
            "password": "p",
            "host": "h",
            "logmech": "TD2",
        }]
    }
    yaml.safe_dump(
        connections, open(Path(tmo_cli.config_dir) / "connections.yaml", "w+")
    )

    args = SimpleNamespace(cwd=None, connection=None)
    monkeypatch.setattr(tmo_cli, "input_select", lambda *a, **k: "conn1")

    tmo_cli.remove_connections(args)

    data = yaml.safe_load(open(Path(tmo_cli.config_dir) / "connections.yaml"))
    assert len(data.get("connections", [])) == 0


def test_remove_connections_empty_list(tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)

    connections = {"connections": []}
    yaml.safe_dump(
        connections, open(Path(tmo_cli.config_dir) / "connections.yaml", "w+")
    )

    args = SimpleNamespace(cwd=None, connection=None)
    tmo_cli.remove_connections(args)


def test_export_connection_no_file(tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)

    args = SimpleNamespace(cwd=None, connection=None)
    with pytest.raises(SystemExit):
        tmo_cli.export_connection(args)


def test_export_connection_not_found(tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)

    connections = {"connections": [{"id": "c1", "name": "conn1"}]}
    yaml.safe_dump(
        connections, open(Path(tmo_cli.config_dir) / "connections.yaml", "w+")
    )

    args = SimpleNamespace(cwd=None, connection="notfound")
    with pytest.raises(SystemExit):
        tmo_cli.export_connection(args)


def test_export_connection_with_select(tmp_path, monkeypatch, capsys):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)

    connection = {
        "id": "c1",
        "name": "conn1",
        "username": "u",
        "password": "p",
        "host": "h",
        "logmech": "TD2",
        "database": "db",
        "val_db": "VAL",
        "byom_db": "BYOM",
    }
    yaml.safe_dump(
        {"connections": [connection]},
        open(Path(tmo_cli.config_dir) / "connections.yaml", "w+"),
    )

    monkeypatch.setattr(tmo_cli, "input_select", lambda *a, **k: "conn1")
    args = SimpleNamespace(cwd=None, connection=None)
    tmo_cli.export_connection(args)
    out, _ = capsys.readouterr()
    assert "export VMO_CONN_USERNAME" in out
    assert "u" in out


def test_export_connection_with_args(tmp_path, monkeypatch, capsys):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)

    connection = {
        "id": "c1",
        "name": "conn1",
        "username": "u",
        "password": "p",
        "host": "h",
        "logmech": "TD2",
        "database": "db",
        "val_db": "VAL",
        "byom_db": "BYOM",
    }
    yaml.safe_dump(
        {"connections": [connection]},
        open(Path(tmo_cli.config_dir) / "connections.yaml", "w+"),
    )

    args = SimpleNamespace(cwd=None, connection="c1")
    tmo_cli.export_connection(args)
    out, _ = capsys.readouterr()
    assert "export VMO_CONN_USERNAME" in out
    assert "u" in out


def test_activate_connection_not_found(tmp_path, monkeypatch):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)

    connections = {
        "connections": [
            {
                "id": "c1",
                "name": "conn1",
                "username": "u",
                "password": "p",
                "host": "h",
                "logmech": "TD2",
                "database": "db",
            },
            {
                "id": "c2",
                "name": "conn2",
                "username": "u2",
                "password": "p2",
                "host": "h2",
                "logmech": "TD2",
                "database": "db2",
            },
        ]
    }
    yaml.safe_dump(
        connections, open(Path(tmo_cli.config_dir) / "connections.yaml", "w+")
    )

    monkeypatch.setattr(tmo_cli, "input_select", lambda *a, **k: "notfound")

    args = SimpleNamespace(cwd=None, connection=None)
    with pytest.raises(SystemExit):
        tmo_cli.activate_connection(args)


def test_activate_connection_no_file(tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)

    args = SimpleNamespace(cwd=None, connection=None)
    with pytest.raises(SystemExit):
        tmo_cli.activate_connection(args)


def test_activate_connection_with_kwargs(tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)

    connection = {
        "id": "c1",
        "name": "conn1",
        "username": "u",
        "password": "p",
        "host": "h",
        "logmech": "TD2",
        "database": "db",
    }
    yaml.safe_dump(
        {"connections": [connection]},
        open(Path(tmo_cli.config_dir) / "connections.yaml", "w+"),
    )

    args = SimpleNamespace(cwd=None, connection=None)
    ret = tmo_cli.activate_connection(args, connection="c1")
    assert ret == "c1"


def test_activate_connection_multiple_selection(monkeypatch, tmp_path):
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)

    connections = {
        "connections": [
            {
                "id": "c1",
                "name": "conn1",
                "username": "u1",
                "password": "p1",
                "host": "h1",
                "logmech": "TD2",
                "database": "db1",
            },
            {
                "id": "c2",
                "name": "conn2",
                "username": "u2",
                "password": "p2",
                "host": "h2",
                "logmech": "TD2",
                "database": "db2",
            },
        ]
    }
    yaml.safe_dump(
        connections, open(Path(tmo_cli.config_dir) / "connections.yaml", "w+")
    )

    monkeypatch.setattr(tmo_cli, "input_select", lambda *a, **k: "conn2")
    args = SimpleNamespace(cwd=None, connection=None)
    ret = tmo_cli.activate_connection(args)
    assert ret == "c2"
    assert os.environ.get("VMO_CONN_USERNAME") == "u2"


def test_create_byom_table_execute_success(monkeypatch, capsys):
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)
    monkeypatch.setattr(tmo, "execute_sql", lambda q: None)

    args = SimpleNamespace(cwd=None, name="test_table", execute_ddl=True)
    tmo_cli.create_byom_table(args)
    out, _ = capsys.readouterr()
    assert "created successfully" in out


def test_compute_stats_categorical(monkeypatch, tmp_path):
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo
    from tmo.stats import stats, store

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)

    class MockDF:
        pass

    monkeypatch.setattr("teradataml.DataFrame.from_query", lambda q: MockDF())

    monkeypatch.setattr(
        stats,
        "compute_categorical_stats",
        lambda df, cols, temp_db=None: {"col1": {"categories": ["a", "b"]}},
    )

    monkeypatch.setattr(store, "save_feature_stats", lambda **kwargs: None)

    args = SimpleNamespace(
        cwd=None,
        source_table="test.table",
        metadata_table="test.metadata",
        feature_type="categorical",
        columns="col1, col2",
        temp_view_database=None,
    )

    tmo_cli.compute_stats(args)


def test_compute_stats_continuous(monkeypatch, tmp_path):
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo
    from tmo.stats import stats, store

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)

    class MockDF:
        pass

    monkeypatch.setattr("teradataml.DataFrame.from_query", lambda q: MockDF())

    monkeypatch.setattr(
        stats,
        "compute_continuous_stats",
        lambda df, cols, temp_db=None: {"col1": {"edges": [1, 2, 3]}},
    )

    monkeypatch.setattr(store, "save_feature_stats", lambda **kwargs: None)

    args = SimpleNamespace(
        cwd=None,
        source_table="test.table",
        metadata_table="test.metadata",
        feature_type="continuous",
        columns="col1, col2",
        temp_view_database=None,
    )

    tmo_cli.compute_stats(args)


def test_compute_stats_error(monkeypatch):
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)
    monkeypatch.setattr(
        "teradataml.DataFrame.from_query",
        lambda q: (_ for _ in ()).throw(Exception("error")),
    )

    args = SimpleNamespace(
        cwd=None,
        source_table="test.table",
        metadata_table="test.metadata",
        feature_type="continuous",
        columns="col1",
        temp_view_database=None,
    )

    with pytest.raises(RuntimeError):
        tmo_cli.compute_stats(args)


def test_compute_stats_with_temp_view_database(monkeypatch, tmp_path):
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo
    from tmo.stats import stats, store

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)

    class MockDF:
        pass

    monkeypatch.setattr("teradataml.DataFrame.from_query", lambda q: MockDF())

    categorical_calls = []
    continuous_calls = []

    def mock_categorical_stats(df, cols, temp_db=None):
        categorical_calls.append({"df": df, "cols": cols, "temp_db": temp_db})
        return {"col1": {"categories": ["a", "b"]}}

    def mock_continuous_stats(df, cols, temp_db=None):
        continuous_calls.append({"df": df, "cols": cols, "temp_db": temp_db})
        return {"col1": {"edges": [1, 2, 3]}}

    monkeypatch.setattr(stats, "compute_categorical_stats", mock_categorical_stats)
    monkeypatch.setattr(stats, "compute_continuous_stats", mock_continuous_stats)
    monkeypatch.setattr(store, "save_feature_stats", lambda **kwargs: None)

    args = SimpleNamespace(
        cwd=None,
        source_table="test.table",
        metadata_table="test.metadata",
        feature_type="categorical",
        columns="col1, col2",
        temp_view_database="temp_view",
    )

    tmo_cli.compute_stats(args)

    assert len(categorical_calls) == 1
    assert categorical_calls[0]["cols"] == ["col1", "col2"]

    categorical_calls.clear()
    args.feature_type = "continuous"

    tmo_cli.compute_stats(args)

    assert len(continuous_calls) == 1
    assert continuous_calls[0]["cols"] == ["col1", "col2"]


def test_list_stats_success(monkeypatch, capsys):
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo
    from tmo.stats import store

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)
    monkeypatch.setattr(
        store,
        "get_feature_stats_summary",
        lambda table: {"col1": "continuous", "col2": "categorical"},
    )

    args = SimpleNamespace(cwd=None, metadata_table="test.metadata")
    tmo_cli.list_stats(args)
    out, _ = capsys.readouterr()
    assert "col1" in out
    assert "col2" in out


def test_list_stats_empty(monkeypatch):
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo
    from tmo.stats import store

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)
    monkeypatch.setattr(store, "get_feature_stats_summary", lambda table: {})

    args = SimpleNamespace(cwd=None, metadata_table="test.metadata")
    with pytest.raises(RuntimeError):
        tmo_cli.list_stats(args)


def test_list_stats_error(monkeypatch):
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo
    from tmo.stats import store

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)
    monkeypatch.setattr(
        store,
        "get_feature_stats_summary",
        lambda table: (_ for _ in ()).throw(Exception("error")),
    )

    args = SimpleNamespace(cwd=None, metadata_table="test.metadata")
    with pytest.raises(RuntimeError):
        tmo_cli.list_stats(args)


def test_create_stats_table_no_execute(capsys):
    args = SimpleNamespace(cwd=None, metadata_table="test.metadata", execute_ddl=False)
    tmo_cli.create_stats_table(args)
    out, _ = capsys.readouterr()
    assert "Execution not requested" in out


def test_create_stats_table_execute_success(monkeypatch, capsys):
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)
    monkeypatch.setattr(tmo, "execute_sql", lambda q: None)

    args = SimpleNamespace(cwd=None, metadata_table="test.metadata", execute_ddl=True)
    tmo_cli.create_stats_table(args)
    out, _ = capsys.readouterr()
    assert "created successfully" in out


def test_create_stats_table_error(monkeypatch):
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)
    monkeypatch.setattr(
        tmo, "execute_sql", lambda q: (_ for _ in ()).throw(Exception("error"))
    )

    args = SimpleNamespace(cwd=None, metadata_table="test.metadata", execute_ddl=True)
    with pytest.raises(RuntimeError):
        tmo_cli.create_stats_table(args)


def test_import_stats_show_example(capsys):
    args = SimpleNamespace(
        cwd=None, show_example=True, statistics_file=None, metadata_table=None
    )
    with pytest.raises(SystemExit):
        tmo_cli.import_stats(args)
    out, _ = capsys.readouterr()
    assert "age" in out
    assert "continuous" in out


def test_import_stats_success(monkeypatch, tmp_path):
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo
    from tmo.stats import store

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)
    monkeypatch.setattr(store, "save_feature_stats", lambda *args, **kwargs: None)

    stats_file = tmp_path / "stats.json"
    stats_data = {
        "features": {
            "age": {"type": "continuous", "edges": [1, 2, 3]},
            "gender": {"type": "categorical", "categories": ["M", "F"]},
        }
    }
    stats_file.write_text(json.dumps(stats_data))

    args = SimpleNamespace(
        cwd=None,
        show_example=False,
        statistics_file=str(stats_file),
        metadata_table="test.metadata",
    )

    tmo_cli.import_stats(args)


def test_import_stats_error(monkeypatch, tmp_path):
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    import tmo

    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)

    stats_file = tmp_path / "stats.json"
    stats_file.write_text("invalid json")

    args = SimpleNamespace(
        cwd=None,
        show_example=False,
        statistics_file=str(stats_file),
        metadata_table="test.metadata",
    )

    with pytest.raises(RuntimeError):
        tmo_cli.import_stats(args)


def test_doctor_success(monkeypatch):
    monkeypatch.setattr(tmo_cli, "test_connection", lambda args: None)
    import tmo

    class PApi:
        def __init__(self, tmo_client, show_archived=False):
            pass

        def __iter__(self):
            return iter([{"id": "p1", "name": "proj1"}])

    monkeypatch.setattr("tmo.ProjectApi", PApi)

    args = SimpleNamespace(cwd=None, connection=None)
    tmo_cli.doctor(args, None, None)


def test_doctor_no_projects(monkeypatch):
    import tmo
    from tmo.types.exceptions import EntityNotFoundError

    class PApi:
        def __init__(self, tmo_client, show_archived=False):
            pass

        def __iter__(self):
            return iter([])

    monkeypatch.setattr("tmo.ProjectApi", PApi)

    args = SimpleNamespace(cwd=None, connection=None)
    with pytest.raises(EntityNotFoundError):
        tmo_cli.doctor(args, None, None)


def test_doctor_connection_error(monkeypatch):
    from tmo.types.exceptions import ConfigurationError

    class PApi:
        def __init__(self, tmo_client, show_archived=False):
            raise ConfigurationError("config error")

    monkeypatch.setattr("tmo.ProjectApi", PApi)
    monkeypatch.setattr(tmo_cli, "test_connection", lambda args: None)

    args = SimpleNamespace(cwd=None, connection=None)
    tmo_cli.doctor(args, None, None)


def test_print_help_no_version(capsys):
    parser = type("P", (), {"print_help": lambda self: print("help")})()
    args = SimpleNamespace(version=False)
    tmo_cli.print_help(args, parent_parser=parser)
    out, _ = capsys.readouterr()
    assert "help" in out


def test_list_and_select_projects_current_project(monkeypatch):
    class RM:
        def read_repo_config(self):
            return {"project_id": "p1"}

    class PApi:
        def __init__(self, tmo_client, show_archived=False):
            pass

        def __iter__(self):
            return iter([{"id": "p1", "name": "proj1"}, {"id": "p2", "name": "proj2"}])

        def find_by_id(self, pid):
            if pid == "p1":
                return {"id": "p1", "name": "proj1"}
            return None

    monkeypatch.setattr("tmo.ProjectApi", PApi)
    monkeypatch.setattr(tmo_cli, "validate_model_catalog_cwd_valid", lambda: True)
    monkeypatch.setattr("builtins.input", lambda prompt="": "")

    result = tmo_cli.list_and_select_projects(
        RM(), None, as_list=False, check_config=True
    )
    assert result["id"] == "p1"


def test_list_and_select_projects_invalid_then_valid(monkeypatch):
    class PApi:
        def __init__(self, tmo_client, show_archived=False):
            pass

        def __iter__(self):
            return iter([{"id": "p1", "name": "proj1"}])

    monkeypatch.setattr("tmo.ProjectApi", PApi)
    monkeypatch.setattr(tmo_cli, "validate_model_catalog_cwd_valid", lambda: False)

    inputs = iter(["abc", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    result = tmo_cli.list_and_select_projects(
        None, None, as_list=False, check_config=False
    )
    assert result["id"] == "p1"


def test_get_current_project_not_found(monkeypatch):
    class RM:
        def read_repo_config(self):
            return {"project_id": "p1"}

    class PApi:
        def __init__(self, tmo_client, show_archived=False):
            pass

        def find_by_id(self, pid):
            return None

    monkeypatch.setattr("tmo.ProjectApi", PApi)
    monkeypatch.setattr(tmo_cli, "validate_model_catalog_cwd_valid", lambda: True)

    result = tmo_cli.get_current_project(RM(), None, check_repo_conf=False)
    assert result is None


def test_get_current_project_no_repo_config(monkeypatch):
    class RM:
        def read_repo_config(self):
            return None

    class PApi:
        def __init__(self, tmo_client, show_archived=False):
            pass

        def find_by_id(self, pid):
            return None

    monkeypatch.setattr("tmo.ProjectApi", PApi)
    monkeypatch.setattr(tmo_cli, "validate_model_catalog_cwd_valid", lambda: True)

    result = tmo_cli.get_current_project(RM(), None, check_repo_conf=False)
    assert result is None


def test_get_current_project_invalid_catalog():
    result = tmo_cli.get_current_project(None, None, check_repo_conf=False)
    assert result is None


def test_clone_with_project_id(monkeypatch):
    class PApi:
        def __init__(self, tmo_client, show_archived=False):
            pass

        def find_by_id(self, pid):
            return {
                "id": "p1",
                "name": "proj1",
                "gitRepositoryUrl": "http://git.example.com/repo",
            }

    class RM:
        def clone_repository(self, url, path, branch):
            pass

        def write_repo_config(self, config, path):
            pass

    monkeypatch.setattr("tmo.ProjectApi", PApi)

    args = SimpleNamespace(cwd=None, project_id="p1", path="/tmp/test")
    tmo_cli.clone(args, RM(), None)


def test_clone_project_not_found(monkeypatch):
    class PApi:
        def __init__(self, tmo_client, show_archived=False):
            pass

        def find_by_id(self, pid):
            return None

    monkeypatch.setattr("tmo.ProjectApi", PApi)
    monkeypatch.setattr(
        tmo_cli,
        "list_and_select_projects",
        lambda rm, tmo, a, b: {
            "id": "p2",
            "name": "proj2",
            "gitRepositoryUrl": "http://git.example.com/repo",
        },
    )

    class RM:
        def clone_repository(self, url, path, branch):
            pass

        def write_repo_config(self, config, path):
            pass

    args = SimpleNamespace(cwd=None, project_id="notfound", path=None)
    tmo_cli.clone(args, RM(), None)


def test_clone_no_args(monkeypatch, tmp_path):
    monkeypatch.setattr(
        tmo_cli,
        "list_and_select_projects",
        lambda rm, tmo, a, b: {
            "id": "p1",
            "name": "testproject",
            "gitRepositoryUrl": "http://git.example.com/repo",
            "branch": "main",
        },
    )

    class RM:
        def clone_repository(self, url, path, branch):
            pass

        def write_repo_config(self, config, path):
            pass

    tmo_cli.base_path = str(tmp_path)
    args = SimpleNamespace(cwd=None, project_id=None, path=None)
    tmo_cli.clone(args, RM(), None)


def test_add_task_invalid_cwd(monkeypatch):
    monkeypatch.setattr(tmo_cli, "validate_fe_tasks_cwd_valid", lambda: False)

    args = SimpleNamespace(cwd=None, template_url=None, branch=None, name=None)
    with pytest.raises(SystemExit):
        tmo_cli.add_task(args, None)


def test_add_task_no_templates(monkeypatch, tmp_path):
    monkeypatch.setattr(tmo_cli, "validate_fe_tasks_cwd_valid", lambda: True)

    class RM:
        def clone_repository(self, url, path, branch):
            pass

        def get_templates(self, entity_type=None, source_path=None):
            return {}

    args = SimpleNamespace(
        cwd=None, template_url="http://example.com", branch="main", name=None
    )
    with pytest.raises(SystemExit):
        tmo_cli.add_task(args, RM())


def test_add_task_success(monkeypatch, tmp_path):
    monkeypatch.setattr(tmo_cli, "validate_fe_tasks_cwd_valid", lambda: True)
    monkeypatch.setattr(tmo_cli, "input_select", lambda *a, **k: "task1")

    class RM:
        def clone_repository(self, url, path, branch):
            pass

        def get_templates(self, entity_type=None, source_path=None):
            return {"task1": "/path/to/template"}

        def add_task(self, template, task_name, base_path):
            pass

    tmo_cli.base_path = str(tmp_path)
    args = SimpleNamespace(
        cwd=None, template_url="http://example.com", branch="main", name="mytask"
    )
    tmo_cli.add_task(args, RM())


def test_run_task_invalid_project(monkeypatch):
    monkeypatch.setattr(tmo_cli, "get_current_project", lambda rm, tmo, check: None)

    args = SimpleNamespace(cwd=None, connection=None, name=None, function_name=None)
    with pytest.raises(SystemExit):
        tmo_cli.run_task(args, None, None)


def test_run_task_success(monkeypatch, tmp_path):
    monkeypatch.setattr(
        tmo_cli,
        "get_current_project",
        lambda rm, tmo, check: {"id": "p1", "name": "proj1"},
    )
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda args: "c1")

    class Client:
        def set_project_id(self, pid):
            pass

    class Runner:
        def __init__(self, rm):
            pass

        def run_task_local(self, base_path, task_name, func):
            return ("task1", "func1")

    import tmo

    monkeypatch.setattr(tmo, "RunTask", Runner)

    tmo_cli.base_path = str(tmp_path)
    args = SimpleNamespace(
        cwd=None, connection=None, name="task1", function_name="func1"
    )
    tmo_cli.run_task(args, None, Client())


def test_list_resources_projects(monkeypatch, capsys):
    monkeypatch.setattr(tmo_cli, "list_and_select_projects", lambda *a, **k: None)

    args = SimpleNamespace(
        cwd=None,
        projects=True,
        models=False,
        local_models=False,
        templates=False,
        datasets=False,
        connections=False,
    )

    with pytest.raises(SystemExit):
        tmo_cli.list_resources(args, None, None)


def test_list_resources_models(monkeypatch):
    monkeypatch.setattr(
        tmo_cli,
        "get_current_project",
        lambda rm, tmo: {"id": "p1", "name": "proj1"},
    )

    class Client:
        def set_project_id(self, pid):
            pass

    class MApi:
        def __init__(self, tmo_client, show_archived=False):
            pass

        def __len__(self):
            return 1

        def __iter__(self):
            return iter([{"id": "m1", "name": "model1", "source": "git"}])

    import tmo

    monkeypatch.setattr(tmo, "ModelApi", MApi)

    args = SimpleNamespace(
        cwd=None,
        projects=False,
        models=True,
        local_models=False,
        templates=False,
        datasets=False,
        connections=False,
    )

    tmo_cli.list_resources(args, None, Client())


def test_list_resources_local_models(monkeypatch, capsys):
    import tmo

    monkeypatch.setattr(
        tmo.TrainModel,
        "get_model_folders",
        lambda catalog, arg: {
            "folder1": {"name": "model1", "id": "m1"},
        },
    )

    args = SimpleNamespace(
        cwd=None,
        projects=False,
        models=False,
        local_models=True,
        templates=False,
        datasets=False,
        connections=False,
    )

    tmo_cli.list_resources(args, None, None)
    out, _ = capsys.readouterr()
    assert "model1" in out


def test_list_resources_templates(monkeypatch):
    monkeypatch.setattr(
        tmo_cli,
        "get_current_project",
        lambda rm, tmo: {"id": "p1", "name": "proj1"},
    )

    class Client:
        def set_project_id(self, pid):
            pass

    class Template:
        def __init__(self):
            self.id = "t1"
            self.name = "template1"

    class TApi:
        def __init__(self, tmo_client, show_archived=False):
            pass

        def find_all(self):
            return [Template()]

    import tmo

    monkeypatch.setattr(tmo, "DatasetTemplateApi", TApi)

    args = SimpleNamespace(
        cwd=None,
        projects=False,
        models=False,
        local_models=False,
        templates=True,
        datasets=False,
        connections=False,
    )

    tmo_cli.list_resources(args, None, Client())


def test_list_resources_datasets(monkeypatch):
    monkeypatch.setattr(
        tmo_cli,
        "get_current_project",
        lambda rm, tmo: {"id": "p1", "name": "proj1"},
    )

    class Client:
        def set_project_id(self, pid):
            pass

    class Dataset:
        def __init__(self):
            self.id = "d1"
            self.name = "dataset1"

    class DApi:
        def __init__(self, tmo_client, show_archived=False):
            pass

        def find_all(self):
            return [Dataset()]

    import tmo

    monkeypatch.setattr(tmo, "DatasetApi", DApi)

    args = SimpleNamespace(
        cwd=None,
        projects=False,
        models=False,
        local_models=False,
        templates=False,
        datasets=True,
        connections=False,
    )

    tmo_cli.list_resources(args, None, Client())


def test_list_resources_connections(monkeypatch):
    monkeypatch.setattr(tmo_cli, "list_connections", lambda args: None)

    args = SimpleNamespace(
        cwd=None,
        projects=False,
        models=False,
        local_models=False,
        templates=False,
        datasets=False,
        connections=True,
    )

    tmo_cli.list_resources(args, None, None)


def test_init_model_directory_with_existing_config(monkeypatch):
    class RM:
        def __init__(self):
            self.inited = False

        def init_model_directory(self):
            self.inited = True

        def repo_config_exists(self):
            return True

    args = SimpleNamespace(cwd=None)
    repo_manager = RM()
    tmo_cli.init_model_directory(args, repo_manager, None)
    assert repo_manager.inited is True


def test_add_model_with_prompts(monkeypatch, tmp_path):
    monkeypatch.setattr(tmo_cli, "validate_model_catalog_cwd_valid", lambda: True)

    inputs = iter(["http://example.com", "main", "model1", "desc"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr(
        tmo_cli,
        "input_select",
        lambda *a, **k: "python" if "language" in str(a) else "Template 1 (t1)",
    )

    class RM:
        def clone_repository(self, url, path, branch):
            pass

        def get_templates(self, entity_type=None, source_path=None):
            return {
                "python": {
                    "t1": ["Template 1", "/path/to/template"],
                }
            }

        def add_model(self, model_id, model_name, model_desc, template, base_path):
            pass

    tmo_cli.base_path = str(tmp_path)
    args = SimpleNamespace(cwd=None, template_url=None, branch=None)
    tmo_cli.add_model(args, RM())


def test_input_string_password_with_is_called_from_test_true(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "secret")
    result = tmo_cli.input_string("test", password=True, is_called_from_test=True)
    assert result == "secret"


def test_input_select_with_label(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "0")
    result = tmo_cli.input_select("item", ["a", "b"], label="Choose one:")
    assert result == "a"
    out, _ = capsys.readouterr()
    assert "Choose one:" in out


def test_yes_or_no_case_insensitive(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "Y")
    assert tmo_cli.yes_or_no("question") is True

    monkeypatch.setattr("builtins.input", lambda prompt="": "N")
    assert tmo_cli.yes_or_no("question") is False


def test_clone_with_project_found(monkeypatch, tmp_path):
    args = type("A", (), {"cwd": None, "project_id": "p1", "path": None})()

    class RM:
        def __init__(self):
            self.cloned = False
            self.config = None

        def clone_repository(self, git, path, branch):
            self.cloned = True

        def write_repo_config(self, config, path=None):
            self.config = (config, path)

    class PApi:
        def __init__(self, tmo_client=None, show_archived=False):
            pass

        def find_by_id(self, pid):
            return {
                "id": pid,
                "name": "proj",
                "gitRepositoryUrl": "git@x",
                "branch": "main",
            }

    monkeypatch.setattr("tmo.ProjectApi", PApi)
    rm = RM()
    tmo_cli.clone(args, rm, None)
    assert rm.cloned is True
    assert rm.config[0]["project_id"] == "p1"


def test_list_connections_prints_when_connections_present(tmp_path, capsys):
    cfg = tmp_path / "cfg"
    tmo_cli.config_dir = str(cfg)
    cfg.mkdir(parents=True)
    con = {
        "connections": [{
            "id": "c1",
            "name": "n",
            "username": "u",
            "password": "p",
            "host": "h",
            "logmech": "TDNEGO",
            "database": "db",
        }]
    }
    yaml.safe_dump(con, open(cfg / "connections.yaml", "w+"))
    args = type("A", (), {"cwd": None})()
    tmo_cli.list_connections(args)
    out, _ = capsys.readouterr()
    assert "List of local connections" in out or "Name: n" in out


def test_add_connections_invalid_args_calls_help_and_exits(monkeypatch):
    args = type(
        "A",
        (),
        {
            "cwd": None,
            "name": None,
            "username": "u",
            "password": None,
            "host": None,
            "database": None,
            "val_db": None,
            "byom_db": None,
            "logmech": None,
            "parent_parser": type("P", (), {"print_help": lambda self: None})(),
        },
    )()
    with pytest.raises(SystemExit):
        tmo_cli.add_connections(args)


def _write_tmp_json(tmp_path, content):
    p = tmp_path / "tmp.json"
    p.write_text(content)
    return str(p)


def test_run_model_calls_train_evaluate_score(tmp_path, monkeypatch):
    import tmo

    model_id = "m1"
    available = {0: {"id": model_id, "name": "M"}}
    monkeypatch.setattr(tmo.TrainModel, "get_model_ids", lambda catalog, arg: available)
    monkeypatch.setattr(
        tmo_cli, "get_current_project", lambda rm, tc, check: {"id": "p1"}
    )

    class RepoManager:
        pass

    class Client:
        def set_project_id(self, pid):
            pass

    # prepare a local dataset file to bypass selection
    dataset_path = _write_tmp_json(tmp_path, '{"data": []}')

    # Train mode
    args = type(
        "A",
        (),
        {
            "cwd": None,
            "model_id": model_id,
            "mode": "train",
            "local_dataset": dataset_path,
            "local_dataset_template": None,
            "dataset_id": None,
            "dataset_template_id": None,
            "connection": None,
        },
    )()
    called = {}

    class FakeTrainer:
        @staticmethod
        def get_model_ids(catalog, arg):
            return available

        def __init__(self, repo_manager):
            pass

        def train_model_local(self, mid, rendered_dataset=None, base_path=None):
            called["train"] = (mid, rendered_dataset is not None)

    monkeypatch.setattr(tmo, "TrainModel", FakeTrainer)
    tmo_cli.run_model(args, RepoManager(), Client())
    assert called.get("train")[0] == model_id

    # Evaluate mode
    called.clear()
    args.mode = "evaluate"

    class FakeEvaluator:
        def __init__(self, repo_manager):
            pass

        def evaluate_model_local(self, mid, rendered_dataset=None, base_path=None):
            called["evaluate"] = (mid, rendered_dataset is not None)

    monkeypatch.setattr(tmo, "EvaluateModel", FakeEvaluator)
    tmo_cli.run_model(args, RepoManager(), Client())
    assert called.get("evaluate")[0] == model_id

    # Score mode uses local dataset template bypass
    called.clear()
    args.mode = "score"
    args.local_dataset = None
    tmp_template = _write_tmp_json(tmp_path, '{"template": true}')
    args.local_dataset_template = tmp_template

    class FakeScorer:
        def __init__(self, repo_manager):
            pass

        def batch_score_model_local(self, mid, rendered_dataset=None, base_path=None):
            called["score"] = (mid, rendered_dataset is not None)

    monkeypatch.setattr(tmo, "ScoreModel", FakeScorer)
    tmo_cli.run_model(args, RepoManager(), Client())
    assert called.get("score")[0] == model_id


def test_import_stats_saves_feature_stats(tmp_path, monkeypatch):
    import tmo

    stats_json = {
        "features": {
            "age": {"type": "continuous", "edges": [1, 2]},
            "flag": {"type": "categorical", "frequencies": ["0", "1"]},
        }
    }
    p = tmp_path / "stats.json"
    p.write_text(json.dumps(stats_json))

    calls = []
    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)
    monkeypatch.setattr(
        "tmo.stats.store.save_feature_stats", lambda *a, **k: calls.append((a, k))
    )

    args = type(
        "A",
        (),
        {
            "cwd": None,
            "show_example": False,
            "statistics_file": str(p),
            "metadata_table": "mt",
        },
    )()
    tmo_cli.import_stats(args)
    # should have saved categorical and continuous
    assert any(call[0][1] == "categorical" for call in calls)
    assert any(call[0][1] == "continuous" for call in calls)


def test_compute_stats_calls_store(tmp_path, monkeypatch):
    import tmo

    monkeypatch.setattr(tmo_cli, "activate_connection", lambda ns: None)
    monkeypatch.setattr(tmo, "tmo_create_context", lambda: None)

    class FakeDF:
        pass

    # mock teradataml.DataFrame.from_query
    import teradataml

    monkeypatch.setattr(
        teradataml.DataFrame, "from_query", classmethod(lambda cls, q: FakeDF())
    )

    # categorical
    monkeypatch.setattr(
        "tmo.stats.stats.compute_categorical_stats",
        lambda df, cols, temp_db=None: {"a": "cat"},
    )
    saved = []
    monkeypatch.setattr(
        "tmo.stats.store.save_feature_stats", lambda *a, **k: saved.append((a, k))
    )
    args = type(
        "A",
        (),
        {
            "cwd": None,
            "source_table": "t",
            "columns": "a",
            "feature_type": "categorical",
            "metadata_table": "mt",
            "temp_view_database": None,
        },
    )()
    tmo_cli.compute_stats(args)
    assert any(call[1].get("feature_type") == "categorical" for call in saved)

    # continuous
    saved.clear()
    monkeypatch.setattr(
        "tmo.stats.stats.compute_continuous_stats",
        lambda df, cols, temp_db=None: {"a": "cont"},
    )
    args.feature_type = "continuous"
    tmo_cli.compute_stats(args)
    assert any(call[1].get("feature_type") == "continuous" for call in saved)


def test_check_connection_exists_found():
    """Test _check_connection_exists when connection is found."""
    connections = [
        {"id": "c1", "name": "conn1"},
        {"id": "c2", "name": "conn2"},
    ]
    assert tmo_cli._check_connection_exists("c1", connections) is True
    assert tmo_cli._check_connection_exists("c3", connections) is False


def test_check_connection_exists_empty_list():
    """Test _check_connection_exists with empty list."""
    assert tmo_cli._check_connection_exists("c1", []) is False


def test_select_connection_from_list_single(capsys):
    """Test _select_connection_from_list with single connection."""
    connections = [{"id": "c1", "name": "conn1"}]
    result = tmo_cli._select_connection_from_list(connections)
    assert result == "c1"
    out, _ = capsys.readouterr()
    assert "Automatic connection selection" in out


def test_select_connection_from_list_multiple(monkeypatch):
    """Test _select_connection_from_list with multiple connections."""
    connections = [
        {"id": "c1", "name": "conn1"},
        {"id": "c2", "name": "conn2"},
    ]
    monkeypatch.setattr(tmo_cli, "input_select", lambda *a, **k: "conn2")
    result = tmo_cli._select_connection_from_list(connections)
    assert result == "c2"


def test_set_connection_env_vars_success():
    """Test _set_connection_env_vars sets environment variables correctly."""
    connections = [{
        "id": "c1",
        "name": "conn1",
        "username": "user1",
        "password": "pass1",
        "host": "host1",
        "logmech": "TDNEGO",
        "database": "db1",
        "val_db": "VAL",
        "ml_db": "MLDB",
    }]
    result = tmo_cli._set_connection_env_vars("c1", connections)
    assert result is True
    assert os.environ.get("VMO_CONN_USERNAME") == "user1"
    assert os.environ.get("VMO_CONN_HOST") == "host1"


def test_set_connection_env_vars_not_found():
    """Test _set_connection_env_vars when connection not found."""
    connections = [{"id": "c1", "name": "conn1"}]
    result = tmo_cli._set_connection_env_vars("c2", connections)
    assert result is False


def test_get_connections_list_with_connections():
    """Test _get_connections_list with valid connections."""
    connections_dict = {
        "connections": [
            {"id": "c1", "name": "conn1"},
            {"id": "c2", "name": "conn2"},
        ]
    }
    result = tmo_cli._get_connections_list(connections_dict)
    assert len(result) == 2
    assert result[0]["id"] == "c1"


def test_get_connections_list_empty():
    """Test _get_connections_list with empty or missing connections."""
    assert tmo_cli._get_connections_list({}) == []
    assert tmo_cli._get_connections_list({"connections": []}) == []


def test_determine_connection_id_from_args():
    """Test _determine_connection_id uses args.connection when available."""
    args = SimpleNamespace(connection="c1")
    kwargs = {}
    connections = [{"id": "c1", "name": "conn1"}]
    result = tmo_cli._determine_connection_id(args, kwargs, connections)
    assert result == "c1"


def test_determine_connection_id_from_kwargs():
    """Test _determine_connection_id uses kwargs when args doesn't have connection."""
    args = SimpleNamespace(connection=None)
    kwargs = {"connection": "c2"}
    connections = [{"id": "c2", "name": "conn2"}]
    result = tmo_cli._determine_connection_id(args, kwargs, connections)
    assert result == "c2"


def test_determine_connection_id_select_from_list(monkeypatch):
    """Test _determine_connection_id selects from list when no args/kwargs."""
    args = SimpleNamespace(connection=None)
    kwargs = {}
    connections = [{"id": "c1", "name": "conn1"}]
    result = tmo_cli._determine_connection_id(args, kwargs, connections)
    assert result == "c1"


def test_print_projects_list_with_projects(capsys):
    """Test _print_projects_list prints projects correctly."""
    projects = [
        {"id": "p1", "name": "Project 1"},
        {"id": "p2", "name": "Project 2"},
    ]
    tmo_cli._print_projects_list(projects, as_list=False)
    out, _ = capsys.readouterr()
    assert "Available projects:" in out
    assert "p1" in out
    assert "Project 1" in out


def test_print_projects_list_empty(capsys):
    """Test _print_projects_list with empty list."""
    tmo_cli._print_projects_list([], as_list=True)
    out, _ = capsys.readouterr()
    assert "List of projects:" in out
    assert "No projects were found" in out


def test_find_current_project_index_found():
    """Test _find_current_project_index when project is found."""
    projects = [
        {"id": "p1", "name": "Project 1"},
        {"id": "p2", "name": "Project 2"},
    ]
    current_project = {"id": "p2"}
    result = tmo_cli._find_current_project_index(projects, current_project)
    assert result == 1


def test_find_current_project_index_not_found():
    """Test _find_current_project_index when project is not found."""
    projects = [{"id": "p1", "name": "Project 1"}]
    current_project = {"id": "p3"}
    result = tmo_cli._find_current_project_index(projects, current_project)
    assert result == "none"


def test_find_current_project_index_none():
    """Test _find_current_project_index with None current project."""
    projects = [{"id": "p1", "name": "Project 1"}]
    result = tmo_cli._find_current_project_index(projects, None)
    assert result == "none"


def test_validate_project_selection_valid():
    """Test _validate_project_selection with valid selection."""
    projects = [{"id": "p1"}, {"id": "p2"}]
    assert tmo_cli._validate_project_selection("0", projects, "none") is True
    assert tmo_cli._validate_project_selection("1", projects, "none") is True
    assert tmo_cli._validate_project_selection("", projects, 0) is True


def test_validate_project_selection_invalid():
    """Test _validate_project_selection with invalid selection."""
    projects = [{"id": "p1"}, {"id": "p2"}]
    assert tmo_cli._validate_project_selection("2", projects, "none") is False
    assert tmo_cli._validate_project_selection("abc", projects, "none") is False
    assert tmo_cli._validate_project_selection("", projects, "none") is False


def test_check_if_any_resource_selected_true():
    """Test _check_if_any_resource_selected returns True when resource selected."""
    args = SimpleNamespace(
        projects=True,
        models=False,
        local_models=False,
        templates=False,
        datasets=False,
        connections=False,
    )
    assert tmo_cli._check_if_any_resource_selected(args) is True


def test_check_if_any_resource_selected_false():
    """Test _check_if_any_resource_selected returns False when none selected."""
    args = SimpleNamespace(
        projects=False,
        models=False,
        local_models=False,
        templates=False,
        datasets=False,
        connections=False,
    )
    assert tmo_cli._check_if_any_resource_selected(args) is False


def test_handle_invalid_grant_error_token_not_active(monkeypatch):
    """Test _handle_invalid_grant_error with 'Token is not active' error."""

    class FakeError:
        description = "Token is not active"

    args = SimpleNamespace(debug=False)
    remove_called = {"called": False}

    def fake_remove():
        remove_called["called"] = True

    with pytest.raises(SystemExit) as exc:
        tmo_cli._handle_invalid_grant_error(FakeError(), args, fake_remove)

    assert exc.value.code == 1
    assert remove_called["called"] is True


def test_handle_invalid_grant_error_session_not_active(monkeypatch):
    """Test _handle_invalid_grant_error with 'Session not active' error."""

    class FakeError:
        description = "Session not active"

    args = SimpleNamespace(debug=False)
    remove_called = {"called": False}

    def fake_remove():
        remove_called["called"] = True

    with pytest.raises(SystemExit) as exc:
        tmo_cli._handle_invalid_grant_error(FakeError(), args, fake_remove)

    assert exc.value.code == 1
    assert remove_called["called"] is True


def test_handle_invalid_grant_error_other_error(monkeypatch):
    """Test _handle_invalid_grant_error with other error types."""

    class FakeError:
        description = "Some other error"

    args = SimpleNamespace(debug=False)

    def fake_remove():
        pass

    # Should call handle_generic_error which exits with code 1
    with pytest.raises(SystemExit) as exc:
        tmo_cli._handle_invalid_grant_error(FakeError(), args, fake_remove)

    assert exc.value.code == 1


def test_load_connections_from_file_success(tmp_path):
    """Test _load_connections_from_file loads file successfully."""
    tmp = tmp_path / "cfg"
    tmo_cli.config_dir = str(tmp)
    tmp.mkdir(parents=True)
    connections_data = {"connections": [{"id": "c1", "name": "conn1"}]}
    yaml.safe_dump(
        connections_data,
        open(Path(tmo_cli.config_dir) / "connections.yaml", "w+"),
    )
    result = tmo_cli._load_connections_from_file()
    assert "connections" in result
    assert len(result["connections"]) == 1


def test_load_connections_from_file_not_found(tmp_path):
    """Test _load_connections_from_file when file doesn't exist."""
    tmp = tmp_path / "cfg_nonexistent"
    tmo_cli.config_dir = str(tmp)
    with pytest.raises(SystemExit) as exc:
        tmo_cli._load_connections_from_file()
    assert exc.value.code == 1
