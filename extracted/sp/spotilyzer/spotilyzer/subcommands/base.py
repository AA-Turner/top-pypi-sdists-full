"""
spotilyzer subcommand base class
"""

# 3rd party imports
import boto3


class SubCommand:
    """
    Subcommand base class.
    """

    def __init__(self, args):
        self.client = boto3.client('ec2')
        self.args = args

    def reconnect(self, region):
        """
        Change region in client.
        :param region: AWS region name
        :return: None
        """
        if self.client.meta.region_name == region:
            return
        if region not in [r['RegionName']
                          for r in self.client.describe_regions()['Regions']]:
            raise ValueError(f"invalid region {region}")
        self.client = boto3.client('ec2', region_name=region)

    def getarg(self, name):
        """
        Return subcommand argument.
        :param name: argument name
        :return: argument value
        """
        return getattr(self.args, name.replace('-', '_'))
