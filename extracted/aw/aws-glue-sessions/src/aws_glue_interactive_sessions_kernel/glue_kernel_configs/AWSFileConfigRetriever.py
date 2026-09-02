import json

from aws_glue_interactive_sessions_kernel.glue_kernel_configs.ConfigRetriever import ConfigRetriever

import botocore

from aws_glue_interactive_sessions_kernel.glue_kernel_utils.GlueSessionsConstants import GLUE_PREFIX, GLUE_VERSION, \
    REGION, SESSION_TYPE, SPARK_CONF, SESSION_ID_PREFIX, TAGS, GLUE_JOB_TYPE, IAM_ROLE, GLUE_ROLE_ARN, \
    EXTRA_PY_FILES, EXTRA_JARS, CONNECTIONS, ADDITIONAL_PYTHON_MODULES
from aws_glue_interactive_sessions_kernel.glue_kernel_utils.ValidationUtils import convert_list_to_string



class AWSFileConfigRetriever(ConfigRetriever):
    def __init__(self, profile=None):
        self.profile = profile

    def get_profile(self):
        # Attempt to retrieve default profile if a profile is not already set
        if not self.profile and botocore.session.Session().full_config["profiles"].get("default"):
            self.profile = "default"
        return self.profile

    def _retrieve_from_aws_config(self, key):
        profile = self.get_profile()
        if profile:
            custom_profile_session = botocore.session.Session(profile=self.get_profile())
            if custom_profile_session.full_config["profiles"].get(profile):
                return custom_profile_session.full_config["profiles"][self.get_profile()].get(key)
        return None
    def get_config_variable(self, config_name):
        # Special handling for these configs where the configs are already used by customers and cannot be changed
        if config_name in [GLUE_VERSION, REGION, SPARK_CONF, SESSION_ID_PREFIX]:
            return self._retrieve_from_aws_config(config_name) \
                if self._retrieve_from_aws_config(config_name) is not None \
                else self._retrieve_from_aws_config(GLUE_PREFIX + config_name)
        # Special handling for session type as the config is already defined as a job_type environment variable.
        if config_name == SESSION_TYPE:
            return self._retrieve_from_aws_config(GLUE_JOB_TYPE) \
                if self._retrieve_from_aws_config(GLUE_JOB_TYPE) \
                else self._retrieve_from_aws_config(GLUE_PREFIX + SESSION_TYPE)

        if config_name == IAM_ROLE:
            return self._retrieve_from_aws_config(GLUE_ROLE_ARN) \
                if self._retrieve_from_aws_config(GLUE_ROLE_ARN) is not None \
                else self._retrieve_from_aws_config(GLUE_PREFIX + IAM_ROLE)
        if config_name == TAGS:
            return self._retrieve_tags_from_aws_config(GLUE_PREFIX + TAGS)

        if config_name in [EXTRA_PY_FILES, ADDITIONAL_PYTHON_MODULES, EXTRA_JARS, CONNECTIONS]:
            return convert_list_to_string(self._retrieve_from_aws_config(GLUE_PREFIX + config_name)) \
                if self._retrieve_from_aws_config(GLUE_PREFIX + config_name) is not None \
                else None
        return self._retrieve_from_aws_config(GLUE_PREFIX + config_name)

    def _retrieve_tags_from_aws_config(self, tags_key):
        tags = self._retrieve_from_aws_config(tags_key)
        if isinstance(tags, str):
            tags_dict = json.loads(tags)
            return tags_dict
        else:
            return tags

