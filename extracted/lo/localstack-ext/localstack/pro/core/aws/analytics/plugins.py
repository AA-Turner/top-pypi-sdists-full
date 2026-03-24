from localstack.pro.core.bootstrap.licensingv2 import get_licensed_environment
from localstack.pro.core.runtime.plugin import PlatformPlugin
class AwsRequestAnalyticsPlugin(PlatformPlugin):
	name='aws-request-analytics'
	def on_platform_start(C):
		from localstack.aws import handlers as A;from.aggregator_rollup import RollupRequestAggregator as D;from.aggregator_sequence import SequenceRequestAggregator as E;from.handler import AwsRequestAnalyticsHandler as F
		if C._should_use_sequence_aggregator():B=E()
		else:B=D()
		A.count_service_request=F(aggregator=B);A.count_service_request.start()
	def _should_use_sequence_aggregator(B):A=get_licensed_environment().product_entitlements;return A.has_entitlement('localstack.stacks.premium')or A.has_entitlement('localstack.stacks.preview')
	def on_platform_shutdown(B):from localstack.aws import handlers as A;A.count_service_request.shutdown()