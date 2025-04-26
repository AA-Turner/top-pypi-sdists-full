# Databricks notebook source
import boto3
import time
import json
import uuid
from datetime import date
from enum import Enum
from botocore.config import Config

# COMMAND ----------

class Log_Level(Enum):
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4

# COMMAND ----------

class LoggerMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Logger():
    def __init__(self, log_stream_name, notebook_name, log_level=Log_Level.ERROR, squad="datalake", cid="",region="us-east-1", log_group_name="databricks-logs"):
        self.log_group_name = f"{squad}-{log_group_name}"
        self.log_stream_name = log_stream_name
        self.region = region
        self.max_attempts = 10
        self.config = Config(region_name=self.region, retries = {'max_attempts': self.max_attempts, 'mode': 'standard'})
        self.logs_client = boto3.client('logs', config=self.config)
        self.cid = str(uuid.uuid4())
        self.notebook_name = notebook_name
        self.processing_date = date.today().strftime("%Y-%m-%d")
        
        self.log_level = log_level

    def create_group_name(self):
        try:
            self.logs_client.create_log_group(logGroupName=self.log_group_name)
        except self.logs_client.exceptions.ResourceAlreadyExistsException:
            pass
        return
        
    def create_log_stream(self):
        try:
            self.logs_client.create_log_stream(logGroupName=self.log_group_name, logStreamName=self.log_stream_name)
        except self.logs_client.exceptions.ResourceAlreadyExistsException:
            pass
        return
    
    def create_log(self):
        self.create_group_name()
        self.create_log_stream()
        return
    
    def DEBUG(self, message, att=[]):
        if self.log_level.value <= Log_Level.DEBUG.value:
            return self.send_log(message, "DEBUG", att)
    
    def INFO(self, message, att=[]):
        if self.log_level.value <= Log_Level.INFO.value:
            return self.send_log(message, "INFO", att)

    def WARN(self, message, att=[]):
        if self.log_level.value <= Log_Level.WARN.value:
            return self.send_log(message, "WARN", att)
        
    def ERROR(self, message, att=[]):
        if self.log_level.value <= Log_Level.ERROR.value:
            return self.send_log(message, "ERROR", att)
    
    def send_log(self, message, severity, attributes=[]):
        
        response = self.logs_client.describe_log_streams(logGroupName=self.log_group_name,
                                               logStreamNamePrefix=self.log_stream_name)
        
        log_message = {
            "Timestamp": time.time(),
            "SeverityText": severity,
            "Attributes": {
                "Cid": self.cid,
                "NotebookName": self.notebook_name,
                "ProcessingDate": self.processing_date

            },
            "Body": message
        }

        for att in attributes:
            orig_attribute = log_message["Attributes"]
            key = list(att.keys())[0]
            orig_attribute[key] = att[key]

        log_event = {
            'logGroupName': self.log_group_name,
            'logStreamName': self.log_stream_name,
            'logEvents': [
                {
                    'timestamp': int(round(time.time() * 1000)),
                    'message': json.dumps(log_message, default=str)
                },
            ],
        }

        #Adding last sequence token to log event before sending logs if it exists
        if len(response['logStreams']) > 0:
            if 'uploadSequenceToken' in response['logStreams'][0]:
                log_event.update(
                    {'sequenceToken': response['logStreams'][0]['uploadSequenceToken']})

        #print("logs to send : ", log_event)
        response = self.logs_client.put_log_events(**log_event)
        time.sleep(1)
        return response

# COMMAND ----------

#logger = Logger("logs_lab", Log_Level.DEBUG)
#logger.create_log()
#logger.DEBUG("TESTE DEBUG")
#logger.INFO("TESTE INFO")
#logger.ERROR("TESTE ERROR")