# cython: language_level=3,fast_fail=True,warning_errors=True
# dython: language_level=3,annotate=True,profile=True,fast_fail=True,warning_errors=True
#!/usr/bin/env python
# coding: utf-8

import numpy as np
cimport numpy as np
from numpy import pi, nan as np_nan
#from numpy cimport nan as np_nan
cimport cython

import operator
firstitemgetter = operator.itemgetter(0)

def submasks(mask, *masks):
    indices, = np.where(mask)
    for othermask in masks:
        indices = indices[othermask]
    return indices

@cython.boundscheck(False)
@cython.wraparound(False)
cdef _within_unit_cube(
    np.ndarray[np.float_t, ndim=2] u, 
    np.ndarray[np.uint8_t, ndim=1] acceptable, 
):
    cdef size_t popsize = u.shape[0]
    cdef size_t ndim = u.shape[1]
    cdef np.uint8_t good

    for i in range(popsize):
        good = True
        for j in range(ndim):
            if not 0 < u[i,j] < 1:
                good = False
                break
        acceptable[i] = good


def within_unit_cube(u):
    acceptable = np.empty(u.shape[0], dtype=bool)
    _within_unit_cube(u, acceptable)
    return acceptable

@cython.boundscheck(False)
@cython.wraparound(False)
cdef _evolve_prepare(
    np.ndarray[np.uint8_t, ndim=1] searching_left, 
    np.ndarray[np.uint8_t, ndim=1] searching_right,
    np.ndarray[np.uint8_t, ndim=1] search_right,
    np.ndarray[np.uint8_t, ndim=1] bisecting
):
    # define three mutually exclusive states: 
    # stepping out to the left, to the right, bisecting on the slice
    cdef size_t n = searching_left.shape[0]
    for i in range(n):
        search_right[i] = not searching_left[i] and searching_right[i]
        bisecting[i] = not (searching_left[i] or searching_right[i])

def evolve_prepare(searching_left, searching_right):
    search_right = np.empty_like(searching_left)
    bisecting = np.empty_like(searching_left)
    _evolve_prepare(searching_left, searching_right, search_right, bisecting)
    return search_right, bisecting

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef evolve_update(
    np.ndarray[np.uint8_t, ndim=1] acceptable, 
    np.ndarray[np.float_t, ndim=1] Lnew, 
    np.float_t Lmin, 
    np.ndarray[np.uint8_t, ndim=1] search_right, 
    np.ndarray[np.uint8_t, ndim=1] bisecting, 
    np.ndarray[np.float_t, ndim=1] currentt,
    np.ndarray[np.float_t, ndim=1] current_left,
    np.ndarray[np.float_t, ndim=1] current_right,
    np.ndarray[np.uint8_t, ndim=1] searching_left,
    np.ndarray[np.uint8_t, ndim=1] searching_right,
    np.ndarray[np.uint8_t, ndim=1] success
):
    cdef size_t popsize = acceptable.shape[0]
    cdef np.uint8_t accepted
    cdef np.int_t j = 0
    
    for i in range(popsize):
        accepted = False
        if acceptable[i]:
            if Lnew[j] > Lmin:
                accepted = True
            j += 1

        # handle cases based on the result:
        # 1) step out further, if still accepting
        if accepted:
            if searching_left[i]:
                current_left[i] *= 2
            if search_right[i]:
                current_right[i] *= 2
        # 2) done stepping out, if rejected
        else:
            if searching_left[i]:
                searching_left[i] = 0
            if search_right[i]:
                searching_right[i] = 0
        # bisecting, rejected or not acceptable
        if bisecting[i]:
            if currentt[i] < 0:
                # bisect shrink left:
                current_left[i] = currentt[i]
            else:
                current_right[i] = currentt[i]
            success[i] = accepted
            # bisect accepted: start new slice and new generation there
            if accepted:
                currentt[i] = np_nan
        else:
            success[i] = 0

pnew_empty = np.empty((0,1))
Lnew_empty = np.empty(0)

def evolve(
    transform, loglike, Lmin, 
    currentu, currentL, currentt, currentv,
    current_left, current_right, searching_left, searching_right,
    log=False
):
    search_right, bisecting = evolve_prepare(searching_left, searching_right)

    unew = currentu
    unew[searching_left,:] = currentu[searching_left,:] + currentv[searching_left,:] * current_left[searching_left].reshape((-1,1))
    unew[search_right,:] = currentu[search_right,:] + currentv[search_right,:] * current_right[search_right].reshape((-1,1))
    currentt[bisecting] = np.random.uniform(current_left[bisecting], current_right[bisecting])
    unew[bisecting,:] = currentu[bisecting,:] + currentv[bisecting,:] * currentt[bisecting].reshape((-1,1))
    # assert np.isfinite(unew).all(), unew

    #acceptable = within_unit_cube(unew)
    acceptable = np.empty_like(searching_left)
    _within_unit_cube(unew, acceptable)

    nc = 0
    if acceptable.any():
        pnew = transform(unew[acceptable,:])
        Lnew = loglike(pnew)
        nc += 1 # len(pnew)
    else:
        pnew = pnew_empty
        Lnew = Lnew_empty

    success = np.empty_like(searching_left)
    evolve_update(
        acceptable, Lnew, Lmin, search_right, bisecting, currentt,
        current_left, current_right, searching_left, searching_right,
        success
    )

    return (
        (
        currentt, currentv,
        current_left, current_right, searching_left, searching_right), 
        (success, unew[success,:], pnew[success[acceptable],:], Lnew[success[acceptable]]), 
        nc
    )

@cython.boundscheck(False)
@cython.wraparound(False)
cdef _count_good_generations(
    np.float_t Lmin,
    np.ndarray[np.float_t, ndim=2] allL,
    np.ndarray[np.int_t, ndim=1] generation,
    np.ndarray[np.int_t, ndim=1] ngood_generations,
):
    # step back where step was excluded by Lmin increase
    cdef size_t popsize = allL.shape[0]
    #cdef size_t ngood
    
    for i in range(popsize):
        # ngood = 0
        for j in range(generation[i]+1):
            if allL[i,j] < Lmin:
                break
            else:
                ngood_generations[i] += 1
        #ngood_generations[i] = ngood

def count_good_generations(Lmin, allL, generation):
    ngood_generations = np.zeros_like(generation)
    _count_good_generations(Lmin, allL, generation, ngood_generations)
    return ngood_generations

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef step_back(
    np.float_t Lmin,
    np.ndarray[np.int_t, ndim=1] generation,
    np.ndarray[np.float_t, ndim=2] allL,
    np.ndarray[np.float_t, ndim=1] currentt
):
    # step back where step was excluded by Lmin increase
    cdef size_t popsize = allL.shape[0]
    #cdef size_t generations = allL.shape[1]
    
    for i in range(popsize):
        for j in range(generation[i]+1):
            #if not np.isfinite(allL[i,j]):
            #    assert False, (allL[i,j], j, generation[i])
            if allL[i,j] < Lmin:
                generation[i] = j - 1
                currentt[i] = np_nan
                allL[i,j] = np_nan
                break

"""
    step = 0
    while True:
        step += 1
        problematic = np.any(self.allL < Lmin, axis=1)
        assert problematic.shape == (self.popsize,), (problematic.shape, self.popsize,)
        if problematic.any():
            i, = np.where(problematic)
            g = self.generation[problematic]
            self.generation[problematic] -= 1
            self.currentt[i] = np.nan
            self.allL[i,g] = np.nan
            if self.log:
                print("resetting %d%%" % (problematic.mean() * 100), 'by', step, 'steps', 'to', g)
        else:
            break
"""

"""
cdef fill_directions(
    np.ndarray[np.float_t, ndim=2] v,
    np.ndarray[np.int_t, ndim=1] indices,
    float scale
):
    cdef size_t nsamples = ui.shape[0]
    cdef size_t ndim = ui.shape[0]
    for i in range(nsamples):
        v[i,indices[j]] = scale
"""
def generate_unit_directions(ui, region, scale=1):
    del region
    nsamples, ndim = ui.shape
    v = np.zeros_like(ui)
    # choose axis
    j = np.random.randint(ndim, size=nsamples)
    #fill_directions(v, j, scale)
    k = np.arange(nsamples)
    v[k,j] = scale
    return v

assert (generate_unit_directions(np.zeros((10,2)), None).sum(axis=1) == 1).all()
