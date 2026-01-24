from datetime import datetime
import getpass
import time
import requests

from adam.config import Config
from adam.utils import OffloadHandler, debug, log2, log_exc, offload
from adam.utils_athena import Athena
from adam.utils_net import get_my_host

class AuditMeta:
   def __init__(self, partitions_last_checked: float, cluster_last_checked: float):
      self.partitions_last_checked = partitions_last_checked
      self.cluster_last_checked = cluster_last_checked

# no state utility class
class Audits:
   PARTITIONS_ADDED = 'partitions-added'
   ADD_CLUSTERS = 'add-clusters'

   def log(cmd: str, cluster = 'NA', drive: str = 'NA', duration: float = 0.0, audit_extra = None):
      payload = {
         'cluster': cluster if cluster else 'NA',
         'ts': time.time(),
         'host': get_my_host(),
         'user': getpass.getuser(),
         'line': cmd.replace('"', '""').replace('\n', ' '),
         'drive': drive,
         'duration': duration,
         'audit_extra': audit_extra if audit_extra else '',
      }
      audit_endpoint = Config().get("audit.endpoint", "https://4psvtaxlcb.execute-api.us-west-2.amazonaws.com/prod/")
      try:
         response = requests.post(audit_endpoint, json=payload, timeout=Config().get("audit.timeout", 10))
         if response.status_code in [200, 201]:
               debug(response.text)
         else:
               log2(f"Error: {response.status_code} {response.text}")
      except requests.exceptions.Timeout as e:
         log2(f"Timeout occurred: {e}")

   def get_meta() -> AuditMeta:
      checked_in = 0.0
      cluster_last_checked = 0.0

      state, _, rs = Athena.query(f'select partitions_last_checked, clusters_last_checked from meta')
      if state == 'SUCCEEDED':
         if len(rs) > 1:
            with log_exc():
               row = rs[1]['Data']
               checked_in = float(row[0]['VarCharValue'])
               cluster_last_checked = float(row[1]['VarCharValue'])

      return AuditMeta(checked_in, cluster_last_checked)

   def put_meta(action: str, meta: AuditMeta, clusters: list[str] = None):
      payload = {
         'action': action,
         'partitions-last-checked': meta.partitions_last_checked,
         'clusters-last-checked': meta.cluster_last_checked
      }
      if clusters:
         payload['clusters'] = clusters

      audit_endpoint = Config().get("audit.endpoint", "https://4psvtaxlcb.execute-api.us-west-2.amazonaws.com/prod/")
      try:
         response = requests.post(audit_endpoint, json=payload, timeout=Config().get("audit.timeout", 10))
         if response.status_code in [200, 201]:
               debug(response.text)
         else:
               log2(f"Error: {response.status_code} {response.text}")
      except requests.exceptions.Timeout as e:
         log2(f"Timeout occurred: {e}")

   def find_new_clusters(cluster_last_checked: float) -> list[str]:
      dt_object = datetime.fromtimestamp(cluster_last_checked)

      # select distinct c2.name from cluster as c1 right outer join
      #     (select distinct c as name from audit where y = '1969' and m = '12' and d >= '31' or y = '1969' and m > '12' or y > '1969') as c2
      #     on c1.name = c2.name where c1.name is null
      query = '\n    '.join([
         'select distinct c2.name from cluster as c1 right outer join',
         f'(select distinct c as name from audit where {Audits.date_from(dt_object)}) as c2',
         'on c1.name = c2.name where c1.name is null'])
      log2(query)
      state, _, rs = Athena.query(query)
      if state == 'SUCCEEDED':
         if len(rs) > 1:
               with log_exc():
                  return [r['Data'][0]['VarCharValue'] for r in rs[1:]]

      return []

   def date_from(dt_object: datetime):
        y = dt_object.strftime("%Y")
        m = dt_object.strftime("%m")
        d = dt_object.strftime("%d")

        return f"y = '{y}' and m = '{m}' and d >= '{d}' or y = '{y}' and m > '{m}' or y > '{y}'"

   def offload() -> OffloadHandler:
       return offload(max_workers=Config().get('audit.workers', 3))