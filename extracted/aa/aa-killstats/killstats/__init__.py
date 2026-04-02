"""Initialize the app"""

__version__ = "2.0.3"
__title__ = "Killstats"

__package_name__ = "aa-killstats"
__app_name__ = "killstats"
__esi_compatibility_date__ = "2025-09-30"
__app_name_useragent__ = "AA-Killstats"

__github_url__ = f"https://github.com/Geuthur/{__package_name__}"

USER_AGENT_TEXT = f"{__app_name_useragent__} v{__version__} @ {__github_url__}"

__killmail_operations__ = [
    "GetKillmailsKillmailIdKillmailHash",
    "PostUniverseNames",
]
