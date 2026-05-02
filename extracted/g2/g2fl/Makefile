tox:
	python3 -m pip install --upgrade tox

release: tox clean pre-commit coverage
	tox run -e release

coverage: tox
	tox run -e coverage

pre-commit: tox
	tox run -e pre-commit


gen-requirements:
	python3 -m pip install --upgrade pipreqs
	pipreqs .

.PHONY:
	clean

clean:
	rm -rf dist
