from localstack.pro.core.runtime.plugin import PlatformPlugin
class AwsRequestLoggerPlugin(PlatformPlugin):
	name='aws-request-logger'
	def on_platform_start(C):from localstack.aws import handlers as A;from localstack.pro.core.analytics.aws_request_logger import RequestLoggerHandler as B;A.count_service_request=B()