import pytest

from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.users.user import User
from cnvrgv2.proxy import Proxy
from cnvrgv2.utils.json_api_format import JAF


class TestUser:

    def test_user_init(self):
        name = "Israel Israeli"
        bio = "Working at cnvrg"
        email = "israeli.israeli@walla.co.il"
        attr = {
            "name": name,
            "bio": bio,
            "email": email
        }
        user = User(domain="domain", token="token", attributes=attr)

        assert user.name == name
        assert user.bio == bio

    def test_user_valid_update_success(self, mocker):
        username = "israeli123"
        name = "Israel Israeli"
        company = "cnvrg.io"
        bio = "A fullstack developer"
        time_zone = "Asia/Jerusalem"

        def mock_call_api(*args, **kwargs):
            response = {
                "data": {
                    "id": "1",
                    "type": "user",
                    "attributes": {
                        "username": username,
                        "name": name,
                        "company": company,
                        "bio": bio,
                        "time_zone": time_zone
                    }
                }
            }

            return JAF(response=response)

        mock_response = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        user = User(domain="domain", token="token")
        user.update(
            **{"name": name,
               "company": company,
               "bio": bio,
               "time_zone": time_zone})

        assert mock_response.call_count == 1
        assert user.name == name
        assert user.bio == bio
        assert user.company == company
        assert user.time_zone == time_zone

    def test_user_save_success(self, mocker):
        username = "israeli123"
        name = "Israel Israeli"
        company = "cnvrg.io"
        bio = "A fullstack developer "
        time_zone = "Asia/Jerusalem"

        def mock_call_api(*args, **kwargs):
            response = {
                "data": {
                    "id": "17",
                    "type": "project",
                    "attributes": {
                        "username": username,
                        "name": name,
                        "company": company,
                        "bio": bio,
                        "time_zone": time_zone
                    }
                }
            }

            return JAF(response=response)

        mock_response = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        user = User(domain="domain", token="token")
        user.name = name
        user.bio = bio
        user.company = company
        user.time_zone = time_zone
        user.save()

        assert mock_response.call_count == 1
        assert user.name == name
        assert user.bio == bio
        assert user.company == company
        assert user.time_zone == time_zone

    def test_user_update_fake_icon_fail(self):
        file_path = "REALLY/FAKE/PATH.file"
        user = User(domain="domain", token="token",
                    attributes={
                        "icon": "https://fakeimg.com/img.png",
                        "name": "Israel Israeli",
                        "email": "israeli.israeli@walla.co.il"
                    })

        with pytest.raises(CnvrgArgumentsError):
            user.update(**{"icon": file_path})

    def test_user_update_fake_vscode_settings_fail(self):
        file_path = "REALLY/FAKE/PATH.file"
        user = User(
            domain="domain",
            token="token",
            attributes={
                "icon": "https://fakeimg.com/img.png",
                "name": "Israel Israeli",
                "email": "israeli.israeli@walla.co.il"
            }
        )

        with pytest.raises(CnvrgArgumentsError):
            user.update(**{"vscode_settings": file_path})

    def test_user_leave_org_success(self, mocker):
        # Void leave org.
        mock_leave = mocker.patch.object(Proxy, "call_api")
        user = User(domain="Domain", token="Token", attributes={
            "organizations": [
                {"id": 1, "slug": "MY_ORG"},
                {"id": 2, "slug": "MY_OTHER_ORG"}
            ],
            "email": "israeli.israeli@walla.co.il"
        },
                    )
        org = user.organizations[0]  # MY_ORG

        user.leave_org(org["slug"])

        assert mock_leave.call_count == 1
        assert org not in user.organizations
