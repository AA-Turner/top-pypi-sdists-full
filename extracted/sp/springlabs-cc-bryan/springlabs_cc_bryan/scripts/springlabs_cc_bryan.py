import click
import time
import glob
from springlabs_cc_bryan import __version__ as version

def validate_search(ctx, param, value):
    if ctx.params['search'] == "si":
        return value
    else:
        if ctx.params['name'].endswith('.js'):
            return value
        else:
            raise click.BadParameter(f"Ingresa un nombre de archivo valido, terminacion '.js'")

@click.command()
@click.version_option(version=version, prog_name="mi programa", message="0.1.1")
@click.option("-s","--search", help="Buscar los console.log de todos los archivos", prompt = "¿Deseas buscar en todos los archivo?", type= click.Choice(["si", "no"], case_sensitive=False))
#@click.option("-n","--name", help="Nombre de todos los archivos", prompt = "Ingresa el nombre del archivo")
def cli(search):
    """ Buscar los console.log de todos los archivos """
    # if name:
    #     with open(name, "r") as file:
    #         search = "console.log"
    #         string = file.read()
    #         found_count = string.count(search)
    #         click.secho(name + " : " + str(found_count), fg="green")
       
    array = []
    for filename in glob.glob('*.js'):
        search = "console.log"
        with open(filename, "r") as file:
            string = file.read()
            found_count = string.count(search)
            dict_count = {
                "file" : filename,
                "count" : found_count
            }
            array.append(dict_count)

    for data in array:
        click.secho(data['file'] + " : " + str(data['count']), fg="green")        
    
if __name__ == '__main__':
    cli()