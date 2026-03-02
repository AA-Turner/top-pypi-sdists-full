from .user import User

from .remediation import Remediation

from pydantic import BaseModel
from .file import File


class AffectedCode(BaseModel):
    """
    The Affected Code object describes details about a code block identified as
    vulnerable.
    """

    file: File # Details about the file that contains the affected code block.

    # Recommended:
    end_line: int | None = None
    start_line: int | None = None

    # Optional:
    owner: User | None = None # Details about the user that owns the affected file.
    remediation: Remediation | None = None
