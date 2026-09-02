"""Static checks for AI Watch Windows MSI sequencing and self-update handoff.

The ``RegisterTasks`` deferred custom action runs ``register-tasks.ps1`` as
SYSTEM during the MSI commit phase. That script reads
``HKLM\\Software\\Runlayer\\AIWatch\\OrgApiKey`` and silently registers nothing
when the value is empty (the OrgApiKey gate — see ``test_windows_ps1_gates.py``).

``OrgApiKey`` is written by the MSI's standard ``WriteRegistryValues`` action
(sequence ~5000), which runs *after* ``InstallFiles`` (~4000). Deferred custom
actions and standard system-state actions both execute in sequence-number order
during ``InstallFinalize``. So ``RegisterTasks`` must be scheduled
``After=WriteRegistryValues`` — scheduling it ``After=InstallFiles`` (~4001) runs
it before the registry is committed, the gate reads an empty ``OrgApiKey``, and
no scheduled tasks are ever registered on install / major-upgrade (ENG-3579).

These are static XML-attribute checks (the contract can't be exercised without
building the MSI + a Windows install), so they pin the relative scheduling that
encodes the dependency.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

_AIWATCH_WXS = Path(__file__).parent.parent / "packaging" / "windows" / "aiwatch.wxs"
_RUNLAYER_WXS = Path(__file__).parent.parent / "packaging" / "windows" / "runlayer.wxs"
_AIWATCH_RELEASE_WORKFLOW = (
    Path(__file__).parents[2] / ".github" / "workflows" / "release-aiwatch.yml"
)


def _package(path: Path) -> tuple[str, ET.Element]:
    root = ET.fromstring(path.read_text())
    ns = root.tag[root.tag.index("{") : root.tag.index("}") + 1]
    package = root.find(f"{ns}Package")
    assert package is not None, f"{path.name} missing <Package>"
    return ns, package


def _install_execute_customs() -> dict[str, ET.Element]:
    """Map Action id -> <Custom> element inside <InstallExecuteSequence>."""
    root = ET.fromstring(_AIWATCH_WXS.read_text())
    ns = root.tag[root.tag.index("{") : root.tag.index("}") + 1]
    package = root.find(f"{ns}Package")
    assert package is not None, "aiwatch.wxs missing <Package>"
    sequence = package.find(f"{ns}InstallExecuteSequence")
    assert sequence is not None, "aiwatch.wxs missing <InstallExecuteSequence>"
    return {custom.get("Action"): custom for custom in sequence.findall(f"{ns}Custom")}


def test_windows_msis_embed_their_payload_cabinet() -> None:
    for path in (_AIWATCH_WXS, _RUNLAYER_WXS):
        ns, package = _package(path)
        media_template = package.find(f"{ns}MediaTemplate")
        assert media_template is not None, (
            f"{path.name} must embed its payload instead of requiring an unpublished "
            "external cab1.cab"
        )
        assert media_template.attrib == {
            "EmbedCab": "yes",
            "CompressionLevel": "high",
        }


def test_aiwatch_release_smoke_covers_gated_service_lifecycle() -> None:
    workflow = _AIWATCH_RELEASE_WORKFLOW.read_text()
    step_start = workflow.index("- name: Smoke-test Windows service install")
    step_end = workflow.index("- name: Build .intunewin", step_start)
    smoke_test = workflow[step_start:step_end]
    cleanup = smoke_test[smoke_test.rindex("} finally {") :]

    install_complete = smoke_test.index("$installed = $true")
    assert_absent = smoke_test.index(
        "Get-Service -Name RunlayerAIWatch -ErrorAction SilentlyContinue"
    )
    enable_gate = smoke_test.index("$backendConfig = @{")
    reconcile = smoke_test.index("& $aiwatch setup hooks install --mdm")
    assert_running = smoke_test.index(
        "Get-Service -Name RunlayerAIWatch -ErrorAction Stop",
        reconcile,
    )
    close_gate = smoke_test.index("$closedBackendConfig.daemon_enabled = $false")
    remove_reconcile = smoke_test.index(
        "& $aiwatch setup hooks install --mdm",
        close_gate,
    )
    assert_removed = smoke_test.index(
        "Get-Service -Name RunlayerAIWatch -ErrorAction SilentlyContinue",
        remove_reconcile,
    )
    assert_no_daemons = smoke_test.index(
        "Get-CimInstance Win32_Process",
        remove_reconcile,
    )
    stop_service = cleanup.index("Stop-Service -Name RunlayerAIWatch")
    wait_processes = cleanup.index("Get-Process -Name aiwatch")
    uninstall = cleanup.index("Start-Process msiexec.exe")

    assert (
        install_complete
        < assert_absent
        < enable_gate
        < reconcile
        < assert_running
        < close_gate
        < remove_reconcile
        < assert_removed
        < assert_no_daemons
    )
    assert stop_service < wait_processes < uninstall
    assert "AddSeconds(15)" in cleanup
    assert "$uninstall.ExitCode -notin @(0, 3010)" in cleanup


def test_self_update_msis_allow_transactional_backend_selected_versions() -> None:
    for path in (_AIWATCH_WXS, _RUNLAYER_WXS):
        ns, package = _package(path)
        major_upgrade = package.find(f"{ns}MajorUpgrade")
        assert major_upgrade is not None, f"{path.name} missing <MajorUpgrade>"
        assert major_upgrade.get("AllowDowngrades") == "yes"
        assert major_upgrade.get("Schedule") == "afterInstallInitialize"
        assert "AllowSameVersionUpgrades" not in major_upgrade.attrib
        assert "DowngradeErrorMessage" not in major_upgrade.attrib

        properties = {prop.get("Id"): prop for prop in package.findall(f"{ns}Property")}
        marker = properties.get("RUNLAYER_SELF_UPDATE_READY")
        assert marker is not None, f"{path.name} missing self-update marker"
        assert marker.get("Value") == "1"


def test_self_update_msis_force_reinstall_files_after_early_removal() -> None:
    for path in (_AIWATCH_WXS, _RUNLAYER_WXS):
        ns, package = _package(path)
        properties = {prop.get("Id"): prop for prop in package.findall(f"{ns}Property")}

        reinstall_mode = properties.get("REINSTALLMODE")
        assert reinstall_mode is not None, (
            f"{path.name} must force file installation because early "
            "RemoveExistingProducts deletes equal-version runtime files after costing"
        )
        assert reinstall_mode.get("Value") == "amus"


def test_aiwatch_msi_only_controls_reconcile_created_service() -> None:
    ns, package = _package(_AIWATCH_WXS)
    components = {
        component.get("Id"): component for component in package.iter(f"{ns}Component")
    }
    daemon_component = components["DaemonService"]
    assert daemon_component.find(f"{ns}ServiceInstall") is None
    service_control = daemon_component.find(f"{ns}ServiceControl")
    assert service_control is not None
    assert service_control.attrib == {
        "Id": "DaemonServiceControl",
        "Name": "RunlayerAIWatch",
        "Stop": "both",
        "Remove": "uninstall",
        "Wait": "yes",
    }


def test_cli_true_uninstall_runs_owned_task_cleanup_only() -> None:
    ns, package = _package(_RUNLAYER_WXS)
    custom_actions = {
        action.get("Id"): action for action in package.findall(f"{ns}CustomAction")
    }
    sequence = package.find(f"{ns}InstallExecuteSequence")
    assert sequence is not None
    scheduled_actions = {
        custom.get("Action"): custom for custom in sequence.findall(f"{ns}Custom")
    }
    for action_id in ("UnregisterCliUpdateTask", "UnregisterCliScheduleTask"):
        cleanup = custom_actions.get(action_id)
        assert cleanup is not None
        assert cleanup.attrib == {
            "Id": action_id,
            "BinaryRef": "Wix4UtilCA_X64",
            "DllEntry": "WixQuietExec64",
            "Execute": "deferred",
            "Impersonate": "no",
            "Return": "ignore",
        }

        setter = scheduled_actions[f"Set{action_id}Cmd"]
        scheduled = scheduled_actions[action_id]
        assert setter.get("Before") == action_id
        assert scheduled.get("Before") == "RemoveFiles"
        expected_condition = 'REMOVE="ALL" AND NOT UPGRADINGPRODUCTCODE'
        assert setter.get("Condition") == expected_condition
        assert scheduled.get("Condition") == expected_condition


def test_aiwatch_recovers_config_after_appsearch_before_launch_conditions() -> None:
    ns, package = _package(_AIWATCH_WXS)
    setters = {
        setter.get("Id"): setter for setter in package.findall(f"{ns}SetProperty")
    }
    recovery_actions = (
        ("AIWATCH_HOST", "RecoverAiWatchHost", "AppSearch"),
        ("AIWATCH_ORG_API_KEY", "RecoverAiWatchOrgApiKey", "RecoverAiWatchHost"),
        ("AIWATCH_USERNAME", "RecoverAiWatchUsername", "RecoverAiWatchOrgApiKey"),
        ("AIWATCH_DEVICE_NAME", "RecoverAiWatchDeviceName", "RecoverAiWatchUsername"),
        (
            "AIWATCH_EFFECTIVE_AUTO_UPDATE",
            "RecoverAiWatchAutoUpdate",
            "RecoverAiWatchDeviceName",
        ),
        (
            "AIWATCH_EFFECTIVE_CPU_CORES",
            "RecoverAiWatchCpuCores",
            "RecoverAiWatchAutoUpdate",
        ),
        (
            "AIWATCH_EFFECTIVE_MAX_CPU_PERCENT",
            "RecoverAiWatchMaxCpuPercent",
            "RecoverAiWatchCpuCores",
        ),
        (
            "AIWATCH_EFFECTIVE_MEMORY_LIMIT_MB",
            "RecoverAiWatchMemoryLimitMb",
            "RecoverAiWatchMaxCpuPercent",
        ),
    )
    for property_id, action, after in recovery_actions:
        setter = setters[property_id]
        assert setter.get("Action") == action
        assert setter.get("After") == after
        assert "Before" not in setter.attrib
        assert setter.get("Sequence") == "first"

    for sequence_name in ("InstallUISequence", "InstallExecuteSequence"):
        sequence = package.find(f"{ns}{sequence_name}")
        assert sequence is not None
        launch_conditions = sequence.find(f"{ns}LaunchConditions")
        assert launch_conditions is not None
        assert launch_conditions.get("After") == "RecoverAiWatchMemoryLimitMb"


def test_aiwatch_upgrade_recovers_string_machine_config_without_argv() -> None:
    ns, package = _package(_AIWATCH_WXS)
    properties = {prop.get("Id"): prop for prop in package.findall(f"{ns}Property")}
    setters = {
        setter.get("Id"): setter for setter in package.findall(f"{ns}SetProperty")
    }
    expected = (
        ("AIWATCH_HOST", "AIWATCH_EXISTING_HOST", "Host", True),
        ("AIWATCH_ORG_API_KEY", "AIWATCH_EXISTING_ORG_API_KEY", "OrgApiKey", True),
        ("AIWATCH_USERNAME", "AIWATCH_EXISTING_USERNAME", "Username", True),
        ("AIWATCH_DEVICE_NAME", "AIWATCH_EXISTING_DEVICE_NAME", "DeviceName", True),
    )
    for target_id, existing_id, registry_name, hidden in expected:
        target = properties.get(target_id)
        assert target is not None
        assert target.get("Secure") == "yes"
        assert (target.get("Hidden") == "yes") is hidden

        existing = properties.get(existing_id)
        assert existing is not None
        assert existing.get("Hidden") == "yes"
        search = existing.find(f"{ns}RegistrySearch")
        assert search is not None
        assert search.attrib == {
            "Id": f"ExistingAiWatch{registry_name}",
            "Root": "HKLM",
            "Key": "Software\\Runlayer\\AIWatch",
            "Name": registry_name,
            "Type": "raw",
            "Bitness": "always64",
        }

        setter = setters.get(target_id)
        assert setter is not None
        assert setter.get("Value") == f"[{existing_id}]"
        expected_condition = f"NOT {target_id} AND {existing_id}"
        assert setter.get("Condition") == expected_condition


def test_aiwatch_upgrade_recovers_dword_machine_config_without_argv() -> None:
    ns, package = _package(_AIWATCH_WXS)
    properties = {prop.get("Id"): prop for prop in package.findall(f"{ns}Property")}
    setters = {
        setter.get("Id"): setter for setter in package.findall(f"{ns}SetProperty")
    }
    components = {
        component.get("Id"): component for component in package.iter(f"{ns}Component")
    }
    expected = (
        (
            "AIWATCH_AUTO_UPDATE",
            "AIWATCH_EFFECTIVE_AUTO_UPDATE",
            "AutoUpdate",
            "ManagedConfigAutoUpdate",
        ),
        (
            "AIWATCH_CPU_CORES",
            "AIWATCH_EFFECTIVE_CPU_CORES",
            "CpuCores",
            "ManagedConfigCpuCores",
        ),
        (
            "AIWATCH_MAX_CPU_PERCENT",
            "AIWATCH_EFFECTIVE_MAX_CPU_PERCENT",
            "MaxCpuPercent",
            "ManagedConfigMaxCpuPercent",
        ),
        (
            "AIWATCH_MEMORY_LIMIT_MB",
            "AIWATCH_EFFECTIVE_MEMORY_LIMIT_MB",
            "MemoryLimitMb",
            "ManagedConfigMemoryLimitMb",
        ),
    )
    for public_id, effective_id, registry_name, component_id in expected:
        public = properties.get(public_id)
        assert public is not None
        assert public.get("Secure") == "yes"
        assert public.get("Value") is None, (
            f"{public_id} must not have an MSI default that overrides the existing "
            "registry value during an upgrade"
        )

        effective = properties.get(effective_id)
        assert effective is not None
        assert effective.get("Secure") == "yes"
        assert effective.get("Hidden") == "yes"
        search = effective.find(f"{ns}RegistrySearch")
        assert search is not None
        assert search.attrib == {
            "Id": f"ExistingAiWatch{registry_name}",
            "Root": "HKLM",
            "Key": "Software\\Runlayer\\AIWatch",
            "Name": registry_name,
            "Type": "raw",
            "Bitness": "always64",
        }

        setter = setters.get(effective_id)
        assert setter is not None
        assert setter.get("Value") == f"#[{public_id}]"
        assert setter.get("Condition") == public_id

        component = components.get(component_id)
        assert component is not None
        assert component.get("Condition") == effective_id
        registry_value = component.find(f"{ns}RegistryValue")
        assert registry_value is not None
        assert registry_value.get("Type") == "string"
        assert registry_value.get("Value") == f"[{effective_id}]"

    assert properties["AIWATCH_EFFECTIVE_AUTO_UPDATE"].get("Value") == "#1", (
        "a fresh MSI install must write the default-on AutoUpdate DWORD while "
        "still allowing AppSearch to recover an existing opt-out"
    )


def test_cli_msi_tenant_properties_are_optional_and_recovered() -> None:
    """The CLI MSI accepts optional CLI_HOST / CLI_ORG_API_KEY tenant properties
    (hosted install.ps1 Test Device flow) that must stay strictly optional: no
    Launch conditions, and the registry components gated on the properties so a
    prop-less install writes nothing and behaves exactly like the historical MSI.
    Upgrades/self-update recover previously written values via AppSearch."""
    ns, package = _package(_RUNLAYER_WXS)
    properties = {prop.get("Id"): prop for prop in package.findall(f"{ns}Property")}
    setters = {
        setter.get("Id"): setter for setter in package.findall(f"{ns}SetProperty")
    }
    components = {
        component.get("Id"): component for component in package.iter(f"{ns}Component")
    }

    assert package.find(f"{ns}Launch") is None, (
        "the CLI MSI must not require tenant properties — MDM/manual installs "
        "legitimately omit them and read the AI Watch configuration"
    )

    expected = (
        ("CLI_HOST", "CLI_EXISTING_HOST", "Host", "ManagedConfigHost"),
        (
            "CLI_ORG_API_KEY",
            "CLI_EXISTING_ORG_API_KEY",
            "OrgApiKey",
            "ManagedConfigOrgApiKey",
        ),
    )
    for target_id, existing_id, registry_name, component_id in expected:
        target = properties.get(target_id)
        assert target is not None
        assert target.get("Secure") == "yes"
        assert target.get("Hidden") == "yes"
        assert target.get("Value") is None, (
            f"{target_id} must not have an MSI default that overrides the "
            "existing registry value during an upgrade"
        )

        existing = properties.get(existing_id)
        assert existing is not None
        assert existing.get("Hidden") == "yes"
        search = existing.find(f"{ns}RegistrySearch")
        assert search is not None
        assert search.attrib == {
            "Id": f"ExistingCli{registry_name}",
            "Root": "HKLM",
            "Key": "Software\\Runlayer\\CLI",
            "Name": registry_name,
            "Type": "raw",
            "Bitness": "always64",
        }

        setter = setters.get(target_id)
        assert setter is not None
        assert setter.get("Value") == f"[{existing_id}]"
        assert setter.get("Condition") == f"NOT {target_id} AND {existing_id}"
        assert setter.get("Sequence") == "first"

        component = components.get(component_id)
        assert component is not None
        assert component.get("Condition") == target_id, (
            f"{component_id} must be gated on {target_id} so a prop-less "
            "install writes no empty registry value"
        )
        assert component.get("Transitive") == "yes", (
            f"{component_id} must be transitive: the install.ps1 bootstrap "
            "uses a same-version REINSTALL=ALL over an existing prop-less "
            "install, and MSI only re-evaluates a component condition on "
            "reinstall when the component is transitive — otherwise the "
            "tenant properties are silently dropped and the Test Device "
            "stays unconfigured"
        )
        registry_value = component.find(f"{ns}RegistryValue")
        assert registry_value is not None
        assert registry_value.attrib == {
            "Root": "HKLM",
            "Key": "Software\\Runlayer\\CLI",
            "Name": registry_name,
            "Type": "string",
            "Value": f"[{target_id}]",
            "KeyPath": "yes",
        }

    setter_ids = {
        setter.get("Action") for setter in package.findall(f"{ns}SetProperty")
    }
    assert {"RecoverCliHost", "RecoverCliOrgApiKey"} <= setter_ids


def test_aiwatch_msi_excludes_backend_managed_capability_config() -> None:
    ns, package = _package(_AIWATCH_WXS)
    forbidden_property_ids = {
        "AIWATCH_MODE",
        "AIWATCH_ENFORCEMENT",
        "AIWATCH_SESSIONS",
        "AIWATCH_DETECT_PROCESSES",
        "AIWATCH_DETECT_CONTAINERS",
        "AIWATCH_PROJECT_DEPTH",
        "AIWATCH_PROJECT_TIMEOUT",
        "AIWATCH_EXISTING_MODE",
        "AIWATCH_EFFECTIVE_ENFORCEMENT",
        "AIWATCH_EFFECTIVE_SESSIONS",
        "AIWATCH_EFFECTIVE_DETECT_PROCESSES",
        "AIWATCH_EFFECTIVE_DETECT_CONTAINERS",
        "AIWATCH_EFFECTIVE_PROJECT_DEPTH",
        "AIWATCH_EFFECTIVE_PROJECT_TIMEOUT",
    }
    property_ids = {prop.get("Id") for prop in package.findall(f"{ns}Property")}
    assert property_ids.isdisjoint(forbidden_property_ids)

    forbidden_registry_names = {
        "Mode",
        "Enforcement",
        "Sessions",
        "DetectProcesses",
        "DetectContainers",
        "ProjectDepth",
        "ProjectTimeout",
    }
    registry_names = {
        element.get("Name")
        for tag in ("RegistrySearch", "RegistryValue", "RemoveRegistryValue")
        for element in package.iter(f"{ns}{tag}")
    }
    assert registry_names.isdisjoint(forbidden_registry_names)


def _managed_config_registry_values() -> dict[str, dict[str, str]]:
    """Map RegistryValue Name -> attrib dict for the ``ManagedConfig`` component's
    ``HKLM\\Software\\Runlayer\\AIWatch`` <RegistryKey>."""
    root = ET.fromstring(_AIWATCH_WXS.read_text())
    ns = root.tag[root.tag.index("{") : root.tag.index("}") + 1]
    for component in root.iter(f"{ns}Component"):
        if component.get("Id") != "ManagedConfig":
            continue
        key = component.find(f"{ns}RegistryKey")
        assert key is not None, "ManagedConfig component missing <RegistryKey>"
        assert key.get("Key") == "Software\\Runlayer\\AIWatch", (
            "ManagedConfig must key HKLM\\Software\\Runlayer\\AIWatch"
        )
        return {
            rv.get("Name"): dict(rv.attrib) for rv in key.findall(f"{ns}RegistryValue")
        }
    raise AssertionError("aiwatch.wxs missing the ManagedConfig component")


def test_register_tasks_runs_after_write_registry_values() -> None:
    """RegisterTasks reads OrgApiKey, so it must run after WriteRegistryValues
    commits that registry value — not merely after InstallFiles lands the exe."""
    customs = _install_execute_customs()
    register = customs.get("RegisterTasks")
    assert register is not None, "RegisterTasks not scheduled in InstallExecuteSequence"

    assert register.get("After") == "WriteRegistryValues", (
        "RegisterTasks must be scheduled After=WriteRegistryValues so "
        "register-tasks.ps1 sees the OrgApiKey value. After=InstallFiles runs it "
        "(~4001) before WriteRegistryValues (~5000) commits the registry, so the "
        "OrgApiKey gate reads empty and no tasks are registered (ENG-3579)."
    )
    assert register.get("After") != "InstallFiles"


def test_register_tasks_is_gated_to_install_not_remove() -> None:
    """RegisterTasks must stay install/upgrade/repair-only (NOT REMOVE)."""
    customs = _install_execute_customs()
    register = customs.get("RegisterTasks")
    assert register is not None
    assert register.get("Condition") == "NOT REMOVE"


def test_set_register_cmd_stages_data_before_deferred_action() -> None:
    """The type-51 SetProperty that stages CustomActionData must still run before
    the deferred RegisterTasks (deferred CAs can't read property refs at runtime),
    so it stays anchored Before=RegisterTasks and moves with it."""
    customs = _install_execute_customs()
    setter = customs.get("SetRegisterTasksCmd")
    assert setter is not None, "SetRegisterTasksCmd not scheduled"
    assert setter.get("Before") == "RegisterTasks"


def test_managed_config_writes_installed_version_reg_sz() -> None:
    """The MSI must stamp the installed version as a REG_SZ under the managed key
    (``HKLM\\Software\\Runlayer\\AIWatch\\Version``) so MDM can inventory it
    without exec'ing ``aiwatch.exe`` (ENG-4161).

    It lives in the always-written ``ManagedConfig`` component (not a gated
    optional component), so every install stamps it unconditionally; the value is
    the pyproject version passed via ``build_msi.ps1 -d Version=$Version``. Being
    part of ``ManagedConfig`` means it's rewritten on ``MajorUpgrade`` and removed
    with the component on ``REMOVE=ALL`` (true uninstall).
    """
    values = _managed_config_registry_values()

    assert "Version" in values, (
        "ManagedConfig must write a Version registry value for MDM inventory"
    )
    version = values["Version"]
    assert version.get("Type") == "string", "Version must be a REG_SZ (Type=string)"
    assert version.get("Value") == "$(var.Version)", (
        "Version must be the pyproject version passed via -d Version=$Version, "
        "not a hardcoded string"
    )
    # Inventory record must not be gated on an optional MDM-owned property —
    # every install stamps it.
    assert "Condition" not in version, (
        "Version must be unconditional so every install/upgrade stamps it"
    )
