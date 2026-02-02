class DataDiffDbtProjectVarsNotFoundError(Exception):
    "Raised when an expected dbt_project.yml section is missing."


class DataDiffDbtNoSuccessfulModelsInRunError(Exception):
    "Raised when there are no successful model runs in the run_results.json"


class DataDiffDbtRunResultsVersionError(Exception):
    "Raised when the dbt version in run_results.json is lower than the minimum version."


class DataDiffDbtSelectNoMatchingModelsError(Exception):
    "Raised when the `--select` flag returns no models."


class DataDiffDbtSelectUnexpectedError(Exception):
    "Catch all for unexpected dbt list --select results."


class DataDiffDbtCoreNoRunnerError(Exception):
    "Raised when the manifest version >= 1.5, but the dbt-core package is < 1.5. This is an edge case most likely to occur in development."


class DataDiffCustomSchemaNoConfigError(Exception):
    "Raised when a model has a custom schema, but there is no prod_custom_schema config. (And not using --state)."


class DataDiffNoDatasourceIdError(Exception):
    "Raised when using --cloud but no datasource_id was found in dbt_project.yml"


class DataDiffDatasourceIdNotFoundError(Exception):
    "Raised when using --cloud but the datasource_id is not found for a particular org."


class DataDiffCloudDiffFailed(Exception):
    "Raised when using --cloud and the remote diff fails."


class DataDiffCloudDiffTimedOut(Exception):
    "Raised when using --cloud and the diff did not return finish before the timeout value."


class DataDiffSimpleSelectNotFound(Exception):
    "Raised when using --select on dbt < 1.5 and a model node is not found in the manifest."
