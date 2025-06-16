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
import linecache
import logging
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from setuptools import archive_util
import zc.buildout
from ..utils import is_true, rmtree, EnvironMixin, Shared
from ..downloadunpacked import unpack_archive

def readElfAsDict(f):
  """Reads ELF information from file"""
  result = subprocess.check_output(('readelf', '-d', f),
                                   stderr=subprocess.STDOUT)[0]
  library_list = []
  rpath_list = []
  runpath_list = []
  for l in result.split('\n'):
    if '(NEEDED)' in l:
      library_list.append(l.split(':')[1].strip(' []'))
    elif '(RPATH)' in l:
      rpath_list = [q.rstrip('/') for q in l.split(':', 1)[1].strip(' []'
        ).split(':')]
    elif '(RUNPATH)' in l:
      runpath_list = [q.rstrip('/') for q in l.split(':', 1)[1].strip(' []'
        ).split(':')]
  if len(runpath_list) == 0:
    runpath_list = rpath_list
  elif len(rpath_list) != 0 and runpath_list != rpath_list:
    raise ValueError('RPATH and RUNPATH are different.')
  return dict(
    library_list=sorted(library_list),
    runpath_list=sorted(runpath_list)
  )

def call(*args, **kwargs):
  """Subprocess call with closed file descriptors and stdin"""
  kwargs.update(
    stdin=subprocess.PIPE,
    close_fds=True)
  popen = subprocess.Popen(*args, **kwargs)
  popen.stdin.close()
  popen.stdin = None
  popen.communicate()
  if popen.returncode != 0:
    raise subprocess.CalledProcessError(popen.returncode, ' '.join(args[0]))

def guessworkdir(path):
  x = os.listdir(path)
  return os.path.join(path, *x) if len(x) == 1 else path

GLOBALS = (lambda *x: {x.__name__: x for x in x})(
  call, guessworkdir, is_true)

class Script(EnvironMixin):
  """Free script building system"""
  def _checkPromise(self, promise_key, location):
    promise_text = self.options.get(promise_key)
    if promise_text is None:
      return True
    promise_problem_list = []
    a = promise_problem_list.append
    for promise in promise_text.split('\n'):
      promise = promise.strip()
      if not promise:
        continue
      if promise.startswith('file:') or promise.startswith('statlib'):
        s, path = promise.split(':')
        if not os.path.exists(os.path.join(location, path)):
          a('File promise not met for %r' % path)
      elif promise.startswith('directory'):
        s, path = promise.split(':')
        if not os.path.isdir(os.path.join(location, path)):
          a('Directory promise not met for %r' %
              path)
      elif promise.startswith('dynlib:'):
        if 'linked:' not in promise:
          raise zc.buildout.UserError('dynlib promise requires \'linked:\' '
            'parameter.')
        if 'rpath:' not in promise:
          rpath_list = []
        for promise_part in promise.split():
          if promise_part.startswith('dynlib:'):
            s, path = promise_part.split(':')
          elif promise_part.startswith('linked:'):
            s, link_list = promise_part.split(':')
            link_list = link_list.split(',')
          elif promise_part.startswith('rpath:'):
            s, rpath_list = promise_part.split(':')
            if rpath_list:
              r = rpath_list
              rpath_list = []
              for q in r.split(','):
                if q.startswith('!'):
                  q = q.replace('!', location)
                rpath_list.append(q)
            else:
              rpath_list = []
        if not os.path.exists(os.path.join(location, path)):
          a('Dynlib promise file not met %r' % promise)
        else:
          elf_dict = readElfAsDict(os.path.join(location, path))
          if sorted(link_list) != sorted(elf_dict['library_list']):
            a('Promise library list not met (wanted: %r, found: %r)' % (
              link_list, elf_dict['library_list']))
          if sorted(rpath_list) != sorted(elf_dict['runpath_list']):
            a('Promise rpath list not met (wanted: %r, found: %r)' % (
              rpath_list, elf_dict['runpath_list']))
      else:
        raise zc.buildout.UserError('Unknown promise %r' % promise)
    if len(promise_problem_list):
      raise zc.buildout.UserError('Promise not met, found issues:\n  %s\n' %
          '\n  '.join(promise_problem_list))

  def download(self, *args, **kw):
    if not (args or 'url' in kw):
        args = self.options['url'], self.options.get('md5sum') or None
    offline = kw.pop('offline', None)
    path, is_temp = zc.buildout.download.Download(self.buildout['buildout'],
      hash_name=True, **({} if offline is None else {'offline': offline})
      )(*args, **kw)
    if is_temp:
      self.cleanup_list.append(path)
    return path

  def extract(self, path):
    extract_dir = tempfile.mkdtemp(self.name)
    self.cleanup_list.append(extract_dir)
    self.logger.debug('Created working directory: %s', extract_dir)
    unpack_archive(self, path, extract_dir)
    return extract_dir

  def pipeCommand(self, command_list_list, *args, **kwargs):
    """Allows to do shell like pipes (|)"""
    subprocess_list = []
    previous = None
    kwargs['stdout'] = subprocess.PIPE
    run_list = []
    for command_list in command_list_list:
      if previous is not None:
        kwargs['stdin'] = previous.stdout
      p = subprocess.Popen(command_list, *args, **kwargs)
      if previous is not None:
        previous.stdout.close()
      command = ' '.join(command_list)
      subprocess_list.append((p, command))
      run_list.append(command)
      previous = p
    self.logger.info('Running: %s', ' | '.join(run_list))
    failed = [command
      for p, command in reversed(subprocess_list)
      if p.wait()]
    if failed:
      raise zc.buildout.UserError('Failed while running:\n  '
        + '\n  '.join(failed))

  def copyTree(self, origin, destination, ignore_dir_list=()):
    """Recursively Copy directory.

    ignore_dir_list is a list of relative directories you want to exclude.
    Example :
    copytree("/from", "/to", ignore_dir_list=["a_private_dir"])
    """
    # Check existence before beginning. We don't want to cleanup something
    # that does not belong to us.
    if os.path.exists(destination):
      raise shutil.Error('Destination already exists: %s' % destination)
    self.logger.info("Copying %r to %r", origin, destination)
    try:
      shutil.copytree(origin, destination, symlinks=True,
                      ignore=lambda src, names: ignore_dir_list)
    except:
      self.cleanup_list.append(destination)
      raise

  cleanup_dir_list = cleanup_file_list = property(
    lambda self: self.cleanup_list)

  def __init__(self, buildout, name, options):
    self.options = options
    self.buildout = buildout
    self.name = name
    missing = True
    keys = 'init', 'install', 'update'
    for option in keys:
      script = options.get(option)
      setattr(self, '_' + option, script)
      if script:
        missing = False
    if missing:
      raise zc.buildout.UserError(
        'at least one of the following option is required: ' + ', '.join(keys))
    if is_true(self.options.get('keep-on-error')):
      self.logger.debug('Keeping directories in case of errors')
      self.keep_on_error = True
    else:
      self.keep_on_error = False
    EnvironMixin.__init__(self, False)
    shared = Shared(buildout, name, options)
    if self._update:
      shared.assertNotShared("option 'update' can't be set")
    if self._install:
      if not options.get('location'):
        options['location'] = shared.location
      if self._init:
        self._exec(self._init)
      if shared.location != options['location']:
        shared.assertNotShared("option 'location' can't be set")
        shared.location = options['location']
      shared.keep_on_error = True
      shared.mkdir_location = False
      self._shared = shared
    else:
      shared.assertNotShared("option 'install' must be set")
      if self._init:
        self._exec(self._init)

  def _exec(self, script):
    options = self.options
    g = dict(GLOBALS, self=self, options=options)
    try:
      g['location'] = options['location']
    except KeyError:
      pass
    linecache.cache[self.name] = (
        len(script),
        None,
        script.splitlines(),
        self.name,
    )
    code = compile(script, self.name, 'exec')
    exec(code, g)

  def install(self):
    if self._install:
      shared = self._shared
      if shared.location:
        return self._shared.install(self.__install)
      self._exec(self._install)
    else:
      self.update()
    return ()

  def __install(self):
    location = self.options['location']
    self.cleanup_list = []
    try:
      self._exec(self._install)
      self._checkPromise('slapos_promise', location)
    except:
      self.cleanup_list.append(location)
      raise
    finally:
      for path in self.cleanup_list:
        if os.path.lexists(path):
          if self.keep_on_error:
            self.logger.info('Left %r as requested', path)
          else:
            self.logger.debug('Removing %r', path)
            rmtree(path)

  def update(self):
    if self._update:
      self._exec(self._update)

  def applyPatchList(self, patch_string, patch_options=None, patch_binary=None, cwd=None):
    if patch_string is not None:
      if patch_options is None:
        patch_options = []
      else:
        patch_options = shlex.split(patch_options)
      if patch_binary is None:
        patch_binary = 'patch'
      else:
        patch_binary = patch_binary.strip()
      kwargs = dict()
      if cwd is not None:
        kwargs['cwd'] = cwd
      for patch in patch_string.splitlines():
        patch = patch.strip()
        if patch:
          if ' ' in patch:
            patch, md5sum = patch.split(' ', 1)
            md5sum = md5sum.strip()
            if md5sum.lower() == 'unknown':
              md5sum = None
          else:
            md5sum = None
          if md5sum is not None and ' ' in md5sum:
            md5sum, patch_options = md5sum.split(' ', 1)
            patch_options = patch_options.split(' ')
          self.logger.info('Applying patch %r', patch)
          with open(self.download(patch, md5sum)) as stdin:
            subprocess.check_call([patch_binary] + patch_options,
                                  stdin=stdin, **kwargs)
