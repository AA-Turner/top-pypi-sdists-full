import functools

from chalk.utils.environment_parsing import env_var_bool


@functools.lru_cache(None)
def should_skip_source_code_parsing():
    """Whether to skip parsing source code for better error messages. Setting `CHALK_DISABLE_SOURCE_CODE_PARSING` to True can help improve graph loading performance."""
    return env_var_bool("CHALK_DISABLE_SOURCE_CODE_PARSING")
