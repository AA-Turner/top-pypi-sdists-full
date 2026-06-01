"""
Datasets API Client for Aigie SDK

Manage datasets for testing and benchmarking LLM applications
"""

import asyncio
import builtins
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import httpx


@dataclass
class Dataset:
    """Dataset metadata"""

    id: str
    name: str
    example_count: int
    created_at: str
    updated_at: str
    description: str | None = None
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    project_name: str | None = None


@dataclass
class DatasetExample:
    """Dataset example"""

    id: str
    dataset_id: str
    input: Any
    created_at: str
    expected_output: Any | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)


@dataclass
class DatasetRunResult:
    """Dataset run result for a single example"""

    id: str
    dataset_id: str
    example_id: str
    output: Any
    execution_time: float
    created_at: str
    scores: list[dict[str, Any]] | None = None
    error: str | None = None
    trace_id: str | None = None


@dataclass
class DatasetRunSummary:
    """Dataset run summary"""

    id: str
    dataset_id: str
    total_examples: int
    successful_examples: int
    failed_examples: int
    total_execution_time: float
    created_at: str
    average_scores: dict[str, float] | None = None
    metadata: dict[str, Any] | None = None


class DatasetsClient:
    """
    Datasets API client for Aigie

    Provides methods for managing datasets and running evaluations

    Example:
        >>> from aigie.datasets import DatasetsClient
        >>>
        >>> client = DatasetsClient()
        >>>
        >>> # Create dataset
        >>> dataset = await client.create(
        ...     name="test-dataset",
        ...     description="Test cases for my agent"
        ... )
        >>>
        >>> # Add examples
        >>> await client.add_example(
        ...     dataset.id,
        ...     input={"query": "What is 2+2?"},
        ...     expected_output="4"
        ... )
        >>>
        >>> # Run evaluation
        >>> async def my_agent(example):
        ...     return await process(example.input)
        >>>
        >>> results = await client.run(dataset.id, my_agent)
    """

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize datasets client

        Args:
            api_url: API URL (defaults to AIGIE_API_URL env var)
            api_key: API key (defaults to AIGIE_API_KEY env var)
        """
        import os

        self.api_url = api_url or os.getenv("AIGIE_API_URL", "")
        self.api_key = api_key or os.getenv("AIGIE_API_KEY", "")
        self.client = httpx.AsyncClient(timeout=30.0)

    async def create(
        self,
        name: str,
        description: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        project_name: str | None = None,
    ) -> Dataset:
        """Create a new dataset"""
        data = {
            "name": name,
            "description": description,
            "tags": tags or [],
            "metadata": metadata or {},
            "project_name": project_name,
        }

        response = await self._request("POST", "/v1/datasets", json=data)
        return Dataset(**response)

    async def get(self, dataset_id: str) -> Dataset:
        """Get dataset by ID"""
        response = await self._request("GET", f"/v1/datasets/{dataset_id}")
        return Dataset(**response)

    async def list(
        self,
        project_name: str | None = None,
        tags: list[str] | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[Dataset], int]:
        """List all datasets"""
        params = {
            "limit": limit,
            "offset": offset,
        }

        if project_name:
            params["projectName"] = project_name
        if tags:
            params["tags"] = ",".join(tags)

        response = await self._request("GET", "/v1/datasets", params=params)

        # Backend may return a raw list or a dict with "datasets" key
        if isinstance(response, list):
            datasets = [Dataset(**d) for d in response]
            total = len(datasets)
        else:
            datasets = [Dataset(**d) for d in response.get("datasets", response.get("items", []))]
            total = response.get("total", len(datasets))

        return datasets, total

    async def update(
        self,
        dataset_id: str,
        name: str | None = None,
        description: str | None = None,
        tags: builtins.list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Dataset:
        """Update dataset"""
        data = {}

        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if tags is not None:
            data["tags"] = tags
        if metadata is not None:
            data["metadata"] = metadata

        response = await self._request("PATCH", f"/v1/datasets/{dataset_id}", json=data)
        return Dataset(**response)

    async def delete(self, dataset_id: str) -> None:
        """Delete dataset"""
        await self._request("DELETE", f"/v1/datasets/{dataset_id}")

    async def add_example(
        self,
        dataset_id: str,
        input: Any,
        expected_output: Any | None = None,
        metadata: dict[str, Any] | None = None,
        tags: builtins.list[str] | None = None,
    ) -> DatasetExample:
        """Add example to dataset"""
        data = {
            "input": input,
            "expectedOutput": expected_output,
            "metadata": metadata or {},
            "tags": tags or [],
        }

        response = await self._request("POST", f"/v1/datasets/{dataset_id}/examples", json=data)
        return DatasetExample(**response)

    async def add_examples(
        self,
        dataset_id: str,
        examples: builtins.list[dict[str, Any]],
    ) -> tuple[builtins.list[DatasetExample], int]:
        """Add multiple examples to dataset"""
        data = {"examples": examples}

        response = await self._request(
            "POST", f"/v1/datasets/{dataset_id}/examples/batch", json=data
        )

        examples_list = [DatasetExample(**e) for e in response["examples"]]
        count = response["count"]

        return examples_list, count

    async def get_examples(
        self,
        dataset_id: str,
        limit: int = 100,
        offset: int = 0,
        tags: builtins.list[str] | None = None,
    ) -> tuple[builtins.list[DatasetExample], int]:
        """Get examples from dataset"""
        params = {
            "limit": limit,
            "offset": offset,
        }

        if tags:
            params["tags"] = ",".join(tags)

        response = await self._request("GET", f"/v1/datasets/{dataset_id}/examples", params=params)

        examples = [DatasetExample(**e) for e in response["examples"]]
        total = response["total"]

        return examples, total

    async def delete_example(self, dataset_id: str, example_id: str) -> None:
        """Delete example from dataset"""
        await self._request("DELETE", f"/v1/datasets/{dataset_id}/examples/{example_id}")

    async def run(
        self,
        dataset_id: str,
        fn: Callable[[DatasetExample], Any],
        evaluators: builtins.list[Any] | None = None,
        metadata: dict[str, Any] | None = None,
        concurrency: int = 1,
    ) -> DatasetRunSummary:
        """
        Run function on dataset

        Executes the provided function on each example in the dataset
        and records the results

        Args:
            dataset_id: Dataset ID
            fn: Function to run on each example
            evaluators: Optional list of evaluators
            metadata: Optional run metadata
            concurrency: Number of concurrent executions

        Returns:
            DatasetRunSummary with results
        """
        from .client import Aigie

        # Get Aigie client for tracing
        try:
            aigie = Aigie._instance
        except AttributeError:
            aigie = None

        # Get all examples
        examples, _ = await self.get_examples(dataset_id)

        # Create run
        run_id = str(uuid.uuid4())
        results: list[DatasetRunResult] = []
        start_time = datetime.now()

        # Process examples with concurrency
        semaphore = asyncio.Semaphore(concurrency)

        async def process_example(example: DatasetExample) -> DatasetRunResult:
            async with semaphore:
                example_start_time = datetime.now()

                try:
                    # Run function with tracing if available
                    if aigie:
                        async with aigie.trace(f"dataset-example-{example.id}") as trace:
                            trace.set_metadata(
                                {
                                    "dataset_id": dataset_id,
                                    "example_id": example.id,
                                    "run_id": run_id,
                                }
                            )

                            output = await fn(example)
                            trace_id = trace.id
                    else:
                        output = await fn(example)
                        trace_id = None

                    execution_time = (datetime.now() - example_start_time).total_seconds()

                    # Run evaluators if provided
                    scores = None

                    if evaluators:
                        scores = []
                        for evaluator in evaluators:
                            result = await evaluator.evaluate(
                                example.input,
                                output,
                                example.expected_output,
                            )

                            scores.append(
                                {
                                    "name": evaluator.name,
                                    "value": result.score,
                                    "passed": result.passed,
                                    "reasoning": result.reasoning,
                                }
                            )

                    return DatasetRunResult(
                        id=str(uuid.uuid4()),
                        dataset_id=dataset_id,
                        example_id=example.id,
                        output=output,
                        scores=scores,
                        execution_time=execution_time,
                        trace_id=trace_id,
                        created_at=datetime.now().isoformat(),
                    )

                except Exception as error:
                    execution_time = (datetime.now() - example_start_time).total_seconds()

                    return DatasetRunResult(
                        id=str(uuid.uuid4()),
                        dataset_id=dataset_id,
                        example_id=example.id,
                        output=None,
                        execution_time=execution_time,
                        error=str(error),
                        trace_id=None,
                        created_at=datetime.now().isoformat(),
                    )

        # Process all examples
        results = await asyncio.gather(*[process_example(ex) for ex in examples])

        total_execution_time = (datetime.now() - start_time).total_seconds()

        # Calculate summary
        summary = DatasetRunSummary(
            id=run_id,
            dataset_id=dataset_id,
            total_examples=len(examples),
            successful_examples=len([r for r in results if not r.error]),
            failed_examples=len([r for r in results if r.error]),
            total_execution_time=total_execution_time,
            metadata=metadata,
            created_at=datetime.now().isoformat(),
        )

        # Calculate average scores
        if evaluators:
            average_scores = {}

            for evaluator in evaluators:
                scores_list = [
                    score["value"]
                    for result in results
                    if result.scores
                    for score in result.scores
                    if score["name"] == evaluator.name
                ]

                if scores_list:
                    average_scores[evaluator.name] = sum(scores_list) / len(scores_list)

            summary.average_scores = average_scores

        # Save run to API
        await self._save_run(summary, results)

        return summary

    async def get_run_results(
        self, run_id: str
    ) -> tuple[DatasetRunSummary, builtins.list[DatasetRunResult]]:
        """Get run results"""
        response = await self._request("GET", f"/v1/dataset-runs/{run_id}")

        summary = DatasetRunSummary(**response["summary"])
        results = [DatasetRunResult(**r) for r in response["results"]]

        return summary, results

    async def list_runs(
        self,
        dataset_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[builtins.list[DatasetRunSummary], int]:
        """List runs for dataset"""
        params = {
            "limit": limit,
            "offset": offset,
        }

        response = await self._request("GET", f"/v1/datasets/{dataset_id}/runs", params=params)

        runs = [DatasetRunSummary(**r) for r in response["runs"]]
        total = response["total"]

        return runs, total

    async def _save_run(self, summary: DatasetRunSummary, results: builtins.list[DatasetRunResult]) -> None:
        """Save run results to API"""
        data = {
            "summary": {
                "id": summary.id,
                "dataset_id": summary.dataset_id,
                "total_examples": summary.total_examples,
                "successful_examples": summary.successful_examples,
                "failed_examples": summary.failed_examples,
                "total_execution_time": summary.total_execution_time,
                "average_scores": summary.average_scores,
                "metadata": summary.metadata,
                "created_at": summary.created_at,
            },
            "results": [
                {
                    "id": r.id,
                    "dataset_id": r.dataset_id,
                    "example_id": r.example_id,
                    "output": r.output,
                    "scores": r.scores,
                    "execution_time": r.execution_time,
                    "error": r.error,
                    "trace_id": r.trace_id,
                    "created_at": r.created_at,
                }
                for r in results
            ],
        }

        await self._request("POST", "/v1/dataset-runs", json=data)

    async def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Make HTTP request to API"""
        url = f"{self.api_url}{path}"

        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }

        try:
            response = await self.client.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=headers,
            )

            response.raise_for_status()

            return response.json()

        except httpx.HTTPError as error:
            print(f"Datasets API Error [{method} {path}]: {error}")
            raise

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
