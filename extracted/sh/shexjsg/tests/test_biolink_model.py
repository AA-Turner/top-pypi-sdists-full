import os

import pytest

from ShExJSG import ShExC, ShExJ
from tests import input_data_dir, output_data_dir
from pyjsg.jsglib.loader import load

update_output = False

@pytest.mark.parametrize("infile", [
    "biolink-model.json",
    "shortand.json",
    "list.json",
    "meta.json",
])
def test_conversion(infile: str) -> None:
    outfile = os.path.join(output_data_dir, infile.rsplit('.', 1)[0] + '.shex')
    shexj = load(os.path.join(input_data_dir, infile), ShExJ)
    shexc = ShExC(shexj)
    assert shexc is not None
    shexc_text = str(shexc)
    if update_output:
        with open(outfile, 'w') as outf:
            outf.write(shexc_text)
    with open(outfile) as outf:
        target_shexc = outf.read()
    assert target_shexc == shexc_text, f"Mismatch for {infile}"
    assert not update_output, "update_output is set to True"
