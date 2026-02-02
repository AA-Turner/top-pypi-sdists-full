"""
Reference parsing utilities for Kodexa object references.
"""
from typing import Optional


class Ref:
    """
    A class to represent a reference to a Kodexa object.

    Attributes
    ----------
    ref : str
        a string reference
    version : str, optional
        a version of the reference, default is None
    resource : str, optional
        a resource of the reference, default is None
    slug : str
        a slug of the reference, default is an empty string
    org_slug : str
        an organization slug of the reference, default is an empty string
    object_ref : str
        a formatted string of the reference

    Methods
    -------
    __init__(self, ref: str)
        Constructs all the necessary attributes for the Ref object.
    """

    def __init__(self, ref: str):
        self.ref: str = ref
        first_part = ref
        self.version: Optional[str] = None
        self.resource: Optional[str] = None
        self.slug: str = ""
        self.org_slug: str = ""

        if ":" in ref:
            (first_part, self.version) = ref.split(":")

            if "/" in self.version:
                (self.version, self.resource) = self.version.split("/")

        (self.org_slug, self.slug) = first_part.split("/")

        self.object_ref = (
            f"{self.org_slug}/{self.slug}:{self.version}"
            if self.version
            else f"{self.org_slug}/{self.slug}"
        )
