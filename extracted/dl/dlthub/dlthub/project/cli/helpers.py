from importlib import resources
from typing import Dict, Any, List, Optional, Tuple
import os
import tomlkit
import importlib
from dlt.common.utils import update_dict_nested

import argparse

from ruamel.yaml import YAML

from dlt.common.destination.reference import DestinationReference
from dlt.extract.reference import SourceReference
from dlt.extract.exceptions import UnknownSourceReference
from dlt._workspace.cli import (
    echo as fmt,
    CliCommandException,
    source_detection,
    DEFAULT_VERIFIED_SOURCES_REPO,
)
from dlt._workspace.cli._init_command import (
    _list_core_sources,
    _list_verified_sources,
    init_pipeline_at_destination,
)
from dlt._workspace.cli.config_toml_writer import WritableConfigValue

from dlthub.project.project_context import (
    ProjectRunContext,
    project_from_args,
    ProjectRunContextNotAvailable,
    create_empty_project_context,
)
from dlthub.common.constants import DEFAULT_PROJECT_CONFIG_FILE
from dlthub.project._templates.project import GIT_IGNORE
from dlthub.project.cli.write_state import ProjectWriteState

BASE_TEMPLATES_PATH = "dlthub.project._templates"
SOURCES_TEMPLATES_PATH = BASE_TEMPLATES_PATH + ".sources"
DESTINATIONS_TEMPLATES_PATH = BASE_TEMPLATES_PATH + ".destinations"
PROJECT_TEMPLATES_PATH = BASE_TEMPLATES_PATH + ".project"
REQUIREMENTS_FILE_NAME = "requirements.txt"
PYPROJECT_FILE_NAME = "pyproject.toml"
PACKAGE_INIT_FILE_NAME = "package_init.py"
TEMPLATE_TYPES = ["arrow", "dataframes", "python"]

CONFIG_TEMPLATES = {
    "rest_api": {
        "client": {
            "base_url": "https://jaffle-shop.dlthub.com/api/v1/",
            "paginator": {
                "type": "header_link",
            },
        },
        "resources": [
            "customers",
            "products",
        ],
    },
    "sql_database": {
        "table_names": ["family", "clan"],
    },
    "filesystem": {
        "bucket_url": "s3://<your-bucket-url>",
    },
    "arrow": {
        "row_count": 100,
    },
    "dataframes": {
        "row_count": 100,
    },
    "python": {
        "row_count": 100,
    },
}
SECRET_TEMPLATES = {
    "sql_database": {
        "credentials": {
            "drivername": "mysql+pymysql",
            "database": "Rfam",
            "username": "rfamro",
            "host": "mysql-rfam-public.ebi.ac.uk",
            "port": 4497,
        }
    }
}


def project_from_args_with_cli_output(
    args: argparse.Namespace, allow_no_project: bool = False
) -> ProjectRunContext:
    try:
        return project_from_args(args)
        # fmt.note(
        #     "Project Context: %s @ %s. Active profile: %s."
        #     % (run_context.name, run_context.run_dir, run_context.profile)
        # )
    except ProjectRunContextNotAvailable:
        if not allow_no_project:
            fmt.error(
                "No project context found. This cli command requires a project context, "
                "get started with `dlt project init` to create a new project."
            )
            raise
    return None


def read_project_yaml(project_run_context: ProjectRunContext) -> Any:
    """Read the project yaml file."""

    yaml = YAML()
    project_yaml_path = os.path.join(project_run_context.run_dir, DEFAULT_PROJECT_CONFIG_FILE)
    with open(project_yaml_path, "r", encoding="utf-8") as file:
        return yaml.load(file)


def write_project_yaml(project_dir: str, project_yaml: Any) -> None:
    """Write the project yaml file."""

    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)

    project_yaml_path = os.path.join(project_dir, DEFAULT_PROJECT_CONFIG_FILE)
    with open(project_yaml_path, "w", encoding="utf-8") as file:
        yaml.dump(project_yaml, file)


def _ensure_unique_name(given_name: str, existing_keys: List[str]) -> None:
    """Create a unique name by appending a number to the given name if it already exists."""
    if given_name in existing_keys:
        fmt.error(f"Name {given_name} already exists in project. Please use a different name.")
        raise CliCommandException()


def ensure_project_dirs(project_run_context: ProjectRunContext) -> None:
    """Ensure the project directories exist."""
    os.makedirs(project_run_context.settings_dir, exist_ok=True)


def init_project(
    root_dir: str, name: str = None, package_name: str = None
) -> Tuple[ProjectRunContext, ProjectWriteState]:
    """
    Prepares a new dlthub project in the given directory by preparing the project state.
    If package_name is provided, the project will be initialized as a pip package.

    To actually create the project, call `project_state.commit()`.
    NOTE: this will overwrite any existing dlt.yml file in the project directory, but will preserve
            the values in .dlt/secrets.toml and .dlt/config.toml files if they exist.

    Returns:
        Tuple[ProjectRunContext, ProjectState]: The project run context and a project_state, holding
            all changes that the project-creation entails.
    """

    yaml = YAML()

    # Load default project YAML template
    template_files = resources.files(PROJECT_TEMPLATES_PATH)
    project_yaml = yaml.load(template_files / DEFAULT_PROJECT_CONFIG_FILE)

    if name:
        project_yaml["project"] = project_yaml.get("project") or {}
        project_yaml["project"]["name"] = name

    # Determine package directory
    package_dir = os.path.join(root_dir, package_name) if package_name else root_dir

    # create new empty context and state
    project_run_context = create_empty_project_context(project_dir=package_dir)
    project_state = ProjectWriteState(project_run_context, read_project_yaml=False)
    project_state.dirs_to_create.append(package_dir)

    # Add project YAML to state
    project_state.dlt_yaml = project_yaml
    # polish-todo: handle existing pin-file. delete pin file if exists (after confirmation?)

    # Get install dependencies
    # from dlthub.version import __version__ as dlt_plus_version
    from dlt.version import __version__ as dlt_version

    dependencies = [f"dlt[hub]=={dlt_version}"]

    # Prepare pyproject.toml and package init file if package
    if package_name:
        pptoml = tomlkit.loads((template_files / PYPROJECT_FILE_NAME).read_text())
        pptoml["project"]["name"] = package_name  # type: ignore
        pptoml["project"]["dependencies"] = dependencies  # type: ignore
        pptoml["project"]["entry-points"]["dlt_package"]["dlt-project"] = package_name  # type: ignore

        # add dlt.yml file to the project
        pptoml["tool"]["setuptools"]["package-data"][package_name] = ["dlt.yml"]  # type: ignore

        project_state.add_new_file(
            os.path.join(root_dir, "pyproject.toml"),
            tomlkit.dumps(pptoml),
        )

        template_file_content = (template_files / PACKAGE_INIT_FILE_NAME).read_text()
        project_state.add_new_file(
            os.path.join(package_dir, "__init__.py"),
            template_file_content,
        )

    # Prepare requirements.txt if not a package
    else:
        project_state.add_new_file(
            os.path.join(root_dir, REQUIREMENTS_FILE_NAME),
            "\n".join(dependencies),
        )

    # Ensure project directories
    project_state.dirs_to_create.append(project_run_context.settings_dir)

    # Add default toml files to state
    project_state.add_new_file(
        os.path.join(project_run_context.settings_dir, "secrets.toml"),
        "# default secrets.toml file",
        accept_existing=True,
    )

    # Add .gitignore file to state
    project_state.add_new_file(
        os.path.join(root_dir, ".gitignore"),
        GIT_IGNORE,
    )

    return project_run_context, project_state


def add_profile(project_state: ProjectWriteState, profile_name: str) -> None:
    """Add a profile to the project."""

    project_state.dlt_yaml["profiles"] = project_state.dlt_yaml.get("profiles") or {}
    project_state.dlt_yaml["profiles"][profile_name] = {}

    # create profile secrets file as new file to be created
    project_state.add_new_file(
        os.path.join(project_state.settings_dir, f"{profile_name}.secrets.toml"),
        f"# secrets for profile {profile_name}\n",
    )


def init_pipeline(
    project_state: ProjectWriteState,
    source_name: str,
    destination_name: str,
    pipeline_name: str = None,
    dataset_name: str = None,
    location: str = None,
    branch: str = None,
    eject_source: bool = False,
    add_example_pipeline_script: bool = False,
    dependency_system: str = None,
) -> Tuple[str, str, str, str]:
    added_source_name = add_source(
        project_state,
        source_name,
        source_type=source_name,
        destination_type=destination_name,
        location=location,
        branch=branch,
        eject_source=eject_source,
        add_example_pipeline_script=add_example_pipeline_script,
        dependency_system=dependency_system,
    )
    # todo will this overwrite secret?
    added_destination_name, added_dataset_name = add_destination(
        project_state,
        destination_name,
        dataset_name=dataset_name,
    )
    pipeline_name = pipeline_name or "my_pipeline"
    add_pipeline(
        project_state,
        pipeline_name,
        added_source_name,
        added_destination_name,
        dataset_name=dataset_name,
    )
    return added_source_name, added_destination_name, pipeline_name, added_dataset_name


def add_source(
    project_state: ProjectWriteState,
    source_name: str,
    source_type: str = None,
    destination_type: str = None,
    location: str = DEFAULT_VERIFIED_SOURCES_REPO,
    branch: str = None,
    eject_source: bool = False,
    add_example_pipeline_script: bool = False,
    dependency_system: str = None,
) -> str:
    """
    Add a source to the project. If destination is provided, the example script will
    be configured to write to this destination, returns the name.
    optionally, context can be provided so that oss-init_command can deduce correct destination
    for sources and secrets automatically and suggest where to install the dependencies
    """

    project_state.dirs_to_create.append(project_state.settings_dir)

    project_yaml = project_state.dlt_yaml
    project_yaml["sources"] = project_yaml.get("sources") or {}

    # ensure unique name
    _ensure_unique_name(source_name, project_yaml["sources"].keys())
    source_type = source_type or source_name

    # todo catch case that source_type is a path to a local file
    # trying to import?
    source_category = None  # local, core, verified, template, default (not implemented yet)

    if source_type in TEMPLATE_TYPES:
        if add_example_pipeline_script and destination_type:
            fmt.warning(
                "There are currently no example pipeline scripts for template types."
                "You can find some in the dlt-repository under /sources/_single_file_templates."
            )
        return _add_template_source(
            project_state,
            source_name,
            source_type,
        )
    # check if we have the source in the project already
    if source_type not in _list_core_sources():
        try:
            return _add_a_local_source(
                project_state,
                source_name,
                source_type,
            )
        except UnknownSourceReference:
            pass

    # use oss-init commmand for core-sources and verified sources
    if add_example_pipeline_script and not destination_type:
        destination_type = "duckdb"
        fmt.echo("Using %s as destination for example script" % fmt.bold(destination_type))

    # handle core and verified sources with oss-init
    files_to_write, source_category, _ = init_pipeline_at_destination(
        # oss_init doesnt know about the name, so we pass the type
        source_name=source_type,
        destination_type=destination_type,
        repo_location=location,
        branch=branch,
        eject_source=eject_source,
        dry_run=True,
        add_example_pipeline_script=add_example_pipeline_script,
        destination_storage_path=project_state.project_dir,
        settings_dir=project_state.settings_dir,
        sources_dir=project_state.sources_dir,
        target_dependency_system=dependency_system,
    )
    if source_category == "template":
        # this means the source_type was an oss-pipeline-template (e.g. debug) or something unknown
        # in which case the source-files are only pipeline-example files
        fmt.error(
            "Dlt-project does not yet support adding the default source or a template source from "
            "OSS"
        )
        raise NotImplementedError()

    # add files to project state
    for file_path, content in files_to_write.items():
        # never write config.toml file
        if file_path.endswith("config.toml"):
            continue
        project_state.dirs_to_create.append(os.path.dirname(file_path))
        project_state.add_new_file(
            file_path,
            content,
            accept_existing=True,
        )
    try:
        source_ref = SourceReference.find(
            source_type, raise_exec_errors=False, import_missing_modules=False
        ).ref
    except UnknownSourceReference:
        # if this didnt work:
        # get first entry from SourceReference.SOURCES.keys() which includes
        # verified_source_name # e.g. slack wont be found in dlt.sources.slack.slack because its
        # slack.slack_source
        source_ref = next(
            (
                value
                for key, value in SourceReference.SOURCES.items()
                if key.startswith(source_type)
            ),
        )

    source_module_path = source_ref.ref
    if source_category == "core" and eject_source:
        source_module_path = _strip_base_path(source_module_path)
        # todo and emit warning that pipeline example script is not pointint there yet

    return _add_source_from_source_info(
        project_state=project_state,
        source_name=source_name,
        source_ref=source_ref,
        source_type=source_type,
        source_module_path=source_module_path,
    )


def _add_template_source(
    project_state: ProjectWriteState,
    source_name: str,
    source_type: str = None,
) -> str:
    """Add a template source to the project, returns the name."""

    source_type = source_type or source_name

    # copy file to sources dir (and adjust source type to module path)
    sources_dir = project_state.sources_dir
    project_state.dirs_to_create.append(sources_dir)
    new_file_path = os.path.join(sources_dir, f"{source_name}.py")
    source_template_file = resources.files(SOURCES_TEMPLATES_PATH) / f"{source_type}.py"
    project_state.add_new_file(new_file_path, source_template_file.read_text())

    # after being written it will be imported from here:
    source_module_path = f"{source_name}.source"

    # but we need to get the source_ref from the templates location
    template_ref = f"{SOURCES_TEMPLATES_PATH}.{source_type}.source"
    source_ref = SourceReference.find(
        template_ref, raise_exec_errors=True, import_missing_modules=True
    ).ref

    return _add_source_from_source_info(
        project_state=project_state,
        source_name=source_name,
        source_ref=source_ref,
        source_type=source_type,
        source_module_path=source_module_path,
    )


def _add_a_local_source(
    project_state: ProjectWriteState,
    source_name: str,
    source_type: str,
) -> str:
    """
    Add a local source to the project, returns the name.
    Optionally, a source_module_path can be provided where the source should be found
    """
    source_ref = SourceReference.find(
        source_type, raise_exec_errors=True, import_missing_modules=True
    ).ref

    return _add_source_from_source_info(
        project_state=project_state,
        source_name=source_name,
        source_ref=source_ref,
        source_type=source_type,
        source_module_path=source_type,
    )


def _add_source_from_source_info(
    project_state: ProjectWriteState,
    source_name: str,
    source_ref: SourceReference,
    source_type: str,
    source_module_path: str,
) -> str:
    """
    Add a SourceReference to the project state. This will extract necessary config and secrets
    too. If config- or secret default for the source_types are available those will be used
    instead
    params:
        project_state: ProjectWriteState - the project state to update
        source_name: str - the name of the source to add
        source_ref: SourceReference - the reference to the source
        source_type: str - the type of the source (e.g. rest_api, sql_database) as mentioned in
            in the initial call by the user
        source_module_path: str - the module path to the decorated function. This can be very
            different from the source_type, because the source_file might be renamed and the method
            name could be generic, e.g. my_new_db_source.source
    """
    required_secrets: Dict[str, WritableConfigValue] = {}
    required_config: Dict[str, WritableConfigValue] = {}

    # look up source and update configs SourceConfiguration
    source_detection.extract_secrets_and_configs_from_source_reference(
        source_info=source_ref,
        required_secrets=required_secrets,
        required_config=required_config,
        section=("sources", source_name),
    )

    # add secrets to project state
    if source_type in SECRET_TEMPLATES:
        _add_secrets_dict_to_project(
            project_state, SECRET_TEMPLATES[source_type], ("sources", source_name)
        )
    else:
        for secret in required_secrets.values():
            project_state.add_secrets_value(secret)

    # update project yaml with configs
    project_yaml = project_state.dlt_yaml
    project_yaml["sources"] = project_yaml.get("sources") or {}
    project_yaml["sources"][source_name] = {"type": source_module_path}

    if source_type in CONFIG_TEMPLATES:
        update_dict_nested(project_yaml["sources"][source_name], CONFIG_TEMPLATES[source_type])
    else:
        _add_configs_to_project_yaml(project_yaml, required_config)

    _multiple_sources_available_message(
        source_module_path=source_module_path, project_state=project_state, source_type=source_type
    )

    return source_name


def _add_secrets_dict_to_project(
    project_state: ProjectWriteState,
    secret_dict: Dict[str, Any],
    sections: Tuple[str, ...],
) -> None:
    """
    Adds a dictionary of secrets to the project state. Sections are derived from the keys of the
    dictionary.

    raises: TypeError if the value to be written is not a string, int, float, or bool.
    """
    for key, value in secret_dict.items():
        hint = type(value)
        if hint is dict:
            _add_secrets_dict_to_project(
                project_state=project_state,
                secret_dict=value,
                sections=sections + (key,),
            )
        else:
            if not isinstance(value, (str, int, float, bool)):
                raise TypeError(
                    f"Invalid type for config value {key}: {hint}. "
                    "Expected str, int, float, or bool."
                )
            config_value = WritableConfigValue(
                name=key,
                hint=hint,
                default_value=value,
                sections=sections,
            )
            project_state.add_secrets_value(config_value)


def _add_configs_to_project_yaml(
    dlt_yaml: Dict[str, Any], config_dict: Dict[str, WritableConfigValue]
) -> None:
    """
    Adds configuration values to the YAML dictionary.

    Args:
        yaml_dict YAML: The YAML dictionary to update.
        config_values (Dict[str, WritableConfigValue]): The configuration values to add.
    """
    for _, config_value in config_dict.items():
        current_level = dlt_yaml
        for section in config_value.sections:
            if section not in current_level:
                current_level[section] = {}
            current_level = current_level[section]
        # if something exists there, continue
        if config_value.name in current_level:
            fmt.warning(
                f"Config value {config_value.name} already exists in the project yaml. "
                "Will not be overwritten with defaults"
            )
            continue
        current_level[config_value.name] = config_value.default_value or "<configure me>"


def _strip_base_path(module_path: str, base_path: str = "dlt.sources.") -> str:
    """
    Strips the base path from the module path if it starts with the base path.
    """
    if module_path.startswith(base_path):
        return module_path.replace(base_path, "")
    return module_path


def _multiple_sources_available_message(
    source_module_path: str,
    project_state: ProjectWriteState,
    source_type: str,
) -> None:
    """
    Display a message when multiple source candidates are available for a verified source.
    """
    source_candidates = [s for s in SourceReference.SOURCES.keys()]
    if len(source_candidates) > 1:
        stripped_items = [item.split(".")[-1] for item in source_candidates]
        # deduplicate
        source_candidates = list(dict.fromkeys(stripped_items))
        fmt.echo("* Note: There are multiple sources/resources available for this source:")
        for candidate in source_candidates:
            if source_module_path.endswith(candidate):
                fmt.echo(f"  - {fmt.bold(candidate)} (selected)")
            else:
                fmt.echo(f"  - {candidate}")
        relative_path = _strip_base_path(
            f"{project_state.sources_dir}/{source_type}/__init__.py",
            base_path=project_state.project_dir,
        )
        fmt.echo(" For details, check out .%s" % fmt.bold(relative_path))


def add_dataset(project_state: ProjectWriteState, dataset_name: str, destination_name: str) -> str:
    """Add a dataset to the project, returns the name."""
    project_yaml = project_state.dlt_yaml
    project_yaml["datasets"] = project_yaml.get("datasets") or {}

    # create name
    _ensure_unique_name(dataset_name, project_yaml["datasets"].keys())

    # add dataset to yaml
    project_yaml["datasets"][dataset_name] = {
        "destination": [destination_name],
    }

    return dataset_name


def add_destination(
    project_state: ProjectWriteState,
    destination_name: str,
    destination_type: str = None,
    dataset_name: str = None,
) -> Tuple[str, str]:
    """Add a destination to the project, returns the name."""
    project_state.dirs_to_create.append(project_state.settings_dir)

    # look up destination
    destination_type = destination_type or destination_name
    destination_ref = DestinationReference.find(
        destination_type,
        raise_exec_errors=True,
        import_missing_modules=True,
    )
    # extract factory if we resolve custom destination (decorator)
    destination_ref = DestinationReference.ensure_factory(destination_ref)

    # ensure unique name
    project_yaml = project_state.dlt_yaml
    project_yaml["destinations"] = project_yaml.get("destinations") or {}
    _ensure_unique_name(destination_name, project_yaml["destinations"].keys())

    # update project yaml
    project_yaml["destinations"][destination_name] = {
        "type": destination_type,
    }

    # extract secrets to toml file
    destination_secrets = WritableConfigValue(
        destination_name, destination_ref.spec, None, ("destination",)
    )
    project_state.add_secrets_value(destination_secrets)

    # add a dataset for this destination
    if dataset_name:
        dataset_name = dataset_name or destination_name + "_dataset"
        dataset_name = add_dataset(project_state, dataset_name, destination_name)
    else:
        dataset_name = None

    return destination_name, dataset_name


def add_pipeline(
    project_state: ProjectWriteState,
    pipeline_name: str,
    source_name: str,
    destination_name: str,
    dataset_name: str = None,
) -> None:
    """Add a pipeline to the project, returns the name."""
    project_yaml = project_state.dlt_yaml
    project_yaml["pipelines"] = project_yaml.get("pipelines") or {}

    # create name
    _ensure_unique_name(pipeline_name, project_yaml["pipelines"].keys())

    # add pipeline to yaml
    project_yaml["pipelines"][pipeline_name] = {
        "source": source_name,
        "destination": destination_name,
    }

    # add dataset name if provided
    if dataset_name:
        project_yaml["pipelines"][pipeline_name]["dataset_name"] = dataset_name
    else:
        project_yaml["pipelines"][pipeline_name]["dataset_name"] = pipeline_name + "_dataset"


def get_available_destinations() -> List[str]:
    """Get all available destinations."""
    return [
        d.replace("dlthub.destinations.", "").replace("dlt.destinations.", "")
        for d in DestinationReference.DESTINATIONS.keys()
    ]


def get_available_source_templates(package: str = SOURCES_TEMPLATES_PATH) -> Dict[str, str]:
    """Get all available single file source templates."""

    templates: Dict[str, str] = {}
    package_files = resources.files(package)
    for source_template in package_files.iterdir():
        if source_template.name.startswith("_"):
            continue
        if not source_template.name.endswith(".py"):
            continue
        module_name = source_template.name.replace(".py", "")
        source = importlib.import_module(package + "." + module_name)
        templates[module_name] = source.__doc__

    return templates


def get_available_core_sources() -> Dict[str, str]:
    """Get all available core sources."""
    ret = {}
    for source_name, source_config in _list_core_sources().items():
        ret[source_name] = source_config.doc
    return ret


def get_verified_sources() -> dict[str, str]:
    """List all available verified sources, cloning from dlt-verified-sources"""
    sources = {}
    with fmt.suppress_echo():
        for source_name, source_config in _list_verified_sources(
            repo_location=DEFAULT_VERIFIED_SOURCES_REPO
        ).items():
            sources[source_name] = source_config.doc
        return sources


def ensure_unique_names(
    project_state: ProjectWriteState,
    source_name: Optional[str] = None,
    destination_name: Optional[str] = None,
    pipeline_name: Optional[str] = None,
    dataset_name: Optional[str] = None,
) -> None:
    """Ensure unique names for source, destination, pipeline, and dataset if they are provided."""
    project_yaml = project_state.dlt_yaml
    project_yaml["sources"] = project_yaml.get("sources") or {}
    project_yaml["destinations"] = project_yaml.get("destinations") or {}
    project_yaml["pipelines"] = project_yaml.get("pipelines") or {}
    project_yaml["datasets"] = project_yaml.get("datasets") or {}

    if source_name:
        _ensure_unique_name(source_name, project_yaml["sources"].keys())
    if destination_name:
        _ensure_unique_name(destination_name, project_yaml["destinations"].keys())
    if pipeline_name:
        _ensure_unique_name(pipeline_name, project_yaml["pipelines"].keys())
    if dataset_name:
        _ensure_unique_name(dataset_name, project_yaml["datasets"].keys())
