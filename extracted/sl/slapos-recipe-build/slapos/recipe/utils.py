import errno, json, logging, os, stat
from hashlib import md5
from zc.buildout import UserError
from zc.buildout.rmtree import rmtree as buildout_rmtree

def generatePassword(length=8):
  from random import SystemRandom
  from string import ascii_lowercase
  choice = SystemRandom().choice
  return ''.join(choice(ascii_lowercase) for _ in range(length))

def is_true(value, default=False):
  return default if value is None else ('false', 'true').index(value)

def make_read_only(path):
  st_mode = os.lstat(path).st_mode
  if not stat.S_ISLNK(st_mode):
    os.chmod(path, st_mode & 0o555)

def make_read_only_recursively(path):
  make_read_only(path)
  for root, dir_list, file_list in os.walk(path): # PY3: speed up with os.fwalk
    for dir_ in dir_list:
      make_read_only(os.path.join(root, dir_))
    for file_ in file_list:
      make_read_only(os.path.join(root, file_))

def rmtree(path):
  try:
    buildout_rmtree(path)
  except OSError as e:
    if e.errno == errno.ENOENT:
      return
    if e.errno != errno.ENOTDIR:
      raise
    os.remove(path)


class EnvironMixin(object):

  def __init__(self, allow_none=True):
    environment = self.options.get('environment')
    if environment:
      if '=' in environment:
        self._environ = env = {}
        for line in environment.splitlines():
          line = line.strip()
          if line:
            try:
              k, v = line.split('=', 1)
            except ValueError:
              raise UserError('Line %r in environment is incorrect' % line)
            k = k.rstrip()
            if k in env:
              raise UserError('Key %r is repeated' % k)
            env[k] = v.lstrip()
      else:
        self._environ = self.buildout[environment]
    else:
      self._environ = None if allow_none else {}

  def __getattr__(self, attr):
    if attr == 'logger':
      value = logging.getLogger(self.name)
    elif attr == 'environ':
      env = self._environ
      del self._environ
      if env is None:
        value = None
      else:
        from os import environ
        value = environ.copy()
        for k in sorted(env):
          value[k] = v = env[k] % environ
          self.logger.info('[ENV] %s = %s', k, v)
    else:
      return self.__getattribute__(attr)
    setattr(self, attr, value)
    return value


class Shared(object):

  keep_on_error = False
  mkdir_location = True
  signature = None

  def __init__(self, buildout, name, options):
    self.maybe_shared = shared = is_true(options.get('shared'))
    if shared:
      # Trigger computation of part signature for shared signature.
      # From now on, we should not pull new dependencies.
      # Ignore if buildout is too old.
      options.get('__buildout_signature__')
      shared = buildout['buildout'].get('shared-part-list')
      if shared:
        profile_base_location = options.get('_profile_base_location_')
        signature = json.dumps({
          k: (v.replace(profile_base_location, '${:_profile_base_location_}')
              if profile_base_location else v)
          for k, v in options.items()
          if k != '_profile_base_location_'
        }, ensure_ascii=False, indent=2, sort_keys=True,
          # BBB: Python 2 ( https://bugs.python.org/issue16333 )
          separators=(',', ': '))
        if not isinstance(signature, bytes): # BBB: Python 3
          signature = signature.encode()
        digest = md5(signature).hexdigest()
        shared_list = []
        for shared in shared.splitlines():
          shared = shared.strip().rstrip('/')
          if shared:
            location = os.path.join(shared, name, digest)
            if os.path.exists(location):
              share_msg = 'shared at %s (already built)'
              break
            shared_list.append((shared, location))
        else:
          for shared, location in shared_list:
            if os.access(shared, os.W_OK):
              share_msg = 'will be shared at %s (needs to build)'
              break
          else:
            location = None
        if location:
          self.logger = logging.getLogger(name)
          self.logger.info(share_msg, location)
          self.location = location
          self.signature = signature
          return
    self.location = os.path.join(buildout['buildout']['parts-directory'], name)

  def assertNotShared(self, reason):
    if self.maybe_shared:
      raise UserError("When shared=true, " + reason)

  def install(self, install):
    signature = self.signature
    location = self.location
    if signature is not None:
      path = os.path.join(location, '.buildout-shared.json')
      if os.path.exists(path):
        self.logger.info('shared part is already installed')
        return ()
    rmtree(location)
    try:
      if self.mkdir_location:
        os.makedirs(location)
      else:
        parent = os.path.dirname(location)
        if parent and not os.path.isdir(parent):
          os.makedirs(parent)
      install()
      try:
        s = os.stat(location)
      except OSError as e:
        if e.errno != errno.ENOENT:
          raise
        raise UserError('%r was not created' % location)
      if self.maybe_shared and not stat.S_ISDIR(s.st_mode):
        raise UserError('%r is not a directory' % location)
      if signature is None:
        return [location]
      tmp = path + '.tmp'
      with open(tmp, 'wb') as f:
        f.write(signature)
      os.rename(tmp, path)
    except:
      if not self.keep_on_error:
        rmtree(location)
      raise
    make_read_only_recursively(location)
    return ()
