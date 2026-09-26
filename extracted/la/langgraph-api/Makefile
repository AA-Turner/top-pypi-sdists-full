.PHONY: build release lint format test test_watch start start-inmem start-inmem-license-oss start build-go-server start-go-server stop-go-server check-version check-base-imports test-a2a-tck test-a2a-tck-must test-a2a-tck-propose-baseline start-test-a2a-tck start-test-a2a-tck-must start-test-a2a-tck-watch test-mcp-conformance start-test-mcp-conformance list-mcp-scenarios test-auth-read-only-assistant

LANGSERVE_GRAPHS_ALL := '$(shell uv run python tests/graphs/configure_langgraph.py --path-prefix ./tests/graphs --emit langserve-env)'

# Go server management
build-go-server:
	@echo "Building core-server..."
	$(MAKE) -C ../core build-core-server

start-go-server: # NOTE: core server will start with sqlite if no DATABASE_URI is provided
	@echo "Starting Core API (SQLite) gRPC server on port 50051..."
	cd ../core && \
	LANGSERVE_GRAPHS=$(LANGSERVE_GRAPHS_ALL) \
	DATABASE_URI= \
	REDIS_URI= \
	./bin/core-server \
		-apply-db-schema &
	@sleep 2

stop-go-server:
	@echo "Stopping Core API gRPC server on port 50051..."
	@lsof -ti:50051 | xargs -r kill -9 || echo "No process found on port 50051"

# lint commands

lint:
	uv run ruff check . --exclude "**/generated/**"
	uv run ruff format . --diff --exclude "**/generated/**"
	uv run ty check --exclude "**/pb/**" --exclude "**/*_test.py" --exclude "**/test_*.py" --exclude "**/tests/**" --exclude "venv/**" --exclude ".venv/**" --exclude "build/**" --exclude "dist/**" --exclude "**/generated/**" .

format:
	uv run ruff check --fix . --exclude "**/generated/**"
	uv run ruff format . --exclude "**/generated/**"

check-base-imports:
	LANGGRAPH_RUNTIME_EDITION=inmem DATABASE_URI=:memory: REDIS_URI=_FAKE uv run python -c "from langgraph_api.config import *; from langgraph_runtime import *"

# test commands

TEST ?= tests/ ../runtime_inmem/tests/
PYTEST_WORKERS ?= 0
AUTH_TEST ?= "tests/integration_tests/test_custom_auth.py"
LANGGRAPH_HTTP ?= {"disable_mcp": false, "disable_a2a": false}
LANGGRAPH_AES_KEY ?= '1234567890123456'
BG_JOB_TIMEOUT_SECS ?= 86400
BG_JOB_ISOLATED_LOOPS ?= false
CRON_SCHEDULER_SLEEP_TIME ?= 0
RELOAD_ARGS ?= --reload --reload-dir langgraph_api --reload-dir ../runtime_inmem
LANGGRAPH_AUTH_LANGSMITH ?= {"path": "tests/graphs/jwt_auth.py:auth", "allow_langsmith_api_keys": true}

ifdef CI
RELOAD_ARGS :=
endif

# pytest-xdist: pass -n <workers> when PYTEST_WORKERS is set to non-zero
ifneq ($(PYTEST_WORKERS),0)
XDIST_ARGS := -n $(PYTEST_WORKERS) --dist loadscope --retries 2
else
XDIST_ARGS :=
endif

START_TARGET ?= start-license-oss
TEST_TARGET ?= test-license-oss
SERVER_HEALTH_URL ?= http://127.0.0.1:9123/ok
SERVER_START_TIMEOUT_SECS ?= 30

ifeq ($(LANGGRAPH_HTTP),fastapi)
	HTTP_CONFIG := {"app": "./tests/graphs/my_router.py:app", "disable_mcp": false, "disable_a2a": false, "mount_prefix": "/my-cool/api"}
else
	HTTP_CONFIG := $(LANGGRAPH_HTTP)
endif

# Dev/test default: opt in to loopback + http webhooks.
# ``test_custom_route`` etc use relative URLs to dispatch to my_router.py;
# ``test_join_*`` / ``test_webhook_payload_on_timeouts`` / ``test_cron_*``
# and the shutdown suite use ``http://localhost:{port}/webhook`` to a
# pytest httpserver fixture — all of these are blocked by the secure
# ``disable_loopback`` default (GHSA-q3v5-r5ch-p57j), and
# ``require_https`` defaults to true once any webhooks.url block is
# present, so explicitly disable it for the http httpserver fixture.
# Production deployers don't use these Makefiles. Override with
# ``LANGGRAPH_WEBHOOKS=...`` on the command line to exercise the secure
# default during local development.
LANGGRAPH_WEBHOOKS ?= {"url": {"disable_loopback": false, "require_https": false}}

LANGGRAPH_STORE ?= ""
ifeq ($(LANGGRAPH_STORE),custom)
	STORE_CONFIG := {"path": "./tests/graphs/custom_store.py:generate_store"}
else
	STORE_CONFIG := {"index": {"dims": 500, "embed": "./tests/graphs/test_utils/embeddings.py:embeddings"}}
endif

LANGGRAPH_CHECKPOINTER ?=
ifeq ($(LANGGRAPH_CHECKPOINTER),custom)
	CHECKPOINTER_CONFIG := {"path": "./tests/graphs/custom_checkpointer.py:generate_checkpointer"}
else ifeq ($(LANGGRAPH_CHECKPOINTER),redis)
	CHECKPOINTER_CONFIG := {"path": "./tests/graphs/custom_redis_checkpointer.py:generate_checkpointer"}
else ifeq ($(strip $(LANGGRAPH_CHECKPOINTER)),)
	CHECKPOINTER_CONFIG :=
else
	CHECKPOINTER_CONFIG := $(LANGGRAPH_CHECKPOINTER)
endif

REVISION ?= $(shell git rev-parse --short HEAD)
LANGGRAPH_ENCRYPTION ?=

test-license-oss:
	LANGGRAPH_RUNTIME_EDITION=inmem LANGGRAPH_WEBHOOKS='$(LANGGRAPH_WEBHOOKS)' LANGGRAPH_HTTP='$(HTTP_CONFIG)' LANGGRAPH_STORE='$(STORE_CONFIG)' LANGGRAPH_CHECKPOINTER='$(CHECKPOINTER_CONFIG)' LANGGRAPH_ENCRYPTION='$(LANGGRAPH_ENCRYPTION)' REDIS_URI=_FAKE DATABASE_URI=:memory: MIGRATIONS_PATH=__inmem__ uv run pytest -v $(XDIST_ARGS) $(TEST)

test-watch-oss:
	LANGGRAPH_RUNTIME_EDITION=inmem LANGGRAPH_WEBHOOKS='$(LANGGRAPH_WEBHOOKS)' LANGGRAPH_HTTP='$(HTTP_CONFIG)' LANGGRAPH_ENCRYPTION='$(LANGGRAPH_ENCRYPTION)' REDIS_URI=_FAKE DATABASE_URI=:memory: MIGRATIONS_PATH=__inmem__ uv run --no-sync ptw . -- -x -vv --ff --capture=no $(TEST)

test: test-license-oss
test-watch: test-watch-oss
unit-test:
	LANGGRAPH_RUNTIME_EDITION="inmem" DATABASE_URI="test" REDIS_URI="test" uv run pytest tests/unit_tests

unit-test-watch:
	LANGGRAPH_RUNTIME_EDITION="inmem" DATABASE_URI="test" REDIS_URI="test" uv run ptw . -- -x -vv --ff --capture=no tests/unit_tests

test-auth:
	LANGGRAPH_RUNTIME_EDITION=inmem LANGGRAPH_AUTH='{"path": "./tests/graphs/fastapi_jwt_auth.py:auth"}' REDIS_URI=_FAKE DATABASE_URI=:memory: MIGRATIONS_PATH=__inmem__ uv run pytest -v $(XDIST_ARGS) $(AUTH_TEST)

test-with-server:
	@bash -euo pipefail -c '$(MAKE) $(START_TARGET) LANGGRAPH_HTTP='\''$(LANGGRAPH_HTTP)'\'' & \
	pid=$$!; \
	cleanup() { kill $$pid >/dev/null 2>&1 || true; }; \
	trap cleanup EXIT; \
	for i in $$(seq 1 $(SERVER_START_TIMEOUT_SECS)); do \
		if curl -sf "$(SERVER_HEALTH_URL)" >/dev/null; then \
			break; \
		fi; \
		sleep 1; \
	done; \
	if ! curl -sf "$(SERVER_HEALTH_URL)" >/dev/null; then \
		echo "Server failed to start within timeout"; \
		exit 1; \
	fi; \
	$(MAKE) $(TEST_TARGET) LANGGRAPH_HTTP='\''$(LANGGRAPH_HTTP)'\'''


define FASTAPI_JWT_AUTH_TEST
	LANGGRAPH_RUNTIME_EDITION=inmem \
	LANGGRAPH_AUTH='{"path": "./tests/graphs/fastapi_jwt_middleware_ordering.py:auth"}' \
	REDIS_URI=_FAKE \
	DATABASE_URI=:memory: \
	MIGRATIONS_PATH=__inmem__ \
	LANGGRAPH_HTTP='{"app": "./tests/graphs/fastapi_jwt_middleware_ordering.py:app", "middleware_order": "$(1)", "enable_custom_route_auth": $(2)}' \
	uv run pytest -v $(AUTH_TEST)
endef

test-auth-fastapi-jwt--before-custom-middleware--no-custom-route-auth:
	$(call FASTAPI_JWT_AUTH_TEST,auth_first,false)

test-auth-fastapi-jwt--after-custom-middleware--no-custom-route-auth:
	$(call FASTAPI_JWT_AUTH_TEST,middleware_first,false)

test-auth-fastapi-jwt--before-custom-middleware--custom-route-auth:
	$(call FASTAPI_JWT_AUTH_TEST,auth_first,true)

test-auth-fastapi-jwt--after-custom-middleware--custom-route-auth:
	$(call FASTAPI_JWT_AUTH_TEST,middleware_first, true)


test-auth-watch:
	LANGGRAPH_RUNTIME_EDITION=inmem LANGGRAPH_AUTH='{"path": "./tests/graphs/fastapi_jwt_auth.py:auth"}' REDIS_URI=_FAKE DATABASE_URI=:memory: MIGRATIONS_PATH=__inmem__ uv run ptw . -- -x -vv --ff --capture=no $(AUTH_TEST)

test-auth-langsmith-api-keys:
	LANGGRAPH_RUNTIME_EDITION=inmem \
	LANGGRAPH_AUTH='$(LANGGRAPH_AUTH_LANGSMITH)' \
	REDIS_URI=_FAKE \
	DATABASE_URI=:memory: \
	MIGRATIONS_PATH=__inmem__ \
	uv run pytest -v tests/integration_tests/test_langsmith_parallel_auth.py

# dev commands
LANGGRAPH_DISABLE_FILE_PERSISTENCE ?= true
LANGSMITH_TRACING ?= false

start:
	LANGGRAPH_DISABLE_FILE_PERSISTENCE=$(LANGGRAPH_DISABLE_FILE_PERSISTENCE) \
	LANGGRAPH_WEBHOOKS='$(LANGGRAPH_WEBHOOKS)' \
	LANGGRAPH_HTTP='$(HTTP_CONFIG)' \
	LANGGRAPH_RUNTIME_EDITION=inmem \
	LANGGRAPH_AES_KEY='$(LANGGRAPH_AES_KEY)' \
	N_JOBS_PER_WORKER=10 \
	LANGSERVE_GRAPHS=$(LANGSERVE_GRAPHS_ALL) \
	LANGGRAPH_STORE='$(STORE_CONFIG)' \
	LANGGRAPH_CHECKPOINTER='$(CHECKPOINTER_CONFIG)' \
	LANGGRAPH_CONFIG='{"agent": {"configurable": {"model_name": "openai"}}}' \
	LANGSMITH_LANGGRAPH_API_VARIANT=test \
	LANGSMITH_TRACING=$(LANGSMITH_TRACING) \
	BG_JOB_TIMEOUT_SECS=$(BG_JOB_TIMEOUT_SECS) \
	BG_JOB_ISOLATED_LOOPS=$(BG_JOB_ISOLATED_LOOPS) \
	CRON_SCHEDULER_SLEEP_TIME=$(CRON_SCHEDULER_SLEEP_TIME) \
	REDIS_URI=fake \
	DATABASE_URI=:memory: \
	MIGRATIONS_PATH=__inmem \
	uv run uvicorn \
		"langgraph_api.server:app" \
		--port 9123 \
		--log-config logging.json \
		$(RELOAD_ARGS) \
		--no-access-log


start-license-oss: start

start-encrypt:
	LANGGRAPH_WEBHOOKS='$(LANGGRAPH_WEBHOOKS)' \
	LANGGRAPH_HTTP='$(HTTP_CONFIG)' \
	LANGGRAPH_RUNTIME_EDITION=inmem \
	LANGGRAPH_AES_KEY='$(LANGGRAPH_AES_KEY)' \
	N_JOBS_PER_WORKER=10 \
	LANGSERVE_GRAPHS=$(LANGSERVE_GRAPHS_ALL) \
	LANGGRAPH_STORE='$(STORE_CONFIG)' \
	LANGGRAPH_CHECKPOINTER='$(CHECKPOINTER_CONFIG)' \
	LANGGRAPH_ENCRYPTION='{"path": "./tests/graphs/custom_encryption.py:encryption"}' \
	LANGGRAPH_CONFIG='{"agent": {"configurable": {"model_name": "openai"}}}' \
	LANGSMITH_LANGGRAPH_API_VARIANT=test \
	BG_JOB_TIMEOUT_SECS=$(BG_JOB_TIMEOUT_SECS) \
	CRON_SCHEDULER_SLEEP_TIME=$(CRON_SCHEDULER_SLEEP_TIME) \
	REDIS_URI=fake \
	DATABASE_URI=:memory: \
	MIGRATIONS_PATH=__inmem \
	uv run uvicorn \
		"langgraph_api.server:app" \
		--port 9123 \
		$(RELOAD_ARGS) \
		--no-access-log


LANGGRAPH_AUTH ?= {"path": "tests/graphs/jwt_auth.py:auth"}

start-auth-jwt:
	LANGGRAPH_RUNTIME_EDITION=inmem LANGGRAPH_HTTP='$(HTTP_CONFIG)' \
	LANGGRAPH_AES_KEY='$(LANGGRAPH_AES_KEY)' \
	N_JOBS_PER_WORKER=10 \
	LANGSERVE_GRAPHS=$(LANGSERVE_GRAPHS_ALL) \
	LANGGRAPH_STORE='$(STORE_CONFIG)' \
	LANGGRAPH_CHECKPOINTER='$(CHECKPOINTER_CONFIG)' \
	LANGGRAPH_AUTH='$(LANGGRAPH_AUTH)' \
	LANGSMITH_LANGGRAPH_API_VARIANT=test \
	REDIS_URI=fake \
	DATABASE_URI=:memory: \
	MIGRATIONS_PATH=__inmem \
	uv run uvicorn \
		"langgraph_api.server:app" \
		--port 9123 \
		$(RELOAD_ARGS) \
		--no-access-log

start-auth-fastapi-jwt:
	LANGGRAPH_RUNTIME_EDITION=inmem LANGGRAPH_HTTP='$(HTTP_CONFIG)' \
	N_JOBS_PER_WORKER=10 \
	LANGSERVE_GRAPHS=$(LANGSERVE_GRAPHS_ALL) \
	LANGGRAPH_STORE='$(STORE_CONFIG)' \
	LANGGRAPH_CHECKPOINTER='$(CHECKPOINTER_CONFIG)' \
	LANGGRAPH_AUTH='{"path": "./tests/graphs/fastapi_jwt_auth.py:auth"}' \
	LANGSMITH_LANGGRAPH_API_VARIANT=test \
	REDIS_URI=fake \
	DATABASE_URI=:memory: \
	MIGRATIONS_PATH=__inmem \
	uv run uvicorn \
		"langgraph_api.server:app" \
		--port 9123 \
		$(RELOAD_ARGS) \
		--no-access-log

start-auth-langsmith-api-keys:
	LANGGRAPH_AUTH_TYPE=langsmith \
	LANGSMITH_AUTH_ENDPOINT=http://localhost:9124 \
	LANGSMITH_TENANT_ID=8a1f2c4e-5b6d-4f70-9a3b-2c1d0e4f5a6b \
	$(MAKE) start-auth-jwt \
		LANGGRAPH_AUTH='$(LANGGRAPH_AUTH_LANGSMITH)'

define RUN_FASTAPI_JWT_MW_ORDERING
	LANGGRAPH_RUNTIME_EDITION=inmem \
	LANGGRAPH_HTTP='{"app": "./tests/graphs/fastapi_jwt_middleware_ordering.py:app", "middleware_order": "$(1)", "enable_custom_route_auth": $(2)}' \
	N_JOBS_PER_WORKER=10 \
	LANGSERVE_GRAPHS=$(LANGSERVE_GRAPHS_ALL) \
	LANGGRAPH_STORE='$(STORE_CONFIG)' \
	LANGGRAPH_CHECKPOINTER='$(CHECKPOINTER_CONFIG)' \
	LANGGRAPH_AUTH='{"path": "./tests/graphs/fastapi_jwt_middleware_ordering.py:auth"}' \
	LANGSMITH_LANGGRAPH_API_VARIANT=test \
	REDIS_URI=fake \
	DATABASE_URI=:memory: \
	MIGRATIONS_PATH=__inmem \
	uv run uvicorn \
		"langgraph_api.server:app" \
		--reload \
		--port 9123 \
		--reload-dir langgraph_api \
		--reload-dir ../runtime_inmem \
		--no-access-log
endef

start-auth-fastapi-jwt--before-custom-middleware--no-custom-route-auth:
	$(call RUN_FASTAPI_JWT_MW_ORDERING,auth_first,false)

start-auth-fastapi-jwt--after-custom-middleware--no-custom-route-auth:
	$(call RUN_FASTAPI_JWT_MW_ORDERING,middleware_first,false)

start-auth-fastapi-jwt--before-custom-middleware--custom-route-auth:
	$(call RUN_FASTAPI_JWT_MW_ORDERING,auth_first,true)

start-auth-fastapi-jwt--after-custom-middleware--custom-route-auth:
	$(call RUN_FASTAPI_JWT_MW_ORDERING,middleware_first,true)


VERSION_KIND ?= patch

bump-version:
	uv run --with hatch hatch version $(VERSION_KIND)

# A2A TCK (Test Compatibility Kit) targets
# Requires a running server: make start (in another terminal)

TCK_PORT ?= 9123
TCK_GRAPH_ID ?= agent_simple
TCK_TRANSPORT ?= jsonrpc

test-a2a-tck:
	uv run python scripts/run_a2a_tck.py \
		--base-url http://localhost:$(TCK_PORT) \
		--graph-id $(TCK_GRAPH_ID) \
		--transport $(TCK_TRANSPORT) \
		--verbose

test-a2a-tck-must:
	uv run python scripts/run_a2a_tck.py \
		--base-url http://localhost:$(TCK_PORT) \
		--graph-id $(TCK_GRAPH_ID) \
		--transport $(TCK_TRANSPORT) \
		--level must \
		--verbose

test-a2a-tck-propose-baseline:
	uv run python scripts/run_a2a_tck.py \
		--base-url http://localhost:$(TCK_PORT) \
		--graph-id $(TCK_GRAPH_ID) \
		--transport $(TCK_TRANSPORT) \
		--propose-baseline

# Combined targets: start server + run A2A TCK together
# Uses npx concurrently to manage both processes
TCK_STARTUP_DELAY ?= 8

start-test-a2a-tck:
	$(MAKE) test-with-server TEST_TARGET=test-a2a-tck

start-test-a2a-tck-must:
	$(MAKE) test-with-server TEST_TARGET=test-a2a-tck-must

# Watch mode: restart tests on file changes (server stays running)
# Useful during development - edit a2a.py and tests re-run automatically
start-test-a2a-tck-watch:
	npx concurrently -k \
		"$(MAKE) start" \
		"sleep $(TCK_STARTUP_DELAY) && npx nodemon --watch langgraph_api/api/a2a.py --ext py --exec '$(MAKE) test-a2a-tck-must'"

# MCP Conformance Test targets
# Uses the official MCP conformance test suite (https://github.com/modelcontextprotocol/conformance)
# Requires a running server: make start (in another terminal)

MCP_CONFORMANCE_URL ?= http://localhost:9123/mcp
MCP_CONFORMANCE_SUITE ?= active
MCP_CONFORMANCE_BASELINE ?= ../mcp-conformance-baseline.yml
MCP_STARTUP_DELAY ?= 10

test-mcp-conformance:
	npx @modelcontextprotocol/conformance@0.1.13 server \
		--url $(MCP_CONFORMANCE_URL) \
		--suite $(MCP_CONFORMANCE_SUITE) \
		--expected-failures $(MCP_CONFORMANCE_BASELINE) \
		--verbose

start-test-mcp-conformance:
	npx concurrently -k -s first \
		"$(MAKE) start" \
		"sleep $(MCP_STARTUP_DELAY) && $(MAKE) test-mcp-conformance"

list-mcp-scenarios:
	npx @modelcontextprotocol/conformance list --server
