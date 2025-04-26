import os
from unittest import TestCase
from unittest.mock import patch

from airflow_mcd.operators.dbt import DbtConfig, DefaultConfigProvider


class TestConfigProvider(DefaultConfigProvider):

    def config(self) -> DbtConfig:
        return DbtConfig(dbt_bin="/usr/bin/dbt")


class InvalidConfigProvider:

    @staticmethod
    def config() -> DbtConfig:
        return DbtConfig(dbt_bin="/usr/bin/dbt")


class DefaultConfigProviderTests(TestCase):

    def test_default_config(self):
        # when
        config = DefaultConfigProvider.get()

        # then
        self.assertEqual("dbt", config.dbt_bin)

    @patch.dict(
        os.environ,
        {
            DefaultConfigProvider.ENV_VAR_NAME: "tests.operators.test_dbt_default_config_provider.TestConfigProvider"
        },
        clear=True
    )
    def test_custom_config(self):
        # when
        config = DefaultConfigProvider.get()

        # then
        self.assertEqual("/usr/bin/dbt", config.dbt_bin)

    @patch.dict(
        os.environ,
        {
            f"AIRFLOW__MC__{DefaultConfigProvider.ENV_VAR_NAME}": "tests.operators.test_dbt_default_config_provider.TestConfigProvider"
        },
        clear=True
    )
    def test_custom_config_mwaa(self):
        # when
        config = DefaultConfigProvider.get()

        # then
        self.assertEqual("/usr/bin/dbt", config.dbt_bin)


    @patch.dict(
        os.environ,
        {
            DefaultConfigProvider.ENV_VAR_NAME: "tests.operators.test_dbt_default_config_provider.InvalidConfigProvider"
        },
        clear=True
    )
    def test_invalid_config(self):
        # when
        with self.assertRaises(Exception) as context:
            DefaultConfigProvider.get()

        # then
        self.assertEqual(
            "dbt configuration provider defined in AIRFLOW_MCD_DBT_CONFIG_PROVIDER is not an instance of DefaultConfigProvider",
            str(context.exception)
        )
