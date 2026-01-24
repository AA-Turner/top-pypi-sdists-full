import unittest
from click.testing import CliRunner
from anc.cli.cli import main  # Import the main CLI entry point

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_loadtest_command(self):
        result = self.runner.invoke(main, ['loadtest', 'run', '--backend', 'vllm', "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("model", result.output)

    def test_dataset_list_command(self):
        result = self.runner.invoke(main, ['ds', 'task'])
        self.assertEqual(result.exit_code, 0)
        expected_string_list = ["boost",
                                "status"]
        for expected_string in expected_string_list:
            self.assertIn(expected_string, result.output)

if __name__ == '__main__':
    unittest.main()