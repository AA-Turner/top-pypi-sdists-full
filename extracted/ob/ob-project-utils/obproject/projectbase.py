import os
import subprocess
from metaflow import (
    FlowSpec,
    Config,
    config_expr,
    project,
    get_namespace,
    namespace,
    Task,
    pyproject_toml_parser,
    FlowMutator,
    pypi_base,
)

from .assets import Asset, _sanitize_branch_name
from .evals_logger import EvalsLogger
from .project_events import ProjectEvent

project_ctx = None


def toml_parser(cfgstr):
    try:
        # python >= 3.11
        import tomllib as toml
    except ImportError:
        import toml
    return toml.loads(cfgstr)


def _detect_git_branch():
    """
    Detect the current git branch from the local repository.
    Returns None if not in a git repository or git is unavailable.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def _get_write_branch(project_spec):
    """
    Determine the write branch for assets.

    Priority order:
    1. Deployed context: use git branch from project_spec (set at deploy time)
    2. Local runs: use metaflow branch (user namespace) for consistency with k8s

    Returns: branch name for asset writes
    """
    from metaflow import current

    # 1. Deployed: use git branch from deploy time
    if project_spec:
        spec = project_spec.get("spec", project_spec)
        # project_spec includes 'branch' and 'project_branch' which are the git branch
        git_branch = spec.get("project_branch") or project_spec.get("branch")
        if git_branch:
            return git_branch

    # 2. Local runs: use metaflow branch for user isolation
    # This ensures local runs behave consistently with --with kubernetes
    return current.branch_name


def _get_read_branch(write_branch, project_config):
    """
    Determine the read branch for assets.

    - If on main branch: read from main (production assets)
    - If on other branch + [dev-assets] configured: read from configured branch
    - Otherwise: read from same branch as write

    Returns: branch name for asset reads
    """
    dev_config = project_config.get("dev-assets", {})
    dev_read_branch = dev_config.get("branch")

    # Main branch is self-contained (production)
    is_main = write_branch == "main"

    # Non-main branches can read from a different branch via [dev-assets]
    if dev_read_branch and not is_main:
        return dev_read_branch

    return write_branch


def resolve_scope(project_config, project_spec):
    """
    Resolve asset branches from config.

    Returns: (project, write_branch, read_branch)

    Assets are scoped to git branches, providing a 1:1 mapping between
    git branches and asset namespaces:
    - main -> assets stored/read from 'main'
    - feature-x -> assets stored/read from 'feature-x'

    The [dev-assets] config allows non-main branches to READ from a different
    branch (typically 'main') while WRITING to their own branch.

    | Context                 | Write Branch      | Read Branch        |
    |-------------------------|-----------------  |------------------  |
    | Deployed from main      | main              | main               |
    | Deployed from feature-x | feature-x         | feature-x          |
    | Deployed + [dev-assets] | feature-x         | configured         |
    | Local with git          | <git branch>      | same or configured |
    | Local without git       | <metaflow branch> | same or configured |
    """
    project_name = project_config["project"]
    write_branch = _get_write_branch(project_spec)
    read_branch = _get_read_branch(write_branch, project_config)
    return project_name, write_branch, read_branch


class ProjectContext:
    def __init__(self, flow):
        from metaflow import current, Flow

        self.flow = flow
        self.project_config = flow.project_config
        self.project_spec = flow.project_spec

        self.project, write_branch, read_branch = resolve_scope(
            self.project_config, self.project_spec
        )
        # for metaflow/argo syntax rules
        self.write_branch = _sanitize_branch_name(write_branch)
        self.read_branch = _sanitize_branch_name(read_branch)
        self.branch = self.read_branch

        try:
            run = Flow(current.flow_name)[current.run_id]
            run.add_tag(f"asset_write_branch:{self.write_branch}")
            if self.read_branch != self.write_branch:
                run.add_tag(f"asset_read_branch:{self.read_branch}")
        except Exception:
            pass  

        # Note: read_only=False enables consumption tracking via PUT with entity_ref
        self._read_asset = Asset(
            project=self.project, branch=self.read_branch, read_only=False
        )
        self._write_asset = Asset(
            project=self.project, branch=self.write_branch, read_only=False
        )
        # Expose read asset as default - consume operations use read branch
        # Registration methods explicitly use _write_asset
        self.asset = self._read_asset
        self.evals = EvalsLogger(project=self.project, branch=self.write_branch)

        if self.read_branch != self.write_branch:
            print(f"Asset client: read from {self.project}/{self.read_branch}")
            print(f"Asset client: write to {self.project}/{self.write_branch}")
        else:
            print(f"Asset client: {self.project}/{self.write_branch} (read-write)")

    def publish_event(self, name, payload=None):
        ProjectEvent(name, project=self.project, branch=self.branch).publish(payload)

    def safe_publish_event(self, name, payload=None):
        ProjectEvent(name, project=self.project, branch=self.branch).safe_publish(
            payload
        )

    def register_data(self, name, artifact, annotations=None, tags=None, description=None):
        """
        Register a Metaflow artifact as a data asset.

        Use this when your data is stored as a flow artifact. For external data
        (S3, databases, etc.), use register_external_data().

        Args:
            name: Asset name/id
            artifact: Flow artifact name (self.<artifact>)
            annotations: Optional dict of metadata key-value pairs
            tags: Optional dict of tag key-value pairs
            description: Optional human-readable description

        Example:
            self.features = compute_features(data)
            self.prj.register_data("fraud_features", "features",
                annotations={"row_count": len(self.features)},
                tags={"version": "v2", "source": "postgres"})
        """
        if hasattr(self.flow, artifact):
            # Merge user annotations with artifact reference
            all_annotations = {"artifact": artifact}
            if annotations:
                all_annotations.update(annotations)

            self._write_asset.register_data_asset(
                name,
                kind="artifact",
                annotations=all_annotations,
                tags=tags,
                description=description
            )
            print(f"📦 Registered data asset: {name}")
            if annotations:
                print(f"   Annotations: {', '.join(f'{k}={v}' for k, v in annotations.items())}")
        else:
            raise AttributeError(
                f"The flow doesn't have an artifact '{artifact}'. Is self.{artifact} set?"
            )

    def register_external_data(self, name, blobs, kind, annotations=None, tags=None, description=None):
        """
        Register external data as a data asset.

        Use this for data living outside Metaflow artifacts: S3 objects, database
        tables, API endpoints, etc. Common in sensor flows, notebooks, and deployments.

        Args:
            name: Asset name/id
            blobs: List of URIs/references to the data (e.g., ["s3://bucket/file.csv"])
            kind: Data type identifier (e.g., "s3_object", "snowflake_table", "postgres_table")
            annotations: Optional dict of metadata
            tags: Optional dict of tags
            description: Optional human-readable description

        Examples:
            # S3 data detected by sensor
            self.prj.register_external_data("raw_sales",
                blobs=["s3://data-lake/sales/2024-01-01.parquet"],
                kind="s3_object",
                annotations={"size_bytes": 1024000, "row_count": 50000},
                tags={"source": "sensor", "format": "parquet"})

            # Snowflake table reference
            self.prj.register_external_data("transactions",
                blobs=["snowflake://prod.analytics.transactions"],
                kind="snowflake_table",
                annotations={"last_updated": "2024-01-01T00:00:00Z"})

            # From notebook or deployment
            self.prj.register_external_data("user_features",
                blobs=["postgresql://db.public.features"],
                kind="postgres_table")
        """
        self._write_asset.register_data_asset(
            name,
            kind=kind,
            blobs=blobs,
            annotations=annotations,
            tags=tags,
            description=description
        )
        print(f"📦 Registered external data asset: {name} (kind={kind})")
        if annotations:
            print(f"   Annotations: {', '.join(f'{k}={v}' for k, v in annotations.items())}")

    def register_model(self, name, artifact, annotations=None, tags=None, description=None):
        """
        Register a Metaflow artifact as a model asset.

        Use this for trained models stored as flow artifacts. For external models
        (HuggingFace Hub, checkpoint directories, etc.), use register_external_model().

        Args:
            name: Asset name/id
            artifact: Flow artifact name (self.<artifact>) containing the model
            annotations: Optional dict of metadata (accuracy, f1, training_time, etc.)
            tags: Optional dict of tags (model_type, framework, status, etc.)
            description: Optional human-readable description

        Example:
            self.model = train(features)
            self.prj.register_model("fraud_model", "model",
                annotations={"accuracy": 0.94, "f1_score": 0.91},
                tags={"framework": "sklearn", "status": "validated"})
        """
        if hasattr(self.flow, artifact):
            # Merge user annotations with artifact reference
            all_annotations = {"artifact": artifact}
            if annotations:
                all_annotations.update(annotations)

            self._write_asset.register_model_asset(
                name,
                kind="artifact",
                annotations=all_annotations,
                tags=tags,
                description=description
            )
            print(f"🧠 Registered model asset: {name}")
            if annotations:
                print(f"   Annotations: {', '.join(f'{k}={v}' for k, v in annotations.items())}")
        else:
            raise AttributeError(
                f"The flow doesn't have an artifact '{artifact}'. Is self.{artifact} set?"
            )

    def register_external_model(self, name, blobs, kind, annotations=None, tags=None, description=None):
        """
        Register an external model as a model asset.

        Use this for models living outside Metaflow artifacts: HuggingFace Hub,
        checkpoint directories, model registries, API endpoints, etc. Common in
        notebooks, deployments, and checkpoint-based workflows.

        Args:
            name: Asset name/id
            blobs: List of URIs/references to the model (e.g., ["s3://models/checkpoint/"])
            kind: Model type identifier (e.g., "checkpoint_dir", "huggingface", "mlflow")
            annotations: Optional dict of metadata
            tags: Optional dict of tags
            description: Optional human-readable description

        Examples:
            # Checkpoint directory from training
            from metaflow import current
            self.prj.register_external_model("training_checkpoints",
                blobs=[current.checkpoint.directory],
                kind="checkpoint_dir",
                annotations={"best_epoch": 42, "best_loss": 0.123},
                tags={"framework": "pytorch", "status": "training"})

            # HuggingFace model reference
            self.prj.register_external_model("base_llm",
                blobs=["meta-llama/Llama-3.1-8B-Instruct"],
                kind="huggingface",
                annotations={"context_length": 8192},
                tags={"model_type": "llm", "provider": "meta"})

            # MLflow model URI
            self.prj.register_external_model("production_model",
                blobs=["models:/fraud_detector/production"],
                kind="mlflow",
                annotations={"mlflow_run_id": "abc123"})
        """
        self._write_asset.register_model_asset(
            name,
            kind=kind,
            blobs=blobs,
            annotations=annotations,
            tags=tags,
            description=description
        )
        print(f"🧠 Registered external model asset: {name} (kind={kind})")
        if annotations:
            print(f"   Annotations: {', '.join(f'{k}={v}' for k, v in annotations.items())}")

    def get_data(self, name, instance="latest"):
        """
        Get a data asset instance.

        Reads from the read_branch (e.g., main for prod assets during local dev).

        Args:
            name: Asset name/id
            instance: Version to retrieve ("latest", "v123", "latest-1")

        Returns:
            The artifact data for the specified version
        """
        ref = self._read_asset.consume_data_asset(name, instance=instance)
        kind = ref["data_properties"]["data_kind"]
        if kind == "artifact":
            ns = get_namespace()
            try:
                namespace(None)
                task = Task(ref["created_by"]["entity_id"])
                artifact = ref["data_properties"]["annotations"]["artifact"]

                return task[artifact].data
            finally:
                namespace(ns)
        else:
            raise AttributeError(
                f"Data asset '{name}' doesn't seem like an artifact. It is of kind '{kind}'"
            )

    def get_model(self, name, instance="latest"):
        """
        Get a model asset instance.

        Reads from the read_branch (e.g., main for prod assets during local dev).

        Args:
            name: Asset name/id
            instance: Version to retrieve ("latest", "v123", "latest-1")

        Returns:
            The artifact data for the specified version
        """
        ref = self._read_asset.consume_model_asset(name, instance=instance)
        kind = ref["model_properties"]["model_kind"]
        if kind == "artifact":
            ns = get_namespace()
            try:
                namespace(None)
                task = Task(ref["created_by"]["entity_id"])
                artifact = ref["model_properties"]["annotations"]["artifact"]

                return task[artifact].data
            finally:
                namespace(ns)
        else:
            raise AttributeError(
                f"Model asset '{name}' doesn't seem like an artifact. It is of kind '{kind}'"
            )


class project_pypi(FlowMutator):
    def pre_mutate(self, mutable_flow):
        # Allow skipping pypi_base for local development
        # Set OBPROJECT_SKIP_PYPI_BASE=1 to run flows without dependency isolation
        if os.getenv("OBPROJECT_SKIP_PYPI_BASE") == "1":
            return

        project_config = dict(mutable_flow.configs).get("project_config")
        project_deps = dict(mutable_flow.configs).get("project_deps")
        include_pyproject = project_config.get("dependencies", {}).get(
            "include_pyproject_toml", True
        )
        if include_pyproject and project_deps["packages"]:
            mutable_flow.add_decorator(
                pypi_base, deco_kwargs=project_deps, duplicates=mutable_flow.ERROR
            )


@project_pypi
@project(name=config_expr("project_config.project"))
class ProjectFlow(FlowSpec):
    project_config = Config(
        "project_config", default="obproject.toml", parser=toml_parser
    )
    project_deps = Config(
        "project_deps", default_value="", parser=pyproject_toml_parser
    )
    project_spec = Config("project_spec", default_value="{}")

    @property
    def prj(self):
        global project_ctx
        if project_ctx is None:
            project_ctx = ProjectContext(self)
        return project_ctx
