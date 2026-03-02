import json
import logging

import pandas as pd
from teradataml import DataFrame

from ..util.connections import execute_sql

logger = logging.getLogger(__name__)

byom_query = """
CREATE TABLE {} (
      model_version VARCHAR(255),
      model_id VARCHAR(255),
      model_type VARCHAR(255),
      project_id VARCHAR(255),
      deployed_at TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6),
      model BLOB(2097088000))
UNIQUE PRIMARY INDEX (model_version);
"""

merge_query = """
MERGE {} target
     USING {} source
       ON target.column_name = source.column_name
     WHEN MATCHED THEN
       UPD SET stats = source.stats, column_type = source.column_type, update_ts = source.update_ts
     WHEN NOT MATCHED THEN
       INS (source.column_name, source.column_type, source.stats, source.update_ts);
"""
temp_table = "tmo_stats_temp"


def save_feature_stats(features_table: str, feature_type: str, stats: dict) -> None:
    cvt_query = (
        f"CREATE VOLATILE TABLE {temp_table} AS {features_table} WITH NO DATA ON COMMIT"
        " PRESERVE ROWS;"
    )
    ins_query = (
        f"INS {temp_table} (column_name,column_type,stats,update_ts)"
        " VALUES(?,?,?,CURRENT_TIMESTAMP);"
    )
    m_query = merge_query.format(features_table, temp_table)
    dt_query = f"DROP TABLE {temp_table};"

    logger.debug(cvt_query)
    execute_sql(cvt_query)
    logger.debug(ins_query)
    execute_sql(ins_query, [[f, feature_type, json.dumps(stats[f])] for f in stats])
    logger.debug(m_query)
    execute_sql(m_query)
    logger.debug(dt_query)
    execute_sql(dt_query)


def get_feature_stats_summary(features_table: str) -> dict:
    try:
        fs = DataFrame.from_query(
            f"SEL column_name, column_type FROM {features_table}"
        ).to_pandas(all_rows=True)
        fs = fs.reset_index().drop(
            fs.columns.difference(["column_name", "column_type"]), axis=1
        )
        fs = fs.set_index("column_name")
        return pd.Series(fs.column_type).to_dict()
    except Exception:  # noqa
        logger.warning("Couldn't read statistics metadata, assuming it's empty")
        return {}


def get_feature_stats(features_table: str, feature_type: str) -> dict:
    try:
        fs = DataFrame.from_query(
            f"SEL * FROM {features_table} WHERE column_type='{feature_type}'"
        ).to_pandas(all_rows=True)
        fs = fs.reset_index().drop(
            fs.columns.difference(["column_name", "stats"]), axis=1
        )
        fs = fs.set_index("column_name")
        fs = pd.Series(fs.stats).to_dict()
        return {k: json.loads(fs[k]) for k in fs}
    except Exception:  # noqa
        logger.warning("Couldn't read statistics metadata, assuming it's empty")
        return {}


def get_features_stats_metadata_ct_query(tablename: str, volatile: bool = False) -> str:
    # It's crucial that we use column_name as a unique index here, because UI currently doesn't allow to set a feature type
    # If the user wants the same column to play as both continuous and categorical features, she must provide a copy of the column with a different name
    ct_query = """
  CREATE {} (
      column_name VARCHAR(128) CHARACTER SET UNICODE NOT CASESPECIFIC, 
      column_type VARCHAR(128) CHARACTER SET UNICODE NOT CASESPECIFIC,
      stats JSON,
      update_ts TIMESTAMP)
  UNIQUE PRIMARY INDEX ( column_name ){}
  """
    if volatile:
        return ct_query.format(
            f"VOLATILE TABLE {tablename}", " ON COMMIT PRESERVE ROWS;"
        )
    else:
        return ct_query.format(f"TABLE {tablename}", ";")


def create_features_stats_table(features_table: str, volatile: bool = False) -> None:
    query = get_features_stats_metadata_ct_query(features_table, volatile)
    logger.debug(query)
    execute_sql(query)
