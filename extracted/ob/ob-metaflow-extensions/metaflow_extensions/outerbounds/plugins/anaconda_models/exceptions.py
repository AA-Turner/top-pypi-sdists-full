class ModelAccessDenied(ValueError):
    """Raised when a model is denied by ModelAccessPolicy."""

    def __init__(self, model_name, reason):
        self.model_name = model_name
        self.reason = reason
        super().__init__("Model '%s' access denied: %s" % (model_name, reason))
