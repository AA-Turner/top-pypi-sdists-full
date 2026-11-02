"""Generated response validation registry. Owned by the schema emitter."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from importlib import import_module
from typing import ClassVar, cast
from urllib.parse import urlsplit

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.serializable_model import SerializableModel


class ResponseRegistry:
    """Validate successful JSON bodies against their generated models."""

    _MODELS: ClassVar[dict[tuple[str, str], tuple[str, str]]] = {
        ("GET", "/api/v1"): ("labqoat._generated.api_index", "ApiIndex"),
        ("POST", "/api/v1/analytics-queries"): ("labqoat._generated.analytics_query", "AnalyticsQuery"),
        ("GET", "/api/v1/analytics-queries/item"): ("labqoat._generated.analytics_query", "AnalyticsQuery"),
        ("GET", "/api/v1/asset-records"): ("labqoat._generated.asset_record_page", "AssetRecordPage"),
        ("POST", "/api/v1/asset-records"): ("labqoat._generated.asset_record", "AssetRecord"),
        ("POST", "/api/v1/asset-records/batch"): ("labqoat._generated.asset_batch_page", "AssetBatchPage"),
        ("POST", "/api/v1/asset-records/batch/complete"): ("labqoat._generated.asset_batch_page", "AssetBatchPage"),
        ("GET", "/api/v1/asset-records/describe"): ("labqoat._generated.asset_record", "AssetRecord"),
        ("GET", "/api/v1/asset-records/item"): ("labqoat._generated.asset_record", "AssetRecord"),
        ("POST", "/api/v1/asset-records/item/complete"): ("labqoat._generated.asset_record", "AssetRecord"),
        ("PUT", "/api/v1/asset-records/item/content"): ("labqoat._generated.asset_record", "AssetRecord"),
        ("GET", "/api/v1/builds"): ("labqoat._generated.build_page", "BuildPage"),
        ("POST", "/api/v1/builds"): ("labqoat._generated.build", "Build"),
        ("GET", "/api/v1/builds/item"): ("labqoat._generated.build", "Build"),
        ("GET", "/api/v1/builds/item/logs"): ("labqoat._generated.build_log_page", "BuildLogPage"),
        ("POST", "/api/v1/builds/item/start"): ("labqoat._generated.build", "Build"),
        ("GET", "/api/v1/capabilities"): ("labqoat._generated.capabilities", "Capabilities"),
        ("GET", "/api/v1/checkpoints"): ("labqoat._generated.checkpoint_page", "CheckpointPage"),
        ("DELETE", "/api/v1/checkpoints/item"): ("labqoat._generated.deletion_receipt", "DeletionReceipt"),
        ("GET", "/api/v1/checkpoints/item"): ("labqoat._generated.checkpoint", "Checkpoint"),
        ("GET", "/api/v1/compute/hosts"): ("labqoat._generated.compute_host_page", "ComputeHostPage"),
        ("POST", "/api/v1/compute/hosts"): ("labqoat._generated.compute_host_enrollment", "ComputeHostEnrollment"),
        ("DELETE", "/api/v1/compute/hosts/{id}"): ("labqoat._generated.compute_host", "ComputeHost"),
        ("GET", "/api/v1/compute/hosts/{id}"): ("labqoat._generated.compute_host", "ComputeHost"),
        ("PATCH", "/api/v1/compute/hosts/{id}"): ("labqoat._generated.compute_host", "ComputeHost"),
        ("GET", "/api/v1/compute/locations/{id}"): (
            "labqoat._generated.compute_location_policy",
            "ComputeLocationPolicy",
        ),
        ("PATCH", "/api/v1/compute/locations/{id}"): (
            "labqoat._generated.compute_location_policy",
            "ComputeLocationPolicy",
        ),
        ("GET", "/api/v1/compute/offerings"): ("labqoat._generated.compute_offering_page", "ComputeOfferingPage"),
        ("GET", "/api/v1/compute/settings"): ("labqoat._generated.compute_settings", "ComputeSettings"),
        ("PATCH", "/api/v1/compute/settings"): ("labqoat._generated.compute_settings", "ComputeSettings"),
        ("GET", "/api/v1/compute/usage"): ("labqoat._generated.compute_usage", "ComputeUsage"),
        ("GET", "/api/v1/dashboards"): ("labqoat._generated.dashboard_page", "DashboardPage"),
        ("POST", "/api/v1/dashboards"): ("labqoat._generated.dashboard", "Dashboard"),
        ("GET", "/api/v1/dashboards/item"): ("labqoat._generated.dashboard", "Dashboard"),
        ("GET", "/api/v1/dashboards/item/changes"): ("labqoat._generated.dashboard_change_page", "DashboardChangePage"),
        ("GET", "/api/v1/dashboards/item/versions"): (
            "labqoat._generated.dashboard_version_page",
            "DashboardVersionPage",
        ),
        ("POST", "/api/v1/dataset-imports"): ("labqoat._generated.dataset_import", "DatasetImport"),
        ("POST", "/api/v1/dataset-imports/huggingface/preview"): (
            "labqoat._generated.hugging_face_preview",
            "HuggingFacePreview",
        ),
        ("GET", "/api/v1/dataset-imports/{id}"): ("labqoat._generated.dataset_import", "DatasetImport"),
        ("GET", "/api/v1/dataset-repositories"): (
            "labqoat._generated.dataset_repository_page",
            "DatasetRepositoryPage",
        ),
        ("POST", "/api/v1/dataset-repositories"): ("labqoat._generated.dataset_repository", "DatasetRepository"),
        ("DELETE", "/api/v1/dataset-repositories/item"): ("labqoat._generated.deletion_receipt", "DeletionReceipt"),
        ("GET", "/api/v1/dataset-repositories/item"): ("labqoat._generated.dataset_repository", "DatasetRepository"),
        ("GET", "/api/v1/dataset-revisions"): ("labqoat._generated.dataset_revision_page", "DatasetRevisionPage"),
        ("GET", "/api/v1/dataset-revisions/files"): (
            "labqoat._generated.dataset_revision_files",
            "DatasetRevisionFiles",
        ),
        ("DELETE", "/api/v1/dataset-revisions/item"): ("labqoat._generated.deletion_receipt", "DeletionReceipt"),
        ("GET", "/api/v1/dataset-revisions/item"): ("labqoat._generated.dataset_revision", "DatasetRevision"),
        ("GET", "/api/v1/dataset-revisions/lineage"): (
            "labqoat._generated.dataset_revision_lineage",
            "DatasetRevisionLineage",
        ),
        ("GET", "/api/v1/dataset-revisions/validation"): (
            "labqoat._generated.dataset_revision_validation",
            "DatasetRevisionValidation",
        ),
        ("GET", "/api/v1/dataset-revisions/{id}"): ("labqoat._generated.dataset_publication", "DatasetPublication"),
        ("GET", "/api/v1/dataset-tags"): ("labqoat._generated.dataset_tag_page", "DatasetTagPage"),
        ("POST", "/api/v1/dataset-tags"): ("labqoat._generated.dataset_tag", "DatasetTag"),
        ("GET", "/api/v1/datasets/resolve"): ("labqoat._generated.dataset_publication", "DatasetPublication"),
        ("GET", "/api/v1/dicts"): ("labqoat._generated.dict_list", "DictList"),
        ("GET", "/api/v1/dicts/{name}"): ("labqoat._generated.dict_summary", "DictSummary"),
        ("DELETE", "/api/v1/dicts/{name}/entries"): ("labqoat._generated.clear_receipt", "ClearReceipt"),
        ("GET", "/api/v1/dicts/{name}/entries"): ("labqoat._generated.dict_entry_page", "DictEntryPage"),
        ("PUT", "/api/v1/dicts/{name}/entries"): ("labqoat._generated.dict_write", "DictWrite"),
        ("DELETE", "/api/v1/dicts/{name}/entries/item"): ("labqoat._generated.dict_entry", "DictEntry"),
        ("GET", "/api/v1/dicts/{name}/entries/item"): ("labqoat._generated.dict_entry", "DictEntry"),
        ("GET", "/api/v1/endpoint-tokens"): ("labqoat._generated.endpoint_token_list", "EndpointTokenList"),
        ("POST", "/api/v1/endpoint-tokens"): ("labqoat._generated.endpoint_token", "EndpointToken"),
        ("GET", "/api/v1/endpoints"): ("labqoat._generated.endpoint_list", "EndpointList"),
        ("GET", "/api/v1/endpoints/{name}"): ("labqoat._generated.endpoint", "Endpoint"),
        ("PUT", "/api/v1/endpoints/{name}"): ("labqoat._generated.endpoint", "Endpoint"),
        ("GET", "/api/v1/locations"): ("labqoat._generated.location_registry", "LocationRegistry"),
        ("GET", "/api/v1/memory/attention"): ("labqoat._generated.knowledge_orientation", "KnowledgeOrientation"),
        ("GET", "/api/v1/memory/brief"): ("labqoat._generated.knowledge_brief", "KnowledgeBrief"),
        ("POST", "/api/v1/memory/brief"): ("labqoat._generated.knowledge_receipt", "KnowledgeReceipt"),
        ("GET", "/api/v1/memory/brief/history"): ("labqoat._generated.knowledge_file_page", "KnowledgeFilePage"),
        ("GET", "/api/v1/memory/catchup"): ("labqoat._generated.knowledge_orientation", "KnowledgeOrientation"),
        ("GET", "/api/v1/memory/changes"): ("labqoat._generated.knowledge_view", "KnowledgeView"),
        ("POST", "/api/v1/memory/commits"): ("labqoat._generated.knowledge_receipt", "KnowledgeReceipt"),
        ("GET", "/api/v1/memory/files"): ("labqoat._generated.knowledge_file_page", "KnowledgeFilePage"),
        ("POST", "/api/v1/memory/files"): ("labqoat._generated.knowledge_receipt", "KnowledgeReceipt"),
        ("GET", "/api/v1/memory/files/history"): ("labqoat._generated.knowledge_file_page", "KnowledgeFilePage"),
        ("GET", "/api/v1/memory/frontier"): ("labqoat._generated.knowledge_orientation", "KnowledgeOrientation"),
        ("POST", "/api/v1/memory/links"): ("labqoat._generated.knowledge_receipt", "KnowledgeReceipt"),
        ("GET", "/api/v1/memory/nodes/history"): ("labqoat._generated.knowledge_history", "KnowledgeHistory"),
        ("GET", "/api/v1/memory/nodes/item"): ("labqoat._generated.knowledge_node", "KnowledgeNode"),
        ("POST", "/api/v1/memory/nodes/revisions"): ("labqoat._generated.knowledge_receipt", "KnowledgeReceipt"),
        ("POST", "/api/v1/memory/nodes/status"): ("labqoat._generated.knowledge_receipt", "KnowledgeReceipt"),
        ("POST", "/api/v1/memory/objectives"): ("labqoat._generated.knowledge_receipt", "KnowledgeReceipt"),
        ("GET", "/api/v1/memory/revisions/item"): ("labqoat._generated.knowledge_node", "KnowledgeNode"),
        ("GET", "/api/v1/memory/search"): ("labqoat._generated.knowledge_view", "KnowledgeView"),
        ("GET", "/api/v1/nodes"): ("labqoat._generated.node_page", "NodePage"),
        ("GET", "/api/v1/nodes/item"): ("labqoat._generated.node", "Node"),
        ("GET", "/api/v1/nodes/item/logs"): ("labqoat._generated.node_log_page", "NodeLogPage"),
        ("GET", "/api/v1/notes"): ("labqoat._generated.note_page", "NotePage"),
        ("POST", "/api/v1/notes"): ("labqoat._generated.note", "Note"),
        ("GET", "/api/v1/notes/{id}"): ("labqoat._generated.note", "Note"),
        ("PATCH", "/api/v1/notes/{id}"): ("labqoat._generated.note", "Note"),
        ("GET", "/api/v1/operation-events"): ("labqoat._generated.operation_event_page", "OperationEventPage"),
        ("POST", "/api/v1/operation-events"): ("labqoat._generated.operation_event", "OperationEvent"),
        ("GET", "/api/v1/pools"): ("labqoat._generated.pool_page", "PoolPage"),
        ("GET", "/api/v1/pools/item"): ("labqoat._generated.pool", "Pool"),
        ("GET", "/api/v1/pools/item/logs"): ("labqoat._generated.pool_log_page", "PoolLogPage"),
        ("GET", "/api/v1/projects"): ("labqoat._generated.project_list", "ProjectList"),
        ("GET", "/api/v1/projects/{name}"): ("labqoat._generated.project", "Project"),
        ("PUT", "/api/v1/projects/{name}"): ("labqoat._generated.project", "Project"),
        ("POST", "/api/v1/projects/{name}/archive"): ("labqoat._generated.project", "Project"),
        ("GET", "/api/v1/projects/{name}/budget"): ("labqoat._generated.project_budget", "ProjectBudget"),
        ("PUT", "/api/v1/projects/{name}/budget"): ("labqoat._generated.project_budget", "ProjectBudget"),
        ("POST", "/api/v1/projects/{name}/moves"): ("labqoat._generated.project_move_result", "ProjectMoveResult"),
        ("POST", "/api/v1/projects/{name}/unarchive"): ("labqoat._generated.project", "Project"),
        ("GET", "/api/v1/queues"): ("labqoat._generated.queue_list", "QueueList"),
        ("GET", "/api/v1/queues/{name}"): ("labqoat._generated.queue_summary", "QueueSummary"),
        ("DELETE", "/api/v1/queues/{name}/items"): ("labqoat._generated.clear_receipt", "ClearReceipt"),
        ("GET", "/api/v1/queues/{name}/items"): ("labqoat._generated.queue_item_page", "QueueItemPage"),
        ("POST", "/api/v1/queues/{name}/items"): ("labqoat._generated.queue_put_receipt", "QueuePutReceipt"),
        ("POST", "/api/v1/queues/{name}/take"): ("labqoat._generated.queue_values", "QueueValues"),
        ("GET", "/api/v1/runs"): ("labqoat._generated.run_page", "RunPage"),
        ("POST", "/api/v1/runs"): ("labqoat._generated.run", "Run"),
        ("DELETE", "/api/v1/runs/{id}"): ("labqoat._generated.deletion_receipt", "DeletionReceipt"),
        ("GET", "/api/v1/runs/{id}"): ("labqoat._generated.run", "Run"),
        ("GET", "/api/v1/runs/{id}/attempts"): ("labqoat._generated.attempt_page", "AttemptPage"),
        ("GET", "/api/v1/runs/{id}/attempts/{attempt_id}/group"): (
            "labqoat._generated.distributed_group_page",
            "DistributedGroupPage",
        ),
        ("POST", "/api/v1/runs/{id}/cancel"): ("labqoat._generated.run", "Run"),
        ("GET", "/api/v1/runs/{id}/fit-budget"): ("labqoat._generated.fit_budget_history", "FitBudgetHistory"),
        ("POST", "/api/v1/runs/{id}/fit-budget/adjustments"): (
            "labqoat._generated.budget_adjustment",
            "BudgetAdjustment",
        ),
        ("POST", "/api/v1/runs/{id}/fit-budget/history"): ("labqoat._generated.fit_budget_history", "FitBudgetHistory"),
        ("GET", "/api/v1/runs/{id}/fit-budget/intervals"): (
            "labqoat._generated.fit_budget_intervals",
            "FitBudgetIntervals",
        ),
        ("GET", "/api/v1/runs/{id}/forks"): ("labqoat._generated.fork_page", "ForkPage"),
        ("POST", "/api/v1/runs/{id}/forks"): ("labqoat._generated.fork_lineage", "ForkLineage"),
        ("GET", "/api/v1/runs/{id}/lineage"): ("labqoat._generated.fork_lineage", "ForkLineage"),
        ("GET", "/api/v1/runs/{id}/logs"): ("labqoat._generated.log_page", "LogPage"),
        ("GET", "/api/v1/runs/{id}/metrics"): ("labqoat._generated.metric_page", "MetricPage"),
        ("GET", "/api/v1/runs/{id}/outputs"): ("labqoat._generated.output_page", "OutputPage"),
        ("GET", "/api/v1/runs/{id}/placement"): ("labqoat._generated.run_placement", "RunPlacement"),
        ("GET", "/api/v1/runs/{id}/produced-assets"): ("labqoat._generated.produced_asset_page", "ProducedAssetPage"),
        ("GET", "/api/v1/runs/{id}/recoveries"): ("labqoat._generated.recovery_page", "RecoveryPage"),
        ("POST", "/api/v1/runs/{id}/recoveries"): ("labqoat._generated.recovery_operation", "RecoveryOperation"),
        ("GET", "/api/v1/runs/{id}/recoveries/{operation_id}"): (
            "labqoat._generated.recovery_operation",
            "RecoveryOperation",
        ),
        ("POST", "/api/v1/runs/{id}/recoveries/{operation_id}/cancel"): (
            "labqoat._generated.recovery_operation",
            "RecoveryOperation",
        ),
        ("GET", "/api/v1/runs/{id}/recoveries/{operation_id}/workflow"): (
            "labqoat._generated.workflow_plan_page",
            "WorkflowPlanPage",
        ),
        ("GET", "/api/v1/runs/{id}/recovery"): ("labqoat._generated.recovery_discovery", "RecoveryDiscovery"),
        ("GET", "/api/v1/runs/{id}/recovery/workflow"): ("labqoat._generated.workflow_preview", "WorkflowPreview"),
        ("GET", "/api/v1/runs/{id}/shards"): ("labqoat._generated.shard_page", "ShardPage"),
        ("DELETE", "/api/v1/runs/{id}/tags/{tag}"): ("labqoat._generated.run", "Run"),
        ("PUT", "/api/v1/runs/{id}/tags/{tag}"): ("labqoat._generated.run", "Run"),
        ("GET", "/api/v1/secrets"): ("labqoat._generated.secret_list", "SecretList"),
        ("POST", "/api/v1/secrets"): ("labqoat._generated.secret", "Secret"),
        ("GET", "/api/v1/secrets/{name}"): ("labqoat._generated.secret", "Secret"),
        ("PUT", "/api/v1/secrets/{name}"): ("labqoat._generated.secret", "Secret"),
        ("GET", "/api/v1/status"): ("labqoat._generated.status", "Status"),
        ("GET", "/api/v1/volumes"): ("labqoat._generated.volume_list", "VolumeList"),
        ("POST", "/api/v1/volumes"): ("labqoat._generated.volume", "Volume"),
        ("GET", "/api/v1/volumes/{name}"): ("labqoat._generated.volume", "Volume"),
        ("GET", "/api/v1/worker-history"): ("labqoat._generated.worker_page", "WorkerPage"),
        ("GET", "/api/v1/worker-pools/{id}"): ("labqoat._generated.compute_worker_pool", "ComputeWorkerPool"),
        ("PATCH", "/api/v1/worker-pools/{id}"): ("labqoat._generated.compute_worker_pool", "ComputeWorkerPool"),
        ("GET", "/api/v1/worker/assets/item"): ("labqoat._generated.asset_record", "AssetRecord"),
        ("POST", "/api/v1/worker/assets/item/complete"): ("labqoat._generated.asset_record", "AssetRecord"),
        ("PUT", "/api/v1/worker/assets/item/content"): ("labqoat._generated.asset_record", "AssetRecord"),
        ("POST", "/api/v1/worker/assignments/begin"): ("labqoat._generated.worker_inputs", "WorkerInputs"),
        ("POST", "/api/v1/worker/assignments/claim"): ("labqoat._generated.worker_ack", "WorkerAck"),
        ("POST", "/api/v1/worker/assignments/complete"): ("labqoat._generated.worker_ack", "WorkerAck"),
        ("POST", "/api/v1/worker/assignments/fail"): ("labqoat._generated.worker_ack", "WorkerAck"),
        ("POST", "/api/v1/worker/assignments/finish"): ("labqoat._generated.worker_ack", "WorkerAck"),
        ("POST", "/api/v1/worker/assignments/heartbeat"): ("labqoat._generated.worker_heartbeat", "WorkerHeartbeat"),
        ("GET", "/api/v1/worker/assignments/inputs"): ("labqoat._generated.worker_inputs", "WorkerInputs"),
        ("POST", "/api/v1/worker/assignments/logs"): ("labqoat._generated.worker_ack", "WorkerAck"),
        ("POST", "/api/v1/worker/assignments/metrics"): ("labqoat._generated.worker_ack", "WorkerAck"),
        ("POST", "/api/v1/worker/assignments/output"): ("labqoat._generated.worker_ack", "WorkerAck"),
        ("POST", "/api/v1/worker/assignments/produced-assets"): ("labqoat._generated.worker_ack", "WorkerAck"),
        ("GET", "/api/v1/worker/assignments/shards"): (
            "labqoat._generated.worker_shard_snapshot",
            "WorkerShardSnapshot",
        ),
        ("POST", "/api/v1/worker/assignments/shards/claim"): ("labqoat._generated.worker_ack", "WorkerAck"),
        ("POST", "/api/v1/worker/assignments/shards/finish"): ("labqoat._generated.shard_outcome", "ShardOutcome"),
        ("POST", "/api/v1/worker/assignments/telemetry"): ("labqoat._generated.worker_ack", "WorkerAck"),
        ("GET", "/api/v1/worker/checkpoints/item"): ("labqoat._generated.checkpoint", "Checkpoint"),
        ("POST", "/api/v1/worker/checkpoints/publish"): ("labqoat._generated.checkpoint", "Checkpoint"),
        ("POST", "/api/v1/worker/datasets"): ("labqoat._generated.dataset_publication", "DatasetPublication"),
        ("GET", "/api/v1/worker/datasets/manifest"): (
            "labqoat._generated.dataset_revision_files",
            "DatasetRevisionFiles",
        ),
        ("GET", "/api/v1/worker/dicts"): ("labqoat._generated.dict_list", "DictList"),
        ("GET", "/api/v1/worker/dicts/{name}"): ("labqoat._generated.dict_summary", "DictSummary"),
        ("DELETE", "/api/v1/worker/dicts/{name}/entries"): ("labqoat._generated.clear_receipt", "ClearReceipt"),
        ("GET", "/api/v1/worker/dicts/{name}/entries"): ("labqoat._generated.dict_entry_page", "DictEntryPage"),
        ("PUT", "/api/v1/worker/dicts/{name}/entries"): ("labqoat._generated.dict_write", "DictWrite"),
        ("DELETE", "/api/v1/worker/dicts/{name}/entries/item"): ("labqoat._generated.dict_entry", "DictEntry"),
        ("GET", "/api/v1/worker/dicts/{name}/entries/item"): ("labqoat._generated.dict_entry", "DictEntry"),
        ("GET", "/api/v1/worker/fit/budget"): ("labqoat._generated.fit_budget_history", "FitBudgetHistory"),
        ("GET", "/api/v1/worker/memory/brief"): ("labqoat._generated.knowledge_brief", "KnowledgeBrief"),
        ("GET", "/api/v1/worker/memory/changes"): ("labqoat._generated.knowledge_view", "KnowledgeView"),
        ("POST", "/api/v1/worker/memory/commits"): ("labqoat._generated.knowledge_receipt", "KnowledgeReceipt"),
        ("GET", "/api/v1/worker/memory/revisions/item"): ("labqoat._generated.knowledge_node", "KnowledgeNode"),
        ("GET", "/api/v1/worker/memory/search"): ("labqoat._generated.knowledge_view", "KnowledgeView"),
        ("GET", "/api/v1/worker/queues"): ("labqoat._generated.queue_list", "QueueList"),
        ("GET", "/api/v1/worker/queues/{name}"): ("labqoat._generated.queue_summary", "QueueSummary"),
        ("DELETE", "/api/v1/worker/queues/{name}/items"): ("labqoat._generated.clear_receipt", "ClearReceipt"),
        ("GET", "/api/v1/worker/queues/{name}/items"): ("labqoat._generated.queue_item_page", "QueueItemPage"),
        ("POST", "/api/v1/worker/queues/{name}/items"): ("labqoat._generated.queue_put_receipt", "QueuePutReceipt"),
        ("POST", "/api/v1/worker/queues/{name}/take"): ("labqoat._generated.queue_values", "QueueValues"),
        ("POST", "/api/v1/worker/restore/acknowledgements"): ("labqoat._generated.restore_receipt", "RestoreReceipt"),
        ("POST", "/api/v1/worker/restore/groups/ranks"): (
            "labqoat._generated.distributed_rank_receipt",
            "DistributedRankReceipt",
        ),
        ("POST", "/api/v1/worker/runs"): ("labqoat._generated.run", "Run"),
        ("POST", "/api/v1/worker/runs/referenced"): ("labqoat._generated.child_outcome", "ChildOutcome"),
        ("POST", "/api/v1/worker/workflow/decisions"): (
            "labqoat._generated.workflow_decision_receipt",
            "WorkflowDecisionReceipt",
        ),
        ("GET", "/api/v1/workers"): ("labqoat._generated.worker_page", "WorkerPage"),
        ("GET", "/api/v1/workers/item"): ("labqoat._generated.worker", "Worker"),
        ("GET", "/api/v1/workers/item/logs"): ("labqoat._generated.worker_log_page", "WorkerLogPage"),
    }

    @staticmethod
    def validate(method: str, target: str, value: object) -> JsonDocument:
        """Validate and normalize one successful JSON response."""
        document = JsonDocument.expect_dict(value)
        selected = ResponseRegistry._lookup(method.upper(), urlsplit(target).path)
        if selected is None:
            return document
        module_name, title = selected
        model = getattr(import_module(module_name), title)
        factory = cast(Callable[[Mapping[str, JsonValue]], SerializableModel], model.from_dict)
        return factory(document).to_dict()

    @staticmethod
    def _lookup(method: str, path: str) -> tuple[str, str] | None:
        """Prefer literal routes, then match exact nonempty path-parameter segments."""
        exact = ResponseRegistry._MODELS.get((method, path))
        if exact is not None:
            return exact
        for (verb, template), model in ResponseRegistry._MODELS.items():
            if verb == method and "{" in template and ResponseRegistry._matches(template, path):
                return model
        return None

    @staticmethod
    def _matches(template: str, path: str) -> bool:
        """Keep method, static segments and path arity bound to the generated operation."""
        expected, actual = template.split("/"), path.split("/")
        if len(expected) != len(actual):
            return False
        return all(
            part == value or (part.startswith("{") and part.endswith("}") and bool(value))
            for part, value in zip(expected, actual, strict=True)
        )
