import ast
import importlib
import sys
from pathlib import Path

from django.test import SimpleTestCase

BASE_DIR = Path(__file__).resolve().parents[1]


# This inventory is the contract for signal modules that must be loaded by
# AppConfig.ready() during Django startup. If a new receiver is added to one of
# these files, this inventory must be updated and the receiver must be covered
# by a focused test in that app.
SIGNAL_INVENTORY = {
    "allianceauth.authentication.signals": {
        "file": "authentication/signals.py",
        "ready_file": "authentication/apps.py",
        "receivers": [
            {
                "name": "state_member_characters_changed",
                "signal": "django.db.models.signals.m2m_changed",
                "sender": "allianceauth.authentication.models.State.member_characters.through",
            },
            {
                "name": "state_member_corporations_changed",
                "signal": "django.db.models.signals.m2m_changed",
                "sender": "allianceauth.authentication.models.State.member_corporations.through",
            },
            {
                "name": "state_member_alliances_changed",
                "signal": "django.db.models.signals.m2m_changed",
                "sender": "allianceauth.authentication.models.State.member_alliances.through",
            },
            {
                "name": "state_member_factions_changed",
                "signal": "django.db.models.signals.m2m_changed",
                "sender": "allianceauth.authentication.models.State.member_factions.through",
            },
            {
                "name": "state_saved",
                "signal": "django.db.models.signals.post_save",
                "sender": "allianceauth.authentication.models.State",
            },
            {
                "name": "reassess_on_profile_save",
                "signal": "django.db.models.signals.post_save",
                "sender": "allianceauth.authentication.models.UserProfile",
            },
            {
                "name": "create_required_models",
                "signal": "django.db.models.signals.post_save",
                "sender": "django.contrib.auth.models.User",
            },
            {
                "name": "record_character_ownership",
                "signal": "django.db.models.signals.post_save",
                "sender": "esi.models.Token",
            },
            {
                "name": "validate_main_character",
                "signal": "django.db.models.signals.pre_delete",
                "sender": "allianceauth.authentication.models.CharacterOwnership",
            },
            {
                "name": "validate_ownership",
                "signal": "django.db.models.signals.post_delete",
                "sender": "esi.models.Token",
            },
            {
                "name": "assign_state_on_active_change",
                "signal": "django.db.models.signals.pre_save",
                "sender": "django.contrib.auth.models.User",
            },
            {
                "name": "check_state_on_character_update",
                "signal": "django.db.models.signals.post_save",
                "sender": "allianceauth.eveonline.models.EveCharacter",
            },
            {
                "name": "ownership_record_creation",
                "signal": "django.db.models.signals.post_save",
                "sender": "allianceauth.authentication.models.CharacterOwnership",
            },
        ],
    },
    "allianceauth.authentication.task_statistics.signals": {
        "file": "authentication/task_statistics/signals.py",
        "ready_file": "authentication/apps.py",
        "receivers": [
            {
                "name": "reset_counters_when_celery_restarted",
                "signal": "celery.signals.worker_ready",
                "sender": None,
            },
            {
                "name": "record_task_succeeded",
                "signal": "celery.signals.task_success",
                "sender": None,
            },
            {
                "name": "record_task_retried",
                "signal": "celery.signals.task_retry",
                "sender": None,
            },
            {
                "name": "record_task_failed",
                "signal": "celery.signals.task_failure",
                "sender": None,
            },
            {
                "name": "record_task_internal_error",
                "signal": "celery.signals.task_internal_error",
                "sender": None,
            },
        ],
    },
    "allianceauth.groupmanagement.signals": {
        "file": "groupmanagement/signals.py",
        "ready_file": "groupmanagement/apps.py",
        "receivers": [
            {
                "name": "find_new_name_for_conflicting_groups",
                "signal": "django.db.models.signals.pre_save",
                "sender": "django.contrib.auth.models.Group",
            },
            {
                "name": "create_auth_group",
                "signal": "django.db.models.signals.post_save",
                "sender": "django.contrib.auth.models.Group",
            },
            {
                "name": "check_groups_on_state_change",
                "signal": "allianceauth.authentication.signals.state_changed",
                "sender": None,
            },
        ],
    },
    "allianceauth.services.signals": {
        "file": "services/signals.py",
        "ready_file": "services/apps.py",
        "receivers": [
            {
                "name": "m2m_changed_user_groups",
                "signal": "django.db.models.signals.m2m_changed",
                "sender": "django.contrib.auth.models.User.groups.through",
            },
            {
                "name": "m2m_changed_user_permissions",
                "signal": "django.db.models.signals.m2m_changed",
                "sender": "django.contrib.auth.models.User.user_permissions.through",
            },
            {
                "name": "m2m_changed_group_permissions",
                "signal": "django.db.models.signals.m2m_changed",
                "sender": "django.contrib.auth.models.Group.permissions.through",
            },
            {
                "name": "m2m_changed_state_permissions",
                "signal": "django.db.models.signals.m2m_changed",
                "sender": "allianceauth.authentication.models.State.permissions.through",
            },
            {
                "name": "check_service_accounts_state_changed",
                "signal": "allianceauth.authentication.signals.state_changed",
                "sender": None,
            },
            {
                "name": "pre_delete_user",
                "signal": "django.db.models.signals.pre_delete",
                "sender": "django.contrib.auth.models.User",
            },
            {
                "name": "disable_services_on_inactive",
                "signal": "django.db.models.signals.pre_save",
                "sender": "django.contrib.auth.models.User",
            },
            {
                "name": "process_main_character_change",
                "signal": "django.db.models.signals.pre_save",
                "sender": "allianceauth.authentication.models.UserProfile",
            },
            {
                "name": "process_main_character_update",
                "signal": "django.db.models.signals.pre_save",
                "sender": "allianceauth.eveonline.models.EveCharacter",
            },
        ],
    },
    "allianceauth.services.modules.teamspeak3.signals": {
        "file": "services/modules/teamspeak3/signals.py",
        "ready_file": "services/modules/teamspeak3/apps.py",
        "receivers": [
            {
                "name": "m2m_changed_authts_group",
                "signal": "django.db.models.signals.m2m_changed",
                "sender": "allianceauth.services.modules.teamspeak3.models.AuthTS.ts_group.through",
            },
            {
                "name": "post_save_authts",
                "signal": "django.db.models.signals.post_save",
                "sender": "allianceauth.services.modules.teamspeak3.models.AuthTS",
            },
            {
                "name": "post_save_authts",
                "signal": "django.db.models.signals.post_save",
                "sender": "allianceauth.services.modules.teamspeak3.models.StateGroup",
            },
            {
                "name": "post_delete_authts",
                "signal": "django.db.models.signals.post_delete",
                "sender": "allianceauth.services.modules.teamspeak3.models.AuthTS",
            },
            {
                "name": "post_delete_authts",
                "signal": "django.db.models.signals.post_delete",
                "sender": "allianceauth.services.modules.teamspeak3.models.StateGroup",
            },
            {
                "name": "check_groups_on_state_change",
                "signal": "allianceauth.authentication.signals.state_changed",
                "sender": None,
            },
        ],
    },
    "allianceauth.eveonline.autogroups.signals": {
        "file": "eveonline/autogroups/signals.py",
        "ready_file": "eveonline/autogroups/apps.py",
        "receivers": [
            {
                "name": "pre_save_config",
                "signal": "django.db.models.signals.pre_save",
                "sender": "allianceauth.eveonline.autogroups.models.AutogroupsConfig",
            },
            {
                "name": "pre_delete_config",
                "signal": "django.db.models.signals.pre_delete",
                "sender": "allianceauth.eveonline.autogroups.models.AutogroupsConfig",
            },
            {
                "name": "check_groups_on_profile_update",
                "signal": "django.db.models.signals.post_save",
                "sender": "allianceauth.authentication.models.UserProfile",
            },
            {
                "name": "autogroups_states_changed",
                "signal": "django.db.models.signals.m2m_changed",
                "sender": "allianceauth.eveonline.autogroups.models.AutogroupsConfig.states.through",
            },
            {
                "name": "check_groups_on_character_update",
                "signal": "django.db.models.signals.post_save",
                "sender": "allianceauth.eveonline.models.EveCharacter",
            },
        ],
    },
}

# Signal modules that intentionally do not participate in the AppConfig.ready()
# startup-loading contract. New entries should be rare and justified.
NOT_TESTED_SIGNAL_MODULES = set()


class TestSignalInventory(SimpleTestCase):
    maxDiff = None

    def test_all_signal_modules_are_classified(self):
        # Welcome to the Twilight Zone
        # You created some signals but haven't defined them above.
        # Please do so <3
        discovered_modules = self._find_signal_modules()
        classified_modules = set(SIGNAL_INVENTORY) | NOT_TESTED_SIGNAL_MODULES
        self.assertSetEqual(discovered_modules, classified_modules)

    def test_inventory_matches_decorated_receivers_in_source(self):
        for module_name, config in SIGNAL_INVENTORY.items():
            with self.subTest(module=module_name):
                actual_receivers = self._find_receiver_names(BASE_DIR / config["file"])
                documented_receivers = {entry["name"] for entry in config["receivers"]}
                self.assertSetEqual(actual_receivers, documented_receivers)

    def test_signal_modules_are_loaded_during_startup(self):
        for module_name in SIGNAL_INVENTORY:
            with self.subTest(module=module_name):
                self.assertIn(
                    module_name,
                    sys.modules,
                    msg=(
                        f"{module_name} was not loaded during Django startup. "
                        "If this module is expected to auto-register signals, "
                        "import it from the owning AppConfig.ready()."
                    ),
                )

    def test_signal_modules_are_imported_in_owning_ready_function(self):
        for module_name, config in SIGNAL_INVENTORY.items():
            with self.subTest(module=module_name):
                ready_imports = self._find_ready_imports(BASE_DIR / config["ready_file"])
                self.assertIn(
                    module_name,
                    ready_imports,
                    msg=(
                        f"{module_name} is not imported in "
                        f"{config['ready_file']}::ready(). "
                        "Signal modules must be explicitly imported by their owning "
                        "AppConfig.ready() so registration failures are caught early."
                    ),
                )

    def test_documented_receivers_are_registered(self):
        for module_name, config in SIGNAL_INVENTORY.items():
            module = sys.modules[module_name]
            for entry in config["receivers"]:
                with self.subTest(module=module_name, receiver=entry["name"]):
                    receiver = getattr(module, entry["name"])
                    signal = self._resolve_dotted_path(
                        entry["signal"], require_project_module_loaded=True
                    )
                    sender = None
                    if entry["sender"]:
                        sender = self._resolve_dotted_path(entry["sender"])
                    self.assertIn(receiver, self._live_receivers(signal, sender))

    @staticmethod
    def _find_receiver_names(file_path: Path) -> set[str]:
        tree = ast.parse(file_path.read_text())
        names = set()
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and getattr(decorator.func, "id", None) == "receiver":
                    names.add(node.name)
                    break
                if isinstance(decorator, ast.Attribute) and decorator.attr == "connect":
                    names.add(node.name)
                    break
        return names

    @staticmethod
    def _find_ready_imports(file_path: Path) -> set[str]:
        tree = ast.parse(file_path.read_text())
        imports = set()
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            for class_node in node.body:
                if not isinstance(class_node, ast.FunctionDef) or class_node.name != "ready":
                    continue
                for statement in class_node.body:
                    if isinstance(statement, ast.Import):
                        for alias in statement.names:
                            imports.add(alias.name)
                    elif isinstance(statement, ast.ImportFrom):
                        if statement.module is None:
                            continue
                        for alias in statement.names:
                            imports.add(f"{statement.module}.{alias.name}")
        return imports

    @staticmethod
    def _find_signal_modules() -> set[str]:
        modules = set()
        for file_path in BASE_DIR.rglob("signals.py"):
            relative_path = file_path.relative_to(BASE_DIR)
            module_name = ".".join(("allianceauth",) + relative_path.with_suffix("").parts)
            modules.add(module_name)
        return modules

    def _resolve_dotted_path(
        self, dotted_path: str, require_project_module_loaded: bool = False
    ):
        parts = dotted_path.split(".")
        for index in range(len(parts), 0, -1):
            module_name = ".".join(parts[:index])
            module = sys.modules.get(module_name)
            if module is None:
                if require_project_module_loaded and module_name.startswith("allianceauth."):
                    continue
                try:
                    module = importlib.import_module(module_name)
                except ModuleNotFoundError:
                    continue
            value = module
            for attr in parts[index:]:
                value = getattr(value, attr)
            return value
        self.fail(f"Could not resolve dotted path: {dotted_path}")

    @staticmethod
    def _live_receivers(signal, sender):
        receivers = signal._live_receivers(sender)
        if isinstance(receivers, tuple):
            sync_receivers, async_receivers = receivers
            return sync_receivers + async_receivers
        return list(receivers)
