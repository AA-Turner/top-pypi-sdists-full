import boto3
from boto3.dynamodb.conditions import Key

_dynamodb_client = boto3.resource("dynamodb")


def get_dynamodb_client():
    return _dynamodb_client


class DataHandler:
    def __init__(self, table_name: str, logger=None, client=None, key="pk"):
        self.key = key
        if client is None:
            self._client = get_dynamodb_client()
        else:
            self._client = client
        self._table_name = table_name
        self._logger = logger
        self.table = self._client.Table(self._table_name)

    def add_item(self, identifier: str, value: dict):
        self.table.put_item(Item={self.key: identifier, **value})

    def update_item(self, identifier: str, value: dict):
        if self.key in value.keys():
            self.log("remove key from the value")
            value.pop(self.key)
        self.table.put_item(Item={self.key: identifier, **value})

    def log(self, message: str):
        if self._logger is None:
            print(message)
        self._logger.info(msg=message)

    def get_item(self, identifier: str):
        response = self.table.query(KeyConditionExpression=Key(self.key).eq(identifier))
        items = response["Items"]

        if not items:
            return None

        if len(items) > 1:
            self.log("Multiple items present in the queryset")
            raise Exception(f"More than one item found for {identifier}")

        entry = items[0]
        return entry

    def scan_items(self, *args, **kwargs):
        result = self.table.scan(**kwargs)
        return result["Items"]

    def query_items(self, *args, **kwargs):
        result = self.table.query(**kwargs)
        if not result:
            return None
        return result["Items"]
