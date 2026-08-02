import named
import typer


def main(func, app=typer.Typer(add_completion=False)):
    if named.get_module(func) == '__main__':
        app.command()(func)
        app()
    return func
