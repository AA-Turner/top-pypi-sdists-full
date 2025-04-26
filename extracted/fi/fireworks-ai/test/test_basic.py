import unittest
import fireworks.client
from fireworks.client import api
from pydantic import BaseModel


class TestBasic(unittest.TestCase):
    def test_import(self):
        self.assertRegex(fireworks.client.__version__, r"^\d+")

    def test_backward_compatiblity(self):
        # doesn't throw in the client
        api.UsageInfo(prompt_tokens=2, total_tokens=3, foo=1)

        # make sure all structs allow extra fields
        checked = 0
        for name in dir(api):
            if name.startswith("_"):
                continue
            cls = getattr(api, name)
            if (
                not hasattr(cls, "__module__")
                or cls.__module__ != "fireworks.client.api"
            ):
                continue
            if not issubclass(cls, BaseModel):
                continue
            checked += 1
            # can be deleted when we move to Pydantic 2 everywhere
            if hasattr(cls, "__config__"):
                self.assertIn(cls.Config.extra, ["ignore", None])
            else:
                self.assertIn(cls.model_config.get("extra"), ["ignore", None])
        self.assertGreater(checked, 5)


if __name__ == "__main__":
    unittest.main()
