"""Manifest planning and execution for dry-run and idempotent issue creation.

Provides ``plan_manifest()`` for assembling a dependency-safe ``OperationPlan``
from a JSON manifest, and ``execute_manifest()`` as a convenience wrapper for
real execution mode.

The manifest describes a tree of issues with parent-child and blocking
relationships. The orchestrator traverses the manifest in topological order,
computes orchestration keys for each operation, and either previews (dry-run)
or executes (real) the operations through an ``IssueProvider``.
"""

from __future__ import annotations

from typing import Any

from agentic_devtools.adapters.cycle_detection import CycleDetectedError, detect_cycles
from agentic_devtools.adapters.idempotency_query_provider import IdempotencyQueryProvider
from agentic_devtools.adapters.issue_provider import VALID_ISSUE_TYPES, IssueProvider
from agentic_devtools.adapters.operation_plan import OperationDescriptor, OperationPlan
from agentic_devtools.adapters.orchestration_key import embed_orchestration_key, generate_orchestration_key


def plan_manifest(
    manifest: dict[str, Any],
    provider: IssueProvider,
    *,
    dry_run: bool = True,
    check_existing: bool = False,
    query_provider: IdempotencyQueryProvider | None = None,
) -> OperationPlan:
    """Assemble a dependency-safe operation plan from a manifest.

    Args:
        manifest: JSON manifest with "nodes" list. Each node has "ref",
            "title", "body", "issue_type", and optionally "parent_ref"
            and "blocked_by" (list of refs).
        provider: IssueProvider for dry-run param extraction / real execution.
        dry_run: When True, no mutations. When False, execute operations.
        check_existing: When True (dry-run only), query provider for
            existing entities. Requires query_provider.
        query_provider: IdempotencyQueryProvider for existence checks.
            Required when check_existing=True.

    Returns:
        OperationPlan with ordered OperationDescriptor entries.

    Raises:
        ValueError: If check_existing=True but query_provider is None.
        ValueError: If check_existing=True but dry_run=False.
        ValueError: If check_existing=True but query_provider does not implement
            the IdempotencyQueryProvider protocol.
        ValueError: If manifest is not a dict, manifest['nodes'] is not a list,
            any node is not a dict, a node is missing a required key
            ('ref', 'title', 'issue_type'), a required key value is not a
            non-empty string after trimming, issue_type is unsupported,
            'body' is present but is neither a string nor null,
            'blocked_by' or 'labels' is present but not a list,
            or duplicate refs are detected.
        ValueError: If a circular dependency is detected among manifest nodes.
        ValueError: If a node's parent_ref or blocked_by ref cannot be resolved during real execution.
        Any provider error: Propagated from adapter calls (FR-009).
    """
    if check_existing and query_provider is None:
        raise ValueError("check_existing=True requires a query_provider")
    if check_existing and not dry_run:
        raise ValueError("check_existing=True is only valid with dry_run=True")
    if check_existing and not isinstance(query_provider, IdempotencyQueryProvider):
        raise ValueError(
            f"query_provider must implement the IdempotencyQueryProvider protocol, got {type(query_provider).__name__}"
        )

    if not isinstance(manifest, dict):
        raise ValueError(f"manifest must be a dict, got {type(manifest).__name__}")

    nodes = manifest.get("nodes", [])

    # Validate manifest structure up front for deterministic, actionable errors.
    if not isinstance(nodes, list):
        raise ValueError(f"manifest['nodes'] must be a list, got {type(nodes).__name__}")
    validated_nodes: list[dict[str, Any]] = []
    seen_refs: set[str] = set()
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise ValueError(f"manifest['nodes'][{i}] must be a dict, got {type(node).__name__}")
        normalized_node = dict(node)
        for key in ("ref", "title", "issue_type"):
            if key not in node:
                raise ValueError(f"manifest['nodes'][{i}] missing required key {key!r}")
            value = node[key]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"manifest['nodes'][{i}][{key!r}] must be a non-empty string, got {type(value).__name__!r}"
                )
            if key == "issue_type":
                normalized_value = value.strip().lower()
                if normalized_value not in VALID_ISSUE_TYPES:
                    raise ValueError(
                        f"Unsupported issue_type {normalized_value!r}. Valid types: {sorted(VALID_ISSUE_TYPES)}"
                    )
            else:
                normalized_value = value.strip()
            normalized_node[key] = normalized_value
        if "body" in node and node["body"] is not None and not isinstance(node["body"], str):
            raise ValueError(
                f"manifest['nodes'][{i}]['body'] must be a string or null, got {type(node['body']).__name__!r}"
            )
        if "parent_ref" in node:
            parent_ref_val = node["parent_ref"]
            if not isinstance(parent_ref_val, str) or not parent_ref_val.strip():
                raise ValueError(
                    f"manifest['nodes'][{i}]['parent_ref'] must be a non-empty string, "
                    f"got {type(parent_ref_val).__name__!r}"
                )
            normalized_node["parent_ref"] = parent_ref_val.strip()
        for list_key in ("blocked_by", "labels"):
            if list_key not in node:
                continue
            value = node[list_key]
            if not isinstance(value, list):
                raise ValueError(f"manifest['nodes'][{i}][{list_key!r}] must be a list, got {type(value).__name__!r}")
            normalized_elems: list[str] = []
            for j, elem in enumerate(value):
                if not isinstance(elem, str) or not elem.strip():
                    raise ValueError(
                        f"manifest['nodes'][{i}][{list_key!r}][{j}] must be a non-empty string, "
                        f"got {type(elem).__name__!r}"
                    )
                normalized_elems.append(elem.strip())
            normalized_node[list_key] = normalized_elems
        node_ref = normalized_node["ref"]
        if node_ref in seen_refs:
            raise ValueError(f"Duplicate ref {node_ref!r} in manifest['nodes']")
        seen_refs.add(node_ref)
        validated_nodes.append(normalized_node)

    # Build node lookup and edges for topological sort
    node_map: dict[str, dict[str, Any]] = {}
    for node in validated_nodes:
        node_map[node["ref"]] = node

    # Determine topological order based on blocked_by relationships
    edges: list[tuple[str, str]] = []
    for node in validated_nodes:
        for blocker_ref in node.get("blocked_by", []):
            # blocker must be created before this node
            edges.append((blocker_ref, node["ref"]))

    # Also ensure parents are created before children
    for node in validated_nodes:
        parent_ref = node.get("parent_ref")
        if parent_ref:
            edges.append((parent_ref, node["ref"]))

    if edges:
        try:
            sorted_refs = detect_cycles(edges)
        except CycleDetectedError as exc:
            raise ValueError(str(exc)) from exc
        # Include any nodes not in the edge graph (isolated nodes)
        sorted_refs_set = set(sorted_refs)
        remaining = [r for r in node_map if r not in sorted_refs_set]
        sorted_refs = sorted_refs + remaining
    else:
        sorted_refs = list(node_map.keys())

    # In real execution, validate all cross-node references before any mutation.
    if not dry_run:
        for ref in sorted_refs:
            if ref not in node_map:
                continue
            node = node_map[ref]
            parent_ref = node.get("parent_ref")
            if parent_ref and parent_ref not in node_map:
                raise ValueError(f"parent_ref {parent_ref!r} for manifest ref {ref!r} could not be resolved")
            for blocker_ref in node.get("blocked_by", []):
                if blocker_ref not in node_map:
                    raise ValueError(f"blocked_by ref {blocker_ref!r} for manifest ref {ref!r} could not be resolved")

    # Phase 1: Generate create operations in topological order
    descriptors: list[OperationDescriptor] = []
    ref_bindings: dict[str, str] = {}  # manifest ref → provider identifier

    for ref in sorted_refs:
        if ref not in node_map:
            continue
        node = node_map[ref]
        orch_key = generate_orchestration_key("create_issue", ref)
        body = node.get("body", "")
        if body is None:
            body = ""
        body_with_key = embed_orchestration_key(body, orch_key)

        provider_params: dict[str, Any] = {
            "title": node["title"],
            "body": body_with_key,
            "issue_type": node["issue_type"],
        }
        if node.get("parent_ref"):
            provider_params["parent_ref"] = node["parent_ref"]
        if node.get("labels"):
            provider_params["labels"] = node["labels"]

        if dry_run and not check_existing:
            # Mode 1: planning-only dry-run — assemble descriptors only.
            descriptors.append(
                OperationDescriptor(
                    operation_type="create_issue",
                    orchestration_key=orch_key,
                    refs=(ref,),
                    status="dry-run",
                    provider_params=provider_params,
                )
            )
        elif dry_run and check_existing:
            # Mode 2: dry-run with existence checks
            assert query_provider is not None
            existing = query_provider.find_existing_issue(orch_key)
            if existing is not None:
                ref_bindings[ref] = existing.identifier
                descriptors.append(
                    OperationDescriptor(
                        operation_type="create_issue",
                        orchestration_key=orch_key,
                        refs=(ref,),
                        status="existing",
                        provider_params=provider_params,
                        result=existing,
                    )
                )
            else:
                descriptors.append(
                    OperationDescriptor(
                        operation_type="create_issue",
                        orchestration_key=orch_key,
                        refs=(ref,),
                        status="dry-run",
                        provider_params=provider_params,
                    )
                )
        else:
            # Mode 3: real execution
            parent_id: str | None = None
            if node.get("parent_ref"):
                parent_id = ref_bindings[node["parent_ref"]]

            result = provider.create_issue(
                title=node["title"],
                body=body_with_key,
                issue_type=node["issue_type"],
                parent_id=parent_id,
                labels=node.get("labels"),
                idempotency_key=orch_key,
                dry_run=False,
            )
            ref_bindings[ref] = result.identifier
            descriptors.append(
                OperationDescriptor(
                    operation_type="create_issue",
                    orchestration_key=orch_key,
                    refs=(ref,),
                    status=result.status,
                    provider_params=provider_params,
                    result=result,
                )
            )

    # Phase 2: Generate link_subissue operations
    for ref in sorted_refs:
        if ref not in node_map:
            continue
        node = node_map[ref]
        parent_ref = node.get("parent_ref")
        if not parent_ref:
            continue

        orch_key = generate_orchestration_key("link_subissue", parent_ref, ref)
        provider_params = {"parent_ref": parent_ref, "child_ref": ref}

        if dry_run and not check_existing:
            descriptors.append(
                OperationDescriptor(
                    operation_type="link_subissue",
                    orchestration_key=orch_key,
                    refs=(parent_ref, ref),
                    status="dry-run",
                    provider_params=provider_params,
                )
            )
        elif dry_run and check_existing:
            assert query_provider is not None
            parent_id = ref_bindings.get(parent_ref)
            child_id = ref_bindings.get(ref)
            if parent_id and child_id:
                link_existing = query_provider.find_existing_link(parent_id, child_id)
                if link_existing is not None:
                    descriptors.append(
                        OperationDescriptor(
                            operation_type="link_subissue",
                            orchestration_key=orch_key,
                            refs=(parent_ref, ref),
                            status="already-linked",
                            provider_params=provider_params,
                            result=link_existing,
                        )
                    )
                else:
                    descriptors.append(
                        OperationDescriptor(
                            operation_type="link_subissue",
                            orchestration_key=orch_key,
                            refs=(parent_ref, ref),
                            status="dry-run",
                            provider_params=provider_params,
                        )
                    )
            else:
                descriptors.append(
                    OperationDescriptor(
                        operation_type="link_subissue",
                        orchestration_key=orch_key,
                        refs=(parent_ref, ref),
                        status="dry-run",
                        provider_params=provider_params,
                    )
                )
        else:
            # Real execution
            parent_id = ref_bindings[parent_ref]
            child_id = ref_bindings[ref]
            link_result = provider.link_subissue(parent_id, child_id, dry_run=False)
            descriptors.append(
                OperationDescriptor(
                    operation_type="link_subissue",
                    orchestration_key=orch_key,
                    refs=(parent_ref, ref),
                    status=link_result.status,
                    provider_params=provider_params,
                    result=link_result,
                )
            )

    # Phase 3: Generate add_blocked_by operations
    for ref in sorted_refs:
        if ref not in node_map:
            continue
        node = node_map[ref]
        for blocker_ref in node.get("blocked_by", []):
            orch_key = generate_orchestration_key("add_blocked_by", ref, blocker_ref)
            provider_params = {"issue_ref": ref, "blocked_by_ref": blocker_ref}

            if dry_run and not check_existing:
                descriptors.append(
                    OperationDescriptor(
                        operation_type="add_blocked_by",
                        orchestration_key=orch_key,
                        refs=(ref, blocker_ref),
                        status="dry-run",
                        provider_params=provider_params,
                    )
                )
            elif dry_run and check_existing:
                assert query_provider is not None
                issue_id = ref_bindings.get(ref)
                blocker_id = ref_bindings.get(blocker_ref)
                if issue_id and blocker_id:
                    dep_existing = query_provider.find_existing_dependency(issue_id, blocker_id)
                    if dep_existing is not None:
                        descriptors.append(
                            OperationDescriptor(
                                operation_type="add_blocked_by",
                                orchestration_key=orch_key,
                                refs=(ref, blocker_ref),
                                status="already-linked",
                                provider_params=provider_params,
                                result=dep_existing,
                            )
                        )
                    else:
                        descriptors.append(
                            OperationDescriptor(
                                operation_type="add_blocked_by",
                                orchestration_key=orch_key,
                                refs=(ref, blocker_ref),
                                status="dry-run",
                                provider_params=provider_params,
                            )
                        )
                else:
                    descriptors.append(
                        OperationDescriptor(
                            operation_type="add_blocked_by",
                            orchestration_key=orch_key,
                            refs=(ref, blocker_ref),
                            status="dry-run",
                            provider_params=provider_params,
                        )
                    )
            else:
                # Real execution
                issue_id = ref_bindings[ref]
                blocker_id = ref_bindings[blocker_ref]
                dep_result = provider.add_blocked_by(issue_id, blocker_id, dry_run=False)
                descriptors.append(
                    OperationDescriptor(
                        operation_type="add_blocked_by",
                        orchestration_key=orch_key,
                        refs=(ref, blocker_ref),
                        status=dep_result.status,
                        provider_params=provider_params,
                        result=dep_result,
                    )
                )

    return OperationPlan(
        operations=tuple(descriptors),
        dry_run=dry_run,
        check_existing=check_existing,
    )


def execute_manifest(
    manifest: dict[str, Any],
    provider: IssueProvider,
) -> OperationPlan:
    """Execute a manifest against a provider (real mutations).

    Convenience wrapper for ``plan_manifest(dry_run=False)``.

    Args:
        manifest: JSON manifest with nodes and edges.
        provider: IssueProvider for real execution.

    Returns:
        OperationPlan with results from the executed operations.
    """
    return plan_manifest(manifest, provider, dry_run=False)
