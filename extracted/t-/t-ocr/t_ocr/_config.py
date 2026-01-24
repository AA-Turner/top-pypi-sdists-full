class AWSConfiguration:
    def __init__(self, account_id: int, region: str, arn: str):
        self.bucket_name = f"t-ocr-{account_id}"
        self.region = region
        self.step_function_arn = f"arn:aws:states:{region}:{account_id}:stateMachine:t_ocr"
        self.parallel_step_function_arn = f"arn:aws:states:{region}:{account_id}:stateMachine:t_ocr_parallel"
        self.arn = arn
