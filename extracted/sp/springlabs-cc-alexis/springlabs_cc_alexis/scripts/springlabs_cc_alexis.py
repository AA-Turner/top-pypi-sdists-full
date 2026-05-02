import click
import time
from springlabs_cc_alexis.prints import pythonprints
from springlabs_cc_alexis import __version__ as version


@click.group(invoke_without_command=False)
@click.version_option(version=version, prog_name="Springlabs Prints", message="%(prog)s, v%(version)s")
@click.pass_context
def cli(ctx, *args, **kwargs):
	"""Programa para respaldar"""
	ctx.invoked_subcommand

@cli.command()
@click.option("-pl","--proglang","programinglanguage", help="Busqueda de archivos (.py,.js)", default="Python", show_default=True, prompt="¿Cuál es el lenguaje que usas?", type= click.Choice(["Python", "JavaScript"], case_sensitive=True))
@click.option("-fp","--findprint", help="Busqueda de prints en archivo")
@click.option("-p","--dpath", help="Direccion de los archivos a escanear", prompt="¿Cuál es tu path?")
def find_print(programinglanguage,findprint,dpath):

	click.secho("ANALIZANDO", fg="green")
	p = pythonprints(dpath)

	if p == True:
		click.secho("TERMINADO CON EXITO", fg="green")
	else:
		click.secho("*************************************", fg="red")
		click.secho("*                                   *", fg="red")
		click.secho("*  ERROR: No existe el directorio   *", fg="red")
		click.secho("*                                   *", fg="red")
		click.secho("*************************************", fg="red")


if __name__ == '__main__':
	cli()
