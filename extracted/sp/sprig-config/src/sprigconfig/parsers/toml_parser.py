import tomllib

class TomlParser:
    def parse(self, text: str):
        try:
            return tomllib.loads(text)
        except tomllib.TOMLDecodeError as e:
            raise ValueError(str(e))
