from fluidattacks_core.logging.sources.types import SourceStrategy
from fluidattacks_core.logging.sources.utils import get_env_var, get_environment, get_version


class DefaultSource(SourceStrategy):
    @staticmethod
    def detect() -> bool:
        return True

    @staticmethod
    def log_metadata() -> dict[str, str]:
        return {
            "ddsource": "python",
            "dd.service": get_env_var("PRODUCT_ID") or "unknown",
            "dd.version": get_version(),
            "deployment.environment": get_environment(),
        }


class LambdaSource(SourceStrategy):
    @staticmethod
    def detect() -> bool:
        return get_env_var("AWS_LAMBDA_FUNCTION_NAME") is not None

    @staticmethod
    def log_metadata() -> dict[str, str]:
        product_id = get_env_var("PRODUCT_ID")
        function_name = get_env_var("AWS_LAMBDA_FUNCTION_NAME")
        service = product_id or function_name or "unknown"

        trace_header = get_env_var("_X_AMZN_TRACE_ID")

        return {
            "ddsource": "lambda",
            "dd.service": service,
            "dd.version": get_version(),
            "deployment.environment": get_environment(),
            "lambda_metadata.function_name": function_name or "unknown",
            "lambda_metadata.trace_header": trace_header or "unknown",
        }


class BatchSource(SourceStrategy):
    @staticmethod
    def detect() -> bool:
        return get_env_var("AWS_BATCH_JOB_ID") is not None

    @staticmethod
    def log_metadata() -> dict[str, str]:
        job_id = get_env_var("AWS_BATCH_JOB_ID")
        attempt = get_env_var("AWS_BATCH_JOB_ATTEMPT")
        compute_environment = get_env_var("AWS_BATCH_CE_NAME")

        product_id = get_env_var("PRODUCT_ID")
        job_definition_name = get_env_var("JOB_DEFINITION_NAME")
        job_name = get_env_var("JOB_NAME")
        job_queue = get_env_var("AWS_BATCH_JQ_NAME")
        service = (
            product_id
            or job_definition_name
            or job_name
            or (f"from-{job_queue}" if job_queue else "unknown")
        )

        return {
            "ddsource": "batch",
            "dd.service": service,
            "dd.version": get_version(),
            "deployment.environment": get_environment(),
            "job_metadata.id": job_id or "unknown",
            "job_metadata.queue": job_queue or "unknown",
            "job_metadata.definition_name": job_definition_name or "unknown",
            "job_metadata.attempt": attempt or "unknown",
            "job_metadata.compute_environment": compute_environment or "unknown",
        }


class PipelineSource(SourceStrategy):
    @staticmethod
    def detect() -> bool:
        return PipelineSource._get_pipeline_metadata() is not None

    @staticmethod
    def log_metadata() -> dict[str, str]:
        metadata = PipelineSource._get_pipeline_metadata()

        return {
            "ddsource": "ci",
            "dd.service": get_env_var("PRODUCT_ID") or "unknown",
            "dd.version": get_version(),
            "deployment.environment": get_environment(),
            **(metadata or {}),
        }

    @staticmethod
    def _get_pipeline_metadata() -> dict[str, str] | None:
        pipeline = None
        if get_env_var("CI_JOB_ID"):
            pipeline = "gitlab_ci"
        elif get_env_var("CIRCLECI"):
            pipeline = "circleci"
        elif get_env_var("System.JobId"):
            pipeline = "azure_devops"
        elif get_env_var("BUILD_NUMBER"):
            pipeline = "jenkins"

        if pipeline is None:
            return None

        return {
            "ddsource": f"ci/{pipeline}",
            "pipeline_metadata.type": pipeline,
            **(
                {
                    "pipeline_metadata.CI_JOB_ID": get_env_var("CI_JOB_ID") or "unknown",
                    "pipeline_metadata.CI_JOB_URL": get_env_var("CI_JOB_URL") or "unknown",
                }
                if pipeline == "gitlab_ci"
                else {}
            ),
            **(
                {
                    "pipeline_metadata.CIRCLE_BUILD_NUM": get_env_var("CIRCLE_BUILD_NUM")
                    or "unknown",
                    "pipeline_metadata.CIRCLE_BUILD_URL": get_env_var("CIRCLE_BUILD_URL")
                    or "unknown",
                }
                if pipeline == "circleci"
                else {}
            ),
            **(
                {
                    "pipeline_metadata.System.JobId": get_env_var("System.JobId") or "unknown",
                }
                if pipeline == "azure_devops"
                else {}
            ),
            **(
                {
                    "pipeline_metadata.BUILD_NUMBER": get_env_var("BUILD_NUMBER") or "unknown",
                    "pipeline_metadata.BUILD_ID": get_env_var("BUILD_ID") or "unknown",
                    "pipeline_metadata.BUILD_URL": get_env_var("BUILD_URL") or "unknown",
                }
                if pipeline == "jenkins"
                else {}
            ),
        }


class ContainerSource(SourceStrategy):
    @staticmethod
    def detect() -> bool:
        return (
            get_env_var("CONTAINER_IMAGE") is not None
            or get_env_var("CONTAINER_NAME") is not None
            or get_env_var("CONTAINER_IMAGE_PATH") is not None
        )

    @staticmethod
    def log_metadata() -> dict[str, str]:
        product_id = get_env_var("PRODUCT_ID")
        container_image = get_env_var("CONTAINER_IMAGE")
        service = product_id or container_image or "unknown"

        return {
            "ddsource": "container",
            "dd.service": service,
            "dd.version": get_version(),
            "deployment.environment": get_environment(),
            "container_metadata.image": container_image or "unknown",
        }


__all__ = [
    "BatchSource",
    "ContainerSource",
    "DefaultSource",
    "LambdaSource",
    "PipelineSource",
]
