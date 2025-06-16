import doctest
import os
import re
import shutil
import tarfile
import tempfile
import unittest
from contextlib import contextmanager
from copy import deepcopy
from functools import wraps
from subprocess import check_call, check_output, CalledProcessError, STDOUT

import zc.buildout.testing
from zc.buildout.download import check_md5sum, ChecksumError
from zc.buildout.testing import buildoutTearDown
from zope.testing import renormalizing

from .. import download, downloadunpacked, gitclone
from ..utils import make_read_only_recursively


optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

GIT_REPOSITORY = 'https://lab.nexedi.com/nexedi/slapos.recipe.build.git'
BAD_GIT_REPOSITORY = 'http://git.erp5.org/repos/nowhere'

def setUp(test):
  # XXX side effect. Disable libnetworkcache because buildout testing
  # infrastructure doesn't support offline install of external egg "forced"
  # into itself.
  zc.buildout.buildout.LIBNETWORKCACHE_ENABLED = False

  zc.buildout.testing.buildoutSetUp(test)
  zc.buildout.testing.install_develop('slapos.recipe.build', test)

@contextmanager
def chdir(path):
  old = os.getcwd()
  try:
    os.chdir(path)
    yield old
  finally:
    os.chdir(old)

def with_buildout(wrapped):
  def wrapper(self):
    self.globs = {}
    setUp(self)
    try:
      wrapped(self, **self.globs)
    finally:
      buildoutTearDown(self)
  return wraps(wrapped)(wrapper)


class TestCase(unittest.TestCase):

  def setUp(self):
    self.dir = os.path.realpath(tempfile.mkdtemp())
    self.addCleanup(shutil.rmtree, self.dir)
    self.parts_directory_path = os.path.join(self.dir, 'test_parts')
    self.buildout = {
        'buildout': {
            'parts-directory': self.parts_directory_path,
            'directory': self.dir,
         }
    }

  def makeGitCloneRecipe(self, options={}):
    options.setdefault('repository', GIT_REPOSITORY)
    return gitclone.Recipe(self.buildout, "working_copy", options)


class DownloadTests(TestCase):

  def test_hardlink(self):
    filename = 'setup.py'
    v0 = '0.50~'
    h0 = '3365d85985af7421eff978b09682d0c8'
    v1 = '0.50'
    h1 = '6673e2f48d641d516f78cbddb281608e'
    options = {'revision': v0}
    self.makeGitCloneRecipe(options).install()
    working_copy = options['location']
    url = os.path.join(working_copy, filename)
    options = {
      'url': url,
      'md5sum': h0,
      'filename': filename,
    }
    download.Recipe(self.buildout, v0, options).install()
    p0 = options['target']
    self.assertTrue(os.path.samefile(p0, url))
    check_call(('git', 'checkout', v1), cwd=working_copy)
    self.assertFalse(os.path.samefile(p0, url))
    options['md5sum'] = h1
    download.Recipe(self.buildout, v1, options).install()
    p1 = options['target']
    self.assertTrue(check_md5sum(p0, h0))
    self.assertTrue(check_md5sum(p1, h1))
    self.assertTrue(os.path.samefile(p1, url))
    open(p1, 'w').close()
    self.assertRaises(ChecksumError,
      download.Recipe(self.buildout, 'fail', options).install)

  @with_buildout
  def test_offline(self, write, start_server, **kw):
    data = 'bar'
    foo = os.path.join(self.dir, 'foo')
    write(foo, data)
    url = start_server(self.dir) + 'foo'
    def check(Recipe, target):
      def check(offline_error, buildout_offline=None, options_offline=None):
        buildout = deepcopy(self.buildout)
        if buildout_offline:
          buildout['buildout']['offline'] = buildout_offline
        options = {'url': url}
        if options_offline:
          options['offline'] = options_offline
        try:
          Recipe(buildout, 'offline', options).install()
        except zc.buildout.UserError:
          if not offline_error:
            raise
        else:
          self.assertFalse(offline_error)
          with open(target(options)) as f:
            self.assertEqual(f.read(), data)
      check(False)
      check(False, 'false')
      check(True,  'true')
      check(False, None, 'false')
      check(True,  None, 'true')
      check(False, 'true', 'false')
      check(True,  'false', 'true')
    check(download.Recipe, lambda options: options['target'])
    with tarfile.open(os.path.join(foo + '.tar'), 'w') as tar:
      tar.add(foo, 'foo')
    url += '.tar'
    check(downloadunpacked.Recipe, lambda options:
        os.path.join(options['target'], 'foo'))


class GitCloneNonInformativeTests(TestCase):

  def setUpParentRepository(self):
    """
    This function sets ups repositories for parent repo and adds file and commit
    to it.
    """
    # Create parent and submodule directory
    self.project_dir = os.path.join(self.dir, 'main_repo')
    os.mkdir(self.project_dir)

    # Add files and folder in parent repo and initialize git in it
    check_call(['git', 'init', '--initial-branch', 'main'], cwd=self.project_dir)
    self.setUpGitConfig(self.project_dir)
    os.mkdir(os.path.join(self.project_dir, 'dir1'))
    self.touch(self.project_dir, 'file1.py')
    self.gitAdd(self.project_dir)
    self.gitCommit(self.project_dir, msg='Add file and folder in main repo')

  def setUpSubmoduleRepository(self):
    """
    This function sets up repositories and config for parent repo and a
    submodule repo and create small commits as well as links the 2 repos.
    """
    # Create parent and submodule directory
    self.submodule_dir = os.path.join(self.dir ,'submodule_repo')
    os.mkdir(self.submodule_dir)

    # Add files in submodule repo and initialize git in it
    check_call(['git', 'init', '--initial-branch', 'main'], cwd=self.submodule_dir)
    self.setUpGitConfig(self.submodule_dir)
    self.touch(self.submodule_dir, 'file1.py')
    self.gitAdd(self.submodule_dir)
    self.gitCommit(self.submodule_dir, msg='Add file1 in submodule repo')

  def attachSubmoduleToParent(self):
    """
    Adds the submodule repo to parent repo and creates a commit in parent if
    parent and submodule repo are present.
    """
    assert hasattr(self, 'project_dir') and hasattr(self, 'submodule_dir'), (
      "Make sure parent repo and submodule repo are present")
    submodule_dir_main_repo = os.path.join(self.project_dir, 'dir1')
    # Add submodule to main repo and commit
    check_call(
      ['git', '-c', 'protocol.file.allow=always', 'submodule', 'add', self.submodule_dir],
      cwd=submodule_dir_main_repo)
    self.gitCommit(self.project_dir, msg='Add submodule repo')

  def createRepositoriesAndConnect(self):
    """
    Creates parent and submodule repository and then adds the submodule repo to
    parent repo and creates a commit in parent.
    """
    self.setUpParentRepository()
    self.setUpSubmoduleRepository()
    self.attachSubmoduleToParent()

  def tearDown(self):
    for var in list(os.environ):
      if var.startswith('SRB_'):
        del os.environ[var]

  def setUpGitConfig(self, proj_dir):
    """
    Setup user and email for given git repository
    """
    check_call(['git', 'config', 'user.email', 'test@example.com'], cwd=proj_dir)
    check_call(['git', 'config', 'user.name', 'Test'], cwd=proj_dir)

  def gitOutput(self, *args, **kw):
    return check_output(('git',) + args, universal_newlines=True, **kw)

  def gitAdd(self, proj_dir):
    """runs a 'git add .' in the provided git repo
    :param proj_dir:    path to a git repo
    """
    check_call(['git', 'add', '.'], cwd=proj_dir)

  def gitCommit(self, proj_dir, msg):
    """runs a 'git commit -m msg' in the provided git repo
    :param proj_dir:  path to a git repo
    """
    check_call(['git', 'commit', '-m', msg], cwd=proj_dir)

  def getRepositoryHeadCommit(self, proj_dir):
    """
    Returns the sha of HEAD of a git repo
    """
    return self.gitOutput('rev-parse', 'HEAD', cwd=proj_dir).rstrip()

  def touch(self, *parts):
    os.close(os.open(os.path.join(*parts), os.O_CREAT, 0o666))

  def readFile(self, *parts):
    with open(os.path.join(*parts), 'r') as f:
      return f.read()

  def checkLocalChanges(self, parent_local_change_path,
                        submodule_local_change_path):
    # Check if the file are created at the expected position and check contents
    self.assertTrue(os.path.exists(parent_local_change_path))
    self.assertTrue(os.path.exists(submodule_local_change_path))
    self.assertEqual(self.readFile(parent_local_change_path), 'foo')
    self.assertEqual(self.readFile(submodule_local_change_path), 'bar')

  def test_using_download_cache_if_git_fails(self):
    recipe = self.makeGitCloneRecipe({"use-cache": "true",
                                      "repository": BAD_GIT_REPOSITORY})
    with chdir(self.dir), \
         self.assertRaises(zc.buildout.UserError) as cm:
      recipe.install()
    self.assertEqual(str(cm.exception), gitclone.GIT_CLONE_CACHE_ERROR_MESSAGE)

  def test_not_using_download_cache_if_forbidden(self):
    recipe = self.makeGitCloneRecipe({"repository": BAD_GIT_REPOSITORY})
    with chdir(self.dir), \
         self.assertRaises(zc.buildout.UserError) as cm:
      recipe.install()
    self.assertEqual(str(cm.exception), gitclone.GIT_CLONE_ERROR_MESSAGE)

  def test_cleanup_of_pyc_files(self):
    self.makeGitCloneRecipe().install()
    working_copy = os.path.join(self.parts_directory_path, "working_copy")
    bad_file_path = os.path.join(working_copy, "foo.pyc")
    open(bad_file_path, 'w').close()
    self.assertTrue(os.path.exists(bad_file_path))
    # install again and make sure pyc file is removed
    self.makeGitCloneRecipe().update()
    self.assertTrue(os.path.exists(working_copy))
    self.assertFalse(os.path.exists(bad_file_path), "pyc file not removed")

  @with_buildout
  def test_clone_and_update_submodule(self, buildout, write,
                                      sample_buildout, **kw):
    """
    Remote:
      Repositories status:  Parent repo(M1) and Submodule repo (S1)
      Parent repo (M1) ---references---> Submodule(S1)
    Local:
      Buildout should install(using branch) at M1+S1

    Remote:
      Repositories status:  Parent repo(M2) and Submodule repo (S2)
      Parent repo (M2) ---references---> Submodule(S1)
    Local:
      Buildout should update to at M2+S1

    Remote:
      Repositories status:  Parent repo(M3) and Submodule repo (S2)
      Parent repo (M3) ---references---> Submodule(S2)
    Local:
      Buildout should update to M3+S2
    """
    self.createRepositoriesAndConnect()

    # Clone repositories in status M1 and S1 (M1---->S1)
    write(sample_buildout, 'buildout.cfg',
"""
[buildout]
parts = git-clone

[git-clone]
recipe = slapos.recipe.build:gitclone
repository = %s
""" % self.project_dir)
    check_call([buildout])

    main_repo_path = os.path.join(sample_buildout, 'parts', 'git-clone')
    self.assertTrue(os.path.exists(main_repo_path))
    submodule_repo_path = os.path.join(main_repo_path, 'dir1',
                                       'submodule_repo')
    # Check if the submodule is not empty
    self.assertTrue(os.listdir(submodule_repo_path))

    # Get the head commit of the submodule repo
    head_commit_submodule_after_clone = self.getRepositoryHeadCommit(
                                              submodule_repo_path)

    # Add untracked files as markers to check that the part
    # was updated rather than removed+reinstalled.
    write(main_repo_path, 'local_change_main', 'foo')
    write(submodule_repo_path, 'local_change_submodule', 'bar')
    parent_local_change_path = os.path.join(main_repo_path,
                                            'local_change_main')
    submodule_local_change_path = os.path.join(submodule_repo_path,
                                               'local_change_submodule')
    self.checkLocalChanges(parent_local_change_path, submodule_local_change_path)

    # Trigger `update` method call for gitclone recipe
    check_call([buildout])

    # The local changes should be still there after update
    self.checkLocalChanges(parent_local_change_path, submodule_local_change_path)

    # On REMOTE, update submodule repository and parent repo with new commit,
    # but do not update the pointer to submodule on parent repo
    self.touch(self.project_dir, 'file2.py')
    self.gitAdd(self.project_dir)
    self.gitCommit(self.project_dir, msg='Add file2 in main repo')
    self.touch(self.submodule_dir, 'file2.py')
    self.gitAdd(self.submodule_dir)
    self.gitCommit(self.submodule_dir, msg='Add file2 in submodule repo')

    # Trigger update on the same branch. Remember the state at remote is
    # M2 and S2 (M2---->S1)
    check_call([buildout])
    head_commit_submodule_after_first_update = self.getRepositoryHeadCommit(
                                                      submodule_repo_path)
    # The local changes should be still there after update
    self.checkLocalChanges(parent_local_change_path, submodule_local_change_path)

    # On REMOTE, add new commit to submodule and then update the submodule
    # pointer on parent repo and commit it
    submodule_dir_main_repo = os.path.join(self.project_dir, 'dir1',
                                           'submodule_repo')
    check_call(['git', 'checkout', 'main'], cwd=submodule_dir_main_repo)
    check_call(['git', 'pull', '--ff'], cwd=submodule_dir_main_repo)
    self.gitAdd(self.project_dir)
    self.gitCommit(self.project_dir, msg='Update submodule version')

    # Trigger update again on the same branch. Remember the state at remote is
    # M3 and S2(M3---->S2)
    check_call([buildout])
    head_commit_submodule_after_second_update = self.getRepositoryHeadCommit(
                                                      submodule_repo_path)
    # The local changes should be still there after update
    self.checkLocalChanges(parent_local_change_path, submodule_local_change_path)


    # Check the HEAD of the submodule
    submodule_head_commit = self.getRepositoryHeadCommit(self.submodule_dir)
    self.assertEqual(head_commit_submodule_after_clone,
                     head_commit_submodule_after_first_update)

    self.assertNotEqual(head_commit_submodule_after_first_update,
                        head_commit_submodule_after_second_update)

    self.assertEqual(head_commit_submodule_after_second_update,
                     submodule_head_commit)

    # Update the recipe with new revision for parent and trigger uninstall/
    # install
    write(sample_buildout, 'buildout.cfg',
"""
[buildout]
parts = git-clone

[git-clone]
recipe = slapos.recipe.build:gitclone
repository = %s
revision = %s
""" % (self.project_dir, str(self.getRepositoryHeadCommit(self.project_dir))))
    check_call([buildout])

    self.assertTrue(os.path.exists(main_repo_path))
    # Check if the submodule is not empty
    self.assertTrue(os.listdir(submodule_repo_path))

    # Since calling buildout should've reinstalled, we expect the local changes
    # to be gone
    self.assertFalse(os.path.exists(parent_local_change_path))
    self.assertFalse(os.path.exists(submodule_local_change_path))

    # Get the head commit of the submodule repo
    head_commit_submodule_with_revision = self.getRepositoryHeadCommit(
                                                      submodule_repo_path)

    self.assertEqual(head_commit_submodule_with_revision,
                     submodule_head_commit)

  @with_buildout
  def test_clone_install_and_udpate_develop_mode(self, buildout, write,
                                                 sample_buildout, **kw):
    """
    Test to verify the result of development mode, i.e., develop = True.
    In this case, we expect local changes to be untouched
    """
    self.createRepositoriesAndConnect()

    # Clone repositories in status M1 and S1 (M1---->S1)
    write(sample_buildout, 'buildout.cfg',
"""
[buildout]
parts = git-clone

[git-clone]
recipe = slapos.recipe.build:gitclone
repository = %s
develop=True
""" % self.project_dir)
    check_call([buildout])

    main_repo_path = os.path.join(sample_buildout, 'parts', 'git-clone')
    self.assertTrue(os.path.exists(main_repo_path))
    submodule_repo_path = os.path.join(main_repo_path, 'dir1',
                                       'submodule_repo')
    # Check if the submodule is not empty
    self.assertTrue(os.listdir(submodule_repo_path))

    # Add untracked files as markers to check that the part
    # was updated rather than removed+reinstalled.
    write(main_repo_path, 'local_change_main', 'foo')
    write(submodule_repo_path, 'local_change_submodule', 'bar')
    parent_local_change_path = os.path.join(main_repo_path,
                                            'local_change_main')
    submodule_local_change_path = os.path.join(submodule_repo_path,
                                               'local_change_submodule')
    self.checkLocalChanges(parent_local_change_path, submodule_local_change_path)

    # Trigger `update` method call for gitclone recipe
    check_call([buildout])

    # The local changes should be still there after update as it is develop mode
    self.checkLocalChanges(parent_local_change_path, submodule_local_change_path)

  @with_buildout
  def test_git_add_for_submodule_changes(self, buildout, write,
                                         sample_buildout, **kw):
    """
    Test to verify the result of `git status` being executed from parent as well
    as submodule repository after making some local changes in submodule repo
    """
    # Create a parent repo
    self.setUpParentRepository()
    # Create submodule repository
    self.setUpSubmoduleRepository()
    # Attach the submodule repository to the parent repo on remote
    self.attachSubmoduleToParent()

    write(sample_buildout, 'buildout.cfg',
"""
[buildout]
parts = git-clone

[git-clone]
recipe = slapos.recipe.build:gitclone
repository = %s
""" % self.project_dir)
    check_call([buildout])

    local_parent_dir = os.path.join(sample_buildout, 'parts', 'git-clone')
    local_submodule_dir = os.path.join(local_parent_dir, 'dir1',
                                       'submodule_repo')

    # Now so some change manually in submodule repo, but don't commit
    self.touch(local_submodule_dir, 'file2.py')
    self.gitAdd(local_submodule_dir)

    # Do `git status` to check if the changes are shown for the repo in parent
    # This should the changes been done in the main as well as submodule repo
    files_changed = self.gitOutput('status', '--porcelain',
                                    cwd=local_parent_dir)
    file_changed, = files_changed.splitlines()
    # Check if submodule directory is part of modified list
    self.assertEqual(file_changed, ' M dir1/submodule_repo')

    # Now that `git status` in parent repo shows changes in the submodule repo,
    # do `git status` in the submodule repo to re-confirm the exact file change
    files_changed = self.gitOutput('status', '--porcelain',
                                    cwd=local_submodule_dir)
    file_changed, = files_changed.splitlines()
    # Check if submodule directory is part of modified list
    self.assertEqual(file_changed, 'A  file2.py')

  def test_ignore_ssl_certificate(self, ignore_ssl_certificate=True):
    # Monkey patch check_call
    original_check_call = gitclone.check_call
    check_call_parameter_list = []
    def patch_check_call(*args, **kw):
      check_call_parameter_list.extend((args, kw))
      original_check_call(args[0])
    try:
      gitclone.check_call = patch_check_call

      self.makeGitCloneRecipe({
        "ignore-ssl-certificate": str(ignore_ssl_certificate).lower(),
      }).install()

      # Check git clone parameters
      _ = self.assertIn if ignore_ssl_certificate else self.assertNotIn
      _("http.sslVerify=false", check_call_parameter_list[0][0])
    finally:
      gitclone.check_call = original_check_call

  def test_ignore_ssl_certificate_false(self):
    self.test_ignore_ssl_certificate(ignore_ssl_certificate=False)

  def test_clone_submodules_by_default(self, ignore_cloning_submodules=False):
    self.createRepositoriesAndConnect()
    self.makeGitCloneRecipe(
      {'repository': self.project_dir,
        'ignore-cloning-submodules': str(ignore_cloning_submodules).lower()}
    ).install()
    main_repo_path = os.path.join(self.parts_directory_path, "working_copy")
    submodule_repo_path = os.path.join(main_repo_path, 'dir1', 'submodule_repo')
    # Check if the folder exists
    self.assertTrue(os.path.exists(main_repo_path))
    # Check is there is anything in submodule repository path
    self.assertNotEqual(bool(ignore_cloning_submodules),
                        bool(os.listdir(submodule_repo_path)))

  def test_ignore_cloning_submodules(self):
    self.test_clone_submodules_by_default(ignore_cloning_submodules=True)

  @with_buildout
  def test_reset_on_update_failure(self, buildout, sample_buildout, write, **kw):
    self.createRepositoriesAndConnect()

    write(sample_buildout, 'buildout.cfg',
"""
[buildout]
parts = git-clone

[git-clone]
recipe = slapos.recipe.build:gitclone
repository = %s
""" % self.project_dir)
    check_call([buildout])

    check_call(
        ['git', 'remote', 'add', 'broken', 'http://git.erp5.org/repos/nowhere'],
        cwd=os.path.join(sample_buildout, "parts", "git-clone"))

    with self.assertRaises(CalledProcessError) as output:
      check_output([buildout], stderr=STDOUT)
    self.assertIn(
        b"error: could not fetch broken",
        output.exception.output.lower()) # old Git prints a C

    # this reset repo
    self.assertFalse(os.path.exists(os.path.join(sample_buildout, "parts", "git-clone")))
    # and running buildout again succeeed
    check_call([buildout])

  def test_clone_depth(self):
    options = {}
    self.makeGitCloneRecipe(options).install()
    get_depth = lambda: int(check_output(('git', 'rev-list', '--count', '@'),
                                         cwd=options['location']))
    self.assertLess(100, get_depth())
    options['depth'] = 10
    self.makeGitCloneRecipe(options).install()
    self.assertEqual(10, get_depth())


class MakeReadOnlyTests(unittest.TestCase):

  def setUp(self):
    self.tmp_dir = tempfile.mkdtemp()
    os.mkdir(os.path.join(self.tmp_dir, 'folder'))
    with open(os.path.join(self.tmp_dir, 'folder', 'file'), 'w') as f:
      f.write('content')

  def tearDown(self):
    for path in (
        ('folder', 'file', ),
        ('folder', 'symlink', ),
        ('folder', 'broken_symlink', ),
        ('folder', 'symlink_to_file_of_another_owner', ),
        ('folder', ),
        ()):
      full_path = os.path.join(self.tmp_dir, *path)
      if os.path.exists(full_path) and not os.path.islink(full_path):
        os.chmod(full_path, 0o700)
    shutil.rmtree(self.tmp_dir)

  def test_make_read_only_recursive(self):
    make_read_only_recursively(self.tmp_dir)
    self.assertRaises(IOError, open, os.path.join(self.tmp_dir, 'folder', 'file'), 'w')
    self.assertRaises(IOError, open, os.path.join(self.tmp_dir, 'folder', 'another_file'), 'w')
    self.assertRaises(OSError, os.mkdir, os.path.join(self.tmp_dir, 'another_folder'))

  def test_make_read_only_recursive_symlink(self):
    os.symlink(
        os.path.join(self.tmp_dir, 'folder', 'file'),
        os.path.join(self.tmp_dir, 'folder', 'symlink'))
    os.symlink(
        os.path.join(self.tmp_dir, 'folder', 'not_exist'),
        os.path.join(self.tmp_dir, 'folder', 'broken_symlink'))
    os.symlink(
        os.devnull,
        os.path.join(self.tmp_dir, 'folder', 'symlink_to_file_of_another_owner'))
    make_read_only_recursively(self.tmp_dir)
    self.assertRaises(IOError, open, os.path.join(self.tmp_dir, 'folder', 'symlink'), 'w')


MD5SUM = []

def md5sum(m):
  x = m.group(0)
  try:
      i = MD5SUM.index(x)
  except ValueError:
      i = len(MD5SUM)
      MD5SUM.append(x)
  return '<MD5SUM:%s>' % i

renormalizing_patterns = [
  zc.buildout.testing.normalize_path,
  zc.buildout.testing.root_logger_messages,
  zc.buildout.testing.not_found,
  (re.compile(
    '.*CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. '
    'Support for it is now deprecated in cryptography, and will be removed in the next release.\n.*'
    ), ''),
  (re.compile('Fetching origin\n'), ''),
  (re.compile('[0-9a-f]{32}'), md5sum),
  (re.compile(r'http://localhost:\d+'), 'http://test.server'),
  (re.compile(
    r'    print\(1 / 0.\) # this is an error !\n'
    r'ZeroDivisionError'),
     '    print(1 / 0.) # this is an error !\n'
     '          ~~^~~~\n'
     'ZeroDivisionError'),
]


def test_suite():
  suite = unittest.TestSuite((
      doctest.DocFileSuite(
          os.path.join(os.path.dirname(__file__), '..', '..', '..', 'README.rst'),
          module_relative=False,
          setUp=setUp,
          tearDown=zc.buildout.testing.buildoutTearDown,
          optionflags=optionflags,
          checker=renormalizing.RENormalizing(renormalizing_patterns),
          globs={'MD5SUM': MD5SUM},
          ),
      unittest.makeSuite(DownloadTests),
      unittest.makeSuite(GitCloneNonInformativeTests),
      unittest.makeSuite(MakeReadOnlyTests),
      ))
  return suite


def load_tests(*args):
  return test_suite()


if __name__ == '__main__':
  unittest.main(defaultTest='test_suite')
