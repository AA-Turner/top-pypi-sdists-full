ci:
	hatch run test
	git diff
test:
	hatch run test

examples:
	$(MAKE) -C examples

build:
	hatch build

upload:
	hatch publish

.PHONY: test build upload examples
