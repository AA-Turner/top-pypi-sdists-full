from __future__ import annotations

from steel import Steel
from steel._utils import parse_datetime

from .harness import conform


def make(base_url: str, api_key: str, strict: bool) -> Steel:
    return Steel(base_url=base_url, steel_api_key=api_key, max_retries=0, _strict_response_validation=strict)


def test_pdf_full() -> None:
    def call(client: Steel) -> object:
        return client.pdf(
            url="https://example.com",
            delay=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            region={},
            use_proxy=True,
        )

    conform("pdf/full", make, call)


def test_pdf_required() -> None:
    def call(client: Steel) -> object:
        return client.pdf(url="https://example.com")

    conform("pdf/required", make, call)


def test_pdf_nulls() -> None:
    def call(client: Steel) -> object:
        return client.pdf(url="https://example.com")

    conform("pdf/nulls", make, call)


def test_scrape_full() -> None:
    def call(client: Steel) -> object:
        return client.scrape(
            url="url",
            delay=0,
            format=["html"],
            pdf=True,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            region={},
            screenshot=True,
            use_proxy=True,
        )

    conform("scrape/full", make, call)


def test_scrape_required() -> None:
    def call(client: Steel) -> object:
        return client.scrape(url="url")

    conform("scrape/required", make, call)


def test_scrape_nulls() -> None:
    def call(client: Steel) -> object:
        return client.scrape(url="url")

    conform("scrape/nulls", make, call)


def test_screenshot_full() -> None:
    def call(client: Steel) -> object:
        return client.screenshot(
            url="https://example.com",
            delay=0,
            full_page=True,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            region={},
            use_proxy=True,
        )

    conform("screenshot/full", make, call)


def test_screenshot_required() -> None:
    def call(client: Steel) -> object:
        return client.screenshot(url="https://example.com")

    conform("screenshot/required", make, call)


def test_screenshot_nulls() -> None:
    def call(client: Steel) -> object:
        return client.screenshot(url="https://example.com")

    conform("screenshot/nulls", make, call)


def test_api_keys_create_full() -> None:
    def call(client: Steel) -> object:
        return client.api_keys.create(
            name="name", project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", scope_type="project"
        )

    conform("api_keys.create/full", make, call)


def test_api_keys_create_required() -> None:
    def call(client: Steel) -> object:
        return client.api_keys.create()

    conform("api_keys.create/required", make, call)


def test_api_keys_create_nulls() -> None:
    def call(client: Steel) -> object:
        return client.api_keys.create()

    conform("api_keys.create/nulls", make, call)


def test_api_keys_create_unknown() -> None:
    def call(client: Steel) -> object:
        return client.api_keys.create()

    conform("api_keys.create/unknown", make, call)


def test_credentials_create_full() -> None:
    def call(client: Steel) -> object:
        return client.credentials.create(
            value={"foo": "string"},
            label="label",
            namespace="namespace",
            origin="origin",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

    conform("credentials.create/full", make, call)


def test_credentials_create_required() -> None:
    def call(client: Steel) -> object:
        return client.credentials.create(value={"foo": "string"})

    conform("credentials.create/required", make, call)


def test_credentials_create_nulls() -> None:
    def call(client: Steel) -> object:
        return client.credentials.create(value={"foo": "string"})

    conform("credentials.create/nulls", make, call)


def test_credentials_update_full() -> None:
    def call(client: Steel) -> object:
        return client.credentials.update(
            label="label",
            namespace="namespace",
            origin="origin",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            value={"foo": "string"},
        )

    conform("credentials.update/full", make, call)


def test_credentials_update_required() -> None:
    def call(client: Steel) -> object:
        return client.credentials.update()

    conform("credentials.update/required", make, call)


def test_credentials_update_nulls() -> None:
    def call(client: Steel) -> object:
        return client.credentials.update()

    conform("credentials.update/nulls", make, call)


def test_credentials_list_full() -> None:
    def call(client: Steel) -> object:
        return client.credentials.list(
            namespace="namespace", origin="origin", project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
        )

    conform("credentials.list/full", make, call)


def test_credentials_list_required() -> None:
    def call(client: Steel) -> object:
        return client.credentials.list()

    conform("credentials.list/required", make, call)


def test_credentials_list_nulls() -> None:
    def call(client: Steel) -> object:
        return client.credentials.list()

    conform("credentials.list/nulls", make, call)


def test_credentials_list_escaped() -> None:
    def call(client: Steel) -> object:
        return client.credentials.list(
            namespace="a b/c?d#e%f+g&h=i é", origin="a b/c?d#e%f+g&h=i é", project_id="a b/c?d#e%f+g&h=i é"
        )

    conform("credentials.list/escaped", make, call)


def test_credentials_delete_full() -> None:
    def call(client: Steel) -> object:
        return client.credentials.delete(
            origin="origin", namespace="namespace", project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
        )

    conform("credentials.delete/full", make, call)


def test_credentials_delete_required() -> None:
    def call(client: Steel) -> object:
        return client.credentials.delete(origin="origin")

    conform("credentials.delete/required", make, call)


def test_credentials_delete_nulls() -> None:
    def call(client: Steel) -> object:
        return client.credentials.delete(origin="origin")

    conform("credentials.delete/nulls", make, call)


def test_extensions_update_full() -> None:
    def call(client: Steel) -> object:
        return client.extensions.update("extensionId", file=b"Example data", url="https://example.com")

    conform("extensions.update/full", make, call)


def test_extensions_update_required() -> None:
    def call(client: Steel) -> object:
        return client.extensions.update("extensionId")

    conform("extensions.update/required", make, call)


def test_extensions_update_nulls() -> None:
    def call(client: Steel) -> object:
        return client.extensions.update("extensionId")

    conform("extensions.update/nulls", make, call)


def test_extensions_update_escaped() -> None:
    def call(client: Steel) -> object:
        return client.extensions.update("a b/c?d#e%f+g&h=i é")

    conform("extensions.update/escaped", make, call)


def test_extensions_list_full() -> None:
    def call(client: Steel) -> object:
        return client.extensions.list()

    conform("extensions.list/full", make, call)


def test_extensions_list_required() -> None:
    def call(client: Steel) -> object:
        return client.extensions.list()

    conform("extensions.list/required", make, call)


def test_extensions_list_nulls() -> None:
    def call(client: Steel) -> object:
        return client.extensions.list()

    conform("extensions.list/nulls", make, call)


def test_extensions_delete_full() -> None:
    def call(client: Steel) -> object:
        return client.extensions.delete("extensionId")

    conform("extensions.delete/full", make, call)


def test_extensions_delete_required() -> None:
    def call(client: Steel) -> object:
        return client.extensions.delete("extensionId")

    conform("extensions.delete/required", make, call)


def test_extensions_delete_nulls() -> None:
    def call(client: Steel) -> object:
        return client.extensions.delete("extensionId")

    conform("extensions.delete/nulls", make, call)


def test_extensions_delete_escaped() -> None:
    def call(client: Steel) -> object:
        return client.extensions.delete("a b/c?d#e%f+g&h=i é")

    conform("extensions.delete/escaped", make, call)


def test_extensions_delete_all_full() -> None:
    def call(client: Steel) -> object:
        return client.extensions.delete_all()

    conform("extensions.delete_all/full", make, call)


def test_extensions_delete_all_required() -> None:
    def call(client: Steel) -> object:
        return client.extensions.delete_all()

    conform("extensions.delete_all/required", make, call)


def test_extensions_delete_all_nulls() -> None:
    def call(client: Steel) -> object:
        return client.extensions.delete_all()

    conform("extensions.delete_all/nulls", make, call)


def test_extensions_download_full() -> None:
    def call(client: Steel) -> object:
        return client.extensions.download("extensionId").read().decode("utf-8")

    conform("extensions.download/full", make, call)


def test_extensions_download_required() -> None:
    def call(client: Steel) -> object:
        return client.extensions.download("extensionId").read().decode("utf-8")

    conform("extensions.download/required", make, call)


def test_extensions_download_escaped() -> None:
    def call(client: Steel) -> object:
        return client.extensions.download("a b/c?d#e%f+g&h=i é").read().decode("utf-8")

    conform("extensions.download/escaped", make, call)


def test_extensions_upload_full() -> None:
    def call(client: Steel) -> object:
        return client.extensions.upload(file=b"Example data", url="https://example.com")

    conform("extensions.upload/full", make, call)


def test_extensions_upload_required() -> None:
    def call(client: Steel) -> object:
        return client.extensions.upload()

    conform("extensions.upload/required", make, call)


def test_extensions_upload_nulls() -> None:
    def call(client: Steel) -> object:
        return client.extensions.upload()

    conform("extensions.upload/nulls", make, call)


def test_files_list_full() -> None:
    def call(client: Steel) -> object:
        return client.files.list()

    conform("files.list/full", make, call)


def test_files_list_required() -> None:
    def call(client: Steel) -> object:
        return client.files.list()

    conform("files.list/required", make, call)


def test_files_list_nulls() -> None:
    def call(client: Steel) -> object:
        return client.files.list()

    conform("files.list/nulls", make, call)


def test_files_delete_full() -> None:
    def call(client: Steel) -> object:
        return client.files.delete("path")

    conform("files.delete/full", make, call)


def test_files_delete_required() -> None:
    def call(client: Steel) -> object:
        return client.files.delete("path")

    conform("files.delete/required", make, call)


def test_files_delete_escaped() -> None:
    def call(client: Steel) -> object:
        return client.files.delete("a b/c?d#e%f+g&h=i é")

    conform("files.delete/escaped", make, call)


def test_files_download_full() -> None:
    def call(client: Steel) -> object:
        return client.files.download("path").read().decode("utf-8")

    conform("files.download/full", make, call)


def test_files_download_required() -> None:
    def call(client: Steel) -> object:
        return client.files.download("path").read().decode("utf-8")

    conform("files.download/required", make, call)


def test_files_download_escaped() -> None:
    def call(client: Steel) -> object:
        return client.files.download("a b/c?d#e%f+g&h=i é").read().decode("utf-8")

    conform("files.download/escaped", make, call)


def test_files_upload_full() -> None:
    def call(client: Steel) -> object:
        return client.files.upload(file=b"Example data", path="path")

    conform("files.upload/full", make, call)


def test_files_upload_required() -> None:
    def call(client: Steel) -> object:
        return client.files.upload(file=b"Example data")

    conform("files.upload/required", make, call)


def test_files_upload_nulls() -> None:
    def call(client: Steel) -> object:
        return client.files.upload(file=b"Example data")

    conform("files.upload/nulls", make, call)


def test_profiles_create_full() -> None:
    def call(client: Steel) -> object:
        return client.profiles.create(
            user_data_dir=b"Example data",
            dimensions={
                "height": 0,
                "width": 0,
            },
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            proxy_url="https://example.com",
            use_proxy="useProxy",
            user_agent="userAgent",
        )

    conform("profiles.create/full", make, call)


def test_profiles_create_required() -> None:
    def call(client: Steel) -> object:
        return client.profiles.create(user_data_dir=b"Example data")

    conform("profiles.create/required", make, call)


def test_profiles_create_nulls() -> None:
    def call(client: Steel) -> object:
        return client.profiles.create(user_data_dir=b"Example data")

    conform("profiles.create/nulls", make, call)


def test_profiles_create_unknown() -> None:
    def call(client: Steel) -> object:
        return client.profiles.create(user_data_dir=b"Example data")

    conform("profiles.create/unknown", make, call)


def test_profiles_update_full() -> None:
    def call(client: Steel) -> object:
        return client.profiles.update(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            query_project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            user_data_dir=b"Example data",
            dimensions={
                "height": 0,
                "width": 0,
            },
            body_project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            proxy_url="https://example.com",
            use_proxy="useProxy",
            user_agent="userAgent",
        )

    conform("profiles.update/full", make, call)


def test_profiles_update_required() -> None:
    def call(client: Steel) -> object:
        return client.profiles.update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", user_data_dir=b"Example data")

    conform("profiles.update/required", make, call)


def test_profiles_update_nulls() -> None:
    def call(client: Steel) -> object:
        return client.profiles.update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", user_data_dir=b"Example data")

    conform("profiles.update/nulls", make, call)


def test_profiles_update_unknown() -> None:
    def call(client: Steel) -> object:
        return client.profiles.update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", user_data_dir=b"Example data")

    conform("profiles.update/unknown", make, call)


def test_profiles_update_escaped() -> None:
    def call(client: Steel) -> object:
        return client.profiles.update(
            "a b/c?d#e%f+g&h=i é", query_project_id="a b/c?d#e%f+g&h=i é", user_data_dir=b"Example data"
        )

    conform("profiles.update/escaped", make, call)


def test_profiles_list_full() -> None:
    def call(client: Steel) -> object:
        return client.profiles.list(project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("profiles.list/full", make, call)


def test_profiles_list_required() -> None:
    def call(client: Steel) -> object:
        return client.profiles.list()

    conform("profiles.list/required", make, call)


def test_profiles_list_nulls() -> None:
    def call(client: Steel) -> object:
        return client.profiles.list()

    conform("profiles.list/nulls", make, call)


def test_profiles_list_unknown() -> None:
    def call(client: Steel) -> object:
        return client.profiles.list()

    conform("profiles.list/unknown", make, call)


def test_profiles_list_escaped() -> None:
    def call(client: Steel) -> object:
        return client.profiles.list(project_id="a b/c?d#e%f+g&h=i é")

    conform("profiles.list/escaped", make, call)


def test_profiles_get_full() -> None:
    def call(client: Steel) -> object:
        return client.profiles.get(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
        )

    conform("profiles.get/full", make, call)


def test_profiles_get_required() -> None:
    def call(client: Steel) -> object:
        return client.profiles.get("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("profiles.get/required", make, call)


def test_profiles_get_nulls() -> None:
    def call(client: Steel) -> object:
        return client.profiles.get("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("profiles.get/nulls", make, call)


def test_profiles_get_unknown() -> None:
    def call(client: Steel) -> object:
        return client.profiles.get("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("profiles.get/unknown", make, call)


def test_profiles_get_escaped() -> None:
    def call(client: Steel) -> object:
        return client.profiles.get("a b/c?d#e%f+g&h=i é", project_id="a b/c?d#e%f+g&h=i é")

    conform("profiles.get/escaped", make, call)


def test_projects_retrieve_full() -> None:
    def call(client: Steel) -> object:
        return client.projects.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("projects.retrieve/full", make, call)


def test_projects_retrieve_required() -> None:
    def call(client: Steel) -> object:
        return client.projects.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("projects.retrieve/required", make, call)


def test_projects_retrieve_nulls() -> None:
    def call(client: Steel) -> object:
        return client.projects.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("projects.retrieve/nulls", make, call)


def test_projects_retrieve_escaped() -> None:
    def call(client: Steel) -> object:
        return client.projects.retrieve("a b/c?d#e%f+g&h=i é")

    conform("projects.retrieve/escaped", make, call)


def test_projects_list_full() -> None:
    def call(client: Steel) -> object:
        return client.projects.list()

    conform("projects.list/full", make, call)


def test_projects_list_required() -> None:
    def call(client: Steel) -> object:
        return client.projects.list()

    conform("projects.list/required", make, call)


def test_projects_list_nulls() -> None:
    def call(client: Steel) -> object:
        return client.projects.list()

    conform("projects.list/nulls", make, call)


def test_sessions_create_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.create(
            block_ads=True,
            ca_certificates=["string"],
            concurrency=-9007199254740991,
            credentials={
                "auto_submit": True,
                "blur_fields": True,
                "credential_provider": "credentialProvider",
                "exact_origin": True,
                "origins": ["string"],
            },
            debug_config={
                "interactive": True,
                "system_cursor": True,
            },
            device_config={"device": "desktop"},
            dimensions={
                "height": -9007199254740991,
                "width": -9007199254740991,
            },
            experimental_features=["string"],
            extension_ids=["string"],
            fullscreen=True,
            headless=True,
            inactivity_timeout=1,
            is_selenium=True,
            metadata={"foo": "string"},
            namespace="namespace",
            optimize_bandwidth=True,
            persist_profile=True,
            profile_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            proxy_url="https://example.com",
            recording=True,
            region={},
            session_context={
                "cookies": [
                    {
                        "name": "name",
                        "value": "value",
                        "domain": "domain",
                        "expires": 0,
                        "http_only": True,
                        "partition_key": {
                            "has_cross_site_ancestor": True,
                            "top_level_site": "topLevelSite",
                        },
                        "path": "path",
                        "priority": "Low",
                        "same_party": True,
                        "same_site": "Strict",
                        "secure": True,
                        "session": True,
                        "size": 0,
                        "source_port": 0,
                        "source_scheme": "Unset",
                        "url": "url",
                    }
                ],
                "indexed_db": {
                    "foo": [
                        {
                            "id": 0,
                            "data": [
                                {
                                    "id": 0,
                                    "name": "name",
                                    "records": [
                                        {
                                            "key": {},
                                            "value": {},
                                            "blob_files": [
                                                {
                                                    "blob_number": 0,
                                                    "mime_type": "mimeType",
                                                    "size": 0,
                                                    "filename": "filename",
                                                    "last_modified": parse_datetime("2019-12-27T18:11:19.117Z"),
                                                    "path": "path",
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ],
                            "name": "name",
                        }
                    ]
                },
                "local_storage": {"foo": {"foo": "string"}},
                "session_storage": {"foo": {"foo": "string"}},
            },
            session_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            solve_captcha=True,
            stealth_config={
                "auto_captcha_solving": True,
                "humanize_interactions": True,
                "skip_fingerprint_injection": True,
            },
            api_timeout=-9007199254740991,
            use_proxy=True,
            user_agent="userAgent",
        )

    conform("sessions.create/full", make, call)


def test_sessions_create_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.create()

    conform("sessions.create/required", make, call)


def test_sessions_create_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.create()

    conform("sessions.create/nulls", make, call)


def test_sessions_create_unknown() -> None:
    def call(client: Steel) -> object:
        return client.sessions.create()

    conform("sessions.create/unknown", make, call)


def test_sessions_retrieve_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.retrieve/full", make, call)


def test_sessions_retrieve_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.retrieve/required", make, call)


def test_sessions_retrieve_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.retrieve/nulls", make, call)


def test_sessions_retrieve_unknown() -> None:
    def call(client: Steel) -> object:
        return client.sessions.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.retrieve/unknown", make, call)


def test_sessions_retrieve_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.retrieve("a b/c?d#e%f+g&h=i é")

    conform("sessions.retrieve/escaped", make, call)


def test_sessions_list_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.list(
            created_after=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_before=parse_datetime("2019-12-27T18:11:19.117Z"),
            cursor_id="cursorId",
            limit=1,
            metadata={"foo": "x"},
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            release_reason="user_requested",
            signal=["captcha_encountered"],
            status="live",
        )

    conform("sessions.list/full", make, call)


def test_sessions_list_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.list()

    conform("sessions.list/required", make, call)


def test_sessions_list_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.list()

    conform("sessions.list/nulls", make, call)


def test_sessions_list_unknown() -> None:
    def call(client: Steel) -> object:
        return client.sessions.list()

    conform("sessions.list/unknown", make, call)


def test_sessions_list_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.list(cursor_id="a b/c?d#e%f+g&h=i é", project_id="a b/c?d#e%f+g&h=i é")

    conform("sessions.list/escaped", make, call)


def test_sessions_list_pages() -> None:
    def call(client: Steel) -> object:
        return [item.id for item in client.sessions.list()]

    conform("sessions.list/pages", make, call)


def test_sessions_agent_traces_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.agent_traces(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            end_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            event_types=["string"],
            limit=1,
            namespace="namespace",
            offset=0,
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

    conform("sessions.agent_traces/full", make, call)


def test_sessions_agent_traces_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.agent_traces("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.agent_traces/required", make, call)


def test_sessions_agent_traces_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.agent_traces("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.agent_traces/nulls", make, call)


def test_sessions_agent_traces_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.agent_traces("a b/c?d#e%f+g&h=i é", namespace="a b/c?d#e%f+g&h=i é")

    conform("sessions.agent_traces/escaped", make, call)


def test_sessions_commands_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.commands(
            "sessionId",
            idempotency_key="idempotency-key",
            commands={
                "command": "navigate",
                "url": "x",
                "tab": "t321669910225",
            },
            after="x",
            events_after="c-321669910225",
            observe={
                "mode": "none",
                "base": "x",
                "compact": True,
                "depth": 0,
                "interactive": True,
                "tab": "t321669910225",
            },
        )

    conform("sessions.commands/full", make, call)


def test_sessions_commands_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.commands(
            "sessionId",
            commands={
                "command": "navigate",
                "url": "x",
            },
        )

    conform("sessions.commands/required", make, call)


def test_sessions_commands_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.commands(
            "sessionId",
            commands={
                "command": "navigate",
                "url": "x",
            },
        )

    conform("sessions.commands/nulls", make, call)


def test_sessions_commands_unknown() -> None:
    def call(client: Steel) -> object:
        return client.sessions.commands(
            "sessionId",
            commands={
                "command": "navigate",
                "url": "x",
            },
        )

    conform("sessions.commands/unknown", make, call)


def test_sessions_commands_variant_0_1() -> None:
    def call(client: Steel) -> object:
        return client.sessions.commands(
            "sessionId",
            commands={
                "command": "navigate",
                "url": "x",
            },
        )

    conform("sessions.commands/variant-0-1", make, call)


def test_sessions_commands_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.commands(
            "a b/c?d#e%f+g&h=i é",
            commands={
                "command": "navigate",
                "url": "x",
            },
        )

    conform("sessions.commands/escaped", make, call)


def test_sessions_computer_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.computer(
            "sessionId", action="move_mouse", coordinates=[0, 0], hold_keys=["string"], screenshot=True
        )

    conform("sessions.computer/full", make, call)


def test_sessions_computer_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.computer("sessionId", action="move_mouse", coordinates=[0, 0])

    conform("sessions.computer/required", make, call)


def test_sessions_computer_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.computer("sessionId", action="move_mouse", coordinates=[0, 0])

    conform("sessions.computer/nulls", make, call)


def test_sessions_computer_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.computer("a b/c?d#e%f+g&h=i é", action="move_mouse", coordinates=[0, 0])

    conform("sessions.computer/escaped", make, call)


def test_sessions_context_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.context("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.context/full", make, call)


def test_sessions_context_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.context("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.context/required", make, call)


def test_sessions_context_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.context("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.context/nulls", make, call)


def test_sessions_context_unknown() -> None:
    def call(client: Steel) -> object:
        return client.sessions.context("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.context/unknown", make, call)


def test_sessions_context_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.context("a b/c?d#e%f+g&h=i é")

    conform("sessions.context/escaped", make, call)


def test_sessions_cost_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.cost("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.cost/full", make, call)


def test_sessions_cost_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.cost("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.cost/required", make, call)


def test_sessions_cost_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.cost("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.cost/nulls", make, call)


def test_sessions_cost_unknown() -> None:
    def call(client: Steel) -> object:
        return client.sessions.cost("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.cost/unknown", make, call)


def test_sessions_cost_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.cost("a b/c?d#e%f+g&h=i é")

    conform("sessions.cost/escaped", make, call)


def test_sessions_events_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.events(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", compressed=True, limit=1, pointer="pointer"
        )

    conform("sessions.events/full", make, call)


def test_sessions_events_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.events("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.events/required", make, call)


def test_sessions_events_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.events("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.events/nulls", make, call)


def test_sessions_events_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.events("a b/c?d#e%f+g&h=i é", pointer="a b/c?d#e%f+g&h=i é")

    conform("sessions.events/escaped", make, call)


def test_sessions_hls_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.hls("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e").read().decode("utf-8")

    conform("sessions.hls/full", make, call)


def test_sessions_hls_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.hls("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e").read().decode("utf-8")

    conform("sessions.hls/required", make, call)


def test_sessions_hls_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.hls("a b/c?d#e%f+g&h=i é").read().decode("utf-8")

    conform("sessions.hls/escaped", make, call)


def test_sessions_live_details_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.live_details("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.live_details/full", make, call)


def test_sessions_live_details_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.live_details("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.live_details/required", make, call)


def test_sessions_live_details_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.live_details("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.live_details/nulls", make, call)


def test_sessions_live_details_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.live_details("a b/c?d#e%f+g&h=i é")

    conform("sessions.live_details/escaped", make, call)


def test_sessions_logs_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.logs(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            end_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            event_types=["string"],
            limit=1,
            namespace="namespace",
            offset=0,
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

    conform("sessions.logs/full", make, call)


def test_sessions_logs_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.logs("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.logs/required", make, call)


def test_sessions_logs_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.logs("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.logs/nulls", make, call)


def test_sessions_logs_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.logs("a b/c?d#e%f+g&h=i é", namespace="a b/c?d#e%f+g&h=i é")

    conform("sessions.logs/escaped", make, call)


def test_sessions_release_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.release("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.release/full", make, call)


def test_sessions_release_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.release("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.release/required", make, call)


def test_sessions_release_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.release("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.release/nulls", make, call)


def test_sessions_release_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.release("a b/c?d#e%f+g&h=i é")

    conform("sessions.release/escaped", make, call)


def test_sessions_release_all_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.release_all(project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.release_all/full", make, call)


def test_sessions_release_all_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.release_all()

    conform("sessions.release_all/required", make, call)


def test_sessions_release_all_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.release_all()

    conform("sessions.release_all/nulls", make, call)


def test_sessions_release_all_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.release_all(project_id="a b/c?d#e%f+g&h=i é")

    conform("sessions.release_all/escaped", make, call)


def test_sessions_replace_metadata_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.replace_metadata("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", metadata={"foo": "string"})

    conform("sessions.replace_metadata/full", make, call)


def test_sessions_replace_metadata_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.replace_metadata("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", metadata={"foo": "string"})

    conform("sessions.replace_metadata/required", make, call)


def test_sessions_replace_metadata_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.replace_metadata("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", metadata={"foo": "string"})

    conform("sessions.replace_metadata/nulls", make, call)


def test_sessions_replace_metadata_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.replace_metadata("a b/c?d#e%f+g&h=i é", metadata={"foo": "string"})

    conform("sessions.replace_metadata/escaped", make, call)


def test_sessions_signal_catalog_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.signal_catalog()

    conform("sessions.signal_catalog/full", make, call)


def test_sessions_signal_catalog_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.signal_catalog()

    conform("sessions.signal_catalog/required", make, call)


def test_sessions_signal_catalog_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.signal_catalog()

    conform("sessions.signal_catalog/nulls", make, call)


def test_sessions_signal_catalog_unknown() -> None:
    def call(client: Steel) -> object:
        return client.sessions.signal_catalog()

    conform("sessions.signal_catalog/unknown", make, call)


def test_sessions_update_metadata_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.update_metadata("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", metadata={"foo": "string"})

    conform("sessions.update_metadata/full", make, call)


def test_sessions_update_metadata_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.update_metadata("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", metadata={"foo": "string"})

    conform("sessions.update_metadata/required", make, call)


def test_sessions_update_metadata_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.update_metadata("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", metadata={"foo": None})

    conform("sessions.update_metadata/nulls", make, call)


def test_sessions_update_metadata_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.update_metadata("a b/c?d#e%f+g&h=i é", metadata={"foo": "string"})

    conform("sessions.update_metadata/escaped", make, call)


def test_sessions_captchas_solve_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.captchas.solve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", page_id="pageId", task_id="taskId", url="url"
        )

    conform("sessions.captchas.solve/full", make, call)


def test_sessions_captchas_solve_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.captchas.solve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.captchas.solve/required", make, call)


def test_sessions_captchas_solve_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.captchas.solve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.captchas.solve/nulls", make, call)


def test_sessions_captchas_solve_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.captchas.solve("a b/c?d#e%f+g&h=i é")

    conform("sessions.captchas.solve/escaped", make, call)


def test_sessions_captchas_solve_image_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.captchas.solve_image(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", image_x_path="imageXPath", input_x_path="inputXPath", url="url"
        )

    conform("sessions.captchas.solve_image/full", make, call)


def test_sessions_captchas_solve_image_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.captchas.solve_image(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", image_x_path="imageXPath", input_x_path="inputXPath"
        )

    conform("sessions.captchas.solve_image/required", make, call)


def test_sessions_captchas_solve_image_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.captchas.solve_image(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e", image_x_path="imageXPath", input_x_path="inputXPath"
        )

    conform("sessions.captchas.solve_image/nulls", make, call)


def test_sessions_captchas_solve_image_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.captchas.solve_image(
            "a b/c?d#e%f+g&h=i é", image_x_path="imageXPath", input_x_path="inputXPath"
        )

    conform("sessions.captchas.solve_image/escaped", make, call)


def test_sessions_captchas_status_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.captchas.status("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.captchas.status/full", make, call)


def test_sessions_captchas_status_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.captchas.status("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.captchas.status/required", make, call)


def test_sessions_captchas_status_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.captchas.status("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

    conform("sessions.captchas.status/nulls", make, call)


def test_sessions_captchas_status_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.captchas.status("a b/c?d#e%f+g&h=i é")

    conform("sessions.captchas.status/escaped", make, call)


def test_sessions_files_list_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.list("sessionId")

    conform("sessions.files.list/full", make, call)


def test_sessions_files_list_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.list("sessionId")

    conform("sessions.files.list/required", make, call)


def test_sessions_files_list_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.list("sessionId")

    conform("sessions.files.list/nulls", make, call)


def test_sessions_files_list_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.list("a b/c?d#e%f+g&h=i é")

    conform("sessions.files.list/escaped", make, call)


def test_sessions_files_delete_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.delete("path", session_id="sessionId")

    conform("sessions.files.delete/full", make, call)


def test_sessions_files_delete_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.delete("path", session_id="sessionId")

    conform("sessions.files.delete/required", make, call)


def test_sessions_files_delete_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.delete("a b/c?d#e%f+g&h=i é", session_id="a b/c?d#e%f+g&h=i é")

    conform("sessions.files.delete/escaped", make, call)


def test_sessions_files_delete_all_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.delete_all("sessionId")

    conform("sessions.files.delete_all/full", make, call)


def test_sessions_files_delete_all_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.delete_all("sessionId")

    conform("sessions.files.delete_all/required", make, call)


def test_sessions_files_delete_all_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.delete_all("a b/c?d#e%f+g&h=i é")

    conform("sessions.files.delete_all/escaped", make, call)


def test_sessions_files_download_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.download("path", session_id="sessionId").read().decode("utf-8")

    conform("sessions.files.download/full", make, call)


def test_sessions_files_download_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.download("path", session_id="sessionId").read().decode("utf-8")

    conform("sessions.files.download/required", make, call)


def test_sessions_files_download_escaped() -> None:
    def call(client: Steel) -> object:
        return (
            client.sessions.files.download("a b/c?d#e%f+g&h=i é", session_id="a b/c?d#e%f+g&h=i é")
            .read()
            .decode("utf-8")
        )

    conform("sessions.files.download/escaped", make, call)


def test_sessions_files_download_archive_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.download_archive("sessionId").read().decode("utf-8")

    conform("sessions.files.download_archive/full", make, call)


def test_sessions_files_download_archive_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.download_archive("sessionId").read().decode("utf-8")

    conform("sessions.files.download_archive/required", make, call)


def test_sessions_files_download_archive_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.download_archive("a b/c?d#e%f+g&h=i é").read().decode("utf-8")

    conform("sessions.files.download_archive/escaped", make, call)


def test_sessions_files_upload_full() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.upload("sessionId", file=b"Example data", path="path")

    conform("sessions.files.upload/full", make, call)


def test_sessions_files_upload_required() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.upload("sessionId", file=b"Example data")

    conform("sessions.files.upload/required", make, call)


def test_sessions_files_upload_nulls() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.upload("sessionId", file=b"Example data")

    conform("sessions.files.upload/nulls", make, call)


def test_sessions_files_upload_escaped() -> None:
    def call(client: Steel) -> object:
        return client.sessions.files.upload("a b/c?d#e%f+g&h=i é", file=b"Example data")

    conform("sessions.files.upload/escaped", make, call)
