import os
class EnvURLS(str):
    LOCAL = "http://localhost:8000"
    DEV = "https://spreadyapi.onrender.com"
    PROD = "https://spreadyapi.onrender.com"


def getEnvURL():
    if os.environ.get("SPREADY_ENV") == "local":
        return EnvURLS.LOCAL
    else:
        return EnvURLS.PROD