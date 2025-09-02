import argparse
import logging
import os

from ipfabric import IPFClient
from ipfabric.models.jobs import TechsupportPayload, Jobs, TechsupportSnapshotSettings
from ipfabric.scripts.shared import load_env, base_args, parse_base_args

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    raise ImportError("rich is required, please install by using `pip install rich or pip install ipfabric[cli]`.")


logger = logging.getLogger("TechSupportCLI")

PROGRESS = "[progress.description]{task.description}"
console = Console()


def parse_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    args = parse_base_args(parser.parse_args())

    if not args.upload_username and not args.upload_password:
        console.log(args)
        raise ValueError(
            "Upload username and password must be provided as an argument or set as an environment variable "
            "(IPF_UPLOAD_USERNAME and IPF_UPLOAD_PASSWORD)."
        )
    return args


def main():  # noqa:C901
    load_env()
    parser = argparse.ArgumentParser(
        description="Upload a techsupport file using IPFabric API. "
        "Environment variables can be exported or configured in the .env file."
    )
    parser = base_args(parser)
    parser.add_argument(
        "-uu",
        "--upload-username",
        default=os.getenv("IPF_UPLOAD_USERNAME", "techsupport"),
        help="Username for uploading the techsupport file or IPF_UPLOAD_USERNAME env variable. Default: techsupport",
    )
    parser.add_argument(
        "-up",
        "--upload-password",
        default=os.getenv("IPF_UPLOAD_PASSWORD", None),
        help="Password for uploading the techsupport file or IPF_UPLOAD_PASSWORD env variable.",
    )
    parser.add_argument(
        "-ur",
        "--upload-region",
        choices=["eu", "us"],
        default=os.getenv("IPF_UPLOAD_REGION", "eu"),
        help="Server region for the upload or IPF_UPLOAD_REGION env variable. Default: eu",
    )
    parser.add_argument(
        "-ut",
        "--upload-timeout",
        type=int,
        default=600,
        help="Timeout for the upload request in seconds. Default: 600",
    )
    parser.add_argument(
        "-nvu",
        "--no-verify-upload",
        dest="upload_verify",
        action="store_false",
        default=True,
        help="Disable verification of the upload process.",
    )
    parser.add_argument(
        "-dt",
        "--download-timeout",
        type=int,
        default=60,
        help="Timeout to wait for the download process in seconds. Default: 60",
    )
    parser.add_argument(
        "-dr",
        "--download-retry",
        type=int,
        default=5,
        help="How many times to wait --download-timeout before failing Default: 5 "
        "(5 Retries of 60 seconds each equals 5 minutes.)",
    )
    parser.add_argument(
        "-DR",
        "--dry-run",
        action="store_true",
        help="Dry run the techsupport process without actually uploading the file.",
    )
    args = parse_args(parser)

    console.log(f"[bold blue]Initializing Techsupport API with base_url={args.base_url}...[/bold blue]")
    ipf = IPFClient(snapshot_id=args.snapshot, base_url=args.base_url, auth=args.auth)
    ipf._client.headers["user-agent"] += "; ipf_techsupport"
    jobs = Jobs(client=ipf)

    payload = TechsupportPayload(snapshot=TechsupportSnapshotSettings(id=args.snapshot))
    if args.dry_run:
        console.log("[bold yellow]Dry run enabled. Skipping techsupport job creation...[/bold yellow]")
        return
    console.log("[bold blue]Starting techsupport job...[/bold blue]")

    with Progress(
        SpinnerColumn(),
        TextColumn(PROGRESS),
        console=console,
    ) as progress:
        _ = progress.add_task(description="Generating techsupport...", total=None)
        try:
            job = jobs.generate_techsupport(
                payload, wait_for_ts=True, timeout=args.download_timeout, retry=args.download_retry
            )
        except Exception as e:
            progress.stop()
            console.log(f"[bold red]Failed to generate techsupport: {e}[/bold red]")
            return

    console.log("[bold blue]Downloading techsupport file...[/bold blue]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(description="Downloading techsupport file...", total=None)
        try:
            techsupport_resp = jobs.download_techsupport_file(job.id)
            progress.update(task, description="Techsupport file downloaded successfully.")
        except Exception as e:
            progress.stop()
            console.log(f"[bold red]Failed to download techsupport file: {e}[/bold red]")
            return

    console.log("[bold blue]Uploading techsupport file...[/bold blue]")
    with Progress(
        SpinnerColumn(),
        TextColumn(PROGRESS),
        console=console,
    ) as progress:
        task = progress.add_task(description="Uploading file...", total=None)
        try:
            jobs.upload_techsupport_file(
                upload_username=args.upload_username,
                upload_password=args.upload_password,
                upload_file_timeout=args.upload_timeout,
                upload_server=args.upload_region,
                techsupport_bytes=techsupport_resp.content,
                upload_verify=args.upload_verify,
            )
            progress.update(task, description="Techsupport file uploaded successfully.")
        except Exception as e:
            progress.stop()
            console.log(f"[bold red]Failed to upload techsupport file: {e}[/bold red]")
            return

    console.log("[bold green]Techsupport process completed successfully.[/bold green]")


if __name__ == "__main__":
    main()
