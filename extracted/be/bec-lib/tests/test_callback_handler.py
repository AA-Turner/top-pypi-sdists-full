from unittest import mock

from bec_lib.callback_handler import CallbackHandler, CallbackRegister


def test_register_callback():
    def dummy():
        pass

    handler = CallbackHandler()
    handler.register("scan_segment", dummy)

    assert len(handler.callbacks) == 1


def test_register_callback_with_cm():
    def dummy():
        pass

    handler = CallbackHandler()
    with CallbackRegister("scan_segment", dummy, callback_handler=handler):
        assert len(handler.callbacks) == 1

    assert len(handler.callbacks) == 0


def test_register_callback_with_cm_multiple():
    def dummy():
        pass

    handler = CallbackHandler()
    scan_id = handler.register("scan_segment", dummy)
    with CallbackRegister("scan_segment", dummy, callback_handler=handler):
        assert len(handler.callbacks) == 2

    assert len(handler.callbacks) == 1
    assert scan_id in handler.callbacks


def test_remove_returns_id():
    def dummy():
        pass

    handler = CallbackHandler()
    scan_id = handler.register("scan_segment", dummy)
    assert handler.remove(scan_id) == scan_id


def test_removal_of_non_existing_item_returns():
    def dummy():
        pass

    handler = CallbackHandler()
    handler.register("scan_segment", dummy)
    assert handler.remove(2) == -1


def test_async_callback_is_called():
    handler = CallbackHandler()
    dummy = mock.MagicMock()
    with CallbackRegister("scan_segment", dummy, callback_handler=handler):
        handler.run("scan_segment", {"data": 1}, {"metadata": 1})
        dummy.assert_called_once_with({"data": 1}, {"metadata": 1})


def test_sync_callback_is_called():
    handler = CallbackHandler()
    dummy = mock.MagicMock()
    with CallbackRegister("scan_segment", dummy, sync=True, callback_handler=handler):
        handler.run("scan_segment", {"data": 1}, {"metadata": 1})
        dummy.assert_not_called()

        handler.poll()
        dummy.assert_called_once_with({"data": 1}, {"metadata": 1})
