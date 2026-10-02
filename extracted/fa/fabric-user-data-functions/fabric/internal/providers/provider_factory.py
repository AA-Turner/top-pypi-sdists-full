# flake8: noqa: I003

from typing import Type


class ProviderFactory:

    # hash table of annotations to provider class
    __providers = {}

    def __init__(self):
        pass

    @classmethod
    def register_provider(cls, annotation: Type, provider: Type):
        if annotation not in cls.__providers:
            cls.__providers[annotation] = provider()

    @classmethod
    def get_provider(cls, annotation: Type):
        return cls.__providers.get(annotation, None)

    @classmethod
    def get_types(cls):
        return list(cls.__providers.keys())