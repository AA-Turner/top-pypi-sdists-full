# Makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = _build
DOCS_REMOTE   = git@codeberg.org:araichev/kml2geojson_docs

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

# Internal variables.
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .

.PHONY: help clean html singlehtml publish-docs linkcheck

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html          to make standalone HTML files"
	@echo "  singlehtml    to make a single large HTML file"
	@echo "  publish-docs  to build and publish the docs to $(DOCS_REMOTE)"
	@echo "  linkcheck     to check all external links for integrity"
	@echo "  clean         to remove the build directory"

clean:
	-rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

singlehtml:
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@out="$(BUILDDIR)/singlehtml/index.html"; \
	if command -v gsed >/dev/null 2>&1; then SED=gsed; else SED=sed; fi; \
	$$SED -i.bak -E 's/#document-[^"#]+#/#/g' "$$out" && rm -f "$$out.bak"
	@echo
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

publish-docs: singlehtml
	@echo "Publishing from '$(BUILDDIR)/singlehtml' to '$(DOCS_REMOTE)' ..."
	ghp-import --no-jekyll --branch=docs-build "$(BUILDDIR)/singlehtml"
	git push "$(DOCS_REMOTE)" docs-build:master --force
	-@git branch -D docs-build >/dev/null 2>&1 || true
	@echo "✅ Docs published."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."
