from collections.abc import Callable
import asyncio
import pandas as pd
import orjson
from ..exceptions import DataNotFound
from ..interfaces.ParrotBot import ParrotBot
from .flow import FlowComponent


class CallAnalysis(ParrotBot, FlowComponent):
    """
    CallAnalysis.

    Overview

        The CallAnalysis class is a component for interacting with an IA Agent for making Call Analysis.
        It extends the FlowComponent class and adds functionality to load file content from paths.

    :widths: auto

        | output_column    |   Yes    | Column for saving the Call Analysis information.                                                 |
        | use_dataframe    |   No     | If True (default), use dataframe mode with file_path_column. If False, use directory/pattern.   |
        | use_bytes_input  |   No     | If True, read content from BytesIO objects instead of file paths. Defaults to False.            |
        | bytes_column     |   No     | Column containing BytesIO objects (used when use_bytes_input is True).                          |
        | file_path_column |   No     | Column containing file paths to load content from (dataframe mode).                             |
        | directory        |   No     | Directory path to search for files (file mode).                                                 |
        | pattern          |   No     | Glob pattern to match files (file mode).                                                        |
        | content_column   |   No     | Column to store loaded file content (defaults to 'content').                                   |
        | as_text          |   No     | Whether to read files as text (True) or bytes (False). Defaults to True.                      |
        | group_analysis   |   No     | If True, group rows by description_column before analysis. Defaults to auto-detection.         |
        | max_concurrent_calls | No   | Maximum number of concurrent API calls. Defaults to 1 (google-genai v1.49.0+ bug).           |
        |                  |          | Controls concurrency. Increase at your own risk until Google fixes aiohttp resolver bug.       |
        | max_requests_per_minute | No | Maximum API requests per minute. Defaults to 50. Helps stay within API rate limits.        |
        | retry_attempts   |   No     | Number of retry attempts for failed API calls. Defaults to 3.                                   |
        | retry_backoff_factor | No   | Exponential backoff factor for retries. Defaults to 2.0. Wait time = factor^attempt.          |
        | skip_existing    |   No     | Skip rows that already have analysis in output_column. Defaults to True. Useful for           |
        |                  |          | reprocessing by batches without wasting API calls on already analyzed data.                   |
    Return

        A Pandas Dataframe with the Call Analysis statistics.

    Example Configuration (Dataframe Mode - Default):

    .. code-block:: yaml

        - CallAnalysis:
            prompt_file: prompt.txt
            llm:
                llm: google
                model: gemini-2.5-flash
                temperature: 0.4
                max_tokens: 4096
            use_dataframe: true
            description_column: call_id
            file_path_column: srt_file_path
            content_column: transcript_content
            output_column: call_analysis
            as_text: true
            columns:
                - call_id
                - customer_name
                - agent_name
                - duration
                - call_date
                - srt_file_path

    Example Configuration (File Mode):

    .. code-block:: yaml

        - CallAnalysis:
            prompt_file: prompt.txt
            llm:
                llm: google
                model: gemini-2.5-flash
                temperature: 0.4
                max_tokens: 4096
            use_dataframe: false
            directory: /home/ubuntu/symbits/placerai/traffic/{day_six}/
            pattern: "*.srt"
            description_column: filename
            content_column: transcript_content
            output_column: call_analysis
            as_text: true

    Example Configuration (BytesIO Mode):

    .. code-block:: yaml

        - CallAnalysis:
            prompt_file: prompt.txt
            llm:
              llm: google
              model: gemini-2.5-flash
              temperature: 0.4
              max_tokens: 4096
            use_dataframe: true
            use_bytes_input: true
            bytes_column: transcript_srt_bytesio
            content_column: transcript_content
            description_column: call_id
            output_column: call_analysis
            as_text: true
            columns:
              - call_id
              - customer_name

    Example Configuration (With Rate Limiting for High Volume):

    .. code-block:: yaml

        - CallAnalysis:
            prompt_file: prompt-audio-sentiment.txt
            llm:
              llm: google
              model: gemini-2.5-pro
              temperature: 0.4
              max_tokens: 8192
            use_dataframe: true
            use_bytes_input: true
            bytes_column: transcript_srt_bytesio
            content_column: transcript_content
            description_column: call_id
            output_column: call_analysis
            as_text: true
            # Rate limiting configuration for processing 200-300 calls
            max_concurrent_calls: 5           # Process max 5 calls at once
            max_requests_per_minute: 50       # Stay under 50 RPM API limit
            retry_attempts: 3                 # Retry failed calls up to 3 times
            retry_backoff_factor: 2.0         # Wait 2^attempt seconds between retries

    Example Configuration (Batch Reprocessing - Skip Existing):

    .. code-block:: yaml

        # Step 1: Query existing analysis from database
        - QueryToPandas:
            query: |
              SELECT call_id, call_analysis
              FROM assurant.call_analysis
              WHERE processing_date >= NOW() - INTERVAL '7 days'
            output_var: existing_analysis

        # Step 2: Merge with new data to avoid reprocessing
        - MergeDataFrames:
            left: current_data
            right: existing_analysis
            on: call_id
            how: left

        # Step 3: Only process calls without analysis
        - CallAnalysis:
            prompt_file: prompt-audio-sentiment.txt
            llm:
              llm: google
              model: gemini-2.5-pro
            use_bytes_input: true
            bytes_column: transcript_srt_bytesio
            output_column: call_analysis
            skip_existing: true              # Skip rows that already have call_analysis
            max_concurrent_calls: 5
            max_requests_per_minute: 50

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          CallAnalysis:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        # Set default goal for call analysis
        kwargs.setdefault(
            'goal',
            'Your task is to analyze call recordings and provide detailed sentiment analysis'
        )

        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

        # File handling parameters
        self.use_dataframe: bool = kwargs.get('use_dataframe', True)
        self.file_path_column: str = kwargs.get('file_path_column')
        self.directory: str = kwargs.get('directory')
        self.pattern: str = kwargs.get('pattern')
        self.content_column: str = kwargs.get('content_column', 'content')
        self.as_text: bool = kwargs.get('as_text', True)
        self.group_analysis: bool = kwargs.get('group_analysis', None)

        # BytesIO input parameters
        self.use_bytes_input: bool = kwargs.get('use_bytes_input', False)
        self.bytes_column: str = kwargs.get('bytes_column')

        # Columns to preserve in the result (required by ParrotBot)
        self.columns: list = kwargs.get('columns', [])

        # Set survey mode to True to avoid rating column dependency
        self._survey_mode: bool = True  # Force survey mode to avoid rating column

        # Override goal if not provided
        self._goal: str = kwargs.get(
            'goal',
            'Your task is to analyze call recordings and provide detailed sentiment analysis'
        )

        # Rate limiting and concurrency control configuration
        # IMPORTANT: google-genai SDK v1.49.0+ has a bug where concurrent requests
        # create separate aiohttp sessions causing AsyncResolver to be None.
        # Default to 1 until Google fixes this issue. Increase at your own risk.
        self.max_concurrent_calls: int = kwargs.get('max_concurrent_calls', 1)
        self.max_requests_per_minute: int = kwargs.get('max_requests_per_minute', 50)
        self.retry_attempts: int = kwargs.get('retry_attempts', 3)
        self.retry_backoff_factor: float = kwargs.get('retry_backoff_factor', 2.0)

        # Skip existing analysis configuration
        self.skip_existing: bool = kwargs.get('skip_existing', True)
        self.lookup_schema_column: str = kwargs.get('schema_column', 'program_slug')

    def load_from_file(
        self,
        df: pd.DataFrame,
        field: str,
        column: str = None,
        as_text: bool = True
    ) -> pd.DataFrame:
        """
        Loads the content of a file specified as a path in `column` into `field`.

        Args:
            df: pandas DataFrame with a column containing file paths.
            field: name of the new column to store the file content.
            column: name of the column with file paths (defaults to `field`).
            as_text: if True, read file as text; otherwise, read as bytes.
        """
        if column is None:
            column = field

        def read_file_content(path: str) -> str | bytes | None:
            if not isinstance(path, str):
                self._logger.warning(f"Invalid path type: {type(path)}, expected string")
                return None
            if pd.isna(path) or path.strip() == '':
                self._logger.warning("Empty or NaN path found")
                return None
            try:
                with open(path, 'r' if as_text else 'rb') as f:
                    content = f.read()
                    self._logger.debug(f"Successfully loaded content from {path}")
                    return content
            except FileNotFoundError:
                self._logger.error(f"File not found: {path}")
                return None
            except PermissionError:
                self._logger.error(f"Permission denied reading file: {path}")
                return None
            except Exception as e:
                self._logger.error(f"Error reading {path}: {e}")
                return None

        df[field] = df[column].apply(read_file_content)
        return df

    def load_from_bytesio(
        self,
        df: pd.DataFrame,
        field: str,
        column: str = None,
        as_text: bool = True
    ) -> pd.DataFrame:
        """
        Loads content from BytesIO objects in a column into a new field.

        Args:
            df: pandas DataFrame with a column containing BytesIO objects.
            field: name of the new column to store the content.
            column: name of the column with BytesIO objects (defaults to `field`).
            as_text: if True, decode bytes to text; otherwise, return bytes.
        """
        if column is None:
            column = field

        def read_bytesio_content(bytesio_obj) -> str | bytes | None:
            from io import BytesIO

            if not isinstance(bytesio_obj, BytesIO):
                self._logger.warning(f"Invalid type: {type(bytesio_obj)}, expected BytesIO")
                return None
            if pd.isna(bytesio_obj) or bytesio_obj is None:
                self._logger.warning("Empty or NaN BytesIO object found")
                return None
            try:
                # Read content from BytesIO
                bytesio_obj.seek(0)  # Ensure we're at the beginning
                content = bytesio_obj.read()

                # Convert to text if requested
                if as_text and isinstance(content, bytes):
                    try:
                        content = content.decode('utf-8')
                    except UnicodeDecodeError:
                        self._logger.warning("Failed to decode bytes as UTF-8, returning raw bytes")

                self._logger.debug(
                    "Successfully loaded content from BytesIO object"
                )
                return content
            except Exception as e:
                self._logger.error(f"Error reading BytesIO object: {e}")
                return None

        df[field] = df[column].apply(read_bytesio_content)
        return df


    async def start(self, **kwargs):
        """
        start

        Overview

            The start method is a method for starting the CallAnalysis component.
            Validates required parameters and loads file content.

        Parameters

            kwargs: dict
                A dictionary containing the parameters for the CallAnalysis component.

        Return

            True if the CallAnalysis component started successfully.

        """
        if self.previous:
            self.data = self.input
        # Check if we're in dataframe mode or file mode
        if not self.use_dataframe:
            # File mode - use directory and pattern like FileList
            self._logger.info("Using file mode with directory and pattern")

            # Validate required parameters for file mode
            if not self.directory:
                from ..exceptions import ConfigError
                raise ConfigError(
                    f"{self._bot_name.lower()}: directory is required when use_dataframe is false"
                )

            if not self.pattern:
                from ..exceptions import ConfigError
                raise ConfigError(
                    f"{self._bot_name.lower()}: pattern is required when use_dataframe is false"
                )

            # Process directory with mask replacement
            if isinstance(self.directory, str) and "{" in self.directory:
                self.directory = self.mask_replacement(self.directory)
                self._logger.info(f"Directory after mask replacement: {self.directory}")

            # Check if directory exists
            from pathlib import Path
            dir_path = Path(self.directory)
            if not dir_path.exists() or not dir_path.is_dir():
                from ..exceptions import ComponentError
                raise ComponentError(f"Directory doesn't exist: {self.directory}")

            # Find files matching pattern
            import glob
            pattern_path = dir_path / self.pattern
            matching_files = glob.glob(str(pattern_path))

            if not matching_files:
                raise DataNotFound(f"No files found matching pattern: {pattern_path}")

            # Create dataframe with found files
            data = []
            for file_path in matching_files:
                path_obj = Path(file_path)
                data.append({
                    self._desc_column: path_obj.stem,  # filename without extension
                    'file_path': str(file_path),
                    'full_filename': path_obj.name  # Keep full filename with extension
                })

            self.data = pd.DataFrame(data)
            self.file_path_column = 'file_path'  # Set the column name for file paths
            self._logger.info(
                f"Found {len(self.data)} files matching pattern '{self.pattern}' in directory '{self.directory}'"
            )

            # Set up columns for ParrotBot (include description_column and file_path)
            if not self.columns:
                self.columns = [self._desc_column, 'file_path', 'full_filename']
            else:
                # Ensure description_column is in columns
                if self._desc_column not in self.columns:
                    self.columns.append(self._desc_column)
                if 'file_path' not in self.columns:
                    self.columns.append('file_path')
                if 'full_filename' not in self.columns:
                    self.columns.append('full_filename')

            # Set up the data for ParrotBot (bypass the previous component check)
            self.input = self.data
            self._component = self  # Set _component to self to satisfy ParrotBot's previous check

            # Call parent start method for file mode
            await super().start(**kwargs)

        else:
            # Dataframe mode - first call parent start to initialize self.data
            if self.use_bytes_input:
                self._logger.info("Using dataframe mode with BytesIO input")
            else:
                self._logger.info("Using dataframe mode with file path input")

            # Call parent start method FIRST to initialize self.data from previous component
            await super().start(**kwargs)

            # Check for empty input before any processing
            if self.data is None or (isinstance(self.data, pd.DataFrame) and self.data.empty):
                raise DataNotFound(
                    f"{self._bot_name.lower()}: received empty DataFrame from previous component. "
                    f"No data to analyze."
                )

            # Normalize dict inputs (e.g., multi-schema outputs) into a single DataFrame
            if isinstance(self.data, dict):
                frames = []
                for schema_key, df_val in self.data.items():
                    if not isinstance(df_val, pd.DataFrame):
                        continue
                    df_local = df_val
                    if self.lookup_schema_column and self.lookup_schema_column not in df_local.columns:
                        df_local = df_local.copy()
                        df_local[self.lookup_schema_column] = schema_key
                    frames.append(df_local)
                if not frames:
                    raise DataNotFound(
                        f"{self._bot_name.lower()}: expected DataFrame input but got dict without DataFrames."
                    )
                self.data = pd.concat(frames, ignore_index=True)
                self._logger.info(
                    f"{self._bot_name.lower()}: flattened dict input into dataframe with {len(self.data)} rows"
                )

            # NOW validate required parameters based on input mode
            if self.use_bytes_input:
                # BytesIO mode - validate bytes_column parameter
                if not self.bytes_column:
                    from ..exceptions import ConfigError
                    raise ConfigError(
                        f"{self._bot_name.lower()}: bytes_column is required when use_bytes_input is true"
                    )

                # Check if bytes_column exists in the data (NOW self.data is initialized)
                # UNLESS we're in skip_existing mode and all rows already have analysis
                if self.bytes_column not in self.data.columns:
                    # Check if we can skip the validation because all rows already have output
                    if self.skip_existing and self.output_column in self.data.columns:
                        # Count rows that need processing (don't have output_column value)
                        rows_needing_processing = self.data[self.output_column].isna().sum()
                        if rows_needing_processing == 0:
                            # All rows already have analysis, we don't need bytes_column
                            self._logger.info(
                                f"All {len(self.data)} rows already have '{self.output_column}'. "
                                f"Skipping '{self.bytes_column}' validation."
                            )
                        else:
                            # Some rows need processing, we need bytes_column
                            raise DataNotFound(
                                f"{self._bot_name.lower()}: bytes_column '{self.bytes_column}' not found in data columns. "
                                f"{rows_needing_processing} rows need processing but bytes_column is missing."
                            )
                    else:
                        raise DataNotFound(
                            f"{self._bot_name.lower()}: bytes_column '{self.bytes_column}' not found in data columns: {list(self.data.columns)}"
                        )

                # Set up columns for ParrotBot
                if not self.columns:
                    # Default columns: include description_column and bytes_column (if it exists)
                    self.columns = [self._desc_column]
                    if self.bytes_column in self.data.columns:
                        self.columns.append(self.bytes_column)
                else:
                    # Ensure required columns are in the list
                    if self._desc_column not in self.columns:
                        self.columns.append(self._desc_column)
                    if self.bytes_column in self.data.columns and self.bytes_column not in self.columns:
                        self.columns.append(self.bytes_column)

            else:
                # File path mode - validate file_path_column parameter
                if not self.file_path_column:
                    from ..exceptions import ConfigError
                    raise ConfigError(
                        f"{self._bot_name.lower()}: file_path_column is required when use_dataframe is true and use_bytes_input is false"
                    )

                # Check if file_path_column exists in the data (NOW self.data is initialized)
                if self.file_path_column not in self.data.columns:
                    raise DataNotFound(
                        f"{self._bot_name.lower()}: file_path_column '{self.file_path_column}' not found in data columns: {list(self.data.columns)}"  # noqa
                    )

                # In dataframe mode with file paths, preserve ALL original columns by default
                if not self.columns:
                    # By default, preserve all columns from the input dataframe
                    self.columns = list(self.data.columns)
                else:
                    # Ensure required columns are in the list
                    if self._desc_column not in self.columns:
                        self.columns.append(self._desc_column)
                    if self.file_path_column not in self.columns:
                        self.columns.append(self.file_path_column)

                self._logger.info(f"Using dataframe mode with {len(self.data)} rows")
                self._logger.info(f"Preserving columns: {self.columns}")

        # Load content into the dataframe based on input mode
        # Only load if the source column exists (might not exist if all rows are skipped)
        if self.use_bytes_input:
            if self.bytes_column in self.data.columns:
                # Load from BytesIO objects
                self._logger.info(f"Loading content from BytesIO column '{self.bytes_column}' into '{self.content_column}'")
                self.data = self.load_from_bytesio(
                    df=self.data,
                    field=self.content_column,
                    column=self.bytes_column,
                    as_text=self.as_text
                )
                # Filter out rows where BytesIO content could not be loaded
                # (e.g. NaN/float values instead of actual BytesIO objects)
                original_count = len(self.data)
                self.data = self.data[
                    self.data[self.content_column].notna()
                ].reset_index(drop=True)
                filtered_count = original_count - len(self.data)
                if filtered_count > 0:
                    self._logger.info(
                        f"Filtered out {filtered_count}/{original_count} rows "
                        f"with no valid content from '{self.bytes_column}'"
                    )
                if self.data.empty:
                    raise DataNotFound(
                        f"{self._bot_name.lower()}: No valid BytesIO data found "
                        f"in column '{self.bytes_column}'. "
                        f"All {original_count} rows had NaN/invalid values."
                    )
            else:
                self._logger.info(
                    f"Skipping content loading: '{self.bytes_column}' not found (all rows will be skipped)"
                )
        else:
            # Load from file paths
            self._logger.info(f"Loading file content from column '{self.file_path_column}' into '{self.content_column}'")
            self.data = self.load_from_file(
                df=self.data,
                field=self.content_column,
                column=self.file_path_column,
                as_text=self.as_text
            )

        # Set eval_column to the content column for bot processing
        self._eval_column = self.content_column

        # Log statistics (only if content was actually loaded)
        if self.content_column in self.data.columns:
            content_loaded = self.data[self.content_column].notna().sum()
            total_records = len(self.data)
            source_type = "BytesIO objects" if self.use_bytes_input else "files"
            self._logger.info(f"Successfully loaded content from {content_loaded}/{total_records} {source_type}")
        else:
            self._logger.info(f"Content loading skipped - will use existing '{self.output_column}' values")

        return True

    def format_question(self, call_identifier, transcripts, row=None):
        """
        Format the question for call analysis.

        Args:
            call_identifier: identifier for the call (from description_column)
            transcripts: list of transcript content
            row: optional row data for additional context

        Returns:
            str: formatted question for the AI bot
        """
        # Combine all transcripts for this call identifier
        combined_transcript = "\n\n".join([
            transcript.strip() if transcript and len(transcript) < 10000
            else (transcript[:10000] + "..." if transcript else "")
            for transcript in transcripts
        ])

        question = f"""
        Call ID: {call_identifier}

        Please analyze the following call transcript and provide a detailed sentiment analysis:

        TRANSCRIPT:
        {combined_transcript}

        Please provide your analysis in the specified JSON format.
        """

        return question

    async def _process_with_rate_limit(
        self,
        call_identifier: str,
        transcripts: list,
        row,
        semaphore: asyncio.Semaphore,
        min_request_interval: float,
        call_key=None
    ) -> tuple:
        """
        Process a single call with rate limiting and retry logic.

        Args:
            call_identifier: Identifier for the call
            transcripts: List of transcript content
            row: Row data for context
            semaphore: Asyncio semaphore for concurrency control
            min_request_interval: Minimum time between requests (seconds)

        Returns:
            Tuple of (call_key or call_identifier, result)
        """
        call_key = call_key or call_identifier
        async with semaphore:
            for attempt in range(self.retry_attempts):
                try:
                    # Wait minimum interval before request to respect RPM limit
                    if min_request_interval > 0:
                        await asyncio.sleep(min_request_interval)

                    # Format and invoke the bot
                    formatted_question = self.format_question(call_identifier, transcripts, row)
                    result = await self._bot.invoke(question=formatted_question)

                    # Try to parse JSON output before returning
                    try:
                        parsed_output = orjson.loads(result.output) if isinstance(result.output, str) else result.output
                    except Exception:
                        parsed_output = result.output  # fallback: keep as string if parsing fails

                    # Success - return the parsed result
                    self._logger.debug(f"✓ Successfully analyzed {call_identifier}")
                    return (call_key, parsed_output)


                except Exception as e:
                    if attempt < self.retry_attempts - 1:
                        # Calculate exponential backoff wait time
                        wait_time = self.retry_backoff_factor ** attempt
                        self._logger.warning(
                            f"Attempt {attempt + 1}/{self.retry_attempts} failed for {call_identifier}: {e}. "
                            f"Retrying in {wait_time:.1f}s..."
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        # All attempts failed
                        self._logger.error(
                            f"All {self.retry_attempts} attempts failed for {call_identifier}: {e}"
                        )
                        return (call_key, None)

        # This should never be reached, but just in case
        return (call_key, None)

    async def bot_evaluation(self):
        """
        bot_evaluation

        Overview

            Custom bot evaluation for call analysis that doesn't require rating column.

        Return

            A Pandas Dataframe with the Call Analysis results.

        """
        # Determine if we should group the data or process row by row
        should_group = self.group_analysis
        schema_col_present = (
            self.lookup_schema_column
            and isinstance(self.lookup_schema_column, str)
            and self.lookup_schema_column in self.data.columns
        )
        if should_group is None:
            # Auto-detect: check if we have duplicate description values
            unique_desc_values = self.data[self._desc_column].nunique()
            total_rows = len(self.data)
            should_group = unique_desc_values < total_rows

            if should_group:
                self._logger.info(
                    f"Auto-detected grouping: {total_rows} rows {unique_desc_values} unique {self._desc_column} values"
                )
            else:
                self._logger.info(
                    f"Auto-detected row-by-row mode: {total_rows} unique rows"
                )

        # Calculate rate limiting parameters
        min_request_interval = 60.0 / self.max_requests_per_minute if self.max_requests_per_minute > 0 else 0
        semaphore = asyncio.Semaphore(self.max_concurrent_calls)

        # Log concurrency configuration (limited to 1 due to google-genai v1.49.0+ bug)
        self._logger.info(
            f"Concurrency: max_concurrent={self.max_concurrent_calls}, "
            f"RPM={self.max_requests_per_minute}"
        )

        # Check if output_column already exists and has values (for skip_existing logic)
        existing_analysis = {}
        if self.skip_existing and self.output_column in self.data.columns:
            # Take first non-null value per key (schema + desc if available)
            def _key_from_row(row):
                if schema_col_present:
                    return (row[self.lookup_schema_column], row[self._desc_column])
                return row[self._desc_column]

            for _, row in self.data.iterrows():
                val = row[self.output_column]
                if pd.isna(val) or str(val).strip() == '':
                    continue
                key = _key_from_row(row)
                existing_analysis.setdefault(key, val)

            if existing_analysis:
                self._logger.info(
                    f"Found {len(existing_analysis)} existing analyses in dataframe. Will skip reprocessing these."
                )

        # Helper to build call key consistently
        def build_call_key(row):
            if schema_col_present:
                return (row[self.lookup_schema_column], row[self._desc_column])
            return row[self._desc_column]

        if should_group:
            # Group mode: combine transcripts with same description_column value
            group_keys = [self.lookup_schema_column, self._desc_column] if schema_col_present else [self._desc_column]
            grouped = self.data.groupby(group_keys)[self._eval_column].apply(list).reset_index()

            # Create tasks for calls that need processing
            tasks = []
            skipped_count = 0
            for _, row in grouped.iterrows():
                call_identifier = row[self._desc_column]
                call_key = build_call_key(row)
                transcripts = row[self._eval_column]

                # Skip if already has analysis
                if self.skip_existing and call_key in existing_analysis:
                    self._logger.debug(f"Skipping {call_identifier} - already has analysis")
                    skipped_count += 1
                    continue

                # Skip if all transcripts are empty
                valid_transcripts = [t for t in transcripts if t and not pd.isna(t)]
                if not valid_transcripts:
                    self._logger.warning(f"No valid transcripts for {call_identifier}, skipping")
                    continue

                # Create task with rate limiting
                task = self._process_with_rate_limit(
                    call_identifier,
                    valid_transcripts,
                    row,
                    semaphore,
                    min_request_interval,
                    call_key=call_key
                )
                tasks.append(task)

            if skipped_count > 0:
                self._logger.info(f"Skipped {skipped_count} calls with existing analysis")

            # Log processing information
            if tasks:
                self._logger.info(
                    f"Processing {len(tasks)} calls with max {self.max_concurrent_calls} concurrent requests, "
                    f"{self.max_requests_per_minute} RPM limit (interval: {min_request_interval:.2f}s)"
                )

                # Process all tasks concurrently (controlled by semaphore)
                import time
                start_time = time.time()
                results = await asyncio.gather(*tasks)
                elapsed_time = time.time() - start_time

                # Convert results to evaluation dict
                _evaluation = {call_id: result for call_id, result in results}

                # Log performance metrics
                successful_count = sum(1 for _, result in results if result is not None)
                failed_count = len(results) - successful_count
                self._logger.info(
                    f"Completed {len(results)} calls in {elapsed_time:.2f}s "
                    f"({len(results) / elapsed_time:.2f} calls/sec). "
                    f"Success: {successful_count}, Failed: {failed_count}"
                )
            else:
                _evaluation = {}
                self._logger.info("No new calls to process")

            # Merge existing analysis with new results
            # Existing analysis takes precedence (won't be overwritten)
            combined_evaluation = {**_evaluation, **existing_analysis}

            # For grouped mode, create result by taking first row of each group
            # and preserving columns specified in self.columns
            group_for_result = [self.lookup_schema_column, self._desc_column] if schema_col_present else [self._desc_column]
            result_df = self.data.groupby(group_for_result, as_index=False).first()

            # Keep only the columns we want to preserve
            columns_to_keep = [col for col in self.columns if col in result_df.columns]
            if schema_col_present and self.lookup_schema_column not in columns_to_keep:
                columns_to_keep.append(self.lookup_schema_column)
            if not columns_to_keep:
                columns_to_keep = result_df.columns.tolist()
            result_df = result_df[columns_to_keep]

            # Add the Call Analysis column (using combined evaluation with existing + new)
            result_df[self.output_column] = result_df.apply(
                lambda row: combined_evaluation.get(build_call_key(row)),
                axis=1
            )

        else:
            # Row-by-row mode: process each row individually
            # Create a copy of the original dataframe to preserve all columns
            result_df = self.data[self.columns].copy() if self.columns else self.data.copy()

            # Initialize analysis results with existing values if they exist
            if self.skip_existing and self.output_column in self.data.columns:
                # Start with existing values
                analysis_results = self.data[self.output_column].tolist()
            else:
                # Start with None for all rows
                analysis_results = [None] * len(self.data)

            # Create tasks for valid rows and track their original indices
            tasks = []
            task_indices = []  # Track which rows have tasks
            skipped_count = 0

            for idx, row in self.data.iterrows():
                call_identifier = row[self._desc_column]
                call_key = build_call_key(row)
                transcript = row[self._eval_column]

                # Skip if already has analysis
                if self.skip_existing and self.output_column in self.data.columns:
                    existing_value = row[self.output_column]
                    if not pd.isna(existing_value) and str(existing_value).strip() != '':
                        self._logger.debug(f"Skipping row {idx} ({call_identifier}) - already has analysis")
                        skipped_count += 1
                        continue
                if self.skip_existing and call_key in existing_analysis:
                    self._logger.debug(f"Skipping row {idx} ({call_identifier}) - found existing analysis in DB")
                    result_position = result_df.index.get_loc(idx)
                    analysis_results[result_position] = existing_analysis.get(call_key)
                    skipped_count += 1
                    continue

                # Skip if no content
                if pd.isna(transcript) or not transcript:
                    self._logger.warning(f"No content for row {idx} ({call_identifier}), skipping analysis")
                    continue

                # Create task with rate limiting
                task = self._process_with_rate_limit(
                    call_identifier,
                    [transcript],
                    row,
                    semaphore,
                    min_request_interval,
                    call_key=call_key
                )
                tasks.append(task)
                task_indices.append((idx, call_key))

            if skipped_count > 0:
                self._logger.info(f"Skipped {skipped_count} rows with existing analysis")

            # Log processing information
            if tasks:
                self._logger.info(
                    f"Processing {len(tasks)} rows with max {self.max_concurrent_calls} concurrent requests, "
                    f"{self.max_requests_per_minute} RPM limit (interval: {min_request_interval:.2f}s)"
                )

                # Process all tasks concurrently (controlled by semaphore)
                import time
                start_time = time.time()
                results = await asyncio.gather(*tasks)
                elapsed_time = time.time() - start_time

                # Map results back to DataFrame maintaining order
                for task_idx, (df_idx, call_key) in enumerate(task_indices):
                    # Get position in result_df (might be different from df_idx)
                    result_position = result_df.index.get_loc(df_idx)
                    _, result = results[task_idx]
                    analysis_results[result_position] = result

                # Log performance metrics
                successful_count = sum(1 for _, result in results if result is not None)
                failed_count = len(results) - successful_count
                self._logger.info(
                    f"Completed {len(tasks)} calls in {elapsed_time:.2f}s "
                    f"({len(tasks) / elapsed_time:.2f} calls/sec). "
                    f"Success: {successful_count}, Failed: {failed_count}"
                )
            else:
                self._logger.info("No new rows to process")

            # Add the analysis results as a new column
            result_df[self.output_column] = analysis_results

        # Clean up JSON formatting in the output column if present
        # Only clean strings, preserve dicts/lists that are already valid JSON objects
        if self.output_column in result_df.columns and not result_df[self.output_column].isna().all():
            import re
            def clean_json_formatting(x):
                if x is None or pd.isna(x):
                    return None
                # If it's already a dict or list, keep it as-is (valid JSONB)
                if isinstance(x, (dict, list)):
                    return x
                # Clean strings: strip markdown markers, then parse to dict/list
                if isinstance(x, str):
                    import json
                    cleaned = re.sub(r'^```json\s*|\s*```$', '', x, flags=re.MULTILINE).strip()
                    try:
                        return json.loads(cleaned)
                    except (json.JSONDecodeError, ValueError):
                        return cleaned
                return x
            result_df[self.output_column] = result_df[self.output_column].apply(clean_json_formatting)

        # Log summary with skip statistics
        total_analyzed = result_df[self.output_column].notna().sum()
        total_rows = len(result_df)

        if self.skip_existing and existing_analysis:
            skipped_existing = len(existing_analysis)
            newly_processed = total_analyzed - skipped_existing
            self._logger.info(
                f"Analysis complete: {total_analyzed}/{total_rows} rows with analysis. "
                f"(Skipped {skipped_existing} existing, Processed {newly_processed} new)"
            )
        else:
            self._logger.info(f"Analysis complete: {total_analyzed}/{total_rows} rows analyzed successfully")

        # Check if any data was successfully processed
        if total_analyzed == 0:
            raise DataNotFound(
                f"{self._bot_name}: No call analysis data was successfully processed. "
                f"All {total_rows} API calls failed or no valid content was found."
            )

        return result_df

    async def run(self):
        """
        Run the CallAnalysis component.

        Returns:
            pandas.DataFrame: DataFrame with call analysis results
        """
        self._result = await self.bot_evaluation()
        self._print_data_(self._result, 'CallAnalysis')
        return self._result

    async def close(self):
        """
        Close the CallAnalysis component.
        """
        pass
