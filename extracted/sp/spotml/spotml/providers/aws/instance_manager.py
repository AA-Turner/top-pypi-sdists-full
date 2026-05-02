import boto3
import requests as requests

from spotml.config.config_utils import DEFAULT_CONFIG_FILENAME
from spotml.config.url import API_URL
from spotml.constants.constants import GENERIC_ERROR_MESSAGE
from spotml.deployment.abstract_cloud_instance.abstract_cloud_instance_manager import AbstractCloudInstanceManager
from spotml.errors.instance_not_running import InstanceNotRunningError
from spotml.providers.aws.config.instance_config import InstanceConfig
from spotml.providers.aws.data_transfer import DataTransfer
from spotml.providers.aws.instance_deployment import InstanceDeployment
from spotml.providers.aws.resource_managers.bucket_manager import BucketManager
from spotml.services.run_service import get_instance_tracking_status
from spotml.utils import render_table
from tabulate import tabulate
from dateutil import parser
from tzlocal import get_localzone


def get_local_time_from_string(utc_date_time_string):
    return parser.parse(utc_date_time_string).astimezone(get_localzone()).strftime('%b %d, %Y -%l:%M%p %Z')


class InstanceManager(AbstractCloudInstanceManager):
    instance_config: InstanceConfig
    bucket_manager: BucketManager
    data_transfer: DataTransfer
    instance_deployment: InstanceDeployment

    def _get_instance_config(self, instance_config: dict) -> InstanceConfig:
        """Validates the instance config and returns an InstanceConfig object."""
        return InstanceConfig(instance_config, self.project_config)

    def _get_bucket_manager(self) -> BucketManager:
        """Returns an bucket manager."""
        return BucketManager(self.instance_config.project_config.project_name, self.instance_config.region)

    def _get_data_transfer(self) -> DataTransfer:
        """Returns a data transfer object."""
        return DataTransfer(
            local_project_dir=self.project_config.project_dir,
            host_project_dir=self.instance_config.host_project_dir,
            sync_filters=self.project_config.sync_filters,
            instance_name=self.instance_config.name,
            region=self.instance_config.region,
        )

    def _get_instance_deployment(self) -> InstanceDeployment:
        """Returns an instance deployment manager."""
        return InstanceDeployment(self.instance_config)

    def sendConfigCredentialFiles(self, script_name: str):
        session = boto3.session.Session()
        credentials = session.get_credentials()

        region = session.region_name
        if not region:
            raise ValueError("You must specify a default region. You can configure your region by "
                             "running 'aws configure'")

        access_key = credentials.access_key
        secret_key = credentials.secret_key

        with open(DEFAULT_CONFIG_FILENAME, 'r') as spotYml:
            with open(self.ssh_key_path, 'r') as sshKey:
                files = {'spotml_config': spotYml, 'ssh_key': sshKey}
                r = requests.post(f'{API_URL}/run', files=files,
                                  data={'script_name': script_name, 'region': region,
                                        'access_key': access_key, 'secret_key': secret_key})
                if r.status_code != 201:
                    print("Oops, looks like something went wrong in scheduling the run")
                    print(GENERIC_ERROR_MESSAGE)
                    raise Exception('Something went wrong in scheduling run in cloud', r)
                old_runs = r.json()['old_runs']
                if len(old_runs) > 0:
                    print("There is already an old scheduled run. Below run will be stopped and replaced by the "
                          "current run.")
                    print("OLD RUN")
                    table = []
                    for run in old_runs:
                        table.append([run['id'], run['script_name'], run['status'],
                                      get_local_time_from_string(run['created_date'])])
                    print(tabulate(table, headers=['Run Id', 'Command', 'Status', 'Created Date'], tablefmt="psql"))

                print("\n CURRENT RUN")
                current_run = r.json()['current_run']
                print(tabulate(
                    [[current_run['id'], current_run['script_name'], current_run['status'],
                      get_local_time_from_string(current_run['created_date'])]],
                    headers=['Run Id', 'Command', 'Status', 'Created Date'], tablefmt="psql"))

    def get_status_text(self) -> str:
        instance = self.instance_deployment.get_instance()
        if not instance:
            table = [
                ('Name', 'Status'),
                (self.instance_config.name, 'Not Running'),
            ]
            return render_table(table)

        table = [
            ('Instance State', instance.state),
            ('Instance Type', instance.instance_type),
            ('Availability Zone', instance.availability_zone),
        ]

        if instance.public_ip_address:
            table.append(('Public IP Address', instance.public_ip_address))

        if instance.lifecycle == 'spot':
            spot_price = instance.get_spot_price()
            table.append(('Purchasing Option', 'Spot Instance'))
            table.append(('Spot Instance Price', '$%.04f' % spot_price))
        else:
            on_demand_price = instance.get_on_demand_price()
            table.append(('Purchasing Option', 'On-Demand Instance'))
            table.append(('Instance Price', ('$%.04f (us-east-1)' % on_demand_price) if on_demand_price else 'Unknown'))

        is_tracking_idle_time = get_instance_tracking_status()
        table.append(('Tracking Idle Time', is_tracking_idle_time))

        return render_table(table)

    @property
    def ssh_key_path(self):
        return self.instance_deployment.key_pair_manager.key_path
