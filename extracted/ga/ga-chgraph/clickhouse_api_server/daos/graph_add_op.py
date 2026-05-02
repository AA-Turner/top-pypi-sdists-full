from config import logger_design

logger = logger_design.get_logger()


class CHGraph(object):

    def __init__(self, client):
        self.client = client
        logger.info('CHGraph Start')

    def execute(self, sql):
        res = self.client.query_dataframe(sql)
        return res
