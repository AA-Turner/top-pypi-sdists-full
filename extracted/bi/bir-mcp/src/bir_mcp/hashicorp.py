import os

import consul
import pydantic

from bir_mcp.utils import disable_urllib_insecure_request_warning


class ConsulKeyValue(pydantic.BaseModel):
    host: str
    key: str
    token: str | None = None
    scheme: str = "https"
    port: int = 443
    verify: bool = False  # Our Consul instances don't have valid SSL certificates.

    @classmethod
    def from_env_variables(cls):
        host = os.environ["CONSUL_HOST"]
        token = os.environ.get("CONSUL_TOKEN")
        key = os.environ["CONSUL_KEY"]
        consul_key_value = cls(host=host, token=token, key=key)
        return consul_key_value

    def model_post_init(self, _context) -> None:
        if not self.verify:
            disable_urllib_insecure_request_warning()

    def get_client(self) -> consul.Consul:
        client = consul.Consul(
            host=self.host,
            port=self.port,
            token=self.token,
            scheme=self.scheme,
            verify=self.verify,
        )
        return client

    def load(self) -> bytes:
        client = self.get_client()
        index, data = client.kv.get(self.key)
        value = data["Value"]
        return value
