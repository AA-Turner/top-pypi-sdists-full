class MadMonkeyHandler:
    """Stub error handler that routes failures to MadMonkey."""

    def handle(self, error_vector):
        return {"handled": True, "vector": error_vector}

    def suggest_bloom_patch(self):
        return "apply_bloom"

__all__ = ["MadMonkeyHandler"]
