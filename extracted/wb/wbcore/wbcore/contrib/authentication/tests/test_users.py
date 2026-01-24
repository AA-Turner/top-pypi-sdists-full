import pytest
from django.core import mail
from django.db.utils import IntegrityError
from faker import Faker
from pytest_mock import MockerFixture
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from wbcore.contrib.authentication.factories import UserFactory
from wbcore.contrib.authentication.models import User
from wbcore.contrib.authentication.viewsets.users import (
    activate_user,
    register_user,
    reset_password_email,
)
from wbcore.contrib.directory.models import Person

fake = Faker()


class TestUser:
    @pytest.fixture
    def test_user(self):
        return User()

    @pytest.fixture
    def test_user_data(self):
        return {
            "email": "john.neumann@intellineers.com",
            "password": "fake_password",
            "first_name": "John",
            "last_name": "Neumann",
        }

    def test_get_short_name(self, test_user_data):
        person = Person(first_name=test_user_data["first_name"], last_name=test_user_data["last_name"])
        user = User(profile=person)
        assert user.get_short_name() == test_user_data["first_name"]

    @pytest.mark.parametrize("is_valid", [True, False])
    def test_reset_password(self, is_valid: bool, mocker: MockerFixture, test_user, test_user_data):
        # Arrange
        mocker.patch.object(test_user, "email", test_user_data["email"])
        mock_password_reset_form = mocker.patch("django.contrib.auth.forms.PasswordResetForm")
        mock_instance = mock_password_reset_form.return_value
        mock_instance.is_valid.return_value = is_valid

        # Act
        test_user.reset_password(request="mocked_request")

        # Assert
        mock_password_reset_form.assert_called_once_with(data={"email": test_user_data["email"]})
        mock_instance.is_valid.assert_called_once()
        if is_valid:
            mock_instance.save.assert_called_once_with(
                request="mocked_request",
                email_template_name="password_reset_email.html",
                html_email_template_name="password_reset_email_html.html",
            )
        else:
            mock_instance.save.assert_not_called()

    def test_generate_and_verify_temporary_toke(self, mocker: MockerFixture, test_user):
        # Arrange
        other_user = User()
        # We need to mock an id, otherwise the generated tokens will be the same
        mocker.patch.object(test_user, "id", 1)
        mocker.patch.object(other_user, "id", 2)

        # Act
        user_token = test_user.generate_temporary_token()
        other_user_token = other_user.generate_temporary_token()

        # Assert
        assert test_user.verify_temporary_token(user_token)
        assert not test_user.verify_temporary_token(other_user_token)
        assert other_user.verify_temporary_token(other_user_token)
        assert not other_user.verify_temporary_token(user_token)

    @pytest.mark.django_db
    @pytest.mark.parametrize("first_name, last_name", [("John", "Neumann")])
    def test_generate_username(self, first_name: str, last_name: str, user_factory: UserFactory):
        username = User.generate_username(first_name, last_name)
        assert username == f"{first_name.lower()}-{last_name.lower()}"
        user_factory.create(username=username)
        username_1 = User.generate_username(first_name, last_name)
        assert username_1 == f"{first_name.lower()}-{last_name.lower()}-2"
        user_factory.create(username=username_1)
        assert User.generate_username(first_name, last_name) == f"{first_name.lower()}-{last_name.lower()}-3"

    def test_create_with_attributes(self, test_user_data, mocker: MockerFixture):
        # Arrange
        user_name = f"{test_user_data['first_name']}-{test_user_data['last_name']}"
        mock_user = mocker.Mock(spec=User)
        generate_user_name = mocker.patch(
            "wbcore.contrib.authentication.models.User.generate_username", return_value=user_name
        )
        create_user_mock = mocker.patch(
            "wbcore.contrib.authentication.models.User.objects.create_user", return_value=mock_user
        )

        # Act
        user = User.create_with_attributes(
            test_user_data["email"],
            test_user_data["password"],
            first_name=test_user_data["first_name"],
            last_name=test_user_data["last_name"],
        )

        # Assert
        assert user.check_password(test_user_data["password"])
        generate_user_name.assert_called_once_with(test_user_data["first_name"], test_user_data["last_name"])
        create_user_mock.assert_called_once_with(
            user_name,
            test_user_data["email"],
            test_user_data["password"],
            is_staff=False,
            is_superuser=False,
            is_active=False,
            is_register=False,
        )


class TestRegistrationAndActivationViews:
    @pytest.fixture
    def test_user(self):
        return User(
            password="fake_password",
            email="john.neumann@intellineers.com",
        )

    @pytest.fixture
    def registration_data(self, test_user):
        return {
            "email": test_user.email,
            "password": test_user.password,
            "first_name": "John",
            "last_name": "Neumann",
        }

    @pytest.fixture
    def missing_data_msg(self):
        return "email, first_name, last_name and password must be provided"

    @pytest.fixture
    def api_factory(self):
        return APIRequestFactory()

    @pytest.fixture
    def register_url(self):
        return reverse("wbcore:authentication:register")

    @pytest.mark.parametrize("should_fail", [True, False])
    def test_reset_password_with_user(self, should_fail, mocker: MockerFixture, test_user, api_factory):
        # Arrange
        mock_get_user = mocker.patch(
            "wbcore.contrib.authentication.models.users.UserManager.get",
            return_value=None if should_fail else test_user,
        )
        mock_reset_password = mocker.patch.object(test_user, "reset_password")
        url = reverse("wbcore:authentication:reset_password_email")

        # Act
        request = api_factory.post(url, {"email": test_user.email})
        response = reset_password_email(request)

        # Assert
        mock_get_user.assert_called_once_with(email="john.neumann@intellineers.com")

        if should_fail:
            mock_reset_password.assert_not_called()
        else:
            mock_reset_password.assert_called_once()
            assert response.data["status"] == "ok"
            assert (
                response.data["msg"]
                == "If the email matches a user, it will receive an email inviting him to reset his password."
            )
        assert response.status_code == 200

    @pytest.mark.parametrize("user_is_already_registered,", [True, False])
    def test_registration(
        self,
        user_is_already_registered,
        mocker: MockerFixture,
        test_user,
        api_factory,
        register_url,
        registration_data,
    ):
        # Arrange
        mocker.patch.object(test_user, "id", 1)
        patch_path = "wbcore.contrib.authentication.models.users.User.create_with_attributes"
        if user_is_already_registered:
            mock_create_with_attributes = mocker.patch(patch_path, side_effect=IntegrityError)
        else:
            mock_create_with_attributes = mocker.patch(patch_path, return_value=test_user)
        current_mailbox_count = len(mail.outbox)

        # Act
        request = api_factory.post(register_url, registration_data)
        response = register_user(request)

        # Assert
        mock_create_with_attributes.assert_called_once_with(
            registration_data["email"],
            registration_data["password"],
            first_name=registration_data["first_name"],
            last_name=registration_data["last_name"],
        )
        if user_is_already_registered:
            assert response.status_code == 409
            assert response.data["status"] == "fail"
            assert response.data["msg"] == "Your account already exists"
            assert len(mail.outbox) == current_mailbox_count
        else:
            assert response.status_code == 200
            assert response.data["status"] == "success"
            assert response.data["msg"] == "Please confirm your email address to complete the registration"
            assert len(mail.outbox) == current_mailbox_count + 1

            sent_mail = mail.outbox[-1]
            assert sent_mail.subject == "Activate your account."
            assert sent_mail.to == [test_user.email]

    @pytest.mark.parametrize("password", ["", "a" * 255])
    def test_registration_with_invalid_password(
        self, password, api_factory, register_url, registration_data, missing_data_msg
    ):
        # Arrange
        current_mailbox_count = len(mail.outbox)

        # Act
        request = api_factory.post(
            register_url,
            {
                "email": registration_data["email"],
                "password": password,
                "first_name": registration_data["first_name"],
                "last_name": registration_data["last_name"],
            },
        )
        response = register_user(request)

        # Assert
        assert response.status_code == 400
        assert response.data["status"] == "fail"
        if not password:
            assert response.data["msg"] == missing_data_msg
        else:
            assert (
                response.data["msg"] == "password is too long. please provider a password shorter than 128 characters."
            )
        assert len(mail.outbox) == current_mailbox_count

    @pytest.mark.parametrize("email", ["", "a" * 255 + "@test.com"])
    def test_registration_with_invalid_email(
        self, email, api_factory, register_url, registration_data, missing_data_msg
    ):
        # Arrange
        current_mailbox_count = len(mail.outbox)

        # Act
        request = api_factory.post(
            register_url,
            {
                "email": email,
                "password": registration_data["password"],
                "first_name": registration_data["first_name"],
                "last_name": registration_data["last_name"],
            },
        )
        response = register_user(request)

        # Assert
        assert response.status_code == 400
        assert response.data["status"] == "fail"
        if not email:
            assert response.data["msg"] == missing_data_msg
        else:
            assert response.data["msg"] == "email is too long. please provider an email shorter than 255 characters."
        assert len(mail.outbox) == current_mailbox_count

    @pytest.mark.parametrize(
        "first_name, last_name", [("", ""), ("a" * 101, ""), ("", "b" * 101), ("a" * 101, "b" * 101)]
    )
    def test_registration_with_invalid_name(
        self, first_name, last_name, api_factory, register_url, registration_data, missing_data_msg
    ):
        # Arrange
        current_mailbox_count = len(mail.outbox)

        # Act
        request = api_factory.post(
            register_url,
            {
                "email": registration_data["email"],
                "password": registration_data["password"],
                "first_name": first_name,
                "last_name": last_name,
            },
        )
        response = register_user(request)

        # Assert
        assert response.status_code == 400
        assert response.data["status"] == "fail"
        if len(first_name) > 100 or len(last_name) > 100:
            assert response.data["msg"] == "first and last name are too long. please provider a shorter name."
        else:
            assert response.data["msg"] == missing_data_msg
        assert len(mail.outbox) == current_mailbox_count

    @pytest.mark.parametrize("should_fail", [True, False])
    def test_activation(self, should_fail, mocker: MockerFixture, test_user, api_factory):
        # Assert
        test_uuid = "test_uuid"
        test_token = "wrong_token" if should_fail else test_user.generate_temporary_token()
        mocker.patch.object(test_user, "is_active", False)
        mocker.patch.object(test_user, "is_register", False)
        mocker.patch("wbcore.contrib.authentication.viewsets.users.get_object_or_404", return_value=test_user)
        test_user.save = mocker.MagicMock()
        url = reverse("wbcore:authentication:activate", args=[test_uuid, test_token])

        # Act
        request = api_factory.get(url)
        response = activate_user(request, test_uuid, test_token)

        # Assert
        if should_fail:
            assert response.status_code == 400
            assert test_user.is_active is False
            assert test_user.is_register is False
        else:
            assert response.status_code == 200
            assert test_user.is_active is True
            assert test_user.is_register is True
            test_user.save.assert_called_once()
