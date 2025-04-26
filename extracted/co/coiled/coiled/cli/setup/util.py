import coiled

SUCCESS_MESSAGE = """
[bold]Setup complete 🎉[/bold]

What's next?

  Run a command line application in the cloud with:

    $ [bold]coiled run echo 'Hello, world'[/bold]

  Or create a Dask cluster with:

    $ ipython

    [bold]import coiled
    cluster = coiled.Cluster(
        n_workers=10,
    )
    client = cluster.get_client()[/bold]

  For more examples see [link]https://docs.coiled.io/user_guide/examples/index.html[/link]
""".strip()


def setup_failure(reason: str, backend: str):
    coiled.add_interaction("setup-failure", error_message=reason, success=False, backend=backend)
