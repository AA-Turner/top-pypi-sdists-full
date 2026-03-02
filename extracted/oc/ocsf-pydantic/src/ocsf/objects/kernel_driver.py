from pydantic import BaseModel

from .file import File


class KernelExtension(BaseModel):
    """
    The Kernel Extension object describes a kernel driver that has been loaded or
    unloaded into the operating system (OS) kernel. Defined by D3FEND <a
    target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:KernelModule/'>d
    3f:KernelModule</a>.
    """

    file: File # The driver/extension file object.

