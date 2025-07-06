#!/usr/bin/env python3

# ------------------------------------------------------------------------------
# Copyright (C) 2018, 2020, 2021 Maximilian Stahlberg
#
# This file is part of PICOS Release Scripts.
#
# PICOS Release Scripts are free software: you can redistribute them and/or
# modify them under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# PICOS Release Scripts are distributed in the hope that they will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

"""Produce version strings for PICOS."""

import datetime
import re
from os import devnull
from pathlib import Path
from subprocess import check_output

VERSION_FILE = Path(__file__).parent / Path("picos", ".version")
CHANGELOG_FILE = Path("CHANGELOG.rst")

# Version lengthes.
SHORT = 0
MEDIUM = 1
MEDIUM_OR_SHORT = 2
LONG = 3


def _file_version_tuple():
    """Report the version stored in the version file as an integer tuple.

    :returns:
        A tuple ``(MINOR, MAJOR)`` or ``(MINOR, MAJOR, PATCH)``.
    """
    with VERSION_FILE.open() as file:
        version = tuple(int(x) for x in file.read().strip().split("."))

    if len(version) not in (2, 3):
        raise RuntimeError("Invalid version file format.")

    return version


def _git_version_tuple():
    """Report the version as reported by git as a tuple.

    :returns:
        A tuple ``()`` or ``(MINOR, MAJOR, PATCH, HASH)`` where all of
        ``MINOR``, ``MAJOR`` and ``PATCH`` and where ``HASH`` is a string.
    """
    try:
        with open(devnull, "w") as DEVNULL:
            mm, p, h = (
                check_output(
                    ["git", "describe", "--long", "--match", "v*"],
                    stderr=DEVNULL,
                )
                .decode("ascii")
                .strip()
                .lstrip("v")
                .split("-")
            )
    except Exception:
        return ()
    else:
        return tuple(int(x) for x in mm.split(".")) + (int(p), h)


def _version_tuple():
    """Report a version tuple that is consistent between version file and git.

    :returns:
        A tuple ``(MINOR, MAJOR)`` or ``(MINOR, MAJOR, PATCH)`` or ``(MINOR,
        MAJOR, PATCH, HASH)`` where all of ``MINOR``, ``MAJOR`` and ``PATCH``
        are integers and where ``HASH`` is a string.
    """
    f = _file_version_tuple()
    g = _git_version_tuple()

    common = min(len(f), len(g))
    if any(f[i] != g[i] for i in range(common)):
        raise RuntimeError(
            "The file version {} and the git version {} are in "
            "conflict.".format(
                ".".join(str(x) for x in f), ".".join(str(x) for x in g)
            )
        )

    version = f[:common] + (f[common:] if len(f) >= len(g) else g[common:])

    if len(version) < 2 or len(version) > 4:
        raise RuntimeError("Invalid version file or git version format.")

    return version


def get_version(length=MEDIUM_OR_SHORT, patchPrefix=".", hashPrefix="+"):
    """Report a version string that is consistent between version file and git.

    :param int length:
        Level of detail.

    :param str patchPrefix:
        String to prefix the PATCH bit with.

    :param str hashPrefix:
        String to prefix the HASH bit with.
    """
    version = _version_tuple()

    string = "{}.{}".format(*version[:2])

    if length != SHORT:
        if len(version) < 3:
            if length == MEDIUM_OR_SHORT:
                return string
            else:
                raise RuntimeError("Only a short version is available.")

        string += "{}{}".format(patchPrefix, version[2])

        if length == LONG:
            if len(version) < 4:
                raise RuntimeError("The commit hash is not available.")

            string += "{}{}".format(hashPrefix, version[3])

    return string


def get_base_version():
    """Report the version in the MAJOR.MINOR format."""
    return get_version(SHORT)


def get_full_version():
    """Report the version in the MAJOR.MINOR.PATCH format."""
    return get_version(MEDIUM)


def get_commit_count():
    """Report number of commits since the last release."""
    version = _version_tuple()

    if len(version) < 3:
        raise RuntimeError(
            "The number of commits since the last release is not available."
        )

    return version[2]


def get_commit_hash():
    """Report the hash of git's HEAD commit."""
    version = _version_tuple()

    if len(version) < 4:
        raise RuntimeError("The commit hash is not available.")

    return version[3]


def get_version_info():
    """Report the version in the format of Python's __version_info__ tuple."""
    return _version_tuple()[:3]


def _repository_is_dirty():
    """Report whether the repository has uncomitted changed."""
    description = check_output(["git", "describe", "--dirty"]).decode("ascii")
    return "dirty" in description


def _bump_changelog(baseVersion):
    with CHANGELOG_FILE.open() as logFile:
        log = logFile.read()

    log, count = re.subn(
        r".. _Unreleased: (.*)master",
        r".. _{0}: \g<1>v{0}".format(baseVersion),
        log,
    )

    if count != 1:
        raise Exception(
            "There is no 'Unreleased' link definition in the changelog."
        )

    log, count = re.subn(
        r"`Unreleased`_",
        "`{}`_ - {}".format(baseVersion, datetime.date.today()),
        log,
    )

    if count != 1:
        raise Exception("There is no 'Unreleased' header in the changelog.")

    with CHANGELOG_FILE.open("w") as logFile:
        logFile.write(log)


def bump_version(*parts):
    """Prepare the release of a new version."""
    for number in parts:
        if type(number) is not int:
            raise TypeError("Version number parts must be int.")

    if _repository_is_dirty():
        raise Exception("You can only bump version in a non-dirty repository.")

    version = ".".join(["{}".format(x) for x in parts])
    if len(parts) == 2:
        major, minor = parts
    else:
        raise Exception("Version format must be MAJOR.MINOR.")

    oldMajor, oldMinor = _version_tuple()[:2]

    notNewer = False
    if major < oldMajor:
        notNewer = True
    elif major == oldMajor:
        if minor < oldMinor:
            notNewer = True

    if notNewer:
        raise Exception(
            "The proposed version of {} is not newer than the "
            "current version of {}.{}.".format(version, oldMajor, oldMinor)
        )

    print("Relabling the 'Unreleased' section in the changelog.")
    _bump_changelog(version)

    print("Writing to version file.")
    with VERSION_FILE.open("w") as versionFile:
        versionFile.write("{}\n".format(version))

    print("Commiting to git.")
    check_output(["git", "add", VERSION_FILE, CHANGELOG_FILE])
    check_output(["git", "commit", "-m", "Bump version to {}.".format(version)])

    print("The following commit has been made:")
    print("-" * 35)
    print(check_output(["git", "show", "-U0"]).decode("ascii").strip())
    print("-" * 35)

    print("Creating an annotated git tag.")
    check_output(
        [
            "git",
            "tag",
            "-a",
            "v{}".format(version),
            "-m",
            "Release of version {}.".format(version),
        ]
    )

    print("Verifying that version file and git tag version match.")
    _ = _version_tuple()

    print("\nAll set. Execute 'git push --follow-tags' to push the release!")


if __name__ == "__main__":
    import argparse

    def version(str):
        """Load a parameter as a version tuple."""
        return tuple(int(x) for x in str.lstrip("v").split("."))

    # fmt: off
    parser = argparse.ArgumentParser(description="PICOS version manager. "
        "When making a proper release, merge into 'master', then bump the "
        "version with this script BEFORE pushing to 'origin/master' "
        "(with --follow-tags).")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--test", action="store_true",
        help="verify that file and git versions match")
    group.add_argument("-b", "--bump", metavar="VER", type=version,
        help="bump version to VER = MAJOR.MINOR")
    group.add_argument("-s", "--short", action="store_true",
        help="print base version as MAJOR.MINOR")
    group.add_argument("-m", "--medium", action="store_true",
        help="print full version as MAJOR.MINOR.PATCH")
    group.add_argument("-f", "--flexible", action="store_true",
        help="like --medium if possible, else like --short (default)")
    group.add_argument("-l", "--long", action="store_true",
        help="print an extended full version with the commit hash")
    group.add_argument("-c", "--commit", action="store_true",
        help="print the current commit short hash")
    group.add_argument("--aur", action="store_true",
        help="same as --long -r '.r' -a '.'")
    group.add_argument("--pep", action="store_true",
        help="same as --flexible -r '.post'")

    parser.add_argument("-p", "--prefix", metavar="STR", type=str,
        default="", help="prefix for the base version")
    parser.add_argument("-r", "--patch-prefix", metavar="STR", type=str,
        default=".", help="prefix for PATCH (or revision) part")
    parser.add_argument("-a", "--hash-prefix", metavar="STR", type=str,
        default="+", help="prefix for the commit hash")
    # fmt: on

    args = parser.parse_args()

    if args.aur:
        args.short, args.flexible, args.medium, args.long = (
            False,
            False,
            False,
            True,
        )
        args.patch_prefix = ".r"
        args.hash_prefix = "."
    elif args.pep:
        args.short, args.flexible, args.medium, args.long = (
            False,
            True,
            False,
            False,
        )
        args.patch_prefix = ".post"

    version = None
    versionArgs = {
        "patchPrefix": args.patch_prefix,
        "hashPrefix": args.hash_prefix,
    }

    if args.test:
        _ = _version_tuple()
    elif args.short:
        version = get_version(SHORT, **versionArgs)
    elif args.medium:
        version = get_version(MEDIUM, **versionArgs)
    elif args.long:
        version = get_version(LONG, **versionArgs)
    elif args.commit:
        print(get_commit_hash())
    elif args.bump:
        bump_version(*args.bump)
    else:  # either args.flexible or none
        version = get_version(MEDIUM_OR_SHORT, **versionArgs)

    if version is not None:
        print(args.prefix + version)
