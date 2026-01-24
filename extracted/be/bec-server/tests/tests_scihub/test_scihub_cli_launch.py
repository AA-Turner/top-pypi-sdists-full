from unittest import mock

from bec_server.scihub.cli.launch import main


def test_main():
    with mock.patch(
        "bec_server.scihub.cli.launch.parse_cmdline_args", return_value=(None, None, None)
    ) as mock_parser:
        with mock.patch("bec_server.scihub.SciHub") as mock_scihub:
            with mock.patch("bec_server.scihub.cli.launch.threading.Event") as mock_event:
                main()
                mock_parser.assert_called_once()
                mock_scihub.assert_called_once()
                mock_event.assert_called_once()


def test_main_shutdown():
    with mock.patch(
        "bec_server.scihub.cli.launch.parse_cmdline_args", return_value=(None, None, None)
    ) as mock_parser:
        with mock.patch("bec_server.scihub.SciHub") as mock_scihub:
            with mock.patch("bec_server.scihub.cli.launch.threading.Event") as mock_event:
                mock_event.return_value.wait.side_effect = KeyboardInterrupt()
                main()
                mock_parser.assert_called_once()
                mock_scihub.assert_called_once()
                mock_event.assert_called_once()
                mock_scihub.return_value.shutdown.assert_called_once()
