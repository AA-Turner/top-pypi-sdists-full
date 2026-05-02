"""
LLMClient Interface.

Generic interface for using ai-parrot clients in Flowtask components.
This interface allows executing any method from ai-parrot clients with flexible data processing.

Note: This is a mixin interface. Components should inherit from both LLMClient and FlowComponent:
    class MyComponent(LLMClient, FlowComponent):
        ...
"""
from typing import Any
from collections.abc import Callable
import time
import asyncio
import pandas as pd
from navconfig.logging import logging
# Lazy-loaded to avoid importing the full parrot + google-genai
# stack (~23s) on startup.
SUPPORTED_CLIENTS = None
from ..exceptions import ConfigError, ComponentError


class LLMClient:
    """
    Generic interface for using ai-parrot clients in Flowtask components.

    This interface allows executing any method from ai-parrot clients
    (ask, ask_to_image, generate_speech, etc.) with flexible data processing.

    Configuration Example:

        ```yaml
        MyComponent:
          client: google
          method: ask
          mode: row_by_row
          client_params:
            model: gemini-2.5-pro
            temperature: 0.4
          method_params:
            max_tokens: 2048
          column_mapping:
            prompt: review_text
            system_prompt: context
          output_column: analysis_result
        ```

    Attributes:
        client_name: Name of the ai-parrot client to use
        method_name: Name of the method to call on the client
        mode: Processing mode ('row_by_row' or 'grouped')
        output_column: Column name for storing results
        group_by: Columns for grouping data (when mode='grouped')
        client_params: Parameters for client initialization
        method_params: Fixed parameters for method calls
        column_mapping: Map DataFrame columns to method parameters
        aggregation_method: How to aggregate values in grouped mode
        max_concurrent_calls: Maximum concurrent API calls (default: 5)
        max_requests_per_minute: Maximum requests per minute (default: 50)
        retry_attempts: Number of retry attempts for failed calls (default: 3)
        retry_backoff_factor: Exponential backoff factor for retries (default: 2.0)
    """

    def __init__(
        self,
        job: Callable = None,
        loop: asyncio.AbstractEventLoop = None,
        *args,
        **kwargs
    ):
        # Client configuration
        self.client_name: str = kwargs.get('client', 'google')
        self.method_name: str = kwargs.get('method', 'ask')

        # Processing mode: 'row_by_row' or 'grouped'
        self.mode: str = kwargs.get('mode', 'row_by_row')

        # Output configuration
        self.output_column: str = kwargs.get('output_column')
        self.group_by: list = kwargs.get('group_by', [])

        # Client initialization parameters (model, temperature, api_key, etc.)
        self.client_params: dict = kwargs.get('client_params', {})

        # Fixed method parameters (max_tokens, etc.)
        self.method_params: dict = kwargs.get('method_params', {})

        # Column mapping: {method_param: dataframe_column}
        # Example: {'prompt': 'review_text', 'system_prompt': 'context'}
        self.column_mapping: dict = kwargs.get('column_mapping', {})

        # Aggregation function for grouped mode ('list', 'join', 'first')
        self.aggregation_method: str = kwargs.get('aggregation_method', 'list')

        # Rate limiting and retry configuration
        self.max_concurrent_calls: int = kwargs.get('max_concurrent_calls', 5)
        self.max_requests_per_minute: int = kwargs.get('max_requests_per_minute', 50)
        self.retry_attempts: int = kwargs.get('retry_attempts', 3)
        self.retry_backoff_factor: float = kwargs.get('retry_backoff_factor', 2.0)

        # Initialize parent - FlowComponent expects (job, *args, **kwargs)
        super(LLMClient, self).__init__(job, loop=loop, *args, **kwargs)

        # Logger
        self._logger = logging.getLogger(f'LLMClient.{self.client_name}')

        # Client instance (will be initialized in run())
        self._client_class = None

    async def start(self, **kwargs):
        """
        Initialize and validate the LLMClient component.

        Validates:
        - Input data exists
        - Required configuration parameters
        - Client name is supported
        - Method exists on the selected client

        Returns:
            bool: True if initialization is successful

        Raises:
            ComponentError: If input data is missing
            ConfigError: If configuration is invalid
        """
        # Validate input data
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError(
                f"{self.__name__}: Input data was not found"
            )

        # Validate output column
        if not self.output_column:
            raise ConfigError(
                f"{self.__name__}: output_column is required"
            )

        # Lazy import: only load parrot when the component is actually used.
        global SUPPORTED_CLIENTS
        if SUPPORTED_CLIENTS is None:
            from parrot.clients.factory import SUPPORTED_CLIENTS as _SC
            SUPPORTED_CLIENTS = _SC

        # Validate client name
        if self.client_name not in SUPPORTED_CLIENTS:
            available = ', '.join(SUPPORTED_CLIENTS.keys())
            raise ConfigError(
                f"{self.__name__}: Unsupported client '{self.client_name}'. "
                f"Available clients: {available}"
            )

        # Get client class
        self._client_class = SUPPORTED_CLIENTS[self.client_name]

        # Validate method exists
        if not hasattr(self._client_class, self.method_name):
            raise ConfigError(
                f"{self.__name__}: Method '{self.method_name}' not found "
                f"on client '{self.client_name}'"
            )

        # Validate mode
        if self.mode not in ['row_by_row', 'grouped']:
            raise ConfigError(
                f"{self.__name__}: Invalid mode '{self.mode}'. "
                f"Must be 'row_by_row' or 'grouped'"
            )

        # Validate grouped mode requirements
        if self.mode == 'grouped' and not self.group_by:
            raise ConfigError(
                f"{self.__name__}: group_by is required when mode='grouped'"
            )

        self._logger.info(
            f"Initialized LLMClient: client={self.client_name}, "
            f"method={self.method_name}, mode={self.mode}"
        )

        return True

    def _map_params(self, row: pd.Series) -> dict:
        """
        Map DataFrame columns to method parameters.

        Combines fixed method_params with dynamic values from the row
        based on column_mapping.

        Args:
            row: A pandas Series representing a DataFrame row

        Returns:
            dict: Combined parameters for the method call

        Example:
            If column_mapping = {'prompt': 'review_text', 'user_id': 'customer_id'}
            and row = {'review_text': 'Great!', 'customer_id': '123'}

            Returns: {'prompt': 'Great!', 'user_id': '123', ...method_params}
        """
        params = self.method_params.copy()

        for param_name, column_name in self.column_mapping.items():
            if column_name in row.index:
                value = row[column_name]
                # Skip NaN values
                if pd.notna(value):
                    params[param_name] = value
            else:
                self._logger.warning(
                    f"Column '{column_name}' not found in row. "
                    f"Skipping parameter '{param_name}'"
                )

        return params

    async def _process_row_with_retry(
        self,
        idx: int,
        row: pd.Series,
        method: Callable,
        semaphore: asyncio.Semaphore,
        min_request_interval: float
    ) -> tuple:
        """
        Process a single row with rate limiting and retry logic.

        Args:
            idx: Row index
            row: Row data
            method: The client method to call
            semaphore: Asyncio semaphore for concurrency control
            min_request_interval: Minimum time between requests (seconds)

        Returns:
            Tuple of (idx, result)
        """
        async with semaphore:
            for attempt in range(self.retry_attempts):
                try:
                    # Wait minimum interval before request to respect RPM limit
                    if min_request_interval > 0:
                        await asyncio.sleep(min_request_interval)

                    # Map parameters from row
                    params = self._map_params(row)

                    # Call the client method
                    self._logger.debug(
                        f"Processing row {idx} with params: {list(params.keys())}"
                    )
                    response = await method(**params)

                    # Extract result based on response type
                    result = self._extract_result(response)

                    # Success - return the result
                    return (idx, result)

                except Exception as e:
                    if attempt < self.retry_attempts - 1:
                        # Calculate exponential backoff wait time
                        wait_time = self.retry_backoff_factor ** attempt
                        self._logger.warning(
                            f"Attempt {attempt + 1}/{self.retry_attempts} failed for row {idx}: {e}. "
                            f"Retrying in {wait_time:.1f}s..."
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        # All attempts failed
                        self._logger.error(
                            f"All {self.retry_attempts} attempts failed for row {idx}: {e}"
                        )
                        return (idx, None)

        # This should never be reached, but just in case
        return (idx, None)

    async def _process_rows(self, method: Callable) -> pd.DataFrame:
        """
        Process data row-by-row mode with rate limiting and retry logic.

        Processes rows concurrently with controlled concurrency and rate limiting.

        Args:
            method: The client method to call

        Returns:
            pd.DataFrame: Data with results in output_column
        """
        # Calculate rate limiting parameters
        min_request_interval = 60.0 / self.max_requests_per_minute if self.max_requests_per_minute > 0 else 0
        semaphore = asyncio.Semaphore(self.max_concurrent_calls)

        # Create tasks for all rows
        tasks = []
        for idx, row in self.data.iterrows():
            task = self._process_row_with_retry(
                idx,
                row,
                method,
                semaphore,
                min_request_interval
            )
            tasks.append(task)

        # Log processing information
        self._logger.info(
            f"Processing {len(tasks)} rows with max {self.max_concurrent_calls} concurrent requests, "
            f"{self.max_requests_per_minute} RPM limit (interval: {min_request_interval:.2f}s)"
        )

        # Process all tasks concurrently (but controlled by semaphore and rate limit)
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        elapsed_time = time.time() - start_time

        # Create results dictionary maintaining order
        results_dict = {idx: result for idx, result in results}

        # Add results to dataframe in correct order
        self.data[self.output_column] = [results_dict.get(idx) for idx in self.data.index]

        # Log performance metrics
        successful_count = sum(1 for _, result in results if result is not None)
        failed_count = len(results) - successful_count
        self._logger.info(
            f"Completed {len(results)} rows in {elapsed_time:.2f}s "
            f"({len(results) / elapsed_time:.2f} rows/sec). "
            f"Success: {successful_count}, Failed: {failed_count}"
        )

        return self.data

    async def _process_grouped(self, method: Callable) -> pd.DataFrame:
        """
        Process data in grouped mode.

        Groups data by specified columns, aggregates values,
        calls the client method once per group.

        Args:
            method: The client method to call

        Returns:
            pd.DataFrame: Grouped data with results
        """
        # Group data
        grouped = self.data.groupby(self.group_by)

        results = {}

        for group_key, group_df in grouped:
            try:
                # Prepare aggregated data for this group
                aggregated_row = self._aggregate_group(group_df)

                # Map parameters
                params = self._map_params(aggregated_row)

                # Call the client method
                self._logger.debug(
                    f"Processing group {group_key}"
                )
                response = await method(**params)

                # Extract and store result
                result = self._extract_result(response)
                results[group_key] = result

            except Exception as err:
                self._logger.error(
                    f"Error processing group {group_key}: {err}"
                )
                results[group_key] = None

        # Create grouped dataframe with results
        grouped_df = self.data.groupby(self.group_by).first().reset_index()

        # Map results to dataframe
        if len(self.group_by) == 1:
            grouped_df[self.output_column] = grouped_df[self.group_by[0]].map(results)
        else:
            grouped_df[self.output_column] = grouped_df[self.group_by].apply(
                lambda x: results.get(tuple(x)), axis=1
            )

        return grouped_df

    def _aggregate_group(self, group_df: pd.DataFrame) -> pd.Series:
        """
        Aggregate a group of rows into a single row for processing.

        Args:
            group_df: DataFrame containing rows for this group

        Returns:
            pd.Series: Aggregated row
        """
        aggregated = {}

        for column in group_df.columns:
            if column in self.group_by:
                # Keep group keys as-is
                aggregated[column] = group_df[column].iloc[0]
            elif column in self.column_mapping.values():
                # Aggregate mapped columns
                if self.aggregation_method == 'list':
                    aggregated[column] = group_df[column].tolist()
                elif self.aggregation_method == 'join':
                    aggregated[column] = '\n'.join(group_df[column].astype(str))
                else:
                    # Use first value as default
                    aggregated[column] = group_df[column].iloc[0]
            else:
                # Other columns: use first value
                aggregated[column] = group_df[column].iloc[0]

        return pd.Series(aggregated)

    def _extract_result(self, response: Any) -> Any:
        """
        Extract the result from the client response.

        Different clients and methods return different response types.
        This method handles common response patterns.

        Args:
            response: The response from the client method

        Returns:
            The extracted result value
        """
        # Handle AIMessage objects
        if hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'content'):
            return response.content
        elif hasattr(response, 'output'):
            return response.output
        # Handle dict responses
        elif isinstance(response, dict):
            # Try common keys
            for key in ['text', 'content', 'output', 'result']:
                if key in response:
                    return response[key]
            return response
        # Return as-is for other types
        else:
            return response

    async def run(self, *args, **kwargs):
        """
        Execute the LLMClient processing.

        Main execution flow:
        1. Initialize the ai-parrot client
        2. Get the specified method
        3. Process data according to mode
        4. Return results

        Returns:
            pd.DataFrame: Processed data with results
        """
        try:
            # Initialize client with context manager
            async with self._client_class(**self.client_params) as client:
                # Get the method to execute
                method = getattr(client, self.method_name)

                # Process according to mode
                if self.mode == 'row_by_row':
                    self.data = await self._process_rows(method)
                elif self.mode == 'grouped':
                    self.data = await self._process_grouped(method)

                self._logger.info(
                    f"Successfully processed {len(self.data)} rows/groups"
                )

        except Exception as err:
            raise ComponentError(
                f"{self.__name__}: Error executing client method: {err}"
            ) from err

        return self.data
