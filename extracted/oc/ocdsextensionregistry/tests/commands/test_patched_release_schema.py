import json
import os
import sys

from ocdsextensionregistry.__main__ import main

args = ["ocdsextensionregistry", "patched-release-schema"]


def test_command(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", [*args, os.path.join("tests", "fixtures", "package.json")])
    main()

    assert "WithheldInformationItem" in json.loads(capsys.readouterr().out)["definitions"]
