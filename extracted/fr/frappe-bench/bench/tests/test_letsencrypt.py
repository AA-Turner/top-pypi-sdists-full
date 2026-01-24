import sys
import os
import unittest
from unittest.mock import MagicMock, patch, mock_open

git_mock = MagicMock()
sys.modules["git"] = git_mock

semver_mock = MagicMock()
sys.modules["semantic_version"] = semver_mock
sys.modules["semantic_version.Version"] = MagicMock()

sys.modules["jinja2"] = MagicMock()
sys.modules["requests"] = MagicMock()

sys.path.insert(0, os.getcwd())

from bench.config import lets_encrypt


class TestLetsEncryptConfig(unittest.TestCase):
	@patch("bench.config.lets_encrypt.create_dir_if_missing")
	@patch("bench.config.env")
	@patch("builtins.open", new_callable=mock_open)
	def test_create_config_with_server(self, mock_file, mock_env, mock_create_dir):
		mock_template = MagicMock()
		mock_env.return_value.get_template.return_value = mock_template

		def render_side_effect(domain, server=None):
			content = f"domain = {domain}\n"
			if server:
				content += f"server = {server}\n"
			return content

		mock_template.render.side_effect = render_side_effect

		lets_encrypt.create_config(
			"site1.local",
			None,
			"https://acme-staging-v02.api.letsencrypt.org/directory",
		)

		mock_template.render.assert_called_with(
			domain="site1.local",
			server="https://acme-staging-v02.api.letsencrypt.org/directory",
		)

		handle = mock_file()
		written = handle.write.call_args[0][0]
		self.assertIn(
			"server = https://acme-staging-v02.api.letsencrypt.org/directory",
			written,
		)

	@patch("bench.config.lets_encrypt.create_dir_if_missing")
	@patch("bench.config.env")
	@patch("builtins.open", new_callable=mock_open)
	def test_create_config_without_server(self, mock_file, mock_env, mock_create_dir):
		mock_template = MagicMock()
		mock_env.return_value.get_template.return_value = mock_template

		def render_side_effect(domain, server=None):
			content = f"domain = {domain}\n"
			if server:
				content += f"server = {server}\n"
			return content

		mock_template.render.side_effect = render_side_effect

		lets_encrypt.create_config("site1.local", None, None)

		mock_template.render.assert_called_with(
			domain="site1.local",
			server=None,
		)

		handle = mock_file()
		written = handle.write.call_args[0][0]
		self.assertNotIn("server =", written)

	@patch("bench.config.lets_encrypt.service")
	@patch("bench.config.lets_encrypt.make_nginx_conf")
	@patch("bench.config.lets_encrypt.setup_crontab")
	@patch("bench.config.lets_encrypt.update_common_site_config")
	@patch("bench.config.lets_encrypt.get_certbot_path")
	@patch("bench.config.lets_encrypt.exec_cmd")
	@patch("bench.config.lets_encrypt.Bench")
	def test_setup_wildcard_ssl_with_server(
		self,
		mock_bench,
		mock_exec,
		mock_get_certbot_path,
		mock_update_common_site_config,
		mock_setup_crontab,
		mock_make_nginx_conf,
		mock_service,
	):
		# Mock Bench config for dns_multitenant
		mock_bench.return_value.conf.get.return_value = True
		mock_get_certbot_path.return_value = "/usr/bin/certbot"

		lets_encrypt.setup_wildcard_ssl(
			"example.com",
			"test@example.com",
			".",
			exclude_base_domain=False,
			custom_server="https://acme-staging",
		)

		expected_cmd = (
			"/usr/bin/certbot certonly --manual --preferred-challenges=dns "
			"--email test@example.com --server https://acme-staging "
			"--agree-tos -d example.com -d *.example.com"
		)
		mock_exec.assert_called_with(expected_cmd)

	@patch("bench.config.lets_encrypt.service")
	@patch("bench.config.lets_encrypt.make_nginx_conf")
	@patch("bench.config.lets_encrypt.setup_crontab")
	@patch("bench.config.lets_encrypt.update_common_site_config")
	@patch("bench.config.lets_encrypt.get_certbot_path")
	@patch("bench.config.lets_encrypt.exec_cmd")
	@patch("bench.config.lets_encrypt.Bench")
	def test_setup_wildcard_ssl_default(
		self,
		mock_bench,
		mock_exec,
		mock_get_certbot_path,
		mock_update_common_site_config,
		mock_setup_crontab,
		mock_make_nginx_conf,
		mock_service,
	):
		# Mock Bench config for dns_multitenant
		mock_bench.return_value.conf.get.return_value = True
		mock_get_certbot_path.return_value = "/usr/bin/certbot"

		lets_encrypt.setup_wildcard_ssl(
			"example.com", "test@example.com", ".", exclude_base_domain=False, custom_server=None
		)

		expected_cmd = (
			"/usr/bin/certbot certonly --manual --preferred-challenges=dns "
			"--email test@example.com  "
			"--agree-tos -d example.com -d *.example.com"
		)
		mock_exec.assert_called_with(expected_cmd)


if __name__ == "__main__":
	unittest.main()
