import pytest

from rosdistro.distribution import Distribution


class MockReleasePackage:
    def __init__(self, repository_name):
        self.repository_name = repository_name


class MockReleaseRepository:
    def __init__(self, version):
        self.version = version


class MockRepositorySpecification:
    def __init__(self, release_repository=None, source_repository=None):
        self.release_repository = release_repository
        self.source_repository = source_repository


class MockDistributionFile:
    def __init__(self, name, release_packages, repositories, source_packages=None):
        self.name = name
        self.release_packages = release_packages
        self.repositories = repositories
        self.source_packages = source_packages or {}



def test_get_release_package_xml_fallback():
    pkg = MockReleasePackage(repository_name='foo_repo')
    release_repo = MockReleaseRepository(version='1.0.0')
    repo_spec = MockRepositorySpecification(release_repository=release_repo)
    dist_file = MockDistributionFile(
        name='foo_dist',
        release_packages={'foo_pkg': pkg},
        repositories={'foo_repo': repo_spec}
    )

    calls = []

    def mp1(dist_name, repo, pkg_name):
        calls.append('mp1')
        raise RuntimeError('mp1 failed')

    def mp2(dist_name, repo, pkg_name):
        calls.append('mp2')
        return '<package>foo_pkg</package>'

    def mp3(dist_name, repo, pkg_name):
        calls.append('mp3')
        return '<package>should not be called</package>'

    dist = Distribution(dist_file, manifest_providers=[mp1, mp2, mp3])
    xml = dist.get_release_package_xml('foo_pkg')

    assert xml == '<package>foo_pkg</package>'
    assert calls == ['mp1', 'mp2']


def test_get_release_package_xml_all_fail():
    pkg = MockReleasePackage(repository_name='foo_repo')
    release_repo = MockReleaseRepository(version='1.0.0')
    repo_spec = MockRepositorySpecification(release_repository=release_repo)
    dist_file = MockDistributionFile(
        name='foo_dist',
        release_packages={'foo_pkg': pkg},
        repositories={'foo_repo': repo_spec}
    )

    def mp1(dist_name, repo, pkg_name):
        raise ValueError('mp1 error')

    def mp2(dist_name, repo, pkg_name):
        raise TypeError('mp2 error')

    dist = Distribution(dist_file, manifest_providers=[mp1, mp2])
    with pytest.raises(TypeError, match='mp2 error'):
        dist.get_release_package_xml('foo_pkg')


def test_get_source_repo_package_xmls_fallback():
    repo_spec = MockRepositorySpecification(source_repository='foo_source_repo')
    dist_file = MockDistributionFile(
        name='foo_dist',
        release_packages={},
        repositories={'foo_repo': repo_spec}
    )

    calls = []

    def mp1(repo):
        calls.append('mp1')
        raise RuntimeError('mp1 failed')

    def mp2(repo):
        calls.append('mp2')
        return {'foo_pkg': ('pkg_path', '<package>foo_pkg</package>')}

    def mp3(repo):
        calls.append('mp3')
        return {'foo_pkg': ('pkg_path', 'should not be called')}

    dist = Distribution(dist_file, source_manifest_providers=[mp1, mp2, mp3])
    res = dist.get_source_repo_package_xmls('foo_repo')

    assert res == {'foo_pkg': ('pkg_path', '<package>foo_pkg</package>')}
    assert calls == ['mp1', 'mp2']


def test_get_source_repo_package_xmls_all_fail():
    repo_spec = MockRepositorySpecification(source_repository='foo_source_repo')
    dist_file = MockDistributionFile(
        name='foo_dist',
        release_packages={},
        repositories={'foo_repo': repo_spec}
    )

    def mp1(repo):
        raise ValueError('mp1 error')

    def mp2(repo):
        raise TypeError('mp2 error')

    dist = Distribution(dist_file, source_manifest_providers=[mp1, mp2])
    with pytest.raises(TypeError, match='mp2 error'):
        dist.get_source_repo_package_xmls('foo_repo')
