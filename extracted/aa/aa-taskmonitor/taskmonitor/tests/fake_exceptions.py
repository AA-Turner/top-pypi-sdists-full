"""Fake exceptions with traceback for tests."""


class FakeCode(object):
    """A fake code object for tests."""

    def __init__(self, co_filename, co_name):
        self.co_filename = co_filename
        self.co_name = co_name


class FakeFrame(object):
    """A fake frame for tests."""

    def __init__(self, f_code, f_globals):
        self.f_code = f_code
        self.f_globals = f_globals


class FakeTraceback(object):
    """A fake traceback for tests."""

    def __init__(self, frames, line_nums):
        if len(frames) != len(line_nums):
            raise ValueError("Ya messed up!")
        self._frames = frames
        self._line_nums = line_nums
        self.tb_frame = frames[0]
        self.tb_lineno = line_nums[0]
        self.tb_lasti = -1  # hack to make the tests work under Py 3.11

    @property
    def tb_next(self):
        if len(self._frames) > 1:
            return FakeTraceback(self._frames[1:], self._line_nums[1:])


class FakeException(Exception):
    """A fake exception for tests."""

    def __init__(self, *args, **kwargs):
        self._tb = None
        super().__init__(*args, **kwargs)

    @property
    def __traceback__(self):
        return self._tb

    @__traceback__.setter
    def __traceback__(self, value):
        self._tb = value

    def with_traceback(self, value):
        self._tb = value
        return self


def make_fake_exception():
    """Generate a fake exception and return it."""
    code1 = FakeCode("made_up_filename.py", "non_existent_function")
    code2 = FakeCode("another_non_existent_file.py", "another_non_existent_method")
    frame1 = FakeFrame(code1, {})
    frame2 = FakeFrame(code2, {})
    traceback = FakeTraceback([frame1, frame2], [1, 3])
    return FakeException("fake exception").with_traceback(traceback)
