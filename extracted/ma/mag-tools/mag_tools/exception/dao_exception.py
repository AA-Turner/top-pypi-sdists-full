from mag_tools.exception.app_exception import AppException


class DaoException(AppException):
    """应用异常类"""

    def __init__(self, message: str):
        super().__init__(message)

    def __str__(self):
        return f"DaoException: {self.message}"
