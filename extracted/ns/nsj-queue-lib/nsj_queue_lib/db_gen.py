import sys

DATABASE_TEMPLATE = """
-- Tabela de controle da fila
create table #SCHEMA.#NOME_FILA (
    id bigserial primary key,
    id_inicial int8,
    data_hora_inicial timestamp with time zone default clock_timestamp(),
    data_hora timestamp with time zone default clock_timestamp(),
    origem varchar(150),
    destino varchar(150),
    processo varchar(250),
    chave_externa varchar(100),
    proxima_tentativa timestamp with time zone,
    tentativa int default 1,
    status varchar(100) default 'pendente',
    reenfileirado boolean default false,
    estouro_tentativas boolean default false,
    mensagem varchar(500),
    id_anterior int8,
    data_hora_anterior timestamp with time zone,
    status_anterior varchar(100),
    mensagem_anterior varchar(500),
    payload text,
    tenant int8,
    grupo_empresarial varchar(40),
    payload_hash bytea,
    pub_sub boolean default false not null,
    publication_id int8,
    subscriber_id varchar(100),
    dead boolean default False not null,
    live_id int8,
    prioridade int default 50
);

-- Índices da tabela de fila
create index "idx_#NOME_FILA_status" on #SCHEMA.#NOME_FILA (status);
create index "idx_#NOME_FILA_status_tentativa_data_hora" on #SCHEMA.#NOME_FILA (status, tentativa, data_hora);
create index "idx_#NOME_FILA_data_hora" on #SCHEMA.#NOME_FILA (data_hora);
create index "idx_#NOME_FILA_chave_externa_payload_hash_status" on #SCHEMA.#NOME_FILA (chave_externa, payload_hash, status);

-- Trigger para notificar inserções na fila
CREATE OR REPLACE FUNCTION #SCHEMA.notify_#NOME_FILA_insert()
RETURNS TRIGGER AS $$
DECLARE
    channel_name text := '#NOME_FILA';
BEGIN
    PERFORM pg_notify(channel_name, '');
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_insert_#NOME_FILA
AFTER INSERT ON #SCHEMA.#NOME_FILA
FOR EACH ROW
WHEN (NEW.data_hora <= clock_timestamp() and NEW.status <> 'agendada')
EXECUTE FUNCTION #SCHEMA.notify_#NOME_FILA_insert();

-- Tabela de assinaturas, para o caso de uso pub_sub
create table #SCHEMA.#NOME_FILA_subscriber(
	id varchar(100) NOT NULL PRIMARY KEY,
	tenant int8,
	grupo_empresarial varchar(40),
	processo varchar(250) NOT NULL,
	url VARCHAR(2048),
	http_method VARCHAR(8),
	headers json,
	ativo boolean not null default true,
	created_at timestamp with time zone not null default now()
);
create index "idx_#NOME_FILA_subscriber_tenant_grupo_empresarial_processo" on #SCHEMA.#NOME_FILA_subscriber (tenant, grupo_empresarial, processo);
"""


def main(schema: str, nome_fila: str):
    script = DATABASE_TEMPLATE.replace("#SCHEMA", schema)
    script = script.replace("#NOME_FILA", nome_fila)

    print(script)
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print(
            """Faltando parâmetros do schema, e do nome da fila. Modo de uso:
python -m nsj_queue_lib.db_gen <schema> <nome_fila>

Parêmetros adicionais serão ignorados."""
        )
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
