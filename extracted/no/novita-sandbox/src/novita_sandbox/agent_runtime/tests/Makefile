# Agent Runtime Tests Makefile

.PHONY: help test unit integration performance compatibility examples
.PHONY: test-all test-parallel test-coverage test-report clean install-deps

# Default target
help:
	@echo "Agent Runtime Testing Tools"
	@echo ""
	@echo "Available commands:"
	@echo "  test-unit         Run unit tests"
	@echo "  test-integration  Run integration tests"
	@echo "  test-performance  Run performance tests"
	@echo "  test-compatibility Run compatibility tests"
	@echo "  test-examples     Run example tests"
	@echo "  test-all          Run all tests"
	@echo "  test-parallel     Run tests in parallel"
	@echo "  test-coverage     Run tests and generate coverage report"
	@echo "  test-report       Generate detailed test report"
	@echo "  lint              Code quality check"
	@echo "  clean             Clean test output"
	@echo "  install-deps      Install test dependencies"

# Test commands
test-unit:
	poetry run python run_tests.py --unit --verbose

test-integration:
	poetry run python run_tests.py --integration --verbose

test-performance:
	poetry run python run_tests.py --performance --verbose

test-compatibility:
	poetry run python run_tests.py --compatibility --verbose

test-examples:
	poetry run python run_tests.py --examples --verbose

test-all:
	poetry run python run_tests.py --all --verbose

test-parallel:
	poetry run python run_tests.py --parallel --verbose

test-coverage:
	poetry run python run_tests.py --unit --coverage

test-report:
	poetry run python run_tests.py --report

# Code quality
lint:
	poetry run python run_tests.py --lint

# Cleanup
clean:
	rm -rf htmlcov/
	rm -rf reports/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Dependencies installation
install-deps:
	poetry add --group test pytest pytest-asyncio pytest-mock pytest-cov
	poetry add --group test pytest-xdist pytest-benchmark pytest-html
	poetry add --group test aioresponses httpx responses
