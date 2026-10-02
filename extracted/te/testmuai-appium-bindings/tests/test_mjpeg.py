"""The MJPEG screenshot path: frame reading, the fallback, and the session verdict.

Every test here runs against a local socket stub, never a device: the stub speaks the
part of the protocol the reader actually depends on — an HTTP response followed by
JPEG frames between SOI/EOI markers — and counts the connections it accepts, which is
what pins "reachability is decided once per session".
"""
import socket
import threading
import time

import pytest

from testmu_appium import _config
from testmu_appium._errors import ScreenshotUnavailable, UnsupportedOnPlatform
from testmu_appium._helpers import _adapters, _mjpeg
from testmu_appium._helpers._perception import capture_perception

_PAGE_SOURCE = """<?xml version="1.0" encoding="UTF-8"?>
<hierarchy rotation="0">
  <node class="android.widget.Button" resource-id="com.app:id/go" text="Go"
        clickable="true" enabled="true" bounds="[40,100][440,220]" />
</hierarchy>
"""


def _jpeg(payload: bytes) -> bytes:
    """A minimal frame: the SOI/EOI markers the reader splits on around a payload."""
    return b"\xff\xd8" + payload + b"\xff\xd9"


class _StreamStub:
    """A local MJPEG endpoint. Serves canned frames and counts accepted connections.

    Binds an EPHEMERAL port and hands it back for the code under test to be pointed
    at. Binding the port a real session forwards (`_config._DEFAULT_MJPEG_PORT`) would
    make `adb forward` fail for anyone driving a device on this machine, so the port
    the kernel hands out is asserted not to be it.
    """

    _RESPONSE_HEAD = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: multipart/x-mixed-replace; boundary=--BoundaryString\r\n\r\n"
    )
    _PART_HEAD = b"----BoundaryString\r\nContent-Type: image/jpeg\r\n\r\n"

    def __init__(self, frames=(), *, serve_frames=True, trailing=b"", keep_open=False):
        self.frames = list(frames)
        self.serve_frames = serve_frames
        self.trailing = trailing
        self.connections = 0
        self._running = True
        # A real broadcaster never ends the response, so the reader cannot lean on EOF.
        self._keep_open = keep_open
        self._closing = threading.Event()
        self._thread = None
        self._listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._listener.bind(("127.0.0.1", 0))
            self._listener.listen(16)
            self._listener.settimeout(0.1)
            self.port = self._listener.getsockname()[1]
            assert self.port != _config._DEFAULT_MJPEG_PORT, (
                "the stub took the port a real device session forwards"
            )
            self._thread = threading.Thread(target=self._serve, daemon=True)
            self._thread.start()
        except BaseException:
            # A half-built stub is never handed to a test, so nothing else can close
            # the listener it already opened.
            self._listener.close()
            raise

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
        return False

    def _serve(self):
        while self._running:
            try:
                conn, _ = self._listener.accept()
            except OSError:
                continue
            self.connections += 1
            try:
                conn.recv(4096)
                if self.serve_frames:
                    conn.sendall(self._RESPONSE_HEAD)
                    for frame in self.frames:
                        conn.sendall(self._PART_HEAD + frame + b"\r\n")
                    if self.trailing:
                        conn.sendall(self.trailing)
                if self._keep_open:
                    self._closing.wait(timeout=5)
            except OSError:
                pass
            finally:
                conn.close()

    def close(self):
        """Release the port and reap the thread. Idempotent, and never raises: a
        listener that outlives the test run is the failure this guards against."""
        self._running = False
        self._closing.set()
        try:
            self._listener.close()
        except OSError:
            pass
        if self._thread is not None:
            self._thread.join(timeout=6)
            assert not self._thread.is_alive(), "the stub's server thread outlived it"
            self._thread = None

    @property
    def listening(self) -> bool:
        """Whether the port still accepts connections."""
        try:
            socket.create_connection(("127.0.0.1", self.port), timeout=0.5).close()
            return True
        except OSError:
            return False


@pytest.fixture
def stream(monkeypatch):
    """Start a stub on an ephemeral port and point the configured port at it.

    Every stub is registered before anything else can fail and closed in the
    fixture's teardown, which pytest runs whether the test passed, failed or raised.
    """
    started = []

    def _start(frames=(), *, serve_frames=True, trailing=b"", keep_open=False):
        stub = _StreamStub(frames, serve_frames=serve_frames, trailing=trailing,
                           keep_open=keep_open)
        started.append(stub)
        monkeypatch.setitem(_config._config, "mjpeg_port", stub.port)
        return stub

    try:
        yield _start
    finally:
        for stub in started:
            stub.close()


@pytest.fixture
def auto_source(monkeypatch):
    """The shipped default: probe the stream on a local run target, fall back."""
    monkeypatch.setitem(_config._config, "screenshot_source", _config.SOURCE_AUTO)
    monkeypatch.setattr(_config, "run_target", "local")


class _Driver:
    """A driver whose screencap works and records how often it was asked."""

    page_source = _PAGE_SOURCE

    def __init__(self):
        self.screenshots = 0

    def get_window_size(self):
        return {"width": 1080, "height": 2340}

    def get_screenshot_as_png(self):
        self.screenshots += 1
        return b"\x89PNG-appium"


class _BlindDriver(_Driver):
    """A driver whose screencap fails, so both paths are gone."""

    def get_screenshot_as_png(self):
        self.screenshots += 1
        raise RuntimeError("screencap timed out")


class TestFrameReader:
    """read_latest_frame() against a stub stream."""

    def test_a_frame_is_read_off_the_stream(self, stream):
        stream([_jpeg(b"only")])
        assert _mjpeg.read_latest_frame() == _jpeg(b"only")

    def test_the_newest_frame_of_the_stream_wins(self, stream):
        """The first frame off the socket can be a frame interval old; the drain keeps
        reading and returns the last complete frame instead."""
        stream([_jpeg(b"oldest"), _jpeg(b"middle"), _jpeg(b"newest")])
        assert _mjpeg.read_latest_frame() == _jpeg(b"newest")

    def test_a_stream_that_never_ends_still_returns_promptly(self, stream):
        """A live broadcaster holds the response open, so the read ends on the drain —
        nothing newer buffered — rather than on EOF or the overall timeout."""
        stream([_jpeg(b"oldest"), _jpeg(b"newest")], keep_open=True)
        started = time.monotonic()
        assert _mjpeg.read_latest_frame() == _jpeg(b"newest")
        assert time.monotonic() - started < _mjpeg._STREAM_TIMEOUT_S

    def test_a_half_written_trailing_frame_is_not_returned(self, stream):
        stream([_jpeg(b"complete")], trailing=b"\xff\xd8partial-no-end-marker")
        assert _mjpeg.read_latest_frame() == _jpeg(b"complete")

    def test_a_stream_that_serves_no_frame_raises(self, stream):
        stream([], serve_frames=False)
        with pytest.raises(RuntimeError, match="no complete MJPEG frame"):
            _mjpeg.read_latest_frame()

    def test_an_unreachable_port_raises(self, stream):
        stub = stream([_jpeg(b"never served")])
        stub.close()
        with pytest.raises(OSError):
            _mjpeg.read_latest_frame()


class TestCaptureTakesTheFastPath:
    def test_the_frame_serves_the_screenshot(self, auto_source, stream):
        import base64

        stream([_jpeg(b"live")])
        driver = _Driver()
        perception = capture_perception(driver)
        assert base64.b64decode(perception.screenshot_b64) == _jpeg(b"live")
        assert perception.screenshot_source == "mjpeg"
        assert driver.screenshots == 0, "the Appium screencap is not paid for as well"

    def test_the_entries_are_captured_alongside_the_frame(self, auto_source, stream):
        stream([_jpeg(b"live")])
        perception = capture_perception(_Driver())
        assert [e["role"] for e in perception.entries] == ["button"]

    def test_no_source_is_recorded_when_no_screenshot_was_asked_for(
        self, auto_source, stream
    ):
        stub = stream([_jpeg(b"live")])
        perception = capture_perception(_Driver(), include_screenshot=False)
        assert perception.screenshot_source is None
        assert stub.connections == 0


class TestPortWiring:
    """The reader opens the CONFIGURED port, which is what lets the tests run on an
    ephemeral one instead of the port a real device session forwards."""

    def test_the_capture_reads_the_caller_supplied_port(self, monkeypatch, stream):
        import base64

        from testmu_appium import configure

        stub = stream([_jpeg(b"on the caller's port")])
        monkeypatch.setitem(_config._config, "mjpeg_port", _config._DEFAULT_MJPEG_PORT)
        monkeypatch.setitem(_config._config, "screenshot_source", _config.SOURCE_AUTO)
        monkeypatch.setattr(_config, "run_target", "local")

        configure(mjpeg_port=stub.port)

        assert _mjpeg.port() == stub.port
        perception = capture_perception(_Driver())
        assert base64.b64decode(perception.screenshot_b64) == _jpeg(b"on the caller's port")
        assert perception.screenshot_source == "mjpeg"
        assert stub.connections == 1


class TestStubHygiene:
    """The stub's own contract: an ephemeral port, released when the test ends."""

    def test_the_stub_never_takes_the_port_a_device_session_forwards(self, stream):
        stub = stream([_jpeg(b"served")])
        assert stub.port != _config._DEFAULT_MJPEG_PORT
        assert stub.listening

    def test_closing_the_stub_releases_the_port(self, stream):
        stub = stream([_jpeg(b"served")])
        stub.close()
        assert not stub.listening

    def test_closing_is_idempotent(self, stream):
        """Teardown runs after a test that closed the stub itself."""
        stub = stream([_jpeg(b"served")])
        stub.close()
        stub.close()
        assert not stub.listening


class TestFallback:
    def test_an_unreachable_stream_falls_back_to_appium(self, auto_source, stream):
        import base64

        stub = stream([], serve_frames=False)
        driver = _Driver()
        perception = capture_perception(driver)
        assert base64.b64decode(perception.screenshot_b64) == b"\x89PNG-appium"
        assert perception.screenshot_source == "appium"
        assert stub.connections == 1

    def test_the_unreachable_verdict_is_decided_once_per_session(
        self, auto_source, stream
    ):
        """A cloud run must not pay a connect attempt on every capture."""
        stub = stream([], serve_frames=False)
        driver = _Driver()
        for _ in range(4):
            assert capture_perception(driver).screenshot_source == "appium"
        assert stub.connections == 1
        assert driver.screenshots == 4

    def test_a_new_session_probes_the_stream_again(self, auto_source, stream):
        stub = stream([], serve_frames=False)
        capture_perception(_Driver())
        _mjpeg.reset()
        capture_perception(_Driver())
        assert stub.connections == 2

    def test_a_cloud_run_target_never_opens_the_stream(self, monkeypatch, stream):
        """The forward Appium creates for a cloud session lives on the device host,
        so 127.0.0.1 here reaches nothing."""
        monkeypatch.setitem(_config._config, "screenshot_source", _config.SOURCE_AUTO)
        monkeypatch.setattr(_config, "run_target", "cloud")
        stub = stream([_jpeg(b"live")])
        perception = capture_perception(_Driver())
        assert perception.screenshot_source == "appium"
        assert stub.connections == 0


class TestForcedSource:
    def test_forcing_appium_skips_the_stream_entirely(self, monkeypatch, stream):
        monkeypatch.setitem(_config._config, "screenshot_source", _config.SOURCE_APPIUM)
        monkeypatch.setattr(_config, "run_target", "local")
        stub = stream([_jpeg(b"live")])
        perception = capture_perception(_Driver())
        assert perception.screenshot_source == "appium"
        assert stub.connections == 0

    @pytest.fixture
    def forced_mjpeg(self, monkeypatch):
        monkeypatch.setitem(_config._config, "screenshot_source", _config.SOURCE_MJPEG)
        monkeypatch.setattr(_config, "run_target", "cloud")

    def test_forcing_mjpeg_reads_the_stream_whatever_the_run_target(
        self, forced_mjpeg, stream
    ):
        stream([_jpeg(b"tunnelled")])
        assert capture_perception(_Driver()).screenshot_source == "mjpeg"

    def test_forcing_mjpeg_forbids_the_appium_fallback(self, forced_mjpeg, stream):
        """A lost stream is a lost screenshot, not a differently-timed one from a
        path the caller ruled out."""
        stream([], serve_frames=False)
        driver = _Driver()
        perception = capture_perception(driver)
        assert perception.screenshot_b64 is None
        assert perception.screenshot_source is None
        assert driver.screenshots == 0
        assert perception.entries, "the entry list is still captured"

    def test_forcing_mjpeg_raises_when_the_screenshot_is_required(
        self, forced_mjpeg, stream
    ):
        stream([], serve_frames=False)
        with pytest.raises(ScreenshotUnavailable):
            capture_perception(_Driver(), require_screenshot=True)

    def test_a_forced_stream_is_not_reprobed_after_it_failed(self, forced_mjpeg, stream):
        stub = stream([], serve_frames=False)
        for _ in range(3):
            assert capture_perception(_Driver()).screenshot_b64 is None
        assert stub.connections == 1


class TestScalingBasis:
    """The per-source scaling factors the android row declares as data."""

    def test_the_mjpeg_source_downscales_by_half(self):
        assert _mjpeg.source_downscale(_config.SOURCE_MJPEG, platform="android") == 0.5

    def test_the_appium_screencap_is_full_resolution(self):
        assert _mjpeg.source_downscale(_config.SOURCE_APPIUM, platform="android") == 1.0

    def test_the_reference_device_frame_size_follows_the_declared_factor(self):
        """The 1080x2400 reference device serves its MJPEG frames at 540x1200."""
        factor = _mjpeg.source_downscale(_config.SOURCE_MJPEG, platform="android")
        assert (1080 * factor, 2400 * factor) == (540, 1200)

    def test_the_configured_platform_serves_the_lookup_by_default(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "android")
        assert _mjpeg.source_downscale(_config.SOURCE_MJPEG) == 0.5

    @pytest.mark.parametrize("source", [_config.SOURCE_MJPEG, _config.SOURCE_APPIUM])
    def test_ios_needs_no_correction_in_the_basis_it_works_in(self, source):
        """iOS works in POINTS end to end — taps, window size and the vision basis
        are all points — so a frame's extra resolution never enters a coordinate
        calculation. 1.0 is the true factor in that basis, not a placeholder; the
        per-device display scale is only meaningful in frame-pixel space."""
        assert _mjpeg.source_downscale(source, platform="ios") == 1.0

    def test_an_unshipped_platform_still_raises(self):
        with pytest.raises(UnsupportedOnPlatform) as exc:
            _mjpeg.source_downscale(_config.SOURCE_MJPEG, platform="tizen")
        assert "screenshot scaling" in str(exc.value)

    def test_both_registry_rows_carry_the_downscale_entry(self):
        for platform in ("android", "ios"):
            assert "downscale" in _adapters._REGISTRIES["screenshot_scaling"][platform]


class TestBothPathsGone:
    def test_a_required_screenshot_raises_when_neither_path_serves(
        self, auto_source, stream
    ):
        stream([], serve_frames=False)
        with pytest.raises(ScreenshotUnavailable) as exc:
            capture_perception(_BlindDriver(), require_screenshot=True)
        assert "screencap timed out" in str(exc.value)

    def test_the_default_capture_still_fails_open(self, auto_source, stream):
        stream([], serve_frames=False)
        perception = capture_perception(_BlindDriver())
        assert perception.screenshot_b64 is None
        assert perception.screenshot_source is None
        assert perception.entries
