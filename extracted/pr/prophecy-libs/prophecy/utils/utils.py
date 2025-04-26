import inspect
import json
import time
from typing import Optional, Any
import traceback
from py4j.protocol import Py4JError, Py4JJavaError
try:
    from pyspark.errors import PySparkAttributeError
except:
    # pyspark.errors was introduced in spark 3.4
    # PySparkAttributeError was introduced in spark 3.4.1.
    # Before that, we would see AttributeError being thrown
    PySparkAttributeError = AttributeError
    pass
from pyspark.sql import *

from prophecy.utils.monitoring_utils import capture_streams, monkey_patch_print, \
    revert_monkey_patching

try:
    # For Spark versions before 3.4.0
    from pyspark.sql.utils import CapturedException
except ImportError:
    # For Spark version 3.4.0 and later
    from pyspark.errors.exceptions.captured import CapturedException

from prophecy.libs.utils import *


class TaskState:
    LAUNCHING = "LAUNCHING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    FINISHED = "FINISHED"


class ProphecyDataFrame:
    def __init__(self, df: DataFrame, spark: SparkSession):
        self.jvm = spark.sparkContext._jvm
        self.spark = spark
        self.sqlContext = SQLContext(spark.sparkContext, sparkSession=spark)

        if type(df) == DataFrame:
            try:  # for backward compatibility
                self.extended_dataframe = (
                    self.jvm.org.apache.spark.sql.ProphecyDataFrame.extendedDataFrame(
                        df._jdf
                    )
                )
            except TypeError:
                self.extended_dataframe = (
                    self.jvm.io.prophecy.libs.package.ExtendedDataFrameGlobal(df._jdf)
                )
            self.dataframe = df
        else:
            try:
                self.extended_dataframe = (
                    self.jvm.org.apache.spark.sql.ProphecyDataFrame.extendedDataFrame(
                        df._jdf
                    )
                )
            except TypeError:
                self.extended_dataframe = (
                    self.jvm.io.prophecy.libs.package.ExtendedDataFrameGlobal(df._jdf)
                )
            self.dataframe = DataFrame(df, self.sqlContext)

    def interim(
            self,
            subgraph,
            component,
            port,
            subPath,
            numRows,
            interimOutput,
            detailedStats=False,
            run_id: Optional[str] = None,
            config: Optional[str] = None
    ) -> DataFrame:
        result = self.extended_dataframe.interim(
            subgraph, component, port, subPath, numRows, interimOutput, detailedStats, run_id, config
        )
        return DataFrame(result, self.sqlContext)

    # Ab Initio extensions to Prophecy DataFrame
    def collectDataFrameColumnsToApplyFilter(
            self, columnList, filterSourceDataFrame
    ) -> DataFrame:
        result = self.extended_dataframe.collectDataFrameColumnsToApplyFilter(
            createScalaList(self.spark, columnList), filterSourceDataFrame._jdf
        )
        return DataFrame(result, self.sqlContext)

    def normalize(
            self,
            lengthExpression,
            finishedExpression,
            finishedCondition,
            alias,
            colsToSelect,
            tempWindowExpr,
            lengthRelatedGlobalExpressions={},
            normalizeRelatedGlobalExpressions={},
            sparkSession=None,
    ) -> DataFrame:
        result = self.extended_dataframe.normalize(
            createScalaColumnOption(self.spark, lengthExpression),
            createScalaColumnOption(self.spark, finishedExpression),
            createScalaColumnOption(self.spark, finishedCondition),
            alias,
            createScalaColumnList(self.spark, colsToSelect),
            createScalaColumnMap(self.spark, tempWindowExpr),
            createScalaColumnMap(self.spark, lengthRelatedGlobalExpressions),
            createScalaColumnMap(self.spark, normalizeRelatedGlobalExpressions),
            createScalaOption(self.spark, sparkSession),
        )
        return DataFrame(result, self.sqlContext)

    def denormalizeSorted(
            self,
            groupByColumns,
            orderByColumns,
            denormalizeRecordExpression,
            finalizeExpressionMap,
            inputFilter,
            outputFilter,
            denormColumnName,
            countColumnName="count",
    ) -> DataFrame:
        result = self.extended_dataframe.denormalizeSorted(
            self,
            createScalaColumnList(self.spark, groupByColumns),
            createScalaColumnList(self.spark, orderByColumns),
            denormalizeRecordExpression,
            createScalaColumnMap(self.spark, finalizeExpressionMap),
            createScalaColumnOption(self.spark, inputFilter),
            createScalaColumnOption(self.spark, outputFilter),
            denormColumnName,
            countColumnName,
        )
        return DataFrame(result, self.sqlContext)

    def readSeparatedValues(
            self, inputColumn, outputSchemaColumns, recordSeparator, fieldSeparator
    ) -> DataFrame:
        result = self.extended_dataframe.readSeparatedValues(
            inputColumn._jc,
            createScalaList(self.spark, outputSchemaColumns),
            recordSeparator,
            fieldSeparator,
        )
        return DataFrame(result, self.sqlContext)

    def fuzzyDedup(
            self, dedupColumnName, threshold, sparkSession, algorithm
    ) -> DataFrame:
        result = self.extended_dataframe.fuzzyDedup(
            dedupColumnName,
            threshold,
            sparkSession._jsparkSession,
            algorithm,
        )
        return DataFrame(result, self.sqlContext)

    def fuzzyPurgeMode(
            self, recordId, threshold, matchFields, includeSimilarityScore
    ) -> DataFrame:
        result = self.extended_dataframe.fuzzyPurgeMode(
            recordId,
            threshold,
            createScalaMap(self.spark, matchFields),
            includeSimilarityScore,
        )
        return DataFrame(result, self.sqlContext)

    def fuzzyMergeMode(
            self, recordId, sourceId, threshold, matchFields, includeSimilarityScore
    ) -> DataFrame:
        result = self.extended_dataframe.fuzzyMergeMode(
            recordId,
            sourceId,
            threshold,
            createScalaMap(self.spark, matchFields),
            includeSimilarityScore,
        )
        return DataFrame(result, self.sqlContext)

    def syncDataFrameColumnsWithSchema(self, columnNames) -> DataFrame:
        result = self.extended_dataframe.syncDataFrameColumnsWithSchema(
            createScalaList(self.spark, columnNames)
        )
        return DataFrame(result, self.sqlContext)

    def zipWithIndex(
            self, startValue, incrementBy, indexColName, sparkSession
    ) -> DataFrame:
        result = self.extended_dataframe.zipWithIndex(
            startValue, incrementBy, indexColName, sparkSession._jsparkSession
        )
        return DataFrame(result, self.sqlContext)

    def metaPivot(self, pivotColumns, nameField, valueField, sparkSession) -> DataFrame:
        result = self.extended_dataframe.metaPivot(
            createScalaList(self.spark, pivotColumns), nameField, valueField, sparkSession._jsparkSession
        )
        return DataFrame(result, self.sqlContext)

    def dynamicReplace(self, rulesDf, rulesOrderBy, baseColName, replacementExpressionColumnName,
                       replacementValueColumnName, sparkSession) -> DataFrame:
        result = self.extended_dataframe.dynamicReplace(rulesDf, rulesOrderBy, baseColName,
                                                        replacementExpressionColumnName, replacementValueColumnName,
                                                        sparkSession._jsparkSession)
        return DataFrame(result, self.sqlContext)

    def dynamicReplaceExpr(self, rulesDf, rulesOrderBy, baseColName, replacementExpressionColumnName,
                           replacementValueColumnName, sparkSession) -> DataFrame:
        result = self.extended_dataframe.dynamicReplaceExpr(rulesDf, rulesOrderBy, baseColName,
                                                            replacementExpressionColumnName, replacementValueColumnName,
                                                            sparkSession._jsparkSession)
        return DataFrame(result, self.sqlContext)

    def evaluate_expression(self, userExpression, selectedColumnNames, sparkSession) -> DataFrame:
        result = self.extended_dataframe.evaluate_expression(
            userExpression, createScalaList(self.spark, selectedColumnNames), sparkSession._jsparkSession
        )
        return DataFrame(result, self.sqlContext)

    def compareRecords(
            self, otherDataFrame, componentName, limit, sparkSession
    ) -> DataFrame:
        result = self.extended_dataframe.compareRecords(
            otherDataFrame._jdf, componentName, limit, sparkSession._jsparkSession
        )
        return DataFrame(result, self.sqlContext)

    def generateSurrogateKeys(
            self,
            keyDF,
            naturalKeys,
            surrogateKey,
            overrideSurrogateKeys,
            computeOldPortOutput,
            spark,
    ) -> (DataFrame, DataFrame, DataFrame):
        result = self.extended_dataframe.generateSurrogateKeys(
            keyDF._jdf,
            createScalaList(self.spark, naturalKeys),
            surrogateKey,
            createScalaOption(self.spark, overrideSurrogateKeys),
            computeOldPortOutput,
            spark._jsparkSession,
        )
        result.toString()
        return (
            DataFrame(result._1(), self.sqlContext),
            DataFrame(result._2(), self.sqlContext),
            DataFrame(result._3(), self.sqlContext),
        )

    def generateLogOutput(
            self,
            componentName,
            subComponentName,
            perRowEventTypes,
            perRowEventTexts,
            inputRowCount,
            outputRowCount,
            finalLogEventType,
            finalLogEventText,
            finalEventExtraColumnMap,
            sparkSession,
    ) -> DataFrame:
        result = self.extended_dataframe.generateLogOutput(
            componentName,
            subComponentName,
            createScalaColumnOption(self.spark, perRowEventTypes),
            createScalaColumnOption(self.spark, perRowEventTexts),
            inputRowCount,
            createScalaOption(self.spark, outputRowCount),
            createScalaColumnOption(self.spark, finalLogEventType),
            createScalaColumnOption(self.spark, finalLogEventText),
            createScalaColumnMap(self.spark, finalEventExtraColumnMap),
            sparkSession._jsparkSession,
        )

        return DataFrame(result, self.sqlContext)

    def mergeMultipleFileContentInDataFrame(
            self,
            fileNameDF,
            spark,
            delimiter,
            readFormat,
            joinWithInputDataframe,
            outputSchema=None,
            ffSchema=None,
            abinitioSchema=None,
    ) -> DataFrame:
        if outputSchema is not None:
            result = self.extended_dataframe.mergeMultipleFileContentInDataFrame(
                fileNameDF._jdf,
                spark._jsparkSession,
                outputSchema.json(),
                delimiter,
                readFormat,
                joinWithInputDataframe,
                createScalaOption(self.spark, ffSchema),
            )
        else:
            result = self.extended_dataframe.mergeMultipleFileContentInDataFrame(
                fileNameDF._jdf,
                spark._jsparkSession,
                abinitioSchema,
                delimiter,
                readFormat,
                joinWithInputDataframe,
            )
        return DataFrame(result, self.sqlContext)

    def breakAndWriteDataFrameForOutputFile(
            self, outputColumns, fileColumnName, format, delimiter
    ):
        self.extended_dataframe.breakAndWriteDataFrameForOutputFile(
            createScalaList(self.spark, outputColumns),
            fileColumnName,
            format,
            createScalaOption(self.spark, delimiter),
            createScalaOption(self.spark, None),
            True
        )

    def breakAndWriteDataFrameForOutputFileWithSchema(
            self, outputSchema, fileColumnName, format, delimiter=None
    ):
        self.extended_dataframe.breakAndWriteDataFrameForOutputFileWithSchema(
            outputSchema,
            fileColumnName,
            format,
            createScalaOption(self.spark, delimiter),
        )

    def writeToOutputFile(self, outputPath, ffSchema, formatType, delimiter):
        self.extended_dataframe.writeToOutputFile(
            outputPath, ffSchema, formatType, delimiter
        )

    def deduplicate(self, typeToKeep, groupByColumns, orderByColumns):
        result = self.extended_dataframe.deduplicate(
            typeToKeep,
            createScalaColumnList(self.spark, groupByColumns),
            createScalaColumnList(self.spark, orderByColumns),
        )
        return DataFrame(result, self.sqlContext)

    def __getattr__(self, item: str):
        if item == "interim":
            self.interim

        if hasattr(self.extended_dataframe, item):
            return getattr(self.extended_dataframe, item)
        else:
            return getattr(self.dataframe, item)


class InterimConfig:
    jvm_accessible = False # unused right now, can use in future.
    def __init__(self):
        self.isInitialized = False
        self.interimOutput = None
        self.session = None

    def initialize(self, spark: SparkSession, sessionForInteractive: str = ""):
        from py4j.java_gateway import JavaPackage

        self.isInitialized = True
        self.session = sessionForInteractive
        # It's `JavaClass` when scala-libs are present, and `JavaPackage` when they are not present.
        try :
            if (
                type(spark.sparkContext._jvm.org.apache.spark.sql.InterimOutputHive2)
                == JavaPackage
            ):
                InterimConfig.jvm_accessible = True
                raise Exception(
                    "Scala Prophecy Libs jar was not found in the classpath. Please add Scala Prophecy Libs and retry the operation"
                )
            self.interimOutput = (
                spark.sparkContext._jvm.org.apache.spark.sql.InterimOutputHive2.apply(
                    sessionForInteractive
                )
            )
        except PySparkAttributeError as ae: # spark >= 3.4.1
            InterimConfig.jvm_accessible = False

    def maybeInitialize(self, spark: SparkSession, sessionForInteractive: str = ""):
        if not self.isInitialized:
            self.initialize(spark, sessionForInteractive)

    def clear(self):
        self.isInitialized = False
        self.interimOutput = None


interimConfig = InterimConfig()


class ProphecyDebugger:
    @classmethod
    def is_prophecy_wheel(cls, path):
        import zipfile

        zip = zipfile.ZipFile(path)
        for name in zip.namelist():
            if "workflow.latest.json" in name:
                return True
        return False

    @classmethod
    def wheels_in_path(cls):
        import sys, pathlib

        l = []
        for p in sys.path:
            try:
                for child in pathlib.Path(p).rglob("*.whl"):
                    if ProphecyDebugger.is_prophecy_wheel(child):
                        l.append(str(child))
            except IOError as e:
                ProphecyDebugger.log(
                    None, f"Error when trying to read path {p}: {str(e)}"
                )
                pass
        ProphecyDebugger.log(None, f"Wheels in path {l}")
        return l

    @classmethod
    def wheels_in_site_packages(cls):
        import sys, os

        target_file = "direct_url.json"
        url_list = []
        # Get list of site-packages directories
        site_packages = [s for s in sys.path if "site-packages" in s]

        # Walk through each site-packages directory
        for site_package in site_packages:
            ProphecyDebugger.log(None, f"site-package: {site_packages}")
            for dirpath, dirnames, filenames in os.walk(site_package):
                ProphecyDebugger.log(None, filenames)
                if target_file in filenames:
                    # Construct full path to the target file
                    file_path = os.path.join(dirpath, target_file)
                    try:
                        # Open and read the target file
                        with open(file_path, "r") as file:
                            data = json.load(file)
                            if "url" in data:
                                url_list.append(data["url"].replace("file://", ""))
                    except Exception as e:
                        ProphecyDebugger.log(None, f"Error reading {file_path}: {e}")

        ProphecyDebugger.log(None, f"urls fetched from site packages: {url_list}")
        return url_list

    # Uses a different ijson library. Accurate, but adds another dependency to libs
    # @classmethod
    # def find_file_in_wheel(cls, filename, wheel_path, desired_value):
    #     try:
    #         with zipfile.ZipFile(wheel_path, 'r') as z:
    #             if filename in z.namelist():
    #                 with z.open(filename) as json_file:
    #                     parser = ijson.parse(json_file)
    #                     for prefix, event, value in parser:
    #                         if prefix == "a.b" and value == desired_value:
    #                             # Reset the file pointer to the beginning
    #                             json_file.seek(0)
    #                             # Read and return the entire content
    #                             return json_file.read().decode('utf-8')
    #     except zipfile.BadZipFile:
    #         print(f"Warning: Could not read {wheel_path}. Might be a corrupted wheel.")
    #     except PermissionError:
    #         print(f"Warning: Permission denied when trying to read {wheel_path}.")
    #     except IOError as e:
    #         print(f"Warning: IO Error ({e}) when trying to read {wheel_path}.")
    #     return None

    @classmethod
    def is_pipeline_wheel(
            cls, wheel_path, pipeline_uri, filename="workflow.latest.json"
    ):
        import zipfile

        key_pattern = f'"uri" : "{pipeline_uri}"'  # Basic pattern match to avoid using new dependencies
        try:
            with zipfile.ZipFile(wheel_path, "r") as z:
                if any(name.endswith(filename) for name in z.namelist()):
                    for file_to_read in z.namelist():
                        if file_to_read.endswith(filename):
                            with z.open(file_to_read) as json_file:
                                content = json_file.read().decode("utf-8")
                                if key_pattern in content:
                                    return True
        except zipfile.BadZipFile:
            ProphecyDebugger.log(
                None,
                f"Warning: Could not read {wheel_path}. Might be a corrupted wheel",
            )
        except PermissionError:
            ProphecyDebugger.log(
                None, f"Warning: Permission denied when trying to read {wheel_path}"
            )
        except IOError as e:
            ProphecyDebugger.log(
                None, f"Warning: IO Error {e} when trying to read {wheel_path}"
            )
        return False

    @classmethod
    def find_pipeline_wheel(cls, pipeline_uri):
        wheels = (
                ProphecyDebugger.wheels_in_path()
                + ProphecyDebugger.wheels_in_site_packages()
        )
        for wheel_path in wheels:
            if ProphecyDebugger.is_pipeline_wheel(wheel_path, pipeline_uri):
                return wheel_path
        ProphecyDebugger.log(
            None,
            f"Could not find pipeline code for pipeline {pipeline_uri} in wheels {wheels}",
        )
        return None

    @classmethod
    def log(cls, spark: SparkSession, s: str):
        import logging

        # log4jLogger = sc._jvm.org.apache.log4j
        # LOGGER = log4jLogger.LogManager.getLogger("ProphecyDebugger")
        # LOGGER.info(s)
        logger = logging.getLogger("py4j")
        logger.info(s)

    @classmethod
    def sparkSqlShow(cls, spark: SparkSession, query: str):
        spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.sparkSqlShow(
            spark._jsparkSession, query
        )

    @classmethod
    def sparkSql(cls, spark: SparkSession, query: str):
        jdf = spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.sparkSql(
            spark._jsparkSession, query
        )
        return DataFrame(jdf, spark)

    @classmethod
    def exception(cls, spark: SparkSession):
        spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.exception(
            spark._jsparkSession
        )

    @classmethod
    def class_details(cls, spark: SparkSession, name: str):
        return (
            spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.classDetails(
                spark._jsparkSession, name
            )
        )

    @classmethod
    def spark_conf(cls, spark: SparkSession):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.sparkConf(
            spark._jsparkSession
        )

    @classmethod
    def runtime_conf(cls, spark: SparkSession):
        return (
            spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.runtimeConf(
                spark._jsparkSession
            )
        )

    @classmethod
    def local_properties(cls, spark: SparkSession):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.localProperties(
            spark._jsparkSession
        )

    @classmethod
    def local_property(cls, spark: SparkSession, key: str):
        return (
            spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.localProperty(
                spark._jsparkSession, key
            )
        )

    @classmethod
    def local_property_async(cls, spark: SparkSession, key: str):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.localPropertyAsync(
            spark._jsparkSession, key
        )

    @classmethod
    def get_scala_object(cls, spark: SparkSession, className: str):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.getScalaObject(
            spark._jsparkSession, className
        )

    @classmethod
    def call_scala_object_method(
            cls, spark: SparkSession, className: str, methodName: str, args: list = []
    ):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.callScalaObjectMethod(
            spark._jsparkSession, className, methodName, args
        )

    @classmethod
    def call_scala_object_method_async(
            cls, spark: SparkSession, className: str, methodName: str, args: list = []
    ):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.callScalaObjectMethodAsync(
            spark._jsparkSession, className, methodName, args
        )


class MetricsCollector:

    jvm_accessible = False

    @classmethod
    def initializeMetrics(cls, spark: SparkSession):
        try:
            spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.initializeMetrics(
                spark._jsparkSession
            )
            cls.jvm_accessible = True
        except:
            print("Failed to initialize MetricsCollector. Spark context is not available")

    # We don't have positional arguments in python code base, thereby moving directly to keyword based argument.
    @classmethod
    def start(
            cls,
            spark: SparkSession,
            sessionForInteractive: str = "",
            pipelineId: str = "",
            config=None,
            **kwargs,
    ):
        global interimConfig
        interimConfig.maybeInitialize(spark, sessionForInteractive)

        # Define a function to convert object to a dictionary
        def should_include(key, value):
            # remove any unwanted objects from the config:
            to_ignore = ["spark", "prophecy_spark", "jvm", "secret_manager"]
            return key not in to_ignore and not isinstance(value, SparkSession)

        def to_dict_trampoline(obj):
            from collections import deque

            stack = deque()
            processed = {}
            result = None

            # Start with the initial object
            stack.append((obj, None, None))

            while stack:
                current_obj, parent_obj, key_in_parent = stack.pop()
                obj_id = id(current_obj)

                if obj_id in processed:
                    value = processed[obj_id]
                    if parent_obj is not None:
                        if isinstance(parent_obj, dict):
                            parent_obj[key_in_parent] = value
                        elif isinstance(parent_obj, list):
                            parent_obj.append(value)  # Append to list
                    else:
                        result = value
                    continue

                if isinstance(current_obj, (list, tuple)):
                    # Process list or tuple
                    new_list = []
                    processed[obj_id] = new_list

                    if parent_obj is not None:
                        if isinstance(parent_obj, dict):
                            parent_obj[key_in_parent] = new_list
                        elif isinstance(parent_obj, list):
                            parent_obj.append(new_list)  # Append to list
                    else:
                        result = new_list

                    # Add items to the stack
                    for item in reversed(current_obj):
                        stack.append((item, new_list, None))  # Use None since we append to list
                elif isinstance(current_obj, dict):
                    # Process dict
                    new_dict = {}
                    processed[obj_id] = new_dict

                    if parent_obj is not None:
                        if isinstance(parent_obj, dict):
                            parent_obj[key_in_parent] = new_dict
                        elif isinstance(parent_obj, list):
                            parent_obj.append(new_dict)
                    else:
                        result = new_dict

                    for key, value in current_obj.items():
                        if should_include(key, value):
                            stack.append((value, new_dict, key))
                elif hasattr(current_obj, "__dict__"):
                    # Process object's __dict__
                    new_dict = {}
                    processed[obj_id] = new_dict

                    if parent_obj is not None:
                        if isinstance(parent_obj, dict):
                            parent_obj[key_in_parent] = new_dict
                        elif isinstance(parent_obj, list):
                            parent_obj.append(new_dict)
                    else:
                        result = new_dict

                    for key, value in current_obj.__dict__.items():
                        if should_include(key, value):
                            stack.append((value, new_dict, key))
                elif hasattr(current_obj, "__slots__"):
                    # Process object's __slots__
                    new_dict = {}
                    processed[obj_id] = new_dict

                    if parent_obj is not None:
                        if isinstance(parent_obj, dict):
                            parent_obj[key_in_parent] = new_dict
                        elif isinstance(parent_obj, list):
                            parent_obj.append(new_dict)
                    else:
                        result = new_dict

                    for slot in current_obj.__slots__:
                        value = getattr(current_obj, slot)
                        if should_include(slot, value):
                            stack.append((value, new_dict, slot))
                else:
                    # Leaf node
                    processed[obj_id] = current_obj
                    if parent_obj is not None:
                        if isinstance(parent_obj, dict):
                            parent_obj[key_in_parent] = current_obj
                        elif isinstance(parent_obj, list):
                            parent_obj.append(current_obj)  # Append to list
                    else:
                        result = current_obj

            return result

        for key, value in kwargs.items():
            ProphecyDebugger.log(
                None, f"Unused argument passed -- key: {key}, value: {value}"
            )

        if isBlank(sessionForInteractive):
            pipeline_wheel_path = ProphecyDebugger.find_pipeline_wheel(
                pipeline_uri=pipelineId
            )
            if pipeline_wheel_path is not None:
                spark.conf.set("spark.prophecy.pipeline.package", pipeline_wheel_path)
        # if isBlank(sessionForInteractive):  # when running as job
        #     # if not set by the user, try to set it automatically
        #     if not spark.conf.get("spark.prophecy.packages", None):
        #         wheels = ProphecyDebugger.wheels_in_path()
        #         str1 = ",".join(wheels)
        #         spark.conf.set("spark.prophecy.packages", str1)
        #         ProphecyDebugger.log(spark, "wheels " + str1)

        if cls.jvm_accessible:
            if config is not None:
                pipeline_config = json.dumps(config, default=to_dict_trampoline, indent=4)
                try:
                    spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.start(
                        spark._jsparkSession,
                        pipelineId,
                        sessionForInteractive,
                        pipeline_config,
                    )
                except Exception as ex:
                    print("Exception while starting metrics collector: ", ex)
                    raise ex
            else:
                spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.start(
                    spark._jsparkSession, pipelineId, sessionForInteractive
                )
        else:
            print("Running pipeline without metrics")

    @classmethod
    def end(cls, spark: SparkSession):
        if cls.jvm_accessible:
            spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.end(
                spark._jsparkSession
            )
        else:
            print("Finished pipeline without metrics")
        global interimConfig
        interimConfig.clear()

    # Use this like MetricsCollector.instrument(args)(pipeline_func_which_takes_spark)
    # Another variation could be annotation based, but going with this right now.
    @classmethod
    def instrument(
            cls,
            spark: SparkSession,
            sessionForInteractive: str = "",
            pipelineId: str = "",
            config=None,
            **kwargs,
    ):
        cls.initializeMetrics(spark)
        def wrapper(f):

            if cls.jvm_accessible:

                state = TaskState.LAUNCHING
                startTime = currentTimeString()
                try:
                    MetricsCollector.start(
                        spark, sessionForInteractive, pipelineId, config, **kwargs
                    )
                    state = TaskState.RUNNING
                    sendPipelineProgressEvent(spark, sessionForInteractive, pipelineId, state,
                                              startTime)
                    try:
                        monkey_patch_print()
                        ret = f(spark)

                        # if there are active streams, wait for them to finish
                        if len(spark.streams.active) > 0:
                            spark.streams.resetTerminated()
                            spark.streams.awaitAnyTermination()

                        return ret
                    # Base exception covers all bases like keyboard interrupt, generator exit and system exit
                    # It is safe to capture it, since we raise it again anyway
                    except BaseException as e:
                        state = TaskState.FAILED
                        endTime = currentTimeString()
                        etype = type(e).__name__
                        emsg = str(e)
                        etrace = traceback.format_exc()

                        if isinstance(e, CapturedException):
                            py4j_error = None
                            if hasattr(e, 'getErrorClass') and e.getErrorClass():
                                py4j_error = e._origin
                            elif e.cause and hasattr(e.cause, 'getErrorClass') and e.cause.getErrorClass():
                                py4j_error = e.cause._origin
                            elif e._origin:
                                py4j_error = e._origin
                            elif e.cause and e.cause._origin:
                                py4j_error = e.cause._origin
                            sendPipelineProgressEvent(spark, sessionForInteractive, pipelineId, state,
                                                      startTime, endTime, py4j_error)
                            spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.setPythonFailedStatus(
                                spark._jsparkSession, etype, emsg, etrace, py4j_error
                            )
                        elif isinstance(e, Py4JJavaError):
                            sendPipelineProgressEvent(spark, sessionForInteractive, pipelineId, state,
                                                      startTime, endTime, e.java_exception)
                            spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.setPythonFailedStatus(
                                spark._jsparkSession, etype, emsg, etrace, e.java_exception
                            )
                        else:
                            # Python exception. Need not be transferred to JVM
                            send_pipeline_progress_event_on_python_exception(spark, sessionForInteractive,
                                                                             pipelineId, state,
                                                                             startTime, endTime, e)
                            spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.setPythonFailedStatus(
                                spark._jsparkSession, etype, emsg, etrace
                            )
                        raise
                finally:
                    try:
                        if state != TaskState.FAILED:
                            state = TaskState.FINISHED
                            endTime = currentTimeString()
                            sendPipelineProgressEvent(spark, sessionForInteractive, pipelineId, state,
                                                      startTime, endTime)
                        revert_monkey_patching()
                        MetricsCollector.end(spark)
                    except:
                        pass

            else:
                ret = f(spark)

                # if there are active streams, wait for them to finish
                if len(spark.streams.active) > 0:
                    spark.streams.resetTerminated()
                    spark.streams.awaitAnyTermination()

                return ret

        return wrapper

    @classmethod
    def withSparkOptimisationsDisabled(cls, fn):
        def wrapper(spark):
            try:
                disabledOpt = spark.conf.get("spark.sql.optimizer.excludedRules")
            except:
                disabledOpt = None
            try:
                aqe = spark.conf.get("spark.sql.adaptive.enabled")
            except:
                aqe = None
            spark.conf.set(
                "spark.sql.optimizer.excludedRules",
                spark.sparkContext._jvm.org.apache.spark.sql.ProphecySparkSession.getAllExcludesRules(),
            )
            spark.conf.set("spark.sql.adaptive.enabled", "false")
            try:
                fn(spark)
            finally:
                if disabledOpt:
                    spark.conf.set("spark.sql.optimizer.excludedRules", disabledOpt)
                else:
                    spark.conf.unset("spark.sql.optimizer.excludedRules")
                if aqe:
                    spark.conf.set("spark.sql.adaptive.enabled", aqe)
                else:
                    spark.conf.unset("spark.sql.adaptive.enabled")

        return wrapper


def collectMetrics(
        spark: SparkSession,
        df: DataFrame,
        subgraph: str,
        component: str,
        port: str,
        numRows: int = 40,
        run_id: Optional[str] = None,
        config=None
) -> DataFrame:
    global interimConfig
    interimConfig.maybeInitialize(spark)
    pdf = ProphecyDataFrame(df, spark)
    conf_str = None
    if config is not None:
        conf_str = json.dumps(config.to_dict(), default=str)

    return pdf.interim(
        subgraph, component, port, "dummy", numRows, interimConfig.interimOutput, detailedStats=False, run_id=run_id,
        config=conf_str
    )


def createEventSendingListener(
        spark: SparkSession, execution_url: str, session: str, scheduled: bool
):
    spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.addSparkListener(
        spark._jsparkSession, execution_url, session, scheduled
    )


def postDataToSplunk(props: dict, payload):
    import gzip
    import requests
    from requests import HTTPError
    from requests.adapters import HTTPAdapter
    from urllib3 import Retry

    with requests.Session() as session:
        adapter = HTTPAdapter(
            max_retries=Retry(
                total=int(props.get("maxRetries", 4)),
                backoff_factor=float(props.get("backoffFactor", 1)),
                status_forcelist=[429, 500, 502, 503, 504],
            )
        )
        session.mount("http://", adapter)
        session.headers.update(
            {
                "Authorization": "Splunk " + props["token"],
                "Content-Encoding": "gzip",
                "BatchId": props.get("batchId", None),
            }
        )
        res = session.post(props["url"], gzip.compress(bytes(payload, encoding="utf8")))
        print(
            f"IN SESSION URL={props['url']} res.status_code = {res.status_code} res={res.text}"
        )
        if res.status_code != 200 and props.get("stopOnFailure", False):
            raise HTTPError(res.reason)


def splunkHECForEachWriter(props: dict):
    def wrapper(batchDF: DataFrame, batchId: int):
        max_load: Optional[int] = props.get("maxPayload")
        # Take 90% of the payload limit and convert KB into Bytes
        max_load = int(0.9 * 1024 * int(max_load)) if max_load else None
        props.update({"batchId": str(batchId)})

        def f(iterableDF):
            payload, prevsize = "", 0

            for row in iterableDF:
                if max_load and prevsize + len(row) >= max_load:
                    print(f"buffer hit at size {prevsize}")
                    postDataToSplunk(props, payload)
                    payload, prevsize = "", 0
                else:
                    payload += '{"event":' + row + "}"
                    prevsize += len(row) + 10  # 10 bytes is for padding

            if payload:
                print(f"last payload with size {prevsize}")
                postDataToSplunk(props, payload)

        batchDF.toJSON().foreachPartition(f)

    return wrapper


def find_first_index(sequence, condition):
    return next((i for i, x in enumerate(sequence) if condition(x)), -1)


def find_last_index(sequence, condition):
    return next((i for i, x in reversed(list(enumerate(sequence))) if condition(x)), -1)


def currentTimeString() -> str:
    return str(int(time.time() * 1000))


def extract_hierarchical_gem_name(stack, current_frame, function) -> str:
    stack_function_names = [f.function for f in stack]
    start_index = find_first_index(stack_function_names, lambda x: x == "inner_wrapper")
    end_index = find_last_index(stack_function_names, lambda x: x == "pipeline")
    sliced_stack = stack_function_names[start_index + 1:end_index]
    stack_without_wrapper_nesting = [s for s in sliced_stack if s != "inner_wrapper"]
    stack_without_wrapper_nesting.reverse()

    frame = current_frame.f_back
    class_name = None

    # Check if 'self' or 'cls' is in the local variables of the caller's frame
    if 'self' in frame.f_locals:
        class_name = frame.f_locals['self'].__class__.__name__
    elif 'cls' in frame.f_locals:
        class_name = frame.f_locals['cls'].__name__

    if class_name:
        full_stack = stack_without_wrapper_nesting + [class_name, function.__name__]
        stack_with_class = [s for s in full_stack if s not in ("execute", "apply", "__run__")]
        return ".".join(stack_with_class)

    if len(stack) > 1:
        caller_frame = stack[1].frame
        caller_self = caller_frame.f_locals.get('self', None)
        if caller_self is not None:
            caller_class_name = caller_self.__class__.__name__
            full_stack = stack_without_wrapper_nesting + [caller_class_name, function.__name__]
            stack_with_class = [s for s in full_stack if s not in ("execute", "apply", "__run__")]
            return ".".join(stack_with_class)

    return ".".join(stack_without_wrapper_nesting + [function.__name__])


# Add support for stdout in pipeline progress
def sendPipelineProgressEvent(spark: SparkSession, userSession: str, pipelineId: str, state: str,
                              startTime: str, endTime: str = "", exception: Optional[Any] = None):
    if exception:
        spark.sparkContext._jvm.org.apache.spark.sql.ProphecySparkSession.sendPipelineProgressEvent(
            spark._jsparkSession, userSession, pipelineId, state, startTime, endTime, exception
        )
    else:
        spark.sparkContext._jvm.org.apache.spark.sql.ProphecySparkSession.sendPipelineProgressEvent(
            spark._jsparkSession, userSession, pipelineId, state, startTime, endTime
        )


def send_pipeline_progress_event_on_python_exception(spark: SparkSession, userSession: str,
                                                     pipelineId: str, state: str, startTime: str,
                                                     endTime: str, exception: BaseException):
    serializable_exception = SerializableException.from_python_exception(exception)
    spark.sparkContext._jvm.org.apache.spark.sql.ProphecySparkSession.sendPipelineProgressEvent(
        spark._jsparkSession, userSession, pipelineId, state, startTime, endTime,
        serializable_exception.exception_type, serializable_exception.msg,
        serializable_exception.cause_msg, serializable_exception.stack_trace
    )


def send_gem_progress_event_on_python_exception(spark: SparkSession, userSession: str, process_id: str,
                                                state: str, startTime: str, endTime: str, stdout: str,
                                                stderr: str, exception: BaseException):
    serializable_exception = SerializableException.from_python_exception(exception)
    spark.sparkContext._jvm.org.apache.spark.sql.ProphecySparkSession.sendGemProgressEvent(
        spark._jsparkSession, userSession, process_id, state, startTime, endTime, stdout,
        stderr, serializable_exception.exception_type, serializable_exception.msg,
        serializable_exception.cause_msg, serializable_exception.stack_trace
    )


def sendGemProgressEvent(spark: SparkSession, userSession: str, process_id: str, state: str,
                         startTime: str, endTime: str = "", stdout: str = "[]", stderr: str = "[]",
                         exception: Optional[Any] = None):
    if exception:
        spark.sparkContext._jvm.org.apache.spark.sql.ProphecySparkSession.sendGemProgressEvent(
            spark._jsparkSession, userSession, process_id, state, startTime, endTime, stdout,
            stderr, exception
        )
    else:
        spark.sparkContext._jvm.org.apache.spark.sql.ProphecySparkSession.sendGemProgressEvent(
            spark._jsparkSession, userSession, process_id, state, startTime, endTime, stdout,
            stderr,
        )


def get_process_from_gem(spark: SparkSession, gemName: str, userSession: str) -> str:
    return spark.sparkContext._jvm.org.apache.spark.sql.ProphecySparkSession.getProcessFromGem(
        spark._jsparkSession, gemName, userSession)


class SerializableException:
    exception_type: str
    msg: str
    cause_msg: str
    stack_trace: str

    def __init__(self, exception_type, msg, cause_msg, stack_trace):
        self.exception_type = exception_type
        self.msg = msg
        self.cause_msg = cause_msg
        self.stack_trace = stack_trace

    @staticmethod
    def from_python_exception(exception: BaseException):
        exception_type = type(exception).__name__
        exception_message = str(exception)
        exception_cause = str(exception.__cause__) if exception.__cause__ else ""
        exception_stack_trace = ''.join(
            traceback.format_exception(None, exception, exception.__traceback__))
        return SerializableException(exception_type, exception_message, exception_cause,
                                     exception_stack_trace)


def instrument(function):
    def inner_wrapper(*args, **kwargs):
        if isinstance(args[0], SparkSession):
            spark = args[0]
        else:
            spark = args[1]

        global interimConfig
        if interimConfig.isInitialized:
            user_session = interimConfig.session
        else:
            user_session = ""
        start_time = currentTimeString()
        state = TaskState.LAUNCHING
        gem_name = extract_hierarchical_gem_name(inspect.stack(), inspect.currentframe(), function)
        process_id = get_process_from_gem(spark, gem_name, user_session)
        sendGemProgressEvent(spark, user_session, process_id, state, start_time)
        with capture_streams() as data_manager:
            try:
                state = TaskState.RUNNING
                sendGemProgressEvent(spark, user_session, process_id, state,
                                     start_time)
                result = function(*args, **kwargs)
                return result
            # Handle PythonException separately, probably similar to normal exception below?
            except CapturedException as captured_error:
                state = TaskState.FAILED
                captured_stdout, captured_stderr = data_manager.drain_thread_output()
                py4j_error = None

                if hasattr(captured_error, 'getErrorClass') and captured_error.getErrorClass():
                    py4j_error = captured_error._origin
                elif captured_error.cause and hasattr(captured_error.cause,
                                                      'getErrorClass') and captured_error.cause.getErrorClass():
                    py4j_error = captured_error.cause._origin
                elif captured_error._origin:
                    py4j_error = captured_error._origin
                elif captured_error.cause and captured_error.cause._origin:
                    py4j_error = captured_error.cause._origin
                sendGemProgressEvent(spark, user_session, process_id, state,
                                     start_time, currentTimeString(), captured_stdout,
                                     captured_stderr, py4j_error)
                raise captured_error
            except Py4JJavaError as py4j_error:
                state = TaskState.FAILED
                captured_stdout, captured_stderr = data_manager.drain_thread_output()
                sendGemProgressEvent(spark, user_session, process_id, state,
                                     start_time, currentTimeString(), captured_stdout,
                                     captured_stderr, py4j_error.java_exception)
                raise py4j_error
            except Exception as exception:
                state = TaskState.FAILED
                captured_stdout, captured_stderr = data_manager.drain_thread_output()
                send_gem_progress_event_on_python_exception(spark, user_session, process_id, state,
                                                            start_time, currentTimeString(),
                                                            captured_stdout,
                                                            captured_stderr, exception)
                raise exception
            except BaseException as base_exception:
                state = TaskState.FAILED
                captured_stdout, captured_stderr = data_manager.drain_thread_output()
                send_gem_progress_event_on_python_exception(spark, user_session, process_id, state,
                                                            start_time, currentTimeString(),
                                                            captured_stdout,
                                                            captured_stderr, base_exception)
                raise base_exception
            finally:
                if state != TaskState.FAILED:
                    state = TaskState.FINISHED
                    captured_stdout, captured_stderr = data_manager.drain_thread_output()
                    sendGemProgressEvent(spark, user_session, process_id, state,
                                         start_time,
                                         currentTimeString(), captured_stdout, captured_stderr)

    return inner_wrapper


class SecretManager:

    def __init__(self, spark: SparkSession):
        self.jvm = spark.sparkContext._jvm
        self.spark = spark
        self.secret_manager = self.jvm.io.prophecy.libs.secrets.ProphecySecrets

    def get(self, scope: str, key: str, provider: str):
        return self.secret_manager.get(scope, key, provider)
