from __future__ import annotations
from localstack.pro.core import config as pro_config
from localstack.pro.core.constants import S3_ASSETS_BUCKET
from localstack.pro.core.plugins import LOG
from localstack.pro.core.runtime.plugin import ProPlatformPlugin
TRANSPARENT_ENDPOINT_INJECTION_NAMES=['.*.amazonaws.com','.*aws.amazon.com','.*cloudfront.net']
DEFAULT_SKIP_PATTERNS={'.*(checkip|forums|console|docs|clientvpn|sso|boto3|(signin(\\-reg)?))\\.([^\\.]+\\.)?(aws\\.amazon|amazonaws)\\.com','.*captcha-prod\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com','^aws\\.amazon\\.com','^github-production-release-.*\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com','^aws-glue-etl-artifacts\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com','^redshift-maven-repository\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com',f"^{S3_ASSETS_BUCKET}\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com",'^localstack-pods-.*\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com','^prod-registry-k8s-io-.*\\.s3\\.(dualstack\\.)?.*\\.amazonaws\\.com','^(?:prod|staging)sharedcertsstack-.*\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com'}
class TransparentEndpointInjectionPlugin(ProPlatformPlugin):
	name='transparent-endpoint-injection'
	def on_platform_start(G):
		from localstack.dns.server import get_dns_server as B,is_server_running as C
		if not pro_config.DISABLE_TRANSPARENT_ENDPOINT_INJECTION and C():
			try:
				LOG.debug('setting up transparent endpoint injection');A=B()
				for D in TRANSPARENT_ENDPOINT_INJECTION_NAMES:A.add_host_pointing_to_localstack(D)
				for E in DEFAULT_SKIP_PATTERNS:A.add_skip(E)
			except Exception as F:LOG.warning('Unable to configure transparent endpoint injection: %s',F)