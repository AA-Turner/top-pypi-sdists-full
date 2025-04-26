"""
    Generic Executor of ETL code.
    Simplifies the actual ETL code by factorizing some common elements.
"""

from datetime import datetime
import time
from collections import defaultdict
from abc import ABCMeta, abstractmethod
import boto3
from pyspark.sql import SparkSession
from .cloudwatch import Logger


class ILogic(object):
    """
        Interface (Abastract Class) for defining the actual logic.
        Method execute() must be provide.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """
            istantiate an helper class
        """
        pass

    def set_logger(self, logger):
        """
            pass logger object
        """
        self.__logger = logger

    def set_spark(self, spark):
        """
            pass spark object
        """
        self._spark = spark

    def set_sync(self, sync):
        """
            pass sync object
        """
        self._sync = sync

    def set_attributes(self, attributes):
        """
            pass attributes object
        """
        self._attributes = attributes
        self._start_date = attributes["start_date"]
        self._end_date = attributes["end_date"]

    def _log(self, message):
        """
            protected method to be used by child classes for logging
        """
        if self.__logger:
            self.__logger.log(message)
        else:
            print(message)

    @abstractmethod
    def execute(self):
        """
            abstract method execute
        """
        pass


class ETLRunner(object):
    """
        Generic ETLRunner
    """

    def __init__(self, logic):
        self.__logger = None
        self.__spark = None
        self.__sync = None
        self.__start_time = None
        self.__attributes = defaultdict(str)
        self.__attributes["max_retries"] = 1
        self.__attributes["retry_wait_time"] = 0

        self.__logic = logic

    def __log(self, message):
        """
            handles logging
        """
        if self.__logger:
            self.__logger.log(message)
        else:
            print(message)

    def __log_start(self):
        """
            logs start of the job
        """
        start_date = self.__attributes["start_date"]
        end_date = self.__attributes["end_date"]
        job_name = self.__attributes["job_name"]
        self.__start_time = datetime.utcnow()

        self.__log("#############################################################")
        self.__log("Starting Job {}".format(job_name))
        self.__log("#############################################################")
        self.__log("Start Date: {}".format(start_date))
        self.__log("End Date: {}".format(end_date))
        self.__log("Qubole Bucket: {}".format(self.__attributes["qubole_bucket"]))

        self.__log("Starting Data Log for job {}".format(job_name))
        self.__log("Loading Data for Start Date = {} and End Date = {}".format(start_date, end_date))

    def __log_end(self):
        """
            logs end of the job
        """
        end_time = datetime.utcnow()
        # Calculate the time taken by the job to run
        duration = (end_time - self.__start_time).total_seconds()

        self.__log("#############################################################")
        self.__log("Job Completed Successfully")
        self.__log("#############################################################")
        self.__log("Start Time = {}".format(self.__start_time))
        self.__log("End Time = {}".format(end_time))
        self.__log("Duration = {}".format(duration))
        self.__log("#############################################################")

    def __create_ready_file(self):
        """
            creates ready file
        """
        qubole_bucket = self.__attributes["qubole_bucket"]
        job_name = self.__attributes["job_name"]
        end_date = self.__attributes["end_date"]
        self.__log("Creating Ready File {}.ready".format(job_name))
        ready_file_key = "ready/{}/{}/_SUCCESS".format(job_name, end_date)
        s3 = boto3.client("s3")
        s3.put_object(Bucket=qubole_bucket, Body="", Key=ready_file_key)
        self.__log("Ready File Created")

    def __loadlibs(self):
        """
            load standard libraries
        """
        job_name = self.__attributes["job_name"]
        cloud_location = "s3://{}/code/python/common/".format(self.__attributes["qubole_bucket"])
        self.__spark = (
            SparkSession.builder.appName(job_name)
            .enableHiveSupport()
            .config("hive.exec.dynamic.partition", "true")
            .config("hive.exec.dynamic.partition.mode", "nonstrict")
            .getOrCreate()
        )
        self.__spark.sparkContext.setLogLevel("WARN")
        self.__spark.sparkContext.addPyFile(cloud_location + "snowflake_sync/snowflake_sync.py")
        self.__spark.sparkContext.addPyFile(cloud_location + "data_quality/data_quality_v2.py")
        from snowflake_sync import SnowflakeSync
        from data_quality_v2 import DataQuality

        self.__logger = Logger(job_name)

        self.__sync = SnowflakeSync(
            self.__attributes["snowflake_wh_name"], self.__attributes["snowflake_db_name"], self.__logger
        )

    def set_attribute(self, name, value):
        """
            sets attribute
        """
        self.__attributes[name] = value

    def run(self):
        """
            main run method
        """

        self.__loadlibs()
        self.__logic.set_logger(self.__logger)
        self.__logic.set_spark(self.__spark)
        self.__logic.set_sync(self.__sync)
        self.__logic.set_attributes(self.__attributes)
        self.__log_start()

        # Execute and attempt to retry in case of unexpected errors
        retries = 0
        execution_successful = False
        while not execution_successful and retries < self.__attributes["max_retries"]:
            retries += 1
            try:
                self.__logic.execute()
                execution_successful = True
            except Exception as exc:
                self.__log("Execution failed.")
                self.__log("{}".format(exc))
                if retries == self.__attributes["max_retries"]:
                    self.__log("Process failed {} times. Exiting...".format(self.__attributes["max_retries"]))
                    raise exc
                self.__log("Waiting...")
                time.sleep(self.__attributes["retry_wait_time"])
                self.__log("Retrying...")

        self.__create_ready_file()

        self.__log_end()
