class MockLambdaContext:
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
        self.function_name = function_name

    def get_remaining_time_in_millis(self) -> int:
        return 1000
