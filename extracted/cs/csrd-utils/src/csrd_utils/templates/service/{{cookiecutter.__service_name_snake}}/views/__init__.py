from fastapi import FastAPI

app = FastAPI(title="{{ cookiecutter.service_name }}")


__all__ = ("app",)
