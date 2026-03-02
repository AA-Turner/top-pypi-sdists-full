import dlt
from dlt.sources import DltSource
import dlthub
from dlt.common.pipeline import LoadInfo
from dlt.common.utils import custom_environ
from typing import Any, Dict, Optional, Union, Sequence, cast
from tenacity import Retrying, stop_after_attempt
from dlt.pipeline.typing import TPipelineStep
from dlt.pipeline import Pipeline

from dlthub._runner.prefect_collector import PrefectCollector
from prefect import task, flow
from prefect.futures import wait
from prefect.cache_policies import NO_CACHE

DEFAULT_RETRY_NO_RETRY = Retrying(stop=stop_after_attempt(1), reraise=True)


# TODO: fix types
def create_run_pipeline_task(  # type: ignore[no-untyped-def]
    log_prints: bool = True,
    run_from_clean_folder: bool = False,
    store_trace_info: Union[bool, Pipeline] = False,
    retry_policy: Retrying = DEFAULT_RETRY_NO_RETRY,
    retry_pipeline_steps: Sequence[TPipelineStep] = ("load",),
    extract_workers: Optional[int] = None,
    load_workers: Optional[int] = None,
    normalize_workers: Optional[int] = None,
    normalize_file_max_bytes: Optional[int] = None,
    normalize_file_max_items: Optional[int] = None,
    **task_kwargs: Any,
):
    """
    Creates and returns a Prefect task for running a pipeline with given data with dlthub.runner()
    This allows dynamic task creation with custom parameters.
    note: CACHE_POLICY will automatically be set to NO_CACHE

    Args:
        log_prints (bool): Whether to log print statements. Defaults to True.
        task_run_name (str): Template for task run name. Defaults to "run_{task_name}".
        store_trace_info (Union[bool, dlt.Pipeline]): Whether to store trace info.
        run_from_clean_folder (bool): Whether to run from a clean folder.
        retry_policy (Retrying): The retry policy to use for running the pipeline.
        retry_pipeline_steps (Sequence[TPipelineStep]): Pipeline steps to retry on
            failure. Defaults to ("load",).
        extract_workers: Number of extract workers for this pipeline
        load_workers: Number of load workers for this pipeline
        normalize_workers: Number of normalize workers for this pipeline
        normalize_file_max_bytes: Max bytes per normalize file for this pipeline
        normalize_file_max_items: Max items per normalize file for this pipeline
        **task_kwargs: Additional keyword arguments to pass to the @task decorator.

    Returns:
        Task: A Prefect task function that can be called or submitted.

    Example:
        @flow
        def my_flow():
            pipeline = dlt.pipeline(...)
            source = sql_database(...)
            run_dlt = create_run_pipeline_task(
                runner_args={"store_trace_info": True},
                task_run_name="run_my_pipeline",
            )
            # execute
            load_info = run_dlt(
                pipeline,
                source,
                task_name="my_task_name",
                write_disposition="write_append",
            )
            print(load_info)
    """

    @task(
        log_prints=log_prints,
        task_run_name="run_{task_name}",
        cache_policy=NO_CACHE,
        **task_kwargs,
    )
    def run_pipeline_task(
        pipeline: dlt.Pipeline,
        data: Any,
        task_name: str,
        **run_kwargs: Any,
    ) -> LoadInfo:
        pipeline.collector = PrefectCollector()

        # Build environment variables for pipeline-specific parallelism settings
        env_vars = build_pipeline_env_vars(
            pipeline.pipeline_name,
            extract_workers=extract_workers,
            load_workers=load_workers,
            normalize_workers=normalize_workers,
            normalize_file_max_bytes=normalize_file_max_bytes,
            normalize_file_max_items=normalize_file_max_items,
        )

        # Execute with temporarily set environment variables
        with custom_environ(env_vars):
            return dlthub.runner(
                pipeline,
                store_trace_info=store_trace_info,
                run_from_clean_folder=run_from_clean_folder,
                retry_policy=retry_policy,
                retry_pipeline_steps=retry_pipeline_steps,
            ).run(data=data, **run_kwargs)

    return run_pipeline_task


# TODO: fix types
def create_run_pipeline_flow(  # type: ignore[no-untyped-def]
    pipeline: dlt.Pipeline,
    source: DltSource,
    decompose: bool = False,
    flow_name: str = "run_pipeline",
    run_from_clean_folder: bool = True,
    store_trace_info: Union[bool, Pipeline] = False,
    retry_policy: Retrying = DEFAULT_RETRY_NO_RETRY,
    retry_pipeline_steps: Sequence[TPipelineStep] = ("load",),
    task_runner_args: Dict[str, Any] = {"log_prints": True},
    extract_workers: Optional[int] = None,
    load_workers: Optional[int] = None,
    normalize_workers: Optional[int] = None,
    normalize_file_max_bytes: Optional[int] = None,
    normalize_file_max_items: Optional[int] = None,
    **flow_kwargs: Any,
):
    """
    Creates and returns a Prefect flow for running a pipeline with a source using dlthub.runner()
    The pipeline and source are captured in the flow, so the returned flow only needs run_kwargs.

    Args:
        pipeline (dlt.Pipeline): The pipeline to use for running.
        source (DltSource): The source to run.
        decompose (bool): Whether to decompose the source and run in parallel tasks.
        flow_name (str): Name for the flow. Defaults to "run_pipeline".
        run_from_clean_folder (bool): Whether to run from a clean folder.
        store_trace_info (Union[bool, dlt.Pipeline]): Whether to store trace info.
        retry_policy (Retrying): The retry policy to use for running the pipeline.
        retry_pipeline_steps (Sequence[TPipelineStep]): Pipeline steps to retry on
            failure. Defaults to ("load",).
        task_runner_args (Dict[str, Any]): Arguments to pass to the task creation
        extract_workers: Number of extract workers for this pipeline
        load_workers: Number of load workers for this pipeline
        normalize_workers: Number of normalize workers for this pipeline
        normalize_file_max_bytes: Max bytes per normalize file for this pipeline
        normalize_file_max_items: Max items per normalize file for this pipeline
        **flow_kwargs: Additional keyword arguments to pass to the @flow decorator.

    Returns:
        Flow: A Prefect flow function that can be called with just run_kwargs.

    Example:
        # Simple pipeline run
        simple_flow = create_run_pipeline_flow(
            pipeline=my_pipeline,
            source=my_source,
            flow_name="simple_run",
        )
        simple_flow(**run_kwargs)

        # Decomposed parallel run
        decomposed_flow = create_run_pipeline_flow(
            pipeline=my_pipeline,
            source=my_source,
            decompose=True,
            flow_name="parallel_run",
            store_trace_info=True,
            task_runner_args={"log_prints": True},
        )
        decomposed_flow(**run_kwargs)
    """
    if pipeline.dev_mode:
        raise ValueError("Cannot decompose pipelines with `dev_mode=True`")

    if decompose:
        # Decomposed parallel execution flow
        @flow(
            name=f"dlt-{flow_name}",
            **flow_kwargs,
        )
        def decomposed_pipeline_flow(**run_kwargs: Any) -> None:
            """
            WARNING: Experimental, do not use in production
            Decomposes source into scc, uses task-pipeline for each.
            Runs first source to establish schema, then all others in parallel tasks
            """
            sources = source.decompose(strategy="scc")
            is_using_custom_trace_pipeline = isinstance(store_trace_info, Pipeline)

            # run first source
            # logic to create source-specific task pipeline and (if required) trace pipeline
            # TODO: should be more DRY
            first_source = sources[0]
            task_name = make_task_name(pipeline, first_source)
            task_pipeline = _make_task_pipeline(pipeline, task_name)
            if is_using_custom_trace_pipeline:
                trace_pipeline = cast(Pipeline, store_trace_info)
                trace_task_name = f"trace_{make_task_name(trace_pipeline, first_source)}"
                store_task_trace_info = _make_task_pipeline(trace_pipeline, trace_task_name)
            else:
                store_task_trace_info = store_trace_info  # type: ignore[assignment]

            # create task
            run_first_source_task = create_run_pipeline_task(
                store_trace_info=store_task_trace_info,
                run_from_clean_folder=run_from_clean_folder,
                retry_policy=retry_policy,
                retry_pipeline_steps=retry_pipeline_steps,
                extract_workers=extract_workers,
                load_workers=load_workers,
                normalize_workers=normalize_workers,
                normalize_file_max_bytes=normalize_file_max_bytes,
                normalize_file_max_items=normalize_file_max_items,
                **task_runner_args,
            )

            # run it
            run_first_source_task(
                task_pipeline,
                first_source,
                task_name,
                **run_kwargs,
            )

            # run rest of sources in parallel
            futures = []
            for s in sources[1:]:
                # prepare task- and trace-pipelines
                task_name = make_task_name(pipeline, s)
                task_pipeline = _make_task_pipeline(pipeline, task_name)
                if is_using_custom_trace_pipeline:
                    trace_pipeline = cast(Pipeline, store_trace_info)
                    trace_task_name = f"trace_{make_task_name(trace_pipeline, s)}"
                    store_task_trace_info = _make_task_pipeline(trace_pipeline, trace_task_name)
                else:
                    store_task_trace_info = store_trace_info  # type: ignore[assignment]

                # create task
                run_task = create_run_pipeline_task(
                    store_trace_info=store_task_trace_info,
                    run_from_clean_folder=run_from_clean_folder,
                    retry_policy=retry_policy,
                    retry_pipeline_steps=retry_pipeline_steps,
                    extract_workers=extract_workers,
                    load_workers=load_workers,
                    normalize_workers=normalize_workers,
                    normalize_file_max_bytes=normalize_file_max_bytes,
                    normalize_file_max_items=normalize_file_max_items,
                    **task_runner_args,
                )

                # run it
                future = run_task.submit(
                    task_pipeline,
                    s,
                    task_name,
                    **run_kwargs,
                )
                futures.append(future)

            wait(futures)

        return decomposed_pipeline_flow
    else:
        # Simple single task execution flow
        @flow(
            name=f"dlt-{flow_name}",
            **flow_kwargs,
        )
        def simple_pipeline_flow(**run_kwargs: Any) -> None:
            """
            Runs the pipeline with the source in a single task.
            """
            run_task = create_run_pipeline_task(
                store_trace_info=store_trace_info,
                run_from_clean_folder=run_from_clean_folder,
                retry_policy=retry_policy,
                retry_pipeline_steps=retry_pipeline_steps,
                extract_workers=extract_workers,
                load_workers=load_workers,
                normalize_workers=normalize_workers,
                normalize_file_max_bytes=normalize_file_max_bytes,
                normalize_file_max_items=normalize_file_max_items,
                **task_runner_args,
            )

            task_name = make_task_name(pipeline, source)
            run_task(
                pipeline,
                source,
                task_name,
                **run_kwargs,
            )

        return simple_pipeline_flow


#
# DECOMPOSITION HELPERS
#
def _task_name_from_source(source: dlt.sources.DltSource) -> str:
    """
    Use the first 4 resource names to create a task name.
    If there are more than 4, add a suffix with the number of additional resources.
    """
    resource_names = list(source.selected_resources.keys())
    task_name = source.name + "_" + "-".join(resource_names[:4])

    if len(resource_names) > 4:
        task_name += f"-{len(resource_names) - 4}-more"

    return task_name


def make_task_name(pipeline: Pipeline, data: Any) -> str:
    """
    Generate a task name based on the selected resources in the source.
    If the data is not a source, the pipeline name is used
    Args:
        pipeline (Pipeline): The pipeline to run.
        data (Any): The data to run the pipeline with.

    Returns:
        str: The name of the task.
    """
    task_name = pipeline.pipeline_name

    if isinstance(data, DltSource):
        task_name = _task_name_from_source(data)

    return task_name


def _make_task_pipeline(pipeline: dlt.Pipeline, new_name: str) -> dlt.Pipeline:
    """
    Creates a new pipeline with the given name, dropping the existing pipeline, syncing from
    the destination to get latest schema and state.
    """
    pipeline.activate()
    task_pipeline = pipeline.drop(pipeline_name=new_name)
    return task_pipeline


#
# PARALLELISM HELPERS
#
def build_pipeline_env_vars(
    pipeline_name: str,
    extract_workers: Optional[int] = None,
    load_workers: Optional[int] = None,
    normalize_workers: Optional[int] = None,
    normalize_file_max_bytes: Optional[int] = None,
    normalize_file_max_items: Optional[int] = None,
) -> Dict[str, str]:
    """
    Build environment variables dictionary for pipeline-specific parallelism settings.

    Args:
        pipeline_name: Name of the pipeline (used as prefix for env vars)
        extract_workers: Number of extract workers for this pipeline
        load_workers: Number of load workers for this pipeline
        normalize_workers: Number of normalize workers for this pipeline
        normalize_file_max_bytes: Max bytes per normalize file for this pipeline
        normalize_file_max_items: Max items per normalize file for this pipeline

    Returns:
        Dict[str, str]: Dictionary of environment variable names to values
    """
    prefix = f"{pipeline_name.upper()}__"
    env_vars = {}

    if extract_workers is not None:
        env_vars[f"{prefix}EXTRACT__WORKERS"] = str(extract_workers)

    if load_workers is not None:
        env_vars[f"{prefix}LOAD__WORKERS"] = str(load_workers)

    if normalize_workers is not None:
        env_vars[f"{prefix}NORMALIZE__WORKERS"] = str(normalize_workers)

    if normalize_file_max_bytes is not None:
        env_vars[f"{prefix}NORMALIZE__FILE_MAX_BYTES"] = str(normalize_file_max_bytes)

    if normalize_file_max_items is not None:
        env_vars[f"{prefix}NORMALIZE__FILE_MAX_ITEMS"] = str(normalize_file_max_items)

    return env_vars
