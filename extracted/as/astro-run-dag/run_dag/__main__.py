import logging
import warnings
from datetime import datetime

import typer
from airflow.models.dagbag import DagBag
from airflow.utils.cli import process_subdir
from dotenv import load_dotenv
from rich import print as rprint
from typer import Exit

from run_dag.utils.exceptions import ConnectionFailed
from run_dag.utils.get_dag import get_dag
from run_dag.utils.parse_settings_file import parse_settings_file
from run_dag.utils.run_dag import run_dag
from run_dag.utils.version_compat import AIRFLOW_V_3_0_PLUS

warnings.filterwarnings(action="ignore")
load_dotenv()
app = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]})


airflow_logger = logging.getLogger("airflow")
airflow_logger.setLevel(logging.CRITICAL)
airflow_logger.propagate = False


@app.command(
    help="""
    Run a DAG locally. This task assumes that there is a local airflow DB (can be a SQLite file), that has been
    initialized with Airflow tables.
    """
)
def run_airflow_dag(
    dag_file: str = typer.Argument(
        default=...,
        show_default=False,
        help="path to DAG file or directory",
    ),
    dag_id: str = typer.Argument(
        default=...,
        show_default=False,
        help="file where the dag is",
    ),
    settings_file_path: str = typer.Argument(
        default=None,
        show_default=False,
        help="path to a file containing astro config settings",
    ),
    connections_file_path: str = typer.Argument(
        default=None,
        show_default=False,
        help="path to a file containing a list of connection objects",
    ),
    variables_file_path: str = typer.Argument(
        default=None,
        show_default=False,
        help="path to a file containing a list of variable objects",
    ),
    execution_date: datetime = typer.Option(
        default=None,
        show_default=False,
        help="execution date for the dagrun. Defaults to now",
    ),
    verbose: bool = typer.Option(
        default=False,
        help="print out the logs of the dag run",
    ),
) -> None:
    import_errors = DagBag(process_subdir(str(dag_file))).import_errors
    if import_errors:
        all_errors = "\n\n".join(list(import_errors.values()))
        rprint(f"[bold red]DAG failed to render[/bold red]\n errors found:\n\n {all_errors}")
        raise Exit(code=1)
    dag = get_dag(dag_id=dag_id, subdir=dag_file, include_examples=False)
    connections, variables = None, None
    if settings_file_path:
        connections, variables = parse_settings_file(settings_file_path)
    try:
        if AIRFLOW_V_3_0_PLUS:
            dr = dag.test(
                logical_date=execution_date,
                variable_file_path=variables_file_path,
                conn_file_path=connections_file_path,
            )
        else:
            dr = run_dag(
                dag,
                execution_date=execution_date,
                conn_file_path=connections_file_path,
                variable_file_path=variables_file_path,
                connections=connections,
                variables=variables,
                verbose=verbose,
            )
    except ConnectionFailed as connection_failed:
        rprint(
            f"  [bold red]{connection_failed}[/bold red] using connection [bold]{connection_failed.conn_id}[/bold]"
        )
        raise Exit(code=1)
    except Exception as exception:
        rprint(f"  [bold red]{exception}[/bold red]")
        raise Exit(code=1)
    rprint(f"Completed running the DAG {dr.dag_id}. 🚀")
    elapsed_seconds = (dr.end_date - dr.start_date).microseconds / 10**6
    rprint(f"Total elapsed time: [bold blue]{elapsed_seconds:.2}s[/bold blue]")


if __name__ == "__main__":  # pragma: no cover
    app()
