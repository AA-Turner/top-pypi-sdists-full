import pytest

from cnvrgv2.errors import CnvrgError


class TestProjectSettings:
    def test_get_settings_success(self, e2e_project):
        assert e2e_project.settings

    def test_save_settings_success(self, e2e_project):
        command = "git command"
        e2e_project.settings.command_to_execute = command
        e2e_project.settings.save()

        assert e2e_project.settings.command_to_execute == command

        e2e_project.settings.command_to_execute = "git command --other"
        e2e_project.settings.save()

        assert e2e_project.settings.command_to_execute != command

    def test_save_settings_default_image_success(self, e2e_project):
        default_image = "cnvrg_spark:v2.4.4-3.2"
        e2e_project.settings.default_image = default_image
        e2e_project.settings.save()
        assert e2e_project.settings.default_image == default_image

    def test_update_settings_success(self, e2e_project):
        default_computes = ["small", "large"]
        check_stuckiness = True
        stuck_time = 99

        e2e_project.settings.update(
            default_computes=default_computes,
            check_stuckiness=check_stuckiness,
            stuck_time=stuck_time
        )

        assert e2e_project.settings.default_computes == default_computes
        assert e2e_project.settings.check_stuckiness == check_stuckiness
        assert e2e_project.settings.stuck_time == stuck_time

    def test_update_non_existing_attribute_fail(self, e2e_project):
        with pytest.raises(CnvrgError):
            e2e_project.settings.update(fake="setting")
