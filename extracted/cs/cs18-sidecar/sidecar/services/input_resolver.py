import re
from typing import List

from sidecar.services.input_value_resolver import InputValueResolver


class InputResolver(InputValueResolver):
    pattern = r'\$\{([\w\d_.-]+)\}'

    def __init__(self, resolvers: List[InputValueResolver]):
        self._resolvers = resolvers

    def can_resolve(self, value: str) -> bool:
        if any(True for _ in re.finditer(self.pattern, value)):
            return True

        if self._is_expression(value):
            resolver = self._try_get_resolver(value[1:])
            if resolver:
                return True
        return False

    def resolve(self, value: str):
        resolved_tokens = {}
        for match in re.finditer(self.pattern, value):
            match_token = match.group()
            if match_token in resolved_tokens:
                continue
            match_value = match.group(1)
            resolver = self._get_resolver(match_value)
            resolved_tokens[match_token] = resolver.resolve(match_value)
            if resolved_tokens:
                for k, v in resolved_tokens.items():
                    value = value.replace(k, v)

        if self._is_expression(value):
            value = value[1:]
            resolver = self._get_resolver(value)
            return resolver.resolve(value)
        return value

    @staticmethod
    def _is_expression(value: str):
        return value.startswith('$')

    def _get_resolver(self, value) -> InputValueResolver:
        resolver = self._try_get_resolver(value)
        if not resolver:
            raise Exception(f'no resolver found for {value}')
        return resolver

    def _try_get_resolver(self, value) -> InputValueResolver:
        resolver = next((r for r in self._resolvers if r.can_resolve(value)), None)
        return resolver
