import json
from typing import List

import click

from ..testpath import TestPath
from . import launchable


@launchable.subset
def subset(client):
    def handler(output: List[TestPath], rests: List[TestPath]):
        # The output would be something like this:
        # {"tests": ["test/example_test.js", "test/login_test.js"]}
        if client.rest:
            with open(client.rest, "w+", encoding="utf-8") as f:
                f.write(json.dumps({"tests": [client.formatter(t) for t in rests]}))
        if output:
            click.echo(json.dumps({"tests": [client.formatter(t) for t in output]}))

    # read lines as test file names
    for t in client.stdin():
        if t.rstrip("\n"):
            client.test_path(t.rstrip("\n"))
    client.output_handler = handler

    client.run()


record_tests = launchable.CommonRecordTestImpls(__name__).file_profile_report_files()

split_subset = launchable.CommonSplitSubsetImpls(__name__).split_subset()
