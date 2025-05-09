import os
import re
import string
from functools import lru_cache
from typing import Optional
from typing import Pattern

from detect_secrets.plugins.base import BasePlugin
from detect_secrets.plugins.base import RegexBasedDetector


def is_sequential_string(secret: str) -> bool:
    sequences = (
        # Base64 letters first
        (
            string.ascii_uppercase +
            string.ascii_uppercase +
            string.digits +
            '+/'
        ),

        # Base64 numbers first
        (
            string.digits +
            string.ascii_uppercase +
            string.ascii_uppercase +
            '+/'
        ),

        # We don't have a specific sequence for alphabetical
        # sequences, since those will happen to be caught by the
        # base64 checks.

        # Alphanumeric sequences
        (string.digits + string.ascii_uppercase) * 2,

        # Capturing any number sequences
        string.digits * 2,

        string.hexdigits.upper() + string.hexdigits.upper(),
        string.ascii_uppercase + '=/',
    )

    uppercase = secret.upper()
    return any(uppercase in sequential_string for sequential_string in sequences)


def is_potential_uuid(secret: str) -> bool:
    match = _get_uuid_regex().search(secret)
    if not match:
        return False

    return match.group() == secret


@lru_cache(maxsize=1)
def _get_uuid_regex() -> Pattern:
    return re.compile(
        r'[a-f0-9]{8}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{4}\-[a-f0-9]{12}',
        re.IGNORECASE,
    )


def is_likely_id_string(secret: str, line: str, plugin: Optional[BasePlugin] = None) -> bool:
    try:
        index = line.index(secret)
    except ValueError:
        return False

    return (not plugin or not isinstance(plugin, RegexBasedDetector)) \
        and bool(_get_id_detector_regex().search(line, pos=0, endpos=index))


@lru_cache(maxsize=1)
def _get_id_detector_regex() -> Pattern:
    """
    Regex Details:
    ^(id|myid|userid) -> Common id identifiers with no prefix
    _id               -> id identifier with prefixes allowed
    s?                -> Optional plural id identifier
    [^a-z0-9]         -> Non-letter/numeric character
    """
    return re.compile(r'(^(id|myid|userid)|_id)s?[^a-z0-9]', re.IGNORECASE)


def is_non_text_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext in IGNORED_FILE_EXTENSIONS


# We don't scan files with these extensions.
# Note: We might be able to do this better with
#       `subprocess.check_output(['file', filename])`
#       and look for "ASCII text", but that might be more expensive.
#
#       Definitely something to look into, if this list gets unruly long.
IGNORED_FILE_EXTENSIONS = {
    '.7z',
    '.bin',
    '.bmp',
    '.bz2',
    '.class',
    '.css',
    '.dmg',
    '.doc',
    '.eot',
    '.exe',
    '.gif',
    '.gz',
    '.ico',
    '.iml',
    '.ipr',
    '.iws',
    '.jar',
    '.jpg',
    '.jpeg',
    '.lock',
    '.map',
    '.mo',
    '.pdf',
    '.png',
    '.prefs',
    '.psd',
    '.rar',
    '.realm',
    '.s7z',
    '.sum',
    '.svg',
    '.tar',
    '.tif',
    '.tiff',
    '.ttf',
    '.webp',
    '.woff',
    '.xls',
    '.xlsx',
    '.zip',
    '.resx',
    '.bim',
    '.mdl',
    '.slx',
    '.hex',
    '.srec',
    '.mot',
    '.csa',
    '.fls',
    '.fl2',
    '.fl3',
    '.fl4',
    '.dll',
    '.dll.deploy',
    '.nupkg',
}


def is_templated_secret(secret: str) -> bool:
    """
    Filters secrets that are shaped like: {secret}, <secret>, or ${secret}.
    """
    try:
        if (
            (secret[0] == '{' and secret[-1] == '}')
            or (secret[0] == '<' and secret[-1] == '>')
            or (secret[0] == '$' and secret[1] == '{' and secret[-1] == '}')
        ):
            return True
    except IndexError:
        # Any one character secret (that causes this to raise an IndexError) is highly
        # likely to be a false positive (or if a true positive, INCREDIBLY weak password).
        return True

    return False


def is_prefixed_with_dollar_sign(secret: str) -> bool:
    # NOTE: This is broken out into its own function since it has more chance of increasing
    # false negatives than `is_templated_secret` (e.g. secrets that actually start with a $).
    # This is best used with files that actually use this as a means of referencing variables.
    # TODO: More intelligent filetype handling?
    if len(secret) > 0 and secret[0] == '$':
        return True
    return False


def is_indirect_reference(line: str) -> bool:
    """
    Filters secrets that take the form of:

        secret = get_secret_key()

    or

        secret = request.headers['apikey']
    """
    # Constrain line length as the heuristic's intention is to target lines that resemble
    # function calls. The constraint avoids catastrophic backtracking failures of the regex.
    if len(line) > 1000:
        return False
    return bool(_get_indirect_reference_regex().search(line))


@lru_cache(maxsize=1)
def _get_indirect_reference_regex() -> Pattern:
    # Regex details:
    #   ([^\v=!:]*)     ->  Something before the assignment or comparison
    #   \s*             ->  Some optional whitespaces
    #   (:=?|[!=]{1,3}) ->  Assignment or comparison: :=, =, ==, ===, !=, !==
    #   \s*             ->  Some optional whitespaces
    #   (
    #       [\w.-]+     ->  Some alphanumeric character, dot or -
    #       [\[\(]      ->  Start of indirect reference: [ or (
    #       [^\v]*      ->  Something except line breaks
    #       [\]\)]      ->  End of indirect reference: ] or )
    #   )
    return re.compile(r'([^\v=!:]*)\s*(:=?|[!=]{1,3})\s*([\w.-]+[\[\(][^\v]*[\]\)])')


def is_lock_file(filename: str) -> bool:
    return os.path.basename(filename) in {
        'Brewfile.lock.json',
        'Cartfile.resolved',
        'composer.lock',
        'Gemfile.lock',
        'Package.resolved',
        'package-lock.json',
        'Podfile.lock',
        'yarn.lock',
        'Pipfile.lock',
        'poetry.lock',
        'Cargo.lock',
        'packages.lock.json',
        'pnpm-lock.yaml',
        'mix.lock',
        'pubspec.lock',
        'go.sum',
        'gradle.lockfile',
        'cabal.project.freeze',
        'stack.yaml.lock',
        'conan.lock',
    }


def is_not_alphanumeric_string(secret: str) -> bool:
    """
    This assumes that secrets should have at least ONE letter in them.
    This helps avoid clear false positives, like `*****`.
    """
    return not bool(set(string.ascii_letters) & set(secret))


def is_swagger_file(filename: str) -> bool:
    """
    Filters swagger files and paths, like swagger-ui.html or /swagger/.
    """
    return bool(_get_swagger_regex().search(filename))


@lru_cache(maxsize=1)
def _get_swagger_regex() -> Pattern:
    return re.compile(r'.*swagger.*')


def is_aws_arn(secret: str) -> bool:
    """
    Filters AWS ARN strings that match the pattern:
    arn:aws:<service>:<region>:<account-id>:<resource-type>:<resource-name>
    """
    return bool(_get_arn_regex().search(secret))


@lru_cache(maxsize=1)
def _get_arn_regex() -> Pattern:
    return re.compile(
        r'^arn:aws:[a-z0-9\-]+:([a-z0-9\-]*:[0-9]{12}|:[0-9]{12}|\*)?:.*$',
    )
