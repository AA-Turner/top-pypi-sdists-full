import datetime

from .client_snowflake_auth import SnowflakeAuthClient
from .constants import *
from .utils import *
from .runner_cluster import ClusterRunner
from .runner_propensity import PropensityRunner
from .runner_regression import RegressionRunner
from .runner_causal import CausalRunner
from .runner_mmm import MMMRunner
from .runner_performance import PerformanceRunner 
from .runner_task import TaskRunner


class Analyzer:
    """
    Parent class for G2M client. This is the class that should be instantiated
    by the client. For detailed methods, see the appropriate runner class.

    :param host: the FQDN for your API tenant
    :type host: str, required
    :verbose: Set to true for verbose output
    :type verbose: boolean, optional
    """

    def __init__(self, host=None, verbose=False):
        """
        Initialize the Analyzer with Snowflake authentication.
        
        Args:
            host (str, optional): The FQDN for your API tenant.
            verbose (bool, optional): Set to true for verbose output.
        """
        # General config
        self.__client = SnowflakeAuthClient(host=host, verbose=verbose)
        self.__base_url = 'https://{}/api/v1'.format(host)
        self.__uri = '{}/analytics/'.format(self.__base_url)
        self.test = TaskRunner(client=self.__client, base_url=self.__base_url)

        # Initialize specific endpoints
        self.cluster = ClusterRunner(client=self.__client, base_url=self.__base_url)
        self.propensity = PropensityRunner(client=self.__client, base_url=self.__base_url)
        self.regression = RegressionRunner(client=self.__client, base_url=self.__base_url)
        self.causal = CausalRunner(client=self.__client, base_url=self.__base_url)
        self.mmm = MMMRunner(client=self.__client, base_url=self.__base_url)
        self.performance = PerformanceRunner(client=self.__client, base_url=self.__base_url)
        return

    def version(self):
        """
        Provide version info

        :return JSON object with version info and other metadata
        """
        copy_client = self.client_version()
        copy_api = self.api_version()
        return {
            'api': {
                'status': copy_api['status'], 
                'version': copy_api['response']['version'] if copy_api['status']==200 else 'N/A',
                'tenant': copy_api['response']['tenant'] if copy_api['status']==200 else 'N/A',
            }, 
            'client': {
                'version': copy_client['version'],
            }, 
            'copyright': copy_client['copyright'], 
        }

    def api_version(self):
        """
        Provide API version info

        :return: JSON object with API version and other metadata
        """
        return self.__client._post(self.__uri, {'command': 'version'})

    def client_version(self):
        """
        Provide client version info

        :return: JSON object with API version and other metadata
        """
        return ({'version': f'{CLIENT_VERSION}', 'copyright': f'{datetime.date.today().year} (c) Go2Market Insights Inc. All rights reserved. Patent pending. '})

    def login(self, user, account, endpoint, endpoint_path='/', role=None, snowflake_account_url=None, lifetime=59, renewal_delay=54, private_key_file_path=None):
        """
        Log in to G2M API using Snowflake key pair authentication.

        Args:
            user (str): Snowflake username.
            account (str): Snowflake account identifier.
            endpoint (str): The ingress endpoint of the service.
            endpoint_path (str, optional): The url path for the ingress endpoint. Defaults to '/'.
            role (str, optional): Snowflake role to use. Defaults to None.
            snowflake_account_url (str, optional): Full Snowflake account URL. Defaults to None.
            lifetime (int, optional): Token lifetime in minutes. Defaults to 59.
            renewal_delay (int, optional): Token renewal delay in minutes. Defaults to 54.
            private_key_file_path (str): Path to private key file for keypair auth.
        
        Returns:
            None
        """
        status_code = self.__client._login(
            user=user, 
            account=account, 
            endpoint=endpoint, 
            endpoint_path=endpoint_path, 
            role=role, 
            snowflake_account_url=snowflake_account_url, 
            lifetime=lifetime, 
            renewal_delay=renewal_delay,
            private_key_file_path=private_key_file_path
        )
        
        if status_code == 200:
            print('Login successful')
        else:
            print(f'Could not log in (status code: {status_code})')

    def logout(self):
        """
        Log out of G2M API

        :rtype: None
        """
        return self.__client._logout()
