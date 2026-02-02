"""
Base Workflow Factory - Base class for all Workflow Factory

Provides standard MLE task loading functionality, users don't need to reimplement
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseWorkflowFactory(ABC):
    """
    Base class for Workflow Factory

    Provides:
    1. Standard LLM/Sandbox/Workspace service creation
    2. Standard MLE task loading (from registry)
    3. run_with_task_id() convenience method

    Users only need to:
    1. Inherit from BaseWorkflowFactory
    2. Implement create_agent() method
    3. Define their own workflow class
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        api_key: str = None,
        api_base: str = None,
        provider: str = None,
        temperature: float = None,
        timeout: int = 300,
        keep_workspace: bool = False,
        **agent_init_kwargs
    ):
        """
        Initialize factory

        Args:
            model: LLM model name
            api_key: API key (optional, read from env var if not provided)
            api_base: API base URL (optional, read from env var if not provided)
            provider: LLM provider (optional)
            temperature: Temperature parameter (optional, read from env var if not provided)
            timeout: Sandbox timeout
            keep_workspace: Whether to keep workspace
            **agent_init_kwargs: Additional parameters, will be passed to create_agent()

        Note:
            Use DSLighting's ConfigBuilder to automatically read config from environment variables:
            - API_KEY, API_BASE, LLM_MODEL
            - LLM_MODEL_CONFIGS (multi-model config)

        Example:
            >>> factory = MyWorkflowFactory(
            ...     model="gpt-4o",
            ...     max_iterations=3,  # Passed to create_agent()
            ...     use_data_insights=True
            ... )
        """
        self.model = model
        self.timeout = timeout
        self.keep_workspace = keep_workspace
        self._agent_init_kwargs = agent_init_kwargs

        # Use DSLighting's ConfigBuilder to automatically read config from environment variables
        from dslighting.core.config_builder import ConfigBuilder
        config_builder = ConfigBuilder()
        config = config_builder.build_config(
            model=model,
            api_key=api_key,
            api_base=api_base,
            provider=provider,
            temperature=temperature,
        )

        # Extract LLM config from configuration
        llm_config = config.llm

        # Create services (infrastructure ready, users don't need to care)
        from dslighting.services import LLMService, SandboxService, WorkspaceService

        self.llm_service = LLMService(config=llm_config)
        self.workspace_service = WorkspaceService(
            run_name=f"{self._get_workflow_name()}_{model.replace('/', '_')}"
        )
        self.sandbox_service = SandboxService(
            workspace=self.workspace_service,
            timeout=timeout
        )

        logger.debug(f"{self.__class__.__name__} initialized")
        logger.debug(f"  - Model: {model}")
        logger.debug(f"  - Timeout: {timeout}s")
        logger.debug(f"  - Keep workspace: {keep_workspace}")

    def _get_workflow_name(self) -> str:
        """
        Get the workflow name (used for logs and workspace naming).

        Subclasses can override this method to provide a custom name.
        """
        return self.__class__.__name__.replace("Factory", "").lower()

    @abstractmethod
    def create_agent(self, **kwargs) -> Any:
        """
        Create an Agent instance (subclasses must implement).

        Args:
            **kwargs: Agent ConfigParameter

        Returns:
            Agent instance
        """
        raise NotImplementedError("Subclasses must implement create_agent()")

    def cleanup(self):
        """Cleanup workspace"""
        if not self.keep_workspace:
            self.workspace_service.cleanup()
            logger.debug(f"✓ Workspace cleaned")

    def run(
        self,
        data=None,
        task_id: Optional[str] = None,
        data_dir: Optional[Path] = None,
        **kwargs
    ):
        """
        Run the workflow (unified entry point, recommended).

        This is a synchronous method; callers do not need to handle async/await.

        Supports multiple calling modes:

        1. Use a LoadedData object (simplest):
           >>> data = dslighting.load_data("/path/to/data")
           >>> result = factory.run(data)

        2. Use task_id:
           >>> result = factory.run(task_id="bike-sharing-demand")

        3. Use task_id + data_dir:
           >>> result = factory.run(
           ...     task_id="bike-sharing-demand",
           ...     data_dir="/path/to/data"
           ... )

        4. Use a dataset dict (returned by datasets.load_xxx()):
           >>> dataset = dslighting.datasets.load_bike_sharing_demand()
           >>> result = factory.run(dataset)

        Args:
            data: Optional. Can be:
                - LoadedData object (returned by dslighting.load_data()).
                - dataset dict (returned by dslighting.datasets.load_xxx()).
                - If provided, task_id and data_dir are extracted from it.
                - If not provided and data is also None, you must pass data_dir separately.
            task_id: Task ID (e.g. "bike-sharing-demand")
                Overrides task_id extracted from data.
            data_dir: Data directory path
            **kwargs: Parameters passed to create_agent().

        Returns:
            Execution result

        Example:
            >>> factory = MyWorkflowFactory(model="gpt-4o")

            # Mode 1: LoadedData
            >>> data = dslighting.load_data("/path/to/data")
            >>> result = factory.run(data)

            # Mode 2: task_id
            >>> result = factory.run(task_id="bike-sharing-demand")

            # Mode 3: dataset dict
            >>> dataset = dslighting.datasets.load_bike_sharing_demand()
            >>> result = factory.run(dataset)
        """
        import asyncio

        async def _run_with_cleanup():
            try:
                return await self._run_async(data=data, task_id=task_id, data_dir=data_dir, **kwargs)
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
                    except Exception:
                        pass
                except Exception:
                    pass
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
                except Exception:
                    pass

        return asyncio.run(_run_with_cleanup())

    async def _run_async(
        self,
        data=None,
        task_id: Optional[str] = None,
        data_dir: Optional[Path] = None,
        **kwargs
    ):
        """
        Run the workflow asynchronously.

        Supports multiple calling modes:

        1. Use a LoadedData object:
           >>> data = dslighting.load_data("/path/to/data")
           >>> await factory.run(data)

        2. Use task_id:
           >>> await factory.run(task_id="bike-sharing-demand")

        3. Use task_id + data_dir:
           >>> await factory.run(
           ...     task_id="bike-sharing-demand",
           ...     data_dir="/path/to/data"
           ... )

        4. Use a dataset dict:
           >>> dataset = dslighting.datasets.load_bike_sharing_demand()
           >>> await factory.run(dataset)

        Args:
            data: Optional. Can be:
                - LoadedData object (returned by dslighting.load_data()).
                - dataset dict (returned by dslighting.datasets.load_xxx()).
                - If provided, task_id and data_dir are extracted from it.
                - If not provided and data is also None, you must pass data_dir separately.
            task_id: Task ID (e.g. "bike-sharing-demand")
                Overrides task_id extracted from data.
            data_dir: Data directory path
            **kwargs: Parameters passed to create_agent().

        Example:
            >>> factory = MyWorkflowFactory(model="gpt-4o")

            # Mode 1: LoadedData
            >>> data = dslighting.load_data("/path/to/data")
            >>> await factory.run(data)

            # Mode 2: task_id
            >>> await factory.run(task_id="bike-sharing-demand")

            # Mode 3: dataset dict
            >>> dataset = dslighting.datasets.load_bike_sharing_demand()
            >>> await factory.run(dataset)
        """
        # Case 1: data parameter provided.
        if data is not None:
            # Extract task_id/data_dir from LoadedData or dataset dict.
            if hasattr(data, 'task_id') and hasattr(data, 'data_dir'):
                # LoadedData object
                logger.info("Detected LoadedData object")
                task_id = data.task_id
                data_dir = data.data_dir
            elif isinstance(data, dict) and 'data_dir' in data:
                # Dataset dict/dictionary
                logger.info("Detected dataset dict/dictionary")
                data_dir = Path(data['data_dir'])
                task_id = task_id or data.get('task_id')
            else:
                raise ValueError(
                    f"Unsupported data type: {type(data)}\n"
                    f"Expected: LoadedData object or dataset dict/dictionary"
                )

        # Case 2: task_id provided but data_dir not provided.
        elif task_id is not None and data_dir is None:
            # Resolve data_dir from registry.
            logger.info("Only task_id provided; resolving data_dir from registry")
            # Delegate to run_with_task_id so it can resolve data_dir internally.
            return await self.run_with_task_id(task_id=task_id, **kwargs)

        # Case 3: validate required inputs.
        if task_id is None:
            raise ValueError("task_id is required (or provide data object containing task_id)")
        if data_dir is None:
            raise ValueError("data_dir is required (or provide data object containing data_dir)")

        # Delegate to run_with_task_id with explicit task_id/data_dir.
        return await self.run_with_task_id(
            task_id=task_id,
            data_dir=Path(data_dir) if not isinstance(data_dir, Path) else data_dir,
            **kwargs
        )

    async def run_with_task_id(
        self,
        task_id: str,
        data_dir: Optional[Path] = None,
        task_loader: Optional[Any] = None,
        output_path: Optional[Path] = None,
        **agent_kwargs
    ) -> None:
        """
        Run the workflow by task_id (async).

        Resolves task config, prepares workspace/sandbox, runs the agent,
        and optionally performs grading.

        Args:
            task_id: Task ID (e.g. "bike-sharing-demand")
            data_dir: Optional data directory. If not provided, resolve from registry.
            task_loader: Optional task loader. If not provided, use MLETaskLoader.
            output_path: Optional submission output path.
            **agent_kwargs: Parameters passed to create_agent() (e.g. max_iterations).

        Example:
            >>> factory = MyWorkflowFactory(model="gpt-4o")
            >>> await factory.run_with_task_id("bike-sharing-demand", max_iterations=3)

            # Custom submission filename
            >>> await factory.run_with_task_id("bike-sharing-demand", output_path="my_submission.csv")
        """
        logger.info(f"=" * 80)
        logger.info(f"Running {self.__class__.__name__} with task_id")
        logger.info(f"=" * 80)
        logger.info(f"  Task ID: {task_id}")
        logger.info(f"  Agent Config: {agent_kwargs}")
        logger.info(f"=" * 80)

        # Use a unique workspace per run to avoid stale/broken symlinks.
        import uuid
        from dslighting.services import SandboxService, WorkspaceService
        run_name = f"{self._get_workflow_name()}_{task_id}_{uuid.uuid4().hex[:8]}"
        self.workspace_service = WorkspaceService(run_name=run_name)
        self.sandbox_service = SandboxService(
            workspace=self.workspace_service,
            timeout=self.timeout
        )

        # Use default task loader if none is provided.
        if task_loader is None:
            from dslighting.benchmark.loaders import MLETaskLoader
            task_loader = MLETaskLoader()

        # Use prepared public data directory.
        public_dir = data_dir / "prepared" / "public"

        if not public_dir.exists():
            logger.error(f"❌ Public data directory not found: {public_dir}")
            logger.error(f"Expected structure: {data_dir}/prepared/public/train.csv")
            raise FileNotFoundError(
                f"Public data directory not found: {public_dir}\n"
                f"Expected structure: {data_dir}/prepared/public/train.csv"
            )

        logger.info(f"Using public data directory (avoid leaking answers): {public_dir}")

        # Load task metadata from public data directory.
        description, io_instructions, _, default_output_path = task_loader.load_task(
            task_id=task_id,
            data_dir=public_dir  # English comment.
        )

        # Use provided output_path or default from task loader.
        output_path = output_path or default_output_path

        # ✅ VerifyLoadresult
        logger.info("Task loaded:")
        logger.info(f"  - Description length: {len(description)} chars")
        logger.info(f"  - I/O instructions length: {len(io_instructions)} chars")
        logger.info(f"  - Public dir: {public_dir}")
        logger.info(f"  - Output path: {output_path}")

        # Link public data into the sandbox workspace.
        # This prevents leaking any private/answer data.
        logger.info("Linking public data into sandbox...")
        logger.info(f"  Source dir: {public_dir}")
        self.workspace_service.link_data_to_workspace(public_dir)
        logger.info("  Sandbox ready")

        # Validate I/O instructions; regenerate if incomplete.
        if len(io_instructions) < 100 or "CRITICAL I/O" not in io_instructions:
            logger.warning(f"I/O instructions may be incomplete (length: {len(io_instructions)})")
            logger.warning(f"  First 200 chars: {io_instructions[:200]}")
            logger.warning("  This may cause the model to misunderstand file path requirements.")
            logger.warning("  Attempting to regenerate full I/O instructions...")

            # Try regenerating full I/O instructions.
            try:
                from dsat.services.data_analyzer import DataAnalyzer
                analyzer = DataAnalyzer()
                io_instructions = analyzer.generate_io_instructions(
                    output_path.name,
                    optimization_context=False
                )
                logger.info(f"Regenerated I/O instructions (length: {len(io_instructions)})")
            except Exception as e:
                logger.error(f"Regenerate failed: {e}")
                # Fallback to a hardcoded I/O instruction template.
                io_instructions = f"""
--- CRITICAL I/O REQUIREMENTS ---

You MUST follow these file system rules precisely. Failure to do so will cause a fatal error.

1. **INPUT DATA:**
   - All input files are located in the **current working directory** (./).
   - Example: Use `pd.read_csv('train.csv')`.

2. **OUTPUT FILE:**
   - You MUST save your final submission file to the **current working directory** (./).
   - The required output filename is: `{output_path.name}`
   - **Correct Example:** `submission_df.to_csv('{output_path.name}', index=False)`

**IMPORTANT:** These path requirements are non-negotiable and must be followed exactly.
"""

        # Create agent (merge init-time and runtime params).
        all_agent_kwargs = {**self._agent_init_kwargs, **agent_kwargs}
        agent = self.create_agent(**all_agent_kwargs)

        # Record start time for duration.
        import time
        start_time = time.time()

        # Run workflow (pass public_dir to workflow).
        await agent.solve(
            description=description,
            io_instructions=io_instructions,
            data_dir=public_dir
        )

        # Calculate execution time.
        duration = time.time() - start_time

        # Auto-grading (base facility; users do not need to handle).
        logger.info(f"\n{'='*80}")
        logger.info("Auto-grading...")
        logger.info(f"{'='*80}")

        score = None
        try:
            # Get submission file path.
            submission_file = self.workspace_service.get_path("sandbox_workdir") / output_path.name

            if submission_file.exists():
                logger.info(f"Submission file: {submission_file}")

                # Common grading flow: try multiple ways to load benchmark.
                benchmark = None
                benchmark_loaded = False

                # Method 1: task_loader.load_benchmark()
                if hasattr(task_loader, 'load_benchmark'):
                    try:
                        logger.info("Trying task_loader.load_benchmark()...")
                        benchmark = task_loader.load_benchmark(
                            task_id=task_id,
                            data_dir=data_dir
                        )
                        if benchmark:
                            benchmark_loaded = True
                            logger.info("Loaded benchmark via task_loader")
                    except Exception as e:
                        logger.warning(f"task_loader.load_benchmark() failed: {e}")

                # Fallback 2: Try loading directly from benchmarks/mlebench
                if not benchmark_loaded:
                    try:
                        logger.info(f"Attempting to load directly from benchmark/mlebench...")
                        from pathlib import Path as LibPath
                        benchmarks_dir = LibPath(__file__).parent.parent.parent / "benchmark" / "mlebench"
                        from dslighting.benchmark.mlebench.registry import Registry

                        registry = Registry(benchmarks_dir)
                        competition = registry.get_competition(task_id)

                        if competition:
                            # Create simple benchmark wrapper
                            class DirectBenchmark:
                                def __init__(self, comp):
                                    self.competition = comp

                                async def grade(self, submission_path: str):
                                    from dslighting.benchmark.mlebench.grade import grade_csv
                                    report = grade_csv(LibPath(submission_path), self.competition)
                                    return {
                                        'score': report.score,
                                        'valid_submission': report.valid_submission
                                    }

                            benchmark = DirectBenchmark(competition)
                            benchmark_loaded = True
                            logger.debug(f"Loaded benchmark directly from MLE-Bench")
                    except Exception as e:
                        logger.warning(f"Failed to load MLE-Bench directly: {e}")

                # Fallback 3: Use universal grading (check file format)
                if not benchmark_loaded:
                    logger.info(f"Using universal grading logic...")
                    try:
                        import pandas as pd
                        # Check if file can be read normally
                        df = pd.read_csv(submission_file)
                        logger.info(f"Valid submission file: {len(df)} rows")

                        # Universal grading: file exists and is readable = success
                        # (Cannot calculate real score without ground truth)
                        score = 0.0
                        logger.info(f"Universal grading: file valid but cannot calculate real score (requires ground truth)")
                        logger.info(f"Tip: Implement task_loader.load_benchmark() method to get real score")
                    except Exception as e:
                        logger.warning(f"Universal grading failed: {e}")

                # If benchmark was successfully loaded, use it for grading
                if benchmark_loaded and benchmark and hasattr(benchmark, 'grade'):
                    try:
                        # Call benchmark.grade() for grading
                        grade_result = await benchmark.grade(
                            submission_path=str(submission_file)
                        )

                        # Extract score (grade_result may be dict or object)
                        if isinstance(grade_result, dict):
                            score = grade_result.get('score', grade_result.get('metric', 0.0))
                        else:
                            score = float(grade_result) if grade_result is not None else 0.0

                        logger.info(f"Auto-grading completed | Score: {score}")
                    except Exception as e:
                        logger.warning(f"Benchmark grading failed: {e}")
                        logger.warning(f"   Will fall back to universal grading")
                        score = 0.0
            else:
                logger.warning(f"Submission file not found: {submission_file}")
                logger.warning(f"   Workflow execution failed, cannot grade")

        except Exception as e:
            logger.warning(f"Auto-grading failed: {e}")
            logger.warning(f"   Please check submission file format and benchmark configuration")

        logger.info(f"{'='*80}\n")

        # Build result object.
        from types import SimpleNamespace
        result = SimpleNamespace()

        # Populate result fields.
        result.score = score if score is not None else 0.0
        result.success = score is not None
        result.error = None if score is not None else "Grading failed or submission not found"

        # Record cost and duration.
        result.cost = self.llm_service.get_total_cost() if hasattr(self.llm_service, 'get_total_cost') else 0.0
        result.duration = duration

        logger.info(f"=" * 80)
        logger.info(f"✓ Workflow completed")
        logger.info(f"  - Success: {result.success}")
        logger.info(f"  - Score: {result.score}")
        logger.info(f"  - Cost: ${result.cost:.4f}")
        logger.info(f"  - Duration: {result.duration:.2f}s")
        logger.info(f"=" * 80)

        # ✅ Returnresultobject
        return result
