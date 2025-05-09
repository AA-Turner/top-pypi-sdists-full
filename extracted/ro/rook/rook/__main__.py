import sys
import six
import traceback


def rook_test():
    six.print_("[Rookout] Testing connection to agent")

    if '-v' in sys.argv:
        from rook.config import LoggingConfiguration

        LoggingConfiguration.LOG_LEVEL = "DEBUG"
        LoggingConfiguration.LOG_TO_STDERR = True

    from rook.config import AgentComConfiguration
    AgentComConfiguration.TIMEOUT = AgentComConfiguration.PING_TIMEOUT + 1

    try:
        import rook

        rook.start(throw_errors=True)
        success = True
    except:  # lgtm[py/catch-base-exception]
        six.print_(file=sys.stderr)
        traceback.print_exc()
        six.print_(file=sys.stderr)

        success = False

    if success:
        six.print_("[Rookout] Test Finished Successfully")
        exit(0)
    else:
        six.print_("[Rookout] Test Failed")
        exit(1)


if '__main__' == __name__:
    rook_test()
