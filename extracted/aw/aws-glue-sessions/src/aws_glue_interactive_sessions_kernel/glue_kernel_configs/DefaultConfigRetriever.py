from aws_glue_interactive_sessions_kernel.glue_kernel_configs.ConfigRetriever import ConfigRetriever


class DefaultConfigRetriever(ConfigRetriever):
    def __init__(self, default_configs):
        self.default_configs = default_configs

    def get_config_variable(self, config_name):
        return getattr(self.default_configs, config_name, None)
