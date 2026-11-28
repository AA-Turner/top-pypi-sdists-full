"""The tables and views of Core's database.

Three kinds of table. What the operator saved (wrappers). What the wrappers published, kept exactly as it was
published (wrapper_documents, wrapper_log): a document or a row is stored whole, as JSON, so a column a newer
wrapper adds is kept without a change here and nothing a wrapper said is lost. And what Core asks of the models:
the grading table (grading_queries), and the rounds of grading calls somebody asked for (grading_rounds).

Everything else is a view over those: the name a thing is read by (calls, loads, models, cards, grades ...) and
the columns it has are defined once, here, by the database itself. Nothing in Python re-derives them. What came of
a grading call is not kept anywhere of its own: it is the call's row of the call log, found by its marker.
"""

TABLES = (
    # the saved connections: one row a wrapper, by the name it gives itself. key is its API key (a linked
    # wrapper's link secret) and is never published
    """CREATE TABLE IF NOT EXISTS wrappers (
        name TEXT PRIMARY KEY,
        url TEXT NOT NULL,
        key TEXT NOT NULL DEFAULT '',
        link INTEGER NOT NULL DEFAULT 0,
        connected INTEGER NOT NULL DEFAULT 1,
        added_at REAL NOT NULL,
        changed_at REAL NOT NULL,
        added_by TEXT)""",
    # what the operator said of routing to a wrapper (wrappers/registry.py wildcard): a row only where it was said.
    # Wildcard allows routing a model without an allocation when the wrapper reports it can run.
    """CREATE TABLE IF NOT EXISTS wrapper_routing (
        name TEXT PRIMARY KEY,
        wildcard INTEGER NOT NULL,
        changed_at REAL NOT NULL,
        changed_by TEXT)""",
    """CREATE TABLE IF NOT EXISTS wrapper_model_routes (
        wrapper TEXT NOT NULL,
        model TEXT NOT NULL,
        explicit INTEGER NOT NULL DEFAULT 0,
        pinned INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (wrapper, model))""",
    """CREATE TABLE IF NOT EXISTS wrapper_model_blocks (
        wrapper TEXT NOT NULL,
        model TEXT NOT NULL,
        PRIMARY KEY (wrapper, model))""",
    """CREATE TABLE IF NOT EXISTS wrapper_model_static (
        wrapper TEXT NOT NULL,
        model TEXT NOT NULL,
        enabled INTEGER NOT NULL,
        PRIMARY KEY (wrapper, model))""",
    """CREATE TABLE IF NOT EXISTS wrapper_context_edits (
        wrapper TEXT NOT NULL,
        model TEXT NOT NULL,
        patch TEXT NOT NULL,
        PRIMARY KEY (wrapper, model))""",
    # the keys Core gave out (keys/keys.py): what is kept of one is its digest and its first characters, never it
    """CREATE TABLE IF NOT EXISTS api_keys (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        kind TEXT NOT NULL,
        prefix TEXT NOT NULL,
        digest TEXT NOT NULL UNIQUE,
        created_at REAL NOT NULL,
        created_by TEXT,
        expires_at REAL,
        last_used_at REAL)""",
    # how the collector stands with each wrapper: the store it reads, the last read, the last failure
    """CREATE TABLE IF NOT EXISTS collector (
        wrapper TEXT PRIMARY KEY,
        store_id TEXT,
        changes INTEGER,
        read_at REAL,
        error TEXT,
        error_at REAL)""",
    # what a wrapper publishes whole, as it last published it: health, state, models, units, drives. read_at is
    # when this content was read: a document that reads the same again is not written again
    """CREATE TABLE IF NOT EXISTS wrapper_documents (
        wrapper TEXT NOT NULL,
        name TEXT NOT NULL,
        document TEXT NOT NULL,
        read_at REAL NOT NULL,
        PRIMARY KEY (wrapper, name))""",
    # the rows of a wrapper's logs (call_log, load_runs, call_stages), each as it published it. A wrapper's
    # database has an identity (store_id): the rows of one that was replaced stay, apart
    """CREATE TABLE IF NOT EXISTS wrapper_log (
        wrapper TEXT NOT NULL,
        store_id TEXT NOT NULL,
        log TEXT NOT NULL,
        id INTEGER NOT NULL,
        row TEXT NOT NULL,
        PRIMARY KEY (wrapper, store_id, log, id))""",
    "CREATE INDEX IF NOT EXISTS wrapper_log_received ON wrapper_log (log, json_extract(row, '$.received_at'))",
    "CREATE INDEX IF NOT EXISTS wrapper_log_request ON wrapper_log (log, json_extract(row, '$.request_id'))",
    # the calls made with a grading marker, by their query: what the grading views read
    """CREATE INDEX IF NOT EXISTS wrapper_log_graded ON wrapper_log
        (json_extract(row, '$.request_body.metadata.grading.query'), wrapper)
        WHERE log = 'call_log' AND json_extract(row, '$.request_body.metadata.grading.query') IS NOT NULL""",
    # the grading table: what a model is asked, by the task it serves (and its engine, when a query is only for
    # one), in tiers. A model's schedule is the queries of its task, tier by tier (the view grading_schedule).
    # body is the call's body without its model; checks is how the answer is checked ([[check, expected], ...],
    # the checks of hugpy_resources answer_checks); answer is a right answer in words, for a person reading a
    # grade. A row whose changed_at is NULL is the code's own (grading/queries.py) and follows it; one the
    # operator changed is theirs and is left as it is
    """CREATE TABLE IF NOT EXISTS grading_queries (
        id TEXT PRIMARY KEY,
        suite TEXT NOT NULL,
        task TEXT NOT NULL,
        engine TEXT,
        category TEXT NOT NULL,
        tier INTEGER NOT NULL,
        position INTEGER NOT NULL,
        endpoint TEXT NOT NULL,
        body TEXT NOT NULL,
        checks TEXT NOT NULL,
        answer TEXT,
        changed_at REAL,
        changed_by TEXT)""",
    # a round: a mass shot of grading calls somebody asked for (a test fire of a wrapper; a grading of chosen
    # models). What was asked, the calls it set out to make and what it left out, with why, are kept here, and
    # so is what a wrapper's door turned away before it reached that wrapper's call log. What came of every
    # other call is the call log's: a call names its round in its marker
    """CREATE TABLE IF NOT EXISTS grading_rounds (
        id TEXT PRIMARY KEY,
        kind TEXT NOT NULL,
        wrappers TEXT NOT NULL,
        asked TEXT NOT NULL,
        plan TEXT NOT NULL,
        skipped TEXT NOT NULL,
        refused TEXT NOT NULL DEFAULT '[]',
        started_at REAL NOT NULL,
        ended_at REAL,
        ended_why TEXT,
        asked_by TEXT)""",
)

# a view is dropped and made again at every start: its definition is this file's
VIEWS = {
    # ── the wrappers, each with how it stands ──
    'wrapper_status': """
        SELECT w.name, w.url, w.link, w.connected, w.added_at, w.changed_at,
               json_extract(h.document, '$.version') AS version,
               json_extract(h.document, '$.status') AS status,
               json_extract(h.document, '$.reasons') AS reasons,
               json_extract(s.document, '$.presence.alive_at') AS alive_at,
               json_extract(s.document, '$.presence.stale_after_s') AS stale_after_s,
               json_extract(s.document, '$.presence.doing') AS doing,
               c.store_id, c.read_at, c.error, c.error_at,
               -- reachable: the one answer to "can this wrapper be asked now": the operator has it connected and
               -- the collector's last read of it succeeded and is recent (a wrapper holds a read at most a minute)
               CASE WHEN w.connected = 1 AND c.error IS NULL AND c.read_at IS NOT NULL
                         AND unixepoch() - c.read_at <= 90 THEN 1 ELSE 0 END AS reachable,
               -- wildcard: whether Core's own choice of a host may take it (wrapper_routing; 1 when nothing was said)
               COALESCE(r.wildcard, 1) AS wildcard
        FROM wrappers w
        LEFT JOIN wrapper_documents h ON h.wrapper = w.name AND h.name = 'health'
        LEFT JOIN wrapper_documents s ON s.wrapper = w.name AND s.name = 'state'
        LEFT JOIN collector c ON c.wrapper = w.name
        LEFT JOIN wrapper_routing r ON r.name = w.name""",
    # ── the call log of every wrapper, one row a call ──
    'calls': """
        SELECT wrapper, store_id, id,
               json_extract(row, '$.request_id') AS request_id,
               json_extract(row, '$.model_name') AS model,
               json_extract(row, '$.endpoint') AS endpoint,
               json_extract(row, '$.task') AS task,
               json_extract(row, '$.call_state') AS state,
               json_extract(row, '$.http_status') AS http_status,
               json_extract(row, '$.received_at') AS received_at,
               json_extract(row, '$.inference_started_at') AS started_at,
               json_extract(row, '$.responded_at') AS responded_at,
               json_extract(row, '$.load_s') AS load_s,
               json_extract(row, '$.prompt_tokens') AS prompt_tokens,
               json_extract(row, '$.completion_tokens') AS completion_tokens,
               json_extract(row, '$.predicted_ms') AS predicted_ms,
               -- the grading marker a call was made with (its body's metadata.grading.query): what associates
               -- the call, and so its answer, with a grading query. NULL for any other call
               json_extract(row, '$.request_body.metadata.grading.query') AS grading_query,
               -- the round of grading calls it was made in (a test fire, a grading of chosen models), if any
               json_extract(row, '$.request_body.metadata.grading.round') AS grading_round,
               json_extract(row, '$.error') AS error,
               row
        FROM wrapper_log WHERE log = 'call_log'""",
    # ── grading: reads of the call log by its marker ──
    # every call made with a grading marker, with the query it was made for (suite is NULL when the marker names
    # a query the table does not have). nth is 1 for the newest call of its model on its query among those that
    # were answered, and among those that were not
    'graded_calls': """
        SELECT c.wrapper, c.store_id, c.id, c.request_id, c.model, c.endpoint, c.state, c.http_status,
               c.received_at, c.started_at, c.responded_at, c.load_s, c.prompt_tokens, c.completion_tokens,
               c.predicted_ms, c.error, c.grading_query AS query, c.grading_round AS round,
               q.suite, q.task, q.category, q.tier, q.position, q.checks, q.answer, q.body,
               json_extract(c.row, '$.response_body') AS reply,
               row_number() OVER (PARTITION BY c.wrapper, c.model, c.grading_query, c.state = 'done'
                                  ORDER BY c.received_at DESC, c.id DESC) AS nth
        FROM calls c LEFT JOIN grading_queries q ON q.id = c.grading_query
        WHERE c.grading_query IS NOT NULL""",
    # what a model's grade on a query is read from: the newest call of the model on the query that was answered.
    # Whether the answer passes is the query's checks applied to reply (grading/read.py): it is worked out when
    # asked, so a query whose checks were changed regrades every answer it ever had
    'grades': """
        SELECT * FROM graded_calls WHERE state = 'done' AND nth = 1 AND suite IS NOT NULL""",
    # every model's schedule: the queries of its task that are called on the route its engine serves, each with
    # the call that graded it (request_id) or how many calls for it its wrapper still holds (asking). A query
    # with neither has not been performed
    'grading_schedule': """
        SELECT m.wrapper, m.id AS model, m.task, m.engine, q.id AS query, q.suite, q.category, q.tier, q.position,
               q.endpoint, g.request_id, g.received_at AS graded_at, coalesce(o.asking, 0) AS asking
        FROM models m
        JOIN engines e ON e.wrapper = m.wrapper AND e.engine = m.engine
        JOIN grading_queries q ON q.task = m.task AND q.endpoint = e.endpoint AND (q.engine IS NULL OR q.engine = m.engine)
        LEFT JOIN grades g ON g.wrapper = m.wrapper AND g.model = m.id AND g.query = q.id
        LEFT JOIN (SELECT wrapper, model, grading_query, count(*) AS asking FROM calls
                   WHERE grading_query IS NOT NULL AND (state IS NULL OR state IN ('pending', 'running'))
                   GROUP BY wrapper, model, grading_query) o
               ON o.wrapper = m.wrapper AND o.model = m.id AND o.grading_query = q.id""",
    # the suites of the grading table: each grades the models of one task
    'grading_suites': """
        SELECT suite AS name, min(task) AS task, count(DISTINCT category) AS categories, max(tier) AS tiers,
               count(*) AS queries
        FROM grading_queries GROUP BY suite""",
    # ── what the call log says of each model on each wrapper: its calls, its tokens over its generating time ──
    'model_calls': """
        SELECT wrapper, model, max(task) AS task, count(*) AS calls,
               sum(state = 'done') AS answered, sum(state = 'failed') AS failed, sum(state = 'cancelled') AS cancelled,
               sum(CASE WHEN state = 'done' AND completion_tokens > 1 AND predicted_ms > 0 THEN 1 ELSE 0 END) AS rated,
               sum(CASE WHEN state = 'done' AND completion_tokens > 1 AND predicted_ms > 0 THEN completion_tokens END) AS tokens,
               sum(CASE WHEN state = 'done' AND completion_tokens > 1 AND predicted_ms > 0 THEN predicted_ms END) / 1000.0 AS seconds,
               avg(CASE WHEN state = 'done' THEN responded_at - received_at END) AS mean_s_per_call,
               avg(load_s) AS mean_load_s, sum(load_s IS NOT NULL) AS loads,
               min(received_at) AS first_call_at, max(received_at) AS last_call_at
        FROM calls WHERE model IS NOT NULL AND endpoint != '/v1/load'
        GROUP BY wrapper, model""",
    'loads': """
        SELECT wrapper, store_id, id,
               json_extract(row, '$.load_id') AS load_id,
               json_extract(row, '$.model_key') AS model,
               json_extract(row, '$.engine') AS engine,
               json_extract(row, '$.placement') AS placement,
               json_extract(row, '$.staged_at') AS staged_at,
               json_extract(row, '$.ready_at') AS ready_at,
               json_extract(row, '$.ended_at') AS ended_at,
               json_extract(row, '$.outcome') AS outcome,
               json_extract(row, '$.end_reason') AS end_reason,
               json_extract(row, '$.vram_bytes') AS vram_bytes,
               row
        FROM wrapper_log WHERE log = 'load_runs'""",
    'call_stages': """
        SELECT wrapper, store_id, id,
               json_extract(row, '$.request_id') AS request_id,
               json_extract(row, '$.stage') AS stage,
               json_extract(row, '$.started_at') AS started_at,
               json_extract(row, '$.finished_at') AS finished_at,
               json_extract(row, '$.predicted_s') AS predicted_s,
               json_extract(row, '$.note') AS note
        FROM wrapper_log WHERE log = 'call_stages'""",
    # ── the models: what each wrapper can serve (its own verdicts), and what its Discovery has recorded ──
    'models': """
        SELECT d.wrapper, json_extract(m.value, '$.id') AS id,
               json_extract(m.value, '$.hub_id') AS model_key,
               json_extract(m.value, '$.owned_by') AS engine,
               json_extract(m.value, '$.primary_task') AS task,
               json_extract(m.value, '$.weight_bytes') AS weight_bytes,
               json_extract(m.value, '$.resident') AS resident,
               json_extract(m.value, '$.accommodated') AS accommodated,
               json_extract(m.value, '$.selectable') AS selectable,
               json_extract(m.value, '$.possible') AS possible,
               COALESCE(json_extract(m.value, '$.offered'), json_extract(m.value, '$.selectable')) AS offered,
               json_extract(m.value, '$.env_status') AS env_status,
               CASE WHEN json_type(m.value, '$.endpoints') = 'array' THEN json_extract(m.value, '$.endpoints')
                    ELSE (SELECT json_group_array(DISTINCT e.endpoint) FROM engines e
                          WHERE e.wrapper = d.wrapper AND e.engine = json_extract(m.value, '$.owned_by')
                            AND e.endpoint IS NOT NULL) END AS endpoints,
               d.read_at, m.value AS row
        FROM wrapper_documents d, json_each(d.document, '$.data') m WHERE d.name = 'models'""",
    # the engines of each wrapper: the route each is called on and the tasks it serves
    'engines': """
        SELECT d.wrapper, json_extract(e.value, '$.engine') AS engine,
               json_extract(e.value, '$.endpoint') AS endpoint,
               json_extract(e.value, '$.tasks') AS tasks,
               json_extract(e.value, '$.counts_tokens') AS counts_tokens
        FROM wrapper_documents d, json_each(d.document, '$.engines') e WHERE d.name = 'state'""",
    'units': """
        SELECT d.wrapper, json_extract(u.value, '$.key') AS model_key,
               json_extract(u.value, '$.variation') AS variation,
               json_extract(u.value, '$.bytes') AS bytes,
               json_extract(u.value, '$.engine') AS engine,
               json_extract(u.value, '$.task') AS task,
               json_extract(u.value, '$.content_id') AS content_id,
               json_extract(u.value, '$.source_role') AS source_role,
               json_extract(u.value, '$.arch') AS arch,
               json_extract(u.value, '$.ctx_train') AS ctx_train,
               d.read_at, u.value AS row
        FROM wrapper_documents d, json_each(d.document, '$.units') u WHERE d.name = 'units'""",
    'drives': """
        SELECT d.wrapper, json_extract(v.value, '$.path') AS path,
               json_extract(v.value, '$.role') AS role,
               json_extract(v.value, '$.total') AS total,
               json_extract(v.value, '$.free') AS free,
               json_extract(v.value, '$.room') AS room,
               json_extract(v.value, '$.models') AS models,
               json_extract(v.value, '$.read_bytes_per_s') AS read_bytes_per_s,
               json_extract(v.value, '$.write_bytes_per_s') AS write_bytes_per_s,
               d.read_at, v.value AS row
        FROM wrapper_documents d, json_each(d.document, '$.drives') v WHERE d.name = 'drives'""",
    # ── each host now: its cards, its memory, what is loaded ──
    'cards': """
        SELECT d.wrapper, json_extract(g.value, '$.device') AS device,
               json_extract(g.value, '$.name') AS name,
               json_extract(g.value, '$.total') AS total,
               json_extract(g.value, '$.used') AS used,
               json_extract(g.value, '$.free') AS free,
               json_extract(g.value, '$.utilization_pct') AS utilization_pct,
               json_extract(g.value, '$.at') AS at
        FROM wrapper_documents d, json_each(d.document, '$.gpu_state') g WHERE d.name = 'state'""",
    'hosts': """
        SELECT d.wrapper, json_extract(h.value, '$.mem_total') AS mem_total,
               json_extract(h.value, '$.mem_available') AS mem_available,
               json_extract(h.value, '$.swap_total') AS swap_total,
               json_extract(h.value, '$.swap_free') AS swap_free,
               json_extract(h.value, '$.at') AS at
        FROM wrapper_documents d, json_each(d.document, '$.host_state') h WHERE d.name = 'state'""",
    'residents': """
        SELECT d.wrapper, json_extract(r.value, '$.key') AS model,
               json_extract(r.value, '$.engine') AS engine,
               json_extract(r.value, '$.state') AS state,
               json_extract(r.value, '$.busy') AS busy,
               json_extract(r.value, '$.loading') AS loading,
               json_extract(r.value, '$.healthy') AS healthy,
               json_extract(r.value, '$.vram_bytes') AS vram_bytes,
               json_extract(r.value, '$.ram_bytes') AS ram_bytes,
               json_extract(r.value, '$.ctx') AS ctx,
               json_extract(r.value, '$.last_used') AS last_used,
               json_extract(r.value, '$.calls') AS calls
        FROM wrapper_documents d, json_each(d.document, '$.residents') r WHERE d.name = 'state'""",
}
