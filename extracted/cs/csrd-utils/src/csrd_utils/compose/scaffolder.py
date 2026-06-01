"""Scaffold services from the cookiecutter template into the workspace layout.

Workspace layout contract::

    <ws-root>/
      src/<service_name_snake>/        ← service source (views, settings, __init__)
      tests/unit/<service_name_snake>/ ← unit tests (snake_case)
      tests/acceptance/<service_name_snake>/  ← acceptance test stub
      Dockerfile.<service-name>        ← per-service Dockerfile

Augment scaffolding adds files into an existing service source tree.
Files are created once and never overwritten (they may contain user edits).
"""

import logging
import shutil
import tempfile
from pathlib import Path
from string import Template

from cookiecutter.main import cookiecutter

from ..models import ComposeSpec, ServiceAugment, ServiceNode
from .augments import AUGMENT_REGISTRY

logger = logging.getLogger(__name__)

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates" / "service"
_AUGMENT_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates" / "augments"


def scaffold_service(service: ServiceNode, workspace_root: Path) -> bool:
    """Scaffold a single service into the workspace layout.

    Skips silently if ``src/<service_name_snake>/`` already exists (idempotent).
    Returns ``True`` if the service was actually scaffolded, ``False`` if skipped.
    """

    service_name_snake = service.name.replace("-", "_")
    src_dest = workspace_root / "src" / service_name_snake
    if src_dest.exists():
        return False

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        cookiecutter(
            str(_TEMPLATE_DIR),
            no_input=True,
            output_dir=str(tmp_path),
            extra_context={
                "service_name": service.name,
                "port": str(service.port),
            },
        )

        rendered = tmp_path / service_name_snake

        # --- Move service source to src/<service-name>/ ---
        src_dest.parent.mkdir(parents=True, exist_ok=True)
        src_rendered = rendered

        # Extract Dockerfile before moving
        dockerfile_src = src_rendered / "Dockerfile"
        dockerfile_dest = workspace_root / f"Dockerfile.{service.name}"
        if dockerfile_src.exists() and not dockerfile_dest.exists():
            shutil.move(str(dockerfile_src), str(dockerfile_dest))
        elif dockerfile_src.exists():
            dockerfile_src.unlink()

        # Extract tests before moving
        tests_src = src_rendered / "tests"
        if tests_src.exists():
            unit_dest = workspace_root / "tests" / "unit" / service_name_snake
            unit_dest.mkdir(parents=True, exist_ok=True)
            for item in tests_src.iterdir():
                dest = unit_dest / item.name
                if not dest.exists():
                    shutil.move(str(item), str(dest))

            # Remove the now-empty tests dir from rendered source
            shutil.rmtree(str(tests_src), ignore_errors=True)

            # Create acceptance stub
            acceptance_dest = workspace_root / "tests" / "acceptance" / service_name_snake
            acceptance_dest.mkdir(parents=True, exist_ok=True)

        # Move everything remaining as the service source
        shutil.move(str(src_rendered), str(src_dest))

    return True


def scaffold_services(spec: ComposeSpec, workspace_root: Path) -> set[str]:
    """Scaffold all services in the spec into the workspace.

    Returns the set of service names that were **newly scaffolded** (not
    previously existing).  Callers use this to decide which spec-rendered
    files (settings.py, __init__.py) need to be written for the first time.
    """

    newly_scaffolded: set[str] = set()
    for service in spec.services:
        # Frontend services use their own scaffold, not the Python cookiecutter
        if service.role == "frontend":
            continue
        if scaffold_service(service, workspace_root):
            newly_scaffolded.add(service.name)
        # Scaffold augment files into the service source tree
        for augment in service.augments:
            scaffold_augment(augment, service, spec, workspace_root)

    # Scaffold workspace augments that target a service role
    for ws_augment in spec.workspace.augments:
        desc = AUGMENT_REGISTRY.get(ws_augment.name)
        if desc is None or desc.applies_to_role is None or desc.template_dir is None:
            continue
        target_svc = next(
            (s for s in spec.services if s.role == desc.applies_to_role),
            None,
        )
        if target_svc is not None:
            scaffold_augment(
                ServiceAugment(name=ws_augment.name, options=ws_augment.options),
                target_svc,
                spec,
                workspace_root,
            )

    return newly_scaffolded


# ---------------------------------------------------------------------------
# Augment scaffolding
# ---------------------------------------------------------------------------


def _augment_template_vars(
    augment: ServiceAugment,
    service: ServiceNode,
    spec: ComposeSpec,
) -> dict[str, str]:
    """Build template variable dict for augment file rendering.

    Uses ``string.Template`` (``$var`` / ``${var}``) for simple
    substitution — no cookiecutter overhead needed for augment files.

    Static variables (service name, port) are always included.
    Augment options are auto-passed. Dynamic variables are resolved
    via the descriptor's ``resolve_template_vars`` callback.
    """
    svc_snake = service.name.replace("-", "_")

    variables: dict[str, str] = {
        "service_name": service.name,
        "service_name_snake": svc_snake,
        "port": str(service.port),
    }

    # Auto-pass augment options as template variables
    for key, value in augment.options.items():
        if isinstance(value, str):
            variables[key] = value

    # Dynamic variables from descriptor resolver
    desc = AUGMENT_REGISTRY.get(augment.name)
    if desc is not None and desc.resolve_template_vars is not None:
        variables.update(desc.resolve_template_vars(augment, service, spec))

    return variables


def scaffold_augment(
    augment: ServiceAugment,
    service: ServiceNode,
    spec: ComposeSpec,
    workspace_root: Path,
) -> None:
    """Scaffold augment template files into a service source tree.

    Template files are found under ``templates/augments/<template_dir>/``.
    Each file is rendered with ``string.Template`` substitution and copied
    into the service's source directory, preserving subdirectory structure.

    When the descriptor provides ``resolve_multi_scaffold_vars``, templates
    are rendered once per returned variable dict (e.g. one per discovered
    entity).  Otherwise templates are rendered once with the standard vars.

    Files that already exist are **never overwritten** — they may contain
    user edits.  This makes the operation idempotent and safe to re-run.
    """
    desc = AUGMENT_REGISTRY.get(augment.name)
    if desc is None or desc.template_dir is None:
        return

    template_dir = _AUGMENT_TEMPLATE_DIR / desc.template_dir
    if not template_dir.is_dir():
        logger.debug(
            "Augment template dir %s does not exist yet — skipping scaffold",
            template_dir,
        )
        return

    svc_dest = workspace_root / "src" / service.name.replace("-", "_")
    if not svc_dest.exists():
        return

    # Multi-instance scaffolding (e.g. crud-scaffold renders per entity)
    if desc.resolve_multi_scaffold_vars is not None:
        var_sets = desc.resolve_multi_scaffold_vars(augment, service, spec)
        for variables in var_sets:
            _render_template_set(template_dir, svc_dest, variables, augment.name)
    else:
        variables = _augment_template_vars(augment, service, spec)
        _render_template_set(template_dir, svc_dest, variables, augment.name)


def _render_template_set(
    template_dir: Path,
    svc_dest: Path,
    variables: dict[str, str],
    augment_name: str,
) -> None:
    """Render a set of template files with the given variables."""
    for template_file in sorted(template_dir.rglob("*")):
        if template_file.is_dir():
            continue
        # Skip __pycache__ and other noise
        if "__pycache__" in str(template_file):
            continue

        relative = template_file.relative_to(template_dir)
        # Apply template substitution to file path (e.g. $entity_name_snake.py → item.py)
        relative = Path(Template(str(relative)).safe_substitute(variables))

        # Skip files with unresolved template variables in the path (e.g.
        # entity-specific templates when rendering with task-only vars)
        if "$" in str(relative):
            continue

        dest = svc_dest / relative

        # Strip .template suffix so e.g. db.py.template → db.py
        if dest.name.endswith(".template"):
            dest = dest.with_name(dest.name.removesuffix(".template"))

        # Never overwrite existing files
        if dest.exists():
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)

        content = template_file.read_text(encoding="utf-8")
        # Apply template substitution (safe_substitute ignores unknown vars)
        rendered = Template(content).safe_substitute(variables)
        dest.write_text(rendered, encoding="utf-8")

        logger.debug("Scaffolded %s for augment '%s'", dest, augment_name)
