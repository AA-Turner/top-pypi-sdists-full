import typer
from openapi_downgrade.converter.loader import load_spec
from openapi_downgrade.converter.transformer import convert_spec
import json

app = typer.Typer()

@app.command()
def convert(input: str, output: str):
    """
    Convert an OpenAPI 3.1.x spec to 3.0.x.
    Supports file paths or URLs.
    To convert a file, use:
    openapi_downgrade <input file path or openapi spec url> <output file name>
    """
    try:
        spec = load_spec(input)
        converted = convert_spec(spec)

        with open(output, "w") as f:
            json.dump(converted, f, indent=2)

        try:
            typer.echo(f"\U00002705 Converted and saved to: {output}")
        except UnicodeEncodeError:
            typer.echo(f"Converted and saved to: {output}")
    except Exception as e:
        try:
            typer.echo(f"\u274C Error: {e}")
        except UnicodeEncodeError:
            typer.echo(f"Error: {e}")

if __name__ == "__main__":
    app()
