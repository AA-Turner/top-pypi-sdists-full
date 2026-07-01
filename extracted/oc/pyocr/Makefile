PYTHON = python3

build:
	echo "Run make build_py"
	echo "or make install"

install: install_py install_c

uninstall: uninstall_py

build_py:
	pip install build
	build

build_c:

doc: install_py
	(cd doc && make html)
	cp doc/index.html doc/build/index.html

check:
	flake8 src/ tests/

test:
	pytest -xv tests/

linux_exe:

windows_exe:

release:
ifeq (${RELEASE}, )
	@echo "You must specify a release version (make release RELEASE=1.2.3)"
else
	@echo "Will release: ${RELEASE}"
	@echo "Checking release is in ChangeLog ..."
	grep ${RELEASE} ChangeLog | grep -v "/xx"
	@echo "Releasing ..."
	git tag -a ${RELEASE} -m ${RELEASE}
	git push origin ${RELEASE}
	make clean
	${PYTHON} ./setup.py sdist
	twine upload dist/pyocr-${RELEASE}.tar.gz
	@echo "All done"
endif

clean:
	rm -rf doc/build
	rm -rf build dist *.egg-info
	rm -rf src/pyocr/__pycache__
	rm -f src/pyocr/_version.py

install_py:
	${PYTHON} -m pip install ${PIP_ARGS} .

install_c:

uninstall_py:
	pip3 uninstall -y pyocr

uninstall_c:

help:
	@echo "make build || make build_py"
	@echo "make check"
	@echo "make doc"
	@echo "make help: display this message"
	@echo "make install || make install_py"
	@echo "make release"
	@echo "make test"
	@echo "make uninstall || make uninstall_py"

.PHONY: \
	build \
	build_c \
	build_py \
	check \
	doc \
	linux_exe \
	windows_exe \
	help \
	install \
	install_c \
	install_py \
	release \
	test \
	uninstall \
	uninstall_c
