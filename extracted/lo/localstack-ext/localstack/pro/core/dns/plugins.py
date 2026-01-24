from __future__ import annotations
from localstack.pro.core import config as pro_config
from localstack.pro.core.constants import S3_ASSETS_BUCKET
from localstack.pro.core.plugins import LOG
from localstack.pro.core.runtime.plugin import ProPlatformPlugin
from localstack.runtime import hooks
TRANSPARENT_ENDPOINT_INJECTION_NAMES=['.*.amazonaws.com','.*aws.amazon.com','.*cloudfront.net']
DEFAULT_SKIP_PATTERNS={'.*(checkip|forums|console|docs|clientvpn|sso|boto3|(signin(\\-reg)?))\\.([^\\.]+\\.)?(aws\\.amazon|amazonaws)\\.com','.*captcha-prod\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com','^aws\\.amazon\\.com','^github-production-release-.*\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com','^aws-glue-etl-artifacts\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com','^redshift-maven-repository\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com',rf"^{S3_ASSETS_BUCKET}\.s3(\.[^\.]+)?\.amazonaws\.com",'^localstack-pods-.*\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com','^prod-registry-k8s-io-.*\\.s3\\.(dualstack\\.)?.*\\.amazonaws\\.com','^(?:prod|staging)sharedcertsstack-.*\\.s3(\\.[^\\.]+)?\\.amazonaws\\.com','^d2glxqk2uabbnd\\.cloudfront\\.net'}
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
@hooks.on_infra_start()
def add_custom_domain_names_resolving_to_localstack():
	A=pro_config.DNS_NAMES_RESOLVING_TO_LOCALSTACK
	if not A:return
	LOG.debug('Adding custom DNS names to resolve to LocalStack')
	try:C:list[str]=[A.strip()for A in A.split(',')]
	except Exception as B:LOG.warning("Unable to configure custom DNS names resolving to LocalStack. The string '%s' should be a comma separated list. Error: %s",A,B);return
	from localstack.dns.server import get_dns_server as D,is_server_running as E
	if not E():return
	try:
		F=D()
		for G in C:F.add_host_pointing_to_localstack(G)
	except Exception as B:LOG.warning("Failed to register custom domain names '%s' with DNS server: %s",C,B)