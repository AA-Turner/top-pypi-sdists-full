import flask

from abstra_internals.contracts_generated import (
    AbstraLibApiEditorDeployPostRequest,
    AbstraLibApiEditorDeployPostResponse,
)
from abstra_internals.controllers.git import GitController
from abstra_internals.controllers.main import MainController
from abstra_internals.interface.cli.deploy_messages import DeployMessages
from abstra_internals.usage import editor_usage


def get_editor_bp(main_controller: MainController):
    bp = flask.Blueprint("editor_deploy", __name__)
    git_controller = GitController()

    @bp.post("/")
    @editor_usage
    def _deploy():
        data = flask.request.json or {}
        req = AbstraLibApiEditorDeployPostRequest.from_dict(data)

        if req.strategy == "direct":
            try:
                main_controller.deploy_without_git()
                return AbstraLibApiEditorDeployPostResponse(success=True).to_dict()
            except Exception as e:
                return (
                    AbstraLibApiEditorDeployPostResponse(
                        success=False, message=str(e)
                    ).to_dict(),
                    400,
                )

        elif req.strategy == "git":
            try:
                DeployMessages.start(method="git")
                DeployMessages.checking_linters()

                issues = (
                    main_controller.linter_repository.get_blocking_checks_for_deploy()
                )

                if len(issues) > 0:
                    DeployMessages.error(
                        "Please fix all linter issues before deploying your project."
                    )
                    return (
                        AbstraLibApiEditorDeployPostResponse(
                            success=False,
                            message="Please fix all linter issues before deploying your project.",
                        ).to_dict(),
                        400,
                    )

                branch = req.branch or "main"
                result = git_controller.push_and_deploy(
                    branch, show_start_message=False
                )
                status_code = 200 if result["success"] else 400
                return (
                    AbstraLibApiEditorDeployPostResponse(
                        success=result["success"], message=result.get("message")
                    ).to_dict(),
                    status_code,
                )

            except Exception as e:
                DeployMessages.error(str(e))
                return (
                    AbstraLibApiEditorDeployPostResponse(
                        success=False, message=str(e)
                    ).to_dict(),
                    500,
                )

        else:
            return (
                AbstraLibApiEditorDeployPostResponse(
                    success=False, message=f"Unknown strategy: {req.strategy}"
                ).to_dict(),
                400,
            )

    return bp
