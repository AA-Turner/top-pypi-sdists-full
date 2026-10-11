"""Unit tests for the hand-written MFA helpers in agilicus/challenges.py.

``user_id`` is writable in the generated TOTPEnrollmentSpec and
TOTPEnrollmentAnswer models (agilicus-api ae573ff4), so the hand-written
helpers use the plain generated constructors. These tests pin their
serialization and the raw ``api_client.call_api`` path used for the newer
org reconcile endpoint.
"""

from unittest.mock import MagicMock, patch

from agilicus import challenges


def test_create_challenge_enrollment_serialises_user_id():
    ctx = MagicMock()
    apiclient = MagicMock()
    with patch.object(challenges.context, "get_token", return_value="tok"), patch.object(
        challenges.context, "get_apiclient", return_value=apiclient
    ):
        challenges.create_challenge_enrollment(ctx, "user-1", nickname="phone")

    model = apiclient.challenges_api.create_totp_enrollment.call_args.args[0]
    assert model.spec.user_id == "user-1"
    assert model.spec.nickname == "phone"
    assert model.to_dict()["spec"]["user_id"] == "user-1"


def test_update_challenge_enrollment_serialises_user_id():
    ctx = MagicMock()
    apiclient = MagicMock()
    with patch.object(challenges.context, "get_token", return_value="tok"), patch.object(
        challenges.context, "get_apiclient", return_value=apiclient
    ):
        challenges.update_challenge_enrollment(ctx, "enr-1", "user-1", "123456")

    args = apiclient.challenges_api.update_totp_enrollment.call_args.args
    assert args[0] == "enr-1"
    model = args[1]
    assert model.user_id == "user-1"
    assert model.answer == "123456"
    assert model.to_dict()["user_id"] == "user-1"


def test_reconcile_org_mfa_origins_posts_raw_api_body():
    ctx = MagicMock()
    apiclient = MagicMock()
    with patch.object(
        challenges.context, "get_apiclient_from_ctx", return_value=apiclient
    ):
        challenges.reconcile_org_mfa_origins(
            ctx,
            "org-1",
            new_origin="new.example",
            old_origin="old.example",
            dry_run=True,
        )

    call = apiclient.org_api.api_client.call_api
    args, kwargs = call.call_args
    assert args[0] == "/v1/orgs/{org_id}/reconcile_mfa_origins"
    assert args[1] == "POST"
    assert kwargs["path_params"] == {"org_id": "org-1"}
    assert kwargs["body"] == {
        "dry_run": True,
        "new_origin": "new.example",
        "old_origin": "old.example",
    }
    assert kwargs["auth_settings"] == ["token-valid"]
    assert kwargs["_return_http_data_only"] is True


def test_reconcile_org_mfa_origins_omits_unset_origins():
    ctx = MagicMock()
    apiclient = MagicMock()
    with patch.object(
        challenges.context, "get_apiclient_from_ctx", return_value=apiclient
    ):
        challenges.reconcile_org_mfa_origins(ctx, "org-1")

    assert apiclient.org_api.api_client.call_api.call_args.kwargs["body"] == {
        "dry_run": False
    }


def test_report_org_webauthn_enrollments_dry_run_joins_and_filters():
    ctx = MagicMock()
    report = {
        "org_id": "org-1",
        "origin": "new.example",
        "dry_run": True,
        "webauthn_affected": [
            {
                "user_id": "u1",
                "challenge_method_id": "cm1",
                "endpoint": "e1",
                "origin": "old.example",
            },
            {
                "user_id": "u2",
                "challenge_method_id": "cm2",
                "endpoint": "e2",
                "origin": "old.example",
            },
        ],
    }
    enrollment = MagicMock()
    enrollment.metadata.id = "e1"
    enrollment.to_dict.return_value = {"id": "e1", "created": "2026-01-01"}
    with patch.object(
        challenges, "reconcile_org_mfa_origins", return_value=report
    ) as reconcile, patch.object(
        challenges, "list_webauthn_enrollments", return_value=[enrollment]
    ):
        result = challenges.report_org_webauthn_enrollments(ctx, "org-1", user_id="u1")

    # The report is read-only: it must never call the reconciler for real.
    assert reconcile.call_args.kwargs["dry_run"] is True
    assert result["webauthn_affected_count"] == 1
    assert result["users_affected_count"] == 1
    entry = result["webauthn_affected"][0]
    assert entry["user_id"] == "u1"
    assert entry["enrollment"] == {"id": "e1", "created": "2026-01-01"}


def test_list_mfa_challenge_methods_json_output():
    from agilicus import main as main_module

    method = MagicMock()
    method.to_dict.return_value = {"metadata": {"id": "cm1"}}
    ctx = MagicMock()
    ctx.obj = {"output_format": "json"}
    with patch.object(
        main_module.users, "list_mfa_challenge_methods", return_value=[method]
    ), patch.object(main_module, "output_json") as output_json:
        # __wrapped__ skips click's pass_context shim so the raw function runs.
        main_module.list_mfa_challenge_methods.callback.__wrapped__(ctx, "user-1")

    output_json.assert_called_once_with(ctx, [{"metadata": {"id": "cm1"}}])


def test_add_totp_prints_key_and_prompts_for_the_answer(capsys):
    from agilicus import main as main_module

    enrollment = MagicMock()
    enrollment.metadata.id = "enr-1"
    enrollment.status.key = "otpauth://totp/agilicus:user?secret=ABC"
    method = MagicMock()
    method.to_dict.return_value = {"metadata": {"id": "cm1"}}
    ctx = MagicMock()
    ctx.obj = {"output_format": "console"}
    with patch.object(
        main_module.challenges,
        "create_challenge_enrollment",
        return_value=enrollment,
    ), patch.object(
        main_module.challenges, "update_challenge_enrollment"
    ) as update, patch.object(
        main_module.users, "add_mfa_challenge_method", return_value=method
    ), patch.object(
        main_module, "output_entry"
    ), patch.object(
        main_module.click, "prompt", return_value="123456"
    ) as prompt:
        # __wrapped__ skips click's pass_context shim so the raw function runs.
        main_module.add_totp.callback.__wrapped__(ctx, "user-1", None)

    assert "otpauth://totp/agilicus:user?secret=ABC" in capsys.readouterr().err
    prompt.assert_called_once()
    assert update.call_args.args[1:] == ("enr-1", "user-1", "123456")


def test_add_totp_with_answer_does_not_prompt():
    from agilicus import main as main_module

    enrollment = MagicMock()
    enrollment.metadata.id = "enr-1"
    enrollment.status.key = "otpauth://totp/x"
    ctx = MagicMock()
    ctx.obj = {"output_format": "json"}
    with patch.object(
        main_module.challenges,
        "create_challenge_enrollment",
        return_value=enrollment,
    ), patch.object(
        main_module.challenges, "update_challenge_enrollment"
    ) as update, patch.object(
        main_module.users, "add_mfa_challenge_method", return_value={}
    ), patch.object(
        main_module, "output_entry"
    ), patch.object(
        main_module.click, "prompt"
    ) as prompt:
        main_module.add_totp.callback.__wrapped__(ctx, "user-1", "123456")

    prompt.assert_not_called()
    assert update.call_args.args[1:] == ("enr-1", "user-1", "123456")
