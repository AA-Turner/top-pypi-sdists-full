# cython: language_level=3,fast_fail=True,warning_errors=True
# dython: language_level=3,annotate=True,profile=True,fast_fail=True,warning_errors=True
#!/usr/bin/env python
# coding: utf-8

import numpy as np
cimport numpy as np
from numpy import pi, nan as np_nan
cimport cython
from cython.parallel import prange

def submasks(mask, *masks):
    indices, = np.where(mask)
    for othermask in masks:
        indices = indices[othermask]
    return indices

@cython.boundscheck(False)
@cython.wraparound(False)
cdef _within_unit_cube(
    np.float_t [:, :] u, 
    np.uint8_t [:] acceptable, 
):
    cdef size_t popsize = u.shape[0]
    cdef size_t ndim = u.shape[1]
    cdef np.uint8_t good
    cdef np.int_t i, j

    for i in range(popsize):
        for j in range(ndim):
            if not 0.0 < u[i,j] < 1.0:
                acceptable[i] = 0
                break


def within_unit_cube(u):
    """whether all fields are between 0 and 1, for each row

    Parameters
    ----------
    u: np.array((npoints, ndim), dtype=float):
        points

    Returns
    ---------
    within: np.array(npoints, dtype=bool):
        for each point, whether it is within the unit cube
    """
    acceptable = np.ones(u.shape[0], dtype=bool)
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
    cdef np.int_t i
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
    np.float_t[:] currentt,
    np.float_t[:] current_left,
    np.float_t[:] current_right,
    np.uint8_t[:] searching_left,
    np.uint8_t[:] searching_right,
    np.uint8_t[:] success
):
    cdef size_t popsize = acceptable.shape[0]
    cdef np.int_t j = 0
    cdef np.int_t i
    cdef float my_nan = np_nan
    
    for i in range(popsize):
        if acceptable[i]:
            if Lnew[j] > Lmin:
                success[i] = 1
            j += 1

    for i in prange(popsize, nogil=True):
        # handle cases based on the result:
        # 1) step out further, if still accepting
        if success[i] != 0:
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
            # bisect accepted: start new slice and new generation there
            if success[i] != 0:
                currentt[i] = my_nan
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

    acceptable = within_unit_cube(unew)
    #acceptable = np.empty_like(searching_left)
    #_within_unit_cube(unew, acceptable)

    nc = 0
    if acceptable.any():
        pnew = transform(unew[acceptable,:])
        Lnew = loglike(pnew)
        nc += 1 # len(pnew)
    else:
        pnew = pnew_empty
        Lnew = Lnew_empty

    success = np.zeros_like(searching_left)
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

cdef fill_directions(
    np.ndarray[np.float_t, ndim=2] v,
    np.ndarray[np.int_t, ndim=1] indices,
    float scale
):
    cdef size_t nsamples = v.shape[0]
    cdef size_t ndim = v.shape[0]
    cdef np.int_t i
    for i in range(nsamples):
        v[i, indices[i]] = scale

def generate_unit_directions(ui, region, scale=1):
    nsamples, ndim = ui.shape
    v = np.zeros((nsamples, ndim))
    # choose axis
    j = np.random.randint(ndim, size=nsamples)
    fill_directions(v, j, scale)
    #k = np.arange(nsamples)
    #v[k,j] = scale
    return v

def step_back(Lmin, allL, generation, currentt, log=False):
    # step back where step was excluded by Lmin increase
    # delete from the back until all are good:
    max_width = generation.max() + 1
    below_threshold = allL[:,:max_width] < Lmin
    problematic_parent = np.any(below_threshold, axis=1)
    if not problematic_parent.any():
        return
    parent_i, = np.where(problematic_parent)
    below_threshold_parent = below_threshold[parent_i,:]
    # first, all of them (because we already identified them)
    problematic = np.ones(len(parent_i), dtype=bool)
    #step = 0
    while True:
        if problematic.any():
            ii, = np.where(problematic)
            i = parent_i[problematic]
            g = generation[i]
            generation[i] -= 1
            currentt[i] = np_nan
            allL[i,g] = np_nan
            below_threshold_parent[problematic, g] = False
            #if log:
            #    print("resetting %d%%" % (problematic.meancount_good_generations() * 100), 'by', step, 'steps', 'to', g)
        else:
            break

        #step += 1
        problematic = np.any(below_threshold_parent, axis=1)
