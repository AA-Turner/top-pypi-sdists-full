import logging
from typing import Any
from localstack.pro.core.runtime.plugin import ProPlatformPlugin
LOG=logging.getLogger(__name__)
class LDMPlugin(ProPlatformPlugin):
	name='lambda-ldm'
	def on_service_load(A,service,provider):
		if service!='lambda':return
		from localstack.pro.core.services.lambda_.lambda_debug_mode import hooks;hooks.SHOULD_LOAD_LDM_PLUGIN=True
	def on_platform_shutdown(B):
		from localstack.pro.core.services.lambda_.lambda_debug_mode.ldm import LDM
		try:LDM.teardown()
		except Exception as A:LOG.error("Unexpected error encountered when attempting to signal the LDM to stop '%s'.",A)