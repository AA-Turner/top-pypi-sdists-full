"""Keep local account identifiers out of source distributions."""
import os
from pathlib import Path
import tarfile
import tempfile

from setuptools import setup
from setuptools.command.sdist import sdist


class AnonymousSdist(sdist):
    def make_archive(self, base_name, format, *args, **kwargs):
        archive = super().make_archive(base_name, format, *args, **kwargs)
        if self.dry_run:
            return archive
        # The release format is gztar; fail rather than silently leak owners.
        if format != "gztar":
            raise ValueError("source releases require the gztar format")
        destination = Path(archive)
        with tempfile.TemporaryDirectory(dir=destination.parent) as temporary:
            cleaned = Path(temporary) / destination.name
            with tarfile.open(destination, "r:gz") as source:
                with tarfile.open(cleaned, "w:gz") as output:
                    for member in source:
                        member.uid = member.gid = 0
                        member.uname = member.gname = ""
                        for key in ("uid", "gid", "uname", "gname"):
                            member.pax_headers.pop(key, None)
                        if member.isfile():
                            with source.extractfile(member) as content:
                                output.addfile(member, content)
                        else:
                            output.addfile(member)
            os.replace(cleaned, destination)
        return archive


setup(cmdclass={"sdist": AnonymousSdist})
