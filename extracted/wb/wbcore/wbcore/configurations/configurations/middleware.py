class Middleware:
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        # "maintenance_mode.middleware.MaintenanceModeMiddleware", # we leave it commented for now to try out the performance gain to not evaluate maintenance mode on every request lifecycle
    ]


class DevMiddleware:
    @property
    def MIDDLEWARE(self):  # noqa
        middleware = []
        middleware_list = Middleware.MIDDLEWARE.copy()
        if self.DEBUG:
            middleware.append("debug_toolbar.middleware.DebugToolbarMiddleware")
        middleware_list.insert(
            middleware_list.index("django.contrib.sessions.middleware.SessionMiddleware") + 1,
            "django.middleware.locale.LocaleMiddleware",
        )  # The django "LocaleMiddleware" needs to come after "SessionMiddleware" and before "CommonMiddleware".
        middleware.extend(middleware_list)
        return middleware
