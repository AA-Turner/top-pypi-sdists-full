import instructor
import logging
import boto3
from anthropic import AnthropicBedrock
from channel_advisor_api.utils.logger import get_logger
from functools import cached_property

logger = get_logger(__name__)


class AwsClient:
    def __init__(self):
        for logger in ["botocore", "boto3", "urllib3", "httpx", "httpcore", "anthropic"]:
            logging.getLogger(logger).setLevel(logging.WARNING)
        for logger in ["instructor"]:
            logging.getLogger(logger).setLevel(logging.INFO)

    @cached_property
    def session(self) -> boto3.Session:
        return boto3.Session()

    def log_kwargs(self, **kwargs):
        logger.info(f"claude client completion called with kwargs: {kwargs}")

    @cached_property
    def claude_client(self) -> instructor.Instructor:

        credentials = self.session.get_credentials()
        credentials = dict(
            aws_access_key=credentials.access_key,
            aws_secret_key=credentials.secret_key,
            aws_session_token=credentials.token,
        )
        client = instructor.from_anthropic(AnthropicBedrock(**credentials))
        client.on("completion:kwargs", self.log_kwargs)
        # Define hook functions
        return client
