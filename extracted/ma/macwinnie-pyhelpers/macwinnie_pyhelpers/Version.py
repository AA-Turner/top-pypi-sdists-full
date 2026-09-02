#!/usr/bin/env python3
import re


class Version:
    """
    Helper to work with [semantic versions](https://semver.org/) – e.g. comparing them.
    """

    def __init__(self, versionString, prefix=[], removePrefix=False):
        """
        Versions could be prefixed:

        * E.g when `v1.2.3` is (or can be) used, the `prefix` parameter has to be set to `v`.
        * If one has multiple options (case sensitive!), `prefix` has to be a list of all options
        * Default is an empty list
        """
        self.prefixes = []
        self.major = 0
        self.minor = 0
        self.patch = 0
        self.prefix = None
        self.given = None
        self.given = versionString
        if type(prefix) == str:
            self.prefixes = [prefix]
        elif type(prefix) == type([]):
            self.prefixes = prefix
        else:
            raise Exception("Prefixes need to be either string or list of strings!")
        if len(self.prefixes) > 0:
            prs = sorted(self.prefixes, key=len)
            prs.reverse()
            for p in prs:
                if versionString.startswith(p):
                    if not removePrefix:
                        self.prefix = p
                    versionString = versionString[len(p) :]
                    break
        vs = versionString.split(".")
        try:
            self.major, self.minor, self.patch = map(int, vs)
        except ValueError:
            vst = type(versionString)
            raise ValueError(
                f'Value "{versionString}" (type "{vst}") is not a Version string!'
            )

    def __str__(self):
        """convert current instance to version string"""
        vString = ".".join(list(map(str, [self.major, self.minor, self.patch])))
        if self.prefix != None:
            return self.prefix + vString
        else:
            return vString

    def cmpPrepare(self, other):
        """Function to prepare comparison version"""
        ot = type(other)
        if ot != Version:
            if type(other) == str:
                other = Version(other)
            else:
                raise TypeError(f'Only able to compare Versions, "{ot}" given.')
        return other

    def __eq__(self, other):
        """Defines comparison method for logical operator `==`"""
        other = self.cmpPrepare(other)
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __ne__(self, other):
        """Defines comparison method for logical operator `!=`"""
        return not (self == other)

    def __lt__(self, other):
        """Defines comparison method for logical operator `<`"""
        other = self.cmpPrepare(other)
        return (self.major < other.major) or (
            self.major == other.major
            and (
                self.minor < other.minor
                or (self.minor == other.minor and self.patch < other.patch)
            )
        )

    def __gt__(self, other):
        """Defines comparison method for logical operator `>`"""
        return not (self < other) and (self != other)

    def __le__(self, other):
        """Defines comparison method for logical operator `<=`"""
        return (self < other) or (self == other)

    def __ge__(self, other):
        """Defines comparison method for logical operator `>=`"""
        return not (self < other)

    def increase(self):
        """Increase the patch part of the current version."""
        self.patch += 1
        return str(self)

    def increaseMinor(self):
        """Increase the minor part of the current version – patch part is reset to `0`."""
        self.patch = 0
        self.minor += 1
        return str(self)

    def increaseMajor(self):
        """Increase the major part of the current version – patch and minor parts are reset to `0`."""
        self.patch = 0
        self.minor = 0
        self.major += 1
        return str(self)
