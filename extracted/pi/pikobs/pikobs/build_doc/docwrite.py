"""Write a generated docstring into a module, with a mark above it.

Every build_*.py generator writes the page of its module as the module
docstring. A change made by hand in that docstring is lost at the next
./pikobs_doc.sh, so the docstring is preceded by two comment lines naming
the generator to edit instead. The comments are not part of the docstring:
the web page and help() are unchanged.

    from docwrite import write_docstring
    write_docstring(target, doc, __file__)
"""
import os
import re

MARK = ("# GENERATED -- this docstring is written by pikobs/build_doc/{gen}.\n"
        "# Edit that file and run ./pikobs_doc.sh; a change made here is lost.\n")
OLD_MARK = re.compile(r"(?m)^# GENERATED -- this docstring is written by .*\n"
                      r"(?:# Edit that file and run \./pikobs_doc\.sh.*\n)?")


def write_docstring(target, doc, generator):
    """Replace the module docstring of target with doc (raw string), the
    mark of generator above it."""
    src = open(target).read()
    start = src.index('"""')
    if start > 0 and src[start - 1] == 'r':
        start -= 1
    end = src.index('"""', src.index('"""', start) + 3) + 3
    head = OLD_MARK.sub("", src[:start])
    mark = MARK.format(gen=os.path.basename(generator))
    open(target, "w").write(head + mark + 'r"""' + doc.lstrip("\n") + '"""' + src[end:])
