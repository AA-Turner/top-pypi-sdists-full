import typer


def print_error(message: str, log_file_path: str) -> None:
    typer.secho(f"Error: {message}", fg=typer.colors.RED, err=True)
    typer.secho(
        f"See logs for details: {log_file_path}", fg=typer.colors.YELLOW, err=True
    )
