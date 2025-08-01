import logging
from localstack.pro.core import config as pro_config
from localstack.pro.core.runtime.plugin import PlatformPlugin
LOG=logging.getLogger(__name__)
class BedrockExtensionPlugin(PlatformPlugin):
	name='bedrock-extension'
	def should_load(A):return super().should_load()and pro_config.BEDROCK_PREWARM
	def on_platform_ready(B):from localstack.pro.core.services.bedrock.backends import get_foundation_model_manager as A;LOG.debug('Pre-warming Bedrock engine because BEDROCK_PREWARM is set');A();LOG.debug('Bedrock engine successfully pre-warmed')