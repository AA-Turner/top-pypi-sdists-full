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

    app: str = field(
        default_factory = lambda: str((Path.cwd() / 'app').resolve()),
        metadata = {
            'description': 'The main application directory containing core code.',
            'default': lambda: str((Path.cwd() / 'app').resolve())
        }
    )

    console: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'console').resolve()),
        metadata = {
            'description': 'Directory containing subfolders for console commands and scheduler.py.',
            'default': lambda: str((Path.cwd() / 'app' / 'console').resolve())
        }
    )

    exceptions: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'exceptions').resolve()),
        metadata = {
            'description': 'Directory containing exception handler classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'exceptions').resolve())
        }
    )

    http: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'http').resolve()),
        metadata = {
            'description': 'Directory containing HTTP-related classes (controllers, middleware, requests).',
            'default': lambda: str((Path.cwd() / 'app' / 'http').resolve())
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

    notifications: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'notifications').resolve()),
        metadata = {
            'description': 'Directory containing notification classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'notifications').resolve())
        }
    )

    services: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'services').resolve()),
        metadata = {
            'description': 'Directory containing business logic service classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'services').resolve())
        }
    )

    jobs: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'jobs').resolve()),
        metadata = {
            'description': 'Directory containing queued job classes.',
            'default': lambda: str((Path.cwd() / 'app' / 'jobs').resolve())
        }
    )

    bootstrap: str = field(
        default_factory = lambda: str((Path.cwd() / 'app' / 'bootstrap').resolve()),
        metadata = {
            'description': 'Directory containing application bootstrap files.',
            'default': lambda: str((Path.cwd() / 'app' / 'bootstrap').resolve())
        }
    )

    config: str = field(
        default_factory = lambda: str((Path.cwd() / 'config').resolve()),
        metadata = {
            'description': 'Directory containing application configuration files.',
            'default': lambda: str((Path.cwd() / 'config').resolve())
        }
    )

    database: str = field(
        default_factory = lambda: str((Path.cwd() / 'database' / 'database').resolve()),
        metadata = {
            'description': 'Directory containing the SQLite database file.',
            'default': lambda: str((Path.cwd() / 'database' / 'database').resolve())
        }
    )

    resources: str = field(
        default_factory = lambda: str((Path.cwd() / 'resources').resolve()),
        metadata = {
            'description': 'Directory containing application resources (views, lang, assets).',
            'default': lambda: str((Path.cwd() / 'resources').resolve())
        }
    )

    routes: str = field(
        default_factory = lambda: str((Path.cwd() / 'routes').resolve()),
        metadata = {
            'description': 'Path to the web routes definition file.',
            'default': lambda: str((Path.cwd() / 'routes').resolve())
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

            # Get the current value of the field
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
