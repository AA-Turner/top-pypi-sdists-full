class LLMCallError(Exception):
    def __init__(self, original_exc, llm_name: str, model: str):
        self.original_exc = original_exc
        self.llm_name = llm_name
        self.model = model
        super().__init__(str(original_exc))


def is_bad_request(exception: Exception) -> bool:
    if hasattr(exception, "status_code"):
        return 400 <= int(exception.status_code) < 500
    return False
