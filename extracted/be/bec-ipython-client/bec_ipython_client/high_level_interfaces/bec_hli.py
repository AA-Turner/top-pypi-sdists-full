from bec_lib.scan_report import ScanReport

# pylint:disable=undefined-variable
# pylint: disable=too-many-arguments


def umv(*args) -> ScanReport:
    """Updated absolute move (i.e. blocking) for one or more devices.

    Returns:
        ScanReport: Status object.

    Examples:
        >>> umv(dev.samx, 1)
        >>> umv(dev.samx, 1, dev.samy, 2)
    """
    return scans.umv(*args, relative=False)


def umvr(*args) -> ScanReport:
    """Updated relative move (i.e. blocking) for one or more devices.

    Returns:
        ScanReport: Status object.

    Examples:
        >>> umvr(dev.samx, 1)
        >>> umvr(dev.samx, 1, dev.samy, 2)
    """
    return scans.umv(*args, relative=True)


def mv(*args) -> ScanReport:
    """Absolute move for one or more devices.

    Returns:
        ScanReport: Status object.

    Examples:
        >>> mv(dev.samx, 1)
        >>> mv(dev.samx, 1, dev.samy, 2)
    """
    return scans.mv(*args, relative=False)


def mvr(*args) -> ScanReport:
    """Relative move for one or more devices.

    Returns:
        ScanReport: Status object.

    Examples:
        >>> mvr(dev.samx, 1)
        >>> mvr(dev.samx, 1, dev.samy, 2)
    """
    return scans.mv(*args, relative=True)
