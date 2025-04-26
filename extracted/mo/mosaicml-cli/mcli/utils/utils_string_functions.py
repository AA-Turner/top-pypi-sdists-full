""" Utils for string validation for user input """
import logging
import re
import string
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

from mcli.api.exceptions import MCLIRunConfigValidationError
from mcli.utils.utils_interactive import ValidationError

MAX_KUBERNETES_LENGTH = 63
RUN_CONFIG_UID_LENGTH = 6
MAX_RUN_NAME_LENGTH = MAX_KUBERNETES_LENGTH - \
    RUN_CONFIG_UID_LENGTH - 1  # -1 for the dash

logger = logging.getLogger(__name__)


def clean_run_name(run_name: Optional[str]) -> str:
    if run_name is None:
        raise MCLIRunConfigValidationError('A run name must be provided using the keyword [bold]name[/]')

    name_validation = validate_rfc1123_name(text=run_name)
    if name_validation.valid:
        return run_name

    if len(run_name) > MAX_RUN_NAME_LENGTH:
        return run_name  # mapi will throw an error for this, don't issue two warnings

    # TODO: Figure out why logging strips out regex []
    # (This is a rich formatting thing. [] is used to style text)
    new_run_name = ensure_rfc1123_compatibility(run_name)

    logger.warning(f'Invalid run name "{run_name}": Run names must contain only lower-case letters, '
                   f'numbers, or "-". Converting to a valid name: {new_run_name}')
    return new_run_name


@dataclass
class StringVerificationResult():
    """ Used to return the result of a string verification

    Overrides __len__ to be truthy based on validity
    Overrides __eq__ to cast when being compared to bools
    """
    valid: bool
    message: Optional[str]

    def __bool__(self) -> bool:
        return self.valid

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, bool):
            return bool(self) == __o
        return super().__eq__(__o)


def rfc_verification(
    text: str,
    length: int,
    special_characters: str,
    start_alnum_verification: bool = True,
    end_alnum_verification: bool = True,
    allow_uppercase: bool = False,
) -> StringVerificationResult:
    """Does General RFC Verification with Parameters

    Args:
        text: The text to verify
        length: The maximum length allowed for the string
        special_characters: Regex Escaped Special Characters to
        start_alnum_verification: The first character must be an alnum
        end_alnum_verification: The last character must be an alnum
        allow_uppercase: Allow uppercase characters

    Returns:
        Returns a truthy StringVerificationResult with possible error messages
    """
    if not text:
        return StringVerificationResult(
            False,
            'Name cannot be empty',
        )

    if len(text) > length:
        return StringVerificationResult(
            False,
            f'Name must be less than {length} characters',
        )

    if allow_uppercase:
        alnum = 'a-zA-Z0-9'
    else:
        alnum = 'a-z0-9'
    valid_characters = f'^[{alnum}{special_characters}]*'

    if re.fullmatch(valid_characters, text) is None:
        valid = "".join([
            string.ascii_lowercase, string.ascii_uppercase if allow_uppercase else '', string.digits, special_characters
        ])
        return StringVerificationResult(
            False,
            f'Invalid value {repr(text)}. Valid characters only include [{valid}]',
        )

    if start_alnum_verification and not text[0].isalnum():
        return StringVerificationResult(
            False,
            'The first character must be alphanumeric',
        )
    if end_alnum_verification and not text[-1].isalnum():
        return StringVerificationResult(
            False,
            'The last character must be alphanumeric',
        )

    return StringVerificationResult(True, None)


def ensure_rfc_compatibility(
    text: str,
    length: int,
    special_characters: str,
    start_alnum_verification: bool = True,
    end_alnum_verification: bool = True,
    alnum_pad: str = '1',
    special_replacement: str = '-',
) -> str:

    invalid_characters = f'[^a-z0-9{special_characters}]'
    repl = re.subn(invalid_characters, special_replacement, text.lower())[0]
    repl = repl[:length]
    if repl == '':
        return repl

    if start_alnum_verification and not repl[0].isalnum():
        repl = alnum_pad + repl[:-len(alnum_pad)]

    if end_alnum_verification and not repl[-1].isalnum():
        repl = repl[:-len(alnum_pad)] + alnum_pad

    return repl


def validate_rfc1123_name(text: str) -> StringVerificationResult:
    """
    A check on text validity based on k8s rfc1123 spec

        contain at most 63 characters
        contain only lowercase alphanumeric characters or '-'
        start with an alphanumeric character
        end with an alphanumeric character
    """
    return rfc_verification(text=text, length=MAX_KUBERNETES_LENGTH, special_characters=r'\-')


def ensure_rfc1123_compatibility(text: str) -> str:
    """
    Ensures that names are valid based on k8s rfc1123 spec
    """
    return ensure_rfc_compatibility(
        text=text,
        length=MAX_KUBERNETES_LENGTH,
        special_characters=r'\-',
    )


def validate_dns_subdomain_name(text: str) -> StringVerificationResult:
    """
    Ensures that secret names are valid based on k8s rfc1123 spec


        contain no more than 253 characters
        contain only lowercase alphanumeric characters, '-' or '.'
        start with an alphanumeric character
        end with an alphanumeric character
    """
    return rfc_verification(text=text, length=253, special_characters=r'\-\.')


def validate_secret_name(secret_name: str) -> StringVerificationResult:
    """
    Ensures that secret names are valid based on k8s spec

        contain no more than 253 characters
        contain only lowercase alphanumeric characters, '-' or '.'
        start with an alphanumeric character
        end with an alphanumeric character
    """

    return validate_dns_subdomain_name(text=secret_name)


def validate_api_plaintext(api_plaintext: str) -> bool:
    """Ensure a plaintext api key for the MosaicML platform is valid

    See https://github.com/mosaicml/mcloud/blob/dev/mapi/src/graphql/apikey/controller/ApiKeyController.ts
    """
    if api_plaintext.startswith('test.mosaicml'):
        # Testing API key may be valid, so let it pass
        return True

    if len(api_plaintext) != 47:
        raise ValidationError(f'API key should be 47 characters long. Current length: {len(api_plaintext)}')

    valid = rfc_verification(
        text=api_plaintext,
        length=47,
        special_characters=r'\-_~\+/\.',
        allow_uppercase=True,
        end_alnum_verification=False,
    )
    if not valid:
        raise ValidationError(valid.message)

    return True


def validate_absolute_path(path: str) -> bool:
    """Ensures that the given path is an absolute path

    Args:
        path: File path

    Returns:
        True if path is absolute
    """

    return Path(path).is_absolute()


def validate_existing_filename(filename: str) -> bool:
    """Ensures that the given filename exists

    Args:
        filename: File path

    Returns:
        True if file exists and is a file
    """
    path = Path(filename).expanduser().absolute()
    return path.exists() and path.is_file()


def validate_existing_directory(directory: str) -> bool:
    """Ensures that the given filename exists

    Args:
        directory: Directory path

    Returns:
        True if directory exists and is a directory
    """
    path = Path(directory).expanduser().absolute()
    return path.exists() and path.is_dir()


def validate_url(url: str) -> bool:
    """Validate that `url` is a valid URL

    Args:
        url: URL

    Returns:
        True if url is valid
    """

    return urlparse(url) is not None


def validate_email_address(email: str) -> bool:
    """Validate that `email` is a valid email address

    Args:
        email: Email address

    Returns:
        True if the email address is valid
    """

    pattern = r'^[^@]*@.*\..*$'
    return re.fullmatch(pattern, email) is not None


KEY_PATTERN = r'^([a-zA-Z_][a-zA-Z0-9_]*)$'
KEY_VALUE_PATTERN = r'^([a-zA-Z_][a-zA-Z0-9_]*)=(.*)'


def validate_env_key(name: str) -> bool:
    """Validate that a string is a valid environment variable

    Args:
        name: Environment variable name

    Returns:
        True of name is valid
    """

    return re.fullmatch(KEY_PATTERN, name) is not None


def validate_key_value_pair(key_value_str: str) -> bool:
    """Validate that a string is of the form KEY=VALUE

    Args:
        key_value_str: String of the form KEY=VALUE

    Returns:
        True if string is valid
    """
    return re.fullmatch(KEY_VALUE_PATTERN, key_value_str) is not None


def is_glob(text: str) -> bool:
    """Returns True if the provided string uses contains characters for glob-style patterns
    """
    glob_chars = r'[*?\[\]!]'
    return re.findall(glob_chars, text) != []


def snake_case_to_camel_case(text: str, capitalize_first: bool = False) -> str:
    """Converts snake_case 🐍 to camelCase 🐪

    Args:
        text: snake case string to convert
        capitalize_first: If true, will capitalize first character

    Returns:
        text in camel case

    Example
    >>> snake_case_to_camel_case("foo_bar")
    "fooBar"
    >>> snake_case_to_camel_case("foo_bar", capitalize_first=True)
    "FooBar"
    """
    converted_text = ''.join(word.title() for word in text.split('_'))
    if capitalize_first:
        return converted_text

    return converted_text[0].lower() + converted_text[1:]


def camel_case_to_snake_case(text: str) -> str:
    """Converts camelCase 🐪 to snake_case 🐍

    Args:
        text: camel case string to convert

    Returns:
        text in snake case

    Example
    >>> camel_case_to_snake_case("fooBar")
    "foo_bar"
    """
    text = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', text).lower()


def docker_image_to_repo_tag(image: str) -> Tuple[str, str]:
    """Disect repo and tag name from the image name
    """
    image, *potential_tag = image.split(':')

    if potential_tag:
        tag = potential_tag[0]
    else:
        tag = 'latest'

    return image, tag


def validate_image(image: str) -> bool:
    """Validate that a string is a valid docker image name

    Args:
        image: image name

    Returns:
        True if image is valid
    """
    if not image:
        return False

    # See https://docs.docker.com/engine/reference/commandline/tag/

    # An image name is made up of slash-separated name components,
    # optionally prefixed by a registry hostname. The hostname must
    # comply with standard DNS rules, but may not contain underscores.
    # If a hostname is present, it may optionally be followed by a port
    # number in the format :8080. If not present, the command uses
    # Docker’s public registry located at registry-1.docker.io by default
    host = r'[a-z0-9\.\-]+(?P<port>\:[0-9]+)?'

    # Name components may contain lowercase letters, digits and separators.
    # A separator is defined as a period, one or two underscores, or one or
    # more dashes. A name component may not start or end with a separator.
    name = r'[a-z0-9]([a-z0-9\-\._]*[a-z0-9])?'

    # A tag name must be valid ASCII and may contain lowercase and uppercase
    # letters, digits, underscores, periods and dashes. A tag name may not
    # start with a period or a dash and may contain a maximum of 128 characters.
    tag = r'\:[\w_][\w\-\._]{0,127}'
    digest = r'@[\w\:]+'

    regex = rf'(?P<host>{host}\/)?(?P<path>{name})(?P<paths>\/{name})*(?P<tag_or_digest>({tag}|{digest}))?'
    return re.fullmatch(regex, image, flags=re.A) is not None
