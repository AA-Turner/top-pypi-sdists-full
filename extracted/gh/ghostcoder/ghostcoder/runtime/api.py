from ghostcoder.runtime.base import Runtime


class APIRuntime(Runtime):

    def __init__(self, url, **kwargs):
        super().__init__(schema_format = "api", **kwargs)

        self.url = url



    def schema(self):
        paths = {}
        for schema in self._function_schemas:
            paths.update(schema)

        return {
            "openapi": "3.1.0",
            "info": {
                "title": "Ghostcoder",
                "version": "0.0.1"
            },
            "servers": [
                {
                    "url": self.url,
                    "description": "Ghostcoder local dev server"
                }
            ],
            "paths": paths
}