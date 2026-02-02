import hashlib
import logging
import os
import sys

from datetime import datetime

from nsj_sql_utils_lib.dbadapter3 import DBAdapter3

SCRIPT_WRAPPER = """DO 
$$
BEGIN 
{script}
END 
$$;"""

logger = None


def config_logger(grafana_url: str, app_name: str):
    """
    Configures the logger for migration scripts, optionally adding a Loki handler for Grafana integration.

    Args:
        grafana_url (str): The URL for the Grafana Loki logging endpoint. If empty, Loki logging is not configured.
        app_name (str): The application name to use in the logger's name and tags.
    """

    if not app_name:
        app_name = "job_migration"

    # Configurando o logger
    global logger
    logger = logging.getLogger(f"migrations_{app_name}")
    logger.setLevel(logging.INFO)

    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    if grafana_url:
        import logging_loki

        application_name = app_name.replace(" ", "_").lower()
        application_name = application_name.replace("-", "_")

        loki_handler = logging_loki.LokiHandler(
            url=grafana_url,
            tags={f"migrations_{application_name}": "migrations_log"},
            version="1",
        )
        loki_handler.setFormatter(log_format)
        logger.addHandler(loki_handler)


def __create_has_column_function(adapter: DBAdapter3):
    sql = """
    CREATE OR REPLACE FUNCTION public.has_column(schemaname character varying, tablename character varying, columnname character varying)
    RETURNS boolean
    LANGUAGE plpgsql
    AS $function$
    BEGIN
        RETURN EXISTS 
        (
            SELECT
                column_name
            FROM
                information_schema.columns
            WHERE
                LOWER(table_schema)=LOWER(schemaName)
                AND LOWER(table_name)=LOWER(tableName)
                AND LOWER(column_name)=LOWER(columnName)
        );
    END;
    $function$
    ;
    """
    adapter.execute(sql)


def __create_scripts_hashes_table(adapter: DBAdapter3):
    sql = """
    DO $$
    BEGIN
    CREATE TABLE IF NOT EXISTS public.scriptshashes (
        scripthash bigserial NOT NULL,
        arquivo varchar(256) NOT NULL,
        hash varchar(32) NOT NULL,
        dataexecucao timestamp NOT NULL DEFAULT now(),
        CONSTRAINT "PK_scriptshashes" PRIMARY KEY (scripthash)
    );

    IF NOT public.has_column('public', 'scriptshashes', 'origem') THEN
        ALTER TABLE public.scriptshashes ADD COLUMN origem smallint DEFAULT 0;
        COMMENT ON COLUMN public.scriptshashes.origem IS '0 - Instalador; 1 - FastUpdate';
    END IF;

    IF NOT public.has_column('public', 'scriptshashes', 'solicitante') THEN
        ALTER TABLE public.scriptshashes ADD COLUMN solicitante varchar(256);
    END IF;

    IF NOT public.has_column('public', 'scriptsversoes', 'origem') THEN
        ALTER TABLE public.scriptsversoes ADD COLUMN origem smallint DEFAULT 0;
        COMMENT ON COLUMN public.scriptsversoes.origem IS '0 - Instalador; 1 - FastUpdate';
    END IF;

    IF NOT public.has_column('public', 'scriptsversoes', 'solicitante') THEN
        ALTER TABLE public.scriptsversoes ADD COLUMN solicitante varchar(256);
    END IF;

    END$$;
    """
    adapter.execute(sql)
    logger.info("Making sure if table public.scriptshashes is created")


def __create_scripts_versoes_table(adapter: DBAdapter3):
    sql = """
    DO $$
    BEGIN
    CREATE TABLE if not exists public.scriptsversoes (
        scriptversao bigserial NOT NULL,
        arquivo varchar(256) NOT NULL,
        dataexecucao timestamp NOT NULL DEFAULT now(),
        CONSTRAINT "PK_scriptsversoes" PRIMARY KEY (scriptversao),
        CONSTRAINT "UK_scriptsversoes" UNIQUE (arquivo) DEFERRABLE
    );
    CREATE INDEX  IF NOT EXISTS idx_scripts_versoes_arquivo ON public.scriptsversoes USING btree (arquivo);

    END$$;
    """
    adapter.execute(sql)
    logger.info("Making sure if table public.scriptsversoes is created")


def __run_migration(adapter: DBAdapter3, filepath, function=False):

    with open(filepath) as file:
        file_contents = file.read()
        if len(file_contents.strip()) == 0:
            logger.info(
                f"Ignoring migration (Empty file): {os.path.basename(file.name)}"
            )
            return
        logger.info(f"Running migration: {os.path.basename(file.name)}")
        prepared_query = (
            SCRIPT_WRAPPER.format(script=file_contents)
            if not function
            else file_contents
        )
        adapter.simple_execute(prepared_query)


def __register_migration_in_db(adapter: DBAdapter3, filename: str, hash=None):
    # É necessário fazer encode e decode do filename da mesma maneira que o instalador faz, pra manter a compatibilidade entre
    # as duas formas de atualização
    # O shell do windows usa, por padrão, o code page 850. Portando, o nome do arquivo está nessa codificação
    # porém, ao criar o arquivo .sql de atualização, cria usando o code page 1252
    # dessa forma, "filename.encode("cp850").decode("cp1252")" é equivalente a
    # "filename >> update.sql" no shell do windows
    # Origem = 0 -> Instalador
    # Origem = 1 -> FastUpdate
    if hash is not None:
        sql = f"insert into public.scriptshashes(arquivo, hash) values ('{filename}', '{hash}');"
    else:
        sql = f"insert into public.scriptsversoes(arquivo) values ('{filename}');"
    log_msg = f"Registering migration in database: {filename}"
    if hash is not None:
        log_msg += f" - with hash: {hash}"
    logger.info(log_msg)
    adapter.execute(sql)


def __get_file_hash(filepath: str):
    with open(filepath) as file:
        file_hash = hashlib.md5(file.read().encode()).hexdigest()
    return file_hash


def __get_all_migrations(adapter: DBAdapter3):
    sql = "select arquivo from scriptsversoes;"
    _, response = adapter.execute(sql)
    return [migration["arquivo"] for migration in response]


def __get_all_hashes(adapter: DBAdapter3):
    sql = "select hash from scriptshashes;"
    _, response = adapter.execute(sql)
    return [migration["hash"] for migration in response]


def __key_migrations(item):
    return item[1]


def run_update(
    adapter: DBAdapter3,
    version: str,
    database_path: str,
    grafana_url: str,
    app_name: str,
):
    config_logger(grafana_url, app_name)

    try:
        logger.info("Starting...")
        logger.info(f"Version: {version}")

        # Creating tables
        __create_has_column_function(adapter)
        __create_scripts_versoes_table(adapter)
        __create_scripts_hashes_table(adapter)

        # Scripts
        repository_root = os.path.join(database_path)
        scripts_path = os.path.join(repository_root, "scripts")
        migrations = __get_all_migrations(adapter)
        por_executar = []

        if os.path.exists(scripts_path):
            for filename in os.listdir(scripts_path):
                relative_file_path = os.path.join(scripts_path, filename)
                if os.path.isfile(relative_file_path):
                    if filename not in migrations and filename.endswith(".sql"):
                        por_executar.append((relative_file_path, filename))
            logger.info("Sorting Scripts")
            por_executar.sort(key=__key_migrations)
            logger.info("Executing Scripts")

        else:
            logger.warning("Scripts Directory not Exists")

        for item in por_executar:
            relative_file_path, filename = item
            try:
                adapter.begin()
                __run_migration(adapter, relative_file_path)
                __register_migration_in_db(adapter, filename)
                adapter.commit()
            except Exception as e:
                logger.exception(
                    f"Erro ao rodar migration: {filename}", stack_info=True
                )
                adapter.rollback()
                raise e

        por_executar_functions = []
        por_executar_views = []
        logger.info("Returning hashes")
        hashes = __get_all_hashes(adapter)

        # Pasta functions
        function_files_path = os.path.join(repository_root, "functions")
        if os.path.exists(function_files_path):
            logger.info("Sorting functions")
            for filename in os.listdir(function_files_path):
                relative_file_path = os.path.join(function_files_path, filename)
                if os.path.isfile(relative_file_path) and relative_file_path.endswith(
                    ".sql"
                ):
                    if __get_file_hash(relative_file_path) not in hashes:
                        por_executar_functions.append((relative_file_path, filename))
            por_executar_functions.sort(key=__key_migrations)
            logger.info("Executing functions")
        else:
            logger.warning("Functions directory not Exists")

        # Executing functions
        for item in por_executar_functions:
            relative_file_path, filename = item
            try:
                adapter.begin()
                __run_migration(adapter, relative_file_path, function=True)
                __register_migration_in_db(
                    adapter, filename, hash=__get_file_hash(relative_file_path)
                )
                adapter.commit()
            except Exception as e:
                logger.exception(f"Erro ao rodar function: {filename}", stack_info=True)
                adapter.rollback()
                raise e

        # Pasta views
        views_files_path = os.path.join(repository_root, "views")
        if os.path.exists(views_files_path):
            logger.info("Sorting views")
            for filename in os.listdir(views_files_path):
                relative_file_path = os.path.join(views_files_path, filename)
                if os.path.isfile(relative_file_path) and relative_file_path.endswith(
                    ".sql"
                ):
                    if __get_file_hash(relative_file_path) not in hashes:
                        por_executar_views.append((relative_file_path, filename))

            por_executar_views.sort(key=__key_migrations)
            logger.info("Executing views")
        else:
            logger.warning("Views directory not Exists")

        # Executing views
        for item in por_executar_views:
            relative_file_path, filename = item
            try:
                adapter.begin()
                __run_migration(adapter, relative_file_path)
                __register_migration_in_db(
                    adapter, filename, hash=__get_file_hash(relative_file_path)
                )
                adapter.commit()
            except Exception as e:
                logger.exception(f"Erro ao rodar view: {filename}", stack_info=True)
                adapter.rollback()
                raise e

        logger.info("End.")
    except Exception as e:
        logger.exception(f"Erro desconhecido", stack_info=True)
        raise e
