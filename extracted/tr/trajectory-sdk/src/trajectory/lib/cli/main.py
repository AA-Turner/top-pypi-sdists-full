"""Agent-friendly command line entry point."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from trajectory import APIConnectionError, APIStatusError, BenchmarkSpec, Client, omit
from trajectory._exceptions import TrajectoryError
from trajectory.lib._exceptions import FileUploadError
from trajectory.lib.cli import assistants, auth_commands
from trajectory.lib.cli.benchmark_source import BenchmarkSource
from trajectory.lib.cli.cookbook_prompt import EXAMPLES
from trajectory.lib.cli.guides import BundledDocs
from trajectory.lib.cli.presentation import Presenter
from trajectory.lib.cli.project import Project
from trajectory.lib.cli.workflows import WorkflowService

try:
  from trajectory.lib.tui import menus
except ImportError as error:
  if not error.name or error.name.partition(".")[0] not in {"textual", "rich"}:
    raise
  menus = None


class CLIError(ValueError):
  pass


class Parser(argparse.ArgumentParser):
  def error(self, message: str) -> None:
    raise CLIError(message)


class CLI:
  @staticmethod
  def parser() -> Parser:
    parser = Parser(
      prog="tj",
      description="Authenticate, onboard projects, ingest benchmarks, evaluate, and train.",
    )
    parser.add_argument(
      "--json",
      action="store_true",
      help="Machine-readable result on stdout; progress goes to stderr",
    )
    parser.add_argument("--non-interactive", action="store_true", help="Never prompt")
    parser.add_argument("--profile")
    parser.add_argument("--base-url")
    subs = parser.add_subparsers(dest="command", required=True)
    auth_commands.configure_parser(subs)
    init = subs.add_parser(
      "init", help="Sign in if needed and prepare a project; starts no remote runs"
    )
    init.add_argument("--template", choices=Project.choices)
    init.add_argument("--directory", type=Path)
    init.add_argument(
      "--cookbook", choices=EXAMPLES, help="Set up a cookbook example (implies --template cookbook)"
    )
    init.add_argument(
      "--assistant",
      choices=assistants.CHOICES,
      help="Continue setup in a coding assistant, copy its prompt, or proceed manually",
    )
    init.add_argument(
      "--repo", help="Local benchmark directory or repository URL (implies --template benchmark)"
    )
    init.add_argument("--agent-id")
    docs = subs.add_parser("docs", help="Locate bundled integration skill and guides")
    docs.add_argument(
      "--topic", choices=("skill", "onboarding", "capture", "index"), default="onboarding"
    )
    schema = subs.add_parser("schema", help="Machine-readable configuration schemas")
    schema.add_argument(
      "resource",
      choices=("evals", "training", "benchmark", "commands"),
      default="commands",
      nargs="?",
    )
    for kind in ("agents", "benchmarks", "evals", "training", "operations", "diagnostics"):
      resource = subs.add_parser(kind)
      actions = resource.add_subparsers(dest="action", required=True)
      if kind != "diagnostics":
        listing = actions.add_parser("list")
        listing.add_argument("--limit", type=int, default=50)
        listing.add_argument("--cursor")
        listing.add_argument("--agent-id")
        listing.add_argument("--bench-id")
      get = actions.add_parser("get")
      get.add_argument("id")
      if kind in {"evals", "training", "operations", "diagnostics"}:
        watch = actions.add_parser(
          "watch", help="Wait for completion with a bounded deadline; exiting detaches"
        )
        watch.add_argument("id")
        watch.add_argument("--timeout", type=float, default=60)
        watch.add_argument("--poll-interval", type=float, default=2)
      if kind == "agents":
        create = actions.add_parser("create")
        create.add_argument("--name", required=True)
      if kind == "benchmarks":
        readiness = actions.add_parser("readiness")
        readiness.add_argument("id")
        push = actions.add_parser("push")
        push.add_argument("--manifest", type=Path)
        push.add_argument("--agent-id")
        push.add_argument("--request-id")
        diagnose = actions.add_parser(
          "diagnose", help="Start a diagnostic for up to 10 tasks; does not auto-retry"
        )
        diagnose.add_argument("id")
        diagnose.add_argument("--config", type=Path)
        diagnose.add_argument("--dry-run", action="store_true")
      if kind in {"evals", "training"}:
        create = actions.add_parser(
          "create",
          help="Submit once; repeated config reconnects. Use a fresh --request-id for another run.",
        )
        create.add_argument("--config", type=Path, required=True)
        create.add_argument("--request-id")
        create.add_argument("--dry-run", action="store_true")
        for action in ("cancel", "progress", "details"):
          target = actions.add_parser(action)
          target.add_argument("id")
      if kind in {"evals", "training", "diagnostics"}:
        actions.add_parser("models")
        options = actions.add_parser("options")
        options.add_argument("--bench-id", required=True)
        options.add_argument("--base-model-slug")
      if kind == "diagnostics":
        results = actions.add_parser("results")
        results.add_argument("id")
    return parser

  @staticmethod
  def normalize_globals(argv: list[str]) -> list[str]:
    globals_: list[str] = []
    local: list[str] = []
    index = 0
    while index < len(argv):
      word = argv[index]
      if word in {"--json", "--non-interactive"}:
        globals_.append(word)
      elif word in {"--profile", "--base-url"}:
        if index + 1 >= len(argv):
          raise CLIError(f"{word} requires a value")
        globals_.extend(argv[index : index + 2])
        index += 1
      elif word.startswith(("--profile=", "--base-url=")):
        globals_.append(word)
      else:
        local.append(word)
      index += 1
    return globals_ + local

  @staticmethod
  def report(message: str) -> None:
    print(message, file=sys.stderr)

  @staticmethod
  def read_config(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
      raise ValueError("Configuration must be a JSON object")
    return value

  @staticmethod
  def init(args: argparse.Namespace) -> object:
    interactive = (
      not args.non_interactive
      and not args.json
      and sys.stdin.isatty()
      and sys.stdout.isatty()
      and sys.stderr.isatty()
    )
    if args.assistant in assistants.ASSISTANTS and not interactive:
      raise CLIError(
        "Launching an assistant requires an interactive terminal. Use --assistant copy --json to get the setup prompt."
      )
    directory = (args.directory or Path.cwd()).expanduser().resolve()
    if args.repo is not None and (args.cookbook or args.template not in {None, "benchmark"}):
      raise CLIError("--repo cannot be combined with --cookbook or another template")
    source = BenchmarkSource.parse(args.repo) if args.repo is not None else None
    source_directory = source is not None and source.kind == "local" and args.directory is None
    if source_directory:
      directory = Path(source.value)
    previous = Project(directory).load()
    if args.cookbook and args.template not in {None, "cookbook"}:
      raise CLIError("--cookbook requires --template cookbook or no explicit template")
    template = args.template or (
      "benchmark" if source else "cookbook" if args.cookbook else previous.get("template")
    )
    show_choices = interactive and not any(
      (args.template, args.repo, args.cookbook, args.assistant)
    )
    organization_key = None
    if interactive:
      if (
        menus is None
        and template != "skip"
        and (template is None or show_choices or args.assistant is None)
      ):
        raise ModuleNotFoundError("Interactive setup requires textual", name="textual")
      identity = auth_commands.AuthCommands(
        args.base_url, args.profile, CLI.report
      ).ensure_authenticated()
      organization_key = (
        identity["organization"]["key"]
        if "organization" in identity
        else identity.get("organization_key")
      )
    resume_setup = True
    while True:
      if template is None or show_choices:
        if not interactive:
          raise CLIError(
            "Choose --template benchmark|connect|cookbook|example|skip for non-interactive setup"
          )
        if menus is None:
          raise ModuleNotFoundError("Interactive setup requires textual", name="textual")
        choices = [
          ("Try an open-source benchmark", "cookbook"),
          ("Bring your own benchmark", "benchmark"),
        ]
        if previous.get("template"):
          label = previous.get("cookbook") or previous.get("repo") or previous["template"]
          choices.insert(0, (f"Resume saved setup ({label})", "resume"))
        choice = menus.choose("What would you like to do?", choices)
        if choice is None or choice == menus.EXIT:
          return {"cancelled": True}
        resume_setup = choice == "resume"
        template = previous["template"] if resume_setup else choice
        if choice == "benchmark":
          template = menus.choose(
            "Where is your benchmark?",
            [
              (f"Use current directory ({directory})", "current"),
              ("Choose another local directory", "local"),
              ("Use a repository URL", "repository"),
            ],
          )
          if template == menus.EXIT:
            return {"cancelled": True}
          if template is None:
            continue
          if template == "current":
            template = "benchmark"
            source_directory = True
      if template in {"local", "repository"}:
        if template == "local":
          selected = menus.choose_directory(directory, "Where is the benchmark repository?")
          source = BenchmarkSource.parse(str(selected)) if selected is not None else None
          if source and args.directory is None:
            directory = Path(source.value)
            source_directory = True
            previous = Project(directory).load()
        else:
          selected = menus.RepositoryApp.prompt()
          source = BenchmarkSource.parse(selected) if selected is not None else None
        if source is None:
          return {"cancelled": True}
        template = "benchmark"
      if (
        resume_setup
        and template == "benchmark"
        and source is None
        and previous.get("repo") is not None
      ):
        source = BenchmarkSource.parse(previous["repo"])
        source_directory = source.kind == "local" and directory == Path(source.value)
      if template == "skip":
        return Project(directory).initialize(template, args.agent_id)
      cookbook = args.cookbook or (
        previous.get("cookbook") if resume_setup and template == "cookbook" else None
      )
      if template == "cookbook" and cookbook is None:
        if not interactive:
          raise CLIError("Choose --cookbook " + "|".join(EXAMPLES) + " for non-interactive setup")
        if menus is None:
          raise ModuleNotFoundError("Interactive setup requires textual", name="textual")
        cookbook = menus.choose(
          "Which cookbook example?",
          [(f"{example.name}: {example.description}", key) for key, example in EXAMPLES.items()],
        )
        if cookbook == menus.EXIT:
          return {"cancelled": True}
        if cookbook is None:
          template = None
          continue
      break
    assistant = args.assistant
    if assistant is None and interactive:
      if menus is None:
        raise ModuleNotFoundError("Interactive setup requires textual", name="textual")
      assistant = menus.choose("Continue setup with…", assistants.assistant_choices())
      if assistant is None or assistant == menus.EXIT:
        return {"cancelled": True}
    if assistant in assistants.ASSISTANTS and args.directory is None and not source_directory:
      if menus is None:
        raise ModuleNotFoundError("Interactive setup requires textual", name="textual")
      selected = menus.choose_directory(directory)
      if selected is None:
        return {"cancelled": True}
      directory = selected.expanduser().resolve()
      if resume_setup and not any((args.template, args.repo, args.cookbook)):
        selected_setup = Project(directory).load()
        if selected_setup:
          template = selected_setup.get("template", template)
          cookbook = selected_setup.get("cookbook") if template == "cookbook" else None
          repo = selected_setup.get("repo") if template == "benchmark" else None
          source = BenchmarkSource.parse(repo) if repo is not None else None
    result = Project(directory).initialize(
      template, args.agent_id, cookbook, source.value if source else None, resume_repo=resume_setup
    )
    if assistant and assistant != "manual":
      if assistant in assistants.ASSISTANTS:
        CLI.report(f"Opening {assistants.ASSISTANTS[assistant][0]} in {directory}…")
      result["assistant"] = assistants.handoff(
        assistant,
        directory,
        template,
        CLI.docs("skill")["content"],
        args.profile,
        args.base_url,
        interactive,
        cookbook,
        result.get("repo"),
        organization_key,
      )
    return result

  @staticmethod
  def docs(topic: str) -> object:
    relative = {
      "skill": "skills/trajectory/SKILL.md",
      "index": "introduction.mdx",
      "capture": "guides/production-traces.mdx",
      "onboarding": "guides/cli.mdx",
    }[topic]
    resource = BundledDocs.path(relative)
    return {
      "path": str(resource),
      "directory": str(BundledDocs.path("introduction.mdx").parent),
      "content": resource.read_text(),
    }

  @staticmethod
  def execute(args: argparse.Namespace) -> object:
    if args.command in {"login", "logout", "whoami", "profiles"}:
      result = auth_commands.run(args, report=CLI.report)
      if (
        args.command == "login"
        and not result.get("already_authenticated", False)
        and not args.non_interactive
        and not args.json
        and sys.stdin.isatty()
        and sys.stdout.isatty()
        and sys.stderr.isatty()
      ):
        try:
          if menus is None:
            raise ModuleNotFoundError("Interactive setup requires textual", name="textual")
          if (
            menus.choose(
              "Authentication saved. What next?",
              [("Set up a project", "setup"), ("Set up later", "skip")],
            )
            == "setup"
          ):
            result["setup"] = CLI.init(
              argparse.Namespace(
                template=None,
                directory=None,
                assistant=None,
                cookbook=None,
                repo=None,
                profile=result["profile"],
                base_url=result.get("base_url", args.base_url),
                agent_id=None,
                non_interactive=False,
                json=False,
              )
            )
        except ModuleNotFoundError:
          CLI.report(
            "Login succeeded. Install trajectory-sdk[tui] for interactive setup, or use tj init --template."
          )
        except auth_commands.AuthError as error:
          CLI.report(
            f"Login succeeded. Project setup stopped: {error} Run tj init to resume project setup."
          )
        except (ValueError, OSError, EOFError, KeyboardInterrupt):
          CLI.report("Login succeeded. Run tj init to resume project setup.")
      return result
    if args.command == "init":
      return CLI.init(args)
    if args.command == "docs":
      return CLI.docs(args.topic)
    if args.command == "schema":
      if args.resource in {"evals", "training"}:
        return WorkflowService.run_schema(args.resource)
      if args.resource == "benchmark":
        return BenchmarkSpec.model_json_schema()
      return {
        "commands": [
          "login",
          "logout",
          "whoami",
          "profiles",
          "init",
          "docs",
          "schema",
          "agents",
          "benchmarks",
          "evals",
          "training",
          "operations",
          "diagnostics",
        ],
        "run_config": "tj schema evals|training",
        "output": "--json",
        "exit_codes": {
          "0": "success",
          "1": "API or local error",
          "2": "invalid input",
          "3": "authentication required",
          "4": "wait timed out",
          "130": "interrupted",
        },
      }
    if args.command in {"evals", "training"} and args.action == "create" and args.dry_run:
      return {
        "valid": True,
        "config": WorkflowService.validate_run(args.command, CLI.read_config(args.config)),
        "submitted": False,
      }
    if args.command == "benchmarks" and args.action == "diagnose" and args.dry_run:
      config = CLI.read_config(args.config) if args.config else {}
      return {
        "valid": True,
        "config": WorkflowService.validate_diagnostic(config),
        "submitted": False,
      }
    with Client(base_url=args.base_url, profile=args.profile) as client:
      if not client.api_key:
        raise auth_commands.AuthError(
          "not_authenticated", "Run tj login or set TRAJECTORY_API_KEY."
        )
      service = WorkflowService(client, report=CLI.report)
      if args.action == "list":
        return service.list_resources(
          args.command, args.agent_id, args.limit, args.bench_id, args.cursor
        )
      if args.action == "get":
        return service.get_resource(args.command, args.id)
      if args.action == "watch":
        return service.watch(args.command, args.id, args.timeout, args.poll_interval)
      if args.action == "create":
        if args.command == "agents":
          return client.agents.create(name=args.name)
        return service.create_run(args.command, CLI.read_config(args.config), args.request_id)
      if args.action == "push":
        project = Project(Path.cwd()).load()
        manifest = args.manifest or project.get("manifest")
        agent_id = args.agent_id or project.get("agent_id")
        if not manifest or not agent_id:
          raise CLIError(
            "Provide --manifest and --agent-id, or set manifest and agent_id in trajectory.toml"
          )
        return service.push_benchmark(Path(manifest), agent_id, args.request_id)
      if args.action == "diagnose":
        return service.diagnose(args.id, CLI.read_config(args.config) if args.config else {})
      if args.action == "readiness":
        return client.benchmarks.retrieve_readiness(args.id)
      if args.action == "results":
        return client.diagnostics.get_diagnostics(args.id)
      if args.action == "cancel":
        return service.cancel_run(args.command, args.id)
      if args.action == "progress":
        return service.progress(args.command, args.id)
      if args.action == "details":
        return service.run_details(args.command, args.id)
      if args.action == "models":
        return getattr(
          client, "evals" if args.command == "diagnostics" else args.command
        ).list_models()
      if args.action == "options":
        if args.command == "diagnostics":
          return service.diagnostic_options(args.bench_id, args.base_model_slug)
        return getattr(client, args.command).list_options(
          bench_id=args.bench_id, base_model_slug=args.base_model_slug or omit
        )
    raise CLIError("Unsupported command")

  @staticmethod
  def run(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    json_output = "--json" in argv
    try:
      args = CLI.parser().parse_args(CLI.normalize_globals(argv))
      result = WorkflowService.serialize(CLI.execute(args))
      print(
        json.dumps(result, ensure_ascii=False)
        if args.json
        else Presenter.render(args.command, result)
      )
      if args.command == "init" and result.get("assistant", {}).get("exit_code"):
        return result["assistant"]["exit_code"]
      if (
        getattr(args, "action", None) == "watch"
        and isinstance(result, dict)
        and result.get("status") in {"failed", "cancelled", "partial_failure"}
      ):
        return 1
      return 0
    except KeyboardInterrupt:
      code, name, message = (
        130,
        "interrupted",
        "Detached; remote operations continue. Reconnect with get or watch.",
      )
    except TimeoutError as error:
      code, name, message = 4, "wait_timeout", str(error)
    except APIStatusError as error:
      code = 3 if error.status_code in {401, 403} else 1
      name, message = "api_error", WorkflowService.error_message(error)
      if error.status_code == 409 and args.command == "diagnostics" and args.action == "results":
        name = "results_not_ready"
        message = (
          f"Diagnostic results are not ready. Run tj diagnostics watch {args.id} "
          f"--timeout 300, then tj diagnostics results {args.id}."
        )
    except APIConnectionError:
      code, name, message = (
        1,
        "connection_error",
        "Could not reach the API. Retry the same submission config to preserve its request ID.",
      )
    except FileUploadError:
      code, name, message = (
        1,
        "upload_failed",
        "Benchmark upload failed. Retry the same manifest to preserve its request ID; inspect local files and connectivity.",
      )
    except TrajectoryError:
      code, name, message = (
        1,
        "sdk_error",
        "The SDK could not process the API response. Retry the same submission to preserve its request ID; check SDK/API compatibility.",
      )
    except ValidationError as error:
      locations = [".".join(map(str, item["loc"])) for item in error.errors(include_input=False)]
      code, name, message = (
        2,
        "invalid_config",
        f"Invalid configuration fields: {', '.join(locations)}",
      )
    except (CLIError, ValueError, TypeError) as error:
      code, name, message = 2, "invalid_input", str(error)
    except (OSError, EOFError) as error:
      code, name, message = 1, "local_error", str(error)
    except ModuleNotFoundError as error:
      code, name, message = (
        1,
        "missing_dependency",
        f"Install interactive setup support with: uv tool install 'trajectory-sdk[tui]' ({error.name})",
      )
    except auth_commands.AuthError as error:
      code, name, message = 3, error.code, str(error)
    value = {"error": {"code": name, "message": message}}
    print(
      json.dumps(value) if json_output else f"{name}: {message}",
      file=sys.stdout if json_output else sys.stderr,
    )
    return code


def main() -> None:
  raise SystemExit(CLI.run())


if __name__ == "__main__":
  main()
