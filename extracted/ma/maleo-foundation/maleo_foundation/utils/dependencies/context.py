from fastapi.requests import Request
from maleo_foundation.models.transfers.general.request import RequestContext

class ContextDependencies:
    @staticmethod
    def get_request_context(
        request: Request
    ) -> RequestContext:
        return request.state.request_context