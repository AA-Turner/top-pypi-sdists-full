from dataclasses import dataclass, field, fields
from pathlib import Path
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.support.entities.base import BaseEntity

@dataclass(frozen=True, kw_only=True)
class Paths(BaseEntity):

    console_scheduler: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'console' / 'scheduler.py').resolve()),
        metadata = {
            'description': 'Path to the console scheduler (Kernel) file.',
            'default': lambda: str((Path.cwd() / 'app' / 'console' / 'scheduler.py').resolve())
        }
    )

    console_commands: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'console' / 'commands').resolve()),
        metadata = {
            'description': 'Directory containing custom ArtisanStyle console commands.',
            'default': lambda: str((Path.cwd() / 'app' / 'console' / 'commands').resolve())
        }
    )

    http_controllers: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'http' / 'controllers').resolve()),
        metadata = {
            'description': 'Directory containing HTTP controller classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'http' / 'controllers').resolve())
        }
    )

    http_middleware: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'http' / 'middleware').resolve()),
        metadata = {
            'description': 'Directory containing HTTP middleware classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'http' / 'middleware').resolve())
        }
    )

    http_requests: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'http' / 'requests').resolve()),
        metadata = {
            'description': 'Directory containing HTTP form request validation classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'http' / 'requests').resolve())
        }
    )

    models: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'models').resolve()),
        metadata = {
            'description': 'Directory containing ORM model classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'models').resolve())
        }
    )

    providers: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'providers').resolve()),
        metadata = {
            'description': 'Directory containing service provider classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'providers').resolve())
        }
    )

    events: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'events').resolve()),
        metadata = {
            'description': 'Directory containing event classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'events').resolve())
        }
    )

    listeners: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'listeners').resolve()),
        metadata = {
            'description': 'Directory containing event listener classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'listeners').resolve())
        }
    )

    notifications: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'notifications').resolve()),
        metadata = {
            'description': 'Directory containing notification classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'notifications').resolve())
        }
    )

    jobs: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'jobs').resolve()),
        metadata = {
            'description': 'Directory containing queued job classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'jobs').resolve())
        }
    )

    policies: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'policies').resolve()),
        metadata = {
            'description': 'Directory containing authorization policy classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'policies').resolve())
        }
    )

    exceptions: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'exceptions').resolve()),
        metadata = {
            'description': 'Directory containing exception handler classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'exceptions').resolve())
        }
    )

    services: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'services').resolve()),
        metadata = {
            'description': 'Directory containing business logic service classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'services').resolve())
        }
    )

    views: str = field(
        default_factory = lambda: str((Path.cwd() / 'resources' / 'views').resolve()),
        metadata = {
            'description': 'Directory containing template view files.',
            'default': lambda: str((Path.cwd() / 'resources' / 'views').resolve())
        }
    )

    lang: str = field(
        default_factory = lambda: str((Path.cwd() / 'resources' / 'lang').resolve()),
        metadata = {
            'description': 'Directory containing internationalization files.',
            'default': lambda: str((Path.cwd() / 'resources' / 'lang').resolve())
        }
    )

    assets: str = field(
        default_factory = lambda: str((Path.cwd() / 'resources' / 'assets').resolve()),
        metadata = {
            'description': 'Directory containing frontend assets (JS, CSS, images).',
            'default': lambda: str((Path.cwd() / 'resources' / 'assets').resolve())
        }
    )

    routes_web: str = field(
        default_factory = lambda: str((Path.cwd() / 'routes' / 'web.py').resolve()),
        metadata = {
            'description': 'Path to the web routes definition file.',
            'default': lambda: str((Path.cwd() / 'routes' / 'web.py').resolve())
        }
    )

    routes_api: str = field(
        default_factory = lambda: str((Path.cwd() / 'routes' / 'api.py').resolve()),
        metadata = {
            'description': 'Path to the API routes definition file.',
            'default': lambda: str((Path.cwd() / 'routes' / 'api.py').resolve())
        }
    )

    routes_console: str = field(
        default_factory = lambda: str((Path.cwd() / 'routes' / 'console.py').resolve()),
        metadata = {
            'description': 'Path to the console routes definition file.',
            'default': lambda: str((Path.cwd() / 'routes' / 'console.py').resolve())
        }
    )

    routes_channels: str = field(
        default_factory = lambda: str((Path.cwd() / 'routes' / 'channels.py').resolve()),
        metadata = {
            'description': 'Path to the broadcast channels routes file.',
            'default': lambda: str((Path.cwd() / 'routes' / 'channels.py').resolve())
        }
    )

    config: str = field(
        default_factory = lambda: str((Path.cwd() / 'config').resolve()),
        metadata = {
            'description': 'Directory containing application configuration files.',
            'default': lambda: str((Path.cwd() / 'config').resolve())
        }
    )

    migrations: str = field(
        default_factory = lambda: str((Path.cwd() / 'database' / 'migrations').resolve()),
        metadata = {
            'description': 'Directory containing database migration files.',
            'default': lambda: str((Path.cwd() / 'database' / 'migrations').resolve())
        }
    )

    seeders: str = field(
        default_factory = lambda: str((Path.cwd() / 'database' / 'seeders').resolve()),
        metadata = {
            'description': 'Directory containing database seeder files.',
            'default': lambda: str((Path.cwd() / 'database' / 'seeders').resolve())
        }
    )

    factories: str = field(
        default_factory = lambda: str((Path.cwd() / 'database' / 'factories').resolve()),
        metadata = {
            'description': 'Directory containing model factory files.',
            'default': lambda: str((Path.cwd() / 'database' / 'factories').resolve())
        }
    )

    storage_logs: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage' / 'logs').resolve()),
        metadata = {
            'description': 'Directory containing application log files.',
            'default': lambda: str((Path.cwd() / 'storage' / 'logs').resolve())
        }
    )

    storage_framework: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage' / 'framework').resolve()),
        metadata = {
            'description': 'Directory for framework-generated files (cache, sessions, views).',
            'default': lambda: str((Path.cwd() / 'storage' / 'framework').resolve())
        }
    )

    storage_sessions: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage' / 'framework' / 'sessions').resolve()),
        metadata = {
            'description': 'Directory containing session files.',
            'default': lambda: str((Path.cwd() / 'storage' / 'framework' / 'sessions').resolve())
        }
    )

    storage_cache: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage' / 'framework' / 'cache').resolve()),
        metadata = {
            'description': 'Directory containing framework cache files.',
            'default': lambda: str((Path.cwd() / 'storage' / 'framework' / 'cache').resolve())
        }
    )

    storage_views: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage' / 'framework' / 'views').resolve()),
        metadata = {
            'description': 'Directory containing compiled view files.',
            'default': lambda: str((Path.cwd() / 'storage' / 'framework' / 'views').resolve())
        }
    )

    storage_testing: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage' / 'framework' / 'testing').resolve()),
        metadata = {
            'description': 'Directory containing compiled view files.',
            'default': lambda: str((Path.cwd() / 'storage' / 'framework' / 'testing').resolve())
        }
    )


    def __post_init__(self) -> None:
        super().__post_init__()
        """
        Ensures all path attributes are of type str.

        Raises
        ------
        OrionisIntegrityException
            If any attribute is not a string.
        """
        for field_ in fields(self):
            value = getattr(self, field_.name)
            if not isinstance(value, str):
                raise OrionisIntegrityException(
                    f"Invalid type for '{field_.name}': expected str, got {type(value).__name__}"
                )