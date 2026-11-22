coverage:
	pytest

test:
	pytest

testall:
	tox

build: clean
	python -m build

clean:
	rm -rf dist/*
	rm -rf build/*

push: build
	git push

release: push
	twine upload -r pypi dist/*

.PHONY: coverage test testall build clean push
