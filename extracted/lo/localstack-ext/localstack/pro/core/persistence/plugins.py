import logging
from localstack.pro.core.config import ACTIVATE_PRO
from localstack.pro.core.runtime.plugin import PlatformPlugin
LOG=logging.getLogger(__name__)
class BasePersistence(PlatformPlugin):
	name='base-persistence'
	def on_platform_start(C):from localstack.pro.core.persistence.avro.reducers import register as A;from localstack.pro.core.persistence.pickling.reducers import register as B;B();A()
	def should_load(A)->bool:return ACTIVATE_PRO
	def on_platform_ready(B):from localstack.pro.core.utils.persistence import update_persistence_health_info as A;A()