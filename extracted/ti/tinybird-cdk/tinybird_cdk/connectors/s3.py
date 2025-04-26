from tinybird_cdk import connector
from tinybird_cdk.cloud import s3


# WARNING: THIS CONNECTOR WAS JUST PROTOTYPED TO HELP DESIGN THE CDK, BUT IT IS
# NOT USED AND IT DOES NOT HAVE TESTS.
class Connector(connector.CloudConnector):
    def __init__(self):
        super().__init__()
        self.client = s3.Client()
