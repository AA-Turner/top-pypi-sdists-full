import logging
from typing import Callable, Dict, Optional

from seshat.data_class import SFrame
from seshat.evaluation.base import Evaluation
from seshat.profiler import ProfileConfig
from seshat.profiler.base import profiler
from seshat.source import Source
from seshat.source.saver import Saver
from seshat.transformer.base import Transformer
from seshat.transformer.pipeline import Pipeline
from seshat.transformer.splitter import Splitter


class FeatureView:
    """
    Manages the retrieval, processing, and optional storage of feature data
    for machine learning models, accommodating both real-time inference and
    batch training workflows. This class abstracts the complexity of handling
    different data sources and processing pipelines depending on whether
    it is operating in online or offline mode.

    Parameters
    ----------
    online : bool
        A flag to indicate the mode of operation. If `True`, the feature view operates
        in online mode for inference. If `False`, it operates in offline mode for training.
    offline_pipeline : Callable
        The processing pipeline used when the feature view is in offline mode.
        It is responsible for transforming the data retrieved from the offline source.
    online_pipeline : Callable
        The processing pipeline used when the feature view is in online mode
    offline_source : Source
        The data source that provides data in offline mode.
    online_source : Source
        The data source that provides data in online mode.
    saver : Saver, optional
        An optional component responsible for saving the processed data during training
        Required only in offline mode.
    on_save_finished : Transformer, Optional
        A Transformer to be called after the save operation completes.
    Examples
    --------
    Define feature view:
    >>> class TokenRecommendation(FeatureView):
    ...    online = False
    ...    name = "Token Recommendation with Local csv as Source and save result to database"
    ...    offline_source = LocalSource(path="./../../data.csv")
    ...    offline_pipeline = Pipeline(
    ...        [
    ...            LowTransactionTrimmer(min_transaction_num=20),
    ...            FeatureTrimmer(),
    ...            ContractTrimmer(get_popular_contracts, contract_list_kwargs={"limit": 100}),
    ...        ]
    ...    )
    ...    saver = SQLDBSaver(
    ...        url=os.getenv("DB_URL"),
    ...        save_configs=[
    ...            SaveConfig(
    ...                sf_key="default",
    ...                table="etherium_record",
    ...                ensure_exists=True,
    ...            ),
    ...        ],
    ...    )

    Use defined feature view:
    >>> recommender = TokenRecommendation()
    ...     view = recommender()
    """

    name: str
    description: str
    online_source: Source = None
    offline_source: Source = None
    online_pipeline: Pipeline = None
    offline_pipeline: Pipeline = None
    splitter: Splitter
    split_at_start: bool = False
    online: bool = False
    data: SFrame
    split_data: Dict[str, SFrame] = None
    saver: Saver = None
    profile_config = ProfileConfig(logging.INFO, default_tracking=True)
    evaluation: Evaluation
    on_save_finished: Optional[Transformer] = None

    def __call__(self, *args, **kwargs):
        source = self._get_source()
        pipeline = self._get_pipeline()

        profiler.setup(config=self.profile_config)
        with profiler:
            self.data = source(*args, **kwargs)
            if self.split_at_start:
                self._split(*args, **kwargs)
                self.run_pipline_on_split_data(pipeline, *args, **kwargs)
            else:
                self.data = pipeline(self.data, *args, **kwargs)

        return self

    def calculate_complexity(self):
        complexity = 0
        if self.saver is not None:
            complexity += self.saver.calculate_complexity()

        if self.online:
            return (
                complexity
                + self.online_source.calculate_complexity()
                + self.online_pipeline.calculate_complexity()
            )

        return (
            complexity
            + self.offline_source.calculate_complexity()
            + self.offline_pipeline.calculate_complexity()
        )

    def run_pipline_on_split_data(self, pipeline, *args, **kwargs):
        for k, data in self.split_data.items():
            self.split_data[k] = pipeline(data, *args, **kwargs)

    def train_data(self) -> SFrame:
        if not self.split_data:
            self._split()
        return self.split_data[self.splitter.train_key]

    def test_data(self) -> SFrame:
        if not self.split_data:
            self._split()
        return self.split_data[self.splitter.test_key]

    def validate_data(self) -> SFrame:
        if not self.split_data:
            self._split()
        return self.split_data[2]  # TODO: fix this.

    def save(self):
        if self.saver is None:
            return
        with profiler:
            (
                self.saver(self.train_data())
                if hasattr(self, "splitter")
                else self.saver(self.data)
            )
        if self.on_save_finished is not None:
            self.on_save_finished(self.data)

    def _split(self, *args, **kwargs):
        self.split_data = self.splitter(self.data, *args, **kwargs)

    def evaluate(self, model_func: Callable = None, **prediction_kwargs):
        if not hasattr(self, "evaluation"):
            return
        return self.evaluation(self.test_data(), model_func, **prediction_kwargs)

    def _get_source(self):
        return self.online_source if self.online else self.offline_source

    def _get_pipeline(self):
        return self.online_pipeline if self.online else self.offline_pipeline
