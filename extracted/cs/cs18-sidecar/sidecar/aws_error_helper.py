from botocore.exceptions import ClientError


class AwsErrorHelper:
    THROTTLING_ERROR_CODE = 'Throttling'

    @staticmethod
    def is_throttling_error(e: Exception) -> bool:
        return isinstance(e, ClientError) and e.response['Error']['Code'] == AwsErrorHelper.THROTTLING_ERROR_CODE
