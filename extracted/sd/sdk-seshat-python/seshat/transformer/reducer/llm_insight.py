import logging
import math
from typing import Callable, List, Dict, Any, TypeAlias

import pandas as pd
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage
from pandas import DataFrame
from pandas._typing import MergeHow
from pyspark import Row
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.data_class import SPFrame
from seshat.general.transformer_story.base import (
    TransformerScenario,
    BaseTransformerStory,
)
from seshat.profiler import track, ProfileConfig
from seshat.profiler.base import profiler, Profiler
from seshat.transformer.reducer import SFrameReducer
from seshat.utils.clean_json import JSONCleaner

InputType: TypeAlias = List[Dict[str, Any]]
OutputType: TypeAlias = List[Dict[str, Any]]
ProcessResponseFn: TypeAlias = Callable[[InputType, InputType], OutputType]
GetExtraCtxFn: TypeAlias = Callable[[List[Dict[str, Any]]], Dict[str, Any]]


def math_nan_to_none(row):
    d = row.asDict()
    for key, value in d.items():
        if value is None:
            continue
        if isinstance(value, float) and math.isnan(value):
            d[key] = None
    return Row(**d)


class LLMInsightExtractor(SFrameReducer):
    """
    A transformer that extracts insights from data using Large Language Models (LLMs).

    This class uses LLMs to analyze data and extract insights. Supports batch and one-shot processing, pandas and
    PySpark DataFrames, grouping, and custom response processing.

    Parameters
    ----------
    get_llm_client : () ->  BaseChatModel
        The LLM client used to generate insights.
    template_prompt : str
        The template prompt to send to the LLM. Should include placeholders for data.
    id_column : str, optional
        The column name to use as an identifier when expanding results. Required if expand_on_id is True.
    join_cols : list[str], optional
        The columns to use for joining the extracted insights back to the original DataFrame. If not provided,
         defaults to [id_column].
    template_context : str, optional
        The system context to provide to the LLM. Defaults to a basic data scientist role.
    llm_input_columns : List[str], optional
        The columns to include in the data sent to the LLM. If None, all columns are included.
    process_llm_json_response_fn : ProcessResponseFn, optional
        Function to process the JSON response from the LLM.
    get_extra_context : ProcessBatchFn, optional
        Function to process data before sending to the LLM. Receives the current data and should return a dict to
        update format_args.
    process_llm_response : Callable, optional
        Function to process the raw LLM response before JSON parsing.
    retry : int, default=3
        Number of times to retry LLM calls on failure.
    batch_mode : bool, default=True
        Whether to process data in batches or all at once.
    chunk_size : int, optional, default=100
        The size of data batches when batch_mode is True.
    group_keys : dict, optional
        Keys to use for grouping data.
    group_by_columns : list[str], optional
        Columns to group data by before processing.
    groupby_inject_key : str, optional
        Key to inject group name into the template prompt. Requires group_by_columns.
    expand_on_id : bool, default=False
        Whether to expand results based on ID column. Requires id_column.
    inject_keys : dict[str, str], optional
        Additional keys to inject into the template prompt.
    merge_result : bool, default=True
        Whether to merge the extracted insights back to the original DataFrame.

    Raises
    ------
    ValueError
        If groupby_inject_key is set but group_by_columns is not set,
        or if expand_on_id is True but id_column is not set.

    Examples
    --------
    Basic usage with a pandas DataFrame in batch mode::

        from langchain_openai import ChatOpenAI
        from seshat.transformer.reducer import LLMInsightExtractor

        # Prepare your DataFrame ``df`` here

        extractor = LLMInsightExtractor(
            llm_client=ChatOpenAI(model="gpt-3.5-turbo"),
            template_prompt="Please analyse the following dataset and respond with a JSON list of insights
            .\n{inject_data}",
            llm_input_columns=["question", "answer"],
        )

        # ``reduce`` always returns a dict keyed by ``group_keys`` (default is "default")
        insights_df = extractor.reduce(df)["default"]

    Grouped processing with ``group_by_columns`` and dynamic prompt injection::

        extractor_grouped = LLMInsightExtractor(
            llm_client=ChatOpenAI(model="gpt-4o"),
            template_prompt="The following data belongs to the group: {country}. {inject_data}",
            group_by_columns=["country"],
            groupby_inject_key="country",
        )

        # Each country is processed separately and concatenated back together
        insights_df = extractor_grouped.reduce(df)["default"]

    One-shot processing (``batch_mode=False``)::

        extractor_one_shot = LLMInsightExtractor(
            llm_client=ChatOpenAI(model="gpt-3.5-turbo"),
            template_prompt="Summarise this dataset: {inject_data}",
            batch_mode=False,
        )

        insights_df = extractor_one_shot.reduce(df)["default"]

    Using custom response post-processing::

        def post_process_llm_json(json_response: list[dict]):
            # Custom cleaning / validation
            return pd.DataFrame(json_response)

        extractor_custom = LLMInsightExtractor(
            llm_client=ChatOpenAI(model="gpt-3.5-turbo"),
            template_prompt="{inject_data}",
            process_llm_json_response_fn=post_process_llm_json,
        )
        insights_df = extractor_custom.reduce(df)["default"]
    """

    def __init__(
        self,
        get_llm_client: Callable[[], "BaseChatModel"],
        template_prompt: str,
        id_column: str = None,
        join_cols: list[str] = None,
        template_context: str = None,
        llm_input_columns: List[str] = None,
        process_llm_json_response_fn: ProcessResponseFn = None,
        get_extra_context: GetExtraCtxFn = None,
        process_llm_response: Callable = None,
        retry: int = 3,
        llm_result_cleaner: Callable = JSONCleaner().clean,
        batch_mode: bool = True,
        chunk_size: int | None = 100,
        group_keys=None,
        group_by_columns: list[str] = None,
        groupby_inject_key: str = None,
        expand_on_id: bool = False,
        inject_keys: dict[str, str] = None,
        merge_result: bool = True,
        merge_how: MergeHow = "left",
    ):

        super().__init__(group_keys)
        self.chunk_size = chunk_size
        self.get_llm_client = get_llm_client
        self.template_prompt = template_prompt
        self.process_llm_json_response_fn = process_llm_json_response_fn
        self.get_extra_context = get_extra_context
        self.retry = retry
        self.batch_mode = batch_mode

        self.cleaner = llm_result_cleaner

        self.llm_input_columns = llm_input_columns
        self.template_context = (
            template_context
            or """
            You are a data scientist.
            Your task is to analyze and provide insights about the given dataset.
        """
        )
        self.merge_result = merge_result
        self.merge_how = merge_how

        self.group_by_columns = group_by_columns
        self.id_column = id_column
        self.join_cols = join_cols or [self.id_column]
        self.expand_on_id = expand_on_id
        self.static_injected_data = inject_keys
        self.process_llm_response = process_llm_response
        self.groupby_inject_key = groupby_inject_key

        if self.groupby_inject_key and not self.group_by_columns:
            raise ValueError(
                "group_by_columns must be set if groupby_inject_key is set"
            )

        if self.expand_on_id and not self.id_column:
            raise ValueError("id_column must be set if expand_on_id is True")

    @track
    def ask_llm(self, prompt: str):
        """
        Send a prompt to the LLM and process the response.

        Parameters
        ----------
        prompt : str
            The prompt to send to the LLM.

        Returns
        -------
        list[dict] or None
            A list of dictionaries containing the processed LLM response, or None if all retry attempts fail.
        """
        retry_count = 0
        llm_client = self.get_llm_client()
        while retry_count < self.retry:
            try:
                messages = [
                    SystemMessage(content=self.template_context.strip()),
                    HumanMessage(content=prompt),
                ]

                llm_response = llm_client.invoke(messages)

                tokens_in = tokens_out = ""
                if hasattr(llm_client, "get_num_tokens"):
                    try:
                        prompt_for_count = "\n".join(
                            f"{m.type}:{m.content}" for m in messages
                        )
                        tokens_in = llm_client.get_num_tokens(prompt_for_count)
                        tokens_out = llm_client.get_num_tokens(llm_response.content)
                    except Exception:
                        pass

                profiler.log(
                    "info",
                    msg="llm_token_usage",
                    method=self.ask_llm.__wrapped__,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                )

                if self.process_llm_response:
                    return self.process_llm_response(llm_response)
                response_json = self.cleaner(llm_response.content)

                assert isinstance(
                    response_json, list
                ), f"{response_json} is not a valid json."
                assert all(
                    isinstance(item, dict) for item in response_json
                ), f"{response_json} is not a valid json."

                return response_json

            except Exception as e:
                retry_count += 1
                profiler.log(
                    "error",
                    msg="Response cannot be proceeded",
                    method=self.ask_llm.__wrapped__,
                    error=str(e),
                )

        return None

    @track
    def extract_insight_batch(self, data: List[List[Dict[str, Any]]], **kwargs):
        """
        Extract insights for batches of data.

        Parameters
        ----------
        data : List[List[dict]]
            List of batches (each batch is a list of dicts).

        Returns
        -------
        list[dict]
            List of dicts with extracted insights.
        """
        batch_result: list[dict[str, Any]] = []
        for batch_data in data:
            prompt_kwargs = (
                self.get_extra_context(batch_result, batch_data) if self.get_extra_context else {}
            )
            res = self.perform_extract(batch_data, prompt_kwargs, **kwargs)
            if res:
                batch_result += res
        return batch_result

    def extract_insight_one_shot(
        self, data: List[Dict[str, Any]], **kwargs
    ) -> List[Dict[str, Any]]:
        prompt_kwargs = self.get_extra_context(data) if self.get_extra_context else {}
        return self.perform_extract(data, prompt_kwargs, **kwargs)

    @track
    def perform_extract(
        self, data: List[Dict[str, Any]], prompt_kwargs=None, **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Extract insights for a single batch or all data.

        Parameters
        ----------
        data : List[dict]
            List of dicts (input records).
        prompt_kwargs : dict, optional
            Extra prompt arguments.

        Returns
        -------
        list[dict]
            List of dicts with extracted insights.
        """
        if not prompt_kwargs:
            prompt_kwargs = {}

        prompt_kwargs |= {"inject_data": str(data)}
        prompt_kwargs.update(self.static_injected_data or {})
        if kwargs.get("group_name") and self.groupby_inject_key:
            prompt_kwargs[self.groupby_inject_key] = kwargs.get("group_name")

        prompt = self.template_prompt.format(**prompt_kwargs)
        llm_result = self.ask_llm(prompt=prompt)

        if llm_result and self.process_llm_json_response_fn:
            return self.process_llm_json_response_fn(data, llm_result)

        return llm_result

    def _find_extract_inputs(self, default, groups, inputs):
        """
        Loop over all groups and keep the all
        inputs of extract function to in a list
        """
        for group in groups:
            if group is None:
                group_df = default
            else:
                mask = True
                for col, val in group.items():
                    mask &= default[col] == val
                group_df = default[mask]

            llm_input_columns = self.llm_input_columns or group_df.columns
            if set(llm_input_columns) - set(group_df.columns):
                continue

            selected = group_df[[*llm_input_columns]]

            if (
                self.id_column in selected.columns
                and selected[self.id_column].isnull().all()
            ):
                continue

            # If batch mode, create chunks otherwise use whole data
            if self.batch_mode:
                data = [
                    selected.iloc[i : i + self.chunk_size].to_dict("records")
                    for i in range(0, len(selected), self.chunk_size)
                ]
            else:
                data = selected.to_dict("records")
            group_name = (
                "-".join([group.get(c) for c in self.group_by_columns]) if group else ""
            )
            inputs.append({"group_name": group_name, "data": data})

    def reduce_df(self, default: DataFrame, **kwargs) -> Dict[str, DataFrame]:
        # Find the groups if group_by_columns set
        if default.empty:
            return {"default": default}

        groups = (
            default[[*self.group_by_columns]].drop_duplicates().to_dict("records")
            if self.group_by_columns
            else [None]
        )

        # Find the inputs of extract function
        inputs = []
        self._find_extract_inputs(default, groups, inputs)

        extract_func = (
            self.extract_insight_batch
            if self.batch_mode
            else self.extract_insight_one_shot
        )
        results = []
        for d in inputs:
            results.extend(extract_func(**d))
        results = pd.DataFrame(results)

        if self.expand_on_id and not results.empty:
            redundant_cols = [
                col
                for col in results.columns
                if col in default.columns
                and col != self.id_column
                and col not in set(self.join_cols)
            ]
            results = (
                results.explode(self.id_column)
                .set_index(self.id_column)
                .drop(columns=redundant_cols, axis=1)
            )
        if not self.merge_result:
            return {"default": results.drop_duplicates()}
        if not results.empty:
            default = (
                pd.merge(default, results, on=self.join_cols, how=self.merge_how)
                .reset_index()
                .drop_duplicates()
            )
        elif self.merge_how in [
            "right",
            "inner",
        ]:  # there are no rows in results, so the output will be an empty dataframe.
            return {"default": results}

        return {"default": default}

    def reduce_spf(
        self, default: PySparkDataFrame, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        # TODO: the cons of using pyspark in this transformer is just to
        #       to call LLM parallel by each executor. Is this worth?

        def process_group(rows):
            rows_list = list(rows)
            if not rows_list:
                return iter([])

            Profiler.setup(ProfileConfig(logging.INFO, default_tracking=True))
            # Convert list of Rows to Pandas DataFrame
            df = pd.DataFrame([row.asDict() for row in rows_list])
            result_df = self.reduce_df(df)["default"]
            result_rows = [Row(**row) for row in result_df.to_dict(orient="records")]

            return iter(result_rows)

        if self.group_by_columns:
            default = default.repartition(*self.group_by_columns)

        # To avoid calling process group again, cache rdd and
        # use count() to trigger running process_group and cache the result.
        rdd = default.rdd.mapPartitions(process_group)
        # Because pandas result maybe contains math nan values and
        # these values are not valid for spark
        rdd = rdd.map(math_nan_to_none)
        rdd.cache()
        rdd.count()

        default = SPFrame.get_spark().createDataFrame(rdd)
        default.cache()
        return {"default": default}

    def calculate_complexity(self):
        return 80


class LLMInsightExtractorStory(BaseTransformerStory):
    transformer = LLMInsightExtractor
    use_cases = [
        "To extract and categorize insights from textual data using a Large Language Model (LLM).",
        "To enrich existing datasets by adding LLM-generated insights or classifications to each record.",
        "To process large volumes of data by sending it to an LLM in manageable batches for analysis.",
    ]
    logic_overview = (
        "This transformer leverages an LLM to analyze input SFrame data and generate structured insights. "
        "It supports both one-shot and batch processing modes, handling LLM communication, response cleaning, "
        "and integration of the generated insights back into the original SFrame. It expects the LLM to return "
        "a JSON list of dictionaries, each containing an insight key, its description, and associated data IDs."
    )
    steps = [
        (
            "Initializes with an LLM client, a prompt template, and configuration for batching, "
            "columns to inject, and ID column."
        ),
        (
            "If specific `cols` are provided, the input SFrame is filtered to include only these columns "
            "and the `id_col` for LLM processing."
        ),
        "Based on the `batch_mode` setting:",
        (
            "  - If `batch_mode` is True: The SFrame data is divided into chunks. For each chunk, "
            "the `prompt` is formatted with the current batch data and any previously found insights "
            "(to maintain context). The formatted prompt is then sent to the LLM."
        ),
        (
            "  - If `batch_mode` is False: The entire filtered SFrame data is formatted into the `prompt` "
            "and sent to the LLM in a single request."
        ),
        (
            "The LLM's response is processed: it's cleaned (JSON parsing) and validated to ensure it's "
            "a list of dictionaries. Retries are attempted if the response is invalid or an error occurs."
        ),
        (
            "Extracted insights (identified by `insight_key` and its corresponding description) are mapped "
            "back to the original data using the `id_col`."
        ),
        (
            "The original input SFrame is then merged with the new columns containing the generated insights "
            "and their descriptions."
        ),
    ]
    tags = ["reducer", "single-sf-operator"]

    def get_scenarios(self):
        from test.transformer.reducer.test_llm_insight_extractor_comprehensive import (
            TestIntegrationWithParentClasses,
        )

        return TransformerScenario.from_testcase(
            TestIntegrationWithParentClasses, transformer=self.transformer
        )
