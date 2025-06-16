import metaflow.metaflow_config_funcs

from metaflow_extensions.outerbounds.remote_config import init_config, reload_config

# we want to overide OSS Metaflow's initialization behavior with our own to support remote configs
# we're reassigning the METAFLOW_CONFIG variable because all downstream settings rely on it and
# users still have the power to overriden them with environment variables
metaflow.metaflow_config_funcs.METAFLOW_CONFIG = init_config()
metaflow.metaflow_config_funcs.init_config = init_config
