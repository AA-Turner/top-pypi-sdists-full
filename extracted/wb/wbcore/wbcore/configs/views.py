from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from wbcore.configs.registry import config_registry


class ConfigAPIView(APIView):
    permission_classes = []

    def get(self, request: Request) -> Response:
        return Response(config_registry.get_config_dict(request))
