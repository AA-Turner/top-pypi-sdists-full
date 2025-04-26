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

def test_pyawkward_ByteMaskedArray_overlay_mask8_1():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1]
    mymask = [1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_2():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1]
    mymask = [0, 0, 0, 0, 0]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_3():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1]
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_4():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1]
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_5():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1]
    mymask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_6():
    tomask = [123, 123, 123]
    theirmask = [0, 0, 0, 0, 0]
    mymask = [1, 1, 1, 1, 1]
    length = 3
    validwhen = False
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_7():
    tomask = [123, 123, 123]
    theirmask = [0, 0, 0, 0, 0]
    mymask = [0, 0, 0, 0, 0]
    length = 3
    validwhen = False
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [0, 0, 0]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_8():
    tomask = [123, 123, 123]
    theirmask = [0, 0, 0, 0, 0]
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = False
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_9():
    tomask = [123, 123, 123]
    theirmask = [0, 0, 0, 0, 0]
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = False
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_10():
    tomask = [123, 123, 123]
    theirmask = [0, 0, 0, 0, 0]
    mymask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    validwhen = False
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [0, 0, 0]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_11():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = [1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_12():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = [0, 0, 0, 0, 0]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_13():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_14():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_15():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_16():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = [1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_17():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = [0, 0, 0, 0, 0]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_18():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_19():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_20():
    tomask = [123, 123, 123]
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_21():
    tomask = [123, 123, 123]
    theirmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mymask = [1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [0, 0, 0]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_22():
    tomask = [123, 123, 123]
    theirmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mymask = [0, 0, 0, 0, 0]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_23():
    tomask = [123, 123, 123]
    theirmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [0, 0, 0]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_24():
    tomask = [123, 123, 123]
    theirmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [0, 0, 0]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

def test_pyawkward_ByteMaskedArray_overlay_mask8_25():
    tomask = [123, 123, 123]
    theirmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mymask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask8')
    funcPy(tomask=tomask, theirmask=theirmask, mymask=mymask, length=length, validwhen=validwhen)
    pytest_tomask = [1, 1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)

