import click

from sprig_aes.core import sprig_encrypt_aes
from sprig_aes.core import sprig_decrypt_aes
from sprig_aes.version import __version__


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]}
)
@click.version_option(__version__, "-v", "--version")
def cli() -> None:  # pragma: no cover
    pass


@cli.command(help="Encrypt plain text using AES CBC mode.")
@click.argument("text")
@click.option("--key", help="Key string.", default="")
@click.option(
    "--key-file",
    type=click.Path(True, resolve_path=True, allow_dash=True),
    help="Read key from file (overrides --key).",
)
def encrypt(text: str, key: str, key_file: str) -> None:
    if key_file:
        with click.open_file(key_file, "r") as f:
            key = f.read().strip()

    enc_text = sprig_encrypt_aes(text, key)
    click.echo(enc_text.decode())


@cli.command(help="Decrypt encrypted text using AES CBC mode.")
@click.argument("text")
@click.option("--key", help="Key string.", default="")
@click.option(
    "--key-file",
    type=click.Path(True, resolve_path=True, allow_dash=True),
    help="Read key from file (overrides --key).",
)
def decrypt(text: str, key: str, key_file: str) -> None:
    if key_file:
        with click.open_file(key_file, "r") as f:
            key = f.read().strip()

    dec_text = sprig_decrypt_aes(text, key)
    click.echo(dec_text.decode())


@cli.command(help="Encrypt contents of a file using AES CBC mode.")
@click.argument("path", type=click.Path(True, resolve_path=True, allow_dash=True))
@click.option("--key", help="Key string.", default="")
@click.option(
    "--key-file",
    type=click.Path(True, resolve_path=True, allow_dash=True),
    help="Read key from file (overrides --key).",
)
def encrypt_file(path: str, key: str, key_file: str) -> None:
    if key_file:
        with click.open_file(key_file, "r") as f:
            key = f.read().strip()

    with click.open_file(path, "r") as f:
        enc_text = sprig_encrypt_aes(f.read(), key)
        click.echo(enc_text.decode())


@cli.command(help="Decrypt contents of a file using AES CBC mode.")
@click.argument("path", type=click.Path(True, resolve_path=True, allow_dash=True))
@click.option("--key", help="Key string.", default="")
@click.option(
    "--key-file",
    type=click.Path(True, resolve_path=True, allow_dash=True),
    help="Read key from file (overrides --key).",
)
def decrypt_file(path: str, key: str, key_file: str) -> None:
    if key_file:
        with click.open_file(key_file, "r") as f:
            key = f.read().strip()

    with click.open_file(path, "r") as f:
        dec_text = sprig_decrypt_aes(f.read(), key)
        click.echo(dec_text.decode())
