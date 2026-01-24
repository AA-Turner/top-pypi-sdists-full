import click
import json
import sys
from requests.exceptions import RequestException

from anc.cli.util import click_group
from anc.api.connection import Connection
from anc.conf.remote import remote_server
from .operators.dataset_operator import DatasetOperator


@click_group()
def ds():
    pass


@ds.command()
@click.argument(
    "source_path",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True
    )
)
@click.option("--version", "-v", type=str, help="Dataset version you want to register", required=True)
@click.option("--message", "-m", type=str, help="Note of the dataset")
@click.pass_context
def add(ctx, source_path, version, message):
    """command like: anc ds add abc.txt -v 0.1"""
    op = DatasetOperator()
    op.remote_add(version, source_path, message)

@ds.command()
@click.option("--name", "-n", help="Name of the datasets in remote",)
@click.option("--verbose", "-v", is_flag=True, default=False, help="verbose of data set information")
def list(name, verbose):
    """command like: anc ds list"""
    op = DatasetOperator()
    op.list_dataset(name, verbose)


@ds.command()
#@click.option("--name", "-n", help="Name of the datasets in remote", required=True)
@click.argument(
    "name"
)
@click.option("--version", "-v", help="Version of the dataset")
@click.option("--dest", "-d", help="Destination path you want to creat the dataset",default=".", show_default=True)
@click.option("--cache_policy", "-c", help="If input is `no` which means no cache used, the dataset will be a completely copy")
@click.pass_context
def get(ctx, name, version, dest, cache_policy):
    """command like: anc ds get abc.txt -v 0.1"""
    op = DatasetOperator()
    op.download_dataset(name, version, dest, cache_policy)


@ds.group()
def queue():
    """Commands for operation task queue"""
    pass

@queue.command()
def status():
    """command like: anc ds queue status"""
    try:
        conn = Connection(url=remote_server)
        response = conn.get("/queue_status")

        if 200 <= response.status_code < 300:
            status_data = response.json()
            print("Queue Status:")
            print(json.dumps(status_data, indent=2))
        else:
            #print(f"Error: Server responded with status code {response.status_code}")
            print(f"Sorry, {response.text}")
    except RequestException as e:
        print(f"Sorry, you can't get queue info out of clusters, please use it in a notebook")
    except json.JSONDecodeError:
        print("Sorry: received invalid JSON response from server")
    except KeyboardInterrupt:
        print(f"Operation interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"Sorry, your command run failed, you can try again or reach out infra team")

@ds.group()
def task():
    """Commands for task operations"""
    pass

@task.command()
@click.argument("task_id", type=int, required=True)
def status(task_id):
    """command like: anc ds task status 201"""
    try:
        conn = Connection(url=remote_server)
        response = conn.get(f"/task_status/{task_id}")

        if 200 <= response.status_code < 300:
            status_data = response.json()
            print(f"Task Status for ID {status_data['task_id']}")
            print(json.dumps(status_data, indent=2))
        else:
            print(f"Error: Server responded with status code {response.status_code}")
            print(f"Sorry, {response.text}")
    except RequestException as e:
        print(f"Sorry, you can't run this command out of clusters, please use it in a notebook")
    except json.JSONDecodeError:
        print("Sorry: received invalid JSON response from server")
    except KeyboardInterrupt:
        print(f"Operation interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"Sorry, your command run failed, you can try again or reach out infra team")


@task.command()
@click.argument("task_id", type=int)
@click.option("--priority", "-p", type=int, required=True, help="New priority value for the task")
def boost(task_id, priority):
    """Set a new priority for a task"""
    try:
        conn = Connection(url=remote_server)
        data = {"new_priority": priority}
        response = conn.post(f"/task/{task_id}/increase_priority", json=data)

        if response.status_code == 200:
            result = response.json()
            print(result["message"])
        elif response.status_code == 400:
            error = response.json()
            print(f"Sorry: {error['error']}, maybe your task is not in pending state")
        elif response.status_code == 404:
            error = response.json()
            print(f"Sorry: {error['error']}, maybe your task is not in pending state")
        else:
            print(f"Sorry: Server responded with status code {response.status_code}")
            print(f"Response: {response.text}")
    except RequestException as e:
        print(f"Sorry, you can't get queue info out of clusters, please use it in a notebook")
    except json.JSONDecodeError:
        print("Sorry: received invalid JSON response from server")
    except KeyboardInterrupt:
        print(f"Operation interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"Sorry, your command run failed, you can try again or reach out infra team")


def add_command(cli_group):
    cli_group.add_command(ds)
