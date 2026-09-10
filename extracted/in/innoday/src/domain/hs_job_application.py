"""Job applications submitted to Haviland Software's own site.

**Why this lives in InnoDay's database rather than Pixelfuel's.** The
`job_applications` table in the Pixelfuel Supabase project is shared with
`pixelfuel-website`, which upserts on `email` alone -- so an applicant who had
already applied to Pixelfuel would have that row overwritten, name, role,
resume and all, with no history. The two companies recruit the same people, so
that is the expected outcome rather than an edge case. A table of our own,
prefixed `hs_`, has no such coupling and needs no coordinated migration in
somebody else's repository.

**The resume is stored as bytes, deliberately and temporarily.** The API has no
object storage today, and a hiring form that cannot take a PDF is worse than
one that keeps a few megabytes in Postgres. At this volume -- applications, not
telemetry -- that is fine, and it is a smaller change than standing up a bucket.
The columns are grouped at the end and never selected by the listing queries,
so moving them to S3 later is a migration and a read-path change, nothing more.
"""

import secrets
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON, Column, LargeBinary, Text
from sqlmodel import Field

from src.domain._base import TimestampMixin

#: What the form offers. The old Pixelfuel route also accepted `salesperson`,
#: which no UI ever presented -- it is left out until something asks for it.
VALID_JOB_ROLES = (
    "software_developer",
    "data_scientist",
    "marketing_design_specialist",
    "project_product_manager",
)

VALID_DEGREES = ("high_school", "associates", "bachelors", "masters", "phd")
VALID_EXPERIENCE = ("junior", "professional", "experienced")

MESSAGE_MIN_CHARS = 100
MESSAGE_MAX_CHARS = 700
MAX_RESUME_BYTES = 5 * 1024 * 1024
ALLOWED_RESUME_TYPES = (
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
)


class HSJobApplication(TimestampMixin, table=True):
    """One application, as submitted. Nothing here is edited by the applicant."""

    __tablename__ = "hs_job_applications"

    id: str = Field(default_factory=lambda: secrets.token_urlsafe(16), primary_key=True)

    # Unique within this table only. A second application from the same address
    # is refused rather than allowed to replace the first, so nobody's
    # submission disappears silently.
    email: str = Field(index=True, unique=True, max_length=320)
    name: str = Field(max_length=200)

    job_role: str = Field(index=True, max_length=64)
    highest_degree: str = Field(max_length=32)
    years_experience: str = Field(max_length=32)

    about_message: str = Field(sa_column=Column(Text, nullable=False))

    #: Chosen technologies, and the same list in the order the applicant ranked
    #: them. Two fields because the set and the ranking answer different
    #: questions, and the ranking is the one worth reading first.
    technologies: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    proficiency_order: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    github_url: Optional[str] = Field(default=None, max_length=500)
    linkedin_url: Optional[str] = Field(default=None, max_length=500)

    #: Whatever the verification checks concluded at submission time, kept as
    #: submitted rather than re-derived: it records what was known then.
    verification: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    status: str = Field(default="NEW", max_length=32)

    # --- the resume, and the only wide columns here. See the module docstring.
    resume_filename: Optional[str] = Field(default=None, max_length=300)
    resume_content_type: Optional[str] = Field(default=None, max_length=120)
    resume_bytes: Optional[bytes] = Field(
        default=None, sa_column=Column(LargeBinary, nullable=True)
    )
