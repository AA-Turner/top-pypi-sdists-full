"""Testing other aspects of the implementation and API."""

import os
import re
import sys
import time
import errno
import builtins
import platform

from contextlib import contextmanager, ExitStack, suppress
from datetime import timedelta
from io import StringIO
from multiprocessing import Process, Queue
from pathlib import Path
from random import randint
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from flufl.lock import Lock, LockState, NotLockedError, SEP, TimeOutError
from flufl.lock._lockfile import CLOCK_SLOP, ERRORS


EMOCKEDFAILURE = 99
EOTHERMOCKEDFAILURE = 98
ENINES = 999


@pytest.fixture
def lock():
    with TemporaryDirectory() as lock_dir:
        lock = Lock(os.path.join(lock_dir, 'test.lck'))
        yield lock
        with suppress(NotLockedError):
            lock.unlock()


def child_locker(filename, queue, *, sleep=3, lifetime=15, keep=False):
    with suppress(NotLockedError):
        with Lock(filename, lifetime=lifetime):
            queue.put(True)
            time.sleep(sleep)
            queue.put(True)
            # The test wants us to keep the lock a little bit longer.
            if keep:
                queue.get()


def test_retry_errno_property(lock):
    assert lock.retry_errnos == []
    lock.retry_errnos = [EMOCKEDFAILURE, EOTHERMOCKEDFAILURE]
    assert lock.retry_errnos == [EMOCKEDFAILURE, EOTHERMOCKEDFAILURE]
    del lock.retry_errnos
    assert lock.retry_errnos == []


class RetryOpen:
    def __init__(self, failure_countdown=0, retry_count=0):
        self.failure_countdown = failure_countdown
        self.retry_count = retry_count
        self._open = builtins.open
        self.errno = EMOCKEDFAILURE

    def __call__(self, *args, **kws):
        if self.failure_countdown <= 0:
            return self._open(*args, **kws)
        self.failure_countdown -= 1
        self.retry_count += 1
        raise OSError(self.errno, 'test exception')


def test_read_retries(lock):
    # Test that _read() will retry when a given expected errno is encountered.
    lock.lock()
    lock.retry_errnos = [EMOCKEDFAILURE]
    retry_open = RetryOpen(failure_countdown=3)
    with patch('builtins.open', retry_open):
        # This should trigger exactly 3 retries.
        assert lock.is_locked
    assert retry_open.retry_count == 3


def test_read_unexpected_errors(lock):
    # Test that _read() will raise when an unexpected errno is encountered.
    lock.lock()
    retry_open = RetryOpen(failure_countdown=3)
    retry_open.errno = ENINES
    with patch('builtins.open', retry_open):
        with pytest.raises(OSError) as excinfo:
            lock.is_locked
        assert excinfo.value.errno == ENINES


def test_is_locked_permission_error(lock):
    with ExitStack() as resources:
        resources.enter_context(patch('os.utime', side_effect=PermissionError))
        log_mock = resources.enter_context(patch('flufl.lock._lockfile.log'))
        assert not lock.is_locked
        log_mock.error.assert_called_once_with(
            'No permission to refresh the log')


def test_nondefault_lifetime(tmpdir):
    lock_file = os.path.join(tmpdir, 'test.lck')
    assert Lock(lock_file, lifetime=77).lifetime.seconds == 77


def test_lockfile_repr(lock):
    # Handle both POSIX and Windows paths.
    assert re.match(
        r'<Lock .*test.lck \[unlocked: \d{1,2}:\d{2}:\d{2}] pid=\d+ at .+>',
        repr(lock))
    lock.lock()
    assert re.match(
        r'<Lock .*test.lck \[locked: \d{1,2}:\d{2}:\d{2}] pid=\d+ at .+>',
        repr(lock))
    lock.unlock()
    assert re.match(
        r'<Lock .*test.lck \[unlocked: \d{1,2}:\d{2}:\d{2}] pid=\d+ at .+>',
        repr(lock))


def test_lockfile_repr_does_not_refresh(lock):
    with lock:
        expiration = lock.expiration
        time.sleep(1)
        repr(lock)
        assert lock.expiration == expiration


def test_details(lock):
    # No details are available if the lock is not locked.
    with pytest.raises(NotLockedError):
        lock.details()
    with lock:
        hostname, pid, filename = lock.details
        assert hostname == lock.hostname
        assert pid == os.getpid()
        assert Path(filename).name == 'test.lck'


def test_expiration(lock):
    with lock:
        expiration = lock.expiration
        time.sleep(1)
        lock.refresh()
        assert lock.expiration > expiration


class FailingOpen:
    def __init__(self, errno=EMOCKEDFAILURE):
        self._errno = errno

    def __call__(self, *args, **kws):
        raise OSError(self._errno, 'test exception')


def test_details_weird_open_failure(lock):
    lock.lock()
    with ExitStack() as resources:
        # Force open() to fail with our unexpected errno.
        resources.enter_context(patch('builtins.open', FailingOpen()))
        # Capture the OSError with the unexpected errno that will occur when
        # .details tries to open the lock file.
        error = resources.enter_context(pytest.raises(OSError))
        lock.details
        assert error.errno == EMOCKEDFAILURE


@contextmanager
def corrupt_open(*args, **kws):
    yield StringIO('bad claim file name')


def test_details_with_corrupt_filename(lock):
    lock.lock()
    with patch('builtins.open', corrupt_open):
        with pytest.raises(NotLockedError, match='Details are unavailable'):
            lock.details


def test_lifetime_property(lock):
    assert lock.lifetime.seconds == 15
    lock.lifetime = timedelta(seconds=31)
    assert lock.lifetime.seconds == 31
    lock.lifetime = 42
    assert lock.lifetime.seconds == 42


def test_refresh(lock):
    with pytest.raises(NotLockedError):
        lock.refresh()
    # With a lifetime parameter, the lock's lifetime is set.
    lock.lock()
    lock.refresh(31)
    assert lock.lifetime.seconds == 31
    # No exception is raised when we try to refresh an unlocked lock
    # unconditionally.
    lock.unlock()
    lock.refresh(unconditionally=True)


def test_lock_with_explicit_timeout(lock):
    queue = Queue()
    Process(target=child_locker, args=(lock.lockfile, queue)).start()
    # Wait for the child process to acquire the lock.
    queue.get()
    with pytest.raises(TimeOutError):
        lock.lock(timeout=1)


def test_lock_with_explicit_timeout_as_timedelta(lock):
    queue = Queue()
    Process(target=child_locker, args=(lock.lockfile, queue)).start()
    # Wait for the child process to acquire the lock.
    queue.get()
    with pytest.raises(TimeOutError):
        lock.lock(timeout=timedelta(seconds=1))


def test_lock_state_with_corrupt_lockfile(lock):
    # Since we're deliberately corrupting the contents of the lock file,
    # unlocking at context manager exit will not work.
    with suppress(NotLockedError):
        with lock:
            with open(lock.lockfile, 'w') as fp:
                fp.write('xxx')
            assert lock.state == LockState.unknown


def test_lock_state_on_other_host(lock):
    # Since we're going to corrupt the lock contents, ignore the exception
    # when we leave the context manager and unlock the lock.
    with suppress(NotLockedError):
        with lock:
            hostname, pid, lockfile = lock.details
            with open(lock.lockfile, 'w') as fp:
                claimfile = SEP.join((
                    lockfile,
                    # Corrupt the hostname to emulate the lock being acquired
                    # on some other host.
                    f'   {hostname}   ',
                    str(pid),
                    str(randint(0, sys.maxsize)),
                    ))
                fp.write(claimfile)
            assert lock.state == LockState.unknown


class SymlinkErrorRaiserBase:
    def __init__(self, errnos):
        self.errnos = errnos
        self.call_count = 0
        self._os_function = None

    def __call__(self, *args, **kws):
        self.call_count += 1
        if self.call_count > len(self.errnos):
            return self._os_function(*args, **kws)
        raise OSError(self.errnos[self.call_count - 1], 'test exception')


class SymlinkErrorRaiser(SymlinkErrorRaiserBase):
    def __init__(self, errnos):
        super().__init__(errnos)
        self._os_function = os.link


def test_os_link_expected_OSError(lock):
    with patch('os.link', SymlinkErrorRaiser([ENINES])):
        with pytest.raises(OSError) as excinfo:
            lock.lock()
        assert excinfo.value.errno == ENINES


def test_os_link_unexpected_OSError(lock):
    raiser = SymlinkErrorRaiser([errno.ENOENT, errno.ESTALE])
    with patch('os.link', raiser):
        lock.lock()
    # os.link() will be called 3 time; the first two will raise exceptions
    # with errnos it can handle.  The third time, goes through okay.
    assert raiser.call_count == 3


class FakeStat:
    st_nlink = 3


class LinkCountCounter:
    def __init__(self):
        self.call_count = 0
        self._os_stat = os.stat

    def __call__(self, *args, **kws):
        if self.call_count == 0:
            self.call_count += 1
            # Return a bogus link count.  This has to be an object with an
            # st_nlink attribute.
            return FakeStat()
        else:
            # Return the real link count.
            return self._os_stat(*args, **kws)


def test_unexpected_st_nlink(lock):
    queue = Queue()
    Process(target=child_locker, args=(lock.lockfile, queue)).start()
    # Wait for the child process to acquire the lock.
    queue.get()
    # Now we try to acquire the lock, which will fail.
    linkcount = LinkCountCounter()
    with patch('os.stat', linkcount):
        lock.lock()
    assert linkcount.call_count == 1


def test_unlock_unconditionally(lock):
    queue = Queue()
    Process(target=child_locker, args=(lock.lockfile, queue)).start()
    # Wait for the child process to acquire the lock.
    queue.get()
    # Try to unlock without supplying the flag; this will fail.
    with pytest.raises(NotLockedError):
        lock.unlock()
    # Try again unconditionally.  This will pass.
    lock.unlock(unconditionally=True)


class SymUnlinkErrorRaiser(SymlinkErrorRaiserBase):
    def __init__(self, errnos):
        super().__init__(errnos)
        self._os_function = os.unlink


def test_unlock_with_expected_OSError(lock):
    lock.lock()
    unlinker = SymUnlinkErrorRaiser([errno.ESTALE])
    with patch('os.unlink', unlinker):
        lock.unlock()
    # os.unlink() gets called twice.  The first one unlinks the lock file, but
    # that results in an expected errno.  The second one unlinks the claimfile.
    assert unlinker.call_count == 2


def test_unlock_with_unexpected_OSError(lock):
    lock.lock()
    unlinker = SymUnlinkErrorRaiser([ENINES])
    with patch('os.unlink', unlinker):
        with pytest.raises(OSError) as excinfo:
            lock.unlock()
        assert excinfo.value.errno == ENINES
    # os.unlink() gets called once, since the unlinking of the lockfile
    # results in an unexpected errno.
    assert unlinker.call_count == 1


def test_unlock_unconditionally_with_expected_OSError(lock):
    unlinker = SymUnlinkErrorRaiser([errno.ESTALE])
    with patch('os.unlink', unlinker):
        lock.unlock(unconditionally=True)
    # Since the lock was not acquired, os.unlink() should have been called
    # exactly once to remove the claim file.
    assert unlinker.call_count == 1


def test_unlock_unconditionally_with_unexpected_OSError(lock):
    unlinker = SymUnlinkErrorRaiser([ENINES])
    with patch('os.unlink', unlinker):
        with pytest.raises(OSError) as excinfo:
            lock.unlock(unconditionally=True)
        assert excinfo.value.errno == ENINES
    # Since the lock was not acquired, os.unlink() should have been called
    # exactly once to remove the claim file.
    assert unlinker.call_count == 1


class MtimeFailure:
    def __init__(self, stat_results):
        self._stat_results = stat_results

    def __getattr__(self, name):
        if name == 'st_mtime':
            raise OSError(ENINES, 'st_mtime failure')
        return getattr(self._stat_results, name)


class StatMtimeFailure:
    def __init__(self):
        self._os_stat = os.stat

    def __call__(self, *args, **kws):
        return MtimeFailure(self._os_stat(*args, **kws))


def test_releasetime_weird_failure(lock):
    # _releasetime() is an internal function that returns the expiration of
    # the lock, but handles error conditions.  We have to basically fail to
    # acquire a lock, don't time out, and the os_stat() of the lock file must
    # fail with an unexpected error.
    queue = Queue()
    Process(target=child_locker, args=(lock.lockfile, queue)).start()
    # Wait for the child process to acquire the lock.
    queue.get()
    # Now we try to acquire the lock, which will fail.
    with patch('os.stat', StatMtimeFailure()):
        with pytest.raises(OSError) as excinfo:
            lock.lock()
    assert excinfo.value.errno == ENINES


class NlinkFailure:
    def __init__(self, stat_results):
        self._stat_results = stat_results

    def __getattr__(self, name):
        if name == 'st_nlink':
            raise OSError(ENINES, 'st_nlink failure')
        return getattr(self._stat_results, name)


class StatNlinkFailure:
    def __init__(self):
        self._os_stat = os.stat

    def __call__(self, *args, **kws):
        return NlinkFailure(self._os_stat(*args, **kws))


def test_linkcount_weird_failure(lock):
    # _releasetime() is an internal function that returns the expiration of
    # the lock, but handles error conditions.  We have to basically fail to
    # acquire a lock, don't time out, and the os_stat() of the lock file must
    # fail with an unexpected error.
    queue = Queue()
    Process(target=child_locker, args=(lock.lockfile, queue)).start()
    # Wait for the child process to acquire the lock.
    queue.get()
    # Now we try to acquire the lock, which will fail.
    with patch('os.stat', StatNlinkFailure()):
        with pytest.raises(OSError) as excinfo:
            lock.is_locked
    assert excinfo.value.errno == ENINES


def test_lock_constructor_with_timeout(lock):
    # Pass an optional timeout value to the constructor.
    queue = Queue()
    Process(target=child_locker, args=(lock.lockfile, queue)).start()
    # Wait for the child process to acquire the lock.
    queue.get()
    with pytest.raises(TimeOutError):
        with Lock(lock.lockfile, default_timeout=1):
            pass


def test_lock_constructor_with_timeout_override(lock):
    # Explicit timeout in the lock() call overrides constructor timeout.
    queue = Queue()
    Process(target=child_locker,
            # Give the child lock a lifetime of 5 seconds.  We'll provide a
            # shorter timeout in the constructor, which should time out, but a
            # longer time in the lock() call which will result in acquiring
            # the lock when the lifetime of the child expires.
            args=(lock.lockfile, queue), kwargs=dict(sleep=3, lifetime=5),
            ).start()
    # Wait for the child process to acquire the lock.
    queue.get()
    my_lock = Lock(lock.lockfile, default_timeout=1)
    try:
        my_lock.lock(timeout=10)
        assert my_lock.is_locked
    finally:
        my_lock.unlock()


@pytest.mark.parametrize('lifetime', [1, 5])
def test_use_unrelated_existing_lockfile(lock, lifetime):
    # If someone gives a lock file that already exists, and that isn't a
    # related lock file, then trying to lock it shouldn't destroy the existing
    # file.
    #
    # https://gitlab.com/warsaw/flufl.lock/-/issues/25
    #
    # There are two cases, one where the lock's lifetime is less than the
    # timeout value and one where the lifetime is greater than the timeout
    # value.  In both cases, the expiration time should be in the past and both
    # should preserve the original (non-)lockfile.
    lock.lifetime = lifetime
    with open(lock.lockfile, 'w') as fp:
        fp.write('save me')
    # Put the lock file's release time in the past.  This has to include the
    # clock slop factor.
    past = time.time() - lifetime - CLOCK_SLOP.seconds
    os.utime(lock.lockfile, (past, past))
    with pytest.raises(TimeOutError):
        lock.lock(timeout=3)
    with open(lock.lockfile) as fp:
        assert fp.read() == 'save me'


# 2023-06-20(warsaw): On CI in Windows, we sometimes see PermissionError when
# unlocking the lock on context manager __exit__(), but only in the lock
# breaking tests.  It appears to happen when we attempt to unlink the lock
# file.
#
# [WinError 32] The process cannot access the file because it is being used
# by another process
#
# Despite the '32' there, by trial and error, it seems that the errno that
# occurs is actually 13.  I have no idea why the original error occurs, nor
# why we get this mysterious value 13, but at least on Windows, this allows CI
# to pass.
WINDOWS_CI_ERRNO = 13


def test_break_lock(lock, monkeypatch, capsys):
    queue = Queue()
    proc = Process(target=child_locker,
            # The child will acquire the lock and sleep for 5 seconds, which
            # is longer than lock's lifetime.  Once the second boolean is
            # placed in the queue, we know that the sleep has completed and
            # the lock should be ready for breakage in the parent.
            args=(lock.lockfile, queue),
            kwargs=dict(sleep=5, lifetime=3, keep=True),
            ).start()
    # Wait for the child process to acquire the lock.
    queue.get()
    child_details = lock.details
    # Wait for the child to finish sleeping.
    queue.get()
    # Now acquire the lock in the parent.  This should break the lock. See
    # above for an explanation of why we have to monkeypatch ERRORS on
    # Windows.
    if platform.system() == 'Windows':
        monkeypatch.setattr(
            'flufl.lock._lockfile.ERRORS',
            list(ERRORS) + [WINDOWS_CI_ERRNO])
    with lock:
        assert lock.is_locked
        # The child no longer has the lock.
        assert child_details != lock.details
        # Let the child exit.
        queue.put(True)


def test_break_lock_with_ununlinkable_winner(lock, monkeypatch):
    queue = Queue()
    proc = Process(target=child_locker,
            # The child will acquire the lock and sleep for 5 seconds, which
            # is longer than lock's lifetime.  Once the second boolean is
            # placed in the queue, we know that the sleep has completed and
            # the lock should be ready for breakage in the parent.
            args=(lock.lockfile, queue),
            kwargs=dict(sleep=5, lifetime=3, keep=True),
            ).start()
    # Wait for the child process to acquire the lock.
    queue.get()
    child_details = lock.details
    # Wait for the child to finish sleeping.
    queue.get()
    # Now acquire the lock in the parent.  This should break the lock.
    #
    # Count how many times os.unlink() gets called when breaking the lock.
    # The fourth call (found by trial and error) should be the attempt to
    # unlink the winner file in Lock._break().
    unlink_count = 2
    os_unlink = os.unlink
    def unlink_counter(*args, **kws):
        nonlocal unlink_count
        unlink_count -= 1
        if unlink_count > 0:
            return os_unlink(*args, **kws)
        raise OSError(ENINES, 'Bad Unlink')
    if platform.system() == 'Windows':
        monkeypatch.setattr(
            'flufl.lock._lockfile.ERRORS',
            list(ERRORS) + [WINDOWS_CI_ERRNO])
    with patch('os.unlink', unlink_counter):
        # This lock attempt will technically succeed, but it will raise an
        # exception (EMOCKEDFAILURE) during the attempt to os.unlink(winner).
        # It's coverage of that call that this test is actually after.
        with pytest.raises(OSError) as excinfo:
            lock.lock()
        assert excinfo.value.errno == ENINES
        # We still need to let the child exit.
        queue.put(True)
