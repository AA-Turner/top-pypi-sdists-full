import os
from unittest import mock

import responses

from launchable.utils.http_client import get_base_url
from tests.cli_test_case import CliTestCase


class SubsetsTest(CliTestCase):

    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_subsets(self):
        # Create subset-before.txt
        with open("subset-before.txt", "w") as f:
            f.write("\n".join([
                "src/test/java/example/DivTest.java",
                "src/test/java/example/DB1Test.java",
                "src/test/java/example/MulTest.java",
                "src/test/java/example/Add2Test.java",
                "src/test/java/example/File1Test.java",
                "src/test/java/example/File0Test.java",
                "src/test/java/example/SubTest.java",
                "src/test/java/example/DB0Test.java",
                "src/test/java/example/AddTest.java",
            ]))

        # Create subset-after.txt
        with open("subset-after.txt", "w") as f:
            f.write("\n".join([
                "src/test/java/example/Add2Test.java",
                "src/test/java/example/MulTest.java",
                "src/test/java/example/AddTest.java",
                "src/test/java/example/File1Test.java",
                "src/test/java/example/DivTest.java",
                "src/test/java/example/File0Test.java",
                "src/test/java/example/DB1Test.java",
                "src/test/java/example/DB0Test.java",
                "src/test/java/example/SubTest.java",
            ]))

        result = self.cli('compare', 'subsets', "subset-before.txt", "subset-after.txt", mix_stderr=False)
        expect = """|   Before |   After |   After - Before | Test                                 |
|----------|---------|------------------|--------------------------------------|
|        9 |       3 |               -6 | src/test/java/example/AddTest.java   |
|        4 |       1 |               -3 | src/test/java/example/Add2Test.java  |
|        3 |       2 |               -1 | src/test/java/example/MulTest.java   |
|        5 |       4 |               -1 | src/test/java/example/File1Test.java |
|        6 |       6 |               +0 | src/test/java/example/File0Test.java |
|        8 |       8 |               +0 | src/test/java/example/DB0Test.java   |
|        7 |       9 |               +2 | src/test/java/example/SubTest.java   |
|        1 |       5 |               +4 | src/test/java/example/DivTest.java   |
|        2 |       7 |               +5 | src/test/java/example/DB1Test.java   |
"""

        self.assertEqual(result.stdout, expect)

    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_subsets_when_new_tests(self):
        # Create subset-before.txt
        with open("subset-before.txt", "w") as f:
            f.write("\n".join([
                "src/test/java/example/SubTest.java",
                "src/test/java/example/DivTest.java",
                "src/test/java/example/Add2Test.java",
                "src/test/java/example/File0Test.java",
                "src/test/java/example/AddTest.java",
                "src/test/java/example/File1Test.java",
                "src/test/java/example/MulTest.java",
                "src/test/java/example/DB0Test.java",
                "src/test/java/example/DB1Test.java"
            ]))

        # Create subset-after.txt (which includes additional test path NewTest.java)
        with open("subset-after.txt", "w") as f:
            f.write("\n".join([
                "src/test/java/example/NewTest.java",
                "src/test/java/example/SubTest.java",
                "src/test/java/example/File0Test.java",
                "src/test/java/example/DB1Test.java",
                "src/test/java/example/DivTest.java",
                "src/test/java/example/MulTest.java",
                "src/test/java/example/File1Test.java",
                "src/test/java/example/DB0Test.java",
                "src/test/java/example/Add2Test.java",
                "src/test/java/example/AddTest.java"
            ]))

        result = self.cli('compare', 'subsets', "subset-before.txt", "subset-after.txt", mix_stderr=False)
        expect = """| Before   |   After | After - Before   | Test                                 |
|----------|---------|------------------|--------------------------------------|
| -        |       1 | NEW              | src/test/java/example/NewTest.java   |
| 9        |       4 | -5               | src/test/java/example/DB1Test.java   |
| 4        |       3 | -1               | src/test/java/example/File0Test.java |
| 7        |       6 | -1               | src/test/java/example/MulTest.java   |
| 8        |       8 | +0               | src/test/java/example/DB0Test.java   |
| 1        |       2 | +1               | src/test/java/example/SubTest.java   |
| 6        |       7 | +1               | src/test/java/example/File1Test.java |
| 2        |       5 | +3               | src/test/java/example/DivTest.java   |
| 5        |      10 | +5               | src/test/java/example/AddTest.java   |
| 3        |       9 | +6               | src/test/java/example/Add2Test.java  |
"""

        self.assertEqual(result.stdout, expect)

    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_subsets_when_deleted_tests(self):
        # Create subset-before.txt
        with open("subset-before.txt", "w") as f:
            f.write("\n".join([
                "src/test/java/example/NewTest.java",
                "src/test/java/example/SubTest.java",
                "src/test/java/example/File0Test.java",
                "src/test/java/example/DB1Test.java",
                "src/test/java/example/DivTest.java",
                "src/test/java/example/MulTest.java",
                "src/test/java/example/File1Test.java",
                "src/test/java/example/DB0Test.java",
                "src/test/java/example/Add2Test.java",
                "src/test/java/example/AddTest.java"
            ]))

        # Create subset-after.txt (which doesn't include NewTest.java)
        with open("subset-after.txt", "w") as f:
            f.write("\n".join([
                "src/test/java/example/DB1Test.java",
                "src/test/java/example/DB0Test.java",
                "src/test/java/example/File1Test.java",
                "src/test/java/example/SubTest.java",
                "src/test/java/example/AddTest.java",
                "src/test/java/example/MulTest.java",
                "src/test/java/example/File0Test.java",
                "src/test/java/example/Add2Test.java",
                "src/test/java/example/DivTest.java"
            ]))

        result = self.cli('compare', 'subsets', "subset-before.txt", "subset-after.txt", mix_stderr=False)
        expect = """|   Before | After   | After - Before   | Test                                 |
|----------|---------|------------------|--------------------------------------|
|        1 | -       | DELETED          | src/test/java/example/NewTest.java   |
|        8 | 2       | -6               | src/test/java/example/DB0Test.java   |
|       10 | 5       | -5               | src/test/java/example/AddTest.java   |
|        7 | 3       | -4               | src/test/java/example/File1Test.java |
|        4 | 1       | -3               | src/test/java/example/DB1Test.java   |
|        9 | 8       | -1               | src/test/java/example/Add2Test.java  |
|        6 | 6       | +0               | src/test/java/example/MulTest.java   |
|        2 | 4       | +2               | src/test/java/example/SubTest.java   |
|        3 | 7       | +4               | src/test/java/example/File0Test.java |
|        5 | 9       | +4               | src/test/java/example/DivTest.java   |
"""

        self.assertEqual(result.stdout, expect)

    def tearDown(self):
        if os.path.exists("subset-before.txt"):
            os.remove("subset-before.txt")
        if os.path.exists("subset-after.txt"):
            os.remove("subset-after.txt")

    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    @responses.activate
    def test_subsets_subset_ids(self):
        responses.add(
            responses.GET,
            f"{get_base_url()}/intake/organizations/{self.organization}/workspaces/{self.workspace}/subset/100",
            json={
                "subsetting": {
                    "id": 100,
                },
                "testPaths": [
                    {"testPath": [{"type": "file", "name": "aaa.py"}], "duration": 10, "density": 0.9, "reason": "Changed file: aaa.py"},  # noqa: E501
                    {"testPath": [{"type": "file", "name": "bbb.py"}], "duration": 10, "density": 0.8, "reason": "Changed file: bbb.py"}  # noqa: E501
                ],
                "rest": [
                    {"testPath": [{"type": "file", "name": "ccc.py"}], "duration": 10, "density": 0.7, "reason": "Changed file: ccc.py"}  # noqa: E501
                ]
            },
            status=200
        )
        responses.add(
            responses.GET,
            f"{get_base_url()}/intake/organizations/{self.organization}/workspaces/{self.workspace}/subset/101",
            json={
                "subsetting": {
                    "id": 101,
                },
                "testPaths": [
                    {"testPath": [{"type": "file", "name": "ddd.py"}], "duration": 10, "density": 0.9, "reason": "Changed file: ddd.py"},  # noqa: E501
                    {"testPath": [{"type": "file", "name": "ccc.py"}], "duration": 10, "density": 0.7, "reason": "Changed file: ccc.py"}  # noqa: E501
                ],
                "rest": [
                    {"testPath": [{"type": "file", "name": "bbb.py"}], "duration": 10, "density": 0.5, "reason": "Changed file: bbb.py"}   # noqa: E501
                ]
            },
            status=200
        )

        result = self.cli('compare', 'subsets',
                          '--subset-id-before', '100',
                          '--subset-id-after', '101',
                          mix_stderr=False)

        self.assert_success(result)
        expect = """PTS subset change summary:
────────────────────────────────
-> 3 tests analyzed | 1 ↑ promoted | 1 ↓ demoted
-> Code files affected: bbb.py, ccc.py, ddd.py
────────────────────────────────

Δ Rank    Subset Rank    Test Name    Reason                Density
--------  -------------  -----------  --------------------  ---------
NEW       1              file=ddd.py  Changed file: ddd.py  0.9
↑1        2              file=ccc.py  Changed file: ccc.py  0.7
↓1        3              file=bbb.py  Changed file: bbb.py  0.5
DELETED   -              file=aaa.py
"""
        self.assertEqual(result.stdout, expect)
