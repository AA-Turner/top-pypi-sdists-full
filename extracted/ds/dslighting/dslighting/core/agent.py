"""
DSLighting Agent - Simplified API for data science automation.

This module provides the main Agent class that wraps the complexity of
DSAT framework while providing full control when needed.
"""

import asyncio
import logging
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from dsat.config import DSATConfig
from dsat.models.task import TaskDefinition, TaskType
from dsat.runner import DSATRunner

from dslighting.core.config_builder import ConfigBuilder
from dslighting.core.data_loader import DataLoader, TaskContext

logger = logging.getLogger(__name__)


@dataclass
class AgentResult:
    """
    Result of running an Agent on a data science task.

    Attributes:
        success: Whether the task completed successfully
        output: Task output (predictions, answer, file path, etc.)
        score: Evaluation score (if available)
        cost: Total LLM cost in USD
        duration: Execution time in seconds
        artifacts_path: Path to generated artifacts
        workspace_path: Path to workspace directory
        error: Error message if failed
        metadata: Additional metadata
    """
    success: bool
    output: Any
    cost: float = 0.0
    duration: float = 0.0
    score: Optional[float] = None
    artifacts_path: Optional[Path] = None
    workspace_path: Optional[Path] = None
    error: Optional[str] = None
    summary: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        if self.success:
            return (
                f"AgentResult(success={self.success}, "
                f"output={self.output}, "
                f"score={self.score}, "
                f"cost=${self.cost:.4f}, "
                f"duration={self.duration:.1f}s)"
            )
        else:
            return (
                f"AgentResult(success={self.success}, "
                f"error={self.error}, "
                f"cost=${self.cost:.4f})"
            )


class Agent:
    """
    Simplified interface to DSLighting's data science automation capabilities.

    The Agent class provides a scikit-learn-like API that handles the complexity
    of workflow selection, configuration, and execution while allowing advanced
    users to access underlying components when needed.

    Examples:
        Simple usage:
            >>> import dslighting
            >>> agent = dslighting.Agent()
            >>> result = agent.run("data/my-competition")

        Advanced usage:
            >>> agent = dslighting.Agent(
            ...     workflow="autokaggle",
            ...     model="gpt-4o",
            ...     temperature=0.5,
            ...     max_iterations=10
            ... )
            >>> result = agent.run(data_path)

        Access underlying components:
            >>> config = agent.get_config()
            >>> runner = agent.get_runner()
    """

    def __init__(
        self,
        workflow: str = None,
        model: str = None,
        api_key: str = None,
        api_base: str = None,
        provider: str = None,
        temperature: float = None,
        max_iterations: int = None,
        num_drafts: int = None,
        workspace_dir: str = None,
        run_name: str = None,
        keep_workspace: bool = False,
        keep_workspace_on_failure: bool = True,
        verbose: bool = True,
        include_package_context: bool = True,
        **kwargs
    ):
        """
        Initialize DSLighting Agent.

        Args:
            workflow: Workflow name (aide, autokaggle, automind, etc.)
                      Defaults to "aide" or auto-detected from data
            model: LLM model name (e.g., "gpt-4o-mini", "deepseek-chat")
                   Defaults to LLM_MODEL env var or "gpt-4o-mini"
            api_key: API key for LLM service
                     Defaults to API_KEY env var
            api_base: API base URL
                      Defaults to API_BASE env var or OpenAI
            provider: LLM provider for LiteLLM (e.g., "siliconflow")
            temperature: LLM temperature (0.0-1.0)
            max_iterations: Maximum agent search iterations
            num_drafts: Number of drafts to generate
            workspace_dir: Custom workspace directory
            run_name: Name for this run
            keep_workspace: Keep workspace after completion (default: False)
            keep_workspace_on_failure: Keep workspace on failure (default: True)
            verbose: Enable verbose logging
            include_package_context: Include available package info in prompts (default: True)
            **kwargs: Additional parameters passed to DSATConfig
        """
        self.verbose = verbose
        self.logger = logger
        self.include_package_context = include_package_context

        # Build configuration
        self.config_builder = ConfigBuilder()
        self.config = self.config_builder.build_config(
            workflow=workflow,
            model=model,
            api_key=api_key,
            api_base=api_base,
            provider=provider,
            temperature=temperature,
            max_iterations=max_iterations,
            num_drafts=num_drafts,
            workspace_dir=workspace_dir,
            run_name=run_name,
            keep_workspace=keep_workspace,
            keep_workspace_on_failure=keep_workspace_on_failure,
            **kwargs
        )

        # Create runner (will be created on first use)
        self._runner: Optional[DSATRunner] = None

        # Track results
        self._results: List[AgentResult] = []

        # Initialize package detector for environment context
        self._package_detector = None
        self._package_context: Optional[str] = None

        if self.include_package_context:
            try:
                from dslighting.utils.package_detector import PackageDetector
                self._package_detector = PackageDetector()
                self.logger.info("Package context enabled: Agent will be aware of available packages")
            except Exception as e:
                self.logger.warning(f"Failed to initialize package detector: {e}")
                self.include_package_context = False

        self.logger.debug(f"Agent initialized with workflow: '{self.config.workflow.name}'")

    def run(
        self,
        data: Union[str, Path, dict, pd.DataFrame, TaskContext] = None,
        task_id: str = None,
        data_dir: str = None,
        output_path: str = None,
        description: str = None,
        task_type: Optional[str] = None,
        registry_dir: str = None,
        keep_workspace: bool = None,
        **kwargs
    ) -> AgentResult:
        """
        Run the agent on a data science task.

        This is the main entry point for executing data science tasks.
        It handles data loading, task creation, workflow execution, and
        result collection.

        Args:
            data: Optional data source (path, DataFrame, dict, or TaskContext).
                  If not provided, use task_id + data_dir pattern.
            task_id: Task/Competition identifier (e.g., "bike-sharing-demand").
                     Required when using MLE benchmark format.
            data_dir: Direct path to task data directory (must contain prepared/ folder).
                     Example: "/path/to/data/competitions/my-task"
                     If not provided, will use global config from setup().
            output_path: Custom output path for results
            description: Optional task description (overrides detected)
            task_type: Advanced override for open-ended tasks.
                      Only two top-level modes exist:
                      - "kaggle" (default when task_type is None)
                      - "open_ended" (explicit)
                      Subtypes of open_ended can be specified as:
                      "analysis", "processing", "modeling".
            registry_dir: Direct path to task registry directory (must contain config.yaml).
                          Example: "/path/to/registry/my-task"
                          If not provided, will use global config from setup().
            keep_workspace: Keep workspace after completion (overrides __init__ setting).
                          If None, uses the value from Agent initialization.
            **kwargs: Additional task parameters

        Returns:
            AgentResult with output, metrics, and metadata

        Examples:
            >>> # Method 1: Using global setup (recommended for multiple tasks)
            >>> import dslighting
            >>> dslighting.setup(
            ...     data_parent_dir="/path/to/data/competitions",
            ...     registry_parent_dir="/path/to/registry"
            ... )
            >>>
            >>> agent = dslighting.Agent()
            >>> result = agent.run(task_id="bike-sharing-demand")

            >>> # Method 2: Using direct paths (explicit and clear)
            >>> result = agent.run(
            ...     task_id="bike-sharing-demand",
            ...     data_dir="/path/to/data/competitions/bike-sharing-demand",
            ...     registry_dir="/path/to/registry/bike-sharing-demand"
            ... )

            >>> # Method 3: Using built-in dataset
            >>> result = agent.run(task_id="bike-sharing-demand")

            >>> # Method 4: Using DataFrame
            >>> result = agent.run(df, description="Predict price")
        """
        # Start timing
        start_time = time.time()

        # Open-ended mode is triggered only by explicit task_type.
        # Without task_type, agent.run defaults to Kaggle/ML logic.
        normalized_task_type = self._normalize_advanced_task_type(task_type)
        open_ended_request = normalized_task_type in {
            "open_ended",
            "analysis",
            "processing",
            "modeling",
        }

        # Temp directory for open-ended data (if needed).
        open_ended_temp_dir = None
        open_ended_data_dir = None
        open_ended_mode = False

        try:
            # ========== Path handling: Two clear modes ==========

            # Mode 1: Built-in dataset (only task_id provided, no data_dir)
            if task_id and data is None and data_dir is None:
                try:
                    import dslighting.datasets
                    # Convert "bike-sharing-demand" to "load_bike_sharing_demand"
                    load_func_name = f'load_{task_id.replace("-", "_")}'
                    load_func = getattr(dslighting.datasets, load_func_name, None)

                    if load_func:
                        self.logger.info(f"Using built-in dataset: {task_id}")
                        loaded_info = load_func()
                        # Load the built-in data
                        loader = DataLoader()
                        loaded_data = loader.load(loaded_info['data_dir'])
                        # Skip to execution (loaded_data is ready)
                        data = loaded_data
                        task_id = None  # Already extracted from loaded_data
                        data_dir = None
                except (AttributeError, FileNotFoundError):
                    # Not a built-in dataset, check global config
                    pass

            # Mode 2: Use global config if no data_dir provided
            if task_id and data is None and data_dir is None:
                from dslighting.core.global_config import get_global_config
                config = get_global_config()
                data_dir_from_config, registry_dir_from_config = config.get_task_paths(task_id)

                if data_dir_from_config is not None:
                    self.logger.info(f"Using global config for task: {task_id}")
                    self.logger.info(f"  Data directory: {data_dir_from_config}")
                    if registry_dir_from_config is not None:
                        self.logger.info(f"  Registry directory: {registry_dir_from_config}")
                        # Use registry from config if not explicitly provided
                        if registry_dir is None:
                            registry_dir = str(registry_dir_from_config)

                    # Load data from configured path
                    loader = DataLoader()
                    loaded_data = loader.load(data_dir_from_config, registry_dir=registry_dir)
                    data = loaded_data
                    task_id = None  # Already extracted from loaded_data
                    data_dir = None
                else:
                    raise ValueError(
                        f"No data directory provided and no global config found.\n"
                        f"Either:\n"
                        f"  1. Provide data_dir explicitly: agent.run(task_id='{task_id}', data_dir='/path/to/{task_id}')\n"
                        f"  2. Set up global config: dslighting.setup(data_parent_dir='/path/to/data/competitions')"
                    )

            # Mode 3: Direct path provided (data_dir is explicit)
            if task_id and data is None and data_dir is not None:
                data_dir_path = Path(data_dir).resolve()

                if not data_dir_path.exists():
                    raise FileNotFoundError(
                        f"Data directory not found: {data_dir_path}\n"
                        f"Please ensure the path exists and contains prepared/ folder."
                    )

                # Verify it's a task directory (has prepared/public)
                if not (data_dir_path / "prepared" / "public").exists():
                    raise ValueError(
                        f"Invalid data directory: {data_dir_path}\n"
                        f"Expected structure: {data_dir_path}/prepared/public/train.csv\n"
                        f"Please provide the direct task directory, not the parent directory."
                    )

                self.logger.info(f"Using direct task path: {data_dir_path}")
                if registry_dir:
                    self.logger.info(f"  Registry directory: {registry_dir}")

                # Load data with explicit paths
                loader = DataLoader()
                loaded_data = loader.load(data_dir_path, registry_dir=registry_dir)
                data = loaded_data
                task_id = None  # Already extracted from loaded_data
                data_dir = None

            # ========== Normal handling for remaining cases ==========
            if data is None:
                raise ValueError("Either 'data' or 'task_id' must be provided")

            # ========== Load data if needed ==========
            if not isinstance(data, TaskContext):
                self.logger.debug("Loading data...")
                loader = DataLoader(auto_detect=False)
                loaded_data = loader.load(data, auto_detect=False)
                self.logger.debug(f"Data loaded, task_id={loaded_data.task_id}")
            else:
                self.logger.debug("Data is already TaskContext")
                loaded_data = data
                self.logger.debug(f"TaskContext has task_id={loaded_data.task_id}")

            # Extract task_id from loaded_data if available
            if loaded_data.task_id:
                # Use task_id from loaded_data for benchmark initialization
                extracted_task_id = loaded_data.task_id
                self.logger.info(f"Detected task_id from data: {extracted_task_id}")
                self.logger.debug(f"Extracted task_id={extracted_task_id}, overriding task_id parameter")

                # Override task_id parameter for benchmark initialization
                task_id = extracted_task_id
                self.logger.debug(f"task_id is now set to: {task_id}")
            if open_ended_request:
                open_ended_mode = True
                if task_id is None:
                    self.logger.info("Open-ended mode detected (no task_id provided).")
                    task_id = f"open_{uuid.uuid4().hex[:8]}"
            elif task_id is None:
                raise ValueError(
                    "Either 'task_id' or 'data' must be provided. "
                    "Example: agent.run(task_id='bike-sharing-demand', data_dir='data/competitions')"
                )

            # Get task information
            task_detection = loaded_data.task_detection

            # Determine workflow
            workflow = self._determine_workflow(task_detection)
            self.logger.info(f"Using workflow: {workflow}")

            # Prepare open-ended data directory (if needed).
            if open_ended_mode:
                open_ended_data_dir = self._prepare_open_ended_data_dir(
                    loaded_data, open_ended_request
                )
                if open_ended_data_dir and open_ended_data_dir.name.startswith("dslighting_open_ended_"):
                    open_ended_temp_dir = open_ended_data_dir

            # Create task definition
            task = self._create_task_definition(
                loaded_data=loaded_data,
                task_id=task_id,
                description=description,
                output_path=output_path,
                open_ended_mode=open_ended_mode,
                advanced_task_type=normalized_task_type,
                open_ended_temp_dir=open_ended_data_dir,
                **kwargs
            )

            # Initialize benchmark for MLE tasks (for grading)
            self.logger.debug(f"Checking benchmark initialization: task_id={task_id}, task_type={loaded_data.get_task_type()}")
            self.logger.info(f"Checking benchmark initialization: task_id={task_id}, task_type={loaded_data.get_task_type()}")

            # The new native benchmark system will handle grading after the task execution.
            # So, we no longer set a benchmark object on the runner.
            if task_id and loaded_data.get_task_type() == "kaggle":
                self.logger.info("Kaggle task detected. Native grading will occur after agent run.")

            # Handle keep_workspace parameter override
            if keep_workspace is not None:
                self.logger.info(f"Overriding keep_workspace setting: {keep_workspace}")
                self.config.run.keep_all_workspaces = keep_workspace

            # Execute task (async wrapper)
            # Use a more robust async execution to handle SSL cleanup gracefully
            import asyncio
            import warnings
            import logging

            # Suppress asyncio SSL cleanup warnings (they're harmless)
            class AsyncioSSLFilter(logging.Filter):
                def filter(self, record):
                    # Filter out SSL transport errors during cleanup
                    if "SSL transport" in record.getMessage() or "Event loop is closed" in record.getMessage():
                        return False
                    return True

            # Temporarily add filter to suppress SSL cleanup errors
            asyncio_logger = logging.getLogger("asyncio")
            ssl_filter = AsyncioSSLFilter()
            asyncio_logger.addFilter(ssl_filter)

            async def _run_with_cleanup():
                try:
                    return await self._execute_task(task, loaded_data)
                finally:
                    try:
                        import litellm
                        close_fn = getattr(litellm, "aclose", None)
                        if callable(close_fn):
                            await close_fn()
                        try:
                            from litellm.llms.custom_httpx.async_client_cleanup import (
                                close_litellm_async_clients,
                            )
                            await close_litellm_async_clients()
                        except Exception as close_all_error:
                            self.logger.debug(f"LiteLLM async client cleanup failed: {close_all_error}")
                    except Exception as close_error:
                        self.logger.debug(f"LiteLLM cleanup failed: {close_error}")
                    # Drain pending tasks so SSL transports close before loop shutdown.
                    try:
                        await asyncio.sleep(0)
                        pending = [
                            t for t in asyncio.all_tasks()
                            if t is not asyncio.current_task()
                        ]
                        if pending:
                            for pending_task in pending:
                                pending_task.cancel()
                            await asyncio.gather(*pending, return_exceptions=True)
                            await asyncio.sleep(0)
                    except Exception as drain_error:
                        self.logger.debug(f"Asyncio drain failed: {drain_error}")

            try:
                result = asyncio.run(_run_with_cleanup())
            finally:
                # Remove filter after execution
                asyncio_logger.removeFilter(ssl_filter)

            # --- GRADING STEP (before any cleanup) ---
            if task_id and loaded_data.get_task_type() == "kaggle" and result.success:
                output = result.output

                # Check if runner already graded the submission
                already_graded = False
                if isinstance(output, dict) and "score" in output:
                    score = output["score"]
                    # Convert NaN to None for invalid scores
                    import math
                    if isinstance(score, float) and math.isnan(score):
                        score = None
                    result.score = score
                    already_graded = True
                    self.logger.info(f"✓ Score available from runner: {score}")
                elif isinstance(output, (str, Path)):
                    # Runner returned a file path but didn't grade it
                    # Grade it now BEFORE workspace cleanup
                    self.logger.info(f"Grading submission from runner: {output}")
                    try:
                        from dslighting.benchmark.grading.evaluator import Evaluator

                        submission_path = Path(output)
                        if not submission_path.exists():
                            self.logger.warning(f"Submission file not found: {submission_path}")
                            result.score = None
                        else:
                            # Resolve registry parent directory
                            if loaded_data.registry_dir:
                                registry_parent_dir = Path(loaded_data.registry_dir)
                                if registry_parent_dir.name == task_id:
                                    registry_parent_dir = registry_parent_dir.parent
                            else:
                                import dslighting
                                registry_parent_dir = Path(dslighting.__file__).parent / "registry"

                            # Resolve data parent directory
                            if loaded_data.data_dir:
                                data_dir = loaded_data.data_dir
                                if data_dir.name == task_id:
                                    data_parent_dir = data_dir.parent
                                else:
                                    data_parent_dir = data_dir
                            else:
                                data_parent_dir = Path("data/competitions")

                            evaluator = Evaluator.from_registry(
                                task_id=task_id,
                                registry_parent_dir=str(registry_parent_dir),
                                data_parent_dir=str(data_parent_dir),
                            )

                            score = evaluator.evaluate_sync(submission_path=submission_path)
                            result.score = score
                            self.logger.info(f"✓ Grading complete. Score: {score}")

                    except Exception as e:
                        self.logger.error(f"Grading failed: {e}", exc_info=True)
                        result.score = None

            # Calculate duration
            duration = time.time() - start_time
            result.duration = duration

            # Build open-ended summary (preview + artifacts) if applicable.
            if open_ended_mode:
                summary = self._build_open_ended_summary(result)
                result.metadata["summary"] = summary
                result.summary = summary
                self._log_open_ended_summary(summary)

            # Store result
            self._results.append(result)

            if self.verbose:
                self._log_result(result)

            return result

        except Exception as e:
            self.logger.error(f"Task execution failed: {e}", exc_info=True)

            duration = time.time() - start_time

            return AgentResult(
                success=False,
                output=None,
                duration=duration,
                error=str(e),
                metadata={"exception_type": type(e).__name__}
            )
        finally:
            if open_ended_temp_dir and open_ended_temp_dir.exists():
                try:
                    import shutil
                    shutil.rmtree(open_ended_temp_dir)
                except Exception:
                    pass

    def run_batch(
        self,
        data_list: List[Union[str, Path, dict, pd.DataFrame]],
        **kwargs
    ) -> List[AgentResult]:
        """
        Run the agent on multiple data sources sequentially.

        Args:
            data_list: List of data sources
            **kwargs: Additional parameters passed to run()

        Returns:
            List of AgentResult objects

        Examples:
            >>> results = agent.run_batch([
            ...     "data/titanic",
            ...     "data/house-prices",
            ...     "data/fraud-detection"
            ... ])
            >>> for r in results:
            ...     print(f"{r.task_id}: {r.score}")
        """
        results = []

        for i, data in enumerate(data_list):
            self.logger.info(f"Running batch task {i+1}/{len(data_list)}")

            result = self.run(data, **kwargs)
            results.append(result)

        return results

    def get_config(self) -> DSATConfig:
        """
        Get the underlying DSAT configuration.

        This allows advanced users to modify configuration directly.

        Returns:
            DSATConfig object

        Examples:
            >>> config = agent.get_config()
            >>> config.llm.temperature = 0.5
        """
        return self.config

    def get_runner(self) -> DSATRunner:
        """
        Get the underlying DSATRunner instance.

        This allows advanced users to interact with the runner directly.

        Returns:
            DSATRunner instance

        Examples:
            >>> runner = agent.get_runner()
            >>> eval_fn = runner.get_eval_function()
        """
        if self._runner is None:
            self._runner = DSATRunner(self.config)

        return self._runner

    def get_results(self) -> List[AgentResult]:
        """Get all results from this agent session."""
        return self._results.copy()

    def _determine_workflow(self, task_detection) -> str:
        """Determine which workflow to use."""
        # If user specified workflow, use it
        if self.config.workflow and self.config.workflow.name:
            return self.config.workflow.name

        # Otherwise, use recommended workflow from detection
        if task_detection and task_detection.recommended_workflow:
            return task_detection.recommended_workflow

        # Fallback to default
        return "aide"

    def _create_task_definition(
        self,
        loaded_data: TaskContext,
        task_id: str = None,
        description: str = None,
        output_path: str = None,
        open_ended_mode: bool = False,
        advanced_task_type: Optional[str] = None,
        open_ended_temp_dir: Optional[Path] = None,
        **kwargs
    ) -> TaskDefinition:
        """Create TaskDefinition from TaskContext."""
        # Generate task ID if not provided
        if task_id is None:
            safe_name = str(uuid.uuid4())[:8]
            task_id = f"task_{safe_name}"

        # Get task type
        task_type = loaded_data.get_task_type()
        task_mode = "standard_ml"
        if open_ended_mode:
            task_type = "open_ended"
            task_mode = "open_ended"

        # Get description
        if description is None:
            description = loaded_data.get_description()
        if open_ended_mode and advanced_task_type and advanced_task_type != "open_ended":
            description = f"User intent: {advanced_task_type}\n\n{description}"

        # Add package context to description if enabled
        if self.include_package_context and self._package_detector:
            try:
                package_context = self._package_detector.format_as_context()
                # Prepend package context to description
                description = f"{package_context}\n\nTask Description:\n{description}"
                self.logger.info("Package context added to task description")
            except Exception as e:
                self.logger.warning(f"Failed to add package context: {e}")

        # Get I/O instructions
        io_instructions = loaded_data.get_io_instructions()

        # Build payload
        payload = kwargs.copy()
        payload["description"] = description
        payload["io_instructions"] = io_instructions
        if advanced_task_type:
            payload["advanced_task_type"] = advanced_task_type

        # Add data directory based on task type
        if loaded_data.data_dir:
            data_dir = loaded_data.data_dir

            if task_type == "kaggle":
                # MLE/Kaggle format: needs public_data_dir and output_submission_path
                # Follow MLEBenchmark pattern: {data_dir}/prepared/public
                prepared_dir = data_dir / "prepared"
                public_dir = prepared_dir / "public"

                # Check if prepared/public exists (MLE format)
                if public_dir.exists():
                    payload["public_data_dir"] = str(public_dir.resolve())
                    self.logger.info(f"Using MLE prepared data: {public_dir.resolve()}")
                else:
                    # Fallback: use data_dir directly
                    payload["public_data_dir"] = str(data_dir.resolve())
                    self.logger.warning(
                        f"Prepared data not found at {public_dir}, using data_dir instead"
                    )

                # Set output path - use simple filename, will be saved in workspace/sandbox
                if output_path is None:
                    # Extract competition_id from data_dir path if possible
                    competition_id = data_dir.name
                    unique_id = str(uuid.uuid4())[:8]
                    output_filename = f"submission_{competition_id}_{unique_id}.csv"

                    # Use just the filename - DSAT will save it in workspace/sandbox
                    output_path = Path(output_filename)

                payload["output_submission_path"] = str(output_path)
                self.logger.info(f"Output submission file: {output_path}")
            else:
                # Other task types: use data_dir
                payload["data_dir"] = str(data_dir)
                if open_ended_mode:
                    payload["raw_data_dir"] = str(data_dir)

        # Add output path if specified (for non-kaggle tasks)
        if output_path and task_type != "kaggle":
            payload["output_submission_path"] = str(output_path)

        # Open-ended payload adjustments (relaxed I/O policy + optional temp data dir).
        if open_ended_mode:
            payload["io_policy"] = "relaxed"
            payload["output_preferences"] = (
                "You may save outputs in 'artifacts/' or 'outputs/' (preferred), "
                "and/or write a report to 'report.md'. "
                "Provide a brief summary and any key figures."
            )
            if open_ended_temp_dir:
                payload["raw_data_dir"] = str(open_ended_temp_dir)

        # Create TaskDefinition
        task = TaskDefinition(
            task_id=task_id,
            task_type=task_type,  # Pass string directly, Pydantic will validate
            mode=task_mode,
            payload=payload
        )

        return task

    def _prepare_open_ended_data_dir(
        self,
        loaded_data: TaskContext,
        open_ended_request: bool
    ) -> Optional[Path]:
        if not open_ended_request:
            return None

        # Use existing data_dir if present.
        if loaded_data.data_dir:
            return loaded_data.data_dir

        # If source is a DataFrame, persist it to a temp directory for sandbox usage.
        if isinstance(loaded_data.source, pd.DataFrame):
            import tempfile
            temp_dir = Path(tempfile.mkdtemp(prefix="dslighting_open_ended_"))
            df_path = temp_dir / "data.csv"
            loaded_data.source.to_csv(df_path, index=False)
            return temp_dir

        # If source is a file path, use its parent directory.
        if isinstance(loaded_data.source, (str, Path)):
            src_path = Path(loaded_data.source)
            if src_path.exists():
                return src_path.parent if src_path.is_file() else src_path

        return None

    def _normalize_advanced_task_type(self, task_type: Optional[str]) -> Optional[str]:
        if task_type is None:
            return None
        value = task_type.strip().lower()
        mapping = {
            "processing": "processing",
            "data_processing": "processing",
            "analysis": "analysis",
            "data_analysis": "analysis",
            "visualization": "analysis",
            "modeling": "modeling",
            "model": "modeling",
            "prediction": "modeling",
            "open_ended": "open_ended",
            "open-ended": "open_ended",
        }
        return mapping.get(value, value)

    def _build_open_ended_summary(self, result: AgentResult) -> Dict[str, Any]:
        summary: Dict[str, Any] = {
            "preview": None,
            "artifacts": [],
            "artifact_dir": None,
            "images": [],
        }

        output_path = result.output
        if isinstance(output_path, str):
            output_path = Path(output_path)

        if not isinstance(output_path, Path) or not output_path.exists():
            return summary

        artifact_dir = output_path if output_path.is_dir() else output_path.parent
        summary["artifact_dir"] = str(artifact_dir)

        artifacts = []
        images = []
        try:
            for path in sorted(artifact_dir.rglob("*")):
                if path.is_file():
                    ext = path.suffix.lower().lstrip(".")
                    artifacts.append({"path": str(path), "ext": ext})
                    if ext in {"png", "jpg", "jpeg", "gif", "svg"}:
                        images.append(str(path))
        except Exception:
            pass

        summary["artifacts"] = artifacts
        summary["images"] = images

        preview = self._extract_report_preview(artifact_dir)
        summary["preview"] = preview
        return summary

    def _extract_report_preview(self, artifact_dir: Path) -> Optional[str]:
        candidate_names = [
            "report.md",
            "summary.md",
            "analysis.md",
            "report.txt",
            "summary.txt",
            "README.md",
        ]

        candidates = [artifact_dir / name for name in candidate_names]
        candidates += list(artifact_dir.glob("*.md")) + list(artifact_dir.glob("*.txt"))

        for path in candidates:
            if path.exists() and path.is_file():
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore").strip()
                    if not text:
                        continue
                    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
                    preview = "\n\n".join(paragraphs[:2])
                    return preview[:1200]
                except Exception:
                    continue
        return None

    def _log_open_ended_summary(self, summary: Dict[str, Any]) -> None:
        if not summary:
            return
        preview = summary.get("preview")
        artifacts = summary.get("artifacts", [])
        if preview:
            self.logger.info("Open-ended summary preview:")
            for line in preview.splitlines()[:15]:
                self.logger.info(f"  {line}")
        if artifacts:
            self.logger.info("Open-ended artifacts:")
            for artifact in artifacts[:10]:
                self.logger.info(f"  - {artifact['path']}")

    def _get_workspace_dir(self) -> Path:
        """Get the workspace directory for this agent run."""
        # Try to get from config
        workspace_dir = None

        if hasattr(self, 'config') and hasattr(self.config, 'run'):
            run_config = self.config.run
            if hasattr(run_config, 'parameters') and run_config.parameters:
                workspace_dir = run_config.parameters.get('workspace_dir')

        # Fallback to default workspace directory
        if workspace_dir is None:
            from dslighting.utils.defaults import DEFAULT_WORKSPACE_DIR
            workspace_dir = DEFAULT_WORKSPACE_DIR

        # Ensure workspace exists
        workspace_path = Path(workspace_dir)
        workspace_path.mkdir(parents=True, exist_ok=True)

        return workspace_path

    def _get_default_benchmark_dir(self) -> Path:
        """
        Get the default benchmark registry directory.

        This is where task registration files (grade.py, description.md, etc.) are stored.
        Priority:
        1. Built-in registry in dslighting package (dslighting/registry/)
        2. Local benchmarks/mlebench/competitions/
        3. Config-provided benchmark_dir

        Returns:
            Path to benchmark registry directory
        """
        # Try to get from config
        benchmark_dir = None

        if hasattr(self, 'config') and hasattr(self.config, 'run'):
            run_config = self.config.run
            if hasattr(run_config, 'parameters') and run_config.parameters:
                benchmark_dir = run_config.parameters.get('benchmark_dir')

        # Fallback 1: Try built-in registry in dslighting package
        if benchmark_dir is None:
            try:
                import dslighting
                dslighting_path = Path(dslighting.__file__).parent
                built_in_registry = dslighting_path / "registry"

                if built_in_registry.exists():
                    self.logger.info(f"Using built-in registry: {built_in_registry}")
                    return built_in_registry.resolve()
            except Exception as e:
                self.logger.debug(f"Could not access built-in registry: {e}")

        # Fallback 2: Use relative path from current working directory
        if benchmark_dir is None:
            # Default: benchmarks/mlebench/competitions/
            benchmark_dir = "benchmarks/mlebench/competitions"

        benchmark_path = Path(benchmark_dir).resolve()

        self.logger.debug(f"Benchmark registry directory: {benchmark_path}")

        return benchmark_path

    async def _execute_task(
        self,
        task: TaskDefinition,
        loaded_data: TaskContext
    ) -> AgentResult:
        """Execute a single task using DSATRunner."""
        runner = self.get_runner()

        # Link data directory to workspace if available
        if loaded_data.data_dir and hasattr(runner, 'benchmark') and runner.benchmark:
            workspace_service = None
            # Try to get workspace service from workflow
            if hasattr(runner, 'factory'):
                try:
                    workflow = runner.factory.create_workflow(self.config, benchmark=runner.benchmark)
                    workspace_service = workflow.services.get("workspace")
                    if workspace_service:
                        workspace_service.link_data_to_workspace(loaded_data.data_dir)
                except Exception:
                    pass

        # Get evaluation function
        eval_fn = runner.get_eval_function()

        # Execute task
        output, cost, usage_summary = await eval_fn(task)

        # Check for errors
        if isinstance(output, str) and output.startswith("[ERROR]"):
            return AgentResult(
                success=False,
                output=output,
                cost=cost,
                error=output
            )

        # Extract score if available
        score = None
        if isinstance(output, (int, float)):
            score = float(output)
        elif isinstance(output, dict) and "score" in output:
            score = output["score"]

        # Get workspace path
        workspace_path = None
        if hasattr(runner, 'run_records') and runner.run_records:
            last_record = runner.run_records[-1]
            workspace_path = last_record.get("workspace_dir")

        return AgentResult(
            success=True,
            output=output,
            cost=cost,
            score=score,
            workspace_path=Path(workspace_path) if workspace_path else None,
            metadata={"usage": usage_summary}
        )

    def _log_result(self, result: AgentResult):
        """Log result summary."""
        if result.success:
            self.logger.info(
                f"✓ Task completed successfully | "
                f"Score: {result.score or 'N/A'} | "
                f"Cost: ${result.cost:.4f} | "
                f"Duration: {result.duration:.1f}s"
            )
        else:
            self.logger.error(
                f"✗ Task failed | "
                f"Error: {result.error} | "
                f"Cost: ${result.cost:.4f}"
            )

    def __repr__(self) -> str:
        return (
            f"Agent(workflow='{self.config.workflow.name}', "
            f"model='{self.config.llm.model}', "
            f"results={len(self._results)})"
        )
