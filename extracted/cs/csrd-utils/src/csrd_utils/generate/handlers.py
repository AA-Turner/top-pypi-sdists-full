"""Command handlers for generate actions."""

from contextlib import suppress
from pathlib import Path
from typing import TypedDict, cast

from ..compose import (
    AUGMENT_REGISTRY,
    INFRA_CATEGORIES,
    ROLE_REGISTRY,
    AugmentDescriptor,
    InfraNode,
    PresetDefinition,
    ServiceAugment,
    ServiceNode,
    available_infra,
    available_service_augments,
    available_workspace_augments,
    configured_infra,
    list_presets,
    load_spec,
    next_available_port,
    render_workspace,
    spec_file_path,
)
from ..compose import add_infra as compose_add_infra
from ..compose import add_service as compose_add_service
from ..compose import add_service_augment as compose_add_service_augment
from ..compose import add_workspace_augment as compose_add_workspace_augment
from ..compose import apply as compose_apply
from ..compose import remove_infra as compose_remove_infra
from ..compose import remove_service as compose_remove_service
from ..compose import rename_service as compose_rename_service
from .helpers import (
    _WIZARD_INTERRUPTED,
    GoBack,
    WizardStep,
    normalize_service_name,
    prompt_multi_select,
    prompt_single_select,
    prompt_text,
    prompt_yes_no,
    resolve_workspace_name,
    run_wizard,
)

# ---------------------------------------------------------------------------
# Typed wizard state — eliminates cast() proliferation
# ---------------------------------------------------------------------------


class _WizardState(TypedDict, total=False):
    """Typed view of the wizard ``dict[str, object]`` state bag.

    Step functions receive ``dict[str, object]`` from ``run_wizard`` but
    can narrow to ``_WizardState`` with a single cast at the top.
    All subsequent key access is then properly typed.
    """

    default_name: str
    name: str
    infra_choices: list[str]
    services: list[ServiceNode]
    workspace_augments: list[str]
    _preset: PresetDefinition | None
    _output_dir: Path
    _pre_existing: bool
    git_init: bool


def _ws(state: dict[str, object]) -> _WizardState:
    """Narrow untyped wizard state to ``_WizardState``."""
    return cast(_WizardState, state)


# ---------------------------------------------------------------------------
# Roles — derived from ROLE_REGISTRY
# ---------------------------------------------------------------------------

_VALID_ROLES = list(ROLE_REGISTRY.keys())

#: Roles that should exist at most once per workspace.
_SINGLETON_ROLES = {name for name, desc in ROLE_REGISTRY.items() if desc.singleton}


def _infer_role(name: str) -> str:
    """Suggest a role based on the service name using ROLE_REGISTRY name_hints."""
    for role_name, desc in ROLE_REGISTRY.items():
        if any(hint in name for hint in desc.name_hints):
            return role_name
    return "app"


def _next_port(services: list[ServiceNode], base: int = 8080) -> int:
    """Return the next available port after existing services."""
    ports = [s.port for s in services]
    return (max(ports) + 1) if ports else base


def _resolve_implies(svc: ServiceNode) -> None:
    """Resolve augment ``implies`` transitively on a service.

    If an augment implies another (e.g. crud-scaffold → db-config),
    the implied augment is added if not already present.  Also auto-wires
    service augments implied by the service's role (e.g. worker → celery-worker).
    Processes transitively until no new augments are added.
    """
    # Role-implied augments
    role_desc = ROLE_REGISTRY.get(svc.role) if svc.role else None
    if role_desc is not None:
        existing = {a.name for a in svc.augments}
        for aug_name in role_desc.implies_service_augments:
            if aug_name not in existing:
                svc.augments.append(ServiceAugment(name=aug_name))

    _resolve_implies_list(svc.augments)


def _resolve_implies_list(augments: list[ServiceAugment]) -> None:
    """Resolve augment ``implies`` transitively on a mutable augment list.

    Shared by ``_resolve_implies`` (ServiceNode) and the wizard step
    loop (local ``service_aug_list``).
    """
    existing = {a.name for a in augments}
    changed = True
    while changed:
        changed = False
        for aug in list(augments):
            desc = AUGMENT_REGISTRY.get(aug.name)
            if desc is None:
                continue
            for implied in desc.implies:
                if implied not in existing:
                    augments.append(ServiceAugment(name=implied))
                    existing.add(implied)
                    changed = True


def _augment_missing_infra(aug_name: str, infra_features: set[str]) -> set[str]:
    """Return infra categories missing for an augment, considering its implies chain.

    Walks the ``implies`` chain transitively and collects all
    ``requires_infra`` from the augment and its implied augments.
    Returns the set of infra categories that are required but not
    present in *infra_features*.
    """
    visited: set[str] = set()
    required: set[str] = set()
    stack = [aug_name]
    while stack:
        name = stack.pop()
        if name in visited:
            continue
        visited.add(name)
        desc = AUGMENT_REGISTRY.get(name)
        if desc is None:
            continue
        required.update(desc.requires_infra)
        stack.extend(desc.implies)
    return required - infra_features


def _available_features_for_infra(infra_choices: list[str]) -> list[str]:
    """Derive selectable features from the workspace's configured infra."""

    feats: list[str] = []
    for cat_label, cat_members, _single in INFRA_CATEGORIES:
        if any(c in cat_members for c in infra_choices):
            feats.append(cat_label)
    return feats


def cancel_ok() -> int:
    """Exit current flow as a successful cancel."""

    print("Cancelled.")
    return 0


# ---------------------------------------------------------------------------
# Shared workspace finalization
# ---------------------------------------------------------------------------


def _cleanup_workspace(state: dict[str, object]) -> None:
    """Remove a partially-created workspace directory.

    Called by ``run_wizard`` via ``on_cancel`` when the user cancels or
    an interrupt occurs after the workspace directory was created.
    Only removes directories that were freshly created during this flow
    (never touches pre-existing directories).
    """

    import shutil

    output_dir = state.get("_output_dir")
    if output_dir is None:
        return

    output_path = Path(str(output_dir))
    if output_path.exists() and not state.get("_pre_existing"):
        shutil.rmtree(output_path, ignore_errors=True)
        print(f"Cleaned up partial workspace: {output_path}")


def _finalize_workspace(
    name: str,
    *,
    infra_choices: list[str],
    services: list[ServiceNode],
    git_init: bool,
    workspace_augments: list[str] | None = None,
    add_frontend: bool = False,
) -> int:
    """Create workspace, add infra/services, render, and print result.

    Shared by both manual and preset workspace creation flows.
    """

    output_dir = (Path.cwd().resolve() / name).resolve()
    compose_apply(output_dir, git_init=git_init)

    for infra_type in infra_choices:
        try:
            compose_add_infra(output_dir, InfraNode(type=infra_type))
            print(f'Added infra "{infra_type}".')
        except ValueError as exc:
            print(f"WARNING: {exc}")

    # Gateway auto-wiring: discover HTTP targets, wire auth
    _wire_gateway(services, workspace_augments or [])

    for svc in services:
        # Frontend services skip Python augment resolution but still get added to spec
        if svc.role != "frontend":
            # Resolve augment implications (e.g. crud-scaffold → db-config)
            _resolve_implies(svc)

            # Auto-apply augments (e.g. structured-logging) if not already present
            existing_aug_names = {a.name for a in svc.augments}
            for aug_name, desc in AUGMENT_REGISTRY.items():
                if desc.auto_apply and aug_name not in existing_aug_names:
                    svc.augments.append(ServiceAugment(name=aug_name))

            # Auto-derive features from augment prerequisites
            existing_features = set(svc.features)
            for aug in svc.augments:
                aug_desc = AUGMENT_REGISTRY.get(aug.name)
                if aug_desc is not None:
                    for req in aug_desc.requires_infra:
                        if req not in existing_features:
                            svc.features.append(req)
                            existing_features.add(req)

        try:
            compose_add_service(output_dir, svc)
        except ValueError as exc:
            print(f"WARNING: {exc}")

    for aug_name in workspace_augments or []:
        try:
            compose_add_workspace_augment(output_dir, aug_name)
        except ValueError as exc:
            print(f"WARNING: {exc}")

    render_workspace(output_dir)

    # Scaffold frontend after workspace is fully rendered (needs spec for gateway discovery)
    if add_frontend:
        frontend_dir = output_dir / "src" / _FRONTEND_SERVICE_NAME
        if not frontend_dir.exists():
            variables = _resolve_frontend_vars(output_dir)
            _scaffold_frontend(output_dir, variables)
            print(f"  Scaffolded src/{_FRONTEND_SERVICE_NAME}/")

    print(f"Generated workspace at: {output_dir}")
    return 0


def _wire_gateway(services: list[ServiceNode], workspace_augments: list[str]) -> None:
    """Auto-wire a gateway service if one exists in the service list.

    - When auth is active: gives gateway ``jwt-auth-consumer`` + ``auth-passthrough``,
      strips ``auth-passthrough`` from inner services
    - Enables actuator on inner services (safe — internal only behind gateway)
    """
    gateway = next((s for s in services if s.role == "gateway"), None)
    if gateway is None:
        return

    has_auth = "jwt-auth-provider" in workspace_augments

    # Auth wiring for gateway
    if has_auth:
        gw_aug_names = {a.name for a in gateway.augments}
        if "jwt-auth-consumer" not in gw_aug_names:
            gateway.augments.insert(0, ServiceAugment(name="jwt-auth-consumer"))
        if "auth-passthrough" not in gw_aug_names:
            idx = next(
                (i for i, a in enumerate(gateway.augments) if a.name == "jwt-auth-consumer"),
                0,
            )
            gateway.augments.insert(idx + 1, ServiceAugment(name="auth-passthrough"))

        # Strip auth-passthrough from inner services (gateway is the sole entry point)
        for svc in services:
            if svc.role == "gateway":
                continue
            svc.augments = [a for a in svc.augments if a.name != "auth-passthrough"]

    # Enable actuator on inner services (safe: only internal network can reach them)
    for svc in services:
        if svc.role in ("gateway", "worker"):
            continue
        svc.include_actuator = True


# ---------------------------------------------------------------------------
# Reusable wizard steps
# ---------------------------------------------------------------------------


def _step_workspace_name(state: dict[str, object]) -> None:
    """Wizard step: prompt for workspace name."""

    ws = _ws(state)
    default = ws.get("default_name", "my-workspace")
    workspace_raw = prompt_text("Workspace name", default=default)
    raw_name = workspace_raw or default

    name = resolve_workspace_name(raw_name)
    if raw_name.strip() and name != raw_name.strip():
        print(f"Normalized workspace name to: {name}")

    output_dir = (Path.cwd().resolve() / name).resolve()
    ws["name"] = name
    ws["_output_dir"] = output_dir
    ws["_pre_existing"] = output_dir.exists()


def _step_template(state: dict[str, object]) -> None:
    """Wizard step: select a template (blank or preset) to pre-fill state."""

    presets = list_presets()
    options = ["blank", *(p.name for p in presets)]
    chosen = prompt_single_select("Start from a template:", options, auto_select=False)

    if chosen is None or chosen == "blank":
        # Blank workspace — no pre-fill
        print("  Template: blank")
        state.setdefault("infra_choices", [])
        state.setdefault("services", [])
        state.setdefault("workspace_augments", [])
        state["_preset"] = None
        return

    preset = next(p for p in presets if p.name == chosen)
    print(f"  Template: {preset.name}")
    print(f"  {preset.description}")
    state["_preset"] = preset

    # Handle composable styles — multi-select of service patterns
    if preset.composable_styles:
        _resolve_composable_styles(preset, state)
        return

    # Non-composable preset — static services
    state["services"] = [s.model_copy() for s in preset.services]
    state["workspace_augments"] = list(preset.workspace_augments)

    # Resolve required infra inline
    infra_choices: list[str] = []
    _resolve_infra_categories(preset.required_infra_categories, infra_choices)

    # Optional infra categories — use preset order
    _resolve_optional_infra(preset.optional_infra_categories, infra_choices)

    state["infra_choices"] = infra_choices


def _resolve_infra_categories(
    required: list[str],
    infra_choices: list[str],
) -> None:
    """Prompt for required infra categories, appending to infra_choices."""
    for cat_label, cat_members, _single in INFRA_CATEGORIES:
        if cat_label in required:
            # Skip if already resolved
            if any(m in infra_choices for m in cat_members):
                continue
            sorted_members = sorted(cat_members)
            if len(sorted_members) == 1:
                print(f"  {cat_label}: {sorted_members[0]}")
                infra_choices.append(sorted_members[0])
            else:
                choice = prompt_single_select(f"Select {cat_label}:", sorted_members, inline=True)
                if choice is not None:
                    infra_choices.append(choice)


def _resolve_optional_infra(
    optional: list[str],
    infra_choices: list[str],
) -> None:
    """Prompt for optional infra categories, appending to infra_choices."""
    optional_cats: list[tuple[str, list[str]]] = []
    for opt_label in optional:
        for label, cat_members, _single in INFRA_CATEGORIES:
            if label == opt_label:
                if not any(m in infra_choices for m in cat_members):
                    optional_cats.append((label, sorted(cat_members)))
                break
    if optional_cats:
        opt_labels = [label for label, _ in optional_cats]
        selected = prompt_multi_select("Optional infrastructure:", opt_labels, inline=True)
        for label in selected:
            opt_members = next(m for cat_l, m in optional_cats if cat_l == label)
            if len(opt_members) == 1:
                print(f"  {label}: {opt_members[0]}")
                infra_choices.append(opt_members[0])
            else:
                choice = prompt_single_select(f"Select {label}:", opt_members, inline=True)
                if choice is not None:
                    infra_choices.append(choice)


def _resolve_composable_styles(
    preset: PresetDefinition,
    state: dict[str, object],
) -> None:
    """Handle a preset with composable styles: multi-select + auth wiring."""

    styles = preset.composable_styles
    labels = [f"{s.label} — {s.description}" for s in styles]

    # Multi-select styles (require at least one)
    while True:
        selected_labels = prompt_multi_select("Service styles (select at least one):", labels)
        if selected_labels:
            break
        print("  Please select at least one style.")

    selected_styles = [styles[labels.index(lbl)] for lbl in selected_labels]

    # Print selections
    for style in selected_styles:
        print(f"  ✓ {style.label}")

    # Set workspace augments
    state["workspace_augments"] = list(preset.workspace_augments)

    # Aggregate infra requirements from preset + selected styles
    infra_choices: list[str] = []
    all_required: list[str] = list(preset.required_infra_categories)
    for style in selected_styles:
        for cat in style.required_infra_categories:
            if cat not in all_required:
                all_required.append(cat)

    _resolve_infra_categories(all_required, infra_choices)

    # Optional infra from preset
    _resolve_optional_infra(preset.optional_infra_categories, infra_choices)

    state["infra_choices"] = infra_choices

    # Merge services from selected styles with auth wiring
    services: list[ServiceNode] = []
    used_names: set[str] = set()
    used_ports: set[int] = set()

    has_auth = "jwt-auth-provider" in preset.workspace_augments

    for style in selected_styles:
        for svc_template in style.services:
            svc = svc_template.model_copy()

            # Resolve name conflicts by prefixing with style name
            if svc.name in used_names:
                svc.name = f"{style.name}-{svc.name}"
            used_names.add(svc.name)

            # Assign non-conflicting port
            if svc.port != 0 and svc.port in used_ports:
                svc.port = _next_port(services, base=svc.port)
            if svc.port != 0:
                used_ports.add(svc.port)

            # Wire auth augments based on foreground/background
            if has_auth:
                existing_aug_names = {a.name for a in svc.augments}
                is_foreground = svc_template.name in style.foreground_services

                if "jwt-auth-consumer" not in existing_aug_names:
                    svc.augments.insert(0, ServiceAugment(name="jwt-auth-consumer"))

                if is_foreground and "auth-passthrough" not in existing_aug_names:
                    # Insert after jwt-auth-consumer
                    idx = next(
                        (i for i, a in enumerate(svc.augments) if a.name == "jwt-auth-consumer"),
                        0,
                    )
                    svc.augments.insert(idx + 1, ServiceAugment(name="auth-passthrough"))

            services.append(svc)

    # Auto-create role-based services required by workspace augments
    # (e.g. jwt-auth-provider requires an "auth" role service)
    for ws_aug_name in preset.workspace_augments:
        desc = AUGMENT_REGISTRY.get(ws_aug_name)
        if (
            desc
            and desc.applies_to_role
            and not any(s.role == desc.applies_to_role for s in services)
        ):
            auto_port = _next_port(services, base=8081)
            auto_svc = ServiceNode(
                name=f"{desc.applies_to_role}-service",
                role=desc.applies_to_role,
                port=auto_port,
                features=list(desc.requires_infra),
            )
            services.append(auto_svc)
            used_names.add(auto_svc.name)
            used_ports.add(auto_port)

    # Offer gateway service — routes all traffic through a single entry point.
    # Available for any preset, not just authenticated clusters.
    if not any(s.role == "gateway" for s in services):  # noqa: SIM102
        if prompt_yes_no("Add a gateway service? (single external entry point)"):
            gw_port = 8000  # outermost service gets the lowest port
            if gw_port in used_ports:
                gw_port = _next_port(services, base=8000)
            gw_svc = ServiceNode(
                name="gateway-service",
                role="gateway",
                port=gw_port,
                augments=[ServiceAugment(name="gateway-proxy")],
            )
            services.append(gw_svc)
            used_names.add(gw_svc.name)
            used_ports.add(gw_port)

            # Follow-up: offer frontend since gateway is the natural proxy target
            if prompt_yes_no("Add a Vue frontend? (login, signup, CRUD scaffold)"):
                fe_port = 3000
                if fe_port in used_ports:
                    fe_port = _next_port(services, base=3000)
                fe_svc = ServiceNode(
                    name="frontend",
                    role="frontend",
                    port=fe_port,
                )
                services.append(fe_svc)
                used_names.add(fe_svc.name)
                used_ports.add(fe_port)
                state["_add_frontend"] = True

    state["services"] = services


def _ensure_infra(category: str, state: dict[str, object]) -> None:
    """Ensure an infra category is configured, prompting if needed."""
    ws = _ws(state)
    infra_choices = ws.setdefault("infra_choices", [])
    for _label, members, _single in INFRA_CATEGORIES:
        if _label == category:
            if any(m in infra_choices for m in members):
                return  # already configured
            sorted_members = sorted(members)
            if len(sorted_members) == 1:
                print(f"  Auto-adding {category}: {sorted_members[0]}")
                infra_choices.append(sorted_members[0])
            else:
                choice = prompt_single_select(f"Select {category}:", sorted_members, inline=True)
                if choice is not None:
                    infra_choices.append(choice)
            return


# ---------------------------------------------------------------------------
# Auto-wiring helpers — generic dependency resolution
# ---------------------------------------------------------------------------


def _ensure_augment_deps(
    aug_name: str,
    *,
    service_aug_list: list[ServiceAugment],
    existing: list[ServiceNode],
    state: dict[str, object] | None,
    ws_aug_set: set[str],
    rebuild_available: object = None,
) -> None:
    """Generically ensure all dependencies for a newly-added augment.

    Walks the augment's ``requires_workspace_augment`` chain and the
    workspace augment's ``applies_to_role`` / ``requires_infra`` to
    auto-wire everything the augment needs.
    """
    desc = AUGMENT_REGISTRY.get(aug_name)
    if desc is None:
        return

    # 1. If this augment requires a workspace augment, ensure it exists
    ws_aug_name = desc.requires_workspace_augment
    if ws_aug_name and ws_aug_name not in ws_aug_set and state is not None:
        ws = _ws(state)
        ws_augs = ws.setdefault("workspace_augments", [])
        if ws_aug_name not in ws_augs:
            ws_augs.append(ws_aug_name)
            ws_aug_set.add(ws_aug_name)
            print(f"  ✓ {ws_aug_name} (auto-wired for {aug_name})")

            # The workspace augment itself may need infra + a role-specific service
            ws_desc = AUGMENT_REGISTRY.get(ws_aug_name)
            if ws_desc is not None:
                for req_infra in ws_desc.requires_infra:
                    _ensure_infra(req_infra, state)

                # Auto-create a service if the workspace augment needs a role
                if ws_desc.applies_to_role:
                    services = ws.get("services", [])
                    role_exists = any(s.role == ws_desc.applies_to_role for s in services) or any(
                        s.role == ws_desc.applies_to_role for s in existing
                    )
                    if not role_exists:
                        auto_port = _next_port(existing + services, base=8081)
                        auto_svc = ServiceNode(
                            name=f"{ws_desc.applies_to_role}-service",
                            role=ws_desc.applies_to_role,
                            port=auto_port,
                        )
                        services.append(auto_svc)
                        ws["services"] = services
                        print(
                            f"  ✓ {ws_desc.applies_to_role}-service on port {auto_port}"
                            f" (auto-wired for {ws_aug_name})"
                        )

            if callable(rebuild_available):
                rebuild_available()

    # 2. Ensure infra required by this augment directly
    if state is not None:
        for req_infra in desc.requires_infra:
            _ensure_infra(req_infra, state)


def _collect_option_prompts(
    augment_desc: object,
    *,
    options: dict[str, str | list[str]],
    service_aug_list: list[ServiceAugment],
    role: str | None,
    existing: list[ServiceNode],
    state: dict[str, object] | None,
    ws_aug_set: set[str],
    rebuild_available: object = None,
) -> None:
    """Walk ``OptionPrompt`` descriptors and collect answers + auto-wire deps.

    Replaces the hardcoded ``if key == "crud-scaffold":`` branching.
    """
    from ..compose.augments import OptionPrompt

    prompts: list[OptionPrompt] = getattr(augment_desc, "option_prompts", [])

    def _walk(prompt_list: list[OptionPrompt]) -> None:
        for op in prompt_list:
            if op.exclude_role and op.exclude_role == role:
                continue

            affirmative = False
            if op.kind == "text":
                try:
                    answer = prompt_text(op.prompt, default=op.default)
                except KeyboardInterrupt:
                    raise
                options[op.key] = answer
                affirmative = bool(answer)
            elif op.kind == "yes_no":
                affirmative = prompt_yes_no(op.prompt)

            if affirmative and op.adds_augments:
                existing_names = {a.name for a in service_aug_list}
                for added in op.adds_augments:
                    if added not in existing_names:
                        service_aug_list.append(ServiceAugment(name=added))
                        existing_names.add(added)
                        _ensure_augment_deps(
                            added,
                            service_aug_list=service_aug_list,
                            existing=existing,
                            state=state,
                            ws_aug_set=ws_aug_set,
                            rebuild_available=rebuild_available,
                        )

            if affirmative and op.follow_ups:
                _walk(op.follow_ups)

    _walk(prompts)


def _step_services(state: dict[str, object]) -> None:
    """Wizard step: show current services, loop to add more or apply presets."""

    ws = _ws(state)
    services = ws.get("services", [])
    applied_presets: set[str] = state.setdefault("_applied_presets", set())  # type: ignore[assignment]

    # Track the initial preset if one was chosen in _step_template
    preset = ws.get("_preset")
    if preset is not None and hasattr(preset, "name"):
        applied_presets.add(preset.name)

    # Show existing services
    if services:
        print("  Current services:")
        for svc in services:
            aug_str = ""
            if svc.augments:
                aug_str = f" [{', '.join(a.name for a in svc.augments)}]"
            print(f"    {svc.name} ({svc.role}) :{svc.port}{aug_str}")

    # Loop to add services or apply presets
    while True:
        # Build choices
        choices = ["add a service", "apply a preset", "done"]
        try:
            choice = prompt_single_select("Add more?", choices, inline=True)
        except KeyboardInterrupt:
            raise

        if choice is None or choice == "done":
            break
        if choice == "add a service":
            try:
                raw = prompt_text("Service name", default="")
            except KeyboardInterrupt:
                raise
            if not raw.strip():
                continue
            if raw.strip().lower() in {"back", "b"}:
                raise GoBack

            new_svc = _prompt_service(
                raw_name=raw,
                existing_services=services,
                preset=preset,
                state=state,
            )
            if new_svc is not None:
                services.append(new_svc)
                print(f'  Added service "{new_svc.name}" to spec.')

        elif choice == "apply a preset":
            _apply_preset_inline(state, services, applied_presets)

    ws["services"] = services


def _apply_preset_inline(
    state: dict[str, object],
    services: list[ServiceNode],
    applied_presets: set[str],
) -> None:
    """Present available presets and merge the chosen one into wizard state."""

    all_presets = list_presets()

    # Build labels, marking already-applied presets
    labels: list[str] = []
    available_indices: list[int] = []
    for i, p in enumerate(all_presets):
        if p.name in applied_presets:
            labels.append(f"{p.name}  ✓ already applied")
        else:
            labels.append(p.name)
            available_indices.append(i)

    if not available_indices:
        print("  All presets have been applied.")
        return

    try:
        chosen = prompt_single_select("Apply preset:", labels)
    except KeyboardInterrupt:
        raise

    if chosen is None:
        return

    # Find the selected preset
    chosen_name = chosen.split("  ✓")[0].strip()  # strip the marker if clicked on applied
    preset = next((p for p in all_presets if p.name == chosen_name), None)
    if preset is None:
        return

    if preset.name in applied_presets:
        print(f'  "{preset.name}" is already applied. Choose another.')
        return

    print(f"  Applying preset: {preset.name}")
    print(f"  {preset.description}")

    # Resolve required infra
    ws = _ws(state)
    infra_choices = ws.setdefault("infra_choices", [])

    for cat_label, cat_members, _single in INFRA_CATEGORIES:
        if cat_label in preset.required_infra_categories:
            # Skip if already configured
            if any(m in infra_choices for m in cat_members):
                continue
            sorted_members = sorted(cat_members)
            if len(sorted_members) == 1:
                print(f"  {cat_label}: {sorted_members[0]}")
                infra_choices.append(sorted_members[0])
            else:
                choice = prompt_single_select(f"Select {cat_label}:", sorted_members, inline=True)
                if choice is not None:
                    infra_choices.append(choice)

    # Optional infra categories
    optional_cats: list[tuple[str, list[str]]] = []
    for opt_label in preset.optional_infra_categories:
        for label, cat_members, _single in INFRA_CATEGORIES:
            if label == opt_label:
                # Skip if already configured
                if not any(m in infra_choices for m in cat_members):
                    optional_cats.append((label, sorted(cat_members)))
                break
    if optional_cats:
        opt_labels = [label for label, _ in optional_cats]
        selected = prompt_multi_select("Optional infrastructure:", opt_labels, inline=True)
        for label in selected:
            opt_members = next(m for cat_l, m in optional_cats if cat_l == label)
            if len(opt_members) == 1:
                print(f"  {label}: {opt_members[0]}")
                infra_choices.append(opt_members[0])
            else:
                choice = prompt_single_select(f"Select {label}:", opt_members, inline=True)
                if choice is not None:
                    infra_choices.append(choice)

    # Merge workspace augments
    ws_augments = ws.setdefault("workspace_augments", [])
    for aug_name in preset.workspace_augments:
        if aug_name not in ws_augments:
            ws_augments.append(aug_name)
            print(f"  ✓ workspace augment: {aug_name}")

    # Add preset services (skip name conflicts)
    existing_names = {s.name for s in services}
    added_count = 0
    for preset_svc in preset.services:
        if preset_svc.name in existing_names:
            print(f"  Skipping {preset_svc.name} (already exists)")
            continue
        # Assign a non-conflicting port
        new_svc = preset_svc.model_copy()
        existing_ports = {s.port for s in services}
        if new_svc.port in existing_ports:
            new_svc.port = _next_port(services, base=new_svc.port)
        services.append(new_svc)
        existing_names.add(new_svc.name)
        added_count += 1
        aug_str = ""
        if new_svc.augments:
            aug_str = f" [{', '.join(a.name for a in new_svc.augments)}]"
        print(f"  + {new_svc.name} ({new_svc.role}) :{new_svc.port}{aug_str}")

    applied_presets.add(preset.name)
    print(f"  Applied {preset.name}: {added_count} service(s) added.")


def _step_summary(state: dict[str, object]) -> None:
    """Wizard step: show summary and ask for confirmation.

    In TTY mode, Escape raises ``GoBack`` directly from inside
    ``prompt_yes_no`` — that propagates normally and lets the wizard
    navigate back to the services step.

    A ``"no"`` answer (or EOF in piped / non-TTY mode) means the user
    wants to **cancel** the wizard, not loop back.  We raise
    ``KeyboardInterrupt`` so ``run_wizard`` invokes the cleanup callback
    and terminates cleanly.
    """

    ws = _ws(state)
    name = ws.get("name", "workspace")
    infra_choices = ws.get("infra_choices", [])
    ws_augments = ws.get("workspace_augments", [])
    services = ws.get("services", [])

    _print_summary(name, infra_choices, ws_augments, services)

    if not prompt_yes_no("Generate?"):
        raise KeyboardInterrupt


def _step_git_init(state: dict[str, object]) -> None:
    """Wizard step: prompt for git init."""

    state["git_init"] = prompt_yes_no("Initialize git repository?")


# ---------------------------------------------------------------------------
# Service prompts (reused by workspace and add-service flows)
# ---------------------------------------------------------------------------


class _SvcState(TypedDict, total=False):
    """Typed view of the service sub-wizard state dict."""

    # Context (set in initial_state, read-only for steps)
    _raw_name: str | None
    _existing: list[ServiceNode]
    _outer_state: dict[str, object] | None
    _ws_aug_set: set[str]
    _infra_fallback: list[str]
    _augment_descs: list[tuple[str, AugmentDescriptor]]
    _preset: PresetDefinition | None
    _preset_defaults: set[str]
    _preset_optionals: set[str]

    # Rebuilt by _rebuild_available_augs
    _infra_features: set[str]
    _available_augs: list[tuple[str, str]]
    _disabled_aug_names: set[str]
    _auto_apply_augs: list[str]

    # Outputs (written by steps)
    name: str
    role: str
    port: int
    features: list[str]
    service_aug_list: list[ServiceAugment]


def _ss(state: dict[str, object]) -> _SvcState:
    """Narrow untyped wizard state to ``_SvcState``."""
    return cast(_SvcState, state)


def _compute_infra_features(
    outer_state: dict[str, object] | None,
    infra_choices_fallback: list[str],
) -> set[str]:
    """Derive infra feature categories from wizard state or legacy params."""
    src: list[str]
    if outer_state is not None:
        src = _ws(outer_state).get("infra_choices", [])
    else:
        src = infra_choices_fallback
    feats: set[str] = set()
    for cat_label, cat_members, _single in INFRA_CATEGORIES:
        if any(c in src for c in cat_members):
            feats.add(cat_label)
    return feats


def _rebuild_available_augs(s: dict[str, object]) -> None:
    """Rebuild available augments list after infra/ws-augment changes.

    Reads and writes shared keys in the sub-wizard state dict.
    """
    st = _ss(s)
    outer_state = st.get("_outer_state")
    infra_fallback = st.get("_infra_fallback", [])
    ws_aug_set = st["_ws_aug_set"]
    augment_descs = st["_augment_descs"]

    infra_features = _compute_infra_features(outer_state, infra_fallback)
    st["_infra_features"] = infra_features

    available: list[tuple[str, str]] = []
    disabled: set[str] = set()
    auto_apply: list[str] = []

    for aug_name, desc in augment_descs:
        if desc.requires_workspace_augment and desc.requires_workspace_augment not in ws_aug_set:
            continue
        if desc.auto_apply:
            if aug_name not in auto_apply:
                auto_apply.append(aug_name)
            continue
        if desc.hidden:
            continue
        if outer_state is not None:
            available.append((aug_name, desc.description))
        else:
            missing = _augment_missing_infra(aug_name, infra_features)
            if missing:
                note = ", ".join(sorted(missing))
                available.append((aug_name, f"{desc.description} (requires {note})"))
                disabled.add(aug_name)
            else:
                available.append((aug_name, desc.description))

    st["_available_augs"] = available
    st["_disabled_aug_names"] = disabled
    st["_auto_apply_augs"] = auto_apply


# -- Step 0: Name ----------------------------------------------------------


def _svc_step_name(s: dict[str, object]) -> None:
    """Prompt for service name with normalization."""
    st = _ss(s)
    raw_name = st.get("_raw_name")

    # First pass with caller-provided name — skip prompt
    if raw_name is not None and "name" not in st:
        name = normalize_service_name(raw_name)
        if name != raw_name.strip():
            print(f"  Normalized to: {name}")
        st["name"] = name
        return

    current = st.get("name", "my-service")
    entered = prompt_text("Service name", default=current)
    # GoBack propagates automatically → wizard cancels at step 0

    name = normalize_service_name(entered)
    if name != entered.strip():
        print(f"  Normalized to: {name}")
    st["name"] = name


# -- Step 1: Role ----------------------------------------------------------


def _svc_step_role(s: dict[str, object]) -> None:
    """Prompt for service role with singleton detection and auto-wiring."""
    st = _ss(s)
    existing = st.get("_existing", [])
    outer_state = st.get("_outer_state")
    ws_aug_set = st["_ws_aug_set"]

    claimed_roles = {svc.role for svc in existing}
    disabled_indices: set[int] = set()
    role_options: list[str] = []

    for i, r in enumerate(_VALID_ROLES):
        if r in _SINGLETON_ROLES and r in claimed_roles:
            role_options.append(f"{r} (already configured)")
            disabled_indices.add(i)
        else:
            role_options.append(r)

    name: str = st["name"]
    suggested = _infer_role(name)

    chosen = prompt_single_select(
        "Role:",
        role_options,
        auto_select=False,
        disabled=disabled_indices,
    )
    # GoBack propagates automatically → wizard goes back to step 0

    role = suggested if chosen is None else chosen.split(" (")[0]
    print(f"  Role: {role}")
    st["role"] = role

    # Auto-wire workspace augments + infra from role descriptor
    role_desc = ROLE_REGISTRY.get(role)
    if role_desc is not None and outer_state is not None:
        ws_augs = _ws(outer_state).setdefault("workspace_augments", [])
        for ws_aug_name in role_desc.implies_workspace_augments:
            if ws_aug_name not in ws_augs:
                ws_augs.append(ws_aug_name)
                ws_aug_set.add(ws_aug_name)
                print(f"  ✓ {ws_aug_name} (auto-wired for {role} role)")
        for req_infra in role_desc.requires_infra:
            _ensure_infra(req_infra, outer_state)
        if role_desc.implies_workspace_augments or role_desc.requires_infra:
            _rebuild_available_augs(s)


# -- Step 2: Capabilities --------------------------------------------------


def _svc_step_capabilities(s: dict[str, object]) -> None:
    """Prompt for augment selection with auto-wiring and feature derivation."""
    st = _ss(s)
    role = st["role"]
    existing = st.get("_existing", [])
    outer_state = st.get("_outer_state")
    ws_aug_set = st["_ws_aug_set"]
    preset = st.get("_preset")
    preset_defaults: set[str] = st.get("_preset_defaults", set())
    preset_optionals: set[str] = st.get("_preset_optionals", set())
    available_augs: list[tuple[str, str]] = st.get("_available_augs", [])
    disabled_aug_names: set[str] = st.get("_disabled_aug_names", set())
    auto_apply_augs: list[str] = st.get("_auto_apply_augs", [])

    features: list[str] = []
    service_aug_list: list[ServiceAugment] = []

    # Auto-apply augments (e.g. structured-logging)
    for aug_name in auto_apply_augs:
        service_aug_list.append(ServiceAugment(name=aug_name))

    # Auto-wire service augments implied by role (e.g. worker → celery-worker)
    role_desc = ROLE_REGISTRY.get(role)
    if role_desc is not None:
        existing_augs = {a.name for a in service_aug_list}
        for aug_name in role_desc.implies_service_augments:
            if aug_name not in existing_augs:
                service_aug_list.append(ServiceAugment(name=aug_name))
                print(f"  ✓ {aug_name} (auto-wired for {role} role)")

    capability_items: list[tuple[str, str, str]] = []  # (kind, key, label)
    if preset and preset_defaults:
        for aug_name, _desc_str in available_augs:
            if aug_name in preset_defaults:
                service_aug_list.append(ServiceAugment(name=aug_name))
                print(f"  ✓ {aug_name} (from template)")
        for aug_name, desc_str in available_augs:
            if aug_name in preset_optionals:
                capability_items.append(("augment", aug_name, f"{aug_name} — {desc_str}"))
    else:
        for aug_name, desc_str in available_augs:
            capability_items.append(("augment", aug_name, f"{aug_name} — {desc_str}"))

    if capability_items:
        labels = [lbl for _, _, lbl in capability_items]
        disabled_cap_indices = {
            i for i, (_, key, _) in enumerate(capability_items) if key in disabled_aug_names
        }
        selected_labels = prompt_multi_select(
            "Capabilities:",
            labels,
            disabled=disabled_cap_indices,
            auto_select_on_enter=True,
        )
        # GoBack propagates automatically → wizard goes back to step 1

        if selected_labels:
            selected_keys = [capability_items[labels.index(lbl)][1] for lbl in selected_labels]
            print(f"  Capabilities: {', '.join(selected_keys)}")

        for lbl in selected_labels:
            _kind, key, _ = capability_items[labels.index(lbl)]
            aug_desc = AUGMENT_REGISTRY[key]
            options: dict[str, str | list[str]] = {}

            if aug_desc.option_prompts:
                _collect_option_prompts(
                    aug_desc,
                    options=options,
                    service_aug_list=service_aug_list,
                    role=role,
                    existing=existing,
                    state=outer_state,
                    ws_aug_set=ws_aug_set,
                    rebuild_available=lambda: _rebuild_available_augs(s),
                )

            if aug_desc.needs_target_selection:
                other_names = [svc.name for svc in existing]
                if other_names:
                    targets = prompt_multi_select("Delegate targets:", other_names)
                    options["targets"] = targets

            service_aug_list.append(ServiceAugment(name=key, options=options))

    # Resolve augment implications (e.g. crud-scaffold → db-config)
    _resolve_implies_list(service_aug_list)

    # Standalone JWT wiring prompt — when jwt-auth-provider is active and
    # the service doesn't already have jwt-auth-consumer (e.g. from
    # crud-scaffold's follow-up), offer to protect this service.
    existing_aug_names = {a.name for a in service_aug_list}
    if "jwt-auth-provider" in ws_aug_set and "jwt-auth-consumer" not in existing_aug_names:  # noqa: SIM102
        if prompt_yes_no("Protect with token auth?"):
            service_aug_list.append(ServiceAugment(name="jwt-auth-consumer"))
            existing_aug_names.add("jwt-auth-consumer")
            print("  ✓ jwt-auth-consumer")
            # Follow-up: passthrough (foreground services only)
            if role != "worker" and role != "auth":  # noqa: SIM102
                if prompt_yes_no("Expose login/signup endpoints on this service?"):
                    service_aug_list.append(ServiceAugment(name="auth-passthrough"))
                    print("  ✓ auth-passthrough")

    # Auto-derive features from augment prerequisites
    for aug in service_aug_list:
        desc = AUGMENT_REGISTRY.get(aug.name)
        if desc is not None:
            for req in desc.requires_infra:
                if req not in features:
                    features.append(req)
                if outer_state is not None:
                    _ensure_infra(req, outer_state)

    if outer_state is not None:
        st["_infra_features"] = _compute_infra_features(outer_state, [])

    st["features"] = features
    st["service_aug_list"] = service_aug_list


# -- Step 3: Port ----------------------------------------------------------


def _svc_step_port(s: dict[str, object]) -> None:
    """Prompt for service port."""
    st = _ss(s)
    existing = st.get("_existing", [])
    default_port = _next_port(existing)

    port_raw = prompt_text("Port", default=str(default_port))
    # GoBack propagates automatically → wizard goes back to step 2

    try:
        port = int(port_raw)
    except ValueError:
        print(f"  Invalid port '{port_raw}', defaulting to {default_port}.")
        port = default_port

    st["port"] = port


# -- Orchestrator -----------------------------------------------------------


def _prompt_service(
    *,
    raw_name: str | None = None,
    existing_services: list[ServiceNode] | None = None,
    workspace_augments: list[str] | None = None,
    infra_choices: list[str] | None = None,
    preset: PresetDefinition | None = None,
    state: dict[str, object] | None = None,
) -> ServiceNode | None:
    """Interactively collect service details.  Returns ``None`` on cancel.

    Uses ``run_wizard`` with four steps so Escape navigates back through:
    name → role → capabilities → port.

    When *state* is provided (wizard flow), infra and workspace augments
    are auto-derived from the selected role and capabilities — no upfront
    infra selection needed.  All augments are shown; selecting one that
    needs infra triggers an inline prompt.

    When *state* is ``None`` (add-service to existing workspace), falls
    back to *infra_choices* and *workspace_augments* for filtering.
    """

    existing = existing_services or []

    # Derive ws augment set and infra fallback from context
    ws_aug_set: set[str]
    infra_fallback: list[str]
    if state is not None:
        ws = _ws(state)
        ws_aug_set = set(ws.get("workspace_augments", []))
        infra_fallback = ws.get("infra_choices", [])
    else:
        ws_aug_set = set(workspace_augments or [])
        infra_fallback = list(infra_choices or [])

    augment_descs = [(n, d) for n, d in sorted(AUGMENT_REGISTRY.items()) if d.scope == "service"]

    preset_defaults = set(preset.default_service_augments) if preset else set()
    preset_optionals = set(preset.optional_service_augments) if preset else set()

    # Build sub-wizard initial state
    sub_state: dict[str, object] = {
        "_raw_name": raw_name,
        "_existing": existing,
        "_outer_state": state,
        "_ws_aug_set": ws_aug_set,
        "_infra_fallback": infra_fallback,
        "_augment_descs": augment_descs,
        "_preset": preset,
        "_preset_defaults": preset_defaults,
        "_preset_optionals": preset_optionals,
    }

    # Seed available augments
    _rebuild_available_augs(sub_state)

    result = run_wizard(
        [_svc_step_name, _svc_step_role, _svc_step_capabilities, _svc_step_port],
        initial_state=sub_state,
    )

    if result is None or result.get(_WIZARD_INTERRUPTED):
        return None

    return ServiceNode(
        name=result["name"],
        role=result["role"],
        port=result["port"],
        features=result["features"],
        augments=result["service_aug_list"],
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def _print_summary(
    name: str,
    infra_choices: list[str],
    workspace_augments: list[str],
    services: list[ServiceNode],
) -> None:
    """Print a formatted summary of what will be generated."""

    # Build content lines first, then size the box to fit
    lines: list[str] = []
    lines.append(f" Workspace: {name}")
    if infra_choices:
        lines.append(f" Infra: {', '.join(infra_choices)}")
    if workspace_augments:
        lines.append(f" Augments: {', '.join(workspace_augments)}")
    lines.append("")
    if services:
        lines.append(" Services:")
        for svc in services:
            lines.append(f"   {svc.name} ({svc.role}) :{svc.port}")
            if svc.augments:
                aug_str = ", ".join(a.name for a in svc.augments)
                lines.append(f"     └ {aug_str}")
    else:
        lines.append(" Services: (none)")
    lines.append("")
    lines.append(" Files: docker-compose.yml, .env.example")

    width = max(len(line) for line in lines) + 4  # right padding
    width = max(width, 40)  # minimum

    print()
    print(f"┌{'─' * width}┐")
    for line in lines:
        print(f"│{line:<{width}}│")
    print(f"└{'─' * width}┘")
    print()


# ---------------------------------------------------------------------------
# Infrastructure prompts (category-based)
# ---------------------------------------------------------------------------


def _prompt_infra_categories(
    existing: set[str] | None = None,
) -> list[str]:
    """Walk through infra categories and collect specific selections.

    1. Multi-select which categories to add (database, messaging, caching).
    2. For each selected category, prompt for the specific type.
       - Single-option categories auto-select.
       - Multi-option categories (database) show a single-select.

    Escape at the category multi-select raises ``GoBack``.
    Escape at a sub-select loops back to the category multi-select.

    Returns a flat list of infra type strings.
    """

    existing = existing or set()

    # Build available categories (skip if all members are already present)
    available_categories: list[tuple[str, list[str], bool]] = []
    for label, members, single in INFRA_CATEGORIES:
        available_members = sorted(m for m in members if m not in existing)
        if available_members:
            available_categories.append((label, available_members, single))

    if not available_categories:
        return []

    while True:
        # Step 1: select categories (GoBack propagates to caller)
        cat_labels = [label for label, _, _ in available_categories]
        selected_labels = prompt_multi_select("Select infrastructure categories:", cat_labels)
        if not selected_labels:
            return []

        # Step 2: for each selected category, pick specific type
        result: list[str] = []
        restarted = False
        for label, avail_members, _single in available_categories:
            if label not in selected_labels:
                continue

            if len(avail_members) == 1:
                # Auto-select the only option
                print(f"  {label}: {avail_members[0]}")
                result.append(avail_members[0])
            else:
                try:
                    choice = prompt_single_select(f"Select {label}:", avail_members)
                except GoBack:
                    # Go back to category selection
                    restarted = True
                    break
                if choice is not None:
                    result.append(choice)

        if restarted:
            continue
        return result


# ---------------------------------------------------------------------------
# Workspace handler
# ---------------------------------------------------------------------------


def _apply_workspace(
    workspace_name: str,
    *,
    git_init: bool = False,
) -> int:
    """Create workspace, render baseline, and print result."""

    try:
        normalized = resolve_workspace_name(workspace_name)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    if workspace_name.strip() and normalized != workspace_name.strip():
        print(f"Normalized workspace name to: {normalized}")

    output_dir = (Path.cwd().resolve() / normalized).resolve()
    compose_apply(output_dir, git_init=git_init)
    print(f"Generated workspace at: {output_dir}")
    return 0


def create_workspace(default_name: str = "my-workspace") -> int:
    """Unified workspace flow using the step wizard.

    Steps: name → template → services → summary → git init.

    Infra and workspace augments are auto-derived from service roles and
    capabilities — no separate infra or augment selection steps.
    Presets pre-fill wizard state; blank starts empty.
    """

    steps: list[WizardStep] = [
        _step_workspace_name,
        _step_template,
        _step_services,
        _step_summary,
        _step_git_init,
    ]

    state: dict[str, object] = {"default_name": default_name}
    result = run_wizard(steps, on_cancel=_cleanup_workspace, initial_state=state)
    if result is None:
        return 0
    if result.get(_WIZARD_INTERRUPTED):
        return 1

    ws = _ws(result)
    return _finalize_workspace(
        ws.get("name", "workspace"),
        infra_choices=ws.get("infra_choices", []),
        services=ws.get("services", []),
        git_init=ws.get("git_init", False),
        workspace_augments=ws.get("workspace_augments", []),
        add_frontend=bool(result.get("_add_frontend")),
    )


def create_workspace_direct(
    workspace_name: str = "my-workspace",
    *,
    git_init: bool = False,
) -> int:
    """Direct (non-interactive) workspace creation."""

    return _apply_workspace(workspace_name, git_init=git_init)


# ---------------------------------------------------------------------------
# Add service handler
# ---------------------------------------------------------------------------


def add_service_interactive() -> int:
    """Prompt for service details and append to the current workspace spec."""

    workspace_dir = Path.cwd().resolve()

    # Load existing services for port awareness and augment prerequisites
    configured = configured_infra(workspace_dir)
    sp = spec_file_path(workspace_dir)
    existing_services: list[ServiceNode] = []
    ws_augments: list[str] = []
    if sp.is_file():
        spec = load_spec(sp)
        existing_services = list(spec.services)
        ws_augments = [a.name for a in spec.workspace.augments]

    try:
        svc = _prompt_service(
            existing_services=existing_services,
            workspace_augments=ws_augments,
            infra_choices=configured,
        )
    except GoBack:
        print("Cancelled.")
        return 0
    if svc is None:
        print("Cancelled.")
        return 0

    try:
        compose_add_service(workspace_dir, svc)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    # Add service augments
    for aug in svc.augments:
        try:
            compose_add_service_augment(workspace_dir, svc.name, aug.name, dict(aug.options))
        except ValueError as exc:
            print(f"WARNING: {exc}")

    render_workspace(workspace_dir)
    print(f'Added service "{svc.name}" to {workspace_dir / "csrd-compose.yaml"}')
    return 0


def add_service_direct(
    *,
    name: str,
    port: int = 8080,
    features: list[str] | None = None,
) -> int:
    """Non-interactive service addition to the current workspace spec."""

    service_name = normalize_service_name(name)
    svc = ServiceNode(name=service_name, port=port, features=features or [])

    # Auto-apply augments
    for aug_name, desc in AUGMENT_REGISTRY.items():
        if desc.auto_apply:
            svc.augments.append(ServiceAugment(name=aug_name))

    # Resolve implies and auto-derive features
    _resolve_implies(svc)

    workspace_dir = Path.cwd().resolve()
    try:
        compose_add_service(workspace_dir, svc)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    render_workspace(workspace_dir)
    print(f'Added service "{svc.name}" to {workspace_dir / "csrd-compose.yaml"}')
    return 0


# ---------------------------------------------------------------------------
# Add augment handler
# ---------------------------------------------------------------------------


def add_augment_interactive() -> int:
    """Prompt for augment scope (workspace/service), select augments, and add."""

    workspace_dir = Path.cwd().resolve()
    sp = spec_file_path(workspace_dir)
    if not sp.is_file():
        print("ERROR: No workspace found. Run from inside a workspace directory.")
        return 1

    spec = load_spec(sp)

    try:
        scope = prompt_single_select("Augment scope:", ["workspace", "service"])
    except GoBack:
        print("Cancelled.")
        return 0
    except KeyboardInterrupt:
        with suppress(KeyboardInterrupt):
            print("\nCancelled.")
        return 1

    if scope == "workspace":
        avail = available_workspace_augments(workspace_dir)
        if not avail:
            print("No workspace augments available (all added or prerequisites unmet).")
            return 0
        # Build labels with descriptions
        labels = []
        for aug_name in avail:
            desc = AUGMENT_REGISTRY.get(aug_name)
            lbl = f"{aug_name} — {desc.description}" if desc else aug_name
            labels.append(lbl)
        try:
            selected = prompt_multi_select("Workspace augments:", labels)
        except GoBack:
            print("No augments selected.")
            return 0
        except KeyboardInterrupt:
            with suppress(KeyboardInterrupt):
                print("\nCancelled.")
            return 1

        for lbl in selected:
            aug_name = avail[labels.index(lbl)]
            try:
                compose_add_workspace_augment(workspace_dir, aug_name)
                print(f'Added workspace augment "{aug_name}".')
            except ValueError as exc:
                print(f"WARNING: {exc}")

            # Auto-create service if needed
            desc = AUGMENT_REGISTRY.get(aug_name)
            if desc and desc.applies_to_role:
                spec = load_spec(sp)
                roles = {s.role for s in spec.services}
                if desc.applies_to_role not in roles:
                    port = next_available_port(spec)
                    svc_name = f"{desc.applies_to_role}-service"
                    features = _available_features_for_infra([i.type for i in spec.infra])
                    svc = ServiceNode(
                        name=svc_name,
                        role=desc.applies_to_role,
                        port=port,
                        features=features,
                    )
                    try:
                        compose_add_service(workspace_dir, svc)
                        print(
                            f"  {aug_name} requires {desc.applies_to_role} service "
                            f"— added {svc_name} on port {port}"
                        )
                    except ValueError as exc:
                        print(f"WARNING: {exc}")

    elif scope == "service":
        if not spec.services:
            print("No services in workspace. Add a service first.")
            return 0
        svc_names = [s.name for s in spec.services]
        try:
            svc_name = prompt_single_select("Which service?", svc_names)
        except GoBack:
            print("Cancelled.")
            return 0
        except KeyboardInterrupt:
            with suppress(KeyboardInterrupt):
                print("\nCancelled.")
            return 1

        if svc_name is None:
            print("Cancelled.")
            return 0

        avail = available_service_augments(workspace_dir, svc_name)
        if not avail:
            print(f"No augments available for {svc_name}.")
            return 0

        labels = []
        for aug_name in avail:
            desc = AUGMENT_REGISTRY.get(aug_name)
            lbl = f"{aug_name} — {desc.description}" if desc else aug_name
            labels.append(lbl)

        try:
            selected = prompt_multi_select("Service augments:", labels)
        except GoBack:
            print("No augments selected.")
            return 0
        except KeyboardInterrupt:
            with suppress(KeyboardInterrupt):
                print("\nCancelled.")
            return 1

        for lbl in selected:
            aug_name = avail[labels.index(lbl)]
            aug_desc = AUGMENT_REGISTRY.get(aug_name)
            options: dict[str, str | list[str]] = {}

            # Data-driven option prompts (text-only in add-augment flow)
            if aug_desc and aug_desc.option_prompts:
                for op in aug_desc.option_prompts:
                    if op.kind == "text":
                        try:
                            answer = prompt_text(op.prompt, default=op.default)
                        except KeyboardInterrupt:
                            with suppress(KeyboardInterrupt):
                                print("\nCancelled.")
                            return 1
                        options[op.key] = answer

            if aug_desc and aug_desc.needs_target_selection:
                other = [s.name for s in spec.services if s.name != svc_name]
                if other:
                    try:
                        targets = prompt_multi_select("Delegate targets:", other)
                    except (GoBack, KeyboardInterrupt):
                        with suppress(KeyboardInterrupt):
                            print("\nCancelled.")
                        return 1
                    options["targets"] = targets

            try:
                compose_add_service_augment(workspace_dir, svc_name, aug_name, options or None)
                print(f'Added augment "{aug_name}" to {svc_name}.')
            except ValueError as exc:
                print(f"WARNING: {exc}")

    render_workspace(workspace_dir)
    return 0


def add_augment_direct(
    *,
    scope: str,
    augment_name: str,
    service_name: str | None,
    options: dict[str, str | list[str]] | None = None,
) -> int:
    """Non-interactive augment addition."""

    workspace_dir = Path.cwd().resolve()

    try:
        if scope == "workspace":
            compose_add_workspace_augment(workspace_dir, augment_name, options)
        elif scope == "service":
            if service_name is None:
                print("ERROR: --service-name required for service-scope augments.")
                return 1
            compose_add_service_augment(workspace_dir, service_name, augment_name, options)
        else:
            print(f"ERROR: Unknown scope '{scope}'. Use 'workspace' or 'service'.")
            return 1
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    render_workspace(workspace_dir)
    print(f'Added augment "{augment_name}".')
    return 0


# ---------------------------------------------------------------------------
# Remove service handler
# ---------------------------------------------------------------------------


def remove_service_interactive() -> int:
    """Prompt user to select a service to remove from the workspace."""

    workspace_dir = Path.cwd().resolve()
    sp = spec_file_path(workspace_dir)
    if not sp.is_file():
        print("ERROR: No workspace found.")
        return 1

    spec = load_spec(sp)

    if not spec.services:
        print("No services to remove.")
        return 0

    svc_names = [s.name for s in spec.services]

    try:
        chosen = prompt_single_select("Remove which service?", svc_names, auto_select=False)
    except GoBack:
        print("Cancelled.")
        return 0
    except KeyboardInterrupt:
        with suppress(KeyboardInterrupt):
            print("\nCancelled.")
        return 1

    if chosen is None:
        print("Cancelled.")
        return 0

    # Warn about dependents
    svc = next(s for s in spec.services if s.name == chosen)
    dependents: list[str] = []
    for other_svc in spec.services:
        if other_svc.name == chosen:
            continue
        for aug in other_svc.augments:
            desc = AUGMENT_REGISTRY.get(aug.name)
            if desc and desc.requires_service_in_spec == svc.role:
                dependents.append(other_svc.name)
                break
            # Check delegate targets
            targets = aug.options.get("targets", [])
            if isinstance(targets, str):
                targets = [targets]
            if chosen in targets:
                dependents.append(other_svc.name)
                break

    if dependents:
        print(f"  WARNING: {', '.join(dependents)} depend on {chosen}.")
        if not prompt_yes_no("Continue removing?", default=False):
            print("Cancelled.")
            return 0

    try:
        compose_remove_service(workspace_dir, chosen)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    render_workspace(workspace_dir)
    print(f'Removed service "{chosen}" from {workspace_dir / "csrd-compose.yaml"}')
    return 0


def remove_service_direct(*, service_name: str) -> int:
    """Non-interactive service removal."""

    workspace_dir = Path.cwd().resolve()

    try:
        compose_remove_service(workspace_dir, service_name)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    render_workspace(workspace_dir)
    print(f'Removed service "{service_name}" from {workspace_dir / "csrd-compose.yaml"}')
    return 0


# ---------------------------------------------------------------------------
# Rename service handler
# ---------------------------------------------------------------------------


def _rename_service_dirs(workspace_dir: Path, old_name: str, new_name: str) -> None:
    """Rename filesystem artifacts after a spec rename.

    Moves ``src/<old_snake>`` → ``src/<new_snake>``, equivalent test
    directories, ``Dockerfile.<old>`` → ``Dockerfile.<new>``, and
    rewrites all ``.py`` files in the affected directories to replace
    old service name references (both kebab-case and snake_case).
    Skips silently when source does not exist.
    """

    old_snake = old_name.replace("-", "_")
    new_snake = new_name.replace("-", "_")

    # Rename directories
    dir_pairs = [
        (workspace_dir / "src" / old_snake, workspace_dir / "src" / new_snake),
        (
            workspace_dir / "tests" / "unit" / old_snake,
            workspace_dir / "tests" / "unit" / new_snake,
        ),
        (
            workspace_dir / "tests" / "acceptance" / old_snake,
            workspace_dir / "tests" / "acceptance" / new_snake,
        ),
    ]

    for src, dst in dir_pairs:
        if src.is_dir() and not dst.exists():
            src.rename(dst)

    # Rewrite Python files in renamed directories
    rewrite_dirs = [
        workspace_dir / "src" / new_snake,
        workspace_dir / "tests" / "unit" / new_snake,
        workspace_dir / "tests" / "acceptance" / new_snake,
    ]
    for d in rewrite_dirs:
        if d.is_dir():
            _rewrite_refs_in_dir(d, old_name, new_name, old_snake, new_snake)

    # Rename Dockerfile
    old_dockerfile = workspace_dir / f"Dockerfile.{old_name}"
    new_dockerfile = workspace_dir / f"Dockerfile.{new_name}"
    if old_dockerfile.is_file() and not new_dockerfile.exists():
        content = old_dockerfile.read_text(encoding="utf-8")
        content = content.replace(old_snake, new_snake)
        content = content.replace(old_name, new_name)
        new_dockerfile.write_text(content, encoding="utf-8")
        old_dockerfile.unlink()


def _rewrite_refs_in_dir(
    directory: Path,
    old_name: str,
    new_name: str,
    old_snake: str,
    new_snake: str,
) -> None:
    """Replace old service name references in all ``.py`` files under *directory*."""

    for py_file in directory.rglob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        updated = content.replace(old_snake, new_snake).replace(old_name, new_name)
        if updated != content:
            py_file.write_text(updated, encoding="utf-8")


def rename_service_interactive() -> int:
    """Prompt user to select a service and provide a new name."""

    workspace_dir = Path.cwd().resolve()
    sp = spec_file_path(workspace_dir)
    if not sp.is_file():
        print("ERROR: No workspace found.")
        return 1

    spec = load_spec(sp)

    if not spec.services:
        print("No services to rename.")
        return 0

    svc_names = [s.name for s in spec.services]

    try:
        chosen = prompt_single_select("Rename which service?", svc_names, auto_select=False)
    except GoBack:
        print("Cancelled.")
        return 0
    except KeyboardInterrupt:
        with suppress(KeyboardInterrupt):
            print("\nCancelled.")
        return 1

    if chosen is None:
        print("Cancelled.")
        return 0

    try:
        raw_new = prompt_text("New name", default="")
    except GoBack:
        print("Cancelled.")
        return 0
    except KeyboardInterrupt:
        with suppress(KeyboardInterrupt):
            print("\nCancelled.")
        return 1

    if not raw_new:
        print("No name entered — cancelled.")
        return 0

    new_name = normalize_service_name(raw_new)

    try:
        compose_rename_service(workspace_dir, chosen, new_name)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    _rename_service_dirs(workspace_dir, chosen, new_name)
    render_workspace(workspace_dir)
    print(f'Renamed service "{chosen}" → "{new_name}"')
    return 0


def rename_service_direct(*, old_name: str, new_name: str) -> int:
    """Non-interactive service rename."""

    workspace_dir = Path.cwd().resolve()
    new_name = normalize_service_name(new_name)

    try:
        compose_rename_service(workspace_dir, old_name, new_name)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    _rename_service_dirs(workspace_dir, old_name, new_name)
    render_workspace(workspace_dir)
    print(f'Renamed service "{old_name}" → "{new_name}"')
    return 0


# ---------------------------------------------------------------------------
# Add infra handler
# ---------------------------------------------------------------------------


def add_infra_interactive() -> int:
    """Category-based infra selection and addition to the current workspace spec."""

    workspace_dir = Path.cwd().resolve()
    avail = available_infra(workspace_dir)

    if not avail:
        print("All infrastructure types are already configured.")
        return 0

    # Determine what's already configured so categories hide filled slots
    sp = spec_file_path(workspace_dir)
    existing: set[str] = set()
    if sp.is_file():
        spec = load_spec(sp)
        existing = {i.type for i in spec.infra}

    try:
        choices = _prompt_infra_categories(existing)
    except GoBack:
        print("No infrastructure selected.")
        return 0
    except KeyboardInterrupt:
        with suppress(KeyboardInterrupt):
            print("\nCancelled.")
        return 1

    if not choices:
        print("No infrastructure selected.")
        return 0

    for infra_type in choices:
        infra = InfraNode(type=infra_type)
        try:
            compose_add_infra(workspace_dir, infra)
            print(f'Added infra "{infra_type}" to {workspace_dir / "csrd-compose.yaml"}')
        except ValueError as exc:
            print(f"WARNING: {exc}")

    render_workspace(workspace_dir)
    return 0


def add_infra_direct(*, infra_type: str) -> int:
    """Non-interactive infra addition to the current workspace spec."""

    infra = InfraNode(type=infra_type)
    workspace_dir = Path.cwd().resolve()

    try:
        compose_add_infra(workspace_dir, infra)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    render_workspace(workspace_dir)
    print(f'Added infra "{infra_type}" to {workspace_dir / "csrd-compose.yaml"}')
    return 0


# ---------------------------------------------------------------------------
# Remove infra handler
# ---------------------------------------------------------------------------


def remove_infra_interactive() -> int:
    """Prompt the user to select configured infra types to remove."""

    workspace_dir = Path.cwd().resolve()
    configured = configured_infra(workspace_dir)

    if not configured:
        print("No infrastructure is currently configured.")
        return 0

    try:
        if len(configured) == 1:
            infra_type = configured[0]
            if not prompt_yes_no(f'Remove "{infra_type}"?'):
                print("Cancelled.")
                return 0
            selected = [infra_type]
        else:
            selected = prompt_multi_select("Select infrastructure to remove:", configured)
    except GoBack:
        print("Cancelled.")
        return 0
    except KeyboardInterrupt:
        with suppress(KeyboardInterrupt):
            print("\nCancelled.")
        return 1

    if not selected:
        print("No infrastructure selected.")
        return 0

    for infra_type in selected:
        try:
            compose_remove_infra(workspace_dir, infra_type)
            print(f'Removed infra "{infra_type}" from {workspace_dir / "csrd-compose.yaml"}')
        except ValueError as exc:
            print(f"WARNING: {exc}")

    render_workspace(workspace_dir)
    return 0


def remove_infra_direct(*, infra_type: str) -> int:
    """Non-interactive infra removal from the current workspace spec."""

    workspace_dir = Path.cwd().resolve()

    try:
        compose_remove_infra(workspace_dir, infra_type)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    render_workspace(workspace_dir)
    print(f'Removed infra "{infra_type}" from {workspace_dir / "csrd-compose.yaml"}')
    return 0


# ---------------------------------------------------------------------------
# List augments handler
# ---------------------------------------------------------------------------


def list_augments() -> int:
    """Print a table of all registered augments with scope, description, and prerequisites."""
    from ..compose.augments import AUGMENT_REGISTRY

    # Column widths
    name_w = max(len(d.name) for d in AUGMENT_REGISTRY.values())
    scope_w = 9  # "workspace"

    print(f"{'Name':<{name_w}}  {'Scope':<{scope_w}}  Description")
    print(f"{'─' * name_w}  {'─' * scope_w}  {'─' * 50}")

    for name in sorted(AUGMENT_REGISTRY):
        desc = AUGMENT_REGISTRY[name]
        reqs: list[str] = []
        if desc.requires_infra:
            reqs.append(f"infra: {', '.join(desc.requires_infra)}")
        if desc.requires_workspace_augment:
            reqs.append(f"needs: {desc.requires_workspace_augment}")
        suffix = f"  [{'; '.join(reqs)}]" if reqs else ""
        hidden_tag = " (hidden)" if desc.hidden else ""
        auto_tag = " (auto)" if desc.auto_apply else ""
        print(
            f"{name:<{name_w}}  {desc.scope:<{scope_w}}  {desc.description}{hidden_tag}{auto_tag}{suffix}"
        )

    print(f"\n{len(AUGMENT_REGISTRY)} augments registered.")
    return 0


# ---------------------------------------------------------------------------
# Add version handler
# ---------------------------------------------------------------------------


def _discover_version_dirs(views_dir: Path) -> list[str]:
    """Find existing version directories under views/ (e.g. v2026_05_09).

    Returns sorted list of version directory names that match the pattern.
    """
    versions: list[str] = []
    if not views_dir.is_dir():
        return versions
    for child in views_dir.iterdir():
        if child.is_dir() and child.name.startswith("v") and "_" in child.name:
            versions.append(child.name)
    return sorted(versions)


def _version_dir_name(date_str: str) -> str:
    """Convert a date string (YYYY-MM-DD) to a valid Python dir name (vYYYY_MM_DD)."""
    return "v" + date_str.replace("-", "_")


def _version_key(date_str: str) -> str:
    """The version key used in version_mapping (YYYY-MM-DD)."""
    return date_str


def _is_flat_views(views_dir: Path) -> bool:
    """Detect whether views/ is still the flat initial structure (no subdirs).

    Flat = views/__init__.py defines `app` directly (no unversioned/ dir).
    """
    unversioned_dir = views_dir / "unversioned"
    return not unversioned_dir.is_dir()


def _migrate_flat_to_structured(svc_dir: Path, svc_name: str) -> None:
    """Migrate flat views/__init__.py → views/unversioned/__init__.py.

    This moves the user's existing routes into the unversioned sub-app
    and replaces views/__init__.py with a re-export barrel.
    """
    views_dir = svc_dir / "views"
    unversioned_dir = views_dir / "unversioned"
    unversioned_dir.mkdir(parents=True, exist_ok=True)

    # Move existing views/__init__.py → views/unversioned/__init__.py
    old_init = views_dir / "__init__.py"
    new_init = unversioned_dir / "__init__.py"

    if old_init.is_file():
        content = old_init.read_text(encoding="utf-8")
        # The existing file has `app = FastAPI(...)` — rename to unversioned_app
        # and write to unversioned/__init__.py
        content = content.replace("app = FastAPI(", "unversioned_app = FastAPI(")
        content = content.replace('__all__ = ("app",)', '__all__ = ("unversioned_app",)')
        new_init.write_text(content, encoding="utf-8")

    # Rewrite views/__init__.py as the barrel
    barrel = (
        '"""Version sub-application registry.\n'
        "\n"
        "Each version module exports a FastAPI sub-app that is registered in\n"
        "the version_mapping passed to compose_versioned_apps().\n"
        '"""\n'
        "\n"
        "from .unversioned import unversioned_app\n"
        "\n"
        "# Alias for backward compatibility with render_init imports\n"
        "app = unversioned_app\n"
        "\n"
        '__all__ = ("app", "unversioned_app")\n'
    )
    old_init.write_text(barrel, encoding="utf-8")


def _create_version_stub(views_dir: Path, date_str: str, svc_name: str) -> Path:
    """Create a new versioned sub-app directory with a stub __init__.py.

    Returns the path to the created directory.
    """
    dir_name = _version_dir_name(date_str)
    version_dir = views_dir / dir_name
    version_dir.mkdir(parents=True, exist_ok=True)

    app_var = f"{dir_name}_app"
    stub = (
        f'"""Version {date_str} — API changes.\n'
        "\n"
        "Add routers for endpoints that differ from the unversioned API.\n"
        "Shared/unchanged endpoints can be imported from views.unversioned.\n"
        '"""\n'
        "\n"
        "from fastapi import FastAPI\n"
        "\n"
        f"{app_var} = FastAPI(\n"
        f'    title="{svc_name} — {date_str}",\n'
        f"    description=__doc__,\n"
        ")\n"
        "\n"
        "# Include routers here:\n"
        "# from ..unversioned import some_router\n"
        f"# {app_var}.include_router(some_router)\n"
        "\n"
        f'__all__ = ("{app_var}",)\n'
    )
    (version_dir / "__init__.py").write_text(stub, encoding="utf-8")
    return version_dir


def _update_views_barrel(views_dir: Path) -> None:
    """Regenerate views/__init__.py to export all discovered version sub-apps."""
    version_dirs = _discover_version_dirs(views_dir)

    imports = ["from .unversioned import unversioned_app"]
    exports = ['"app"', '"unversioned_app"']

    for vdir in version_dirs:
        app_var = f"{vdir}_app"
        imports.append(f"from .{vdir} import {app_var}")
        exports.append(f'"{app_var}"')

    barrel = (
        '"""Version sub-application registry.\n'
        "\n"
        "Each version module exports a FastAPI sub-app that is registered in\n"
        "the version_mapping passed to compose_versioned_apps().\n"
        '"""\n'
        "\n" + "\n".join(imports) + "\n"
        "\n"
        "# Alias for backward compatibility with render_init imports\n"
        "app = unversioned_app\n"
        "\n"
        f"__all__ = ({', '.join(exports)})\n"
    )
    (views_dir / "__init__.py").write_text(barrel, encoding="utf-8")


def _update_service_init(svc_dir: Path, svc_name: str, views_dir: Path) -> None:
    """Regenerate the service __init__.py to include all versions in version_mapping.

    Unlike render_init (which uses the spec), this operates on the filesystem
    directly — it discovers version dirs and writes the mapping.
    """
    version_dirs = _discover_version_dirs(views_dir)

    # Read the existing __init__.py to preserve lifespan/middleware/routers
    init_path = svc_dir / "__init__.py"
    if not init_path.is_file():
        return

    content = init_path.read_text(encoding="utf-8")

    # Add version imports if not present
    for vdir in version_dirs:
        app_var = f"{vdir}_app"
        import_line = f"from .views.{vdir} import {app_var}"
        # Also check barrel import style
        barrel_import = f"from .views import {app_var}"
        if import_line not in content and barrel_import not in content:
            # Insert after the existing views import
            content = content.replace(
                "from .views import app as unversioned_app",
                f"from .views import app as unversioned_app\nfrom .views import {app_var}",
            )

    # Update version_mapping to include new versions
    # Find the existing version_mapping line and expand it
    if "version_mapping={UNVERSIONED: unversioned_app}," in content:
        mapping_lines = "version_mapping={\n"
        mapping_lines += "            UNVERSIONED: unversioned_app,\n"
        for vdir in version_dirs:
            date_str = vdir[1:].replace("_", "-")  # v2026_05_09 → 2026-05-09
            app_var = f"{vdir}_app"
            mapping_lines += f'            "{date_str}": {app_var},\n'
        mapping_lines += "        },"
        content = content.replace(
            "version_mapping={UNVERSIONED: unversioned_app},",
            mapping_lines,
        )
    elif "version_mapping={" in content:
        # Already multi-line — find the closing brace and add new entries before it
        # Simple approach: check if the version is already there
        for vdir in version_dirs:
            date_str = vdir[1:].replace("_", "-")
            app_var = f"{vdir}_app"
            entry = f'"{date_str}": {app_var},'
            if entry not in content:
                # Insert before the closing `}` of version_mapping
                content = content.replace(
                    "        },\n        config=VersionedAppComposeConfig(",
                    f"            {entry}\n        }},\n        config=VersionedAppComposeConfig(",
                )

    init_path.write_text(content, encoding="utf-8")


def add_version_interactive() -> int:
    """Interactive handler: prompt for service and date, create version stub."""
    from datetime import date

    workspace_dir = Path.cwd().resolve()
    sp = spec_file_path(workspace_dir)
    if not sp.is_file():
        print("ERROR: No workspace found.")
        return 1

    spec = load_spec(sp)

    if not spec.services:
        print("No services found.")
        return 0

    # Filter to non-worker services (workers don't have versioned APIs)
    svc_names = [s.name for s in spec.services if s.role != "worker"]
    if not svc_names:
        print("No API services to version (workers don't have versioned endpoints).")
        return 0

    try:
        chosen = prompt_single_select("Add version to which service?", svc_names, auto_select=True)
    except GoBack:
        print("Cancelled.")
        return 0
    except KeyboardInterrupt:
        with suppress(KeyboardInterrupt):
            print("\nCancelled.")
        return 1

    if chosen is None:
        print("Cancelled.")
        return 0

    today = date.today().isoformat()
    try:
        date_str = prompt_text("Version date (YYYY-MM-DD)", default=today)
    except GoBack:
        print("Cancelled.")
        return 0
    except KeyboardInterrupt:
        with suppress(KeyboardInterrupt):
            print("\nCancelled.")
        return 1

    if not date_str:
        date_str = today

    return _do_add_version(workspace_dir, chosen, date_str)


def add_version_direct(*, service_name: str, date_str: str | None = None) -> int:
    """Non-interactive add-version from CLI flags."""
    from datetime import date

    workspace_dir = Path.cwd().resolve()

    if date_str is None:
        date_str = date.today().isoformat()

    return _do_add_version(workspace_dir, service_name, date_str)


def _do_add_version(workspace_dir: Path, service_name: str, date_str: str) -> int:
    """Core implementation shared by interactive and direct handlers."""
    import re

    # Validate date format
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        print(f"ERROR: Invalid date format '{date_str}'. Expected YYYY-MM-DD.")
        return 1

    # Find service source directory
    svc_snake = service_name.replace("-", "_")
    svc_dir = workspace_dir / "src" / svc_snake
    if not svc_dir.is_dir():
        print(f"ERROR: Service directory not found: {svc_dir}")
        return 1

    views_dir = svc_dir / "views"
    if not views_dir.is_dir():
        print(f"ERROR: Views directory not found: {views_dir}")
        return 1

    dir_name = _version_dir_name(date_str)
    if (views_dir / dir_name).is_dir():
        print(f"ERROR: Version directory already exists: views/{dir_name}")
        return 1

    # Step 1: Migrate flat → structured if needed
    if _is_flat_views(views_dir):
        print("  Migrating flat views/ → views/unversioned/")
        _migrate_flat_to_structured(svc_dir, service_name)

    # Step 2: Create version stub
    version_dir = _create_version_stub(views_dir, date_str, service_name)
    print(f"  Created {version_dir.relative_to(workspace_dir)}/")

    # Step 3: Update views barrel
    _update_views_barrel(views_dir)
    print("  Updated views/__init__.py")

    # Step 4: Update service __init__.py with version_mapping
    _update_service_init(svc_dir, service_name, views_dir)
    print(f"  Updated {svc_snake}/__init__.py version_mapping")

    print(f"\n✓ Added version {date_str} to {service_name}")
    print(f"  Edit: src/{svc_snake}/views/{dir_name}/__init__.py")
    return 0


# ---------------------------------------------------------------------------
# add-frontend
# ---------------------------------------------------------------------------

_FRONTEND_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates" / "frontend-vue"

_FRONTEND_DEFAULT_PORT = 3000
_FRONTEND_SERVICE_NAME = "frontend"


def _resolve_frontend_vars(workspace_dir: Path) -> dict[str, str]:
    """Resolve template variables for the frontend scaffold."""
    sp = spec_file_path(workspace_dir)
    spec = load_spec(sp)

    workspace_name = spec.workspace.name

    # Find gateway service for proxy target
    gateway_svc = next((s for s in spec.services if s.role == "gateway"), None)
    gateway_host = gateway_svc.name if gateway_svc else "localhost"
    gateway_port = str(gateway_svc.port) if gateway_svc else "8000"

    return {
        "workspace_name": workspace_name,
        "service_name": _FRONTEND_SERVICE_NAME,
        "frontend_port": str(_FRONTEND_DEFAULT_PORT),
        "gateway_host": gateway_host,
        "gateway_port": gateway_port,
    }


def _scaffold_frontend(workspace_dir: Path, variables: dict[str, str]) -> Path:
    """Copy and render the frontend template into the workspace."""
    from string import Template

    frontend_dir = workspace_dir / "src" / _FRONTEND_SERVICE_NAME
    if frontend_dir.exists():
        raise ValueError(f"Frontend directory already exists: {frontend_dir}")

    frontend_dir.mkdir(parents=True, exist_ok=True)

    for template_file in sorted(_FRONTEND_TEMPLATE_DIR.rglob("*")):
        if template_file.is_dir():
            continue
        if "__pycache__" in str(template_file):
            continue

        relative = template_file.relative_to(_FRONTEND_TEMPLATE_DIR)
        dest = frontend_dir / relative
        dest.parent.mkdir(parents=True, exist_ok=True)

        content = template_file.read_text(encoding="utf-8")
        rendered = Template(content).safe_substitute(variables)
        dest.write_text(rendered, encoding="utf-8")

    # Dockerfile goes at workspace root
    dockerfile_src = frontend_dir / "Dockerfile"
    dockerfile_dest = workspace_dir / f"Dockerfile.{_FRONTEND_SERVICE_NAME}"
    if dockerfile_src.exists():
        import shutil

        shutil.move(str(dockerfile_src), str(dockerfile_dest))

    return frontend_dir


def _add_frontend_to_spec(workspace_dir: Path) -> None:
    """Add the frontend service to csrd-compose.yaml and re-render compose."""
    sp = spec_file_path(workspace_dir)
    spec = load_spec(sp)

    # Check if frontend already in spec
    if any(s.name == _FRONTEND_SERVICE_NAME for s in spec.services):
        return

    frontend_node = ServiceNode(
        name=_FRONTEND_SERVICE_NAME,
        role="frontend",
        port=_FRONTEND_DEFAULT_PORT,
    )
    spec.services.append(frontend_node)

    from ..compose import save_spec

    save_spec(spec, sp)

    # Re-render docker-compose.yml
    compose_apply(workspace_dir)


def _do_add_frontend(workspace_dir: Path) -> int:
    """Core implementation for add-frontend."""
    sp = spec_file_path(workspace_dir)
    if not sp.is_file():
        print("ERROR: No csrd-compose.yaml found. Run from a workspace directory.")
        return 1

    frontend_dir = workspace_dir / "src" / _FRONTEND_SERVICE_NAME
    if frontend_dir.exists():
        print(f"ERROR: Frontend directory already exists: {frontend_dir}")
        return 1

    print("Adding frontend to workspace...")

    # Step 1: Resolve template variables
    variables = _resolve_frontend_vars(workspace_dir)
    print(f"  Gateway proxy: {variables['gateway_host']}:{variables['gateway_port']}")

    # Step 2: Scaffold frontend files
    _scaffold_frontend(workspace_dir, variables)
    print(f"  Scaffolded src/{_FRONTEND_SERVICE_NAME}/")

    # Step 3: Add to spec and re-render compose
    _add_frontend_to_spec(workspace_dir)
    print("  Updated csrd-compose.yaml and docker-compose.yml")

    print("\n✓ Frontend added to workspace")
    print(f"  Source:  src/{_FRONTEND_SERVICE_NAME}/")
    print(f"  Port:    {_FRONTEND_DEFAULT_PORT}")
    print("  Start:   docker compose up --build")
    return 0


def add_frontend_interactive() -> int:
    """Interactive add-frontend handler."""
    workspace_dir = Path.cwd().resolve()
    return _do_add_frontend(workspace_dir)


def add_frontend_direct() -> int:
    """Non-interactive add-frontend from CLI flags."""
    workspace_dir = Path.cwd().resolve()
    return _do_add_frontend(workspace_dir)
