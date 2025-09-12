from localstack.pro.core import config as pro_config
from localstack.pro.core.bootstrap.licensingv2 import LicensedPluginLoaderGuard
from localstack.runtime import hooks
from werkzeug.routing import Rule
_ROUTER_RULES_LAMBDA_DEBUG_MODE_ENDPOINT=[]
@hooks.on_infra_start()
def enable_lambda_executor_licensing():from localstack.services.lambda_.invocation.runtime_executor import EXECUTOR_PLUGIN_MANAGER as A;A.add_listener(LicensedPluginLoaderGuard())
@hooks.on_infra_start(should_load=pro_config.ACTIVATE_PRO and pro_config.LDM_PREVIEW)
def register_lambda_debug_mode_endpoints():from localstack.pro.core.services.lambda_.lambda_debug_mode.endpoint import LambdaDebugModeEndpoints as A;from localstack.services.edge import ROUTER as B;global _ROUTER_RULES_LAMBDA_DEBUG_MODE_ENDPOINT;_ROUTER_RULES_LAMBDA_DEBUG_MODE_ENDPOINT=B.add(A())
@hooks.on_infra_shutdown()
def remove_lambda_debug_mode_endpoints():from localstack.services.edge import ROUTER as A;A.remove(_ROUTER_RULES_LAMBDA_DEBUG_MODE_ENDPOINT)