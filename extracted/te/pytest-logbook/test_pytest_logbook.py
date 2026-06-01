import pytest


pytest_plugins = 'pytester'


def test_call_report(testdir):
    testdir.makepyfile("""
        import logbook

        def test_foo():
            logbook.info('hello')
            assert 0
    """)
    result = testdir.runpytest()
    result.stdout.fnmatch_lines([
        '*Captured logbook call*',
    ])


def test_setup_report(testdir):
    testdir.makepyfile("""
        import logbook, pytest

        @pytest.fixture
        def fix():
            logbook.info('hello')
            raise Exception('oops')

        def test_foo(fix):
            pass
    """)
    result = testdir.runpytest()
    result.stdout.fnmatch_lines([
        '*Captured logbook setup*',
    ])


def test_teardown_report(testdir):
    testdir.makepyfile("""
        import logbook, pytest

        @pytest.fixture
        def fix(request):
            def fin():
                logbook.info('hello')
                raise Exception('oops')
            request.addfinalizer(fin)

        def test_foo(fix):
            pass
    """)
    result = testdir.runpytest()
    result.stdout.fnmatch_lines([
        '*Captured logbook teardown*',
    ])


def test_fixture(testdir):
    testdir.makepyfile("""
        import logbook, pytest

        @pytest.fixture
        def fix(request):
            logbook.info('setup')
            request.addfinalizer(lambda: logbook.info('teardown'))

        def test_foo(fix, loghandler):
            logbook.info('test')
            assert isinstance(loghandler, logbook.TestHandler)
            assert len(loghandler.records) == 1
            assert loghandler.records[0].message == 'test'
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_fixture_in_class(testdir):
    testdir.makepyfile("""
        import logbook

        class TestFoo:
            def test_foo(self, loghandler):
                logbook.info('test')
                assert loghandler.has_info('test')
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)

def test_fixture_setup(testdir):
    testdir.makepyfile("""
        import logbook, pytest

        @pytest.fixture
        def fix():
            logbook.info('setup')

        def test_foo(fix, loghandler_setup):
            logbook.info('test')
            assert isinstance(loghandler_setup, logbook.TestHandler)
            assert len(loghandler_setup.records) == 1
            assert loghandler_setup.records[0].message == 'setup'
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_fixture_teardown(testdir):
    testdir.makepyfile("""
        import logbook, pytest

        @pytest.fixture
        def fix(request, loghandler_teardown):
            def fin():
                logbook.info('teardown')
                assert len(loghandler_teardown.records) == 1
                assert loghandler_teardown.records[0].message == 'teardown'
            request.addfinalizer(fin)

        def test_foo(fix):
            logbook.info('test')
    """)
    result = testdir.runpytest()
    result.stdout.fnmatch_lines([
        '*1 passed in*',
    ])


def test_stdlib_redir(testdir):
    testdir.makepyfile("""
        import logging

        def test_foo(loghandler):
            logging.info('hello')
            assert loghandler.records[0].message == 'hello'
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_disable_stdlib_redir(testdir):
    testdir.makeini("""
        [pytest]
        logbook_stdlib = false
    """)
    testdir.makepyfile("""
        import logging

        def test_foo(loghandler):
            logging.info('hello')
            assert len(loghandler.records) == 0
    """)
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(passed=1)


def test_stack_unclean(testdir):
    testdir.makepyfile("""
        import logbook

        def test_foo():
            handler = logbook.TestHandler()
            handler.push_application()
    """)
    result = testdir.runpytest_subprocess()
    for line in result.stdout.lines:
        assert 'INTERNALERROR' not in line
