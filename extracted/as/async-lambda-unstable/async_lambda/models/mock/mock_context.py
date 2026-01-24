class MockLambdaContext:
    """
    Mock implementation of the AWS Lambda context object for local testing.

    Attributes:
        function_name (str): Name of the Lambda function.
        function_version (str): Version of the Lambda function.
        invoked_function_arn (str): ARN of the invoked Lambda function.
        memory_limit_in_mb (int): Memory limit for the function in MB.
        aws_request_id (str): AWS request ID for the invocation.
        log_group_name (str): Log group name for the function.
        log_stream_name (str): Log stream name for the function.
    """

    function_name: str
    function_version: str = "1"
    invoked_function_arn: str = (
        "arn:aws:lambda:us-east-1:123456789012:function:my-function:1"
    )
    memory_limit_in_mb: int = 128
    aws_request_id: str = "a-request-id"
    log_group_name: str = "a-log-group"
    log_stream_name: str = "a-log-stream"

    def __init__(self, function_name: str):
        """
        Initialize a MockLambdaContext instance.

        Args:
            function_name (str): Name of the Lambda function.
        """
        self.function_name = function_name

    def get_remaining_time_in_millis(self) -> int:
        """
        Return the remaining execution time in milliseconds (mocked as 1000 ms).

        Returns:
            int: Remaining time in milliseconds.
        """
        return 1000
