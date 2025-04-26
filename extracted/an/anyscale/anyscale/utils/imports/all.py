import click


def try_import_ray():
    try:
        import ray

        return ray
    except ImportError:
        raise click.ClickException(
            "Ray not installed locally on this machine but required "
            "for the command. Please install with `pip install 'anyscale[all]'`."
        )
