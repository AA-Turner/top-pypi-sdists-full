import json
import os

import click

from app.src.application.services.auth_service import AuthService
from app.src.application.services.task_service import TaskService
from app.src.presentation.cli import cli
from app.src.presentation.utils import TokenManager, async_command, require_auth

API_URL = os.getenv("API_URL", "http://localhost:8000")


@cli.group()
def task():
    """Task management commands"""
    pass


@task.command()
@click.option("--page", default=1, help="Number of pages")
@click.option(
    "--per_page", default=20, help="Maximum number of tasks to return per page"
)
@require_auth
@async_command
async def list(page, per_page):
    """List tasks"""
    token = TokenManager.get_token()
    auth_service = AuthService(api_url=API_URL)
    auth_service.set_token(token)
    task_repo = await auth_service.get_task_repository()
    task_service = TaskService(task_repo)
    try:
        tasks = await task_service.get_tasks(page=page, per_page=per_page)
    except ValueError as e:
        click.echo(f"Error:{str(e)}")
        return

    click.echo(f"Found {len(tasks)} tasks")
    for task in tasks:
        task_id = task.get("task_id")
        status_val = task.get("status")
        question = task.get("question", "")[:60]
        assignee_val = task.get("assigned_to", "Unassigned")
        created_by = task.get("created_by")
        click.echo(f"ID: #{task_id}")
        click.echo(f"  Status: {status_val}")
        click.echo(f"  Question: {question}")
        click.echo(f"  Assignee: {assignee_val}")
        click.echo(f"  Created by: {created_by}")
        if "bid" in task:
            click.echo(f"  Bid: {task['bid']}")
        click.echo()


@task.command()
@click.argument("task_id", type=int)
@require_auth
@async_command
async def get(task_id):
    """Get task details"""
    token = TokenManager.get_token()
    auth_service = AuthService(api_url=API_URL)
    auth_service.set_token(token)
    task_repo = await auth_service.get_task_repository()
    task_service = TaskService(task_repo)
    try:
        result = await task_service.get_task(task_id)
        click.echo(json.dumps(result, indent=2, default=str))
    except Exception as e:
        click.echo(f"Failed to get task: {str(e)}")


@task.command()
@click.option("--question", required=True, help="Task question")
@click.option("--bid", type=int, required=True, help="Bid amount")
@click.option("--assign-to", type=int, help="Assign to user ID")
@click.option("--schema", type=int, help="Schema ID")
@click.option("--crop", type=int, help="Crop ID")
@require_auth
@async_command
async def create(question, bid, assign_to, schema, crop):
    """Create a new task"""
    token = TokenManager.get_token()
    auth_service = AuthService(api_url=API_URL)
    auth_service.set_token(token)
    task_repo = await auth_service.get_task_repository()
    task_service = TaskService(task_repo)

    task_data = {"question": question, "bid": bid}
    if assign_to:
        task_data["assigned_to"] = assign_to
        task_data["assign_task"] = True
    if schema:
        task_data["schema_id"] = schema
    if crop:
        task_data["crop_id"] = crop

    try:
        result = await task_service.create_task(task_data)
        click.echo("Task created")
        click.echo(json.dumps(result, indent=2, default=str))
    except Exception as e:
        click.echo(f"Failed to create task: {str(e)}")


@task.command()
@click.argument("task_id", type=int)
@click.argument("fields", nargs=-1)
@require_auth
@async_command
async def update(task_id, fields):
    """Update task fields (field=value format)"""
    token = TokenManager.get_token()
    auth_service = AuthService(api_url=API_URL)
    auth_service.set_token(token)
    task_repo = await auth_service.get_task_repository()
    task_service = TaskService(task_repo)

    update_data = {}
    for field_pair in fields:
        if "=" in field_pair:
            key, value = field_pair.split("=", 1)
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            elif value.isdigit():
                value = int(value)
            elif key == "json_data":
                value = json.loads(value)
            update_data[key] = value
    try:
        result = await task_service.update_task(task_id, update_data)
        click.echo("Task updated")
        click.echo(json.dumps(result, indent=2, default=str))
    except Exception as e:
        click.echo(f"Failed to update task: {str(e)}")


@task.command()
@click.argument("task_id", type=int)
@require_auth
@async_command
async def delete(task_id):
    """Delete a task"""
    token = TokenManager.get_token()
    auth_service = AuthService(api_url=API_URL)
    auth_service.set_token(token)
    task_repo = await auth_service.get_task_repository()
    task_service = TaskService(task_repo)

    try:
        result = await task_service.delete_task(task_id)
        click.echo("Task deleted")
        click.echo(json.dumps(result, indent=2, default=str))
    except Exception as e:
        click.echo(f"Failed to delete task: {str(e)}")


@task.command()
@click.argument("task_id", type=int)
@click.argument("user_id", type=int)
@require_auth
@async_command
async def assign(task_id, user_id):
    """Assign task to user"""
    token = TokenManager.get_token()
    auth_service = AuthService(api_url=API_URL)
    auth_service.set_token(token)
    task_repo = await auth_service.get_task_repository()
    task_service = TaskService(task_repo)

    try:
        result = await task_service.assign_task(task_id, user_id)
        click.echo("Task assigned")
        click.echo(json.dumps(result, indent=2, default=str))
    except Exception as e:
        click.echo(f"Failed to assign task: {str(e)}")


@task.command()
@click.argument("task_id", type=int)
@require_auth
@async_command
async def start(task_id):
    """Start working on task"""
    token = TokenManager.get_token()
    auth_service = AuthService(api_url=API_URL)
    auth_service.set_token(token)
    task_repo = await auth_service.get_task_repository()
    task_service = TaskService(task_repo)

    try:
        result = await task_service.start_task(task_id)
        click.echo("Task started")
        click.echo(json.dumps(result, indent=2, default=str))
    except Exception as e:
        click.echo(f"Failed to start task: {str(e)}")


@task.command()
@click.argument("task_id", type=int)
@require_auth
@async_command
async def finalize(task_id):
    """Finalize task"""
    token = TokenManager.get_token()
    auth_service = AuthService(api_url=API_URL)
    auth_service.set_token(token)
    task_repo = await auth_service.get_task_repository()
    task_service = TaskService(task_repo)

    try:
        result = await task_service.finalize_task(task_id)
        click.echo("Task finalized")
        click.echo(json.dumps(result, indent=2, default=str))
    except Exception as e:
        click.echo(f"Failed to finalize task: {str(e)}")


@task.command()
@click.argument("task_id", type=int)
@require_auth
@async_command
async def approve(task_id):
    """Approve task"""
    token = TokenManager.get_token()
    auth_service = AuthService(api_url=API_URL)
    auth_service.set_token(token)
    task_repo = await auth_service.get_task_repository()
    task_service = TaskService(task_repo)

    try:
        result = await task_service.approve_task(task_id)
        click.echo("Task approved")
        click.echo(json.dumps(result, indent=2, default=str))
    except Exception as e:
        click.echo(f"Failed to approve task: {str(e)}")


@task.command()
@click.argument("task_id", type=int)
@require_auth
@async_command
async def reject(task_id):
    """Reject task"""
    token = TokenManager.get_token()
    auth_service = AuthService(api_url=API_URL)
    auth_service.set_token(token)
    task_repo = await auth_service.get_task_repository()
    task_service = TaskService(task_repo)
    try:
        result = await task_service.reject_task(task_id)
        click.echo("Task rejected")
        click.echo(json.dumps(result, indent=2, default=str))
    except Exception as e:
        click.echo(f"Failed to reject task: {str(e)}")
