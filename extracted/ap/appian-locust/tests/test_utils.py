import json
from unittest import mock

import appian_locust.utilities.loadDriverUtils
from appian_locust.utilities import loadDriverUtils
import os
import unittest


def side_effect_os_path_exists(arg1) -> bool:  # type: ignore[no-untyped-def]
    return True


def side_effect_builtins_open(arg1) -> str:  # type: ignore[no-untyped-def]
    return appian_locust.utilities.DEFAULT_CONFIG_PATH


class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        self.util = loadDriverUtils()

    def test_loadconfig_with_valid_config_file(self) -> None:
        patcher_os_path_exists = mock.patch('os.path.exists')
        mock_os_path_exists = patcher_os_path_exists.start()
        mock_os_path_exists.side_effect = side_effect_os_path_exists

        mock_builtins_open = mock.mock_open(read_data=json.dumps(self.util.c))
        with mock.patch('builtins.open', mock_builtins_open):
            output = self.util.load_config(appian_locust.utilities.DEFAULT_CONFIG_PATH)
        self.assertEqual(output, self.util.c)

        mock_builtins_open.assert_called_once()
        mock_os_path_exists.assert_called_once()

        mock_os_path_exists.assert_called_once_with(appian_locust.utilities.DEFAULT_CONFIG_PATH)
        mock_builtins_open.assert_called_once_with(appian_locust.utilities.DEFAULT_CONFIG_PATH)

        patcher_os_path_exists.stop()

    def test_loadconfig_with_no_config_file(self) -> None:
        patcher_os_path_exists = mock.patch('os.path.exists')
        mock_os_path_exists = patcher_os_path_exists.start()
        mock_os_path_exists.side_effect = side_effect_os_path_exists

        mock_builtins_open = mock.mock_open(read_data=json.dumps(self.util.c))
        with mock.patch('builtins.open', mock_builtins_open):
            output = self.util.load_config(appian_locust.utilities.DEFAULT_CONFIG_PATH)
        self.assertEqual(output, self.util.c)

        mock_os_path_exists.assert_called_once()
        mock_builtins_open.assert_called_once()

        mock_os_path_exists.assert_called_once_with(appian_locust.utilities.DEFAULT_CONFIG_PATH)
        mock_builtins_open.assert_called_once_with(appian_locust.utilities.DEFAULT_CONFIG_PATH)

        patcher_os_path_exists.stop()

    def test_loadconfig_missing_file(self) -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with self.assertRaises(SystemExit):
            missing_file_path = os.path.join(dir_path, "missing_config.json")
            self.util.load_config(missing_file_path)


if __name__ == '__main__':
    unittest.main()
