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

    def fake_input(prompt=""):  # noqa
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
        def fetchall(self):  # noqa
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
        def read_repo_config(self):  # noqa
            return {"project_id": "p1"}

    class PApi:
        def __init__(self, tmo_client, show_archived=False):  # noqa # noqa
            pass

        def find_by_id(self, pid):  # noqa
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

        def repo_config_exists(self):  # noqa
            return False

    repo_manager = RM()
    called = {"link": False}
    monkeypatch.setattr(
        tmo_cli,
        "link_repo",
        lambda repo_manager, tmo_client: called.update({"link": True}),  # noqa
    )
    args = type("A", (), {"cwd": None})()
    tmo_cli.init_model_directory(args, repo_manager, None)
    assert repo_manager.inited is True
    assert called["link"] is True


def test_add_model_templates_empty_exits(monkeypatch, tmp_path):
    args = type("A", (), {"cwd": None, "template_url": "u", "branch": "b"})()

    class RM:
        def clone_repository(self, url, path, branch):  # noqa
            return None

        def get_templates(self, entity_type=None, source_path=None):  # noqa
            return {}

        def repo_config_exists(self):  # noqa
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
    import tmo.tmo_cli  # noqa

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
    monkeypatch.setattr(
        store, "save_feature_stats", lambda *args, **kwargs: None  # noqa
    )

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
    monkeypatch.setattr(tmo_cli, "test_connection", lambda args: None)  # noqa
    import tmo  # noqa

    class PApi:
        def __init__(self, tmo_client, show_archived=False):  # noqa
            pass

        def __iter__(self):
            return iter([{"id": "p1", "name": "proj1"}])

    monkeypatch.setattr("tmo.ProjectApi", PApi)

    args = SimpleNamespace(cwd=None, connection=None)
    tmo_cli.doctor(args, None, None)


def test_doctor_no_projects(monkeypatch):
    import tmo  # noqa
    from tmo.types.exceptions import EntityNotFoundError

    class PApi:
        def __init__(self, tmo_client, show_archived=False):  # noqa
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
        def __init__(self, tmo_client, show_archived=False):  # noqa
            raise ConfigurationError("config error")

    monkeypatch.setattr("tmo.ProjectApi", PApi)
    monkeypatch.setattr(tmo_cli, "test_connection", lambda args: None)  # noqa

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
        def read_repo_config(self):  # noqa
            return {"project_id": "p1"}

    class PApi:
        def __init__(self, tmo_client, show_archived=False):  # noqa
            pass

        def __iter__(self):
            return iter([{"id": "p1", "name": "proj1"}, {"id": "p2", "name": "proj2"}])

        def find_by_id(self, pid):  # noqa
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
        def __init__(self, tmo_client, show_archived=False):  # noqa
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
        def read_repo_config(self):  # noqa
            return {"project_id": "p1"}

    class PApi:
        def __init__(self, tmo_client, show_archived=False):  # noqa
            pass

        def find_by_id(self, pid):  # noqa
            return None

    monkeypatch.setattr("tmo.ProjectApi", PApi)
    monkeypatch.setattr(tmo_cli, "validate_model_catalog_cwd_valid", lambda: True)

    result = tmo_cli.get_current_project(RM(), None, check_repo_conf=False)
    assert result is None


def test_get_current_project_no_repo_config(monkeypatch):
    class RM:
        def read_repo_config(self):  # noqa
            return None

    class PApi:
        def __init__(self, tmo_client, show_archived=False):  # noqa
            pass

        def find_by_id(self, pid):  # noqa
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
        def __init__(self, tmo_client, show_archived=False):  # noqa # noqa
            pass

        def find_by_id(self, pid):  # noqa
            return {
                "id": "p1",
                "name": "proj1",
                "gitRepositoryUrl": "https://git.example.com/repo",
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
        def __init__(self, tmo_client, show_archived=False):  # noqa
            pass

        def find_by_id(self, pid):  # noqa
            return None

    monkeypatch.setattr("tmo.ProjectApi", PApi)
    monkeypatch.setattr(
        tmo_cli,
        "list_and_select_projects",
        lambda rm, tmo, a, b: {
            "id": "p2",
            "name": "proj2",
            "gitRepositoryUrl": "https://git.example.com/repo",
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
            "gitRepositoryUrl": "https://git.example.com/repo",
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

        def get_templates(self, entity_type=None, source_path=None):  # noqa
            return {}

    args = SimpleNamespace(
        cwd=None, template_url="https://example.com", branch="main", name=None
    )
    with pytest.raises(SystemExit):
        tmo_cli.add_task(args, RM())


def test_add_task_success(monkeypatch, tmp_path):
    monkeypatch.setattr(tmo_cli, "validate_fe_tasks_cwd_valid", lambda: True)
    monkeypatch.setattr(tmo_cli, "input_select", lambda *a, **k: "task1")

    class RM:
        def clone_repository(self, url, path, branch):
            pass

        def get_templates(self, entity_type=None, source_path=None):  # noqa
            return {"task1": "/path/to/template"}

        def add_task(self, template, task_name, base_path):
            pass

    tmo_cli.base_path = str(tmp_path)
    args = SimpleNamespace(
        cwd=None, template_url="https://example.com", branch="main", name="mytask"
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
        lambda rm, tmo, check: {"id": "p1", "name": "proj1"},  # noqa
    )
    monkeypatch.setattr(tmo_cli, "activate_connection", lambda args: "c1")  # noqa

    class Client:
        def set_project_id(self, pid):
            pass

    class Runner:
        def __init__(self, rm):  # noqa
            pass

        def run_task_local(self, base_path, task_name, func):  # noqa
            return ("task1", "func1")  # noqa

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
        lambda rm, tmo: {"id": "p1", "name": "proj1"},  # noqa
    )

    class Client:
        def set_project_id(self, pid):
            pass

    class MApi:
        def __init__(self, tmo_client, show_archived=False):  # noqa
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
        lambda rm, tmo: {"id": "p1", "name": "proj1"},  # noqa
    )

    class Client:
        def set_project_id(self, pid):
            pass

    class Template:
        def __init__(self):
            self.id = "t1"
            self.name = "template1"

    class TApi:
        def __init__(self, tmo_client, show_archived=False):  # noqa
            pass

        def find_all(self):  # noqa
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
        lambda rm, tmo: {"id": "p1", "name": "proj1"},  # noqa
    )

    class Client:
        def set_project_id(self, pid):
            pass

    class Dataset:
        def __init__(self):
            self.id = "d1"
            self.name = "dataset1"

    class DApi:
        def __init__(self, tmo_client, show_archived=False):  # noqa
            pass

        def find_all(self):  # noqa
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
    monkeypatch.setattr(tmo_cli, "list_connections", lambda args: None)  # noqa

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

        def repo_config_exists(self):  # noqa
            return True

    args = SimpleNamespace(cwd=None)
    repo_manager = RM()
    tmo_cli.init_model_directory(args, repo_manager, None)
    assert repo_manager.inited is True


def test_add_model_with_prompts(monkeypatch, tmp_path):
    monkeypatch.setattr(tmo_cli, "validate_model_catalog_cwd_valid", lambda: True)

    inputs = iter(["https://example.com", "main", "model1", "desc"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr(
        tmo_cli,
        "input_select",
        lambda *a, **k: "python" if "language" in str(a) else "Template 1 (t1)",
    )

    class RM:
        def clone_repository(self, url, path, branch):
            pass

        def get_templates(self, entity_type=None, source_path=None):  # noqa
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


def test_set_cwd_valid_path_changes_directory(tmp_path, monkeypatch):
    """Test set_cwd changes directory when path is valid."""
    test_dir = tmp_path / "valid_dir"
    test_dir.mkdir()

    original_cwd = os.getcwd()
    tmo_cli.set_cwd(str(test_dir))

    # Verify directory was changed
    assert os.getcwd() == str(test_dir)

    # Restore original directory
    os.chdir(original_cwd)


def test_yes_or_no_handles_invalid_then_valid(monkeypatch):
    """Test yes_or_no retries on invalid input."""
    inputs = iter(["maybe", "x", "y"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    result = tmo_cli.yes_or_no("Proceed")
    assert result is True


def test_yes_or_no_uppercase_y(monkeypatch):
    """Test yes_or_no handles uppercase Y."""
    monkeypatch.setattr("builtins.input", lambda prompt: "Y")
    assert tmo_cli.yes_or_no("question") is True


def test_yes_or_no_uppercase_n(monkeypatch):
    """Test yes_or_no handles uppercase N."""
    monkeypatch.setattr("builtins.input", lambda prompt: "N")
    assert tmo_cli.yes_or_no("question") is False


def test_yes_or_no_yes_full_word(monkeypatch):
    """Test yes_or_no accepts 'yes' as input."""
    monkeypatch.setattr("builtins.input", lambda prompt: "yes")
    assert tmo_cli.yes_or_no("question") is True


def test_yes_or_no_no_full_word(monkeypatch):
    """Test yes_or_no accepts 'no' as input."""
    monkeypatch.setattr("builtins.input", lambda prompt: "no")
    assert tmo_cli.yes_or_no("question") is False


def test_bash_escape_handles_multiple_backslashes():
    """Test bash_escape with multiple backslashes."""
    assert tmo_cli.bash_escape(r"C:\path\to\file\deep") == r"C:\\path\\to\\file\\deep"


def test_bash_escape_empty_string():
    """Test bash_escape with empty string."""
    assert tmo_cli.bash_escape("") == ""


def test_bash_escape_string_without_backslashes():
    """Test bash_escape with string that has no backslashes."""
    assert tmo_cli.bash_escape("normal/path/here") == "normal/path/here"


def test_input_string_with_tooltip(monkeypatch, capsys):
    """Test input_string displays tooltip when provided."""
    monkeypatch.setattr("builtins.input", lambda prompt: "value")

    result = tmo_cli.input_string("name", tooltip="This is a helpful tooltip")

    captured = capsys.readouterr()
    assert "This is a helpful tooltip" in captured.out
    assert result == "value"


def test_input_string_required_empty_then_value(monkeypatch, capsys):
    """Test input_string retries when empty and required."""
    inputs = iter(["", "actual_value"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    result = tmo_cli.input_string("field", required=True)

    captured = capsys.readouterr()
    assert "Value required" in captured.out
    assert result == "actual_value"


def test_input_select_with_label(monkeypatch, capsys):
    """Test input_select prints label when provided."""
    monkeypatch.setattr("builtins.input", lambda prompt: "0")

    result = tmo_cli.input_select("option", ["A", "B"], label="Select One")

    captured = capsys.readouterr()
    assert "Select One" in captured.out
    assert "---" in captured.out  # Underline from print_underscored
    assert result == "A"


def test_input_select_empty_list_returns_none():
    """Test input_select returns None when values list is empty."""
    result = tmo_cli.input_select("option", [])
    assert result is None


def test_input_select_default_with_blank_input(monkeypatch):
    """Test input_select returns default when blank input provided."""
    monkeypatch.setattr("builtins.input", lambda prompt: "")

    result = tmo_cli.input_select("option", ["A", "B", "C"], default="B")
    assert result == "B"


def test_input_select_invalid_index_retries(monkeypatch, capsys):
    """Test input_select retries on invalid index."""
    inputs = iter(["99", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    result = tmo_cli.input_select("option", ["A", "B"])

    captured = capsys.readouterr()
    assert "Wrong selection" in captured.out
    assert result == "A"


def test_input_select_non_numeric_retries(monkeypatch, capsys):
    """Test input_select retries on non-numeric input."""
    inputs = iter(["abc", "1"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    result = tmo_cli.input_select("option", ["A", "B"])

    captured = capsys.readouterr()
    assert "Wrong selection" in captured.out
    assert result == "B"


def test_validate_model_catalog_cwd_valid_true(tmp_path, monkeypatch):
    """Test validate_model_catalog_cwd_valid returns True when directory exists."""
    model_dir = tmp_path / "model_definitions"
    model_dir.mkdir(parents=True)

    # Temporarily change base_path
    original_base = tmo_cli.base_path
    original_catalog = tmo_cli.model_catalog
    tmo_cli.base_path = str(tmp_path)
    tmo_cli.model_catalog = str(model_dir)

    result = tmo_cli.validate_model_catalog_cwd_valid()
    assert result is True

    # Restore
    tmo_cli.base_path = original_base
    tmo_cli.model_catalog = original_catalog


def test_validate_model_catalog_cwd_valid_false(tmp_path, monkeypatch):
    """Test validate_model_catalog_cwd_valid returns False when directory missing."""
    # Temporarily change to non-existent path
    original_catalog = tmo_cli.model_catalog
    tmo_cli.model_catalog = str(tmp_path / "nonexistent")

    result = tmo_cli.validate_model_catalog_cwd_valid()
    assert result is False

    # Restore
    tmo_cli.model_catalog = original_catalog


def test_validate_fe_tasks_cwd_valid_true(tmp_path):
    """Test validate_fe_tasks_cwd_valid returns True when directory exists."""
    fe_dir = tmp_path / "feature_engineering_tasks"
    fe_dir.mkdir(parents=True)

    original_catalog = tmo_cli.fe_tasks_catalog
    tmo_cli.fe_tasks_catalog = str(fe_dir)

    result = tmo_cli.validate_fe_tasks_cwd_valid()
    assert result is True

    tmo_cli.fe_tasks_catalog = original_catalog


def test_validate_fe_tasks_cwd_valid_false(tmp_path):
    """Test validate_fe_tasks_cwd_valid returns False when directory missing."""
    original_catalog = tmo_cli.fe_tasks_catalog
    tmo_cli.fe_tasks_catalog = str(tmp_path / "nonexistent")

    result = tmo_cli.validate_fe_tasks_cwd_valid()
    assert result is False

    tmo_cli.fe_tasks_catalog = original_catalog


def test_print_underscored_empty_message(capsys):
    """Test print_underscored with empty message."""
    tmo_cli.print_underscored("")
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    assert len(lines) == 2
    assert lines[0] == ""
    assert lines[1] == ""


def test_print_underscored_long_message(capsys):
    """Test print_underscored with long message."""
    long_msg = "A" * 100
    tmo_cli.print_underscored(long_msg)
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    assert lines[0] == long_msg
    assert lines[1] == "-" * 100


def test_set_connection_env_vars_all_fields(tmp_path):
    """Test _set_connection_env_vars sets all environment variables."""
    connection = {
        "id": "conn1",
        "username": "user1",
        "password": "pass1",
        "host": "localhost",
        "logmech": "TDNEGO",
        "database": "db1",
        "val_db": "val1",
        "ml_db": "byom1",  # Note: implementation uses ml_db, not byom_db
    }
    connections_list = [connection]

    # Clear any existing env vars
    for key in [
        "VMO_CONN_USERNAME",
        "VMO_CONN_PASSWORD",
        "VMO_CONN_HOST",
        "VMO_CONN_LOG_MECH",  # Note: implementation uses LOG_MECH with underscore
        "VMO_CONN_DATABASE",
        "VMO_VAL_INSTALL_DB",  # Note: implementation uses VAL_INSTALL_DB
        "VMO_BYOM_INSTALL_DB",  # Note: implementation uses BYOM_INSTALL_DB
    ]:
        os.environ.pop(key, None)

    tmo_cli._set_connection_env_vars("conn1", connections_list)

    assert os.environ.get("VMO_CONN_USERNAME") == "user1"
    assert os.environ.get("VMO_CONN_PASSWORD") == "pass1"
    assert os.environ.get("VMO_CONN_HOST") == "localhost"
    assert os.environ.get("VMO_CONN_LOG_MECH") == "TDNEGO"  # Correct env var name
    assert os.environ.get("VMO_CONN_DATABASE") == "db1"
    assert os.environ.get("VMO_VAL_INSTALL_DB") == "val1"  # Correct env var name
    assert os.environ.get("VMO_BYOM_INSTALL_DB") == "byom1"  # Correct env var name


def test_set_connection_env_vars_minimal_fields(tmp_path):
    """Test _set_connection_env_vars with only required fields."""
    connection = {
        "id": "conn2",
        "username": "user2",
        "password": "pass2",
        "host": "host2",
        "logmech": "TD2",
    }
    connections_list = [connection]

    tmo_cli._set_connection_env_vars("conn2", connections_list)

    assert os.environ.get("VMO_CONN_USERNAME") == "user2"
    assert os.environ.get("VMO_CONN_PASSWORD") == "pass2"


def test_select_connection_from_list_single_connection(monkeypatch):
    """Test _select_connection_from_list auto-selects when only one connection."""
    connections = [{"id": "only_one", "name": "Only Connection"}]

    result = tmo_cli._select_connection_from_list(connections)
    assert result == "only_one"


def test_select_connection_from_list_multiple_connections(monkeypatch):
    """Test _select_connection_from_list prompts when multiple connections."""
    connections = [
        {"id": "c1", "name": "Connection 1"},
        {"id": "c2", "name": "Connection 2"},
    ]

    # Mock accepts name, values, label (positional), plus **kwargs
    monkeypatch.setattr(
        tmo_cli, "input_select", lambda name, values, label="", **kwargs: "Connection 2"
    )

    result = tmo_cli._select_connection_from_list(connections)
    assert result == "c2"


def test_check_connection_exists_found_in_middle():  # noqa
    """Test _check_connection_exists finds connection in middle of list."""
    connections = [
        {"id": "c1"},
        {"id": "c2"},
        {"id": "c3"},
    ]
    assert tmo_cli._check_connection_exists("c2", connections) is True


def test_check_connection_exists_case_sensitivity():  # noqa
    """Test _check_connection_exists is case-sensitive."""
    connections = [{"id": "MyConn"}]
    assert tmo_cli._check_connection_exists("MyConn", connections) is True
    assert tmo_cli._check_connection_exists("myconn", connections) is False


def test_get_connections_list_with_single_connection():  # noqa
    """Test _get_connections_list with single connection."""
    connections_dict = {"connections": [{"id": "c1", "name": "Connection 1"}]}
    result = tmo_cli._get_connections_list(connections_dict)
    assert len(result) == 1
    assert result[0]["id"] == "c1"


def test_get_connections_list_preserves_order():  # noqa
    """Test _get_connections_list preserves connection order."""
    connections_dict = {
        "connections": [
            {"id": "c1", "name": "First"},
            {"id": "c2", "name": "Second"},
            {"id": "c3", "name": "Third"},
        ]
    }
    result = tmo_cli._get_connections_list(connections_dict)
    assert result[0]["id"] == "c1"
    assert result[1]["id"] == "c2"
    assert result[2]["id"] == "c3"


class TestSecurityNotice:

    def test_security_notice_constant_is_defined(self):
        assert hasattr(tmo_cli, "SECURITY_NOTICE")
        assert isinstance(tmo_cli.SECURITY_NOTICE, str)
        assert len(tmo_cli.SECURITY_NOTICE) > 0

    def test_security_notice_contains_required_phrases(self):
        notice = tmo_cli.SECURITY_NOTICE
        assert "protected system" in notice
        assert "authorized users" in notice
        assert "monitored" in notice
        assert "logged" in notice
        assert "audited" in notice
        assert "consent" in notice
        assert "Unauthorized access" in notice

    def test_security_notice_printed_for_remote_command(self, monkeypatch, capsys):
        import sys
        from unittest.mock import MagicMock

        monkeypatch.setattr(sys, "argv", ["tmo", "list", "-p"])

        mock_repo_manager = MagicMock()
        mock_tmo_client = MagicMock()

        mock_tmo_module = MagicMock()
        mock_tmo_module.RepoManager.return_value = mock_repo_manager
        mock_tmo_module.TmoClient.return_value = mock_tmo_client
        mock_tmo_module.__version__ = "1.0.0"

        original_tmo = sys.modules.get("tmo")
        sys.modules["tmo"] = mock_tmo_module

        monkeypatch.setattr(
            tmo_cli,
            "list_resources",
            lambda args, repo_manager, tmo_client, parent_parser: None,
        )

        try:
            tmo_cli.main()
        except SystemExit:
            pass
        finally:
            if original_tmo:
                sys.modules["tmo"] = original_tmo

        out, _ = capsys.readouterr()
        assert tmo_cli.SECURITY_NOTICE in out

    def test_security_notice_not_printed_for_local_command(self, monkeypatch, capsys):
        import sys

        monkeypatch.setattr(sys, "argv", ["tmo", "connection", "list"])
        monkeypatch.setattr(tmo_cli, "list_connections", lambda args, **kwargs: None)

        try:
            tmo_cli.main()
        except SystemExit:
            pass

        out, _ = capsys.readouterr()
        assert tmo_cli.SECURITY_NOTICE not in out

    def test_security_notice_not_printed_for_version_flag(self, monkeypatch, capsys):
        import sys

        monkeypatch.setattr(sys, "argv", ["tmo", "--version"])

        mock_tmo_module = type(sys)("tmo")
        mock_tmo_module.__version__ = "9.9.9"

        original_tmo = sys.modules.get("tmo")
        sys.modules["tmo"] = mock_tmo_module

        try:
            tmo_cli.main()
        except SystemExit:
            pass
        finally:
            if original_tmo:
                sys.modules["tmo"] = original_tmo

        out, _ = capsys.readouterr()
        assert tmo_cli.SECURITY_NOTICE not in out


class TestPrintProjectsList:
    """Tests for _print_projects_list function."""

    def test_print_projects_list_with_projects_as_list_true(self, capsys):
        """Test printing projects with as_list=True."""
        projects = [
            {"id": "id1", "name": "Project 1"},
            {"id": "id2", "name": "Project 2"},
        ]
        tmo_cli._print_projects_list(projects, as_list=True)

        captured = capsys.readouterr()
        assert "List of projects:" in captured.out
        assert "[0] (id1) Project 1" in captured.out
        assert "[1] (id2) Project 2" in captured.out

    def test_print_projects_list_with_projects_as_list_false(self, capsys):
        """Test printing projects with as_list=False."""
        projects = [
            {"id": "id1", "name": "Project 1"},
        ]
        tmo_cli._print_projects_list(projects, as_list=False)

        captured = capsys.readouterr()
        assert "Available projects:" in captured.out
        assert "[0] (id1) Project 1" in captured.out

    def test_print_projects_list_with_empty_list(self, capsys):
        """Test printing when no projects exist."""
        projects = []
        tmo_cli._print_projects_list(projects, as_list=False)

        captured = capsys.readouterr()
        assert "No projects were found" in captured.out

    def test_print_projects_list_with_single_project(self, capsys):
        """Test printing single project."""
        projects = [{"id": "single-id", "name": "Single Project"}]
        tmo_cli._print_projects_list(projects, as_list=True)

        captured = capsys.readouterr()
        assert "[0] (single-id) Single Project" in captured.out

    def test_print_projects_list_with_many_projects(self, capsys):
        """Test printing many projects."""
        projects = [{"id": f"id{i}", "name": f"Project {i}"} for i in range(10)]
        tmo_cli._print_projects_list(projects, as_list=False)

        captured = capsys.readouterr()
        assert "[0] (id0) Project 0" in captured.out
        assert "[9] (id9) Project 9" in captured.out


class TestFindCurrentProjectIndex:
    """Tests for _find_current_project_index function."""

    def test_find_current_project_index_with_matching_project(self):
        """Test finding index when project exists in list."""
        projects = [
            {"id": "id1", "name": "P1"},
            {"id": "id2", "name": "P2"},
            {"id": "id3", "name": "P3"},
        ]
        current_project = {"id": "id2", "name": "P2"}

        result = tmo_cli._find_current_project_index(projects, current_project)
        assert result == 1

    def test_find_current_project_index_with_first_project(self):
        """Test finding index when project is first."""
        projects = [
            {"id": "id1", "name": "P1"},
            {"id": "id2", "name": "P2"},
        ]
        current_project = {"id": "id1"}

        result = tmo_cli._find_current_project_index(projects, current_project)
        assert result == 0

    def test_find_current_project_index_with_last_project(self):
        """Test finding index when project is last."""
        projects = [
            {"id": "id1", "name": "P1"},
            {"id": "id2", "name": "P2"},
            {"id": "id3", "name": "P3"},
        ]
        current_project = {"id": "id3"}

        result = tmo_cli._find_current_project_index(projects, current_project)
        assert result == 2

    def test_find_current_project_index_with_no_match(self):
        """Test finding index when project not in list."""
        projects = [
            {"id": "id1", "name": "P1"},
            {"id": "id2", "name": "P2"},
        ]
        current_project = {"id": "id999", "name": "Not Found"}

        result = tmo_cli._find_current_project_index(projects, current_project)
        assert result == "none"

    def test_find_current_project_index_with_none_current_project(self):
        """Test finding index when current_project is None."""
        projects = [{"id": "id1", "name": "P1"}]

        result = tmo_cli._find_current_project_index(projects, None)
        assert result == "none"

    def test_find_current_project_index_with_empty_current_project(self):
        """Test finding index when current_project is empty dict."""
        projects = [{"id": "id1", "name": "P1"}]
        current_project = {}

        result = tmo_cli._find_current_project_index(projects, current_project)
        assert result == "none"

    def test_find_current_project_index_with_empty_projects_list(self):
        """Test finding index when projects list is empty."""
        projects = []
        current_project = {"id": "id1"}

        result = tmo_cli._find_current_project_index(projects, current_project)
        assert result == "none"

    def test_find_current_project_index_without_id_key_in_current(self):
        """Test when current_project doesn't have 'id' key."""
        projects = [{"id": "id1", "name": "P1"}]
        current_project = {"name": "P1"}  # No 'id' key

        result = tmo_cli._find_current_project_index(projects, current_project)
        assert result == "none"


class TestValidateProjectSelection:
    """Tests for _validate_project_selection function."""

    def test_validate_project_selection_with_valid_numeric_index(self):
        """Test validation with valid numeric index."""
        projects = [{"id": "1"}, {"id": "2"}, {"id": "3"}]

        result = tmo_cli._validate_project_selection("1", projects, "none")
        assert result is True

    def test_validate_project_selection_with_zero_index(self):
        """Test validation with index 0."""
        projects = [{"id": "1"}, {"id": "2"}]

        result = tmo_cli._validate_project_selection("0", projects, "none")
        assert result is True

    def test_validate_project_selection_with_last_index(self):
        """Test validation with last valid index."""
        projects = [{"id": "1"}, {"id": "2"}, {"id": "3"}]

        result = tmo_cli._validate_project_selection("2", projects, "none")
        assert result is True

    def test_validate_project_selection_with_index_out_of_range(self):
        """Test validation with index >= len(projects)."""
        projects = [{"id": "1"}, {"id": "2"}]

        result = tmo_cli._validate_project_selection("5", projects, "none")
        assert result is False

    def test_validate_project_selection_with_index_equal_to_length(self):
        """Test validation with index == len(projects)."""
        projects = [{"id": "1"}, {"id": "2"}]

        result = tmo_cli._validate_project_selection("2", projects, "none")
        assert result is False

    def test_validate_project_selection_with_negative_index(self):
        """Test validation with negative index string."""
        projects = [{"id": "1"}, {"id": "2"}]

        # "-1" is not numeric according to isnumeric()
        result = tmo_cli._validate_project_selection("-1", projects, "none")
        assert result is False

    def test_validate_project_selection_with_non_numeric_string(self):
        """Test validation with non-numeric string."""
        projects = [{"id": "1"}, {"id": "2"}]

        result = tmo_cli._validate_project_selection("abc", projects, "none")
        assert result is False

    def test_validate_project_selection_with_empty_string_and_valid_current(self):
        """Test validation with empty string when current_index is valid."""
        projects = [{"id": "1"}, {"id": "2"}]

        result = tmo_cli._validate_project_selection("", projects, 1)
        assert result is True

    def test_validate_project_selection_with_empty_string_and_none_current(self):
        """Test validation with empty string when current_index is 'none'."""
        projects = [{"id": "1"}, {"id": "2"}]

        result = tmo_cli._validate_project_selection("", projects, "none")
        assert result is False

    def test_validate_project_selection_with_whitespace_string(self):
        """Test validation with whitespace string."""
        projects = [{"id": "1"}, {"id": "2"}]

        result = tmo_cli._validate_project_selection("  ", projects, "none")
        assert result is False

    def test_validate_project_selection_with_float_string(self):
        """Test validation with float string."""
        projects = [{"id": "1"}, {"id": "2"}]

        result = tmo_cli._validate_project_selection("1.5", projects, "none")
        assert result is False

    def test_validate_project_selection_complex_condition_true(self):
        """Test the TRUE path of the complex condition."""
        # (not tmp_index.isnumeric() or int(tmp_index) >= len(projects)) and tmp_index != ""
        # TRUE and TRUE = TRUE → return False
        projects = [{"id": "1"}]

        # Case 1: not numeric AND not empty
        result = tmo_cli._validate_project_selection("abc", projects, 0)
        assert result is False

        # Case 2: numeric but out of range AND not empty
        result = tmo_cli._validate_project_selection("10", projects, 0)
        assert result is False

    def test_validate_project_selection_complex_condition_false(self):
        """Test the FALSE path of the complex condition."""
        # (not tmp_index.isnumeric() or int(tmp_index) >= len(projects)) and tmp_index != ""
        # FALSE and X = FALSE → check second condition
        projects = [{"id": "1"}, {"id": "2"}]

        # tmp_index is empty string, current_index is valid
        result = tmo_cli._validate_project_selection("", projects, 0)
        assert (
            result is True
        )  # Second condition is False, so overall False → return True


class TestHandleInvalidGrantError:
    """Tests for _handle_invalid_grant_error function."""

    def test_handle_invalid_grant_error_token_not_active_calls_exit(
        self, monkeypatch, caplog
    ):
        """Test handling 'Token is not active' error."""
        from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

        ge = InvalidGrantError(description="Token is not active")
        args = type("Args", (), {"debug": False})()

        remove_called = []

        def mock_remove():
            remove_called.append(True)

        # Mock sys.exit to prevent actual exit
        exit_called = []
        monkeypatch.setattr("sys.exit", lambda code: exit_called.append(code))

        tmo_cli._handle_invalid_grant_error(ge, args, mock_remove)

        # Should call remove_token_func
        assert len(remove_called) == 1
        # Should call sys.exit(1)
        assert exit_called == [1]

        # Should log error message
        assert any("Token is not active" in record.message for record in caplog.records)

    def test_handle_invalid_grant_error_session_not_active_calls_exit(
        self, monkeypatch, caplog  # noqa
    ):
        """Test handling 'Session not active' error."""
        from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

        ge = InvalidGrantError(description="Session not active")
        args = type("Args", (), {"debug": False})()

        remove_called = []

        def mock_remove():
            remove_called.append(True)

        exit_called = []
        monkeypatch.setattr("sys.exit", lambda code: exit_called.append(code))

        tmo_cli._handle_invalid_grant_error(ge, args, mock_remove)

        assert len(remove_called) == 1
        assert exit_called == [1]

        # Should log error message
        assert any("Session not active" in record.message for record in caplog.records)

    def test_handle_invalid_grant_error_other_description_calls_generic_handler(
        self, monkeypatch
    ):
        """Test handling other InvalidGrantError descriptions."""
        from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

        ge = InvalidGrantError(description="Some other error")
        args = type("Args", (), {"debug": True})()

        # Mock handle_generic_error
        generic_error_calls = []
        monkeypatch.setattr(
            tmo_cli,
            "handle_generic_error",
            lambda err, debug: generic_error_calls.append((err, debug)),
        )

        tmo_cli._handle_invalid_grant_error(ge, args, lambda: None)

        # Should call handle_generic_error with the exception and debug flag
        assert len(generic_error_calls) == 1
        assert generic_error_calls[0][0] == ge
        assert generic_error_calls[0][1] is True

    def test_handle_invalid_grant_error_does_not_call_remove_for_other_errors(
        self, monkeypatch
    ):
        """Test that remove_token is NOT called for other error descriptions."""
        from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

        ge = InvalidGrantError(description="Different error")
        args = type("Args", (), {"debug": False})()

        remove_called = []

        def mock_remove():
            remove_called.append(True)

        monkeypatch.setattr(tmo_cli, "handle_generic_error", lambda err, debug: None)

        tmo_cli._handle_invalid_grant_error(ge, args, mock_remove)

        # Should NOT call remove_token_func
        assert len(remove_called) == 0


class TestPrintUnderscored:
    """Tests for print_underscored function."""

    def test_print_underscored_short_message(self, capsys):
        """Test printing with short message."""
        tmo_cli.print_underscored("Test Message")

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert lines[0] == "Test Message"
        assert lines[1] == "------------"

    def test_print_underscored_long_message(self, capsys):
        """Test printing with message longer than 100 chars."""
        long_msg = "A" * 150
        tmo_cli.print_underscored(long_msg)

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert lines[0] == long_msg
        assert lines[1] == "-" * 150  # Should match message length

    def test_print_underscored_empty_message(self, capsys):
        """Test printing with empty message."""
        tmo_cli.print_underscored("")

        captured = capsys.readouterr()
        # With empty message, prints two empty lines
        # Using splitlines() removes trailing empty lines, so check raw output
        assert (
            captured.out == "\n\n"
        )  # Empty message + empty underline + trailing newline

    def test_print_underscored_exactly_100_chars(self, capsys):
        """Test printing with exactly 100 character message."""
        msg = "X" * 100
        tmo_cli.print_underscored(msg)

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert lines[0] == msg
        assert lines[1] == "-" * 100


class TestCheckIfAnyResourceSelected:
    """Tests for _check_if_any_resource_selected function."""

    def test_check_if_any_resource_selected_all_false(self):
        """Test when no resources are selected."""
        args = type(
            "Args",
            (),
            {
                "projects": False,
                "models": False,
                "local_models": False,
                "templates": False,
                "datasets": False,
                "connections": False,
            },
        )()

        result = tmo_cli._check_if_any_resource_selected(args)
        assert result is False

    def test_check_if_any_resource_selected_projects_true(self):
        """Test when projects is selected."""
        args = type(
            "Args",
            (),
            {
                "projects": True,
                "models": False,
                "local_models": False,
                "templates": False,
                "datasets": False,
                "connections": False,
            },
        )()

        result = tmo_cli._check_if_any_resource_selected(args)
        assert result is True

    def test_check_if_any_resource_selected_templates_true(self):
        """Test when templates is selected."""
        args = type(
            "Args",
            (),
            {
                "projects": False,
                "models": False,
                "local_models": False,
                "templates": True,
                "datasets": False,
                "connections": False,
            },
        )()

        result = tmo_cli._check_if_any_resource_selected(args)
        assert result is True

    def test_check_if_any_resource_selected_datasets_true(self):
        """Test when datasets is selected."""
        args = type(
            "Args",
            (),
            {
                "projects": False,
                "models": False,
                "local_models": False,
                "templates": False,
                "datasets": True,
                "connections": False,
            },
        )()

        result = tmo_cli._check_if_any_resource_selected(args)
        assert result is True

    def test_check_if_any_resource_selected_local_models_true(self):
        """Test when local_models is selected."""
        args = type(
            "Args",
            (),
            {
                "projects": False,
                "models": False,
                "local_models": True,
                "templates": False,
                "datasets": False,
                "connections": False,
            },
        )()

        result = tmo_cli._check_if_any_resource_selected(args)
        assert result is True

    def test_check_if_any_resource_selected_multiple_true(self):
        """Test when multiple resources are selected."""
        args = type(
            "Args",
            (),
            {
                "projects": True,
                "models": True,
                "local_models": False,
                "templates": True,
                "datasets": False,
                "connections": False,
            },
        )()

        result = tmo_cli._check_if_any_resource_selected(args)
        assert result is True

    def test_check_if_any_resource_selected_all_true(self):
        """Test when all resources are selected."""
        args = type(
            "Args",
            (),
            {
                "projects": True,
                "models": True,
                "local_models": True,
                "templates": True,
                "datasets": True,
                "connections": True,
            },
        )()

        result = tmo_cli._check_if_any_resource_selected(args)
        assert result is True


class TestListConnectionsEdgeCases:
    """Tests for list_connections edge cases and error paths."""

    def test_list_connections_with_cwd(self, tmp_path, monkeypatch):
        """Test list_connections with args.cwd parameter."""
        connections_file = tmp_path / ".tmo" / "connections.yaml"
        connections_file.parent.mkdir(parents=True, exist_ok=True)
        connections_file.write_text(
            yaml.dump({
                "connections": [{
                    "id": "conn1",
                    "name": "Test Connection",
                    "username": "user1",
                    "host": "host1",
                    "database": "db1",
                }]
            })
        )

        monkeypatch.setattr(tmo_cli, "config_dir", str(tmp_path / ".tmo"))

        args = type("Args", (), {"cwd": str(tmp_path)})()
        tmo_cli.list_connections(args)
        # Should not raise, just prints

    def test_list_connections_empty_connections_list(self, tmp_path, monkeypatch):
        """Test list_connections when connections list is empty."""
        connections_file = tmp_path / ".tmo" / "connections.yaml"
        connections_file.parent.mkdir(parents=True, exist_ok=True)
        connections_file.write_text(yaml.dump({"connections": []}))

        monkeypatch.setattr(tmo_cli, "config_dir", str(tmp_path / ".tmo"))

        args = type("Args", (), {"cwd": None})()
        tmo_cli.list_connections(args)
        # Should log error about no connections


class TestAddConnectionsEdgeCases:
    """Tests for add_connections error handling paths."""

    def test_add_connections_save_file_error(self, tmp_path, monkeypatch):
        """Test add_connections when saving file fails."""
        from pathlib import Path

        # Use home directory which is in safe_dirs
        home_tmo = Path.home() / ".tmo_test_save_error"
        home_tmo.mkdir(parents=True, exist_ok=True)

        # Mock config_dir to point to home location
        monkeypatch.setattr(tmo_cli, "config_dir", str(home_tmo))
        monkeypatch.setattr(tmo_cli, "CONNECTIONS_YAML_FILE", "{}/connections.yaml")
        monkeypatch.setattr(tmo_cli, "KEY_FILE", "{}/{}.key")
        monkeypatch.setattr(tmo_cli, "PASS_FILE", "{}/{}.pass")

        # Mock inputs
        inputs = iter(["TestConn", "host", "user", "pass", "", "val", "mldb", "TD2"])
        monkeypatch.setattr(
            tmo_cli, "input_string", lambda name, req=False, **kw: next(inputs)
        )

        # Mock crypto to avoid file system issues
        from tmo import crypto

        monkeypatch.setattr(
            crypto, "td_encrypt_password", lambda password=None, **kwargs: "encrypted"
        )

        # Mock yaml.safe_dump to raise exception
        def mock_dump(*args, **kwargs):  # noqa
            raise Exception("Write failed")

        monkeypatch.setattr(yaml, "safe_dump", mock_dump)

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "name": "TestConn",
                "host": "host",
                "username": "user",
                "password": "pass",
                "database": "",
                "val_db": "val",
                "byom_db": "mldb",
                "logmech": "TD2",
            },
        )()

        try:
            with pytest.raises(SystemExit) as exc:
                tmo_cli.add_connections(args)
            assert exc.value.code == 1
        finally:
            # Cleanup
            import shutil

            if home_tmo.exists():
                shutil.rmtree(home_tmo)


class TestRemoveConnectionsEdgeCases:
    """Tests for remove_connections error handling paths."""

    def test_remove_connections_with_key_and_pass_files(self, tmp_path, monkeypatch):
        """Test remove_connections removes key and pass files if they exist."""
        from pathlib import Path

        # Use home directory which is in safe_dirs
        config_path = Path.home() / ".tmo_test_remove_keys"
        config_path.mkdir(parents=True, exist_ok=True)

        # Create connections file
        connections_file = config_path / "connections.yaml"
        connections_file.write_text(
            yaml.dump({
                "connections": [{
                    "id": "conn1",
                    "name": "Test Connection",
                    "username": "user1",
                    "host": "host1",
                }]
            })
        )

        # Create key and pass files
        key_file = config_path / "conn1.key"
        pass_file = config_path / "conn1.pass"
        key_file.write_text("keydata")
        pass_file.write_text("passdata")

        monkeypatch.setattr(tmo_cli, "config_dir", str(config_path))
        monkeypatch.setattr(tmo_cli, "KEY_FILE", "{}/{}.key")
        monkeypatch.setattr(tmo_cli, "PASS_FILE", "{}/{}.pass")
        monkeypatch.setattr(tmo_cli, "CONNECTIONS_YAML_FILE", "{}/connections.yaml")

        args = type("Args", (), {"cwd": None, "connection": "conn1"})()

        try:
            tmo_cli.remove_connections(args)

            # Verify files were removed
            assert not key_file.exists()
            assert not pass_file.exists()
        finally:
            # Cleanup
            import shutil

            if config_path.exists():
                shutil.rmtree(config_path)

    def test_remove_connections_save_error(self, tmp_path, monkeypatch):
        """Test remove_connections when save fails."""
        from pathlib import Path

        # Use home directory
        config_path = Path.home() / ".tmo_test_remove_save_err"
        config_path.mkdir(parents=True, exist_ok=True)

        connections_file = config_path / "connections.yaml"
        connections_file.write_text(
            yaml.dump({
                "connections": [
                    {"id": "conn1", "name": "Test", "username": "u", "host": "h"}
                ]
            })
        )

        monkeypatch.setattr(tmo_cli, "config_dir", str(config_path))
        monkeypatch.setattr(tmo_cli, "CONNECTIONS_YAML_FILE", "{}/connections.yaml")

        # Mock yaml.safe_dump to raise exception
        def mock_dump(*args, **kwargs):  # noqa
            raise Exception("Write failed")

        monkeypatch.setattr(yaml, "safe_dump", mock_dump)

        args = type("Args", (), {"cwd": None, "connection": "conn1"})()

        try:
            with pytest.raises(SystemExit) as exc:
                tmo_cli.remove_connections(args)
            assert exc.value.code == 1
        finally:
            # Cleanup
            import shutil

            if config_path.exists():
                shutil.rmtree(config_path)


class TestExportConnectionEdgeCases:
    """Tests for export_connection error handling paths."""

    def test_export_connection_with_cwd(self, tmp_path, monkeypatch, capsys):
        """Test export_connection with args.cwd parameter."""
        config_path = tmp_path / ".tmo"
        config_path.mkdir(parents=True, exist_ok=True)

        connections_file = config_path / "connections.yaml"
        connections_file.write_text(
            yaml.dump({
                "connections": [{
                    "id": "conn1",
                    "name": "Test Connection",
                    "username": "user1",
                    "host": "host1",
                    "database": "db1",
                    "logmech": "TD2",
                    "password": "encrypted_pass",
                }]
            })
        )

        monkeypatch.setattr(tmo_cli, "config_dir", str(config_path))

        args = type("Args", (), {"cwd": str(tmp_path), "connection": "conn1"})()
        tmo_cli.export_connection(args)

        captured = capsys.readouterr()
        assert "export VMO_CONN_HOST" in captured.out
        assert "host1" in captured.out


class TestActivateConnectionEdgeCases:
    """Tests for activate_connection additional paths."""

    def test_activate_connection_with_cwd(self, tmp_path, monkeypatch):
        """Test activate_connection with args.cwd parameter."""
        config_path = tmp_path / ".tmo"
        config_path.mkdir(parents=True, exist_ok=True)

        connections_file = config_path / "connections.yaml"
        connections_file.write_text(
            yaml.dump({
                "connections": [{
                    "id": "conn1",
                    "name": "Test",
                    "username": "user1",
                    "host": "host1",
                    "database": "db1",
                    "logmech": "TD2",
                    "password": "encrypted_pass",
                }]
            })
        )

        monkeypatch.setattr(tmo_cli, "config_dir", str(config_path))

        args = type("Args", (), {"cwd": str(tmp_path), "connection": "conn1"})()
        result = tmo_cli.activate_connection(args)
        assert result == "conn1"


class TestAddModelEdgeCases:
    """Tests for add_model function paths."""

    def test_add_model_with_cwd(self, tmp_path, monkeypatch):
        """Test add_model with args.cwd parameter."""
        # Setup mock repo directory
        repo_dir = tmp_path / "model_repo"
        repo_dir.mkdir(parents=True, exist_ok=True)
        (repo_dir / "model_definitions").mkdir()

        # Mock validate function
        monkeypatch.setattr(tmo_cli, "validate_model_catalog_cwd_valid", lambda: True)

        # Mock inputs - input_string is called for: model name, model description
        string_inputs = iter(["NewModel", "Test model"])
        monkeypatch.setattr(
            tmo_cli, "input_string", lambda name, req=False, **kw: next(string_inputs)
        )

        # Mock input_select - called for: model language, model template
        select_inputs = iter(["python", "desc1 (template1)"])
        monkeypatch.setattr(
            tmo_cli,
            "input_select",
            lambda name, values, label="", default=None: next(select_inputs),
        )

        class MockRepoManager:
            def clone_repository(self, url, path, branch):
                pass

            def get_templates(self, entity_type, source_path):  # noqa
                return {"python": {"template1": ("desc1", str(tmp_path / "template"))}}

            def add_model(self, **kwargs):
                pass

        repo_manager = MockRepoManager()

        args = type(
            "Args",
            (),
            {
                "cwd": str(repo_dir),
                "template_url": "https://github.com/test/repo",
                "branch": "main",
            },
        )()

        # Should not raise
        tmo_cli.add_model(args, repo_manager)

    def test_add_model_no_branch_defaults_to_main(self, tmp_path, monkeypatch):
        """Test add_model when branch is not provided defaults to main."""
        monkeypatch.setattr(tmo_cli, "validate_model_catalog_cwd_valid", lambda: True)

        # Mock input_string - called for: template_url, branch, model name, model description
        string_inputs = iter([
            "https://github.com/test/repo",
            "",  # branch empty - should default to "main"
            "NewModel",
            "Test model",
        ])
        monkeypatch.setattr(
            tmo_cli, "input_string", lambda name, req=False, **kw: next(string_inputs)
        )

        # Mock input_select - called for: model language, model template
        select_inputs = iter(["python", "desc1 (template1)"])
        monkeypatch.setattr(
            tmo_cli,
            "input_select",
            lambda name, values, label="", default=None: next(select_inputs),
        )

        class MockRepoManager:
            def __init__(self):
                self.cloned_branch = None

            def clone_repository(self, url, path, branch):  # noqa
                self.cloned_branch = branch

            def get_templates(self, entity_type, source_path):  # noqa
                return {"python": {"template1": ("desc1", str(tmp_path / "template"))}}

            def add_model(self, **kwargs):
                pass

        repo_manager = MockRepoManager()

        args = type("Args", (), {"cwd": None, "template_url": None, "branch": None})()

        tmo_cli.add_model(args, repo_manager)
        assert repo_manager.cloned_branch == "main"


class TestAddTaskEdgeCases:
    """Tests for add_task function additional paths."""

    def test_add_task_with_cwd(self, tmp_path, monkeypatch):
        """Test add_task with args.cwd parameter."""
        task_repo_dir = tmp_path / "task_repo"
        task_repo_dir.mkdir(parents=True, exist_ok=True)
        (task_repo_dir / "feature_engineering_tasks").mkdir()

        monkeypatch.setattr(tmo_cli, "validate_fe_tasks_cwd_valid", lambda: True)

        # Mock input_select - called for: task template selection
        select_inputs = iter(["task1"])
        monkeypatch.setattr(
            tmo_cli,
            "input_select",
            lambda name, values, label="", default=None: next(select_inputs),
        )

        # Mock input_string - called for: task name (only if args.name is None)
        # Since args.name is "TaskName", input_string won't be called
        string_inputs = iter([])
        monkeypatch.setattr(
            tmo_cli, "input_string", lambda name, req=False, **kw: next(string_inputs)
        )

        class MockRepoManager:
            def clone_repository(self, url, path, branch):
                pass

            def get_templates(self, entity_type, source_path):  # noqa
                return {"task1": str(tmp_path / "task_template")}

            def add_task(self, **kwargs):
                pass

        repo_manager = MockRepoManager()

        args = type(
            "Args",
            (),
            {
                "cwd": str(task_repo_dir),
                "template_url": "https://github.com/test/repo",
                "branch": "main",
                "name": "TaskName",
            },
        )()

        tmo_cli.add_task(args, repo_manager)

    def test_add_task_empty_name_uses_template_name(self, tmp_path, monkeypatch):
        """Test add_task when name is empty defaults to template name."""
        monkeypatch.setattr(tmo_cli, "validate_fe_tasks_cwd_valid", lambda: True)

        # Mock input_string - called for: template_url, branch, task name
        string_inputs = iter([
            "https://github.com/test/repo",
            "main",
            "",  # Empty task name - should use template name
        ])
        monkeypatch.setattr(
            tmo_cli, "input_string", lambda name, req=False, **kw: next(string_inputs)
        )

        # Mock input_select - called for: task template
        select_inputs = iter(["task1"])
        monkeypatch.setattr(
            tmo_cli,
            "input_select",
            lambda name, values, label="", default=None: next(select_inputs),
        )

        class MockRepoManager:
            def __init__(self):
                self.task_name_used = None

            def clone_repository(self, url, path, branch):
                pass

            def get_templates(self, entity_type, source_path):  # noqa
                return {"task1": str(tmp_path / "task_template")}

            def add_task(self, task_name, **kwargs):  # noqa
                self.task_name_used = task_name

        repo_manager = MockRepoManager()

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "template_url": None,
                "branch": None,
                "name": "",
            },
        )()

        tmo_cli.add_task(args, repo_manager)
        assert repo_manager.task_name_used == "task1"


class TestRunTaskEdgeCases:
    """Tests for run_task function additional paths."""

    def test_run_task_with_cwd(self, tmp_path, monkeypatch):
        """Test run_task processes cwd parameter."""
        # Track if set_cwd was called
        cwd_calls = []

        def mock_set_cwd(path):
            cwd_calls.append(path)

        monkeypatch.setattr(tmo_cli, "set_cwd", mock_set_cwd)

        # Mock get_current_project to return None and trigger early exit
        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: None,
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": str(tmp_path),
                "connection": None,
                "name": None,
                "function_name": None,
            },
        )()

        # Should call set_cwd then exit due to no project
        with pytest.raises(SystemExit):
            tmo_cli.run_task(args, repo_manager, tmo_client)

        # Verify cwd was processed
        assert len(cwd_calls) == 1
        assert cwd_calls[0] == str(tmp_path)


class TestMainFunctionPaths:
    """Tests for main() function execution paths."""

    def test_main_with_version_flag(self, monkeypatch, capsys):
        """Test main() with --version flag."""
        monkeypatch.setattr("sys.argv", ["tmo", "--version"])

        tmo_cli.main()

        captured = capsys.readouterr()
        # Check that output contains a version number (e.g., "7.2.3")
        assert captured.out.strip()  # Not empty
        # Version format is typically x.y.z
        import re

        assert re.match(r"\d+\.\d+\.\d+", captured.out.strip())

    def test_main_connection_error_with_debug(self, monkeypatch, caplog):
        """Test main() handles ConnectionError with debug flag."""
        from unittest.mock import MagicMock
        import requests
        import sys

        monkeypatch.setattr("sys.argv", ["tmo", "list", "-p", "--debug"])

        # Mock TmoClient to raise ConnectionError
        class MockTmoClient:
            def __init__(self):
                raise requests.exceptions.ConnectionError("Connection failed")

        original_tmo = sys.modules.get("tmo")

        mock_tmo = MagicMock()
        mock_tmo.TmoClient = MockTmoClient
        mock_tmo.RepoManager = MagicMock()
        sys.modules["tmo"] = mock_tmo

        with pytest.raises(SystemExit) as exc:
            tmo_cli.main()

        assert exc.value.code == 1

        # Check that error was logged (not printed to stdout)
        assert any(
            "Could not connect to ModelOps API" in record.message
            for record in caplog.records
        )

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_main_invalid_token_error(self, monkeypatch, capsys, tmp_path):
        """Test main() handles InvalidTokenError."""
        from unittest.mock import MagicMock
        import oauthlib.oauth2.rfc6749.errors
        import sys

        monkeypatch.setattr("sys.argv", ["tmo", "list", "-p"])

        # Mock token cache file
        token_file = tmp_path / "token_cache.json"
        token_file.write_text("{}")

        # Note: TmoClient is imported inside main(), not in tmo_cli module
        # We need to mock it via sys.modules instead

        # Mock TmoClient to raise InvalidTokenError
        class MockTmoClient:
            DEFAULT_TOKEN_CACHE_FILE_PATH = str(token_file)

            def __init__(self):
                raise oauthlib.oauth2.rfc6749.errors.InvalidTokenError("Token invalid")

        original_tmo = sys.modules.get("tmo")

        mock_tmo = MagicMock()
        mock_tmo.TmoClient = MockTmoClient
        mock_tmo.RepoManager = MagicMock()
        sys.modules["tmo"] = mock_tmo

        with pytest.raises(SystemExit) as exc:
            tmo_cli.main()

        assert exc.value.code == 1
        assert not token_file.exists()  # Token cache should be removed

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_main_keyboard_interrupt(self, monkeypatch, caplog):
        """Test main() handles KeyboardInterrupt gracefully."""
        from unittest.mock import MagicMock
        import sys

        monkeypatch.setattr("sys.argv", ["tmo", "list", "-p"])

        # Mock TmoClient to raise KeyboardInterrupt
        class MockTmoClient:
            def __init__(self):
                raise KeyboardInterrupt()

        original_tmo = sys.modules.get("tmo")

        mock_tmo = MagicMock()
        mock_tmo.TmoClient = MockTmoClient
        mock_tmo.RepoManager = MagicMock()
        sys.modules["tmo"] = mock_tmo

        with pytest.raises(SystemExit) as exc:
            tmo_cli.main()

        assert exc.value.code == 1

        # Check that message was logged
        assert any("Keyboard interrupt" in record.message for record in caplog.records)

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_main_generic_exception_with_debug(self, monkeypatch, caplog):
        """Test main() handles generic exception with debug flag."""
        from unittest.mock import MagicMock
        import sys

        monkeypatch.setattr("sys.argv", ["tmo", "list", "-p", "--debug"])

        # Mock TmoClient to raise generic exception
        class MockTmoClient:
            def __init__(self):
                raise RuntimeError("Something went wrong")

        original_tmo = sys.modules.get("tmo")

        mock_tmo = MagicMock()
        mock_tmo.TmoClient = MockTmoClient
        mock_tmo.RepoManager = MagicMock()
        sys.modules["tmo"] = mock_tmo

        # Should call handle_generic_error which logs exception when debug=True
        # Note: handle_generic_error doesn't exit when debug=True, just logs
        tmo_cli.main()

        # Check that error was logged
        assert any("An error occurred" in record.message for record in caplog.records)

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_main_local_function_no_client_needed(self, monkeypatch, tmp_path):
        """Test main() with local functions that don't need TmoClient."""
        config_path = tmp_path / ".tmo"
        config_path.mkdir(parents=True, exist_ok=True)

        connections_file = config_path / "connections.yaml"
        connections_file.write_text(
            yaml.dump({
                "connections": [
                    {"id": "c1", "name": "Test", "username": "u", "host": "h"}
                ]
            })
        )

        monkeypatch.setattr(tmo_cli, "config_dir", str(config_path))
        monkeypatch.setattr("sys.argv", ["tmo", "connection", "list"])

        # Should execute without needing TmoClient
        tmo_cli.main()


class TestRunModelComplexPaths:
    """Tests for complex run_model function logic."""

    def test_run_model_with_cwd_parameter(self, tmp_path, monkeypatch):
        """Test run_model with args.cwd set."""
        from unittest.mock import MagicMock

        # Mock get_current_project to return a project
        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: {"id": "proj-123"},
        )

        # Create complex mock for run_model
        mock_train_model = MagicMock()
        mock_train_model.get_model_ids.return_value = {
            0: {"id": "model-1", "name": "TestModel"}
        }

        mock_dataset_template_api = MagicMock()
        mock_template = MagicMock()
        mock_template.id = "template-1"
        mock_template.name = "TestTemplate"
        mock_dataset_template_api.return_value.find_all.return_value = [mock_template]
        mock_dataset_template_api.return_value.render.return_value = {"data": "test"}

        import sys

        original_tmo = sys.modules.get("tmo")
        mock_tmo = MagicMock()
        mock_tmo.TrainModel = mock_train_model
        mock_tmo.DatasetTemplateApi = mock_dataset_template_api
        mock_tmo.EvaluateModel = MagicMock()
        mock_tmo.ScoreModel = MagicMock()
        sys.modules["tmo"] = mock_tmo

        # Mock input_select to simulate user selections
        inputs = iter(["TestModel", "score", "TestTemplate"])
        monkeypatch.setattr(
            tmo_cli,
            "input_select",
            lambda name, values, label="", default=None: next(inputs),
        )

        # Mock _select_connection
        monkeypatch.setattr(
            tmo_cli, "activate_connection", lambda args: "conn-1"  # noqa
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            def set_project_id(self, id):
                pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": str(tmp_path),
                "model_id": None,
                "mode": None,
                "dataset_id": None,
                "dataset_template_id": None,
                "local_dataset": None,
                "local_dataset_template": None,
                "connection": None,
            },
        )()

        try:
            # Execute
            tmo_cli.run_model(args, repo_manager, tmo_client)
        finally:
            # Cleanup
            if original_tmo:
                sys.modules["tmo"] = original_tmo
            else:
                del sys.modules["tmo"]

    def test_run_model_with_local_dataset(self, tmp_path, monkeypatch):
        """Test run_model with local dataset file."""
        from unittest.mock import MagicMock

        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: {"id": "proj-123"},
        )

        # Create local dataset file
        dataset_file = tmp_path / "dataset.json"
        dataset_file.write_text(json.dumps({"sql": "SELECT * FROM table"}))

        mock_train_model = MagicMock()
        mock_train_model.get_model_ids.return_value = {
            0: {"id": "model-1", "name": "TestModel"}
        }

        import sys

        original_tmo = sys.modules.get("tmo")
        mock_tmo = MagicMock()
        mock_tmo.TrainModel = mock_train_model
        mock_tmo.EvaluateModel = MagicMock()
        mock_tmo.ScoreModel = MagicMock()
        sys.modules["tmo"] = mock_tmo

        monkeypatch.setattr(
            tmo_cli,
            "input_select",
            lambda name, values, label="", default=None: (
                values[0] if values else "train"
            ),
        )
        monkeypatch.setattr(
            tmo_cli, "activate_connection", lambda args: "conn-1"  # noqa
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            def set_project_id(self, id):
                pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "model_id": "model-1",
                "mode": "train",
                "dataset_id": None,
                "dataset_template_id": None,
                "local_dataset": str(dataset_file),
                "local_dataset_template": None,
                "connection": "conn-1",
            },
        )()

        tmo_cli.run_model(args, repo_manager, tmo_client)

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_run_model_with_local_dataset_template(self, tmp_path, monkeypatch):
        """Test run_model with local dataset template file for score mode."""
        from unittest.mock import MagicMock

        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: {"id": "proj-123"},
        )

        # Create local dataset template file
        template_file = tmp_path / "template.json"
        template_file.write_text(json.dumps({"sql": "SELECT * FROM table"}))

        mock_train_model = MagicMock()
        mock_train_model.get_model_ids.return_value = {
            0: {"id": "model-1", "name": "TestModel"}
        }

        import sys

        original_tmo = sys.modules.get("tmo")
        mock_tmo = MagicMock()
        mock_tmo.TrainModel = mock_train_model
        mock_tmo.ScoreModel = MagicMock()
        sys.modules["tmo"] = mock_tmo

        monkeypatch.setattr(
            tmo_cli, "activate_connection", lambda args: "conn-1"  # noqa
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            def set_project_id(self, id):
                pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "model_id": "model-1",
                "mode": "score",
                "dataset_id": None,
                "dataset_template_id": None,
                "local_dataset": None,
                "local_dataset_template": str(template_file),
                "connection": "conn-1",
            },
        )()

        tmo_cli.run_model(args, repo_manager, tmo_client)

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_run_model_evaluate_mode(self, tmp_path, monkeypatch):
        """Test run_model in evaluate mode."""
        from unittest.mock import MagicMock

        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: {"id": "proj-123"},
        )

        dataset_file = tmp_path / "dataset.json"
        dataset_file.write_text(json.dumps({"sql": "SELECT * FROM table"}))

        mock_train_model = MagicMock()
        mock_train_model.get_model_ids.return_value = {
            0: {"id": "model-1", "name": "TestModel"}
        }

        import sys

        original_tmo = sys.modules.get("tmo")
        mock_tmo = MagicMock()
        mock_tmo.TrainModel = mock_train_model
        mock_tmo.EvaluateModel = MagicMock()
        sys.modules["tmo"] = mock_tmo

        monkeypatch.setattr(
            tmo_cli, "activate_connection", lambda args: "conn-1"  # noqa
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            def set_project_id(self, id):
                pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "model_id": "model-1",
                "mode": "evaluate",
                "dataset_id": None,
                "dataset_template_id": None,
                "local_dataset": str(dataset_file),
                "local_dataset_template": None,
                "connection": "conn-1",
            },
        )()

        tmo_cli.run_model(args, repo_manager, tmo_client)

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_run_model_invalid_mode(self, tmp_path, monkeypatch):
        """Test run_model with invalid mode prompts for selection."""
        from unittest.mock import MagicMock

        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: {"id": "proj-123"},
        )

        dataset_file = tmp_path / "dataset.json"
        dataset_file.write_text(json.dumps({"sql": "SELECT * FROM table"}))

        mock_train_model = MagicMock()
        mock_train_model.get_model_ids.return_value = {
            0: {"id": "model-1", "name": "TestModel"}
        }

        import sys

        original_tmo = sys.modules.get("tmo")
        mock_tmo = MagicMock()
        mock_tmo.TrainModel = mock_train_model
        mock_tmo.EvaluateModel = MagicMock()
        mock_tmo.ScoreModel = MagicMock()
        sys.modules["tmo"] = mock_tmo

        monkeypatch.setattr(
            tmo_cli, "activate_connection", lambda args: "conn-1"  # noqa
        )

        # Mock input_select to return a valid mode when prompted
        # (when mode is invalid, code will prompt for selection)
        monkeypatch.setattr(
            tmo_cli,
            "input_select",
            lambda name, values, label="", default=None: "train",
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            def set_project_id(self, id):
                pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "model_id": "model-1",
                "mode": "invalid_mode",  # Invalid mode triggers selection
                "dataset_id": None,
                "dataset_template_id": None,
                "local_dataset": str(dataset_file),
                "local_dataset_template": None,
                "connection": "conn-1",
            },
        )()

        try:
            # Should execute without error - invalid mode is replaced by selection
            tmo_cli.run_model(args, repo_manager, tmo_client)
        finally:
            # Cleanup
            if original_tmo:
                sys.modules["tmo"] = original_tmo
            else:
                del sys.modules["tmo"]

    def test_run_model_with_dataset_id(self, tmp_path, monkeypatch):
        """Test run_model with specific dataset_id."""
        from unittest.mock import MagicMock

        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: {"id": "proj-123"},
        )

        mock_train_model = MagicMock()
        mock_train_model.get_model_ids.return_value = {
            0: {"id": "model-1", "name": "TestModel"}
        }

        mock_dataset = MagicMock()
        mock_dataset.id = "dataset-1"
        mock_dataset.name = "TestDataset"

        mock_dataset_api = MagicMock()
        mock_dataset_api.return_value.find_by_id.return_value = mock_dataset
        mock_dataset_api.return_value.render.return_value = {"data": "test"}

        import sys

        original_tmo = sys.modules.get("tmo")
        mock_tmo = MagicMock()
        mock_tmo.TrainModel = mock_train_model
        mock_tmo.EvaluateModel = MagicMock()
        mock_tmo.DatasetApi = mock_dataset_api
        mock_tmo.DatasetTemplateApi = MagicMock()
        sys.modules["tmo"] = mock_tmo

        monkeypatch.setattr(
            tmo_cli, "activate_connection", lambda args: "conn-1"  # noqa
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            def set_project_id(self, id):
                pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "model_id": "model-1",
                "mode": "train",
                "dataset_id": "dataset-1",
                "dataset_template_id": None,
                "local_dataset": None,
                "local_dataset_template": None,
                "connection": "conn-1",
            },
        )()

        tmo_cli.run_model(args, repo_manager, tmo_client)

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_run_model_score_with_dataset_template_id(self, tmp_path, monkeypatch):
        """Test run_model in score mode with dataset_template_id."""
        from unittest.mock import MagicMock

        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: {"id": "proj-123"},
        )

        mock_train_model = MagicMock()
        mock_train_model.get_model_ids.return_value = {
            0: {"id": "model-1", "name": "TestModel"}
        }

        mock_template = MagicMock()
        mock_template.id = "template-1"
        mock_template.name = "TestTemplate"

        mock_dataset_template_api = MagicMock()
        mock_dataset_template_api.return_value.find_all.return_value = [mock_template]
        mock_dataset_template_api.return_value.find_by_id.return_value = mock_template
        mock_dataset_template_api.return_value.render.return_value = {"data": "test"}

        import sys

        original_tmo = sys.modules.get("tmo")
        mock_tmo = MagicMock()
        mock_tmo.TrainModel = mock_train_model
        mock_tmo.ScoreModel = MagicMock()
        mock_tmo.DatasetTemplateApi = mock_dataset_template_api
        sys.modules["tmo"] = mock_tmo

        monkeypatch.setattr(
            tmo_cli, "activate_connection", lambda args: "conn-1"  # noqa
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            def set_project_id(self, id):
                pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "model_id": "model-1",
                "mode": "score",
                "dataset_id": None,
                "dataset_template_id": "template-1",
                "local_dataset": None,
                "local_dataset_template": None,
                "connection": "conn-1",
            },
        )()

        tmo_cli.run_model(args, repo_manager, tmo_client)

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_run_model_model_not_found_prompts_selection(
        self, tmp_path, monkeypatch, capsys
    ):
        """Test run_model when model_id not found prompts user."""
        from unittest.mock import MagicMock

        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: {"id": "proj-123"},
        )

        dataset_file = tmp_path / "dataset.json"
        dataset_file.write_text(json.dumps({"sql": "SELECT * FROM table"}))

        mock_train_model = MagicMock()
        mock_train_model.get_model_ids.return_value = {
            0: {"id": "model-1", "name": "TestModel"}
        }

        import sys

        original_tmo = sys.modules.get("tmo")
        mock_tmo = MagicMock()
        mock_tmo.TrainModel = mock_train_model
        mock_tmo.EvaluateModel = MagicMock()
        sys.modules["tmo"] = mock_tmo

        # User selects model from prompt
        inputs = iter(["TestModel"])
        monkeypatch.setattr(
            tmo_cli,
            "input_select",
            lambda name, values, label="", default=None: next(inputs),
        )
        monkeypatch.setattr(
            tmo_cli, "activate_connection", lambda args: "conn-1"  # noqa
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            def set_project_id(self, id):
                pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "model_id": "nonexistent-model",
                "mode": "train",
                "dataset_id": None,
                "dataset_template_id": None,
                "local_dataset": str(dataset_file),
                "local_dataset_template": None,
                "connection": "conn-1",
            },
        )()

        tmo_cli.run_model(args, repo_manager, tmo_client)

        captured = capsys.readouterr()
        assert "Model not found" in captured.out

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_run_model_mode_not_found_prompts_selection(
        self, tmp_path, monkeypatch, capsys
    ):
        """Test run_model when mode not valid prompts user."""
        from unittest.mock import MagicMock

        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: {"id": "proj-123"},
        )

        dataset_file = tmp_path / "dataset.json"
        dataset_file.write_text(json.dumps({"sql": "SELECT * FROM table"}))

        mock_train_model = MagicMock()
        mock_train_model.get_model_ids.return_value = {
            0: {"id": "model-1", "name": "TestModel"}
        }

        import sys

        original_tmo = sys.modules.get("tmo")
        mock_tmo = MagicMock()
        mock_tmo.TrainModel = mock_train_model
        mock_tmo.EvaluateModel = MagicMock()
        sys.modules["tmo"] = mock_tmo

        # User selects mode from prompt
        inputs = iter(["train"])
        monkeypatch.setattr(
            tmo_cli,
            "input_select",
            lambda name, values, label="", default=None: next(inputs),
        )
        monkeypatch.setattr(
            tmo_cli, "activate_connection", lambda args: "conn-1"  # noqa
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            def set_project_id(self, id):
                pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "model_id": "model-1",
                "mode": "invalid_mode",
                "dataset_id": None,
                "dataset_template_id": None,
                "local_dataset": str(dataset_file),
                "local_dataset_template": None,
                "connection": "conn-1",
            },
        )()

        tmo_cli.run_model(args, repo_manager, tmo_client)

        captured = capsys.readouterr()
        assert "Mode not found" in captured.out

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_run_model_score_template_not_found_prompts(self, tmp_path, monkeypatch):
        """Test run_model score mode when template_id not found."""
        from unittest.mock import MagicMock

        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: {"id": "proj-123"},
        )

        mock_train_model = MagicMock()
        mock_train_model.get_model_ids.return_value = {
            0: {"id": "model-1", "name": "TestModel"}
        }

        mock_template = MagicMock()
        mock_template.id = "template-1"
        mock_template.name = "TestTemplate"

        mock_dataset_template_api = MagicMock()
        mock_dataset_template_api.return_value.find_all.return_value = [mock_template]
        mock_dataset_template_api.return_value.find_by_id.return_value = mock_template
        mock_dataset_template_api.return_value.render.return_value = {"data": "test"}

        import sys

        original_tmo = sys.modules.get("tmo")
        mock_tmo = MagicMock()
        mock_tmo.TrainModel = mock_train_model
        mock_tmo.ScoreModel = MagicMock()
        mock_tmo.DatasetTemplateApi = mock_dataset_template_api
        sys.modules["tmo"] = mock_tmo

        inputs = iter(["TestTemplate"])
        monkeypatch.setattr(
            tmo_cli,
            "input_select",
            lambda name, values, label="", default=None: next(inputs),
        )
        monkeypatch.setattr(
            tmo_cli, "activate_connection", lambda args: "conn-1"  # noqa
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            def set_project_id(self, id):
                pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "model_id": "model-1",
                "mode": "score",
                "dataset_id": None,
                "dataset_template_id": "nonexistent-template",
                "local_dataset": None,
                "local_dataset_template": None,
                "connection": "conn-1",
            },
        )()

        tmo_cli.run_model(args, repo_manager, tmo_client)

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_run_model_interactive_dataset_selection_train(self, tmp_path, monkeypatch):
        """Test run_model with interactive dataset/template selection for train mode."""
        from unittest.mock import MagicMock

        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: {"id": "proj-123"},
        )

        mock_train_model = MagicMock()
        mock_train_model.get_model_ids.return_value = {
            0: {"id": "model-1", "name": "TestModel"}
        }

        mock_dataset = MagicMock()
        mock_dataset.id = "dataset-1"
        mock_dataset.name = "TestDataset"
        mock_dataset.scope = "TRAIN"

        mock_template = MagicMock()
        mock_template.id = "template-1"
        mock_template.name = "TestTemplate"

        mock_dataset_api = MagicMock()
        mock_dataset_api.return_value.find_by_dataset_template_id.return_value = [
            mock_dataset
        ]
        mock_dataset_api.return_value.render.return_value = {"data": "test"}

        mock_dataset_template_api = MagicMock()
        mock_dataset_template_api.return_value.find_all.return_value = [mock_template]

        import sys

        original_tmo = sys.modules.get("tmo")
        mock_tmo = MagicMock()
        mock_tmo.TrainModel = mock_train_model
        mock_tmo.DatasetApi = mock_dataset_api
        mock_tmo.DatasetTemplateApi = mock_dataset_template_api
        mock_tmo.Scope = MagicMock()
        sys.modules["tmo"] = mock_tmo

        # User selections: template, dataset
        inputs = iter(["TestTemplate", "TestDataset"])
        monkeypatch.setattr(
            tmo_cli,
            "input_select",
            lambda name, values, label="", default=None: next(inputs),
        )
        monkeypatch.setattr(
            tmo_cli, "activate_connection", lambda args: "conn-1"  # noqa
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            def set_project_id(self, id):
                pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "model_id": "model-1",
                "mode": "train",
                "dataset_id": None,
                "dataset_template_id": None,
                "local_dataset": None,
                "local_dataset_template": None,
                "connection": "conn-1",
            },
        )()

        tmo_cli.run_model(args, repo_manager, tmo_client)

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]

    def test_run_model_score_interactive_template_selection(
        self, tmp_path, monkeypatch
    ):
        """Test run_model score mode with interactive template selection."""
        from unittest.mock import MagicMock

        monkeypatch.setattr(
            tmo_cli,
            "get_current_project",
            lambda rm, tc, validate: {"id": "proj-123"},
        )

        mock_train_model = MagicMock()
        mock_train_model.get_model_ids.return_value = {
            0: {"id": "model-1", "name": "TestModel"}
        }

        mock_template = MagicMock()
        mock_template.id = "template-1"
        mock_template.name = "TestTemplate"

        mock_dataset_template_api = MagicMock()
        mock_dataset_template_api.return_value.find_all.return_value = [mock_template]
        mock_dataset_template_api.return_value.render.return_value = {"data": "test"}

        import sys

        original_tmo = sys.modules.get("tmo")
        mock_tmo = MagicMock()
        mock_tmo.TrainModel = mock_train_model
        mock_tmo.ScoreModel = MagicMock()
        mock_tmo.DatasetTemplateApi = mock_dataset_template_api
        sys.modules["tmo"] = mock_tmo

        inputs = iter(["TestTemplate"])
        monkeypatch.setattr(
            tmo_cli,
            "input_select",
            lambda name, values, label="", default=None: next(inputs),
        )
        monkeypatch.setattr(
            tmo_cli, "activate_connection", lambda args: "conn-1"  # noqa
        )

        class MockRepoManager:
            pass

        class MockTmoClient:
            def set_project_id(self, id):
                pass

        repo_manager = MockRepoManager()
        tmo_client = MockTmoClient()

        args = type(
            "Args",
            (),
            {
                "cwd": None,
                "model_id": "model-1",
                "mode": "score",
                "dataset_id": None,
                "dataset_template_id": None,
                "local_dataset": None,
                "local_dataset_template": None,
                "connection": "conn-1",
            },
        )()

        tmo_cli.run_model(args, repo_manager, tmo_client)

        # Cleanup
        if original_tmo:
            sys.modules["tmo"] = original_tmo
        else:
            del sys.modules["tmo"]
