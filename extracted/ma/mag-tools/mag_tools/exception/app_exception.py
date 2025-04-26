class AppException(Exception):
    """应用异常类"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"AppException: {self.message}"
