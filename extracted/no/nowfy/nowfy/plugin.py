import base64
import hashlib
import json
import os
import pkgutil
import random
import re
import requests
import threading
import time
import builtins as _py_builtins
from datetime import datetime
from PIL import Image, ImageFilter, ImageDraw
from java.util import Locale, ArrayList
from java.io import File
from java.lang import Class as JClass, Float as JFloat, Integer, Boolean
from java import dynamic_proxy, jarray, jint, jclass
from android.content import Intent
from android.net import Uri
from android.os import Build
from android.view import WindowManager, Gravity, View, MotionEvent
from android.util import TypedValue
from android.widget import TextView, LinearLayout, FrameLayout, ImageView, ScrollView
from android.graphics import Color, BitmapFactory, Canvas, Paint, SweepGradient, PorterDuff, PorterDuffColorFilter
from android.graphics.drawable import ShapeDrawable
from android.graphics.drawable.shapes import OvalShape
from android.graphics.drawable import GradientDrawable
from org.telegram.messenger import ApplicationLoader
from org.telegram.messenger import AndroidUtilities, ChatObject, MessageObject
from org.telegram.messenger import R
from org.telegram.ui.ActionBar import BottomSheet, Theme
from org.telegram.ui.Components import BackupImageView, AvatarDrawable, LayoutHelper
from org.telegram.ui import ChatActivity
from org.telegram.ui.Stories.recorder import ButtonWithCounterView
from com.exteragram.messenger.plugins import PluginsController
from com.exteragram.messenger.plugins.ui import PluginSettingsActivity
from ui.settings import Header, Divider, Input, Switch, Text, Selector
from ui.alert import AlertDialogBuilder
from ui.bulletin import BulletinHelper
from client_utils import get_send_messages_helper, run_on_queue, get_last_fragment, get_user_config, get_messages_controller, send_document
from android_utils import run_on_ui_thread, log, OnClickListener
from base_plugin import BasePlugin, HookResult, HookStrategy, MenuItemData, MenuItemType, MethodHook, hook_filters, HookFilter
from hook_utils import find_class, get_private_field, set_private_field
from .core import NowfyCore
from . import core as nowfycore

NOWFY_CORE_API = None
NOWFY_CORE_IMPORT_ERROR = None
NOWFY_CORE_BACKEND_MIXIN = object
try:
    NOWFY_CORE_API = nowfycore.get_nowfy_core_api()
    NOWFY_CORE_BACKEND_MIXIN = getattr(nowfycore, "NowfyCoreBackendMixin", object)
except Exception as _core_import_error:
    NOWFY_CORE_IMPORT_ERROR = _core_import_error
__id__ = "nowfy"
__name__ = "Nowfy"
__description__ = "Nowfy brings dynamic music cards, visual themes, and seamless integration with multiple music services to enhance the Now Playing experience in chat.\n\n• Powered by [Dotted Plugins](https://t.me/exteraDevPlugins)"
__author__ = "@AGeekApple"
__version__ = "1.1.6"
__min_version__ = "12.5.1"
__requirements__ = "nowfy"
__icon__ = "ApplePlugins/23"
__priority__ = 100
GEEKSTATS_BASE = "https://geekstats.meyankut.workers.dev"
GEEKSTATS_INGEST_URL = f"{GEEKSTATS_BASE}/v1/ingest"
GEEKSTATS_INGEST_TOKEN = ""


def _get_private_field_silent(obj, name, default=None):
    try:
        if obj is None or not name:
            return default
        cls = obj.getClass()
        while cls is not None:
            try:
                f = cls.getDeclaredField(name)
                f.setAccessible(True)
                return f.get(obj)
            except Exception:
                pass
            try:
                cls = cls.getSuperclass()
            except Exception:
                cls = None
        return default
    except Exception:
        return default

class NowfySettingsHeaderHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin
    @hook_filters(HookFilter.Condition("param.thisObject != null"), HookFilter.ArgumentNotNull(0))
    def after_hooked_method(self, param):
        try:
            activity = param.thisObject
            items = param.args[0]
            if not items or items.size() == 0:
                return
            plugin_obj = get_private_field(activity, "plugin")
            if not plugin_obj:
                return
            plugin_id = str(plugin_obj.getId())
            if plugin_id not in ("nowfy", "nowfycore"):
                return
            try:
                self.plugin._apply_link_aliases(items)
            except Exception:
                pass
            if plugin_id == "nowfycore":
                try:
                    self.plugin._inject_nowfycore_theme_multiselect(activity, items)
                except Exception:
                    pass
                return
            callback = get_private_field(activity, "createSubFragmentCallback")
            is_main_settings = callback is None
            is_flow_callback_direct = False
            flow_header_inserted = False
            is_themes_settings = False
            is_services_settings = False
            is_spotify_settings = False
            is_lastfm_settings = False
            is_statsfm_settings = False
            is_statsfm_top_settings = False
            is_ymusic_settings = False
            is_extended_settings = False
            is_flow_settings = False
            is_home_cover_settings = False
            is_nowtab_settings = False
            is_track_hub_settings = False
            is_link_options_settings = False
            is_panel_settings = False
            is_vinify_ui_settings = False
            is_about_settings = False
            is_core_settings = False
            if callback:
                cb_name = None
                try:
                    cb_name = getattr(callback, "__name__", None)
                except Exception:
                    cb_name = None
                if callback == self.plugin.create_themes_subfragment:
                    is_themes_settings = True
                if callback == self.plugin.create_services_subfragment:
                    is_services_settings = True
                if callback == self.plugin.create_spotify_credentials_subfragment:
                    is_spotify_settings = True
                if callback == self.plugin.create_lastfm_credentials_subfragment:
                    is_lastfm_settings = True
                if callback == self.plugin.create_statsfm_credentials_subfragment:
                    is_statsfm_settings = True
                if hasattr(self.plugin, "create_ymusic_credentials_subfragment") and callback == self.plugin.create_ymusic_credentials_subfragment:
                    is_ymusic_settings = True
                if hasattr(self.plugin, "create_statsfm_top_subfragment") and callback == self.plugin.create_statsfm_top_subfragment:
                    is_statsfm_settings = True
                    is_statsfm_top_settings = True
                if cb_name == "create_lastfm_credentials_subfragment":
                    is_lastfm_settings = True
                if cb_name == "create_statsfm_credentials_subfragment":
                    is_statsfm_settings = True
                if cb_name == "create_statsfm_top_subfragment":
                    is_statsfm_settings = True
                    is_statsfm_top_settings = True
                if cb_name == "create_ymusic_credentials_subfragment":
                    is_ymusic_settings = True
                if callback == self.plugin.create_extended_subfragment:
                    is_extended_settings = True
                if hasattr(self.plugin, "create_extended_flow_subfragment") and callback == self.plugin.create_extended_flow_subfragment:
                    is_flow_settings = True
                    is_flow_callback_direct = True
                if hasattr(self.plugin, "create_extended_home_cover_subfragment") and callback == self.plugin.create_extended_home_cover_subfragment:
                    is_home_cover_settings = True
                if callback == self.plugin.create_extended_tab_subfragment:
                    is_nowtab_settings = True
                if callback == self.plugin.create_track_hub_subfragment:
                    is_track_hub_settings = True
                if callback == self.plugin.create_link_options_subfragment:
                    is_link_options_settings = True
                if callback == self.plugin.create_vinify_ui_options:
                    is_vinify_ui_settings = True
                if hasattr(self.plugin, "create_vinify_background_subfragment") and callback == self.plugin.create_vinify_background_subfragment:
                    is_vinify_ui_settings = True
                if hasattr(self.plugin, "create_vinify_logo_subfragment") and callback == self.plugin.create_vinify_logo_subfragment:
                    is_vinify_ui_settings = True
                if cb_name == "create_vinify_ui_options":
                    is_vinify_ui_settings = True
                if cb_name == "create_vinify_background_subfragment":
                    is_vinify_ui_settings = True
                if cb_name == "create_vinify_logo_subfragment":
                    is_vinify_ui_settings = True
                if callback == self.plugin.create_nowfy_panel_subfragment:
                    is_panel_settings = True
                if callback == self.plugin.create_about_plugin_subfragment:
                    is_about_settings = True
                if hasattr(self.plugin, "create_nowfy_core_subfragment") and callback == self.plugin.create_nowfy_core_subfragment:
                    is_core_settings = True
                if cb_name == "create_nowfy_core_subfragment":
                    is_core_settings = True
                if cb_name == "create_extended_home_cover_subfragment":
                    is_home_cover_settings = True
                if cb_name == "create_extended_flow_subfragment":
                    is_flow_settings = True
                    is_flow_callback_direct = True
            if not is_lastfm_settings:
                try:
                    for i in range(items.size()):
                        it = items.get(i)
                        k = self.plugin._get_uitem_setting_key(it)
                        if k in ("lastfm_username", "lastfm_api_key", "current_player"):
                            is_lastfm_settings = True
                            break
                except Exception:
                    pass
            if not is_statsfm_settings:
                try:
                    for i in range(items.size()):
                        it = items.get(i)
                        k = self.plugin._get_uitem_setting_key(it)
                        if k in ("statsfm_username", "statsfm_source_player"):
                            is_statsfm_settings = True
                            break
                except Exception:
                    pass
            if not is_services_settings:
                try:
                    svc_hits = 0
                    for i in range(items.size()):
                        it = items.get(i)
                        k = self.plugin._get_uitem_setting_key(it)
                        if k in ("nowfy_services_spotify", "nowfy_services_lastfm", "nowfy_services_statsfm", "nowfy_services_ymusic"):
                            is_services_settings = True
                            break
                        try:
                            si = getattr(it, "settingItem", None)
                            txt = str(getattr(si, "text", "") or "").strip().lower() if si else ""
                        except Exception:
                            txt = ""
                        if txt in ("spotify", "last.fm", "stats.fm", "yandex music", "ymusic"):
                            svc_hits += 1
                    if not is_services_settings and svc_hits >= 2:
                        is_services_settings = True
                except Exception:
                    pass
            if not is_ymusic_settings:
                try:
                    for i in range(items.size()):
                        it = items.get(i)
                        k = self.plugin._get_uitem_setting_key(it)
                        if k in ("ymusic_api_token",):
                            is_ymusic_settings = True
                            break
                except Exception:
                    pass
            if not is_flow_settings:
                try:
                    for i in range(items.size()):
                        it = items.get(i)
                        k = str(self.plugin._get_uitem_setting_key(it) or "").strip().lower()
                        la = str(getattr(it, "link_alias", "") or "").strip().lower()
                        txt = str(self.plugin._get_uitem_text(it) or "").strip().lower()
                        if (
                            k in ("nowfy_flow_enabled", "nowfy_flow_side", "nowfy_flow_transparency")
                            or "nowfy_flow" in k
                            or "nowfy_flow" in la
                            or txt in ("nowfy flow", "flow position in chat", "flow transparency")
                        ):
                            is_flow_settings = True
                            break
                except Exception:
                    pass
            if not is_main_settings and not is_themes_settings and not is_services_settings and not is_spotify_settings and not is_lastfm_settings and not is_statsfm_settings and not is_ymusic_settings and not is_extended_settings and not is_flow_settings and not is_home_cover_settings and not is_nowtab_settings and not is_track_hub_settings and not is_link_options_settings and not is_panel_settings and not is_vinify_ui_settings and not is_about_settings and not is_core_settings:
                return
            if is_core_settings:
                try:
                    self.plugin._inject_nowfycore_theme_multiselect(activity, items)
                except Exception:
                    pass
            if is_extended_settings:
                try:
                    self.plugin._extended_settings_activity = activity
                except Exception:
                    pass
                try:
                    self.plugin._inject_custom_cover_slide(activity, items)
                except Exception:
                    pass
                try:
                    self.plugin._inject_nowfy_pulse_style_slide(activity, items)
                except Exception:
                    pass
            if is_home_cover_settings:
                try:
                    self.plugin._inject_custom_cover_slide(activity, items)
                except Exception:
                    pass
            if is_themes_settings:
                try:
                    self.plugin._themes_settings_activity = activity
                except Exception:
                    pass
                try:
                    self.plugin._inject_theme_skin_slides(activity, items)
                except Exception:
                    pass
                try:
                    self.plugin._inject_font_favorites_expandable(activity, items)
                except Exception:
                    pass
            if is_nowtab_settings:
                try:
                    self.plugin._inject_nowtab_buttons_expandable(activity, items)
                except Exception:
                    pass
                try:
                    self.plugin._inject_nowtab_lyrics_autoscroll_slide(activity, items)
                except Exception:
                    pass
                try:
                    self.plugin._inject_nowtab_control_style_slide(activity, items)
                except Exception:
                    pass
                try:
                    self.plugin._inject_nowfy_flow_side_slide(activity, items)
                except Exception:
                    pass
                try:
                    self.plugin._inject_nowfy_flow_transparency_slide(activity, items)
                except Exception:
                    pass
            if is_flow_callback_direct:
                try:
                    from org.telegram.ui.Components import UItem
                    if activity and hasattr(activity, "getContext"):
                        flow_header = self.plugin._criar_visualizacao_cabecalho_nowfy_flow(activity.getContext())
                    else:
                        flow_header = None
                    if flow_header:
                        try:
                            from com.exteragram.messenger.plugins.models import HeaderSetting
                            hi = UItem.asCustom(flow_header)
                            hi.settingItem = HeaderSetting("nowfy_header_flow")
                        except Exception:
                            hi = UItem.asCustom(flow_header)
                        try:
                            hi.setTransparent(True)
                        except Exception:
                            pass
                        items.add(0, hi)
                        items.add(1, UItem.asShadow())
                        flow_header_inserted = True
                except Exception:
                    pass
                try:
                    self.plugin._inject_nowfy_flow_style_buttons(activity, items)
                except Exception:
                    pass
                try:
                    self.plugin._inject_nowfy_flow_side_slide(activity, items)
                except Exception:
                    pass
                try:
                    self.plugin._inject_nowfy_flow_transparency_slide(activity, items)
                except Exception:
                    pass
            elif is_flow_settings:
                try:
                    self.plugin._inject_nowfy_flow_style_buttons(activity, items)
                except Exception:
                    pass
                try:
                    self.plugin._inject_nowfy_flow_side_slide(activity, items)
                except Exception:
                    pass
                try:
                    self.plugin._inject_nowfy_flow_transparency_slide(activity, items)
                except Exception:
                    pass
            if is_track_hub_settings:
                try:
                    if self.plugin._core_addon_enabled("addon_track_hub_enabled", False):
                        self.plugin._inject_track_hub_source_slide(activity, items)
                except Exception:
                    pass
            if is_link_options_settings:
                try:
                    self.plugin._inject_link_options_slide(activity, items)
                except Exception:
                    pass
            if is_vinify_ui_settings:
                try:
                    self.plugin._inject_vinify_cover_shape_slide(activity, items)
                except Exception:
                    pass
            if is_panel_settings:
                pass
            if is_main_settings:
                pass
            if is_spotify_settings:
                try:
                    self.plugin._spotify_settings_activity = activity
                except Exception:
                    pass
                try:
                    self.plugin._inject_spotify_connect_custom(activity, items)
                except Exception:
                    pass
            if is_statsfm_settings:
                try:
                    self.plugin._statsfm_settings_activity = activity
                except Exception:
                    pass
                try:
                    self.plugin._inject_statsfm_profile_custom(activity, items)
                except Exception:
                    pass
            if is_ymusic_settings:
                try:
                    self.plugin._inject_ymusic_profile_custom(activity, items)
                except Exception:
                    pass
            if is_lastfm_settings:
                try:
                    self.plugin._inject_lastfm_profile_custom(activity, items)
                except Exception:
                    pass
            if is_services_settings:
                try:
                    self.plugin._inject_services_cards_custom(activity, items)
                except Exception:
                    pass
            is_home_like = bool(is_main_settings)
            if not is_home_like:
                try:
                    for _ix in range(items.size()):
                        _it = items.get(_ix)
                        _la = str(getattr(_it, "link_alias", "") or "")
                        _k = str(self.plugin._get_uitem_setting_key(_it) or "")
                        if _la in ("nowfy_credit_dotted", "nowfy_about_subfragment", "nowfy_home_meta") or _k in ("nowfy_credit_dotted", "nowfy_about_subfragment", "nowfy_home_meta"):
                            is_home_like = True
                            break
                except Exception:
                    pass
            if is_home_like:
                try:
                    self.plugin._inject_home_meta_custom(items, activity)
                except Exception:
                    pass
                try:
                    self.plugin._inject_home_services_entry_custom(activity, items)
                except Exception:
                    pass
            if is_about_settings:
                try:
                    if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_about_support_rich_header"):
                        NOWFY_CORE_API.inject_about_support_rich_header(self.plugin, activity, items)
                except Exception:
                    pass
            header = None
            if is_home_like:
                header = self.plugin._criar_visualizacao_cabecalho(activity.getContext())
            elif is_themes_settings:
                header = self.plugin._criar_visualizacao_cabecalho_temas(activity.getContext())
            elif is_services_settings:
                header = None
            elif is_spotify_settings:
                header = self.plugin._criar_visualizacao_cabecalho_spotify(activity.getContext())
            elif is_lastfm_settings:
                header = self.plugin._criar_visualizacao_cabecalho_lastfm(activity.getContext())
            elif is_statsfm_top_settings:
                header = None
            elif is_statsfm_settings:
                header = self.plugin._criar_visualizacao_cabecalho_statsfm(activity.getContext())
            elif is_ymusic_settings:
                header = None
            elif is_nowtab_settings:
                header = self.plugin._criar_visualizacao_cabecalho_nowtab(activity.getContext())
            elif is_flow_callback_direct:
                header = self.plugin._criar_visualizacao_cabecalho_nowfy_flow(activity.getContext())
            if header and not flow_header_inserted:
                from org.telegram.ui.Components import UItem
                try:
                    from com.exteragram.messenger.plugins.models import HeaderSetting
                    item = UItem.asCustom(header)
                    item.settingItem = HeaderSetting("nowfy_header")
                except Exception:
                    item = UItem.asCustom(header)
                try:
                    item.setTransparent(True)
                except Exception:
                    pass
                items.add(0, item)
                items.add(1, UItem.asShadow())
        except Exception:
            pass

class NowfyFontPickerHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin

    def before_hooked_method(self, param):
        try:
            font_active = bool(getattr(self.plugin, "_font_picker_active", False))
            backup_active = bool(getattr(self.plugin, "_backup_picker_active", False))
            cover_active = bool(getattr(self.plugin, "_custom_cover_picker_active", False))
            cover_crop_active = bool(getattr(self.plugin, "_custom_cover_crop_active", False))
            if not font_active and not backup_active and not cover_active and not cover_crop_active:
                return
            req_code, res_code, data = param.args
            if backup_active:
                if req_code == getattr(self.plugin, "_backup_picker_request", -1):
                    param.setResult(None)
                    self.plugin._handle_backup_picker_result(res_code, data)
                    return
            if cover_active:
                if req_code == getattr(self.plugin, "_custom_cover_picker_request", -1):
                    param.setResult(None)
                    self.plugin._handle_custom_cover_picker_result(res_code, data)
                    return
            if cover_crop_active:
                if req_code == getattr(self.plugin, "_custom_cover_crop_request", -1):
                    param.setResult(None)
                    self.plugin._handle_custom_cover_crop_result(res_code, data)
                    return
            if font_active and req_code == getattr(self.plugin, "_font_picker_request", -1):
                param.setResult(None)
                self.plugin._handle_font_picker_result(res_code, data)
        except Exception:
            pass

class NowfyBackupOpenFileHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin

    def before_hooked_method(self, param):
        try:
            if not param or not hasattr(param, "args") or not param.args:
                return
            file_obj = param.args[0]
            if not file_obj:
                return
            path = ""
            try:
                path = str(file_obj.getAbsolutePath() or "")
            except Exception:
                path = str(file_obj or "")
            if not path or not path.lower().endswith(".nowfy"):
                return
            handled = False
            try:
                if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "run_backup_file_restore"):
                    handled = bool(NOWFY_CORE_API.run_backup_file_restore(self.plugin, path))
            except Exception:
                handled = False
            if handled:
                try:
                    param.setResult(True)
                except Exception:
                    pass
        except Exception:
            pass

class NowfyChatFabCreateViewHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin

    def after_hooked_method(self, param):
        try:
            fragment = param.thisObject
            try:
                run_on_ui_thread(lambda: self.plugin._sync_home_actionbar_shortcut(fragment))
            except Exception:
                pass
            try:
                if isinstance(fragment, ChatActivity):
                    run_on_ui_thread(lambda: self.plugin._attach_chat_quick_share_button(fragment))
            except Exception:
                pass
            try:
                flow_enabled = bool(self.plugin.get_setting("fab_chat_enabled", False))
            except Exception:
                flow_enabled = False
            try:
                quick_list_enabled = bool(self.plugin._is_quick_flow_list_enabled())
            except Exception:
                quick_list_enabled = False
            if (not flow_enabled) and (not quick_list_enabled):
                return
            run_on_ui_thread(lambda: self.plugin._attach_chat_fab(fragment))
        except Exception:
            pass

class NowfyChatFabResumeHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin

    def after_hooked_method(self, param):
        try:
            fragment = param.thisObject
            try:
                run_on_ui_thread(lambda: self.plugin._sync_home_actionbar_shortcut(fragment))
            except Exception:
                pass
            try:
                if isinstance(fragment, ChatActivity):
                    run_on_ui_thread(lambda: self.plugin._attach_chat_quick_share_button(fragment))
            except Exception:
                pass
            try:
                flow_enabled = bool(self.plugin.get_setting("fab_chat_enabled", False))
            except Exception:
                flow_enabled = False
            try:
                quick_list_enabled = bool(self.plugin._is_quick_flow_list_enabled())
            except Exception:
                quick_list_enabled = False
            if (not flow_enabled) and (not quick_list_enabled):
                return
            run_on_ui_thread(lambda: self.plugin._attach_chat_fab(fragment))
        except Exception:
            pass

class NowfyDrawerResumeHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin

    def after_hooked_method(self, param):
        try:
            if bool(self.plugin.get_setting("nowfy_drawer_enabled", False)):
                self.plugin._ensure_nowfy_drawer_item()
            else:
                self.plugin._remove_nowfy_drawer_item()
        except Exception:
            pass

class NowfyPanelRoundCheckboxClickHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin

    def before_hooked_method(self, param):
        try:
            item = param.args[0]
            view = param.args[1]
            if not item:
                return
            activity = param.thisObject
            callback = get_private_field(activity, "createSubFragmentCallback")
            cb_name = None
            try:
                cb_name = getattr(callback, "__name__", None)
            except Exception:
                cb_name = None
            key = str(getattr(item, "object2", "") or "")
            try:
                plugin_obj = get_private_field(activity, "plugin")
                _pid = str(plugin_obj.getId()) if plugin_obj else ""
            except Exception:
                _pid = ""
            is_core_settings_context = (_pid == "nowfycore") or (callback == getattr(self.plugin, "create_nowfy_core_subfragment", None)) or (cb_name == "create_nowfy_core_subfragment")
            if is_core_settings_context:
                if key == "__core_themes_parent__":
                    expanded = bool(getattr(self.plugin, "_core_theme_expand_expanded", False))
                    self.plugin._core_theme_expand_expanded = (not expanded)
                    try:
                        item.setCollapsed(expanded)
                    except Exception:
                        pass
                    try:
                        list_view = get_private_field(activity, "listView")
                        if list_view and hasattr(list_view, "adapter"):
                            self.plugin._request_settings_list_update(list_view, channel="core_theme_expand")
                    except Exception:
                        pass
                    param.setResult(None)
                    return
                if key.startswith("coretheme_"):
                    tkey = key.replace("coretheme_", "", 1).strip().lower()
                    enabled = set(self.plugin._get_core_enabled_optional_themes())
                    if tkey in enabled:
                        enabled.remove(tkey)
                        new_val = False
                    else:
                        enabled.add(tkey)
                        new_val = True
                    self.plugin._set_core_enabled_optional_themes(enabled)
                    try:
                        self.plugin.reload_settings()
                    except Exception:
                        pass
                    try:
                        list_view = get_private_field(activity, "listView")
                        if list_view and hasattr(list_view, "adapter"):
                            self.plugin._request_settings_list_update(list_view, channel="core_theme_toggle")
                    except Exception:
                        pass
                    try:
                        item.setChecked(bool(new_val))
                    except Exception:
                        pass
                    try:
                        CheckBoxCell = find_class("org.telegram.ui.Cells.CheckBoxCell")
                        if CheckBoxCell and isinstance(view, CheckBoxCell):
                            view.setChecked(bool(new_val), True)
                    except Exception:
                        pass
                    try:
                        param.setResult(bool(new_val))
                    except Exception:
                        param.setResult(None)
                    return
                return
            if callback == self.plugin.create_extended_tab_subfragment:
                if key == "__nowtab_buttons_parent__":
                    expanded = bool(getattr(self.plugin, "_nowtab_buttons_expanded", False))
                    self.plugin._nowtab_buttons_expanded = (not expanded)
                    try:
                        item.setCollapsed(expanded)
                    except Exception:
                        pass
                    try:
                        list_view = get_private_field(activity, "listView")
                        if list_view and hasattr(list_view, "adapter"):
                            self.plugin._request_settings_list_update(list_view, channel="nowtab_buttons_expand")
                    except Exception:
                        pass
                    param.setResult(None)
                    return
                if key == "nowfy_lyrics_button":
                    current = int(self.plugin.get_setting("nowfy_lyrics_button", 1) or 0)
                    new_val = 0 if current == 1 else 1
                    self.plugin.set_setting("nowfy_lyrics_button", new_val)
                elif key == "nowfy_embed_button":
                    current = int(self.plugin.get_setting("nowfy_embed_button", 1) or 0)
                    new_val = 0 if current == 1 else 1
                    self.plugin.set_setting("nowfy_embed_button", new_val)
                elif key == "nowfy_control_enabled":
                    current = bool(self.plugin.get_setting("nowfy_control_enabled", False))
                    new_val = not current
                    self.plugin.set_setting("nowfy_control_enabled", new_val)
                elif key == "nowfy_music_preview_button":
                    current = int(self.plugin.get_setting("nowfy_music_preview_button", 1) or 0)
                    new_val = 0 if current == 1 else 1
                    self.plugin.set_setting("nowfy_music_preview_button", new_val)
                elif key == "nowfy_track_download_button":
                    current = int(self.plugin.get_setting("nowfy_track_download_button", 1) or 0)
                    new_val = 0 if current == 1 else 1
                    self.plugin.set_setting("nowfy_track_download_button", new_val)
                else:
                    return
                try:
                    self.plugin._rebuild_nowfy_tab_current_emoji()
                except Exception:
                    pass
            elif callback == self.plugin.create_themes_subfragment or callback == self.plugin.create_vinify_ui_options or cb_name == "create_vinify_ui_options":
                try:
                    la = str(getattr(item, "link_alias", "") or "")
                except Exception:
                    la = ""
                if la == "nowfy_themes_font_upload":
                    try:
                        self.plugin._trace_font_bridge("hook click: nowfy_themes_font_upload")
                    except Exception:
                        pass
                    try:
                        self.plugin._open_font_upload_from_main()
                    except Exception:
                        pass
                    param.setResult(None)
                    return
                if la == "nowfy_themes_font_manage":
                    try:
                        self.plugin._trace_font_bridge("hook click: nowfy_themes_font_manage")
                    except Exception:
                        pass
                    try:
                        self.plugin._open_font_manager_from_main()
                    except Exception:
                        pass
                    param.setResult(None)
                    return
                if key == "__font_random_favorites_parent__":
                    expanded = bool(getattr(self.plugin, "_font_favorites_expanded", False))
                    self.plugin._font_favorites_expanded = (not expanded)
                    try:
                        item.setCollapsed(expanded)
                    except Exception:
                        pass
                    try:
                        list_view = get_private_field(activity, "listView")
                        if list_view and hasattr(list_view, "adapter"):
                            self.plugin._request_settings_list_update(list_view, channel="font_favorites_expand")
                    except Exception:
                        pass
                    param.setResult(None)
                    return
                elif key.startswith("fontfav_"):
                    try:
                        fav_idx = int(key.split("_", 1)[1])
                    except Exception:
                        return
                    favs = set(self.plugin._get_font_random_favorites())
                    if fav_idx in favs:
                        favs.remove(fav_idx)
                        new_val = False
                    else:
                        favs.add(fav_idx)
                        new_val = True
                    self.plugin._set_font_random_favorites(sorted(favs))
                    try:
                        self.plugin.reload_settings()
                    except Exception:
                        pass
                else:
                    return
            elif callback == self.plugin.create_myconfigs_subfragment or cb_name == "create_myconfigs_subfragment":
                try:
                    la = str(getattr(item, "link_alias", "") or "")
                except Exception:
                    la = ""
                if la == "nowfy_myconfigs_backup_upload":
                    try:
                        self.plugin._trace_font_bridge("hook click: nowfy_myconfigs_backup_upload")
                    except Exception:
                        pass
                    try:
                        self.plugin._open_backup_upload_from_main()
                    except Exception:
                        pass
                    param.setResult(None)
                    return
                return
            elif callback == self.plugin.create_extended_subfragment or cb_name == "create_extended_subfragment" or (hasattr(self.plugin, "create_extended_home_cover_subfragment") and callback == self.plugin.create_extended_home_cover_subfragment) or cb_name == "create_extended_home_cover_subfragment":
                try:
                    la = str(getattr(item, "link_alias", "") or "")
                except Exception:
                    la = ""
                if la == "nowfy_extended_custom_cover_upload":
                    try:
                        self.plugin._trace_font_bridge("hook click: nowfy_extended_custom_cover_upload")
                    except Exception:
                        pass
                    try:
                        self.plugin._open_custom_cover_upload_from_main()
                    except Exception:
                        pass
                    param.setResult(None)
                    return
                return
            elif callback == self.plugin.create_statsfm_credentials_subfragment or cb_name == "create_statsfm_credentials_subfragment":
                if key == "__statsfm_profile_custom__":
                    try:
                        current_user = str(self.plugin.get_setting("statsfm_username", "") or "").strip()
                    except Exception:
                        current_user = ""
                    if not current_user:
                        try:
                            run_on_ui_thread(lambda: self.plugin._show_statsfm_username_input_dialog())
                        except Exception:
                            pass
                    param.setResult(None)
                    return
                if key == "__statsfm_logout_text_item__":
                    try:
                        self.plugin._perform_statsfm_logout()
                        try:
                            list_view = get_private_field(activity, "listView")
                            if list_view and hasattr(list_view, "adapter"):
                                self.plugin._request_settings_list_update(list_view, channel="statsfm_logout")
                            else:
                                self.plugin.reload_settings()
                        except Exception:
                            self.plugin.reload_settings()
                    except Exception:
                        pass
                    param.setResult(None)
                    return
                return
            elif callback == self.plugin.create_spotify_credentials_subfragment or cb_name == "create_spotify_credentials_subfragment":
                if key == "__spotify_profile_custom__":
                    try:
                        st = self.plugin._get_quick_spotify_state()
                        if not st.get("connected", False) or st.get("force_renew", False) or st.get("expired", True):
                            self.plugin._start_quick_spotify_connect()
                            try:
                                self.plugin._refresh_spotify_settings_ui()
                            except Exception:
                                pass
                    except Exception:
                        pass
                    param.setResult(None)
                    return
                if key == "__spotify_connect_action__":
                    try:
                        st = self.plugin._get_quick_spotify_state()
                        if st.get("connected", False) and not st.get("force_renew", False) and not st.get("expired", True):
                            self.plugin._show_quick_renew_dialog()
                        else:
                            self.plugin._start_quick_spotify_connect()
                        try:
                            self.plugin._refresh_spotify_settings_ui()
                        except Exception:
                            pass
                    except Exception:
                        pass
                    param.setResult(None)
                    return
                if key == "__spotify_confirmation_code_item__":
                    try:
                        run_on_ui_thread(lambda: self.plugin._show_spotify_confirmation_code_dialog())
                    except Exception:
                        try:
                            self.plugin._show_spotify_confirmation_code_dialog()
                        except Exception:
                            pass
                    param.setResult(None)
                    return
                return
            else:
                return
            try:
                item.setChecked(new_val)
            except Exception:
                pass
            try:
                CheckBoxCell = find_class("org.telegram.ui.Cells.CheckBoxCell")
                if CheckBoxCell and isinstance(view, CheckBoxCell):
                    view.setChecked(new_val, True)
            except Exception:
                pass
            try:
                list_view = get_private_field(activity, "listView")
                if list_view and hasattr(list_view, "adapter"):
                    self.plugin._request_settings_list_update(list_view, channel="checkbox_final")
            except Exception:
                pass
            param.setResult(None)
        except Exception:
            pass
NOWFY_TAB_INDEX = 3
NOWFY_TAB_VIEW_TAG = "NOWFY_CUSTOM_TAB_VIEW_TAG"
ICON_HEADPHONES = "https://assets.nowfy/nowfy_np.png"
ICON_GEAR = "https://assets.nowfy/nowfy_gr.png"
ICON_CONTROL_PLAY = "https://assets.nowfy/player_play.png"
ICON_CONTROL_PAUSE = "https://assets.nowfy/player_pause.png"
ICON_CONTROL_BACK = "https://assets.nowfy/player_skip_back.png"
ICON_CONTROL_SKIP = "https://assets.nowfy/player_skip_forward.png"
ICON_CONTROL_SEARCH = "https://assets.nowfy/search_2.png"
ICON_CONTROL_VOL_MINUS = "https://assets.nowfy/volless.png"
ICON_CONTROL_VOL_PLUS = "https://assets.nowfy/volmore.png"
ICON_CONTROL_TAB = "https://assets.nowfy/control_2.png"
ICON_SETTINGS_TAB_CONTROL = "https://assets.nowfy/nowfy_settings.png"
ICON_LYRICS_BUTTON = "https://assets.nowfy/lyrics.png"
ICON_LINK_BUTTON = "https://assets.nowfy/link.png"
ICON_MUSIC_PREVIEW_BUTTON = "https://assets.nowfy/music-preview.png"
ICON_TRACK_DOWNLOAD_BUTTON = "https://assets.nowfy/download.png"
ICON_EXTENDED_HEADER = "https://assets.nowfy/extended.png"
ICON_EXTENDED_HEADER_LIGHT = "https://assets.nowfy/extended-dark.png"
HEADER_FALLBACK_COVERS = [
    "https://assets.nowfy/etgpaper1.png",
]

def get_java_class(name):
    try:
        return JClass.forName(name)
    except Exception:
        return None

def find_constructor_exact(clazz, *params):
    try:
        ctor = clazz.getDeclaredConstructor(*params)
        ctor.setAccessible(True)
        return ctor
    except Exception:
        return None

def find_method_exact(clazz, name, *params):
    try:
        m = clazz.getDeclaredMethod(name, *params)
        m.setAccessible(True)
        return m
    except Exception:
        return None

def _create_nowfy_tab_button(context, text, subtext, enabled, listener, tonal=True):
    if text == "":
        return None
    button = ButtonWithCounterView(context, tonal, None)
    button.setText(text, False)
    if subtext:
        button.setSubText(subtext, False)
    button.setEnabled(enabled)
    if button.isEnabled() and listener is not None:
        button.setOnClickListener(listener)
    return button

def create_nowfy_tab_view(context, plugin):
    _fab_sheet_mode = bool(getattr(plugin, "_fab_force_apple_tab", False))
    _control_only_mode = False
    try:
        _control_only_mode = bool(getattr(plugin, "_fab_open_control_page", False))
    except Exception:
        _control_only_mode = False
    _flow_compact_mode = False
    try:
        _flow_compact_mode = bool(_fab_sheet_mode and str(plugin.get_setting("nowfy_flow_card_mode", "cc") or "cc").strip().lower() == "cc")
    except Exception:
        _flow_compact_mode = False
    _tab_feedback = {"busy": False, "no_track": False, "no_track_until": 0.0}
    _chatlist_flow_mode = False
    try:
        _chatlist_flow_mode = bool(_fab_sheet_mode and getattr(plugin, "_fab_chatlist_mode", False))
    except Exception:
        _chatlist_flow_mode = False
    _control_state = {"is_playing": False}
    _page_state = {"index": 0}
    _control_enabled = bool(plugin.get_setting("nowfy_control_enabled", False))
    _control_allowed = False
    try:
        _active_player = str(plugin._detect_current_player() or "").strip().lower()
        _control_allowed = (_active_player == "spotify")
    except Exception:
        _control_allowed = False
    if not _control_allowed:
        try:
            _sources_ctrl, _labels_ctrl = plugin._get_tab_source_options()
            _idx_ctrl = int(plugin.get_setting("nowfy_tab_source", 0) or 0)
            if isinstance(_sources_ctrl, list) and _sources_ctrl:
                if _idx_ctrl < 0 or _idx_ctrl >= len(_sources_ctrl):
                    _idx_ctrl = 0
                _src_ctrl = str(_sources_ctrl[_idx_ctrl] or "").strip().lower()
                _control_allowed = (_src_ctrl in ("spotify", "statsfm"))
        except Exception:
            pass
    _control_enabled = bool(_control_enabled and _control_allowed)
    try:
        if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "get_nowtab_control_style"):
            _control_style = int(NOWFY_CORE_API.get_nowtab_control_style(plugin))
        else:
            _control_style = int(plugin.get_setting("nowfy_control_style", 0) or 0)
    except Exception:
        _control_style = 0
    if _control_style < 0 or _control_style > 1:
        _control_style = 0
    _control_tab_icon_url = ICON_CONTROL_TAB
    try:
        if bool(getattr(plugin, "_fab_force_apple_tab", False)):
            _tab_style = 0
        else:
            _tab_style = int(plugin.get_setting("nowfy_tab_style", 0) or 0)
    except Exception:
        _tab_style = 0
    if _tab_style < 0 or _tab_style > 1:
        _tab_style = 0
    _use_focus_style = (_tab_style == 0)
    _is_apple_style = (_tab_style == 0)
    _nowplay_meta = {
        "sub_view": None,
        "default_sub": tr("nowfy_tab_card_now_sub"),
        "request_id": 0
    }
    _primary_stroke = Color.parseColor("#5AA78BFF")
    _primary_stroke_pressed = Color.parseColor("#88C8B2FF")
    _secondary_stroke = Color.parseColor("#3A4668")
    _secondary_stroke_pressed = Color.parseColor("#4A5B8C")
    status = None
    hello = None
    avatar = None
    focus_cover = None
    status_glow_bg = None
    def _can_send_now_card(fragment_obj):
        try:
            if not isinstance(fragment_obj, ChatActivity):
                return False
            chat = getattr(fragment_obj, "currentChat", None)
            if chat is None:
                return True
            try:
                if not bool(ChatObject.canSendPhoto(chat)):
                    return False
            except Exception:
                return False
            try:
                if bool(ChatObject.isChannel(chat)) and not bool(getattr(chat, "megagroup", False)):
                    if hasattr(ChatObject, "canPost"):
                        return bool(ChatObject.canPost(chat))
                    if bool(getattr(chat, "creator", False)):
                        return True
                    rights = getattr(chat, "admin_rights", None)
                    return bool(rights is not None and bool(getattr(rights, "post_messages", False)))
            except Exception:
                pass
            return True
        except Exception:
            return False
    def _get_tab_source_key_safe():
        try:
            _srcs, _lbls = plugin._get_tab_source_options()
            _idx = int(plugin.get_setting("nowfy_tab_source", 0) or 0)
            if not isinstance(_srcs, list) or not _srcs:
                return ""
            if _idx < 0 or _idx >= len(_srcs):
                _idx = 0
            return str(_srcs[_idx] or "").strip().lower()
        except Exception:
            return ""
    def _is_like_supported_source():
        try:
            return _get_tab_source_key_safe() in ("spotify", "statsfm")
        except Exception:
            return False
    def _extract_title_artist(track_obj):
        try:
            if not isinstance(track_obj, dict):
                return "", ""
            title = str(track_obj.get("name") or track_obj.get("title") or "").strip()
            artist = track_obj.get("artist")
            if isinstance(artist, dict):
                artist = str(artist.get("#text") or "").strip()
            elif isinstance(artist, list):
                artist = ", ".join([str(x).strip() for x in artist if str(x).strip()])
            else:
                artist = str(artist or "").strip()
            return title, artist
        except Exception:
            return "", ""
    def _spotify_headers():
        try:
            token = plugin._get_access_token(show_error_bulletin=False)
        except Exception:
            try:
                token = plugin._get_access_token()
            except Exception:
                token = None
        if not token:
            return None
        return {"Authorization": f"Bearer {token}"}
    def _spotify_current_track_id(headers):
        try:
            resp = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers, timeout=6)
            if int(getattr(resp, "status_code", 0) or 0) != 200 or not resp.content:
                return None
            data = resp.json() if resp.content else {}
            item = (data or {}).get("item") if isinstance(data, dict) else None
            if not isinstance(item, dict):
                return None
            tid = str(item.get("id") or "").strip()
            return tid or None
        except Exception:
            return None
    def _spotify_search_track_id(headers, title, artist):
        try:
            q = f'track:"{title}" artist:"{artist}"' if artist else f'track:"{title}"'
            resp = requests.get(
                "https://api.spotify.com/v1/search",
                headers=headers,
                params={"q": q, "type": "track", "limit": 1},
                timeout=6
            )
            if int(getattr(resp, "status_code", 0) or 0) != 200 or not resp.content:
                return None
            data = resp.json() if resp.content else {}
            items = (((data or {}).get("tracks") or {}).get("items") or []) if isinstance(data, dict) else []
            if not items:
                return None
            tid = str((items[0] or {}).get("id") or "").strip()
            return tid or None
        except Exception:
            return None
    def _resolve_spotify_track_id_for_like(track_obj=None):
        try:
            headers = _spotify_headers()
            if not headers:
                return None, None
            tid = _spotify_current_track_id(headers)
            if tid:
                return tid, headers
            t_obj = track_obj if isinstance(track_obj, dict) else _get_tab_track()
            title, artist = _extract_title_artist(t_obj)
            if not title:
                return None, headers
            tid = _spotify_search_track_id(headers, title, artist)
            return (tid or None), headers
        except Exception:
            return None, None
    def _spotify_is_liked(headers, track_id):
        try:
            resp = requests.get(f"https://api.spotify.com/v1/me/tracks/contains?ids={track_id}", headers=headers, timeout=6)
            scode = int(getattr(resp, "status_code", 0) or 0)
            if scode != 200:
                try:
                    body = str(getattr(resp, "text", "") or "")[:160]
                    log(f"[Nowfy][TabLike] contains status={scode} body={body}")
                except Exception:
                    pass
                return None
            data = resp.json()
            if isinstance(data, list) and data:
                return bool(data[0])
            return None
        except Exception:
            return None
    def _set_like_icon_visual(icon_view, liked_state):
        try:
            if icon_view is None:
                return
            _load_icon(icon_view, "https://assets.nowfy/liked.png", "nowfy_tab_apple_liked.png")
        except Exception:
            pass
    def _refresh_like_state_async(track_obj=None):
        try:
            icon_view = getattr(plugin, "_nowfy_like_icon_ref", None)
            btn_view = getattr(plugin, "_nowfy_like_btn_ref", None)
            if icon_view is None:
                return
            if not _is_like_supported_source():
                try:
                    log("[Nowfy][TabLike] state refresh skipped: source unsupported")
                except Exception:
                    pass
                run_on_ui_thread(lambda: (icon_view.setVisibility(View.GONE), btn_view.setVisibility(View.GONE) if btn_view is not None else None))
                return
            run_on_ui_thread(lambda: (icon_view.setVisibility(View.GONE), btn_view.setVisibility(View.GONE) if btn_view is not None else None))
            def _job():
                tid, headers = _resolve_spotify_track_id_for_like(track_obj=track_obj)
                liked = None
                if tid and headers:
                    liked = _spotify_is_liked(headers, tid)
                if liked is None:
                    liked = False
                try:
                    plugin._nowfy_like_track_id = str(tid or "")
                    plugin._nowfy_like_track_liked = bool(liked)
                except Exception:
                    pass
                try:
                    log(f"[Nowfy][TabLike] state refresh track_id={str(tid or '')} liked={bool(liked)}")
                except Exception:
                    pass
                def _apply():
                    try:
                        if bool(liked):
                            _set_like_icon_visual(icon_view, True)
                            icon_view.setVisibility(View.VISIBLE)
                            if btn_view is not None:
                                btn_view.setVisibility(View.VISIBLE)
                        else:
                            icon_view.setVisibility(View.GONE)
                            if btn_view is not None:
                                btn_view.setVisibility(View.GONE)
                    except Exception:
                        pass
                run_on_ui_thread(_apply)
            threading.Thread(target=_job, daemon=True).start()
        except Exception:
            pass
    def _animate_heart_like_in_hero():
        try:
            ov = getattr(plugin, "_nowfy_like_overlay_ref", None)
            if ov is None:
                return
            def _run():
                try:
                    ov.setVisibility(View.VISIBLE)
                    ov.setAlpha(0.0)
                    ov.setScaleX(0.52)
                    ov.setScaleY(0.52)
                    ov.clearColorFilter()
                    try:
                        ov.setColorFilter(Color.parseColor("#FF3B5C"))
                    except Exception:
                        pass
                    ov.animate().alpha(1.0).scaleX(1.0).scaleY(1.0).setDuration(140).start()
                    def _phase2():
                        try:
                            ov.animate().alpha(0.0).scaleX(1.28).scaleY(1.28).setDuration(240).start()
                        except Exception:
                            pass
                    def _hide_end():
                        try:
                            ov.setVisibility(View.GONE)
                        except Exception:
                            pass
                    threading.Timer(0.15, lambda: run_on_ui_thread(_phase2)).start()
                    threading.Timer(0.42, lambda: run_on_ui_thread(_hide_end)).start()
                except Exception:
                    pass
            run_on_ui_thread(_run)
        except Exception:
            pass
    def _tab_like_action(from_double_tap=False, force_unlike=False, track_obj=None):
        try:
            if not _is_like_supported_source():
                try:
                    log("[Nowfy][TabLike] action skipped: source unsupported")
                except Exception:
                    pass
                return
            if getattr(plugin, "_nowfy_like_busy", False):
                try:
                    log("[Nowfy][TabLike] action skipped: busy")
                except Exception:
                    pass
                return
            plugin._nowfy_like_busy = True
            def _job():
                try:
                    tid, headers = _resolve_spotify_track_id_for_like(track_obj=track_obj)
                    try:
                        log(f"[Nowfy][TabLike] action start from_double={bool(from_double_tap)} force_unlike={bool(force_unlike)} track_id={str(tid or '')}")
                    except Exception:
                        pass
                    if not tid or not headers:
                        run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_no_track_playing")))
                        return
                    if force_unlike:
                        resp = requests.delete("https://api.spotify.com/v1/me/tracks", headers=headers, params={"ids": tid}, timeout=8)
                        rcode = int(getattr(resp, "status_code", 0) or 0)
                        try:
                            body = str(getattr(resp, "text", "") or "")[:160]
                            log(f"[Nowfy][TabLike] unlike(force) status={rcode} body={body}")
                        except Exception:
                            pass
                        if rcode in (200, 202, 204):
                            run_on_ui_thread(lambda: BulletinHelper.show_info(tr("nowfy_tab_unliked_done")))
                            icon_view = getattr(plugin, "_nowfy_like_icon_ref", None)
                            btn_view = getattr(plugin, "_nowfy_like_btn_ref", None)
                            run_on_ui_thread(lambda: (icon_view.setVisibility(View.GONE) if icon_view is not None else None, btn_view.setVisibility(View.GONE) if btn_view is not None else None))
                            plugin._nowfy_like_track_liked = False
                            plugin._nowfy_like_track_id = str(tid)
                        elif rcode == 401:
                            run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_auth")))
                        elif rcode == 429:
                            run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_unknown")))
                        else:
                            run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_unknown")))
                        return
                    try:
                        cached_tid = str(getattr(plugin, "_nowfy_like_track_id", "") or "")
                        cached_liked = bool(getattr(plugin, "_nowfy_like_track_liked", False))
                    except Exception:
                        cached_tid = ""
                        cached_liked = False
                    if from_double_tap and (not force_unlike):
                        if cached_tid == str(tid) and cached_liked:
                            run_on_ui_thread(lambda: BulletinHelper.show_info(tr("nowfy_tab_like_again_hint")))
                            return
                        resp = requests.put("https://api.spotify.com/v1/me/tracks", headers=headers, params={"ids": tid}, timeout=8)
                        code = int(getattr(resp, "status_code", 0) or 0)
                        try:
                            body = str(getattr(resp, "text", "") or "")[:160]
                            log(f"[Nowfy][TabLike] like(double) status={code} body={body}")
                        except Exception:
                            pass
                        if code in (200, 202, 204):
                            run_on_ui_thread(lambda: BulletinHelper.show_info(tr("bulletin_liked")))
                            icon_view = getattr(plugin, "_nowfy_like_icon_ref", None)
                            btn_view = getattr(plugin, "_nowfy_like_btn_ref", None)
                            run_on_ui_thread(lambda: (_set_like_icon_visual(icon_view, True), icon_view.setVisibility(View.VISIBLE) if icon_view is not None else None, btn_view.setVisibility(View.VISIBLE) if btn_view is not None else None))
                            plugin._nowfy_like_track_liked = True
                            plugin._nowfy_like_track_id = str(tid)
                            _animate_heart_like_in_hero()
                        elif code == 401:
                            run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_auth")))
                        elif code == 403:
                            run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_premium_required")))
                        elif code == 429:
                            run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_unknown")))
                        else:
                            run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_unknown")))
                        return
                    liked = _spotify_is_liked(headers, tid)
                    if liked is None:
                        run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_unknown")))
                        return
                    if bool(liked):
                        if from_double_tap:
                            run_on_ui_thread(lambda: BulletinHelper.show_info(tr("nowfy_tab_like_again_hint")))
                        else:
                            resp = requests.delete("https://api.spotify.com/v1/me/tracks", headers=headers, params={"ids": tid}, timeout=8)
                            rcode = int(getattr(resp, "status_code", 0) or 0)
                            try:
                                body = str(getattr(resp, "text", "") or "")[:160]
                                log(f"[Nowfy][TabLike] unlike(by-icon) status={rcode} body={body}")
                            except Exception:
                                pass
                            if rcode in (200, 202, 204):
                                run_on_ui_thread(lambda: BulletinHelper.show_info(tr("nowfy_tab_unliked_done")))
                                icon_view = getattr(plugin, "_nowfy_like_icon_ref", None)
                                btn_view = getattr(plugin, "_nowfy_like_btn_ref", None)
                                run_on_ui_thread(lambda: (icon_view.setVisibility(View.GONE) if icon_view is not None else None, btn_view.setVisibility(View.GONE) if btn_view is not None else None))
                                plugin._nowfy_like_track_liked = False
                                plugin._nowfy_like_track_id = str(tid)
                            elif rcode == 401:
                                run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_auth")))
                            elif rcode == 429:
                                run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_unknown")))
                            else:
                                run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_unknown")))
                        return
                    resp = requests.put("https://api.spotify.com/v1/me/tracks", headers=headers, params={"ids": tid}, timeout=8)
                    code = int(getattr(resp, "status_code", 0) or 0)
                    try:
                        body = str(getattr(resp, "text", "") or "")[:160]
                        log(f"[Nowfy][TabLike] like status={code} body={body}")
                    except Exception:
                        pass
                    if code in (200, 202, 204):
                        run_on_ui_thread(lambda: BulletinHelper.show_info(tr("bulletin_liked")))
                        icon_view = getattr(plugin, "_nowfy_like_icon_ref", None)
                        btn_view = getattr(plugin, "_nowfy_like_btn_ref", None)
                        run_on_ui_thread(lambda: (_set_like_icon_visual(icon_view, True), icon_view.setVisibility(View.VISIBLE) if icon_view is not None else None, btn_view.setVisibility(View.VISIBLE) if btn_view is not None else None))
                        plugin._nowfy_like_track_liked = True
                        plugin._nowfy_like_track_id = str(tid)
                        if from_double_tap:
                            _animate_heart_like_in_hero()
                    elif code == 401:
                        run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_auth")))
                    elif code == 403:
                        run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_premium_required")))
                    elif code == 429:
                        run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_unknown")))
                    else:
                        run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_unknown")))
                except Exception as e:
                    try:
                        log(f"[Nowfy][TabLike] action exception: {e}")
                    except Exception:
                        pass
                    run_on_ui_thread(lambda: BulletinHelper.show_info(tr("error_unknown")))
                finally:
                    plugin._nowfy_like_busy = False
            threading.Thread(target=_job, daemon=True).start()
        except Exception:
            try:
                plugin._nowfy_like_busy = False
            except Exception:
                pass
    class SendNowPlayButtonListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            fragment = get_last_fragment()
            if not isinstance(fragment, ChatActivity):
                return
            if not _can_send_now_card(fragment):
                try:
                    _tab_feedback["no_track"] = True
                    _tab_feedback["no_track_until"] = time.time() + 1.8
                except Exception:
                    pass
                try:
                    if status is not None:
                        run_on_ui_thread(lambda: status.setText(tr("nowfy_tab_status_no_permission")))
                except Exception:
                    pass
                return
            if _tab_feedback.get("busy"):
                return
            has_track, status_text = _get_track_status_info()
            if not has_track:
                try:
                    _tab_feedback["no_track"] = True
                    _tab_feedback["no_track_until"] = time.time() + 1.8
                except Exception:
                    pass
                try:
                    if status is not None:
                        run_on_ui_thread(lambda: status.setText(tr("nowfy_tab_status_no_track")))
                except Exception:
                    pass
                return
            _tab_feedback["busy"] = True
            _tab_feedback["no_track"] = False
            _nowplay_meta["request_id"] = int(_nowplay_meta.get("request_id", 0)) + 1
            req_id = int(_nowplay_meta["request_id"])
            try:
                if status is not None:
                    run_on_ui_thread(lambda: status.setText(tr("nowfy_tab_status_generating")))
            except Exception:
                pass
            def _progress_loop(local_req_id):
                last_pct = -1
                while True:
                    if local_req_id != int(_nowplay_meta.get("request_id", 0)):
                        return
                    if not _tab_feedback.get("busy"):
                        return
                    try:
                        done = bool(getattr(plugin, "_tab_feedback_done", False))
                    except Exception:
                        done = False
                    if done:
                        _set_nowplaying_subtext("100%")
                        return
                    try:
                        pct = int(getattr(plugin, "_tab_feedback_progress", 0))
                    except Exception:
                        pct = 0
                    pct = max(1, min(99, pct)) if pct > 0 else 0
                    if pct and pct != last_pct:
                        last_pct = pct
                        _set_nowplaying_subtext(f"{pct}%")
                    time.sleep(0.25)
            def _send_and_restore(local_req_id):
                try:
                    try:
                        plugin._tab_feedback_pending = True
                        plugin._tab_feedback_done = False
                        plugin._tab_feedback_progress = 1
                    except Exception:
                        pass
                    try:
                        _set_nowplaying_subtext("1%")
                    except Exception:
                        pass
                    threading.Thread(target=lambda: _progress_loop(local_req_id), daemon=True).start()
                    plugin._send_now_playing_card_for_tab()
                    started = time.time()
                    while time.time() - started < 25:
                        try:
                            if bool(getattr(plugin, "_tab_feedback_done", False)):
                                break
                        except Exception:
                            pass
                        time.sleep(0.30)
                finally:
                    try:
                        plugin._tab_feedback_pending = False
                    except Exception:
                        pass
                    _tab_feedback["busy"] = False
                    _set_nowplaying_subtext(None)
                    _bind_track()
            threading.Thread(target=lambda: _send_and_restore(req_id), daemon=True).start()
    class SharePreviewLongClickListener(dynamic_proxy(View.OnLongClickListener)):
        def onLongClick(self, view):
            try:
                run_on_ui_thread(lambda: plugin._open_tab_share_preview())
            except Exception:
                pass
            return True
    class MusicPreviewButtonListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            try:
                BulletinHelper.show_info(tr("nowfy_tab_share_hold_to_send_hint"))
            except Exception:
                pass
    class MusicPreviewButtonHoldListener(dynamic_proxy(View.OnLongClickListener)):
        def onLongClick(self, view):
            try:
                fragment = get_last_fragment()
                if not _can_send_now_card(fragment):
                    try:
                        _tab_feedback["no_track"] = True
                        _tab_feedback["no_track_until"] = time.time() + 1.8
                    except Exception:
                        pass
                    try:
                        if status is not None:
                            run_on_ui_thread(lambda: status.setText(tr("nowfy_tab_status_no_permission")))
                    except Exception:
                        pass
                    return True
                run_on_queue(lambda: plugin._send_tab_share_lyrics_from_tab())
            except Exception:
                pass
            return True
    class TrackDownloadButtonListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            try:
                fragment = get_last_fragment()
                if not _can_send_now_card(fragment):
                    try:
                        _tab_feedback["no_track"] = True
                        _tab_feedback["no_track_until"] = time.time() + 1.8
                    except Exception:
                        pass
                    try:
                        if status is not None:
                            run_on_ui_thread(lambda: status.setText(tr("nowfy_tab_status_no_permission")))
                    except Exception:
                        pass
                    return
                try:
                    setattr(plugin, "_nowfy_track_download_animating", True)
                except Exception:
                    pass
                try:
                    _start_track_download_icon_effect(getattr(plugin, "_nowfy_track_download_icon_ref", None))
                except Exception:
                    pass
                if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "send_tab_track_download"):
                    NOWFY_CORE_API.send_tab_track_download(plugin)
                else:
                    BulletinHelper.show_info("Track Download is unavailable.")
                    try:
                        setattr(plugin, "_nowfy_track_download_animating", False)
                    except Exception:
                        pass
            except Exception:
                BulletinHelper.show_info("Track Download is unavailable.")
                try:
                    setattr(plugin, "_nowfy_track_download_animating", False)
                except Exception:
                    pass
    class LikeButtonListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            try:
                try:
                    log("[Nowfy][TabLike] liked icon clicked")
                except Exception:
                    pass
                fragment = get_last_fragment()
                if not _can_send_now_card(fragment):
                    try:
                        _tab_feedback["no_track"] = True
                        _tab_feedback["no_track_until"] = time.time() + 1.8
                    except Exception:
                        pass
                    try:
                        if status is not None:
                            run_on_ui_thread(lambda: status.setText(tr("nowfy_tab_status_no_permission")))
                    except Exception:
                        pass
                    return
                _tab_like_action(from_double_tap=False, force_unlike=True)
            except Exception:
                pass
    class AppleHeroDoubleTapTouchListener(dynamic_proxy(View.OnTouchListener)):
        def onTouch(self, v, event):
            try:
                if event is None:
                    return False
                action = int(event.getAction())
                if action != int(MotionEvent.ACTION_DOWN):
                    return False
                if not _is_like_supported_source():
                    return False
                try:
                    w = float(v.getWidth() or 0)
                    h = float(v.getHeight() or 0)
                    x = float(event.getX() or 0.0)
                    y = float(event.getY() or 0.0)
                    if w > 0 and h > 0:
                        if x < (w * 0.20) or x > (w * 0.80) or y < (h * 0.18) or y > (h * 0.82):
                            return False
                except Exception:
                    pass
                now_ms = int(time.time() * 1000)
                cooldown_until = int(getattr(plugin, "_nowfy_tab_like_cooldown_until", 0) or 0)
                if now_ms < cooldown_until:
                    return False
                last_ms = int(getattr(plugin, "_nowfy_tab_last_tap_ms", 0) or 0)
                plugin._nowfy_tab_last_tap_ms = now_ms
                if (now_ms - last_ms) <= 320:
                    try:
                        log("[Nowfy][TabLike] double tap detected")
                    except Exception:
                        pass
                    try:
                        plugin._nowfy_tab_like_cooldown_until = now_ms + 900
                    except Exception:
                        pass
                    _tab_like_action(from_double_tap=True, force_unlike=False)
                else:
                    try:
                        log("[Nowfy][TabLike] first tap captured")
                    except Exception:
                        pass
            except Exception:
                pass
            return False
    class SettingsButtonListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            run_on_ui_thread(lambda: plugin._open_plugin_settings())
    class PanelButtonListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            run_on_ui_thread(lambda: plugin._open_nowfy_panel_settings())
    class ControlOpenListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            def _open():
                try:
                    if _is_apple_style and (not _fab_sheet_mode):
                        plugin._open_chat_fab_sheet(control_only=True)
                        return
                except Exception:
                    pass
                _show_tab_page(1)
            run_on_ui_thread(_open)
    class PressTouchListener(dynamic_proxy(View.OnTouchListener)):
        def onTouch(self, v, event):
            try:
                action = event.getAction()
                if action == MotionEvent.ACTION_DOWN:
                    v.setScaleX(0.97)
                    v.setScaleY(0.97)
                    v.setAlpha(0.95)
                    try:
                        bg = v.getBackground()
                        tag = v.getTag()
                        if isinstance(bg, GradientDrawable):
                            if tag == "nowfy_card_primary":
                                bg.setStroke(AndroidUtilities.dp(2), _primary_stroke_pressed)
                            elif tag == "nowfy_card_secondary":
                                bg.setStroke(AndroidUtilities.dp(1), _secondary_stroke_pressed)
                    except Exception:
                        pass
                elif action == MotionEvent.ACTION_UP or action == MotionEvent.ACTION_CANCEL:
                    v.setScaleX(1.0)
                    v.setScaleY(1.0)
                    v.setAlpha(1.0)
                    try:
                        bg = v.getBackground()
                        tag = v.getTag()
                        if isinstance(bg, GradientDrawable):
                            if tag == "nowfy_card_primary":
                                bg.setStroke(AndroidUtilities.dp(2), _primary_stroke)
                            elif tag == "nowfy_card_secondary":
                                bg.setStroke(AndroidUtilities.dp(1), _secondary_stroke)
                    except Exception:
                        pass
            except Exception:
                pass
            return False
    def _start_track_download_icon_effect(icon_view):
        try:
            if icon_view is None:
                return
            if bool(getattr(plugin, "_nowfy_track_download_fx_running", False)):
                return
            setattr(plugin, "_nowfy_track_download_fx_running", True)
            colors = [None, "#52D273", "#9D6CFF", None]
            def _paint(c):
                def _ui():
                    try:
                        if c:
                            icon_view.setColorFilter(Color.parseColor(str(c)))
                        else:
                            icon_view.clearColorFilter()
                    except Exception:
                        pass
                run_on_ui_thread(_ui)
            def _loop():
                try:
                    i = 0
                    started = time.time()
                    while True:
                        active = bool(getattr(plugin, "_nowfy_track_download_animating", False))
                        if ((not active) and (time.time() - started > 0.8)) or (time.time() - started > 22.0):
                            break
                        _paint(colors[i % len(colors)])
                        i += 1
                        time.sleep(0.42)
                except Exception:
                    pass
                finally:
                    _paint(None)
                    try:
                        setattr(plugin, "_nowfy_track_download_fx_running", False)
                    except Exception:
                        pass
            threading.Thread(target=_loop, daemon=True).start()
        except Exception:
            try:
                setattr(plugin, "_nowfy_track_download_fx_running", False)
            except Exception:
                pass
    class ControlBackListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            run_on_queue(lambda: plugin._previous_track(None))
    class ControlSkipListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            run_on_queue(lambda: plugin._skip_track(None))
    class ControlPlayPauseListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            is_playing = bool(_control_state.get("is_playing", False))
            def _run():
                try:
                    if hasattr(plugin, "_toggle_playback_only"):
                        plugin._toggle_playback_only(None)
                    else:
                        if is_playing:
                            plugin._pause_playback_only(None)
                        else:
                            plugin._resume_playback_only(None)
                except Exception:
                    pass
                _sync_control_play_state()
            run_on_queue(_run)
    class ControlSearchListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            run_on_ui_thread(lambda: plugin._show_spotify_search_dialog())
    def _open_lyrics_safe():
        opened = False
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "open_nowtab_lyrics"):
                NOWFY_CORE_API.open_nowtab_lyrics(plugin)
                opened = True
        except Exception:
            pass
        try:
            if not opened and hasattr(plugin, "_open_nowtab_lyrics"):
                plugin._open_nowtab_lyrics()
                opened = True
        except Exception:
            pass
        try:
            if not opened and hasattr(plugin, "_open_nowbox_lyrics"):
                plugin._open_nowbox_lyrics()
                opened = True
        except Exception:
            pass
        if not opened:
            BulletinHelper.show_info(tr("nowbox_lyrics_not_found"))
    class ControlVolumeDownListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            run_on_queue(lambda: plugin._adjust_spotify_volume(-5))
    class ControlVolumeUpListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            run_on_queue(lambda: plugin._adjust_spotify_volume(5))
    class ControlReturnListener(dynamic_proxy(View.OnClickListener)):
        def onClick(self, view):
            if _fab_sheet_mode and _control_only_mode:
                run_on_ui_thread(lambda: plugin._close_chat_fab_sheet())
            else:
                run_on_ui_thread(lambda: _show_tab_page(0))
    layout_helper = find_class("org.telegram.ui.Components.LayoutHelper")
    try:
        ScrollView = find_class("androidx.core.widget.NestedScrollView")
    except Exception:
        ScrollView = None
    if ScrollView is None:
        ScrollView = find_class("android.widget.ScrollView")
    if ScrollView is None:
        return None
    fragment = get_last_fragment()
    can_send_card = _can_send_now_card(fragment)
    if _chatlist_flow_mode:
        can_send_card = False
    root_container = FrameLayout(context)
    scroll_view = ScrollView(context)
    scroll_view.setFillViewport(True)
    scroll_view.setVerticalScrollBarEnabled(False)
    scroll_view.setNestedScrollingEnabled(True)
    vertical_container = LinearLayout(context)
    vertical_container.setOrientation(LinearLayout.VERTICAL)
    vertical_container.setPadding(
        AndroidUtilities.dp(16),
        AndroidUtilities.dp(16),
        AndroidUtilities.dp(16),
        AndroidUtilities.dp(12)
    )
    if layout_helper:
        scroll_view.addView(vertical_container, layout_helper.createScroll(-1, -2, Gravity.TOP))
    else:
        scroll_view.addView(vertical_container)
    control_scroll = ScrollView(context)
    control_scroll.setFillViewport(True)
    control_scroll.setVerticalScrollBarEnabled(False)
    control_scroll.setNestedScrollingEnabled(True)
    control_foreground_host = None
    control_container = LinearLayout(context)
    control_container.setOrientation(LinearLayout.VERTICAL)
    _is_flow_compact_control = bool(_fab_sheet_mode and _flow_compact_mode)
    control_container.setPadding(
        AndroidUtilities.dp(16),
        AndroidUtilities.dp(16),
        AndroidUtilities.dp(16),
        AndroidUtilities.dp(12)
    )
    _flow_transparent_mode = False
    _flow_surface_color = Color.parseColor("#1A2435")
    _flow_text_primary = Color.WHITE
    _flow_text_secondary = Color.parseColor("#C8D1FF")
    _flow_button_bg = Color.parseColor("#2F3B73")
    _flow_notice_bg = Color.parseColor("#243058")
    _flow_return_bg = Color.parseColor("#263259")
    if _fab_sheet_mode:
        try:
            _flow_transparent_mode = bool(plugin.get_setting("nowfy_flow_bt_debug", True))
        except Exception:
            _flow_transparent_mode = False
        try:
            _flow_surface_color = Theme.getColor(Theme.key_dialogBackground)
        except Exception:
            pass
        try:
            _flow_text_primary = Theme.getColor(Theme.key_dialogTextBlack)
        except Exception:
            pass
        try:
            _flow_text_secondary = Theme.getColor(Theme.key_dialogTextGray3)
        except Exception:
            pass
        try:
            _flow_button_bg = Theme.getColor(Theme.key_featuredStickers_addButton)
        except Exception:
            pass
        try:
            _flow_notice_bg = Theme.getColor(Theme.key_featuredStickers_addButtonPressed)
        except Exception:
            _flow_notice_bg = _flow_button_bg
        try:
            _flow_return_bg = Theme.getColor(Theme.key_featuredStickers_addButton)
        except Exception:
            _flow_return_bg = _flow_button_bg
    if _fab_sheet_mode and _flow_transparent_mode:
        try:
            _panel_bg = GradientDrawable()
            _panel_bg.setCornerRadius(AndroidUtilities.dp(24 if _is_flow_compact_control else 26))
            _panel_bg.setColor(Color.argb(122, 255, 255, 255))
            try:
                _panel_bg.setStroke(AndroidUtilities.dp(1), Color.argb(88, 255, 255, 255))
            except Exception:
                pass
            control_container.setBackground(_panel_bg)
            control_container.setPadding(
                AndroidUtilities.dp(12 if _is_flow_compact_control else 14),
                AndroidUtilities.dp(12 if _is_flow_compact_control else 14),
                AndroidUtilities.dp(12 if _is_flow_compact_control else 14),
                AndroidUtilities.dp(10 if _is_flow_compact_control else 12)
            )
        except Exception:
            pass
    if _is_flow_compact_control and _flow_transparent_mode:
        control_foreground_host = LinearLayout(context)
        control_foreground_host.setOrientation(LinearLayout.VERTICAL)
        try:
            control_foreground_host.setGravity(Gravity.CENTER_HORIZONTAL)
            control_foreground_host.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(10), AndroidUtilities.dp(14), AndroidUtilities.dp(10))
        except Exception:
            pass
        try:
            lp_inner = LinearLayout.LayoutParams(-1, -2)
            lp_inner.leftMargin = AndroidUtilities.dp(26)
            lp_inner.rightMargin = AndroidUtilities.dp(26)
            control_foreground_host.addView(control_container, lp_inner)
        except Exception:
            control_foreground_host.addView(control_container)
        if layout_helper:
            control_scroll.addView(control_foreground_host, layout_helper.createScroll(-1, -2, Gravity.TOP))
        else:
            control_scroll.addView(control_foreground_host)
    else:
        if layout_helper:
            control_scroll.addView(control_container, layout_helper.createScroll(-1, -2, Gravity.TOP))
        else:
            control_scroll.addView(control_container)
    try:
        if _is_flow_compact_control:
            lpcc = control_container.getLayoutParams()
            if lpcc is not None:
                try:
                    lpcc.leftMargin = AndroidUtilities.dp(22 if _flow_transparent_mode else 18)
                    lpcc.rightMargin = AndroidUtilities.dp(22 if _flow_transparent_mode else 18)
                except Exception:
                    pass
                control_container.setLayoutParams(lpcc)
    except Exception:
        pass

    def _show_tab_page(index):
        _page_state["index"] = 1 if int(index) == 1 else 0
        try:
            scroll_view.setVisibility(View.VISIBLE if _page_state["index"] == 0 else View.GONE)
            control_scroll.setVisibility(View.VISIBLE if _page_state["index"] == 1 else View.GONE)
        except Exception:
            pass

    def _load_icon(icon_view, url, cache_name):
        try:
            is_nowfy_asset = bool(str(url or "").strip().lower().startswith("https://assets.nowfy/"))
            if url and url.startswith("data:image"):
                try:
                    b64 = url.split("base64,", 1)[1]
                    data = base64.b64decode(b64)
                    bmp2 = BitmapFactory.decodeByteArray(data, 0, len(data))
                    if bmp2:
                        run_on_ui_thread(lambda: icon_view.setImageBitmap(bmp2))
                    return
                except Exception:
                    pass
            base_dir = ApplicationLoader.getFilesDirFixed()
            if not base_dir:
                return
            icon_dir = File(base_dir, "NowfyTabIcons")
            if not icon_dir.exists():
                icon_dir.mkdirs()
            icon_path = File(icon_dir, cache_name)
            if icon_path.exists() and not is_nowfy_asset:
                bmp = BitmapFactory.decodeFile(icon_path.getAbsolutePath())
                if bmp:
                    run_on_ui_thread(lambda: icon_view.setImageBitmap(bmp))
                    return
            try:
                cache_key = f"tab_icon_{cache_name}" if cache_name else ("tab_icon_" + hashlib.md5(str(url).encode()).hexdigest()[:12])
                data_cached = plugin._get_cached_image_enhanced(url, cache_key=cache_key) if hasattr(plugin, "_get_cached_image_enhanced") else None
                if data_cached:
                    try:
                        with open(icon_path.getAbsolutePath(), "wb") as f:
                            f.write(data_cached)
                    except Exception:
                        pass
                    bmp_cached = BitmapFactory.decodeByteArray(data_cached, 0, len(data_cached))
                    if bmp_cached:
                        run_on_ui_thread(lambda: icon_view.setImageBitmap(bmp_cached))
                        return
            except Exception:
                pass
            def _fetch():
                try:
                    headers = {
                        "Accept": "image/*,*/*;q=0.8",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
                    }
                    resp = requests.get(url, headers=headers, timeout=10)
                    if resp.status_code == 200:
                        data = resp.content
                        try:
                            with open(icon_path.getAbsolutePath(), "wb") as f:
                                f.write(data)
                        except Exception:
                            pass
                        bmp2 = BitmapFactory.decodeByteArray(data, 0, len(data))
                        if bmp2:
                            run_on_ui_thread(lambda: icon_view.setImageBitmap(bmp2))
                except Exception:
                    pass
            threading.Thread(target=_fetch, daemon=True).start()
        except Exception:
            pass

    def _load_cover(cover_view, url):
        try:
            url = str(url or "").strip()
            if not url:
                return
            cache_key = "nowfy_focus_cover_" + hashlib.md5(url.encode()).hexdigest()[:10] + ".png"
            _load_icon(cover_view, url, cache_key)
        except Exception:
            pass

    _flow_panel_state = {"request_id": 0, "last_url": ""}

    def _apply_flow_panel_background_bitmap(bmp):
        try:
            if not (_fab_sheet_mode and _is_flow_compact_control and _flow_transparent_mode):
                return
            if bmp is None:
                return
            from hook_utils import find_class
            GradientDrawable = find_class("android.graphics.drawable.GradientDrawable")
            LayerDrawable = find_class("android.graphics.drawable.LayerDrawable")
            BitmapDrawable = find_class("android.graphics.drawable.BitmapDrawable")
            if not GradientDrawable:
                return
            out = bmp
            try:
                if hasattr(plugin, "_apply_simple_blur_mini_control"):
                    b2 = plugin._apply_simple_blur_mini_control(bmp, 24)
                    if b2 is not None:
                        out = b2
            except Exception:
                pass
            radius = AndroidUtilities.dp(24)
            def _rounded_bitmap(src_bmp, rr):
                try:
                    BitmapCls = find_class("android.graphics.Bitmap")
                    CanvasCls = find_class("android.graphics.Canvas")
                    PaintCls = find_class("android.graphics.Paint")
                    RectFCls = find_class("android.graphics.RectF")
                    BitmapShaderCls = find_class("android.graphics.BitmapShader")
                    ShaderCls = find_class("android.graphics.Shader")
                    if not all([BitmapCls, CanvasCls, PaintCls, RectFCls, BitmapShaderCls, ShaderCls]):
                        return src_bmp
                    w = int(src_bmp.getWidth())
                    h = int(src_bmp.getHeight())
                    if w <= 0 or h <= 0:
                        return src_bmp
                    out_bmp = BitmapCls.createBitmap(w, h, BitmapCls.Config.ARGB_8888)
                    canvas = CanvasCls(out_bmp)
                    paint = PaintCls()
                    try:
                        paint.setAntiAlias(True)
                    except Exception:
                        pass
                    shader = BitmapShaderCls(src_bmp, ShaderCls.TileMode.CLAMP, ShaderCls.TileMode.CLAMP)
                    paint.setShader(shader)
                    rect = RectFCls(0.0, 0.0, float(w), float(h))
                    canvas.drawRoundRect(rect, float(rr), float(rr), paint)
                    return out_bmp
                except Exception:
                    return src_bmp
            def _set_bg():
                try:
                    mask_bg = GradientDrawable()
                    mask_bg.setColor(Color.argb(170, 20, 27, 39))
                    mask_bg.setCornerRadius(float(radius))
                    try:
                        mask_bg.setStroke(AndroidUtilities.dp(1), Color.argb(92, 255, 255, 255))
                    except Exception:
                        pass
                    if LayerDrawable and BitmapDrawable:
                        try:
                            BitmapCls = find_class("android.graphics.Bitmap")
                            target_w = int(control_container.getWidth() or 0)
                            target_h = int(control_container.getHeight() or 0)
                            if target_w <= 0:
                                target_w = int(AndroidUtilities.dp(320))
                            if target_h <= 0:
                                target_h = int(AndroidUtilities.dp(152 if _is_flow_compact_control else 208))
                            if BitmapCls and out is not None:
                                src_w = int(out.getWidth() or 0)
                                src_h = int(out.getHeight() or 0)
                                if src_w > 0 and src_h > 0 and target_w > 0 and target_h > 0:
                                    scale = max(float(target_w) / float(src_w), float(target_h) / float(src_h))
                                    scaled_w = max(1, int(round(float(src_w) * scale)))
                                    scaled_h = max(1, int(round(float(src_h) * scale)))
                                    scaled = BitmapCls.createScaledBitmap(out, scaled_w, scaled_h, True)
                                    if scaled is not None:
                                        crop_x = max(0, int((scaled_w - target_w) / 2))
                                        crop_y = max(0, int((scaled_h - target_h) / 2))
                                        crop_w = min(target_w, scaled_w)
                                        crop_h = min(target_h, scaled_h)
                                        try:
                                            out_local = BitmapCls.createBitmap(scaled, crop_x, crop_y, crop_w, crop_h)
                                        except Exception:
                                            out_local = scaled
                                    else:
                                        out_local = out
                                else:
                                    out_local = out
                            else:
                                out_local = out
                        except Exception:
                            out_local = out
                        rounded = _rounded_bitmap(out_local, radius)
                        img = BitmapDrawable(context.getResources(), rounded)
                        try:
                            img.setDither(True)
                            img.setFilterBitmap(True)
                        except Exception:
                            pass
                        overlay = GradientDrawable()
                        overlay.setColor(Color.argb(118, 8, 13, 22))
                        overlay.setCornerRadius(float(radius))
                        stroke = GradientDrawable()
                        stroke.setColor(Color.TRANSPARENT)
                        stroke.setCornerRadius(float(radius))
                        try:
                            stroke.setStroke(AndroidUtilities.dp(1), Color.argb(96, 255, 255, 255))
                        except Exception:
                            pass
                        layers = [img, overlay, stroke]
                        control_container.setBackground(LayerDrawable(layers))
                    else:
                        control_container.setBackground(mask_bg)
                    try:
                        control_container.setMinimumHeight(0)
                    except Exception:
                        pass
                    try:
                        if _is_flow_compact_control and _flow_transparent_mode:
                            lp_fix = control_container.getLayoutParams()
                            if lp_fix is not None:
                                lp_fix.height = AndroidUtilities.dp(156)
                                control_container.setLayoutParams(lp_fix)
                    except Exception:
                        pass
                    try:
                        from hook_utils import find_class
                        ViewOutlineProvider = find_class("android.view.ViewOutlineProvider")
                        control_container.setClipToOutline(True)
                        if ViewOutlineProvider:
                            control_container.setOutlineProvider(ViewOutlineProvider.BACKGROUND)
                    except Exception:
                        pass
                except Exception:
                    pass
            run_on_ui_thread(_set_bg)
        except Exception:
            pass

    def _set_flow_panel_fallback():
        try:
            if not (_fab_sheet_mode and _is_flow_compact_control and _flow_transparent_mode):
                return
            from hook_utils import find_class
            BitmapFactoryLocal = find_class("android.graphics.BitmapFactory")
            if not BitmapFactoryLocal:
                return
            candidates = [
                os.path.join(os.path.dirname(__file__), "assets", "png", "control_bg.png"),
                os.path.join(os.path.dirname(__file__), "nowfy", "assets", "png", "control_bg.png"),
            ]
            for p in candidates:
                try:
                    if p and os.path.isfile(p):
                        bmp = BitmapFactoryLocal.decodeFile(p)
                        if bmp:
                            _apply_flow_panel_background_bitmap(bmp)
                            return
                except Exception:
                    pass
        except Exception:
            pass

    def _update_flow_panel_background(track_info=None):
        try:
            if not (_fab_sheet_mode and _is_flow_compact_control and _flow_transparent_mode):
                return
            _flow_panel_state["last_url"] = ""
            _set_flow_panel_fallback()
        except Exception:
            pass
    try:
        if _fab_sheet_mode and _is_flow_compact_control and _flow_transparent_mode:
            _set_flow_panel_fallback()
    except Exception:
        pass

    def _apply_control_icon(icon_view, fallback_view, icon_url, fallback_text, cache_name):
        try:
            icon_url = str(icon_url or "").strip()
            if icon_url:
                icon_view.setVisibility(View.VISIBLE)
                fallback_view.setVisibility(View.GONE)
                _load_icon(icon_view, icon_url, cache_name)
            else:
                icon_view.setVisibility(View.GONE)
                fallback_view.setVisibility(View.VISIBLE)
                fallback_view.setText(fallback_text)
        except Exception:
            try:
                icon_view.setVisibility(View.GONE)
                fallback_view.setVisibility(View.VISIBLE)
                fallback_view.setText(fallback_text)
            except Exception:
                pass

    def _set_nowplaying_subtext(progress_text=None):
        try:
            sub_view = _nowplay_meta.get("sub_view")
            if sub_view is None:
                return
            if progress_text is None:
                run_on_ui_thread(lambda: sub_view.setText(_nowplay_meta.get("default_sub", tr("nowfy_tab_card_now_sub"))))
                return
            label = tr("nowfy_tab_creating_percent").format(percent=progress_text)
            run_on_ui_thread(lambda: sub_view.setText(label))
        except Exception:
            pass

    def _create_card(title_text, sub_text, icon_url, icon_cache, is_primary, listener, tactile=False):
        card = LinearLayout(context)
        card.setOrientation(LinearLayout.HORIZONTAL)
        card.setGravity(Gravity.CENTER_VERTICAL)
        card.setPadding(AndroidUtilities.dp(18), AndroidUtilities.dp(16), AndroidUtilities.dp(18), AndroidUtilities.dp(16))
        if is_primary:
            bg = GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                [Color.parseColor("#6E57FF"), Color.parseColor("#B26BFF")]
            )
            bg.setCornerRadius(AndroidUtilities.dp(22))
            try:
                bg.setStroke(AndroidUtilities.dp(2), _primary_stroke)
            except Exception:
                pass
        else:
            bg = GradientDrawable()
            bg.setColor(Color.parseColor("#232E4A"))
            bg.setCornerRadius(AndroidUtilities.dp(18))
            try:
                bg.setStroke(AndroidUtilities.dp(1), _secondary_stroke)
            except Exception:
                pass
        card.setBackground(bg)
        try:
            card.setElevation(AndroidUtilities.dp(4.0 if is_primary else 2.6))
            card.setTranslationZ(AndroidUtilities.dp(2.0 if is_primary else 1.2))
        except Exception:
            pass
        card.setTag("nowfy_card_primary" if is_primary else "nowfy_card_secondary")
        icon = ImageView(context)
        compact_icon_only = (not title_text and not sub_text)
        is_control_logo = (icon_url == ICON_CONTROL_TAB or icon_url == ICON_SETTINGS_TAB_CONTROL)
        if is_control_logo:
            icon_w = AndroidUtilities.dp(76)
            icon_h = AndroidUtilities.dp(36)
            icon_lp = LinearLayout.LayoutParams(icon_w, icon_h)
        else:
            icon_size = AndroidUtilities.dp(46 if is_primary else (42 if compact_icon_only else 40))
            icon_lp = LinearLayout.LayoutParams(icon_size, icon_size)
        icon_lp.setMargins(0, 0, AndroidUtilities.dp(0 if compact_icon_only else 14), 0)
        card.addView(icon, icon_lp)
        try:
            icon.setScaleType(ImageView.ScaleType.FIT_CENTER)
        except Exception:
            pass
        _load_icon(icon, icon_url, icon_cache)
        if not compact_icon_only:
            text_wrap = LinearLayout(context)
            text_wrap.setOrientation(LinearLayout.VERTICAL)
            title = TextView(context)
            title.setText(title_text)
            title.setTextColor(Color.WHITE)
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18 if is_primary else 16)
            try:
                title.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
            except Exception:
                pass
            title.setMaxLines(1)
            text_wrap.addView(title)
            sub = TextView(context)
            sub.setText(sub_text)
            sub.setTextColor(Color.parseColor("#E1E4FF") if is_primary else Color.parseColor("#C3CAE5"))
            try:
                sub.setAlpha(0.78 if is_primary else 0.70)
            except Exception:
                pass
            sub.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
            sub.setMaxLines(2)
            text_wrap.addView(sub)
            if is_primary:
                _nowplay_meta["sub_view"] = sub
            card.addView(text_wrap, LinearLayout.LayoutParams(-1, -2))
        else:
            card.setGravity(Gravity.CENTER)
        card.setClickable(True)
        card.setFocusable(True)
        card.setOnClickListener(listener)
        if tactile:
            card.setOnTouchListener(PressTouchListener())
        return card
    if not _use_focus_style:
        primary_card = _create_card(
            tr("nowfy_tab_card_now_title"),
            tr("nowfy_tab_card_now_sub"),
            ICON_HEADPHONES,
            "nowfy_tab_headphones.png",
            True,
            SendNowPlayButtonListener(),
            True
        )
        primary_lp = LinearLayout.LayoutParams(-1, -2)
        primary_lp.setMargins(AndroidUtilities.dp(6), AndroidUtilities.dp(14), AndroidUtilities.dp(6), AndroidUtilities.dp(10))
        vertical_container.addView(primary_card, primary_lp)
        if _control_enabled:
            secondary_row = LinearLayout(context)
            secondary_row.setOrientation(LinearLayout.HORIZONTAL)
            secondary_row.setGravity(Gravity.CENTER_VERTICAL)
            panel_card = _create_card(
                "",
                "",
                ICON_SETTINGS_TAB_CONTROL,
                "nowfy_tab_settings_control.png",
                False,
                PanelButtonListener()
            )
            control_card = _create_card(
                "",
                "",
                _control_tab_icon_url,
                "nowfy_tab_control.png",
                False,
                ControlOpenListener()
            )
            panel_lp = LinearLayout.LayoutParams(0, -2, 1.0)
            panel_lp.setMargins(AndroidUtilities.dp(6), AndroidUtilities.dp(4), AndroidUtilities.dp(5), AndroidUtilities.dp(6))
            control_lp = LinearLayout.LayoutParams(0, -2, 1.0)
            control_lp.setMargins(AndroidUtilities.dp(5), AndroidUtilities.dp(4), AndroidUtilities.dp(6), AndroidUtilities.dp(6))
            secondary_row.addView(panel_card, panel_lp)
            secondary_row.addView(control_card, control_lp)
            vertical_container.addView(secondary_row, LinearLayout.LayoutParams(-1, -2))
        else:
            panel_card = _create_card(
                tr("nowfy_tab_card_panel_title"),
                tr("nowfy_tab_card_panel_sub"),
                ICON_GEAR,
                "nowfy_tab_settings.png",
                False,
                PanelButtonListener()
            )
            panel_lp = LinearLayout.LayoutParams(-1, -2)
            panel_lp.setMargins(AndroidUtilities.dp(6), AndroidUtilities.dp(4), AndroidUtilities.dp(6), AndroidUtilities.dp(6))
            vertical_container.addView(panel_card, panel_lp)
        status_row = LinearLayout(context)
        status_row.setOrientation(LinearLayout.HORIZONTAL)
        status_row.setGravity(Gravity.CENTER_VERTICAL)
        status_row.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(10), AndroidUtilities.dp(12), AndroidUtilities.dp(10))
        status_bg = GradientDrawable()
        status_bg.setColor(Color.TRANSPARENT)
        status_bg.setCornerRadius(AndroidUtilities.dp(16))
        status_bg.setStroke(0, Color.TRANSPARENT)
        status_row.setBackground(status_bg)
        avatar = BackupImageView(context)
        avatar.setRoundRadius(AndroidUtilities.dp(22))
        avatar_lp = LinearLayout.LayoutParams(AndroidUtilities.dp(44), AndroidUtilities.dp(44))
        avatar_lp.setMargins(0, 0, AndroidUtilities.dp(12), 0)
        status_row.addView(avatar, avatar_lp)
        text_wrap = LinearLayout(context)
        text_wrap.setOrientation(LinearLayout.VERTICAL)
        hello = TextView(context)
        hello.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
        hello.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
        try:
            hello.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
        except Exception:
            pass
        text_wrap.addView(hello)
        status = TextView(context)
        status.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
        status.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
        status.setMaxLines(2)
        text_wrap.addView(status)
        status_row.addView(text_wrap, LinearLayout.LayoutParams(-1, -2))
        status_shell = FrameLayout(context)
        status_lp = LinearLayout.LayoutParams(-1, -2)
        status_lp.setMargins(AndroidUtilities.dp(6), AndroidUtilities.dp(10), AndroidUtilities.dp(6), 0)
        status_shell.addView(status_row, FrameLayout.LayoutParams(-1, -2, Gravity.CENTER))
        trail_line = View(context)
        trail_bg = GradientDrawable()
        trail_bg.setCornerRadius(AndroidUtilities.dp(2))
        trail_bg.setColor(Color.parseColor("#7A5CFF"))
        trail_line.setBackground(trail_bg)
        trail_line.setVisibility(View.GONE)
        trail_lp = FrameLayout.LayoutParams(AndroidUtilities.dp(46), AndroidUtilities.dp(4), Gravity.TOP | Gravity.LEFT)
        status_shell.addView(trail_line, trail_lp)
        vertical_container.addView(status_shell, status_lp)
    else:
        if _is_apple_style:
            apple_container = LinearLayout(context)
            apple_container.setOrientation(LinearLayout.VERTICAL)
            if _fab_sheet_mode:
                apple_container.setPadding(AndroidUtilities.dp(0), AndroidUtilities.dp(0), AndroidUtilities.dp(0), AndroidUtilities.dp(0))
            else:
                apple_container.setPadding(AndroidUtilities.dp(10), AndroidUtilities.dp(8), AndroidUtilities.dp(10), AndroidUtilities.dp(8))
            hero = FrameLayout(context)
            hero.setClickable(False)
            hero.setFocusable(False)
            _hero_dt_listener = AppleHeroDoubleTapTouchListener()
            hero.setOnTouchListener(_hero_dt_listener)
            try:
                plugin._apple_hero_view = hero
            except Exception:
                pass
            hero_bg = GradientDrawable()
            hero_bg.setCornerRadius(AndroidUtilities.dp(24))
            hero_bg.setColor(Color.parseColor("#F7F8FB"))
            hero.setBackground(hero_bg)
            try:
                hero.setClipToOutline(True)
            except Exception:
                pass
            focus_cover = ImageView(context)
            try:
                focus_cover.setScaleType(ImageView.ScaleType.CENTER_CROP)
            except Exception:
                pass
            hero.addView(focus_cover, FrameLayout.LayoutParams(-1, -1))
            try:
                like_fx = ImageView(context)
                like_fx.setVisibility(View.GONE)
                like_fx.setAlpha(0.0)
                try:
                    like_fx.setScaleType(ImageView.ScaleType.FIT_CENTER)
                except Exception:
                    pass
                _load_icon(like_fx, "https://assets.nowfy/heart_like.png", "nowfy_tab_apple_heart_like.png")
                fx_lp = FrameLayout.LayoutParams(AndroidUtilities.dp(82), AndroidUtilities.dp(82), Gravity.CENTER)
                hero.addView(like_fx, fx_lp)
                plugin._nowfy_like_overlay_ref = like_fx
            except Exception:
                try:
                    plugin._nowfy_like_overlay_ref = None
                except Exception:
                    pass
            hero_overlay = View(context)
            hero_overlay_bg = GradientDrawable(
                GradientDrawable.Orientation.BOTTOM_TOP,
                [Color.parseColor("#DD0E111A"), Color.parseColor("#2210111A")]
            )
            hero_overlay_bg.setCornerRadius(AndroidUtilities.dp(24))
            hero_overlay.setBackground(hero_overlay_bg)
            hero.addView(hero_overlay, FrameLayout.LayoutParams(-1, -1))
            status_block = LinearLayout(context)
            status_block.setOrientation(LinearLayout.HORIZONTAL)
            status_block.setGravity(Gravity.CENTER_VERTICAL)
            status_block.setPadding(
                AndroidUtilities.dp(12),
                AndroidUtilities.dp(8 if _flow_compact_mode else 12),
                AndroidUtilities.dp(12),
                AndroidUtilities.dp(8 if _flow_compact_mode else 12)
            )
            try:
                status_glow_bg = GradientDrawable()
                status_glow_bg.setColor(Color.TRANSPARENT)
                status_glow_bg.setCornerRadius(AndroidUtilities.dp(18))
                status_glow_bg.setStroke(AndroidUtilities.dp(1), Color.argb(0, 255, 255, 255))
                status_block.setBackground(status_glow_bg)
            except Exception:
                status_glow_bg = None
            avatar = BackupImageView(context)
            avatar.setRoundRadius(AndroidUtilities.dp(20))
            avatar_lp = LinearLayout.LayoutParams(AndroidUtilities.dp(40), AndroidUtilities.dp(40))
            avatar_lp.setMargins(0, 0, AndroidUtilities.dp(10), 0)
            status_block.addView(avatar, avatar_lp)
            info_wrap = LinearLayout(context)
            info_wrap.setOrientation(LinearLayout.VERTICAL)
            hello = TextView(context)
            hello.setTextColor(Color.WHITE)
            hello.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
            try:
                hello.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
            except Exception:
                pass
            info_wrap.addView(hello)
            status = TextView(context)
            status.setTextColor(Color.parseColor("#DDE3F5"))
            status.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 12)
            status.setMaxLines(2)
            info_wrap.addView(status)
            status_block.addView(info_wrap, LinearLayout.LayoutParams(-1, -2))
            if _chatlist_flow_mode:
                try:
                    reserve_right = View(context)
                    status_block.addView(
                        reserve_right,
                        LinearLayout.LayoutParams(AndroidUtilities.dp(78), 1)
                    )
                except Exception:
                    pass
            status_lp = FrameLayout.LayoutParams(-1, -2, Gravity.TOP | Gravity.LEFT)
            status_lp.setMargins(AndroidUtilities.dp(14), AndroidUtilities.dp(10 if _flow_compact_mode else 14), AndroidUtilities.dp(14), 0)
            hero.addView(status_block, status_lp)
            try:
                _srcs_preview, _labels_preview = plugin._get_tab_source_options()
                _idx_preview = int(plugin.get_setting("nowfy_tab_source", 0) or 0)
                if _idx_preview < 0 or _idx_preview >= len(_srcs_preview):
                    _idx_preview = 0
                _source_key_preview = _srcs_preview[_idx_preview] if _srcs_preview else "spotify"
            except Exception:
                _source_key_preview = "spotify"
            try:
                _music_preview_enabled = int(plugin.get_setting("nowfy_music_preview_button", 1) or 0) == 1
            except Exception:
                _music_preview_enabled = True
            try:
                _track_download_enabled = int(plugin.get_setting("nowfy_track_download_button", 1) or 0) == 1
            except Exception:
                _track_download_enabled = True
            _show_music_preview = bool(_music_preview_enabled)
            now_button = LinearLayout(context)
            now_button.setOrientation(LinearLayout.HORIZONTAL)
            now_button.setGravity(Gravity.CENTER_VERTICAL)
            now_button.setClickable(True)
            now_button.setFocusable(True)
            now_button.setOnClickListener(SendNowPlayButtonListener())
            now_button.setOnLongClickListener(SharePreviewLongClickListener())
            now_button.setOnTouchListener(PressTouchListener())
            now_button.setBackground(None)
            now_button.setPadding(AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6))
            share_text = TextView(context)
            share_text.setText(tr("nowfy_tab_share"))
            share_text.setTextColor(Color.WHITE)
            share_text.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 12)
            try:
                share_text.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
            except Exception:
                pass
            text_lp = LinearLayout.LayoutParams(-2, -2)
            text_lp.setMargins(0, 0, AndroidUtilities.dp(8), 0)
            now_button.addView(share_text, text_lp)
            icon_np = ImageView(context)
            try:
                icon_np.setScaleType(ImageView.ScaleType.FIT_CENTER)
            except Exception:
                pass
            icon_np_lp = LinearLayout.LayoutParams(AndroidUtilities.dp(30), AndroidUtilities.dp(30))
            now_button.addView(icon_np, icon_np_lp)
            _load_icon(icon_np, "https://assets.nowfy/share-now-playing.png", "nowfy_tab_apple_nowplay.png")
            buttons_shadow = View(context)
            shadow_bg = GradientDrawable(
                GradientDrawable.Orientation.BOTTOM_TOP,
                [Color.parseColor("#B0121622"), Color.parseColor("#00121622")]
            )
            shadow_bg.setCornerRadius(AndroidUtilities.dp(24))
            buttons_shadow.setBackground(shadow_bg)
            hero.addView(buttons_shadow, FrameLayout.LayoutParams(-1, AndroidUtilities.dp(88), Gravity.BOTTOM))
            now_lp = FrameLayout.LayoutParams(-2, -2, Gravity.BOTTOM | Gravity.RIGHT)
            now_lp.setMargins(0, 0, AndroidUtilities.dp(12), AndroidUtilities.dp(12))
            if not _chatlist_flow_mode:
                hero.addView(now_button, now_lp)
            if _track_download_enabled:
                _like_btn_supported = bool(_is_like_supported_source())
                if _like_btn_supported:
                    like_btn = FrameLayout(context)
                    like_btn.setClickable(True)
                    like_btn.setFocusable(True)
                    like_btn.setOnClickListener(LikeButtonListener())
                    like_btn.setOnTouchListener(PressTouchListener())
                    like_btn.setBackground(None)
                    like_btn.setPadding(AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6))
                    like_icon = ImageView(context)
                    try:
                        like_icon.setScaleType(ImageView.ScaleType.FIT_CENTER)
                    except Exception:
                        pass
                    like_icon_lp = FrameLayout.LayoutParams(AndroidUtilities.dp(28), AndroidUtilities.dp(28), Gravity.CENTER)
                    like_btn.addView(like_icon, like_icon_lp)
                    _load_icon(like_icon, "https://assets.nowfy/heart_like.png", "nowfy_tab_apple_heart_like.png")
                    try:
                        setattr(plugin, "_nowfy_like_icon_ref", like_icon)
                        setattr(plugin, "_nowfy_like_btn_ref", like_btn)
                    except Exception:
                        pass
                    try:
                        like_btn.setVisibility(View.GONE)
                        like_icon.setVisibility(View.GONE)
                    except Exception:
                        pass
                    like_lp = FrameLayout.LayoutParams(-2, -2, Gravity.TOP | Gravity.RIGHT)
                    like_right = AndroidUtilities.dp(12 if _chatlist_flow_mode else 48)
                    like_lp.setMargins(0, AndroidUtilities.dp(12), like_right, 0)
                    hero.addView(like_btn, like_lp)
                if not _chatlist_flow_mode:
                    track_download_btn = FrameLayout(context)
                    track_download_btn.setClickable(True)
                    track_download_btn.setFocusable(True)
                    track_download_btn.setOnClickListener(TrackDownloadButtonListener())
                    track_download_btn.setOnTouchListener(PressTouchListener())
                    track_download_btn.setBackground(None)
                    track_download_btn.setPadding(AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6))
                    track_download_icon = ImageView(context)
                    try:
                        track_download_icon.setScaleType(ImageView.ScaleType.FIT_CENTER)
                    except Exception:
                        pass
                    track_download_icon_lp = FrameLayout.LayoutParams(AndroidUtilities.dp(28), AndroidUtilities.dp(28), Gravity.CENTER)
                    track_download_btn.addView(track_download_icon, track_download_icon_lp)
                    _load_icon(track_download_icon, ICON_TRACK_DOWNLOAD_BUTTON, "nowfy_tab_apple_track_download.png")
                    try:
                        setattr(plugin, "_nowfy_track_download_icon_ref", track_download_icon)
                    except Exception:
                        pass
                    track_download_lp = FrameLayout.LayoutParams(-2, -2, Gravity.TOP | Gravity.RIGHT)
                    track_download_lp.setMargins(0, AndroidUtilities.dp(12), AndroidUtilities.dp(12), 0)
                    hero.addView(track_download_btn, track_download_lp)
            if (not _chatlist_flow_mode) and _show_music_preview:
                preview_btn = FrameLayout(context)
                preview_btn.setClickable(True)
                preview_btn.setFocusable(True)
                preview_btn.setOnClickListener(MusicPreviewButtonListener())
                preview_btn.setOnLongClickListener(MusicPreviewButtonHoldListener())
                preview_btn.setOnTouchListener(PressTouchListener())
                preview_btn.setBackground(None)
                preview_btn.setPadding(AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6))
                preview_icon = ImageView(context)
                try:
                    preview_icon.setScaleType(ImageView.ScaleType.FIT_CENTER)
                except Exception:
                    pass
                preview_icon_lp = FrameLayout.LayoutParams(AndroidUtilities.dp(28), AndroidUtilities.dp(28), Gravity.CENTER)
                preview_btn.addView(preview_icon, preview_icon_lp)
                _load_icon(preview_icon, ICON_MUSIC_PREVIEW_BUTTON, "nowfy_tab_apple_music_preview.png")
                preview_lp = FrameLayout.LayoutParams(-2, -2, Gravity.BOTTOM | Gravity.RIGHT)
                preview_lp.setMargins(0, 0, AndroidUtilities.dp(12), AndroidUtilities.dp(52))
                hero.addView(preview_btn, preview_lp)
            if _fab_sheet_mode:
                hero_h = AndroidUtilities.dp(196 if _flow_compact_mode else 290)
            else:
                hero_h = AndroidUtilities.dp(224)
            hero_lp = LinearLayout.LayoutParams(-1, hero_h)
            if _fab_sheet_mode:
                hero_lp.setMargins(AndroidUtilities.dp(10), AndroidUtilities.dp(10), AndroidUtilities.dp(10), AndroidUtilities.dp(0))
            else:
                hero_lp.setMargins(0, AndroidUtilities.dp(14), 0, AndroidUtilities.dp(2))
            apple_container.addView(hero, hero_lp)
            if not _fab_sheet_mode:
                footer = TextView(context)
                try:
                    _srcs, _labels = plugin._get_tab_source_options()
                    _idx = int(plugin.get_setting("nowfy_tab_source", 0) or 0)
                    if _idx < 0 or _idx >= len(_labels):
                        _idx = 0
                    _label = _labels[_idx] if _labels else "Spotify"
                except Exception:
                    _label = "Spotify"
                try:
                    _source_key = _srcs[_idx] if _srcs and _idx < len(_srcs) else "spotify"
                except Exception:
                    _source_key = "spotify"
                try:
                    _music_preview_enabled = int(plugin.get_setting("nowfy_music_preview_button", 1) or 0) == 1
                except Exception:
                    _music_preview_enabled = True
                _show_music_preview = bool(_music_preview_enabled)
                footer.setText(f"{_label} • Powered by Nowfy")
                try:
                    footer.setTextColor(Color.parseColor("#B0B0B0"))
                except Exception:
                    footer.setTextColor(Color.GRAY)
                footer.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 12)
                footer.setGravity(Gravity.CENTER)
                try:
                    footer.setShadowLayer(2.5, 0.0, 1.0, Color.parseColor("#55000000"))
                except Exception:
                    pass
                try:
                    footer.setIncludeFontPadding(True)
                except Exception:
                    pass
                try:
                    footer.setPadding(0, AndroidUtilities.dp(2), 0, AndroidUtilities.dp(2))
                except Exception:
                    pass
                footer_lp = LinearLayout.LayoutParams(-1, -2)
                footer_lp.setMargins(0, AndroidUtilities.dp(2), 0, AndroidUtilities.dp(0))
                apple_container.addView(footer, footer_lp)
            actions = LinearLayout(context)
            actions.setOrientation(LinearLayout.HORIZONTAL)
            actions.setGravity(Gravity.CENTER_VERTICAL)
            def _apple_icon_button(icon_url, icon_cache, listener):
                btn = FrameLayout(context)
                btn.setClickable(True)
                btn.setFocusable(True)
                btn.setOnClickListener(listener)
                btn.setOnTouchListener(PressTouchListener())
                btn.setBackground(None)
                btn.setPadding(AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6))
                icon = ImageView(context)
                try:
                    icon.setScaleType(ImageView.ScaleType.FIT_CENTER)
                except Exception:
                    pass
                icon_lp = FrameLayout.LayoutParams(AndroidUtilities.dp(28), AndroidUtilities.dp(28), Gravity.CENTER)
                btn.addView(icon, icon_lp)
                _load_icon(icon, icon_url, icon_cache)
                return btn
            btn_settings = _apple_icon_button("https://assets.nowfy/nowfy_gr.png", "nowfy_tab_apple_settings.png", PanelButtonListener())
            btn_control = _apple_icon_button("https://assets.nowfy/control.png", "nowfy_tab_apple_control.png", ControlOpenListener())
            actions.addView(btn_settings, LinearLayout.LayoutParams(-2, -2))
            if _control_enabled:
                actions.addView(btn_control, LinearLayout.LayoutParams(-2, -2))
            try:
                _raw_lyrics_state = plugin.get_setting("nowfy_lyrics_button", 1)
                if isinstance(_raw_lyrics_state, bool):
                    _lyrics_sel = 1 if _raw_lyrics_state else 0
                elif isinstance(_raw_lyrics_state, str):
                    _s = _raw_lyrics_state.strip().lower()
                    _lyrics_sel = 1 if _s in ("1", "on", "true", "ativado") else 0
                else:
                    _lyrics_sel = int(_raw_lyrics_state or 1)
                _lyrics_btn_enabled = bool(_is_apple_style and _lyrics_sel == 1)
            except Exception:
                _lyrics_btn_enabled = False
            if _lyrics_btn_enabled:
                class LyricsOpenListener(dynamic_proxy(View.OnClickListener)):
                    def onClick(self, v):
                        try:
                            run_on_ui_thread(_open_lyrics_safe)
                        except Exception:
                            _open_lyrics_safe()
                btn_lyrics = _apple_icon_button(ICON_LYRICS_BUTTON, "nowfy_tab_apple_lyrics.png", LyricsOpenListener())
                actions.addView(btn_lyrics, LinearLayout.LayoutParams(-2, -2))
            try:
                _raw_embed_state = plugin.get_setting("nowfy_embed_button", 1)
                if isinstance(_raw_embed_state, bool):
                    _embed_sel = 1 if _raw_embed_state else 0
                elif isinstance(_raw_embed_state, str):
                    _s2 = _raw_embed_state.strip().lower()
                    _embed_sel = 1 if _s2 in ("1", "on", "true", "ativado") else 0
                else:
                    _embed_sel = int(_raw_embed_state or 1)
                _embed_btn_enabled = bool(_is_apple_style and _embed_sel == 1)
            except Exception:
                _embed_btn_enabled = False
            if _embed_btn_enabled:
                class EmbedOpenListener(dynamic_proxy(View.OnClickListener)):
                    def onClick(self, v):
                        try:
                            try:
                                log("[Nowfy] Link button clicked")
                            except Exception:
                                pass
                            plugin._open_nowtab_embed()
                        except Exception:
                            pass
                btn_embed = _apple_icon_button(ICON_LINK_BUTTON, "nowfy_tab_apple_link.png", EmbedOpenListener())
                actions.addView(btn_embed, LinearLayout.LayoutParams(-2, -2))
            actions_lp = FrameLayout.LayoutParams(-2, -2, Gravity.BOTTOM | Gravity.LEFT)
            actions_lp.setMargins(AndroidUtilities.dp(12), 0, 0, AndroidUtilities.dp(12))
            hero.addView(actions, actions_lp)
            vertical_container.addView(apple_container, LinearLayout.LayoutParams(-1, -2))
        else:
            try:
                plugin._apple_hero_view = None
            except Exception:
                pass
            focus_row = LinearLayout(context)
            focus_row.setOrientation(LinearLayout.HORIZONTAL)
            focus_row.setGravity(Gravity.TOP)
            focus_row.setPadding(AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6))
            focus_card = FrameLayout(context)
            focus_card.setClickable(True)
            focus_card.setFocusable(True)
            focus_card.setOnClickListener(SendNowPlayButtonListener())
            focus_card.setOnTouchListener(PressTouchListener())
            cover_bg = GradientDrawable()
            cover_bg.setCornerRadius(AndroidUtilities.dp(22))
            cover_bg.setColor(Color.parseColor("#1A1E2B"))
            focus_card.setBackground(cover_bg)
            try:
                focus_card.setClipToOutline(True)
            except Exception:
                pass
            focus_cover = ImageView(context)
            try:
                focus_cover.setScaleType(ImageView.ScaleType.CENTER_CROP)
            except Exception:
                pass
            focus_card.addView(focus_cover, FrameLayout.LayoutParams(-1, -1))
            overlay = View(context)
            overlay_bg = GradientDrawable(
                GradientDrawable.Orientation.TOP_BOTTOM,
                [Color.parseColor("#5510151E"), Color.parseColor("#CC0A0D16")]
            )
            overlay_bg.setCornerRadius(AndroidUtilities.dp(22))
            overlay.setBackground(overlay_bg)
            focus_card.addView(overlay, FrameLayout.LayoutParams(-1, -1))
            title_wrap = LinearLayout(context)
            title_wrap.setOrientation(LinearLayout.HORIZONTAL)
            title_wrap.setGravity(Gravity.CENTER_VERTICAL)
            title_wrap.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(14), AndroidUtilities.dp(16), AndroidUtilities.dp(14))
            title_lp = FrameLayout.LayoutParams(-1, -2, Gravity.TOP | Gravity.LEFT)
            focus_card.addView(title_wrap, title_lp)
            icon_np = ImageView(context)
            try:
                icon_np.setScaleType(ImageView.ScaleType.FIT_CENTER)
            except Exception:
                pass
            icon_np_lp = LinearLayout.LayoutParams(AndroidUtilities.dp(26), AndroidUtilities.dp(26))
            icon_np_lp.setMargins(0, 0, AndroidUtilities.dp(10), 0)
            title_wrap.addView(icon_np, icon_np_lp)
            _load_icon(icon_np, ICON_HEADPHONES, "nowfy_tab_headphones.png")
            title_text = TextView(context)
            title_text.setText(tr("nowfy_tab_card_now_title"))
            title_text.setTextColor(Color.WHITE)
            title_text.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18)
            try:
                title_text.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
            except Exception:
                pass
            title_wrap.addView(title_text)
            focus_card_lp = LinearLayout.LayoutParams(0, AndroidUtilities.dp(210), 1.0)
            focus_card_lp.setMargins(0, 0, AndroidUtilities.dp(10), 0)
            focus_row.addView(focus_card, focus_card_lp)
            right_col = LinearLayout(context)
            right_col.setOrientation(LinearLayout.VERTICAL)
            right_col.setGravity(Gravity.TOP)
            def _make_focus_button(label, icon_url, icon_cache, listener):
                wrap = LinearLayout(context)
                wrap.setOrientation(LinearLayout.HORIZONTAL)
                wrap.setGravity(Gravity.CENTER_VERTICAL)
                wrap.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(12), AndroidUtilities.dp(16), AndroidUtilities.dp(12))
                bg = GradientDrawable()
                bg.setColor(Color.parseColor("#1E2638"))
                bg.setCornerRadius(AndroidUtilities.dp(18))
                try:
                    bg.setStroke(AndroidUtilities.dp(1), Color.parseColor("#2C3B5A"))
                except Exception:
                    pass
                wrap.setBackground(bg)
                icon = ImageView(context)
                try:
                    icon.setScaleType(ImageView.ScaleType.FIT_CENTER)
                except Exception:
                    pass
                icon_lp = LinearLayout.LayoutParams(AndroidUtilities.dp(26), AndroidUtilities.dp(26))
                icon_lp.setMargins(0, 0, AndroidUtilities.dp(12), 0)
                wrap.addView(icon, icon_lp)
                _load_icon(icon, icon_url, icon_cache)
                text = TextView(context)
                text.setText(label)
                text.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
                text.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
                try:
                    text.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
                except Exception:
                    pass
                wrap.addView(text, LinearLayout.LayoutParams(-2, -2))
                wrap.setClickable(True)
                wrap.setFocusable(True)
                wrap.setOnClickListener(listener)
                wrap.setOnTouchListener(PressTouchListener())
                return wrap
            btn_settings = _make_focus_button("Nowfy Settings", ICON_SETTINGS_TAB_CONTROL, "nowfy_tab_settings_control.png", PanelButtonListener())
            _control_available = bool(_control_enabled)
            if _control_available:
                btn_control = _make_focus_button("Nowfy Control", _control_tab_icon_url, "nowfy_tab_control.png", ControlOpenListener())
            right_col.addView(btn_settings, LinearLayout.LayoutParams(-1, -2))
            if _control_available:
                btn_control_lp = LinearLayout.LayoutParams(-1, -2)
                btn_control_lp.setMargins(0, AndroidUtilities.dp(10), 0, 0)
                right_col.addView(btn_control, btn_control_lp)
            try:
                _raw_lyrics_state = plugin.get_setting("nowfy_lyrics_button", 1)
                if isinstance(_raw_lyrics_state, bool):
                    _lyrics_sel = 1 if _raw_lyrics_state else 0
                elif isinstance(_raw_lyrics_state, str):
                    _s = _raw_lyrics_state.strip().lower()
                    _lyrics_sel = 1 if _s in ("1", "on", "true", "ativado") else 0
                else:
                    _lyrics_sel = int(_raw_lyrics_state or 1)
                _lyrics_btn_enabled = bool(_is_apple_style and _lyrics_sel == 1)
            except Exception:
                _lyrics_btn_enabled = False
            if _lyrics_btn_enabled:
                class LyricsOpenListener(dynamic_proxy(View.OnClickListener)):
                    def onClick(self, v):
                        try:
                            run_on_ui_thread(_open_lyrics_safe)
                        except Exception:
                            _open_lyrics_safe()
                btn_lyrics = _make_focus_button(tr("lyrics_button"), ICON_LYRICS_BUTTON, "nowfy_tab_lyrics.png", LyricsOpenListener())
                btn_lyrics_lp = LinearLayout.LayoutParams(-1, -2)
                btn_lyrics_lp.setMargins(0, AndroidUtilities.dp(10), 0, 0)
                right_col.addView(btn_lyrics, btn_lyrics_lp)
            status_block = LinearLayout(context)
            status_block.setOrientation(LinearLayout.HORIZONTAL)
            status_block.setGravity(Gravity.CENTER_VERTICAL)
            status_block.setPadding(0, AndroidUtilities.dp(16), 0, 0)
            avatar = BackupImageView(context)
            avatar.setRoundRadius(AndroidUtilities.dp(18))
            avatar_lp = LinearLayout.LayoutParams(AndroidUtilities.dp(36), AndroidUtilities.dp(36))
            avatar_lp.setMargins(0, 0, AndroidUtilities.dp(10), 0)
            status_block.addView(avatar, avatar_lp)
            info_wrap = LinearLayout(context)
            info_wrap.setOrientation(LinearLayout.VERTICAL)
            hello = TextView(context)
            hello.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            hello.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
            try:
                hello.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
            except Exception:
                pass
            info_wrap.addView(hello)
            status = TextView(context)
            status.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            status.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 12)
            status.setMaxLines(2)
            info_wrap.addView(status)
            status_block.addView(info_wrap, LinearLayout.LayoutParams(-1, -2))
            right_col.addView(status_block, LinearLayout.LayoutParams(-1, -2))
            right_lp = LinearLayout.LayoutParams(0, -2, 1.12)
            focus_row.addView(right_col, right_lp)
            vertical_container.addView(focus_row, LinearLayout.LayoutParams(-1, -2))
    title_row = LinearLayout(context)
    title_row.setOrientation(LinearLayout.HORIZONTAL)
    if _fab_sheet_mode:
        title_row.setGravity(Gravity.CENTER)
    else:
        title_row.setGravity(Gravity.CENTER_VERTICAL)
    control_title = TextView(context)
    control_title.setText("NOWFY CONTROL")
    if _fab_sheet_mode:
        control_title.setTextColor(Color.WHITE)
    else:
        control_title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
    control_title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13 if _fab_sheet_mode else 18)
    try:
        control_title.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
    except Exception:
        pass
    try:
        if _fab_sheet_mode:
            control_title.setAlpha(0.82)
    except Exception:
        pass
    try:
        if _is_flow_compact_control and (not _flow_transparent_mode):
            control_title.setVisibility(View.GONE)
    except Exception:
        pass
    control_title.setGravity(Gravity.CENTER)
    if _fab_sheet_mode:
        title_row.addView(control_title, LinearLayout.LayoutParams(-1, -2))
    else:
        title_row.addView(control_title, LinearLayout.LayoutParams(0, -2, 1.0))

    def _make_volume_title_button(icon_url, cache_name, listener, fallback_symbol):
        btn = FrameLayout(context)
        bg = GradientDrawable()
        if _fab_sheet_mode:
            bg.setColor(Color.argb(58, 255, 255, 255))
        else:
            bg.setColor(Color.parseColor("#2F3B73"))
        bg.setCornerRadius(AndroidUtilities.dp(22 if _fab_sheet_mode else 12))
        try:
            bg.setStroke(0, 0)
        except Exception:
            pass
        btn.setBackground(bg)
        btn.setClickable(True)
        btn.setFocusable(True)
        btn.setOnClickListener(listener)
        btn.setOnTouchListener(PressTouchListener())
        icon_view = ImageView(context)
        try:
            icon_view.setScaleType(ImageView.ScaleType.CENTER_INSIDE)
        except Exception:
            pass
        icon_lp = FrameLayout.LayoutParams(AndroidUtilities.dp(16), AndroidUtilities.dp(16), Gravity.CENTER)
        btn.addView(icon_view, icon_lp)
        fallback_view = TextView(context)
        fallback_view.setText(fallback_symbol)
        fallback_view.setGravity(Gravity.CENTER)
        fallback_view.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
        if _fab_sheet_mode:
            fallback_view.setTextColor(_flow_text_primary)
        else:
            fallback_view.setTextColor(Color.WHITE)
        try:
            fallback_view.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
        except Exception:
            pass
        btn.addView(fallback_view, FrameLayout.LayoutParams(-2, -2, Gravity.CENTER))
        _apply_control_icon(icon_view, fallback_view, icon_url, fallback_symbol, cache_name)
        return btn
    vol_down_btn = _make_volume_title_button(
        ICON_CONTROL_VOL_MINUS,
        "nowfy_control_vol_minus.png",
        ControlVolumeDownListener(),
        "-"
    )
    vol_up_btn = _make_volume_title_button(
        ICON_CONTROL_VOL_PLUS,
        "nowfy_control_vol_plus.png",
        ControlVolumeUpListener(),
        "+"
    )
    vol_down_lp = LinearLayout.LayoutParams(
        AndroidUtilities.dp(40 if _is_flow_compact_control else (50 if _fab_sheet_mode else 34)),
        AndroidUtilities.dp(40 if _is_flow_compact_control else (50 if _fab_sheet_mode else 34))
    )
    vol_down_lp.setMargins(AndroidUtilities.dp(3 if _is_flow_compact_control else 6), 0, AndroidUtilities.dp(3 if _is_flow_compact_control else 4), 0)
    if not _fab_sheet_mode:
        title_row.addView(vol_down_btn, vol_down_lp)
    vol_up_lp = LinearLayout.LayoutParams(
        AndroidUtilities.dp(40 if _is_flow_compact_control else (50 if _fab_sheet_mode else 34)),
        AndroidUtilities.dp(40 if _is_flow_compact_control else (50 if _fab_sheet_mode else 34))
    )
    vol_up_lp.setMargins(AndroidUtilities.dp(3 if _is_flow_compact_control else 4), 0, AndroidUtilities.dp(3 if _is_flow_compact_control else 0), 0)
    if not _fab_sheet_mode:
        title_row.addView(vol_up_btn, vol_up_lp)
    control_lp = LinearLayout.LayoutParams(-1, -2)
    control_lp.setMargins(AndroidUtilities.dp(6), AndroidUtilities.dp(8), AndroidUtilities.dp(6), AndroidUtilities.dp(6 if _is_flow_compact_control else 12))
    control_container.addView(title_row, control_lp)
    if _fab_sheet_mode and control_foreground_host is not None:
        try:
            chip_row = LinearLayout(context)
            chip_row.setOrientation(LinearLayout.HORIZONTAL)
            chip_row.setGravity(Gravity.CENTER_HORIZONTAL)
            def _make_flow_chip(label, listener, icon_url, cache_name):
                chip = LinearLayout(context)
                chip.setOrientation(LinearLayout.HORIZONTAL)
                chip.setGravity(Gravity.CENTER_VERTICAL)
                chip.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(8), AndroidUtilities.dp(14), AndroidUtilities.dp(8))
                chip_bg = GradientDrawable()
                chip_bg.setCornerRadius(AndroidUtilities.dp(24))
                chip_bg.setColor(Color.argb(70, 20, 24, 38))
                try:
                    chip_bg.setStroke(AndroidUtilities.dp(1), Color.argb(80, 255, 255, 255))
                except Exception:
                    pass
                chip.setBackground(chip_bg)
                chip_icon = ImageView(context)
                try:
                    chip_icon.setScaleType(ImageView.ScaleType.CENTER_INSIDE)
                except Exception:
                    pass
                chip.addView(chip_icon, LinearLayout.LayoutParams(AndroidUtilities.dp(18), AndroidUtilities.dp(18)))
                _load_icon(chip_icon, icon_url, cache_name)
                chip_text = TextView(context)
                chip_text.setText(label)
                chip_text.setTextColor(Color.WHITE)
                chip_text.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
                chip_text.setGravity(Gravity.CENTER_VERTICAL)
                try:
                    chip_text.setIncludeFontPadding(False)
                    chip_text.setTranslationY(-float(AndroidUtilities.dp(1)))
                except Exception:
                    pass
                try:
                    chip_text.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
                except Exception:
                    pass
                lp_txt = LinearLayout.LayoutParams(-2, -2)
                lp_txt.leftMargin = AndroidUtilities.dp(8)
                chip.addView(chip_text, lp_txt)
                chip.setClickable(True)
                chip.setFocusable(True)
                chip.setOnClickListener(listener)
                chip.setOnTouchListener(PressTouchListener())
                return chip
            chip_back = _make_flow_chip(tr("nowfy_control_back_label"), ControlReturnListener(), "https://assets.nowfy/back_button.png", "nowfy_control_back_chip.png")
            chip_search = _make_flow_chip(tr("search_button"), ControlSearchListener(), ICON_CONTROL_SEARCH, "nowfy_control_search_chip.png")
            lp_back = LinearLayout.LayoutParams(-2, -2)
            lp_back.rightMargin = AndroidUtilities.dp(8)
            chip_row.addView(chip_back, lp_back)
            chip_row.addView(chip_search, LinearLayout.LayoutParams(-2, -2))
            lp_chip = LinearLayout.LayoutParams(-2, -2)
            lp_chip.bottomMargin = AndroidUtilities.dp(8)
            lp_chip.gravity = Gravity.CENTER_HORIZONTAL
            control_foreground_host.addView(chip_row, 0, lp_chip)
        except Exception:
            pass
    premium_notice_bg = None
    if not _is_flow_compact_control:
        premium_notice_wrap = LinearLayout(context)
        premium_notice_wrap.setOrientation(LinearLayout.VERTICAL)
        premium_notice_wrap.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(10), AndroidUtilities.dp(12), AndroidUtilities.dp(10))
        premium_notice_bg = GradientDrawable()
        if _fab_sheet_mode:
            premium_notice_bg.setColor(_flow_notice_bg)
        else:
            premium_notice_bg.setColor(Color.parseColor("#243058"))
        premium_notice_bg.setCornerRadius(AndroidUtilities.dp(12))
        try:
            premium_notice_bg.setStroke(0, 0)
        except Exception:
            pass
        premium_notice_wrap.setBackground(premium_notice_bg)
        premium_title = TextView(context)
        premium_title.setText(tr("nowfy_control_premium_notice_title"))
        premium_title.setTextColor(Color.WHITE)
        premium_title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
        try:
            premium_title.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
        except Exception:
            pass
        premium_notice_wrap.addView(premium_title)
        premium_sub = TextView(context)
        premium_sub.setText(tr("nowfy_control_premium_notice_sub"))
        premium_sub.setTextColor(Color.parseColor("#E9EEFF"))
        premium_sub.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 12)
        premium_sub.setMaxLines(3)
        premium_notice_wrap.addView(premium_sub)
        premium_lp = LinearLayout.LayoutParams(-1, -2)
        premium_lp.setMargins(AndroidUtilities.dp(6), 0, AndroidUtilities.dp(6), AndroidUtilities.dp(10))
        control_container.addView(premium_notice_wrap, premium_lp)
    try:
        import threading
        def _get_nowtab_source_key():
            try:
                sources, _labels = plugin._get_tab_source_options()
                idx = int(plugin.get_setting("nowfy_tab_source", 0) or 0)
                if idx < 0 or idx >= len(sources):
                    idx = 0
                return str(sources[idx] or "").strip().lower()
            except Exception:
                return "spotify"
        def _update_premium_notice():
            try:
                source_key = _get_nowtab_source_key()
                if source_key == "lastfm":
                    run_on_ui_thread(lambda: premium_title.setText("Nowfy Control"))
                    run_on_ui_thread(lambda: premium_sub.setText("Compatible with Spotify (API) and Stats.fm."))
                    return
                if not hasattr(plugin, "_get_spotify_user_profile"):
                    return
                profile = plugin._get_spotify_user_profile()
                product_raw = str((profile or {}).get("product") or "").strip().lower()
                if product_raw == "premium":
                    run_on_ui_thread(lambda: premium_title.setText(tr("nowfy_control_ready_title")))
                    run_on_ui_thread(lambda: premium_sub.setText(tr("nowfy_control_ready_sub")))
                else:
                    run_on_ui_thread(lambda: premium_title.setText(tr("nowfy_control_premium_notice_title")))
                    run_on_ui_thread(lambda: premium_sub.setText(tr("nowfy_control_premium_notice_sub")))
            except Exception:
                pass
        if not _is_flow_compact_control:
            threading.Thread(target=_update_premium_notice, daemon=True).start()
    except Exception:
        pass
    controls_row = LinearLayout(context)
    controls_row.setOrientation(LinearLayout.HORIZONTAL)
    controls_row.setGravity(Gravity.CENTER)
    controls_row.setPadding(AndroidUtilities.dp(4), AndroidUtilities.dp(4), AndroidUtilities.dp(4), AndroidUtilities.dp(4))
    play_icon_url = ICON_CONTROL_PLAY
    pause_icon_url = ICON_CONTROL_PAUSE
    back_icon_url = ICON_CONTROL_BACK
    skip_icon_url = ICON_CONTROL_SKIP
    search_icon_url = ICON_CONTROL_SEARCH

    def _make_control_button(symbol, listener, icon_url="", cache_name=""):
        btn = FrameLayout(context)
        bg = GradientDrawable()
        if _fab_sheet_mode:
            bg.setColor(Color.argb(58, 255, 255, 255))
        else:
            bg.setColor(Color.parseColor("#2F3B73"))
        bg.setCornerRadius(AndroidUtilities.dp(32 if _fab_sheet_mode else 18))
        try:
            if _fab_sheet_mode:
                bg.setStroke(AndroidUtilities.dp(1), Color.argb(74, 255, 255, 255))
            else:
                bg.setStroke(0, 0)
        except Exception:
            pass
        btn.setBackground(bg)
        btn.setClickable(True)
        btn.setFocusable(True)
        btn.setOnClickListener(listener)
        btn.setOnTouchListener(PressTouchListener())
        icon_view = ImageView(context)
        try:
            icon_view.setScaleType(ImageView.ScaleType.CENTER_INSIDE)
        except Exception:
            pass
        icon_lp = FrameLayout.LayoutParams(AndroidUtilities.dp(30), AndroidUtilities.dp(30), Gravity.CENTER)
        btn.addView(icon_view, icon_lp)
        fallback_view = TextView(context)
        fallback_view.setText(symbol)
        fallback_view.setGravity(Gravity.CENTER)
        fallback_view.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 24)
        if _fab_sheet_mode:
            fallback_view.setTextColor(_flow_text_primary)
        else:
            fallback_view.setTextColor(Color.WHITE)
        try:
            fallback_view.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
        except Exception:
            pass
        fallback_lp = FrameLayout.LayoutParams(-2, -2, Gravity.CENTER)
        btn.addView(fallback_view, fallback_lp)
        _apply_control_icon(icon_view, fallback_view, icon_url, symbol, cache_name)
        if _fab_sheet_mode:
            btn_size = AndroidUtilities.dp(46 if _is_flow_compact_control else 64)
            lp = LinearLayout.LayoutParams(btn_size, btn_size)
            lp.setMargins(AndroidUtilities.dp(3 if _is_flow_compact_control else 4), 0, AndroidUtilities.dp(3 if _is_flow_compact_control else 4), 0)
        else:
            lp = LinearLayout.LayoutParams(0, AndroidUtilities.dp(68 if _is_flow_compact_control else 84), 1.0)
            lp.setMargins(AndroidUtilities.dp(6), 0, AndroidUtilities.dp(6), 0)
        return btn, icon_view, fallback_view, lp
    btn_back, btn_back_icon, btn_back_fallback, lp_back = _make_control_button(
        "⏮", ControlBackListener(), back_icon_url, "nowfy_control_back.png"
    )
    btn_play_pause, btn_play_pause_icon, btn_play_pause_fallback, lp_pp = _make_control_button(
        "▶", ControlPlayPauseListener(), play_icon_url, "nowfy_control_play_pause.png"
    )
    btn_skip, btn_skip_icon, btn_skip_fallback, lp_skip = _make_control_button(
        "⏭", ControlSkipListener(), skip_icon_url, "nowfy_control_skip.png"
    )
    btn_search, btn_search_icon, btn_search_fallback, lp_search = _make_control_button(
        "⌕", ControlSearchListener(), search_icon_url, "nowfy_control_search.png"
    )
    _show_search_in_main_row = True
    if _fab_sheet_mode:
        _show_search_in_main_row = False
    try:
        plugin._nowtab_control_modern_play_label = None
    except Exception:
        pass
    if int(_control_style) == 1:
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "apply_nowtab_control_modern_ui"):
                _show_search_in_main_row = bool(
                    NOWFY_CORE_API.apply_nowtab_control_modern_ui(
                        plugin, context, controls_row, control_container,
                        title_row, premium_notice_bg,
                        btn_back, btn_play_pause, btn_play_pause_icon, btn_play_pause_fallback,
                        btn_skip, btn_search, btn_search_icon, btn_search_fallback,
                        lp_back, lp_pp, lp_skip, lp_search
                    )
                )
            else:
                _show_search_in_main_row = False
        except Exception:
            _show_search_in_main_row = False
    if _fab_sheet_mode:
        try:
            play_bg = GradientDrawable()
            play_bg.setColor(Color.argb(84, 255, 255, 255))
            play_bg.setCornerRadius(AndroidUtilities.dp(40))
            play_bg.setStroke(AndroidUtilities.dp(2), Color.argb(132, 255, 255, 255))
            btn_play_pause.setBackground(play_bg)
            lp_pp.width = AndroidUtilities.dp(58 if _is_flow_compact_control else 80)
            lp_pp.height = AndroidUtilities.dp(58 if _is_flow_compact_control else 80)
            lp_pp.setMargins(AndroidUtilities.dp(4 if _is_flow_compact_control else 6), 0, AndroidUtilities.dp(4 if _is_flow_compact_control else 6), 0)
        except Exception:
            pass
        try:
            controls_row.removeAllViews()
        except Exception:
            pass
        try:
            controls_row.setGravity(Gravity.CENTER)
            controls_row.setPadding(AndroidUtilities.dp(0), AndroidUtilities.dp(2), AndroidUtilities.dp(0), AndroidUtilities.dp(2))
        except Exception:
            pass
        controls_row.addView(vol_down_btn, vol_down_lp)
        controls_row.addView(btn_back, lp_back)
        controls_row.addView(btn_play_pause, lp_pp)
        controls_row.addView(btn_skip, lp_skip)
        controls_row.addView(vol_up_btn, vol_up_lp)
    else:
        controls_row.addView(btn_back, lp_back)
        controls_row.addView(btn_play_pause, lp_pp)
        controls_row.addView(btn_skip, lp_skip)
        if _show_search_in_main_row:
            controls_row.addView(btn_search, lp_search)
    _controls_lp = LinearLayout.LayoutParams(-1, -2)
    if _fab_sheet_mode and _is_flow_compact_control:
        _controls_lp = LinearLayout.LayoutParams(-2, -2)
        _controls_lp.gravity = Gravity.CENTER_HORIZONTAL
        _controls_lp.topMargin = AndroidUtilities.dp(2)
    control_container.addView(controls_row, _controls_lp)
    return_btn = TextView(context)
    return_btn.setText(tr("nowfy_control_back_label"))
    return_btn.setGravity(Gravity.CENTER)
    if _fab_sheet_mode:
        return_btn.setTextColor(_flow_text_primary)
    else:
        return_btn.setTextColor(Color.parseColor("#D7DEFF"))
    return_btn.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
    try:
        return_btn.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
    except Exception:
        pass
    return_bg = GradientDrawable()
    if _fab_sheet_mode:
        return_bg.setColor(_flow_return_bg)
    else:
        return_bg.setColor(Color.parseColor("#263259"))
    return_bg.setCornerRadius(AndroidUtilities.dp(12))
    try:
        return_bg.setStroke(0, 0)
    except Exception:
        pass
    return_btn.setBackground(return_bg)
    return_btn.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(8 if _is_flow_compact_control else 10), AndroidUtilities.dp(14), AndroidUtilities.dp(8 if _is_flow_compact_control else 10))
    return_btn.setClickable(True)
    return_btn.setFocusable(True)
    return_btn.setOnClickListener(ControlReturnListener())
    try:
        if _is_flow_compact_control and _flow_transparent_mode:
            return_btn.setVisibility(View.GONE)
    except Exception:
        pass
    return_lp = LinearLayout.LayoutParams(-1, -2)
    return_lp.setMargins(AndroidUtilities.dp(6), AndroidUtilities.dp(8 if _is_flow_compact_control else 14), AndroidUtilities.dp(6), AndroidUtilities.dp(4))
    control_container.addView(return_btn, return_lp)

    def _bind_user():
        try:
            account = get_user_config()
            mc = get_messages_controller()
            user = None
            if mc and account:
                user = mc.getUser(account.getClientUserId())
            if hello is None or avatar is None:
                return
            name = user.first_name if user and user.first_name else "User"
            hello.setText(tr("nowfy_tab_status_hello").format(name=name))
            if user:
                drawable = AvatarDrawable(user)
                avatar.setForUserOrChat(user, drawable)
            else:
                avatar.setImageDrawable(AvatarDrawable())
        except Exception:
            try:
                if hello is not None:
                    hello.setText(tr("nowfy_tab_status_hello").format(name="User"))
            except Exception:
                pass

    def _extract_cover_from_lastfm(track):
        try:
            images = track.get("image") if isinstance(track, dict) else None
            if isinstance(images, list) and images:
                for img in reversed(images):
                    if isinstance(img, dict) and img.get("#text"):
                        return img.get("#text")
        except Exception:
            pass
        return None

    def _get_tab_track():
        try:
            sources, _labels = plugin._get_tab_source_options()
            idx = int(plugin.get_setting("nowfy_tab_source", 0))
            if idx < 0 or idx >= len(sources):
                idx = 0
            source_key = sources[idx]
            track = None
            if source_key == "spotify":
                track = plugin._get_spotify_current_track_simple()
                if track and track.get("cover_url"):
                    return track
            elif source_key == "lastfm":
                user = str(plugin.get_setting("lastfm_user", plugin.get_setting("lastfm_username", ""))).strip()
                key = str(plugin.get_setting("lastfm_api_key", "")).strip()
                if user and key:
                    track = plugin._get_lastfm_current_track(user, key)
                    if track and isinstance(track.get("artist"), dict):
                        track["artist"] = track.get("artist", {}).get("#text", "")
                    if track and not track.get("cover_url"):
                        img = track.get("image_url")
                        if img:
                            track["cover_url"] = img
                    if track and not track.get("cover_url"):
                        cover = _extract_cover_from_lastfm(track)
                        if cover:
                            track["cover_url"] = cover
                    if track and not track.get("cover_url"):
                        title = str(track.get("name") or track.get("title") or "").strip()
                        artist = str(track.get("artist") or "").strip()
                        if title:
                            try:
                                resolved = plugin._resolve_music_artwork_url(artist, title)
                            except Exception:
                                resolved = None
                            if resolved:
                                track["cover_url"] = resolved
                                try:
                                    plugin._di_last_cover_url = resolved
                                except Exception:
                                    pass
                    try:
                        if track:
                            title = str(track.get("name") or track.get("title") or "").strip()
                            artist = str(track.get("artist") or "").strip()
                            if title:
                                resolved = plugin._resolve_music_artwork_url(artist, title)
                                if resolved:
                                    track["cover_url"] = resolved
                                    try:
                                        plugin._di_last_cover_url = resolved
                                    except Exception:
                                        pass
                    except Exception:
                        pass
            elif source_key == "statsfm":
                user = str(plugin.get_setting("statsfm_username", "")).strip()
                if user:
                    track = plugin._get_statsfm_current_track(user)
                    if track and not track.get("cover_url"):
                        cover = track.get("image_url")
                        if cover:
                            track["cover_url"] = cover
            return track
        except Exception:
            return None

    def _get_track_status_info():
        try:
            track = _get_tab_track()
            if track:
                title = track.get("name") or track.get("title")
                artist = track.get("artist") or ""
                if isinstance(artist, dict):
                    artist = artist.get("#text", "")
                if title:
                    text = f"{title} - {artist}" if artist else title
                    if _is_apple_style:
                        return True, text
                    return True, tr("nowfy_tab_status_listening").format(track=text)
            return False, tr("nowfy_tab_status_empty")
        except Exception:
            return False, tr("nowfy_tab_status_empty")

    def _get_track_status_text():
        return _get_track_status_info()[1]

    def _bind_track():
        if _tab_feedback.get("busy"):
            return
        info_track = None
        try:
            info_track = _get_tab_track()
        except Exception:
            info_track = None
        try:
            _update_flow_panel_background(info_track)
        except Exception:
            pass
        status_text = _get_track_status_text()
        if _is_apple_style and status_text:
            try:
                prefix = tr("nowfy_tab_status_listening").format(track="").strip()
                if prefix and status_text.startswith(prefix):
                    status_text = status_text[len(prefix):].lstrip(": ").strip()
            except Exception:
                pass
        try:
            if status is not None:
                run_on_ui_thread(lambda: status.setText(status_text))
        except Exception:
            pass
        try:
            info = info_track if info_track is not None else _get_tab_track()
            if info and bool(plugin.get_setting("nowbox_lyrics_enabled", False)):
                _t = str(info.get("name", "") or info.get("title", "") or "").strip()
                _a = info.get("artist")
                if isinstance(_a, dict):
                    _a = str(_a.get("#text", "")).strip()
                else:
                    _a = str(_a or "").strip()
                if _t:
                    try:
                        plugin._prefetch_lyrics_for_track(_t, _a)
                    except Exception:
                        pass
        except Exception:
            pass
        try:
            _refresh_like_state_async(info_track if isinstance(info_track, dict) else None)
        except Exception:
            pass
        if _use_focus_style and focus_cover is not None:
            try:
                info = info_track if info_track is not None else _get_tab_track()
                cover_url = info.get("cover_url") if info else None
                if not cover_url or (isinstance(cover_url, str) and plugin._is_lastfm_placeholder_image(cover_url)):
                    try:
                        _t = str(info.get("name", "") or info.get("title", "") or "").strip()
                        _a = info.get("artist")
                        if isinstance(_a, dict):
                            _a = str(_a.get("#text", "")).strip()
                        else:
                            _a = str(_a or "").strip()
                        resolved_url = plugin._resolve_music_artwork_url(_a, _t) if _t else None
                        if resolved_url:
                            cover_url = resolved_url
                            try:
                                plugin._di_last_cover_url = cover_url
                            except Exception:
                                pass
                    except Exception:
                        pass
                if cover_url:
                    _load_cover(focus_cover, cover_url)
                else:
                    try:
                        if _is_apple_style:
                            fallback_cover = "https://assets.nowfy/nowfy_2.png"
                        else:
                            fallback_cover = plugin._get_header_fallback_url()
                    except Exception:
                        fallback_cover = None
                    if fallback_cover:
                        _load_cover(focus_cover, fallback_cover)
            except Exception:
                pass

    def _sync_control_play_state():
        try:
            is_playing = bool(plugin._check_music_playing())
        except Exception:
            is_playing = False
        _control_state["is_playing"] = is_playing
        def _apply():
            icon_url = pause_icon_url if is_playing else play_icon_url
            fallback = "⏸" if is_playing else "▶"
            _apply_control_icon(
                btn_play_pause_icon,
                btn_play_pause_fallback,
                icon_url,
                fallback,
                "nowfy_control_play_pause.png"
            )
            try:
                if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "update_nowtab_control_modern_state"):
                    NOWFY_CORE_API.update_nowtab_control_modern_state(plugin, is_playing)
            except Exception:
                pass
        run_on_ui_thread(_apply)
    _bind_user()
    threading.Thread(target=_bind_track, daemon=True).start()
    threading.Thread(target=_sync_control_play_state, daemon=True).start()
    _tab_live = {"run": True, "last": None}
    _status_anim = {"phase": 0.0}
    class TabAttachListener(dynamic_proxy(View.OnAttachStateChangeListener)):
        def onViewAttachedToWindow(self, v):
            _tab_live["run"] = True
        def onViewDetachedFromWindow(self, v):
            _tab_live["run"] = False
    try:
        root_container.addOnAttachStateChangeListener(TabAttachListener())
    except Exception:
        pass
    try:
        from ui.bulletin import BulletinHelper
        if not bool(getattr(plugin, "_fab_force_apple_tab", False)):
            if bool(plugin.get_setting("nowfy_tab_available_notify", False)):
                BulletinHelper.show_success(tr("nowfy_tab_available_notice"))
    except Exception:
        pass

    def _apply_status_idle():
        try:
            status_bg.setStroke(0, Color.TRANSPARENT)
            trail_line.setVisibility(View.GONE)
        except Exception:
            pass

    def _apply_trail(progress):
        try:
            row_w = status_row.getWidth()
            row_h = status_row.getHeight()
            if row_w <= 0 or row_h <= 0:
                return
            seg_w = AndroidUtilities.dp(46)
            seg_h = AndroidUtilities.dp(4)
            inset = AndroidUtilities.dp(2)
            corner = float(AndroidUtilities.dp(16))
            left = float(inset)
            top = float(inset)
            right = float(max(inset + 1, row_w - inset))
            bottom = float(max(inset + 1, row_h - inset))
            w = max(1.0, right - left)
            h = max(1.0, bottom - top)
            r = max(1.0, min(corner, w / 2.0, h / 2.0))
            import math as _math
            top_line = max(1.0, w - 2.0 * r)
            side_line = max(1.0, h - 2.0 * r)
            arc = (_math.pi * r) / 2.0
            perimeter = (top_line * 2.0) + (side_line * 2.0) + (arc * 4.0)
            d = float(progress % perimeter)
            x = left + r
            y = top
            angle = 0.0
            if d < top_line:
                x = left + r + d
                y = top
                angle = 0.0
            else:
                d -= top_line
                if d < arc:
                    t = d / arc
                    th = (-_math.pi / 2.0) + ((_math.pi / 2.0) * t)
                    cx = right - r
                    cy = top + r
                    x = cx + r * _math.cos(th)
                    y = cy + r * _math.sin(th)
                    angle = (th * 180.0 / _math.pi) + 90.0
                else:
                    d -= arc
                    if d < side_line:
                        x = right
                        y = top + r + d
                        angle = 90.0
                    else:
                        d -= side_line
                        if d < arc:
                            t = d / arc
                            th = 0.0 + ((_math.pi / 2.0) * t)
                            cx = right - r
                            cy = bottom - r
                            x = cx + r * _math.cos(th)
                            y = cy + r * _math.sin(th)
                            angle = (th * 180.0 / _math.pi) + 90.0
                        else:
                            d -= arc
                            if d < top_line:
                                x = right - r - d
                                y = bottom
                                angle = 180.0
                            else:
                                d -= top_line
                                if d < arc:
                                    t = d / arc
                                    th = (_math.pi / 2.0) + ((_math.pi / 2.0) * t)
                                    cx = left + r
                                    cy = bottom - r
                                    x = cx + r * _math.cos(th)
                                    y = cy + r * _math.sin(th)
                                    angle = (th * 180.0 / _math.pi) + 90.0
                                else:
                                    d -= arc
                                    if d < side_line:
                                        x = left
                                        y = bottom - r - d
                                        angle = -90.0
                                    else:
                                        d -= side_line
                                        t = min(1.0, d / arc)
                                        th = _math.pi + ((_math.pi / 2.0) * t)
                                        cx = left + r
                                        cy = top + r
                                        x = cx + r * _math.cos(th)
                                        y = cy + r * _math.sin(th)
                                        angle = (th * 180.0 / _math.pi) + 90.0
            lp = trail_line.getLayoutParams()
            if lp is None:
                lp = FrameLayout.LayoutParams(seg_w, seg_h, Gravity.TOP | Gravity.LEFT)
            lp.width = seg_w
            lp.height = seg_h
            lp.leftMargin = int(x - (seg_w / 2.0))
            lp.topMargin = int(y - (seg_h / 2.0))
            tcol = (progress % 220.0) / 220.0
            ca = (122, 92, 255)
            cb = (84, 176, 255)
            rr = int(ca[0] * (1.0 - tcol) + cb[0] * tcol)
            gg = int(ca[1] * (1.0 - tcol) + cb[1] * tcol)
            bb = int(ca[2] * (1.0 - tcol) + cb[2] * tcol)
            trail_bg.setColor(Color.rgb(rr, gg, bb))
            trail_line.setLayoutParams(lp)
            trail_line.setRotation(float(angle))
            trail_line.setVisibility(View.VISIBLE)
        except Exception:
            pass

    def _status_border_loop():
        color_a = (122, 92, 255)
        color_b = (84, 176, 255)
        while True:
            try:
                if not _tab_live.get("run", True):
                    time.sleep(0.25)
                    continue
                if _tab_feedback.get("no_track"):
                    try:
                        if time.time() > float(_tab_feedback.get("no_track_until", 0.0)):
                            _tab_feedback["no_track"] = False
                        else:
                            c = Color.parseColor("#FF5A5A")
                            if _is_apple_style and status_glow_bg is not None:
                                run_on_ui_thread(lambda c=c: status_glow_bg.setStroke(AndroidUtilities.dp(1), c))
                            else:
                                run_on_ui_thread(lambda c=c: status_bg.setStroke(AndroidUtilities.dp(2), c))
                            time.sleep(0.08)
                            continue
                    except Exception:
                        pass
                if _tab_feedback.get("busy"):
                    _status_anim["phase"] += 0.20
                    import math as _math
                    t = (_math.sin(_status_anim["phase"]) + 1.0) / 2.0
                    if _is_apple_style and status_glow_bg is not None:
                        a = int(40 + (160 * t))
                        c = Color.argb(a, 255, 255, 255)
                        run_on_ui_thread(lambda c=c: status_glow_bg.setStroke(AndroidUtilities.dp(1), c))
                    else:
                        r = int(color_a[0] * (1.0 - t) + color_b[0] * t)
                        g = int(color_a[1] * (1.0 - t) + color_b[1] * t)
                        b = int(color_a[2] * (1.0 - t) + color_b[2] * t)
                        c = Color.rgb(r, g, b)
                        run_on_ui_thread(lambda c=c: status_bg.setStroke(AndroidUtilities.dp(2), c))
                    time.sleep(0.08)
                else:
                    if _is_apple_style and status_glow_bg is not None:
                        run_on_ui_thread(lambda: status_glow_bg.setStroke(AndroidUtilities.dp(1), Color.argb(0, 255, 255, 255)))
                    run_on_ui_thread(_apply_status_idle)
                    time.sleep(0.22)
            except Exception:
                time.sleep(0.30)

    def _track_loop():
        while True:
            try:
                if not _tab_live.get("run", True):
                    time.sleep(0.5)
                    continue
                if _tab_feedback.get("busy"):
                    time.sleep(1)
                    continue
                info = _get_tab_track()
                if info:
                    title = info.get("name") or info.get("title")
                    artist = info.get("artist") or ""
                    if isinstance(artist, dict):
                        artist = artist.get("#text", "")
                    if title:
                        new_text = tr("nowfy_tab_status_listening").format(track=(f"{title} - {artist}" if artist else title))
                    else:
                        new_text = tr("nowfy_tab_status_empty")
                else:
                    new_text = tr("nowfy_tab_status_empty")
                if new_text != _tab_live["last"]:
                    _tab_live["last"] = new_text
                    if status is not None:
                        run_on_ui_thread(lambda: status.setText(new_text))
                if _use_focus_style and focus_cover is not None:
                    try:
                        cover_url = info.get("cover_url") if info else None
                        last_cover = _tab_live.get("last_cover")
                        if cover_url and cover_url != last_cover:
                            _tab_live["last_cover"] = cover_url
                            _load_cover(focus_cover, cover_url)
                    except Exception:
                        pass
                _sync_control_play_state()
            except Exception:
                pass
            time.sleep(1.2)
    threading.Thread(target=_track_loop, daemon=True).start()
    threading.Thread(target=_status_border_loop, daemon=True).start()
    is_fab_embed = bool(getattr(plugin, "_fab_force_apple_tab", False))
    if is_fab_embed:
        lp_main = LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT)
    else:
        lp_main = LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, AndroidUtilities.dp(300))
    root_container.addView(scroll_view, FrameLayout.LayoutParams(-1, -1))
    root_container.addView(control_scroll, FrameLayout.LayoutParams(-1, -1))
    _initial_control_page = False
    try:
        _initial_control_page = bool(getattr(plugin, "_fab_open_control_page", False))
    except Exception:
        _initial_control_page = False
    _show_tab_page(1 if _initial_control_page else 0)
    try:
        if _initial_control_page:
            plugin._fab_open_control_page = False
    except Exception:
        pass
    root_container.setTag(NOWFY_TAB_VIEW_TAG)
    root_container.setVisibility(View.VISIBLE if is_fab_embed else View.INVISIBLE)
    root_container.setLayoutParams(lp_main)
    root_container.setClickable(True)
    root_container.setFocusable(True)
    return root_container

def force_update_ui(emoji_view):
    try:
        type_tabs = get_private_field(emoji_view, "typeTabs")
        pager = get_private_field(emoji_view, "pager")
        if pager and pager.getAdapter():
            pager.getAdapter().notifyDataSetChanged()
        if type_tabs and pager:
            methods = type_tabs.getClass().getMethods()
            for m in methods:
                if m.getName() == "setViewPager" and len(m.getParameterTypes()) == 1:
                    m.invoke(type_tabs, pager)
                    break
    except Exception:
        pass

class NowfyTrackHubRowsHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin
    @hook_filters(HookFilter.Condition("param.thisObject != null"))
    def before_hooked_method(self, param):
        activity = param.thisObject
        state = self.plugin._track_hub_profile_states.setdefault(activity, {"row": -1, "profile_id": 0, "enabled": False})
        state["row"] = -1
        state["profile_id"] = 0
        state["enabled"] = False
        try:
            if not bool(self.plugin.get_setting("track_hub_enabled", False)):
                try:
                    log("[Nowfy][TrackHub] rows.before: disabled")
                except Exception:
                    pass
                return
            if not bool(self.plugin._is_track_hub_target_user_profile(activity)):
                try:
                    log("[Nowfy][TrackHub] rows.before: skip non-user profile")
                except Exception:
                    pass
                return
            pid = int(self.plugin._extract_profile_id_for_track_hub(activity) or 0)
            if pid == 0:
                try:
                    log("[Nowfy][TrackHub] rows.before: user profile id not found")
                except Exception:
                    pass
                return
            me = 0
            try:
                me = int(self.plugin._track_hub_get_current_uid() or 0)
            except Exception:
                me = 0
            if me > 0 and pid != me:
                if not bool(self.plugin._track_hub_remote_payload_exists(pid)):
                    try:
                        log(f"[Nowfy][TrackHub] rows.before: skip pid={pid} (no remote payload)")
                    except Exception:
                        pass
                    return
            state["profile_id"] = pid
            state["enabled"] = True
            try:
                log(f"[Nowfy][TrackHub] rows.before: enabled pid={pid}")
            except Exception:
                pass
        except Exception:
            pass
    @hook_filters(HookFilter.Condition("param.thisObject != null"))
    def after_hooked_method(self, param):
        activity = param.thisObject
        state = self.plugin._track_hub_profile_states.get(activity)
        if not state or not state.get("enabled"):
            return
        pos = self._calc_insert_pos(activity)
        if pos == -1:
            state["row"] = -1
            try:
                log("[Nowfy][TrackHub] rows.after: insert pos not found")
            except Exception:
                pass
            return
        state["row"] = pos
        try:
            rc = self._get_int(activity, "rowCount")
            if rc != -1:
                self._set_int(activity, "rowCount", rc + 1)
            self._shift_rows(activity, pos)
            try:
                log(f"[Nowfy][TrackHub] rows.after: inserted row={pos} oldRowCount={rc}")
            except Exception:
                pass
        except Exception:
            pass

    def _calc_insert_pos(self, activity):
        for name in ("phoneRow", "usernameRow", "bioRow", "channelInfoRow", "userInfoRow"):
            v = self._get_int(activity, name)
            if v != -1:
                return v + 1
        try:
            rc = self._get_int(activity, "rowCount")
            if rc >= 0:
                return rc
        except Exception:
            pass
        return -1

    def _shift_rows(self, activity, threshold):
        try:
            IntCls = jclass("java.lang.Integer")
            fields = activity.getClass().getDeclaredFields()
            for f in fields:
                n = f.getName()
                if "Row" not in n and "row" not in n:
                    continue
                if n in ("rowCount", "phoneRow", "linkRow"):
                    continue
                ft = f.getType()
                if ft != IntCls.TYPE and ft != IntCls:
                    continue
                f.setAccessible(True)
                val = f.get(activity)
                if val is not None and int(val) >= int(threshold) and int(val) != -1:
                    f.setInt(activity, int(val) + 1)
        except Exception:
            pass

    def _get_int(self, obj, field_name):
        try:
            f = obj.getClass().getDeclaredField(field_name)
            f.setAccessible(True)
            return f.getInt(obj)
        except Exception:
            return -1

    def _set_int(self, obj, field_name, value):
        try:
            f = obj.getClass().getDeclaredField(field_name)
            f.setAccessible(True)
            f.setInt(obj, int(value))
        except Exception:
            pass

class NowfyTrackHubTypeHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin
    @hook_filters(HookFilter.Condition("param.thisObject != null"), HookFilter.ArgumentNotNull(0))
    def before_hooked_method(self, param):
        adapter = param.thisObject
        activity = self._get_activity(adapter)
        if not activity:
            return
        state = self.plugin._track_hub_profile_states.get(activity)
        if not state:
            return
        position = int(param.args[0])
        if position == int(state.get("row", -1)):
            try:
                param.setResult(jclass("java.lang.Integer")(2))
                try:
                    log(f"[Nowfy][TrackHub] type.before: forcing type=2 at pos={position}")
                except Exception:
                    pass
            except Exception:
                pass

    def _get_activity(self, adapter):
        try:
            f = adapter.getClass().getDeclaredField("this$0")
            f.setAccessible(True)
            return f.get(adapter)
        except Exception:
            pass
        try:
            fields = adapter.getClass().getDeclaredFields()
            for f in fields:
                try:
                    if "this$0" in str(f.getName()):
                        f.setAccessible(True)
                        return f.get(adapter)
                except Exception:
                    pass
        except Exception:
            pass
        return None

class NowfyTrackHubBindHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin
    @hook_filters(HookFilter.ArgumentNotNull(0), HookFilter.ArgumentNotNull(1))
    def after_hooked_method(self, param):
        try:
            position = int(param.args[1])
            adapter = param.thisObject
            activity = self._get_activity(adapter)
            if not activity:
                return
            holder = param.args[0]
            cell = holder.itemView if holder else None
            if cell:
                try:
                    self.plugin._track_hub_clear_cell_extras(cell)
                except Exception:
                    pass
            state = self.plugin._track_hub_profile_states.get(activity)
            if not state:
                return
            if position != int(state.get("row", -1)):
                return
            if not cell:
                return
            try:
                log(f"[Nowfy][TrackHub] bind.after: rendering row={position} pid={int(state.get('profile_id', 0))}")
            except Exception:
                pass
            self.plugin._render_track_hub_profile_cell(cell, int(state.get("profile_id", 0)))
        except Exception:
            pass

    def _get_activity(self, adapter):
        try:
            f = adapter.getClass().getDeclaredField("this$0")
            f.setAccessible(True)
            return f.get(adapter)
        except Exception:
            pass
        try:
            fields = adapter.getClass().getDeclaredFields()
            for f in fields:
                try:
                    if "this$0" in str(f.getName()):
                        f.setAccessible(True)
                        return f.get(adapter)
                except Exception:
                    pass
        except Exception:
            pass
        return None

class NowfyEmojiViewConstructorHook(MethodHook):

    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin

    def after_hooked_method(self, param):
        if not bool(self.plugin.get_setting("nowfy_tab_enabled", True)):
            return
        emoji_view = param.thisObject
        context = param.args[4]
        all_tabs = get_private_field(emoji_view, "allTabs")
        py_all_tabs = list(ArrayList(all_tabs).toArray()) if all_tabs else []
        if len(py_all_tabs) <= 1:
            return
        try:
            my_view = create_nowfy_tab_view(context, self.plugin)
            tab_class = get_java_class("org.telegram.ui.Components.EmojiView$Tab")
            if not tab_class or not my_view:
                return
            tab_ctor = tab_class.getDeclaredConstructors()[0]
            tab_ctor.setAccessible(True)
            new_tab = tab_ctor.newInstance(emoji_view)
            set_private_field(new_tab, "type", Integer.valueOf(int(NOWFY_TAB_INDEX)))
            set_private_field(new_tab, "view", my_view)
            current_tabs = get_private_field(emoji_view, "currentTabs")
            if all_tabs is not None:
                all_tabs.add(new_tab)
            if current_tabs is not None:
                current_tabs.add(new_tab)
            try:
                self.plugin._attach_emoji_pager_listener(emoji_view, my_view)
            except Exception:
                pass
            try:
                self.plugin._attach_nowfy_tab_open_listener(emoji_view)
            except Exception:
                pass
            run_on_ui_thread(lambda: force_update_ui(emoji_view))
            try:
                self.plugin._apply_nowfy_tab_priority_on_open(emoji_view)
            except Exception:
                pass
        except Exception:
            pass

class NowfySetAllowHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin

    def after_hooked_method(self, param):
        emoji_view = param.thisObject
        all_tabs = get_private_field(emoji_view, "allTabs")
        current_tabs = get_private_field(emoji_view, "currentTabs")
        if not all_tabs or not current_tabs:
            return
        my_tab = None
        for i in range(all_tabs.size()):
            t = all_tabs.get(i)
            if get_private_field(t, "type") == NOWFY_TAB_INDEX:
                my_tab = t
                break
        if not bool(self.plugin.get_setting("nowfy_tab_enabled", True)):
            if my_tab and current_tabs.contains(my_tab):
                current_tabs.remove(my_tab)
                run_on_ui_thread(lambda: force_update_ui(emoji_view))
            return
        if not my_tab:
            return
        if not current_tabs.contains(my_tab):
            current_tabs.add(my_tab)
            run_on_ui_thread(lambda: force_update_ui(emoji_view))
        try:
            self.plugin._apply_nowfy_tab_priority_on_open(emoji_view)
        except Exception:
            pass

class NowfyAdapterGetIconHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin

    def after_hooked_method(self, param):
        if not bool(self.plugin.get_setting("nowfy_tab_enabled", True)):
            return
        position = param.args[0]
        if position == NOWFY_TAB_INDEX:
            param.setResult(None)

class NowfyAdapterGetTitleHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin

    def after_hooked_method(self, param):
        if not bool(self.plugin.get_setting("nowfy_tab_enabled", True)):
            return
        position = param.args[0]
        if position == NOWFY_TAB_INDEX:
            param.setResult("Nowfy")

class NowfySettingsInlineHook(MethodHook):

    def __init__(self, plugin, is_long=False):
        super().__init__()
        self.plugin = plugin
        self._is_long = bool(is_long)

    def before_hooked_method(self, param):
        try:
            cell = param.args[0] if param.args and len(param.args) > 0 else None
            btn = param.args[1] if param.args and len(param.args) > 1 else None
            self.plugin._handle_nowfysettings_inline_press(cell, btn, param, is_long=self._is_long)
        except Exception:
            pass

class NowfyCheckGridVisibilityHook(MethodHook):

    def __init__(self, plugin):
        self.plugin = plugin

    def after_hooked_method(self, param):
        emoji_view = param.thisObject
        position = param.args[0]
        pager = get_private_field(emoji_view, "pager")
        my_view = emoji_view.findViewWithTag(NOWFY_TAB_VIEW_TAG)
        stickers = get_private_field(emoji_view, "stickersTabContainer")
        search = get_private_field(emoji_view, "emojiSearchField")
        enabled = bool(self.plugin.get_setting("nowfy_tab_enabled", True))
        if position == NOWFY_TAB_INDEX and enabled:
            if my_view:
                try:
                    current_vis = int(my_view.getVisibility())
                except Exception:
                    current_vis = -1
                if current_vis != int(View.VISIBLE):
                    my_view.setVisibility(View.VISIBLE)
            if stickers:
                stickers.setVisibility(View.GONE)
            if search:
                search.setVisibility(View.GONE)
        else:
            if my_view:
                try:
                    current_item = int(pager.getCurrentItem()) if pager else -1
                except Exception:
                    current_item = -1
                target_vis = View.VISIBLE if current_item == NOWFY_TAB_INDEX else View.INVISIBLE
                try:
                    current_vis = int(my_view.getVisibility())
                except Exception:
                    current_vis = -1
                if current_vis != int(target_vis):
                    my_view.setVisibility(target_vis)
try:
    _ORIGINAL_LOG = log
    try:
        _ORIGINAL_PRINT = print
    except Exception:
        _ORIGINAL_PRINT = None
except Exception:
    _ORIGINAL_LOG = None
_NOWFY_LOGS_MUTED = True
_NOWFY_PRINT_MUTED = True
_NOWFY_ERROR_LOGS = []

def _capture_error_log(msg):
    try:
        text = str(msg)
        low = text.lower()
        if "nowfy" not in low:
            return
        keywords = ["error", "erro", "exception", "traceback", "failed", "falha", "timeout", "401", "403", "429", "500", "forbidden", "unauthorized"]
        if any(k in low for k in keywords):
            _NOWFY_ERROR_LOGS.append(text.strip())
            if len(_NOWFY_ERROR_LOGS) > 80:
                _NOWFY_ERROR_LOGS[:] = _NOWFY_ERROR_LOGS[-80:]
    except Exception:
        pass

def _set_log_muted(muted: bool):
    global _NOWFY_LOGS_MUTED
    _NOWFY_LOGS_MUTED = bool(muted)

def _set_print_muted(muted: bool):
    global _NOWFY_PRINT_MUTED
    _NOWFY_PRINT_MUTED = bool(muted)

def _log_wrapper(*args, **kwargs):
    try:
        if _NOWFY_LOGS_MUTED:
            return
        try:
            if args:
                _capture_error_log(" ".join([str(a) for a in args]))
        except Exception:
            pass
        if _ORIGINAL_LOG:
            _ORIGINAL_LOG(*args, **kwargs)
    except Exception:
        pass

def _apply_log_wrapper(enabled: bool):
    global log
    if _ORIGINAL_LOG:
        log = _log_wrapper
        try:
            import android_utils as _au
            _au.log = _log_wrapper
        except Exception:
            pass
    else:
        log = _ORIGINAL_LOG

def _print_wrapper(*args, **kwargs):
    try:
        if _NOWFY_PRINT_MUTED:
            return
        try:
            if args:
                _capture_error_log(" ".join([str(a) for a in args]))
        except Exception:
            pass
        if _ORIGINAL_PRINT:
            _ORIGINAL_PRINT(*args, **kwargs)
    except Exception:
        pass

def _apply_print_wrapper(enabled: bool):
    global print
    if _ORIGINAL_PRINT:
        print = _print_wrapper
        try:
            _py_builtins.print = _print_wrapper
        except Exception:
            pass
    else:
        print = _ORIGINAL_PRINT
        try:
            _py_builtins.print = _ORIGINAL_PRINT
        except Exception:
            pass
_apply_log_wrapper(True)
_apply_print_wrapper(True)
APPLE_BACKGROUNDS = {
    "Spotify": {
        "Light": "https://assets.nowfy/applelight.png",
        "Dark":  "https://assets.nowfy/appledark.png",
        "Red":   "https://assets.nowfy/applered.png",
    },
    "YouTube": {
        "Light": "https://assets.nowfy/appleredyoutubelight.png",
        "Dark":  "https://assets.nowfy/appleredyoutubedark.png",
        "Red":   "https://assets.nowfy/appleredyoutubered.png",
    },
    "YouTube Music": {
        "Light": "https://assets.nowfy/applelightytmusic.png",
        "Dark":  "https://assets.nowfy/appledarkytmusic.png",
        "Red":   "https://assets.nowfy/appleredytmusic.png",
    },
    "exteraGram": {
        "Light": "https://assets.nowfy/etglight.png",
        "Dark":  "https://assets.nowfy/etgdark.png",
        "Red":   "https://assets.nowfy/etgred.png",
    },
    "AyuGram": {
        "Light": "https://assets.nowfy/ayulight.png",
        "Dark":  "https://assets.nowfy/ayudark.png",
        "Red":   "https://assets.nowfy/ayured.png",
    },
    "SoundCloud": {
        "Light": "https://assets.nowfy/applelightsoundcloud.png",
        "Dark":  "https://assets.nowfy/appledarksoundcloud.png",
        "Red":   "https://assets.nowfy/appleredsoundcloud.png",
    },
    "Apple Music": {
        "Light": "https://assets.nowfy/applelightapplelight.png",
        "Dark":  "https://assets.nowfy/appledarkapple.png",
        "Red":   "https://assets.nowfy/appledarkapple.png",
    },
    "Yandex Music": {
        "Light": "https://assets.nowfy/yandexlight.png",
        "Dark":  "https://assets.nowfy/yandexdark.png",
        "Red":   "https://assets.nowfy/yandexred.png",
    },
}

def _prefetch_current_player_backgrounds(self):
    try:
        from org.telegram.messenger import ApplicationLoader
        from java.io import File
        import os
        current_player = self._detect_current_player()
        apple_players = list(APPLE_BACKGROUNDS.keys())
        if current_player not in apple_players:
            current_player = "Spotify"
        temp_dir = File(ApplicationLoader.getFilesDirFixed(), "exteraFy/cards")
        if not temp_dir.exists():
            temp_dir.mkdirs()
        def _suffix_for_player(p):
            if p == "SoundCloud":
                return "_soundcloud"
            if p == "YouTube":
                return "_youtube"
            if p == "YouTube Music":
                return "_ytmusic"
            if p == "exteraGram":
                return "_exteragram"
            if p == "AyuGram":
                return "_ayugram"
            if p == "Apple Music":
                return "_applemusic"
            if p == "Yandex Music":
                return "_yandex"
            return ""
        suffix = _suffix_for_player(current_player)
        for skin in ["Light", "Dark"]:
            try:
                url = APPLE_BACKGROUNDS.get(current_player, {}).get(skin) or APPLE_BACKGROUNDS["Spotify"][skin]
                filename = f"apple{skin.lower()}{suffix}.png"
                versionfile = f"apple{skin.lower()}{suffix}_version.txt"
                base_path = File(temp_dir, filename).getAbsolutePath()
                version_path = File(temp_dir, versionfile).getAbsolutePath()
                needs = False
                if not os.path.exists(base_path) or not os.path.exists(version_path):
                    needs = True
                else:
                    try:
                        with open(version_path, "r") as vf:
                            saved = vf.read().strip()
                        needs = saved != url
                    except Exception:
                        needs = True
                if needs and url:
                    data = self._get_cached_image_original(url)
                    if data:
                        with open(base_path, "wb") as f:
                            f.write(data)
                        with open(version_path, "w") as vf:
                            vf.write(url)
                        try:
                            log(f"[Nowfy] Prefetched Apple background {skin} for {current_player}")
                        except Exception:
                            pass
            except Exception:
                pass
    except Exception:
        pass
NOWCAST_MESSAGES = {}
APPLE_SKIN_STYLE = {
    0: {
        "playing_color": "#888888",
        "title_color": "#000000",
        "artist_color": "#888888",
        "exteraBar_fn": "exteraBarSeek_light_opposite",
    },
    1: {
        "playing_color": "#DDDDDD",
        "title_color": "#FFFFFF",
        "artist_color": "#CCCCCC",
        "exteraBar_fn": "exteraBarSeek_dark_opposite",
    },
    2: {
        "playing_color": "#DDDDDD",
        "title_color": "#FFFFFF",
        "artist_color": "#CCCCCC",
        "exteraBar_fn": "exteraBarSeek_red_opposite",
    },
}
SPOTLIGHT_SKIN_STYLE = {
    0: {
        "time_color": (0, 0, 0, 255),
        "bar_bg_color": (200, 200, 200, 255),
        "bar_fill_color": (0, 0, 0, 255),
        "bg_color": (255, 255, 255),
        "use_blur_bg": False,
    },
    1: {
        "time_color": (255, 255, 255, 255),
        "bar_bg_color": (60, 60, 60, 255),
        "bar_fill_color": (255, 255, 255, 255),
        "bg_color": (0, 0, 0),
        "use_blur_bg": False,
    },
    2: {
        "time_color": (255, 255, 255, 255),
        "bar_bg_color": (60, 60, 60, 255),
        "bar_fill_color": (255, 255, 255, 255),
        "bg_color": (255, 255, 255),
        "use_blur_bg": True,
    },
}
try:
    TRANSLATIONS = nowfycore.get_nowfy_translations() if (nowfycore is not None and hasattr(nowfycore, "get_nowfy_translations")) else {}
except Exception:
    TRANSLATIONS = {}
try:
    if "nowfy_font_upload_label" not in TRANSLATIONS:
        TRANSLATIONS["nowfy_font_upload_label"] = {
            "pt": "Enviar arquivo de fonte",
            "en": "Upload font file",
            "ru": "Загрузить файл шрифта"
        }
    if "nowfy_font_manage_label" not in TRANSLATIONS:
        TRANSLATIONS["nowfy_font_manage_label"] = {
            "pt": "Gerenciar fontes",
            "en": "Manage fonts",
            "ru": "Управление шрифтами"
        }
except Exception:
    pass
_NOWFY_LANG_OVERRIDE = None

def tr(key):
    lang = None
    try:
        if _NOWFY_LANG_OVERRIDE:
            lang = _NOWFY_LANG_OVERRIDE
    except Exception:
        lang = None
    if not lang:
        try:
            controller = PluginsController.getInstance()
            plugin = controller.plugins.get("nowfy") if controller else None
            if plugin and hasattr(plugin, "get_setting"):
                idx = int(plugin.get_setting("plugin_lang", 0))
                codes = ["en", "pt", "ru"]
                if 0 <= idx < len(codes):
                    lang = codes[idx]
        except Exception:
            lang = None
    if not lang:
        lang = Locale.getDefault().getLanguage()
    if lang not in ["pt", "en", "ru"]:
        lang = "en"
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang) or entry.get("en") or key

class _MessageMenuRegistry:

    def __init__(self):
        self.items = []
        self._unhook_fill = None
        self._unhook_process = None

    def ensure_hooks(self, plugin):
        try:
            if not self._unhook_fill:
                ChatActivity = find_class("org.telegram.ui.ChatActivity")
                MessageObject = find_class("org.telegram.messenger.MessageObject")
                fill_method = ChatActivity.getClass().getDeclaredMethod(
                    "fillMessageMenu",
                    MessageObject,
                    ArrayList,
                    ArrayList,
                    ArrayList
                )
                self._unhook_fill = plugin.hook_method(fill_method, _FillMenuHook(self))
        except Exception as e:
            log(f"[Nowfy] fillMessageMenu hook error: {str(e)}")
        try:
            if not self._unhook_process:
                ChatActivity = find_class("org.telegram.ui.ChatActivity")
                process_method = ChatActivity.getClass().getDeclaredMethod(
                    "processSelectedOption",
                    Integer.TYPE
                )
                self._unhook_process = plugin.hook_method(process_method, _ProcessOptionHook(self))
        except Exception as e:
            log(f"[Nowfy] processSelectedOption hook error: {str(e)}")

    def register_item(self, *, text: str, option_id: int, icon_res: int, condition_predicate, on_click, insert_at_top: bool):
        handle = {
            'text': text,
            'option_id': int(option_id),
            'icon_res': int(icon_res),
            'condition': condition_predicate,
            'on_click': on_click,
            'insert_top': bool(insert_at_top),
        }
        self.items.append(handle)
        return handle

    def unregister_item(self, handle):
        if handle in self.items:
            self.items.remove(handle)

    def cleanup_hooks(self, plugin):
        try:
            if self._unhook_fill:
                plugin.unhook_method(self._unhook_fill)
                self._unhook_fill = None
            if self._unhook_process:
                plugin.unhook_method(self._unhook_process)
                self._unhook_process = None
        except Exception:
            pass

class _FillMenuHook:

    def __init__(self, registry: _MessageMenuRegistry):
        self.registry = registry

    def before_hooked_method(self, param):
        pass

    def after_hooked_method(self, param):
        try:
            primary = param.args[0]
            if primary is None:
                return
            try:
                self.registry.last_message = primary
            except Exception:
                pass
            icons = param.args[1]
            items = param.args[2]
            options = param.args[3]
            for entry in list(self.registry.items):
                try:
                    if entry.get('condition') and callable(entry['condition']):
                        if not entry['condition'](primary):
                            continue
                    if entry.get('insert_top'):
                        icons.add(0, Integer(entry['icon_res']))
                        options.add(0, Integer(entry['option_id']))
                        items.add(0, entry['text'])
                    else:
                        icons.add(Integer(entry['icon_res']))
                        options.add(Integer(entry['option_id']))
                        items.add(entry['text'])
                except Exception:
                    continue
        except Exception:
            pass

class _ProcessOptionHook:

    def __init__(self, registry: _MessageMenuRegistry):
        self.registry = registry

    def before_hooked_method(self, param):
        try:
            option = param.args[0]
            try:
                opt_val = int(option)
            except Exception:
                try:
                    opt_val = option.intValue()
                except Exception:
                    return
            for entry in list(self.registry.items):
                if opt_val == entry.get('option_id'):
                    try:
                        chat_activity = param.thisObject
                        message = getattr(chat_activity, 'selectedObject', None)
                        if message is None:
                            message = getattr(self.registry, 'last_message', None)
                        try:
                            chat_activity.closeMenu()
                        except Exception:
                            pass
                        if callable(entry.get('on_click')):
                            entry['on_click'](chat_activity, message)
                        param.setResult(None)
                    except Exception:
                        pass
                    finally:
                        return
        except Exception:
            pass

    def after_hooked_method(self, param):
        pass
_message_menu_registry = _MessageMenuRegistry()

def _ensure_message_menu_hooks(plugin):
    _message_menu_registry.ensure_hooks(plugin)

def cleanup_message_menu_hooks(plugin):
    _message_menu_registry.cleanup_hooks(plugin)

class MessageMenuUtilities:

    def register_message_menu_item(self, *, text: str, option_id: int, icon_res: int = R.drawable.files_music, condition_predicate=None, on_click=None, insert_at_top: bool = False):
        try:
            return _message_menu_registry.register_item(
                text=text,
                option_id=option_id,
                icon_res=icon_res,
                condition_predicate=condition_predicate,
                on_click=on_click,
                insert_at_top=insert_at_top,
            )
        except Exception as e:
            log(f"[Nowfy] register_message_menu_item error: {str(e)}")
            return None

    def unregister_message_menu_item(self, handle):
        try:
            if handle:
                _message_menu_registry.unregister_item(handle)
        except Exception as e:
            log(f"[Nowfy] unregister_message_menu_item error: {str(e)}")
message_menu_utilities = MessageMenuUtilities()

class exteraFyPlugin(NOWFY_CORE_BACKEND_MIXIN, BasePlugin):

    def __init__(self):
        super().__init__()
        try:
            self.core = NowfyCore(self)
        except Exception:
            self.core = None
        self._message_lock = threading.Lock()
        self._cache_lock = threading.Lock()
        self._image_cache = {}
        self._cache_timestamps = {}
        self._cache_enabled = False
        self._cache_thread = None
        self._cache_running = False
        self._cache_ttl = 300
        self._cache_max_size = 10
        self._disk_cache_dir = File(ApplicationLoader.getFilesDirFixed(), "exteraFyCache")
        if not self._disk_cache_dir.exists():
            self._disk_cache_dir.mkdirs()
        self._enhanced_image_cache = {}
        self._base_theme_cache = {}
        self._performance_mode = "balanced"
        self._preload_enabled = False
        self._compression_enabled = True
        self._standard_cover_size = (298, 298)
        self._last_track_id = None
        self._nowplaying_cache = {}
        self._nowplaying_cache_ttl = 8.0
        self._precard_cache = {}
        self._precard_cache_ttl = 45.0
        self._precard_lock = threading.Lock()
        self._settings_version = 0
        self._precard_enabled = True
        self._bio_update_thread = None
        self._stop_bio_update = False
        self._nowcast_worker_running = False
        self._nowcast_last_track_hash = None
        self._nowcast_post_history = []
        self._nowcast_cooldown_time = 0
        self._track_hub_profile_states = {}
        self._track_hub_rows_hook_ref = None
        self._track_hub_type_hook_ref = None
        self._track_hub_bind_hook_ref = None
        self._track_hub_thread = None
        self._track_hub_stop = threading.Event()
        self._nowcast_min_interval = 30
        self._nowfy_chat_menu_item = None
        self._nowfy_pocket_chat_menu_item = None
        self._nowfy_pocket_install_in_progress = False
        self._nowfy_pocket_install_lock = threading.Lock()
        try:
            val = bool(self.get_setting("disable_logs", False))
            _set_log_muted(val)
            _apply_log_wrapper(True)
        except Exception:
            pass
        try:
            self._sync_nowfy_pocket_setting_from_file()
        except Exception:
            pass
        try:
            self._original_set_setting = self.set_setting
            def _wrapped_set_setting(key, value):
                try:
                    self._settings_version += 1
                except Exception:
                    pass
                return self._original_set_setting(key, value)
            self.set_setting = _wrapped_set_setting
        except Exception:
            pass
        self._di_is_active = False
        self._di_window_manager = None
        self._di_layout = None
        self._di_layout_params = None
        self._di_text_view = None
        self._di_dragging = False
        self._di_drag_start_raw_x = 0
        self._di_drag_start_raw_y = 0
        self._di_drag_start_x = 0
        self._di_drag_start_y = 0
        self._di_refresh_stop_event = None
        self._di_refresh_thread = None
        bio_addon_enabled = True
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "is_addon_enabled"):
                bio_addon_enabled = bool(NOWFY_CORE_API.is_addon_enabled(self, "addon_bio_features_enabled", False))
        except Exception:
            bio_addon_enabled = True
        try:
            if bio_addon_enabled and not bool(self.get_setting("disable_logs", False)):
                self._bio_update_thread = threading.Thread(target=self._bio_update_worker, daemon=True)
                self._bio_update_thread.start()
            else:
                self._bio_update_thread = None
        except Exception:
            self._bio_update_thread = None
        self._load_external_commands()
        self._search_cache = {}
        self._spotify_volume_cache_value = None
        self._spotify_volume_cache_ts = 0.0
        self._core_resources_bootstrap_running = False
        self._settings_update_tokens = {}
        self._settings_update_lock = threading.Lock()
        self._telemetry_lock = threading.Lock()
        self._telemetry_sending = False
        self._telemetry_queue = []
        self._telemetry_last_flush_ts = 0
        self._telemetry_install_id = ""

    def on_send_message_hook(self, account, params):
        try:
            raw_msg = None
            if hasattr(params, "message") and isinstance(params.message, str):
                raw_msg = params.message
            elif isinstance(params, dict):
                m = params.get("message", None)
                if isinstance(m, str):
                    raw_msg = m
            if isinstance(raw_msg, str):
                cmd = raw_msg.strip()
                cmd_low = cmd.lower()
                if cmd_low == ".fab on":
                    try:
                        params.message = ""
                    except Exception:
                        pass
                    try:
                        params["message"] = ""
                    except Exception:
                        pass
                    self.set_setting("fab_chat_enabled", True)
                    try:
                        self.set_setting("nowfy_flow_enabled", True)
                    except Exception:
                        pass
                    self._apply_chat_fab_state()
                    try:
                        BulletinHelper.show_success("FAB enabled")
                    except Exception:
                        pass
                    return HookResult(strategy=HookStrategy.CANCEL)
                if cmd_low == ".fab off":
                    try:
                        params.message = ""
                    except Exception:
                        pass
                    try:
                        params["message"] = ""
                    except Exception:
                        pass
                    self.set_setting("fab_chat_enabled", False)
                    try:
                        self.set_setting("nowfy_flow_enabled", False)
                    except Exception:
                        pass
                    self._apply_chat_fab_state()
                    try:
                        BulletinHelper.show_info("FAB disabled")
                    except Exception:
                        pass
                    return HookResult(strategy=HookStrategy.CANCEL)
                if cmd == ".sync":
                    try:
                        params.message = ""
                    except Exception:
                        pass
                    run_on_queue(self._run_internal_sync_local)
                    return HookResult(strategy=HookStrategy.CANCEL)
                if cmd == "!notice" or cmd == "!release":
                    try:
                        params.message = ""
                    except Exception:
                        pass
                    run_on_queue(self._run_internal_notice_local)
                    return HookResult(strategy=HookStrategy.CANCEL)
                if cmd == ".backup":
                    try:
                        params.message = ""
                    except Exception:
                        pass
                    self._run_internal_backup_local(params)
                    return HookResult(strategy=HookStrategy.CANCEL)
                first_token = (cmd_low.split(" ", 1)[0] if cmd_low else "")
                if first_token == "!nowfy" or first_token.startswith("!nowfy@"):
                    try:
                        try:
                            params.message = ""
                        except Exception:
                            pass
                        try:
                            params["message"] = ""
                        except Exception:
                            pass
                        ok = bool(self._send_nowfysettings_inline_message(params))
                    except Exception:
                        ok = False
                    try:
                        log(f"[Nowfy][NowfySettings] command intercepted ok={ok}")
                    except Exception:
                        pass
                    if ok:
                        return HookResult(strategy=HookStrategy.CANCEL)
                    try:
                        BulletinHelper.show_info("NowfySettings unavailable")
                    except Exception:
                        pass
                    return HookResult(strategy=HookStrategy.CANCEL)
        except Exception:
            pass
        try:
            parent = getattr(super(), "on_send_message_hook", None)
            if callable(parent):
                return parent(account, params)
        except Exception:
            pass
        return HookResult()

    def _run_internal_sync_local(self):
        try:
            if nowfycore is not None and hasattr(nowfycore, "attach_host_plugin"):
                try:
                    nowfycore.attach_host_plugin(self)
                except Exception:
                    pass
            if nowfycore is not None and hasattr(nowfycore, "get_nowfy_core_api"):
                try:
                    global NOWFY_CORE_API
                    NOWFY_CORE_API = nowfycore.get_nowfy_core_api()
                except Exception:
                    pass
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "run_internal_sync"):
                ok = bool(NOWFY_CORE_API.run_internal_sync(self))
                if ok:
                    return
            BulletinHelper.show_info("Sync unavailable")
        except Exception:
            try:
                BulletinHelper.show_info("Sync unavailable")
            except Exception:
                pass

    def _run_internal_notice_local(self):
        try:
            if nowfycore is not None and hasattr(nowfycore, "attach_host_plugin"):
                try:
                    nowfycore.attach_host_plugin(self)
                except Exception:
                    pass
            if nowfycore is not None and hasattr(nowfycore, "get_nowfy_core_api"):
                try:
                    global NOWFY_CORE_API
                    NOWFY_CORE_API = nowfycore.get_nowfy_core_api()
                except Exception:
                    pass
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "run_release_notice"):
                ok = bool(NOWFY_CORE_API.run_release_notice(self))
                if ok:
                    return
            BulletinHelper.show_info("Notice unavailable")
        except Exception:
            try:
                BulletinHelper.show_info("Notice unavailable")
            except Exception:
                pass

    def _run_internal_backup_local(self, params):
        try:
            if nowfycore is not None and hasattr(nowfycore, "attach_host_plugin"):
                try:
                    nowfycore.attach_host_plugin(self)
                except Exception:
                    pass
            if nowfycore is not None and hasattr(nowfycore, "get_nowfy_core_api"):
                try:
                    global NOWFY_CORE_API
                    NOWFY_CORE_API = nowfycore.get_nowfy_core_api()
                except Exception:
                    pass
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "run_backup_command"):
                ok = bool(NOWFY_CORE_API.run_backup_command(self, params))
                if ok:
                    return
            try:
                local_fn = getattr(self, "_show_backup_chat_bottom_sheet", None)
                if callable(local_fn):
                    run_on_ui_thread(lambda: local_fn(params))
                    return
            except Exception:
                pass
            try:
                run_on_ui_thread(lambda: self._show_backup_chat_bottom_sheet_local(params))
                return
            except Exception:
                pass
            BulletinHelper.show_info("Backup unavailable")
        except Exception:
            try:
                BulletinHelper.show_info("Backup unavailable")
            except Exception:
                pass

    def _show_backup_chat_bottom_sheet_local(self, params):
        try:
            fragment = get_last_fragment()
            ctx = fragment.getParentActivity() if fragment and fragment.getParentActivity() else ApplicationLoader.applicationContext
            if ctx is None:
                BulletinHelper.show_info("Backup unavailable")
                return
            sheet = BottomSheet(ctx, True)
            container = LinearLayout(ctx)
            container.setOrientation(LinearLayout.VERTICAL)
            container.setPadding(AndroidUtilities.dp(20), AndroidUtilities.dp(18), AndroidUtilities.dp(20), AndroidUtilities.dp(16))
            try:
                hero = ImageView(ctx)
                candidates = [
                    os.path.join(os.path.dirname(__file__), "nowfy", "assets", "png", "backup_data.png"),
                    os.path.join(os.path.dirname(__file__), "assets", "png", "backup_data.png"),
                ]
                for hero_path in candidates:
                    if os.path.isfile(hero_path):
                        bmp = BitmapFactory.decodeFile(hero_path)
                        if bmp is not None:
                            hero.setImageBitmap(bmp)
                            hero.setAdjustViewBounds(False)
                            hero.setScaleType(ImageView.ScaleType.CENTER_CROP)
                            lp_hero = LinearLayout.LayoutParams(-1, AndroidUtilities.dp(180))
                            lp_hero.gravity = Gravity.CENTER_HORIZONTAL
                            lp_hero.bottomMargin = AndroidUtilities.dp(8)
                            container.addView(hero, lp_hero)
                            break
            except Exception:
                pass
            title = TextView(ctx)
            title.setText(tr("backup_chat_title"))
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18)
            title.setGravity(Gravity.CENTER_HORIZONTAL)
            try:
                title.setTypeface(AndroidUtilities.bold())
            except Exception:
                pass
            try:
                title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                pass
            container.addView(title)
            desc = TextView(ctx)
            desc.setText(tr("backup_chat_desc"))
            desc.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
            desc.setGravity(Gravity.CENTER_HORIZONTAL)
            try:
                desc.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            except Exception:
                pass
            lp_desc = LinearLayout.LayoutParams(-1, -2)
            lp_desc.topMargin = AndroidUtilities.dp(10)
            container.addView(desc, lp_desc)
            create_btn = TextView(ctx)
            create_btn.setText(tr("backup_chat_create_button"))
            create_btn.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
            create_btn.setGravity(Gravity.CENTER)
            try:
                create_btn.setTypeface(AndroidUtilities.bold())
            except Exception:
                pass
            bg_create = GradientDrawable()
            bg_create.setCornerRadius(float(AndroidUtilities.dp(12)))
            try:
                bg_create.setColor(Theme.getColor(Theme.key_featuredStickers_addButton))
                create_btn.setTextColor(Theme.getColor(Theme.key_featuredStickers_buttonText))
            except Exception:
                bg_create.setColor(0x332D87FF)
            create_btn.setBackground(bg_create)
            lp_create = LinearLayout.LayoutParams(-1, AndroidUtilities.dp(44))
            lp_create.topMargin = AndroidUtilities.dp(16)
            container.addView(create_btn, lp_create)
            close_btn = TextView(ctx)
            close_btn.setText(tr("backup_chat_cancel_button"))
            close_btn.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
            close_btn.setGravity(Gravity.CENTER)
            bg_close = GradientDrawable()
            bg_close.setCornerRadius(float(AndroidUtilities.dp(12)))
            try:
                bg_close.setColor(Theme.getColor(Theme.key_windowBackgroundGray))
                close_btn.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlueText))
            except Exception:
                bg_close.setColor(0x22394B6A)
            close_btn.setBackground(bg_close)
            lp_close = LinearLayout.LayoutParams(-1, AndroidUtilities.dp(44))
            lp_close.topMargin = AndroidUtilities.dp(10)
            container.addView(close_btn, lp_close)
            def _do_create(_v):
                try:
                    sheet.dismiss()
                except Exception:
                    pass
                run_on_queue(lambda: self._backup_create_and_send_local(params))
            def _do_close(_v):
                try:
                    sheet.dismiss()
                except Exception:
                    pass
            create_btn.setOnClickListener(OnClickListener(_do_create))
            close_btn.setOnClickListener(OnClickListener(_do_close))
            sheet.setCustomView(container)
            sheet.show()
        except Exception:
            try:
                BulletinHelper.show_info("Backup unavailable")
            except Exception:
                pass

    def _backup_create_and_send_local(self, params):
        try:
            manager = BackupManager(self)
            filepath = str(manager.export_backup() or "")
            if not filepath or (not os.path.isfile(filepath)):
                try:
                    files = [f for f in os.listdir(manager.backup_dir) if str(f).lower().endswith(".nowfy")]
                    files.sort(key=lambda x: os.path.getmtime(os.path.join(manager.backup_dir, x)), reverse=True)
                    if files:
                        filepath = os.path.join(manager.backup_dir, files[0])
                except Exception:
                    filepath = ""
            if not filepath or (not os.path.isfile(filepath)):
                BulletinHelper.show_info("Backup unavailable")
                return
            peer = None
            try:
                peer = getattr(params, "peer", None)
            except Exception:
                peer = None
            if not peer:
                try:
                    fragment = get_last_fragment()
                    peer = fragment.getDialogId() if fragment and hasattr(fragment, "getDialogId") else None
                except Exception:
                    peer = None
            if not peer:
                BulletinHelper.show_info("Backup unavailable")
                return
            send_document(peer, filepath, caption=(tr("backup_chat_sent_caption")))
            BulletinHelper.show_success(tr("backup_chat_sent_success"))
        except Exception:
            try:
                BulletinHelper.show_info("Backup unavailable")
            except Exception:
                pass

    def _core_addon_enabled(self, addon_key, default_value=False):
        try:
            key = str(addon_key or "").strip()
            addon_plugin_map = {
                "addon_nowcast_enabled": "nowfy_nowcast",
            }
            pid = str(addon_plugin_map.get(key, "") or "").strip()
            if pid:
                try:
                    controller = PluginsController.getInstance()
                    pth = controller.getPluginPath(pid) if controller else None
                    if (not pth) or (not os.path.isfile(str(pth))):
                        return False
                except Exception:
                    return False
        except Exception:
            pass
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "is_addon_enabled"):
                return bool(NOWFY_CORE_API.is_addon_enabled(self, addon_key, default_value))
        except Exception:
            pass
        try:
            return bool(self.get_setting(str(addon_key), bool(default_value)))
        except Exception:
            return bool(default_value)

    def _apply_addon_runtime_patches(self):
        try:
            if bool(getattr(self, "_addon_runtime_patched", False)):
                return 0
            import importlib
            patched_total = 0
            plan = [
                ("addon_nowcast_enabled", "nowfy_nowcast"),
            ]
            for addon_key, module_name in plan:
                try:
                    if not self._core_addon_enabled(addon_key, False):
                        continue
                    mod = importlib.import_module(module_name)
                    fn = getattr(mod, "patch_nowfy_runtime", None)
                    if callable(fn):
                        patched_total += int(fn() or 0)
                except Exception as e:
                    try:
                        log(f"[Nowfy][Addon] lazy patch failed {module_name}: {e}")
                    except Exception:
                        pass
            self._addon_runtime_patched = True
            try:
                log(f"[Nowfy][Addon] lazy patched={patched_total}")
            except Exception:
                pass
            return patched_total
        except Exception:
            return 0

    def _request_settings_list_update(self, list_view, delay_ms=0, channel="default"):
        try:
            adapter = getattr(list_view, "adapter", None) if list_view is not None else None
            if adapter is None:
                return False
            try:
                token = int(time.time() * 1000)
                with self._settings_update_lock:
                    self._settings_update_tokens[str(channel)] = token
            except Exception:
                token = int(time.time() * 1000)
            def _do_refresh(expected=token, ch=str(channel)):
                try:
                    with self._settings_update_lock:
                        if int(self._settings_update_tokens.get(ch, -1) or -1) != int(expected):
                            return
                except Exception:
                    pass
                try:
                    ad = getattr(list_view, "adapter", None)
                    if ad is not None:
                        ad.update(True)
                except Exception:
                    pass
            run_on_ui_thread(_do_refresh, int(delay_ms or 0))
            return True
        except Exception:
            return False

    def _load_external_commands(self):
        try:
            resp = requests.get(self._external_commands_url, timeout=5)
            if resp.status_code == 200:
                self._external_commands = resp.json()
                return
        except Exception:
            pass
        try:
            with open(self._external_commands_local, "r", encoding="utf-8") as f:
                self._external_commands = json.load(f)
        except Exception:
            self._external_commands = None

    def _get_external_command(self, cmd):
        if not self._external_commands:
            self._load_external_commands()
        if self._external_commands and "commands" in self._external_commands:
            return self._external_commands["commands"].get(cmd)
        return None

    def _get_caption_template(self, style, track_data):
        templates = {
            "Apple Based": "[\U0001F399](5909015791088439934) *{track}*\nby *{artist}* from *{album}*\n[\U0001F517](5256057883082107781)",
            "Pepe": "[\U0001F918](5942984300885446067) *{track}*\nby *{artist}* from *{album}*\n[\U0001F3B8](5938034540055366532)",
            "Minim": "[\U0001F3B5](5258289810082111221) *Now Playing*: {track}\n*by* {artist} | {album}",
            "Spoty": "[\U0001F3B5](5294137402430858861) *{track}*\nfrom *{album}* by *{artist}*"
        }
        if style not in templates:
            return ""
        template = templates[style]
        if track_data:
            template = template.replace("{track}", track_data.get("name", "Unknown Track"))
            template = template.replace("{artist}", track_data.get("artist", "Powered by Nowfy"))
            template = template.replace("{album}", track_data.get("album", "Unknown Album"))
        return template

    def _add_menu_items(self):
        try:
            self.remove_menu_items()
            if self.get_setting("show_chat_menu", True):
                self._nowfy_chat_menu_item = self.add_menu_item(MenuItemData(
                    menu_type=MenuItemType.CHAT_ACTION_MENU,
                    text=tr("Nowfy"),
                    icon="files_music",
                    priority=5,
                    on_click=lambda ctx: run_on_ui_thread(lambda: self._open_plugin_settings())
                ))
                if bool(self.get_setting("nowfy_pocket_shortcut_enabled", False)):
                    self._nowfy_pocket_chat_menu_item = self.add_menu_item(MenuItemData(
                        menu_type=MenuItemType.CHAT_ACTION_MENU,
                        text="Nowfy Pocket",
                        icon="msg_tone_on",
                        priority=6,
                        on_click=lambda ctx: run_on_ui_thread(lambda: self._toggle_nowfy_pocket())
                    ))
        except Exception as e:
            log(f"[Nowfy] Failed to add menu items: {e}")

    def remove_menu_items(self):
        try:
            try:
                if getattr(self, "_nowfy_chat_menu_item", None):
                    self.remove_menu_item(self._nowfy_chat_menu_item)
                    self._nowfy_chat_menu_item = None
            except Exception:
                pass
            try:
                if getattr(self, "_nowfy_pocket_chat_menu_item", None):
                    self.remove_menu_item(self._nowfy_pocket_chat_menu_item)
                    self._nowfy_pocket_chat_menu_item = None
            except Exception:
                pass
        except Exception as e:
            log(f"[Nowfy] Failed to remove menu items: {e}")

    def _is_service_message(self, message):
        try:
            from org.telegram.tgnet import TLRPC
            return message and hasattr(message, 'messageOwner') and isinstance(message.messageOwner, TLRPC.TL_messageService)
        except Exception:
            return False

    def _is_failed_message(self, message):
        try:
            if not message or not hasattr(message, 'messageOwner') or not message.messageOwner:
                return False
            message_owner = message.messageOwner
            return (
                (hasattr(message_owner, 'send_state') and message_owner.send_state == 2)
                or (hasattr(message_owner, 'id') and message_owner.id < 0)
            )
        except Exception:
            return False

    def _on_now_playing_context_click(self, chat_activity, message):
        try:
            log(f"[Nowfy] Now Playing clicked in context menu")
            self._send_now_playing_card()
        except Exception as e:
            log(f"[Nowfy] Error in Now Playing context click: {e}")
            BulletinHelper.show_info(f"Error: {e}")

    def _open_plugin_settings(self):
        try:
            log("[Nowfy] Attempting to open plugin settings...")
            controller = PluginsController.getInstance()
            log(f"[Nowfy] Controller instance: {controller}")
            plugin = controller.plugins.get(self.id)
            log(f"[Nowfy] Plugin instance: {plugin}")
            fragment = get_last_fragment()
            log(f"[Nowfy] Fragment instance: {fragment}")
            if plugin and fragment:
                def _open():
                    try:
                        fragment.presentFragment(PluginSettingsActivity(plugin))
                        log("[Nowfy] Settings opened successfully")
                    except Exception as ee:
                        log(f"[Nowfy] Failed opening settings after resource check: {ee}")
                ready = True
                try:
                    if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "are_translation_resources_ready"):
                        ready = bool(NOWFY_CORE_API.are_translation_resources_ready())
                except Exception:
                    ready = True
                if ready:
                    _open()
                    return
                if getattr(self, "_core_resources_bootstrap_running", False):
                    return
                self._core_resources_bootstrap_running = True
                ctx = None
                try:
                    ctx = fragment.getParentActivity() if fragment else None
                except Exception:
                    ctx = None
                if ctx is None:
                    ctx = ApplicationLoader.applicationContext
                progress_dialog = None
                try:
                    progress_dialog = AlertDialogBuilder(ctx, AlertDialogBuilder.ALERT_TYPE_LOADING)
                    progress_dialog.set_title("Downloading resources...")
                    progress_dialog.set_message("Preparing NowfyCore translations")
                    progress_dialog.set_progress(5)
                    try:
                        progress_dialog.set_cancelable(False)
                    except Exception:
                        pass
                    progress_dialog.show()
                except Exception:
                    progress_dialog = None
                def _worker():
                    ok = False
                    try:
                        if progress_dialog:
                            run_on_ui_thread(lambda: progress_dialog.set_progress(25))
                        if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "ensure_translation_resources"):
                            ok = bool(NOWFY_CORE_API.ensure_translation_resources(False))
                        else:
                            ok = True
                        if progress_dialog:
                            run_on_ui_thread(lambda: progress_dialog.set_progress(100))
                    except Exception:
                        ok = False
                    finally:
                        try:
                            if progress_dialog:
                                run_on_ui_thread(lambda: progress_dialog.dismiss())
                        except Exception:
                            pass
                        self._core_resources_bootstrap_running = False
                        if ok:
                            run_on_ui_thread(_open)
                        else:
                            try:
                                run_on_ui_thread(lambda: BulletinHelper.show_info("Could not download resources right now."))
                            except Exception:
                                pass
                            run_on_ui_thread(_open)
                threading.Thread(target=_worker, daemon=True).start()
            else:
                log(f"[Nowfy] Failed to open settings - Plugin: {plugin}, Fragment: {fragment}")
        except Exception as e:
            log(f"[Nowfy] Error opening plugin settings: {str(e)}\nType: {type(e)}")
            import traceback
            log(traceback.format_exc())

    def _nowfy_pocket_local_paths(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(base_dir)
            main_path = os.path.join(root_dir, "nowfy.plugin")
            normal_cached = os.path.join(root_dir, "nowfy.plugin.cache.normal")
            pocket_cached = os.path.join(root_dir, "nowfy.plugin.cache.pocket")
            return main_path, normal_cached, pocket_cached
        except Exception:
            return None, None, None

    def _nowfy_pocket_requirements_line(self):
        return '__requirements__ = "nowfy"'

    def _nowfy_pocket_normalize_bytes(self, data, want_pocket):
        try:
            if not data:
                return b""
            text = data.decode("utf-8-sig", "ignore")
            lines = text.splitlines()
            req_line = self._nowfy_pocket_requirements_line()
            clean_lines = [line for line in lines if not re.match(r"^\s*__requirements__\s*=", str(line or ""))]
            if not want_pocket:
                insert_at = 0
                for idx, line in enumerate(clean_lines):
                    if str(line or "").startswith("__name__"):
                        insert_at = idx + 1
                        break
                clean_lines.insert(insert_at, req_line)
            normalized = "\n".join(clean_lines).strip() + "\n"
            return normalized.encode("utf-8")
        except Exception:
            return data

    def _nowfy_pocket_file_matches(self, file_path, want_pocket):
        try:
            if not file_path or not os.path.exists(file_path) or os.path.getsize(file_path) <= 0:
                return False
            with open(file_path, "rb") as fh:
                raw = fh.read()
            text = raw.decode("utf-8-sig", "ignore")
            has_requirements = bool(re.search(r"^\s*__requirements__\s*=\s*[\"']nowfy[\"']", text, re.M))
            return (not has_requirements) if want_pocket else has_requirements
        except Exception:
            return False

    def _nowfy_pocket_write_variant(self, out_path, data, want_pocket):
        try:
            normalized = self._nowfy_pocket_normalize_bytes(data, want_pocket)
            tmp = str(out_path or "") + ".tmp"
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass
            with open(tmp, "wb") as fh:
                fh.write(normalized)
            os.replace(tmp, out_path)
            return True
        except Exception:
            return False

    def _sync_nowfy_pocket_setting_from_file(self):
        try:
            main_path, _normal_cached, _pocket_cached = self._nowfy_pocket_local_paths()
            if not main_path or not os.path.exists(main_path):
                return False
            self.set_setting("nowfy_pocket_mode", bool(self._nowfy_pocket_file_matches(main_path, True)))
            return True
        except Exception:
            return False

    def _nowfy_pocket_remote_urls(self, want_pocket):
        try:
            base = "https://coreupdates.meyankut.workers.dev"
            normal = [
                f"{base}/nowfy.plugin",
            ]
            pocket = [
                f"{base}/nowfy_pocket.plugin",
                f"{base}/nowfy_pocket_mode.plugin",
                f"{base}/nowfy-pocket.plugin",
                f"{base}/nowfy_pocketmode.plugin",
                f"{base}/nowfy_no_requirements.plugin",
                f"{base}/nowfy_no_reqs.plugin",
                f"{base}/nowfy.plugin",
            ]
            return pocket if want_pocket else normal
        except Exception:
            return []

    def _nowfy_pocket_download_first_ok(self, urls, out_path, want_pocket):
        for url in list(urls or []):
            try:
                if not url:
                    continue
                fetch_url = f"{str(url)}{'&' if '?' in str(url) else '?'}_nowfy_ts={int(time.time() * 1000)}"
                resp = requests.get(
                    fetch_url,
                    timeout=20,
                    headers={
                        "User-Agent": "Mozilla/5.0 (NowfyPocket)",
                        "Cache-Control": "no-cache, no-store, must-revalidate",
                        "Pragma": "no-cache",
                        "Expires": "0",
                    },
                )
                if int(resp.status_code or 0) != 200:
                    continue
                data = resp.content or b""
                if not data:
                    continue
                if not self._nowfy_pocket_write_variant(out_path, data, want_pocket):
                    continue
                return True
            except Exception:
                continue
        return False

    def _nowfy_pocket_prepare_install_file(self, want_pocket):
        main_path, normal_cached, pocket_cached = self._nowfy_pocket_local_paths()
        if not main_path:
            raise Exception("Nowfy Pocket: local path unavailable")
        target_cached = pocket_cached if want_pocket else normal_cached
        try:
            if target_cached and os.path.exists(target_cached):
                os.remove(target_cached)
        except Exception:
            pass
        ok = self._nowfy_pocket_download_first_ok(self._nowfy_pocket_remote_urls(want_pocket), target_cached, want_pocket)
        if not ok:
            if not os.path.exists(main_path):
                raise Exception("Nowfy Pocket: installed plugin missing")
            with open(main_path, "rb") as fh:
                raw = fh.read()
            if not self._nowfy_pocket_write_variant(target_cached, raw, want_pocket):
                raise Exception("Nowfy Pocket: fallback write failed")
        install_base = os.path.dirname(str(main_path))
        if not install_base:
            raise Exception("Nowfy Pocket: temp directory unavailable")
        tmp_install = os.path.join(install_base, ".temp_nowfy_install.plugin")
        with open(target_cached, "rb") as src:
            if not self._nowfy_pocket_write_variant(tmp_install, src.read(), want_pocket):
                raise Exception("Nowfy Pocket: install file prepare failed")
        return tmp_install

    def _nowfy_pocket_install_silently(self, install_path, want_pocket, done_cb=None):
        try:
            if not install_path or not os.path.exists(install_path):
                raise Exception("Nowfy Pocket: install file missing")
            PluginsConstants = jclass("com.exteragram.messenger.plugins.PluginsConstants")
            NotificationCenter = jclass("org.telegram.messenger.NotificationCenter")
            Callback = jclass("org.telegram.messenger.Utilities$Callback")
            controller = PluginsController.getInstance()
            if controller is None:
                raise Exception("Nowfy Pocket: plugins controller unavailable")
            python_engine = None
            try:
                python_engine = PluginsController.engines.get(PluginsConstants.PYTHON)
            except Exception:
                python_engine = None
            if python_engine is None:
                try:
                    python_engine = controller.engines.get("python")
                except Exception:
                    python_engine = None
            if python_engine is None:
                raise Exception("Nowfy Pocket: python engine unavailable")
            plugin = self

            class _InstallCallback(dynamic_proxy(Callback)):
                def run(self_cb, error):
                    def _finish():
                        success = not bool(error)
                        try:
                            plugin._nowfy_pocket_install_in_progress = False
                        except Exception:
                            pass
                        try:
                            if getattr(plugin, "_nowfy_pocket_loading_dialog", None):
                                plugin._nowfy_pocket_loading_dialog.dismiss()
                                plugin._nowfy_pocket_loading_dialog = None
                        except Exception:
                            pass
                        if success:
                            try:
                                plugin.set_setting("nowfy_pocket_mode", bool(want_pocket))
                            except Exception:
                                pass
                            try:
                                controller.loadPluginSettings(__id__)
                            except Exception:
                                pass
                            try:
                                controller.setPluginEnabled(__id__, True, None)
                            except Exception:
                                pass
                            try:
                                NotificationCenter.getGlobalInstance().postNotificationName(NotificationCenter.pluginsUpdated)
                            except Exception:
                                pass
                            try:
                                BulletinHelper.show_success("Nowfy Pocket enabled." if want_pocket else "Nowfy Pocket disabled.")
                            except Exception:
                                pass
                        else:
                            try:
                                BulletinHelper.show_error(str(error) or "Nowfy Pocket installation failed.")
                            except Exception:
                                pass
                        try:
                            if install_path and os.path.exists(install_path):
                                os.remove(install_path)
                        except Exception:
                            pass
                        try:
                            if callable(done_cb):
                                done_cb(bool(success), bool(want_pocket) if success else bool(plugin.get_setting("nowfy_pocket_mode", False)))
                        except Exception:
                            pass
                    run_on_ui_thread(_finish)

            python_engine.loadPluginFromFile(str(install_path), None, _InstallCallback())
            return True
        except Exception as e:
            log(f"[Nowfy] Nowfy Pocket install start fail: {e}")
            return False

    def _toggle_nowfy_pocket(self, desired_enabled=None, done_cb=None):
        try:
            with self._nowfy_pocket_install_lock:
                if bool(self._nowfy_pocket_install_in_progress):
                    return
                current_enabled = bool(self.get_setting("nowfy_pocket_mode", False))
                want_pocket = (not current_enabled) if desired_enabled is None else bool(desired_enabled)
                self._nowfy_pocket_install_in_progress = True
            frag = get_last_fragment()
            ctx = frag.getParentActivity() if frag and frag.getParentActivity() else ApplicationLoader.applicationContext
            if ctx is None:
                self._nowfy_pocket_install_in_progress = False
                raise Exception("Nowfy Pocket: UI context missing")
            try:
                if getattr(self, "_nowfy_pocket_loading_dialog", None) is not None:
                    self._nowfy_pocket_loading_dialog.dismiss()
                    self._nowfy_pocket_loading_dialog = None
            except Exception:
                pass
            dialog = AlertDialogBuilder(ctx, AlertDialogBuilder.ALERT_TYPE_SPINNER)
            dialog.set_title("Nowfy Pocket")
            dialog.set_message("Applying changes...")
            dialog.set_cancelable(True)
            dialog.set_canceled_on_touch_outside(True)
            self._nowfy_pocket_loading_dialog = dialog
            dialog.show()

            def _worker():
                ok = False
                err = ""
                install_path = None
                try:
                    install_path = self._nowfy_pocket_prepare_install_file(want_pocket)
                    ok = True
                except Exception as e:
                    err = str(e)
                    ok = False

                def _done():
                    if ok:
                        started = False
                        try:
                            started = self._nowfy_pocket_install_silently(install_path, want_pocket, done_cb=done_cb)
                        except Exception:
                            started = False
                        if not started:
                            try:
                                self._nowfy_pocket_install_in_progress = False
                            except Exception:
                                pass
                            try:
                                if getattr(self, "_nowfy_pocket_loading_dialog", None) is dialog:
                                    dialog.dismiss()
                                    self._nowfy_pocket_loading_dialog = None
                            except Exception:
                                pass
                            try:
                                BulletinHelper.show_error("Nowfy Pocket installation failed to start.")
                            except Exception:
                                pass
                    else:
                        try:
                            self._nowfy_pocket_install_in_progress = False
                        except Exception:
                            pass
                        try:
                            if getattr(self, "_nowfy_pocket_loading_dialog", None) is dialog:
                                dialog.dismiss()
                                self._nowfy_pocket_loading_dialog = None
                        except Exception:
                            pass
                        try:
                            BulletinHelper.show_error(err or "Nowfy Pocket installation failed.")
                        except Exception:
                            pass
                        try:
                            if callable(done_cb):
                                done_cb(False, bool(self.get_setting("nowfy_pocket_mode", False)))
                        except Exception:
                            pass

                run_on_ui_thread(_done)

            threading.Thread(target=_worker, daemon=True).start()
        except Exception as e:
            try:
                self._nowfy_pocket_install_in_progress = False
            except Exception:
                pass
            log(f"[Nowfy] Nowfy Pocket toggle fail: {e}")

    def _on_nowfy_pocket_changed(self, enabled):
        try:
            want = bool(enabled)
            if bool(self._nowfy_pocket_install_in_progress):
                return
            self._toggle_nowfy_pocket(desired_enabled=want, done_cb=lambda _ok, _state: self.reload_settings())
        except Exception as e:
            log(f"[Nowfy] Nowfy Pocket switch fail: {e}")

    def _set_subfragment_callback(self, activity, callback_fn):
        def _make_proxy(iface):
            Proxy = dynamic_proxy(iface)
            class _Callback(Proxy):
                def __init__(self, plugin):
                    super().__init__()
                    self._plugin = plugin
                def _call(self, *args):
                    try:
                        return callback_fn()
                    except TypeError:
                        try:
                            return callback_fn(*args)
                        except Exception:
                            return callback_fn()
                    except Exception:
                        return callback_fn()
                def apply(self, *args):
                    return self._call(*args)
                def call(self, *args):
                    return self._call(*args)
                def invoke(self, *args):
                    return self._call(*args)
                def create(self, *args):
                    return self._call(*args)
                def createSubFragment(self, *args):
                    return self._call(*args)
            return _Callback(self)
        def _find_callback_field(clazz):
            cur = clazz
            while cur is not None:
                try:
                    f = cur.getDeclaredField("createSubFragmentCallback")
                    if f is not None:
                        f.setAccessible(True)
                        return f
                except Exception:
                    pass
                try:
                    cur = cur.getSuperclass()
                except Exception:
                    cur = None
            return None
        try:
            cls = activity.getClass()
            field = _find_callback_field(cls)
            if field is None:
                raise RuntimeError("callback field not found")
            cb_type = field.getType()
            if cb_type and cb_type.isInterface():
                field.set(activity, _make_proxy(cb_type))
                try:
                    log("[Nowfy] _set_subfragment_callback: interface proxy OK")
                except Exception:
                    pass
                return True
        except Exception:
            pass
        for iface_name in (
            "kotlin.jvm.functions.Function0",
            "kotlin.jvm.functions.Function1",
            "java.util.function.Function",
            "java.util.concurrent.Callable",
        ):
            try:
                iface = jclass(iface_name)
                cls = activity.getClass()
                field = _find_callback_field(cls)
                if field is None:
                    continue
                field.set(activity, _make_proxy(iface))
                try:
                    log(f"[Nowfy] _set_subfragment_callback: fallback proxy OK ({iface_name})")
                except Exception:
                    pass
                return True
            except Exception:
                continue
        try:
            log("[Nowfy] _set_subfragment_callback: failed (no compatible proxy)")
        except Exception:
            pass
        return False

    def _open_nowfy_panel_settings(self):
        try:
            controller = PluginsController.getInstance()
            plugin = controller.plugins.get(self.id)
            fragment = get_last_fragment()
            if not plugin or not fragment:
                return
            activity = PluginSettingsActivity(plugin)
            try:
                self._set_subfragment_callback(activity, self.create_nowfy_panel_subfragment)
            except Exception:
                pass
            fragment.presentFragment(activity)
        except Exception:
            pass

    def _open_extended_settings(self):
        try:
            controller = PluginsController.getInstance()
            plugin = controller.plugins.get(self.id)
            fragment = get_last_fragment()
            if not plugin or not fragment:
                return
            try:
                log("[Nowfy] Opening Extended subfragment")
            except Exception:
                pass
            activity = PluginSettingsActivity(plugin)
            try:
                ok = self._set_subfragment_callback(activity, self.create_extended_subfragment)
                try:
                    log(f"[Nowfy] Extended callback set: {ok}")
                except Exception:
                    pass
            except Exception:
                pass
            fragment.presentFragment(activity)
        except Exception:
            pass

    def _handle_home_cover_quick_unlock_tap(self):
        try:
            unlocked_raw = self.get_setting("home_cover_quick_menu_unlocked", False)
            unlocked = False
            if isinstance(unlocked_raw, bool):
                unlocked = unlocked_raw
            else:
                unlocked = str(unlocked_raw).strip().lower() in ("1", "true", "yes", "on")
            if unlocked:
                return
            count = int(self.get_setting("home_cover_quick_menu_taps", 0) or 0) + 1
            self.set_setting("home_cover_quick_menu_taps", count)
            if count >= 20:
                self.set_setting("home_cover_quick_menu_unlocked", True)
                self.set_setting("home_cover_quick_menu_taps", 0)
                try:
                    BulletinHelper.show_info(":)")
                except Exception:
                    pass
        except Exception:
            pass

    def _show_home_cover_quick_menu(self, anchor_view):
        try:
            PopupWindow = find_class("android.widget.PopupWindow")
            if not PopupWindow:
                return
            ctx = None
            try:
                frag = get_last_fragment()
                if frag:
                    ctx = frag.getParentActivity()
            except Exception:
                ctx = None
            if not ctx:
                try:
                    ctx = ApplicationLoader.applicationContext
                except Exception:
                    ctx = None
            if not ctx or not anchor_view:
                return
            try:
                old_popup = getattr(self, "_home_cover_quick_popup", None)
                if old_popup:
                    old_popup.dismiss()
            except Exception:
                pass
            enabled = bool(self.get_setting("header_cover_enabled", True))
            LinearLayoutCls = find_class("android.widget.LinearLayout")
            TextViewCls = find_class("android.widget.TextView")
            if not LinearLayoutCls or not TextViewCls:
                return
            root = LinearLayoutCls(ctx)
            root.setOrientation(LinearLayout.VERTICAL)
            try:
                bg = GradientDrawable()
                bg.setCornerRadius(AndroidUtilities.dp(16))
                bg.setColor(Theme.getColor(Theme.key_windowBackgroundWhite))
                root.setBackground(bg)
            except Exception:
                pass
            try:
                if Build.VERSION.SDK_INT >= 21:
                    root.setElevation(float(AndroidUtilities.dp(8)))
            except Exception:
                pass

            row = LinearLayoutCls(ctx)
            row.setOrientation(LinearLayout.HORIZONTAL)
            row.setGravity(Gravity.CENTER_VERTICAL | Gravity.LEFT)
            row.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(12))

            tv = TextViewCls(ctx)
            tv.setText(str(tr("nowfy_extended_cover_label")))
            try:
                tv.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
                tv.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
                tv.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
            except Exception:
                pass
            row.addView(tv, LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT))

            cb = LinearLayoutCls(ctx)
            cb.setGravity(Gravity.CENTER)
            try:
                cb_bg = GradientDrawable()
                cb_bg.setCornerRadius(AndroidUtilities.dp(6))
                if enabled:
                    cb_bg.setColor(0x00000000)
                    cb_bg.setStroke(AndroidUtilities.dp(1), Theme.getColor(Theme.key_switchTrackChecked))
                else:
                    cb_bg.setColor(0x00000000)
                    cb_bg.setStroke(AndroidUtilities.dp(1), Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
                cb.setBackground(cb_bg)
            except Exception:
                pass

            mark = TextViewCls(ctx)
            mark.setText("✓" if enabled else "")
            try:
                mark.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
                mark.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
                mark.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                pass
            try:
                cb.addView(mark, LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT))
            except Exception:
                cb.addView(mark)

            lp_cb = LinearLayout.LayoutParams(AndroidUtilities.dp(24), AndroidUtilities.dp(24))
            lp_cb.leftMargin = AndroidUtilities.dp(10)
            row.addView(cb, lp_cb)

            root.addView(row, LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT))
            popup = PopupWindow(root, LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT, True)
            try:
                popup.setOutsideTouchable(True)
                popup.setFocusable(True)
            except Exception:
                pass

            plugin_ref = self

            def _toggle(_v=None):
                try:
                    nv = not bool(plugin_ref.get_setting("header_cover_enabled", True))
                    plugin_ref.set_setting("header_cover_enabled", bool(nv))
                    if bool(nv):
                        try:
                            plugin_ref._start_header_cover_worker()
                        except Exception:
                            pass
                    else:
                        try:
                            plugin_ref._stop_header_cover_worker()
                        except Exception:
                            pass
                        try:
                            def _hide_cover_now():
                                try:
                                    cv = getattr(plugin_ref, "_header_cover_view", None)
                                    if cv:
                                        cv.setVisibility(View.GONE)
                                except Exception:
                                    pass
                                try:
                                    gv = getattr(plugin_ref, "_header_cover_gif_view", None)
                                    if gv:
                                        gv.setVisibility(View.GONE)
                                except Exception:
                                    pass
                            run_on_ui_thread(_hide_cover_now)
                        except Exception:
                            pass
                    try:
                        plugin_ref._apply_header_cover_settings_consistency()
                    except Exception:
                        pass
                    try:
                        plugin_ref.reload_settings()
                    except Exception:
                        pass
                    try:
                        plugin_ref._refresh_header_action_icons()
                    except Exception:
                        pass
                except Exception:
                    pass
                try:
                    popup.dismiss()
                except Exception:
                    pass

            try:
                row.setOnClickListener(OnClickListener(_toggle))
            except Exception:
                pass

            try:
                if Build.VERSION.SDK_INT >= 19:
                    popup.showAsDropDown(anchor_view, 0, AndroidUtilities.dp(8), Gravity.START)
                else:
                    popup.showAsDropDown(anchor_view, 0, AndroidUtilities.dp(8))
                self._home_cover_quick_popup = popup
            except Exception:
                try:
                    popup.showAsDropDown(anchor_view)
                    self._home_cover_quick_popup = popup
                except Exception:
                    pass
        except Exception:
            pass
    def _get_tab_source_options(self):
        sources = []
        labels = []
        try:
            if self._has_spotify_credentials():
                sources.append("spotify")
                labels.append("Spotify")
        except Exception:
            pass
        try:
            lastfm_user = str(self.get_setting("lastfm_user", self.get_setting("lastfm_username", ""))).strip()
            lastfm_key = str(self.get_setting("lastfm_api_key", "")).strip()
            if lastfm_user and lastfm_key:
                sources.append("lastfm")
                labels.append("Last.fm")
        except Exception:
            pass
        try:
            stats_user = str(self.get_setting("statsfm_username", "")).strip()
            if stats_user:
                sources.append("statsfm")
                labels.append("Stats.fm")
        except Exception:
            pass
        try:
            ym_token = str(self.get_setting("ymusic_api_token", "") or "").strip()
            if ym_token:
                sources.append("ymusic")
                labels.append("Yandex Music")
        except Exception:
            pass
        if not sources:
            sources = ["spotify"]
            labels = ["Spotify"]
        return sources, labels

    def _send_now_playing_card_for_tab(self):
        try:
            sources, labels = self._get_tab_source_options()
            idx = int(self.get_setting("nowfy_tab_source", 0))
            if idx < 0 or idx >= len(sources):
                idx = 0
            source_key = sources[idx]
            self._send_now_playing_card_with_source(source_key)
        except Exception as e:
            log(f"[Nowfy] Tab send error: {e}")
            try:
                self._tab_feedback_done = True
            except Exception:
                pass

    def _send_now_playing_card_with_source(self, source_key):
        try:
            try:
                self._telemetry_track_source(source_key)
            except Exception:
                pass
            source_map = {
                "spotify": self.get_setting("custom_command", ".now"),
                "lastfm": ".fm",
                "statsfm": ".stats",
                "ymusic": ".ymusic"
            }
            command = source_map.get(source_key, ".now")
            self._last_overlay_trigger_command = command
            fragment = get_last_fragment()
            if not fragment:
                try:
                    self._tab_feedback_done = True
                except Exception:
                    pass
                return
            dialog_id = fragment.getDialogId()
            if not dialog_id:
                try:
                    self._tab_feedback_done = True
                except Exception:
                    pass
                return
            try:
                force_spotify = (source_key == "spotify")
                params = self._build_send_params_for_dialog(dialog_id)
                if params and self._try_send_precard(params, source_key, force_spotify=force_spotify):
                    return
            except Exception:
                pass
            # Yandex path should never leak a literal ".ymusic" message in chat.
            # If pre-card failed, show local feedback and stop here.
            if str(source_key or "").strip().lower() == "ymusic":
                try:
                    run_on_ui_thread(lambda: BulletinHelper.show_info(tr("no_track_ymusic") if "no_track_ymusic" in TRANSLATIONS else tr("nowfy_tab_status_no_track")))
                except Exception:
                    pass
                try:
                    self._tab_feedback_done = True
                except Exception:
                    pass
                return
            def send_command():
                try:
                    send_helper = get_send_messages_helper()
                    from org.telegram.messenger import SendMessagesHelper
                    def _do_send():
                        try:
                            send_helper.sendMessage(
                                SendMessagesHelper.SendMessageParams.of(
                                    command,
                                    dialog_id
                                )
                            )
                        except Exception as e:
                            log(f"[Nowfy] Tab command send failed: {e}")
                            try:
                                self._tab_feedback_done = True
                            except Exception:
                                pass
                    run_on_ui_thread(_do_send)
                except Exception as e:
                    log(f"[Nowfy] Tab command queue failed: {e}")
                    try:
                        self._tab_feedback_done = True
                    except Exception:
                        pass
            run_on_queue(send_command)
        except Exception as e:
            log(f"[Nowfy] Tab source send error: {e}")
            try:
                self._tab_feedback_done = True
            except Exception:
                pass

    def _open_tab_share_preview(self):
        try:
            fragment = get_last_fragment()
            if not isinstance(fragment, ChatActivity):
                try:
                    fragment = getattr(self, "_chat_fab_fragment", None)
                except Exception:
                    fragment = None
            if not isinstance(fragment, ChatActivity):
                try:
                    fragment = getattr(self, "_preview_fragment_hint", None)
                except Exception:
                    fragment = None
            if not isinstance(fragment, ChatActivity):
                try:
                    run_on_ui_thread(lambda: BulletinHelper.show_info(tr("tab_preview_unavailable")))
                except Exception:
                    pass
                return
            try:
                theme = int(self.get_setting("theme_selector", 0) or 0)
            except Exception:
                theme = 0
            try:
                _ext, _sp, _vi, _nv, _ca, _cfm, _legacy_min = self._get_theme_indices()
            except Exception:
                pass
            if False:
                self._show_spotify_info_bottom_sheet(
                    "Preview",
                    None,
                    tr("tab_preview_compact_message"),
                    tr("spotify_control_understood"),
                    None
                )
                return
            run_on_ui_thread(
                lambda: BulletinHelper.show_success(
                    tr("tab_preview_preparing")
                )
            )
            threading.Thread(target=self._build_tab_share_preview, daemon=True).start()
        except Exception as e:
            log(f"[Nowfy] Tab preview open failed: {e}")

    def _build_tab_share_preview(self):
        try:
            def _is_valid_preview_path(path_value):
                try:
                    if not path_value:
                        return False
                    if not isinstance(path_value, str):
                        return False
                    pv = path_value.strip()
                    if not pv or pv in ("True", "False", "None"):
                        return False
                    f = File(pv)
                    return f.exists() and f.isFile()
                except Exception:
                    return False
            sources, _labels = self._get_tab_source_options()
            try:
                idx = int(self.get_setting("nowfy_tab_source", 0) or 0)
            except Exception:
                idx = 0
            if idx < 0 or idx >= len(sources):
                idx = 0
            source_key = sources[idx]
            force_spotify = (source_key == "spotify")
            is_fm_command = (source_key == "lastfm")
            snapshot = self._get_now_playing_snapshot(preferred_source=source_key, allow_cached=True)
            if not snapshot or not snapshot.get("track"):
                run_on_ui_thread(lambda: BulletinHelper.show_info(tr("nowfy_tab_status_no_track")))
                return
            track = self._prepare_track_for_send(snapshot.get("track"))
            progress_ms = snapshot.get("progress_ms", 0)
            temp_path = None
            try:
                track_key = self._make_track_key(source_key, track)
                entry = self._get_precard_entry(source_key)
                if entry and entry.get("path") and entry.get("track_key") == track_key:
                    temp_path = entry.get("path")
            except Exception:
                temp_path = None
            if not _is_valid_preview_path(temp_path):
                temp_path = None
            if not temp_path:
                original_forced_player = getattr(self, "_forced_player", None)
                try:
                    if source_key == "lastfm":
                        self._forced_player = "FM"
                    elif source_key == "statsfm":
                        try:
                            stats_source = int(self.get_setting("statsfm_source_player", 0) or 0)
                        except Exception:
                            stats_source = 0
                        self._forced_player = "Apple Music" if stats_source == 1 else "Spotify"
                    elif source_key == "spotify":
                        self._forced_player = "Spotify"
                    elif source_key == "ymusic":
                        self._forced_player = "Yandex Music"
                    temp_path = self._generate_card(track, None, progress_ms, force_spotify=force_spotify, etg_cover_image=None, is_fm_command=is_fm_command)
                finally:
                    if original_forced_player is not None:
                        self._forced_player = original_forced_player
                    else:
                        if hasattr(self, "_forced_player"):
                            try:
                                delattr(self, "_forced_player")
                            except Exception:
                                pass
                if not _is_valid_preview_path(temp_path):
                    temp_path = None
            if not temp_path:
                try:
                    _ext, spotlight_index, vinni_index, nowv_index, card_index, _legacy_theme_a, _legacy_theme_b = self._get_theme_indices()
                except Exception:
                    spotlight_index, vinni_index, nowv_index, card_index = 1, 2, 3, 4
                try:
                    theme = int(self.get_setting("theme_selector", 0) or 0)
                except Exception:
                    theme = 0
                original_forced_player = getattr(self, "_forced_player", None)
                try:
                    if source_key == "lastfm":
                        self._forced_player = "FM"
                    elif source_key == "statsfm":
                        try:
                            stats_source = int(self.get_setting("statsfm_source_player", 0) or 0)
                        except Exception:
                            stats_source = 0
                        self._forced_player = "Apple Music" if stats_source == 1 else "Spotify"
                    elif source_key == "spotify":
                        self._forced_player = "Spotify"
                    elif source_key == "ymusic":
                        self._forced_player = "Yandex Music"
                    if theme == 0:
                        temp_path = self._generate_apple_unified_card(track, None, progress_ms, force_spotify=force_spotify, etg_cover_image=None)
                    elif theme == spotlight_index:
                        temp_path = self._generate_spotlight_card(track, None, progress_ms, force_spotify=force_spotify, etg_cover_image=None)
                    elif theme == vinni_index:
                        temp_path = self._generate_vinni_card(track, None, progress_ms, force_spotify=force_spotify, etg_cover_image=None, is_fm_command=is_fm_command)
                    elif theme == nowv_index:
                        temp_path = self._generate_nowv_card(track, None, progress_ms, force_spotify=force_spotify, etg_cover_image=None, is_fm_command=is_fm_command)
                    elif theme == card_index:
                        temp_path = self._generate_card_theme_card(track, None, progress_ms, force_spotify=force_spotify, etg_cover_image=None, is_fm_command=is_fm_command)
                finally:
                    if original_forced_player is not None:
                        self._forced_player = original_forced_player
                    else:
                        if hasattr(self, "_forced_player"):
                            try:
                                delattr(self, "_forced_player")
                            except Exception:
                                pass
                if not _is_valid_preview_path(temp_path):
                    temp_path = None
            if not temp_path:
                run_on_ui_thread(lambda: BulletinHelper.show_info(tr("preview_build_failed")))
                return
            run_on_ui_thread(lambda: self._show_tab_preview_sheet(temp_path, track, source_key, force_spotify))
        except Exception as e:
            log(f"[Nowfy] Tab preview build failed: {e}")

    def _show_tab_preview_sheet(self, image_path, track, source_key, force_spotify):
        try:
            fragment = get_last_fragment()
            if not isinstance(fragment, ChatActivity):
                try:
                    fragment = getattr(self, "_chat_fab_fragment", None)
                except Exception:
                    fragment = None
            if not isinstance(fragment, ChatActivity):
                try:
                    fragment = getattr(self, "_preview_fragment_hint", None)
                except Exception:
                    fragment = None
            if not isinstance(fragment, ChatActivity):
                try:
                    BulletinHelper.show_info(tr("tab_preview_unavailable"))
                except Exception:
                    pass
                return
            ctx = fragment.getParentActivity() if fragment and fragment.getParentActivity() else ApplicationLoader.applicationContext
            if not ctx:
                return
            from org.telegram.ui.ActionBar import BottomSheet, Theme
            from org.telegram.ui.Components import LayoutHelper
            from android.widget import LinearLayout, TextView, ImageView
            from android.view import Gravity, View
            from android.util import TypedValue
            from android.graphics.drawable import GradientDrawable
            from android_utils import OnClickListener
            sheet = BottomSheet(ctx, True)
            root = LinearLayout(ctx)
            root.setOrientation(LinearLayout.VERTICAL)
            try:
                root.setPadding(AndroidUtilities.dp(18), AndroidUtilities.dp(18), AndroidUtilities.dp(18), AndroidUtilities.dp(14))
            except Exception:
                pass
            title_view = TextView(ctx)
            title_view.setText("Preview")
            title_view.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 20)
            title_view.setGravity(Gravity.START)
            try:
                title_view.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                title_view.setTextColor(0xFFFFFFFF)
            root.addView(title_view, LayoutHelper.createLinear(-1, -2))
            sub = TextView(ctx)
            sub.setText(tr("tab_preview_subtext"))
            sub.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
            sub.setGravity(Gravity.START)
            try:
                sub.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            except Exception:
                sub.setTextColor(0xFFD0D6E0)
            try:
                sub.setPadding(0, AndroidUtilities.dp(2), 0, AndroidUtilities.dp(10))
            except Exception:
                pass
            root.addView(sub, LayoutHelper.createLinear(-1, -2))
            card = ImageView(ctx)
            try:
                card.setScaleType(ImageView.ScaleType.FIT_CENTER)
                card.setAdjustViewBounds(True)
            except Exception:
                pass
            preview_display_path = image_path
            try:
                try:
                    src_path = str(image_path) if image_path else None
                    if src_path and os.path.isfile(src_path):
                        temp_dir = File(ApplicationLoader.getFilesDirFixed(), "exteraFy/preview")
                        if not temp_dir.exists():
                            temp_dir.mkdirs()
                        rounded_name = f"preview_round_{hashlib.md5(src_path.encode()).hexdigest()}.png"
                        rounded_path = File(temp_dir, rounded_name).getAbsolutePath()
                        try:
                            src_mtime = int(os.path.getmtime(src_path))
                        except Exception:
                            src_mtime = 0
                        need_regen = True
                        try:
                            if os.path.exists(rounded_path):
                                rounded_mtime = int(os.path.getmtime(rounded_path))
                                need_regen = rounded_mtime < src_mtime
                        except Exception:
                            need_regen = True
                        if need_regen:
                            try:
                                pimg = Image.open(src_path).convert("RGBA")
                                mask = Image.new("L", pimg.size, 0)
                                mdraw = ImageDraw.Draw(mask)
                                radius = max(18, int(min(pimg.size) * 0.04))
                                mdraw.rounded_rectangle((0, 0, pimg.size[0], pimg.size[1]), radius=radius, fill=255)
                                pimg.putalpha(mask)
                                pimg.save(rounded_path, format="PNG", optimize=True, compress_level=2)
                            except Exception:
                                rounded_path = src_path
                        preview_display_path = rounded_path
                except Exception:
                    preview_display_path = image_path
                bmp = BitmapFactory.decodeFile(str(preview_display_path))
                if bmp:
                    card.setImageBitmap(bmp)
            except Exception:
                pass
            frame_bg = GradientDrawable()
            frame_bg.setCornerRadius(AndroidUtilities.dp(16))
            try:
                frame_bg.setColor(Theme.getColor(Theme.key_dialogBackground))
                frame_bg.setStroke(AndroidUtilities.dp(1), Theme.getColor(Theme.key_windowBackgroundWhiteGrayText4))
            except Exception:
                frame_bg.setColor(0x221A1F2E)
                frame_bg.setStroke(AndroidUtilities.dp(1), 0x553C4A6A)
            card.setBackground(frame_bg)
            try:
                card.setPadding(AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6))
            except Exception:
                pass
            root.addView(card, LayoutHelper.createLinear(-1, -2, Gravity.TOP, 0, 0, 0, 0))
            btn = TextView(ctx)
            btn.setText(tr("tab_preview_share_button"))
            btn.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
            btn.setGravity(Gravity.CENTER)
            try:
                btn.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(10), AndroidUtilities.dp(16), AndroidUtilities.dp(10))
            except Exception:
                pass
            try:
                bg = GradientDrawable()
                bg.setCornerRadius(AndroidUtilities.dp(20))
                try:
                    bg.setColor(Theme.getColor(Theme.key_featuredStickers_addButton))
                except Exception:
                    bg.setColor(0xFF2B7FFF)
                try:
                    bg.setStroke(AndroidUtilities.dp(2), Theme.getColor(Theme.key_dialogTextBlue))
                except Exception:
                    bg.setStroke(AndroidUtilities.dp(2), 0xFF8FC1FF)
                btn.setBackground(bg)
                try:
                    btn.setTextColor(Theme.getColor(Theme.key_featuredStickers_buttonText))
                except Exception:
                    btn.setTextColor(0xFFFFFFFF)
            except Exception:
                pass
            def _share_click(v):
                try:
                    frag = get_last_fragment()
                    dialog_id = frag.getDialogId() if frag else 0
                    params = self._build_send_params_for_dialog(dialog_id) if dialog_id else None
                    if params:
                        def _send():
                            original_forced_player = getattr(self, "_forced_player", None)
                            try:
                                if source_key == "lastfm":
                                    self._forced_player = "FM"
                                elif source_key == "statsfm":
                                    try:
                                        stats_source = int(self.get_setting("statsfm_source_player", 0) or 0)
                                    except Exception:
                                        stats_source = 0
                                    self._forced_player = "Apple Music" if stats_source == 1 else "Spotify"
                                elif source_key == "spotify":
                                    self._forced_player = "Spotify"
                                elif source_key == "ymusic":
                                    self._forced_player = "Yandex Music"
                                self._send_card_with_caption(params, image_path, track, force_spotify=force_spotify, skip_compact=True)
                            finally:
                                if original_forced_player is not None:
                                    self._forced_player = original_forced_player
                                else:
                                    if hasattr(self, "_forced_player"):
                                        try:
                                            delattr(self, "_forced_player")
                                        except Exception:
                                            pass
                        run_on_queue(_send)
                except Exception:
                    pass
                try:
                    sheet.dismiss()
                except Exception:
                    pass
            btn.setOnClickListener(OnClickListener(_share_click))
            root.addView(btn, LayoutHelper.createLinear(-1, -2, Gravity.TOP, 0, AndroidUtilities.dp(14), 0, 0))
            sheet.setCustomView(root)
            run_on_ui_thread(sheet.show)
        except Exception as e:
            log(f"[Nowfy] Tab preview sheet error: {e}")

    def _send_tab_music_preview_from_statsfm(self):
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "send_tab_music_preview"):
                NOWFY_CORE_API.send_tab_music_preview(self)
                return
        except Exception:
            pass
        try:
            run_on_ui_thread(lambda: BulletinHelper.show_info(
                tr("tab_music_preview_send_failed")
            ))
        except Exception:
            pass

    def _send_tab_share_lyrics_from_tab(self):
        try:
            fragment = get_last_fragment()
            if not fragment:
                try:
                    run_on_ui_thread(lambda: BulletinHelper.show_info(tr("nowfy_tab_status_no_permission")))
                except Exception:
                    pass
                return
            dialog_id = 0
            try:
                dialog_id = int(fragment.getDialogId() or 0)
            except Exception:
                dialog_id = 0
            if dialog_id == 0:
                try:
                    run_on_ui_thread(lambda: BulletinHelper.show_info(tr("nowfy_tab_status_no_permission")))
                except Exception:
                    pass
                return
            def _send():
                try:
                    send_helper = get_send_messages_helper()
                    from org.telegram.messenger import SendMessagesHelper
                    def _do_send():
                        try:
                            send_helper.sendMessage(
                                SendMessagesHelper.SendMessageParams.of(
                                    "!share",
                                    dialog_id
                                )
                            )
                        except Exception:
                            try:
                                BulletinHelper.show_info(tr("share_lyrics_error") if "share_lyrics_error" in TRANSLATIONS else "Failed to generate lyrics card.")
                            except Exception:
                                pass
                    run_on_ui_thread(_do_send)
                except Exception:
                    try:
                        run_on_ui_thread(lambda: BulletinHelper.show_info(tr("share_lyrics_error") if "share_lyrics_error" in TRANSLATIONS else "Failed to generate lyrics card."))
                    except Exception:
                        pass
            run_on_queue(_send)
        except Exception:
            try:
                run_on_ui_thread(lambda: BulletinHelper.show_info(tr("share_lyrics_error") if "share_lyrics_error" in TRANSLATIONS else "Failed to generate lyrics card."))
            except Exception:
                pass

    def _get_spotify_music_preview_info(self):
        return None

    def _get_statsfm_music_preview_info(self, username):
        return None

    def _get_statsfm_spotify_preview_info(self, username):
        return None

    def _download_statsfm_preview_audio(self, preview_url, title, artist):
        return None

    def _send_preview_audio_to_chat(self, file_path, title=None):
        return False

    def _toggle_dynamic_island_overlay(self, enabled):
        return None

    def _toggle_mini_control(self, enabled, persist=True):
        return None

    def _update_frame_corners(self):
        return None

    def _toggle_send_button(self, enabled, persist=True):
        try:
            if bool(persist):
                self.set_setting("send_button_enabled", bool(enabled))
            try:
                btn = getattr(self, "_di_btn_send", None)
                if btn is not None:
                    btn.setVisibility(0 if bool(enabled) else 8)
            except Exception:
                pass
        except Exception as e:
            log(f"[Nowfy] Send button toggle error: {e}")

    def _toggle_search_button(self, enabled, persist=True):
        try:
            if bool(persist):
                self.set_setting("search_button_enabled", bool(enabled))
            try:
                btn = getattr(self, "_di_btn_search", None)
                if btn is not None:
                    btn.setVisibility(0 if bool(enabled) else 8)
            except Exception:
                pass
        except Exception as e:
            log(f"[Nowfy] Search button toggle error: {e}")

    def _create_dynamic_island_view(self, ctx):
        return None

    def _sync_cover_style(self, style_idx, is_pill=False):
        try:
            if not hasattr(self, '_di_cover') or not self._di_cover:
                return
            from android.graphics.drawable import GradientDrawable
            ctx = ApplicationLoader.applicationContext
            cover_bg = GradientDrawable()
            cover_bg.setShape(GradientDrawable.RECTANGLE)
            cover_bg.setColor(0x00000000)
            if style_idx == 1:
                if is_pill:
                    radius = AndroidUtilities.dp(14) if AndroidUtilities else int(ctx.getResources().getDisplayMetrics().density * 14)
                else:
                    radius = AndroidUtilities.dp(26) if AndroidUtilities else int(ctx.getResources().getDisplayMetrics().density * 26)
                cover_bg.setCornerRadius(float(radius))
            else:
                if is_pill:
                    radius = AndroidUtilities.dp(8) if AndroidUtilities else int(ctx.getResources().getDisplayMetrics().density * 8)
                else:
                    radius = AndroidUtilities.dp(10) if AndroidUtilities else int(ctx.getResources().getDisplayMetrics().density * 10)
                cover_bg.setCornerRadius(float(radius))
            try:
                self._di_cover.setBackground(cover_bg)
                self._di_cover.setClipToOutline(True)
            except Exception:
                pass
        except Exception:
            pass

    def _get_default_island_y(self, ctx):
        try:
            res = ctx.getResources()
            res_id = res.getIdentifier("status_bar_height", "dimen", "android")
            sb_height = 0
            if res_id and res_id > 0:
                sb_height = int(res.getDimensionPixelSize(res_id))
        except Exception:
            sb_height = 0
        try:
            if bool(self.get_setting('on_notch_enabled', False)):
                offset_dp = -5
                margin = AndroidUtilities.dp(offset_dp) if AndroidUtilities else int(ctx.getResources().getDisplayMetrics().density * offset_dp)
            else:
                margin = AndroidUtilities.dp(12) if AndroidUtilities else int(ctx.getResources().getDisplayMetrics().density * 12)
        except Exception:
            margin = int(ctx.getResources().getDisplayMetrics().density * -5) if bool(self.get_setting('on_notch_enabled', False)) else int(ctx.getResources().getDisplayMetrics().density * 12)
        try:
            base = max(0, sb_height) + margin
            if base < 0:
                base = max(0, sb_height // 2)
            return int(base)
        except Exception:
            return margin if margin > 0 else 0

    def _reposition_dynamic_island_to_notch(self):
        return False

    def _start_dynamic_island_overlay(self):
        return None

    def _stop_dynamic_island_overlay(self):
        return None

    def _is_pop_island_allowed(self, allow_bulletin=False):
        return False

    def _safe_start_dynamic_island_overlay(self):
        return None

    def _start_dynamic_island_refresh(self):
        return None

    def _update_dynamic_island_content(self, track_data):
        return None

    def _apply_pop_style_to_overlay(self):
        return None

    def _apply_island_style_to_overlay(self):
        return None

    def _apply_default_island_background(self, frame, GD, Color, AndroidUtilities):
        return None

    def _apply_bg_cover_island_background(self, frame, GD, Color, BitmapDrawable, AndroidUtilities):
        return None

    def _apply_no_blur_island_background(self, frame, GD, Color, BitmapDrawable, AndroidUtilities):
        return None

    def _apply_pure_island_background(self, frame, GD, Color, AndroidUtilities):
        return None

    def _apply_blur_and_darken(self, bitmap):
        return bitmap

    def _apply_mini_control_backdrop_blur(self, mini_controls, ctx):
        return None

    def _apply_simple_blur_mini_control(self, bitmap, radius):
        try:
            if bitmap is None:
                return bitmap
            r = int(radius or 0)
            if r <= 0:
                return bitmap
            ByteArrayOutputStream = jclass("java.io.ByteArrayOutputStream")
            BitmapFactoryLocal = jclass("android.graphics.BitmapFactory")
            BitmapCls = jclass("android.graphics.Bitmap")
            stream = ByteArrayOutputStream()
            ok = bitmap.compress(BitmapCls.CompressFormat.PNG, 100, stream)
            if not ok:
                return bitmap
            data = bytes(stream.toByteArray())
            if not data:
                return bitmap
            from io import BytesIO
            img = Image.open(BytesIO(data)).convert("RGBA")
            blur_radius = max(1.0, min(32.0, float(r) * 0.72))
            img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            out_buf = BytesIO()
            img.save(out_buf, format="PNG")
            out_data = out_buf.getvalue()
            if not out_data:
                return bitmap
            return BitmapFactoryLocal.decodeByteArray(out_data, 0, len(out_data)) or bitmap
        except Exception:
            return bitmap

    def _apply_control_style_to_overlay(self):
        return None

    def _runtime_guard_enabled(self):
        try:
            conf = jclass("com.exteragram.messenger.ExteraConfig")
            flag = getattr(conf, "pluginsSafeMode", None)
            if flag is None:
                try:
                    flag = conf.getPluginsSafeMode()
                except Exception:
                    flag = False
            return bool(flag)
        except Exception:
            return False
    def on_setting_changed(self, key, value):
        if key == "show_chat_menu":
            self.remove_menu_items()
            self._add_menu_items()
        elif key == "nowcast_enabled":
            if not self._core_addon_enabled("addon_nowcast_enabled", False):
                try:
                    if bool(value):
                        self.set_setting("nowcast_enabled", False)
                        BulletinHelper.show_info("NowCast addon not installed")
                except Exception:
                    pass
                return
            try:
                self._apply_addon_runtime_patches()
            except Exception:
                pass
            try:
                if hasattr(self, "_on_nowcast_toggle"):
                    self._on_nowcast_toggle(bool(value))
            except Exception:
                pass

    def _ensure_core_ready_with_retry(self, attempts=120, sleep_sec=0.2):
        global nowfycore, NOWFY_CORE_API, NOWFY_CORE_IMPORT_ERROR, NOWFY_CORE_BACKEND_MIXIN
        last_error = NOWFY_CORE_IMPORT_ERROR
        for i in range(max(1, int(attempts))):
            try:
                if nowfycore is not None:
                    NOWFY_CORE_BACKEND_MIXIN = getattr(nowfycore, "NowfyCoreBackendMixin", NOWFY_CORE_BACKEND_MIXIN)
                if nowfycore is not None and hasattr(nowfycore, "attach_host_plugin"):
                    try:
                        nowfycore.attach_host_plugin(self)
                    except Exception:
                        pass
                if nowfycore is not None and hasattr(nowfycore, "get_nowfy_core_api"):
                    NOWFY_CORE_API = nowfycore.get_nowfy_core_api()
                core_active = False
                if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "is_core_active"):
                    core_active = bool(NOWFY_CORE_API.is_core_active())
                if not core_active and nowfycore is not None:
                    core_active = bool(
                        hasattr(nowfycore, "NowfyCore")
                        and getattr(nowfycore.NowfyCore, "instance", None) is not None
                    )
                if not core_active and nowfycore is not None:
                    try:
                        inst = getattr(getattr(nowfycore, "NowfyCore", None), "instance", None)
                        core_active = bool(inst is not None and getattr(inst, "api", None) is not None)
                    except Exception:
                        pass
                if core_active:
                    NOWFY_CORE_IMPORT_ERROR = None
                    try:
                        self.core = NowfyCore(self)
                    except Exception:
                        self.core = None
                    return True, None
                last_error = Exception("NowfyCore not active yet")
            except Exception as e:
                last_error = e
            try:
                time.sleep(float(sleep_sec))
            except Exception:
                pass
        return False, last_error

    def _bind_core_backend_methods_if_needed(self):
        try:
            global nowfycore
            if not nowfycore or not hasattr(nowfycore, "NowfyCoreBackendMixin"):
                return 0
            mixin = nowfycore.NowfyCoreBackendMixin
            cls = self.__class__
            added = 0
            for name, member in getattr(mixin, "__dict__", {}).items():
                if not name or name.startswith("__"):
                    continue
                if not callable(member):
                    continue
                if hasattr(cls, name):
                    continue
                setattr(cls, name, member)
                added += 1
            return added
        except Exception:
            return 0

    def _stats_enabled(self):
        try:
            return bool(self.get_setting("nowfy_stats_enabled", True))
        except Exception:
            return True

    def _load_telemetry_queue(self):
        try:
            raw = self.get_setting("nowfy_stats_queue_v1", "[]")
            arr = json.loads(str(raw or "[]"))
            self._telemetry_queue = arr if isinstance(arr, list) else []
        except Exception:
            self._telemetry_queue = []

    def _save_telemetry_queue(self):
        try:
            self.set_setting("nowfy_stats_queue_v1", json.dumps(list(self._telemetry_queue or []), ensure_ascii=True, separators=(",", ":")))
        except Exception:
            pass

    def _telemetry_install_id_get(self):
        try:
            if self._telemetry_install_id:
                return str(self._telemetry_install_id)
            cached = str(self.get_setting("nowfy_stats_install_id", "") or "").strip()
            if cached:
                self._telemetry_install_id = cached
                return cached
            sid = "nowfy_{0:x}{1:x}".format(int(time.time() * 1000), random.randint(0, 0xFFFFFF))
            self.set_setting("nowfy_stats_install_id", sid)
            self._telemetry_install_id = sid
            return sid
        except Exception:
            return "nowfy_unknown"

    def _telemetry_app_snapshot(self):
        out = {
            "app_id": "unknown",
            "app_variant": "unknown",
            "app_version": "unknown",
            "plugin_version": str(__version__),
            "mode": "nowfy",
        }
        try:
            ctx = ApplicationLoader.applicationContext
            if ctx is None:
                return out
            pkg = str(ctx.getPackageName() or "unknown").strip() or "unknown"
            out["app_id"] = pkg
            low = pkg.lower()
            if "ayu" in low:
                out["app_variant"] = "ayugram"
            elif "extera" in low:
                out["app_variant"] = "exteragram"
            else:
                out["app_variant"] = "telegram_mod"
            try:
                pm = ctx.getPackageManager()
                pi = pm.getPackageInfo(pkg, 0)
                out["app_version"] = str(getattr(pi, "versionName", "") or getattr(pi, "versionCode", "unknown"))
            except Exception:
                pass
        except Exception:
            pass
        return out

    def _telemetry_slug(self, value):
        try:
            s = str(value or "").strip().lower()
            s = re.sub(r"[^a-z0-9]+", "_", s)
            s = re.sub(r"_+", "_", s).strip("_")
            return s or "unknown"
        except Exception:
            return "unknown"

    def _telemetry_queue_event(self, event_name, feature=None, count=1, force_flush=False):
        try:
            if not self._stats_enabled():
                return
            item = {
                "ts": int(time.time()),
                "event": str(event_name or "").strip(),
                "feature": str(feature or "").strip(),
                "count": max(1, int(count or 1)),
            }
            if not item["event"]:
                return
            with self._telemetry_lock:
                q = list(self._telemetry_queue or [])
                q.append(item)
                if len(q) > 300:
                    q = q[-300:]
                self._telemetry_queue = q
            self._save_telemetry_queue()
            now_ts = int(time.time())
            if force_flush or (now_ts - int(self._telemetry_last_flush_ts or 0) >= 20):
                self._telemetry_flush_async()
        except Exception:
            pass

    def _telemetry_flush_async(self):
        try:
            if not self._stats_enabled():
                return
            with self._telemetry_lock:
                if self._telemetry_sending:
                    return
                queue = list(self._telemetry_queue or [])
                if not queue:
                    return
                self._telemetry_sending = True
            payload = {
                "plugin": str(__id__),
                "install_id": self._telemetry_install_id_get(),
                "mode": "nowfy",
                "app": self._telemetry_app_snapshot(),
                "events": queue[:100],
            }

            def _worker():
                ok = False
                try:
                    ok = self._telemetry_post(payload)
                except Exception:
                    ok = False
                try:
                    with self._telemetry_lock:
                        if ok:
                            cur = list(self._telemetry_queue or [])
                            drop = len(payload.get("events") or [])
                            self._telemetry_queue = cur[drop:]
                            self._telemetry_last_flush_ts = int(time.time())
                            self._save_telemetry_queue()
                        self._telemetry_sending = False
                except Exception:
                    self._telemetry_sending = False

            threading.Thread(target=_worker, daemon=True).start()
        except Exception:
            try:
                self._telemetry_sending = False
            except Exception:
                pass

    def _telemetry_post(self, payload):
        try:
            headers = {"Content-Type": "application/json; charset=utf-8"}
            token = str(GEEKSTATS_INGEST_TOKEN or "").strip()
            if token:
                headers["x-ingest-token"] = token
            resp = requests.post(
                GEEKSTATS_INGEST_URL,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers=headers,
                timeout=8,
            )
            return bool(resp is not None and int(resp.status_code) < 300)
        except Exception:
            return False

    def _telemetry_track_cards_generated(self, track, force_spotify=False):
        try:
            if not self._stats_enabled() or not isinstance(track, dict):
                return
            title = str(track.get("name", "") or "")
            artists = ", ".join([str(a.get("name", "") or "") for a in (track.get("artists") or []) if isinstance(a, dict)])
            album = str(((track.get("album") or {}) if isinstance(track.get("album"), dict) else {}).get("name", "") or "")
            letters = len(title) + len(artists) + len(album)
            self._telemetry_queue_event("feature_use", feature="cards_generated", count=1, force_flush=False)
            if letters > 0:
                self._telemetry_queue_event("feature_use", feature="letters_generated", count=max(1, int(letters)), force_flush=False)
            player_name = "Spotify" if force_spotify else self._detect_current_player()
            if player_name:
                self._telemetry_queue_event("feature_use", feature="player_" + self._telemetry_slug(player_name), count=1, force_flush=False)
        except Exception:
            pass

    def _telemetry_track_card_sent(self):
        try:
            if self._stats_enabled():
                self._telemetry_queue_event("feature_use", feature="cards_sent", count=1, force_flush=False)
        except Exception:
            pass

    def _telemetry_track_source(self, source_key):
        try:
            if not self._stats_enabled():
                return
            source_slug = self._telemetry_slug(source_key)
            self._telemetry_queue_event("feature_use", feature="service_" + source_slug, count=1, force_flush=False)
            self._telemetry_queue_event("feature_use", feature="source_" + source_slug, count=1, force_flush=False)
            player_name = self._detect_current_player()
            if player_name:
                self._telemetry_queue_event("feature_use", feature="player_" + self._telemetry_slug(player_name), count=1, force_flush=False)
        except Exception:
            pass

    def on_plugin_load(self):
        if self._runtime_guard_enabled():
            try:
                log("[Nowfy] Plugin safe mode is enabled. Runtime hooks skipped.")
            except Exception:
                pass
            return
        core_ok, core_err = self._ensure_core_ready_with_retry()
        if not core_ok:
            raise Exception("NowfyCore must be active before loading Nowfy.") from core_err
        try:
            if nowfycore is not None and hasattr(nowfycore, "attach_host_plugin"):
                nowfycore.attach_host_plugin(self)
        except Exception:
            pass
        try:
            self._bind_core_backend_methods_if_needed()
        except Exception:
            pass
        try:
            if not hasattr(self, "_engine_install_busy"):
                self._engine_install_busy = False
            if not hasattr(self, "_engine_install_lock") or self._engine_install_lock is None:
                self._engine_install_lock = threading.Lock()
            if not hasattr(self, "_nowfy_install_busy"):
                self._nowfy_install_busy = False
            if not hasattr(self, "_nowfy_install_lock") or self._nowfy_install_lock is None:
                self._nowfy_install_lock = threading.Lock()
            if not hasattr(self, "_core_remote_dir"):
                self._core_remote_dir = None
        except Exception:
            pass
        try:
            codes = ["en", "pt", "es", "fr", "ru"]
            idx = int(self.get_setting("plugin_lang", 0))
            if 0 <= idx < len(codes):
                global _NOWFY_LANG_OVERRIDE
                _NOWFY_LANG_OVERRIDE = codes[idx]
        except Exception:
            pass
        try:
            muted = bool(self.get_setting("disable_logs", False))
            _set_log_muted(muted)
            _set_print_muted(muted)
            _apply_log_wrapper(True)
            _apply_print_wrapper(True)
        except Exception:
            pass
        try:
            self._load_telemetry_queue()
            if self._stats_enabled():
                snap = self._telemetry_app_snapshot()
                sig = "{0}|{1}|{2}|{3}".format(
                    str(__version__),
                    str(snap.get("app_id", "unknown")),
                    str(snap.get("app_variant", "unknown")),
                    str(snap.get("app_version", "unknown")),
                )
                self._telemetry_queue_event("session_start", feature="", count=1, force_flush=True)
                prev = str(self.get_setting("nowfy_stats_install_signature_v1", "") or "").strip()
                if prev != sig:
                    self.set_setting("nowfy_stats_install_signature_v1", sig)
                    self._telemetry_queue_event("install", feature="", count=1, force_flush=True)
        except Exception:
            pass
        try:
            self._font_picker_active = False
            if not hasattr(self, "_font_picker_request"):
                self._font_picker_request = 10901
        except Exception:
            pass
        addon_track_hub_enabled = self._core_addon_enabled("addon_track_hub_enabled", False)
        addon_nowcast_enabled = self._core_addon_enabled("addon_nowcast_enabled", False)
        addon_bio_enabled = self._core_addon_enabled("addon_bio_features_enabled", False)
        addon_nowbox_enabled = self._core_addon_enabled("addon_nowbox_enabled", False)
        self.add_on_send_message_hook()
        if not addon_nowcast_enabled:
            try:
                if bool(self.get_setting("nowcast_enabled", False)):
                    self.set_setting("nowcast_enabled", False)
                self._nowcast_worker_running = False
            except Exception:
                pass
        if not addon_bio_enabled:
            try:
                self._stop_bio_update = True
            except Exception:
                pass
        if not addon_track_hub_enabled:
            try:
                if bool(self.get_setting("track_hub_enabled", False)):
                    self.set_setting("track_hub_enabled", False)
                self._stop_track_hub_worker()
                self._remove_track_hub_profile_hooks()
            except Exception:
                pass
        if not addon_nowbox_enabled:
            try:
                if bool(self.get_setting("hooking_enabled", False)):
                    self.set_setting("hooking_enabled", False)
                self._stop_hooking_worker()
            except Exception:
                pass
        run_on_queue(lambda: self._finish_on_plugin_load_async(addon_track_hub_enabled, addon_nowcast_enabled, addon_bio_enabled, addon_nowbox_enabled))

    def _finish_on_plugin_load_async(self, addon_track_hub_enabled, addon_nowcast_enabled, addon_bio_enabled, addon_nowbox_enabled):
        try:
            self._start_cache_system()
        except Exception:
            pass
        try:
            self._preload_header_fallback_covers()
        except Exception:
            pass
        try:
            self._configurar_hook_cabecalho()
        except Exception:
            pass
        if addon_track_hub_enabled:
            try:
                self._setup_track_hub_profile_hooks()
            except Exception:
                pass
        try:
            self._add_menu_items()
        except Exception:
            pass
        try:
            self._apply_addon_runtime_patches()
        except Exception:
            pass
        try:
            if bool(self.get_setting("nowfy_drawer_enabled", True)):
                self._ensure_nowfy_drawer_item()
        except Exception as _e:
            log(f"[Nowfy] Failed to add Nowfy drawer item: {_e}")
        try:
            run_on_ui_thread(lambda: self._sync_home_actionbar_shortcut(get_last_fragment()))
        except Exception:
            pass
        if addon_nowcast_enabled and self.get_setting("nowcast_enabled", False):
            try:
                self._apply_addon_runtime_patches()
            except Exception:
                pass
        try:
            if bool(self.get_setting("nowplaying_pill_enabled", False)):
                try:
                    log("[Nowfy][Pulse] on_plugin_load -> start worker")
                except Exception:
                    pass
                self._start_nowplaying_pill_worker()
        except Exception as e:
            try:
                log(f"[Nowfy][Pulse] start on load failed: {e}")
            except Exception:
                pass
        try:
            self._start_header_cover_worker()
        except Exception:
            pass
        try:
            self._apply_header_cover_settings_consistency()
        except Exception:
            pass
        if addon_bio_enabled:
            try:
                self._capture_original_bio()
            except Exception:
                pass
        if addon_nowbox_enabled:
            try:
                if bool(self.get_setting("hooking_enabled", False)):
                    self._start_hooking_worker()
                    self._apply_hooking_hint_hook()
            except Exception:
                pass
        try:
            if bool(self.get_setting("nowfy_tab_enabled", True)):
                self._setup_nowfy_tab_hooks()
        except Exception:
            pass
        try:
            self._apply_chat_fab_state()
        except Exception:
            pass
        try:
            self._setup_backup_open_hook()
        except Exception:
            pass
        try:
            self._setup_drawer_refresh_hook()
        except Exception:
            pass
        try:
            self._setup_nowfysettings_inline_hook()
        except Exception:
            pass
        try:
            if addon_track_hub_enabled and bool(self.get_setting("track_hub_enabled", False)):
                self._start_track_hub_worker()
        except Exception:
            pass
        try:
            self._sanitize_theme_selector_by_core()
        except Exception:
            pass
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "maybe_show_nowfy_welcome_sheet"):
                NOWFY_CORE_API.maybe_show_nowfy_welcome_sheet(self)
        except Exception:
            pass

    def on_plugin_unload(self):
        self._stop_bio_update = True
        try:
            self._telemetry_flush_async()
        except Exception:
            pass
        if self._bio_update_thread:
            self._bio_update_thread.join(timeout=1)
        try:
            self.remove_menu_items()
        except:
            pass
        try:
            self._stop_nowplaying_pill_worker()
        except Exception:
            pass
        try:
            self._stop_header_cover_worker()
        except Exception:
            pass
        try:
            self._remove_pop_island_drawer_item()
        except Exception:
            pass
        try:
            self._remove_nowfy_drawer_item()
        except Exception:
            pass
        try:
            self._remove_nowfy_tab_hooks()
        except Exception:
            pass
        try:
            self._remove_track_hub_profile_hooks()
        except Exception:
            pass
        try:
            self._stop_track_hub_worker()
        except Exception:
            pass
        try:
            if getattr(self, "_font_picker_hook", None):
                self.unhook_method(self._font_picker_hook)
                self._font_picker_hook = None
        except Exception:
            pass
        try:
            if getattr(self, "_backup_open_hook_ref", None):
                self.unhook_method(self._backup_open_hook_ref)
                self._backup_open_hook_ref = None
        except Exception:
            pass
        try:
            self._remove_drawer_refresh_hook()
        except Exception:
            pass
        try:
            self._remove_home_actionbar_shortcut()
        except Exception:
            pass
        try:
            self._remove_chat_fab_hook()
            self._detach_chat_fab()
        except Exception:
            pass
        try:
            hooks = list(getattr(self, "_font_picker_hooks", []) or [])
            for h in hooks:
                try:
                    self.unhook_method(h)
                except Exception:
                    pass
            self._font_picker_hooks = []
        except Exception:
            pass
        try:
            self._font_picker_active = False
        except Exception:
            pass
        try:
            self._remove_nowfysettings_inline_hook()
        except Exception:
            pass

    def _setup_backup_open_hook(self):
        try:
            if getattr(self, "_backup_open_hook_ref", None):
                return
        except Exception:
            pass
        try:
            method = AndroidUtilities.getClass().getDeclaredMethod(
                "openForView",
                find_class("java.io.File"),
                find_class("java.lang.String"),
                find_class("java.lang.String"),
                find_class("android.app.Activity"),
                find_class("org.telegram.ui.ActionBar.Theme$ResourcesProvider"),
                getattr(find_class("boolean"), "TYPE", bool)
            )
            method.setAccessible(True)
            self._backup_open_hook_ref = self.hook_method(method, NowfyBackupOpenFileHook(self))
            return
        except Exception:
            pass
        try:
            methods = AndroidUtilities.getClass().getDeclaredMethods()
            for m in methods:
                try:
                    if str(m.getName()) == "openForView":
                        m.setAccessible(True)
                        self._backup_open_hook_ref = self.hook_method(m, NowfyBackupOpenFileHook(self))
                        return
                except Exception:
                    pass
        except Exception:
            pass

    def _setup_chat_fab_hook(self):
        def _resolve_method(class_name, method_name, *param_types):
            cls = None
            try:
                cls = find_class(class_name)
            except Exception:
                cls = None
            if not cls:
                return None
            try:
                m = cls.getDeclaredMethod(method_name, *param_types)
                m.setAccessible(True)
                return m
            except Exception:
                pass
            try:
                if cls is not None:
                    m = cls.getClass().getDeclaredMethod(method_name, *[p.getClass() if p is not None else p for p in param_types if p is not None])
                    m.setAccessible(True)
                    return m
            except Exception:
                pass
            try:
                methods = cls.getDeclaredMethods()
                for cand in methods:
                    try:
                        if str(cand.getName()) != str(method_name):
                            continue
                        cand.setAccessible(True)
                        return cand
                    except Exception:
                        pass
            except Exception:
                pass
            return None
        try:
            if not getattr(self, "_chat_fab_hook_ref", None):
                ctx_cls = find_class("android.content.Context")
                method = _resolve_method("org.telegram.ui.ChatActivity", "createView", ctx_cls) if ctx_cls else _resolve_method("org.telegram.ui.ChatActivity", "createView")
                if method:
                    self._chat_fab_hook_ref = self.hook_method(method, NowfyChatFabCreateViewHook(self))
                    self._trace_flow_debug("hook chat createView=ok")
                else:
                    self._trace_flow_debug("hook chat createView=missing")
        except Exception:
            self._trace_flow_debug("hook chat createView=error")
        try:
            if not getattr(self, "_chat_fab_resume_hook_ref", None):
                m_resume = _resolve_method("org.telegram.ui.ChatActivity", "onResume")
                if m_resume:
                    self._chat_fab_resume_hook_ref = self.hook_method(m_resume, NowfyChatFabResumeHook(self))
                    self._trace_flow_debug("hook chat onResume=ok")
                else:
                    self._trace_flow_debug("hook chat onResume=missing")
        except Exception:
            self._trace_flow_debug("hook chat onResume=error")
        try:
            if not getattr(self, "_chat_fab_dialogs_hook_ref", None):
                ctx_cls = find_class("android.content.Context")
                method_dialogs = _resolve_method("org.telegram.ui.DialogsActivity", "createView", ctx_cls) if ctx_cls else _resolve_method("org.telegram.ui.DialogsActivity", "createView")
                if method_dialogs:
                    self._chat_fab_dialogs_hook_ref = self.hook_method(method_dialogs, NowfyChatFabCreateViewHook(self))
                    self._trace_flow_debug("hook dialogs createView=ok")
                else:
                    self._trace_flow_debug("hook dialogs createView=missing")
        except Exception:
            self._trace_flow_debug("hook dialogs createView=error")
        try:
            if not getattr(self, "_chat_fab_dialogs_resume_hook_ref", None):
                m_resume_dialogs = _resolve_method("org.telegram.ui.DialogsActivity", "onResume")
                if m_resume_dialogs:
                    self._chat_fab_dialogs_resume_hook_ref = self.hook_method(m_resume_dialogs, NowfyChatFabResumeHook(self))
                    self._trace_flow_debug("hook dialogs onResume=ok")
                else:
                    self._trace_flow_debug("hook dialogs onResume=missing")
        except Exception:
            self._trace_flow_debug("hook dialogs onResume=error")

    def _remove_chat_fab_hook(self):
        try:
            if getattr(self, "_chat_fab_hook_ref", None):
                self.unhook_method(self._chat_fab_hook_ref)
                self._chat_fab_hook_ref = None
        except Exception:
            pass
        try:
            if getattr(self, "_chat_fab_dialogs_hook_ref", None):
                self.unhook_method(self._chat_fab_dialogs_hook_ref)
                self._chat_fab_dialogs_hook_ref = None
        except Exception:
            pass
        try:
            if getattr(self, "_chat_fab_dialogs_resume_hook_ref", None):
                self.unhook_method(self._chat_fab_dialogs_resume_hook_ref)
                self._chat_fab_dialogs_resume_hook_ref = None
        except Exception:
            pass

    def _setup_drawer_refresh_hook(self):
        try:
            if getattr(self, "_drawer_refresh_hook_ref", None):
                return
        except Exception:
            pass
        try:
            cls = find_class("org.telegram.ui.DialogsActivity")
            if not cls:
                return
            m = cls.getDeclaredMethod("onResume")
            m.setAccessible(True)
            self._drawer_refresh_hook_ref = self.hook_method(m, NowfyDrawerResumeHook(self))
        except Exception:
            pass

    def _remove_drawer_refresh_hook(self):
        try:
            if getattr(self, "_drawer_refresh_hook_ref", None):
                self.unhook_method(self._drawer_refresh_hook_ref)
                self._drawer_refresh_hook_ref = None
        except Exception:
            pass
        try:
            if getattr(self, "_chat_fab_resume_hook_ref", None):
                self.unhook_method(self._chat_fab_resume_hook_ref)
                self._chat_fab_resume_hook_ref = None
        except Exception:
            pass

    def _setup_nowfysettings_inline_hook(self):
        try:
            refs = getattr(self, "_nowfysettings_inline_hook_refs", None)
            if isinstance(refs, list) and refs:
                return
            if getattr(self, "_nowfysettings_inline_hook_ref", None):
                return
        except Exception:
            pass
        try:
            delegate_cls = find_class("org.telegram.ui.ChatActivity$ChatMessageCellDelegate")
            if delegate_cls is None:
                try:
                    log("[Nowfy][NowfySettings] ChatMessageCellDelegate not found")
                except Exception:
                    pass
                return
            methods = {}
            try:
                try:
                    declared = delegate_cls.getClass().getDeclaredMethods()
                except Exception:
                    declared = delegate_cls.getDeclaredMethods()
                methods = {repr(m): m for m in declared}
            except Exception as e:
                try:
                    log(f"[Nowfy][NowfySettings] enumerate delegate methods failed: {e}")
                except Exception:
                    pass
                return

            press = (
                methods.get(
                    "<java.lang.reflect.Method 'public void org.telegram.ui.ChatActivity$ChatMessageCellDelegate."
                    "didPressBotButton(org.telegram.ui.Cells.ChatMessageCell,org.telegram.tgnet.TLRPC$KeyboardButton)'>"
                )
                or next((m for s, m in methods.items() if "didPressBotButton" in s), None)
            )
            long_press = (
                methods.get(
                    "<java.lang.reflect.Method 'public void org.telegram.ui.ChatActivity$ChatMessageCellDelegate."
                    "didLongPressBotButton(org.telegram.ui.Cells.ChatMessageCell,org.telegram.tgnet.TLRPC$KeyboardButton)'>"
                )
                or next((m for s, m in methods.items() if "didLongPressBotButton" in s), None)
            )

            if not press:
                try:
                    log("[Nowfy][NowfySettings] didPressBotButton not found")
                except Exception:
                    pass
                return

            hooked = []
            try:
                ref = self.hook_method(
                    press,
                    NowfySettingsInlineHook(self, False),
                    priority=2147483647
                )
                if ref is not None:
                    hooked.append(ref)
            except Exception as e:
                try:
                    log(f"[Nowfy][NowfySettings] hook didPressBotButton failed: {e}")
                except Exception:
                    pass

            if long_press:
                try:
                    ref2 = self.hook_method(
                        long_press,
                        NowfySettingsInlineHook(self, True),
                        priority=2147483647
                    )
                    if ref2 is not None:
                        hooked.append(ref2)
                except Exception as e:
                    try:
                        log(f"[Nowfy][NowfySettings] hook didLongPressBotButton failed: {e}")
                    except Exception:
                        pass
            if not hooked:
                try:
                    log("[Nowfy][NowfySettings] no inline hooks installed")
                except Exception:
                    pass
                return
            self._nowfysettings_inline_hook_refs = hooked
            try:
                self._nowfysettings_inline_hook_ref = hooked[0]
            except Exception:
                self._nowfysettings_inline_hook_ref = None
            try:
                log(f"[Nowfy][NowfySettings] inline hooks={len(hooked)}")
            except Exception:
                pass
        except Exception:
            pass

    def _remove_nowfysettings_inline_hook(self):
        try:
            refs = getattr(self, "_nowfysettings_inline_hook_refs", None)
            if isinstance(refs, list):
                for ref in refs:
                    try:
                        self.unhook_method(ref)
                    except Exception:
                        pass
            self._nowfysettings_inline_hook_refs = []
            if getattr(self, "_nowfysettings_inline_hook_ref", None):
                try:
                    self.unhook_method(self._nowfysettings_inline_hook_ref)
                except Exception:
                    pass
                self._nowfysettings_inline_hook_ref = None
        except Exception:
            pass

    def _nowfysettings_is_playing(self):
        try:
            token = None
            try:
                token = self._get_access_token(show_error_bulletin=False)
            except Exception:
                token = self._get_access_token()
            if not token:
                return None
            resp = requests.get(
                "https://api.spotify.com/v1/me/player",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json() if resp and resp.content else {}
                return bool((data or {}).get("is_playing", False))
            return None
        except Exception:
            return None

    def _build_nowfysettings_reply_markup(self):
        try:
            from org.telegram.tgnet import TLRPC
            is_playing = self._nowfysettings_is_playing()
            play_text = "Pause" if is_playing is True else "Play"

            markup = TLRPC.TL_replyInlineMarkup()
            row1 = TLRPC.TL_keyboardButtonRow()
            row2 = TLRPC.TL_keyboardButtonRow()

            b_play = TLRPC.TL_keyboardButtonCallback()
            b_play.text = play_text
            b_play.data = b"nowfy:settings:playpause"
            b_play.requires_password = False
            row1.buttons.add(b_play)

            b_like = TLRPC.TL_keyboardButtonCallback()
            b_like.text = "Like"
            b_like.data = b"nowfy:settings:like"
            b_like.requires_password = False
            row1.buttons.add(b_like)

            b_back = TLRPC.TL_keyboardButtonCallback()
            b_back.text = "Back"
            b_back.data = b"nowfy:settings:back"
            b_back.requires_password = False
            row2.buttons.add(b_back)

            b_skip = TLRPC.TL_keyboardButtonCallback()
            b_skip.text = "Skip"
            b_skip.data = b"nowfy:settings:skip"
            b_skip.requires_password = False
            row2.buttons.add(b_skip)

            markup.rows.add(row1)
            markup.rows.add(row2)
            return markup
        except Exception:
            return None

    def _send_nowfysettings_inline_message(self, params):
        try:
            if params is None:
                return False
            txt = str(tr("nowfy_settings_inline_caption") or "").strip() or "Nowfy Settings"
            markup = self._build_nowfysettings_reply_markup()
            if markup is None:
                try:
                    log("[Nowfy][NowfySettings] markup build failed")
                except Exception:
                    pass
                return False
            dialog_id = None
            try:
                peer = getattr(params, "peer", None)
                if isinstance(peer, int):
                    dialog_id = int(peer)
            except Exception:
                dialog_id = None
            if dialog_id is None:
                try:
                    frag = get_last_fragment()
                    if frag and hasattr(frag, "getDialogId"):
                        dialog_id = int(frag.getDialogId())
                except Exception:
                    dialog_id = None
            if dialog_id is None:
                try:
                    log("[Nowfy][NowfySettings] no dialog id")
                except Exception:
                    pass
                return False
            def _inject():
                try:
                    chat_activity = self._get_nowfysettings_chat_activity(dialog_id)
                    if chat_activity is None:
                        try:
                            log("[Nowfy][NowfySettings] current fragment is not chat")
                        except Exception:
                            pass
                        return
                    topic_id = 0
                    try:
                        if hasattr(chat_activity, "getTopicId"):
                            topic_id = int(chat_activity.getTopicId() or 0)
                    except Exception:
                        topic_id = 0
                    msg_obj = self._build_nowfysettings_local_message(dialog_id, topic_id, txt, markup)
                    if msg_obj is None:
                        try:
                            log("[Nowfy][NowfySettings] build local message failed")
                        except Exception:
                            pass
                        return
                    ok_local = self._insert_nowfysettings_local_message(chat_activity, msg_obj)
                    try:
                        log(f"[Nowfy][NowfySettings] local inject ok={bool(ok_local)}")
                    except Exception:
                        pass
                except Exception:
                    try:
                        log("[Nowfy][NowfySettings] local inject failed")
                    except Exception:
                        pass
            run_on_ui_thread(_inject)
            return True
        except Exception:
            try:
                log("[Nowfy][NowfySettings] prepare failed")
            except Exception:
                pass
            return False

    def _build_nowfysettings_local_message(self, dialog_id, topic_id, text, markup):
        try:
            from org.telegram.tgnet import TLRPC
            try:
                from markdown_utils import parse_markdown as _parse_markdown
            except Exception:
                _parse_markdown = None
            uc = get_user_config()
            account = int(getattr(uc, "selectedAccount", 0)) if uc is not None else 0
            my_id = int(uc.getClientUserId()) if uc is not None else 0
            msg = TLRPC.TL_message()
            msg.id = -random.randint(1, 2_000_000_000)
            msg.date = int(time.time())
            raw_text = str(text or "")
            parsed = None
            if _parse_markdown is not None:
                try:
                    parsed = _parse_markdown(raw_text)
                except Exception as e_md:
                    parsed = None
                    try:
                        log(f"[Nowfy][NowfySettings] markdown fallback: {e_md}")
                    except Exception:
                        pass
            msg.message = parsed.text if parsed is not None else raw_text
            if parsed is not None and getattr(parsed, "entities", None):
                entities = ArrayList()
                for ent in parsed.entities:
                    entities.add(ent.to_tlrpc_object())
                msg.entities = entities
                msg.flags |= 128
            peer = None
            try:
                mc = get_messages_controller()
                if mc is not None:
                    peer = mc.getPeer(int(dialog_id))
            except Exception:
                peer = None
            if peer is None:
                did = int(dialog_id)
                if did > 0:
                    p = TLRPC.TL_peerUser()
                    p.user_id = did
                    peer = p
                else:
                    abs_did = abs(did)
                    if str(abs_did).startswith("100"):
                        p = TLRPC.TL_peerChannel()
                        p.channel_id = int(abs_did - 1000000000000)
                        peer = p
                    else:
                        p = TLRPC.TL_peerChat()
                        p.chat_id = int(abs_did)
                        peer = p
            msg.peer_id = peer
            if my_id > 0:
                from_peer = TLRPC.TL_peerUser()
                from_peer.user_id = my_id
                msg.from_id = from_peer
            msg.out = True
            msg.flags |= 2
            msg.flags |= 256
            if int(topic_id or 0):
                reply = TLRPC.TL_messageReplyHeader()
                reply.reply_to_top_id = int(topic_id)
                msg.reply_to = reply
                msg.flags |= 8
            if markup is not None:
                msg.reply_markup = markup
                msg.flags |= 64
            return MessageObject(account, msg, False, False)
        except Exception as e:
            try:
                log(f"[Nowfy][NowfySettings] local build error: {e}")
            except Exception:
                pass
            return None

    def _insert_nowfysettings_local_message(self, chat_activity, msg_obj):
        try:
            method = chat_activity.getClass().getDeclaredMethod("processNewMessages", ArrayList)
            method.setAccessible(True)
            arr = ArrayList()
            arr.add(msg_obj)
            method.invoke(chat_activity, arr)
            return True
        except Exception:
            return False

    def _get_nowfysettings_chat_activity(self, dialog_id):
        try:
            frag = get_last_fragment()
            if frag is None:
                return None
            try:
                if hasattr(frag, "getDialogId") and int(frag.getDialogId()) != int(dialog_id):
                    return None
            except Exception:
                return None
            chat_activity_cls = find_class("org.telegram.ui.ChatActivity")
            if chat_activity_cls is None:
                return frag
            return frag if isinstance(frag, chat_activity_cls) else None
        except Exception:
            return None

    def _handle_nowfysettings_inline_press(self, cell, btn, hook_param, is_long=False):
        try:
            if btn is None:
                try:
                    log("[Nowfy][NowfySettings] press ignored: button is None")
                except Exception:
                    pass
                return
            data_raw = getattr(btn, "data", None)
            if data_raw is None:
                try:
                    log("[Nowfy][NowfySettings] press ignored: button has no data")
                except Exception:
                    pass
                return
            try:
                payload = bytes(data_raw).decode("utf-8", errors="ignore")
            except Exception:
                payload = str(data_raw or "")
            if not payload.startswith("nowfy:settings:"):
                try:
                    log(f"[Nowfy][NowfySettings] press ignored: payload={payload}")
                except Exception:
                    pass
                return
            try:
                log(f"[Nowfy][NowfySettings] press payload={payload}")
            except Exception:
                pass
            hook_param.setResult(None)
            action = payload.split(":", 2)[2] if ":" in payload else ""
            self._dispatch_nowfysettings_action(action)
            try:
                for obj in (hook_param.args or []):
                    try:
                        if hasattr(obj, "invalidate"):
                            run_on_ui_thread(lambda v=obj: v.invalidate())
                    except Exception:
                        pass
            except Exception:
                pass
        except Exception:
            pass

    def _dispatch_nowfysettings_action(self, action):
        try:
            act = str(action or "").strip().lower()
            if not act:
                return
            try:
                self._nowfysettings_log_action_preflight(act)
            except Exception:
                pass
            def _run():
                try:
                    try:
                        log(f"[Nowfy][NowfySettings] action start={act}")
                    except Exception:
                        pass
                    self._run_nowfysettings_spotify_action(act)
                    try:
                        log(f"[Nowfy][NowfySettings] action done={act}")
                    except Exception:
                        pass
                except Exception as e:
                    try:
                        log(f"[Nowfy][NowfySettings] action error {act}: {e}")
                    except Exception:
                        pass
            try:
                run_on_queue(_run)
            except Exception:
                _run()
        except Exception:
            pass

    def _nowfysettings_show_notice(self, text):
        try:
            run_on_ui_thread(lambda: self._show_control_notice(text))
        except Exception:
            try:
                self._show_control_notice(text)
            except Exception:
                pass

    def _nowfysettings_activate_any_device(self, token):
        try:
            resp = requests.get(
                "https://api.spotify.com/v1/me/player/devices",
                headers={"Authorization": f"Bearer {token}"},
                timeout=6
            )
            try:
                log(f"[Nowfy][NowfySettings] devices status={int(resp.status_code)}")
            except Exception:
                pass
            if resp.status_code != 200 or not resp.content:
                return False
            data = resp.json() or {}
            devices = data.get("devices") if isinstance(data, dict) else None
            if not isinstance(devices, list) or not devices:
                return False
            target = None
            for d in devices:
                if isinstance(d, dict) and bool(d.get("is_active", False)):
                    target = d
                    break
            if target is None:
                for d in devices:
                    if isinstance(d, dict) and d.get("id"):
                        target = d
                        break
            if not isinstance(target, dict):
                return False
            device_id = str(target.get("id") or "").strip()
            if not device_id:
                return False
            move = requests.put(
                "https://api.spotify.com/v1/me/player",
                headers={"Authorization": f"Bearer {token}"},
                json={"device_ids": [device_id], "play": True},
                timeout=6
            )
            try:
                log(f"[Nowfy][NowfySettings] transfer status={int(move.status_code)} id={device_id}")
            except Exception:
                pass
            return int(move.status_code) in (200, 202, 204)
        except Exception as e:
            try:
                log(f"[Nowfy][NowfySettings] activate device error={e}")
            except Exception:
                pass
            return False

    def _run_nowfysettings_spotify_action(self, act):
        token = None
        try:
            try:
                token = self._get_access_token(show_error_bulletin=False)
            except Exception:
                token = self._get_access_token()
        except Exception:
            token = None
        if not token:
            self._nowfysettings_show_notice(tr("error_auth"))
            return

        headers = {"Authorization": f"Bearer {token}"}

        def _call(method, url, **kwargs):
            fn = getattr(requests, method.lower())
            return fn(url, headers=headers, timeout=6, **kwargs)

        def _retry_if_no_device(method, url, **kwargs):
            r = _call(method, url, **kwargs)
            code = int(getattr(r, "status_code", 0) or 0)
            try:
                log(f"[Nowfy][NowfySettings] {act} status={code}")
            except Exception:
                pass
            if code != 404:
                return r
            if not self._nowfysettings_activate_any_device(token):
                return r
            r2 = _call(method, url, **kwargs)
            try:
                log(f"[Nowfy][NowfySettings] {act} retry status={int(getattr(r2, 'status_code', 0) or 0)}")
            except Exception:
                pass
            return r2

        try:
            if act == "playpause":
                state = _call("get", "https://api.spotify.com/v1/me/player")
                code = int(getattr(state, "status_code", 0) or 0)
                try:
                    log(f"[Nowfy][NowfySettings] playpause state status={code}")
                except Exception:
                    pass
                if code == 401:
                    self._nowfysettings_show_notice(tr("error_auth"))
                    return
                if code == 404:
                    if self._nowfysettings_activate_any_device(token):
                        state = _call("get", "https://api.spotify.com/v1/me/player")
                        code = int(getattr(state, "status_code", 0) or 0)
                if code != 200:
                    self._nowfysettings_show_notice(tr("error_no_active_device") if code == 404 else tr("error_unknown"))
                    return
                data = state.json() if state and state.content else {}
                is_playing = bool((data or {}).get("is_playing", False))
                endpoint = "https://api.spotify.com/v1/me/player/pause" if is_playing else "https://api.spotify.com/v1/me/player/play"
                resp = _retry_if_no_device("put", endpoint)
                rcode = int(getattr(resp, "status_code", 0) or 0)
                if rcode in (200, 202, 204):
                    self._nowfysettings_show_notice(tr("bulletin_paused") if is_playing else tr("bulletin_resumed"))
                elif rcode == 403:
                    self._nowfysettings_show_notice(tr("error_premium_required"))
                elif rcode == 404:
                    self._nowfysettings_show_notice(tr("error_no_active_device"))
                else:
                    self._nowfysettings_show_notice(tr("error_unknown"))
                return

            if act == "skip":
                resp = _retry_if_no_device("post", "https://api.spotify.com/v1/me/player/next")
                rcode = int(getattr(resp, "status_code", 0) or 0)
                if rcode in (200, 202, 204):
                    self._nowfysettings_show_notice(tr("bulletin_skipped"))
                elif rcode == 403:
                    self._nowfysettings_show_notice(tr("error_premium_required"))
                elif rcode == 404:
                    self._nowfysettings_show_notice(tr("error_no_active_device"))
                else:
                    self._nowfysettings_show_notice(tr("error_unknown"))
                return

            if act == "back":
                resp = _retry_if_no_device("post", "https://api.spotify.com/v1/me/player/previous")
                rcode = int(getattr(resp, "status_code", 0) or 0)
                if rcode in (200, 202, 204):
                    self._nowfysettings_show_notice(tr("bulletin_previous"))
                elif rcode == 403:
                    self._nowfysettings_show_notice(tr("error_premium_required"))
                elif rcode == 404:
                    self._nowfysettings_show_notice(tr("error_no_active_device"))
                else:
                    self._nowfysettings_show_notice(tr("error_unknown"))
                return

            if act == "like":
                current = _call("get", "https://api.spotify.com/v1/me/player/currently-playing")
                ccode = int(getattr(current, "status_code", 0) or 0)
                try:
                    log(f"[Nowfy][NowfySettings] like currently-playing status={ccode}")
                except Exception:
                    pass
                if ccode != 200 or not current.content:
                    self._nowfysettings_show_notice(tr("error_no_track_playing"))
                    return
                item = (current.json() or {}).get("item") if current else None
                track_id = str((item or {}).get("id") or "").strip()
                if not track_id:
                    self._nowfysettings_show_notice(tr("error_no_track_playing"))
                    return
                contains = _call("get", f"https://api.spotify.com/v1/me/tracks/contains?ids={track_id}")
                if int(getattr(contains, "status_code", 0) or 0) == 200:
                    try:
                        data = contains.json()
                        if isinstance(data, list) and data and bool(data[0]):
                            self._nowfysettings_show_notice(tr("bulletin_already_liked"))
                            return
                    except Exception:
                        pass
                like = _call("put", "https://api.spotify.com/v1/me/tracks", json={"ids": [track_id]})
                lcode = int(getattr(like, "status_code", 0) or 0)
                try:
                    log(f"[Nowfy][NowfySettings] like put status={lcode}")
                except Exception:
                    pass
                if lcode in (200, 202, 204):
                    self._nowfysettings_show_notice(tr("bulletin_liked"))
                elif lcode == 403:
                    self._nowfysettings_show_notice(tr("error_premium_required"))
                else:
                    self._nowfysettings_show_notice(tr("error_unknown"))
                return
        except Exception as e:
            try:
                log(f"[Nowfy][NowfySettings] action exception {act}: {e}")
            except Exception:
                pass
            self._nowfysettings_show_notice(tr("error_unknown"))

    def _nowfysettings_log_action_preflight(self, action):
        try:
            token = None
            try:
                token = self._get_access_token(show_error_bulletin=False)
            except Exception:
                token = self._get_access_token()
            tok_ok = bool(token)
            try:
                log(f"[Nowfy][NowfySettings] preflight action={action} token={tok_ok}")
            except Exception:
                pass
            if not token:
                return
            try:
                resp = requests.get(
                    "https://api.spotify.com/v1/me/player",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=5
                )
                try:
                    log(f"[Nowfy][NowfySettings] preflight /me/player status={int(resp.status_code)}")
                except Exception:
                    pass
            except Exception as e_player:
                try:
                    log(f"[Nowfy][NowfySettings] preflight /me/player error={e_player}")
                except Exception:
                    pass
            if str(action or "") == "like":
                try:
                    resp2 = requests.get(
                        "https://api.spotify.com/v1/me/player/currently-playing",
                        headers={"Authorization": f"Bearer {token}"},
                        timeout=5
                    )
                    try:
                        log(f"[Nowfy][NowfySettings] preflight /currently-playing status={int(resp2.status_code)}")
                    except Exception:
                        pass
                except Exception as e_track:
                    try:
                        log(f"[Nowfy][NowfySettings] preflight /currently-playing error={e_track}")
                    except Exception:
                        pass
        except Exception:
            pass

    def _apply_chat_fab_state(self):
        try:
            self._setup_chat_fab_hook()
        except Exception:
            pass
        try:
            enabled = bool(self.get_setting("fab_chat_enabled", False)) or bool(self._is_quick_flow_list_enabled())
        except Exception:
            enabled = False
        try:
            self._trace_flow_debug(f"apply state enabled={enabled}")
        except Exception:
            pass
        if enabled:
            self._setup_chat_fab_hook()
            try:
                fragment = get_last_fragment()
                try:
                    cname = str(fragment.getClass().getName() or "") if fragment else "None"
                except Exception:
                    cname = "unknown"
                self._trace_flow_debug(f"current fragment={cname}")
                if isinstance(fragment, ChatActivity) or self._is_dialogs_fragment(fragment):
                    run_on_ui_thread(lambda: self._attach_chat_fab(fragment))
            except Exception:
                pass
        else:
            self._detach_chat_fab()

    def _is_dialogs_fragment(self, fragment):
        try:
            if fragment is None:
                return False
            name = str(fragment.getClass().getName() or "")
            return "DialogsActivity" in name
        except Exception:
            return False

    def _trace_flow_debug(self, message):
        try:
            try:
                if _NOWFY_LOGS_MUTED or bool(self.get_setting("disable_logs", False)):
                    return
            except Exception:
                if _NOWFY_LOGS_MUTED:
                    return
            msg = str(message or "")
            if not msg:
                return
            log(f"[Nowfy][QuickFlow] {msg}")
        except Exception:
            pass

    def _is_quick_flow_list_enabled(self):
        try:
            if not bool(self.get_setting("nowfy_quick_flow_enabled", True)):
                self._trace_flow_debug("quick-flow list disabled: switch off")
                return False
            self._trace_flow_debug("quick-flow list enabled=True")
            return True
        except Exception:
            self._trace_flow_debug("quick-flow list disabled: exception")
            return False

    def _load_assets_png_bitmap(self, filename):
        try:
            name = str(filename or "").strip()
            if not name:
                return None
            candidates = [
                os.path.join(os.path.dirname(__file__), "assets", "png", name),
                os.path.join(os.path.dirname(__file__), "nowfy", "assets", "png", name),
            ]
            for p in candidates:
                try:
                    if p and os.path.isfile(p):
                        bmp = BitmapFactory.decodeFile(p)
                        if bmp:
                            return bmp
                except Exception:
                    pass
            try:
                for pkg_path in (f"assets/png/{name}", f"assets/icons/{name}"):
                    try:
                        data = pkgutil.get_data("nowfy", pkg_path)
                    except Exception:
                        data = None
                    if data:
                        try:
                            bmp = BitmapFactory.decodeByteArray(data, 0, len(data))
                            if bmp:
                                return bmp
                        except Exception:
                            pass
            except Exception:
                pass
        except Exception:
            pass
        return None

    def _can_send_now_card_from_fragment(self, fragment):
        try:
            if not isinstance(fragment, ChatActivity):
                return False
            chat = getattr(fragment, "currentChat", None)
            if chat is None:
                return True
            try:
                if not bool(ChatObject.canSendPhoto(chat)):
                    return False
            except Exception:
                return False
            try:
                if bool(ChatObject.isChannel(chat)) and not bool(getattr(chat, "megagroup", False)):
                    if hasattr(ChatObject, "canPost"):
                        return bool(ChatObject.canPost(chat))
            except Exception:
                pass
            return True
        except Exception:
            return False

    def _attach_chat_quick_share_button(self, fragment):
        try:
            if not isinstance(fragment, ChatActivity):
                return
            enter_view = None
            try:
                enter_view = _get_private_field_silent(fragment, "chatActivityEnterView")
            except Exception:
                enter_view = None
            if enter_view is None:
                return
            host = None
            try:
                host = _get_private_field_silent(enter_view, "attachLayout")
            except Exception:
                host = None
            if host is None:
                try:
                    host = _get_private_field_silent(enter_view, "sendButtonContainer")
                except Exception:
                    host = None
            if host is None:
                return
            try:
                existing = host.findViewWithTag("__nowfy_quick_share_btn__")
            except Exception:
                existing = None
            if existing is not None:
                try:
                    self._schedule_quick_share_reorder(host, existing)
                except Exception:
                    pass
                return
            btn = FrameLayout(host.getContext())
            try:
                btn.setTag("__nowfy_quick_share_btn__")
            except Exception:
                pass
            try:
                btn.setBackground(None)
            except Exception:
                pass
            icon = ImageView(host.getContext())
            _custom_icon = None
            try:
                bgc = int(Theme.getColor(Theme.key_windowBackgroundWhite))
                r = (bgc >> 16) & 0xFF
                g = (bgc >> 8) & 0xFF
                b = bgc & 0xFF
                is_dark_theme = (((r * 299 + g * 587 + b * 114) / 1000.0) < 150)
            except Exception:
                is_dark_theme = True
            try:
                icon_name = "nowfy_send_white.png" if is_dark_theme else "nowfy_send_black.png"
                _custom_icon = self._load_assets_png_bitmap(icon_name)
            except Exception:
                _custom_icon = None
            try:
                if _custom_icon:
                    icon.setImageBitmap(_custom_icon)
                else:
                    icon.setImageResource(R.drawable.files_music)
            except Exception:
                pass
            try:
                tint = int(Theme.getColor(Theme.key_chat_messagePanelIcons))
            except Exception:
                try:
                    tint = int(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
                except Exception:
                    tint = 0xFF8A8A8A
            try:
                icon.setColorFilter(tint)
            except Exception:
                pass
            try:
                icon.setScaleType(ImageView.ScaleType.CENTER_INSIDE)
                icon.setPadding(0, 0, 0, 0)
                icon.setTranslationX(0.0)
            except Exception:
                pass
            try:
                btn.addView(icon, FrameLayout.LayoutParams(AndroidUtilities.dp(24), AndroidUtilities.dp(24), Gravity.CENTER))
            except Exception:
                btn.addView(icon)
            try:
                if isinstance(host, LinearLayout):
                    lp = LinearLayout.LayoutParams(AndroidUtilities.dp(28), AndroidUtilities.dp(28))
                    try:
                        lp.gravity = Gravity.CENTER_VERTICAL
                    except Exception:
                        pass
                    try:
                        lp.leftMargin = AndroidUtilities.dp(2)
                        lp.rightMargin = AndroidUtilities.dp(2)
                    except Exception:
                        pass
                    try:
                        host.addView(btn, lp)
                    except Exception:
                        host.addView(btn, lp)
                else:
                    lp = FrameLayout.LayoutParams(AndroidUtilities.dp(28), AndroidUtilities.dp(28), Gravity.RIGHT | Gravity.BOTTOM)
                    lp.rightMargin = AndroidUtilities.dp(52)
                    lp.bottomMargin = AndroidUtilities.dp(2)
                    host.addView(btn, lp)
            except Exception:
                host.addView(btn)
            try:
                btn.setAlpha(0.92)
                btn.setScaleX(1.0)
                btn.setScaleY(1.0)
                btn.setTranslationY(0.0)
                btn.bringToFront()
            except Exception:
                pass
            class _NowfyQuickShareHold(dynamic_proxy(View.OnLongClickListener)):
                def onLongClick(self_obj, v):
                    try:
                        if not self._can_send_now_card_from_fragment(fragment):
                            BulletinHelper.show_info(tr("nowfy_tab_status_no_permission"))
                            return True
                        try:
                            v.animate().scaleX(0.9).scaleY(0.9).alpha(0.72).setDuration(80).start()
                        except Exception:
                            pass
                        self._send_now_playing_card_for_tab()
                        try:
                            v.animate().scaleX(1.0).scaleY(1.0).alpha(0.92).setDuration(120).start()
                        except Exception:
                            pass
                    except Exception:
                        pass
                    return True
            class _NowfyQuickShareClick(dynamic_proxy(View.OnClickListener)):
                def onClick(self_obj, v):
                    try:
                        BulletinHelper.show_info(tr("nowfy_hold_to_send_hint"))
                    except Exception:
                        pass
            try:
                btn.setOnLongClickListener(_NowfyQuickShareHold())
            except Exception:
                pass
            try:
                btn.setOnClickListener(_NowfyQuickShareClick())
            except Exception:
                pass
            try:
                setattr(self, "_chat_nowfy_quick_share_button", btn)
            except Exception:
                pass
            try:
                self._schedule_quick_share_reorder(host, btn)
            except Exception:
                pass
        except Exception:
            pass

    def _schedule_quick_share_reorder(self, host, btn):
        try:
            if not isinstance(host, LinearLayout):
                return
            if btn is None:
                return
            def _do_reorder_once():
                try:
                    if btn.getParent() is not host:
                        return
                    lp_prev = btn.getLayoutParams()
                    try:
                        host.removeView(btn)
                    except Exception:
                        return
                    try:
                        host.addView(btn, lp_prev)
                    except Exception:
                        try:
                            host.addView(btn)
                        except Exception:
                            pass
                except Exception:
                    pass
            run_on_ui_thread(_do_reorder_once)
            def _retry():
                for _ in range(3):
                    try:
                        time.sleep(0.22)
                    except Exception:
                        pass
                    run_on_ui_thread(_do_reorder_once)
            run_on_queue(_retry)
        except Exception:
            pass

    def _find_dialogs_native_fab(self, fragment, host):
        candidates = self._get_dialogs_native_fab_candidates(fragment)
        for v in candidates:
            try:
                if v and v.getParent() is not None:
                    return v
            except Exception:
                pass
        try:
            for v in candidates:
                try:
                    if v and host and v.getParent() is host:
                        return v
                except Exception:
                    pass
        except Exception:
            pass
        return None

    def _get_dialogs_native_fab_candidates(self, fragment):
        candidates = []
        seen = set()
        for k in (
            "floatingButtonContainer", "floatingButton2Container",
            "floatingButton", "floatingButton2",
            "writeButtonContainer", "writeButton", "floatingButtonView"
        ):
            try:
                v = _get_private_field_silent(fragment, k)
            except Exception:
                v = None
            if v is None:
                continue
            try:
                self._trace_flow_debug(f"dialogs native field={k} ok")
            except Exception:
                pass
            try:
                oid = int(v.hashCode())
            except Exception:
                oid = id(v)
            if oid in seen:
                continue
            seen.add(oid)
            candidates.append(v)
        return candidates

    def _get_dialogs_nav_bounds(self, fragment, host):
        try:
            if fragment is None or host is None:
                return None
            host_h = int(host.getHeight() or 0)
            host_w = int(host.getWidth() or 0)
            if host_h <= 0 or host_w <= 0:
                return None
            candidates = []
            for fname in (
                "bottomNavigationView", "bottomNavigationLayout", "bottomNavigation",
                "bottomTabs", "bottomBar", "tabsView", "tabLayout", "actionBarTabs"
            ):
                try:
                    v = _get_private_field_silent(fragment, fname)
                except Exception:
                    v = None
                if v is not None:
                    candidates.append(v)
            for v in candidates:
                try:
                    if not bool(v.isShown()):
                        continue
                    vw = int(v.getWidth() or 0)
                    vh = int(v.getHeight() or 0)
                    if vw <= 0 or vh <= 0:
                        continue
                    if vh > AndroidUtilities.dp(140):
                        continue
                    loc_h = jarray(jint)(2)
                    loc_v = jarray(jint)(2)
                    host.getLocationOnScreen(loc_h)
                    v.getLocationOnScreen(loc_v)
                    left = int(loc_v[0]) - int(loc_h[0])
                    top = int(loc_v[1]) - int(loc_h[1])
                    if top < AndroidUtilities.dp(40):
                        continue
                    if top > (host_h - AndroidUtilities.dp(40)):
                        continue
                    return (left, top, vw, vh)
                except Exception:
                    pass
            return None
        except Exception:
            return None

    def _hide_dialogs_native_fab(self, fragment, host):
        return None

    def _restore_dialogs_native_fab(self):
        return

    def _attach_chat_fab(self, fragment):
        try:
            is_chat = isinstance(fragment, ChatActivity)
            is_dialogs = self._is_dialogs_fragment(fragment)
            if fragment is None or (not is_chat and not is_dialogs):
                self._detach_chat_fab()
                return
            if is_chat and (not bool(self.get_setting("fab_chat_enabled", False))):
                self._trace_flow_debug("attach chat fab skipped: flow off")
                return
            if is_dialogs and (not self._is_quick_flow_list_enabled()):
                self._trace_flow_debug("attach dialogs fab skipped: quick-flow off")
                self._detach_chat_fab()
                return
            self._trace_flow_debug(f"attach fab start chat={is_chat} dialogs={is_dialogs}")
            activity = fragment.getParentActivity()
            if not activity:
                return
            host = None
            if is_dialogs:
                try:
                    host = fragment.getFragmentView()
                except Exception:
                    host = None
            if is_dialogs and (not host):
                try:
                    self._trace_flow_debug("dialogs attach skipped: fragment view missing")
                except Exception:
                    pass
                self._detach_chat_fab()
                return
            if not host:
                try:
                    host = activity.findViewById(16908290)
                except Exception:
                    host = None
            if not host:
                try:
                    host = get_private_field(fragment, "fragmentView")
                except Exception:
                    host = None
            if is_dialogs:
                pass
            if not host:
                return
            old_btn = getattr(self, "_chat_fab_button", None)
            old_host = getattr(self, "_chat_fab_host", None)
            if old_btn and old_host:
                try:
                    if old_btn.getParent() is old_host and fragment == getattr(self, "_chat_fab_fragment", None):
                        return
                except Exception:
                    pass
            self._detach_chat_fab()
            btn = FrameLayout(activity)
            try:
                s56 = AndroidUtilities.dp(56)
                btn.setMinimumWidth(0)
                btn.setMinimumHeight(0)
                btn.setPadding(0, 0, 0, 0)
            except Exception:
                pass
            try:
                bg = GradientDrawable()
                try:
                    if is_dialogs:
                        bg.setShape(GradientDrawable.RECTANGLE)
                        bg.setCornerRadius(AndroidUtilities.dp(14))
                    else:
                        bg.setShape(GradientDrawable.OVAL)
                except Exception:
                    pass
                try:
                    if is_dialogs:
                        bg.setColor(Theme.getColor(Theme.key_featuredStickers_addButton))
                    else:
                        bg.setColor(Theme.getColor(Theme.key_featuredStickers_addButton))
                except Exception:
                    bg.setColor(Color.parseColor("#3B82F6"))
                btn.setBackground(bg)
            except Exception:
                pass
            try:
                btn.setClickable(True)
            except Exception:
                pass
            icon = ImageView(activity)
            _fab_custom_icon = self._load_assets_png_bitmap("buttom_nowfy.png")
            try:
                if _fab_custom_icon:
                    icon.setImageBitmap(_fab_custom_icon)
                else:
                    icon.setImageResource(R.drawable.files_music)
            except Exception:
                pass
            if not _fab_custom_icon:
                try:
                    icon.setColorFilter(Theme.getColor(Theme.key_featuredStickers_buttonText))
                except Exception:
                    try:
                        icon.setColorFilter(Color.WHITE)
                    except Exception:
                        pass
            _fab_btn_size_dialogs = AndroidUtilities.dp(48)
            _fab_btn_size_chat = AndroidUtilities.dp(56)
            _fab_icon_size_dialogs = AndroidUtilities.dp(22)
            _fab_icon_size_chat = AndroidUtilities.dp(24)
            lp_icon = FrameLayout.LayoutParams(
                _fab_icon_size_dialogs if is_dialogs else _fab_icon_size_chat,
                _fab_icon_size_dialogs if is_dialogs else _fab_icon_size_chat,
                Gravity.CENTER
            )
            btn.addView(icon, lp_icon)
            flow_side = self._get_nowfy_flow_side() if is_chat else 0
            quick_side_mode = self._get_nowfy_quick_flow_side_mode() if is_dialogs else 0
            if is_dialogs:
                try:
                    host.addView(btn)
                    lp_any = btn.getLayoutParams()
                    if lp_any is not None:
                        lp_any.width = _fab_btn_size_dialogs
                        lp_any.height = _fab_btn_size_dialogs
                        btn.setLayoutParams(lp_any)
                    try:
                        host_h0 = int(host.getHeight() or 0)
                        host_w0 = int(host.getWidth() or 0)
                    except Exception:
                        host_h0 = 0
                        host_w0 = 0
                    try:
                        side0 = AndroidUtilities.dp(16)
                        btn_w0 = _fab_btn_size_dialogs
                        fb0 = AndroidUtilities.dp(86)
                        if int(quick_side_mode) == 1:
                            fx0, fy0 = self._get_nowfy_quick_flow_free_position()
                            if int(fx0) >= 0 and int(fy0) >= 0:
                                x0 = int(fx0)
                                y0 = int(fy0)
                            else:
                                nav_bounds0 = self._get_dialogs_nav_bounds(fragment, host)
                                if nav_bounds0:
                                    left0, top0, navw0, navh0 = nav_bounds0
                                    x0 = max(0, int(left0))
                                    y0 = int(top0) - btn_w0 - AndroidUtilities.dp(12)
                                else:
                                    x0 = side0
                                    y0 = (host_h0 - btn_w0 - fb0) if host_h0 > 0 else AndroidUtilities.dp(220)
                        else:
                            nav_bounds0 = self._get_dialogs_nav_bounds(fragment, host)
                            if nav_bounds0:
                                left0, top0, navw0, navh0 = nav_bounds0
                                x0 = max(0, int(left0))
                                y0 = int(top0) - btn_w0 - AndroidUtilities.dp(12)
                            else:
                                x0 = side0
                                y0 = (host_h0 - btn_w0 - fb0) if host_h0 > 0 else AndroidUtilities.dp(220)
                        if y0 < AndroidUtilities.dp(84):
                            y0 = AndroidUtilities.dp(84)
                        btn.setX(float(max(0, x0)))
                        btn.setY(float(max(0, y0)))
                    except Exception:
                        pass
                    self._trace_flow_debug("dialogs addView overlay ok")
                except Exception as _dialogs_add_err:
                    try:
                        self._trace_flow_debug(f"dialogs addView overlay failed: {_dialogs_add_err}")
                    except Exception:
                        pass
                    return
            else:
                side_gravity = Gravity.LEFT if int(flow_side) in (0, 2) else Gravity.RIGHT
                lp = FrameLayout.LayoutParams(AndroidUtilities.dp(56), AndroidUtilities.dp(56), Gravity.BOTTOM | side_gravity)
                try:
                    if int(flow_side) in (0, 2):
                        lp.setMargins(AndroidUtilities.dp(16), 0, 0, AndroidUtilities.dp(86))
                    else:
                        lp.setMargins(0, 0, AndroidUtilities.dp(16), AndroidUtilities.dp(86))
                except Exception:
                    pass
                host.addView(btn, lp)
            try:
                btn.bringToFront()
            except Exception:
                pass
            def _fab_click(_view):
                try:
                    try:
                        if float(getattr(self, "_chat_fab_block_click_until", 0.0) or 0.0) > float(time.time()):
                            return
                    except Exception:
                        pass
                    self._open_chat_fab_sheet(forced_fragment=fragment)
                except Exception:
                    pass
            btn.setOnClickListener(OnClickListener(_fab_click))
            if (is_chat and int(flow_side) == 2) or (is_dialogs and int(quick_side_mode) == 1):
                plugin_ref = self
                class _FabLongPressMove(dynamic_proxy(View.OnLongClickListener)):
                    def onLongClick(self, _v):
                        try:
                            plugin_ref._chat_fab_drag_mode = True
                            plugin_ref._chat_fab_drag_has_moved = False
                            plugin_ref._chat_fab_drag_target = btn
                            plugin_ref._chat_fab_drag_host = host
                            plugin_ref._chat_fab_drag_fragment = fragment
                            plugin_ref._chat_fab_drag_pressed = True
                            plugin_ref._chat_fab_drag_token = int(getattr(plugin_ref, "_chat_fab_drag_token", 0) or 0) + 1
                            plugin_ref._chat_fab_drag_down_ts = float(time.time())
                            plugin_ref._chat_fab_drag_start_x = float(btn.getX())
                            plugin_ref._chat_fab_drag_start_y = float(btn.getY())
                        except Exception:
                            pass
                        try:
                            BulletinHelper.show_info(tr("nowfy_flow_free_move_ready"))
                        except Exception:
                            pass
                        return True
                btn.setOnLongClickListener(_FabLongPressMove())
                class _FabFreeTouch(dynamic_proxy(View.OnTouchListener)):
                    def onTouch(self, _v, event):
                        try:
                            if event is None:
                                return False
                            action = int(event.getActionMasked())
                        except Exception:
                            return False
                        try:
                            if action == int(MotionEvent.ACTION_DOWN):
                                plugin_ref._chat_fab_drag_pressed = True
                                plugin_ref._chat_fab_drag_has_moved = False
                                plugin_ref._chat_fab_drag_down_x_raw = float(event.getRawX())
                                plugin_ref._chat_fab_drag_down_y_raw = float(event.getRawY())
                                tok = int(getattr(plugin_ref, "_chat_fab_drag_token", 0) or 0) + 1
                                plugin_ref._chat_fab_drag_token = tok
                                def _restore_if_holding(token=tok):
                                    try:
                                        if int(getattr(plugin_ref, "_chat_fab_drag_token", 0) or 0) != int(token):
                                            return
                                        if not bool(getattr(plugin_ref, "_chat_fab_drag_pressed", False)):
                                            return
                                        if bool(getattr(plugin_ref, "_chat_fab_drag_has_moved", False)):
                                            return
                                        if is_dialogs:
                                            plugin_ref._reset_nowfy_quick_flow_free_position()
                                        else:
                                            plugin_ref._reset_nowfy_flow_free_position()
                                        plugin_ref._chat_fab_drag_mode = False
                                        plugin_ref._chat_fab_block_click_until = float(time.time()) + 0.9
                                        try:
                                            BulletinHelper.show_info(tr("nowfy_flow_free_restored"))
                                        except Exception:
                                            pass
                                        plugin_ref._update_chat_fab_position_once()
                                    except Exception:
                                        pass
                                run_on_ui_thread(_restore_if_holding, 5000)
                            elif action == int(MotionEvent.ACTION_MOVE):
                                if not bool(getattr(plugin_ref, "_chat_fab_drag_mode", False)):
                                    return False
                                try:
                                    bx = float(btn.getX())
                                    by = float(btn.getY())
                                    nx = float(event.getRawX()) - float(btn.getWidth()) / 2.0
                                    ny = float(event.getRawY()) - float(btn.getHeight()) / 2.0
                                    if abs(nx - bx) > float(AndroidUtilities.dp(2)) or abs(ny - by) > float(AndroidUtilities.dp(2)):
                                        plugin_ref._chat_fab_drag_has_moved = True
                                except Exception:
                                    pass
                                try:
                                    host_w = int(host.getWidth() or 0)
                                    host_h = int(host.getHeight() or 0)
                                    bw = int(btn.getWidth() or (AndroidUtilities.dp(48) if is_dialogs else AndroidUtilities.dp(56)))
                                    bh = int(btn.getHeight() or (AndroidUtilities.dp(48) if is_dialogs else AndroidUtilities.dp(56)))
                                    min_x = int(AndroidUtilities.dp(4))
                                    max_x = int(max(min_x, host_w - bw - AndroidUtilities.dp(4)))
                                    min_y = int(AndroidUtilities.dp(84))
                                    max_y = int(max(min_y, host_h - bh - AndroidUtilities.dp(10)))
                                    nx = int(float(event.getRawX()) - float(bw) / 2.0)
                                    ny = int(float(event.getRawY()) - float(bh) / 2.0)
                                    if nx < min_x:
                                        nx = min_x
                                    if nx > max_x:
                                        nx = max_x
                                    if ny < min_y:
                                        ny = min_y
                                    if ny > max_y:
                                        ny = max_y
                                    btn.setX(float(nx))
                                    btn.setY(float(ny))
                                    btn.bringToFront()
                                except Exception:
                                    pass
                                return True
                            elif action in (int(MotionEvent.ACTION_UP), int(MotionEvent.ACTION_CANCEL)):
                                plugin_ref._chat_fab_drag_pressed = False
                                if not bool(getattr(plugin_ref, "_chat_fab_drag_mode", False)):
                                    return False
                                plugin_ref._chat_fab_drag_mode = False
                                if bool(getattr(plugin_ref, "_chat_fab_drag_has_moved", False)):
                                    try:
                                        if is_dialogs:
                                            plugin_ref._save_nowfy_quick_flow_free_position(int(btn.getX()), int(btn.getY()))
                                        else:
                                            plugin_ref._save_nowfy_flow_free_position(int(btn.getX()), int(btn.getY()))
                                    except Exception:
                                        pass
                                    try:
                                        BulletinHelper.show_info(tr("nowfy_flow_free_position_saved"))
                                    except Exception:
                                        pass
                                    plugin_ref._chat_fab_block_click_until = float(time.time()) + 0.5
                                    return True
                                plugin_ref._chat_fab_block_click_until = float(time.time()) + 0.5
                                return True
                        except Exception:
                            return False
                        return False
                btn.setOnTouchListener(_FabFreeTouch())
            if is_dialogs:
                try:
                    self._trace_flow_debug("dialogs attach: native fab untouched, quick-flow overlay only")
                except Exception:
                    pass
                try:
                    cf = get_last_fragment()
                    if isinstance(cf, ChatActivity):
                        btn.setVisibility(View.GONE)
                    else:
                        btn.setVisibility(View.VISIBLE)
                except Exception:
                    pass
            self._chat_fab_host = host
            self._chat_fab_button = btn
            self._chat_fab_fragment = fragment
            self._chat_fab_is_dialogs = bool(is_dialogs)
            if is_chat:
                try:
                    self._attach_chat_quick_share_button(fragment)
                except Exception:
                    pass
            try:
                self._apply_chat_fab_visual()
            except Exception:
                pass
            self._start_chat_fab_position_tracker()
            try:
                run_on_ui_thread(self._update_chat_fab_position_once)
            except Exception:
                pass
        except Exception:
            pass

    def _detach_chat_fab(self):
        try:
            self._stop_chat_fab_position_tracker()
        except Exception:
            pass
        try:
            btn = getattr(self, "_chat_fab_button", None)
            if btn:
                parent = btn.getParent()
                if parent:
                    parent.removeView(btn)
        except Exception:
            pass
        try:
            self._chat_fab_button = None
            self._chat_fab_host = None
            self._chat_fab_fragment = None
            self._chat_fab_is_dialogs = False
            self._chat_fab_drag_mode = False
            self._chat_fab_drag_pressed = False
            self._chat_fab_drag_target = None
            self._chat_fab_drag_host = None
            self._chat_fab_drag_fragment = None
        except Exception:
            pass

    def _update_chat_fab_position_once(self):
        try:
            btn = getattr(self, "_chat_fab_button", None)
            fragment = getattr(self, "_chat_fab_fragment", None)
            host = getattr(self, "_chat_fab_host", None)
            if btn is None or fragment is None or host is None:
                return
            try:
                current_fragment = get_last_fragment()
            except Exception:
                current_fragment = None
            is_dialogs = bool(getattr(self, "_chat_fab_is_dialogs", False))
            if current_fragment is None:
                if is_dialogs:
                    return
                try:
                    self._detach_chat_fab()
                except Exception:
                    pass
                return
            if is_dialogs:
                if current_fragment is None:
                    try:
                        btn.setVisibility(View.GONE)
                    except Exception:
                        pass
                    return
                try:
                    if isinstance(current_fragment, ChatActivity):
                        btn.setVisibility(View.GONE)
                        return
                    # exteraGram may report MainTabsActivity while dialogs list is visible.
                    # For chat-list overlay, trust host visibility instead of strict fragment class.
                    host_visible = False
                    try:
                        host_visible = bool(host.isShown()) and int(host.getWindowVisibility()) == int(View.VISIBLE)
                    except Exception:
                        host_visible = False
                    if not host_visible:
                        btn.setVisibility(View.GONE)
                        return
                    btn.setVisibility(View.VISIBLE)
                except Exception:
                    pass
                try:
                    if self._is_dialogs_fragment(current_fragment) and current_fragment != fragment:
                        self._chat_fab_fragment = current_fragment
                        fragment = current_fragment
                        new_host = None
                        try:
                            new_host = fragment.getFragmentView()
                        except Exception:
                            new_host = None
                        if new_host is not None and new_host != host:
                            try:
                                old_parent = btn.getParent()
                                if old_parent is not None:
                                    old_parent.removeView(btn)
                            except Exception:
                                pass
                            try:
                                new_host.addView(btn)
                                lp_any = btn.getLayoutParams()
                                if lp_any is not None:
                                    lp_any.width = AndroidUtilities.dp(48)
                                    lp_any.height = AndroidUtilities.dp(48)
                                    btn.setLayoutParams(lp_any)
                            except Exception:
                                pass
                            self._chat_fab_host = new_host
                            host = new_host
                except Exception:
                    pass
            else:
                if (not isinstance(current_fragment, ChatActivity)) or (current_fragment != fragment):
                    try:
                        self._detach_chat_fab()
                    except Exception:
                        pass
                    return
            enter_view = None
            if not is_dialogs:
                try:
                    enter_view = _get_private_field_silent(fragment, "chatActivityEnterView")
                except Exception:
                    enter_view = None
            host_h = 0
            host_w = 0
            try:
                host_h = int(host.getHeight() or 0)
                host_w = int(host.getWidth() or 0)
            except Exception:
                host_h = 0
                host_w = 0
            if host_h <= 0 or host_w <= 0:
                return
            try:
                if bool(getattr(self, "_chat_fab_drag_mode", False)) and getattr(self, "_chat_fab_drag_target", None) is btn:
                    return
            except Exception:
                pass
            btn_w = AndroidUtilities.dp(56)
            if is_dialogs:
                try:
                    btn_w = int(btn.getWidth() or 0)
                except Exception:
                    btn_w = 0
                if btn_w <= 0:
                    btn_w = AndroidUtilities.dp(48)
            side = AndroidUtilities.dp(16)
            fallback_bottom = AndroidUtilities.dp(86)
            gap = AndroidUtilities.dp(14)
            y = host_h - btn_w - fallback_bottom
            flow_side = self._get_nowfy_flow_side() if (not is_dialogs) else 0
            quick_side_mode = self._get_nowfy_quick_flow_side_mode() if is_dialogs else 0
            is_free_side = bool((not is_dialogs) and int(flow_side) == 2)
            is_quick_free_side = bool(is_dialogs and int(quick_side_mode) == 1)
            if flow_side == 0:
                x = side
            elif flow_side == 1:
                x = host_w - btn_w - side
            else:
                fx, fy = self._get_nowfy_flow_free_position()
                if int(fx) >= 0 and int(fy) >= 0:
                    x = int(fx)
                    y = int(fy)
                else:
                    x = side
            try:
                if (not is_free_side) and enter_view is not None:
                    hloc = jarray(jint)(2)
                    eloc = jarray(jint)(2)
                    host.getLocationOnScreen(hloc)
                    enter_view.getLocationOnScreen(eloc)
                    enter_top_rel = int(eloc[1]) - int(hloc[1])
                    y = enter_top_rel - btn_w - gap
            except Exception:
                pass
            if is_dialogs:
                if is_quick_free_side:
                    try:
                        qfx, qfy = self._get_nowfy_quick_flow_free_position()
                        if int(qfx) >= 0 and int(qfy) >= 0:
                            x = int(qfx)
                            y = int(qfy)
                        else:
                            nav_bounds = self._get_dialogs_nav_bounds(fragment, host)
                            if nav_bounds:
                                left, top, navw, navh = nav_bounds
                                x = int(left)
                                y = int(top) - btn_w - AndroidUtilities.dp(12)
                    except Exception:
                        pass
                else:
                    try:
                        nav_bounds = self._get_dialogs_nav_bounds(fragment, host)
                    except Exception:
                        nav_bounds = None
                    if nav_bounds:
                        try:
                            left, top, navw, navh = nav_bounds
                            x = int(left)
                            y = int(top) - btn_w - AndroidUtilities.dp(12)
                        except Exception:
                            pass
            min_x = AndroidUtilities.dp(4)
            max_x = host_w - btn_w - AndroidUtilities.dp(4)
            if max_x < min_x:
                max_x = min_x
            if x < min_x:
                x = min_x
            if x > max_x:
                x = max_x
            min_y = AndroidUtilities.dp(84)
            max_y = host_h - btn_w - AndroidUtilities.dp(10)
            if max_y < min_y:
                max_y = min_y
            if y < min_y:
                y = min_y
            if y > max_y:
                y = max_y
            try:
                btn.setX(float(max(0, x)))
                btn.setY(float(max(0, y)))
                btn.bringToFront()
            except Exception:
                pass
        except Exception:
            pass

    def _start_chat_fab_position_tracker(self):
        try:
            self._stop_chat_fab_position_tracker()
        except Exception:
            pass
        stop_evt = threading.Event()
        self._chat_fab_pos_stop = stop_evt
        def _loop():
            while not stop_evt.is_set():
                try:
                    run_on_ui_thread(self._update_chat_fab_position_once)
                except Exception:
                    pass
                try:
                    if stop_evt.wait(0.50):
                        break
                except Exception:
                    time.sleep(0.50)
        try:
            th = threading.Thread(target=_loop, daemon=True)
            self._chat_fab_pos_thread = th
            th.start()
        except Exception:
            self._chat_fab_pos_thread = None

    def _stop_chat_fab_position_tracker(self):
        try:
            evt = getattr(self, "_chat_fab_pos_stop", None)
            if evt:
                evt.set()
        except Exception:
            pass
        try:
            self._chat_fab_pos_stop = None
            self._chat_fab_pos_thread = None
        except Exception:
            pass

    def _open_chat_fab_sheet(self, control_only=False, forced_fragment=None, allow_anywhere=False, force_chatlist_mode=None):
        try:
            fragment = forced_fragment or get_last_fragment()
            if fragment is None:
                try:
                    fragment = getattr(self, "_chat_fab_fragment", None)
                except Exception:
                    fragment = None
            is_chat = isinstance(fragment, ChatActivity)
            is_dialogs = self._is_dialogs_fragment(fragment)
            if (not allow_anywhere) and (not is_chat) and (not (is_dialogs and self._is_quick_flow_list_enabled())):
                return
            try:
                self._chat_fab_fragment = fragment
            except Exception:
                pass
            try:
                self._preview_fragment_hint = fragment
            except Exception:
                pass
            ctx = fragment.getParentActivity() if fragment and fragment.getParentActivity() else ApplicationLoader.applicationContext
            if not ctx:
                return
            layout_helper = find_class("org.telegram.ui.Components.LayoutHelper")
            sheet = BottomSheet(ctx, True)
            try:
                self._chat_fab_sheet_ref = sheet
            except Exception:
                pass
            root = LinearLayout(ctx)
            root.setOrientation(LinearLayout.VERTICAL)
            try:
                root.setPadding(AndroidUtilities.dp(0), AndroidUtilities.dp(0), AndroidUtilities.dp(0), AndroidUtilities.dp(0))
            except Exception:
                pass
            try:
                self._fab_force_apple_tab = True
            except Exception:
                pass
            try:
                if force_chatlist_mode is None:
                    self._fab_chatlist_mode = bool(is_dialogs)
                else:
                    self._fab_chatlist_mode = bool(force_chatlist_mode)
            except Exception:
                pass
            try:
                self._fab_open_control_page = bool(control_only)
            except Exception:
                pass
            tab_view = create_nowfy_tab_view(ctx, self)
            try:
                self._fab_force_apple_tab = False
            except Exception:
                pass
            try:
                self._fab_open_control_page = False
            except Exception:
                pass
            try:
                self._fab_chatlist_mode = False
            except Exception:
                pass
            if tab_view is not None:
                try:
                    root.addView(tab_view, LinearLayout.LayoutParams(-1, -2))
                except Exception:
                    if layout_helper:
                        root.addView(tab_view, layout_helper.createLinear(-1, -2))
                    else:
                        root.addView(tab_view)
            else:
                placeholder = TextView(ctx)
                placeholder.setText(tr("nowfy_tab_status_no_track"))
                try:
                    placeholder.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
                except Exception:
                    pass
                try:
                    placeholder.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(12), AndroidUtilities.dp(16), AndroidUtilities.dp(16))
                except Exception:
                    pass
                root.addView(placeholder, LinearLayout.LayoutParams(-1, -2))
            sheet.setCustomView(root)
            try:
                sheet.show()
            except Exception:
                return
            try:
                self._style_chat_fab_sheet_surface(sheet)
            except Exception:
                pass
        except Exception:
            pass

    def _close_chat_fab_sheet(self):
        try:
            sheet = getattr(self, "_chat_fab_sheet_ref", None)
            if sheet is not None:
                sheet.dismiss()
        except Exception:
            pass
        finally:
            try:
                self._chat_fab_sheet_ref = None
            except Exception:
                pass

    def _style_chat_fab_sheet_surface(self, sheet):
        if not sheet:
            return
        dev_transparent = False
        try:
            dev_transparent = bool(self.get_setting("nowfy_flow_bt_debug", True))
        except Exception:
            dev_transparent = True
        targets = []
        for fname in ("containerView", "container", "sheetContainer", "sheetView"):
            try:
                v = get_private_field(sheet, fname)
            except Exception:
                v = None
            if v is not None and v not in targets:
                targets.append(v)
        for v in targets:
            try:
                bg = GradientDrawable()
                if dev_transparent:
                    bg.setColor(0x00000000)
                else:
                    bg.setColor(0xFF16233A)
                r = AndroidUtilities.dp(22)
                try:
                    bg.setCornerRadius(r)
                except Exception:
                    bg.setCornerRadius(r)
                v.setBackground(bg)
                try:
                    v.setAlpha(1.0)
                except Exception:
                    pass
            except Exception:
                pass
        try:
            w = sheet.getWindow()
        except Exception:
            w = None
        if w is None:
            return
        try:
            win_bg = GradientDrawable()
            win_bg.setColor(0x00000000)
            w.setBackgroundDrawable(win_bg)
        except Exception:
            pass
        if dev_transparent:
            try:
                w.setDimAmount(0.0)
            except Exception:
                pass
            try:
                w.clearFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND)
            except Exception:
                pass
            try:
                if int(Build.VERSION.SDK_INT) >= 31:
                    w.setBackgroundBlurRadius(0)
            except Exception:
                pass
        else:
            try:
                w.setDimAmount(0.35)
            except Exception:
                pass
            try:
                w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND)
            except Exception:
                pass

    def _get_nowfy_flow_side(self):
        try:
            raw = self.get_setting("nowfy_flow_side", 0)
        except Exception:
            raw = 0
        try:
            if isinstance(raw, str):
                rv = raw.strip().lower()
                if rv in ("left", "0"):
                    return 0
                if rv in ("right", "1"):
                    return 1
                if rv in ("free", "2"):
                    return 2
            v = int(raw)
        except Exception:
            v = 0
        if v < 0:
            v = 0
        if v > 2:
            v = 2
        return v

    def _reset_nowfy_flow_free_position(self):
        try:
            self.set_setting("nowfy_flow_free_x", -1)
            self.set_setting("nowfy_flow_free_y", -1)
        except Exception:
            pass

    def _get_nowfy_flow_free_position(self):
        try:
            rx = int(self.get_setting("nowfy_flow_free_x", -1) or -1)
        except Exception:
            rx = -1
        try:
            ry = int(self.get_setting("nowfy_flow_free_y", -1) or -1)
        except Exception:
            ry = -1
        return (rx, ry)

    def _save_nowfy_flow_free_position(self, x, y):
        try:
            self.set_setting("nowfy_flow_free_x", int(x))
            self.set_setting("nowfy_flow_free_y", int(y))
        except Exception:
            pass

    def _get_nowfy_quick_flow_side_mode(self):
        try:
            raw = self.get_setting("nowfy_quick_flow_side_mode", 0)
            v = int(raw)
        except Exception:
            v = 0
        if v < 0:
            v = 0
        if v > 1:
            v = 1
        return v

    def _reset_nowfy_quick_flow_free_position(self):
        try:
            self.set_setting("nowfy_quick_flow_free_x", -1)
            self.set_setting("nowfy_quick_flow_free_y", -1)
        except Exception:
            pass

    def _get_nowfy_quick_flow_free_position(self):
        try:
            rx = int(self.get_setting("nowfy_quick_flow_free_x", -1) or -1)
        except Exception:
            rx = -1
        try:
            ry = int(self.get_setting("nowfy_quick_flow_free_y", -1) or -1)
        except Exception:
            ry = -1
        return (rx, ry)

    def _save_nowfy_quick_flow_free_position(self, x, y):
        try:
            self.set_setting("nowfy_quick_flow_free_x", int(x))
            self.set_setting("nowfy_quick_flow_free_y", int(y))
        except Exception:
            pass

    def _get_nowfy_flow_transparency_mode(self):
        try:
            raw = self.get_setting("nowfy_flow_transparency", 0)
        except Exception:
            raw = 0
        try:
            if isinstance(raw, str):
                rv = raw.strip().lower()
                if rv in ("default", "0"):
                    return 0
                if rv in ("50", "50%", "1"):
                    return 1
                if rv in ("70", "70%", "2"):
                    return 2
            v = int(raw)
        except Exception:
            v = 0
        if v < 0:
            v = 0
        if v > 2:
            v = 2
        return v

    def _get_nowfy_flow_button_alpha(self):
        mode = self._get_nowfy_flow_transparency_mode()
        if mode == 1:
            return 0.5
        if mode == 2:
            return 0.3
        return 1.0

    def _apply_chat_fab_visual(self):
        try:
            btn = getattr(self, "_chat_fab_button", None)
            if btn is None:
                return
            is_dialogs = bool(getattr(self, "_chat_fab_is_dialogs", False))
            alpha = 1.0 if is_dialogs else float(self._get_nowfy_flow_button_alpha())
            if alpha < 0.1:
                alpha = 0.1
            if alpha > 1.0:
                alpha = 1.0
            btn.setAlpha(alpha)
        except Exception:
            pass

    def _configurar_hook_cabecalho(self):
        try:
            PSA = find_class("com.exteragram.messenger.plugins.ui.PluginSettingsActivity")
            if not PSA:
                return
            method = PSA.getClass().getDeclaredMethod(
                "fillItems",
                find_class("java.util.ArrayList"),
                find_class("org.telegram.ui.Components.UniversalAdapter")
            )
            method.setAccessible(True)
            self.hook_settings_header_ref = self.hook_method(method, NowfySettingsHeaderHook(self))
        except Exception:
            pass
        try:
            PSA = find_class("com.exteragram.messenger.plugins.ui.PluginSettingsActivity")
            if not PSA:
                return
            UItem = find_class("org.telegram.ui.Components.UItem")
            ViewClass = find_class("android.view.View")
            IntType = find_class("java.lang.Integer").TYPE
            FloatType = find_class("java.lang.Float").TYPE
            click_method = PSA.getClass().getDeclaredMethod("onClick", UItem, ViewClass, IntType, FloatType, FloatType)
            click_method.setAccessible(True)
            self.hook_settings_onclick_ref = self.hook_method(click_method, NowfyPanelRoundCheckboxClickHook(self))
        except Exception:
            pass

    def _setup_track_hub_profile_hooks(self):
        try:
            try:
                log("[Nowfy][TrackHub] setup hooks: starting")
            except Exception:
                pass
            IntType = jclass("java.lang.Integer").TYPE
            VH = jclass("androidx.recyclerview.widget.RecyclerView$ViewHolder")
            ProfileActivity = find_class("org.telegram.ui.ProfileActivity")
            Adapter = find_class("org.telegram.ui.ProfileActivity$ListAdapter")
            if not ProfileActivity or not Adapter or not VH:
                try:
                    log(f"[Nowfy][TrackHub] setup hooks: class missing Profile={bool(ProfileActivity)} Adapter={bool(Adapter)} VH={bool(VH)}")
                except Exception:
                    pass
                return
            if not self._track_hub_rows_hook_ref:
                m_rows = None
                try:
                    m_rows = ProfileActivity.getClass().getDeclaredMethod("updateRowsIds")
                except Exception:
                    try:
                        m_rows = ProfileActivity.getClass().getDeclaredMethod("updateRows")
                    except Exception:
                        pass
                if not m_rows:
                    try:
                        methods = ProfileActivity.getClass().getDeclaredMethods()
                        for m in methods:
                            if str(m.getName()) in ("updateRowsIds", "updateRows") and len(m.getParameterTypes()) == 0:
                                m_rows = m
                                break
                    except Exception:
                        pass
                if not m_rows:
                    try:
                        log("[Nowfy][TrackHub] setup hooks: updateRowsIds not found")
                    except Exception:
                        pass
                    return
                m_rows.setAccessible(True)
                self._track_hub_rows_hook_ref = self.hook_method(m_rows, NowfyTrackHubRowsHook(self))
            if not self._track_hub_type_hook_ref:
                m_type = None
                try:
                    m_type = Adapter.getClass().getDeclaredMethod("getItemViewType", IntType)
                except Exception:
                    try:
                        methods = Adapter.getClass().getDeclaredMethods()
                        for m in methods:
                            if str(m.getName()) == "getItemViewType" and len(m.getParameterTypes()) == 1:
                                m_type = m
                                break
                    except Exception:
                        pass
                if not m_type:
                    try:
                        log("[Nowfy][TrackHub] setup hooks: getItemViewType not found")
                    except Exception:
                        pass
                else:
                    m_type.setAccessible(True)
                    self._track_hub_type_hook_ref = self.hook_method(m_type, NowfyTrackHubTypeHook(self))
            if not self._track_hub_bind_hook_ref:
                m_bind = None
                try:
                    m_bind = Adapter.getClass().getDeclaredMethod("onBindViewHolder", VH, IntType)
                except Exception:
                    try:
                        methods = Adapter.getClass().getDeclaredMethods()
                        for m in methods:
                            if str(m.getName()) == "onBindViewHolder" and len(m.getParameterTypes()) == 2:
                                m_bind = m
                                break
                    except Exception:
                        pass
                if not m_bind:
                    try:
                        log("[Nowfy][TrackHub] setup hooks: onBindViewHolder not found")
                    except Exception:
                        pass
                    return
                m_bind.setAccessible(True)
                self._track_hub_bind_hook_ref = self.hook_method(m_bind, NowfyTrackHubBindHook(self))
            try:
                log("[Nowfy][TrackHub] setup hooks: done")
            except Exception:
                pass
        except Exception as e:
            try:
                log(f"[Nowfy][TrackHub] setup hooks: failed ({str(e)})")
            except Exception:
                pass

    def _remove_track_hub_profile_hooks(self):
        try:
            if self._track_hub_rows_hook_ref:
                self.unhook_method(self._track_hub_rows_hook_ref)
                self._track_hub_rows_hook_ref = None
        except Exception:
            pass
        try:
            if self._track_hub_type_hook_ref:
                self.unhook_method(self._track_hub_type_hook_ref)
                self._track_hub_type_hook_ref = None
        except Exception:
            pass
        try:
            if self._track_hub_bind_hook_ref:
                self.unhook_method(self._track_hub_bind_hook_ref)
                self._track_hub_bind_hook_ref = None
        except Exception:
            pass
        try:
            self._track_hub_stop.set()
        except Exception:
            pass
        try:
            self._track_hub_thread = None
        except Exception:
            pass
        try:
            self._track_hub_profile_states = {}
        except Exception:
            pass

    def _extract_profile_id_for_track_hub(self, activity):
        try:
            f = activity.getClass().getDeclaredField("userId")
            f.setAccessible(True)
            v = f.getLong(activity)
            if int(v) != 0:
                return int(v)
        except Exception:
            pass
        try:
            f = activity.getClass().getDeclaredField("userInfo")
            f.setAccessible(True)
            info = f.get(activity)
            if info:
                u = getattr(info, "user", None)
                if u and int(getattr(u, "id", 0)) != 0:
                    return int(u.id)
        except Exception:
            pass
        try:
            uid = get_private_field(activity, "userId")
            if uid and int(uid) != 0:
                return int(uid)
        except Exception:
            pass
        return 0

    def _is_track_hub_target_user_profile(self, activity):
        try:
            if activity is None:
                return False
            try:
                chat_id = get_private_field(activity, "chatId")
                if chat_id is not None and int(chat_id) != 0:
                    return False
            except Exception:
                pass
            try:
                f = activity.getClass().getDeclaredField("chatId")
                f.setAccessible(True)
                if int(f.getLong(activity)) != 0:
                    return False
            except Exception:
                pass
            pid = int(self._extract_profile_id_for_track_hub(activity) or 0)
            return pid > 0
        except Exception:
            return False

    def _track_hub_remote_payload_exists(self, profile_id):
        try:
            pid = int(profile_id or 0)
            if pid <= 0:
                return False
            now_ts = int(time.time())
            cache = getattr(self, "_track_hub_remote_exists_cache", None)
            if not isinstance(cache, dict):
                cache = {}
            entry = cache.get(pid)
            if isinstance(entry, dict):
                ts = int(entry.get("ts", 0) or 0)
                if now_ts - ts < 60:
                    return bool(entry.get("ok", False))
            payload = self._track_hub_fetch_public_payload(pid)
            ok = isinstance(payload, dict) and bool(payload.get("title"))
            cache[pid] = {"ts": now_ts, "ok": bool(ok)}
            self._track_hub_remote_exists_cache = cache
            return bool(ok)
        except Exception:
            return False

    def _render_track_hub_profile_cell(self, cell, profile_id):
        try:
            from org.telegram.ui.Cells import TextDetailCell
            if not isinstance(cell, TextDetailCell):
                try:
                    log("[Nowfy][TrackHub] render: itemView is not TextDetailCell")
                except Exception:
                    pass
                return
        except Exception:
            return
        try:
            payload = self._track_hub_get_profile_payload(int(profile_id or 0), force_refresh=False) or {}
        except Exception:
            payload = {}
        title_text = str(payload.get("title", "") or "").strip() or tr("track_hub_empty_title")
        artist_text = str(payload.get("artist", "") or "").strip() or "Powered by Nowfy"
        is_playing = bool(payload.get("playing", False))
        player_label = str(payload.get("player", "") or "").strip()
        if not player_label:
            src = str(payload.get("source", "") or "").strip().lower()
            if src == "lastfm":
                player_label = "Last.fm"
            elif src == "statsfm":
                player_label = "Stats.fm"
            else:
                player_label = "Spotify"
        artist_upper = artist_text.upper()
        style_idx = 0
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "get_track_hub_style"):
                style_idx = int(NOWFY_CORE_API.get_track_hub_style(self) or 0)
            else:
                style_idx = int(self.get_setting("track_hub_style", 0) or 0)
        except Exception:
            style_idx = 0
        try:
            log(f"[Nowfy][TrackHub] render: pid={int(profile_id or 0)} title='{title_text}' artist='{artist_upper}' player='{player_label}'")
        except Exception:
            pass
        try:
            card = cell.findViewWithTag("nowfy_track_hub_card")
            if card:
                card.setVisibility(View.GONE)
        except Exception:
            pass
        try:
            subtitle = artist_upper if not is_playing else f"{artist_upper} \u2022 {player_label}"
            if style_idx == 1:
                if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "render_track_hub_box_cell"):
                    NOWFY_CORE_API.render_track_hub_box_cell(self, cell, title_text, subtitle, str(payload.get("cover_url", "") or ""))
                else:
                    self._render_track_hub_profile_cell_box(cell, title_text, subtitle, str(payload.get("cover_url", "") or ""))
            else:
                cell.setTextAndValue(title_text, subtitle, True)
                cell.textView.setVisibility(View.VISIBLE)
                cell.valueTextView.setVisibility(View.VISIBLE)
                cell.valueTextView.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText2))
        except Exception:
            pass
        try:
            if style_idx != 1:
                self._track_hub_add_open_button(cell, "msg_tone_on", (lambda: None))
        except Exception:
            pass
        try:
            cell.setOnClickListener(OnClickListener(lambda v: None))
            try:
                cell.setClickable(False)
                cell.setEnabled(True)
            except Exception:
                pass
        except Exception:
            pass
        try:
            cell.setOnLongClickListener(None)
        except Exception:
            pass

    def _render_track_hub_profile_cell_box(self, cell, title_text, subtitle_text, cover_url=""):
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "render_track_hub_box_cell"):
                NOWFY_CORE_API.render_track_hub_box_cell(self, cell, title_text, subtitle_text, cover_url)
                return
        except Exception:
            pass

    def _track_hub_clear_cell_extras(self, cell):
        try:
            btn = cell.findViewWithTag("nowfy_track_hub_btn")
            if btn:
                try:
                    btn.setOnClickListener(None)
                except Exception:
                    pass
                try:
                    btn.setVisibility(View.GONE)
                except Exception:
                    pass
                try:
                    parent = btn.getParent()
                    if parent:
                        parent.removeView(btn)
                except Exception:
                    pass
        except Exception:
            pass
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "clear_track_hub_box_cell"):
                NOWFY_CORE_API.clear_track_hub_box_cell(self, cell)
        except Exception:
            pass

    def _track_hub_open_url(self, url):
        try:
            target = str(url or "").strip()
            if not target:
                try:
                    log("[Nowfy][TrackHub] open_url: empty")
                except Exception:
                    pass
                return
            if not target.startswith("http"):
                target = "https://" + target
            try:
                log(f"[Nowfy][TrackHub] open_url: target='{target[:180]}'")
            except Exception:
                pass
            def _open():
                try:
                    BrowserCls = find_class("org.telegram.messenger.browser.Browser")
                    frag = get_last_fragment()
                    if frag and hasattr(frag, "getParentActivity") and frag.getParentActivity():
                        BrowserCls.openUrl(frag.getParentActivity(), target)
                        try:
                            log("[Nowfy][TrackHub] open_url: Browser(activity) ok")
                        except Exception:
                            pass
                        return
                    BrowserCls.openUrl(ApplicationLoader.applicationContext, target)
                    try:
                        log("[Nowfy][TrackHub] open_url: Browser(appContext) ok")
                    except Exception:
                        pass
                    return
                except Exception as e:
                    try:
                        log(f"[Nowfy][TrackHub] open_url: Browser failed ({str(e)})")
                    except Exception:
                        pass
                try:
                    intent = Intent(Intent.ACTION_VIEW, Uri.parse(target))
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    ApplicationLoader.applicationContext.startActivity(intent)
                    try:
                        log("[Nowfy][TrackHub] open_url: Intent fallback ok")
                    except Exception:
                        pass
                except Exception as e:
                    try:
                        log(f"[Nowfy][TrackHub] open_url: Intent fallback failed ({str(e)})")
                    except Exception:
                        pass
            run_on_ui_thread(_open)
        except Exception:
            pass

    def _track_hub_add_open_button(self, cell, icon_name, on_click):
        try:
            tag = "nowfy_track_hub_btn"
            btn = cell.findViewWithTag(tag)
            ctx = cell.getContext()
            rn = str(icon_name or "msg_tone_on")
            if not btn:
                btn = ImageView(ctx)
                btn.setTag(tag)
                btn.setScaleType(ImageView.ScaleType.CENTER)
                lp = FrameLayout.LayoutParams(AndroidUtilities.dp(48), AndroidUtilities.dp(48))
                lp.gravity = Gravity.RIGHT | Gravity.CENTER_VERTICAL
                lp.rightMargin = AndroidUtilities.dp(12)
                btn.setLayoutParams(lp)
                btn.setBackground(Theme.createSimpleSelectorCircleDrawable(AndroidUtilities.dp(48), 0, Theme.getColor(Theme.key_listSelector)))
                cell.addView(btn)
            rid = ctx.getResources().getIdentifier(rn, "drawable", ctx.getPackageName())
            if rid == 0:
                rid = ctx.getResources().getIdentifier("msg_tone_on", "drawable", ctx.getPackageName())
            if rid != 0:
                btn.setImageResource(rid)
            btn.setColorFilter(PorterDuffColorFilter(Theme.getColor(Theme.key_switch2TrackChecked), PorterDuff.Mode.SRC_IN))
            def _btn_click(v):
                try:
                    log("[Nowfy][TrackHub] click: button")
                except Exception:
                    pass
                on_click()
            btn.setOnClickListener(OnClickListener(_btn_click))
            try:
                btn.setClickable(True)
                btn.setFocusable(True)
            except Exception:
                pass
            btn.setVisibility(View.VISIBLE)
        except Exception:
            pass

    def _start_track_hub_worker(self):
        try:
            self._track_hub_stop.clear()
        except Exception:
            pass
        try:
            if self._track_hub_thread and self._track_hub_thread.is_alive():
                return
        except Exception:
            pass
        def _loop():
            try:
                log("[Nowfy][TrackHub] worker: started")
            except Exception:
                pass
            while True:
                try:
                    if self._track_hub_stop.is_set():
                        try:
                            log("[Nowfy][TrackHub] worker: stop requested")
                        except Exception:
                            pass
                        break
                    if bool(self.get_setting("track_hub_enabled", False)):
                        try:
                            if (not self._track_hub_rows_hook_ref) or (not self._track_hub_bind_hook_ref):
                                self._setup_track_hub_profile_hooks()
                        except Exception:
                            pass
                        ok = bool(self._track_hub_publish_payload())
                        try:
                            log(f"[Nowfy][TrackHub] worker: publish={ok}")
                        except Exception:
                            pass
                        if ok:
                            try:
                                self._track_hub_refresh_visible_profiles()
                            except Exception:
                                pass
                except Exception:
                    pass
                try:
                    if self._track_hub_stop.wait(25):
                        break
                except Exception:
                    time.sleep(25)
            try:
                log("[Nowfy][TrackHub] worker: ended")
            except Exception:
                pass
        try:
            self._track_hub_thread = threading.Thread(target=_loop, daemon=True)
            self._track_hub_thread.start()
        except Exception:
            pass

    def _stop_track_hub_worker(self):
        try:
            self._track_hub_stop.set()
        except Exception:
            pass
        try:
            self._track_hub_thread = None
        except Exception:
            pass

    def _track_hub_refresh_visible_profiles(self):
        try:
            def _refresh():
                try:
                    states = dict(getattr(self, "_track_hub_profile_states", {}) or {})
                except Exception:
                    states = {}
                for activity, st in states.items():
                    try:
                        if not st or int(st.get("row", -1)) < 0:
                            continue
                        list_view = None
                        try:
                            list_view = get_private_field(activity, "listView")
                        except Exception:
                            list_view = None
                        if not list_view:
                            try:
                                f = activity.getClass().getDeclaredField("listView")
                                f.setAccessible(True)
                                list_view = f.get(activity)
                            except Exception:
                                list_view = None
                        if list_view and hasattr(list_view, "getAdapter"):
                            ad = list_view.getAdapter()
                            if ad:
                                ad.notifyDataSetChanged()
                    except Exception:
                        pass
            run_on_ui_thread(_refresh)
        except Exception:
            pass

    def _toggle_nowfy_tab(self, enabled):
        self.set_setting("nowfy_tab_enabled", bool(enabled))
        if enabled:
            self._setup_nowfy_tab_hooks()
            self._rebuild_nowfy_tab_current_emoji()
        else:
            self._remove_nowfy_tab_hooks()
            self._remove_nowfy_tab_from_current_emoji()
        self.reload_settings()

    def _rebuild_nowfy_tab_current_emoji(self):
        try:
            fragment = get_last_fragment()
            if not isinstance(fragment, ChatActivity):
                return
            enter_view = get_private_field(fragment, "chatActivityEnterView")
            emoji_view = get_private_field(enter_view, "emojiView") if enter_view else None
            if not emoji_view:
                return
            all_tabs = get_private_field(emoji_view, "allTabs")
            current_tabs = get_private_field(emoji_view, "currentTabs")
            if not all_tabs or not current_tabs:
                return
            old_tab = None
            for i in range(all_tabs.size()):
                t = all_tabs.get(i)
                if get_private_field(t, "type") == NOWFY_TAB_INDEX:
                    old_tab = t
                    break
            if old_tab:
                try:
                    if current_tabs.contains(old_tab):
                        current_tabs.remove(old_tab)
                except Exception:
                    pass
                try:
                    if all_tabs.contains(old_tab):
                        all_tabs.remove(old_tab)
                except Exception:
                    pass
            if bool(self.get_setting("nowfy_tab_enabled", True)):
                context = None
                try:
                    context = emoji_view.getContext()
                except Exception:
                    pass
                if context:
                    tab_class = get_java_class("org.telegram.ui.Components.EmojiView$Tab")
                    if tab_class:
                        ctor = tab_class.getDeclaredConstructors()[0]
                        ctor.setAccessible(True)
                        new_tab = ctor.newInstance(emoji_view)
                        set_private_field(new_tab, "type", Integer.valueOf(int(NOWFY_TAB_INDEX)))
                        set_private_field(new_tab, "view", create_nowfy_tab_view(context, self))
                        all_tabs.add(new_tab)
                        current_tabs.add(new_tab)
            run_on_ui_thread(lambda: force_update_ui(emoji_view))
        except Exception as e:
            log(f"[Nowfy] Tab rebuild failed: {e}")

    def _setup_nowfy_tab_hooks(self):
        if not hasattr(self, "_nowfy_tab_hooks"):
            self._nowfy_tab_hooks = []
        if self._nowfy_tab_hooks:
            return
        try:
            emoji_view = get_java_class("org.telegram.ui.Components.EmojiView")
            if not emoji_view:
                return
            base_fragment = get_java_class("org.telegram.ui.ActionBar.BaseFragment")
            resources_provider = get_java_class("org.telegram.ui.ActionBar.Theme$ResourcesProvider")
            chat_full = get_java_class("org.telegram.tgnet.TLRPC$ChatFull")
            context = get_java_class("android.content.Context")
            view_group = get_java_class("android.view.ViewGroup")
            ctor = find_constructor_exact(
                emoji_view,
                base_fragment,
                Boolean.TYPE,
                Boolean.TYPE,
                Boolean.TYPE,
                context,
                Boolean.TYPE,
                chat_full,
                view_group,
                Boolean.TYPE,
                resources_provider,
                Boolean.TYPE,
                Boolean.TYPE
            )
            if ctor is None:
                ctor = find_constructor_exact(
                    emoji_view,
                    base_fragment,
                    Boolean.TYPE,
                    Boolean.TYPE,
                    Boolean.TYPE,
                    context,
                    Boolean.TYPE,
                    chat_full,
                    view_group,
                    Boolean.TYPE,
                    resources_provider,
                    Boolean.TYPE
                )
            if ctor is None:
                return
            self._nowfy_tab_hooks.append(self.hook_method(ctor, NowfyEmojiViewConstructorHook(self)))
            set_allow = find_method_exact(emoji_view, "setAllow", Boolean.TYPE, Boolean.TYPE, Boolean.TYPE)
            if set_allow:
                self._nowfy_tab_hooks.append(self.hook_method(set_allow, NowfySetAllowHook(self)))
            check_grid = find_method_exact(emoji_view, "checkGridVisibility", Integer.TYPE, JFloat.TYPE)
            if check_grid and not bool(getattr(self, "_use_optimized_tab_visibility", True)):
                self._nowfy_tab_hooks.append(self.hook_method(check_grid, NowfyCheckGridVisibilityHook(self)))
            adapter_class = get_java_class("org.telegram.ui.Components.EmojiView$EmojiPagesAdapter")
            if adapter_class:
                get_icon = find_method_exact(adapter_class, "getPageIconDrawable", Integer.TYPE)
                if get_icon:
                    self._nowfy_tab_hooks.append(self.hook_method(get_icon, NowfyAdapterGetIconHook(self)))
                get_title = find_method_exact(adapter_class, "getPageTitle", Integer.TYPE)
                if get_title:
                    self._nowfy_tab_hooks.append(self.hook_method(get_title, NowfyAdapterGetTitleHook(self)))
        except Exception:
            pass

    def _remove_nowfy_tab_hooks(self):
        try:
            hooks = getattr(self, "_nowfy_tab_hooks", [])
            for h in hooks:
                try:
                    self.unhook_method(h)
                except Exception:
                    pass
            self._nowfy_tab_hooks = []
        except Exception:
            pass

    def _attach_emoji_pager_listener(self, emoji_view, my_view):
        pager = get_private_field(emoji_view, "pager")
        if not pager or not my_view:
            return
        Listener = find_class("androidx.viewpager.widget.ViewPager$OnPageChangeListener")
        if not Listener:
            Listener = find_class("android.support.v4.view.ViewPager$OnPageChangeListener")
        if not Listener:
            return
        class _OnPageChange(dynamic_proxy(Listener)):
            def onPageScrolled(self_obj, a, b, c):
                pass
            def onPageSelected(self_obj, pos):
                try:
                    if int(pos) == int(NOWFY_TAB_INDEX):
                        my_view.setVisibility(View.VISIBLE)
                    else:
                        my_view.setVisibility(View.INVISIBLE)
                except Exception:
                    pass
            def onPageScrollStateChanged(self_obj, state):
                pass
        listener = _OnPageChange()
        try:
            pager.addOnPageChangeListener(listener)
        except Exception:
            return
        try:
            current_item = int(pager.getCurrentItem())
            if current_item == int(NOWFY_TAB_INDEX):
                my_view.setVisibility(View.VISIBLE)
            else:
                my_view.setVisibility(View.INVISIBLE)
        except Exception:
            pass

    def _attach_nowfy_tab_open_listener(self, emoji_view):
        try:
            if not emoji_view:
                return
            try:
                refs = getattr(self, "_nowfy_tab_attach_listener_refs", None)
                if not isinstance(refs, dict):
                    refs = {}
                    self._nowfy_tab_attach_listener_refs = refs
            except Exception:
                refs = {}
                self._nowfy_tab_attach_listener_refs = refs
            try:
                vid = int(id(emoji_view))
            except Exception:
                vid = None
            if vid is not None and vid in refs:
                return
            plugin = self
            class _NowfyTabAttachListener(dynamic_proxy(View.OnAttachStateChangeListener)):
                def onViewAttachedToWindow(self, v):
                    try:
                        plugin._apply_nowfy_tab_priority_on_open(emoji_view)
                    except Exception:
                        pass
                def onViewDetachedFromWindow(self, v):
                    pass
            listener = _NowfyTabAttachListener()
            try:
                emoji_view.addOnAttachStateChangeListener(listener)
            except Exception:
                return
            if vid is not None:
                refs[vid] = listener
        except Exception:
            pass

    def _apply_nowfy_tab_priority_on_open(self, emoji_view):
        try:
            if not bool(self.get_setting("nowfy_tab_enabled", True)):
                return
            if int(self._get_nowfy_tab_priority_mode()) == 2:
                return
            now_ts = float(time.time())
            try:
                state_map = getattr(self, "_nowfy_tab_priority_state", None)
                if not isinstance(state_map, dict):
                    state_map = {}
                vid = int(id(emoji_view))
                last_ts = float(state_map.get(vid, 0.0) or 0.0)
                if (now_ts - last_ts) < 0.45:
                    return
                state_map[vid] = now_ts
                if len(state_map) > 40:
                    fresh = {}
                    for k, v in list(state_map.items()):
                        try:
                            if (now_ts - float(v or 0.0)) <= 30.0:
                                fresh[int(k)] = float(v)
                        except Exception:
                            pass
                    state_map = fresh
                self._nowfy_tab_priority_state = state_map
            except Exception:
                pass
            try:
                token_map = getattr(self, "_nowfy_tab_priority_tokens", None)
                if not isinstance(token_map, dict):
                    token_map = {}
                vid = int(id(emoji_view))
                token = int(token_map.get(vid, 0) or 0) + 1
                token_map[vid] = token
                self._nowfy_tab_priority_tokens = token_map
            except Exception:
                token = 0
            pager = get_private_field(emoji_view, "pager")
            if not pager:
                return
            target_index = -1
            try:
                current_tabs = get_private_field(emoji_view, "currentTabs")
                if current_tabs:
                    for i in range(current_tabs.size()):
                        t = current_tabs.get(i)
                        try:
                            tv = get_private_field(t, "view")
                        except Exception:
                            tv = None
                        try:
                            tag = str(tv.getTag()) if tv is not None else ""
                        except Exception:
                            tag = ""
                        if tag == str(NOWFY_TAB_VIEW_TAG):
                            target_index = int(i)
                            break
                        try:
                            if tv is not None and tv.findViewWithTag(NOWFY_TAB_VIEW_TAG):
                                target_index = int(i)
                                break
                        except Exception:
                            pass
            except Exception:
                target_index = -1
            if target_index < 0:
                return
            def _set_priority_tab_once():
                try:
                    if int(token) > 0:
                        tm = getattr(self, "_nowfy_tab_priority_tokens", {})
                        if int(tm.get(int(id(emoji_view)), 0) or 0) != int(token):
                            return
                except Exception:
                    pass
                try:
                    adapter = pager.getAdapter()
                except Exception:
                    adapter = None
                try:
                    count = int(adapter.getCount()) if adapter else 0
                except Exception:
                    count = 0
                if target_index < 0 or count <= int(target_index):
                    return
                try:
                    current = int(pager.getCurrentItem())
                except Exception:
                    current = -1
                if current != int(target_index):
                    try:
                        pager.setCurrentItem(int(target_index), False)
                    except Exception:
                        try:
                            pager.setCurrentItem(int(target_index))
                        except Exception:
                            pass
            run_on_ui_thread(_set_priority_tab_once)
            def _retry(ms):
                try:
                    def _run():
                        try:
                            if int(token) > 0:
                                tm = getattr(self, "_nowfy_tab_priority_tokens", {})
                                if int(tm.get(int(id(emoji_view)), 0) or 0) != int(token):
                                    return
                        except Exception:
                            pass
                        try:
                            run_on_ui_thread(_set_priority_tab_once)
                        except Exception:
                            pass
                    threading.Timer(float(ms) / 1000.0, _run).start()
                except Exception:
                    pass
            mode = int(self._get_nowfy_tab_priority_mode())
            if mode == 1:
                _retry(120)
                _retry(260)
                _retry(450)
                _retry(700)
                _retry(1000)
                _retry(1400)
                _retry(1800)
            else:
                _retry(120)
                _retry(260)
        except Exception:
            pass

    def _get_nowfy_tab_priority_mode(self):
        try:
            raw_mode = self.get_setting("nowfy_tab_priority_mode", None)
            if raw_mode is not None:
                mode = int(raw_mode)
                if mode < 0:
                    mode = 0
                if mode > 2:
                    mode = 2
                return mode
        except Exception:
            pass
        try:
            enabled = bool(self.get_setting("nowfy_tab_priority_enabled", True))
            return 0 if enabled else 2
        except Exception:
            return 0

    def _remove_nowfy_tab_from_current_emoji(self):
        try:
            fragment = get_last_fragment()
            if not isinstance(fragment, ChatActivity):
                return
            enter_view = get_private_field(fragment, "chatActivityEnterView")
            emoji_view = get_private_field(enter_view, "emojiView") if enter_view else None
            if not emoji_view:
                return
            all_tabs = get_private_field(emoji_view, "allTabs")
            current_tabs = get_private_field(emoji_view, "currentTabs")
            if not all_tabs or not current_tabs:
                return
            for i in range(all_tabs.size()):
                t = all_tabs.get(i)
                if get_private_field(t, "type") == NOWFY_TAB_INDEX:
                    if current_tabs.contains(t):
                        current_tabs.remove(t)
                    if all_tabs.contains(t):
                        all_tabs.remove(t)
                    break
            run_on_ui_thread(lambda: force_update_ui(emoji_view))
        except Exception:
            pass

    def _criar_header_base(self, context):
        try:
            from android.widget import FrameLayout, LinearLayout
            from org.telegram.ui.Components import LayoutHelper
            from android.view import Gravity
            container = FrameLayout(context)
            content = LinearLayout(context)
            content.setOrientation(LinearLayout.VERTICAL)
            container.addView(content, LayoutHelper.createFrame(-1, -2, Gravity.CENTER))
            return container, content
        except Exception:
            return None, None

    def _apply_link_aliases(self, items):
        try:
            try:
                iterator = iter(items)
                iterable_items = list(iterator)
            except Exception:
                iterable_items = None
            if iterable_items is None:
                try:
                    count = items.size()
                    iterable_items = [items.get(i) for i in range(count)]
                except Exception:
                    iterable_items = []
            for it in iterable_items:
                try:
                    if getattr(it, "no_link_alias", False):
                        continue
                    if getattr(it, "link_alias", None):
                        try:
                            si0 = getattr(it, "settingItem", None)
                            if si0 is not None and not getattr(si0, "link_alias", None):
                                si0.link_alias = getattr(it, "link_alias", None)
                        except Exception:
                            pass
                        continue
                    key = getattr(it, "key", None)
                    if key:
                        it.link_alias = key
                        try:
                            si = getattr(it, "settingItem", None)
                            if si is not None and not getattr(si, "link_alias", None):
                                si.link_alias = key
                        except Exception:
                            pass
                        continue
                    cb = getattr(it, "create_sub_fragment", None)
                    if cb:
                        try:
                            name = getattr(cb, "__name__", None)
                            if name:
                                it.link_alias = f"nowfy_{name}"
                                try:
                                    si = getattr(it, "settingItem", None)
                                    if si is not None and not getattr(si, "link_alias", None):
                                        si.link_alias = it.link_alias
                                except Exception:
                                    pass
                                continue
                        except Exception:
                            pass
                    click = getattr(it, "on_click", None)
                    text = getattr(it, "text", None)
                    if click and text:
                        it.link_alias = f"nowfy_action_{self._slug_alias(text)}"
                        try:
                            si = getattr(it, "settingItem", None)
                            if si is not None and not getattr(si, "link_alias", None):
                                si.link_alias = it.link_alias
                        except Exception:
                            pass
                        continue
                except Exception:
                    pass
        except Exception:
            pass
        return items

    def _slug_alias(self, text):
        try:
            s = str(text).strip().lower()
            s = re.sub(r"[^a-z0-9]+", "_", s)
            s = re.sub(r"_+", "_", s).strip("_")
            return s or "item"
        except Exception:
            return "item"

    def _get_uitem_setting_key(self, uitem):
        try:
            si = getattr(uitem, "settingItem", None)
            if not si:
                return None
            try:
                k = getattr(si, "key", None)
                if k:
                    return str(k)
            except Exception:
                pass
            try:
                m = si.getClass().getMethod("getKey")
                m.setAccessible(True)
                k = m.invoke(si)
                if k:
                    return str(k)
            except Exception:
                pass
            try:
                f = si.getClass().getDeclaredField("key")
                f.setAccessible(True)
                k = f.get(si)
                if k:
                    return str(k)
            except Exception:
                pass
        except Exception:
            pass
        return None

    def _get_uitem_text(self, uitem):
        try:
            if not uitem:
                return None
            try:
                t = getattr(uitem, "text", None)
                if t:
                    return str(t)
            except Exception:
                pass
            try:
                m = uitem.getClass().getMethod("getText")
                m.setAccessible(True)
                t = m.invoke(uitem)
                if t:
                    return str(t)
            except Exception:
                pass
            try:
                f = uitem.getClass().getDeclaredField("text")
                f.setAccessible(True)
                t = f.get(uitem)
                if t:
                    return str(t)
            except Exception:
                pass
        except Exception:
            pass
        return None

    def _inject_theme_skin_slides(self, activity, items):
        try:
            external_themes = self._get_external_themes()
            spotlight_index = len(external_themes) + 1
            vinify_index = spotlight_index + 1
            current_theme = int(self.get_setting("theme_selector", 0) or 0)
            if current_theme not in (0, spotlight_index, vinify_index):
                return
            from org.telegram.ui.Components import UItem
            from org.telegram.messenger import Utilities
            from java import dynamic_proxy, jarray, jclass
            insert_idx = -1
            remove_indices = []
            for i in range(items.size()):
                try:
                    it = items.get(i)
                    key = self._get_uitem_setting_key(it)
                    if key in ("theme_selector", "theme_selector_view"):
                        insert_idx = i + 1
                    elif key in ("spotlight_skin", "apple_skin", "vinify_skin_mode"):
                        remove_indices.append(i)
                except Exception:
                    pass
            for idx in reversed(remove_indices):
                try:
                    items.remove(idx)
                except Exception:
                    pass
            if insert_idx < 0:
                insert_idx = 0
            CallbackInterface = Utilities.Callback
            String = jclass("java.lang.String")
            plugin = self
            is_apple = current_theme == 0
            is_spotlight = current_theme == spotlight_index
            is_vinify = current_theme == vinify_index
            if is_apple:
                current_player = self._detect_current_player()
                if current_player == "SoundCloud":
                    skin_labels = ["Dark", tr("dynamic_skins_random")]
                    setting_key = "apple_skin"
                    current_skin = int(self.get_setting("apple_skin", 0) or 0)
                    current_skin = max(0, min(1, current_skin))
                else:
                    skin_labels = ["Light", "Dark", tr("dynamic_skins_random")]
                    setting_key = "apple_skin"
                    current_skin = int(self.get_setting("apple_skin", 0) or 0)
                    current_skin = max(0, min(2, current_skin))
            elif is_spotlight:
                skin_labels = ["Light", "Dark", "Blur", tr("dynamic_skins_random")]
                setting_key = "spotlight_skin"
                current_skin = int(self.get_setting("spotlight_skin", 0) or 0)
                current_skin = max(0, min(3, current_skin))
            elif is_vinify:
                skin_labels = ["Soft", "Focus", tr("vinify_skin_surprise")]
                setting_key = "vinify_skin_mode"
                current_skin = int(self.get_setting("vinify_skin_mode", 0) or 0)
                current_skin = max(0, min(2, current_skin))
            else:
                return
            max_idx = len(skin_labels) - 1
            class ThemeSlideCallback(dynamic_proxy(CallbackInterface)):
                def run(self, value):
                    try:
                        v = int(str(value))
                    except Exception:
                        v = 0
                    v = max(0, min(max_idx, v))
                    try:
                        plugin.set_setting(setting_key, v)
                    except Exception:
                        pass
                    try:
                        plugin.reload_settings()
                    except Exception:
                        pass
                    try:
                        lv = get_private_field(activity, "listView")
                        if lv is not None and getattr(lv, "adapter", None) is not None:
                            plugin._request_settings_list_update(lv, channel="theme_slide")
                    except Exception:
                        pass
            slide_items = jarray(String)(skin_labels)
            items.add(insert_idx, UItem.asSlideView(slide_items, current_skin, ThemeSlideCallback()))
            try:
                items.add(insert_idx + 1, UItem.asShadow())
            except Exception:
                pass
            if is_vinify and current_skin == 2:
                try:
                    rm = []
                    for i in range(items.size()):
                        try:
                            it = items.get(i)
                            remove = False
                            if str(getattr(it, "link_alias", "")) == "nowfy_themes_vinify_ui_options":
                                remove = True
                            if not remove:
                                try:
                                    txt = self._get_uitem_text(it) or ""
                                    if txt.strip().lower() == "vinify ui":
                                        remove = True
                                except Exception:
                                    pass
                            if not remove:
                                try:
                                    cb = getattr(it, "create_sub_fragment", None)
                                    if cb == self.create_vinify_ui_options:
                                        remove = True
                                except Exception:
                                    pass
                            if remove:
                                rm.append(i)
                        except Exception:
                            pass
                    for i in reversed(rm):
                        try:
                            items.remove(i)
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception:
            pass

    def _inject_link_options_slide(self, activity, items):
        try:
            from org.telegram.ui.Components import UItem
            from org.telegram.messenger import Utilities
            from java import dynamic_proxy, jarray, jclass
            try:
                show_track_link = bool(self.get_setting("show_track_link", True))
            except Exception:
                show_track_link = True
            insert_idx = -1
            remove_indices = []
            for i in range(items.size()):
                try:
                    it = items.get(i)
                    key = self._get_uitem_setting_key(it)
                    if key == "platform_links":
                        remove_indices.append(i)
                        if insert_idx < 0:
                            insert_idx = i
                except Exception:
                    pass
            if insert_idx < 0:
                return
            for idx in reversed(remove_indices):
                try:
                    items.remove(idx)
                except Exception:
                    pass
            if not show_track_link:
                return
            labels = ["Spotify", "Universal", tr("platform_links_both")]
            try:
                current = int(self.get_setting("platform_links", 0) or 0)
            except Exception:
                current = 0
            current = max(0, min(2, current))
            CallbackInterface = Utilities.Callback
            String = jclass("java.lang.String")
            plugin = self
            class _PlatformSlideCallback(dynamic_proxy(CallbackInterface)):
                def run(self, value):
                    try:
                        v = int(value)
                    except Exception:
                        v = 0
                    v = max(0, min(2, v))
                    try:
                        plugin.set_setting("platform_links", v)
                    except Exception:
                        pass
                    if v == 1:
                        try:
                            plugin.show_universal_link_dialog()
                        except Exception:
                            pass
            slide_items = jarray(String)(labels)
            items.add(insert_idx, UItem.asSlideView(slide_items, current, _PlatformSlideCallback()))
            try:
                items.add(insert_idx + 1, UItem.asShadow())
            except Exception:
                pass
        except Exception:
            pass

    def _inject_track_hub_source_slide(self, activity, items):
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_track_hub_source_slide"):
                NOWFY_CORE_API.inject_track_hub_source_slide(self, activity, items)
        except Exception:
            pass

    def _inject_nowtab_control_style_slide(self, activity, items):
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_nowtab_control_style_slide"):
                NOWFY_CORE_API.inject_nowtab_control_style_slide(self, activity, items)
        except Exception:
            pass


    def _inject_nowfy_flow_side_slide(self, activity, items):
        try:
            from org.telegram.ui.Components import UItem
            from org.telegram.messenger import Utilities
            from java import dynamic_proxy, jarray, jclass
            if not bool(self.get_setting("nowfy_flow_enabled", False)):
                return
            insert_idx = -1
            remove_indices = []
            for i in range(items.size()):
                try:
                    it = items.get(i)
                    key = self._get_uitem_setting_key(it)
                    if key == "nowfy_flow_side":
                        remove_indices.append(i)
                        if insert_idx < 0:
                            insert_idx = i
                except Exception:
                    pass
            if insert_idx < 0:
                return
            for idx in reversed(remove_indices):
                try:
                    items.remove(idx)
                except Exception:
                    pass
            current = self._get_nowfy_flow_side()
            labels = [tr("nowfy_flow_side_left"), tr("nowfy_flow_side_right"), tr("nowfy_flow_side_free")]
            CallbackInterface = Utilities.Callback
            String = jclass("java.lang.String")
            plugin = self
            class _FlowSideSlideCallback(dynamic_proxy(CallbackInterface)):
                def run(self, value):
                    try:
                        v = int(value)
                    except Exception:
                        v = 1
                    if v < 0:
                        v = 0
                    if v > 2:
                        v = 2
                    try:
                        plugin.set_setting("nowfy_flow_side", v)
                        if int(v) == 2:
                            plugin._reset_nowfy_flow_free_position()
                            plugin._maybe_show_flow_free_info_sheet()
                    except Exception:
                        pass
                    try:
                        plugin._update_chat_fab_position_once()
                    except Exception:
                        pass
                    try:
                        plugin._apply_chat_fab_state()
                    except Exception:
                        pass
                    try:
                        plugin.reload_settings()
                    except Exception:
                        pass
            slide_items = jarray(String)(labels)
            items.add(insert_idx, UItem.asSlideView(slide_items, current, _FlowSideSlideCallback()))
        except Exception:
            pass

    def _inject_nowfy_flow_transparency_slide(self, activity, items):
        try:
            from org.telegram.ui.Components import UItem
            from org.telegram.messenger import Utilities
            from java import dynamic_proxy, jarray, jclass
            if not bool(self.get_setting("nowfy_flow_enabled", False)):
                return
            insert_idx = -1
            remove_indices = []
            for i in range(items.size()):
                try:
                    it = items.get(i)
                    key = self._get_uitem_setting_key(it)
                    if key == "nowfy_flow_transparency":
                        remove_indices.append(i)
                        if insert_idx < 0:
                            insert_idx = i
                except Exception:
                    pass
            if insert_idx < 0:
                return
            for idx in reversed(remove_indices):
                try:
                    items.remove(idx)
                except Exception:
                    pass
            current = self._get_nowfy_flow_transparency_mode()
            labels = [tr("nowfy_flow_alpha_default"), "50%", "70%"]
            CallbackInterface = Utilities.Callback
            String = jclass("java.lang.String")
            plugin = self
            class _FlowTransparencySlideCallback(dynamic_proxy(CallbackInterface)):
                def run(self, value):
                    try:
                        v = int(value)
                    except Exception:
                        v = 0
                    if v < 0:
                        v = 0
                    if v > 2:
                        v = 2
                    try:
                        plugin.set_setting("nowfy_flow_transparency", v)
                    except Exception:
                        pass
                    try:
                        plugin._apply_chat_fab_visual()
                    except Exception:
                        pass
                    try:
                        plugin.reload_settings()
                    except Exception:
                        pass
            slide_items = jarray(String)(labels)
            items.add(insert_idx, UItem.asSlideView(slide_items, current, _FlowTransparencySlideCallback()))
        except Exception:
            pass

    def _inject_nowtab_lyrics_autoscroll_slide(self, activity, items):
        try:
            from org.telegram.ui.Components import UItem
            from org.telegram.messenger import Utilities
            from java import dynamic_proxy, jarray, jclass
            if not bool(self.get_setting("nowfy_lyrics_autoscroll_enabled", False)):
                return
            insert_idx = -1
            remove_indices = []
            for i in range(items.size()):
                try:
                    it = items.get(i)
                    key = self._get_uitem_setting_key(it)
                    if key == "nowfy_lyrics_autoscroll_speed":
                        remove_indices.append(i)
                        if insert_idx < 0:
                            insert_idx = i
                except Exception:
                    pass
            if insert_idx < 0:
                return
            for idx in reversed(remove_indices):
                try:
                    items.remove(idx)
                except Exception:
                    pass
            try:
                current = int(self.get_setting("nowfy_lyrics_autoscroll_speed", 0) or 0)
            except Exception:
                current = 0
            current = max(0, min(2, current))
            labels = [tr("color_default"), "2x", "3x"]
            CallbackInterface = Utilities.Callback
            String = jclass("java.lang.String")
            plugin = self
            class _LyricsAutoScrollSpeedSlideCallback(dynamic_proxy(CallbackInterface)):
                def run(self, value):
                    try:
                        v = int(value)
                    except Exception:
                        v = 0
                    v = max(0, min(2, v))
                    try:
                        plugin.set_setting("nowfy_lyrics_autoscroll_speed", v)
                    except Exception:
                        pass
            slide_items = jarray(String)(labels)
            items.add(insert_idx, UItem.asSlideView(slide_items, current, _LyricsAutoScrollSpeedSlideCallback()))
        except Exception:
            pass

    def _inject_nowfy_flow_style_buttons(self, activity, items):
        try:
            from org.telegram.ui.Components import UItem
            from android_utils import OnClickListener
            from android.widget import LinearLayout, TextView
            from android.view import Gravity
            from android.util import TypedValue
            from android.graphics.drawable import GradientDrawable
            insert_idx = -1
            remove_indices = []
            for i in range(items.size()):
                try:
                    it = items.get(i)
                    marker = str(getattr(it, "object2", "") or "")
                    if marker == "__nowfy_flow_style_custom__":
                        remove_indices.append(i)
                        continue
                    key = self._get_uitem_setting_key(it)
                    if key == "nowfy_flow_card_mode":
                        remove_indices.append(i)
                        if insert_idx < 0:
                            insert_idx = i
                except Exception:
                    pass
            if insert_idx < 0:
                return
            for idx in reversed(remove_indices):
                try:
                    items.remove(idx)
                except Exception:
                    pass
            ctx = activity.getContext()
            wrap = LinearLayout(ctx)
            wrap.setOrientation(LinearLayout.VERTICAL)
            try:
                wrap.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(8), AndroidUtilities.dp(16), AndroidUtilities.dp(8))
            except Exception:
                pass
            title = TextView(ctx)
            title.setText("")
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
            try:
                title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                title.setTextColor(0xFFFFFFFF)
            wrap.addView(title)
            row = LinearLayout(ctx)
            row.setOrientation(LinearLayout.HORIZONTAL)
            try:
                lp_row = LinearLayout.LayoutParams(-1, -2)
                lp_row.topMargin = AndroidUtilities.dp(8)
                row.setLayoutParams(lp_row)
            except Exception:
                pass
            try:
                bg = int(Theme.getColor(Theme.key_windowBackgroundWhite))
                r = (bg >> 16) & 0xFF
                g = (bg >> 8) & 0xFF
                b = bg & 0xFF
                is_dark_theme = (((r * 299 + g * 587 + b * 114) / 1000.0) < 150)
            except Exception:
                is_dark_theme = True
            try:
                current_mode = str(self.get_setting("nowfy_flow_card_mode", "cc") or "cc").strip().lower()
            except Exception:
                current_mode = "cc"
            current = 1 if current_mode == "cc" else 0
            def _btn_bg(selected):
                gd = GradientDrawable()
                try:
                    gd.setCornerRadius(AndroidUtilities.dp(12))
                except Exception:
                    pass
                if selected:
                    sel_bg = Color.parseColor("#3B82F6")
                    gd.setColor(sel_bg)
                    try:
                        gd.setStroke(AndroidUtilities.dp(1), sel_bg)
                    except Exception:
                        pass
                else:
                    if is_dark_theme:
                        gd.setColor(Color.parseColor("#242B36"))
                        try:
                            gd.setStroke(AndroidUtilities.dp(1), Color.parseColor("#30384A"))
                        except Exception:
                            pass
                    else:
                        gd.setColor(Color.parseColor("#E9EEF5"))
                        try:
                            gd.setStroke(AndroidUtilities.dp(1), Color.parseColor("#D1D9E6"))
                        except Exception:
                            pass
                return gd
            def _make_btn(text, selected):
                tv = TextView(ctx)
                tv.setText(str(text))
                tv.setGravity(Gravity.CENTER)
                tv.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
                try:
                    tv.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
                except Exception:
                    pass
                try:
                    tv.setBackground(_btn_bg(bool(selected)))
                except Exception:
                    pass
                try:
                    tv.setMinHeight(AndroidUtilities.dp(42))
                    tv.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(10), AndroidUtilities.dp(12), AndroidUtilities.dp(10))
                except Exception:
                    pass
                try:
                    tv.setTextColor(Color.parseColor("#FFFFFF" if selected else ("#F2F5FA" if is_dark_theme else "#1B2330")))
                except Exception:
                    pass
                return tv
            btn_default = _make_btn(tr("nowfy_flow_alpha_default"), current == 0)
            btn_compact = _make_btn(tr("nowfy_flow_style_compact"), current == 1)
            def _paint_state(sel_idx):
                try:
                    btn_default.setBackground(_btn_bg(sel_idx == 0))
                    btn_compact.setBackground(_btn_bg(sel_idx == 1))
                    btn_default.setTextColor(Color.parseColor("#FFFFFF" if sel_idx == 0 else ("#F2F5FA" if is_dark_theme else "#1B2330")))
                    btn_compact.setTextColor(Color.parseColor("#FFFFFF" if sel_idx == 1 else ("#F2F5FA" if is_dark_theme else "#1B2330")))
                except Exception:
                    pass
            def _apply_select(v):
                try:
                    vv = 1 if int(v) == 1 else 0
                except Exception:
                    vv = 0
                _paint_state(vv)
                try:
                    self.set_setting("nowfy_flow_card_mode", "cc" if vv == 1 else "default")
                except Exception:
                    pass
                try:
                    self.reload_settings()
                except Exception:
                    pass
            btn_default.setOnClickListener(OnClickListener(lambda v: _apply_select(0)))
            btn_compact.setOnClickListener(OnClickListener(lambda v: _apply_select(1)))
            _paint_state(current)
            try:
                lp_a = LinearLayout.LayoutParams(0, -2, 1.0)
                lp_b = LinearLayout.LayoutParams(0, -2, 1.0)
                lp_b.leftMargin = AndroidUtilities.dp(8)
                row.addView(btn_default, lp_a)
                row.addView(btn_compact, lp_b)
            except Exception:
                row.addView(btn_default)
                row.addView(btn_compact)
            wrap.addView(row)
            custom = UItem.asCustom(wrap)
            custom.object2 = "__nowfy_flow_style_custom__"
            items.add(insert_idx, custom)
        except Exception:
            pass

    def _inject_vinify_logo_position_radios(self, activity, items):
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_vinify_logo_position_radios"):
                if NOWFY_CORE_API.inject_vinify_logo_position_radios(self, activity, items):
                    return
        except Exception:
            pass

    def _inject_vinify_cover_shape_slide(self, activity, items):
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_vinify_cover_shape_slide"):
                NOWFY_CORE_API.inject_vinify_cover_shape_slide(self, activity, items)
        except Exception:
            pass

    def _inject_nowfy_pulse_style_slide(self, activity, items):
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_nowfy_pulse_style_slide"):
                NOWFY_CORE_API.inject_nowfy_pulse_style_slide(self, activity, items)
        except Exception:
            pass

    def _inject_custom_cover_slide(self, activity, items):
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_custom_cover_selector"):
                NOWFY_CORE_API.inject_custom_cover_selector(self, activity, items)
        except Exception:
            pass

    def _on_custom_cover_select(self, value):
        try:
            handled = False
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "on_custom_cover_select"):
                try:
                    handled = bool(NOWFY_CORE_API.on_custom_cover_select(self, value))
                except Exception:
                    handled = False
            if not handled:
                self.set_setting("custom_cover_selection", 1 if int(str(value)) == 1 else 0)
                self._apply_header_cover_settings_consistency()
            else:
                try:
                    self.set_setting("custom_cover_selection", 1 if int(str(value)) == 1 else 0)
                    self._apply_header_cover_settings_consistency()
                except Exception:
                    pass
        except Exception:
            pass

    def _on_custom_cover_toggle(self, enabled_value):
        try:
            handled = False
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "on_custom_cover_toggle"):
                try:
                    handled = bool(NOWFY_CORE_API.on_custom_cover_toggle(self, enabled_value))
                except Exception:
                    handled = False
            if not handled:
                enabled = bool(int(str(enabled_value))) if str(enabled_value).isdigit() else bool(enabled_value)
                self.set_setting("custom_cover_unlocked", enabled)
                if not enabled:
                    self.set_setting("custom_cover_selection", 0)
                self._apply_header_cover_settings_consistency()
            else:
                try:
                    enabled = bool(int(str(enabled_value))) if str(enabled_value).isdigit() else bool(enabled_value)
                    self.set_setting("custom_cover_unlocked", enabled)
                    if not enabled:
                        self.set_setting("custom_cover_selection", 0)
                    self._apply_header_cover_settings_consistency()
                except Exception:
                    pass
        except Exception:
            pass

    def _inject_panel_cache_round_checkboxes(self, activity, items):
        try:
            from org.telegram.ui.Components import UItem
            target_keys = ("enable_cache", "enable_preload")
            callbacks = {
                "enable_cache": (lambda v: self._toggle_cache_system(v)),
                "enable_preload": (lambda v: self._toggle_preload_system(v)),
            }
            defaults = {}
            cbs = {}
            for i in range(items.size()):
                try:
                    it = items.get(i)
                    key = self._get_uitem_setting_key(it)
                    if key not in target_keys:
                        continue
                    si = getattr(it, "settingItem", None)
                    text = key
                    default = False
                    on_change = None
                    try:
                        if si:
                            text = getattr(si, "text", None) or key
                            default = bool(getattr(si, "default", False))
                            on_change = getattr(si, "on_change", None)
                    except Exception:
                        pass
                    checked = bool(self.get_setting(key, default))
                    rc = UItem.asRoundCheckbox(hash(f"nowfy_{key}") & 0x7FFFFFFF, text)
                    rc.setChecked(checked)
                    rc.pad()
                    rc.object2 = key
                    items.set(i, rc)
                    defaults[key] = default
                    cbs[key] = callbacks.get(key, on_change)
                except Exception:
                    pass
            self._panel_round_defaults = defaults
            self._panel_round_callbacks = cbs
        except Exception:
            pass

    def _inject_nowtab_buttons_expandable(self, activity, items):
        try:
            from org.telegram.ui.Components import UItem
            from android_utils import OnClickListener
            try:
                if not bool(self.get_setting("nowfy_tab_enabled", True)):
                    return
            except Exception:
                return
            try:
                current_style = int(self.get_setting("nowfy_tab_style", 0) or 0)
            except Exception:
                current_style = 0
            if current_style != 0:
                return
            divider_text = tr("now_tab_buttons_divider")
            parent_text = tr("now_tab_buttons_title")
            try:
                srcs, _lbls = self._get_tab_source_options()
                src_idx = int(self.get_setting("nowfy_tab_source", 0) or 0)
                if src_idx < 0 or src_idx >= len(srcs):
                    src_idx = 0
                source_key = srcs[src_idx] if srcs else "spotify"
            except Exception:
                source_key = "spotify"
            supports_preview = True
            insert_idx = -1
            remove_indices = []
            for i in range(items.size()):
                try:
                    it = items.get(i)
                    key = self._get_uitem_setting_key(it)
                    si = getattr(it, "settingItem", None)
                    txt = ""
                    try:
                        txt = str(getattr(si, "text", "") or "")
                    except Exception:
                        txt = ""
                    if key in ("nowfy_lyrics_button", "nowfy_embed_button", "nowfy_control_enabled", "nowfy_music_preview_button", "nowfy_track_download_button"):
                        remove_indices.append(i)
                        if insert_idx < 0:
                            insert_idx = i
                    elif txt == divider_text and insert_idx < 0:
                        insert_idx = i + 1
                except Exception:
                    pass
            for idx in reversed(remove_indices):
                try:
                    items.remove(idx)
                except Exception:
                    pass
            if insert_idx < 0:
                insert_idx = items.size()
            lyr_on = int(self.get_setting("nowfy_lyrics_button", 1) or 0) == 1
            link_on = int(self.get_setting("nowfy_embed_button", 1) or 0) == 1
            try:
                _active_player = str(self._detect_current_player() or "").strip().lower()
                _control_allowed = (_active_player == "spotify")
            except Exception:
                _control_allowed = False
            if not _control_allowed:
                try:
                    _sources_ctrl, _labels_ctrl = self._get_tab_source_options()
                    _idx_ctrl = int(self.get_setting("nowfy_tab_source", 0) or 0)
                    if isinstance(_sources_ctrl, list) and _sources_ctrl:
                        if _idx_ctrl < 0 or _idx_ctrl >= len(_sources_ctrl):
                            _idx_ctrl = 0
                        _src_ctrl = str(_sources_ctrl[_idx_ctrl] or "").strip().lower()
                        _control_allowed = (_src_ctrl in ("spotify", "statsfm"))
                except Exception:
                    pass
            ctrl_on = bool(self.get_setting("nowfy_control_enabled", False)) and bool(_control_allowed)
            preview_on = int(self.get_setting("nowfy_music_preview_button", 1) or 0) == 1
            track_download_on = int(self.get_setting("nowfy_track_download_button", 1) or 0) == 1
            total_max = (5 if supports_preview else 4) - (0 if _control_allowed else 1)
            if total_max < 0:
                total_max = 0
            total_on = (1 if lyr_on else 0) + (1 if link_on else 0) + (1 if ctrl_on else 0) + (1 if track_download_on else 0) + ((1 if preview_on else 0) if supports_preview else 0)
            expanded = bool(getattr(self, "_nowtab_buttons_expanded", False))
            parent = UItem.asExteraExpandableSwitch(
                hash("nowfy_nowtab_buttons_expand") & 0x7FFFFFFF,
                parent_text,
                f"{total_on}/{total_max}",
                OnClickListener(lambda v: None)
            )
            parent.setChecked(total_on > 0)
            parent.setCollapsed(not expanded)
            parent.object2 = "__nowtab_buttons_parent__"
            items.add(insert_idx, parent)
            if expanded:
                child_lyrics = UItem.asRoundCheckbox(hash("nowfy_lyrics_button") & 0x7FFFFFFF, tr("lyrics_button"))
                child_lyrics.setChecked(lyr_on)
                child_lyrics.pad()
                child_lyrics.object2 = "nowfy_lyrics_button"
                items.add(insert_idx + 1, child_lyrics)
                child_link = UItem.asRoundCheckbox(hash("nowfy_embed_button") & 0x7FFFFFFF, tr("music_link"))
                child_link.setChecked(link_on)
                child_link.pad()
                child_link.object2 = "nowfy_embed_button"
                items.add(insert_idx + 2, child_link)
                next_idx = insert_idx + 3
                if _control_allowed:
                    child_control = UItem.asRoundCheckbox(hash("nowfy_control_enabled") & 0x7FFFFFFF, "Nowfy Control")
                    child_control.setChecked(ctrl_on)
                    child_control.pad()
                    child_control.object2 = "nowfy_control_enabled"
                    items.add(next_idx, child_control)
                    next_idx += 1
                child_track_download = UItem.asRoundCheckbox(hash("nowfy_track_download_button") & 0x7FFFFFFF, tr("nowfy_tab_button_track_download_title"))
                child_track_download.setChecked(track_download_on)
                child_track_download.pad()
                child_track_download.object2 = "nowfy_track_download_button"
                items.add(next_idx, child_track_download)
                next_idx += 1
                if supports_preview:
                    child_preview = UItem.asRoundCheckbox(hash("nowfy_music_preview_button") & 0x7FFFFFFF, tr("nowfy_tab_button_music_preview_title"))
                    child_preview.setChecked(preview_on)
                    child_preview.pad()
                    child_preview.object2 = "nowfy_music_preview_button"
                    items.add(next_idx, child_preview)
        except Exception:
            pass

    def _get_font_random_favorites(self):
        try:
            raw = str(self.get_setting("font_random_favorites", "") or "").strip()
            if not raw:
                return []
            out = []
            for part in raw.split(","):
                part = str(part).strip()
                if not part:
                    continue
                try:
                    v = int(part)
                except Exception:
                    continue
                if v >= 1:
                    out.append(v)
            return sorted(list(set(out)))
        except Exception:
            return []

    def _set_font_random_favorites(self, values):
        try:
            vals = []
            for v in (values or []):
                try:
                    i = int(v)
                except Exception:
                    continue
                if i >= 1:
                    vals.append(i)
            vals = sorted(list(set(vals)))
            self.set_setting("font_random_favorites", ",".join(str(x) for x in vals))
        except Exception:
            pass

    def _get_core_enabled_optional_themes(self):
        try:
            raw = str(self.get_setting("core_enabled_optional_themes", "") or "").strip()
            if raw == "__none__":
                return set()
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "get_core_setting"):
                raw_api = str(NOWFY_CORE_API.get_core_setting("core_enabled_optional_themes", "") or "").strip()
                if raw_api:
                    raw = raw_api
            if raw == "__none__":
                return set()
            if not raw:
                enabled = set()
                if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "is_theme_enabled"):
                    if NOWFY_CORE_API.is_theme_enabled(self, "core_theme_spotlight_enabled", False):
                        enabled.add("spotlight")
                    if NOWFY_CORE_API.is_theme_enabled(self, "core_theme_nowv_enabled", False):
                        enabled.add("nowv")
                elif any([
                    self.get_setting("core_theme_spotlight_enabled", None) is not None,
                    self.get_setting("core_theme_nowv_enabled", None) is not None,
                    self.get_setting("core_theme_nowv_enabled", None) is not None
                ]):
                    if bool(self.get_setting("core_theme_spotlight_enabled", False)):
                        enabled.add("spotlight")
                    if bool(self.get_setting("core_theme_nowv_enabled", False)):
                        enabled.add("nowv")
                else:
                    enabled = set()
                return enabled
            return set([x.strip().lower() for x in raw.split(",") if str(x).strip()])
        except Exception:
            return set()

    def _set_core_enabled_optional_themes(self, enabled_set):
        try:
            allowed = ["spotlight", "nowv"]
            clean = [k for k in allowed if k in set(enabled_set or set())]
            raw = ",".join(clean) if clean else "__none__"
            try:
                self.set_setting("core_enabled_optional_themes", raw)
            except Exception:
                pass
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "set_core_setting"):
                NOWFY_CORE_API.set_core_setting("core_enabled_optional_themes", raw)
                NOWFY_CORE_API.set_core_setting("core_theme_spotlight_enabled", ("spotlight" in clean))
                NOWFY_CORE_API.set_core_setting("core_theme_nowv_enabled", ("nowv" in clean))
            else:
                self.set_setting("core_theme_spotlight_enabled", ("spotlight" in clean))
                self.set_setting("core_theme_nowv_enabled", ("nowv" in clean))
        except Exception:
            pass

    def _inject_nowfycore_theme_multiselect(self, activity, items):
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_core_theme_multiselect"):
                if NOWFY_CORE_API.inject_core_theme_multiselect(self, activity, items):
                    return
        except Exception:
            pass

    def _inject_font_favorites_expandable(self, activity, items):
        try:
            from org.telegram.ui.Components import UItem
            from android_utils import OnClickListener
            try:
                font_selector = int(self.get_setting("font_selector", 0) or 0)
            except Exception:
                font_selector = 0
            if font_selector != 0:
                return
            insert_idx = -1
            remove_indices = []
            for i in range(items.size()):
                try:
                    it = items.get(i)
                    key = self._get_uitem_setting_key(it)
                    if key == "font_selector":
                        insert_idx = i + 1
                    k2 = str(getattr(it, "object2", "") or "")
                    if k2 == "__font_random_favorites_parent__" or k2.startswith("fontfav_"):
                        remove_indices.append(i)
                except Exception:
                    pass
            for idx in reversed(remove_indices):
                try:
                    items.remove(idx)
                except Exception:
                    pass
            if insert_idx < 0:
                return
            custom_fonts = self._list_custom_fonts()
            custom_font_labels = self._list_custom_fonts_display()
            font_items = [
                "SourceSansPro",
                "exteraCJK",
                "NotoNaskhArabic"
            ]
            if custom_fonts:
                font_items += custom_font_labels
            favs = set(self._get_font_random_favorites())
            max_idx = len(font_items)
            favs = set(i for i in favs if 1 <= int(i) <= max_idx)
            total_on = len(favs)
            expanded = bool(getattr(self, "_font_favorites_expanded", False))
            parent = UItem.asExteraExpandableSwitch(
                hash("nowfy_font_favorites_expand") & 0x7FFFFFFF,
                tr("font_favorites_title"),
                f"{total_on}/{max_idx}",
                OnClickListener(lambda v: None)
            )
            try:
                if hasattr(parent, "setIcon"):
                    parent.setIcon("msg_select_between_solar")
                elif hasattr(parent, "icon"):
                    parent.icon = "msg_select_between_solar"
                else:
                    si = getattr(parent, "settingItem", None)
                    if si is not None and hasattr(si, "icon"):
                        si.icon = "msg_select_between_solar"
            except Exception:
                pass
            parent.setChecked(total_on > 0)
            parent.setCollapsed(not expanded)
            parent.object2 = "__font_random_favorites_parent__"
            items.add(insert_idx, parent)
            if expanded:
                for idx, label in enumerate(font_items, start=1):
                    chk = UItem.asRoundCheckbox(hash(f"fontfav_{idx}") & 0x7FFFFFFF, str(label))
                    chk.setChecked(idx in favs)
                    chk.pad()
                    chk.object2 = f"fontfav_{idx}"
                    items.add(insert_idx + idx, chk)
        except Exception:
            pass

    def _inject_home_meta_custom(self, items, activity):
        try:
            from org.telegram.ui.Components import UItem
            from android.widget import LinearLayout, TextView, ImageView
            from android.view import Gravity
            from android.util import TypedValue
            from android.graphics.drawable import GradientDrawable
            from org.telegram.ui.ActionBar import Theme
            from android_utils import OnClickListener
            ctx = activity.getContext() if activity else None
            if not ctx:
                return
            target_map = {}
            remove_indices = []
            insert_idx = -1
            for i in range(items.size()):
                try:
                    it = items.get(i)
                    marker = str(getattr(it, "object2", "") or "")
                    if marker in ("__home_dotted_custom__", "__home_about_custom__", "__home_meta_custom__"):
                        if insert_idx < 0:
                            insert_idx = i
                        remove_indices.append(i)
                        continue
                    la = str(getattr(it, "link_alias", "") or "")
                    key = str(self._get_uitem_setting_key(it) or "")
                    if la in ("nowfy_credit_dotted", "nowfy_about_subfragment", "nowfy_home_meta") or key in ("nowfy_credit_dotted", "nowfy_about_subfragment", "nowfy_home_meta"):
                        if insert_idx < 0:
                            insert_idx = i
                        remove_indices.append(i)
                        if la:
                            target_map[la] = it
                        if key:
                            target_map[key] = it
                except Exception:
                    pass
            if insert_idx < 0:
                return
            for idx_rm in reversed(sorted(list(set(remove_indices)))):
                try:
                    items.remove(idx_rm)
                except Exception:
                    pass
            def _open_native(setting_key):
                try:
                    native_item = target_map.get(str(setting_key or "").strip())
                    if native_item is None or not activity:
                        return
                    UItemCls = find_class("org.telegram.ui.Components.UItem")
                    ViewCls = find_class("android.view.View")
                    IntType = find_class("java.lang.Integer").TYPE
                    FloatType = find_class("java.lang.Float").TYPE
                    if not UItemCls or not ViewCls or not IntType or not FloatType:
                        return
                    click_method = activity.getClass().getDeclaredMethod("onClick", UItemCls, ViewCls, IntType, FloatType, FloatType)
                    click_method.setAccessible(True)
                    run_on_ui_thread(lambda: click_method.invoke(activity, native_item, None, jint(0), JFloat(0.0), JFloat(0.0)))
                except Exception:
                    pass
            def _feature_like_card(icon_name, text, open_key):
                wrap = LinearLayout(ctx)
                wrap.setOrientation(LinearLayout.HORIZONTAL)
                wrap.setGravity(Gravity.CENTER_VERTICAL)
                try:
                    wrap.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(14), AndroidUtilities.dp(14), AndroidUtilities.dp(14))
                except Exception:
                    pass
                try:
                    bg = GradientDrawable()
                    bg.setCornerRadius(AndroidUtilities.dp(18))
                    bg.setColor(Theme.getColor(Theme.key_windowBackgroundWhite))
                    wrap.setBackground(bg)
                except Exception:
                    pass
                icon_box = LinearLayout(ctx)
                icon_box.setOrientation(LinearLayout.HORIZONTAL)
                icon_box.setGravity(Gravity.CENTER)
                try:
                    ibg = GradientDrawable()
                    ibg.setShape(GradientDrawable.OVAL)
                    ibg.setColor(0x14000000)
                    icon_box.setBackground(ibg)
                    icon_box.setPadding(AndroidUtilities.dp(10), AndroidUtilities.dp(10), AndroidUtilities.dp(10), AndroidUtilities.dp(10))
                except Exception:
                    pass
                iv = ImageView(ctx)
                try:
                    use_dotted_theme_icon = (str(icon_name or "").strip() == "__dotted_theme__")
                    if use_dotted_theme_icon:
                        try:
                            bg = int(Theme.getColor(Theme.key_windowBackgroundWhite))
                            r = ((bg >> 16) & 0xFF)
                            g = ((bg >> 8) & 0xFF)
                            b = (bg & 0xFF)
                            is_dark_theme = (((r * 299 + g * 587 + b * 114) / 1000.0) < 150)
                        except Exception:
                            is_dark_theme = True
                        file_name = "dotted_white.png" if is_dark_theme else "dotted_black.png"
                        urls = [
                            f"https://coreupdates.meyankut.workers.dev/{file_name}",
                            f"https://assets.nowfy/{file_name}",
                        ]
                        def _load_remote():
                            try:
                                BitmapFactoryLocal = find_class("android.graphics.BitmapFactory")
                                if not BitmapFactoryLocal:
                                    return
                                local_candidates = [
                                    os.path.join(os.path.dirname(__file__), "assets", "png", file_name),
                                    os.path.join(os.path.dirname(__file__), "nowfy", "assets", "png", file_name),
                                ]
                                for p in local_candidates:
                                    try:
                                        if p and os.path.isfile(p):
                                            bmp_local = BitmapFactoryLocal.decodeFile(p)
                                            if bmp_local:
                                                run_on_ui_thread(lambda b=bmp_local: iv.setImageBitmap(b))
                                                return
                                    except Exception:
                                        pass
                                data = None
                                headers = {
                                    "Accept": "image/*,*/*;q=0.8",
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
                                    "Cache-Control": "no-cache",
                                }
                                cache_key = f"home_dotted_{'dark' if is_dark_theme else 'light'}"
                                for u in urls:
                                    try:
                                        data = None
                                        if hasattr(self, "_get_cached_image_enhanced"):
                                            data = self._get_cached_image_enhanced(u, cache_key=cache_key)
                                        if not data:
                                            resp = requests.get(u, headers=headers, timeout=10)
                                            if resp.status_code == 200 and resp.content:
                                                data = resp.content
                                        if data:
                                            try:
                                                ctype = str(getattr(resp, "headers", {}).get("Content-Type", "") if 'resp' in locals() else "")
                                                if ctype and ("image" not in ctype.lower()):
                                                    data = None
                                                    continue
                                            except Exception:
                                                pass
                                            break
                                    except Exception:
                                        data = None
                                if not data:
                                    return
                                bmp = BitmapFactoryLocal.decodeByteArray(data, 0, len(data))
                                if bmp:
                                    run_on_ui_thread(lambda b=bmp: iv.setImageBitmap(b))
                            except Exception:
                                pass
                        run_on_queue(_load_remote)
                    else:
                        rid = ctx.getResources().getIdentifier(str(icon_name), "drawable", ctx.getPackageName())
                        if rid:
                            iv.setImageResource(rid)
                except Exception:
                    pass
                try:
                    if str(icon_name or "").strip() != "__dotted_theme__":
                        iv.setColorFilter(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
                except Exception:
                    pass
                try:
                    icon_box.addView(iv, LinearLayout.LayoutParams(AndroidUtilities.dp(22), AndroidUtilities.dp(22)))
                except Exception:
                    icon_box.addView(iv)
                wrap.addView(icon_box, LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT))
                tv = TextView(ctx)
                tv.setText(str(text or ""))
                tv.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
                try:
                    tv.setTypeface(AndroidUtilities.getTypeface("fonts/rmedium.ttf"))
                except Exception:
                    pass
                try:
                    tv.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
                except Exception:
                    pass
                lp_tv = LinearLayout.LayoutParams(-1, -2)
                lp_tv.leftMargin = AndroidUtilities.dp(12)
                wrap.addView(tv, lp_tv)
                try:
                    wrap.setClickable(True)
                    wrap.setFocusable(True)
                    wrap.setOnClickListener(OnClickListener(lambda v: _open_native(open_key)))
                except Exception:
                    pass
                try:
                    if str(open_key or "") == "nowfy_credit_dotted":
                        self_outer = self
                        class _DottedPreviewLong(dynamic_proxy(View.OnLongClickListener)):
                            def onLongClick(self, v):
                                try:
                                    return bool(self_outer._open_username_peek_preview("exteraDevPlugins"))
                                except Exception:
                                    return False
                        wrap.setOnLongClickListener(_DottedPreviewLong())
                except Exception:
                    pass
                return wrap
            dotted_view = _feature_like_card("__dotted_theme__", "Dotted Plugins", "nowfy_credit_dotted")
            about_view = _feature_like_card("msg_reactions", "Nowfy", "nowfy_about_subfragment")
            version_view = LinearLayout(ctx)
            version_view.setOrientation(LinearLayout.VERTICAL)
            version_view.setGravity(Gravity.CENTER_HORIZONTAL)
            try:
                version_view.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(12))
            except Exception:
                pass
            try:
                bgv = GradientDrawable()
                bgv.setCornerRadius(AndroidUtilities.dp(14))
                bgv.setColor(Theme.getColor(Theme.key_windowBackgroundWhite))
                version_view.setBackground(bgv)
            except Exception:
                pass
            icon_info = ImageView(ctx)
            try:
                rid_info = ctx.getResources().getIdentifier("msg_info", "drawable", ctx.getPackageName())
                if rid_info:
                    icon_info.setImageResource(rid_info)
                icon_info.setColorFilter(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                pass
            try:
                version_view.addView(icon_info, LinearLayout.LayoutParams(AndroidUtilities.dp(22), AndroidUtilities.dp(22)))
            except Exception:
                pass
            title = TextView(ctx)
            title.setText(f"v{__version__}")
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
            title.setGravity(Gravity.CENTER_HORIZONTAL)
            try:
                title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                pass
            version_view.addView(title)
            sub = TextView(ctx)
            sub.setText(f"by {__author__}")
            sub.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
            sub.setGravity(Gravity.CENTER_HORIZONTAL)
            try:
                sub.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            except Exception:
                pass
            version_view.addView(sub)
            try:
                version_view.setClickable(True)
                version_view.setFocusable(True)
                version_view.setOnClickListener(OnClickListener(lambda v: self._show_nowfy_update_bottom_sheet()))
            except Exception:
                pass
            def _with_insets(card_view, top_dp=0):
                outer = LinearLayout(ctx)
                outer.setOrientation(LinearLayout.VERTICAL)
                try:
                    outer.setPadding(AndroidUtilities.dp(16), 0, AndroidUtilities.dp(16), 0)
                except Exception:
                    pass
                try:
                    lp_card = LinearLayout.LayoutParams(-1, -2)
                    if int(top_dp or 0) > 0:
                        lp_card.topMargin = AndroidUtilities.dp(int(top_dp))
                    outer.addView(card_view, lp_card)
                except Exception:
                    outer.addView(card_view)
                return outer
            item_dotted = UItem.asCustom(_with_insets(dotted_view, 0))
            item_about = UItem.asCustom(_with_insets(about_view, 8))
            item_ver = UItem.asCustom(_with_insets(version_view, 8))
            try:
                item_dotted.object2 = "__home_dotted_custom__"
                item_about.object2 = "__home_about_custom__"
                item_ver.object2 = "__home_meta_custom__"
            except Exception:
                pass
            items.add(insert_idx, item_dotted)
            items.add(insert_idx + 1, item_about)
            items.add(insert_idx + 2, item_ver)
        except Exception:
            pass

    def _inject_statsfm_profile_custom(self, activity, items):
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_statsfm_profile_custom"):
                return NOWFY_CORE_API.inject_statsfm_profile_custom(self, activity, items)
        except Exception:
            pass

    def _inject_ymusic_profile_custom(self, activity, items):
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_ymusic_profile_custom"):
                return NOWFY_CORE_API.inject_ymusic_profile_custom(self, activity, items)
        except Exception:
            pass

    def _inject_services_cards_custom(self, activity, items):
        try:
            core_has_ymusic = bool(NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_ymusic_profile_custom"))
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_services_cards_custom") and core_has_ymusic:
                try:
                    log("[Nowfy][Services] bridge -> core injector")
                except Exception:
                    pass
                return NOWFY_CORE_API.inject_services_cards_custom(self, activity, items)
            try:
                if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_services_cards_custom") and (not core_has_ymusic):
                    log("[Nowfy][Services] legacy core detected, using native services list")
                else:
                    log("[Nowfy][Services] bridge missing core injector")
            except Exception:
                pass
        except Exception:
            try:
                import traceback
                log(f"[Nowfy][Services] bridge error: {traceback.format_exc()[:400]}")
            except Exception:
                pass

    def _inject_home_services_entry_custom(self, activity, items):
        try:
            try:
                log("[Nowfy][HomeServices] bridge -> core injector")
            except Exception:
                pass
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_home_services_entry_custom"):
                NOWFY_CORE_API.inject_home_services_entry_custom(self, activity, items)
                try:
                    has_custom = False
                    for i in range(items.size()):
                        try:
                            mk = str(getattr(items.get(i), "object2", "") or "")
                            if mk in ("__home_services_custom_entry__", "__home_feature_cards_custom_entry__", "__home_tail_cards_custom_entry__"):
                                has_custom = True
                                break
                        except Exception:
                            pass
                    if has_custom:
                        legacy_aliases = {
                            "nowfy_credit_dotted",
                            "nowfy_about_subfragment",
                        }
                        rm = []
                        for i in range(items.size()):
                            try:
                                it = items.get(i)
                                mk = str(getattr(it, "object2", "") or "")
                                if mk in ("__home_services_custom_entry__", "__home_feature_cards_custom_entry__", "__home_tail_cards_custom_entry__", "__home_dotted_custom__", "__home_about_custom__", "__home_meta_custom__"):
                                    continue
                                la = str(getattr(it, "link_alias", "") or "")
                                si = getattr(it, "settingItem", None)
                                if not la:
                                    la = str(getattr(si, "link_alias", "") or "") if si else ""
                                cb = (
                                    getattr(it, "create_sub_fragment", None)
                                    or getattr(it, "createSubFragment", None)
                                    or (getattr(si, "create_sub_fragment", None) if si else None)
                                    or (getattr(si, "createSubFragment", None) if si else None)
                                )
                                cb_name = str(getattr(cb, "__name__", "") or "").strip()
                                try:
                                    txt = str(self._get_uitem_text(it) or "").strip().lower()
                                except Exception:
                                    txt = str(getattr(si, "text", "") or "").strip().lower() if si else ""
                                if (
                                    la in legacy_aliases
                                    or cb_name in (
                                        "create_about_plugin_subfragment",
                                    )
                                    or txt in (
                                        "nowfy",
                                        "dotted plugins",
                                    )
                                ):
                                    rm.append(i)
                            except Exception:
                                pass
                        for idx in reversed(rm):
                            try:
                                items.remove(idx)
                            except Exception:
                                pass
                except Exception:
                    pass
                return
            try:
                log("[Nowfy][HomeServices] bridge missing core injector")
            except Exception:
                pass
        except Exception:
            try:
                import traceback
                log(f"[Nowfy][HomeServices] bridge error: {traceback.format_exc()[:400]}")
            except Exception:
                pass

    def _is_lastfm_verified_for_current_user(self):
        try:
            user = str(self.get_setting("lastfm_user", self.get_setting("lastfm_username", "")) or "").strip()
            api = str(self.get_setting("lastfm_api_key", "") or "").strip()
            if not user or not api:
                return False
            if not bool(self.get_setting("lastfm_account_verified", False)):
                return False
            verified_user = str(self.get_setting("lastfm_account_verified_user", "") or "").strip().lower()
            return bool(verified_user) and verified_user == user.lower()
        except Exception:
            return False

    def _get_lastfm_top_artists(self, username, limit=5):
        try:
            api_key = str(self.get_setting("lastfm_api_key", "") or "").strip()
            user = str(username or "").strip()
            if not api_key or not user:
                return []
            try:
                lim = int(limit)
            except Exception:
                lim = 5
            lim = max(1, min(10, lim))
            resp = requests.get(
                "https://ws.audioscrobbler.com/2.0/",
                params={
                    "method": "library.getartists",
                    "user": user,
                    "api_key": api_key,
                    "format": "json",
                    "limit": lim,
                    "page": 1
                },
                timeout=10,
                headers={"User-Agent": "Nowfy/1.1.1"}
            )
            if resp.status_code == 200:
                data = resp.json() if hasattr(resp, "json") else {}
                lib = data.get("artists", {}) if isinstance(data, dict) else {}
                artists = lib.get("artist", []) if isinstance(lib, dict) else []
                if isinstance(artists, dict):
                    artists = [artists]
                if isinstance(artists, list) and artists:
                    return artists[:lim]
            resp2 = requests.get(
                "https://ws.audioscrobbler.com/2.0/",
                params={
                    "method": "user.gettopartists",
                    "user": user,
                    "api_key": api_key,
                    "format": "json",
                    "limit": lim,
                    "period": "overall"
                },
                timeout=10,
                headers={"User-Agent": "Nowfy/1.1.1"}
            )
            if resp2.status_code != 200:
                return []
            data2 = resp2.json() if hasattr(resp2, "json") else {}
            top = data2.get("topartists", {}) if isinstance(data2, dict) else {}
            artists2 = top.get("artist", []) if isinstance(top, dict) else []
            if isinstance(artists2, dict):
                artists2 = [artists2]
            if not isinstance(artists2, list):
                return []
            return artists2[:lim]
        except Exception:
            return []

    def _normalize_https_url(self, url):
        try:
            u = str(url or "").strip()
            if not u:
                return ""
            if u.startswith("http://"):
                u = "https://" + u[7:]
            return u
        except Exception:
            return ""

    def _is_lastfm_placeholder_image(self, url):
        try:
            u = str(url or "").strip().lower()
            if not u:
                return True
            return ("2a96cbd8b46e442fc41c2b86b821562f" in u) or ("/noimage/" in u)
        except Exception:
            return True

    def _get_lastfm_artist_image_url(self, artist_obj):
        try:
            if not isinstance(artist_obj, dict):
                return ""
            images = artist_obj.get("image")
            if isinstance(images, list) and images:
                for img in reversed(images):
                    try:
                        if isinstance(img, dict):
                            u = self._normalize_https_url(img.get("#text"))
                            if u and not self._is_lastfm_placeholder_image(u):
                                return u
                    except Exception:
                        pass
            return ""
        except Exception:
            return ""

    def _get_lastfm_artist_image_url_from_info(self, artist_name):
        try:
            api_key = str(self.get_setting("lastfm_api_key", "") or "").strip()
            name = str(artist_name or "").strip()
            if not api_key or not name:
                return ""
            resp = requests.get(
                "https://ws.audioscrobbler.com/2.0/",
                params={
                    "method": "artist.getinfo",
                    "artist": name,
                    "api_key": api_key,
                    "format": "json",
                    "autocorrect": 1
                },
                timeout=8,
                headers={"User-Agent": "Nowfy/1.1.1"}
            )
            if resp.status_code != 200:
                return ""
            data = resp.json() if hasattr(resp, "json") else {}
            artist = data.get("artist", {}) if isinstance(data, dict) else {}
            if not isinstance(artist, dict):
                return ""
            return self._get_lastfm_artist_image_url(artist)
        except Exception:
            return ""

    def _get_deezer_artist_image_url(self, artist_name):
        try:
            name = str(artist_name or "").strip()
            if not name:
                return ""
            resp = requests.get(
                "https://api.deezer.com/search/artist",
                params={"q": name, "limit": 1},
                timeout=8,
                headers={"User-Agent": "Nowfy/1.1.1"}
            )
            if resp.status_code != 200:
                return ""
            data = resp.json() if hasattr(resp, "json") else {}
            arr = data.get("data", []) if isinstance(data, dict) else []
            if not isinstance(arr, list) or not arr:
                return ""
            a0 = arr[0] if isinstance(arr[0], dict) else {}
            url = self._normalize_https_url(a0.get("picture_xl") or a0.get("picture_big") or a0.get("picture_medium") or a0.get("picture"))
            return url if url else ""
        except Exception:
            return ""

    def _inject_lastfm_profile_custom(self, activity, items):
        try:
            from org.telegram.ui.Components import UItem
            from org.telegram.ui.ActionBar import Theme
            from android.widget import LinearLayout, TextView, ImageView
            from android.view import Gravity
            from android.util import TypedValue
            from android.graphics.drawable import GradientDrawable
            from android_utils import OnClickListener
            remove_indices = []
            for i in range(items.size()):
                try:
                    it = items.get(i)
                    marker = str(getattr(it, "object2", "") or "")
                    if marker in ("__lastfm_top_artists_custom__", "__lastfm_scrobbles_custom__"):
                        remove_indices.append(i)
                except Exception:
                    pass
            for idx in reversed(remove_indices):
                try:
                    items.remove(idx)
                except Exception:
                    pass
            if not self._is_lastfm_verified_for_current_user():
                return
            lastfm_user = str(self.get_setting("lastfm_user", self.get_setting("lastfm_username", "")) or "").strip()
            if not lastfm_user:
                return
            ctx = activity.getContext()
            artists_wrap = LinearLayout(ctx)
            artists_wrap.setOrientation(LinearLayout.VERTICAL)
            artists_wrap.setGravity(Gravity.CENTER_VERTICAL)
            try:
                artists_wrap.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(10), AndroidUtilities.dp(12), AndroidUtilities.dp(10))
            except Exception:
                pass
            try:
                bg1 = GradientDrawable()
                bg1.setCornerRadius(AndroidUtilities.dp(14))
                bg1.setColor(0x142A3A52)
                bg1.setStroke(AndroidUtilities.dp(1), 0x446FA8DC)
                artists_wrap.setBackground(bg1)
            except Exception:
                pass
            row = LinearLayout(ctx)
            row.setOrientation(LinearLayout.HORIZONTAL)
            row.setGravity(Gravity.CENTER_HORIZONTAL | Gravity.CENTER_VERTICAL)
            artists_wrap.addView(row, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT))
            artist_views = []
            for i in range(5):
                iv = ImageView(ctx)
                try:
                    iv.setScaleType(ImageView.ScaleType.CENTER_CROP)
                except Exception:
                    pass
                try:
                    ph = GradientDrawable()
                    ph.setShape(GradientDrawable.OVAL)
                    ph.setColor(0x263D4F6B)
                    iv.setBackground(ph)
                    try:
                        iv.setClipToOutline(True)
                    except Exception:
                        pass
                except Exception:
                    pass
                lp = LinearLayout.LayoutParams(AndroidUtilities.dp(46), AndroidUtilities.dp(46))
                try:
                    lp.leftMargin = AndroidUtilities.dp(5)
                    lp.rightMargin = AndroidUtilities.dp(5)
                    if i > 0:
                        lp.leftMargin = AndroidUtilities.dp(-4)
                except Exception:
                    pass
                row.addView(iv, lp)
                artist_views.append(iv)
            artists_item = UItem.asCustom(artists_wrap)
            artists_item.object2 = "__lastfm_top_artists_custom__"
            items.add(0, artists_item)
            sc_wrap = LinearLayout(ctx)
            sc_wrap.setOrientation(LinearLayout.VERTICAL)
            sc_wrap.setGravity(Gravity.CENTER_VERTICAL)
            try:
                sc_wrap.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(10), AndroidUtilities.dp(12), AndroidUtilities.dp(10))
            except Exception:
                pass
            try:
                bg2 = GradientDrawable()
                bg2.setCornerRadius(AndroidUtilities.dp(14))
                bg2.setColor(0x102A3A52)
                bg2.setStroke(AndroidUtilities.dp(1), 0x336FA8DC)
                sc_wrap.setBackground(bg2)
            except Exception:
                pass
            sc_title = TextView(ctx)
            sc_title.setText(tr("lastfm_scrobbles_title"))
            sc_title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
            try:
                sc_title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            except Exception:
                sc_title.setTextColor(0xFFD2DCEB)
            sc_wrap.addView(sc_title)
            sc_value = TextView(ctx)
            sc_value.setText("0")
            sc_value.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18)
            try:
                sc_value.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                sc_value.setTextColor(0xFFFFFFFF)
            sc_wrap.addView(sc_value)
            try:
                sc_wrap.setClickable(True)
                sc_wrap.setFocusable(True)
                sc_wrap.setOnClickListener(OnClickListener(lambda v: self._show_lastfm_listening_snapshot_sheet()))
            except Exception:
                pass
            sc_item = UItem.asCustom(sc_wrap)
            sc_item.object2 = "__lastfm_scrobbles_custom__"
            items.add(1, sc_item)
            def _load_lastfm_custom():
                try:
                    info = self._get_lastfm_user_info(lastfm_user)
                    if isinstance(info, dict):
                        cnt = str(info.get("playcount", "0") or "0")
                        run_on_ui_thread(lambda: sc_value.setText(cnt))
                    top = self._get_lastfm_top_artists(lastfm_user, limit=5)
                    for j, a in enumerate(top[:5]):
                        try:
                            artist_name = ""
                            try:
                                artist_name = str((a or {}).get("name") or "").strip()
                            except Exception:
                                artist_name = ""
                            url = self._get_lastfm_artist_image_url(a)
                            if not url and artist_name:
                                url = self._get_lastfm_artist_image_url_from_info(artist_name)
                            if not url and artist_name:
                                url = self._get_deezer_artist_image_url(artist_name)
                            if not url:
                                continue
                            data = self._get_cached_image_enhanced(url, cache_key=f"lastfm_top_artist_{hash(url)}")
                            if not data:
                                try:
                                    rr = requests.get(url, timeout=8, headers={"User-Agent": "Nowfy/1.1.1"})
                                    if rr.status_code == 200 and rr.content:
                                        data = rr.content
                                except Exception:
                                    data = None
                            if not data:
                                continue
                            bmp = BitmapFactory.decodeByteArray(data, 0, len(data))
                            if not bmp:
                                continue
                            def _apply(ix=j, b=bmp):
                                try:
                                    if 0 <= ix < len(artist_views):
                                        artist_views[ix].setImageBitmap(b)
                                except Exception:
                                    pass
                            run_on_ui_thread(_apply)
                        except Exception:
                            pass
                except Exception:
                    pass
            threading.Thread(target=_load_lastfm_custom, daemon=True).start()
        except Exception:
            pass

    def _format_count_with_commas(self, value):
        try:
            return f"{int(str(value or '0').replace(',', '').strip() or 0):,}"
        except Exception:
            return str(value or "0")

    def _get_lastfm_top_track_this_month(self, username):
        try:
            api_key = str(self.get_setting("lastfm_api_key", "") or "").strip()
            user = str(username or "").strip()
            if not api_key or not user:
                return ""
            resp = requests.get(
                "https://ws.audioscrobbler.com/2.0/",
                params={
                    "method": "user.gettoptracks",
                    "user": user,
                    "api_key": api_key,
                    "format": "json",
                    "limit": 1,
                    "period": "1month"
                },
                timeout=10,
                headers={"User-Agent": "Nowfy/1.1.1"}
            )
            if resp.status_code != 200:
                return ""
            data = resp.json() if hasattr(resp, "json") else {}
            top = data.get("toptracks", {}) if isinstance(data, dict) else {}
            tracks = top.get("track", []) if isinstance(top, dict) else []
            if isinstance(tracks, dict):
                tracks = [tracks]
            if not isinstance(tracks, list) or not tracks:
                return ""
            t0 = tracks[0] if isinstance(tracks[0], dict) else {}
            return str(t0.get("name") or "").strip()
        except Exception:
            return ""

    def _get_lastfm_top_artist_name(self, username):
        try:
            arr = self._get_lastfm_top_artists(username, limit=1)
            if not arr:
                return ""
            a0 = arr[0] if isinstance(arr[0], dict) else {}
            return str(a0.get("name") or "").strip()
        except Exception:
            return ""

    def _get_lastfm_listening_streak_days(self, username):
        try:
            api_key = str(self.get_setting("lastfm_api_key", "") or "").strip()
            user = str(username or "").strip()
            if not api_key or not user:
                return 0
            resp = requests.get(
                "https://ws.audioscrobbler.com/2.0/",
                params={
                    "method": "user.getrecenttracks",
                    "user": user,
                    "api_key": api_key,
                    "format": "json",
                    "limit": 200,
                    "page": 1
                },
                timeout=10,
                headers={"User-Agent": "Nowfy/1.1.1"}
            )
            if resp.status_code != 200:
                return 0
            data = resp.json() if hasattr(resp, "json") else {}
            rec = data.get("recenttracks", {}) if isinstance(data, dict) else {}
            tracks = rec.get("track", []) if isinstance(rec, dict) else []
            if isinstance(tracks, dict):
                tracks = [tracks]
            if not isinstance(tracks, list) or not tracks:
                return 0
            import datetime
            day_set = set()
            for t in tracks:
                try:
                    if not isinstance(t, dict):
                        continue
                    d = t.get("date", {})
                    uts = None
                    if isinstance(d, dict):
                        uts = d.get("uts")
                    if not uts:
                        continue
                    ts = int(str(uts).strip())
                    day_set.add(datetime.datetime.utcfromtimestamp(ts).date())
                except Exception:
                    pass
            if not day_set:
                return 0
            cursor = max(day_set)
            streak = 0
            delta = datetime.timedelta(days=1)
            while cursor in day_set:
                streak += 1
                cursor -= delta
            return int(streak)
        except Exception:
            return 0

    def _show_lastfm_listening_snapshot_sheet(self):
        try:
            if not self._is_lastfm_verified_for_current_user():
                return
            user = str(self.get_setting("lastfm_user", self.get_setting("lastfm_username", "")) or "").strip()
            if not user:
                return
            def _worker():
                try:
                    info = self._get_lastfm_user_info(user) or {}
                    total = self._format_count_with_commas(info.get("playcount", "0"))
                    since_year = tr("lastfm_snapshot_unknown")
                    try:
                        reg = info.get("registered", {}) if isinstance(info, dict) else {}
                        uts = None
                        if isinstance(reg, dict):
                            uts = reg.get("unixtime") or reg.get("#text")
                        if uts:
                            import datetime
                            since_year = str(datetime.datetime.utcfromtimestamp(int(str(uts))).year)
                    except Exception:
                        pass
                    top_artist = self._get_lastfm_top_artist_name(user) or tr("lastfm_snapshot_unknown")
                    top_track_month = self._get_lastfm_top_track_this_month(user) or tr("lastfm_snapshot_unknown")
                    streak_days = self._get_lastfm_listening_streak_days(user)
                    lines = [
                        tr("lastfm_snapshot_line_scrobbles").format(count=total),
                        tr("lastfm_snapshot_line_since").format(year=since_year),
                        tr("lastfm_snapshot_line_top_artist").format(artist=top_artist),
                        tr("lastfm_snapshot_line_top_track_month").format(track=top_track_month),
                        tr("lastfm_snapshot_line_streak").format(days=streak_days),
                    ]
                    message = "\n".join(lines)
                    run_on_ui_thread(lambda: self._show_spotify_info_bottom_sheet(
                        tr("lastfm_snapshot_title"),
                        None,
                        message,
                        (tr("spotify_control_understood")),
                        None
                    ))
                except Exception as e:
                    try:
                        log(f"[Nowfy] LastFM snapshot error: {e}")
                    except Exception:
                        pass
            threading.Thread(target=_worker, daemon=True).start()
        except Exception:
            pass

    def _show_nowfy_update_bottom_sheet(self):
        try:
            log("[Nowfy] Opening update test bottom sheet...")
            self._show_nowfy_update_bottom_sheet_fallback()
            return
        except Exception as e:
            try:
                log(f"[Nowfy] Update sheet open failed: {e}")
            except Exception:
                pass
            try:
                BulletinHelper.show_info("Failed to open update sheet")
            except Exception:
                pass

    def _open_username_peek_preview(self, username):
        try:
            uname = str(username or "").strip().lstrip("@")
            if not uname:
                return False
            frag = get_last_fragment()
            mc = get_messages_controller()
            if frag is None or mc is None:
                return False
            BundleCls = find_class("android.os.Bundle")
            ChatActivityCls = find_class("org.telegram.ui.ChatActivity")
            if BundleCls is None or ChatActivityCls is None:
                return False
            args = BundleCls()
            obj = None
            try:
                obj = mc.getUserOrChat(uname)
            except Exception:
                obj = None
            if obj is not None:
                try:
                    cname = str(obj.getClass().getName() or "")
                except Exception:
                    cname = ""
                try:
                    if "TLRPC$User" in cname:
                        uid = int(getattr(obj, "id", 0) or 0)
                        if uid > 0:
                            args.putLong("user_id", jlong(uid))
                    elif "TLRPC$Chat" in cname:
                        cid = int(getattr(obj, "id", 0) or 0)
                        if cid != 0:
                            args.putLong("chat_id", jlong(cid))
                except Exception:
                    pass
            try:
                has_ids = bool(args.getLong("user_id", 0) or args.getLong("chat_id", 0))
            except Exception:
                has_ids = False
            if not has_ids:
                try:
                    run_on_ui_thread(lambda: mc.openByUserName(uname, frag, 1))
                except Exception:
                    pass
                return True
            try:
                if hasattr(mc, "checkCanOpenChat") and (not bool(mc.checkCanOpenChat(args, frag))):
                    return False
            except Exception:
                pass

            def _open():
                try:
                    chat_frag = ChatActivityCls(args)
                    if hasattr(frag, "presentFragmentAsPreview"):
                        frag.presentFragmentAsPreview(chat_frag)
                        return
                    if hasattr(frag, "presentFragment"):
                        frag.presentFragment(chat_frag)
                        return
                    mc.openByUserName(uname, frag, 1)
                except Exception:
                    try:
                        mc.openByUserName(uname, frag, 1)
                    except Exception:
                        pass

            run_on_ui_thread(_open)
            return True
        except Exception:
            return False

    def _show_nowfy_update_bottom_sheet_fallback(self):
        frag = get_last_fragment()
        ctx = frag.getParentActivity() if frag and frag.getParentActivity() else ApplicationLoader.applicationContext
        if not ctx:
            return
        from org.telegram.ui.ActionBar import BottomSheet
        from org.telegram.ui.ActionBar import Theme
        from org.telegram.ui.Components import LayoutHelper
        from android.widget import LinearLayout, TextView, ImageView
        from android.view import Gravity
        from android.util import TypedValue
        from android.graphics.drawable import GradientDrawable
        from android_utils import OnClickListener
        sheet = BottomSheet(ctx, True)
        root = LinearLayout(ctx)
        root.setOrientation(LinearLayout.VERTICAL)
        try:
            root.setPadding(AndroidUtilities.dp(18), AndroidUtilities.dp(18), AndroidUtilities.dp(18), AndroidUtilities.dp(14))
        except Exception:
            pass
        hero = LinearLayout(ctx)
        hero.setOrientation(LinearLayout.HORIZONTAL)
        hero.setGravity(Gravity.CENTER_VERTICAL)
        logo = ImageView(ctx)
        try:
            logo.setScaleType(ImageView.ScaleType.CENTER_CROP)
        except Exception:
            pass
        try:
            from android.graphics.drawable import GradientDrawable as _GD
            ph = _GD()
            ph.setCornerRadius(AndroidUtilities.dp(10))
            try:
                ph.setColor(Theme.getColor(Theme.key_dialogBackgroundGray))
            except Exception:
                ph.setColor(0x223D4F6B)
            logo.setBackground(ph)
        except Exception:
            pass
        hero.addView(logo, LayoutHelper.createLinear(AndroidUtilities.dp(38), AndroidUtilities.dp(38), Gravity.CENTER_VERTICAL, 0, 0, AndroidUtilities.dp(10), 0))
        text_wrap = LinearLayout(ctx)
        text_wrap.setOrientation(LinearLayout.VERTICAL)
        title = TextView(ctx)
        title.setText(tr("nowfy_update_sheet_title"))
        title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 20)
        title.setGravity(Gravity.START)
        try:
            title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
        except Exception:
            title.setTextColor(0xFFFFFFFF)
        text_wrap.addView(title, LayoutHelper.createLinear(-1, -2))
        desc = TextView(ctx)
        desc.setText(tr("nowfy_update_sheet_message"))
        desc.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
        desc.setGravity(Gravity.START)
        try:
            desc.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
        except Exception:
            desc.setTextColor(0xFFFFFFFF)
        text_wrap.addView(desc, LayoutHelper.createLinear(-1, -2, Gravity.START, 0, AndroidUtilities.dp(4), 0, 0))
        hero.addView(text_wrap, LayoutHelper.createLinear(-1, -2, Gravity.CENTER_VERTICAL, 0, 0, 0, 0))
        root.addView(hero, LayoutHelper.createLinear(-1, -2))
        def _load_nowfy_logo():
            try:
                logo_url = "https://assets.nowfy/ageekapple.png"
                local_path = None
                try:
                    local_path = os.path.join(str(self._get_cache_dir()), "ageekapple.png")
                    if local_path and os.path.exists(local_path):
                        with open(local_path, "rb") as f:
                            local_data = f.read()
                        if local_data:
                            local_bmp = BitmapFactory.decodeByteArray(local_data, 0, len(local_data))
                            if local_bmp:
                                run_on_ui_thread(lambda: logo.setImageBitmap(local_bmp))
                                return
                except Exception:
                    pass
                data = self._get_cached_image_enhanced(logo_url, cache_key="nowfylogo")
                if not data:
                    return
                bmp = BitmapFactory.decodeByteArray(data, 0, len(data))
                if not bmp:
                    return
                try:
                    if local_path:
                        with open(local_path, "wb") as f:
                            f.write(data)
                except Exception:
                    pass
                run_on_ui_thread(lambda b=bmp: logo.setImageBitmap(b))
            except Exception:
                pass
        run_on_queue(_load_nowfy_logo)
        btn = TextView(ctx)
        btn.setText(tr("nowfy_update_sheet_button"))
        btn.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
        btn.setGravity(Gravity.CENTER)
        try:
            btn.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(10), AndroidUtilities.dp(16), AndroidUtilities.dp(10))
        except Exception:
            pass
        try:
            bg = GradientDrawable()
            bg.setCornerRadius(AndroidUtilities.dp(20))
            try:
                bg.setColor(Theme.getColor(Theme.key_featuredStickers_addButton))
            except Exception:
                bg.setColor(0xFF2B7FFF)
            try:
                bg.setStroke(AndroidUtilities.dp(2), Theme.getColor(Theme.key_dialogTextBlue))
            except Exception:
                bg.setStroke(AndroidUtilities.dp(2), 0xFF8FC1FF)
            btn.setBackground(bg)
            try:
                btn.setTextColor(Theme.getColor(Theme.key_featuredStickers_buttonText))
            except Exception:
                btn.setTextColor(0xFFFFFFFF)
        except Exception:
            pass
        btn.setOnClickListener(OnClickListener(lambda v: (self._open_nowfy_update_url(), sheet.dismiss())))
        root.addView(btn, LayoutHelper.createLinear(-1, -2, Gravity.TOP, 0, AndroidUtilities.dp(14), 0, 0))
        sheet.setCustomView(root)
        run_on_ui_thread(sheet.show)

    def _open_nowfy_update_url(self):
        try:
            frag = get_last_fragment()
            try:
                run_on_ui_thread(lambda: get_messages_controller().openByUserName("ApplesBio", frag, 1))
                return
            except Exception:
                pass
            update_url = "tg://resolve?domain=ApplesBio"
            try:
                Browser = find_class("org.telegram.messenger.browser.Browser")
                app_context = ApplicationLoader.applicationContext
                if Browser and app_context:
                    run_on_ui_thread(lambda: Browser.openUrl(app_context, update_url))
                    return
            except Exception:
                pass
            try:
                from android.content import Intent
                from android.net import Uri
                intent = Intent(Intent.ACTION_VIEW)
                intent.setData(Uri.parse(update_url))
                frag = get_last_fragment()
                activity = frag.getParentActivity() if frag else None
                if activity:
                    activity.startActivity(intent)
            except Exception:
                pass
        except Exception:
            pass

    def _criar_visualizacao_cabecalho(self, context):
        try:
            from android.widget import TextView
            from android.view import Gravity
            from android.util import TypedValue
            from org.telegram.ui.ActionBar import Theme
            from org.telegram.ui.Components import LayoutHelper, BackupImageView, AvatarDrawable
            from org.telegram.messenger import UserConfig
            from org.telegram.messenger import UserConfig, MessagesController
            container, content = self._criar_header_base(context)
            if not container or not content:
                return None
            try:
                cover_enabled = bool(self.get_setting("header_cover_enabled", True))
            except Exception:
                cover_enabled = True
            bg_cover = BackupImageView(context)
            try:
                self._header_fallback_url = None
                self._header_cover_last_url = ""
                self._header_cover_last_key = ""
                self._header_fallback_refresh = True
            except Exception:
                pass
            try:
                self._preload_header_fallback_covers()
            except Exception:
                pass
            try:
                self._header_cover_view = bg_cover
                self._start_header_cover_worker()
            except Exception:
                pass
            try:
                bg_cover.setRoundRadius(AndroidUtilities.dp(18))
            except Exception:
                pass
            try:
                cover_bg = GradientDrawable()
                cover_bg.setCornerRadius(AndroidUtilities.dp(18))
                cover_bg.setColor(Color.TRANSPARENT)
                bg_cover.setBackground(cover_bg)
                try:
                    bg_cover.setClipToOutline(True)
                except Exception:
                    pass
            except Exception:
                pass
            try:
                from android.widget import ImageView
                st = getattr(ImageView, "ScaleType", None)
                if st and getattr(st, "CENTER_CROP", None):
                    bg_cover.setScaleType(st.CENTER_CROP)
            except Exception:
                pass
            try:
                bg_cover.setVisibility(View.GONE)
            except Exception:
                pass
            try:
                bg_cover.setAlpha(0.0)
            except Exception:
                pass
            container.addView(
                bg_cover,
                0,
                LayoutHelper.createFrame(-1, 160, Gravity.CENTER_HORIZONTAL, 16, 46, 16, 12)
            )
            try:
                gif_cover = ImageView(context)
                try:
                    gif_cover.setScaleType(ImageView.ScaleType.CENTER_CROP)
                except Exception:
                    pass
                try:
                    gif_bg = GradientDrawable()
                    gif_bg.setCornerRadius(AndroidUtilities.dp(18))
                    gif_bg.setColor(Color.TRANSPARENT)
                    gif_cover.setBackground(gif_bg)
                    try:
                        gif_cover.setClipToOutline(True)
                    except Exception:
                        pass
                except Exception:
                    pass
                try:
                    gif_cover.setVisibility(View.GONE)
                except Exception:
                    pass
                try:
                    gif_cover.setAlpha(0.0)
                except Exception:
                    pass
                container.addView(
                    gif_cover,
                    1,
                    LayoutHelper.createFrame(-1, 160, Gravity.CENTER_HORIZONTAL, 16, 46, 16, 12)
                )
                self._header_cover_gif_view = gif_cover
            except Exception:
                self._header_cover_gif_view = None
            try:
                cover_shadow = View(context)
                try:
                    shadow_bg = GradientDrawable(
                        GradientDrawable.Orientation.BOTTOM_TOP,
                        [0xB8000000, 0x00000000]
                    )
                    shadow_bg.setCornerRadius(AndroidUtilities.dp(18))
                    cover_shadow.setBackground(shadow_bg)
                except Exception:
                    pass
                try:
                    cover_shadow.setVisibility(View.GONE)
                except Exception:
                    pass
                container.addView(
                    cover_shadow,
                    2,
                    LayoutHelper.createFrame(-1, 92, Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL, 16, 0, 16, 12)
                )
                self._header_cover_shadow_view = cover_shadow
            except Exception:
                self._header_cover_shadow_view = None
            try:
                from android.widget import ImageView
                from android_utils import OnClickListener
                mini_cover = ImageView(context)
                try:
                    mini_cover.setAdjustViewBounds(True)
                except Exception:
                    pass
                try:
                    st = getattr(ImageView, "ScaleType", None)
                    if st and getattr(st, "FIT_CENTER", None):
                        mini_cover.setScaleType(st.FIT_CENTER)
                except Exception:
                    pass
                try:
                    mini_cover_bg = GradientDrawable()
                    mini_cover_bg.setCornerRadius(AndroidUtilities.dp(10))
                    mini_cover_bg.setColor(Color.TRANSPARENT)
                    mini_cover.setBackground(mini_cover_bg)
                    try:
                        mini_cover.setClipToOutline(True)
                    except Exception:
                        pass
                except Exception:
                    pass
                try:
                    def _open_extended():
                        try:
                            frag = get_last_fragment()
                            run_on_ui_thread(lambda: get_messages_controller().openByUserName("AGeekApple", frag, 1))
                        except Exception:
                            pass
                    mini_cover.setOnClickListener(OnClickListener(lambda v: run_on_ui_thread(_open_extended)))
                except Exception:
                    pass
                container.addView(
                    mini_cover,
                    LayoutHelper.createFrame(24, 30, Gravity.RIGHT | Gravity.TOP, 0, 60, 40, 0)
                )
                try:
                    self._header_mini_cover_icon_view = mini_cover
                except Exception:
                    pass
                def _load_mini_cover():
                    try:
                        icon_url = ICON_EXTENDED_HEADER
                        try:
                            home_cover_enabled = bool(self.get_setting("header_cover_enabled", True))
                            bg = int(Theme.getColor(Theme.key_windowBackgroundWhite))
                            r = (bg >> 16) & 0xFF
                            g = (bg >> 8) & 0xFF
                            b = bg & 0xFF
                            if (not home_cover_enabled) and (((r * 299 + g * 587 + b * 114) / 1000.0) >= 150):
                                icon_url = ICON_EXTENDED_HEADER_LIGHT
                        except Exception:
                            icon_url = ICON_EXTENDED_HEADER
                        cache_key = "nowfy_extended_header_icon_light" if icon_url == ICON_EXTENDED_HEADER_LIGHT else "nowfy_extended_header_icon_dark"
                        data = self._get_cached_image_enhanced(icon_url, cache_key=cache_key)
                        if not data:
                            return
                        bmp = BitmapFactory.decodeByteArray(data, 0, len(data))
                        if not bmp:
                            return
                        def _apply():
                            try:
                                mini_cover.setImageBitmap(bmp)
                            except Exception:
                                pass
                        run_on_ui_thread(_apply)
                    except Exception:
                        pass
                threading.Thread(target=_load_mini_cover, daemon=True).start()
            except Exception:
                pass
            try:
                from android.widget import ImageView
                from android_utils import OnClickListener
                menu_icon = ImageView(context)
                try:
                    menu_icon.setAdjustViewBounds(True)
                except Exception:
                    pass
                try:
                    st = getattr(ImageView, "ScaleType", None)
                    if st and getattr(st, "FIT_CENTER", None):
                        menu_icon.setScaleType(st.FIT_CENTER)
                except Exception:
                    pass
                try:
                    menu_icon_bg = GradientDrawable()
                    menu_icon_bg.setCornerRadius(AndroidUtilities.dp(10))
                    menu_icon_bg.setColor(Color.TRANSPARENT)
                    menu_icon.setBackground(menu_icon_bg)
                    try:
                        menu_icon.setClipToOutline(True)
                    except Exception:
                        pass
                except Exception:
                    pass
                try:
                    menu_icon.setOnClickListener(OnClickListener(lambda v: run_on_ui_thread(lambda: self._show_home_cover_quick_menu(menu_icon))))
                except Exception:
                    pass
                try:
                    unlocked_raw = self.get_setting("home_cover_quick_menu_unlocked", False)
                    unlocked = False
                    if isinstance(unlocked_raw, bool):
                        unlocked = unlocked_raw
                    else:
                        unlocked = str(unlocked_raw).strip().lower() in ("1", "true", "yes", "on")
                    if not unlocked:
                        menu_icon.setVisibility(View.GONE)
                except Exception:
                    pass
                container.addView(
                    menu_icon,
                    LayoutHelper.createFrame(24, 30, Gravity.LEFT | Gravity.TOP, 40, 60, 0, 0)
                )
                try:
                    self._header_menu_icon_view = menu_icon
                except Exception:
                    pass
                def _load_menu_icon():
                    try:
                        BitmapFactoryLocal = find_class("android.graphics.BitmapFactory")
                        if not BitmapFactoryLocal:
                            return
                        try:
                            bg = int(Theme.getColor(Theme.key_windowBackgroundWhite))
                            r = (bg >> 16) & 0xFF
                            g = (bg >> 8) & 0xFF
                            b = bg & 0xFF
                            is_dark_theme = (((r * 299 + g * 587 + b * 114) / 1000.0) < 150)
                        except Exception:
                            is_dark_theme = True
                        try:
                            home_cover_enabled = bool(self.get_setting("header_cover_enabled", True))
                        except Exception:
                            home_cover_enabled = True
                        preferred = "nowfy_menu_white.png" if (home_cover_enabled or is_dark_theme) else "nowfy_menu_black.png"
                        alt = "nowfy_menu_black.png" if preferred == "nowfy_menu_white.png" else "nowfy_menu_white.png"
                        local_candidates = [
                            os.path.join(os.path.dirname(__file__), "assets", "png", preferred),
                            os.path.join(os.path.dirname(__file__), "assets", "png", alt),
                            os.path.join(os.path.dirname(__file__), "assets", "png", "nowfy_menu.png"),
                            os.path.join(os.path.dirname(__file__), "nowfy", "assets", "png", preferred),
                            os.path.join(os.path.dirname(__file__), "nowfy", "assets", "png", alt),
                            os.path.join(os.path.dirname(__file__), "nowfy", "assets", "png", "nowfy_menu.png"),
                        ]
                        for p in local_candidates:
                            try:
                                if p and os.path.isfile(p):
                                    bmp_local = BitmapFactoryLocal.decodeFile(p)
                                    if bmp_local:
                                        run_on_ui_thread(lambda b=bmp_local: menu_icon.setImageBitmap(b))
                                        return
                            except Exception:
                                pass
                        urls = [
                            f"https://assets.nowfy/{preferred}",
                            f"https://coreupdates.meyankut.workers.dev/{preferred}",
                            "https://assets.nowfy/nowfy_menu.png",
                            "https://coreupdates.meyankut.workers.dev/nowfy_menu.png"
                        ]
                        for u in urls:
                            try:
                                data = None
                                if hasattr(self, "_get_cached_image_enhanced"):
                                    data = self._get_cached_image_enhanced(u, cache_key="nowfy_home_menu_icon")
                                if not data:
                                    resp = requests.get(
                                        u,
                                        headers={"Accept": "image/*,*/*;q=0.8", "Cache-Control": "no-cache"},
                                        timeout=10
                                    )
                                    if resp.status_code == 200 and resp.content:
                                        data = resp.content
                                if data:
                                    bmp = BitmapFactoryLocal.decodeByteArray(data, 0, len(data))
                                    if bmp:
                                        run_on_ui_thread(lambda b=bmp: menu_icon.setImageBitmap(b))
                                        return
                            except Exception:
                                pass
                    except Exception:
                        pass
                threading.Thread(target=_load_menu_icon, daemon=True).start()
            except Exception:
                pass
            try:
                custom_selected = False
                try:
                    custom_selected = int(self.get_setting("custom_cover_selection", 0)) == 1
                except Exception:
                    custom_selected = False
                try:
                    force_nowfy = bool(self.get_setting("custom_cover_force_nowfy", False))
                except Exception:
                    force_nowfy = False
                custom_path = self._get_custom_cover_path()
                if custom_selected and not custom_path:
                    try:
                        self.set_setting("custom_cover_selection", 0)
                    except Exception:
                        pass
                    custom_selected = False
                if custom_selected and custom_path:
                    self._apply_header_cover_local_file(bg_cover, custom_path)
                else:
                    immediate_cover_url = None
                    try:
                        enabled = bool(self.get_setting("header_cover_enabled", True))
                        show_mode = int(self.get_setting("header_cover_show_mode", 0))
                        if enabled and show_mode in (0, 1):
                            immediate_cover_url = self._get_header_fallback_url()
                    except Exception:
                        immediate_cover_url = self._get_header_fallback_url()
                    if immediate_cover_url:
                        bmp = getattr(self, "_header_fallback_bitmap", None)
                        if bmp:
                            def _apply_fallback_bmp():
                                try:
                                    try:
                                        gif_view = getattr(self, "_header_cover_gif_view", None)
                                        if gif_view:
                                            gif_view.setImageDrawable(None)
                                            gif_view.setVisibility(View.GONE)
                                    except Exception:
                                        pass
                                    try:
                                        self._set_header_cover_shadow_visible(False)
                                    except Exception:
                                        pass
                                    bg_cover.setImageBitmap(bmp)
                                    bg_cover.setVisibility(View.VISIBLE)
                                    try:
                                        bg_cover.setAlpha(0.0)
                                        bg_cover.animate().alpha(0.92).setDuration(220).start()
                                    except Exception:
                                        try:
                                            bg_cover.setAlpha(0.92)
                                        except Exception:
                                            pass
                                    bg_cover.invalidate()
                                    try:
                                        self._set_header_cover_text_mode(True)
                                    except Exception:
                                        pass
                                except Exception:
                                    pass
                            run_on_ui_thread(_apply_fallback_bmp)
                        else:
                            threading.Thread(
                                target=lambda: self._apply_header_cover_cached_only(bg_cover, immediate_cover_url),
                                daemon=True
                            ).start()
            except Exception:
                pass
            user = None
            try:
                account = getattr(UserConfig, 'selectedAccount', 0)
                mc = MessagesController.getInstance(account)
                uc = UserConfig.getInstance(account)
                if mc and uc:
                    user = mc.getUser(uc.getClientUserId())
            except Exception:
                user = None
            if user:
                avatar_shell = FrameLayout(context)
                avatar_shell_bg = GradientDrawable()
                avatar_shell_bg.setCornerRadius(AndroidUtilities.dp(48))
                avatar_shell_bg.setColor(Color.TRANSPARENT)
                try:
                    avatar_shell_bg.setStroke(AndroidUtilities.dp(2), Color.TRANSPARENT)
                except Exception:
                    pass
                try:
                    avatar_shell.setBackground(avatar_shell_bg)
                except Exception:
                    pass
                try:
                    avatar_shell.setPadding(AndroidUtilities.dp(2), AndroidUtilities.dp(2), AndroidUtilities.dp(2), AndroidUtilities.dp(2))
                except Exception:
                    pass
                img = BackupImageView(context)
                img.setRoundRadius(AndroidUtilities.dp(46))
                avatar_drawable = AvatarDrawable(user)
                img.setForUserOrChat(user, avatar_drawable)
                avatar_shell.addView(
                    img,
                    LayoutHelper.createFrame(92, 92, Gravity.CENTER)
                )
                ring_view = ImageView(context)
                try:
                    ring_size = AndroidUtilities.dp(96)
                except Exception:
                    ring_size = int(context.getResources().getDisplayMetrics().density * 96)
                try:
                    ring_drawable = ShapeDrawable(OvalShape())
                    ring_paint = ring_drawable.getPaint()
                    ring_paint.setAntiAlias(True)
                    ring_paint.setStyle(Paint.Style.STROKE)
                    ring_paint.setStrokeWidth(AndroidUtilities.dp(3))
                    try:
                        ring_paint.setStrokeCap(Paint.Cap.ROUND)
                    except Exception:
                        pass
                    try:
                        color_array = jarray('i')([
                            int(Color.parseColor("#8B5CFF")),
                            int(Color.parseColor("#4CC2FF")),
                            int(Color.parseColor("#8B5CFF"))
                        ])
                        gradient = SweepGradient(
                            float(ring_size) / 2.0,
                            float(ring_size) / 2.0,
                            color_array,
                            None
                        )
                        ring_paint.setShader(gradient)
                    except Exception:
                        pass
                    try:
                        ring_drawable.setBounds(0, 0, ring_size, ring_size)
                    except Exception:
                        pass
                    try:
                        ring_view.setBackground(ring_drawable)
                    except Exception:
                        ring_view.setImageDrawable(ring_drawable)
                except Exception:
                    pass
                try:
                    ring_view.setVisibility(8)
                except Exception:
                    pass
                avatar_shell.addView(
                    ring_view,
                    LayoutHelper.createFrame(96, 96, Gravity.CENTER)
                )
                try:
                    avatar_shell.setClickable(True)
                    avatar_shell.setLongClickable(True)
                    img.setClickable(True)
                    img.setLongClickable(True)
                    avatar_shell.setOnClickListener(OnClickListener(lambda v: self._handle_home_cover_quick_unlock_tap()))
                    img.setOnClickListener(OnClickListener(lambda v: self._handle_home_cover_quick_unlock_tap()))
                except Exception:
                    pass
            if user:
                try:
                    from java import dynamic_proxy
                    from android.view import View
                    plugin_ref = self
                    class _LongClick(dynamic_proxy(View.OnLongClickListener)):
                        def onLongClick(self, v):
                            try:
                                plugin_ref._vibrate_feedback(35, 85)
                            except Exception:
                                pass
                            try:
                                run_on_ui_thread(lambda: plugin_ref._open_chat_fab_sheet(allow_anywhere=True, force_chatlist_mode=True))
                            except Exception:
                                pass
                            return True
                    avatar_shell.setOnLongClickListener(_LongClick())
                    img.setOnLongClickListener(_LongClick())
                except Exception:
                    pass
                content.addView(
                    avatar_shell,
                    LayoutHelper.createLinear(96, 96, Gravity.CENTER_HORIZONTAL, 0, 20, 0, 12)
                )
                try:
                    avatar_shell.setCameraDistance(float(AndroidUtilities.dp(800)))
                except Exception:
                    pass
                try:
                    avatar_shell.setTranslationY(float(AndroidUtilities.dp(34)))
                except Exception:
                    pass
                try:
                    avatar_shell.setAlpha(0.0)
                except Exception:
                    pass
                try:
                    avatar_shell.setRotationY(-120.0)
                except Exception:
                    pass
                try:
                    avatar_shell.animate().cancel()
                except Exception:
                    pass
                try:
                    avatar_shell.animate().translationY(0.0).alpha(1.0).rotationY(0.0).setDuration(620).start()
                except Exception:
                    pass
            title = TextView(context)
            title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 20)
            try:
                title.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_MEDIUM))
            except Exception:
                pass
            name = user.first_name if user and user.first_name else "User"
            title.setText(tr("nowfy_home_hello").format(name))
            title.setGravity(Gravity.CENTER)
            content.addView(title, LayoutHelper.createLinear(-2, -2, Gravity.CENTER_HORIZONTAL, 16, 0, 16, 12))
            desc = TextView(context)
            desc.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            desc.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
            try:
                desc.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_REGULAR))
            except Exception:
                pass
            try:
                keys = [
                    "nowfy_home_desc_1",
                    "nowfy_home_desc_2",
                    "nowfy_home_desc_3",
                    "nowfy_home_desc_4",
                    "nowfy_home_desc_5",
                ]
                desc.setText(tr(random.choice(keys)))
            except Exception:
                desc.setText(tr("nowfy_home_desc_1"))
            desc.setGravity(Gravity.CENTER)
            content.addView(desc, LayoutHelper.createLinear(-2, -2, Gravity.CENTER_HORIZONTAL, 16, 0, 16, 16))
            try:
                self._header_title_view = title
                self._header_desc_view = desc
            except Exception:
                pass
            try:
                if cover_enabled:
                    def _load_header_cover():
                        try:
                            try:
                                custom_selected = int(self.get_setting("custom_cover_selection", 0)) == 1
                            except Exception:
                                custom_selected = False
                            custom_path = None
                            if custom_selected:
                                try:
                                    custom_path = self._get_custom_cover_path()
                                except Exception:
                                    custom_path = None
                            if custom_selected and custom_path:
                                return
                            def _process_cover_bytes(data_bytes):
                                return self._process_header_cover_bytes(cover_url, data_bytes)
                            cover_url = None
                            allow_dynamic = True
                            enabled = True
                            show_mode = 0
                            try:
                                enabled = bool(self.get_setting("header_cover_enabled", True))
                                show_mode = int(self.get_setting("header_cover_show_mode", 0))
                                allow_dynamic = enabled and (show_mode == 0)
                            except Exception:
                                allow_dynamic = True
                            if not enabled:
                                return
                            if allow_dynamic:
                                for _attempt in range(2):
                                    try:
                                        cover_url = getattr(self, "_di_last_cover_url", None)
                                    except Exception:
                                        cover_url = None
                                    if not cover_url:
                                        try:
                                            info = self._get_current_track_info()
                                            if info and isinstance(info, dict):
                                                cover_url = info.get("cover_url")
                                        except Exception:
                                            cover_url = None
                                    if not cover_url:
                                        try:
                                            info2 = self._get_spotify_current_track_simple()
                                            if info2 and isinstance(info2, dict):
                                                cover_url = info2.get("cover_url")
                                        except Exception:
                                            cover_url = None
                                    if cover_url:
                                        break
                                    try:
                                        time.sleep(0.8)
                                    except Exception:
                                        pass
                            if not cover_url:
                                try:
                                    cover_url = getattr(self, "_header_fallback_url", None)
                                    if not cover_url:
                                        cover_url = self._get_header_fallback_url()
                                except Exception:
                                    cover_url = None
                            if not cover_url:
                                try:
                                    log("[Nowfy] header cover: no cover available")
                                except Exception:
                                    pass
                                return
                            cache_dir = self._di_cache_dir() or ApplicationLoader.getFilesDirFixed()
                            cache_dir = str(cache_dir)
                            try:
                                if not os.path.exists(cache_dir):
                                    os.makedirs(cache_dir)
                            except Exception:
                                pass
                            key = hashlib.md5(cover_url.encode("utf-8")).hexdigest()[:12]
                            cache_path = os.path.join(cache_dir, f"nowfy_header_cover_{key}.png")
                            bmp = None
                            try:
                                cached_bytes = self._get_cached_image_enhanced(cover_url, cache_key=f"nowfy_header_cover_{hash(cover_url)}")
                                if cached_bytes:
                                    processed = _process_cover_bytes(cached_bytes)
                                    bmp = BitmapFactory.decodeByteArray(processed, 0, len(processed))
                            except Exception:
                                bmp = None
                            if bmp is None:
                                try:
                                    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 128:
                                        bmp = BitmapFactory.decodeFile(cache_path)
                                except Exception:
                                    bmp = None
                            if bmp is None:
                                try:
                                    resp = requests.get(cover_url, timeout=(5, 10))
                                    if resp.status_code == 200 and resp.content:
                                        data = _process_cover_bytes(resp.content)
                                        bmp = BitmapFactory.decodeByteArray(data, 0, len(data))
                                        if bmp:
                                            try:
                                                with open(cache_path, "wb") as f:
                                                    f.write(data)
                                            except Exception:
                                                pass
                                except Exception:
                                    bmp = None
                            if bmp:
                                try:
                                    def _apply():
                                        try:
                                            bg_cover.setImageBitmap(bmp)
                                            bg_cover.setVisibility(View.VISIBLE)
                                            bg_cover.invalidate()
                                            try:
                                                self._set_header_cover_text_mode(True)
                                            except Exception:
                                                pass
                                        except Exception:
                                            pass
                                    run_on_ui_thread(_apply)
                                except Exception:
                                    try:
                                        bg_cover.setImageBitmap(bmp)
                                        bg_cover.setVisibility(View.VISIBLE)
                                        bg_cover.invalidate()
                                        try:
                                            self._set_header_cover_text_mode(True)
                                        except Exception:
                                            pass
                                    except Exception:
                                        pass
                                try:
                                    self._header_cover_last_active_ts = time.time()
                                except Exception:
                                    pass
                                try:
                                    log("[Nowfy] header cover: applied")
                                except Exception:
                                    pass
                            else:
                                try:
                                    log("[Nowfy] header cover: failed to decode")
                                except Exception:
                                    pass
                        except Exception:
                            pass
                    threading.Thread(target=_load_header_cover, daemon=True).start()
            except Exception:
                pass
            return container
        except Exception:
            return None

    def _set_header_cover_text_mode(self, active):
        try:
            from android.graphics import Color
            title = getattr(self, '_header_title_view', None)
            desc = getattr(self, '_header_desc_view', None)
            if not title and not desc:
                return
            def _apply():
                try:
                    if active:
                        if title: title.setTextColor(Color.WHITE)
                        if desc: desc.setTextColor(Color.WHITE)
                    else:
                        if title: title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
                        if desc: desc.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
                except Exception:
                    pass
            run_on_ui_thread(_apply)
        except Exception:
            pass

    def _set_header_cover_shadow_visible(self, visible):
        try:
            sh = getattr(self, "_header_cover_shadow_view", None)
            if not sh:
                return
            def _apply():
                try:
                    sh.setVisibility(View.VISIBLE if bool(visible) else View.GONE)
                except Exception:
                    pass
            run_on_ui_thread(_apply)
        except Exception:
            pass

    def _refresh_header_action_icons(self):
        try:
            mini_cover = getattr(self, "_header_mini_cover_icon_view", None)
            menu_icon = getattr(self, "_header_menu_icon_view", None)
            if not mini_cover and not menu_icon:
                return
            try:
                bg = int(Theme.getColor(Theme.key_windowBackgroundWhite))
                r = (bg >> 16) & 0xFF
                g = (bg >> 8) & 0xFF
                b = bg & 0xFF
                is_dark_theme = (((r * 299 + g * 587 + b * 114) / 1000.0) < 150)
            except Exception:
                is_dark_theme = True
            try:
                home_cover_enabled = bool(self.get_setting("header_cover_enabled", True))
            except Exception:
                home_cover_enabled = True
            if mini_cover is not None:
                def _load_mini():
                    try:
                        icon_url = ICON_EXTENDED_HEADER
                        if (not home_cover_enabled) and (not is_dark_theme):
                            icon_url = ICON_EXTENDED_HEADER_LIGHT
                        data = self._get_cached_image_enhanced(icon_url, cache_key=("nowfy_extended_header_icon_light" if icon_url == ICON_EXTENDED_HEADER_LIGHT else "nowfy_extended_header_icon_dark"))
                        if not data:
                            return
                        bmp = BitmapFactory.decodeByteArray(data, 0, len(data))
                        if not bmp:
                            return
                        run_on_ui_thread(lambda b=bmp: mini_cover.setImageBitmap(b))
                    except Exception:
                        pass
                threading.Thread(target=_load_mini, daemon=True).start()
            if menu_icon is not None:
                def _load_menu():
                    try:
                        BitmapFactoryLocal = find_class("android.graphics.BitmapFactory")
                        if not BitmapFactoryLocal:
                            return
                        preferred = "nowfy_menu_white.png" if (home_cover_enabled or is_dark_theme) else "nowfy_menu_black.png"
                        alt = "nowfy_menu_black.png" if preferred == "nowfy_menu_white.png" else "nowfy_menu_white.png"
                        local_candidates = [
                            os.path.join(os.path.dirname(__file__), "assets", "png", preferred),
                            os.path.join(os.path.dirname(__file__), "assets", "png", alt),
                            os.path.join(os.path.dirname(__file__), "nowfy", "assets", "png", preferred),
                            os.path.join(os.path.dirname(__file__), "nowfy", "assets", "png", alt),
                        ]
                        for p in local_candidates:
                            try:
                                if p and os.path.isfile(p):
                                    bmp_local = BitmapFactoryLocal.decodeFile(p)
                                    if bmp_local:
                                        run_on_ui_thread(lambda b=bmp_local: menu_icon.setImageBitmap(b))
                                        return
                            except Exception:
                                pass
                        for u in (
                            f"https://assets.nowfy/{preferred}",
                            f"https://coreupdates.meyankut.workers.dev/{preferred}",
                            f"https://assets.nowfy/{alt}",
                            f"https://coreupdates.meyankut.workers.dev/{alt}",
                        ):
                            try:
                                data = self._get_cached_image_enhanced(u, cache_key=f"nowfy_home_menu_icon_{preferred}")
                                if not data:
                                    continue
                                bmp = BitmapFactoryLocal.decodeByteArray(data, 0, len(data))
                                if bmp:
                                    run_on_ui_thread(lambda b=bmp: menu_icon.setImageBitmap(b))
                                    return
                            except Exception:
                                pass
                    except Exception:
                        pass
                threading.Thread(target=_load_menu, daemon=True).start()
        except Exception:
            pass

    def _criar_visualizacao_cabecalho_temas(self, context):
        try:
            from android.widget import TextView
            from android.view import Gravity
            from android.util import TypedValue
            from org.telegram.ui.ActionBar import Theme
            from org.telegram.ui.Components import LayoutHelper
            from android.widget import ImageView
            container, content = self._criar_header_base(context)
            if not container or not content:
                return None
            img = ImageView(context)
            try:
                img.setAdjustViewBounds(True)
            except Exception:
                pass
            try:
                st = getattr(ImageView, "ScaleType", None)
                if st and getattr(st, "CENTER_CROP", None):
                    img.setScaleType(st.CENTER_CROP)
            except Exception:
                pass
            content.addView(
                img,
                LayoutHelper.createLinear(280, -2, Gravity.CENTER_HORIZONTAL, 0, 16, 0, 10)
            )
            title = TextView(context)
            title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18)
            try:
                title.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_MEDIUM))
            except Exception:
                pass
            title.setText(tr("nowfy_themes_header_title"))
            title.setGravity(Gravity.CENTER)
            content.addView(title, LayoutHelper.createLinear(-2, -2, Gravity.CENTER_HORIZONTAL, 16, 0, 16, 12))
            try:
                import threading
                try:
                    from hook_utils import find_class
                    BitmapFactory = find_class("android.graphics.BitmapFactory")
                    cache_dir = self._di_cache_dir() or ApplicationLoader.getFilesDirFixed()
                    cache_path = os.path.join(str(cache_dir), "nowfy_themes_header.png")
                    if BitmapFactory and os.path.exists(cache_path) and os.path.getsize(cache_path) > 128:
                        bmp_sync = BitmapFactory.decodeFile(cache_path)
                        if bmp_sync:
                            try:
                                img.setImageBitmap(bmp_sync)
                            except Exception:
                                pass
                except Exception:
                    pass
                def _load():
                    try:
                        import requests, os
                        from hook_utils import find_class
                        BitmapFactory = find_class("android.graphics.BitmapFactory")
                        if not BitmapFactory:
                            return
                        cache_dir = self._di_cache_dir() or ApplicationLoader.getFilesDirFixed()
                        cache_path = os.path.join(str(cache_dir), "nowfy_themes_header.png")
                        try:
                            if os.path.exists(cache_path) and os.path.getsize(cache_path) > 128:
                                bmp = BitmapFactory.decodeFile(cache_path)
                                if bmp:
                                    try:
                                        run_on_ui_thread(lambda: img.setImageBitmap(bmp))
                                    except Exception:
                                        img.setImageBitmap(bmp)
                                    return
                        except Exception:
                            pass
                        url = "https://assets.nowfy/themes-Nowfy.pngv_2.png"
                        headers = {"Cache-Control": "no-cache"}
                        resp = requests.get(url, headers=headers, timeout=(5, 10))
                        if resp.status_code != 200 or not resp.content:
                            return
                        data = resp.content
                        bmp = BitmapFactory.decodeByteArray(data, 0, len(data))
                        if not bmp:
                            return
                        try:
                            with open(cache_path, "wb") as f:
                                f.write(data)
                        except Exception:
                            pass
                        try:
                            run_on_ui_thread(lambda: img.setImageBitmap(bmp))
                        except Exception:
                            try:
                                img.setImageBitmap(bmp)
                            except Exception:
                                pass
                    except Exception:
                        pass
                threading.Thread(target=_load, daemon=True).start()
            except Exception:
                pass
            return container
        except Exception:
            return None

    def _criar_visualizacao_cabecalho_servicos(self, context):
        try:
            from android.widget import TextView
            from android.view import Gravity
            from android.util import TypedValue
            from org.telegram.ui.ActionBar import Theme
            from org.telegram.ui.Components import LayoutHelper, BackupImageView, AvatarDrawable
            from org.telegram.messenger import UserConfig, MessagesController
            container, content = self._criar_header_base(context)
            if not container or not content:
                return None
            user = None
            try:
                account = getattr(UserConfig, 'selectedAccount', 0)
                mc = MessagesController.getInstance(account)
                uc = UserConfig.getInstance(account)
                if mc and uc:
                    user = mc.getUser(uc.getClientUserId())
            except Exception:
                user = None
            if user:
                img = BackupImageView(context)
                img.setRoundRadius(AndroidUtilities.dp(48))
                avatar_drawable = AvatarDrawable(user)
                img.setForUserOrChat(user, avatar_drawable)
                content.addView(
                    img,
                    LayoutHelper.createLinear(96, 96, Gravity.CENTER_HORIZONTAL, 0, 20, 0, 12)
                )
            title = TextView(context)
            title_default_color = Theme.getColor(Theme.key_windowBackgroundWhiteBlackText)
            title.setTextColor(title_default_color)
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 20)
            try:
                title.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_MEDIUM))
            except Exception:
                pass
            title.setText(tr("nowfy_services_header_title"))
            title.setGravity(Gravity.CENTER)
            content.addView(title, LayoutHelper.createLinear(-2, -2, Gravity.CENTER_HORIZONTAL, 16, 0, 16, 8))
            desc = TextView(context)
            desc_default_color = Theme.getColor(Theme.key_windowBackgroundWhiteGrayText)
            desc.setTextColor(desc_default_color)
            desc.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
            try:
                desc.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_REGULAR))
            except Exception:
                pass
            desc.setText(tr("nowfy_services_header_desc"))
            desc.setGravity(Gravity.CENTER)
            content.addView(desc, LayoutHelper.createLinear(-2, -2, Gravity.CENTER_HORIZONTAL, 16, 0, 16, 16))
            return container
        except Exception:
            return None

    def _criar_visualizacao_cabecalho_servicos_simples(self, context):
        try:
            from android.widget import TextView
            from android.view import Gravity
            from android.util import TypedValue
            from org.telegram.ui.ActionBar import Theme
            from org.telegram.ui.Components import LayoutHelper
            from android.widget import ImageView
            container, content = self._criar_header_base(context)
            if not container or not content:
                return None
            img = ImageView(context)
            try:
                img.setAdjustViewBounds(True)
            except Exception:
                pass
            try:
                st = getattr(ImageView, "ScaleType", None)
                if st and getattr(st, "CENTER_CROP", None):
                    img.setScaleType(st.CENTER_CROP)
            except Exception:
                pass
            content.addView(
                img,
                LayoutHelper.createLinear(260, -2, Gravity.CENTER_HORIZONTAL, 0, 12, 0, 10)
            )
            title = TextView(context)
            title_default_color = Theme.getColor(Theme.key_windowBackgroundWhiteBlackText)
            title.setTextColor(title_default_color)
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 20)
            try:
                title.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_MEDIUM))
            except Exception:
                pass
            title.setText(tr("nowfy_services_header_title"))
            title.setGravity(Gravity.CENTER)
            content.addView(title, LayoutHelper.createLinear(-2, -2, Gravity.CENTER_HORIZONTAL, 16, 0, 16, 8))
            desc = TextView(context)
            desc_default_color = Theme.getColor(Theme.key_windowBackgroundWhiteGrayText)
            desc.setTextColor(desc_default_color)
            desc.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
            try:
                desc.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_REGULAR))
            except Exception:
                pass
            desc.setText(tr("nowfy_services_header_desc"))
            desc.setGravity(Gravity.CENTER)
            content.addView(desc, LayoutHelper.createLinear(-2, -2, Gravity.CENTER_HORIZONTAL, 16, 0, 16, 16))
            try:
                import threading
                def _load():
                    try:
                        import requests, os
                        from hook_utils import find_class
                        BitmapFactory = find_class("android.graphics.BitmapFactory")
                        if not BitmapFactory:
                            return
                        cache_dir = self._di_cache_dir() or ApplicationLoader.getFilesDirFixed()
                        cache_path = os.path.join(str(cache_dir), "nowfy_services_header.png")
                        try:
                            if os.path.exists(cache_path) and os.path.getsize(cache_path) > 128:
                                bmp = BitmapFactory.decodeFile(cache_path)
                                if bmp:
                                    try:
                                        run_on_ui_thread(lambda: img.setImageBitmap(bmp))
                                    except Exception:
                                        img.setImageBitmap(bmp)
                                    return
                        except Exception:
                            pass
                        url = "https://assets.nowfy/serivces.png"
                        headers = {"Cache-Control": "no-cache"}
                        resp = requests.get(url, headers=headers, timeout=(5, 10))
                        if resp.status_code != 200 or not resp.content:
                            return
                        data = resp.content
                        bmp = BitmapFactory.decodeByteArray(data, 0, len(data))
                        if not bmp:
                            return
                        try:
                            with open(cache_path, "wb") as f:
                                f.write(data)
                        except Exception:
                            pass
                        try:
                            run_on_ui_thread(lambda: img.setImageBitmap(bmp))
                        except Exception:
                            try:
                                img.setImageBitmap(bmp)
                            except Exception:
                                pass
                    except Exception:
                        pass
                threading.Thread(target=_load, daemon=True).start()
            except Exception:
                pass
            return container
        except Exception:
            return None

    def _criar_visualizacao_cabecalho_nowtab(self, context):
        try:
            from android.widget import TextView
            from android.view import Gravity
            from android.util import TypedValue
            from org.telegram.ui.ActionBar import Theme
            from org.telegram.ui.Components import LayoutHelper
            from android.widget import ImageView
            container, content = self._criar_header_base(context)
            if not container or not content:
                return None
            img = ImageView(context)
            try:
                img.setAdjustViewBounds(True)
            except Exception:
                pass
            try:
                st = getattr(ImageView, "ScaleType", None)
                if st and getattr(st, "CENTER_CROP", None):
                    img.setScaleType(st.CENTER_CROP)
            except Exception:
                pass
            content.addView(
                img,
                LayoutHelper.createLinear(280, -2, Gravity.CENTER_HORIZONTAL, 0, 16, 0, 10)
            )
            title = TextView(context)
            title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18)
            try:
                title.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_MEDIUM))
            except Exception:
                pass
            title.setText("Now Tab")
            title.setGravity(Gravity.CENTER)
            content.addView(title, LayoutHelper.createLinear(-2, -2, Gravity.CENTER_HORIZONTAL, 16, 0, 16, 12))
            desc = TextView(context)
            desc.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            desc.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
            desc.setGravity(Gravity.CENTER)
            try:
                desc.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_REGULAR))
            except Exception:
                pass
            desc.setText(tr("nowfy_nowtab_header_desc"))
            content.addView(desc, LayoutHelper.createLinear(-2, -2, Gravity.CENTER_HORIZONTAL, 16, 0, 16, 16))
            try:
                from hook_utils import find_class
                BitmapFactory = find_class("android.graphics.BitmapFactory")
                if BitmapFactory:
                    candidates = [
                        os.path.join(os.path.dirname(__file__), "assets", "png", "tab-style.png"),
                        os.path.join(os.path.dirname(__file__), "nowfy", "assets", "png", "tab-style.png"),
                    ]
                    for p in candidates:
                        try:
                            if p and os.path.isfile(p):
                                bmp = BitmapFactory.decodeFile(p)
                                if bmp:
                                    img.setImageBitmap(bmp)
                                    break
                        except Exception:
                            pass
            except Exception:
                pass
            return container
        except Exception:
            return None

    def _criar_visualizacao_cabecalho_nowfy_flow(self, context):
        try:
            container, content = self._criar_header_base(context)
            if not container or not content:
                return None
            img = ImageView(context)
            try:
                img.setAdjustViewBounds(True)
            except Exception:
                pass
            try:
                st = getattr(ImageView, "ScaleType", None)
                if st and getattr(st, "CENTER_CROP", None):
                    img.setScaleType(st.CENTER_CROP)
            except Exception:
                pass
            content.addView(
                img,
                LayoutHelper.createLinear(280, -2, Gravity.CENTER_HORIZONTAL, 0, 16, 0, 10)
            )
            title = TextView(context)
            title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18)
            try:
                title.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_MEDIUM))
            except Exception:
                pass
            title.setText(tr("nowfy_flow_header_title"))
            title.setGravity(Gravity.CENTER)
            content.addView(title, LayoutHelper.createLinear(-2, -2, Gravity.CENTER_HORIZONTAL, 16, 0, 16, 12))
            desc = TextView(context)
            desc.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            desc.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
            desc.setGravity(Gravity.CENTER)
            try:
                desc.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_REGULAR))
            except Exception:
                pass
            desc.setText(tr("nowfy_flow_header_desc"))
            content.addView(desc, LayoutHelper.createLinear(-2, -2, Gravity.CENTER_HORIZONTAL, 16, 0, 16, 16))
            try:
                from hook_utils import find_class
                BitmapFactory = find_class("android.graphics.BitmapFactory")
                if BitmapFactory:
                    candidates = [
                        os.path.join(os.path.dirname(__file__), "assets", "png", "nowfy_flow.png"),
                        os.path.join(os.path.dirname(__file__), "nowfy", "assets", "png", "nowfy_flow.png"),
                    ]
                    for p in candidates:
                        try:
                            if p and os.path.isfile(p):
                                bmp = BitmapFactory.decodeFile(p)
                                if bmp:
                                    img.setImageBitmap(bmp)
                                    break
                        except Exception:
                            pass
            except Exception:
                pass
            return container
        except Exception:
            return None

    def _criar_visualizacao_cabecalho_spotify(self, context):
        try:
            from android.widget import TextView, LinearLayout, ImageView
            from android.view import Gravity
            from android.util import TypedValue
            from org.telegram.ui.ActionBar import Theme
            from org.telegram.ui.Components import LayoutHelper, BackupImageView, AvatarDrawable
            if not self._has_spotify_credentials():
                return None
            container, content = self._criar_header_base(context)
            if not container or not content:
                return None
            row = LinearLayout(context)
            row.setOrientation(LinearLayout.HORIZONTAL)
            row.setGravity(Gravity.CENTER_VERTICAL)
            content.addView(row, LayoutHelper.createLinear(-1, -2, Gravity.START, 16, 16, 16, 12))
            img = BackupImageView(context)
            img.setRoundRadius(AndroidUtilities.dp(12))
            try:
                img.setImageDrawable(AvatarDrawable())
            except Exception:
                pass
            img_lp = LinearLayout.LayoutParams(AndroidUtilities.dp(64), AndroidUtilities.dp(64))
            img_lp.rightMargin = AndroidUtilities.dp(12)
            row.addView(img, img_lp)
            col = LinearLayout(context)
            col.setOrientation(LinearLayout.VERTICAL)
            col.setGravity(Gravity.START)
            row.addView(col, LinearLayout.LayoutParams(-1, -2))
            title = TextView(context)
            title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 20)
            try:
                title.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_MEDIUM))
            except Exception:
                pass
            title.setText("Spotify User")
            title.setGravity(Gravity.START)
            col.addView(title)
            account_row = LinearLayout(context)
            account_row.setOrientation(LinearLayout.HORIZONTAL)
            account_row.setGravity(Gravity.CENTER_VERTICAL)
            badge = ImageView(context)
            try:
                badge.setScaleType(ImageView.ScaleType.CENTER_CROP)
            except Exception:
                pass
            account_row.addView(badge, LinearLayout.LayoutParams(AndroidUtilities.dp(14), AndroidUtilities.dp(14)))
            account_type = TextView(context)
            account_type.setText("Premium")
            account_type.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
            try:
                account_type.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            except Exception:
                account_type.setTextColor(0xFFD2DCEB)
            try:
                alp = LinearLayout.LayoutParams(-2, -2)
                alp.leftMargin = AndroidUtilities.dp(6)
                account_row.addView(account_type, alp)
            except Exception:
                account_row.addView(account_type)
            col.addView(account_row)
            followers_tv = TextView(context)
            followers_tv.setText("-- followers")
            followers_tv.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
            try:
                followers_tv.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            except Exception:
                followers_tv.setTextColor(0xFFD2DCEB)
            col.addView(followers_tv)
            def _load_image_into(image_view, url, cache_key):
                try:
                    if not url:
                        return
                    data = self._get_cached_image_enhanced(url, cache_key=cache_key)
                    if not data:
                        return
                    bmp = BitmapFactory.decodeByteArray(data, 0, len(data))
                    if bmp:
                        run_on_ui_thread(lambda b=bmp, iv=image_view: iv.setImageBitmap(b))
                except Exception:
                    pass
            try:
                import threading
                def _load():
                    try:
                        profile = self._get_spotify_user_profile() or {}
                        profile_name = str(profile.get("display_name") or profile.get("id") or "Spotify User").strip()
                        profile_img_url = str(profile.get("profile_image_url") or "").strip()
                        product_raw = str(profile.get("product") or "").strip().lower()
                        if product_raw == "premium":
                            product = "Premium"
                        elif product_raw in ("free", "open"):
                            product = "Free"
                        else:
                            product = "Unknown"
                        followers = self._format_count_with_commas(profile.get("followers", 0))
                        _load_image_into(badge, "https://assets.nowfy/spfynow.png", "spotify_head_badge_icon")
                        is_fallback = (str(profile_name or "").strip().lower() == "spotify user")
                        if is_fallback:
                            tg_user = None
                            try:
                                acct = getattr(UserConfig, "selectedAccount", 0)
                                uc = UserConfig.getInstance(acct)
                                tg_user = uc.getCurrentUser() if uc else None
                            except Exception:
                                tg_user = None
                            tg_name = ""
                            try:
                                tg_name = str(getattr(tg_user, "first_name", None) or getattr(tg_user, "username", None) or "").strip()
                            except Exception:
                                tg_name = ""
                            if not tg_name:
                                tg_name = "Nowfy User"
                            run_on_ui_thread(lambda n=tg_name: title.setText(n))
                            run_on_ui_thread(lambda: account_type.setText("Powered by Nowfy"))
                            run_on_ui_thread(lambda: followers_tv.setText(f"v{__version__}"))
                            try:
                                if tg_user:
                                    avatar_drawable = AvatarDrawable(tg_user)
                                    run_on_ui_thread(lambda u=tg_user, d=avatar_drawable: img.setForUserOrChat(u, d))
                            except Exception:
                                pass
                        else:
                            run_on_ui_thread(lambda: title.setText(profile_name))
                            run_on_ui_thread(lambda: account_type.setText(product))
                            run_on_ui_thread(lambda: followers_tv.setText(f"{followers} followers"))
                            _load_image_into(img, profile_img_url, f"spotify_head_profile_{hash(profile_img_url)}")
                    except Exception:
                        pass
                threading.Thread(target=_load, daemon=True).start()
            except Exception:
                pass
            return container
        except Exception:
            return None

    def _criar_visualizacao_cabecalho_statsfm(self, context):
        try:
            from android.widget import TextView, LinearLayout
            from android.view import Gravity
            from android.util import TypedValue
            from org.telegram.ui.Components import LayoutHelper
            from android.graphics.drawable import GradientDrawable
            from org.telegram.ui.ActionBar import Theme
            container, content = self._criar_header_base(context)
            if not container or not content:
                return None
            layout = LinearLayout(context)
            layout.setOrientation(LinearLayout.VERTICAL)
            layout.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(14), AndroidUtilities.dp(14), AndroidUtilities.dp(14))
            bg = GradientDrawable()
            bg.setCornerRadius(AndroidUtilities.dp(16))
            bg.setColor(0x162B3E5A)
            layout.setBackground(bg)
            t1 = TextView(context)
            t1.setText(tr("global_rich_title"))
            t1.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18)
            t1.setGravity(Gravity.START)
            try:
                t1.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                t1.setTextColor(0xFFFFFFFF)
            layout.addView(t1)
            t2 = TextView(context)
            stats_user = str(self.get_setting("statsfm_username", "") or "").strip()
            stats_sub_key = "statsfm_rich_subtitle_ready" if stats_user else "statsfm_rich_subtitle"
            t2.setText(tr(stats_sub_key))
            t2.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
            t2.setGravity(Gravity.START)
            try:
                t2.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            except Exception:
                t2.setTextColor(0xFFD2DCEB)
            layout.addView(t2)
            content.addView(layout, LayoutHelper.createLinear(-1, -2, Gravity.START, 16, 16, 16, 10))
            return container
        except Exception:
            return None

    def _criar_visualizacao_cabecalho_lastfm(self, context):
        try:
            from android.widget import TextView, LinearLayout
            from android.view import Gravity
            from android.util import TypedValue
            from org.telegram.ui.Components import LayoutHelper
            from android.graphics.drawable import GradientDrawable
            from org.telegram.ui.ActionBar import Theme
            container, content = self._criar_header_base(context)
            if not container or not content:
                return None
            layout = LinearLayout(context)
            layout.setOrientation(LinearLayout.VERTICAL)
            layout.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(14), AndroidUtilities.dp(14), AndroidUtilities.dp(14))
            bg = GradientDrawable()
            bg.setCornerRadius(AndroidUtilities.dp(16))
            bg.setColor(0x162B3E5A)
            layout.setBackground(bg)
            t1 = TextView(context)
            t1.setText(tr("global_rich_title"))
            t1.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18)
            t1.setGravity(Gravity.START)
            try:
                t1.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                t1.setTextColor(0xFFFFFFFF)
            layout.addView(t1)
            t2 = TextView(context)
            last_user = str(self.get_setting("lastfm_user", self.get_setting("lastfm_username", "")) or "").strip()
            last_sub_key = "lastfm_rich_subtitle_ready" if last_user else "lastfm_rich_subtitle"
            t2.setText(tr(last_sub_key))
            t2.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
            t2.setGravity(Gravity.START)
            try:
                t2.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            except Exception:
                t2.setTextColor(0xFFD2DCEB)
            layout.addView(t2)
            content.addView(layout, LayoutHelper.createLinear(-1, -2, Gravity.START, 16, 16, 16, 10))
            return container
        except Exception:
            return None

    def _get_plugin_lang_index(self):
        try:
            if NOWFY_CORE_API:
                return int(NOWFY_CORE_API.get_plugin_lang_index(self))
        except Exception:
            pass
        try:
            return int(self.get_setting("plugin_lang", 0))
        except Exception:
            return 0

    def _on_change_plugin_lang(self, idx):
        try:
            i = int(NOWFY_CORE_API.normalize_plugin_lang_index(idx)) if NOWFY_CORE_API else int(idx)
        except Exception:
            i = 0
        self.set_setting("plugin_lang", i)
        try:
            code = NOWFY_CORE_API.get_plugin_lang_code(i) if NOWFY_CORE_API else ["en", "pt", "ru"][i]
            global _NOWFY_LANG_OVERRIDE
            _NOWFY_LANG_OVERRIDE = code
        except Exception:
            pass
        try:
            run_on_ui_thread(lambda: self.reload_settings())
        except Exception:
            pass

    def _ensure_pop_island_drawer_item(self):
        return None

    def _remove_pop_island_drawer_item(self):
        return None

    def _on_pop_island_drawer_click(self, context):
        return None

    def _ensure_nowfy_drawer_item(self):
        try:
            if not getattr(self, "_nowfy_drawer_item", None):
                self._nowfy_drawer_item = self.add_menu_item(MenuItemData(
                    menu_type=MenuItemType.DRAWER_MENU,
                    text=(tr("nowfy_drawer")),
                    icon="msg_tone_on",
                    priority=159,
                    on_click=lambda ctx: run_on_ui_thread(lambda: self._open_plugin_settings())
                ))
        except Exception as e:
            log(f"[Nowfy] Nowfy drawer item creation failed: {e}")

    def _remove_nowfy_drawer_item(self):
        try:
            if getattr(self, "_nowfy_drawer_item", None):
                self.remove_menu_item(self._nowfy_drawer_item)
                self._nowfy_drawer_item = None
        except Exception:
            pass

    def _on_nowfy_panel_drawer_toggle(self, enabled):
        try:
            if NOWFY_CORE_API:
                NOWFY_CORE_API.on_panel_drawer_toggle(self, enabled)
                return
        except Exception:
            pass
        try:
            self._ensure_nowfy_drawer_item() if bool(enabled) else self._remove_nowfy_drawer_item()
            self.reload_settings()
        except Exception:
            pass

    def _on_nowfy_panel_home_actionbar_toggle(self, enabled):
        try:
            self.set_setting("nowfy_home_actionbar_enabled", bool(enabled))
            self.reload_settings()
        except Exception:
            pass
        try:
            run_on_ui_thread(lambda: self._sync_home_actionbar_shortcut(get_last_fragment()))
        except Exception:
            pass

    def _sync_home_actionbar_shortcut(self, fragment):
        try:
            if fragment is None:
                self._remove_home_actionbar_shortcut()
                return
            if (not self._is_dialogs_fragment(fragment)) or (not bool(self.get_setting("nowfy_home_actionbar_enabled", False))):
                self._remove_home_actionbar_shortcut()
                return
            self._ensure_home_actionbar_shortcut(fragment)
            try:
                btn = getattr(self, "_home_actionbar_btn", None)
                if btn is not None:
                    btn.setVisibility(View.GONE if self._is_home_actionbar_search_active(fragment) else View.VISIBLE)
            except Exception:
                pass
            try:
                self._sync_home_actionbar_title_spacing(fragment)
            except Exception:
                pass
        except Exception:
            pass

    def _is_home_actionbar_search_active(self, fragment):
        try:
            action_bar = fragment.getActionBar() if fragment else None
        except Exception:
            action_bar = None
        try:
            if action_bar and bool(action_bar.isSearchFieldVisible()):
                return True
        except Exception:
            pass
        try:
            searching = bool(_get_private_field_silent(fragment, "searching"))
            if searching:
                return True
        except Exception:
            pass
        try:
            fs = _get_private_field_silent(fragment, "fragmentSearchField")
            if fs is not None:
                edit = getattr(fs, "editText", None)
                if edit is not None and bool(edit.hasFocus()):
                    return True
        except Exception:
            pass
        return False

    def _ensure_home_actionbar_shortcut(self, fragment):
        try:
            action_bar = fragment.getActionBar() if fragment else None
        except Exception:
            action_bar = None
        if not action_bar:
            self._remove_home_actionbar_shortcut()
            return
        try:
            old_btn = getattr(self, "_home_actionbar_btn", None)
            if old_btn and getattr(self, "_home_actionbar_fragment", None) is fragment:
                try:
                    if old_btn.getParent() is action_bar:
                        old_btn.setVisibility(View.VISIBLE)
                        return
                except Exception:
                    pass
        except Exception:
            pass
        self._remove_home_actionbar_shortcut()
        try:
            ctx = fragment.getParentActivity()
            if not ctx:
                return
            btn = ImageView(ctx)
            btn.setScaleType(ImageView.ScaleType.CENTER)
            rid = 0
            try:
                rid = ctx.getResources().getIdentifier("msg_tone_on", "drawable", ctx.getPackageName())
            except Exception:
                rid = 0
            if not rid:
                try:
                    rid = ctx.getResources().getIdentifier("msg_topics", "drawable", ctx.getPackageName())
                except Exception:
                    rid = 0
            if rid:
                btn.setImageResource(rid)
            try:
                btn.setColorFilter(Theme.getColor(Theme.key_actionBarDefaultIcon))
            except Exception:
                pass
            try:
                btn.setBackground(Theme.getSelectorDrawable(False))
            except Exception:
                pass
            h = 56
            try:
                ActionBarCls = find_class("org.telegram.ui.ActionBar.ActionBar")
                if ActionBarCls and hasattr(ActionBarCls, "getCurrentActionBarHeight"):
                    h = int(ActionBarCls.getCurrentActionBarHeight() or 56)
            except Exception:
                h = 56
            try:
                lp = LayoutHelper.createFrame(54, float(h) / float(AndroidUtilities.density), Gravity.LEFT | Gravity.BOTTOM)
            except Exception:
                lp = FrameLayout.LayoutParams(AndroidUtilities.dp(54), AndroidUtilities.dp(56), Gravity.LEFT | Gravity.BOTTOM)
            action_bar.addView(btn, lp)
            btn.setOnClickListener(OnClickListener(lambda _v: self._open_plugin_settings()))
            self._home_actionbar_btn = btn
            self._home_actionbar_fragment = fragment
            try:
                self._layout_home_actionbar_shortcut(fragment, btn)
                run_on_ui_thread(lambda: self._layout_home_actionbar_shortcut(fragment, btn), 120)
                run_on_ui_thread(lambda: self._layout_home_actionbar_shortcut(fragment, btn), 320)
            except Exception:
                pass
            try:
                self._sync_home_actionbar_title_spacing(fragment)
            except Exception:
                pass
            self._start_home_actionbar_visibility_watch()
        except Exception:
            pass

    def _layout_home_actionbar_shortcut(self, fragment, btn=None):
        try:
            if not fragment:
                return
            action_bar = fragment.getActionBar() if fragment else None
            if action_bar is None:
                return
            if btn is None:
                btn = getattr(self, "_home_actionbar_btn", None)
            if btn is None:
                return
            try:
                if btn.getParent() is not action_bar:
                    return
            except Exception:
                return

            bar_w = 0
            try:
                bar_w = int(action_bar.getWidth() or 0)
            except Exception:
                bar_w = 0
            if bar_w <= 0:
                return

            btn_w = 0
            try:
                btn_w = int(btn.getWidth() or 0)
            except Exception:
                btn_w = 0
            if btn_w <= 0:
                btn_w = int(AndroidUtilities.dp(54))

            target_left = int(AndroidUtilities.dp(6))
            max_left = max(int(AndroidUtilities.dp(4)), bar_w - btn_w - int(AndroidUtilities.dp(4)))
            target_left = max(int(AndroidUtilities.dp(4)), min(target_left, max_left))

            lp = None
            try:
                lp = btn.getLayoutParams()
            except Exception:
                lp = None
            if lp is None:
                return
            try:
                if hasattr(lp, "setMargins"):
                    lp.setMargins(int(target_left), 0, 0, 0)
                else:
                    lp.leftMargin = int(target_left)
                btn.setLayoutParams(lp)
            except Exception:
                pass
        except Exception:
            pass

    def _remove_home_actionbar_shortcut(self):
        try:
            self._stop_home_actionbar_visibility_watch()
            try:
                frag = getattr(self, "_home_actionbar_fragment", None)
                if frag is not None:
                    self._sync_home_actionbar_title_spacing(frag, force_reset=True)
            except Exception:
                pass
            btn = getattr(self, "_home_actionbar_btn", None)
            if btn:
                try:
                    parent = btn.getParent()
                    if parent:
                        parent.removeView(btn)
                except Exception:
                    pass
            self._home_actionbar_btn = None
            self._home_actionbar_fragment = None
        except Exception:
            pass

    def _start_home_actionbar_visibility_watch(self):
        try:
            if bool(getattr(self, "_home_actionbar_watch_running", False)):
                return
            self._home_actionbar_watch_running = True

            def _tick():
                try:
                    if not bool(getattr(self, "_home_actionbar_watch_running", False)):
                        return
                    frag = getattr(self, "_home_actionbar_fragment", None)
                    btn = getattr(self, "_home_actionbar_btn", None)
                    if (frag is None) or (btn is None):
                        self._home_actionbar_watch_running = False
                        return
                    btn.setVisibility(View.GONE if self._is_home_actionbar_search_active(frag) else View.VISIBLE)
                    try:
                        if int(btn.getVisibility()) == int(View.VISIBLE):
                            self._layout_home_actionbar_shortcut(frag, btn)
                    except Exception:
                        pass
                    try:
                        self._sync_home_actionbar_title_spacing(frag)
                    except Exception:
                        pass
                    run_on_ui_thread(_tick, 250)
                except Exception:
                    self._home_actionbar_watch_running = False

            run_on_ui_thread(_tick, 250)
        except Exception:
            self._home_actionbar_watch_running = False

    def _stop_home_actionbar_visibility_watch(self):
        try:
            self._home_actionbar_watch_running = False
        except Exception:
            pass

    def _sync_home_actionbar_title_spacing(self, fragment, force_reset=False):
        try:
            if fragment is None:
                return
            avatar = None
            try:
                avatar = _get_private_field_silent(fragment, "avatarContainer")
            except Exception:
                avatar = None
            if avatar is None:
                return
            base_pad = int(AndroidUtilities.dp(12))
            target = base_pad
            try:
                last = int(getattr(self, "_home_actionbar_last_avatar_padding", -1))
            except Exception:
                last = -1
            if last == int(target):
                return
            try:
                if hasattr(avatar, "setLeftPadding"):
                    avatar.setLeftPadding(int(target))
                elif hasattr(avatar, "setPadding"):
                    t = int(target)
                    avatar.setPadding(t, avatar.getPaddingTop(), avatar.getPaddingRight(), avatar.getPaddingBottom())
            except Exception:
                pass
            try:
                self._home_actionbar_last_avatar_padding = int(target)
            except Exception:
                pass
            try:
                if hasattr(avatar, "requestLayout"):
                    avatar.requestLayout()
                if hasattr(avatar, "invalidate"):
                    avatar.invalidate()
            except Exception:
                pass
        except Exception:
            pass

    def _on_nowfy_panel_disable_logs_toggle(self, enabled):
        try:
            if NOWFY_CORE_API:
                NOWFY_CORE_API.on_panel_disable_logs_toggle(
                    self,
                    enabled,
                    _set_log_muted,
                    _set_print_muted,
                    _apply_log_wrapper,
                    _apply_print_wrapper,
                )
                return
        except Exception:
            pass
        try:
            self.set_setting("disable_logs", bool(enabled))
            _set_log_muted(bool(enabled))
            _set_print_muted(bool(enabled))
            _apply_log_wrapper(True)
            _apply_print_wrapper(True)
            self.reload_settings()
        except Exception:
            pass

    def _on_nowfy_lab_nowplaying_pill_toggle(self, enabled):
        core_called = False
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "on_lab_nowplaying_pill_toggle"):
                NOWFY_CORE_API.on_lab_nowplaying_pill_toggle(self, enabled)
                core_called = True
        except Exception:
            pass
        try:
            self.set_setting("nowplaying_pill_enabled", bool(enabled))
            self._start_nowplaying_pill_worker() if bool(enabled) else self._stop_nowplaying_pill_worker()
            self.reload_settings()
        except Exception:
            if core_called:
                try:
                    log(f"[Nowfy][Pulse] local toggle fallback failed")
                except Exception:
                    pass

    def _on_nowfy_lab_send_haptic_toggle(self, enabled):
        try:
            if NOWFY_CORE_API:
                NOWFY_CORE_API.on_lab_send_haptic_toggle(self, enabled)
                return
        except Exception:
            pass
        try:
            self.set_setting("send_haptic_enabled", bool(enabled))
            if bool(enabled):
                self._vibrate_feedback(35, 85)
            self.reload_settings()
        except Exception:
            pass

    def _clear_cache(self):
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "clear_cache_data"):
                NOWFY_CORE_API.clear_cache_data(self)
            else:
                try:
                    with self._cache_lock:
                        if hasattr(self, "_image_cache"):
                            self._image_cache.clear()
                        if hasattr(self, "_cache_timestamps"):
                            self._cache_timestamps.clear()
                        if hasattr(self, "_enhanced_image_cache"):
                            self._enhanced_image_cache.clear()
                        if hasattr(self, "_base_theme_cache"):
                            self._base_theme_cache.clear()
                        if hasattr(self, "_apple_cache"):
                            self._apple_cache.clear()
                except Exception:
                    pass
            try:
                run_on_ui_thread(lambda: BulletinHelper.show_success(tr("cache_cleared")))
            except Exception:
                BulletinHelper.show_success(tr("cache_cleared"))
        except Exception:
            try:
                run_on_ui_thread(lambda: BulletinHelper.show_info(tr("cache_cleared")))
            except Exception:
                try:
                    BulletinHelper.show_info(tr("cache_cleared"))
                except Exception:
                    pass

    def create_nowcast_info_warning(self):
        return [Divider(text="NowCast addon not installed")]

    def create_nowcast_how_to_use(self):
        return [Divider(text="NowCast addon not installed")]

    def create_services_subfragment(self):
        user_name = "User"
        try:
            from org.telegram.messenger import UserConfig, MessagesController
            account = getattr(UserConfig, 'selectedAccount', 0)
            mc = MessagesController.getInstance(account)
            uc = UserConfig.getInstance(account)
            if mc and uc:
                u = mc.getUser(uc.getClientUserId())
                if u and u.first_name:
                    user_name = u.first_name
        except Exception:
            pass
        items = [
            Divider(text=tr("nowfy_services_greeting").format(name=user_name)),
            Text(text="Spotify", icon="menu_feature_reliable", create_sub_fragment=self.create_spotify_credentials_subfragment, link_alias="nowfy_services_spotify"),
            Text(text="Last.FM", icon="msg_permissions_solar", create_sub_fragment=self.create_lastfm_credentials_subfragment, link_alias="nowfy_services_lastfm"),
            Text(text="Stats.FM", icon="menu_username_change", create_sub_fragment=self.create_statsfm_credentials_subfragment, link_alias="nowfy_services_statsfm"),
            Text(text="Yandex Music", icon="files_music", create_sub_fragment=self.create_ymusic_credentials_subfragment, link_alias="nowfy_services_ymusic"),
        ]
        return self._apply_link_aliases(items)

    def create_nowfy_panel_subfragment(self):
        def _addon_enabled(addon_key, default_value=True):
            try:
                if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "is_addon_enabled"):
                    return bool(NOWFY_CORE_API.is_addon_enabled(self, addon_key, default_value))
            except Exception:
                pass
            try:
                return bool(self.get_setting(addon_key, bool(default_value)))
            except Exception:
                return bool(default_value)
        addon_cache_settings_enabled = _addon_enabled("addon_cache_settings_enabled", False)
        addon_bio_features_enabled = _addon_enabled("addon_bio_features_enabled", False)
        addon_nowbox_enabled = _addon_enabled("addon_nowbox_enabled", False)
        items = [Divider(text=tr("nowfy_panel_section_desc"))]
        if addon_bio_features_enabled:
            items.append(Text(
                text=tr("smart_bio_header"),
                icon="msg_contacts",
                on_click=lambda _v: self._show_nowfy_panel_section_sheet("bio")
            ))
        if addon_cache_settings_enabled:
            items.append(Divider())
            items.append(Text(
                text=tr("show_cache_settings"),
                icon="msg_addfolder",
                on_click=lambda _v: self._show_nowfy_panel_section_sheet("cache")
            ))
        if addon_nowbox_enabled:
            items.append(Divider())
            items.append(Divider(text="Nowbox"))
            items.append(
                Switch(
                    key="hooking_enabled",
                    text="Nowbox",
                    subtext=tr("hooking_sub"),
                    default=self.get_setting("hooking_enabled", False),
                    icon="msg_viewreplies_solar",
                    on_change=lambda v: (
                        (self._start_hooking_worker(), self._apply_hooking_hint_hook()) if v else self._stop_hooking_worker(),
                        self.reload_settings()
                    ),
                    link_alias="nowfy_extended_hooking_enabled"
                )
            )
            if self._setting_bool("hooking_enabled", False):
                items.append(
                    Selector(
                        key="hooking_provider",
                        text=tr("hooking_provider_label"),
                        default=int(self.get_setting("hooking_provider", 0)),
                        items=["Spotify", "Last.fm", "Stats.fm"],
                        icon="msg_newphone",
                        on_change=lambda v: (
                            self.set_setting("hooking_provider", int(v)),
                            self.reload_settings()
                        ),
                        link_alias="nowfy_extended_hooking_provider"
                    )
                )
                items.append(
                    Switch(
                        key="nowbox_show_cover_actionbar",
                        text=tr("nowbox_show_cover_label"),
                        subtext=tr("nowbox_show_cover_sub"),
                        default=self.get_setting("nowbox_show_cover_actionbar", False),
                        icon="msg_photos",
                        on_change=lambda v: (
                            self.set_setting("nowbox_show_cover_actionbar", bool(v)),
                            self.reload_settings()
                        ),
                        link_alias="nowfy_extended_nowbox_show_cover_actionbar"
                    )
                )
                items.append(
                    Switch(
                        key="nowbox_lyrics_enabled",
                        text=tr("nowbox_lyrics_label"),
                        subtext=tr("nowbox_lyrics_sub"),
                        default=self.get_setting("nowbox_lyrics_enabled", False),
                        icon="menu_quote_remix",
                        on_change=lambda v: (
                            self.set_setting("nowbox_lyrics_enabled", bool(v)),
                            self.reload_settings()
                        ),
                        link_alias="nowfy_extended_nowbox_lyrics_enabled"
                    )
                )
                items.append(
                    Selector(
                        key="nowbox_eq_mode",
                        text=tr("nowbox_eq_label"),
                        default=int(self.get_setting("nowbox_eq_mode", 0)),
                        items=["Off", "On"],
                        icon="msg_noise_on_remix",
                        on_change=lambda v: (
                            self.set_setting("nowbox_eq_mode", int(v)),
                            self.reload_settings()
                        ),
                        link_alias="nowfy_extended_nowbox_eq_mode"
                    )
                )
                if int(self.get_setting("nowbox_eq_mode", 0)) == 1:
                    items.append(
                        Text(
                            text=tr("nowbox_eq_color_label"),
                            icon="ic_colorpicker_solar",
                            on_click=lambda v: self._open_color_picker_for_setting("nowbox_eq_color", "nowbox_eq_color_title"),
                            link_alias="nowfy_extended_nowbox_eq_color"
                        )
                    )
        items.append(Divider())
        items.append(Text(
            text=tr("diversos_header"),
            icon="notifications_settings",
            on_click=lambda _v: self._show_nowfy_panel_section_sheet("misc")
        ))
        items.append(Divider())
        items.append(
            Switch(
                key="nowfy_pocket_shortcut_enabled",
                text="Nowfy Pocket",
                default=bool(self.get_setting("nowfy_pocket_shortcut_enabled", False)),
                icon="msg_tone_on",
                on_change=lambda v: (
                    self.set_setting("nowfy_pocket_shortcut_enabled", bool(v)),
                    self.remove_menu_items(),
                    self._add_menu_items(),
                    self.reload_settings()
                ),
            )
        )
        items.append(Divider())
        items.append(Selector(
            key="plugin_lang",
            text=tr("plugin_lang_label"),
            default=self._get_plugin_lang_index(),
            items=[
                tr("lang_english"),
                tr("lang_portuguese"),
                tr("lang_russian"),
            ],
            icon="msg_plugins",
            on_change=self._on_change_plugin_lang,
            link_alias="nowfy_panel_plugin_lang"
        ))
        return self._apply_link_aliases(items)

    def _open_plugin_subfragment(self, callback):
        try:
            controller = PluginsController.getInstance()
            plugin = controller.plugins.get(self.id)
            fragment = get_last_fragment()
            if not plugin or not fragment:
                return
            activity = PluginSettingsActivity(plugin)
            try:
                self._set_subfragment_callback(activity, callback)
            except Exception:
                pass
            fragment.presentFragment(activity)
        except Exception:
            pass

    def _show_panel_text_input_dialog(self, title_text, setting_key, default_text="", on_apply=None):
        try:
            frag = get_last_fragment()
            ctx = frag.getParentActivity() if frag and frag.getParentActivity() else ApplicationLoader.applicationContext
            if not ctx:
                return
            from org.telegram.ui.Components import EditTextBoldCursor
            from android.text import InputType
            from android.widget import LinearLayout
            from android.graphics.drawable import GradientDrawable
            input_field = EditTextBoldCursor(ctx)
            input_field.setHint(str(default_text or ""))
            input_field.setInputType(InputType.TYPE_CLASS_TEXT)
            input_field.setMaxLines(1)
            input_field.setSingleLine(True)
            input_field.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
            try:
                input_field.setText(str(self.get_setting(setting_key, default_text) or ""))
            except Exception:
                pass
            try:
                input_field.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
                input_field.setHintTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
                input_field.setCursorColor(Theme.getColor(Theme.key_dialogTextLink))
            except Exception:
                try:
                    input_field.setTextColor(Theme.getColor(Theme.key_dialogTextBlack))
                    input_field.setHintTextColor(Theme.getColor(Theme.key_dialogTextHint))
                    input_field.setCursorColor(Theme.getColor(Theme.key_dialogTextLink))
                except Exception:
                    pass
            try:
                input_field.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(12), AndroidUtilities.dp(12), AndroidUtilities.dp(12))
            except Exception:
                pass
            try:
                ip_bg = GradientDrawable()
                ip_bg.setCornerRadius(AndroidUtilities.dp(12))
                try:
                    ip_bg.setColor(Theme.getColor(Theme.key_windowBackgroundWhite))
                    ip_bg.setStroke(AndroidUtilities.dp(1), Theme.getColor(Theme.key_windowBackgroundWhiteGrayText4))
                except Exception:
                    ip_bg.setColor(0x1A2A3A52)
                    ip_bg.setStroke(AndroidUtilities.dp(1), 0x556FA8DC)
                input_field.setBackground(ip_bg)
            except Exception:
                pass
            content = LinearLayout(ctx)
            content.setOrientation(LinearLayout.VERTICAL)
            try:
                content.setPadding(AndroidUtilities.dp(22), AndroidUtilities.dp(8), AndroidUtilities.dp(22), AndroidUtilities.dp(8))
            except Exception:
                pass
            content.addView(input_field)
            builder = AlertDialogBuilder(ctx)
            builder.set_title(str(title_text or ""))
            builder.set_view(content)
            def _save(dlg, _which):
                try:
                    val = str(input_field.getText().toString() if input_field.getText() is not None else "").strip()
                except Exception:
                    val = ""
                try:
                    self.set_setting(setting_key, val)
                    self.reload_settings()
                except Exception:
                    pass
                try:
                    if callable(on_apply):
                        on_apply(val)
                except Exception:
                    pass
                try:
                    if dlg:
                        dlg.dismiss()
                except Exception:
                    pass
            builder.set_positive_button(tr("save"), _save)
            builder.set_negative_button(tr("cancel"), lambda d, w: d.dismiss() if d else None)
            run_on_ui_thread(builder.show)
        except Exception:
            pass

    def _show_cache_advanced_options_sheet(self):
        try:
            frag = get_last_fragment()
            ctx = frag.getParentActivity() if frag and frag.getParentActivity() else ApplicationLoader.applicationContext
            if not ctx:
                return
            sheet = BottomSheet(ctx, True)
            root = LinearLayout(ctx)
            root.setOrientation(LinearLayout.VERTICAL)
            try:
                root.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(14), AndroidUtilities.dp(16), AndroidUtilities.dp(18))
            except Exception:
                pass
            def _row(title, sub, key, default=False):
                cur = bool(self._setting_bool(key, default))
                wrap = LinearLayout(ctx)
                wrap.setOrientation(LinearLayout.HORIZONTAL)
                wrap.setGravity(Gravity.CENTER_VERTICAL)
                wrap.setClickable(True)
                wrap.setFocusable(True)
                try:
                    wrap.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(12))
                except Exception:
                    pass
                bg = GradientDrawable()
                bg.setCornerRadius(float(AndroidUtilities.dp(14)))
                try:
                    bg.setColor(Theme.getColor(Theme.key_dialogBackground))
                    bg.setStroke(AndroidUtilities.dp(1), Theme.getColor(Theme.key_windowBackgroundWhiteGrayText4))
                except Exception:
                    bg.setColor(0x1A2A3A52)
                wrap.setBackground(bg)
                left = LinearLayout(ctx)
                left.setOrientation(LinearLayout.VERTICAL)
                t = TextView(ctx)
                t.setText(str(title or ""))
                t.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
                try:
                    t.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
                except Exception:
                    pass
                left.addView(t)
                st = TextView(ctx)
                st.setText(str(sub or ""))
                st.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
                try:
                    st.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
                except Exception:
                    pass
                left.addView(st)
                wrap.addView(left, LinearLayout.LayoutParams(0, -2, 1.0))
                rv = TextView(ctx)
                rv.setText(tr("nowfy_extended_cover_blur_on") if cur else tr("nowfy_extended_cover_blur_off"))
                rv.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
                try:
                    rv.setPadding(AndroidUtilities.dp(10), AndroidUtilities.dp(6), AndroidUtilities.dp(10), AndroidUtilities.dp(6))
                except Exception:
                    pass
                chip = GradientDrawable()
                chip.setCornerRadius(float(AndroidUtilities.dp(999)))
                try:
                    chip.setColor(Theme.getColor(Theme.key_featuredStickers_addButton))
                    rv.setTextColor(Theme.getColor(Theme.key_featuredStickers_buttonText))
                except Exception:
                    chip.setColor(0x334A8DFF)
                rv.setBackground(chip)
                try:
                    rv.setMinWidth(AndroidUtilities.dp(76))
                    rv.setGravity(Gravity.CENTER)
                except Exception:
                    pass
                wrap.addView(rv)
                def _toggle():
                    try:
                        self.set_setting(key, not bool(self._setting_bool(key, default)))
                        self.reload_settings()
                    except Exception:
                        pass
                    try:
                        sheet.dismiss()
                    except Exception:
                        pass
                    run_on_ui_thread(lambda: self._show_cache_advanced_options_sheet())
                wrap.setOnClickListener(OnClickListener(lambda _v: _toggle()))
                lp = LinearLayout.LayoutParams(-1, -2)
                lp.bottomMargin = AndroidUtilities.dp(8)
                root.addView(wrap, lp)
            title = TextView(ctx)
            title.setText(tr("advanced_options_title"))
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18)
            try:
                title.setTypeface(AndroidUtilities.bold())
            except Exception:
                pass
            try:
                title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                pass
            root.addView(title)
            _row(tr("youtube_cache"), tr("youtube_cache_sub"), "enable_youtube_thumbnail_cache", False)
            _row(tr("soundcloud_cache"), tr("soundcloud_cache_sub"), "enable_soundcloud_thumbnail_cache", False)
            _row(tr("quality_fallback"), tr("quality_fallback_sub"), "enable_quality_fallback", True)
            _row(tr("url_cache"), tr("url_cache_sub"), "enable_url_cache", True)
            _row(tr("adaptive_compression"), tr("adaptive_compression_sub"), "enable_adaptive_compression", False)
            back_btn = TextView(ctx)
            back_btn.setText(tr("statsfm_top_back_button"))
            back_btn.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
            back_btn.setGravity(Gravity.CENTER)
            try:
                back_btn.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(12))
            except Exception:
                pass
            bg_back = GradientDrawable()
            bg_back.setCornerRadius(float(AndroidUtilities.dp(12)))
            try:
                bg_back.setColor(Theme.getColor(Theme.key_windowBackgroundGray))
                back_btn.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlueText))
            except Exception:
                bg_back.setColor(0x22394B6A)
            back_btn.setBackground(bg_back)
            def _go_back(_v):
                try:
                    sheet.dismiss()
                except Exception:
                    pass
                run_on_ui_thread(lambda: self._show_nowfy_panel_section_sheet("cache"))
            back_btn.setOnClickListener(OnClickListener(_go_back))
            lp_back = LinearLayout.LayoutParams(-1, -2)
            lp_back.topMargin = AndroidUtilities.dp(8)
            root.addView(back_btn, lp_back)
            sheet.setCustomView(root)
            run_on_ui_thread(sheet.show)
        except Exception:
            pass

    def _show_nowfy_panel_section_sheet(self, section_key):
        try:
            frag = get_last_fragment()
            ctx = frag.getParentActivity() if frag and frag.getParentActivity() else ApplicationLoader.applicationContext
            if not ctx:
                return
            sheet = BottomSheet(ctx, True)
            root_scroll = ScrollView(ctx)
            root = LinearLayout(ctx)
            root.setOrientation(LinearLayout.VERTICAL)
            try:
                root.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(14), AndroidUtilities.dp(16), AndroidUtilities.dp(18))
            except Exception:
                pass
            root_scroll.addView(root)

            def _divider(label):
                tv = TextView(ctx)
                tv.setText(str(label or ""))
                tv.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
                try:
                    tv.setTypeface(AndroidUtilities.bold())
                except Exception:
                    pass
                try:
                    tv.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
                except Exception:
                    pass
                lp = LinearLayout.LayoutParams(-1, -2)
                lp.topMargin = AndroidUtilities.dp(10)
                lp.bottomMargin = AndroidUtilities.dp(6)
                root.addView(tv, lp)

            def _row(label, subtext=None, value=None, on_click=None, red=False):
                wrap = LinearLayout(ctx)
                wrap.setOrientation(LinearLayout.HORIZONTAL)
                wrap.setGravity(Gravity.CENTER_VERTICAL)
                wrap.setClickable(True)
                wrap.setFocusable(True)
                try:
                    wrap.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(12))
                except Exception:
                    pass
                bg = GradientDrawable()
                bg.setCornerRadius(float(AndroidUtilities.dp(14)))
                try:
                    if bool(red):
                        bg.setColor(Theme.getColor(Theme.key_dialogBackground))
                        try:
                            bg.setStroke(AndroidUtilities.dp(1), Theme.getColor(Theme.key_dialogTextRed))
                        except Exception:
                            bg.setStroke(AndroidUtilities.dp(1), Theme.getColor(Theme.key_text_RedBold))
                    else:
                        bg.setColor(Theme.getColor(Theme.key_dialogBackground))
                        bg.setStroke(AndroidUtilities.dp(1), Theme.getColor(Theme.key_windowBackgroundWhiteGrayText4))
                except Exception:
                    bg.setColor(0x1A2A3A52)
                wrap.setBackground(bg)
                left = LinearLayout(ctx)
                left.setOrientation(LinearLayout.VERTICAL)
                t = TextView(ctx)
                t.setText(str(label or ""))
                t.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
                try:
                    if bool(red):
                        try:
                            t.setTextColor(Theme.getColor(Theme.key_text_RedBold))
                        except Exception:
                            t.setTextColor(Theme.getColor(Theme.key_dialogTextRed))
                    else:
                        t.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
                except Exception:
                    pass
                left.addView(t)
                if subtext:
                    st = TextView(ctx)
                    st.setText(str(subtext))
                    st.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
                    try:
                        st.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
                    except Exception:
                        pass
                    left.addView(st)
                wrap.addView(left, LinearLayout.LayoutParams(0, -2, 1.0))
                if value is not None:
                    rv = TextView(ctx)
                    rv.setText(str(value))
                    rv.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
                    try:
                        rv.setPadding(AndroidUtilities.dp(10), AndroidUtilities.dp(6), AndroidUtilities.dp(10), AndroidUtilities.dp(6))
                    except Exception:
                        pass
                    chip = GradientDrawable()
                    chip.setCornerRadius(float(AndroidUtilities.dp(999)))
                    try:
                        chip.setColor(Theme.getColor(Theme.key_featuredStickers_addButton))
                        rv.setTextColor(Theme.getColor(Theme.key_featuredStickers_buttonText))
                    except Exception:
                        chip.setColor(0x334A8DFF)
                    rv.setBackground(chip)
                    try:
                        rv.setMinWidth(AndroidUtilities.dp(64))
                        rv.setGravity(Gravity.CENTER)
                    except Exception:
                        pass
                    wrap.addView(rv)
                if callable(on_click):
                    wrap.setOnClickListener(OnClickListener(lambda _v: on_click()))
                lp = LinearLayout.LayoutParams(-1, -2)
                lp.bottomMargin = AndroidUtilities.dp(8)
                root.addView(wrap, lp)

            def _bool_value(key, default=False):
                try:
                    return bool(self._setting_bool(key, default))
                except Exception:
                    return bool(self.get_setting(key, default))

            def _toggle_row(key, text_key, sub_key=None, default=False, on_change=None):
                cur = _bool_value(key, default)
                _row(tr(text_key), tr(sub_key) if sub_key else None, tr("nowfy_extended_cover_blur_on") if cur else tr("nowfy_extended_cover_blur_off"), on_click=lambda: _toggle_apply(), red=False)
                def _toggle_apply():
                    nv = not _bool_value(key, default)
                    try:
                        self.set_setting(key, nv)
                        self.reload_settings()
                    except Exception:
                        pass
                    try:
                        if callable(on_change):
                            on_change(nv)
                    except Exception:
                        pass
                    try:
                        sheet.dismiss()
                    except Exception:
                        pass
                    run_on_ui_thread(lambda: self._show_nowfy_panel_section_sheet(section_key))

            def _cycle_row(key, title, options, default_idx=0, on_apply=None):
                try:
                    idx = int(self.get_setting(key, default_idx) or 0)
                except Exception:
                    idx = int(default_idx)
                if idx < 0 or idx >= len(options):
                    idx = int(default_idx)
                _row(title, None, str(options[idx]), on_click=lambda: _cycle_apply())
                def _cycle_apply():
                    try:
                        cur = int(self.get_setting(key, default_idx) or 0)
                    except Exception:
                        cur = int(default_idx)
                    nxt = (cur + 1) % max(1, len(options))
                    try:
                        self.set_setting(key, int(nxt))
                        self.reload_settings()
                    except Exception:
                        pass
                    try:
                        if callable(on_apply):
                            on_apply(int(nxt))
                    except Exception:
                        pass
                    try:
                        sheet.dismiss()
                    except Exception:
                        pass
                    run_on_ui_thread(lambda: self._show_nowfy_panel_section_sheet(section_key))

            if section_key == "bio":
                _divider(tr("bio_automation_section"))
                _toggle_row("enable_autobio", "smart_bio_enabled", "autobio_sub", False)
                _toggle_row("enable_auto_bio_update", "smart_bio_auto_refresh", "enable_auto_bio_update_sub", False)
                _toggle_row("show_bio_notification", "show_bio_notification", "show_bio_notification_sub", True)
                try:
                    service_items, _service_keys, service_default_idx = (NOWFY_CORE_API.get_bio_feature_services(self) if NOWFY_CORE_API else ([], [], 0))
                except Exception:
                    service_items, service_default_idx = ([], 0)
                if len(service_items) >= 2:
                    _cycle_row("bio_feature_service_idx", tr("services"), service_items, int(service_default_idx), on_apply=lambda v: self.set_setting("bio_feature_service_idx", v))
                _divider(tr("bio_customization_section_hint"))
                _row(tr("bio_text"), None, ">", on_click=lambda: self._show_panel_text_input_dialog(tr("bio_text"), "autobio_text", "Now Playing: {track} by {artist}"))
                _row(tr("restore_bio_text"), None, ">", on_click=lambda: self._show_panel_text_input_dialog(tr("restore_bio_text"), "restore_bio_text", "I'm using nowFy!"))
                _divider(tr("bio_help_section"))
                _row(tr("bio_command_info"), None, ">", on_click=lambda: self._show_bio_command_info_dialog())
            elif section_key == "cache":
                _divider(tr("cache_core_section"))
                _toggle_row("enable_cache", "enable_cache", "enable_cache_sub", False, on_change=lambda v: self._toggle_cache_system(v))
                _toggle_row("enable_compression", "enable_compression", "enable_compression_sub", False)
                _row(tr("cache_ttl"), None, ">", on_click=lambda: self._show_panel_text_input_dialog(tr("cache_ttl"), "cache_ttl", "5", on_apply=lambda v: self._on_cache_ttl_changed(v)))
                _divider(tr("cache_loading_section"))
                _cycle_row(
                    "enable_preload",
                    tr("enable_preload"),
                    [tr("nowfy_extended_cover_blur_on"), tr("nowfy_extended_cover_blur_off")],
                    0 if _bool_value("enable_preload", False) else 1,
                    on_apply=lambda v: self._toggle_preload_system(int(v) == 0)
                )
                _divider(tr("cache_performance_section"))
                _toggle_row("enhanced_cache", "enhanced_cache", "enhanced_cache_sub", True)
                _cycle_row("performance_mode", tr("performance_mode"), [tr("turbo_mode"), tr("balanced_mode"), tr("quality_mode")], 1)
                _row(tr("advanced_options_title"), None, ">", on_click=lambda: _open_advanced_from_sheet())
                _divider(tr("cache_management_section"))
                _row(tr("clear_cache"), None, ">", on_click=lambda: _clear_cache_from_sheet(), red=True)
            else:
                _divider(tr("interface_settings_section"))
                _toggle_row("show_chat_menu", "diversos_show_chat_menu", "show_chat_menu_sub", True, on_change=lambda _v: self.reload_settings())
                _toggle_row("nowfy_drawer_enabled", "nowfy_drawer_label", "nowfy_drawer_sub", True, on_change=lambda v: self._on_nowfy_panel_drawer_toggle(v))
                _toggle_row("nowfy_home_actionbar_enabled", "nowfy_home_actionbar_label", "nowfy_home_actionbar_sub", False, on_change=lambda v: self._on_nowfy_panel_home_actionbar_toggle(v))
                _toggle_row("nowfy_stats_enabled", "nowfy_stats_label", "nowfy_stats_sub", True)
                _toggle_row("disable_logs", "disable_logs_label", "disable_logs_sub", False, on_change=lambda v: self._on_nowfy_panel_disable_logs_toggle(v))

            close_btn = TextView(ctx)
            close_btn.setText(tr("cancel"))
            close_btn.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
            close_btn.setGravity(Gravity.CENTER)
            try:
                close_btn.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(12))
            except Exception:
                pass
            bg_close = GradientDrawable()
            bg_close.setCornerRadius(float(AndroidUtilities.dp(12)))
            try:
                bg_close.setColor(Theme.getColor(Theme.key_windowBackgroundGray))
                close_btn.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlueText))
            except Exception:
                bg_close.setColor(0x22394B6A)
            close_btn.setBackground(bg_close)
            close_btn.setOnClickListener(OnClickListener(lambda _v: sheet.dismiss()))
            def _clear_cache_from_sheet():
                try:
                    sheet.dismiss()
                except Exception:
                    pass
                run_on_queue(lambda: self._clear_cache())
            def _open_advanced_from_sheet():
                try:
                    sheet.dismiss()
                except Exception:
                    pass
                run_on_ui_thread(self._show_cache_advanced_options_sheet)
            lp_close = LinearLayout.LayoutParams(-1, -2)
            lp_close.topMargin = AndroidUtilities.dp(8)
            root.addView(close_btn, lp_close)
            sheet.setCustomView(root_scroll)
            run_on_ui_thread(sheet.show)
        except Exception:
            pass

    def create_nowfy_core_subfragment(self):
        items = []
        try:
            core_inst = getattr(self, "core", None)
            if core_inst is not None and hasattr(core_inst, "create_settings"):
                items = core_inst.create_settings() or []
        except Exception:
            items = []
        if not items:
            items = [
                Divider(text="Nowfy Core options are unavailable right now."),
            ]
        return self._apply_link_aliases(items)

    def create_nowfy_lab_subfragment(self):
        def _addon_enabled(addon_key, default_value=True):
            try:
                if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "is_addon_enabled"):
                    return bool(NOWFY_CORE_API.is_addon_enabled(self, addon_key, default_value))
            except Exception:
                pass
            try:
                return bool(self.get_setting(addon_key, bool(default_value)))
            except Exception:
                return bool(default_value)
        items = [
            Divider(text=tr("nowfy_lab_section_desc")),
            Text(text=tr("nowfy_myconfigs_title"), icon="menu_sendfile_plus", create_sub_fragment=self.create_myconfigs_subfragment, link_alias="nowfy_lab_myconfigs"),
        ]
        try:
            items.insert(2, Text(text="Nowfy Core", icon="msg_settings", create_sub_fragment=self.create_nowfy_core_subfragment, link_alias="nowfy_lab_core"))
        except Exception:
            items.append(Text(text="Nowfy Core", icon="msg_settings", create_sub_fragment=self.create_nowfy_core_subfragment, link_alias="nowfy_lab_core"))
        if _addon_enabled("addon_nowcast_enabled", False):
            items.append(Text(text=tr("NowCast"), icon="filled_premium_bots", create_sub_fragment=self.create_nowcast_subfragment, link_alias="nowfy_lab_nowcast"))
        items.extend([
            Divider(text=tr("appearance_options_section")),
        ])
        items.append(
            Switch(
                key="enable_aurasend_on_send",
                text="AuraSend",
                subtext=tr("send_visual_effect_sub"),
                default=False,
                icon="msg_brightness_low_solar",
                on_change=lambda v: self.reload_settings(),
                link_alias="nowfy_lab_aurasend"
            )
        )
        items.append(
            Switch(
                key="enable_flip_on_send",
                text=tr("nowfy_lab_flip_on_send_title"),
                subtext=tr("nowfy_lab_flip_on_send_sub"),
                default=False,
                icon="msg_arrow_avatar",
                on_change=lambda v: self.reload_settings(),
                link_alias="nowfy_lab_flip_on_send"
            )
        )
        items.append(
            Switch(
                key="enable_quick_dismiss",
                text=tr("quick_dismiss_label"),
                subtext=tr("quick_dismiss_subtext"),
                default=True,
                icon="msg_autodelete_badge2",
                on_change=lambda v: self.reload_settings(),
                link_alias="nowfy_lab_quick_dismiss"
            )
        )
        items.append(
            Switch(
                key="send_haptic_enabled",
                text=tr("send_haptic_label"),
                subtext=tr("send_haptic_sub"),
                default=self.get_setting("send_haptic_enabled", False),
                icon="msg_location_alert",
                on_change=lambda v: self._on_nowfy_lab_send_haptic_toggle(v),
                link_alias="nowfy_lab_send_haptic"
            )
        )
        items.append(Divider(text=tr("compact_card_images_section")))
        items.append(
            Switch(
                key="compact_card_images",
                text=tr("compact_card_images"),
                subtext=tr("compact_card_images_sub"),
                default=False,
                icon="menu_quality_sd",
                on_change=lambda v: self.set_setting("compact_card_images", bool(v)),
                link_alias="nowfy_lab_compact_card_images"
            )
        )
        return self._apply_link_aliases(items)

    def create_myconfigs_subfragment(self):
        items = [
            Divider(text=tr("nowfy_myconfigs_desc")),
            Text(
                text=tr("nowfy_backup_create"),
                icon="files_internal_remix",
                on_click=lambda v: BackupManager(self).export_backup(),
                link_alias="nowfy_myconfigs_backup_create"
            ),
            Text(
                text=tr("nowfy_backup_restore"),
                icon="msg_retry",
                on_click=lambda v: self._open_backup_restore_sheet(),
                link_alias="nowfy_myconfigs_backup_restore"
            ),
            Divider(text=tr("nowfy_backup_section_files")),
            Text(
                text=tr("nowfy_backup_manage"),
                icon="msg_folder_solar",
                on_click=lambda v: self._open_backup_manager(),
                link_alias="nowfy_myconfigs_backup_manage"
            ),
            Text(
                text=tr("nowfy_backup_upload"),
                icon="gift_upgrade",
                on_click=lambda v: self._open_backup_upload_from_main(),
                link_alias="nowfy_myconfigs_backup_upload"
            ),
        ]
        return self._apply_link_aliases(items)

    def _open_backup_restore_sheet(self):
        try:
            import os
            files = self._list_backup_files_local()
            if not files:
                BulletinHelper.show_info(tr("backup_no_backups_found"))
                return
            fragment = get_last_fragment()
            if not fragment:
                return
            ctx = fragment.getParentActivity() if fragment and fragment.getParentActivity() else ApplicationLoader.applicationContext
            from org.telegram.ui.ActionBar import BottomSheet, Theme
            from org.telegram.ui.Components import LayoutHelper
            from android.widget import LinearLayout, TextView
            from android.view import Gravity
            from android.util import TypedValue
            from android.graphics.drawable import GradientDrawable
            try:
                from androidx.core.widget import NestedScrollView
            except Exception:
                NestedScrollView = None
            try:
                from android_utils import OnClickListener
            except Exception:
                OnClickListener = None
            sheet = BottomSheet(ctx, True)
            container = LinearLayout(ctx)
            container.setOrientation(LinearLayout.VERTICAL)
            container.setPadding(AndroidUtilities.dp(18), AndroidUtilities.dp(18), AndroidUtilities.dp(18), AndroidUtilities.dp(14))
            title = TextView(ctx)
            title.setText(tr("nowfy_backup_restore_title"))
            try:
                title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                title.setTextColor(0xFFFFFFFF)
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 20)
            try:
                title.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_MEDIUM))
            except Exception:
                pass
            container.addView(title, LayoutHelper.createLinear(-1, -2, Gravity.START, 0, 0, 0, 6))
            subtitle = TextView(ctx)
            subtitle.setText(tr("nowfy_backup_restore_sheet_desc"))
            subtitle.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
            subtitle.setGravity(Gravity.START)
            try:
                subtitle.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            except Exception:
                subtitle.setTextColor(0xFFB7BFCC)
            container.addView(subtitle, LayoutHelper.createLinear(-1, -2, Gravity.START, 0, 0, 0, 12))
            list_wrap = LinearLayout(ctx)
            list_wrap.setOrientation(LinearLayout.VERTICAL)
            backup_dir = BackupManager(self).backup_dir
            for idx, name in enumerate(files):
                try:
                    item = LinearLayout(ctx)
                    item.setOrientation(LinearLayout.VERTICAL)
                    item.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(12))
                    try:
                        item_bg = GradientDrawable()
                        item_bg.setCornerRadius(AndroidUtilities.dp(14))
                        try:
                            item_bg.setColor(Theme.getColor(Theme.key_dialogBackground))
                        except Exception:
                            item_bg.setColor(0xFF1E2330)
                        try:
                            item_bg.setStroke(AndroidUtilities.dp(1), Theme.getColor(Theme.key_windowBackgroundWhiteGrayText4))
                        except Exception:
                            item_bg.setStroke(AndroidUtilities.dp(1), 0x334C5A73)
                        item.setBackground(item_bg)
                    except Exception:
                        pass
                    size_text = ""
                    try:
                        size_bytes = os.path.getsize(os.path.join(backup_dir, name))
                        size_kb = max(1, int(size_bytes / 1024))
                        size_text = f"{size_kb} KB"
                    except Exception:
                        size_text = ""
                    name_view = TextView(ctx)
                    name_view.setText(str(name))
                    name_view.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
                    name_view.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
                    try:
                        name_view.setTypeface(AndroidUtilities.getTypeface(AndroidUtilities.TYPEFACE_ROBOTO_MEDIUM))
                    except Exception:
                        pass
                    item.addView(name_view, LayoutHelper.createLinear(-1, -2))
                    sub = TextView(ctx)
                    sub.setText(size_text)
                    sub.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
                    sub.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 12)
                    item.addView(sub, LayoutHelper.createLinear(-1, -2, Gravity.START, 0, 4, 0, 0))
                    def _make_click(ix, item_view):
                        def _click(v):
                            try:
                                try:
                                    item_view.setAlpha(0.6)
                                    item_view.postDelayed(lambda: item_view.setAlpha(1.0), 140)
                                except Exception:
                                    pass
                                try:
                                    sheet.dismiss()
                                except Exception:
                                    pass
                                selected = files[ix]
                                log("[Nowfy] Restore selected")
                                BackupManager(self).restore_from_backup(selected)
                            except Exception:
                                log("[Nowfy] Error restoring backup")
                                BulletinHelper.show_info(tr("backup_restore_error"))
                        return _click
                    if OnClickListener:
                        item.setOnClickListener(OnClickListener(_make_click(idx, item)))
                    else:
                        item.setOnClickListener(lambda v, ix=idx, it=item: _make_click(ix, it)(v))
                    list_wrap.addView(item, LayoutHelper.createLinear(-1, -2, Gravity.START, 0, 0, 0, 10))
                except Exception:
                    pass
            if NestedScrollView is not None and len(files) > 2:
                scroll = NestedScrollView(ctx)
                try:
                    scroll.setFillViewport(False)
                except Exception:
                    pass
                scroll.addView(list_wrap, LayoutHelper.createFrame(-1, -2))
                visible_rows = 2
                row_height = AndroidUtilities.dp(58)
                max_h = AndroidUtilities.dp(180)
                desired_h = visible_rows * row_height
                if desired_h > max_h:
                    desired_h = max_h
                container.addView(scroll, LayoutHelper.createLinear(-1, desired_h))
            else:
                container.addView(list_wrap, LayoutHelper.createLinear(-1, -2))
            close_btn = TextView(ctx)
            close_btn.setText(tr("nowfy_backup_restore_back_button"))
            close_btn.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
            close_btn.setGravity(Gravity.CENTER)
            try:
                close_btn.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(10), AndroidUtilities.dp(16), AndroidUtilities.dp(10))
            except Exception:
                pass
            try:
                close_bg = GradientDrawable()
                close_bg.setCornerRadius(AndroidUtilities.dp(20))
                try:
                    close_bg.setColor(Theme.getColor(Theme.key_featuredStickers_addButton))
                except Exception:
                    close_bg.setColor(0xFF2B7FFF)
                try:
                    close_bg.setStroke(AndroidUtilities.dp(2), Theme.getColor(Theme.key_dialogTextBlue))
                except Exception:
                    close_bg.setStroke(AndroidUtilities.dp(2), 0xFF8FC1FF)
                close_btn.setBackground(close_bg)
                try:
                    close_btn.setTextColor(Theme.getColor(Theme.key_featuredStickers_buttonText))
                except Exception:
                    close_btn.setTextColor(0xFFFFFFFF)
            except Exception:
                pass
            try:
                if OnClickListener:
                    close_btn.setOnClickListener(OnClickListener(lambda v: sheet.dismiss()))
                else:
                    close_btn.setOnClickListener(lambda v: sheet.dismiss())
            except Exception:
                pass
            container.addView(close_btn, LayoutHelper.createLinear(-1, -2, Gravity.TOP, 0, AndroidUtilities.dp(14), 0, 0))
            sheet.setCustomView(container)
            run_on_ui_thread(sheet.show)
        except Exception:
            try:
                BulletinHelper.show_info(tr("backup_list_error"))
            except Exception:
                pass

    def create_extended_subfragment(self):
        items = [Divider(text=tr("nowfy_extended_section_desc"))]
        items.append(Divider())
        items.append(Text(text="Now Tab", icon="msg_media", create_sub_fragment=self.create_extended_tab_subfragment, link_alias="nowfy_extended_now_tab"))
        items.append(Divider())
        items.append(Text(text="Nowfy Flow", icon="files_music", create_sub_fragment=self.create_extended_flow_subfragment, link_alias="nowfy_extended_nowfy_flow"))
        items.append(Divider())
        items.append(Text(text=tr("nowfy_extended_cover_label"), icon="msg_copy_photo_solar", create_sub_fragment=self.create_extended_home_cover_subfragment, link_alias="nowfy_extended_home_cover"))
        items.append(Divider())
        items.append(
            Switch(
                key="nowfy_quick_flow_enabled",
                text=tr("nowfy_quick_flow_title"),
                subtext=tr("nowfy_quick_flow_sub"),
                default=bool(self.get_setting("nowfy_quick_flow_enabled", True)),
                icon="msg_share_solar",
                on_change=lambda v: (
                    self.set_setting("nowfy_quick_flow_enabled", bool(v)),
                    self.set_setting("nowfy_flow_card_mode", "cc") if bool(v) else None,
                    self.set_setting("nowfy_flow_bt_debug", True) if bool(v) else None,
                    self._apply_chat_fab_state(),
                    self.reload_settings()
                ),
                link_alias="nowfy_quick_flow_enabled"
            )
        )
        if bool(self.get_setting("nowfy_quick_flow_enabled", True)):
            items.append(
                Selector(
                    key="nowfy_quick_flow_side_mode",
                    text=tr("nowfy_quick_flow_side_mode_title"),
                    default=int(self.get_setting("nowfy_quick_flow_side_mode", 0) or 0),
                    items=[tr("nowfy_flow_alpha_default"), tr("nowfy_flow_side_free")],
                    icon="msg_inputarrow",
                    on_change=lambda v: (
                        self.set_setting("nowfy_quick_flow_side_mode", int(v)),
                        self._reset_nowfy_quick_flow_free_position() if int(v) == 0 else None,
                        self._update_chat_fab_position_once(),
                        self.reload_settings()
                    ),
                    link_alias="nowfy_quick_flow_side_mode"
                )
            )
        items.append(Divider())
        items.append(
            Switch(
                key="nowplaying_pill_enabled",
                text="Nowfy Pulse",
                subtext=tr("nowfy_extended_pill_sub"),
                default=self.get_setting("nowplaying_pill_enabled", False),
                icon="input_notify_on",
                on_change=lambda v: self._on_nowfy_lab_nowplaying_pill_toggle(v),
                link_alias="nowfy_extended_nowplaying_pill"
            )
        )
        if bool(self.get_setting("nowplaying_pill_enabled", False)):
            items.append(
                Selector(
                    key="nowplaying_pill_style",
                    text="Nowfy Pulse",
                    default=int(self.get_setting("nowplaying_pill_style", 0) or 0),
                    items=[tr("nowfy_pulse_style_pill"), "Applefy"],
                    icon="msg_replace_remix",
                    on_change=lambda v: self.set_setting("nowplaying_pill_style", int(v)),
                    link_alias="nowfy_extended_nowplaying_pill_style"
                )
            )
            items.append(Divider(text=tr("nowfy_pulse_atv")))
        if self._core_addon_enabled("addon_track_hub_enabled", False):
            items.append(Text(text="Track Hub", icon="msg_openprofile", create_sub_fragment=self.create_track_hub_subfragment, link_alias="nowfy_extended_track_hub"))
        return self._apply_link_aliases(items)

    def create_extended_home_cover_subfragment(self):
        items = [Divider(text=tr("nowfy_extended_home_cover_title"))]
        try:
            header_cover_sub = tr("nowfy_extended_cover_album_sub")
            try:
                show_mode = int(self.get_setting("header_cover_show_mode", 0) or 0)
                has_custom = bool(self._has_custom_cover())
                try:
                    core_sel = None
                    if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "get_core_setting"):
                        core_sel = NOWFY_CORE_API.get_core_setting("custom_cover_selection", None)
                except Exception:
                    core_sel = None
                custom_unlocked = bool(self.get_setting("custom_cover_unlocked", False))
                custom_selected = (int(core_sel) == 1) if (core_sel is not None) else (int(self.get_setting("custom_cover_selection", 0)) == 1)
                force_nowfy = bool(self.get_setting("custom_cover_force_nowfy", False))
                if show_mode == 1:
                    header_cover_sub = tr("nowfy_extended_cover_sub")
                elif has_custom and custom_unlocked and custom_selected and not force_nowfy:
                    header_cover_sub = tr("nowfy_extended_cover_custom_sub")
                elif has_custom and custom_unlocked:
                    header_cover_sub = tr("nowfy_extended_cover_album_with_custom_sub")
            except Exception:
                pass
            cover_switch = Switch(
                key="header_cover_enabled",
                text=tr("nowfy_extended_cover_label"),
                subtext=header_cover_sub,
                default=self.get_setting("header_cover_enabled", True),
                icon="msg_copy_photo_solar",
                on_change=lambda v: (
                    self.set_setting("header_cover_enabled", bool(v)),
                    (self._start_header_cover_worker() if bool(v) else self._stop_header_cover_worker()),
                    self._apply_header_cover_settings_consistency(),
                    self.reload_settings()
                ),
                on_long_click=None
            )
            try:
                cover_switch.no_link_alias = True
            except Exception:
                pass
            items.append(cover_switch)
        except Exception:
            pass
        if bool(self.get_setting("header_cover_enabled", True)):
            items.append(Divider(text=tr("nowfy_home_cover_display_section")))
            items.append(
                Selector(
                    key="header_cover_show_mode",
                    text=tr("nowfy_extended_cover_show_label"),
                    default=int(self.get_setting("header_cover_show_mode", 0)),
                    items=[tr("nowfy_extended_cover_show_on"), tr("nowfy_extended_cover_show_off")],
                    icon="ic_gallery_background_solar",
                    on_change=lambda v: (
                        self.set_setting("header_cover_show_mode", int(v)),
                        self._apply_header_cover_settings_consistency(),
                        self.reload_settings()
                    ),
                    link_alias="nowfy_extended_cover_show_mode"
                )
            )
            items.append(
                Selector(
                    key="header_cover_blur",
                    text=tr("nowfy_extended_cover_blur_label"),
                    default=int(self.get_setting("header_cover_blur", 1)),
                    items=[tr("nowfy_extended_cover_blur_on"), tr("nowfy_extended_cover_blur_off")],
                    icon="msg_blur_radial",
                    on_change=lambda v: (
                        self.set_setting("header_cover_blur", int(v)),
                        self.reload_settings()
                    ),
                    link_alias="nowfy_extended_cover_blur"
                )
            )
            items.append(
                Divider(text=tr("nowfy_home_cover_custom_section"))
            )
            items.append(
                Selector(
                    key="custom_cover_unlocked",
                    text="Custom Cover",
                    default=1 if bool(self.get_setting("custom_cover_unlocked", False)) else 0,
                    items=[tr("nowfy_extended_cover_show_off"), tr("nowfy_extended_cover_show_on")],
                    icon="filled_add_photo",
                    on_change=lambda v: (
                        (NOWFY_CORE_API.on_custom_cover_toggle(self, v) if (NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "on_custom_cover_toggle")) else self._on_custom_cover_toggle(v)),
                        self.reload_settings()
                    )
                )
            )
        if bool(self.get_setting("custom_cover_unlocked", False)):
            items.append(Divider(text=tr("nowfy_home_cover_manage_section")))
            items.append(
                Text(
                    text=tr("nowfy_custom_cover_upload"),
                    icon="gift_upgrade",
                    on_click=lambda v: self._open_custom_cover_upload_from_main(),
                    link_alias="nowfy_extended_custom_cover_upload"
                )
            )
            if self._has_custom_cover():
                try:
                    core_sel = None
                    if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "get_core_setting"):
                        core_sel = NOWFY_CORE_API.get_core_setting("custom_cover_selection", None)
                except Exception:
                    core_sel = None
                try:
                    current_cover_sel = int(core_sel if core_sel is not None else self.get_setting("custom_cover_selection", 0))
                except Exception:
                    current_cover_sel = 0
                if current_cover_sel < 0 or current_cover_sel > 1:
                    current_cover_sel = 0
                user_label = self._get_custom_cover_label()
                items.append(
                    Selector(
                        key="custom_cover_selection",
                        text=tr("nowfy_custom_cover_selector"),
                        default=current_cover_sel,
                        items=["Nowfy", user_label],
                        icon="msg_gallery",
                        on_change=lambda v: (
                            (NOWFY_CORE_API.on_custom_cover_select(self, v) if (NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "on_custom_cover_select")) else self._on_custom_cover_select(v)),
                            self.reload_settings()
                        ),
                        link_alias="nowfy_extended_custom_cover_selection"
                    )
                )
                if current_cover_sel == 1:
                    items.append(
                        Text(
                            text=tr("nowfy_custom_cover_delete"),
                            icon="menu_clear_recent",
                            red=True,
                            on_click=lambda v: self._delete_custom_cover(),
                            link_alias="nowfy_extended_custom_cover_delete"
                        )
                    )
        return self._apply_link_aliases(items)

    def create_extended_tab_subfragment(self):
        items = []
        items.append(Divider(text="Now Tab"))
        tab_enabled = bool(self.get_setting("nowfy_tab_enabled", True))
        items.append(
            Switch(
                key="nowfy_tab_enabled",
                text=tr("nowfy_tab_label"),
                subtext=tr("nowfy_tab_sub"),
                default=tab_enabled,
                icon="msg_media",
                on_change=lambda v: self._toggle_nowfy_tab(bool(v)),
                link_alias="nowfy_tab_enabled"
            )
        )
        if not tab_enabled:
            items.append(
                Switch(
                    key="nowfy_lyrics_autoscroll_enabled",
                    text=tr("nowfy_lyrics_autoscroll_title"),
                    subtext=tr("nowfy_lyrics_autoscroll_sub"),
                    default=bool(self.get_setting("nowfy_lyrics_autoscroll_enabled", False)),
                    icon="msg_speed_normal",
                    on_change=lambda v: self.reload_settings(),
                    link_alias="nowfy_tab_lyrics_autoscroll_enabled"
                )
            )
            if bool(self.get_setting("nowfy_lyrics_autoscroll_enabled", False)):
                items.append(
                    Selector(
                        key="nowfy_lyrics_autoscroll_speed",
                        text=tr("nowfy_lyrics_autoscroll_speed_title"),
                        default=int(self.get_setting("nowfy_lyrics_autoscroll_speed", 0) or 0),
                        items=[tr("color_default"), "2x", "3x"],
                        icon="menu_feature_hourglass",
                        on_change=lambda v: self.set_setting("nowfy_lyrics_autoscroll_speed", int(v)),
                        link_alias="nowfy_tab_lyrics_autoscroll_speed"
                    )
                )
            return self._apply_link_aliases(items)
        if tab_enabled:
            items.append(
                Switch(
                    key="nowfy_tab_available_notify",
                    text=tr("nowfy_tab_available_notify_label"),
                    subtext=tr("nowfy_tab_available_notify_sub"),
                    default=self.get_setting("nowfy_tab_available_notify", True),
                    icon="msg_notifications_solar",
                    on_change=lambda v: self.set_setting("nowfy_tab_available_notify", bool(v)),
                    link_alias="nowfy_tab_available_notify"
                )
            )
            items.append(
                Selector(
                    key="nowfy_tab_priority_mode",
                    text=tr("nowfy_tab_priority_label"),
                    default=int(self._get_nowfy_tab_priority_mode()),
                    items=[tr("nowfy_tab_priority_mode_default"), tr("nowfy_tab_priority_mode_priority"), tr("nowfy_extended_cover_blur_off")],
                    icon="menu_browser_bookmark",
                    on_change=lambda v: (
                        self.set_setting("nowfy_tab_priority_mode", int(v)),
                        self.set_setting("nowfy_tab_priority_enabled", int(v) != 2)
                    ),
                    link_alias="nowfy_tab_priority_enabled"
                )
            )
            items.append(
                Divider()
            )
            tab_sources, tab_labels = self._get_tab_source_options()
            current_idx = int(self.get_setting("nowfy_tab_source", 0))
            if current_idx < 0 or current_idx >= len(tab_labels):
                current_idx = 0
            items.append(
                Selector(
                    key="nowfy_tab_source",
                    text=tr("nowfy_tab_source_label"),
                    default=current_idx,
                    items=tab_labels,
                    icon="msg_newphone",
                    on_change=lambda v: (
                        self.set_setting("nowfy_tab_source", int(v)),
                        self.reload_settings()
                    ),
                    link_alias="nowfy_tab_source"
                )
            )
            try:
                current_style = int(self.get_setting("nowfy_tab_style", 0))
            except Exception:
                current_style = 0
            if current_style < 0:
                current_style = 0
            if current_style > 1:
                current_style = 1
            if current_style == 0:
                items.append(
                    Selector(
                        key="nowfy_songlink_method",
                        text="Link View",
                        default=int(self.get_setting("nowfy_songlink_method", 0)),
                        items=[tr("browser"), "Soon!"],
                        icon="msg_link2_remix",
                        on_change=lambda v: (self.set_setting("nowfy_songlink_method", 0) if int(v) != 0 else self.set_setting("nowfy_songlink_method", 0)),
                        link_alias="nowfy_tab_link_view"
                    )
                )
            items.append(Divider(text=tr("nowfy_tab_config_section")))
            items.append(
                Selector(
                    key="nowfy_tab_style",
                    text=tr("nowfy_tab_style_label"),
                    default=current_style,
                    items=["Apple", "Core"],
                    icon="msg_replace_remix",
                    on_change=lambda v: self.set_setting("nowfy_tab_style", int(v)),
                    link_alias="nowfy_tab_style"
                )
            )
            items.append(
                Switch(
                    key="nowfy_lyrics_autoscroll_enabled",
                    text=tr("nowfy_lyrics_autoscroll_title"),
                    subtext=tr("nowfy_lyrics_autoscroll_sub"),
                    default=bool(self.get_setting("nowfy_lyrics_autoscroll_enabled", False)),
                    icon="msg_speed_normal",
                    on_change=lambda v: self.reload_settings(),
                    link_alias="nowfy_tab_lyrics_autoscroll_enabled"
                )
            )
            if bool(self.get_setting("nowfy_lyrics_autoscroll_enabled", False)):
                items.append(
                    Selector(
                        key="nowfy_lyrics_autoscroll_speed",
                        text=tr("nowfy_lyrics_autoscroll_speed_title"),
                        default=int(self.get_setting("nowfy_lyrics_autoscroll_speed", 0) or 0),
                        items=[tr("color_default"), "2x", "3x"],
                        icon="menu_feature_hourglass",
                        on_change=lambda v: self.set_setting("nowfy_lyrics_autoscroll_speed", int(v)),
                        link_alias="nowfy_tab_lyrics_autoscroll_speed"
                    )
                )
            try:
                current_control_style = int(self.get_setting("nowfy_control_style", 0) or 0)
            except Exception:
                current_control_style = 0
            if current_control_style < 0 or current_control_style > 1:
                current_control_style = 0
            try:
                _active_player = str(self._detect_current_player() or "").strip().lower()
                _control_allowed = (_active_player == "spotify")
            except Exception:
                _control_allowed = False
            if not _control_allowed:
                try:
                    _sources_ctrl, _labels_ctrl = self._get_tab_source_options()
                    _idx_ctrl = int(self.get_setting("nowfy_tab_source", 0) or 0)
                    if isinstance(_sources_ctrl, list) and _sources_ctrl:
                        if _idx_ctrl < 0 or _idx_ctrl >= len(_sources_ctrl):
                            _idx_ctrl = 0
                        _src_ctrl = str(_sources_ctrl[_idx_ctrl] or "").strip().lower()
                        _control_allowed = (_src_ctrl in ("spotify", "statsfm"))
                except Exception:
                    pass
            if current_style == 1 and _control_allowed:
                items.append(
                    Selector(
                        key="nowfy_control_style",
                        text="Nowfy Control",
                        default=current_control_style,
                        items=["Control", "Modern"],
                        icon="msg_replace_remix",
                        on_change=lambda v: self.set_setting("nowfy_control_style", int(v))
                    )
                )
            if current_style == 0:
                items.append(Divider(text=tr("now_tab_buttons_divider")))
                items.append(Divider(text=tr("now_tab_buttons_help_divider")))
                items.append(
                    Selector(
                        key="nowfy_lyrics_button",
                        text=tr("lyrics_button"),
                        default=int(self.get_setting("nowfy_lyrics_button", 1) or 0),
                        items=[tr("nowfy_extended_cover_show_off"), tr("nowfy_extended_cover_show_on")],
                        icon="menu_quote_remix",
                        on_change=lambda v: (
                            self.set_setting("nowfy_lyrics_button", int(v)),
                            self.reload_settings()
                        )
                    )
                )
                items.append(
                    Selector(
                        key="nowfy_embed_button",
                        text=tr("music_link"),
                        default=int(self.get_setting("nowfy_embed_button", 1) or 0),
                        items=[tr("nowfy_extended_cover_show_off"), tr("nowfy_extended_cover_show_on")],
                        icon="msg_link2",
                        on_change=lambda v: (
                            self.set_setting("nowfy_embed_button", int(v)),
                            self.reload_settings()
                        )
                    )
                )
                if _control_allowed:
                    items.append(
                        Switch(
                            key="nowfy_control_enabled",
                            text="Nowfy Control",
                            default=bool(self.get_setting("nowfy_control_enabled", False)),
                            icon="msg_audio",
                            on_change=lambda v: (
                                self.set_setting("nowfy_control_enabled", bool(v)),
                                self.reload_settings()
                            )
                    )
                )
        return self._apply_link_aliases(items)

    def _show_nowtab_initial_tab_sheet(self):
        try:
            frag = get_last_fragment()
            ctx = frag.getParentActivity() if frag and frag.getParentActivity() else ApplicationLoader.applicationContext
            if not ctx:
                return
            sheet = BottomSheet(ctx, True)
            root = LinearLayout(ctx)
            root.setOrientation(LinearLayout.VERTICAL)
            try:
                root.setPadding(AndroidUtilities.dp(18), AndroidUtilities.dp(16), AndroidUtilities.dp(18), AndroidUtilities.dp(14))
            except Exception:
                pass
            title = TextView(ctx)
            title.setText(tr("nowfy_tab_priority_label"))
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 21)
            try:
                title.setTypeface(AndroidUtilities.bold())
            except Exception:
                pass
            try:
                title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                pass
            root.addView(title, LayoutHelper.createLinear(-1, -2))

            current_mode = int(self._get_nowfy_tab_priority_mode())

            def _option_row(label_text, sub_text, selected, on_click):
                wrap = LinearLayout(ctx)
                wrap.setOrientation(LinearLayout.HORIZONTAL)
                wrap.setGravity(Gravity.CENTER_VERTICAL)
                wrap.setClickable(True)
                wrap.setFocusable(True)
                try:
                    wrap.setPadding(AndroidUtilities.dp(6), AndroidUtilities.dp(10), AndroidUtilities.dp(6), AndroidUtilities.dp(10))
                except Exception:
                    pass
                radio = TextView(ctx)
                radio.setText("◉" if bool(selected) else "○")
                radio.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 24)
                try:
                    radio.setTextColor(
                        Theme.getColor(Theme.key_featuredStickers_addButton) if bool(selected)
                        else Theme.getColor(Theme.key_windowBackgroundWhiteGrayText)
                    )
                except Exception:
                    pass
                wrap.addView(radio, LayoutHelper.createLinear(-2, -2, Gravity.TOP, 0, 2, 12, 0))

                text_col = LinearLayout(ctx)
                text_col.setOrientation(LinearLayout.VERTICAL)
                tv = TextView(ctx)
                tv.setText(str(label_text or ""))
                tv.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
                try:
                    tv.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
                except Exception:
                    pass
                text_col.addView(tv, LayoutHelper.createLinear(-1, -2))
                if str(sub_text or "").strip():
                    st = TextView(ctx)
                    st.setText(str(sub_text))
                    st.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
                    try:
                        st.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
                    except Exception:
                        pass
                    text_col.addView(st, LayoutHelper.createLinear(-1, -2, Gravity.START, 0, 2, 0, 0))
                wrap.addView(text_col, LayoutHelper.createLinear(0, -2, 1.0))
                wrap.setOnClickListener(OnClickListener(lambda _v: on_click()))
                root.addView(wrap, LayoutHelper.createLinear(-1, -2))

            def _apply_state(mode):
                try:
                    self.set_setting("nowfy_tab_priority_mode", int(mode))
                    self.set_setting("nowfy_tab_priority_enabled", int(mode) != 2)
                    self.reload_settings()
                except Exception:
                    pass
                try:
                    sheet.dismiss()
                except Exception:
                    pass

            _option_row(
                tr("nowfy_tab_priority_mode_default"),
                tr("nowfy_tab_priority_on_sub"),
                current_mode == 0,
                lambda: _apply_state(0),
            )
            _option_row(
                tr("nowfy_tab_priority_mode_priority"),
                tr("nowfy_tab_priority_on_sub"),
                current_mode == 1,
                lambda: _apply_state(1),
            )
            _option_row(
                tr("nowfy_extended_cover_blur_off"),
                tr("nowfy_tab_priority_off_sub"),
                current_mode == 2,
                lambda: _apply_state(2),
            )

            cancel_btn = TextView(ctx)
            cancel_btn.setText(tr("cancel"))
            cancel_btn.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
            cancel_btn.setGravity(Gravity.CENTER)
            try:
                cancel_btn.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(10), AndroidUtilities.dp(12), AndroidUtilities.dp(10))
            except Exception:
                pass
            cancel_btn.setOnClickListener(OnClickListener(lambda _v: sheet.dismiss()))
            root.addView(cancel_btn, LayoutHelper.createLinear(-1, -2, Gravity.CENTER_HORIZONTAL, 0, 8, 0, 0))
            sheet.setCustomView(root)
            run_on_ui_thread(sheet.show)
        except Exception:
            pass

    def _maybe_show_flow_free_info_sheet(self):
        try:
            disabled = bool(self.get_setting("nowfy_flow_free_sheet_always", False))
            if disabled:
                return
            self._show_flow_free_info_sheet()
        except Exception:
            pass

    def _show_flow_free_info_sheet(self):
        try:
            frag = get_last_fragment()
            ctx = frag.getParentActivity() if frag and frag.getParentActivity() else ApplicationLoader.applicationContext
            if not ctx:
                return
            sheet = BottomSheet(ctx, True)
            root = LinearLayout(ctx)
            root.setOrientation(LinearLayout.VERTICAL)
            try:
                root.setPadding(AndroidUtilities.dp(18), AndroidUtilities.dp(16), AndroidUtilities.dp(18), AndroidUtilities.dp(14))
            except Exception:
                pass
            img = ImageView(ctx)
            try:
                img.setScaleType(ImageView.ScaleType.FIT_CENTER)
                img.setAdjustViewBounds(True)
            except Exception:
                pass
            try:
                bg = GradientDrawable()
                bg.setCornerRadius(float(AndroidUtilities.dp(16)))
                bg.setColor(int(Theme.getColor(Theme.key_windowBackgroundWhite)))
                img.setBackground(bg)
                img.setClipToOutline(True)
            except Exception:
                pass
            try:
                gif_path = File(os.path.join(os.path.dirname(__file__), "assets", "png", "hold_flow.gif")).getAbsolutePath()
                try:
                    from android.graphics import ImageDecoder
                    from android.graphics.drawable import AnimatedImageDrawable
                    src = ImageDecoder.createSource(File(gif_path))
                    drawable = ImageDecoder.decodeDrawable(src)
                    if drawable is not None:
                        img.setImageDrawable(drawable)
                        try:
                            if isinstance(drawable, AnimatedImageDrawable):
                                try:
                                    drawable.setRepeatCount(-1)
                                except Exception:
                                    pass
                                drawable.start()
                        except Exception:
                            pass
                except Exception:
                    hold_path = File(os.path.join(os.path.dirname(__file__), "assets", "png", "hold_flow.png")).getAbsolutePath()
                    bmp = BitmapFactory.decodeFile(hold_path)
                    if bmp is not None:
                        img.setImageBitmap(bmp)
            except Exception:
                pass
            root.addView(img, LayoutHelper.createLinear(-1, AndroidUtilities.dp(104), Gravity.CENTER_HORIZONTAL, 0, 0, 0, 10))

            title = TextView(ctx)
            title.setText(tr("nowfy_flow_free_sheet_title"))
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 20)
            try:
                title.setTypeface(AndroidUtilities.bold())
            except Exception:
                pass
            try:
                title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                pass
            root.addView(title, LayoutHelper.createLinear(-1, -2))

            desc = TextView(ctx)
            desc.setText(tr("nowfy_flow_free_sheet_desc"))
            desc.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 14)
            try:
                desc.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            except Exception:
                pass
            try:
                desc.setPadding(0, AndroidUtilities.dp(6), 0, AndroidUtilities.dp(12))
            except Exception:
                pass
            root.addView(desc, LayoutHelper.createLinear(-1, -2))

            row = LinearLayout(ctx)
            row.setOrientation(LinearLayout.HORIZONTAL)
            row.setGravity(Gravity.CENTER)

            ok_btn = TextView(ctx)
            ok_btn.setText(tr("nowfy_flow_free_sheet_ok"))
            ok_btn.setGravity(Gravity.CENTER)
            ok_btn.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
            try:
                ok_btn.setTextColor(Theme.getColor(Theme.key_featuredStickers_buttonText))
            except Exception:
                pass
            try:
                ok_btn.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(10), AndroidUtilities.dp(12), AndroidUtilities.dp(10))
            except Exception:
                pass
            try:
                ok_bg = GradientDrawable()
                ok_bg.setCornerRadius(float(AndroidUtilities.dp(12)))
                try:
                    ok_bg.setColor(Theme.getColor(Theme.key_featuredStickers_addButton))
                except Exception:
                    ok_bg.setColor(0xFF2D87FF)
                ok_btn.setBackground(ok_bg)
            except Exception:
                pass

            toggle_btn = TextView(ctx)
            toggle_btn.setText(tr("nowfy_flow_free_sheet_toggle"))
            toggle_btn.setGravity(Gravity.CENTER)
            toggle_btn.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
            try:
                toggle_btn.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                pass
            try:
                toggle_btn.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(10), AndroidUtilities.dp(12), AndroidUtilities.dp(10))
            except Exception:
                pass
            try:
                tg_bg = GradientDrawable()
                tg_bg.setCornerRadius(float(AndroidUtilities.dp(12)))
                try:
                    tg_bg.setColor(Theme.getColor(Theme.key_windowBackgroundWhite))
                except Exception:
                    tg_bg.setColor(0xFF202A37)
                try:
                    tg_bg.setStroke(int(AndroidUtilities.dp(1)), int(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText4)))
                except Exception:
                    pass
                toggle_btn.setBackground(tg_bg)
            except Exception:
                pass

            def _close_sheet():
                try:
                    sheet.dismiss()
                except Exception:
                    pass

            def _toggle_always():
                try:
                    self.set_setting("nowfy_flow_free_sheet_always", True)
                except Exception:
                    pass
                try:
                    sheet.dismiss()
                except Exception:
                    pass

            ok_btn.setOnClickListener(OnClickListener(lambda _v: _close_sheet()))
            toggle_btn.setOnClickListener(OnClickListener(lambda _v: _toggle_always()))
            row.addView(ok_btn, LayoutHelper.createLinear(0, -2, 1.0, Gravity.CENTER, 0, 0, 6, 0))
            row.addView(toggle_btn, LayoutHelper.createLinear(0, -2, 1.0, Gravity.CENTER, 6, 0, 0, 0))
            root.addView(row, LayoutHelper.createLinear(-1, -2))

            sheet.setCustomView(root)
            run_on_ui_thread(sheet.show)
        except Exception:
            pass

    def create_extended_flow_subfragment(self):
        items = []
        items.append(
            Switch(
                key="nowfy_flow_enabled",
                text="Nowfy Flow",
                default=bool(self.get_setting("nowfy_flow_enabled", False)),
                icon="filled_fab_compose_32",
                on_change=lambda v: (
                    self.set_setting("nowfy_flow_enabled", bool(v)),
                    self.set_setting("fab_chat_enabled", bool(v)),
                    self.set_setting("nowfy_flow_side", 0) if bool(v) else None,
                    self.set_setting("nowfy_flow_transparency", 0) if bool(v) else None,
                    self.set_setting("nowfy_flow_free_sheet_always", False),
                    self.set_setting("nowfy_flow_free_sheet_seen", False),
                    self._apply_chat_fab_state(),
                    self.reload_settings()
                ),
                link_alias="nowfy_flow_enabled"
            )
        )
        if bool(self.get_setting("nowfy_flow_enabled", False)):
            items.append(Divider(text=tr("nowfy_flow_side_title")))
            flow_side = self._get_nowfy_flow_side()
            items.append(
                Selector(
                    key="nowfy_flow_side",
                    text=tr("nowfy_flow_side_label"),
                    default=flow_side,
                    items=[tr("nowfy_flow_side_left"), tr("nowfy_flow_side_right"), tr("nowfy_flow_side_free")],
                    icon="msg_replace_remix",
                    on_change=lambda v: (
                        self._reset_nowfy_flow_free_position() if int(v) == 2 else None,
                        self._maybe_show_flow_free_info_sheet() if int(v) == 2 else None,
                        self._update_chat_fab_position_once(),
                        self._apply_chat_fab_state()
                    ),
                    link_alias="nowfy_flow_side"
                )
            )
            flow_alpha = self._get_nowfy_flow_transparency_mode()
            items.append(
                Selector(
                    key="nowfy_flow_transparency",
                    text=tr("nowfy_flow_alpha_label"),
                    default=flow_alpha,
                    items=[tr("nowfy_flow_alpha_default"), "50%", "70%"],
                    icon="msg_replace_remix",
                    on_change=lambda v: None,
                    link_alias="nowfy_flow_transparency"
                )
            )
            flow_style_default = 0
            try:
                flow_style_default = 1 if str(self.get_setting("nowfy_flow_card_mode", "cc") or "cc").strip().lower() == "cc" else 0
            except Exception:
                flow_style_default = 0
            items.append(Divider(text="Flow Styles"))
            items.append(
                Selector(
                    key="nowfy_flow_card_mode",
                    text="Flow Styles",
                    default=flow_style_default,
                    items=[tr("nowfy_flow_alpha_default"), tr("nowfy_flow_style_compact")],
                    icon="msg_replace_remix",
                    on_change=lambda v: (
                        self.set_setting("nowfy_flow_card_mode", "cc" if int(v) == 1 else "default"),
                        self.reload_settings()
                    ),
                    link_alias="nowfy_flow_card_mode"
                )
            )
            flow_bg_default = 0
            try:
                flow_bg_default = 1 if bool(self.get_setting("nowfy_flow_bt_debug", True)) else 0
            except Exception:
                flow_bg_default = 0
            items.append(
                Selector(
                    key="nowfy_flow_bt_debug",
                    text="Flow BG",
                    default=flow_bg_default,
                    items=[tr("nowfy_flow_alpha_default"), tr("nowfy_flow_bg_floating")],
                    icon="msg_replace_remix",
                    on_change=lambda v: (
                        self.set_setting("nowfy_flow_bt_debug", bool(int(v) == 1)),
                        self.reload_settings()
                    ),
                    link_alias="nowfy_flow_bt_debug"
                )
            )
        items.append(Divider(text=tr("nowfy_flow_section_title")))
        return self._apply_link_aliases(items)

    def create_track_hub_subfragment(self):
        try:
            if not self._core_addon_enabled("addon_track_hub_enabled", False):
                return self._apply_link_aliases([
                    Divider(text="Track Hub is disabled in NowfyCore Addons.")
                ])
        except Exception:
            pass
        items = []
        try:
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "build_track_hub_subfragment_items"):
                items = NOWFY_CORE_API.build_track_hub_subfragment_items(self) or []
        except Exception:
            items = []
        return self._apply_link_aliases(items)

    def _is_optional_theme_enabled_by_core(self, theme_key, default_value=False):
        try:
            mapping = {
                "core_theme_spotlight_enabled": "spotlight",
                "core_theme_nowv_enabled": "nowv",
            }
            mk = mapping.get(str(theme_key or "").strip(), "")
            if mk:
                return mk in set(self._get_core_enabled_optional_themes())
            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "is_theme_enabled"):
                return bool(NOWFY_CORE_API.is_theme_enabled(self, theme_key, default_value))
            return bool(self.get_setting(theme_key, bool(default_value)))
        except Exception:
            return bool(default_value)

    def _theme_real_index_to_key(self, real_idx, external_themes=None):
        try:
            ext = external_themes if isinstance(external_themes, dict) else (self._get_external_themes() or {})
            ext_count = len(ext)
            spotlight_index = ext_count + 1
            vinify_index = spotlight_index + 1
            nowv_index = vinify_index + 1
            i = int(real_idx or 0)
            if i == 0:
                return "apple"
            if 1 <= i <= ext_count:
                try:
                    ext_keys = list(ext.keys())
                    return f"ext:{ext_keys[i - 1]}"
                except Exception:
                    return "apple"
            if i == spotlight_index:
                return "spotlight"
            if i == vinify_index:
                return "vinify"
            if i == nowv_index:
                return "nowv"
            return "apple"
        except Exception:
            return "apple"

    def _theme_key_to_real_index(self, theme_key, external_themes=None):
        try:
            ext = external_themes if isinstance(external_themes, dict) else (self._get_external_themes() or {})
            ext_count = len(ext)
            spotlight_index = ext_count + 1
            vinify_index = spotlight_index + 1
            nowv_index = vinify_index + 1
            k = str(theme_key or "").strip().lower()
            if not k:
                return 0
            if k == "apple":
                return 0
            if k.startswith("ext:"):
                want = k[4:]
                ext_keys = list(ext.keys())
                if want in ext_keys:
                    return ext_keys.index(want) + 1
                return 0
            if k == "spotlight":
                return spotlight_index
            if k == "vinify":
                return vinify_index
            if k == "nowv":
                return nowv_index
            return 0
        except Exception:
            return 0

    def _sanitize_theme_selector_by_core(self):
        try:
            external_themes = self._get_external_themes()
            spotlight_index = len(external_themes) + 1
            vinify_index = spotlight_index + 1
            nowv_index = vinify_index + 1
            current_theme = int(self.get_setting("theme_selector", 0) or 0)
            try:
                saved_key = str(self.get_setting("theme_selector_key", "") or "").strip()
            except Exception:
                saved_key = ""
            if saved_key:
                remapped = int(self._theme_key_to_real_index(saved_key, external_themes) or 0)
                if remapped != current_theme:
                    current_theme = remapped
                    try:
                        self.set_setting("theme_selector", current_theme)
                    except Exception:
                        pass
            else:
                try:
                    self.set_setting("theme_selector_key", self._theme_real_index_to_key(current_theme, external_themes))
                except Exception:
                    pass
            if current_theme == spotlight_index and not self._is_optional_theme_enabled_by_core("core_theme_spotlight_enabled", False):
                self.set_setting("theme_selector", 0)
                self.set_setting("theme_selector_key", "apple")
                return 0
            if current_theme == nowv_index and not self._is_optional_theme_enabled_by_core("core_theme_nowv_enabled", False):
                self.set_setting("theme_selector", 0)
                self.set_setting("theme_selector_key", "apple")
                return 0
            if current_theme > nowv_index:
                self.set_setting("theme_selector", 0)
                self.set_setting("theme_selector_key", "apple")
                return 0
            if str(saved_key).lower() in ("fmcard", "legacy_b"):
                self.set_setting("theme_selector", 0)
                self.set_setting("theme_selector_key", "apple")
                return 0
            return current_theme
        except Exception:
            return int(self.get_setting("theme_selector", 0) or 0)

    def _invoke_core_font_action(self, action_name):
        try:
            try:
                self._trace_font_bridge(f"tap action={action_name}")
                def _bridge_msg():
                    key_map = {
                        "_open_font_upload": "core_opening_font_upload",
                        "_open_backup_upload": "core_opening_backup_upload",
                        "_open_custom_cover_upload": "core_opening_custom_cover_upload",
                    }
                    k = key_map.get(str(action_name or "").strip(), "")
                    if k:
                        txt = tr(k)
                        if txt and txt != k:
                            BulletinHelper.show_info(txt)
                run_on_ui_thread(_bridge_msg)
            except Exception:
                pass
            try:
                self._bind_core_backend_methods_if_needed()
            except Exception:
                pass
            try:
                if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "invoke_core_action"):
                    if bool(NOWFY_CORE_API.invoke_core_action(action_name)):
                        self._trace_font_bridge(f"calling core_api.{action_name}()")
                        return True
                    else:
                        self._trace_font_bridge(f"core_api.{action_name}() unavailable")
            except Exception as e:
                try:
                    self._trace_font_bridge(f"core_api invoke error ({action_name}): {e}")
                except Exception:
                    pass
            try:
                core_inst = getattr(getattr(nowfycore, "NowfyCore", None), "instance", None)
            except Exception:
                core_inst = None
            if core_inst is not None:
                core_fn = getattr(core_inst, action_name, None)
                if callable(core_fn):
                    try:
                        self._trace_font_bridge(f"calling core.{action_name}()")
                    except Exception:
                        pass
                    core_fn()
                    return True
            fn = getattr(self, action_name, None)
            if callable(fn):
                try:
                    self._trace_font_bridge(f"calling self.{action_name}()")
                except Exception:
                    pass
                fn()
                return True
            try:
                self._trace_font_bridge("core font module unavailable")
                run_on_ui_thread(lambda: BulletinHelper.show_info(
                    tr("core_action_unavailable")
                    if tr("core_action_unavailable") != "core_action_unavailable"
                    else "Action unavailable in NowfyCore."
                ))
            except Exception:
                pass
            return False
        except Exception as e:
            try:
                self._trace_font_bridge(f"bridge error ({action_name}): {e}")
            except Exception:
                pass
            try:
                run_on_ui_thread(lambda: BulletinHelper.show_info(
                    tr("core_action_error").format(error=str(e))
                    if tr("core_action_error") != "core_action_error"
                    else f"Core action failed: {str(e)}"
                ))
            except Exception:
                pass
            return False

    def _trace_font_bridge(self, message):
        try:
            msg = f"[Nowfy][FontsBridge] {message}"
            try:
                log(msg)
            except Exception:
                pass
            try:
                paths = [
                    "/storage/emulated/0/Android/media/com.exteragram.messenger/nowfy_fonts_bridge.log",
                    "/storage/emulated/0/Android/media/com.radolyn.ayugram/nowfy_fonts_bridge.log",
                ]
                for path in paths:
                    try:
                        d = os.path.dirname(path)
                        if d and not os.path.exists(d):
                            os.makedirs(d)
                        with open(path, "a", encoding="utf-8") as fp:
                            fp.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
                    except Exception:
                        pass
            except Exception:
                pass
        except Exception:
            pass

    def _open_font_upload_from_main(self):
        return self._invoke_core_font_action("_open_font_upload")

    def _open_font_manager_from_main(self):
        return self._invoke_core_font_action("_open_font_manager")

    def _open_backup_upload_from_main(self):
        return self._invoke_core_font_action("_open_backup_upload")

    def _open_custom_cover_upload_from_main(self):
        return self._invoke_core_font_action("_open_custom_cover_upload")

    def create_themes_subfragment(self):
        current_theme_real = self._sanitize_theme_selector_by_core()
        external_themes = self._get_external_themes()
        full_theme_items = ["Apple"]
        if external_themes:
            for theme_id, theme_data in external_themes.items():
                full_theme_items.append(theme_data['name'])
        full_theme_items.append("Spotlight")
        full_theme_items.append("Vinify")
        full_theme_items.append("Nowv")
        ext_count = len(external_themes)
        spotlight_index = ext_count + 1
        vinify_index = spotlight_index + 1
        nowv_index = vinify_index + 1
        visible_theme_items = []
        visible_real_indices = []
        visible_theme_items.append("Apple")
        visible_real_indices.append(0)
        if external_themes:
            ext_i = 1
            for theme_id, theme_data in external_themes.items():
                visible_theme_items.append(theme_data['name'])
                visible_real_indices.append(ext_i)
                ext_i += 1
        if self._is_optional_theme_enabled_by_core("core_theme_spotlight_enabled", False):
            visible_theme_items.append("Spotlight")
            visible_real_indices.append(spotlight_index)
        visible_theme_items.append("Vinify")
        visible_real_indices.append(vinify_index)
        if self._is_optional_theme_enabled_by_core("core_theme_nowv_enabled", False):
            visible_theme_items.append("Nowv")
            visible_real_indices.append(nowv_index)
        if current_theme_real not in visible_real_indices:
            current_theme_real = 0
            try:
                self.set_setting("theme_selector", 0)
                self.set_setting("theme_selector_key", "apple")
            except Exception:
                pass
        try:
            current_theme_view_idx = visible_real_indices.index(current_theme_real)
        except Exception:
            current_theme_view_idx = 0
        items = []
        items.extend([
            Divider(text=tr("theme_selection_section")),
            Selector(
                key="theme_selector_view",
                text=tr("theme_selector"),
                default=current_theme_view_idx,
                items=visible_theme_items,
                icon="msg_theme",
                on_change=lambda v: (
                    self.set_setting("theme_selector", int(visible_real_indices[max(0, min(len(visible_real_indices) - 1, int(v)))])),
                    self.set_setting("theme_selector_key", self._theme_real_index_to_key(int(visible_real_indices[max(0, min(len(visible_real_indices) - 1, int(v)))]), external_themes)),
                    self.reload_settings()
                ),
                link_alias="nowfy_themes_selector"
            )
        ])
        current_theme = int(current_theme_real or 0)
        if str(self.get_setting("theme_selector_key", "") or "").strip().lower() in ("fmcard", "legacy_b"):
            current_theme = 0
            try:
                self.set_setting("theme_selector", 0)
                self.set_setting("theme_selector_key", "apple")
            except Exception:
                pass
        if current_theme == 0:
            pass
            items.append(
                Switch(
                    key="show_extera_bar",
                    text="exteraBar",
                    subtext=tr("extera_bar_sub"),
                    default=True,
                    icon="msg_noise_on",
                    on_change=lambda v: self.reload_settings(),
                    link_alias="nowfy_themes_exterabar"
                )
            )
        if current_theme == spotlight_index:
            pass
        items.extend(self._get_dynamic_ui_options(full_theme_items))
        if True:
            try:
                migrated = bool(self.get_setting("font_selector_random_migrated", False))
                if not migrated:
                    old_val = int(self.get_setting("font_selector", 0) or 0)
                    self.set_setting("font_selector", max(0, old_val) + 1)
                    self.set_setting("font_selector_random_migrated", True)
            except Exception:
                pass
            custom_fonts = self._list_custom_fonts()
            custom_font_labels = self._list_custom_fonts_display()
            font_items = [
                tr("dynamic_skins_random"),
                "SourceSansPro",
                "exteraCJK",
                "NotoNaskhArabic"
            ]
            if custom_fonts:
                font_items += custom_font_labels
            items.append(
                Selector(
                    key="font_selector",
                    text=tr("font_selector_label"),
                    default=1,
                    items=font_items,
                    icon="msg_photo_text_framed3",
                    link_alias="nowfy_themes_font_selector"
                )
            )
            items.append(
                Selector(
                    key="font_apply_scope",
                    text=tr("font_apply_scope_label"),
                    default=2,
                    items=[tr("font_apply_scope_music"), tr("font_apply_scope_artist"), tr("font_apply_scope_both")],
                    icon="msg_select_between_solar",
                    link_alias="nowfy_themes_font_apply_scope"
                )
            )
            items.append(
                Text(
                    text=tr("nowfy_font_upload_label"),
                    icon="gift_upgrade",
                    on_click=lambda v: self._open_font_upload_from_main(),
                    link_alias="nowfy_themes_font_upload"
                )
            )
            items.append(
                Text(
                    text=tr("nowfy_font_manage_label"),
                    icon="msg_list",
                    on_click=lambda v: self._open_font_manager_from_main(),
                    link_alias="nowfy_themes_font_manage"
                )
            )
        items.extend([Divider(text=tr("extra_section"))])
        items.append(
            Switch(
                key="random_theme_mode",
                text=tr("random_theme_mode"),
                subtext=tr("random_theme_mode_sub"),
                default=False,
                icon="menu_random",
                link_alias="nowfy_themes_random_mode"
            )
        )
        items.append(
            Switch(
                key="show_caption",
                text=tr("show_caption"),
                default=True,
                icon="msg_chats_add_solar",
                on_change=lambda v: self.reload_settings(),
                link_alias="nowfy_themes_show_caption"
            )
        )
        if self.get_setting("show_caption", True):
            caption_style_items = ["Custom", "Apple Based", "Pepe", "Minim", "Spoty"]
            items.append(
                Selector(
                    key="caption_style",
                    text=tr("caption_style"),
                    default=0,
                    items=caption_style_items,
                    icon="msg_photo_text_framed3",
                    on_change=lambda v: self.reload_settings(),
                    link_alias="nowfy_themes_caption_style"
                )
            )
            if self.get_setting("caption_style", 0) == 0:
                items.append(
                    Input(
                        key="custom_footer_text",
                        text=tr("custom_caption"),
                        default="",
                        icon="menu_tag_edit_solar",
                        link_alias="nowfy_themes_custom_caption"
                    )
                )
        items.extend([
            Divider(text=tr("customization_section")),
            Text(
                text=tr("link_options_header"),
                icon="msg_link2_remix",
                create_sub_fragment=self.create_link_options_subfragment,
                link_alias="nowfy_themes_link_options"
            ),
            Divider(),
        ])
        return self._apply_link_aliases(items)

    def create_settings(self):
        show_credentials = self.get_setting("show_credentials", False)
        show_cache_settings = self.get_setting("show_cache_settings", False)
        custom_fonts = self._list_custom_fonts()
        custom_font_labels = self._list_custom_fonts_display()
        font_selector = self.get_setting("font_selector", 0)
        font_items = [
            "SourceSansPro",
            "exteraCJK",
            "NotoNaskhArabic"
        ]
        if custom_fonts:
            font_items += custom_font_labels
        settings = []
        settings.append(Text(text=tr("services_section_title"), icon="msg_tone_on", create_sub_fragment=self.create_services_subfragment, link_alias="nowfy_home_services"))
        settings.append(Divider())
        settings.append(Text(text=tr("nowfy_panel_section_title"), icon="msg_photo_settings_remix", create_sub_fragment=self.create_nowfy_panel_subfragment, link_alias="nowfy_home_panel"))
        settings.append(Text(text="Nowfy Lab", icon="msg_trending_solar", create_sub_fragment=self.create_nowfy_lab_subfragment, link_alias="nowfy_home_lab"))
        settings.append(Text(text=tr("nowfy_extended_section_title"), icon="media_photo_flash_on2_remix", create_sub_fragment=self.create_extended_subfragment, link_alias="nowfy_home_extended"))
        settings.append(Text(text=tr("themes_section_title"), icon="msg_payment_card_solar", create_sub_fragment=self.create_themes_subfragment, link_alias="nowfy_home_themes"))
        settings.append(Divider())
        current_theme = self.get_setting("theme_selector", 0)
        settings.append(Divider())
        settings.append(Text(
            text="Dotted Plugins",
            icon="etg_settings",
            accent=True,
            on_click=lambda view: run_on_ui_thread(lambda: get_messages_controller().openByUserName("exteraDevPlugins", get_last_fragment(), 1)),
            link_alias="nowfy_credit_dotted"
        ))
        settings.append(Text(
            text="Nowfy",
            icon="msg_reactions",
            accent=True,
            create_sub_fragment=self.create_about_plugin_subfragment,
            link_alias="nowfy_about_subfragment"
        ))
        return self._apply_link_aliases(settings)

    def create_lastfm_credentials_secure(self):
        items = [
            Input(
                key="lastfm_user",
                text="Username",
                icon="menu_username_change",
                default=self.get_setting("lastfm_user", ""),
                subtext=tr("lastfm_user_subtext")
            ),
            Input(
                key="lastfm_api_key",
                text="Last.FM API Key",
                icon="filled_access_fingerprint",
                default=self.get_setting("lastfm_api_key", ""),
                subtext=tr("lastfm_api_key_subtext")
            ),
            Input(
                key="statsfm_username",
                text="Stats.fm Username",
                icon="menu_username_change",
                default=self.get_setting("statsfm_username", ""),
                subtext="Seu username do stats.fm"
            ),
            Text(
                text=tr("lastfm_title"),
                icon="msg2_help",
                accent=True,
                on_click=lambda view: self._show_lastfm_api_dialog()
            ),
        ]
        return self._apply_link_aliases(items)

    def create_about_plugin_subfragment(self):
        items = []
        try:
            has_rich = bool(NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "inject_about_support_rich_header"))
        except Exception:
            has_rich = False
        if not has_rich:
            items.append(Divider(text=tr("about_plugin_description")))
        items += [
            Text(
                text=tr("about_plugin_donate"),
                icon="msg_reactions",
                accent=True,
                on_click=lambda view: self._open_url("https://livepix.gg/makios")
            ),
            Text(
                text=tr("about_plugin_donate_kofi"),
                icon="msg_reactions",
                accent=True,
                on_click=lambda view: self._open_url("https://ko-fi.com/ageekapple")
            ),
            Text(
                text="TON",
                icon="msg_copy",
                accent=True,
                on_click=lambda view: run_on_ui_thread(lambda: self._copy_to_clipboard("TON", "UQCy_iox46geMTCNxxZ0G8W0_gg0NXQXz4_A2ho8UtciXvW1"))
            ),
            Text(
                text="TON Telegram",
                icon="msg_copy",
                accent=True,
                on_click=lambda view: run_on_ui_thread(lambda: self._copy_to_clipboard("TON Telegram", "UQAnV3cohn83QODugckxVP-f9jfjwsBgp6MR_RS4hLDWy1rT"))
            ),
            Text(
                text="BTC",
                icon="msg_copy",
                accent=True,
                on_click=lambda view: run_on_ui_thread(lambda: self._copy_to_clipboard("BTC", "bc1qkyq4zqy07agmspnuve6gtjlt40ew278l94ljry8fulykec7vhfuqnuh7he"))
            ),
            Text(
                text="Ethereum (ERC20)",
                icon="msg_copy",
                accent=True,
                on_click=lambda view: run_on_ui_thread(lambda: self._copy_to_clipboard("Ethereum", "0xd41a8f8aed90108380688a46b97ad0a15a91598b"))
            )
        ]
        return self._apply_link_aliases(items)

    def _open_lastfm_settings(self):
        try:
            fragment = get_last_fragment()
            if fragment:
                from ui.alert import AlertDialogBuilder
                ctx = fragment.getParentActivity() if fragment and fragment.getParentActivity() else ApplicationLoader.applicationContext
                builder = AlertDialogBuilder(ctx)
                builder.set_title("LastFM Settings")
                builder.set_message("Aqui será a interface de configurações do LastFM.")
                builder.set_positive_button("OK", lambda b, w: b.dismiss())
                run_on_ui_thread(builder.show)
        except Exception as e:
            log(f"[Nowfy] Erro ao abrir LastFM Settings: {e}")

    def _show_dynamic_island_preview_dialog(self):
        return None

    def _di_icon_catalog(self):
        try:
            return {
                "classic": {
                    "back": {
                        "primary": "https://assets.nowfy/back.png",
                    },
                    "play": {
                        "primary": "https://assets.nowfy/play.png",
                    },
                    "pause": {
                        "primary": "https://assets.nowfy/pause.png",
                    },
                    "next": {
                        "primary": "https://assets.nowfy/next.png",
                    },
                    "send": {
                        "primary": "https://assets.nowfy/send.png",
                    },
                    "search": {
                        "primary": "https://assets.nowfy/search.png",
                    },
                },
                "modern": {
                    "back": {
                        "primary": "https://assets.nowfy/back-modern.png",
                    },
                    "play": {
                        "primary": "https://assets.nowfy/play-modern.png",
                    },
                    "pause": {
                        "primary": "https://assets.nowfy/pause-modern.png",
                    },
                    "next": {
                        "primary": "https://assets.nowfy/next-modern.png",
                    },
                    "send": {
                        "primary": "https://assets.nowfy/send-modern.png",
                    },
                    "search": {
                        "primary": "https://assets.nowfy/search-modern.png",
                    },
                },
                "gradient": {
                    "back": {
                        "primary": "https://assets.nowfy/back-gradient.png"
                    },
                    "play": {
                        "primary": "https://assets.nowfy/play-gradient.png"
                    },
                    "pause": {
                        "primary": "https://assets.nowfy/pause-gradient.png"
                    },
                    "next": {
                        "primary": "https://assets.nowfy/next-gradient.png"
                    },
                    "send": {
                        "primary": "https://assets.nowfy/send-gradient.png"
                    },
                    "search": {
                        "primary": "https://assets.nowfy/search-gradient.png",
                    },
                },
                "silver": {
                    "back": {
                        "primary": "https://assets.nowfy/back-silver.png"
                    },
                    "play": {
                        "primary": "https://assets.nowfy/play-silver.png"
                    },
                    "pause": {
                        "primary": "https://assets.nowfy/pause-silver.png"
                    },
                    "next": {
                        "primary": "https://assets.nowfy/next-silver.png"
                    },
                    "send": {
                        "primary": "https://assets.nowfy/send-silver.png"
                    },
                    "search": {
                        "primary": "https://assets.nowfy/search-silver.png",
                    },
                },
            }
        except Exception:
            return {"classic": {}, "modern": {}, "gradient": {}}

    def _di_icon_sources(self):
        try:
            style_idx = 0
            try:
                style_idx = int(self.get_setting("control_style_selector", 0))
            except Exception:
                style_idx = 0
            catalog = self._di_icon_catalog()
            if style_idx == 3:
                return catalog.get("silver", {})
            if style_idx == 2:
                return catalog.get("gradient", {})
            return catalog.get("modern", {}) if style_idx == 1 else catalog.get("classic", {})
        except Exception:
            return {}

    def _di_cache_dir(self):
        try:
            import os
            from org.telegram.messenger import ApplicationLoader as _AL
            ext_base = "/storage/emulated/0/Android/media/com.exteragram.messenger"
            ayu_base = "/storage/emulated/0/Android/media/com.radolyn.ayugram"
            pkg = ""
            try:
                pkg = str(_AL.applicationContext.getPackageName() or "").lower()
            except Exception:
                pkg = ""
            base = None
            if "ayugram" in pkg:
                if os.path.isdir(ayu_base):
                    base = ayu_base
                elif os.path.isdir(ext_base):
                    base = ext_base
            elif "exteragram" in pkg:
                if os.path.isdir(ext_base):
                    base = ext_base
                elif os.path.isdir(ayu_base):
                    base = ayu_base
            else:
                if os.path.isdir(ext_base):
                    base = ext_base
                elif os.path.isdir(ayu_base):
                    base = ayu_base
            if not base:
                base = _AL.getFilesDir().getAbsolutePath()
            p = os.path.join(base, "nowfy_icons")
            os.makedirs(p, exist_ok=True)
            return p
        except Exception:
            return None

    def _download_pop_island_resources(self):
        return None

    def _show_quick_renew_dialog(self):
        try:
            from ui.alert import AlertDialogBuilder
            frag = get_last_fragment()
            ctx = frag.getParentActivity() if frag and frag.getParentActivity() else None
            builder = AlertDialogBuilder(ctx if ctx else ApplicationLoader.applicationContext)
            builder.set_title(tr("spotify_quick_renew_dialog_title"))
            builder.set_message(
                tr("spotify_quick_renew_dialog_desc")
            )
            builder.set_positive_button(
                tr("spotify_quick_renew_yes"),
                lambda d, w: self._confirm_quick_renew(d)
            )
            builder.set_negative_button(
                tr("cancel"),
                lambda d, w: d.dismiss() if d else None
            )
            run_on_ui_thread(builder.show)
        except Exception:
            try:
                self._confirm_quick_renew(None)
            except Exception:
                pass

    def _refresh_spotify_settings_ui(self):
        try:
            activity = getattr(self, "_spotify_settings_activity", None)
            if activity:
                try:
                    list_view = get_private_field(activity, "listView")
                    adapter = getattr(list_view, "adapter", None) if list_view else None
                    if adapter:
                        try:
                            run_on_ui_thread(lambda: adapter.update(False))
                        except Exception:
                            pass
                        run_on_ui_thread(lambda: adapter.update(True))
                        try:
                            self.reload_settings()
                        except Exception:
                            pass
                        try:
                            frag = get_last_fragment()
                            if frag:
                                try:
                                    run_on_ui_thread(lambda: frag.rebuildSettings())
                                except Exception:
                                    run_on_ui_thread(lambda: frag.rebuildAllFragments(True))
                        except Exception:
                            pass
                        return
                except Exception:
                    pass
            fragment = get_last_fragment()
            if fragment:
                try:
                    lv = getattr(fragment, "listView", None)
                    ad = getattr(lv, "adapter", None) if lv else None
                    if ad:
                        try:
                            run_on_ui_thread(lambda: ad.update(False))
                        except Exception:
                            pass
                        run_on_ui_thread(lambda: ad.update(True))
                        try:
                            self.reload_settings()
                        except Exception:
                            pass
                        try:
                            run_on_ui_thread(lambda: fragment.rebuildSettings())
                        except Exception:
                            try:
                                run_on_ui_thread(lambda: fragment.rebuildAllFragments(True))
                            except Exception:
                                pass
                        return
                except Exception:
                    pass
            self.reload_settings()
        except Exception:
            try:
                self.reload_settings()
            except Exception:
                pass

    def _inject_spotify_connect_custom(self, activity, items):
        try:
            from org.telegram.ui.Components import UItem
            from android.widget import LinearLayout, TextView, ImageView
            from android.view import Gravity
            from android.util import TypedValue
            from android.graphics.drawable import GradientDrawable
            from android_utils import OnClickListener
            st = self._get_quick_spotify_state()
            connected_ready = bool(st.get("connected", False)) and not bool(st.get("force_renew", False)) and not bool(st.get("expired", True))
            menu_open = bool(self.get_setting("spotify_profile_menu_open", False))
            insert_idx = None
            fallback_idx = None
            remove_indices = []
            for i in range(items.size()):
                try:
                    it = items.get(i)
                    marker = str(getattr(it, "object2", "") or "")
                    if marker in ("__spotify_quick_rich_header__", "__spotify_profile_custom__", "__spotify_connect_action__"):
                        remove_indices.append(i)
                        continue
                    key = self._get_uitem_setting_key(it)
                    if key == "quick_oauth_code":
                        if insert_idx is None:
                            insert_idx = i
                    elif key == "custom_command":
                        if fallback_idx is None:
                            fallback_idx = max(0, i - 1)
                except Exception:
                    pass
            if insert_idx is None:
                insert_idx = fallback_idx if fallback_idx is not None else items.size()
            for idx in reversed(remove_indices):
                try:
                    items.remove(idx)
                except Exception:
                    pass
            ctx = activity.getContext()
            wrap = LinearLayout(ctx)
            wrap.setOrientation(LinearLayout.HORIZONTAL)
            wrap.setGravity(Gravity.CENTER_VERTICAL)
            try:
                wrap.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(12))
            except Exception:
                pass
            try:
                bg = GradientDrawable()
                bg.setCornerRadius(AndroidUtilities.dp(14))
                bg.setColor(0x1A2A3A52)
                bg.setStroke(AndroidUtilities.dp(1), 0x556FA8DC)
                wrap.setBackground(bg)
            except Exception:
                pass
            avatar_url = "https://assets.nowfy/connected.png" if connected_ready else ""
            if avatar_url:
                avatar = ImageView(ctx)
                try:
                    avatar.setScaleType(ImageView.ScaleType.CENTER_CROP)
                except Exception:
                    pass
                try:
                    ph = GradientDrawable()
                    ph.setCornerRadius(AndroidUtilities.dp(20))
                    ph.setColor(0x223D4F6B)
                    avatar.setBackground(ph)
                    try:
                        avatar.setClipToOutline(True)
                    except Exception:
                        pass
                except Exception:
                    pass
                wrap.addView(avatar, LinearLayout.LayoutParams(AndroidUtilities.dp(40), AndroidUtilities.dp(40)))
                try:
                    if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "animate_opening_avatar"):
                        NOWFY_CORE_API.animate_opening_avatar(self, avatar, 20, 620)
                except Exception:
                    pass
                def _load_avatar():
                    try:
                        data = self._get_cached_image_enhanced(avatar_url, cache_key=f"spotify_profile_{hash(avatar_url)}")
                        if data:
                            bmp = BitmapFactory.decodeByteArray(data, 0, len(data))
                            if bmp:
                                run_on_ui_thread(lambda b=bmp: avatar.setImageBitmap(b))
                    except Exception:
                        pass
                run_on_queue(_load_avatar)
            text_wrap = LinearLayout(ctx)
            text_wrap.setOrientation(LinearLayout.VERTICAL)
            text_wrap.setGravity(Gravity.CENTER_VERTICAL)
            try:
                lp = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1.0)
                lp.leftMargin = AndroidUtilities.dp(10) if avatar_url else 0
                wrap.addView(text_wrap, lp)
            except Exception:
                wrap.addView(text_wrap)
            title = TextView(ctx)
            title.setText((tr("spotify_quick_connected")) if connected_ready else (tr("spotify_quick_connect")))
            title.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 15)
            try:
                title.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
            except Exception:
                title.setTextColor(0xFFFFFFFF)
            text_wrap.addView(title)
            sub = TextView(ctx)
            sub.setText(
                (tr("spotify_quick_status_connected"))
                if connected_ready
                else (tr("spotify_quick_code_sub"))
            )
            sub.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
            try:
                sub.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
            except Exception:
                sub.setTextColor(0xFFD2DCEB)
            text_wrap.addView(sub)
            if connected_ready:
                arrow = ImageView(ctx)
                try:
                    arrow.setScaleType(ImageView.ScaleType.CENTER_CROP)
                except Exception:
                    pass
                try:
                    ap = GradientDrawable()
                    ap.setCornerRadius(AndroidUtilities.dp(10))
                    ap.setColor(0x2A3D4F6B)
                    arrow.setBackground(ap)
                    try:
                        arrow.setClipToOutline(True)
                    except Exception:
                        pass
                except Exception:
                    pass
                try:
                    wrap.addView(arrow, LinearLayout.LayoutParams(AndroidUtilities.dp(26), AndroidUtilities.dp(26)))
                except Exception:
                    wrap.addView(arrow)
                def _load_arrow():
                    try:
                        arrow_url = "https://assets.nowfy/check.png"
                        data = self._get_cached_image_enhanced(arrow_url, cache_key="spotify_connected_check")
                        if data:
                            bmp = BitmapFactory.decodeByteArray(data, 0, len(data))
                            if bmp:
                                run_on_ui_thread(lambda b=bmp: arrow.setImageBitmap(b))
                    except Exception:
                        pass
                run_on_queue(_load_arrow)
                def _toggle_menu(v):
                    try:
                        self.set_setting("spotify_profile_menu_open", (not bool(self.get_setting("spotify_profile_menu_open", False))))
                        self._refresh_spotify_settings_ui()
                    except Exception:
                        pass
                try:
                    arrow.setOnClickListener(OnClickListener(_toggle_menu))
                except Exception:
                    pass
            if not connected_ready:
                def _open_connect(v):
                    try:
                        self._start_quick_spotify_connect()
                        self._refresh_spotify_settings_ui()
                    except Exception:
                        pass
                try:
                    wrap.setClickable(True)
                    wrap.setFocusable(True)
                    wrap.setOnClickListener(OnClickListener(_open_connect))
                except Exception:
                    pass
            add_idx = min(int(insert_idx), items.size())
            try:
                rich = LinearLayout(ctx)
                rich.setOrientation(LinearLayout.VERTICAL)
                rich.setGravity(Gravity.START)
                try:
                    rich.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(14), AndroidUtilities.dp(14), AndroidUtilities.dp(14))
                except Exception:
                    pass
                try:
                    rbg = GradientDrawable()
                    rbg.setCornerRadius(AndroidUtilities.dp(16))
                    rbg.setColor(0x162B3E5A)
                    rich.setBackground(rbg)
                except Exception:
                    pass
                rt = TextView(ctx)
                rt.setText(tr("spotify_connection_title"))
                rt.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18)
                rt.setGravity(Gravity.START)
                try:
                    rt.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText))
                except Exception:
                    rt.setTextColor(0xFFFFFFFF)
                rich.addView(rt)
                rs = TextView(ctx)
                rs.setText(tr("spotify_quick_section_desc"))
                rs.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 13)
                rs.setGravity(Gravity.START)
                try:
                    rs.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText))
                except Exception:
                    rs.setTextColor(0xFFD2DCEB)
                rich.addView(rs)
                rich_item = UItem.asCustom(rich)
                rich_item.object2 = "__spotify_quick_rich_header__"
                items.add(add_idx, rich_item)
                add_idx += 1
            except Exception:
                pass
            custom_item = UItem.asCustom(wrap)
            custom_item.object2 = "__spotify_profile_custom__"
            items.add(add_idx, custom_item)
            try:
                code_visible = self._setting_bool("quick_code_visible", False)
            except Exception:
                code_visible = False
            if code_visible:
                has_quick_input = False
                try:
                    for j in range(items.size()):
                        itj = items.get(j)
                        if self._get_uitem_setting_key(itj) == "quick_oauth_code":
                            has_quick_input = True
                            break
                except Exception:
                    pass
                if not has_quick_input:
                    try:
                        code_item = UItem.asButton(
                            94112,
                            tr("spotify_quick_code")
                        ).accent()
                    except Exception:
                        code_item = UItem.asButton(
                            94112,
                            tr("spotify_quick_code")
                        )
                    try:
                        code_item.setIcon("todo_icon")
                    except Exception:
                        pass
                    try:
                        code_item.object2 = "__spotify_confirmation_code_item__"
                    except Exception:
                        pass
                    items.add(min(add_idx + 1, items.size()), code_item)
            if connected_ready:
                action_text = tr("spotify_quick_renew_code")
                try:
                    action_item = UItem.asButton(94111, action_text).accent()
                except Exception:
                    action_item = UItem.asButton(94111, action_text)
                try:
                    action_item.setIcon("menu_feature_reliable")
                except Exception:
                    pass
                try:
                    action_item.object2 = "__spotify_connect_action__"
                except Exception:
                    pass
                items.add(min(add_idx + 1, items.size()), action_item)
        except Exception:
            pass

    def _reopen_spotify_subfragment(self):
        try:
            try:
                log("[Nowfy] reopen Spotify requested")
            except Exception:
                pass
            fragment = get_last_fragment()
            controller = PluginsController.getInstance()
            plugin = controller.plugins.get(self.id) if controller else None
            if not plugin:
                try:
                    log("[Nowfy] reopen Spotify failed: plugin not found")
                except Exception:
                    pass
                return False
            activity = PluginSettingsActivity(plugin)
            try:
                ok = bool(self._set_subfragment_callback(activity, self.create_spotify_credentials_subfragment))
            except Exception:
                ok = False
            if not ok:
                try:
                    log("[Nowfy] reopen Spotify failed: callback bind failed")
                except Exception:
                    pass
                return False
            if fragment:
                fragment.presentFragment(activity)
                try:
                    log("[Nowfy] reopen Spotify success")
                except Exception:
                    pass
                return True
        except Exception:
            pass
        return False

    def _reopen_lastfm_subfragment(self):
        try:
            try:
                log("[Nowfy] reopen LastFM requested")
            except Exception:
                pass
            fragment = get_last_fragment()
            controller = PluginsController.getInstance()
            plugin = controller.plugins.get(self.id) if controller else None
            if not plugin:
                try:
                    log("[Nowfy] reopen LastFM failed: plugin not found")
                except Exception:
                    pass
                return False
            activity = PluginSettingsActivity(plugin)
            try:
                ok = bool(self._set_subfragment_callback(activity, self.create_lastfm_credentials_subfragment))
            except Exception:
                ok = False
            if not ok:
                try:
                    log("[Nowfy] reopen LastFM failed: callback bind failed")
                except Exception:
                    pass
                return False
            if fragment:
                fragment.presentFragment(activity)
                try:
                    log("[Nowfy] reopen LastFM success")
                except Exception:
                    pass
                return True
        except Exception:
            pass
        return False

    def _reopen_statsfm_subfragment(self):
        try:
            try:
                log("[Nowfy] reopen StatsFM requested")
            except Exception:
                pass
            fragment = get_last_fragment()
            controller = PluginsController.getInstance()
            plugin = controller.plugins.get(self.id) if controller else None
            if not plugin:
                try:
                    log("[Nowfy] reopen StatsFM failed: plugin not found")
                except Exception:
                    pass
                return False
            activity = PluginSettingsActivity(plugin)
            try:
                ok = bool(self._set_subfragment_callback(activity, self.create_statsfm_credentials_subfragment))
            except Exception:
                ok = False
            if not ok:
                try:
                    log("[Nowfy] reopen StatsFM failed: callback bind failed")
                except Exception:
                    pass
                return False
            if fragment:
                fragment.presentFragment(activity)
                try:
                    log("[Nowfy] reopen StatsFM success")
                except Exception:
                    pass
                return True
        except Exception:
            pass
        return False

    def _reopen_statsfm_top_subfragment(self):
        try:
            fragment = get_last_fragment()
            controller = PluginsController.getInstance()
            plugin = controller.plugins.get(self.id) if controller else None
            if not plugin:
                return False
            activity = PluginSettingsActivity(plugin)
            try:
                ok = bool(self._set_subfragment_callback(activity, self.create_statsfm_top_subfragment))
            except Exception:
                ok = False
            if not ok:
                return False
            if fragment:
                fragment.presentFragment(activity)
                return True
        except Exception:
            pass
        return False

    def _reopen_services_subfragment(self):
        try:
            try:
                log("[Nowfy] reopen Services requested")
            except Exception:
                pass
            fragment = get_last_fragment()
            controller = PluginsController.getInstance()
            plugin = controller.plugins.get(self.id) if controller else None
            if not plugin:
                return False
            activity = PluginSettingsActivity(plugin)
            try:
                ok = bool(self._set_subfragment_callback(activity, self.create_services_subfragment))
            except Exception:
                ok = False
            if not ok:
                return False
            if fragment:
                fragment.presentFragment(activity)
                try:
                    log("[Nowfy] reopen Services success")
                except Exception:
                    pass
                return True
        except Exception:
            pass
        return False

    def _show_spotify_confirmation_code_dialog(self):
        try:
            fragment = get_last_fragment()
            ctx = fragment.getParentActivity() if fragment and fragment.getParentActivity() else ApplicationLoader.applicationContext
            if not ctx:
                return
            from org.telegram.ui.Components import EditTextBoldCursor
            from android.text import InputType
            from android.widget import LinearLayout
            from android.graphics.drawable import GradientDrawable
            from org.telegram.ui.ActionBar import Theme
            from ui.alert import AlertDialogBuilder
            input_field = EditTextBoldCursor(ctx)
            input_field.setHint(tr("spotify_quick_code"))
            input_field.setInputType(InputType.TYPE_CLASS_TEXT)
            input_field.setMaxLines(1)
            input_field.setSingleLine(True)
            input_field.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
            try:
                input_field.setText(str(self.get_setting("quick_oauth_code", "") or ""))
            except Exception:
                pass
            try:
                input_field.setTextColor(Theme.getColor(Theme.key_dialogTextBlack))
                input_field.setHintTextColor(Theme.getColor(Theme.key_dialogTextHint))
                input_field.setCursorColor(Theme.getColor(Theme.key_dialogTextLink))
            except Exception:
                pass
            try:
                input_field.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(12), AndroidUtilities.dp(12), AndroidUtilities.dp(12))
            except Exception:
                pass
            try:
                ip_bg = GradientDrawable()
                ip_bg.setCornerRadius(AndroidUtilities.dp(12))
                try:
                    ip_bg.setColor(Theme.getColor(Theme.key_dialogBackground))
                    ip_bg.setStroke(AndroidUtilities.dp(1), Theme.getColor(Theme.key_windowBackgroundWhiteGrayText4))
                except Exception:
                    ip_bg.setColor(0x1A2A3A52)
                    ip_bg.setStroke(AndroidUtilities.dp(1), 0x556FA8DC)
                input_field.setBackground(ip_bg)
            except Exception:
                pass
            content = LinearLayout(ctx)
            content.setOrientation(LinearLayout.VERTICAL)
            try:
                content.setPadding(AndroidUtilities.dp(22), AndroidUtilities.dp(4), AndroidUtilities.dp(22), AndroidUtilities.dp(6))
            except Exception:
                pass
            content.addView(input_field, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT))
            builder = AlertDialogBuilder(ctx)
            builder.set_title(tr("spotify_quick_code"))
            builder.set_view(content)
            def _save(dialog, widget):
                try:
                    code = str(input_field.getText().toString() if input_field.getText() is not None else "").strip()
                    if not code:
                        return
                    try:
                        self.set_setting("quick_oauth_code", code)
                    except Exception:
                        pass
                    try:
                        self._finalize_quick_spotify_connect(code)
                    except Exception:
                        pass
                    try:
                        dialog.dismiss()
                    except Exception:
                        pass
                except Exception:
                    pass
            builder.set_positive_button(tr("done"), _save)
            builder.set_negative_button(tr("cancel_button"), None)
            run_on_ui_thread(builder.show)
        except Exception:
            pass

    def _get_spotify_current_track_id(self):
        try:
            token = self._get_access_token(show_error_bulletin=False)
            if not token:
                return None
            resp = requests.get(
                "https://api.spotify.com/v1/me/player/currently-playing",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5
            )
            if resp.status_code != 200 or not resp.content:
                return None
            data = resp.json() if resp.content else {}
            if not isinstance(data, dict):
                return None
            if not bool(data.get("is_playing", False)):
                return None
            item = data.get("item") or {}
            if not isinstance(item, dict):
                return None
            tid = item.get("id")
            return tid if tid else None
        except Exception as e:
            log(f"[Nowfy] Error getting Spotify current track: {str(e)}")
            return None

    def _get_spotify_last_track(self):
        try:
            token = self._get_access_token(show_error_bulletin=False)
            if not token:
                return None
            resp = requests.get(
                "https://api.spotify.com/v1/me/player/recently-played?limit=1",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5
            )
            if resp.status_code != 200 or not resp.content:
                return None
            data = resp.json() if resp.content else {}
            items = data.get("items", []) if isinstance(data, dict) else []
            if not items:
                return None
            track = items[0].get("track", {})
            if not isinstance(track, dict):
                return None
            title = track.get("name", "")
            artist = ""
            try:
                artist = ", ".join([a.get("name", "") for a in track.get("artists", []) if isinstance(a, dict)]).strip()
            except Exception:
                artist = ""
            image_url = ""
            try:
                images = track.get("album", {}).get("images", []) if isinstance(track.get("album"), dict) else []
                if images:
                    image_url = images[0].get("url", "") or ""
            except Exception:
                image_url = ""
            return {
                "title": title,
                "artist": artist,
                "image_url": image_url,
                "id": track.get("id", "")
            }
        except Exception as e:
            log(f"[Nowfy] Error getting Spotify last track: {str(e)}")
            return None

    def _get_spotify_recent_track_ids(self, limit=8):
        try:
            token = self._get_access_token(show_error_bulletin=False)
            if not token:
                return []
            lim = max(1, min(int(limit or 8), 20))
            resp = requests.get(
                f"https://api.spotify.com/v1/me/player/recently-played?limit={lim}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=6
            )
            if resp.status_code != 200 or not resp.content:
                return []
            data = resp.json() if resp.content else {}
            items = data.get("items", []) if isinstance(data, dict) else []
            ids = []
            for it in items or []:
                trk = (it or {}).get("track") or {}
                tid = (trk or {}).get("id")
                if tid and tid not in ids:
                    ids.append(tid)
            return ids
        except Exception as e:
            log(f"[Nowfy] Error getting Spotify recent track IDs: {str(e)}")
            return []

    def _get_spotify_top_tracks(self, limit=8):
        try:
            token = self._get_access_token(show_error_bulletin=False)
            if not token:
                return []
            url = f"https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit={max(1, min(int(limit or 8), 20))}"
            resp = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=6)
            if resp.status_code != 200 or not resp.content:
                return []
            data = resp.json() if resp.content else {}
            items = data.get("items", [])
            ids = []
            for t in items or []:
                tid = (t or {}).get("id")
                if tid:
                    ids.append(tid)
            return ids
        except Exception as e:
            log(f"[Nowfy] Error getting Spotify top tracks: {str(e)}")
            return []

    def _get_spotify_audio_features(self, track_ids):
        try:
            token = self._get_access_token(show_error_bulletin=False)
            if not token:
                return []
            ids = ",".join([str(x) for x in (track_ids or []) if x])
            if not ids:
                return []
            url = f"https://api.spotify.com/v1/audio-features?ids={ids}"
            resp = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=6)
            if resp.status_code != 200 or not resp.content:
                return []
            data = resp.json() if resp.content else {}
            features = data.get("audio_features")
            if isinstance(features, list):
                return features
            return []
        except Exception as e:
            log(f"[Nowfy] Error getting Spotify audio features: {str(e)}")
            return []

    def create_link_options_subfragment(self):
        current_player_setting = self.get_setting("current_player", 0)
        is_fm_player = current_player_setting == 9
        external_themes = self._get_external_themes() or {}
        current_theme = self.get_setting("theme_selector", 0)
        spotlight_index = len(external_themes) + 1
        vinify_index = spotlight_index + 1
        nowv_index = vinify_index + 1
        show_player_duplicate = is_fm_player and (current_theme in [0, spotlight_index, vinify_index, nowv_index])
        options = [
            Divider(text=tr("link_options_welcome")),
            Switch(
                key="show_track_link",
                text=tr("show_track_link"),
                subtext=tr("show_track_link_sub"),
                default=True,
                icon="filled_link_remix",
                on_change=lambda v: self.reload_settings()
            ),
        ]
        if self.get_setting("show_track_link", True):
            options.append(
                Selector(
                    key="platform_links",
                    text="Platform Links",
                    default=0,
                    items=[
                        "Spotify",
                        "Universal",
                        tr("platform_links_both")
                    ],
                    icon="msg_link",
                    on_change=lambda value: self.show_universal_link_dialog() if value == 1 else None
                )
            )
        options.extend([
            Divider(text="FM Links"),
            Selector(
                key="fm_link_option",
                icon="menu_username_change",
                text=tr("fm_link_selector"),
                default=0,
                items=["None", "LastFM", "StatsFM", "Custom Link"]
            )
        ])
        if is_fm_player:
            options.append(Input(
                key="fm_custom_link_url",
                text=tr("fm_custom_link_url"),
                icon="msg_link2_remix",
                default=self.get_setting("fm_custom_link_url", ""),
                subtext=tr("fm_custom_link_url_sub")
            ))
        if show_player_duplicate:
            options.append(Input(
                key="fm_custom_player_name",
                text=tr("fmcard_custom_player_name"),
                icon="msg_photo_text_framed3",
                default=self.get_setting("fm_custom_player_name", "Custom Player"),
                subtext=tr("fmcard_custom_player_name_sub")
            ))
        return options

    def create_advanced_options_subfragment(self):
        return [
            Divider(text=tr("thumbnail_cache_section")),
            Switch(
                key="enable_youtube_thumbnail_cache",
                text=tr("youtube_cache"),
                subtext=tr("youtube_cache_sub"),
                default=False,
                icon="msg_data"
            ),
            Switch(
                key="enable_soundcloud_thumbnail_cache",
                text=tr("soundcloud_cache"),
                subtext=tr("soundcloud_cache_sub"),
                default=False,
                icon="msg_data"
            ),
            Divider(text=tr("quality_options_section")),
            Switch(
                key="enable_quality_fallback",
                text=tr("quality_fallback"),
                subtext=tr("quality_fallback_sub"),
                default=True,
                icon="msg_retry"
            ),
            Switch(
                key="enable_url_cache",
                text=tr("url_cache"),
                subtext=tr("url_cache_sub"),
                default=True,
                icon="msg_link"
            ),
            Switch(
                key="enable_adaptive_compression",
                text=tr("adaptive_compression"),
                subtext=tr("adaptive_compression_sub"),
                default=False,
                icon="msg_premium_speed"
            )
        ]

    def create_spotify_credentials_subfragment(self):
        show_auth = self.get_setting("show_spotify_auth", False)
        items = [
            Divider(text=tr("spotify_auth_section")),
            Switch(
                key="show_spotify_auth",
                text="Spotify Auth",
                subtext=tr("spotify_auth_toggle_sub"),
                default=show_auth,
                icon="msg_filled_unlockedrecord",
                on_change=lambda v: self.reload_settings(),
                link_alias="nowfy_services_spotify_show_auth"
            )
        ]
        if show_auth:
            items.extend([
                Input(
                    key="client_id",
                    text="Client ID",
                    default=self.get_setting("client_id", ""),
                    icon="trusted_mini",
                    subtext=tr("client_id_subtext"),
                    link_alias="nowfy_services_spotify_client_id"
                ),
                Input(
                    key="client_secret",
                    text="Client Secret",
                    default=self.get_setting("client_secret", ""),
                    icon="trusted_mini",
                    subtext=tr("client_secret_subtext"),
                    link_alias="nowfy_services_spotify_client_secret"
                ),
                Input(
                    key="refresh_token",
                    text="Refresh Token",
                    default=self.get_setting("refresh_token", ""),
                    icon="trusted_mini",
                    subtext=tr("refresh_token_subtext"),
                    link_alias="nowfy_services_spotify_refresh_token"
                ),
            ])
        else:
            items.append(Text(text=tr("spotify_auth_hidden_notice"), icon="msg_info", link_alias="nowfy_services_spotify_auth_hidden"))
        items.append(Divider())
        try:
            st = self._get_quick_spotify_state()
            connected_ready = bool(st.get("connected", False)) and not bool(st.get("force_renew", False)) and not bool(st.get("expired", True))
            force_code_visible = self._setting_bool("quick_code_visible", False)
            if (not connected_ready) or force_code_visible:
                items.append(Input(
                    key="quick_oauth_code",
                    text=(tr("spotify_quick_code")),
                    default="",
                    icon="todo_icon",
                    subtext=(tr("spotify_quick_code_sub")),
                    link_alias="nowfy_services_spotify_quick_code"
                ))
        except Exception:
            items.append(Input(
                key="quick_oauth_code",
                text=(tr("spotify_quick_code")),
                default="",
                icon="todo_icon",
                subtext=(tr("spotify_quick_code_sub")),
                link_alias="nowfy_services_spotify_quick_code_fallback"
            ))
        items.extend([
            Divider(text=tr("spotify_custom_command_section")),
            Input(
                key="custom_command",
                text=tr("custom_command"),
                default=self.get_setting("custom_command", ".now"),
                icon="input_bot1",
                subtext=tr("custom_command_sub"),
                link_alias="nowfy_services_spotify_custom_command"
            ),
            Divider(text=tr("spotify_help_section")),
            Text(
                text=tr("credentials_info"),
                icon="msg2_help",
                accent=True,
                on_click=lambda view: self._show_credentials_info_dialog(),
                link_alias="nowfy_services_spotify_credentials_info"
            ),
            Text(
                text="Spotify Control",
                icon="live_stream",
                accent=True,
                on_click=lambda view: self._show_spotify_control_dialog(),
                link_alias="nowfy_services_spotify_control_info"
            ),
        ])
        try:
            code = str(self.get_setting("quick_oauth_code", "")).strip()
            last = str(getattr(self, "_last_quick_code_processed", "") or "")
            if code and code != last:
                self._last_quick_code_processed = code
                try:
                    self._finalize_quick_spotify_connect(code)
                except Exception:
                    pass
        except Exception:
            pass
        return items

    def _spotify_pick_best_image_url(self, images):
        try:
            if not isinstance(images, list) or not images:
                return ""
            sorted_images = sorted(
                [img for img in images if isinstance(img, dict)],
                key=lambda x: int((x.get("width") or 0) or 0) * int((x.get("height") or 0) or 0),
                reverse=True
            )
            if not sorted_images:
                return ""
            return str(sorted_images[0].get("url") or "").strip()
        except Exception:
            return ""

    def create_lastfm_credentials_subfragment(self):
        visible = self.get_setting("lastfm_api_key_visible", True)
        try:
            raw_player = self.get_setting("current_player", 0)
            if isinstance(raw_player, str) and raw_player.isdigit():
                raw_player = int(raw_player)
            if not isinstance(raw_player, int):
                raw_player = 0
            if raw_player < 0 or raw_player > 9:
                raw_player = 0
            current_player_idx = int(raw_player)
            try:
                if int(self.get_setting("current_player", 0) or 0) != current_player_idx:
                    self.set_setting("current_player", current_player_idx)
            except Exception:
                pass
        except Exception:
            current_player_idx = 0
        items = [
            Divider(text=tr("lastfm_auth_section")),
            Input(
                key="lastfm_username",
                text=tr("lastfm_username"),
                icon="menu_username_change",
                default=self.get_setting("lastfm_username", ""),
                subtext=tr("lastfm_user_subtext"),
                link_alias="nowfy_services_lastfm_username"
            ),
            Switch(
                key="lastfm_api_key_visible",
                text=tr("lastfm_key_visibility"),
                subtext=tr("lastfm_key_visibility_sub"),
                default=self.get_setting("lastfm_api_key_visible", True),
                icon="msg_permissions_solar",
                link_alias="nowfy_services_lastfm_key_visibility"
            ),
        ]
        if visible:
            items.append(
                Input(
                    key="lastfm_api_key",
                    text=tr("lastfm_api_key"),
                    icon="filled_access_fingerprint",
                    default=self.get_setting("lastfm_api_key", ""),
                    subtext=tr("lastfm_api_key_subtext"),
                    link_alias="nowfy_services_lastfm_api_key"
                )
            )
        items += [
            Divider(text=tr("music_detection_section")),
            Selector(
                key="current_player",
                icon="header_goinline_solar",
                text=tr("active_player"),
                default=current_player_idx,
                items=["Spotify", "YouTube", "YouTube Music", "exteraGram", "AyuGram", "SoundCloud", "Apple Music", "Yandex Music", "Deezer", "FM"],
                on_change=lambda value: (self._on_player_changed(value), self.reload_settings()),
                link_alias="nowfy_services_lastfm_active_player"
            ),
        ]
        if current_player_idx == 0:
            items += [
                Selector(
                    key="media_source",
                    icon="msg_filled_datausage",
                    text=tr("data_mode"),
                    default=self.get_setting("media_source", 0),
                    items=["Player", "Via Last.FM"],
                    link_alias="nowfy_services_lastfm_media_source"
                ),
            ]
        if current_player_idx == 9:
            items += [
                Input(
                    key="fm_custom_player_name",
                    text=tr("fmcard_custom_player_name"),
                    default=self.get_setting("fm_custom_player_name", "Custom Player"),
                    icon="msg_photo_text_framed3",
                    subtext=tr("fmcard_custom_player_name_sub"),
                    link_alias="nowfy_services_lastfm_fm_custom_player_name"
                ),
            ]
        items += [
            Divider(text=tr("apis_integration_section")),
            Selector(
                key="artwork_priority",
                icon="msg_saved_ny_remix",
                text=tr("diversos_artwork_api"),
                default=0,
                items=["Default", "Spotify", "Deezer", "Cover Art Archive", "iTunes", "YouTube", "LastFM"],
                link_alias="nowfy_services_lastfm_artwork_priority"
            ),
        ]
        items += [
            Divider(text=tr("lastfm_help_section")),
            Text(
                text=tr("test_lastfm_account"),
                icon="msg_limit_accounts",
                accent=True,
                on_click=lambda view: self._test_lastfm_account(),
                link_alias="nowfy_services_lastfm_test_account"
            ),
            Text(
                text=tr("lastfm_title"),
                icon="msg2_help",
                accent=True,
                on_click=lambda view: self._show_lastfm_api_dialog(),
                link_alias="nowfy_services_lastfm_help"
            ),
            Divider(text=tr("lastfm_players_welcome")),
        ]
        return items

    def create_statsfm_credentials_subfragment(self):
        statsfm_user = str(self.get_setting("statsfm_username", "") or "").strip()
        welcome_text = tr("statsfm_welcome")
        if statsfm_user:
            try:
                welcome_text = f"{welcome_text}\n\n{tr('statsfm_welcome_connected_extra')}"
            except Exception:
                pass
        items = [
            Selector(
                key="statsfm_source_player",
                text=tr("statsfm_source_player"),
                icon="header_goinline_solar",
                default=self.get_setting("statsfm_source_player", 0),
                items=["Spotify", "Apple Music"],
                link_alias="nowfy_services_statsfm_source_player"
            ),
        ]
        if statsfm_user:
            items.append(
                Text(
                    text=tr("statsfm_stats_nowfy"),
                    icon="msg_stats",
                    create_sub_fragment=self.create_statsfm_top_subfragment,
                    link_alias="nowfy_services_statsfm_top"
                )
            )
        items.append(Divider(text=welcome_text))
        return items

    def create_statsfm_top_subfragment(self):
        return [
            Divider(text=tr("statsfm_top_subfragment_welcome")),
        ]

    def create_ymusic_credentials_subfragment(self):
        try:
            self._ymusic_log("open settings subfragment")
        except Exception:
            pass
        return [
            Divider(text=(tr("ymusic_service_desc"))),
            Input(
                key="ymusic_api_token",
                text=(tr("ymusic_token_title")),
                icon="outline_shield_check",
                default=self.get_setting("ymusic_api_token", ""),
                subtext=(tr("ymusic_token_sub")),
                link_alias="nowfy_services_ymusic_token"
            ),
            Text(
                text=tr("ymusic_test_token_title"),
                icon="todo_icon",
                accent=True,
                on_click=lambda view: self._test_ymusic_token(),
                link_alias="nowfy_services_ymusic_test_token"
            ),
            Divider(text=(tr("ymusic_now_playing_desc"))),
            Text(
                text=tr("ymusic_help_subfragment_title"),
                icon="msg2_help",
                create_sub_fragment=self.create_ymusic_help_subfragment,
                link_alias="nowfy_services_ymusic_help"
            ),
        ]

    def create_ymusic_help_subfragment(self):
        return [
            Divider(text=tr("ymusic_help_subfragment_divider")),
        ]

    def _test_ymusic_token(self):
        try:
            token = str(self.get_setting("ymusic_api_token", "") or "").strip()
            self._ymusic_log(f"test token start has_token={bool(token)}")
            if not token:
                BulletinHelper.show_info(tr("ymusic_test_token_empty"))
                return
            BulletinHelper.show_info(tr("ymusic_test_token_loading"))
            def _worker():
                try:
                    base_headers = {
                        "Accept": "application/json",
                        "User-Agent": "Nowfy/1.0",
                        "X-Yandex-Music-Client": "YandexMusicAndroid/24023621",
                        "X-Yandex-Music-Device": "os=Android; os_version=16; manufacturer=Nowfy; model=NowfyPlugin; clid=; device_id=nowfy; uuid=nowfy",
                        "Authorization": f"OAuth {token}",
                    }
                    def _probe(url):
                        try:
                            r = requests.get(url, headers=base_headers, timeout=10)
                            status = int(r.status_code or 0)
                            if status != 200 or not r.content:
                                return False, False, status
                            body = r.json()
                            if not isinstance(body, dict):
                                return False, False, status
                            result = body.get("result") if isinstance(body.get("result"), dict) else body
                            if not isinstance(result, dict):
                                return False, False, status
                            acc = result.get("account") if isinstance(result.get("account"), dict) else {}
                            uid = acc.get("uid")
                            login = str(acc.get("login") or "").strip()
                            fullname = str(acc.get("fullName") or "").strip()
                            has_identity = bool(uid or login or fullname)
                            # serviceAvailable can be false for some accounts; token is still valid.
                            return True, has_identity, status
                        except Exception:
                            return False, False, 0

                    ok, auth_ok, status = _probe("https://api.music.yandex.net/account/status")
                    self._ymusic_log(f"test account/status ok={ok} auth_ok={auth_ok} status={status}")
                    if not ok:
                        ok, auth_ok, status = _probe("https://api.music.yandex.net/rotor/account/status")
                        self._ymusic_log(f"test rotor/account/status ok={ok} auth_ok={auth_ok} status={status}")
                    if ok:
                        try:
                            np_ok = False
                            if NOWFY_CORE_API and hasattr(NOWFY_CORE_API, "get_ymusic_now_playing_panel_data"):
                                pdata = NOWFY_CORE_API.get_ymusic_now_playing_panel_data(self) or {}
                                np_ok = bool(
                                    isinstance(pdata, dict)
                                    and pdata.get("has_session")
                                    and str(pdata.get("title") or "").strip()
                                )
                                self._ymusic_log(
                                    "panel_data has_session={} title='{}'".format(
                                        bool(pdata.get("has_session")),
                                        str(pdata.get("title") or "").strip()
                                    )
                                )
                            if np_ok:
                                run_on_ui_thread(lambda: BulletinHelper.show_success(tr("ymusic_test_token_valid")))
                            else:
                                run_on_ui_thread(lambda: BulletinHelper.show_info(tr("ymusic_test_token_no_active_session")))
                        except Exception:
                            run_on_ui_thread(lambda: BulletinHelper.show_success(tr("ymusic_test_token_valid")))
                    else:
                        self._ymusic_log(f"test token invalid status={status} auth_ok={auth_ok}")
                        if status == 200 and not auth_ok:
                            msg = tr("ymusic_test_token_missing_uid")
                        else:
                            try:
                                msg = str(tr("ymusic_test_token_invalid_status") or "").format(status=status)
                            except Exception:
                                msg = f"{tr('ymusic_test_token_invalid')} ({status})"
                        run_on_ui_thread(lambda m=msg: BulletinHelper.show_info(m))
                except Exception:
                    self._ymusic_log("test token worker failed")
                    run_on_ui_thread(lambda: BulletinHelper.show_info(tr("ymusic_test_token_failed")))
            threading.Thread(target=_worker, daemon=True).start()
        except Exception:
            try:
                BulletinHelper.show_info(tr("ymusic_test_token_failed"))
            except Exception:
                pass

    def _ymusic_log(self, message):
        try:
            if bool(self.get_setting("disable_logs", False)):
                return
        except Exception:
            pass
        try:
            log(f"[Nowfy][YMusic] {str(message)}")
        except Exception:
            pass

    def _show_statsfm_username_input_dialog(self):
        try:
            fragment = get_last_fragment()
            ctx = fragment.getParentActivity() if fragment and fragment.getParentActivity() else ApplicationLoader.applicationContext
            if not ctx:
                return
            from org.telegram.ui.Components import EditTextBoldCursor
            from android.text import InputType
            from android.util import TypedValue
            from org.telegram.ui.ActionBar import Theme
            from android.widget import LinearLayout, TextView
            from android.view import Gravity
            from android.graphics.drawable import GradientDrawable
            input_field = EditTextBoldCursor(ctx)
            input_field.setHint("@username")
            input_field.setInputType(InputType.TYPE_CLASS_TEXT)
            input_field.setMaxLines(1)
            input_field.setSingleLine(True)
            input_field.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 16)
            try:
                input_field.setText(str(self.get_setting("statsfm_username", "") or ""))
            except Exception:
                pass
            try:
                input_field.setTextColor(Theme.getColor(Theme.key_dialogTextBlack))
                input_field.setHintTextColor(Theme.getColor(Theme.key_dialogTextHint))
                input_field.setCursorColor(Theme.getColor(Theme.key_dialogTextLink))
            except Exception:
                pass
            try:
                input_field.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(12), AndroidUtilities.dp(12), AndroidUtilities.dp(12))
            except Exception:
                pass
            try:
                ip_bg = GradientDrawable()
                ip_bg.setCornerRadius(AndroidUtilities.dp(12))
                try:
                    ip_bg.setColor(Theme.getColor(Theme.key_dialogBackground))
                    ip_bg.setStroke(AndroidUtilities.dp(1), Theme.getColor(Theme.key_windowBackgroundWhiteGrayText4))
                except Exception:
                    ip_bg.setColor(0x1A2A3A52)
                    ip_bg.setStroke(AndroidUtilities.dp(1), 0x556FA8DC)
                input_field.setBackground(ip_bg)
            except Exception:
                pass
            content = LinearLayout(ctx)
            content.setOrientation(LinearLayout.VERTICAL)
            try:
                content.setPadding(AndroidUtilities.dp(22), AndroidUtilities.dp(4), AndroidUtilities.dp(22), AndroidUtilities.dp(6))
            except Exception:
                pass
            sub = TextView(ctx)
            sub.setText(tr("statsfm_username_sub"))
            sub.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 12)
            sub.setGravity(Gravity.START)
            try:
                sub.setTextColor(Theme.getColor(Theme.key_dialogTextHint))
            except Exception:
                sub.setTextColor(0xFFD2DCEB)
            try:
                slp = LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT)
                slp.topMargin = AndroidUtilities.dp(0)
                slp.bottomMargin = AndroidUtilities.dp(10)
                content.addView(sub, slp)
            except Exception:
                content.addView(sub)
            content.addView(input_field, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT))
            builder = AlertDialogBuilder(ctx)
            builder.set_title(tr("statsfm_username"))
            builder.set_view(content)
            def _save(dialog, widget):
                try:
                    username = str(input_field.getText().toString() if input_field.getText() is not None else "").strip().lstrip("@")
                    if not username:
                        return
                    def _worker():
                        try:
                            if not self._statsfm_username_exists(username):
                                try:
                                    run_on_ui_thread(lambda: BulletinHelper.show_info(tr("statsfm_username_invalid")))
                                except Exception:
                                    BulletinHelper.show_info(tr("statsfm_username_invalid"))
                                return
                            def _apply_valid_username():
                                try:
                                    prev_user = str(self.get_setting("statsfm_username", "") or "").strip().lower().lstrip("@")
                                    new_user = str(username or "").strip().lower().lstrip("@")
                                    self.set_setting("statsfm_username", username)
                                    self.set_setting("statsfm_profile_menu_open", False)
                                    try:
                                        self.set_setting("statsfm_profile_cache_bust", str(int(time.time() * 1000)))
                                    except Exception:
                                        pass
                                    if prev_user != new_user:
                                        try:
                                            self._invalidate_statsfm_recent_cache()
                                        except Exception:
                                            try:
                                                self.set_setting("statsfm_recent_cache_bust", str(int(time.time() * 1000)))
                                            except Exception:
                                                pass
                                    self._refresh_statsfm_settings_ui()
                                    BulletinHelper.show_success(tr("saved"))
                                    try:
                                        dialog.dismiss()
                                    except Exception:
                                        pass
                                except Exception:
                                    pass
                            try:
                                run_on_ui_thread(_apply_valid_username)
                            except Exception:
                                _apply_valid_username()
                        except Exception:
                            try:
                                run_on_ui_thread(lambda: BulletinHelper.show_info(tr("statsfm_username_invalid")))
                            except Exception:
                                BulletinHelper.show_info(tr("statsfm_username_invalid"))
                    threading.Thread(target=_worker, daemon=True).start()
                except Exception:
                    pass
            builder.set_positive_button(tr("done"), _save)
            builder.set_negative_button(tr("cancel_button"), None)
            run_on_ui_thread(builder.show)
        except Exception as e:
            log(f"[Nowfy] StatsFM input dialog error: {e}")

    def _refresh_statsfm_settings_ui(self):
        try:
            activity = getattr(self, "_statsfm_settings_activity", None)
            if activity:
                try:
                    list_view = get_private_field(activity, "listView")
                    adapter = getattr(list_view, "adapter", None) if list_view else None
                    if adapter:
                        try:
                            run_on_ui_thread(lambda: adapter.update(False))
                        except Exception:
                            pass
                        run_on_ui_thread(lambda: adapter.update(True))
                        try:
                            self.reload_settings()
                        except Exception:
                            pass
                        try:
                            frag = get_last_fragment()
                            if frag:
                                try:
                                    run_on_ui_thread(lambda: frag.rebuildSettings())
                                except Exception:
                                    run_on_ui_thread(lambda: frag.rebuildAllFragments(True))
                        except Exception:
                            pass
                        return
                except Exception:
                    pass
            fragment = get_last_fragment()
            if fragment:
                try:
                    lv = getattr(fragment, "listView", None)
                    ad = getattr(lv, "adapter", None) if lv else None
                    if ad:
                        try:
                            run_on_ui_thread(lambda: ad.update(False))
                        except Exception:
                            pass
                        run_on_ui_thread(lambda: ad.update(True))
                        try:
                            self.reload_settings()
                        except Exception:
                            pass
                        try:
                            run_on_ui_thread(lambda: fragment.rebuildSettings())
                        except Exception:
                            try:
                                run_on_ui_thread(lambda: fragment.rebuildAllFragments(True))
                            except Exception:
                                pass
                        return
                except Exception:
                    pass
            self.reload_settings()
        except Exception:
            try:
                self.reload_settings()
            except Exception:
                pass

    def _perform_statsfm_logout(self):
        try:
            self.set_setting("statsfm_username", "")
            self.set_setting("statsfm_profile_menu_open", False)
            try:
                self.set_setting("statsfm_profile_cache_bust", str(int(time.time() * 1000)))
                self.set_setting("statsfm_recent_cache_bust", str(int(time.time() * 1000)))
            except Exception:
                pass
            try:
                self._invalidate_statsfm_recent_cache()
            except Exception:
                pass
            self._refresh_statsfm_settings_ui()
        except Exception:
            pass

    def _invalidate_statsfm_recent_cache(self):
        try:
            mem = getattr(self, "_statsfm_recent_blob_memory", None)
            if isinstance(mem, dict):
                mem.clear()
        except Exception:
            pass
        try:
            self.set_setting("statsfm_recent_cache_bust", str(int(time.time() * 1000)))
            self.set_setting("statsfm_profile_cache_bust", str(int(time.time() * 1000)))
        except Exception:
            pass

    def create_nowcast_subfragment(self):
        return [Divider(text="NowCast addon not installed")]

    def create_pop_island_subfragment(self):
        return [Divider(text="Floatify addon not installed")]

    def create_mods_subfragment(self):
        return [
            Header(text=(tr("mods_section"))),
            Switch(
                key="on_notch_enabled",
                text=(tr("on_notch_label")),
                subtext=(tr("on_notch_sub")),
                default=self.get_setting("on_notch_enabled", False),
                icon="msg_go_up",
                on_change=lambda v: (
                    self.set_setting("on_notch_enabled", v),
                    self._reposition_dynamic_island_to_notch(),
                    self.reload_settings()
                )
            ),
            Divider(),
            Switch(
                key="overlay_activation_bulletin_enabled",
                text=(tr("overlay_activation_bulletin_label")),
                subtext=(tr("overlay_activation_bulletin_sub")),
                default=self.get_setting("overlay_activation_bulletin_enabled", False),
                icon="msg_notspam",
                on_change=lambda v: self.set_setting("overlay_activation_bulletin_enabled", v)
            ),
            Divider(),
            Switch(
                key="overlay_auto_disable_inactivity",
                text=(tr("overlay_auto_disable_inactivity_label")),
                subtext=(tr("overlay_auto_disable_inactivity_sub")),
                default=self.get_setting("overlay_auto_disable_inactivity", False),
                icon="msg2_night_auto",
                on_change=lambda v: self.set_setting("overlay_auto_disable_inactivity", v)
            ),
            Selector(
                key="overlay_inactivity_timeout_minutes",
                text=(tr("overlay_inactivity_timeout_label")),
                default=([5,10,15,30,60,1].index(self.get_setting("overlay_inactivity_timeout_minutes", 10)) if self.get_setting("overlay_inactivity_timeout_minutes", 10) in [5,10,15,30,60,1] else 1),
                items=["5 min","10 min","15 min","30 min","60 min","1 min"],
                icon="msg_stories_timer",
                on_change=lambda v: self.set_setting("overlay_inactivity_timeout_minutes", [5,10,15,30,60,1][v])
            ),
            Divider(),
            Switch(
                key="di_haptic_enabled",
                text=(tr("di_haptic_label")),
                subtext=(tr("di_haptic_sub")),
                default=self.get_setting("di_haptic_enabled", False),
                icon="msg2_sticker",
                on_change=lambda v: self.reload_settings()
            ),
        ]
    NO_TRACK_PLAYING = {
        "en": "No track playing on %s",
        "pt": "Nenhuma faixa tocando no %s",
        "es": "Ninguna pista se está reproduciendo en %s",
        "fr": "Aucune piste en cours de lecture sur %s",
        "ru": "Нет воспроизводимой дорожки в %s",
    }

class BackupManager:

    def __init__(self, plugin_instance):
        self.plugin = plugin_instance
        self._impl = None
        try:
            if nowfycore is not None and hasattr(nowfycore, "BackupManager"):
                self._impl = nowfycore.BackupManager(plugin_instance)
        except Exception:
            self._impl = None
        self.backup_dir = str(getattr(self._impl, "backup_dir", "") or "")

    def _call(self, name, *args, **kwargs):
        try:
            fn = getattr(self._impl, name, None)
            if callable(fn):
                return fn(*args, **kwargs)
        except Exception:
            pass
        return None

    def export_backup(self):
        out = self._call("export_backup")
        if out is not None:
            return out
        try:
            BulletinHelper.show_info(tr("backup_export_error"))
        except Exception:
            BulletinHelper.show_info("Backup unavailable")
        return None

    def import_backup(self):
        out = self._call("import_backup")
        if out is not None:
            return out
        try:
            BulletinHelper.show_info(tr("backup_import_error"))
        except Exception:
            BulletinHelper.show_info("Backup unavailable")
        return None

    def restore_from_backup(self, filename):
        out = self._call("restore_from_backup", filename)
        if out is not None:
            return out
        try:
            BulletinHelper.show_info(tr("backup_restore_error"))
        except Exception:
            BulletinHelper.show_info("Backup unavailable")
        return None

    def list_backups(self):
        out = self._call("list_backups")
        if out is not None:
            return out
        try:
            BulletinHelper.show_info(tr("backup_list_error"))
        except Exception:
            BulletinHelper.show_info("Backup unavailable")
        return None

    def collect_all_settings(self):
        out = self._call("collect_all_settings")
        return out if isinstance(out, dict) else {}

    def export_data(self):
        try:
            settings = self.collect_all_settings()
            return {
                "version": __version__,
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "plugin_name": "Nowfy",
                "settings": settings,
                "total_settings": len(settings)
            }
        except Exception:
            return {}

    def import_data(self, data):
        try:
            if not isinstance(data, dict):
                return False
            settings = data.get("settings")
            if not isinstance(settings, dict):
                return False
            for key, value in settings.items():
                try:
                    self.plugin.set_setting(key, value)
                except Exception:
                    pass
            return True
        except Exception:
            return False
try:
    exteraFyPlugin.__name__ = "NowfyPlugin"
    exteraFyPlugin.__qualname__ = "NowfyPlugin"
except Exception:
    pass
