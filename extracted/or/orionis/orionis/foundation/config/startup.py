from dataclasses import dataclass, field
from orionis.foundation.config.app.entities.app import App
from orionis.foundation.config.auth.entities.auth import Auth
from orionis.foundation.config.cache.entities.cache import Cache
from orionis.foundation.config.cors.entities.cors import Cors
from orionis.foundation.config.database.entities.database import Database
from orionis.foundation.config.roots.paths import Paths
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.foundation.config.filesystems.entitites.filesystems import Filesystems
from orionis.foundation.config.logging.entities.logging import Logging
from orionis.foundation.config.mail.entities.mail import Mail
from orionis.foundation.config.queue.entities.queue import Queue
from orionis.foundation.config.session.entities.session import Session
from orionis.foundation.config.testing.entities.testing import Testing
from orionis.support.entities.base import BaseEntity

@dataclass(unsafe_hash=True, kw_only=True)
class Configuration(BaseEntity):
    """
    Main configuration dataclass for Orionis Framework startup.

    Parameters
    ----------
    app : App or dict, optional
        Application configuration settings.
    auth : Auth or dict, optional
        Authentication configuration settings.
    cache : Cache or dict, optional
        Cache configuration settings.
    cors : Cors or dict, optional
        CORS configuration settings.
    database : Database or dict, optional
        Database configuration settings.
    filesystems : Filesystems or dict, optional
        Filesystem configuration settings.
    logging : Logging or dict, optional
        Logging configuration settings.
    mail : Mail or dict, optional
        Mail configuration settings.
    path : Paths or dict, optional
        Path configuration settings.
    queue : Queue or dict, optional
        Queue configuration settings.
    session : Session or dict, optional
        Session configuration settings.
    testing : Testing or dict, optional
        Testing configuration settings.

    Raises
    ------
    OrionisIntegrityException
        If any configuration section is initialized with an invalid type.
    """

    app : App | dict = field(
        default_factory = lambda: App(),
        metadata = {
            "description": "Application configuration settings.",
            "default": lambda: App().toDict()
        }
    )

    auth : Auth | dict = field(
        default_factory = lambda: Auth(),
        metadata = {
            "description": "Authentication configuration settings.",
            "default": lambda: Auth().toDict()
        }
    )

    cache : Cache | dict = field(
        default_factory = lambda: Cache(),
        metadata = {
            "description": "Cache configuration settings.",
            "default": lambda: Cache().toDict()
        }
    )

    cors : Cors | dict = field(
        default_factory = lambda: Cors(),
        metadata = {
            "description": "CORS configuration settings.",
            "default": lambda: Cors().toDict()
        }
    )

    database : Database | dict = field(
        default_factory = lambda: Database(),
        metadata = {
            "description": "Database configuration settings.",
            "default": lambda: Database().toDict()
        }
    )

    filesystems : Filesystems | dict = field(
        default_factory = lambda: Filesystems(),
        metadata = {
            "description": "Filesystem configuration settings.",
            "default": lambda: Filesystems().toDict()
        }
    )

    logging : Logging | dict = field(
        default_factory = lambda: Logging(),
        metadata = {
            "description": "Logging configuration settings.",
            "default": lambda: Logging().toDict()
        }
    )

    mail : Mail | dict = field(
        default_factory = lambda: Mail(),
        metadata = {
            "description": "Mail configuration settings.",
            "default": lambda: Mail().toDict()
        }
    )

    path : Paths | dict = field(
        default_factory = lambda: Paths(),
        metadata={
            "description": "Path configuration settings.",
            "default": lambda: Paths().toDict()
        }
    )

    queue : Queue | dict = field(
        default_factory = lambda: Queue(),
        metadata = {
            "description": "Queue configuration settings.",
            "default": lambda: Queue().toDict()
        }
    )

    session : Session | dict = field(
        default_factory = lambda: Session(),
        metadata = {
            "description": "Session configuration settings.",
            "default": lambda: Session().toDict()
        }
    )

    testing : Testing | dict = field(
        default_factory = lambda: Testing(),
        metadata = {
            "description": "Testing configuration settings.",
            "default": lambda: Testing().toDict()
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Validates and converts configuration attributes to their respective entity types.

        Raises
        ------
        OrionisIntegrityException
            If any attribute is not an instance of the expected type or a dictionary.
        """

        # Validate `app` attribute
        if not isinstance(self.app, (App, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'app': expected App or dict, got {type(self.app).__name__}"
            )
        if isinstance(self.app, dict):
            self.app = App(**self.app)

        # Validate `auth` attribute
        if not isinstance(self.auth, (Auth, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'auth': expected Auth or dict, got {type(self.auth).__name__}"
            )
        if isinstance(self.auth, dict):
            self.auth = Auth(**self.auth)

        # Validate `cache` attribute
        if not isinstance(self.cache, (Cache, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'cache': expected Cache or dict, got {type(self.cache).__name__}"
            )
        if isinstance(self.cache, dict):
            self.cache = Cache(**self.cache)

        # Validate `cors` attribute
        if not isinstance(self.cors, (Cors, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'cors': expected Cors or dict, got {type(self.cors).__name__}"
            )
        if isinstance(self.cors, dict):
            self.cors = Cors(**self.cors)

        # Validate `database` attribute
        if not isinstance(self.database, (Database, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'database': expected Database or dict, got {type(self.database).__name__}"
            )
        if isinstance(self.database, dict):
            self.database = Database(**self.database)

        # Validate `filesystems` attribute
        if not isinstance(self.filesystems, (Filesystems, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'filesystems': expected Filesystems or dict, got {type(self.filesystems).__name__}"
            )
        if isinstance(self.filesystems, dict):
            self.filesystems = Filesystems(**self.filesystems)

        # Validate `logging` attribute
        if not isinstance(self.logging, (Logging, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'logging': expected Logging or dict, got {type(self.logging).__name__}"
            )
        if isinstance(self.logging, dict):
            self.logging = Logging(**self.logging)

        # Validate `mail` attribute
        if not isinstance(self.mail, (Mail, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'mail': expected Mail or dict, got {type(self.mail).__name__}"
            )
        if isinstance(self.mail, dict):
            self.mail = Mail(**self.mail)

        # Validate `path` attribute
        if not isinstance(self.path, (Paths, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'path': expected Paths or dict, got {type(self.path).__name__}"
            )
        if isinstance(self.path, dict):
            self.path = Paths(**self.path)

        # Validate `queue` attribute
        if not isinstance(self.queue, (Queue, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'queue': expected Queue or dict, got {type(self.queue).__name__}"
            )
        if isinstance(self.queue, dict):
            self.queue = Queue(**self.queue)

        # Validate `session` attribute
        if not isinstance(self.session, (Session, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'session': expected Session or dict, got {type(self.session).__name__}"
            )
        if isinstance(self.session, dict):
            self.session = Session(**self.session)

        # Validate `testing` attribute
        if not isinstance(self.testing, (Testing, dict)):
            raise OrionisIntegrityException(
                f"Invalid type for 'testing': expected Testing or dict, got {type(self.testing).__name__}"
            )
        if isinstance(self.testing, dict):
            self.testing = Testing(**self.testing)