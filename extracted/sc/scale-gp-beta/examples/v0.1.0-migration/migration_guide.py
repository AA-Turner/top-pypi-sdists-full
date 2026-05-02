# pyright: basic
# type: ignore
"""
Migration Guide: scale-gp-beta v0.1.0-alpha.x -> v0.1.0

This file demonstrates before/after code for every breaking change in v0.1.0.
Each function shows the OLD pattern (commented out) and the NEW pattern.

NOTE: This file targets the v0.1.0 API. Type errors are expected if checked
against an alpha version of the SDK.

See BREAKING_CHANGES.md at the repo root for full documentation.
"""

from __future__ import annotations

from scale_gp_beta import SGPClient

client = SGPClient(api_key="your-api-key", account_id="your-account-id")


# =============================================================================
# Section 1: Method Signatures — Nested Object Parameters
# =============================================================================


def evaluation_create_standalone() -> None:
    """Create an evaluation with inline data."""

    # BEFORE (alpha):
    # client.evaluations.create(
    #     name="my-eval",
    #     data=[{"input": "hello", "expected": "world"}],
    #     tags=["v1"],
    #     tasks=[{"type": "human", "name": "review"}],
    # )

    # AFTER (v0.1.0):
    client.evaluations.create(
        evaluation={
            "name": "my-eval",
            "data": [{"input": "hello", "expected": "world"}],
            "tags": ["v1"],
            "tasks": [{"type": "human", "name": "review"}],
        }
    )


def evaluation_create_from_dataset() -> None:
    """Create an evaluation referencing an existing dataset."""

    # BEFORE (alpha):
    # client.evaluations.create(
    #     name="my-eval",
    #     dataset_id="ds_123",
    # )

    # AFTER (v0.1.0):
    client.evaluations.create(
        evaluation={
            "name": "my-eval",
            "dataset_id": "ds_123",
        }
    )


def evaluation_create_with_new_dataset() -> None:
    """Create an evaluation that also creates a reusable dataset."""

    # BEFORE (alpha):
    # client.evaluations.create(
    #     name="my-eval",
    #     data=[{"input": "hello"}],
    #     dataset={"name": "my-dataset"},
    # )

    # AFTER (v0.1.0):
    client.evaluations.create(
        evaluation={
            "name": "my-eval",
            "data": [{"input": "hello"}],
            "dataset": {"name": "my-dataset"},
        }
    )


def evaluation_update() -> None:
    """Update an evaluation, including restore."""

    # BEFORE (alpha):
    # client.evaluations.update("eval_123", name="new-name", tags=["v2"])
    # client.evaluations.update("eval_123", restore=True)

    # AFTER (v0.1.0):
    client.evaluations.update("eval_123", evaluation={"name": "new-name", "tags": ["v2"]})
    client.evaluations.update("eval_123", evaluation={"restore": True})


def model_create() -> None:
    """Create a model (Launch or LLM Engine)."""

    # BEFORE (alpha):
    # client.models.create(
    #     name="my-model",
    #     vendor_configuration={
    #         "model_image": {"registry": "us-docker", "repository": "my-repo", "tag": "latest", "command": ["serve"]},
    #         "model_infra": {"gpus": 1, "gpu_type": "nvidia-ampere-a10"},
    #     },
    #     model_vendor="launch",
    # )

    # AFTER (v0.1.0):
    client.models.create(
        model={
            "name": "my-model",
            "vendor_configuration": {
                "model_image": {
                    "registry": "us-docker",
                    "repository": "my-repo",
                    "tag": "latest",
                    "command": ["serve"],
                },
                "model_infra": {"gpus": 1, "gpu_type": "nvidia-ampere-a10"},
            },
            "model_vendor": "launch",
        }
    )


def model_update() -> None:
    """Update a model — metadata, vendor config, or name swap."""

    # BEFORE (alpha) — three separate overloads:
    # client.models.update("model_123", model_metadata={"key": "value"})
    # client.models.update("model_123", vendor_configuration={...})
    # client.models.update("model_123", name="new-name", on_conflict="swap")

    # AFTER (v0.1.0) — single param, dict shape determines variant:
    client.models.update("model_123", model={"model_metadata": {"key": "value"}})
    client.models.update("model_123", model={"name": "new-name", "on_conflict": "swap"})


def question_create() -> None:
    """Create a question (categorical, rating, number, free_text, form, or timestamp)."""

    # BEFORE (alpha) — per-type overloads:
    # client.questions.create(
    #     name="quality",
    #     prompt="Rate the quality",
    #     question_type="categorical",
    #     configuration={"choices": ["good", "bad"], "multi": False},
    # )

    # AFTER (v0.1.0) — single nested param:
    client.questions.create(
        question={
            "name": "quality",
            "prompt": "Rate the quality",
            "question_type": "categorical",
            "configuration": {"choices": ["good", "bad"], "multi": False},
        }
    )


def question_create_rating() -> None:
    """Create a rating question."""

    # BEFORE (alpha):
    # client.questions.create(
    #     name="helpfulness",
    #     prompt="Rate helpfulness",
    #     question_type="rating",
    #     configuration={"min_label": "Bad", "max_label": "Great", "steps": 5},
    # )

    # AFTER (v0.1.0):
    client.questions.create(
        question={
            "name": "helpfulness",
            "prompt": "Rate helpfulness",
            "question_type": "rating",
            "configuration": {"min_label": "Bad", "max_label": "Great", "steps": 5},
        }
    )


def rubric_update() -> None:
    """Update a rubric, including restore."""

    # BEFORE (alpha) — flat kwargs with overloads:
    # client.rubrics.update("r_123", title="Updated Title", tags=["new-tag"])
    # client.rubrics.update("r_123", restore=True)

    # AFTER (v0.1.0) — nested rubric param:
    client.rubrics.update("r_123", rubric={"title": "Updated Title", "tags": ["new-tag"]})
    client.rubrics.update("r_123", rubric={"restore": True})


def rubric_create_with_criteria() -> None:
    """Create a rubric — criteria param type changed."""

    # BEFORE (alpha):
    # from scale_gp_beta.types import rubric_create_params
    # criteria: list[rubric_create_params.Criterion] = [
    #     {"title": "Accuracy", "weight": 1.0},
    #     {"title": "Relevance", "weight": 0.5},
    # ]
    # client.rubrics.create(title="My Rubric", criteria=criteria)

    # AFTER (v0.1.0):
    from scale_gp_beta.types.rubrics import RubricCriteriaInputParam

    criteria: list[RubricCriteriaInputParam] = [
        {"title": "Accuracy", "weight": 1.0},
        {"title": "Relevance", "weight": 0.5},
    ]
    client.rubrics.create(title="My Rubric", criteria=criteria)


def dataset_update() -> None:
    """Update a dataset, including restore."""

    # BEFORE (alpha):
    # client.datasets.update("ds_123", name="new-name", tags=["v2"])
    # client.datasets.update("ds_123", restore=True)

    # AFTER (v0.1.0):
    client.datasets.update("ds_123", dataset={"name": "new-name", "tags": ["v2"]})
    client.datasets.update("ds_123", dataset={"restore": True})


# =============================================================================
# Section 2: Method Renames
# =============================================================================


def question_delete_to_archive() -> None:
    """questions.delete() renamed to questions.archive()."""

    # BEFORE (alpha):
    # client.questions.delete("q_123")

    # AFTER (v0.1.0):
    client.questions.archive("q_123")


def rubric_delete_to_archive() -> None:
    """rubrics.delete() renamed to rubrics.archive(). Return type: RubricArchiveResponse."""

    # BEFORE (alpha):
    # from scale_gp_beta.types import RubricDeleteResponse
    # result: RubricDeleteResponse = client.rubrics.delete("r_123")

    # AFTER (v0.1.0):
    from scale_gp_beta.types import RubricArchiveResponse

    result: RubricArchiveResponse = client.rubrics.archive("r_123")


def dataset_delete_to_archive() -> None:
    """datasets.delete() renamed to datasets.archive(). Return type: DatasetArchiveResponse."""

    # BEFORE (alpha):
    # from scale_gp_beta.types import DatasetDeleteResponse
    # result: DatasetDeleteResponse = client.datasets.delete("ds_123")

    # AFTER (v0.1.0):
    from scale_gp_beta.types import DatasetArchiveResponse

    result: DatasetArchiveResponse = client.datasets.archive("ds_123")


def dataset_item_delete_to_archive() -> None:
    """dataset_items.delete() renamed to dataset_items.archive(). Return type: DatasetItemArchiveResponse."""

    # BEFORE (alpha):
    # from scale_gp_beta.types import DatasetItemDeleteResponse
    # result: DatasetItemDeleteResponse = client.dataset_items.delete("di_123")

    # AFTER (v0.1.0):
    from scale_gp_beta.types import DatasetItemArchiveResponse

    result: DatasetItemArchiveResponse = client.dataset_items.archive("di_123")


def evaluation_delete_to_archive() -> None:
    """evaluations.delete() renamed to evaluations.archive()."""

    # BEFORE (alpha):
    # client.evaluations.delete("eval_123")

    # AFTER (v0.1.0):
    client.evaluations.archive("eval_123")


def evaluation_group_delete_to_archive() -> None:
    """evaluation_groups.delete() renamed to evaluation_groups.archive()."""

    # BEFORE (alpha):
    # client.evaluation_groups.delete("grp_123")

    # AFTER (v0.1.0):
    client.evaluation_groups.archive("grp_123")


def evaluation_dashboard_delete_to_archive() -> None:
    """evaluation_dashboards.delete() renamed to evaluation_dashboards.archive()."""

    # BEFORE (alpha):
    # client.evaluation_dashboards.delete("dash_123")

    # AFTER (v0.1.0):
    client.evaluation_dashboards.archive("dash_123")


def dashboard_widget_delete_to_remove() -> None:
    """evaluation_dashboards.widgets.delete() renamed to widgets.remove()."""

    # BEFORE (alpha):
    # client.evaluation_dashboards.widgets.delete("w_123", dashboard_id="dash_123")

    # AFTER (v0.1.0):
    client.evaluation_dashboards.widgets.remove("w_123", dashboard_id="dash_123")


def criteria_add_to_create() -> None:
    """rubrics.criteria.add() renamed to rubrics.criteria.create()."""

    # BEFORE (alpha):
    # client.rubrics.criteria.add("r_123", title="Criterion A", weight=1.0)

    # AFTER (v0.1.0):
    client.rubrics.criteria.create("r_123", title="Criterion A", weight=1.0)


# =============================================================================
# Section 3: Response Type Consolidation
# =============================================================================


def build_response_types() -> None:
    """Build response types consolidated into AgentexCloudBuild."""

    # BEFORE (alpha):
    # from scale_gp_beta.types import (
    #     BuildCreateResponse,
    #     BuildRetrieveResponse,
    #     BuildListResponse,
    # )
    # created: BuildCreateResponse = client.build.create(...)
    # retrieved: BuildRetrieveResponse = client.build.retrieve("build_123")
    # builds: SyncCursorPage[BuildListResponse] = client.build.list()

    # AFTER (v0.1.0):
    from scale_gp_beta.types import AgentexCloudBuild

    retrieved: AgentexCloudBuild = client.build.retrieve("build_123")
    cancelled: AgentexCloudBuild = client.build.cancel("build_123")  # was `object`


def deploy_response_types() -> None:
    """Deploy response types consolidated into AgentexCloudDeploy."""

    # BEFORE (alpha):
    # from scale_gp_beta.types import (
    #     DeployCreateResponse,
    #     DeployRetrieveResponse,
    #     DeployListResponse,
    # )

    # AFTER (v0.1.0):
    from scale_gp_beta.types import AgentexCloudDeploy

    deploy: AgentexCloudDeploy = client.deploy.retrieve("deploy_123")


def rubric_response_types() -> None:
    """Rubric response types consolidated into RubricResponse."""

    # BEFORE (alpha):
    # from scale_gp_beta.types import (
    #     RubricCreateResponse,
    #     RubricRetrieveResponse,
    #     RubricUpdateResponse,
    #     RubricListResponse,
    #     RubricDeleteResponse,
    # )

    # AFTER (v0.1.0):
    from scale_gp_beta.types import RubricResponse, RubricArchiveResponse

    rubric: RubricResponse = client.rubrics.retrieve("r_123")
    archived: RubricArchiveResponse = client.rubrics.archive("r_123")


def criteria_response_types() -> None:
    """Criterion response types consolidated into RubricCriteriaResponse."""

    # BEFORE (alpha):
    # from scale_gp_beta.types.rubrics import CriterionCreateResponse, CriterionUpdateResponse

    # AFTER (v0.1.0):
    from scale_gp_beta.types.rubrics import RubricCriteriaResponse

    result: RubricCriteriaResponse = client.rubrics.criteria.create("r_123", title="A", weight=1.0)


def dataset_response_types() -> None:
    """Dataset delete response types renamed."""

    # BEFORE (alpha):
    # from scale_gp_beta.types import DatasetDeleteResponse, DatasetItemDeleteResponse

    # AFTER (v0.1.0):
    from scale_gp_beta.types import DatasetArchiveResponse, DatasetItemArchiveResponse

    ds_result: DatasetArchiveResponse = client.datasets.archive("ds_123")
    di_result: DatasetItemArchiveResponse = client.dataset_items.archive("di_123")


def span_batch_response_type() -> None:
    """SpanBatchResponse and SpanUpsertBatchResponse renamed to APIListSpan."""

    # BEFORE (alpha):
    # from scale_gp_beta.types import SpanBatchResponse, SpanUpsertBatchResponse

    # AFTER (v0.1.0):

    # Both spans.batch() and spans.upsert_batch() now return APIListSpan.
    # The `items` parameter type changed from span_batch_params.Item to SpanCreateParam.


# =============================================================================
# Section 4: Type Renames
# =============================================================================


def file_type_renamed() -> None:
    """File renamed to SGPFile."""

    # BEFORE (alpha):
    # from scale_gp_beta.types import File
    # my_file: File = client.files.retrieve("file_123")

    # AFTER (v0.1.0):
    from scale_gp_beta.types import SGPFile

    my_file: SGPFile = client.files.retrieve("file_123")


def response_type_removed() -> None:
    """Response type removed from exports."""

    # BEFORE (alpha):
    # from scale_gp_beta.types import Response

    # AFTER (v0.1.0):
    # The Response type no longer exists. Use ResponseCreateResponse for
    # the return type of client.responses.create().


# =============================================================================
# Section 5: Literal → Enum Type Changes
# =============================================================================


def sort_order_type() -> None:
    """sort_order param type changed from Literal to SortOrder."""

    # BEFORE (alpha):
    # from typing import Literal
    # sort_order: Literal["asc", "desc"] = "asc"
    # client.evaluations.list(sort_order=sort_order)

    # AFTER (v0.1.0):
    # String values "asc"/"desc" still work at runtime. The type annotation changed.
    from scale_gp_beta.types.chat import SortOrder

    sort_order: SortOrder = "asc"
    client.evaluations.list(sort_order=sort_order)


def evaluation_views_type() -> None:
    """views param type changed from Literal to EvaluationViews / EvaluationGroupViews."""

    # BEFORE (alpha):
    # from typing import List, Literal
    # views: List[Literal["tasks"]] = ["tasks"]
    # client.evaluations.list(views=views)

    # AFTER (v0.1.0):

    client.evaluations.list(views=["tasks"])  # views param typed as EvaluationViews
    client.evaluation_groups.list(views=["members"])  # views param typed as EvaluationGroupViews


def widget_type_enum() -> None:
    """Widget type param changed from Literal to EvaluationWidgetTypeEnum."""

    # BEFORE (alpha):
    # from typing import Literal
    # widget_type: Literal["bar", "histogram", "donut", ...] = "bar"

    # AFTER (v0.1.0):

    # String values still work at runtime.


def export_format_and_method_types() -> None:
    """Export format/method params changed from Literal to ExportFormat/ExportMethod."""

    # BEFORE (alpha):
    # from typing import Literal
    # export_format: Literal["json", "jsonl", "csv"] = "json"
    # export_method: Literal["signed_url", "direct"] = "signed_url"

    # AFTER (v0.1.0):

    # String values still work at runtime.


# =============================================================================
# Section 6: Vector Store Pagination
# =============================================================================
# The vector store list endpoint now uses `items` and `starting_after` as the
# standard field/param names, consistent with all other V5 paginated endpoints.
#
# DEPRECATED (will be removed in a future release):
#   - Response field `vectors` — use `items` instead
#   - Query param `cursor` — use `starting_after` instead
# =============================================================================


def vector_store_type_changes() -> None:
    """VectorRetrieveResponse → VectorDocument, VectorListResponse → paginated cursor page."""

    # BEFORE (alpha):
    # from scale_gp_beta.types.vector_stores import VectorRetrieveResponse, VectorListResponse
    # doc: VectorRetrieveResponse = client.vector_stores.vectors.retrieve("my-store", "doc_123")
    # response: VectorListResponse = client.vector_stores.vectors.list("my-store")
    # for vec in response.vectors:
    #     print(vec.id)

    # AFTER (v0.1.0):
    from scale_gp_beta.types.vector_stores import VectorDocument

    doc: VectorDocument = client.vector_stores.vectors.retrieve("my-store", "doc_123")  # noqa: F841
    # list() now returns a paginated SyncCursorPageVectors[VectorDocument]
    page = client.vector_stores.vectors.list("my-store")
    for item in page.items:
        print(item.id)


def vector_store_list_preferred() -> None:
    """Use `items` and `starting_after` (preferred pattern)."""

    # DEPRECATED — do not use `cursor` or access `.vectors`:
    # page = client.vector_stores.vectors.list("my-store", cursor="doc_abc")
    # docs = page.vectors

    # PREFERRED (v0.1.0):
    page = client.vector_stores.vectors.list("my-store", starting_after="doc_abc", limit=100)
    docs = page.items  # not page.vectors
    for doc in docs:
        print(doc.id)


def vector_store_list_auto_pagination() -> None:
    """Auto-pagination uses `starting_after` internally — just iterate."""

    # The SDK handles pagination automatically. Access results via `items`.
    all_pages = client.vector_stores.vectors.list("my-store", limit=100)
    for doc in all_pages:
        print(doc.id)
