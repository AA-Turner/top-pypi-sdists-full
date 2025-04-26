# AUTO GENERATED ON 2025-03-19 AT 21:19:36
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import pytest
import numpy as np
import kernels

def test_pyawkward_UnionArray8_32_validity_1():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_2():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_3():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_4():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_5():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_6():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_7():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_8():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_9():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_10():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_11():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_12():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_13():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_14():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_15():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_16():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_17():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_18():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_19():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_20():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_21():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_22():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_23():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_24():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_25():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_26():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_27():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_28():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_29():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_30():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_31():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_32():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_33():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_34():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_35():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_36():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_37():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_38():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_39():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_40():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 2
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_41():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 2
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_42():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 2
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_43():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 2
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_44():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 2
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_45():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 2
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_46():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 2
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_47():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 2
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_48():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 2
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_49():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 2
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_50():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 2
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_51():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_52():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_53():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_54():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_55():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_56():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_57():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_58():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_59():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_60():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_61():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_62():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_63():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_64():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_65():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_66():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_67():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_68():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_69():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_70():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_71():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_72():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_73():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_74():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_75():
    tags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_76():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_77():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_78():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_79():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_80():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_81():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_82():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_83():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_84():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_85():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_86():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_87():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_88():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_89():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_90():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_91():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_92():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_93():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_94():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_95():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_96():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_97():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_98():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_99():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_100():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 3
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_101():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_102():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_103():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_104():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_105():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_106():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_107():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_108():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_109():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_110():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_111():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_112():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_113():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_114():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_115():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    numcontents = 10
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_116():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 10
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_117():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 10
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_118():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 10
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_119():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 10
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_120():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    numcontents = 10
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_121():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 10
    lencontents = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_122():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 10
    lencontents = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_123():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 10
    lencontents = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_124():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 10
    lencontents = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

def test_pyawkward_UnionArray8_32_validity_125():
    tags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    numcontents = 10
    lencontents = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_UnionArray8_32_validity')
    with pytest.raises(Exception):
        funcPy(tags=tags, index=index, length=length, numcontents=numcontents, lencontents=lencontents)

