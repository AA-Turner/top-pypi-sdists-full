from rich.console import Console
from rich.table import Table

from seshat.general.command.base import BaseTyperCommand, ApiConfig
from seshat.utils.rest import RestClient
from seshat.general.exceptions import RestClientException


class JobStatusCommand(BaseTyperCommand):
    def __init__(self, base_url: str = None, auth_token: str = None, report=True):
        super().__init__(report)
        self.job_config = ApiConfig(base_url=base_url, auth_token=auth_token)

        self.rest_client = RestClient(
            base_url=self.job_config.base_url,
            timeout=30,
            max_retries=5,
            retry_delay=1,
            headers={
                "Authorization": f"Bearer {self.job_config.auth_token}",
                "Content-Type": "application/json",
            },
        )

    def job_status(self, job_id: str) -> dict:
        """
        Check the status of a job

        Args:
            job_id: ID of the job to check

        Returns:
            dict: Full response data from the API

        Raises:
            RestClientException: If there's an API communication error
            ValueError: If API configuration is missing
        """
        if not self.job_config.base_url or not self.job_config.auth_token:
            self.echo("API configuration missing. Please set base_url and auth_token")
            raise ValueError("API configuration missing")

        try:
            response_data = self.rest_client.get(f"jobs/{job_id}/status")
            data = response_data.get("data", {})
            status = data.get("state", "Unknown")
            updated_at = data.get("updated_at", "Unknown")
            current_load = str(data.get("current_load", "Unknown"))
            message = response_data.get("message", "")
            api_status = response_data.get("status", "")

            table = Table(title="Job Status")
            table.add_column("Job ID", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Updated At", style="blue")
            table.add_column("Current Load", style="yellow")
            table.add_column("Message", style="magenta")
            table.add_column("API Status", style="red")

            # Add row
            table.add_row(job_id, status, updated_at, current_load, message, api_status)
            Console().print(table)

            return response_data

        except RestClientException:
            self.echo("❌ Failed to get job status")
        except Exception as e:
            self.echo(f"❌ Failed to get job status: {str(e)}")
