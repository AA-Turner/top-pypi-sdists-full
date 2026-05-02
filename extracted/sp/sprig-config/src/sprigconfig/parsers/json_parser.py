import json

class JsonParser:
    def parse(self, text: str):
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(str(e))
