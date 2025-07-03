.PHONY: build release lint format test test_watch start start-inmem start-inmem-license-oss start check-version

# lint commands

lint:
	uv run ruff check .
	uv run ruff format . --diff

format:
	uv run ruff check --fix .
	uv run ruff format .

# test commands

TEST ?= tests/
AUTH_TEST ?= "tests/integration_tests/test_custom_auth.py"
LANGGRAPH_HTTP ?= {"disable_mcp": false}
LANGGRAPH_AES_KEY ?= '1234567890123456'

ifeq ($(LANGGRAPH_HTTP),fastapi)
	HTTP_CONFIG := {"app": "./tests/graphs/my_router.py:app", "disable_mcp": false, "mount_prefix": "/my-cool/api"}
else
	HTTP_CONFIG := $(LANGGRAPH_HTTP)
endif

LANGGRAPH_STORE ?= ""
ifeq ($(LANGGRAPH_STORE),custom)
	STORE_CONFIG := {"path": "./tests/graphs/custom_store.py:generate_store"}
else
	STORE_CONFIG := {"index": {"dims": 500, "embed": "./tests/graphs/test_utils/embeddings.py:embeddings"}}
endif

REVISION ?= $(shell git rev-parse --short HEAD)

test-license-oss:
	LANGGRAPH_RUNTIME_EDITION=inmem LANGGRAPH_HTTP='$(HTTP_CONFIG)' LANGGRAPH_STORE='$(STORE_CONFIG)' REDIS_URI=_FAKE DATABASE_URI=:memory: MIGRATIONS_PATH=__inmem__ uv run pytest -v $(TEST)

test-watch-oss:
	LANGGRAPH_RUNTIME_EDITION=inmem LANGGRAPH_HTTP='$(HTTP_CONFIG)' REDIS_URI=_FAKE DATABASE_URI=:memory: MIGRATIONS_PATH=__inmem__ uv run ptw . -- -x -vv --ff --capture=no $(TEST)

test: test-license-oss
test-watch: test-watch-oss

test-auth:
	LANGGRAPH_RUNTIME_EDITION=inmem LANGGRAPH_AUTH='{"path": "./tests/graphs/fastapi_jwt_auth.py:get_current_active_user"}' REDIS_URI=_FAKE DATABASE_URI=:memory: MIGRATIONS_PATH=__inmem__ uv run pytest -v $(AUTH_TEST)

test-auth-watch:
	LANGGRAPH_RUNTIME_EDITION=inmem LANGGRAPH_AUTH='{"path": "./tests/graphs/fastapi_jwt_auth.py:get_current_active_user"}' REDIS_URI=_FAKE DATABASE_URI=:memory: MIGRATIONS_PATH=__inmem__ uv run ptw . -- -x -vv --ff --capture=no $(AUTH_TEST)

# dev commands

start:
	LANGGRAPH_HTTP='$(HTTP_CONFIG)' \
	LANGGRAPH_RUNTIME_EDITION=inmem \
	LANGGRAPH_AES_KEY='$(LANGGRAPH_AES_KEY)' \
	N_JOBS_PER_WORKER=2 \
	LANGGRAPH_CONFIG='{"agent": {"configurable": {"model_name": "openai"}}}' \
	LANGSERVE_GRAPHS='{"agent": "./tests/graphs/agent.py:graph", "single_node": "./tests/graphs/single_node.py:graph", "benchmark": "./tests/graphs/benchmark.py:graph", "other": "./tests/graphs/other.py:make_graph", "weather": "./tests/graphs/weather.py:mk_weather_graph", "searchy": "./tests/graphs/searchy.py:graph", "agent_simple": "./tests/graphs/agent_simple.py:graph"}' \
	LANGGRAPH_STORE='$(STORE_CONFIG)' \
	LANGGRAPH_CONFIG='{"agent": {"configurable": {"model_name": "openai"}}}' \
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


start-license-oss: start


start-auth-jwt:
	LANGGRAPH_RUNTIME_EDITION=inmem LANGGRAPH_HTTP='$(HTTP_CONFIG)' \
	LANGGRAPH_AES_KEY='$(LANGGRAPH_AES_KEY)' \
	N_JOBS_PER_WORKER=2 \
	LANGSERVE_GRAPHS='{"agent": "./tests/graphs/agent.py:graph", "other": "./tests/graphs/other.py:make_graph", "weather": "./tests/graphs/weather.py:mk_weather_graph", "searchy": "./tests/graphs/searchy.py:graph", "agent_simple": "./tests/graphs/agent_simple.py:graph"}' \
	LANGGRAPH_STORE='$(STORE_CONFIG)' \
	LANGGRAPH_AUTH='{"path": "tests/graphs/jwt_auth.py:auth"}' \
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

start-auth-fastapi-jwt:
	LANGGRAPH_RUNTIME_EDITION=inmem LANGGRAPH_HTTP='$(HTTP_CONFIG)' \
	N_JOBS_PER_WORKER=2 \
	LANGSERVE_GRAPHS='{"agent": "./tests/graphs/agent.py:graph", "other": "./tests/graphs/other.py:make_graph", "weather": "./tests/graphs/weather.py:mk_weather_graph", "searchy": "./tests/graphs/searchy.py:graph", "agent_simple": "./tests/graphs/agent_simple.py:graph"}' \
	LANGGRAPH_STORE='$(STORE_CONFIG)' \
	LANGGRAPH_AUTH='{"path": "./tests/graphs/fastapi_jwt_auth.py:auth"}' \
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

VERSION_KIND ?= patch

bump-version:
	uv run --with hatch hatch version $(VERSION_KIND)