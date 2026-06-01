from csrd.models import BaseSettings


class Settings(BaseSettings):

    app_name: str = "{{ cookiecutter.service_name }}"
    port: int = {{ cookiecutter.port }}
    include_actuator_endpoints: bool = False


settings = Settings()
