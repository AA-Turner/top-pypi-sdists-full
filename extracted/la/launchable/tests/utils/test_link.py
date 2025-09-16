from unittest import TestCase

import click

from launchable.utils.link import LinkKind, capture_link, capture_links, capture_links_from_options


class LinkTest(TestCase):
    def test_jenkins(self):
        envs = {
            "JENKINS_URL": "https://jenkins.io",
            "BUILD_URL": "https://jenkins.launchableinc.com/build/123",
            "JOB_NAME": "foo",
            "BUILD_DISPLAY_NAME": "#123"
        }
        self.assertEqual(capture_link(envs), [{
            "kind": LinkKind.JENKINS.name,
            "title": "foo #123",
            "url": "https://jenkins.launchableinc.com/build/123",
        }])

    def test_github_actions(self):
        envs = {
            "GITHUB_ACTIONS": "true",
            "GITHUB_SERVER_URL": "https://github.com",
            "GITHUB_REPOSITORY": "launchable/cli",
            "GITHUB_RUN_ID": 123,
            "GITHUB_WORKFLOW": "workflow",
            "GITHUB_JOB": "job",
            "GITHUB_RUN_NUMBER": "234"
        }
        self.assertEqual(capture_link(envs), [{
            "kind": LinkKind.GITHUB_ACTIONS.name,
            "title": "workflow / job #234",
            "url": "https://github.com/launchable/cli/actions/runs/123",
        }])

    def test_circleci(self):
        envs = {
            "CIRCLECI": "true",
            "CIRCLE_BUILD_URL": "https://circleci.com/build/123",
            "CIRCLE_JOB": "job",
            "CIRCLE_BUILD_NUM": "234"}
        self.assertEqual(capture_link(envs), [{
            "kind": LinkKind.CIRCLECI.name,
            "title": "job (234)",
            "url": "https://circleci.com/build/123",
        }])

    def test_capture_links_from_options(self):
        # Invalid kind
        link_options = [("INVALID_KIND|PR", "https://github.com/launchableinc/cli/pull/1")]
        with self.assertRaises(click.UsageError):
            capture_links_from_options(link_options)

        # Invalid URL
        link_options = [("GITHUB_PULL_REQUEST|PR", "https://github.com/launchableinc/cli/pull/1/files")]
        with self.assertRaises(click.UsageError):
            capture_links_from_options(link_options)

        # Infer kind
        link_options = [("PR", "https://github.com/launchableinc/cli/pull/1")]
        self.assertEqual(capture_links_from_options(link_options), [{
            "kind": LinkKind.GITHUB_PULL_REQUEST.name,
            "title": "PR",
            "url": "https://github.com/launchableinc/cli/pull/1",
        }])

        # Explicit kind
        link_options = [("GITHUB_PULL_REQUEST|PR", "https://github.com/launchableinc/cli/pull/1")]
        self.assertEqual(capture_links_from_options(link_options), [{
            "kind": LinkKind.GITHUB_PULL_REQUEST.name,
            "title": "PR",
            "url": "https://github.com/launchableinc/cli/pull/1",
        }])

    def test_capture_links(self):
        # Capture from environment
        envs = {
            "GITHUB_PULL_REQUEST_URL": "https://github.com/launchableinc/cli/pull/1"
        }
        link_options = []
        self.assertEqual(capture_links(link_options, envs), [{
            "kind": LinkKind.GITHUB_PULL_REQUEST.name,
            "title": "",
            "url": "https://github.com/launchableinc/cli/pull/1",
        }])

        # Priority check
        envs = {
            "GITHUB_PULL_REQUEST_URL": "https://github.com/launchableinc/cli/pull/1"
        }
        link_options = [("GITHUB_PULL_REQUEST|PR", "https://github.com/launchableinc/cli/pull/2")]
        self.assertEqual(capture_links(link_options, envs), [{
            "kind": LinkKind.GITHUB_PULL_REQUEST.name,
            "title": "PR",
            "url": "https://github.com/launchableinc/cli/pull/2",
        }])
