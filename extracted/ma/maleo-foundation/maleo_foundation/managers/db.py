import os
from contextlib import contextmanager
from pydantic import BaseModel, Field
from sqlalchemy import MetaData, text
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator
from maleo_foundation.types import BaseTypes
from maleo_foundation.utils.logging import ServiceLogger

class MetadataManager:
    Base: DeclarativeMeta = declarative_base()
    metadata: MetaData = Base.metadata

class SessionManager:
    def __init__(
        self,
        logger: ServiceLogger,
        engine: Engine
    ):
        self._logger = logger
        self._logger.info("Initializing SessionMaker")
        self._sessionmaker:sessionmaker[Session] = sessionmaker(
            bind=engine,
            expire_on_commit=False
        )
        self._logger.info("SessionMaker initialized successfully")

    def _session_handler(self) -> Generator[Session, None, None]:
        """Reusable function for managing database sessions."""
        session = self._sessionmaker()
        self._logger.debug("New database session created.")
        try:
            yield session  #* Provide session
            session.commit()  #* Auto-commit on success
        except SQLAlchemyError as e:
            session.rollback()  #* Rollback on error
            self._logger.error(f"[SQLAlchemyError] Database transaction failed: {e}", exc_info=True)
            raise
        except Exception as e:
            session.rollback()  #* Rollback on error
            self._logger.error(f"[Exception] Database transaction failed: {e}", exc_info=True)
            raise
        finally:
            session.close()  #* Ensure session closes
            self._logger.debug("Database session closed.")

    def inject(self) -> Generator[Session, None, None]:
        """Returns a generator that yields a SQLAlchemy session for dependency injection."""
        return self._session_handler()

    @contextmanager
    def get(self) -> Generator[Session, None, None]:
        """Context manager for manual session handling. Supports `with SessionManager.get() as session:`"""
        yield from self._session_handler()

    def dispose(self) -> None:
        """Dispose of the sessionmaker and release any resources."""
        if self._sessionmaker is not None:
            self._sessionmaker.close_all()
            self._sessionmaker = None

        self._logger.info("SessionManager disposed successfully")
        self._logger = None

class DatabaseConfigurations(BaseModel):
    username: str = Field("postgres", description="Database user's username")
    password: str = Field(..., description="Database user's password")
    host: str = Field(..., description="Database's host")
    port: int = Field(5432, description="Database's port")
    database: str = Field(..., description="Database")

    @property
    def url(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

class DatabaseManager:
    def __init__(
        self,
        metadata: MetaData,
        logger: ServiceLogger,
        url: BaseTypes.OptionalString = None
    ):
        self._metadata = metadata #* Define database metadata
        self._logger = logger #* Define database logger

        #* Create engine
        url = url or os.getenv("DB_URL")
        if url is None:
            raise ValueError("DB_URL environment variable must be set if url is not provided")
        self._logger.info("Creating SQlAlchemy engine")
        self._engine = create_engine(
            url=url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600)
        self._logger.info("SQlAlchemy engine created successfully")

        #* Creating all table from metadata
        self._logger.info("Creating all tables defined in metadata")
        self._metadata.create_all(bind=self._engine) #* Create all tables
        self._logger.info("Created all tables defined in metadata")

        #* Initializing session manager
        self._logger.info("Initializing session manager")
        #* Create session
        self._session = SessionManager(
            logger=self._logger,
            engine=self._engine
        )
        self._logger.info("Session manager initialized successfully")

    @property
    def metadata(self) -> MetaData:
        return self._metadata

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def session(self) -> SessionManager:
        return self._session

    def check_connection(self) -> bool:
        """Check database connectivity by executing a simple query."""
        self._logger.info("Checking database connectivity...")
        try:
            with self._session.get() as session:
                session.execute(text("SELECT 1"))
            self._logger.info("Database connectivity check successful.")
            return True
        except SQLAlchemyError as se:
            self._logger.error(f"Database connectivity check failed: {se}", exc_info=True)
            return False
        except Exception as e:
            self._logger.error(f"Unexpected error during connectivity check: {e}", exc_info=True)
            return False

    def dispose(self) -> None:
        #* Dispose session
        if self._session is not None:
            self._logger.info("Disposing Session Manager")
            self._session.dispose()
            self._session = None
        #* Dispose engine
        if self._engine is not None:
            self._logger.info("Disposing Engine Manager")
            self._engine.dispose()
            self._engine = None
            self._logger.info("Engine Manager disposed successfully")
        #* Dispose metadata
        if self._metadata is not None:
            self._logger.info("Disposing DB Metadata")
            self._metadata = None
            self._logger.info("DB Metadata diposed succesfully")