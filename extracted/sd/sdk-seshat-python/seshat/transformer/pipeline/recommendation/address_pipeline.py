from seshat.general import configs
from seshat.transformer.deriver import (
    FeatureForAddressDeriver,
    SFrameFromColsDeriver,
    OperationOnColsDeriver,
    PercentileTransactionValueDeriver,
    InteractedSymbolsToSentenceDeriver,
)
from seshat.transformer.pipeline import Pipeline

address_pipeline = Pipeline(
    [
        SFrameFromColsDeriver(
            cols=(configs.FROM_ADDRESS_COL, configs.TO_ADDRESS_COL),
            result_col="address",
        ),
        FeatureForAddressDeriver(
            value_col="SYMBOL",
            is_numeric=False,
            result_col="unique_tokens_count",
            agg_func="count",
        ),
        FeatureForAddressDeriver(
            value_col="AMOUNT_USD",
            is_numeric=False,
            result_col="sent_amount",
        ),
        FeatureForAddressDeriver(
            value_col="AMOUNT_USD",
            is_numeric=False,
            address_index_col=configs.TO_ADDRESS_COL,
            result_col="received_amount",
        ),
        FeatureForAddressDeriver(
            value_col="SYMBOL",
            is_numeric=False,
            result_col="sent_symbols",
            agg_func="unique",
        ),
        FeatureForAddressDeriver(
            value_col="SYMBOL",
            is_numeric=False,
            address_index_col=configs.TO_ADDRESS_COL,
            result_col="received_symbols",
            agg_func="unique",
        ),
        FeatureForAddressDeriver(
            value_col=configs.FROM_ADDRESS_COL,
            is_numeric=False,
            address_index_col=configs.TO_ADDRESS_COL,
            result_col="received_partners",
            agg_func="nunique",
        ),
        FeatureForAddressDeriver(
            value_col=configs.TO_ADDRESS_COL,
            is_numeric=False,
            result_col="sent_partners",
            agg_func="nunique",
        ),
        OperationOnColsDeriver(
            cols=("received_amount", "sent_amount"),
            result_col="interacted_avg_amount",
        ),
        OperationOnColsDeriver(
            group_keys={"default": "address"},
            cols=("received_amount", "sent_amount"),
            agg_func="sum",
            result_col="interacted_total_amount",
        ),
        PercentileTransactionValueDeriver(
            group_keys={"default": "address"},
            value_col="interacted_avg_amount",
        ),
        InteractedSymbolsToSentenceDeriver(
            symbol_col="SYMBOL",
            result_col="sentence_symbols",
        ),
    ]
)
