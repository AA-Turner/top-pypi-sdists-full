import typing
from typing import Dict

import numpy as np
import pandas as pd
from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, FloatType, Row, StringType
from pyspark.sql.window import Window
from sklearn.metrics.pairwise import cosine_similarity

from seshat.data_class import DFrame, SPFrame
from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.vectorizer.base import SFrameVectorizer
from seshat.transformer.vectorizer.pivot import TokenPivotVectorizer


class CosineSimilarityVectorizer(SFrameVectorizer):
    """
    Calculates cosine similarity between vectors in an SFrame.

    This transformer takes a vectorized SFrame (typically from TokenPivotVectorizer)
    and computes the pairwise cosine similarity between the vectors. It can output
    a square similarity matrix or a long-format table of similarities, with optional
    thresholding and identification of top addresses by similarity sum.

    Parameters
    ----------
    square_shape : bool
        If True, output is a square matrix; otherwise, a long-format table.
    address_col : str
        Column name for addresses in the input vector SFrame.
    threshold : typing.Literal["by_count", "by_value", "none"]
        Method for thresholding similarity results.
    threshold_value : float | int
        The value used for thresholding based on the chosen method.
    find_top_address : bool
        If True, identifies top addresses based on the sum of their similarities.
    top_address_limit : int
        The number of top addresses to find if `find_top_address` is True.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "vector": configs.VECTOR_SF_KEY,
        "cosine_sim": configs.COSINE_SIM_SF_KEY,
        "top_address": configs.TOP_ADDRESS_SF_KEY,
        "exclusion": configs.EXCLUSION_SF_KEY,
    }

    def __init__(
        self,
        square_shape: bool = True,
        address_col: str = configs.ADDRESS_COL,
        address_1_col: str = "address_1",
        address_2_col: str = "address_2",
        cosine_col: str = "cosine",
        exclusion_token_col: str = configs.CONTRACT_ADDRESS_COL,
        threshold_value: float | int = 100,
        threshold: typing.Literal["by_count", "by_value", "none"] = "none",
        find_top_address: bool = False,
        top_address_limit: int = 100,
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.square_shape = square_shape
        self.address_col = address_col
        self.address_1_col = address_1_col
        self.address_2_col = address_2_col
        self.cosine_col = cosine_col
        self.exclusion_token_col = exclusion_token_col
        self.threshold = threshold
        self.threshold_value = threshold_value
        self.find_top_address = find_top_address
        self.top_address_limit = top_address_limit

    def vectorize_df(
        self,
        default: DataFrame = None,
        vector: DataFrame = None,
        exclusion: DataFrame = None,
        *args,
        **kwargs,
    ) -> Dict[str, DataFrame]:
        if vector is None:
            sf_input = DFrame.from_raw(default).make_group(self.default_sf_key)
            sf_output = TokenPivotVectorizer(result_address_col=self.address_col)(
                sf_input
            )
            vector = sf_output.get(configs.VECTOR_SF_KEY).to_raw()
        if exclusion is not None:
            vector = vector[
                ~vector[self.address_col].isin(exclusion[self.exclusion_token_col])
            ]

        attributes = vector.iloc[:, 1:].values
        all_addresses = vector[self.address_col].values
        cosine = cosine_similarity(attributes)
        cosine = pd.DataFrame(columns=all_addresses, index=all_addresses, data=cosine)
        return_kwargs = {"default": default, "cosine_sim": cosine}

        if self.find_top_address:
            top_series = cosine.sum(axis=1).nlargest(self.top_address_limit)
            top_address = pd.DataFrame(
                {self.address_col: top_series.index, self.cosine_col: top_series.values}
            )
            return_kwargs["top_address"] = top_address

        if not self.square_shape:
            mask = np.triu(np.ones(cosine.shape[0])).astype(bool)
            cosine = cosine.where(~mask, 0)
            cosine = cosine.stack().reset_index()
            cosine.columns = [self.address_1_col, self.address_2_col, self.cosine_col]
            cosine = cosine.rename(columns={"index": self.address_2_col})
            cosine = cosine[cosine[self.cosine_col] != 0]
            cosine.reset_index(drop=True, inplace=True)

            if self.threshold == "by_value":
                cosine = cosine[cosine[self.cosine_col] >= self.threshold_value]
            elif self.threshold == "by_count":
                left = cosine
                right = cosine.rename(
                    columns={
                        self.address_1_col: "temp",
                        self.address_2_col: self.address_1_col,
                    }
                ).rename(columns={"temp": self.address_2_col})
                agg_cosine = pd.concat([left, right])
                del left
                del right

                agg_cosine = agg_cosine.sort_values("cosine", ascending=False)
                agg_cosine = agg_cosine.groupby(self.address_1_col).head(
                    self.threshold_value
                )
                agg_cosine[[self.address_1_col, self.address_2_col]] = pd.DataFrame(
                    np.sort(
                        agg_cosine[[self.address_1_col, self.address_2_col]], axis=1
                    ),
                    index=agg_cosine.index,
                )
                cosine = agg_cosine.drop_duplicates().reset_index(drop=True)
            return_kwargs["cosine_sim"] = cosine

        return return_kwargs

    def vectorize_spf(
        self,
        default: PySparkDataFrame = None,
        vector: PySparkDataFrame = None,
        exclusion: PySparkDataFrame = None,
        *args,
        **kwargs,
    ):
        if vector is None:
            sf_input = SPFrame.from_raw(default).make_group(self.default_sf_key)
            sf_output = TokenPivotVectorizer(result_address_col=self.address_col)(
                sf_input
            )
            vector = sf_output.get(configs.VECTOR_SF_KEY).to_raw()
        attributes = np.array(vector.select(vector.columns[1:]).collect())
        all_address = [
            row[self.address_col] for row in vector.select(self.address_col).collect()
        ]

        cosine = cosine_similarity(attributes)
        schema = StructType(
            [StructField(str(address), FloatType(), True) for address in all_address],
        )
        cosine = SPFrame.get_spark().createDataFrame(cosine, schema=schema)
        return_kwargs = {"default": default, "vector": vector, "cosine_sim": cosine}
        if self.find_top_address:
            top_address = cosine.withColumn(
                self.cosine_col, sum([F.col(c) for c in cosine.columns])
            )
            top_address = top_address.sort(self.cosine_col, ascending=False)
            window = Window.orderBy(self.cosine_col)
            top_address = top_address.withColumn(
                "index", F.row_number().over(window) - 1
            )
            cols = top_address.columns

            def get_address(index):
                return str(cols[index])

            top_address = top_address.withColumn(
                self.address_col, F.udf(get_address, StringType())(F.col("index"))
            )

            to_drop = set(cols) - {self.address_col, self.cosine_col}
            top_address = top_address.drop(*to_drop)
            top_address = top_address.limit(self.top_address_limit)

            return_kwargs["top_address"] = top_address

        if not self.square_shape:
            cosine = cosine.withColumn(
                "row_id",
                F.row_number().over(Window.orderBy(F.monotonically_increasing_id()))
                - 1,
            )
            for i, col_name in enumerate(cosine.columns):
                cosine = cosine.withColumn(
                    col_name,
                    F.when(F.col("row_id") == F.lit(i), F.lit(0)).otherwise(
                        F.col(col_name)
                    ),
                )
            cosine = cosine.drop("row_id")

            addresses_rdd = (
                SPFrame.get_spark()
                .sparkContext.parallelize(all_address)
                .map(lambda x: Row(address=x))
            )

            address = SPFrame.get_spark().createDataFrame(addresses_rdd)
            address = address.withColumn("index", F.monotonically_increasing_id())
            cosine = cosine.withColumn("index", F.monotonically_increasing_id())
            w = Window.orderBy("index")
            address = address.withColumn("index", F.row_number().over(w))
            cosine = cosine.withColumn("index", F.row_number().over(w))
            cosine = cosine.join(address, "index", "left").drop("index")

            unpivot_cols = cosine.columns
            unpivot_cols.remove(self.address_col)
            cosine = cosine.melt(
                self.address_col,
                unpivot_cols,
                self.address_2_col,
                self.cosine_col,
            )
            cosine = cosine.withColumnRenamed(self.address_col, self.address_1_col)

            cosine = cosine.withColumn(
                "min_address",
                F.least(F.col(self.address_1_col), F.col(self.address_2_col)),
            ).withColumn(
                "max_address",
                F.greatest(F.col(self.address_1_col), F.col(self.address_2_col)),
            )

            cosine = cosine.dropDuplicates(
                ["min_address", "max_address", self.cosine_col]
            )
            cosine = cosine.drop("min_address", "max_address")
            cosine = cosine.filter(F.col(self.cosine_col) != 0)

            if self.threshold == "by_count":
                left = cosine
                right = cosine.selectExpr(
                    f"{self.address_2_col} as {self.address_1_col}",
                    f"{self.address_1_col} as {self.address_2_col}",
                    self.cosine_col,
                )

                agg_cosine = left.unionByName(right)

                window = Window.partitionBy(self.address_1_col).orderBy(
                    F.col(self.cosine_col).desc()
                )
                agg_cosine = agg_cosine.withColumn(
                    "row_num", F.row_number().over(window)
                )
                agg_cosine = agg_cosine.filter(
                    F.col("row_num") <= self.threshold_value
                ).drop("row_num")

                agg_cosine = (
                    agg_cosine.withColumn(
                        "address_min",
                        F.array_sort(F.array(self.address_1_col, self.address_2_col))[
                            0
                        ],
                    )
                    .withColumn(
                        "address_max",
                        F.array_sort(F.array(self.address_1_col, self.address_2_col))[
                            1
                        ],
                    )
                    .drop(self.address_1_col, self.address_2_col)
                )

                agg_cosine = agg_cosine.withColumnRenamed(
                    "address_min", self.address_1_col
                )
                agg_cosine = agg_cosine.withColumnRenamed(
                    "address_max", self.address_2_col
                )

                cosine = agg_cosine.dropDuplicates().orderBy(
                    self.cosine_col, ascending=False
                )
            elif self.threshold == "by_value":
                cosine = cosine.filter(F.col(self.cosine_col) >= self.threshold_value)

            return_kwargs["cosine_sim"] = cosine
        return return_kwargs


class CosineSimilarityVectorizerStory(BaseTransformerStory):
    transformer = CosineSimilarityVectorizer
    use_cases = [
        "To calculate the pairwise cosine similarity between vectors, typically generated by a vectorization transformer like TokenPivotVectorizer.",
        "To identify addresses with high similarity based on their vector representations.",
        "To filter similarity results based on value or count thresholds.",
    ]
    logic_overview = (
        "Takes a vectorized SFrame (or generates one if not provided) and computes the cosine similarity "
        "matrix between the vectors. It can handle both pandas and PySpark DataFrames. "
        "The output can be a square similarity matrix or a long-format table. "
        "Optional features include filtering by similarity threshold and identifying top addresses by similarity sum."
    )
    steps = [
        "If a vector SFrame is not provided, generate one using TokenPivotVectorizer.",
        "If an exclusion SFrame is provided, filter out addresses present in the exclusion list from the vector SFrame.",
        "Extract the numerical attributes from the vector SFrame.",
        "Calculate the pairwise cosine similarity matrix using the extracted attributes.",
        "Convert the similarity matrix into an SFrame.",
        "If `find_top_address` is True, calculate the sum of similarities for each address and identify the top addresses based on `top_address_limit`.",
        "If `square_shape` is False, convert the square similarity matrix into a long-format table (address_1, address_2, cosine).",
        "If a `threshold` is specified, filter the long-format table based on the `threshold_value` (either by value or by count of related addresses).",
        "Return the original default SFrame (if available), the vector SFrame (if generated), the cosine similarity SFrame, and optionally the top addresses SFrame.",
    ]
    tags = ["vectorizer", "similarity", "single-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "CosineSimilarityVectorizerDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
