# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import contextlib
import os.path
import platform
import subprocess
from textwrap import dedent
from unittest import mock

import distro
import fixtures
import ometa.runtime
from testtools import ExpectedException
from testtools.matchers import Contains
from testtools.matchers import Equals
from testtools.matchers import MatchesSetwise
from testtools import TestCase

from bindep.depends import _eval
from bindep.depends import Brew
from bindep.depends import Depends
from bindep.depends import Dpkg
from bindep.depends import Emerge
from bindep.depends import Pacman
from bindep.depends import Rpm
from bindep.depends import Apk


# NOTE(notmorgan): In python3 subprocess.check_output returns bytes not
# string. All mock calls for subprocess.check_output have been updated to
# ensure bytes is used over string. In python 2 this is a no-op change.

FIXTURE_DIR = os.path.join(os.path.dirname(__file__),
                           'fixtures')


class DistroFixture(fixtures.Fixture):
    def __init__(self, distro_name):
        self.distro_name = distro_name.lower()

    def _setUp(self):
        # Python 2.7 and 3.5 need older distro which has different src paths
        if distro.__version__ < '1.7.0':
            distro_patch_path = 'distro._distro'
        else:
            distro_patch_path = 'distro.distro._distro'
        # This type of monkey patching is borrowed from the distro test
        # suite.
        os_release = os.path.join(FIXTURE_DIR, self.distro_name,
                                  'etc', 'os-release')
        mydistro = distro.LinuxDistribution(False, os_release, 'non')
        self.useFixture(
            fixtures.MonkeyPatch(distro_patch_path, mydistro))
        if self.distro_name not in ['darwin']:
            self.useFixture(fixtures.MonkeyPatch(
                'platform.system', lambda *x: 'Linux'))
        else:
            self.useFixture(fixtures.MonkeyPatch(
                'distro.id', lambda *x: self.distro_name))


class TestDepends(TestCase):

    def test_filename(self):
        depends = Depends("")
        self.assertIsNone(depends.filename)
        depends = Depends("", "/some/path/to/bindep.txt")
        self.assertEqual(depends.filename, "/some/path/to/bindep.txt")

    def test_empty_file(self):
        depends = Depends("")
        self.assertEqual([], depends.profiles())

    def test_3tuple(self):
        depends = Depends(u"erlang [(infra rabbitmq hipe)]\n")
        self.assertEqual(sorted([u'infra', u'rabbitmq', u'hipe']),
                         depends.profiles())

    def test_platform_profiles_succeeds(self):
        with DistroFixture('Ubuntu'):
            depends = Depends("")
            self.assertIsInstance(depends.platform_profiles(), list)

    @contextlib.contextmanager
    def _mock_lsb(self, platform):
        r_val = "%s\n14.04\ntrusty\n" % platform
        mock_checkoutput = self.useFixture(
            fixtures.MockPatchObject(
                subprocess,
                'check_output',
                return_value=r_val.encode('utf-8'))).mock
        yield mock_checkoutput
        mock_checkoutput.assert_called_once_with(["lsb_release", "-cirs"],
                                                 stderr=subprocess.STDOUT)

    @contextlib.contextmanager
    def _mock_platform_darwin(self, system):
        r_val = system
        mock_checkoutput = self.useFixture(
            fixtures.MockPatchObject(
                platform,
                'system',
                return_value=r_val)).mock
        yield mock_checkoutput
        mock_checkoutput.assert_called_once_with()

    def test_detects_unknown(self):
        with DistroFixture("Unknown"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:unknown"))
            with ExpectedException(Exception,
                                   "Unknown package manager for "
                                   "current platform."):
                depends.platform.get_pkg_version('x')

    def test_detects_amazon_linux(self):
        with DistroFixture("AmazonAMI"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:amazonami"))

    def test_detects_centos(self):
        with DistroFixture("CentOS"):
            depends = Depends("")
            platform_profiles = depends.platform_profiles()
            self.assertThat(platform_profiles, Contains("platform:centos"))
            self.assertThat(platform_profiles, Contains("platform:redhat"))

    def test_detects_darwin(self):
        with self._mock_platform_darwin("Darwin"):
            depends = Depends("")
            platform_profiles = depends.platform_profiles()
            self.assertThat(platform_profiles, Contains("platform:darwin"))

    def test_detects_rhel7(self):
        with DistroFixture("RHELServer7"):
            depends = Depends("")
            platform_profiles = depends.platform_profiles()
            self.assertThat(
                platform_profiles,
                Contains("platform:redhatenterpriseserver"))
            self.assertThat(
                platform_profiles,
                Contains("platform:rhel"))
            self.assertThat(
                platform_profiles,
                Contains("platform:redhat"))
            self.assertThat(platform_profiles, Contains("platform:base-py2"))

    def test_detects_rhel_workstation(self):
        with DistroFixture("RHELWorkstation7"):
            depends = Depends("")
            platform_profiles = depends.platform_profiles()
            self.assertThat(
                platform_profiles,
                Contains("platform:redhatenterpriseworkstation"))
            self.assertThat(
                platform_profiles,
                Contains("platform:rhel"))
            self.assertThat(
                platform_profiles,
                Contains("platform:redhat"))
            self.assertThat(platform_profiles, Contains("platform:base-py2"))

    def test_detects_fedora23(self):
        with DistroFixture("Fedora23"):
            depends = Depends("")
            platform_profiles = depends.platform_profiles()
            self.assertThat(platform_profiles, Contains("platform:fedora"))
            self.assertThat(platform_profiles, Contains("platform:redhat"))
            self.assertThat(platform_profiles, Contains("platform:base-py3"))

    def test_detects_rhel8(self):
        with DistroFixture("rhel8"):
            depends = Depends("")
            platform_profiles = depends.platform_profiles()
            self.assertThat(platform_profiles, Contains("platform:redhat"))
            self.assertThat(platform_profiles, Contains("platform:base-py3"))

    def test_detects_opensuse_project(self):
        # TODO what does an os-release for opensuse project look like?
        # Is this different than sles, leap, and tumbleweed?
        with DistroFixture("openSUSEleap"):
            depends = Depends("")
            platform_profiles = depends.platform_profiles()
            self.assertThat(platform_profiles,
                            Contains("platform:opensuseproject"))
            self.assertThat(platform_profiles,
                            Contains("platform:opensuse"))
            self.assertThat(platform_profiles,
                            Contains("platform:opensuseproject-42.1"))
            self.assertThat(platform_profiles,
                            Contains("platform:suse"))

    def test_detects_opensuse(self):
        with DistroFixture("openSUSEleap"):
            depends = Depends("")
            platform_profiles = depends.platform_profiles()
            self.assertThat(platform_profiles,
                            Contains("platform:opensuse"))
            self.assertThat(platform_profiles,
                            Contains("platform:suse"))

    def test_detects_opensuse_leap15(self):
        with DistroFixture("openSUSEleap15"):
            depends = Depends("")
            platform_profiles = depends.platform_profiles()
            self.assertThat(platform_profiles,
                            Contains("platform:opensuse"))
            self.assertThat(platform_profiles,
                            Contains("platform:suse"))

    def test_detects_suse_linux(self):
        with DistroFixture("SLES"):
            depends = Depends("")
            platform_profiles = depends.platform_profiles()
            self.assertThat(platform_profiles, Contains("platform:suselinux"))
            self.assertThat(platform_profiles, Contains("platform:suse"))

    def test_detects_ubuntu(self):
        with DistroFixture("Ubuntu"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:ubuntu"))

    def test_detects_alpine(self):
        with DistroFixture("Alpine"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:alpine"))

    def test_detects_oraclelinux(self):
        with DistroFixture("oraclelinux"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:rpm"))

    def test_detects_rocky(self):
        with DistroFixture("rocky"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:rpm"))

    def test_detects_almalinux(self):
        with DistroFixture("almalinux"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:rpm"))

    def test_detects_debian_sid(self):
        with DistroFixture("DebianSid"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:debian"))
            self.assertThat(
                depends.platform_profiles(),
                Contains("platform:debian-xyzzy"))

    def test_detects_release(self):
        with DistroFixture("Ubuntu"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:ubuntu-16"))

    def test_detects_subrelease(self):
        with DistroFixture("Ubuntu"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:ubuntu-16.04"))

    def test_detects_codename(self):
        with DistroFixture("Ubuntu"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(),
                Contains("platform:ubuntu-xenial"))

    def test_centos_implies_rpm(self):
        with DistroFixture("CentOS"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:rpm"))
            self.assertIsInstance(depends.platform, Rpm)

    def test_darwin_implies_brew(self):
        with self._mock_platform_darwin("Darwin"):
            with DistroFixture("Darwin"):
                # to make it believe `which brew` succeeded
                self.useFixture(
                    fixtures.MockPatchObject(
                        os,
                        'system',
                        return_value=0)).mock
                depends = Depends("")
                self.assertThat(
                    depends.platform_profiles(), Contains("platform:brew"))
                self.assertIsInstance(depends.platform, Brew)

    def test_rhel_implies_rpm(self):
        with DistroFixture("RHELServer7"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:rpm"))
            self.assertIsInstance(depends.platform, Rpm)

    def test_fedora_implies_rpm(self):
        with DistroFixture("Fedora23"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:rpm"))
            self.assertIsInstance(depends.platform, Rpm)

    def test_opensuse_project_implies_rpm(self):
        with DistroFixture("openSUSEleap"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:rpm"))
            self.assertIsInstance(depends.platform, Rpm)

    def test_opensuse_implies_rpm(self):
        with DistroFixture("openSUSEleap"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:rpm"))
            self.assertIsInstance(depends.platform, Rpm)

    def test_opensuse_leap15_implies_rpm(self):
        with DistroFixture("openSUSEleap15"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:rpm"))
            self.assertIsInstance(depends.platform, Rpm)

    def test_suse_linux_implies_rpm(self):
        with DistroFixture("SLES"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:rpm"))
            self.assertIsInstance(depends.platform, Rpm)

    def test_ubuntu_implies_dpkg(self):
        with DistroFixture("Ubuntu"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:dpkg"))
            self.assertIsInstance(depends.platform, Dpkg)

    def test_alpine_implies_apk(self):
        with DistroFixture("Alpine"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:apk"))
            self.assertIsInstance(depends.platform, Apk)

    def test_arch_implies_pacman(self):
        with DistroFixture("Arch"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:pacman"))
            self.assertIsInstance(depends.platform, Pacman)

    def test_manjaro_implies_pacman(self):
        with DistroFixture("manjaro"):
            depends = Depends("")
            self.assertThat(
                depends.platform_profiles(), Contains("platform:pacman"))
            self.assertIsInstance(depends.platform, Pacman)

    def test_finds_profiles(self):
        depends = Depends(dedent("""\
            foo
            bar [something]
            quux [anotherthing !nothing] <=12
            """))
        self.assertThat(
            depends.profiles(),
            MatchesSetwise(*map(
                Equals, ["something", "anotherthing", "nothing"])))

    def test_empty_rules(self):
        depends = Depends("")
        self.assertEqual([], depends._rules)

    def test_no_newline(self):
        depends = Depends("foo")
        self.assertEqual(
            [("foo", [], [])],
            depends._rules)

    def test_selectors(self):
        depends = Depends("foo [!bar baz quux]\n")
        self.assertEqual(
            [("foo", [(False, "bar"), (True, "baz"), (True, "quux")], [])],
            depends._rules)

    def test_single_group_only(self):
        depends = Depends("foo [(bar)]\n")
        self.assertTrue(depends._evaluate(depends._rules[0][1], ["bar"]))
        self.assertFalse(depends._evaluate(depends._rules[0][1], ["baz"]))

    def test_multiple_groups_only(self):
        depends = Depends("foo [(bar baz) (quux)]\n")
        self.assertTrue(depends._evaluate(depends._rules[0][1],
                                          ["bar", "baz"]))
        self.assertTrue(depends._evaluate(depends._rules[0][1], ["quux"]))
        self.assertFalse(depends._evaluate(depends._rules[0][1], ["baz"]))
        self.assertFalse(depends._evaluate(depends._rules[0][1], ["bar"]))

    def test_whitespace(self):
        depends = Depends("foo [ ( bar !baz ) quux ]\n")
        self.assertEqual(
            [("foo", [[(True, "bar"), (False, "baz")], (True, "quux")], [])],
            depends._rules)

    def test_group_selectors(self):
        depends = Depends("foo [(bar !baz) quux]\n")
        self.assertEqual(
            [("foo", [[(True, "bar"), (False, "baz")], (True, "quux")], [])],
            depends._rules)

    def test_multiple_group_selectors(self):
        depends = Depends("foo [(bar baz) (baz quux)]\n")
        parsed_profiles = [
            [(True, "bar"), (True, "baz")],
            [(True, "baz"), (True, "quux")],
        ]
        self.assertEqual(
            [("foo", parsed_profiles, [])],
            depends._rules)

    def test_single_profile_group_selectors(self):
        depends = Depends("foo [(bar) (!baz)]\n")
        self.assertEqual(
            [("foo", [[(True, "bar")], [(False, "baz")]], [])],
            depends._rules)

    def test_versions(self):
        depends = Depends("foo <=1,!=2\n")
        self.assertEqual(
            [("foo", [], [('<=', '1'), ('!=', '2')])],
            depends._rules)

    def test_no_selector_active(self):
        depends = Depends("foo\n")
        self.assertEqual([("foo", [], [])], depends.active_rules(["default"]))

    def test_negative_selector_removes_rule(self):
        depends = Depends("foo [!off]\n")
        self.assertEqual([], depends.active_rules(["on", "off"]))

    def test_positive_selector_includes_rule(self):
        depends = Depends("foo [on]\n")
        self.assertEqual(
            [("foo", [(True, "on")], [])],
            depends.active_rules(["on", "off"]))

    def test_positive_selector_not_in_profiles_inactive(self):
        depends = Depends("foo [on]\n")
        self.assertEqual([], depends.active_rules(["default"]))

    def test_check_rule_missing(self):
        depends = Depends("")
        depends.platform = mock.MagicMock()
        mock_depend_platform = self.useFixture(
            fixtures.MockPatchObject(depends.platform, 'get_pkg_version',
                                     return_value=None)).mock
        self.assertEqual(
            [('missing', ['foo'])], depends.check_rules([("foo", [], [])]))
        mock_depend_platform.assert_called_once_with("foo")

    def test_check_rule_missing_version(self):
        depends = Depends("")
        depends.platform = mock.MagicMock()
        mock_depend_platform = self.useFixture(
            fixtures.MockPatchObject(depends.platform, 'get_pkg_version',
                                     return_value=None)).mock
        self.assertEqual(
            [('missing', ['foo'])],
            depends.check_rules([("foo", [], [(">=", "1.2.3")])]))
        mock_depend_platform.assert_called_once_with("foo")

    def test_check_rule_present(self):
        depends = Depends("")
        depends.platform = mock.MagicMock()
        mock_depend_platform = self.useFixture(
            fixtures.MockPatchObject(depends.platform, 'get_pkg_version',
                                     return_value="123")).mock
        self.assertEqual([], depends.check_rules([("foo", [], [])]))
        mock_depend_platform.assert_called_once_with("foo")

    def test_check_rule_incompatible(self):
        depends = Depends("")
        depends.platform = mock.MagicMock()
        depends.platform = mock.MagicMock()
        mock_depend_platform = self.useFixture(
            fixtures.MockPatchObject(depends.platform, 'get_pkg_version',
                                     return_value="123")).mock
        self.assertEqual(
            [('badversion', [('foo', "!=123", "123")])],
            depends.check_rules([("foo", [], [("!=", "123")])]))
        mock_depend_platform.assert_called_once_with("foo")

    def test_parser_patterns(self):
        depends = Depends(dedent("""\
            foo
            bar [something]
            category/packagename # for gentoo
            baz [platform:this platform:that-those]
            blaz [platform:rpm !platform:opensuseproject-42.2]
            quux [anotherthing !nothing] <=12
            womp # and a comment
            # a standalone comment and a blank line

            # all's ok? good then
            """))
        self.assertEqual(len(depends.active_rules(['default'])), 3)

    def test_parser_accepts_full_path_to_tools(self):
        # at least yum/dnf allow these instead of mentioning rpm names
        depends = Depends(dedent("""\
            /usr/bin/bash
            """))
        self.assertEqual(
            [("/usr/bin/bash", [], [])],
            depends.active_rules(["default"]))

    def test_parser_invalid(self):
        self.assertRaises(ometa.runtime.ParseError,
                          lambda: Depends("foo [platform:bar@baz]\n"))

    def test_platforms_include(self):
        # 9 tests for the nine cases of _include in Depends
        depends = Depends(dedent("""\
            # False, False -> False
            install1 [platform:dpkg quark]
            # False, None -> False
            install2 [platform:dpkg]
            # False, True -> False
            install3 [platform:dpkg test]
            # None, False -> False
            install4 [quark]
            # None, None -> True
            install5
            # None, True -> True
            install6 [test]
            # True, False -> False
            install7 [platform:rpm quark]
            # True, None -> True
            install8 [platform:rpm]
            # True, True -> True
            install9 [platform:rpm test]
            """))

        # With platform:dpkg and quark False and platform:rpm and test
        # True, the above mimics the conditions from _include.
        self.expectThat(
            set(r[0] for r in depends.active_rules(['platform:rpm', 'test'])),
            Equals({"install5", "install6", "install8", "install9"}))

    def test_list_all(self):
        depends = Depends(dedent("""\
            install1
            install2 [test]
            install3 [platform:rpm]
            install4 [platform:dpkg]
            install5 [quark]
            install6 [platform:dpkg test]
            install7 [quark test]
            install8 [platform:dpkg platform:rpm]
            install9 [platform:dpkg platform:rpm test]
            installA [!platform:dpkg]
            installB [!platform:dpkg test]
            installC [!platform:dpkg !test]
            installD [platform:dpkg !test]
            installE [platform:dpkg !platform:rpm]
            installF [platform:dpkg !platform:rpm test]
            installG [!platform:dpkg !platform:rpm]
            installH [!platform:dpkg !platform:rpm test]
            installI [!platform:dpkg !platform:rpm !test]
            installJ [platform:dpkg !platform:rpm !test]
            """))

        rules_dpkg = depends.active_rules(['platform:dpkg'])
        result_dpkg = set(r[0] for r in rules_dpkg)
        self.assertEqual(result_dpkg,
                         set(depends.list_all_packages(rules_dpkg,
                             output_format='newline')))
        self.assertEqual(result_dpkg,
                         set(depends.list_all_packages(rules_dpkg,
                             output_format='csv')))

        rules_dpkg_test = depends.active_rules(['platform:dpkg', 'test'])
        result_dpkg_test = set(r[0] for r in rules_dpkg_test)
        self.assertEqual(result_dpkg_test, set(depends.list_all_packages(
                                               rules_dpkg_test,
                                               output_format='newline')))
        self.assertEqual(result_dpkg_test, set(depends.list_all_packages(
                                               rules_dpkg_test,
                                               output_format='csv')))

        rules_rpm = depends.active_rules(['platform:rpm'])
        result_rpm = set(r[0] for r in rules_rpm)
        self.assertEqual(result_rpm, set(depends.list_all_packages(rules_rpm,
                                         output_format='newline')))
        self.assertEqual(result_rpm, set(depends.list_all_packages(rules_rpm,
                                         output_format='csv')))

        rules_rpm_test = depends.active_rules(['platform:rpm', 'test'])
        result_rpm_test = set(r[0] for r in rules_rpm_test)
        self.assertEqual(result_rpm_test,
                         set(depends.list_all_packages(
                             rules_rpm_test,
                             output_format='newline')))
        self.assertEqual(result_rpm_test,
                         set(depends.list_all_packages(
                             rules_rpm_test,
                             output_format='csv')))

    def test_platforms(self):
        depends = Depends(dedent("""\
            install1
            install2 [test]
            install3 [platform:rpm]
            install4 [platform:dpkg]
            install5 [quark]
            install6 [platform:dpkg test]
            install7 [quark test]
            install8 [platform:dpkg platform:rpm]
            install9 [platform:dpkg platform:rpm test]
            installA [!platform:dpkg]
            installB [!platform:dpkg test]
            installC [!platform:dpkg !test]
            installD [platform:dpkg !test]
            installE [platform:dpkg !platform:rpm]
            installF [platform:dpkg !platform:rpm test]
            installG [!platform:dpkg !platform:rpm]
            installH [!platform:dpkg !platform:rpm test]
            installI [!platform:dpkg !platform:rpm !test]
            installJ [platform:dpkg !platform:rpm !test]
            """))

        # Platform-only rules and rules with no platform are activated
        # by a matching platform.
        self.expectThat(
            set(r[0] for r in depends.active_rules(['platform:dpkg'])),
            Equals({"install1", "install4", "install8", "installD",
                    "installE", "installJ"}))

        # Non-platform rules matching one-or-more profiles plus any
        # matching platform guarded rules.
        self.expectThat(
            set(r[0] for r in depends.active_rules(['platform:dpkg', 'test'])),
            Equals({"install1", "install2", "install4", "install6", "install7",
                    "install8", "install9", "installE", "installF"}))

        # When multiple platforms are present, none-or-any-platform is
        # enough to match.
        self.expectThat(
            set(r[0] for r in depends.active_rules(['platform:rpm'])),
            Equals({"install1", "install3", "install8", "installA",
                    "installC"}))

        # If there are any platform profiles on a rule one of them
        # must match an active platform even when other profiles match
        # for the rule to be active.
        self.expectThat(
            set(r[0] for r in depends.active_rules(['platform:rpm', 'test'])),
            Equals({"install1", "install2", "install3", "install7", "install8",
                    "install9", "installA", "installB"}))


class TestDpkg(TestCase):

    def test_not_installed(self):
        platform = Dpkg()
        mock_checkoutput = self.useFixture(
            fixtures.MockPatchObject(
                subprocess,
                'check_output',
                return_value=b"foo deinstall ok config-files 4.0.0-0ubuntu1\n")
        ).mock
        self.assertEqual(None, platform.get_pkg_version("foo"))
        mock_checkoutput.assert_called_once_with(
            ["dpkg-query", "-W", "-f",
             "${Package} ${Status} ${Version}\n", "foo"],
            stderr=subprocess.STDOUT)

    def test_unknown_package(self):
        platform = Dpkg()
        mock_checkoutput = self.useFixture(
            fixtures.MockPatchObject(subprocess, 'check_output')).mock

        def _side_effect_raise(*args, **kwargs):
            raise subprocess.CalledProcessError(
                1, [], b"dpkg-query: no packages found matching foo\n")

        mock_checkoutput.side_effect = _side_effect_raise
        self.assertEqual(None, platform.get_pkg_version("foo"))
        mock_checkoutput.assert_called_once_with(
            ["dpkg-query", "-W", "-f",
             "${Package} ${Status} ${Version}\n", "foo"],
            stderr=subprocess.STDOUT)

    def test_installed_version(self):
        platform = Dpkg()
        mocked_checkoutput = self.useFixture(
            fixtures.MockPatchObject(
                subprocess,
                'check_output',
                return_value=b"foo install ok installed 4.0.0-0ubuntu1\n")
        ).mock
        self.assertEqual("4.0.0-0ubuntu1", platform.get_pkg_version("foo"))
        mocked_checkoutput.assert_called_once_with(
            ["dpkg-query", "-W", "-f",
             "${Package} ${Status} ${Version}\n", "foo"],
            stderr=subprocess.STDOUT)


class TestEmerge(TestCase):

    def test_not_installed(self):
        platform = Emerge()

        def _side_effect_raise(*args, **kwargs):
            raise subprocess.CalledProcessError(3, [], b'')

        mocked_checkoutput = self.useFixture(
            fixtures.MockPatchObject(subprocess, 'check_output')).mock

        mocked_checkoutput.side_effect = _side_effect_raise
        self.assertEqual(None, platform.get_pkg_version("foo"))
        mocked_checkoutput.assert_called_once_with(
            ['equery', 'l', '--format=\'$version\'', 'foo'],
            stderr=subprocess.STDOUT)

    def test_unknown_package(self):
        platform = Emerge()

        def _side_effect_raise(*args, **kwargs):
            raise subprocess.CalledProcessError(3, [], b'')

        mocked_checkoutput = self.useFixture(
            fixtures.MockPatchObject(subprocess, 'check_output')).mock

        mocked_checkoutput.side_effect = _side_effect_raise
        self.assertEqual(None, platform.get_pkg_version("foo"))
        mocked_checkoutput.assert_called_once_with(
            ['equery', 'l', '--format=\'$version\'', 'foo'],
            stderr=subprocess.STDOUT)

    def test_installed_version(self):
        platform = Emerge()
        mock_checkoutput = self.useFixture(
            fixtures.MockPatchObject(subprocess, 'check_output',
                                     return_value=b"4.0.0\n")).mock
        self.assertEqual("4.0.0", platform.get_pkg_version("foo"))
        mock_checkoutput.assert_called_once_with(
            ['equery', 'l', '--format=\'$version\'', 'foo'],
            stderr=subprocess.STDOUT)


class TestPacman(TestCase):

    def test_unknown_package(self):
        platform = Pacman()

        def _side_effect_raise(*args, **kwargs):
            raise subprocess.CalledProcessError(
                1, [], b"error: package 'foo' was not found")

        mock_checkoutput = self.useFixture(
            fixtures.MockPatchObject(subprocess, "check_output")).mock
        mock_checkoutput.side_effect = _side_effect_raise

        self.assertEqual(None, platform.get_pkg_version("foo"))
        mock_checkoutput.assert_called_once_with(
            ['pacman', '-Q', 'foo'],
            stderr=subprocess.STDOUT)
        self.assertEqual(None, platform.get_pkg_version("foo"))

    def test_installed_version(self):
        platform = Pacman()
        mock_checkoutput = self.useFixture(
            fixtures.MockPatchObject(subprocess, "check_output")).mock
        mock_checkoutput.return_value = b'foo 4.0.0-2'
        self.assertEqual("4.0.0-2", platform.get_pkg_version("foo"))
        mock_checkoutput.assert_called_once_with(
            ['pacman', '-Q', 'foo'],
            stderr=subprocess.STDOUT)


class TestApk(TestCase):

    @mock.patch('subprocess.Popen')
    def test_unknown_package(self, mock_popen):
        platform = Apk()

        proc_mock = mock.Mock()
        proc_mock.communicate.return_value = (b'Installed: Available:\n', b'')
        mock_popen.returncode = 1
        mock_popen.return_value = proc_mock

        self.assertEqual(None, platform.get_pkg_version("foo"))
        mock_popen.assert_called_once_with(
            ['apk', 'version', 'foo'], stdout=subprocess.PIPE)
        self.assertEqual(None, platform.get_pkg_version("foo"))

    @mock.patch('subprocess.Popen')
    def test_installed_version(self, mock_popen):
        platform = Apk()

        proc_mock = mock.Mock()
        proc_mock.communicate.return_value = (
            b'Insd: Able: foo-4.0.0-r1 = 4.0.0-r1', b'')
        mock_popen.return_value = proc_mock
        self.assertEqual('4.0.0-r1', platform.get_pkg_version("foo"))
        mock_popen.assert_called_once_with(
            ['apk', 'version', 'foo'], stdout=subprocess.PIPE)

    @mock.patch('subprocess.Popen')
    def test_handles_warnings(self, mock_popen):
        platform = Apk()
        process_mock = mock.Mock()
        values = b'Installed:   Available:\n'
        warnings = b'WARNING: Ignoring APKINDEX.blah\nWARNING2: blah blah\n'
        process_mock.communicate.return_value = (values, warnings)
        mock_popen.return_value = process_mock
        self.assertIsNone(platform.get_pkg_version("bar"))
        mock_popen.assert_called_once_with(
            ['apk', 'version', 'bar'], stdout=subprocess.PIPE)


class TestRpm(TestCase):

    # NOTE: test_not_installed is not implemented as rpm seems to only be aware
    # of installed packages

    def test_unknown_package(self):
        platform = Rpm()

        def _side_effect_raise(*args, **kwargs):
            raise subprocess.CalledProcessError(
                1, [], b"package foo is not installed\n")

        mock_checkoutput = self.useFixture(
            fixtures.MockPatchObject(subprocess, 'check_output')).mock
        mock_checkoutput.side_effect = _side_effect_raise
        self.assertEqual(None, platform.get_pkg_version("foo"))
        mock_checkoutput.assert_called_once_with(
            ["rpm", "--qf",
             "%{NAME} %|EPOCH?{%{EPOCH}:}|%{VERSION}-%{RELEASE}\n",
             "--whatprovides", "-q", "foo"],
            stderr=subprocess.STDOUT)
        self.assertEqual(None, platform.get_pkg_version("foo"))

    def test_installed_version(self):
        platform = Rpm()
        mock_checkoutput = self.useFixture(
            fixtures.MockPatchObject(subprocess, 'check_output',
                                     return_value=b"foo 4.0.0-0.el6\n")).mock
        self.assertEqual("4.0.0-0.el6", platform.get_pkg_version("foo"))
        mock_checkoutput.assert_called_once_with(
            ["rpm", "--qf",
             "%{NAME} %|EPOCH?{%{EPOCH}:}|%{VERSION}-%{RELEASE}\n",
             "--whatprovides", "-q", "foo"],
            stderr=subprocess.STDOUT)


class TestEval(TestCase):

    def test_lt(self):
        self.assertEqual(True, _eval("3.5-ubuntu", "<", "4"))
        self.assertEqual(False, _eval("4", "<", "3.5-ubuntu"))
        self.assertEqual(False, _eval("4", "<", "4"))
        # Epoch comes first
        self.assertEqual(True, _eval("1:2", "<", "2:1"))
        # ~'s
        self.assertEqual(True, _eval("1~~", "<", "1~~a"))
        self.assertEqual(True, _eval("1~~a", "<", "1~"))
        self.assertEqual(True, _eval("1~", "<", "1"))
        self.assertEqual(True, _eval("1", "<", "1a"))
        # debver's
        self.assertEqual(True, _eval("1-a~~", "<", "1-a~~a"))
        self.assertEqual(True, _eval("1-a~~a", "<", "1-a~"))
        self.assertEqual(True, _eval("1-a~", "<", "1-a"))
        self.assertEqual(True, _eval("1-a", "<", "1-aa"))
        # end-of-segment
        self.assertEqual(True, _eval("1a", "<", "1aa"))
        self.assertEqual(True, _eval("1a-a", "<", "1a-aa"))

    def test_lte(self):
        self.assertEqual(True, _eval("3.5-ubuntu", "<=", "4"))
        self.assertEqual(False, _eval("4", "<=", "3.5-ubuntu"))
        self.assertEqual(True, _eval("4", "<=", "4"))

    def test_eq(self):
        self.assertEqual(True, _eval("3.5-ubuntu", "==", "3.5-ubuntu"))
        self.assertEqual(False, _eval("4", "==", "3.5-ubuntu"))
        self.assertEqual(False, _eval("3.5-ubuntu", "==", "4"))

    def test_neq(self):
        self.assertEqual(False, _eval("3.5-ubuntu", "!=", "3.5-ubuntu"))
        self.assertEqual(True, _eval("4", "!=", "3.5-ubuntu"))
        self.assertEqual(True, _eval("3.5-ubuntu", "!=", "4"))

    def test_gt(self):
        self.assertEqual(False, _eval("3.5-ubuntu", ">", "4"))
        self.assertEqual(True, _eval("4", ">", "3.5-ubuntu"))
        self.assertEqual(False, _eval("4", ">", "4"))

    def test_gte(self):
        self.assertEqual(False, _eval("3.5-ubuntu", ">=", "4"))
        self.assertEqual(True, _eval("4", ">=", "3.5-ubuntu"))
        self.assertEqual(True, _eval("4", ">=", "4"))
