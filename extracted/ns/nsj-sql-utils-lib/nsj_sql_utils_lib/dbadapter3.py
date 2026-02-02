import re

from sqlalchemy.engine.base import Connection as AlchemyConnection
from sqlalchemy.exc import ResourceClosedError
from sqlparams import SQLParams


class DBAdapter3:
    """
    Adaptador de banco de dados para uso com o Psycopg2.

    Obs.: Esse adapter é simplificado, com relação ao DBAdapter2 e o DBAdapter, mas,
    contém função para execução de instruções SQL multivaloradas.
    """

    def __init__(self, conn):
        self.conn = conn
        self._transaction = None
        self._adapter2_placeholder_pattern = '(?<=[^:a-zA-Z0-9_]):{1}([^ \n,\:)"/=]+)'
        self._adapter2_matcher = re.compile(f".*{self._adapter2_placeholder_pattern}")

    def begin(self):
        if self._transaction is None:
            self.execute("begin")
            self._transaction = True

    def commit(self):
        if self._transaction is not None:
            self.execute("commit")
            self._transaction = None

    def rollback(self):
        if self._transaction is not None:
            self.execute("rollback")
            self._transaction = None

    def in_transaction(self):
        return self._transaction is not None

    def _handle_result(self, cur) -> tuple[int, list[dict[str, any]]]:
        """
        Trata os resultados contidos no cursor, os convertendo para uma
        tupla cm uma lista de dicionários, e o total de linhas no cursor.
        """

        if cur.description is not None:
            lista = []
            item = cur.fetchone()
            while item is not None:
                obj = {}
                for i in range(len(cur.description)):
                    column = cur.description[i]
                    if isinstance(column, tuple):
                        obj[column[0]] = item[i]
                    else:
                        obj[column.name] = item[i]

                lista.append(obj)
                item = cur.fetchone()

            return (cur.rowcount, lista)
        else:
            return (cur.rowcount, [])

    def simple_execute(self, sql) -> tuple[int, list[dict[str, any]]]:
        # Verificando se a query está no padrão do DBAdapter2
        if self._adapter2_matcher.match(sql.replace("\n", " ####### ")):
            sql = self._ajustar_query_adapter2_to3(sql)

        with self.conn.cursor() as cur:
            cur.execute(sql)

            return self._handle_result(cur)

    def execute(self, sql, **kwargs) -> tuple[int, list[dict[str, any]]]:
        """
        Executa uma query (parâmetro sql), que pode ser tanto select, quanto update ou delete,
        retornando uma tupla, onde o primeiro elemento é uma lista de dicionários,
        e a chave de cada dicionário corresponde às colunas da query (se for select),
        e o segundo elemento repesenta o total de linhas no retorno (se for um update
        ou insert, representa o total de linhas impactadas).

        Os parâmetros do comando sql devem ser passados com a sintaxe %(nome)s, no SQL,
        e seus valores devem ser passados como kwargs.
        """

        if not isinstance(self.conn, AlchemyConnection):
            # Verificando se a query está no padrão do DBAdapter2
            if self._adapter2_matcher.match(sql.replace("\n", " ####### ")):
                sql = self._ajustar_query_adapter2_to3(sql)

            with self.conn.cursor() as cur:
                cur.execute(sql, kwargs)

                return self._handle_result(cur)
        else:
            return self._execute_sqlalchemy(sql, **kwargs)

    def _execute_sqlalchemy(self, sql, **kwargs) -> tuple[int, list[dict[str, any]]]:
        sql2, pars2 = self._ajustar_query_sqlalchemy(sql, kwargs)

        cur = None
        try:
            cur = self.conn.execute(sql2, pars2)

            try:
                result = [dict(rec.items()) for rec in cur.fetchall()]
            except ResourceClosedError:
                return (cur.rowcount, [])

            return (cur.rowcount, result)
        finally:
            if cur is not None:
                cur.close()

    def execute_many(
        self, sql, data: list[dict[str, any]]
    ) -> tuple[int, list[dict[str, any]]]:
        """
        Executa uma query N vezes, de acordo com a lista de valores, em dicionários,
        recebidos no parâmetro "data"

        A query normalmente deve ser um insert, update ou delete, e
        retornan uma tupla, onde o primeiro elemento é uma lista de dicionários,
        e a chave de cada dicionário corresponde às colunas da query (se for select),
        e o segundo elemento repesenta o total de linhas no retorno (se for um update
        ou insert, representa o total de linhas impactadas).

        Os parâmetros do comando sql devem ser passados com a sintaxe %(nome)s, no SQL,
        e seus valores devem ser passados nos dicionários contidos na lista data.
        """

        if isinstance(self.conn, AlchemyConnection):
            raise Exception(
                "Execução de SQL com múltiplos valores ainda não suportada para conexões do SQL Alchemy."
            )

        with self.conn.cursor() as cur:
            cur.executemany(sql, data)

            return self._handle_result(cur)

    def _ajustar_query_sqlalchemy(self, sql: str, pars: dict[str, any]):
        sql = re.sub(r"%\(([^\(\)]+)\)s", r":\1", sql)
        return SQLParams("named", "format").format(sql, pars)

    def _ajustar_query_adapter2_to3(self, sql: str):
        sql = re.sub(self._adapter2_placeholder_pattern, r"%(\1)s", sql)
        return sql

    def execute_query_to_model(self, sql: str, model_class: object, **kwargs) -> list:
        """
        Executando uma instrução sql com retorno.

        O retorno é feito em forma de uma lista (list), com elementos do tipo passado pelo parâmetro
        "model_class".

        É importante destacar que para cada coluna do retorno, será procurado um atributo no model_class
        com mesmo nome, para setar o valor. Se este não for encontrado, a coluna do retorno é ignorada.

        Obs.: Esse método foi criado para compatibilidade com o DBAdapter2
        """

        _, lista = self.execute(sql, **kwargs)

        result = []
        for rec in lista:
            model = model_class()

            for key in rec:
                if hasattr(model, key):
                    setattr(model, key, rec[key])

            result.append(model)

        return result
