_B=None
_A=True
import logging
from alembic import context
from localstack.pro.core.appinspector.database.database import Base
from localstack.pro.core.appinspector.database.models import EventDBModel,SpanDBModel
from localstack.pro.core.appinspector.utils.logger import APPINSPECTOR_LOG,AdapterProcessFilter,_logger
from sqlalchemy import Engine,engine_from_config,pool
from sqlalchemy.engine.base import Connection
target_metadata=Base.metadata
def setup_alembic_logging():
	A=logging.getLogger('alembic')
	if A.handlers:return
	for B in _logger.handlers:A.addHandler(B)
	A.addFilter(AdapterProcessFilter(APPINSPECTOR_LOG));A.setLevel(_logger.level);A.propagate=False
def run_migrations_offline()->_B:
	setup_alembic_logging();A=context.config.get_main_option('sqlalchemy.url');context.configure(url=A,target_metadata=target_metadata,literal_binds=_A,dialect_opts={'paramstyle':'named'},render_as_batch=_A)
	with context.begin_transaction():context.run_migrations()
def do_run_migrations(connection:Connection):
	context.configure(connection=connection,target_metadata=target_metadata,render_as_batch=_A)
	with context.begin_transaction():context.run_migrations()
def run_migrations_online()->_B:
	setup_alembic_logging();A=context.config.attributes.get('connection',_B)
	if A is _B:A=engine_from_config(context.config.get_section(context.config.config_ini_section,{}),prefix='sqlalchemy.',poolclass=pool.NullPool)
	if isinstance(A,Engine):
		with A.connect()as B:do_run_migrations(B)
	else:do_run_migrations(A)
try:
	if context.is_offline_mode():run_migrations_offline()
	else:run_migrations_online()
except Exception as e:APPINSPECTOR_LOG.debug('The AppInspector Alembic env.py file should not be imported directly. Exception: %s',e,exc_info=_A);raise Exception('Error while importing the AppInspector Alembic script. This is expected when creating entrypoints')from e