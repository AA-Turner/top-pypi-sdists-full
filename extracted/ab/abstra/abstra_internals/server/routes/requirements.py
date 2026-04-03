import flask

from abstra_internals.controllers.linter_events import LinterEventController
from abstra_internals.controllers.main import MainController
from abstra_internals.repositories.linter.rules import run_after_package_install
from abstra_internals.services.requirements import (
    RequirementsRepository,
    create_requirement,
    uninstall_requirement,
)
from abstra_internals.usage import editor_usage


def _with_post_install_linters(streamer, controller: MainController):
    yield from streamer
    checks = controller.linter_repository.update_specific_checks(
        run_after_package_install
    )
    LinterEventController.broadcast(checks)


def get_editor_bp(controller: MainController):
    bp = flask.Blueprint("editor_requirements", __name__)

    @bp.get("/")
    def _get_requirements():
        return RequirementsRepository.load().to_dict()

    @bp.post("/")
    @editor_usage
    def _create_requirement():
        data = flask.request.json

        if not data:
            flask.abort(400)

        name = data["name"]
        version = data.get("version")

        requirements = RequirementsRepository.load()
        requirements.add(name, version)
        RequirementsRepository.save(requirements)
        return requirements.to_dict()

    @bp.post("/install")
    def _install_requirements():
        requirements = RequirementsRepository.load()
        streamer = requirements.install()
        if streamer is None:
            flask.abort(403)

        return flask.Response(
            _with_post_install_linters(streamer, controller),
            mimetype="text/event-stream",
        )

    @bp.post("/<name>/uninstall")
    def _uninstall_requirement(name: str):
        req = create_requirement(name)
        streamer = uninstall_requirement(req)
        if streamer is None:
            flask.abort(403)
        reqs = RequirementsRepository.load()
        reqs.delete(name)
        RequirementsRepository.save(reqs)
        return flask.Response(
            _with_post_install_linters(streamer, controller),
            mimetype="text/event-stream",
        )

    @bp.delete("/<name>")
    @editor_usage
    def _delete_requirement(name: str):
        requirements = RequirementsRepository.load()
        requirements.delete(name)
        RequirementsRepository.save(requirements)
        return requirements.to_dict()

    @bp.get("/recommendations")
    def _get_requirements_recommendation():
        return [r.to_dict() for r in RequirementsRepository.get_recommendation()]

    return bp
