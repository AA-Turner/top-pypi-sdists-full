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
import errno
import os
from zc.buildout import download, UserError
from .utils import is_true, Shared

class Recipe(object):

  _shared = None

  def __init__(self, buildout, name, options):
    self._buildout = buildout['buildout']
    self._url = options['url']
    self._alternate = options.get('alternate-url')
    self._md5sum = options.get('md5sum') or None
    offline = options.get('offline')
    self._offline = is_true(offline) if offline else None
    # 'mode' option was dropped; don't reimplement it
    # an 'executable' boolean option may be acceptable
    if 'mode' in options:
      raise UserError("option 'mode' not supported")

    shared = Shared(buildout, name, options)
    if not self._md5sum:
      shared.assertNotShared("option 'md5sum' must be set")

    destination = options.get('destination')
    if destination:
      shared.assertNotShared("option 'destination' can't be set")
    else:
      self._shared = shared
      filename = options.get('filename')
      destination = os.path.join(shared.location,
        # filename may be used to also construct source-related options
        # and we have values that start with a subfolder
        os.path.basename(filename) if filename else name)
      # Compatibility with other recipes: expose location
      options['location'] = shared.location
    options['target'] = self._destination = destination

  def install(self):
    shared = self._shared
    if shared:
      return shared.install(self._download)
    destination = self._destination
    try:
      os.remove(destination)
    except OSError as e:
      if e.errno != errno.ENOENT:
        raise
    self._download()
    return [destination]

  def _download(self):
    offline = self._offline
    kw = {} if offline is None else {'offline': offline}
    dl = download.Download(self._buildout, hash_name=True, **kw)
    alternate = self._alternate
    kw = {'alternate_url': alternate} if alternate else {}
    path, is_temp = dl(self._url, self._md5sum, self._destination, **kw)
    assert path == self._destination and not is_temp, (
      "SlapOS buildout >= 2.7.1+slapos014 needed")

  def update(self):
    if not self._md5sum:
      self._download()
