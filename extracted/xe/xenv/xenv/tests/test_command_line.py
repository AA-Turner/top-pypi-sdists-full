import sys
import xenv


def setup():
    xenv.__version__ = 'test-version'


def test_version():
    try:
        from StringIO import StringIO
    except ImportError:  # this is Python 3
        from io import StringIO
    sys.stdout = StringIO()
    sys.stderr = StringIO()

    try:
        xenv.Script(prog='xenv', args=['--version']).main()
        assert False, 'the script should have exited'
    except SystemExit as x:
        if sys.version_info >= (3, ):
            out = sys.stdout.getvalue()
        else:
            out = sys.stderr.getvalue()

        assert x.code == 0
        assert out == 'xenv test-version\n'
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


def test_command_args():
    s = xenv.Script(args=['command'])
    assert s.args.actions == []
    assert s.args.command == ['command']

    s = xenv.Script(args=['-s', 'VAR=Value', 'command'])
    assert s.args.actions == [('set', ('VAR', 'Value'))]
    assert s.args.command == ['command']

    s = xenv.Script(args=['-s', 'VAR=Value', 'command', 'arg1'])
    assert s.args.actions == [('set', ('VAR', 'Value'))]
    assert s.args.command == ['command', 'arg1']

    s = xenv.Script(args=['-s', 'VAR=Value', 'command', 'arg1', '$VAR'])
    assert s.args.actions == [('set', ('VAR', 'Value'))]
    assert s.args.command == ['command', 'arg1', '$VAR']

    s = xenv.Script(
        args=['-s', 'VAR=Value', 'command', '--command-option', 'opt'])
    assert s.args.actions == [('set', ('VAR', 'Value'))]
    assert s.args.command == ['command', '--command-option', 'opt']
