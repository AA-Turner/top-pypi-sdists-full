from pyspark.sql import functions as F

from seshat.general import configs
from seshat.utils.mixin import RawHandlerDispatcherMixin
from seshat.utils.singleton import Singleton


class PopularContractsFinder(RawHandlerDispatcherMixin, metaclass=Singleton):
    HANDLER_NAME = "find"

    def find(
        self,
        raw,
        contract_address_col: str = configs.CONTRACT_ADDRESS_COL,
        limit: int = 100,
    ):
        return self.call_handler(raw, contract_address_col, limit)

    def find_df(self, raw, contract_address_col, limit):
        df_agg = raw.groupby(contract_address_col).size().reset_index(name="count")
        df_agg = df_agg.sort_values(by="count", ascending=False).reset_index(drop=True)

        popular_contracts = df_agg.head(limit)[contract_address_col]
        return popular_contracts

    def find_spf(self, raw, contract_address_col, limit):
        spf_agg = raw.groupBy(contract_address_col).count()
        spf_agg = spf_agg.orderBy(F.col("count").desc())
        return [
            row[contract_address_col]
            for row in spf_agg.limit(limit).select(contract_address_col).collect()
        ]