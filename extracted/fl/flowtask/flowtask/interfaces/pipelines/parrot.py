import asyncio
import importlib
from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod
import pandas as pd
from navconfig.logging import logging
from parrot.clients.google import GoogleGenAIClient
from parrot.models.google import GoogleModel
from ...exceptions import (
    ComponentError,
    ConfigError
)


class AIPipeline(ABC):
    """
    AIPipeline Interface

    Overview:
        Interface for components that need to execute AI pipelines on DataFrame rows.
        Provides functionality to dynamically load pipelines by name and execute them
        over each row in a pandas DataFrame.

    This interface handles:
        - Dynamic pipeline loading by name
        - Row-by-row processing of DataFrames
        - Pipeline result aggregation
        - Error handling and logging
    """

    def __init__(self, *args, **kwargs):
        """Initialize the AIPipeline interface."""
        self._pipeline_name: str = kwargs.pop('pipeline', None)
        self._pipeline: Any = None
        self._pipeline_results: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(
            f'Flowtask.Pipelines.{self.__class__.__name__}'
        )
        if not self._pipeline_name:
            raise ConfigError("Pipeline name is required")
        super().__init__(*args, **kwargs)

    def _load_pipeline(self, pipeline_name: str) -> Any:
        """
        Load a pipeline class dynamically by name.

        Args:
            pipeline_name: Name of the pipeline (e.g., 'planogram_compliance')

        Returns:
            Pipeline class instance

        Raises:
            ComponentError: If pipeline cannot be loaded
        """
        pipeline_mapping = {
            'planogram_compliance': 'parrot_pipelines.planogram.plan.PlanogramCompliance',
            # Add more pipeline mappings here as needed
        }

        if pipeline_name not in pipeline_mapping:
            raise ComponentError(
                f"Unknown pipeline: {pipeline_name}"
            )

        module_path = pipeline_mapping[pipeline_name]
        try:
            # Split the module path to get module and class name
            module_name, class_name = module_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            pipeline_class = getattr(module, class_name)
            self.logger.info(
                f"Successfully loaded pipeline: {pipeline_name}"
            )
            return pipeline_class

        except ImportError as e:
            raise ComponentError(
                f"Could not import pipeline module {module_name}: {e}"
            )
        except AttributeError as e:
            raise ComponentError(
                f"Pipeline class {class_name} not found in module {module_name}: {e}"
            )

    def _initialize_pipeline(self, pipeline_class: Any, **pipeline_kwargs) -> Any:
        """
        Initialize the pipeline with the provided arguments.

        Args:
            pipeline_class: The pipeline class to initialize
            **pipeline_kwargs: Arguments to pass to the pipeline constructor

        Returns:
            Initialized pipeline instance
        """
        try:
            return pipeline_class(**pipeline_kwargs)
        except Exception as e:
            raise ComponentError(f"Failed to initialize pipeline: {e}")

    async def _process_dataframe_rows(
        self,
        df: pd.DataFrame,
        pipeline_method: str = 'run'
    ) -> List[Dict[str, Any]]:
        """
        Process each row in the DataFrame through the pipeline.

        Args:
            df: DataFrame to process
            pipeline_method: Name of the pipeline method to call (default: 'run')

        Returns:
            List of results from pipeline execution
        """
        results = []

        for idx, row in df.iterrows():
            try:
                # Convert row to dictionary for pipeline
                row_dict = row.to_dict()

                # Get the pipeline method
                if not hasattr(self._pipeline, pipeline_method):
                    raise ComponentError(f"Pipeline does not have method '{pipeline_method}'")

                method = getattr(self._pipeline, pipeline_method)
                self.logger.debug('Processing row %s', idx)
                # Execute pipeline method
                if asyncio.iscoroutinefunction(method):
                    result = await method(
                        **row_dict
                    )
                else:
                    result = method(**row_dict)

                # Store result with row index for tracking
                results.append({
                    'row_index': idx,
                    'result': result,
                    'status': 'success'
                })

                self.logger.debug(
                    f"Successfully processed row {idx}"
                )

            except Exception as e:
                self.logger.error(f"Error processing row {idx}: {e}")
                results.append({
                    'row_index': idx,
                    'result': None,
                    'status': 'error',
                    'error': str(e)
                })

        return results

    @abstractmethod
    def _post_process_results(
        self,
        results: List[Dict[str, Any]],
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Post-process the pipeline results and integrate them back into the DataFrame.

        Args:
            results: List of pipeline results
            df: Original DataFrame

        Returns:
            DataFrame with integrated results
        """
        pass

    async def execute_pipeline(
        self,
        df: pd.DataFrame,
        **pipeline_kwargs
    ) -> pd.DataFrame:
        """
        Execute the pipeline on the entire DataFrame.

        Args:
            df: DataFrame to process
            **pipeline_kwargs: Arguments to pass to pipeline initialization

        Returns:
            DataFrame with pipeline results integrated
        """
        # Load and initialize pipeline
        pipeline_class = self._load_pipeline(self._pipeline_name)
        if 'llm' not in pipeline_kwargs:
            pipeline_kwargs['llm'] = GoogleGenAIClient(
                model=GoogleModel.GEMINI_3_PRO_PREVIEW
            )

        # Initialize pipeline instance:
        self._pipeline = self._initialize_pipeline(
            pipeline_class,
            **pipeline_kwargs
        )

        # Process all rows
        results = await self._process_dataframe_rows(df)

        # Store results for potential debugging/analysis
        self._pipeline_results = results

        # Post-process and return updated DataFrame
        return self._post_process_results(results, df)
