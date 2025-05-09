from localstack.pro.core.services.appsync.event_api.handlers.authorize import AuthorizerHandler
from localstack.pro.core.services.appsync.event_api.handlers.code_execute import CodeExecuteHandler
from localstack.pro.core.services.appsync.event_api.handlers.publish import PublishHandler

authorize_handler = AuthorizerHandler()
code_execute_handler = CodeExecuteHandler()
publish_handler = PublishHandler()
