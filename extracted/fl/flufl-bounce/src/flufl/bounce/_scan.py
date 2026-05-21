import logging

from public import public

from flufl.bounce.interfaces import BounceDetector, Recipients
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


log = logging.getLogger('flufl.bounce')


# Detectors are run in order of most specific/authoritative to least.
_DETECTORS: list[type[BounceDetector]] = [
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
def scan_message(msg) -> Recipients:
    """Detect the set of all permanently bouncing original recipients.

    :param msg: The bounce message.
    :type msg: `email.message.Message`
    :return: The set of detected original recipients.
    """
    permanent_failures: set[bytes] = set()
    for detector_class in _DETECTORS:
        log.info(f'Running detector: {detector_class}')
        try:
            temporary, permanent = detector_class().process(msg)
        except Exception:
            log.exception(f'Exception in detector: {detector_class}')
            raise
        permanent_failures.update(permanent)
        if temporary or permanent:
            break
    return frozenset(permanent_failures)


@public
def all_failures(msg) -> tuple[Recipients, Recipients]:
    """Detect the set of all bouncing original recipients.

    :param msg: The bounce message.
    :type msg: `email.message.Message`
    :return: 2-tuple of the temporary failure set and permanent failure set.
    """
    temporary_failures: set[bytes] = set()
    permanent_failures: set[bytes] = set()
    for detector_class in _DETECTORS:
        log.info(f'Running detector: {detector_class}')
        temporary, permanent = detector_class().process(msg)
        temporary_failures.update(temporary)
        permanent_failures.update(permanent)
        if temporary or permanent:
            break
    return frozenset(temporary_failures), frozenset(permanent_failures)
