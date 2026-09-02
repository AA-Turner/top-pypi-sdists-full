import pathlib
from enum import Enum, unique
from tabulate import tabulate


class SessionTable:
    def __init__(self):
        self.table_data = []

    def add_session_info(self, session_id, status, created_on):
        self.table_data.append([session_id, status, created_on])

    def format_session_info(self):
        table_headers = ["SessionId", "Status", "CreatedOn"]
        table = tabulate(self.table_data, headers=table_headers, tablefmt="grid")
        return table


# Symbols for referencing Mime types
class MimeTypes(Enum):
    TextPlain = ("text/plain")
    ImagePng = ("image/png")
    S3URI = ("text/uri-list")

# Symbols for referencing session types
@unique
class SessionType(Enum):

    def __new__(cls, value, pretty_name, python_version):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._pretty_name = pretty_name
        obj._python_version = python_version
        return obj

    etl = ("glueetl", 'etl',  "3")
    streaming = ("gluestreaming", 'streaming', "3")

    def python_version(self):
        return self._python_version

    def session_type(self):
        return self._value_

    def pretty_name(self):
        return self._pretty_name


WAIT_TIME = 1

READY_SESSION_STATUS = "READY"
PROVISIONING_SESSION_STATUS = "PROVISIONING"
NOT_FOUND_SESSION_STATUS = "NOT_FOUND"
FAILED_SESSION_STATUS = "FAILED"
STOPPING_SESSION_STATUS = "STOPPING"
STOPPED_SESSION_STATUS = "STOPPED"
TIMEOUT_SESSION_STATUS = "TIMEOUT"
UNHEALTHY_SESSION_STATUS = [NOT_FOUND_SESSION_STATUS, FAILED_SESSION_STATUS, STOPPING_SESSION_STATUS,
                            STOPPED_SESSION_STATUS]

ERROR_STATEMENT_STATUS = "ERROR"
FAILED_STATEMENT_STATUS = "FAILED"
CANCELLED_STATEMENT_STATUS = "CANCELLED"
AVAILABLE_STATEMENT_STATUS = "AVAILABLE"
COMPLETED_STATEMENT_STATUS = "COMPLETED"
FINAL_STATEMENT_STATUS = [FAILED_STATEMENT_STATUS, ERROR_STATEMENT_STATUS, CANCELLED_STATEMENT_STATUS,
                          AVAILABLE_STATEMENT_STATUS, COMPLETED_STATEMENT_STATUS]
SQL_CELL_MAGIC = "%%sql"

CELL_MAGICS = {"%%configure", "%%sql", "%%tags", "%%assume_role"}

VALID_GLUE_VERSIONS = {"2.0", "3.0", "4.0"}

CHINA_REGIONS = {"cn-north-1", "cn-northwest-1"}

ADC_REGION_ENDPOINTS = {
    "us-isof-south-1": "https://glue.us-isof-south-1.csp.hci.ic.gov",
    "us-isof-east-1": "https://glue.us-isof-east-1.csp.hci.ic.gov",
    "eu-isoe-west-1": "https://glue.eu-isoe-west-1.cloud.adc-e.uk",
    "LTW": "https://glue.us-isof-east-1.csp.hci.ic.gov",
    "NCL": "https://glue.eu-isoe-west-1.cloud.adc-e.uk",
    "ALE": "https://glue.us-isof-south-1.csp.hci.ic.gov"
}

ADC_REGION_STS_ENDPOINTS = {
    "us-isof-south-1": "https://sts.us-isof-south-1.csp.hci.ic.gov",
    "us-isof-east-1": "https://sts.us-isof-east-1.csp.hci.ic.gov",
    "eu-isoe-west-1": "https://sts.eu-isoe-west-1.cloud.adc-e.uk",
    "LTW": "https://sts.us-isof-east-1.csp.hci.ic.gov",
    "NCL": "https://sts.eu-isoe-west-1.cloud.adc-e.uk",
    "ALE": "https://sts.us-isof-south-1.csp.hci.ic.gov"
}


US_GOV_REGIONS = {"us-gov-east-1", "us-gov-west-1"}


class Colour:
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    LightGray = "\033[37m"
    DarkGray = "\033[90m"
    LightRed = "\033[91m"
    LightGreen = "\033[92m"
    LightYellow = "\033[93m"
    LightBlue = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan = "\033[96m"
    White = "\033[97m"
    Bold = "\033[1m"
    Reset = "\033[0m"


HELP_TEXT = f'''
# Available Magic Commands

## Sessions Magic

----
    %help                             Return a list of descriptions and input types for all magic commands. 
    %profile            String        Specify a profile in your aws configuration to use as the credentials provider.
    %region             String        Specify the AWS region in which to initialize a session. 
                                      Default from ~/.aws/config on Linux or macOS, 
                                      or C:\\Users\\ USERNAME \\.aws\\config" on Windows.
    %idle_timeout       Int           The number of minutes of inactivity after which a session will timeout. 
                                      Default: 2880 minutes (48 hours).
    %timeout            Int           The number of minutes after which a session will timeout. 
                                      Default: 2880 minutes (48 hours).
    %session_id_prefix  String        Define a String that will precede all session IDs in the format 
                                      [session_id_prefix]-[session_id]. If a session ID is not provided,
                                      a random UUID will be generated.
    %status                           Returns the status of the current Glue session including its duration, 
                                      configuration and executing user / role.
    %session_id                       Returns the session ID for the running session.
    %list_sessions                    Lists all currently running sessions by ID.
    %stop_session                     Stops the current session.
    %glue_version       String        The version of Glue to be used by this session. 
                                      Currently, the only valid options are 2.0, 3.0 and 4.0. 
                                      Default: 2.0.
    %reconnect          String        Specify a live session ID to switch/reconnect to the sessions.
----

## Selecting Session Types

----
    %streaming          String        Sets the session type to Glue Streaming.
    %etl                String        Sets the session type to Glue ETL.
    %session_type       String        Specify a session_type to be used. Supported values: streaming and etl.
----

## Glue Config Magic 
*(common across all session types)*

----

    %%configure         Dictionary    A json-formatted dictionary consisting of all configuration parameters for 
                                      a session. Each parameter can be specified here or through individual magics.
    %iam_role           String        Specify an IAM role ARN to execute your session with.
                                      Default from ~/.aws/config on Linux or macOS, 
                                      or C:\\Users\\%USERNAME%\\.aws\\config` on Windows.
    %number_of_workers  int           The number of workers of a defined worker_type that are allocated 
                                      when a session runs.
                                      Default: 5.
    %additional_python_modules  List  Comma separated list of additional Python modules to include in your cluster 
                                      (can be from Pypi or S3).
    %%tags        Dictionary          Specify a json-formatted dictionary consisting of tags to use in the session.
    
    %%assume_role Dictionary, String  Specify a json-formatted dictionary or an IAM role ARN string to create a session 
                                      for cross account access.
                                      E.g. {{valid arn}}
                                      %%assume_role 
                                      'arn:aws:iam::XXXXXXXXXXXX:role/AWSGlueServiceRole' 
                                      E.g. {{credentials}}
                                      %%assume_role
                                      {{
                                            "aws_access_key_id" : "XXXXXXXXXXXX",
                                            "aws_secret_access_key" : "XXXXXXXXXXXX",
                                            "aws_session_token" : "XXXXXXXXXXXX"
                                       }}
----

                                      
## Magic for Spark Sessions (ETL & Streaming)

----
    %worker_type        String        Set the type of instances the session will use as workers. 
    %connections        List          Specify a comma separated list of connections to use in the session.
    %extra_py_files     List          Comma separated list of additional Python files From S3.
    %extra_jars         List          Comma separated list of additional Jars to include in the cluster.
    %spark_conf         String        Specify custom spark configurations for your session. 
                                      E.g. %spark_conf spark.serializer=org.apache.spark.serializer.KryoSerializer
----

## Action Magic

----

    %%sql               String        Run SQL code. All lines after the initial %%sql magic will be passed
                                      as part of the SQL code.  
    %matplot      Matplotlib figure   Visualize your data using the matplotlib library.
                                      E.g. 
                                      import matplotlib.pyplot as plt
                                      # Set X-axis and Y-axis values
                                      x = [5, 2, 8, 4, 9]
                                      y = [10, 4, 8, 5, 2]
                                      # Create a bar chart 
                                      plt.bar(x, y) 
                                      # Show the plot
                                      %matplot plt    
    %plotly            Plotly figure  Visualize your data using the plotly library.
                                      E.g.
                                      import plotly.express as px
                                      #Create a graphical figure
                                      fig = px.line(x=["a","b","c"], y=[1,3,2], title="sample figure")
                                      #Show the figure
                                      %plotly fig

  
                
----

'''

OWNER_TAG = "owner"
GLUE_STUDIO_NOTEBOOK_IDENTIFIER = "GlueStudioNotebook"
SAGEMAKER_STUDIO_NOTEBOOK_IDENTIFIERS = ['SageMakerStudioPySparkNotebook', 'SageMakerStudioSparkNotebook']

# GlueStudio Env Variables
REQUEST_ORIGIN = "request_origin"
REGION = "region"
SESSION_ID = "session_id"
GLUE_ROLE_ARN = "glue_role_arn"
AWS_REGION = "AWS_REGION"

# Configs. These are the variable names which are used in the config file.
GLUE_VERSION = "glue_version"
GLUE_JOB_TYPE = "glue_job_type"
GLUE_TAGS = "aws_glue_tags"
USER_ID = "userId"
GLUE_PREFIX = "glue_"
ENDPOINT_URL = "endpoint_url"
PROFILE = "profile"
IAM_ROLE = "iam_role"
SESSION_ID_PREFIX = "session_id_prefix"
IDLE_TIMEOUT = "idle_timeout"
EXTRA_PY_FILES = "extra_py_files"
ENABLE_DATA_CATALOG = "enable_data_catalog"
EXTRA_JARS = "extra_jars"
ADDITIONAL_PYTHON_MODULES = "additional_python_modules"
CONNECTIONS = "connections"
NUMBER_OF_WORKERS = "number_of_workers"
MAX_CAPACITY = "max_capacity"
WORKER_TYPE = "worker_type"
SECURITY_CONFIG = "security_config"
SESSION_TYPE = "session_type"
SPARK_CONF = "spark_conf"
TAGS = "tags"
TEMP_CREDENTIALS = "temp_credentials"
TIMEOUT = "timeout"

# Retriever names
AWS_CONFIG_RETRIEVER = "AWSFileConfigRetriever"
DEFAULT_RETRIEVER = "DefaultRetriever"
OVERRIDES_RETRIEVER = "OverridenConfigRetriever"
SYSTEM_ENV_RETRIEVER = "SystemEnvConfigRetriever"


# Session Types
GLUE_ETL = "glueetl"
GLUE_STREAMING = "gluestreaming"