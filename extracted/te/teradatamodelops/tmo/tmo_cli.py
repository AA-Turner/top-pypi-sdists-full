#!/usr/bin/env python

import argparse
import logging
import os
import re
import sys
import traceback
from pathlib import Path

import oauthlib
import requests
import yaml

from tmo.crypto import crypto
from tmo.types.dataset import Scope
from tmo.types.entity import EntityType
from tmo.types.exceptions import (
    EntityCreationError,
    EntityNotFoundError,
    ConfigurationError,
)

os.system("")  # enables ansi escape characters in terminal

COLOR = {
    "WARN": "\033[91m",
    "END": "\033[0m",
}
CWD_MODEL_REPO_ERROR = (
    "Current working directory must the root of a model repository to execute this"
    " command"
)
CWD_FE_TASKS_REPO_ERROR = (
    "Current working directory must the root of a feature engineering task repository"
    " to execute this command"
)
CONNECTIONS_YAML_FILE = "{}/connections.yaml"
KEY_FILE = "{}/{}.key"
PASS_FILE = "{}/{}.pass"
VALID_ACTIONS_STR = "valid actions"
LOCAL_CONNECTION_ID_STR = "Local connection id"
METADATA_TABLE_HELP = "Metadata table for feature stats, including database name"
MODEL_CATALOG_PATH = "model_definitions"
FE_TASKS_CATALOG_PATH = "feature_engineering_tasks"

base_path = os.path.abspath(os.getcwd())
model_catalog = os.path.join(base_path, f"{MODEL_CATALOG_PATH}/")
fe_tasks_catalog = os.path.join(base_path, f"{FE_TASKS_CATALOG_PATH}/")
available_modes = ["Train", "Evaluate", "Score"]
config_dir = f"{Path.home()}/.tmo"
called_from_test = os.getenv("CALLED_FROM_TEST") == "true"


def validate_model_catalog_cwd_valid() -> bool:
    return os.path.exists(model_catalog) and os.path.isdir(model_catalog)


def validate_fe_tasks_cwd_valid() -> bool:
    return os.path.exists(fe_tasks_catalog) and os.path.isdir(fe_tasks_catalog)


def init_model_directory(args, repo_manager, tmo_client, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    repo_manager.init_model_directory()

    if not repo_manager.repo_config_exists():
        link_repo(repo_manager=repo_manager, tmo_client=tmo_client)


def input_string(
    name, required=False, tooltip="", password=False, is_called_from_test=False
):
    from getpass import getpass

    if tooltip != "":
        print(tooltip)

    value = (
        getpass("Enter {}: ".format(name))
        if password and not is_called_from_test
        else input("Enter {}: ".format(name))
    )

    if value == "" and required:
        print("Value required. Please try again.")
        print("You may cancel at anytime by pressing Ctrl+C")
        print("")
        return input_string(name, required, tooltip)

    return value


def input_select(name, values, label="", default=None):
    if len(values) == 0:
        return None

    if label != "":
        print_underscored(label)

    for ix, item in enumerate(values):  # noqa
        default_text = " (default)" if default and default == item else ""
        print("[{}] {}".format(ix, item) + default_text)

    tmp_index = (
        input("Select {} by index (or leave blank for the default one): ".format(name))
        if default
        else input("Select {} by index: ".format(name))
    )

    if default and default in values and tmp_index == "":
        tmp_index = values.index(default)
    elif (tmp_index == "" and not default) or (
        not tmp_index.isnumeric() or int(tmp_index) >= len(values)
    ):
        print(
            "Wrong selection, please try again by selecting the index number on the"
            " first column."
        )
        print("You may cancel at anytime by pressing Ctrl+C.")
        print("")
        return input_select(name, values, label, default)

    return values[int(tmp_index)]


def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question + " (y/n): ")).lower().strip()
        if reply.startswith("y"):
            return True
        if reply.startswith("n"):
            return False


def bash_escape(string):
    return string.replace("\\", "\\\\") if string else string


def add_model(args, repo_manager, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    if not validate_model_catalog_cwd_valid():
        logging.error(CWD_MODEL_REPO_ERROR)
        sys.exit(1)

    if not args.template_url:
        args.template_url = input_string("template url", True)

    if not args.branch:
        args.branch = input_string("branch (leave empty for main)")
    if not args.branch:
        args.branch = "main"

    import tempfile

    temp_path = tempfile.TemporaryDirectory()
    logging.info("Using this model catalog from Git repo {}".format(args.template_url))
    repo_manager.clone_repository(args.template_url, temp_path.name, args.branch)

    templates = repo_manager.get_templates(
        entity_type=EntityType.MODEL, source_path=temp_path.name
    )
    if len(templates) == 0:
        logging.error(
            "Repo doesn't contain any models to use as templates, use different repo as"
            " a model catalog"
        )
        sys.exit(1)

    print("")
    model_lang = input_select(
        "model language", list(templates.keys()), "Available languages:"
    )

    print("")
    models = {f"{v[0]} ({k})": k for k, v in templates[model_lang].items()}
    model_template = input_select(
        "model template", list(models.keys()), "Available models:"
    )
    model_template_dir = templates[model_lang][models[model_template]][1]

    model_name = input_string("model name", True)
    model_desc = input_string("model description", False)

    import uuid

    model_id = str(uuid.uuid4())

    repo_manager.add_model(
        model_id=model_id,
        model_name=model_name,
        model_desc=model_desc,
        template=model_template_dir,
        base_path=base_path,
    )
    print(f"Creating folder structure for model: {model_name} ({model_id})")


def run_model(args, repo_manager, tmo_client, **kwargs):  # noqa
    from tmo import (
        TrainModel,
        EvaluateModel,
        ScoreModel,
        DatasetApi,
        DatasetTemplateApi,
    )
    import json

    if args.cwd:
        set_cwd(args.cwd)

    current_project = get_current_project(repo_manager, tmo_client, True)
    if not current_project:
        logging.error(CWD_MODEL_REPO_ERROR)
        sys.exit(1)

    tmo_client.set_project_id(current_project["id"])

    def _select_model_id(catalog):
        catalog_values = [catalog[i]["name"] for i in catalog]
        selected_model_value = input_select(
            "model", catalog_values, "Available models:"
        )
        selected_model = next(
            (catalog[i] for i in catalog if catalog[i]["name"] == selected_model_value),
            None,
        )
        print("")
        return selected_model["id"] if "id" in selected_model else None

    def _select_mode():
        selected_mode = input_select(
            "mode", available_modes, "Available modes:"
        ).lower()
        print("")
        return selected_mode

    def _select_dataset(dataset_list=None, scope=None):
        if dataset_list is None:
            dataset_list = dataset_api.find_by_dataset_template_id(
                template.id,
                archived=False,
            )
        if scope is not None:
            dataset_list = [i for i in dataset_list if i.scope == Scope(scope)]

        dataset_values = [i.name for i in dataset_list]
        selected_dataset_value = input_select(
            ("" if scope is None else scope + " ") + "dataset",
            dataset_values,
            "Available " + ("" if scope is None else scope + " ") + "datasets:",
        )
        selected_dataset = next(
            (i for i in dataset_list if i.name == selected_dataset_value),
            None,
        )
        print("")
        return selected_dataset

    def _select_dataset_template(template_list):
        template_values = [i.name for i in template_list]
        selected_template_value = input_select(
            "dataset template", template_values, "Available dataset templates:"
        )
        selected_template = next(
            (i for i in template_list if i.name == selected_template_value), None
        )
        print("")
        return selected_template

    def _select_connection(connection=None):
        from argparse import Namespace

        return activate_connection(Namespace(cwd=None, connection=connection))

    def _select_dataset_template_and_dataset(template_api_obj, scope=None):
        _available_templates = template_api_obj.find_all()
        _template = _select_dataset_template(_available_templates)
        if not _template:
            logging.error("No dataset template found in project")
            sys.exit(1)

        available_datasets = dataset_api.find_by_dataset_template_id(_template.id)

        _dataset = _select_dataset(available_datasets, scope)
        if not _dataset:
            logging.error(
                "No "
                + ("" if scope is None else scope + " ")
                + "datasets found in project"
            )
            sys.exit(1)
        return _dataset, _template

    available_models = TrainModel.get_model_ids(model_catalog, True)
    dataset_id = None
    dataset_template_id = None

    if len(available_models) == 0:
        logging.error("No models found in local model catalog, please add them first.")
        sys.exit(1)

    if not args.model_id:
        model_id = _select_model_id(available_models)
    else:
        model_id_exists = next(
            (
                available_models[i]
                for i in available_models
                if available_models[i]["id"] == args.model_id
            ),
            False,
        )
        if not model_id_exists:
            print(
                "Model not found. Please select one from the list below or press Ctrl+C"
                " to quit."
            )
        model_id = (
            args.model_id if model_id_exists else _select_model_id(available_models)
        )

    if not args.mode:
        mode = _select_mode()

    else:
        mode_exists = (
            True if args.mode in [x.lower() for x in available_modes] else False
        )
        if not mode_exists:
            print(
                "Mode not found. Please select one from the list below or press Ctrl+C"
                " to quit."
            )
        mode = args.mode if mode_exists else _select_mode()

    if args.local_dataset:
        with open(args.local_dataset, "r") as f:
            rendered_dataset = json.load(f)

    elif args.local_dataset_template:
        with open(args.local_dataset_template, "r") as f:
            rendered_dataset = json.load(f)

    else:
        if mode == "score":
            dataset_template_api = DatasetTemplateApi(
                tmo_client=tmo_client, show_archived=False
            )

            available_templates = dataset_template_api.find_all()
            template = None
            if not args.local_dataset_template and not args.dataset_template_id:
                template = _select_dataset_template(available_templates)
                if not template:
                    logging.error("No dataset templates found in project")
                    sys.exit(1)

            elif args.dataset_template_id:
                template_exists = next(
                    (
                        True
                        for i in available_templates
                        if str(i.id) == args.dataset_template_id
                    ),
                    False,
                )
                if not template_exists:
                    print(
                        "Dataset template not found. Please select one from the list"
                        " below or press Ctrl+C to quit."
                    )
                template = (
                    dataset_template_api.find_by_id(args.dataset_template_id)
                    if template_exists
                    else _select_dataset_template(available_templates)
                )

            dataset_template_id = template.id

            rendered_dataset = dataset_template_api.render(id=dataset_template_id)

        else:
            template_api = DatasetTemplateApi(
                tmo_client=tmo_client, show_archived=False
            )
            dataset_api = DatasetApi(tmo_client=tmo_client, show_archived=False)
            dataset = None

            if not args.local_dataset and not args.dataset_id:
                dataset, template = _select_dataset_template_and_dataset(template_api)

            elif args.dataset_id:
                dataset = dataset_api.find_by_id(args.dataset_id)
                if not dataset:
                    print(
                        "Dataset not found. Please select one from the list below or"
                        " press Ctrl+C to quit."
                    )
                    dataset, template = _select_dataset_template_and_dataset(
                        template_api, mode
                    )

            dataset_id = dataset.id if hasattr(dataset, "id") else dataset.get("id")

            rendered_dataset = dataset_api.render(dataset_id)

    connection_id = _select_connection(args.connection if args.connection else None)

    print("")
    print("To execute the same command again run:")
    if mode != "score":
        if args.local_dataset:
            print(
                f"tmo run -m {mode} -id {model_id} -c {connection_id} -ld"
                f" {args.local_dataset}"
            )
        else:
            print(
                f"tmo run -m {mode} -id {model_id} -d {dataset_id} -c {connection_id}"
            )
    else:
        if args.local_dataset_template:
            print(
                f"tmo run -m {mode} -id {model_id} -c {connection_id} -lt"
                f" {args.local_dataset_template}"
            )
        else:
            print(
                f"tmo run -m {mode} -id {model_id} -t {dataset_template_id} -c"
                f" {connection_id}"
            )
    print("")
    print("")

    if mode == "train":
        trainer = TrainModel(repo_manager)
        trainer.train_model_local(
            model_id, rendered_dataset=rendered_dataset, base_path=base_path
        )
    elif mode == "evaluate":
        evaluator = EvaluateModel(repo_manager)
        evaluator.evaluate_model_local(
            model_id, rendered_dataset=rendered_dataset, base_path=base_path
        )
    elif mode == "score":
        scorer = ScoreModel(repo_manager)
        scorer.batch_score_model_local(
            model_id, rendered_dataset=rendered_dataset, base_path=base_path
        )
    else:
        logging.error(f"Unsupported mode used: {mode}")
        sys.exit(1)


def add_task(args, repo_manager, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    if not validate_fe_tasks_cwd_valid():
        logging.error(CWD_FE_TASKS_REPO_ERROR)
        sys.exit(1)

    if not args.template_url:
        args.template_url = input_string("template url", True)

    if not args.branch:
        args.branch = input_string("branch (leave empty for main)")
    if not args.branch:
        args.branch = "main"

    import tempfile

    temp_path = tempfile.TemporaryDirectory()
    logging.info("Using this catalog from Git repo {}".format(args.template_url))
    repo_manager.clone_repository(args.template_url, temp_path.name, args.branch)

    templates = repo_manager.get_templates(
        entity_type=EntityType.FEATURE_ENGINEERING_TASK, source_path=temp_path.name
    )

    if len(templates) == 0:
        logging.error(
            "Repo doesn't contain any valid tasks, use different repo as a feature"
            " engineering task catalog"
        )
        sys.exit(1)

    print("")

    tasks = {f"{k}": k for k, v in templates.items()}
    task_template = input_select(
        "task template", list(tasks.keys()), "Available tasks:"
    )
    print("")

    if not args.name or args.name == "":
        args.name = input_string(f"task name (leave empty for {task_template})")
    if not args.name:
        args.name = task_template

    repo_manager.add_task(
        template=templates[task_template], task_name=args.name, base_path=base_path
    )
    print(f"Creating folder structure for task: {args.name}")


def run_task(args, repo_manager, tmo_client, **kwargs):  # noqa
    from tmo import RunTask

    if args.cwd:
        set_cwd(args.cwd)

    current_project = get_current_project(repo_manager, tmo_client, True)
    if not current_project:
        logging.error(CWD_MODEL_REPO_ERROR)
        sys.exit(1)

    tmo_client.set_project_id(current_project["id"])

    def _select_connection(connection=None):
        from argparse import Namespace

        return activate_connection(Namespace(cwd=None, connection=connection))

    connection_id = _select_connection(args.connection if args.connection else None)

    runner = RunTask(repo_manager)

    task_name, func_name = runner.run_task_local(
        base_path=base_path, task_name=args.name, func=args.function_name
    )

    print("")
    print("To execute the same command again run:")
    print(f"tmo task run -n {task_name} -c {connection_id} -f {func_name}")
    print("")
    print("")


def _get_project_for_listing(repo_manager, tmo_client):
    """Get current project or select one, and set project ID in tmo_client."""
    project = get_current_project(repo_manager, tmo_client)
    if project:
        tmo_client.set_project_id(project["id"])
    else:
        project = list_and_select_projects(repo_manager, tmo_client, False, True)
    return project


def _list_remote_models(project, tmo_client):
    """List remote models for a project."""
    from tmo import ModelApi

    model_api = ModelApi(tmo_client, show_archived=False)
    print_underscored("List of models for project {}:".format(project["name"]))
    if len(model_api) <= 0:
        print("No models were found")
    for i, model in enumerate(model_api):  # noqa
        print(
            "[{}] Id: ({}) Type: ({}) {}".format(
                i, model["id"], model["source"], model["name"]  # noqa
            )
        )


def _list_local_models():
    """List local models from the catalog."""
    from tmo import TrainModel

    local_models = TrainModel.get_model_folders(model_catalog, True)
    print_underscored("List of local models:")
    if len(local_models) <= 0:
        print("No local models were found")
    for local_model in local_models:
        print(
            "[{}] {} (Git: {})".format(
                local_model,
                local_models[local_model]["name"],
                local_models[local_model]["id"],
            )
        )


def _list_dataset_templates(project, tmo_client):
    """List dataset templates for a project."""
    from tmo import DatasetTemplateApi

    template_api = DatasetTemplateApi(tmo_client=tmo_client, show_archived=False)
    print_underscored(f"List of dataset templates for project {project['name']}:")
    if len(template_api.find_all()) <= 0:
        print("No dataset templates were found")
    for i, template in enumerate(template_api.find_all()):
        print(f"[{i}] ({template.id}) {template.name}")


def _list_datasets(project, tmo_client):
    """List datasets for a project."""
    from tmo import DatasetApi

    dataset_api = DatasetApi(tmo_client=tmo_client, show_archived=False)
    print_underscored(f"List of datasets for project {project['name']}:")
    if len(dataset_api.find_all()) <= 0:
        print("No datasets were found")
    for i, dataset in enumerate(dataset_api.find_all()):
        print(f"[{i}] ({dataset.id}) {dataset.name}")


def _check_if_any_resource_selected(args):
    """Check if any resource option was selected."""
    return (
        args.projects
        or args.models
        or args.local_models
        or args.templates
        or args.datasets
        or args.connections
    )


def list_resources(args, repo_manager, tmo_client, **kwargs):
    if args.cwd:
        set_cwd(args.cwd)

    if args.projects:
        list_and_select_projects(repo_manager, tmo_client, True, False)
        sys.exit(0)

    if args.models:
        project = _get_project_for_listing(repo_manager, tmo_client)
        _list_remote_models(project, tmo_client)

    if args.local_models:
        _list_local_models()

    if args.templates:
        project = _get_project_for_listing(repo_manager, tmo_client)
        _list_dataset_templates(project, tmo_client)

    if args.datasets:
        project = _get_project_for_listing(repo_manager, tmo_client)
        _list_datasets(project, tmo_client)

    if args.connections:
        from argparse import Namespace

        list_connections(Namespace(cwd=None, connections=None))

    elif not _check_if_any_resource_selected(args):
        logging.error("Invalid object selection...")
        kwargs.get("parent_parser").print_help()
        sys.exit(1)


def clone(args, repo_manager, tmo_client, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    if not args.project_id:
        project = list_and_select_projects(repo_manager, tmo_client, False, True)
    else:
        from tmo import ProjectApi

        project_api = ProjectApi(tmo_client=tmo_client, show_archived=False)
        try:
            project = project_api.find_by_id(args.project_id)
        except Exception:  # noqa
            project = None
        if not project:
            print(
                "Project not found. Please select one from the list below or press"
                " Ctrl+C to quit."
            )
            project = list_and_select_projects(repo_manager, tmo_client, False, True)

    if args.path:
        path = args.path
    else:
        path = os.path.join(base_path, project["name"])

    project_git = project["gitRepositoryUrl"]

    repo_manager.clone_repository(
        project_git, path, project.get("branch", "master") if project else "master"
    )

    config = {"project_id": project["id"]}
    repo_manager.write_repo_config(config, path)
    print("Project cloned at {}".format(path))


def list_connections(args, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    try:
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        connections_file = f"{config_dir}/connections.yaml"
        with open(connections_file, "r") as f:
            connections = yaml.safe_load(f)
    except:  # noqa
        logging.error("No connections file found. Please add them first.")
        sys.exit(1)

    if "connections" in connections and len(connections["connections"]) > 0:
        print_underscored("List of local connections:")
        for i, connection in enumerate(connections["connections"]):
            print(
                "[{}] ({}) Name: {} Username: {} Host: {} Database: {}".format(
                    i,
                    connection["id"],
                    connection["name"],
                    connection["username"],
                    connection["host"],
                    connection.get("database", ""),
                )
            )
    else:
        logging.error("No connections found in file. Please add them first.")


def add_connections(args, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    try:
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        connections_file = CONNECTIONS_YAML_FILE.format(config_dir)
        with open(connections_file, "r") as f:
            connections_dict = yaml.safe_load(f)
            if connections_dict is None:
                connections_dict = {}
    except:  # noqa
        logging.info("No connections file found, creating new one...")
        connections_dict = {}

    connections = (
        connections_dict["connections"]
        if connections_dict
        and "connections" in connections_dict
        and len(connections_dict["connections"]) > 0
        else []
    )

    if args.name and args.username and args.password and args.host:
        name = args.name
        username = args.username
        password = args.password
        host = args.host
        database = args.database
        val_db = args.val_db
        byom_db = args.byom_db
        logmech = args.logmech

    elif not (args.username or args.password or args.name or args.host):
        name = input_string(name="name", tooltip="Type the connection name")
        username = input_string(name="username", tooltip="Type the connection username")
        password = input_string(
            name="password",
            tooltip="Type the connection password (will be redacted)",
            password=True,
            is_called_from_test=called_from_test,
        )
        host = input_string(name="host", tooltip="Type the connection host")
        byom_db = input_string(
            name="BYOM database", required=True, tooltip="The BYOM installation to use"
        )
        val_db = input_string(
            name="VAL database ", required=True, tooltip="The VAL installation to use"
        )
        database = input_string(
            name="database",
            required=False,
            tooltip="Type the default database (optional)",
        )
        logmech = input_string(
            name="logmech", tooltip="The Logmech to use (TD2, LDAP or TDNEGO)"
        )

    else:
        logging.error("Invalid arguments...")
        args.parent_parser.print_help()
        sys.exit(1)

    import uuid

    connection_id = str(uuid.uuid4())
    encrypted_password = crypto.td_encrypt_password(
        password=password,
        pass_key_filename=KEY_FILE.format(config_dir, connection_id),
        enc_pass_filename=PASS_FILE.format(config_dir, connection_id),
    )

    connections.append({
        "id": connection_id,
        "name": name,
        "username": username,
        "password": encrypted_password,
        "host": host,
        "logmech": logmech,
        "database": database,
        "val_db": val_db,
        "byom_db": byom_db,
    })
    connections_dict["connections"] = connections  # noqa

    try:
        connections_file = CONNECTIONS_YAML_FILE.format(config_dir)
        with open(connections_file, "w+") as f:
            yaml.safe_dump(connections_dict, f, default_flow_style=False)
    except Exception as ex:
        logging.error("Can't save connections file: {}".format(ex))
        sys.exit(1)


def remove_connections(args, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    def _remove_connection(id, obj):
        if os.path.exists(KEY_FILE.format(config_dir, id)):
            os.remove(KEY_FILE.format(config_dir, id))
        if os.path.exists(PASS_FILE.format(config_dir, id)):
            os.remove(PASS_FILE.format(config_dir, id))
        result = []
        for item in obj:
            if item["id"] != id:
                result.append(item)
        return result

    try:
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        connections_file = CONNECTIONS_YAML_FILE.format(config_dir)
        with open(connections_file, "r") as f:
            connections_dict = yaml.safe_load(f)
            if connections_dict is None or not (
                "connections" in connections_dict
                and len(connections_dict["connections"]) > 0
            ):
                logging.info("No connections defined, nothing to remove.")
    except:  # noqa
        logging.info("No connections file found, nothing to remove.")
        sys.exit(0)

    connections = (
        connections_dict["connections"]
        if "connections" in connections_dict
        and len(connections_dict["connections"]) > 0
        else []
    )

    if args.connection:
        _id = args.connection
        if not _check_connection_exists(_id, connections):
            logging.info("Connection does not exists, exiting.")
            sys.exit(1)
        connection = _id
    else:
        name = input_select(
            "connection",
            [item["name"] for item in connections],
            "List of local connections",
        )
        connection = next(
            (
                connections[i]["id"]
                for i, item in enumerate(connections)
                if connections[i]["name"] == name
            ),
            None,
        )

    connections = _remove_connection(connection, connections)
    connections_dict["connections"] = connections  # noqa

    try:
        connections_file = CONNECTIONS_YAML_FILE.format(config_dir)
        with open(connections_file, "w+") as f:
            yaml.safe_dump(connections_dict, f, default_flow_style=False)
    except Exception as ex:
        logging.error("Can't save connections file: {}".format(ex))
        sys.exit(1)


def export_connection(args, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    try:
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        connections_file = CONNECTIONS_YAML_FILE.format(config_dir)
        with open(connections_file, "r") as f:
            connections_dict = yaml.safe_load(f)
            if connections_dict is None or not (
                "connections" in connections_dict
                and len(connections_dict["connections"]) > 0
            ):
                logging.info("No connections defined, please add them first.")
    except:  # noqa
        logging.info("No connections file found, please add them first.")
        sys.exit(0)

    connections = (
        connections_dict["connections"]
        if "connections" in connections_dict
        and len(connections_dict["connections"]) > 0
        else []
    )
    if args.connection:
        _id = args.connection
        if not _check_connection_exists(_id, connections):
            logging.info("Connection does not exists, exiting.")
            sys.exit(1)
        connection = next(
            (conn for conn in connections if conn["id"] == _id),
            None,
        )
    else:
        name = input_select(
            "connection",
            [item["name"] for item in connections],
            "List of local connections",
        )
        connection = next(
            (
                connections[i]
                for i, item in enumerate(connections)
                if connections[i]["name"] == name
            ),
            None,
        )

    print("\nCopy the below command and execute in your terminal: \n")
    print(
        'export VMO_CONN_USERNAME="{}" && \\\n'.format(
            bash_escape(connection["username"])
        )
        + 'export VMO_CONN_PASSWORD="{}" && \\\n'.format(
            bash_escape(connection["password"])
        )
        + 'export VMO_CONN_HOST="{}" && \\\n'.format(bash_escape(connection["host"]))
        + 'export VMO_CONN_LOG_MECH="{}" && \\\n'.format(
            bash_escape(connection["logmech"])
        )
        + 'export VMO_CONN_DATABASE="{}" && \\\n'.format(
            bash_escape(connection.get("database", "") if connection else "")
        )
        + 'export VMO_VAL_INSTALL_DB="{}" && \\\n'.format(
            bash_escape(connection.get("val_db", "VAL") if connection else "VAL")
        )
        + 'export VMO_BYOM_INSTALL_DB="{}" && \\\n'.format(
            bash_escape(connection.get("byom_db", "BYOM") if connection else "BYOM")
        )
    )


def _check_connection_exists(connection_id, connections_list):
    """Check if a connection ID exists in the connections list."""
    for connection in connections_list:
        if "id" in connection and connection["id"] == connection_id:
            return True
    return False


def _select_connection_from_list(connections_list):
    """Select a connection from the list interactively or automatically."""
    if len(connections_list) == 1:
        print(
            "Automatic connection selection as only one available: {}".format(
                connections_list[0]["name"]
            )
        )
        return connections_list[0]["id"]

    selected_connection_value = input_select(
        "connection",
        [item["name"] for item in connections_list],
        "Available connections:",
    )
    connection_id = next(
        (
            connections_list[i]["id"]
            for i, item in enumerate(connections_list)
            if connections_list[i]["name"] == selected_connection_value
        ),
        None,
    )
    return connection_id


def _set_connection_env_vars(connection_id, connections_list):
    """Set environment variables for the specified connection."""
    for connection in connections_list:
        if "id" in connection and connection["id"] == connection_id:
            os.environ["VMO_CONN_USERNAME"] = connection["username"]
            os.environ["VMO_CONN_PASSWORD"] = connection["password"]
            os.environ["VMO_CONN_HOST"] = connection["host"]
            os.environ["VMO_CONN_LOG_MECH"] = connection["logmech"]
            os.environ["VMO_CONN_DATABASE"] = connection.get("database", "")
            os.environ["VMO_VAL_INSTALL_DB"] = connection.get("val_db", "VAL")
            os.environ["VMO_BYOM_INSTALL_DB"] = connection.get("ml_db", "MLDB")
            return True
    return False


def _load_connections_from_file():
    """Load connections dictionary from YAML file."""
    try:
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        connections_file = CONNECTIONS_YAML_FILE.format(config_dir)
        with open(connections_file, "r") as f:
            connections_dict = yaml.safe_load(f)
            if connections_dict is None:
                connections_dict = {}
        return connections_dict
    except:  # noqa
        logging.info("No connections file found, you must create a connection first.")
        sys.exit(1)


def _get_connections_list(connections_dict):
    """Extract connections list from connections dictionary."""
    return (
        connections_dict["connections"]
        if "connections" in connections_dict
        and len(connections_dict["connections"]) > 0
        else []
    )


def _determine_connection_id(args, kwargs, connections_list):
    """Determine which connection ID to use based on args and kwargs."""
    if args.connection and _check_connection_exists(args.connection, connections_list):
        return args.connection
    elif kwargs.get("connection") and _check_connection_exists(
        kwargs.get("connection"), connections_list
    ):
        return kwargs.get("connection")
    else:
        return _select_connection_from_list(connections_list)


def activate_connection(args, **kwargs):
    if args.cwd:
        set_cwd(args.cwd)

    # Load connections from file
    connections_dict = _load_connections_from_file()
    connections = _get_connections_list(connections_dict)

    # Determine which connection to activate
    connection_id = _determine_connection_id(args, kwargs, connections)

    # Activate the connection
    if _check_connection_exists(connection_id, connections):
        _set_connection_env_vars(connection_id, connections)
    else:
        logging.error("The specified connection was not found.")
        sys.exit(1)

    return connection_id


def test_connection(args, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    def _test_connection():
        from tmo import tmo_create_context, execute_sql

        tmo_create_context()
        test_query = "SEL infodata FROM dbc.dbcinfo WHERE infokey = 'VERSION'"
        logging.debug(test_query)
        result = execute_sql(test_query).fetchall()
        return result[0][0]

    from argparse import Namespace

    activate_connection(
        Namespace(cwd=None, connection=args.connection if args.connection else None)
    )

    try:
        ver = _test_connection()
        print("Connection successful, Vantage version: {}".format(ver))
    except Exception as ex:
        logging.error("Failed to test connection: {}".format(ex))
        logging.error("Please use 'tmo connection add' to add working connection")
        sys.exit(1)


def create_byom_table(args, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    from tmo.stats import store
    from tmo import execute_sql

    ct_query = store.byom_query.format(args.name)
    print(ct_query)

    if args.execute_ddl:
        from argparse import Namespace

        activate_connection(Namespace(cwd=None, connection=None))
        from tmo import tmo_create_context

        try:
            tmo_create_context()
            logging.debug(ct_query)
            execute_sql(ct_query)
        except Exception as ex:
            raise EntityCreationError(
                "Could not create BYOM table: {}".format(ex)
            ) from ex

        print("BYOM table {} created successfully".format(args.name))
    else:
        print(
            "Execution not requested, just showing DDL. To execute this DDL, add -e to"
            " the command."
        )


def compute_stats(args, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    from argparse import Namespace

    activate_connection(Namespace(cwd=None, connection=None))

    from tmo import tmo_create_context
    from tmo.stats import stats, store
    from teradataml import DataFrame, configure

    try:
        tmo_create_context()

        if args.temp_view_database:
            configure.temp_view_database = args.temp_view_database

        df = DataFrame.from_query(f"SELECT * FROM {args.source_table}")

        columns = list(map(str.strip, map(str.lower, args.columns.split(","))))  # noqa
        if args.feature_type == "categorical":
            fs = stats.compute_categorical_stats(df, columns)
            store.save_feature_stats(
                features_table=args.metadata_table, feature_type="categorical", stats=fs
            )

        elif args.feature_type == "continuous":
            fs = stats.compute_continuous_stats(df, columns)
            store.save_feature_stats(
                features_table=args.metadata_table, feature_type="continuous", stats=fs
            )
    except Exception as ex:
        raise RuntimeError("Could not compute feature stats: {}".format(ex)) from ex

    logging.info("Statistics computed successfully")


def list_stats(args, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    from argparse import Namespace

    activate_connection(Namespace(cwd=None, connection=None))
    from tmo import tmo_create_context
    from tmo.stats import store

    try:
        tmo_create_context()
        stats_summary = store.get_feature_stats_summary(args.metadata_table)
        logging.debug(stats_summary)

        if len(stats_summary) == 0:
            raise RuntimeError(
                "No statistics stored in the table {}".format(args.metadata_table)
            )

        width = len(max(list(stats_summary.keys()), key=len))
        print_underscored("List of stored feature stats:")
        for v in stats_summary:
            print(
                "{feature: <{width}} | {type}".format(
                    feature=v, width=width, type=stats_summary[v]
                )
            )
    except Exception as ex:
        raise RuntimeError("Could not list feature stats: {}".format(ex)) from ex


def create_stats_table(args, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)

    from tmo.stats.store import get_features_stats_metadata_ct_query
    from tmo import execute_sql

    ct_query = get_features_stats_metadata_ct_query(args.metadata_table)
    print(ct_query)

    if args.execute_ddl:
        from argparse import Namespace

        activate_connection(Namespace(cwd=None, connection=None))
        from tmo import tmo_create_context

        try:
            tmo_create_context()
            logging.debug(ct_query)
            execute_sql(ct_query)
        except Exception as ex:
            raise RuntimeError("Could not create statistics: {}".format(ex)) from ex

        print("Statistics table {} created successfully".format(args.metadata_table))
    else:
        print(
            "Execution not requested, just showing DDL. To execute this DDL, add -e to"
            " the command."
        )


def import_stats(args, **kwargs):  # noqa
    if args.cwd:
        set_cwd(args.cwd)
    if args.show_example:
        print("""
            {
                "age": {
                    "type": "continuous",
                    "edges": [21.0, 27.0, 33.0, 39.0, 45.0, 51.0, 57.0, 63.0, 69.0, 75.0, 81.0]
                }, 
                "hasdiabetes": {
                    "type": "categorical",
                    "frequencies": ["0", "1"]
                }
            }
        """)
        sys.exit(0)

    from argparse import Namespace

    activate_connection(Namespace(cwd=None, connection=None))
    from tmo import tmo_create_context
    from tmo.stats import store
    import json

    try:
        tmo_create_context()
        json_file = open(args.statistics_file)
        stats = json.load(json_file)

        categorical_features = {
            x: stats["features"][x]
            for x in stats["features"]
            if stats["features"][x]["type"] == "categorical"
        }
        store.save_feature_stats(
            args.metadata_table, "categorical", categorical_features
        )
        continuous_features = {
            x: stats["features"][x]
            for x in stats["features"]
            if stats["features"][x]["type"] == "continuous"
        }
        store.save_feature_stats(args.metadata_table, "continuous", continuous_features)

    except Exception as ex:
        raise RuntimeError("Could not list feature stats: {}".format(ex)) from ex

    print(
        "Successfully saved statistics in {} features table".format(args.metadata_table)
    )


def doctor(args, repo_manager, tmo_client, **kwargs):  # noqa
    print("Testing ModelOps service configuration")

    from tmo import ProjectApi

    try:
        project_api = ProjectApi(tmo_client=tmo_client, show_archived=False)
        projects = list(project_api)  # noqa
        if len(projects) > 0:
            print(f"ModelOps service configured, number of projects: {len(projects)}")
        else:
            raise EntityNotFoundError("No projects found")
    except ConfigurationError:
        logging.error(
            "Failed to connect to ModelOps or find any project. \n"
            + "Please (re)copy the CLI configuration from ModelOps UI -> Session"
            " Details -> CLI Config"
        )

    print("")

    print("Testing Vantage connections")
    args.connection = None
    test_connection(args)


def set_cwd(path):
    import os

    if not os.path.exists(path):
        logging.error("The specified path does not exist... exiting")
        sys.exit(1)
    os.chdir(path)
    global base_path, model_catalog, fe_tasks_catalog
    base_path = os.path.abspath(os.getcwd())
    model_catalog = os.path.join(base_path, f"{MODEL_CATALOG_PATH}/")
    fe_tasks_catalog = os.path.join(base_path, f"{FE_TASKS_CATALOG_PATH}/")


def print_help(args, **kwargs):
    from tmo import __version__

    if args.version:
        print("{}".format(__version__))
    else:
        kwargs.get("parent_parser").print_help()


def print_underscored(message):
    print(message)
    print("-" * len(message))


def _print_projects_list(projects, as_list):
    """Print the list of projects."""
    print_underscored("List of projects:" if as_list else "Available projects:")
    if len(projects) <= 0:
        print("No projects were found")
    for ix, item in enumerate(projects):
        print("[{}] ({}) {}".format(ix, item["id"], item["name"]))


def _find_current_project_index(projects, current_project):
    """Find the index of the current project in the projects list."""
    if not current_project:
        return "none"

    for ix, item in enumerate(projects):
        if "id" in current_project and current_project["id"] == item["id"]:
            return ix
    return "none"


def _validate_project_selection(tmp_index, projects, current_index):
    """Validate if the selected project index is valid."""
    if (
        (not tmp_index.isnumeric() or int(tmp_index) >= len(projects))
        and tmp_index != ""
    ) or (tmp_index == "" and current_index == "none"):
        return False
    return True


def list_and_select_projects(
    repo_manager, tmo_client, as_list=False, check_config=False
):
    from tmo import ProjectApi

    project_api = ProjectApi(tmo_client=tmo_client, show_archived=False)
    projects = list(project_api)  # noqa

    _print_projects_list(projects, as_list)

    if as_list:
        return None

    current_project = get_current_project(repo_manager, tmo_client, check_config)
    current_index = _find_current_project_index(projects, current_project)

    tmp_index = input(
        "Select project by index (current selection: {}): ".format(current_index)
    )
    print("")

    if not _validate_project_selection(tmp_index, projects, current_index):
        print(
            "Wrong selection, please try again by selecting the index number on the"
            " first column."
        )
        print("")
        return list_and_select_projects(repo_manager, tmo_client, as_list, check_config)

    if tmp_index == "":
        tmp_index = current_index

    selected_project = projects[int(tmp_index)]

    if tmo_client:
        tmo_client.set_project_id(selected_project["id"])

    return selected_project


def get_current_project(repo_manager, tmo_client, check_repo_conf=False):
    from tmo import ProjectApi

    if not validate_model_catalog_cwd_valid():
        return None

    repo_conf = repo_manager.read_repo_config()
    current_project_id = (
        repo_conf["project_id"] if repo_conf and "project_id" in repo_conf else ""
    )
    project_api = ProjectApi(tmo_client=tmo_client, show_archived=False)
    current_project = project_api.find_by_id(current_project_id)

    if current_project:
        return current_project
    elif not current_project and check_repo_conf:
        print("The repository is not linked to a ModelOps project.")
        print("Please execute 'tmo link'")
        print("")

    return None


def link_repo(repo_manager, tmo_client, **kwargs):  # noqa
    current_project = list_and_select_projects(repo_manager, tmo_client, False, False)
    config = {"project_id": current_project["id"]}
    repo_manager.write_repo_config(config)
    print("Repo linked to Project.")


def handle_generic_error(ex: Exception, debug: bool):
    if debug:
        logging.exception("An error occurred, printing stack trace output.")
    else:
        logging.error("An error occurred: {}".format(ex))
        sys.exit(1)


def _handle_invalid_grant_error(ge, args, remove_token_func):
    """Handle OAuth InvalidGrantError exception."""
    if ge.description in ["Token is not active", "Session not active"]:
        logging.error(
            ge.description
            + "\n"
            + COLOR["WARN"]
            + "Clearing the token cache. Please re-run cmd and login again."
            + COLOR["END"]
            + "\n"
        )
        remove_token_func()
        sys.exit(1)
    else:
        handle_generic_error(ge, args.debug)


def main():
    def __remove_cached_token():
        if os.path.exists(TmoClient.DEFAULT_TOKEN_CACHE_FILE_PATH):
            os.remove(TmoClient.DEFAULT_TOKEN_CACHE_FILE_PATH)

    args = None
    try:
        parent_parser = argparse.ArgumentParser(description="TMO CLI")
        parent_parser.add_argument(
            "--debug", action="store_true", help="Enable debug logging"
        )
        parent_parser.add_argument(
            "--version", action="store_true", help="Display the version of this tool"
        )
        parent_parser.set_defaults(func=print_help)

        subparsers = parent_parser.add_subparsers(
            title="actions", description=VALID_ACTIONS_STR, dest="command"
        )

        common_parser = argparse.ArgumentParser(add_help=False)
        common_parser.add_argument(
            "--debug", action="store_true", help="Enable debug logging"
        )
        common_parser.add_argument("-cwd", "--cwd", type=str, help=argparse.SUPPRESS)
        common_parser.add_argument(
            "--test", action="store_true", help=argparse.SUPPRESS
        )

        parser_list = subparsers.add_parser(
            "list",
            help="List projects, models, local models or datasets",
            parents=[common_parser],
        )
        parser_list.add_argument(
            "-p", "--projects", action="store_true", help="List projects"
        )
        parser_list.add_argument(
            "-m",
            "--models",
            action="store_true",
            help="List registered models (committed / pushed)",
        )
        parser_list.add_argument(
            "-lm",
            "--local-models",
            action="store_true",
            help=(
                "List local models. Includes registered and non-registered"
                " (non-committed / non-pushed)"
            ),
        )
        parser_list.add_argument(
            "-t", "--templates", action="store_true", help="List dataset templates"
        )
        parser_list.add_argument(
            "-d", "--datasets", action="store_true", help="List datasets"
        )
        parser_list.add_argument(
            "-c", "--connections", action="store_true", help="List local connections"
        )
        parser_list.set_defaults(func=list_resources)

        parser_add = subparsers.add_parser(
            "add", help="Add model to working dir", parents=[common_parser]
        )
        parser_add.add_argument(
            "-t",
            "--template-url",
            type=str,
            help="Git URL for template repository",
        )
        parser_add.add_argument(
            "-b",
            "--branch",
            type=str,
            help="Git branch to pull templates (default is main)",
        )
        parser_add.set_defaults(func=add_model)

        parser_run = subparsers.add_parser(
            "run", help="Train and Evaluate model locally", parents=[common_parser]
        )
        parser_run.add_argument("-id", "--model-id", type=str, help="Id of model")
        parser_run.add_argument(
            "-m", "--mode", type=str, help="Mode (train or evaluate)"
        )
        parser_run.add_argument("-d", "--dataset-id", type=str, help="Remote datasetId")
        parser_run.add_argument(
            "-t", "--dataset-template-id", type=str, help="Remote datasetTemplateId"
        )
        parser_run.add_argument(
            "-ld",
            "--local-dataset",
            type=str,
            help="Path to local dataset metadata file",
        )
        parser_run.add_argument(
            "-lt",
            "--local-dataset-template",
            type=str,
            help="Path to local dataset template metadata file",
        )
        parser_run.add_argument(
            "-c", "--connection", type=str, help=LOCAL_CONNECTION_ID_STR
        )
        parser_run.set_defaults(func=run_model)

        parser_init = subparsers.add_parser(
            "init",
            help="Initialize model directory with basic structure",
            parents=[common_parser],
        )
        parser_init.set_defaults(func=init_model_directory)

        parser_clone = subparsers.add_parser(
            "clone", help="Clone Project Repository", parents=[common_parser]
        )
        parser_clone.add_argument(
            "-id", "--project-id", type=str, help="Id of Project to clone"
        )
        parser_clone.add_argument(
            "-p", "--path", type=str, help="Path to clone repository to"
        )
        parser_clone.set_defaults(func=clone)

        parser_configure = subparsers.add_parser(
            "link", help="Link local repo to project", parents=[common_parser]
        )
        parser_configure.set_defaults(func=link_repo)

        parser_tasks = subparsers.add_parser(
            "task", help="Manage feature engineering tasks"
        )
        subparser_tasks = parser_tasks.add_subparsers(
            title="actions", description=VALID_ACTIONS_STR, dest="command"
        )

        subparser_add_task = subparser_tasks.add_parser(
            "add",
            help="Add feature engineering task to working dir",
            parents=[common_parser],
        )
        subparser_add_task.add_argument(
            "-t",
            "--template-url",
            type=str,
            help="Git URL for template repository",
        )
        subparser_add_task.add_argument(
            "-b",
            "--branch",
            type=str,
            help="Git branch to pull templates (default is main)",
        )
        subparser_add_task.add_argument(
            "-n",
            "--name",
            type=str,
            help="Name of the new local task",
        )
        subparser_add_task.set_defaults(func=add_task)

        subparser_run_task = subparser_tasks.add_parser(
            "run", help="Run feature engineering tasks locally", parents=[common_parser]
        )
        subparser_run_task.add_argument(
            "-c", "--connection", type=str, help=LOCAL_CONNECTION_ID_STR
        )
        subparser_run_task.add_argument(
            "-n", "--name", type=str, help="Local task name"
        )
        subparser_run_task.add_argument(
            "-f", "--function-name", type=str, help="Task function name"
        )
        subparser_run_task.set_defaults(func=run_task)

        parser_connections = subparsers.add_parser(
            "connection", help="Manage local connections"
        )
        subparser_connections = parser_connections.add_subparsers(
            title="actions", description=VALID_ACTIONS_STR, dest="command"
        )
        subparser_list_connections = subparser_connections.add_parser(
            "list", help="List all local connections", parents=[common_parser]
        )
        subparser_list_connections.set_defaults(func=list_connections)
        subparser_add_connections = subparser_connections.add_parser(
            "add", help="Add a local connection", parents=[common_parser]
        )
        subparser_add_connections.add_argument(
            "-n", "--name", type=str, help="Connection name"
        )
        subparser_add_connections.add_argument(
            "-H", "--host", type=str, help="Connection host"
        )
        subparser_add_connections.add_argument(
            "-u", "--username", type=str, help="Connection username"
        )
        subparser_add_connections.add_argument(
            "-p", "--password", type=str, help="Connection password"
        )
        subparser_add_connections.add_argument(
            "-d", "--database", type=str, help="Connection default database"
        )
        subparser_add_connections.add_argument(
            "--val-db",
            type=str,
            default="val",
            help="Configure VAL installation db (default is val)",
        )
        subparser_add_connections.add_argument(
            "--byom-db",
            type=str,
            default="mldb",
            help="Configure BYOM installation db (default is mldb)",
        )
        subparser_add_connections.add_argument(
            "-l", "--logmech", type=str, help="Logmech to use"
        )
        subparser_add_connections.set_defaults(
            func=add_connections, parent_parser=subparser_add_connections
        )
        subparser_remove_connections = subparser_connections.add_parser(
            "remove", help="Remove a local connection", parents=[common_parser]
        )
        subparser_remove_connections.add_argument(
            "-c", "--connection", type=str, help=LOCAL_CONNECTION_ID_STR
        )
        subparser_remove_connections.set_defaults(func=remove_connections)
        subparser_export_connections = subparser_connections.add_parser(
            "export",
            help="Export a local connection to be used as a shell script",
            parents=[common_parser],
        )
        subparser_export_connections.add_argument(
            "-c", "--connection", type=str, help=LOCAL_CONNECTION_ID_STR
        )
        subparser_export_connections.set_defaults(func=export_connection)
        subparser_test_connections = subparser_connections.add_parser(
            "test", help="Test a local connection", parents=[common_parser]
        )
        subparser_test_connections.add_argument(
            "-c", "--connection", type=str, help=LOCAL_CONNECTION_ID_STR
        )
        subparser_test_connections.set_defaults(func=test_connection)

        subparser_create_byom_table = subparser_connections.add_parser(
            "create-byom-table",
            help="Create a table to store BYOM models",
            parents=[common_parser],
        )
        subparser_create_byom_table.add_argument(
            "-n",
            "--name",
            type=str,
            default="tmo_byom_models",
            help="Name of BYOM table (default is tmo_byom_models)",
        )
        subparser_create_byom_table.add_argument(
            "-e",
            "--execute-ddl",
            action="store_true",
            help="Execute CREATE TABLE DDL, not just generate it",
        )
        subparser_create_byom_table.set_defaults(func=create_byom_table)

        parser_features = subparsers.add_parser(
            "feature", help="Manage feature statistics"
        )
        subparser_feature = parser_features.add_subparsers(
            title="action", description=VALID_ACTIONS_STR, dest="command"
        )
        subparser_compute_stats = subparser_feature.add_parser(
            "compute-stats", help="Compute feature statistics", parents=[common_parser]
        )
        subparser_compute_stats.add_argument(
            "-s",
            "--source-table",
            type=str,
            help="Feature source table/view",
            required=True,
        )
        subparser_compute_stats.add_argument(
            "-m",
            "--metadata-table",
            type=str,
            help=METADATA_TABLE_HELP,
            required=True,
        )
        subparser_compute_stats.add_argument(
            "-t",
            "--feature-type",
            choices=["continuous", "categorical"],
            default="continuous",
            help="Feature type: continuous or categorical (default is continuous)",
        )
        subparser_compute_stats.add_argument(
            "-c", "--columns", type=str, help="List of feature columns", required=True
        )
        subparser_compute_stats.add_argument(
            "--temp-view-database",
            type=str,
            help="Database for creating temporary views (optional)",
            required=False,
        )
        subparser_compute_stats.set_defaults(
            func=compute_stats, parent_parser=subparser_compute_stats
        )
        subparser_list_stats = subparser_feature.add_parser(
            "list-stats", help="List available statistics", parents=[common_parser]
        )
        subparser_list_stats.add_argument(
            "-m",
            "--metadata-table",
            type=str,
            help=METADATA_TABLE_HELP,
            required=True,
        )
        subparser_list_stats.set_defaults(
            func=list_stats, parent_parser=subparser_list_stats
        )
        subparser_create_stats_table = subparser_feature.add_parser(
            "create-stats-table",
            help="Create statistics table",
            parents=[common_parser],
        )
        subparser_create_stats_table.add_argument(
            "-m",
            "--metadata-table",
            type=str,
            help=METADATA_TABLE_HELP,
            required=True,
        )
        subparser_create_stats_table.add_argument(
            "-e",
            "--execute-ddl",
            action="store_true",
            help="Execute CREATE TABLE DDL, not just generate it",
        )
        subparser_create_stats_table.set_defaults(
            func=create_stats_table, parent_parser=subparser_create_stats_table
        )
        subparser_import_stats = subparser_feature.add_parser(
            "import-stats",
            help="Import column statistics from local JSON file",
            parents=[common_parser],
        )
        subparser_import_stats.add_argument(
            "-m",
            "--metadata-table",
            type=str,
            help=METADATA_TABLE_HELP,
            required=True,
        )
        subparser_import_stats.add_argument(
            "-f",
            "--statistics-file",
            type=str,
            help="Name of statistics JSON file",
            required=True,
        )
        subparser_import_stats.add_argument(
            "-s",
            "--show-example",
            action="store_true",
            help="Show file structure example and exit",
        )
        subparser_import_stats.set_defaults(
            func=import_stats, parent_parser=subparser_import_stats
        )

        parser_doctor = subparsers.add_parser(
            "doctor", help="Diagnose configuration issues", parents=[common_parser]
        )
        parser_doctor.set_defaults(func=doctor)

        args = parent_parser.parse_args()

        logging_level = logging.DEBUG if args.debug else logging.INFO
        logging.basicConfig(
            format="%(message)s", stream=sys.stdout, level=logging_level
        )
        print("")

        # Certain functions don't need an API connection, can be called without initializing a client and repo manager
        local_functions = [
            print_help,
            list_connections,
            remove_connections,
            add_connections,
            test_connection,
            export_connection,
            create_byom_table,
            create_stats_table,
            import_stats,
            list_stats,
            compute_stats,
        ]
        if args.command and args.func not in local_functions:
            from tmo import RepoManager, TmoClient

            repo_manager = RepoManager(base_path)
            tmo_client = TmoClient()

            args.func(
                repo_manager=repo_manager,
                tmo_client=tmo_client,
                args=args,
                parent_parser=parent_parser,
            )
        else:
            args.func(args=args, parent_parser=parent_parser)

    except requests.exceptions.ConnectionError:
        logging.error(
            COLOR["WARN"]
            + "Could not connect to ModelOps API. "
            + COLOR["END"]
            + "\n"
            + "Please verify you are connected to network and have access to ModelOps"
            " UI.\n"
            + "If you are connected and have access, "
            + "try (re)copy the CLI configuration from ModelOps UI -> Session Details"
            " -> CLI Config.\n\n"
            + "For more details, run with --debug.\n"
        )

        if args.debug:
            logging.exception(
                COLOR["WARN"]
                + "An error occurred, printing stack trace output."
                + COLOR["END"]
            )

        sys.exit(1)

    except oauthlib.oauth2.rfc6749.errors.InvalidGrantError as ge:  # noqa
        _handle_invalid_grant_error(ge, args, __remove_cached_token)

    except oauthlib.oauth2.rfc6749.errors.InvalidTokenError as ge:  # noqa
        logging.error(
            ge.description
            + "\n"
            + COLOR["WARN"]
            + "Clearing the token cache. Please re-run cmd and login again."
            + COLOR["END"]
            + "\n"
        )

        __remove_cached_token()

        sys.exit(1)

    except KeyboardInterrupt:
        logging.info("")
        logging.info(
            f"{COLOR['WARN']}Keyboard interrupt... exiting{COLOR['END']}\33[?25h"
        )
        sys.exit(1)

    except Exception as ex:
        handle_generic_error(ex, args.debug)


filename = re.findall(r'File\s+"([^"]+)"', traceback.format_stack()[0])[0]

if filename in ["aoa"]:
    print(
        COLOR["WARN"],
        "This is an old version of Teradata ModelOps utility, still working, but"
        " consider using tmo command instead of aoa.",
        COLOR["END"],
    )

if __name__ in ["__main__", "aoa", "tmo"]:
    main()
