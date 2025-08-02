import logging

from flufl.bounce._detectors import (
    aol,
    caiwireless,
    dsn,
    exchange,
    exim,
    groupwise,
    llnl,
    microsoft,
    netscape,
    postfix,
    qmail,
    simplematch,
    simplewarning,
    sina,
    smtp32,
    yahoo,
    yale,
    )
from public import public


log = logging.getLogger('flufl.bounce')


def _find_detectors():
    """Get all detectors in order of most specific/authoritative to least"""
    yield from [
        # RFC compliant DSNs.
        dsn.DSN,
        # Detectors for specific providers without heuristics.
        exim.Exim,
        sina.Sina,
        # Provider specific heuristic detectors.
        yahoo.Yahoo,
        yale.Yale,
        smtp32.SMTP32,
        postfix.Postfix,
        qmail.Qmail,
        groupwise.GroupWise,
        microsoft.Microsoft,
        caiwireless.Caiwireless,
        exchange.Exchange,
        netscape.Netscape,
        aol.AOL,
        # Generic and other heuristic detectors.
        simplematch.SimpleMatch,
        simplewarning.SimpleWarning,
        llnl.LLNL,
        ]


@public
def scan_message(msg):
    """Detect the set of all permanently bouncing original recipients.

    :param msg: The bounce message.
    :type msg: `email.message.Message`
    :return: The set of detected original recipients.
    :rtype: set of strings
    """
    permanent_failures = set()
    for detector_class in _find_detectors():
        log.info('Running detector: {}'.format(detector_class))
        try:
            temporary, permanent = detector_class().process(msg)
        except Exception:
            log.exception('Exception in detector: {}'.format(detector_class))
            raise
        permanent_failures.update(permanent)
        if temporary or permanent:
            break
    return permanent_failures


@public
def all_failures(msg):
    """Detect the set of all bouncing original recipients.

    :param msg: The bounce message.
    :type msg: `email.message.Message`
    :return: 2-tuple of the temporary failure set and permanent failure set.
    :rtype: (set of strings, set of string)
    """
    temporary_failures = set()
    permanent_failures = set()
    for detector_class in _find_detectors():
        log.info('Running detector: {}'.format(detector_class))
        temporary, permanent = detector_class().process(msg)
        temporary_failures.update(temporary)
        permanent_failures.update(permanent)
        if temporary or permanent:
            break
    return temporary_failures, permanent_failures
