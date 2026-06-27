from typing import cast

from abstra_internals.controllers import language_server as language_server_controller
from abstra_internals.controllers.docs import DocsController
from abstra_internals.controllers.git import EmailProvider, GitController
from abstra_internals.controllers.main import MainController
from abstra_internals.controllers.tasks import TasksController
from abstra_internals.controllers.workflows import WorkflowController
from abstra_internals.environment import EDITOR_MODE
from abstra_internals.utils.mcp import requires_approval
from abstra_internals.utils.mcp_bp import mcp_bp


def get_editor_bp(main_controller: MainController):
    tasks_controller = TasksController(main_controller.repositories)
    workflow_controller = WorkflowController(main_controller.repositories)
    docs_controller = DocsController(main_controller.repositories)
    git_controller = (
        GitController(email_provider=cast(EmailProvider, main_controller))
        if EDITOR_MODE == "local"
        else GitController()
    )

    return mcp_bp(
        [
            docs_controller.read_abstra_docs,
            docs_controller.get_stage_guide,
            docs_controller.list_all_modules_in_abstra_lib,
            docs_controller.list_objects_in_abstra_module,
            docs_controller.describe_class,
            docs_controller.describe_function,
            main_controller.list_directory,
            main_controller.find_files_by_pattern,
            main_controller.grep_codebase,
            main_controller.search_file_with_context,
            language_server_controller.analyze_python_syntax_file,
            main_controller.list_linter_issues,
            main_controller.read_file_with_pagination,
            main_controller.read_document,
            main_controller.read_stage_file_with_pagination,
            main_controller.list_all_stages,
            main_controller.get_stage,
            main_controller.create_stage,
            requires_approval(main_controller.update_stage),
            requires_approval(main_controller.delete_stage),
            main_controller.get_workspace,
            requires_approval(main_controller.update_workspace),
            workflow_controller.get_workflow_settings,
            workflow_controller.add_transition,
            requires_approval(workflow_controller.delete_transition),
            main_controller.list_access_controls,
            requires_approval(main_controller.update_access_control),
            main_controller.list_executions,
            main_controller.get_execution_logs,
            main_controller.get_execution_tasks,
            requires_approval(main_controller.stop_execution),
            requires_approval(main_controller.run_job),
            requires_approval(main_controller.run_tasklet),
            requires_approval(main_controller.run_hook),
            requires_approval(main_controller.run_page),
            tasks_controller.list_tasks,
            tasks_controller.create_task,
            tasks_controller.update_task_status,
            requires_approval(tasks_controller.clear_tasks),
            requires_approval(main_controller.browser_open_page),
            requires_approval(main_controller.browser_navigate),
            main_controller.browser_list_tabs,
            main_controller.browser_close,
            main_controller.browser_get_page_summary,
            main_controller.browser_get_text,
            main_controller.browser_get_html,
            main_controller.browser_get_console_logs,
            main_controller.browser_get_network_requests,
            requires_approval(main_controller.browser_click),
            requires_approval(main_controller.browser_fill),
            requires_approval(main_controller.browser_execute_javascript),
            main_controller.browser_wait,
            requires_approval(main_controller.execute_code_snippet),
            requires_approval(main_controller.add_and_install_requirement),
            requires_approval(main_controller.linter_repository.fix_issue_in_codebase),
            git_controller.get_status,
            git_controller.get_commit_history,
            git_controller.commit_changes,
            requires_approval(git_controller.revert_commit),
        ]
    )
