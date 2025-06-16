##############################################################################
#
# Copyright (c) 2010 Vifib SARL and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
import contextlib
import os
import subprocess
import tarfile
import tempfile
from functools import partial
from setuptools import archive_util
from .utils import is_true, EnvironMixin, Shared

class Recipe(EnvironMixin):

  def __init__(self, buildout, name, options):
    self.buildout = buildout
    self.name = name
    self.options = options
    self._strip = is_true(options.get('strip-top-level-dir'), None)
    self._url = options['url']

    shared = Shared(buildout, name, options)
    destination = options.get('destination')
    if destination:
      shared.assertNotShared("option 'destination' can't be set")
      shared.location = destination
    self._shared = shared
    # backward compatibility with other recipes -- expose location
    options['location'] = \
    options['target'] = shared.location

    EnvironMixin.__init__(self, True)

  def install(self):
    return self._shared.install(self._install)

  def _install(self):
    # WKRD: do not import at module-level because of circular imports
    #       inside slapos.buildout (see networkcache support)
    from zc.buildout import download
    location = self._shared.location
    offline = self.options.get('offline')
    kw = {'offline': is_true(offline)} if offline else {}
    dl = download.Download(self.buildout['buildout'], hash_name=True, **kw)
    alternate = self.options.get('alternate-url')
    kw = {'alternate_url': alternate} if alternate else {}
    path, is_temp = dl(self._url, self.options.get('md5sum') or None, **kw)
    try:
      unpack_archive(self, path, location)
    finally:
      if is_temp:
        os.unlink(path)

    strip = self._strip
    if strip is None:
      a = os.listdir(location)
      if len(a) != 1:
        return
      a = os.path.join(location, *a)
      if not os.path.isdir(a):
        return
    elif strip:
      a, = os.listdir(location)
      a = os.path.join(location, a)
    else:
      return
    b = os.path.join(location, os.path.basename(tempfile.mktemp(dir=a)))
    os.rename(a, b)
    for a in os.listdir(b):
      os.rename(os.path.join(b, a), os.path.join(location, a))
    os.rmdir(b)

  def update(self):
    pass


def unpack_archive(recipe, *args):
  # Monkey patch to keep symlinks in tarfile
  def unpack_tarfile_patched(filename, extract_dir,
                             progress_filter=archive_util.default_filter):
    """Unpack tar/tar.gz/tar.bz2 `filename` to `extract_dir`

    Raises ``UnrecognizedFormat`` if `filename` is not a tarfile (as determined
    by ``tarfile.open()``).  See ``unpack_archive()`` for an explanation
    of the `progress_filter` argument.
    """
    try:
        tarobj = tarfile.open(filename)
    except tarfile.TarError:
        # ad-hoc support for .xz and .lz archive
        with open(filename, 'rb') as f:
            hdr = f.read(6)
        for magic, cmd in ((b'\xfd7zXZ\x00', ('xzcat',)),
                           (b'LZIP', ('lunzip', '-c'))):
            if hdr.startswith(magic):
                with tempfile.NamedTemporaryFile() as uncompressed_archive:
                    subprocess.check_call(cmd + (filename,),
                        stdout=uncompressed_archive, env=recipe.environ)
                    unpack_archive(uncompressed_archive.name,
                                   extract_dir, progress_filter)
                return True
        raise archive_util.UnrecognizedFormat(
            "%s is not a compressed or uncompressed tar file" % (filename,)
        )
    with contextlib.closing(tarobj):
        # don't do any chowning!
        tarobj.chown = lambda *args: None
        for member in tarobj:
            name = member.name
            # don't extract absolute paths or ones with .. in them
            if not name.startswith('/') and '..' not in name.split('/'):
                prelim_dst = os.path.join(extract_dir, *name.split('/'))

                if member is not None and (member.isfile() or member.isdir() or member.islnk() or member.issym()):
                    # Prepare the link target for makelink().
                    if member.islnk():
                        member._link_target = os.path.join(extract_dir, member.linkname)
                    final_dst = progress_filter(name, prelim_dst)
                    if final_dst:
                        if final_dst.endswith(os.sep):
                            final_dst = final_dst[:-1]
                        try:
                            # XXX Ugh
                            tarobj._extract_member(member, final_dst)
                        except tarfile.ExtractError:
                            # chown/chmod/mkfifo/mknode/makedev failed
                            pass
        return True

  unpack_archive = partial(archive_util.unpack_archive,
    drivers = archive_util.extraction_drivers[:2] + (unpack_tarfile_patched,))
  return unpack_archive(*args)
