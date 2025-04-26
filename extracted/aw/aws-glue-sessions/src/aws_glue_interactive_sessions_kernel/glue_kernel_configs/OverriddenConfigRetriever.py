from aws_glue_interactive_sessions_kernel.glue_kernel_configs.ConfigRetriever import ConfigRetriever


class OverriddenConfigRetriever(ConfigRetriever):
    def __init__(self, overridden_configs):
        self.overridden_configs = overridden_configs

    def get_config_variable(self, config_name):
        return getattr(self.overridden_configs, config_name)
