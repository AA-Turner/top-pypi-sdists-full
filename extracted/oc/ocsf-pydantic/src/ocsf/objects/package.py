from pydantic import BaseModel

class SoftwarePackage(BaseModel):
    """
    The Software Package object describes details about a software package. Defined
    by D3FEND <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:Sof
    twarePackage/'>d3f:SoftwarePackage</a>.
    """

    name: str # The software package name.
    version: str # The software package version.

    # Recommended:
    architecture: str | None = None

    # Optional:
    epoch: int | None = None
    license: str | None = None # The software license applied to this package.
    purl: str | None = None
    release: str | None = None
