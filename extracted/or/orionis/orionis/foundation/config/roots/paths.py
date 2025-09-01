from dataclasses import dataclass, field, fields
from pathlib import Path
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.support.entities.base import BaseEntity

@dataclass(frozen=True, kw_only=True)
class Paths(BaseEntity):

    root: str = field(
        default_factory = lambda: str(Path.cwd().resolve()),
        metadata = {
            'description': 'The root directory of the application.',
            'default': lambda: str(Path.cwd().resolve())
        }
    )

    console: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'console').resolve()),
        metadata = {
            'description': 'Directory containing subfolders for console commands and scheduler.py.',
            'default': lambda: str((Path.cwd() / 'app' / 'console').resolve())
        }
    )

    controllers: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'http' / 'controllers').resolve()),
        metadata = {
            'description': 'Directory containing HTTP controller classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'http' / 'controllers').resolve())
        }
    )

    middleware: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'http' / 'middleware').resolve()),
        metadata = {
            'description': 'Directory containing HTTP middleware classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'http' / 'middleware').resolve())
        }
    )

    requests: str = field(
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

    routes: str = field(
        default_factory = lambda: str((Path.cwd() / 'routes').resolve()),
        metadata = {
            'description': 'Path to the web routes definition file.',
            'default': lambda: str((Path.cwd() / 'routes').resolve())
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

    logs: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage' / 'logs').resolve()),
        metadata = {
            'description': 'Directory containing application log files.',
            'default': lambda: str((Path.cwd() / 'storage' / 'logs').resolve())
        }
    )

    framework: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage' / 'framework').resolve()),
        metadata = {
            'description': 'Directory for framework-generated files (cache, sessions, views).',
            'default': lambda: str((Path.cwd() / 'storage' / 'framework').resolve())
        }
    )

    sessions: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage' / 'framework' / 'sessions').resolve()),
        metadata = {
            'description': 'Directory containing session files.',
            'default': lambda: str((Path.cwd() / 'storage' / 'framework' / 'sessions').resolve())
        }
    )

    cache: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage' / 'framework' / 'cache').resolve()),
        metadata = {
            'description': 'Directory containing framework cache files.',
            'default': lambda: str((Path.cwd() / 'storage' / 'framework' / 'cache').resolve())
        }
    )

    views: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage' / 'framework' / 'views').resolve()),
        metadata = {
            'description': 'Directory containing compiled view files.',
            'default': lambda: str((Path.cwd() / 'storage' / 'framework' / 'views').resolve())
        }
    )

    testing: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage' / 'framework' / 'testing').resolve()),
        metadata = {
            'description': 'Directory containing compiled view files.',
            'default': lambda: str((Path.cwd() / 'storage' / 'framework' / 'testing').resolve())
        }
    )

    storage: str = field(
        default_factory = lambda: str((Path.cwd() / 'storage').resolve()),
        metadata = {
            'description': 'Directory for application storage files.',
            'default': lambda: str((Path.cwd() / 'storage').resolve())
        }
    )

    tests : str = field(
        default_factory = lambda: str((Path.cwd() / 'tests').resolve()),
        metadata = {
            'description': 'Directory containing test files.',
            'default': lambda: str((Path.cwd() / 'tests').resolve())
        }
    )

    def __post_init__(self) -> None:
        """
        Post-initialization hook to validate and normalize path attributes.

        This method is called automatically after the dataclass is initialized.
        It ensures that all path-related attributes of the class are stored as strings.
        If any attribute is a `pathlib.Path`, it is converted to a string. If any attribute
        cannot be converted to a string, an `OrionisIntegrityException` is raised.

        Parameters
        ----------
        self : Paths
            The instance of the Paths dataclass.

        Returns
        -------
        None
            This method does not return any value. It modifies the instance in place if necessary.

        Raises
        ------
        OrionisIntegrityException
            If any attribute is not a string after conversion.
        """

        # Call the parent class's __post_init__ if it exists
        super().__post_init__()

        # Iterate over all dataclass fields to validate and normalize their values
        for field_ in fields(self):
            value = getattr(self, field_.name)
            # Convert Path objects to strings
            if isinstance(value, Path):
                object.__setattr__(self, field_.name, str(value))
                value = str(value)
            # Raise an exception if the value is not a string
            if not isinstance(value, str):
                raise OrionisIntegrityException(
                    f"Invalid type for '{field_.name}': expected str, got {type(value).__name__}"
                )
