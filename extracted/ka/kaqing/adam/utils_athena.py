import functools
import time
import boto3
import botocore

from adam.config import Config
from adam.utils import log2, log_exc, wait_log
from adam.utils_tabulize import tabulize
from adam.utils_context import Context

# no state utility class
class Athena:
   @functools.lru_cache()
   def database_names(like: str = None):
      # this function is called only from export currently
      wait_log(f'Inspecting export database schema...')

      query = f"SELECT schema_name FROM information_schema.schemata WHERE schema_name <> 'information_schema'"
      if like:
         query = f"{query} AND schema_name like '{like}'"

      with log_exc():
         state, reason, rs = Athena.query(query)
         if rs:
            names = []
            for row in rs[1:]:
                  row_data = [col.get('VarCharValue') if col else '' for col in row['Data']]
                  names.append(row_data[0])

            return names

      return []

   def clear_cache(cache: str = None):
      if not cache or cache == 'databases':
         Athena.database_names.cache_clear()
      if not cache or cache == 'tables':
         Athena.table_names.cache_clear()
      if not cache or cache == 'columns':
         Athena.column_names.cache_clear()

   @functools.lru_cache()
   def table_names(database: str = 'audit', function: str = 'audit'):
      table_names = []
      try:
         region_name = Config().get(f'{function}.athena.region', 'us-west-2')
         database_name = Config().get(f'{function}.athena.database', database)
         catalog_name = Config().get(f'{function}.athena.catalog', 'AwsDataCatalog')

         athena_client = boto3.client('athena', region_name=region_name)
         paginator = athena_client.get_paginator('list_table_metadata')

         for page in paginator.paginate(CatalogName=catalog_name, DatabaseName=database_name):
            for table_metadata in page.get('TableMetadataList', []):
               table_names.append(table_metadata['Name'])
      except botocore.exceptions.NoCredentialsError as e:
         # aws credentials not found
         if function == 'audit':
            log2(f'Please configure AWS credentials to Audit Log Database.')
      except:
         pass

      return table_names

   @functools.lru_cache()
   def column_names(tables: list[str] = [], database: str = None, function: str = 'audit', partition_cols_only = False):
      with log_exc():
         if not database:
            database = Config().get(f'{function}.athena.database', 'audit')

         if not tables:
            tables = Config().get(f'{function}.athena.tables', 'audit').split(',')

         table_names = "'" + "','".join([table.strip() for table in tables]) + "'"

         query = f"select column_name from information_schema.columns where table_name in ({table_names}) and table_schema = '{database}'"
         if partition_cols_only:
            query = f"{query} and extra_info = 'partition key'"

         _, _, rs = Athena.query(query)
         if rs:
            return [row['Data'][0].get('VarCharValue') for row in rs[1:]]

      return []

   def run_query(sql: str, database: str = None, ctx: Context = Context.NULL):
      state, reason, rs = Athena.query(sql, database)

      # log_file = None
      if state == 'SUCCEEDED':
         if rs:
            column_info = rs[0]['Data']
            columns = [col.get('VarCharValue') for col in column_info]
            tabulize(rs[1:],
                     lambda r: '\t'.join(col.get('VarCharValue') if col else '' for col in r['Data']),
                     header='\t'.join(columns),
                     separator='\t',
                     ctx=ctx)

            return len(rs)-1, ctx.log_file
      else:
         ctx.log2(f"Query failed or was cancelled. State: {state}")
         ctx.log2(f"Reason: {reason}")

      return 0

   def query(sql: str, database: str = None, function: str = 'audit') -> tuple[str, str, list]:
      region_name = Config().get(f'{function}.athena.region', 'us-west-2')
      athena_client = boto3.client('athena', region_name=region_name)

      if not database:
         database = Config().get(f'{function}.athena.database', 'audit')

      s3_output_location = Config().get(f'{function}.athena.output', f's3://s3.ops--{function}/ddl/results')

      response = athena_client.start_query_execution(
         QueryString=sql,
         QueryExecutionContext={
               'Database': database
         },
         ResultConfiguration={
               'OutputLocation': s3_output_location
         }
      )

      query_execution_id = response['QueryExecutionId']

      while True:
         query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
         state = query_status['QueryExecution']['Status']['State']
         if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
               break
         time.sleep(1)

      if state == 'SUCCEEDED':
         results_response = athena_client.get_query_results(QueryExecutionId=query_execution_id)
         if results_response['ResultSet']['Rows']:
            return (state, None, results_response['ResultSet']['Rows'])

         return (state, None, [])
      else:
         return (state, query_status['QueryExecution']['Status'].get('StateChangeReason'), [])