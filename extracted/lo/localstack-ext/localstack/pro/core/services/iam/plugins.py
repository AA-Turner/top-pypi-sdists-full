import logging
from typing import Any
from localstack.aws.chain import CompositeHandler
from localstack.http import Router
from localstack.http.dispatcher import Handler as RouteHandler
from localstack.pro.core import config as pro_config
from localstack.pro.core.runtime.plugin import ProPlatformPlugin
from localstack.runtime import hooks
LOG=logging.getLogger(__name__)
class IamEnforcementPlugin(ProPlatformPlugin):
	name='iam-enforcement'
	def on_service_load(B,service:str,provider:Any):
		if service!='iam':return
		from localstack.pro.core.services.iam.policy_engine.policy_simulator import AdvanceIAMPolicySimulator as A;provider.policy_simulator=A();LOG.info('Configured IAM provider to use Advance Policy Simulator')
	def update_request_handlers(B,handlers:CompositeHandler):from localstack.pro.core.services.iam.policy_engine.handler import IamEnforcementHandler as A;handlers.append(A.get())
	def update_gateway_routes(B,router:Router[RouteHandler]):from localstack.pro.core.services.iam.router import IAMEnforcementRouter as A;A(router).register_routes()
class IamStreamPlugin(ProPlatformPlugin):
	name='iam-stream'
	def update_gateway_routes(B,router:Router[RouteHandler]):from localstack.pro.core.services.iam.router import IAMStreamRouter as A;A(router).register_routes()
	def on_platform_shutdown(B):from localstack.pro.core.services.iam.policy_generation.policy_generator import PolicyGenerator as A;A.get().shutdown()
WANTED_ENFORCE_IAM=pro_config.ENFORCE_IAM
@hooks.on_infra_start(should_load=pro_config.ACTIVATE_PRO and WANTED_ENFORCE_IAM,priority=20)
def _disable_iam_during_startup():pro_config.ENFORCE_IAM=False
@hooks.on_infra_ready(should_load=pro_config.ACTIVATE_PRO and WANTED_ENFORCE_IAM,priority=-20)
def _enable_iam_after_ready():pro_config.ENFORCE_IAM=True