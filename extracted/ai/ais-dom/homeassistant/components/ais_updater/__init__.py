"""
Support to check for available updates for AIS

"""
import asyncio
from distutils.version import StrictVersion
import json
import logging
import os
import platform
import subprocess
from subprocess import PIPE, Popen
import sys

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.components.ais_dom import ais_global
from homeassistant.const import (
    ATTR_FRIENDLY_NAME,
    STATE_ON,
    __version__ as current_version,
)
from homeassistant.helpers import event
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util

_LOGGER = logging.getLogger(__name__)

ATTR_RELEASE_NOTES = "release_notes"

CONF_REPORTING = "reporting"
CONF_COMPONENT_REPORTING = "include_used_components"

DOMAIN = "ais_updater"
SERVICE_SET_UPDATE_STATUS = "set_update_status"
SERVICE_SET_UPDATE_PROGRESS = "set_update_progress"
SERVICE_CHECK_VERSION = "check_version"
SERVICE_UPGRADE_PACKAGE = "upgrade_package"
SERVICE_EXECUTE_UPGRADE = "execute_upgrade"
SERVICE_DOWNLOAD_UPGRADE = "download_upgrade"
SERVICE_INSTALL_UPGRADE = "install_upgrade"
SERVICE_APPLAY_THE_FIX = "applay_the_fix"
ENTITY_ID = "sensor.version_info"
ATTR_UPDATE_STATUS = "update_status"
ATTR_UPDATE_CHECK_TIME = "update_check_time"

UPDATE_STATUS_CHECKING = "checking"
UPDATE_STATUS_OUTDATED = "outdated"
UPDATE_STATUS_DOWNLOADING = "downloading"
UPDATE_STATUS_INSTALLING = "installing"
UPDATE_STATUS_UPDATED = "updated"
UPDATE_STATUS_RESTART = "restart"
UPDATE_STATUS_UNKNOWN = "unknown"

UPDATER_URL = "https://" + ais_global.AIS_HOST + "/ords/dom/dom/updater_new"
APT_VERSION_INFO_FILE = ".ais_apt"
ZIGBEE2MQTT_VERSION_PACKAGE_FILE = (
    "/data/data/com.termux/files/home/zigbee2mqtt/package.json"
)
G_CURRENT_ANDROID_DOM_V = "0"
G_CURRENT_ANDROID_LAUNCHER_V = "0"
G_CURRENT_ANDROID_TTS_V = "0"
G_CURRENT_ANDROID_STT_V = "0"
G_CURRENT_LINUX_V = "0"
G_CURRENT_ZIGBEE2MQTT_V = "0"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: {
            vol.Optional(CONF_REPORTING, default=True): cv.boolean,
            vol.Optional(CONF_COMPONENT_REPORTING, default=False): cv.boolean,
        }
    },
    extra=vol.ALLOW_EXTRA,
)


def _set_update_status(hass, status):
    state = hass.states.get(ENTITY_ID)
    attr = state.attributes
    new_attr = attr.copy()
    info = ""
    if status == UPDATE_STATUS_DOWNLOADING:
        info = "Pobieram."
    elif status == UPDATE_STATUS_INSTALLING:
        info = "Instaluje."
    elif status == UPDATE_STATUS_RESTART:
        info = "Restartuje."

    new_attr[ATTR_UPDATE_STATUS] = status
    new_attr[ATTR_UPDATE_CHECK_TIME] = get_current_dt()
    hass.states.set(ENTITY_ID, info, new_attr)

    # inform about downloading
    if info != "":
        hass.services.call(
            "ais_ai_service", "say_it", {"text": "Aktualizacja. " + info}
        )


def _set_update_progress(hass, progress):
    state = hass.states.get(ENTITY_ID)
    attr = state.attributes
    status = state.state
    new_attr = attr.copy()
    set_progress = 0.5
    set_buffer = 0.1
    if ":" in progress:
        set_progress = progress.split(":")[0]
        set_buffer = progress.split(":")[1]
    new_attr["progress"] = set_progress
    new_attr["buffer"] = set_buffer
    hass.states.set(ENTITY_ID, status, new_attr)


async def async_setup(hass, config):
    """Set up the updater component."""

    config = config.get(DOMAIN, {})
    include_components = config.get(CONF_COMPONENT_REPORTING)

    async def check_version(now):
        # check if the call was from scheduler or service / web app
        if "ServiceCall" in str(type(now)):
            # call is from service or automation
            allow_auto_update = False
            allow_to_say = True
            if "autoUpdate" in now.data:
                allow_auto_update = now.data["autoUpdate"]
            if "sayIt" in now.data:
                allow_to_say = now.data["sayIt"]
        else:
            # call is from scheduler
            allow_auto_update = True
            allow_to_say = False
        """Check if a new version is available and report if one is."""
        if not ais_global.G_AIS_START_IS_DONE or not allow_auto_update:
            # do not update on start
            # to prevent the restart loop in case of problem with update
            auto_update = False
        else:
            if hass.states.get("input_boolean.ais_auto_update").state == STATE_ON:
                auto_update = True
            else:
                auto_update = False

        result = await get_newest_version(hass, include_components, auto_update)

        if result is None:
            return

        # overriding auto_update, in case the we don't want to zigbee2mqtt without user
        need_to_update, dom_app_newest_version, release_notes = result

        # Validate version
        if need_to_update:
            _LOGGER.info("The latest available version is %s", dom_app_newest_version)
            if auto_update:
                info = "Aktualizuje system do najnowszej wersji. " + release_notes
            else:
                info = "Dostępna jest aktualizacja. " + release_notes

            hass.states.async_set(
                "script.ais_update_system",
                "off",
                {
                    ATTR_FRIENDLY_NAME: " Zainstaluj aktualizację",
                    "icon": "mdi:download",
                },
            )

            # notify about update
            if auto_update:
                hass.components.persistent_notification.async_create(
                    title="Aktualizuje system do najnowszej wersji ",
                    message=(
                        info + "[ Status aktualizacji](/config/ais_dom_config_update)"
                    ),
                    notification_id="ais_update_notification",
                )
            else:
                hass.components.persistent_notification.async_create(
                    title="Dostępna jest aktualizacja ",
                    message=(
                        info
                        + "[ Przejdź, by zainstalować](/config/ais_dom_config_update)"
                    ),
                    notification_id="ais_update_notification",
                )

            # say info about update
            if ais_global.G_AIS_START_IS_DONE and allow_to_say:
                await hass.services.async_call(
                    "ais_ai_service", "say_it", {"text": info}
                )
        else:
            # dismiss update notification
            hass.components.persistent_notification.async_dismiss(
                "ais_update_notification"
            )
            info = "Twój system jest aktualny"

            # only if not executed by scheduler
            if ais_global.G_AIS_START_IS_DONE and allow_to_say:
                await hass.services.async_call(
                    "ais_ai_service", "say_it", {"text": info}
                )
            info += release_notes
            hass.states.async_set(
                "script.ais_update_system",
                "off",
                {
                    ATTR_FRIENDLY_NAME: " Sprawdź dostępność aktualizacji",
                    "icon": "mdi:refresh",
                },
            )
            _LOGGER.info("You are on the latest version of Assystent domowy")

    # Update daily, start at 9AM + some random minutes and seconds based on the system startup
    _dt = dt_util.utcnow()
    event.async_track_utc_time_change(
        hass, check_version, hour=9, minute=_dt.minute, second=_dt.second
    )

    def upgrade_package_task(package):
        _LOGGER.info("upgrade_package_task " + str(package))
        env = os.environ.copy()
        args = [sys.executable, "-m", "pip", "install", "--quiet", package, "--upgrade"]
        process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=env)
        _, stderr = process.communicate()
        if process.returncode != 0:
            _LOGGER.error(
                "Unable to install package %s: %s",
                package,
                stderr.decode("utf-8").lstrip().strip(),
            )
        else:
            if package.startswith("yt-dlp"):
                path = (
                    str(
                        os.path.abspath(
                            os.path.join(
                                os.path.dirname(__file__), "..", "ais_yt_service"
                            )
                        )
                    )
                    + "/manifest.json"
                )
                manifest = {
                    "domain": "ais_yt_service",
                    "name": "AIS YouTube",
                    "config_flow": False,
                    "documentation": "https://www.ai-speaker.com",
                    "requirements": [package],
                    "dependencies": [],
                    "codeowners": [],
                }
                with open(path, "w+") as jsonFile:
                    json.dump(manifest, jsonFile)

    def upgrade_package(call):
        """Ask AIS dom service if the package need to be upgraded,
        if yes -> Install a package on PyPi
        """
        if "package" not in call.data:
            _LOGGER.error("No package specified")
            return
        package = call.data["package"]
        if "version" in call.data:
            package = package + "==" + call.data["version"]
        _LOGGER.info("Attempting install of %s", package)
        # todo Starting the installation as independent task
        import threading

        update_thread = threading.Thread(target=upgrade_package_task, args=(package,))
        update_thread.start()

    def set_update_status(call):
        _LOGGER.info("set_update_status")
        if "status" in call.data:
            _set_update_status(hass, call.data["status"])
        else:
            _set_update_status(hass, UPDATE_STATUS_UNKNOWN)

    def set_update_progress(call):
        _LOGGER.info("set_update_progress")
        if "progress" in call.data:
            _set_update_progress(hass, call.data["progress"])

    def execute_upgrade(call):
        _LOGGER.info("execute_upgrade")
        _set_update_status(hass, UPDATE_STATUS_CHECKING)
        do_execute_upgrade(hass, call)

    def download_upgrade(call):
        _LOGGER.info("download_upgrade")
        _set_update_status(hass, UPDATE_STATUS_DOWNLOADING)
        do_download_upgrade(hass, call)

    def install_upgrade(call):
        _LOGGER.info("install_upgrade")
        _set_update_status(hass, UPDATE_STATUS_INSTALLING)
        do_install_upgrade(hass, call)

    def applay_the_fix(call):
        _LOGGER.info("applay_the_fix")
        do_applay_the_fix(hass, call)

    # register services
    hass.services.async_register(DOMAIN, SERVICE_SET_UPDATE_STATUS, set_update_status)
    hass.services.async_register(
        DOMAIN, SERVICE_SET_UPDATE_PROGRESS, set_update_progress
    )
    hass.services.async_register(DOMAIN, SERVICE_CHECK_VERSION, check_version)
    hass.services.async_register(DOMAIN, SERVICE_UPGRADE_PACKAGE, upgrade_package)
    hass.services.async_register(DOMAIN, SERVICE_EXECUTE_UPGRADE, execute_upgrade)
    hass.services.async_register(DOMAIN, SERVICE_DOWNLOAD_UPGRADE, download_upgrade)
    hass.services.async_register(DOMAIN, SERVICE_INSTALL_UPGRADE, install_upgrade)
    hass.services.async_register(DOMAIN, SERVICE_APPLAY_THE_FIX, applay_the_fix)
    return True


def get_current_dt():
    from datetime import datetime

    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def get_current_android_apk_version():
    try:
        apk_dom_version = "0"
        apk_launcher_version = "0"
        apk_tts_version = "0"
        apk_stt_version = "0"
        if ais_global.has_root():
            apk_dom_version = subprocess.check_output(
                'su -c "dumpsys package com.termux | grep versionName"',
                shell=True,  # nosec
                timeout=15,
            )
            apk_dom_version = (
                apk_dom_version.decode("utf-8")
                .replace("\n", "")
                .strip()
                .replace("versionName=", "")
            )

            apk_launcher_version = subprocess.check_output(
                'su -c "dumpsys package launcher.sviete.pl.domlauncherapp | grep versionName"',
                shell=True,  # nosec
                timeout=15,
            )
            apk_launcher_version = (
                apk_launcher_version.decode("utf-8")
                .replace("\n", "")
                .strip()
                .replace("versionName=", "")
            )
            # TTS
            try:
                apk_tts_version = subprocess.check_output(
                    'su -c "dumpsys package com.google.android.tts | grep versionName"',
                    shell=True,  # nosec
                    timeout=15,
                )
                apk_tts_version = (
                    apk_tts_version.decode("utf-8")
                    .replace("\n", "")
                    .strip()
                    .replace("versionName=", "")
                )
            except Exception as e:
                _LOGGER.info("Can't get android android.tts apk version! " + str(e))
            # STT
            try:
                apk_stt_version = subprocess.check_output(
                    'su -c "dumpsys package com.google.android.googlequicksearchbox | grep versionName"',
                    shell=True,  # nosec
                    timeout=15,
                )
            except Exception as e:
                _LOGGER.info(
                    "Can't get android googlequicksearchbox apk version! " + str(e)
                )
                try:
                    apk_stt_version = subprocess.check_output(
                        'su -c "dumpsys package com.google.android.katniss | grep versionName"',
                        shell=True,  # nosec
                        timeout=15,
                    )
                except Exception as e:
                    _LOGGER.info("Can't get android katniss apk version! " + str(e))

            apk_stt_version = (
                apk_stt_version.decode("utf-8")
                .replace("\n", "")
                .strip()
                .replace("versionName=", "")
            )
        else:
            # to work for not rooted devices - get the version from gate api
            import requests

            call = requests.get("http://localhost:8122/", timeout=5)
            ws_resp = call.json()
            apk_dom_version = ws_resp["AisServerVersion"]

        return apk_dom_version, apk_launcher_version, apk_tts_version, apk_stt_version
    except Exception as e:
        _LOGGER.info("Can't get android apk version! " + str(e))
        return "0", "0", "0", "0"


def get_current_linux_apt_version(hass):
    # get version of the apt from file ~/AIS/.ais_apt
    try:
        with open(hass.config.path(APT_VERSION_INFO_FILE)) as fptr:
            apt_current_version = fptr.read().replace("\n", "")
            return apt_current_version
    except Exception as e:
        _LOGGER.info("Error get_current_linux_apt_version " + str(e))
        return current_version


def get_current_zigbee2mqtt_version(hass):
    # try to take version from file
    try:
        with open(ZIGBEE2MQTT_VERSION_PACKAGE_FILE) as json_file:
            z2m_settings = json.load(json_file)
            return z2m_settings["version"].replace("-dev", "")
    except Exception as e:
        _LOGGER.info("Error get_current_zigbee2mqtt_version " + str(e))
    return "0"


async def get_system_info(hass, include_components):
    """Return info about the system."""
    global G_CURRENT_ANDROID_DOM_V
    global G_CURRENT_ANDROID_LAUNCHER_V
    global G_CURRENT_ANDROID_TTS_V
    global G_CURRENT_ANDROID_STT_V
    global G_CURRENT_LINUX_V
    global G_CURRENT_ZIGBEE2MQTT_V
    gate_id = hass.states.get("sensor.ais_secure_android_id_dom").state
    (
        G_CURRENT_ANDROID_DOM_V,
        G_CURRENT_ANDROID_LAUNCHER_V,
        G_CURRENT_ANDROID_TTS_V,
        G_CURRENT_ANDROID_STT_V,
    ) = get_current_android_apk_version()
    G_CURRENT_LINUX_V = get_current_linux_apt_version(hass)
    G_CURRENT_ZIGBEE2MQTT_V = get_current_zigbee2mqtt_version(hass)

    info_object = {
        "arch": platform.machine(),
        "os_name": platform.system(),
        "python_version": platform.python_version(),
        "gate_id": gate_id,
        "dom_app_version": current_version,
        "android_app_version": G_CURRENT_ANDROID_DOM_V,
        "android_app_launcher_version": G_CURRENT_ANDROID_LAUNCHER_V,
        "android_app_tts_version": G_CURRENT_ANDROID_TTS_V,
        "android_app_stt_version": G_CURRENT_ANDROID_STT_V,
        "linux_apt_version": G_CURRENT_LINUX_V,
        "zigbee2mqtt_version": G_CURRENT_ZIGBEE2MQTT_V,
        "gate_model": ais_global.get_ais_gate_model(),
    }

    if include_components:
        info_object["components"] = list(hass.config.components)

    return info_object


def get_system_info_sync(hass):
    """Return info about the system."""
    global G_CURRENT_ANDROID_DOM_V
    global G_CURRENT_ANDROID_LAUNCHER_V
    global G_CURRENT_ANDROID_TTS_V
    global G_CURRENT_ANDROID_STT_V
    global G_CURRENT_LINUX_V
    global G_CURRENT_ZIGBEE2MQTT_V
    gate_id = hass.states.get("sensor.ais_secure_android_id_dom").state
    (
        G_CURRENT_ANDROID_DOM_V,
        G_CURRENT_ANDROID_LAUNCHER_V,
        G_CURRENT_ANDROID_TTS_V,
        G_CURRENT_ANDROID_STT_V,
    ) = get_current_android_apk_version()
    G_CURRENT_LINUX_V = get_current_linux_apt_version(hass)
    G_CURRENT_ZIGBEE2MQTT_V = get_current_zigbee2mqtt_version(hass)
    info_object = {
        "gate_id": gate_id,
        "dom_app_version": current_version,
        "android_app_version": G_CURRENT_ANDROID_DOM_V,
        "android_app_launcher_version": G_CURRENT_ANDROID_LAUNCHER_V,
        "android_app_tts_version": G_CURRENT_ANDROID_TTS_V,
        "android_app_stt_version": G_CURRENT_ANDROID_STT_V,
        "linux_apt_version": G_CURRENT_LINUX_V,
        "zigbee2mqtt_version": G_CURRENT_ZIGBEE2MQTT_V,
        "gate_model": ais_global.get_ais_gate_model(),
    }
    return info_object


async def get_newest_version(hass, include_components, go_to_download):
    """Get the newest Ais dom version."""
    hass.states.async_set(
        ENTITY_ID,
        "Sprawdzam dostępność aktualizacji",
        {
            ATTR_FRIENDLY_NAME: "Wersja",
            "icon": "mdi:update",
            ATTR_UPDATE_STATUS: UPDATE_STATUS_CHECKING,
            ATTR_UPDATE_CHECK_TIME: get_current_dt(),
        },
    )

    info_object = await get_system_info(hass, include_components)
    session = async_get_clientsession(hass)
    release_script = ""
    fix_script = ""

    try:
        with async_timeout.timeout(10):
            req = await session.post(UPDATER_URL, json=info_object)
    except (asyncio.TimeoutError, aiohttp.ClientError):
        _LOGGER.error("Could not contact AIS dom to check " "for updates")
        info = "Nie można skontaktować się z usługą AIS dom."
        info += "Spróbuj ponownie później."
        hass.states.async_set(
            ENTITY_ID,
            info,
            {
                ATTR_FRIENDLY_NAME: "Wersja",
                "icon": "mdi:update",
                "dom_app_current_version": current_version,
                "reinstall_dom_app": False,
                "android_app_current_version": G_CURRENT_ANDROID_DOM_V,
                "reinstall_android_app": False,
                "linux_apt_current_version": G_CURRENT_LINUX_V,
                "reinstall_linux_apt": False,
                "zigbee2mqtt_current_version": G_CURRENT_ZIGBEE2MQTT_V,
                "reinstall_zigbee2mqtt": False,
                "release_script": release_script,
                "fix_script": fix_script,
                ATTR_UPDATE_STATUS: UPDATE_STATUS_UPDATED,
                ATTR_UPDATE_CHECK_TIME: get_current_dt(),
            },
        )
        return None

    try:
        res = await req.json()
        # check if we should update
        reinstall_dom_app = False
        reinstall_android_app = False
        reinstall_linux_apt = False
        reinstall_zigbee2mqtt = False

        # 1. fix script first
        if "fix_script" in res:
            fix_script = res["fix_script"]
        if fix_script != "":
            await hass.services.async_call(
                "ais_updater", "applay_the_fix", {"fix_script": fix_script}
            )

        if StrictVersion(res["dom_app_version"]) > StrictVersion(current_version):
            reinstall_dom_app = True
        if G_CURRENT_ANDROID_DOM_V != "0":
            if StrictVersion(res["android_app_version"]) > StrictVersion(
                G_CURRENT_ANDROID_DOM_V
            ):
                reinstall_android_app = True
        if G_CURRENT_LINUX_V != "0":
            if StrictVersion(res["linux_apt_version"]) > StrictVersion(
                G_CURRENT_LINUX_V
            ):
                reinstall_linux_apt = True
        if G_CURRENT_ZIGBEE2MQTT_V != "0":
            if StrictVersion(res["zigbee2mqtt_version"]) > StrictVersion(
                G_CURRENT_ZIGBEE2MQTT_V
            ):
                reinstall_zigbee2mqtt = True
        need_to_update = False
        info = "Twój system jest aktualny. " + res["release_notes"]
        system_status = UPDATE_STATUS_UPDATED
        if (
            reinstall_dom_app
            or reinstall_android_app
            or reinstall_linux_apt
            or reinstall_zigbee2mqtt
        ):
            need_to_update = True
            info = "Dostępna jest aktualizacja. " + res["release_notes"]
            system_status = UPDATE_STATUS_OUTDATED

        if "release_script" in res:
            release_script = res["release_script"]

        if "ais_cloud_services_host" in res:
            ais_global.AIS_HOST = res["ais_cloud_services_host"]

        hass.states.async_set(
            ENTITY_ID,
            info,
            {
                ATTR_FRIENDLY_NAME: "Aktualizacja",
                "icon": "mdi:update",
                "dom_app_current_version": current_version,
                "dom_app_newest_version": res["dom_app_version"],
                "reinstall_dom_app": reinstall_dom_app,
                "android_app_current_version": G_CURRENT_ANDROID_DOM_V,
                "android_app_newest_version": res["android_app_version"],
                "reinstall_android_app": reinstall_android_app,
                "linux_apt_current_version": G_CURRENT_LINUX_V,
                "linux_apt_newest_version": res["linux_apt_version"],
                "reinstall_linux_apt": reinstall_linux_apt,
                "zigbee2mqtt_current_version": G_CURRENT_ZIGBEE2MQTT_V,
                "zigbee2mqtt_newest_version": res["zigbee2mqtt_version"],
                "reinstall_zigbee2mqtt": reinstall_zigbee2mqtt,
                "release_script": release_script,
                "fix_script": fix_script,
                ATTR_UPDATE_STATUS: system_status,
                ATTR_UPDATE_CHECK_TIME: get_current_dt(),
                "ais_cloud_services_host": ais_global.AIS_HOST,
            },
        )
        if need_to_update and go_to_download:
            # call the download service
            await hass.services.async_call("ais_updater", "download_upgrade")
        return need_to_update, res["dom_app_version"], res["release_notes"]
    except ValueError:
        _LOGGER.error("Received invalid JSON from AIS dom Update")
        info = "Wersja. Otrzmyano nieprawidłową odpowiedz z usługi AIS dom "
        hass.states.async_set(
            ENTITY_ID,
            info,
            {
                ATTR_FRIENDLY_NAME: "Wersja",
                "icon": "mdi:update",
                "dom_app_current_version": current_version,
                "reinstall_dom_app": False,
                "android_app_current_version": G_CURRENT_ANDROID_DOM_V,
                "reinstall_android_app": False,
                "linux_apt_current_version": G_CURRENT_LINUX_V,
                "reinstall_linux_apt": False,
                "release_script": release_script,
                "zigbee2mqtt_current_version": G_CURRENT_ZIGBEE2MQTT_V,
                "reinstall_zigbee2mqtt": False,
                "fix_script": fix_script,
                ATTR_UPDATE_STATUS: UPDATE_STATUS_UPDATED,
                ATTR_UPDATE_CHECK_TIME: get_current_dt(),
            },
        )
        return None


def get_package_version(package) -> str:
    # get version from manifest.json
    if package == "yt-dlp":
        path = (
            str(
                os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "ais_yt_service")
                )
            )
            + "/manifest.json"
        )
        with open(path) as f:
            manifest = json.load(f)
        _LOGGER.info(str(manifest["requirements"][0]))
        return manifest["requirements"][0]
    return ""


def do_execute_upgrade(hass, call):
    # check the status of the sensor to choice if it's upgrade or version check
    state = hass.states.get("sensor.version_info")
    attr = state.attributes
    reinstall_dom_app = attr.get("reinstall_dom_app", False)
    reinstall_android_app = attr.get("reinstall_android_app", False)
    reinstall_linux_apt = attr.get("reinstall_linux_apt", False)
    reinstall_zigbee2mqtt = attr.get("reinstall_zigbee2mqtt", False)

    if (
        reinstall_dom_app is False
        and reinstall_android_app is False
        and reinstall_linux_apt is False
        and reinstall_zigbee2mqtt is False
    ):
        # this call was only version check
        hass.services.call(
            "ais_ai_service", "say_it", {"text": "Sprawdzam dostępność aktualizacji"}
        )
        hass.services.call(
            "ais_updater", "check_version", {"autoUpdate": False, "sayIt": True}
        )
        return

    # this call was upgrade call
    # check the newest version again before update
    need_to_update = True
    try:
        import requests

        info_object = get_system_info_sync(hass)
        call = requests.post(UPDATER_URL, json=info_object, timeout=5)
        ws_resp = call.json()
        # check if we should update
        reinstall_dom_app = False
        reinstall_android_app = False
        reinstall_linux_apt = False
        reinstall_zigbee2mqtt = False
        _LOGGER.info(str(StrictVersion(ws_resp["dom_app_version"])))
        _LOGGER.info(str(StrictVersion(current_version)))
        if StrictVersion(ws_resp["dom_app_version"]) > StrictVersion(current_version):
            reinstall_dom_app = True
        if G_CURRENT_ANDROID_DOM_V != "0":
            if StrictVersion(ws_resp["android_app_version"]) > StrictVersion(
                G_CURRENT_ANDROID_DOM_V
            ):
                reinstall_android_app = True
        if G_CURRENT_LINUX_V != "0":
            if StrictVersion(ws_resp["linux_apt_version"]) > StrictVersion(
                G_CURRENT_LINUX_V
            ):
                reinstall_linux_apt = True
        if G_CURRENT_ZIGBEE2MQTT_V != "0":
            if StrictVersion(ws_resp["zigbee2mqtt_version"]) > StrictVersion(
                G_CURRENT_ZIGBEE2MQTT_V
            ):
                reinstall_zigbee2mqtt = True

        info = "Twój system jest aktualny. " + ws_resp["release_notes"]
        system_status = UPDATE_STATUS_UPDATED
        need_to_update = False
        if (
            reinstall_dom_app
            or reinstall_android_app
            or reinstall_linux_apt
            or reinstall_zigbee2mqtt
        ):
            need_to_update = True
            info = "Dostępna jest aktualizacja. " + ws_resp["release_notes"]
            system_status = UPDATE_STATUS_OUTDATED

        release_script = ""
        if "release_script" in ws_resp:
            release_script = ws_resp["release_script"]

        # fix script first
        fix_script = ""
        if "fix_script" in ws_resp:
            fix_script = ws_resp["fix_script"]
        if fix_script != "":
            hass.services.call(
                "ais_updater", "applay_the_fix", {"fix_script": fix_script}
            )

        hass.states.set(
            ENTITY_ID,
            info,
            {
                ATTR_FRIENDLY_NAME: "Aktualizacja",
                "icon": "mdi:update",
                "dom_app_current_version": current_version,
                "dom_app_newest_version": ws_resp["dom_app_version"],
                "reinstall_dom_app": reinstall_dom_app,
                "android_app_current_version": G_CURRENT_ANDROID_DOM_V,
                "android_app_newest_version": ws_resp["android_app_version"],
                "reinstall_android_app": reinstall_android_app,
                "linux_apt_current_version": G_CURRENT_LINUX_V,
                "linux_apt_newest_version": ws_resp["linux_apt_version"],
                "reinstall_linux_apt": reinstall_linux_apt,
                "zigbee2mqtt_current_version": G_CURRENT_ZIGBEE2MQTT_V,
                "zigbee2mqtt_newest_version": ws_resp["zigbee2mqtt_version"],
                "reinstall_zigbee2mqtt": reinstall_zigbee2mqtt,
                "release_script": release_script,
                "fix_script": fix_script,
                ATTR_UPDATE_STATUS: system_status,
                ATTR_UPDATE_CHECK_TIME: get_current_dt(),
            },
        )

    except Exception as e:
        _LOGGER.error("Received invalid info from AIS dom Update " + str(e))
        _set_update_status(hass, UPDATE_STATUS_UNKNOWN)
        return

    if need_to_update:
        # clear tmp
        subprocess.check_output(
            "rm -rf /data/data/com.termux/files/usr/tmp/* ", shell=True  # nosec
        )
        # call the download service
        hass.services.call("ais_updater", "download_upgrade")
    else:
        _set_update_status(hass, UPDATE_STATUS_UPDATED)


def run_shell_command(command):
    _LOGGER.info("run_shell_command: " + str(command))
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        # returns None while subprocess is running
        ret_code = p.poll()
        line = p.stdout.readline()
        _LOGGER.info(str(line.decode("utf-8")))
        if ret_code is not None:
            break
    _LOGGER.info("subprocess return code: " + str(p.returncode))
    return p.returncode


def grant_write_to_sdcard():
    if not ais_global.has_root():
        return
    try:
        ret_output = subprocess.check_output(
            'su -c "pm grant launcher.sviete.pl.domlauncherapp android.permission.READ_EXTERNAL_STORAGE"',
            shell=True,  # nosec
            timeout=15,
        )
        _LOGGER.info(str(ret_output.decode("utf-8")))
        ret_output = subprocess.check_output(
            'su -c "pm grant launcher.sviete.pl.domlauncherapp android.permission.WRITE_EXTERNAL_STORAGE"',
            shell=True,  # nosec
            timeout=15,
        )
        _LOGGER.info(str(ret_output.decode("utf-8")))
        ret_output = subprocess.check_output(
            'su -c "pm grant com.termux android.permission.READ_EXTERNAL_STORAGE"',
            shell=True,  # nosec
            timeout=15,
        )
        _LOGGER.info(str(ret_output.decode("utf-8")))
        ret_output = subprocess.check_output(
            'su -c "pm grant com.termux android.permission.WRITE_EXTERNAL_STORAGE"',
            shell=True,  # nosec
            timeout=15,
        )
        _LOGGER.info(str(ret_output.decode("utf-8")))
    except Exception as e:
        _LOGGER.error(str(e))


def do_download_upgrade(hass, call):
    # get the version status from sensor
    state = hass.states.get(ENTITY_ID)
    attr = state.attributes
    reinstall_android_app = attr.get("reinstall_android_app", False)
    release_script = attr.get("release_script", "")

    # add the grant to save on sdcard
    if reinstall_android_app:
        grant_write_to_sdcard()

    # download release script
    _LOGGER.info("Release script " + str(release_script))
    try:
        file_script = str(os.path.dirname(__file__))
        file_script += "/scripts/release_script.sh"
        f = open(str(file_script), "w")
        if platform.machine() == "x86_64":
            f.write("#!/bin/sh" + os.linesep)
        else:
            f.write("#!/data/data/com.termux/files/usr/bin/sh" + os.linesep)
        for ln in release_script.split("-#-"):
            f.write(ln + os.linesep)
        f.close()
        # go next - execute the upgrade
        hass.services.call("ais_updater", "install_upgrade")
    except Exception as e:
        _LOGGER.error("Can't download release_script, error: " + str(e))
        hass.services.call(
            "ais_ai_service", "say_it", {"text": "Nie udało się pobrać aktualizacji."}
        )
        _set_update_status(hass, UPDATE_STATUS_UNKNOWN)


def do_fix_scripts_permissions():
    # fix permissions
    try:
        subprocess.check_output(
            "chmod -R 777 " + str(os.path.dirname(__file__)) + "/scripts/",
            shell=True,  # nosec
        )
    except Exception as e:
        _LOGGER.error("do_fix_scripts_permissions: " + str(e))


def do_install_upgrade(hass, call):
    # get the version status from sensor
    state = hass.states.get(ENTITY_ID)
    attr = state.attributes
    release_script = attr.get("release_script", "")

    # linux
    _LOGGER.info("We have release_script to execute " + str(release_script))
    try:
        do_fix_scripts_permissions()
        file_script = str(os.path.dirname(__file__))
        file_script += "/scripts/release_script.sh"
        apt_process = subprocess.Popen(
            file_script, shell=True, stdout=None, stderr=None  # nosec
        )
        apt_process.wait()
        _LOGGER.info("release_script, return: " + str(apt_process.returncode))
        if apt_process.returncode != 0:
            _set_update_status(hass, UPDATE_STATUS_UNKNOWN)
            _LOGGER.error(
                "Can't install release_script, returncode: "
                + str(apt_process.returncode)
            )
    except Exception as e:
        _LOGGER.error("Can't install release_script, error: " + str(e))


def do_applay_the_fix(hass, call):
    # fix script will not trust the info reported by Asystent domowy
    # fix have to check himself if the fix is needed or not
    if "fix_script" in call.data:
        fix_script = call.data["fix_script"]
    else:
        # get the version status from sensor
        state = hass.states.get(ENTITY_ID)
        attr = state.attributes
        fix_script = attr.get("fix_script", "")

    # save fix script
    if fix_script != "":
        _LOGGER.info("We have fix_script " + str(fix_script))
        try:
            file_script = str(os.path.dirname(__file__))
            file_script += "/scripts/fix_script.sh"
            f = open(str(file_script), "w")
            if platform.machine() == "x86_64":
                f.write("#!/bin/sh" + os.linesep)
            else:
                f.write("#!/data/data/com.termux/files/usr/bin/sh" + os.linesep)
            for ln in fix_script.split("-#-"):
                f.write(ln + os.linesep)
            f.close()

            # execute fix script
            try:
                do_fix_scripts_permissions()
                fix_process = subprocess.Popen(
                    file_script, shell=True, stdout=None, stderr=None  # nosec
                )
                fix_process.wait()
                _LOGGER.info("fix_script, return: " + str(fix_process.returncode))
            except Exception as e:
                _LOGGER.error("Can't execute fix_script, error: " + str(e))
        except Exception as e:
            _LOGGER.error("Can prepare fix_script, error: " + str(e))
    else:
        _LOGGER.info("No fix_script this time!")
