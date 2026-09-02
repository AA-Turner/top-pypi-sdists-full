from collections import defaultdict
from aws_glue_interactive_sessions_kernel.glue_kernel_utils.GlueSessionsConstants import SessionType


class Config:
    def __init__(self):
        self.profile = None
        self.endpoint_url = None
        self.region = None
        self.iam_role = None
        self.session_id_prefix = None
        self.max_capacity = None
        self.number_of_workers = None
        self.worker_type = None
        self.connections = None
        self.glue_version = None
        self.security_config = None
        self.idle_timeout = None
        self.tags = defaultdict()
        self.additional_python_modules = None
        self.extra_py_files = None
        self.enable_data_catalog = None
        self.extra_jars = None
        self.spark_conf = None
        self.session_type = None
        self.temp_credentials = None
        self.timeout = None


default_configs = Config()
default_configs.session_type = SessionType.etl.pretty_name()
default_configs.glue_version = "4.0"
