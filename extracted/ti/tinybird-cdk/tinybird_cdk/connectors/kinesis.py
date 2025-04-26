import multiprocessing

from kinesis.consumer import KinesisConsumer
from kinesis.state import DynamoDB

from tinybird_cdk import connector

# https://github.com/borgstrom/offspring/issues/4
multiprocessing.set_start_method("fork")

# WARNING: THIS CONNECTOR WAS JUST PROTOTYPED TO HELP DESIGN THE CDK, BUT IT IS
# NOT USED AND IT DOES NOT HAVE TESTS.
class Connector(connector.StreamingConnector):
    def stream(self, stream_name, data_source):
        state = DynamoDB(table_name=f'tb_{stream_name}_{data_source}')
        for message in KinesisConsumer(stream_name=stream_name, state=state):
            self.tb.append_event(message['Data'], data_source=data_source)
