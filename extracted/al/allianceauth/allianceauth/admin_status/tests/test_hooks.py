import requests
import requests_mock

from allianceauth.admin_status.hooks import (
    Announcement,
    AppAnnouncementHook,
    get_all_applications_announcements,
    _fetch_list_from_gitlab,
    _fetch_list_from_github,
)
from allianceauth.utils.testing import NoSocketsTestCase
from unittest.mock import patch


class TestAnnouncementDataclass(NoSocketsTestCase):
    def test_build_from_gitlab_issue_dict_and_hash_is_stable(self):
        gitlab_issue = {
            "web_url": "https://gitlab.example/1",
            "iid": 42,
            "title": "Fix bug",
        }
        ann = Announcement.build_from_gitlab_issue_dict("MyApp", gitlab_issue)
        self.assertEqual(ann.application_name, "MyApp")
        self.assertEqual(ann.announcement_url, "https://gitlab.example/1")
        self.assertEqual(ann.announcement_number, 42)
        self.assertEqual(ann.announcement_text, "Fix bug")
        # hash should be deterministic for same app and issue number
        expected_hash = Announcement(
            "MyApp", gitlab_issue["web_url"], gitlab_issue["iid"], gitlab_issue["title"]
        ).get_hash()
        self.assertEqual(ann.get_hash(), expected_hash)

    def test_build_from_github_issue_dict_and_hash_is_stable(self):
        github_issue = {
            "html_url": "https://github.example/2",
            "number": 7,
            "title": "New feature",
        }
        ann = Announcement.build_from_github_issue_dict("OtherApp", github_issue)
        self.assertEqual(ann.application_name, "OtherApp")
        self.assertEqual(ann.announcement_url, "https://github.example/2")
        self.assertEqual(ann.announcement_number, 7)
        self.assertEqual(ann.announcement_text, "New feature")
        expected_hash = Announcement(
            "OtherApp",
            github_issue["html_url"],
            github_issue["number"],
            github_issue["title"],
        ).get_hash()
        self.assertEqual(ann.get_hash(), expected_hash)


class TestAppAnnouncementHookIntegration(NoSocketsTestCase):
    @requests_mock.mock()
    def test_gitlab_hook_fetches_and_builds_announcements(self, requests_mocker):
        namespace = "owner/repo"
        url = f"https://gitlab.com/api/v4/projects/owner%2Frepo/issues?labels=announcement&state=opened"
        gitlab_payload = [
            {
                "web_url": "https://gitlab.example/issue/1",
                "iid": 1,
                "title": "Issue One",
            }
        ]
        requests_mocker.get(url, json=gitlab_payload)
        hook = AppAnnouncementHook(
            "MyApp", namespace, AppAnnouncementHook.Service.GITLAB
        )
        announcements = hook.get_announcement_list()
        self.assertEqual(len(announcements), 1)
        ann = announcements[0]
        self.assertEqual(ann.application_name, "MyApp")
        self.assertEqual(ann.announcement_url, "https://gitlab.example/issue/1")
        self.assertEqual(ann.announcement_number, 1)
        self.assertEqual(ann.announcement_text, "Issue One")

    @requests_mock.mock()
    def test_github_hook_fetches_and_builds_announcements(self, requests_mocker):
        namespace = "owner/repo"
        url = f"https://api.github.com/repos/{namespace}/issues?labels=announcement"
        github_payload = [
            {
                "html_url": "https://github.example/issue/2",
                "number": 2,
                "title": "Issue Two",
            }
        ]
        requests_mocker.get(url, json=github_payload)
        hook = AppAnnouncementHook(
            "GHApp", namespace, AppAnnouncementHook.Service.GITHUB
        )
        announcements = hook.get_announcement_list()
        self.assertEqual(len(announcements), 1)
        ann = announcements[0]
        self.assertEqual(ann.application_name, "GHApp")
        self.assertEqual(ann.announcement_url, "https://github.example/issue/2")
        self.assertEqual(ann.announcement_number, 2)
        self.assertEqual(ann.announcement_text, "Issue Two")


class TestFetchListHelpers(NoSocketsTestCase):
    @requests_mock.mock()
    def test_fetch_list_from_gitlab_handles_pagination_and_combines_pages(
        self, requests_mocker
    ):
        url = "https://gitlab.com/api/v4/projects/allianceauth%2Fallianceauth/repository/tags"
        tags = [{"name": "v1"}, {"name": "v2"}, {"name": "v3"}]

        # callback that simulates paging
        def callback(request, context):
            page = int(request.qs["page"][0])
            page_size = 1
            start = (page - 1) * page_size
            end = start + page_size
            if page > 3:
                context.status_code = 200
                return []
            context.headers["x-total-pages"] = "3"
            return tags[start:end]

        requests_mocker.get(url, json=callback, headers={"x-total-pages": "3"})
        result = _fetch_list_from_gitlab(url, max_pages=5)
        self.assertEqual(result, tags)

    @requests_mock.mock()
    def test_fetch_list_from_gitlab_returns_empty_on_http_error(self, requests_mocker):
        url = "https://gitlab.com/api/v4/projects/allianceauth%2Fallianceauth/repository/tags"
        requests_mocker.get(url, status_code=500)
        result = _fetch_list_from_gitlab(url)
        self.assertEqual(result, [])

    @requests_mock.mock()
    def test_fetch_list_from_github_handles_pagination_link_header(
        self, requests_mocker
    ):
        url = "https://api.github.com/repos/owner/repo/issues?labels=announcement"
        page1 = [{"id": 1}]
        page2 = [{"id": 2}]

        # serve different pages based on the `page` query parameter
        def callback(request, context):
            page = int(request.qs.get("page", ["1"])[0])
            if page == 1:
                context.headers["link"] = (
                    '<https://api.github.com/repos/owner/repo/issues?page=2>; rel="next"'
                )
                return page1
            if page == 2:
                return page2
            return []

        requests_mocker.get(url, json=callback)
        result = _fetch_list_from_github(url, max_pages=5)
        ids = {item.get("id") for item in result}
        self.assertTrue({1, 2}.issubset(ids))

    @requests_mock.mock()
    def test_fetch_list_from_github_returns_empty_on_request_exception(
        self, requests_mocker
    ):
        url = "https://api.github.com/repos/owner/repo/issues?labels=announcement"
        requests_mocker.get(url, exc=requests.exceptions.Timeout)
        result = _fetch_list_from_github(url)
        self.assertEqual(result, [])


class TestGetAllApplicationsAnnouncements(NoSocketsTestCase):
    def test_get_all_applications_announcements_uses_cache_and_limits_results(self):
        # prepare a hook object with an app_name and a callable get_announcement_list
        class DummyHook:
            def __init__(self, app_name, anns):
                self.app_name = app_name
                self._anns = anns

            def get_announcement_list(self):
                return self._anns

        anns = [
            Announcement("App", f"https://example/{i}", i, f"title {i}")
            for i in range(15)
        ]
        hook = DummyHook("App", anns)

        with patch(
            "allianceauth.admin_status.hooks.get_hooks", return_value=[lambda: hook]
        ):
            result = get_all_applications_announcements()
            self.assertEqual(len(result), 10)
            self.assertEqual(result[0].announcement_number, 0)

    def test_get_all_applications_announcements_handles_http_error_and_skips_hook(
        self,
    ):
        class DummyHook:
            def __init__(self, app_name):
                self.app_name = app_name

            def get_announcement_list(self):
                raise requests.HTTPError()

        hook = DummyHook("AppErr")

        with patch(
            "allianceauth.admin_status.hooks.get_hooks",
            return_value=[lambda: hook],
        ):
            result = get_all_applications_announcements()
            self.assertEqual(result, [])
