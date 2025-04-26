from unittest import TestCase

from airflow_mcd.operators.dbt import DbtConfig


class DbtCliConfigTests(TestCase):
    def test_build_command_with_default_config(self):
        # given
        config = DbtConfig()

        # when
        command = config.build_command("run")

        # then
        self.assertEqual([
            "dbt",
            "run",
        ], command)

    def test_build_command_with_non_default_config(self):
        # given
        config = DbtConfig(
            dbt_bin="/usr/bin/dbt",
            profiles_dir="/usr/local/dbt/.profiles",
            target_path="/tmp/dbt/target",
            target="prod",
            vars={"foo": "bar"},
            models="model",
            exclude="excluded_model",
            select="selected_model",
            warn_error=True,
            full_refresh=True,
            data=True,
            schema=True,
        )

        # when
        command = config.build_command("docs generate")

        # then
        self.assertEqual([
            "/usr/bin/dbt",
            "--warn-error",
            "docs",
            "generate",
            "--profiles-dir",
            "/usr/local/dbt/.profiles",
            "--target",
            "prod",
            "--vars",
            "{\"foo\": \"bar\"}",
            "--models",
            "model",
            "--exclude",
            "excluded_model",
            "--select",
            "selected_model",
            "--full-refresh",
            "--data",
            "--schema",
        ], command)
