from click.testing import CliRunner


def test_cli_encrypt(keyed_data, keyless_data):
    from sprig_aes.cli import encrypt

    for data in [keyed_data, keyless_data]:
        runner = CliRunner()
        result = runner.invoke(encrypt, [data.text, "--key", data.key])

        assert result.exit_code == 0
        assert result.output.strip() == data.encrypted_text


def test_cli_encrypt_with_key_file(keyed_data, keyless_data):
    from sprig_aes.cli import encrypt

    for data in [keyed_data, keyless_data]:
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("key.txt", "w") as f:
                f.write(data.key)

            result = runner.invoke(
                encrypt,
                [data.text, "--key-file", "key.txt"],
            )
            assert result.exit_code == 0
            assert result.output.strip() == data.encrypted_text


def test_cli_decrypt(keyed_data, keyless_data):
    from sprig_aes.cli import decrypt

    for data in [keyed_data, keyless_data]:
        runner = CliRunner()
        result = runner.invoke(decrypt, [data.encrypted_text, "--key", data.key])
        assert result.exit_code == 0
        assert result.output.strip() == data.text


def test_cli_decrypt_with_key_file(keyed_data, keyless_data):
    from sprig_aes.cli import decrypt

    for data in [keyed_data, keyless_data]:
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("key.txt", "w") as f:
                f.write(data.key)

            result = runner.invoke(decrypt, [data.encrypted_text, "--key-file", "key.txt"])
            assert result.exit_code == 0
            assert result.output.strip() == data.text


def test_cli_encrypt_file(json_keyed_data, json_keyless_data):
    from sprig_aes.cli import encrypt_file

    for data in [json_keyed_data, json_keyless_data]:
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("simple.json", "w") as f:
                f.write(data.text)

            result = runner.invoke(encrypt_file, ["simple.json", "--key", data.key])

            assert result.exit_code == 0
            assert result.output.strip() == data.encrypted_text


def test_cli_encrypt_file_with_key_file(json_keyed_data, json_keyless_data):
    from sprig_aes.cli import encrypt_file

    for data in [json_keyed_data, json_keyless_data]:
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("simple.json", "w") as f:
                f.write(data.text)

            with open("key.txt", "w") as f:
                f.write(data.key)

            result = runner.invoke(
                encrypt_file,
                ["simple.json", "--key-file", "key.txt"],
            )
            assert result.exit_code == 0
            assert result.output.strip() == data.encrypted_text


def test_cli_decrypt_file(json_keyed_data, json_keyless_data):
    from sprig_aes.cli import decrypt_file

    for data in [json_keyed_data, json_keyless_data]:
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("simple.enc", "w") as f:
                f.write(data.encrypted_text)

            result = runner.invoke(decrypt_file, ["simple.enc", "--key", data.key])
            assert result.exit_code == 0
            assert result.output.strip() == data.text


def test_cli_decrypt_file_with_key_file(json_keyed_data, json_keyless_data):
    from sprig_aes.cli import decrypt_file

    for data in [json_keyed_data, json_keyless_data]:
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("simple.enc", "w") as f:
                f.write(data.encrypted_text)

            with open("key.txt", "w") as f:
                f.write(data.key)

            result = runner.invoke(decrypt_file, ["simple.enc", "--key-file", "key.txt"])
            assert result.exit_code == 0
            assert result.output.strip() == data.text
