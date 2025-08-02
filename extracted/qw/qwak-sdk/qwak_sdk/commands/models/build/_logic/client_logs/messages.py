BUILD_LOGS_URL = (
    "{base_url}/models/{model_id}/build/{build_id}"
)

SUCCESS_MSG_REMOTE = """
Build ID \033[4m{build_id}\033[0m triggered remotely

########### Follow build logs in the CLI
qwak models builds logs -b {build_id} --follow

########### Follow build logs in the platform
{base_url}/models/{model_id}/build/{build_id}
"""

SUCCESS_MSG_REMOTE_WITH_DEPLOY = """
Build ID \033[4m{build_id}\033[0m finished successfully and deployed

########### View the model using platform
{base_url}/models/{model_id}
"""

FAILED_CONTACT_QWAK_SUPPORT = """
Build ID \033[4m{build_id}\033[0m failed!!
You can share the logs from \033[4m{log_file}.zip\033[0m with the support team.
"""

FAILED_REMOTE_BUILD_SUGGESTION = """
Your build failed. Check the failure reason in the platform:
{base_url}/models/{model_id}/build/{build_id}
"""

FAILED_DEPLOY_BUILD_SUGGESTION = """
Deploying the build failed. Check the failure reason in the platform:
{base_url}/models/{model_id}?tabId=1
Try and redeploy this build either from the platform or the CLI
"""
