# ------------------------------------------------------------------------------
# Copyright (C) 2020 Guillaume Sagnol
#
# This file is part of PICOS Testbench.
#
# PICOS Testbench is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# PICOS Testbench is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

"""Test the problems from the optdes tutorial with any solver/dualization."""

import cvxopt as cvx
import picos
import numpy as np

# --------------------------------- #
#  First generate some data :       #
#        _ a list of 8 matrices A   #
#        _ a vector c               #
# --------------------------------- #
A = [cvx.matrix([[1, 0, 0, 0, 0],
                 [0, 3, 0, 0, 0],
                 [0, 0, 1, 0, 0]]),
     cvx.matrix([[0, 0, 2, 0, 0],
                 [0, 1, 0, 0, 0],
                 [0, 0, 0, 1, 0]]),
     cvx.matrix([[0, 0, 0, 2, 0],
                 [4, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0]]),
     cvx.matrix([[1, 0, 0, 0, 0],
                 [0, 0, 2, 0, 0],
                 [0, 0, 0, 0, 4]]),
     cvx.matrix([[1, 0, 2, 0, 0],
                 [0, 3, 0, 1, 2],
                 [0, 0, 1, 2, 0]]),
     cvx.matrix([[0, 1, 1, 1, 0],
                 [0, 3, 0, 1, 0],
                 [0, 0, 2, 2, 0]]),
     cvx.matrix([[1, 2, 0, 0, 0],
                 [0, 3, 3, 0, 5],
                 [1, 0, 0, 2, 0]]),
     cvx.matrix([[1, 0, 3, 0, 1],
                 [0, 3, 2, 0, 0],
                 [1, 0, 0, 2, 0]])
     ]
c = cvx.matrix([1, 2, 3, 4, 5])


def c_SOCP(solver='cvxopt', dualize=False):  # noqa
    # create the problem, variables and params
    c_primal_SOCP = picos.Problem()
    AA = [picos.Constant('A[{0}]'.format(i), Ai)
          for i, Ai in enumerate(A)]  # each AA[i].T is a 3x5 observation matrix
    s = len(AA)
    cc = picos.Constant('c', c)
    z = [picos.RealVariable('z[{0}]'.format(i), AA[i].size[1])
         for i in range(s)]
    mu = picos.RealVariable('mu', s)

    # define the constraints and objective function
    cones = c_primal_SOCP.add_list_of_constraints([abs(z[i]) <= mu[i]
                                                   for i in range(s)])
    lin = c_primal_SOCP.add_constraint(picos.sum([AA[i] * z[i]
                                                  for i in range(s)]) == cc)
    c_primal_SOCP.set_objective('min', (1 | mu))

    solution = c_primal_SOCP.solve(dualize=dualize, solver=solver)
    mu = mu.value
    wopt = mu / sum(mu)

    exp_opt = [0, 0, 0, 0, 1.28422e-01, 0, 8.7158e-01, 0]
    return np.linalg.norm(wopt - cvx.matrix(exp_opt), np.inf)


def c_LP(solver='cvxopt', dualize=False):  # noqa
    # create the problem, variables and params
    c_primal_LP = picos.Problem()
    A1 = [cvx.sparse(a[:, i], tc='d') for i in range(3) for a in A[4:]]
    A1 = A1[:-1]  # remove the last design point (same as the last-but-one)
    s = len(A1)
    AA = [picos.Constant('A[{0}]'.format(i), Ai)
          for i, Ai in enumerate(A1)]  # each AA[i].T is a 1 x 5 obs matrix
    cc = picos.Constant('c', c)
    z = [picos.RealVariable('z[{0}]'.format(i), 1) for i in range(s)]
    mu = picos.RealVariable('mu', s)
    # define the constraints and objective function
    abs_con = c_primal_LP.add_list_of_constraints([abs(z[i]) <= mu[i]
                                                   for i in range(s)])
    lin_con = c_primal_LP.add_constraint(picos.sum([AA[i] * z[i]
                                                    for i in range(s)]) == cc)
    c_primal_LP.set_objective('min', (1 | mu))

    solution = c_primal_LP.solve(dualize=dualize, solver=solver)
    mu = mu.value
    wopt = mu / sum(mu)

    exp_opt = [0, 0, 0, 0, 3.36700e-02, 0, 2.79461e-01,
               1.17845e-01, 2.76094e-01, 0, 2.92929e-01]
    return np.linalg.norm(wopt - cvx.matrix(exp_opt), np.inf)


def c_SDP(solver='cvxopt', dualize=False):  # noqa
    # create the problem, variables and params
    c_primal_SDP = picos.Problem()
    AA = [picos.Constant('A[{0}]'.format(i), Ai)
          for i, Ai in enumerate(A)]  # each AA[i].T is a 3 x 5 obs matrix
    s = len(AA)
    cc = picos.Constant('c', c)
    mu = picos.RealVariable('mu', s)
    # define the constraints and objective function
    lmi = c_primal_SDP.add_constraint(
        picos.sum([mu[i] * AA[i] * AA[i].T for i in range(s)]) >> cc * cc.T)
    lin_cons = c_primal_SDP.add_constraint(mu >= 0)
    c_primal_SDP.set_objective('min', (1 | mu))

    solution = c_primal_SDP.solve(dualize=dualize, solver=solver)
    w = mu.value
    wopt = w / sum(w)

    exp_opt = [0, 0, 0, 0, 1.28422e-01, 0, 8.7158e-01, 0]
    return np.linalg.norm(wopt - cvx.matrix(exp_opt), np.inf)


def A_SDP(solver='cvxopt', dualize=False):  # noqa
    A_primal_SOCP = picos.Problem()
    AA = [picos.Constant('A[{0}]'.format(i), Ai)
          for i, Ai in enumerate(A)]  # each AA[i].T is a 3 x 5 obs matrix
    s = len(AA)
    Z = [picos.RealVariable('Z[{0}]'.format(i), AA[i].T.size) for i in range(s)]
    mu = picos.RealVariable('mu', s)

    # define the constraints and objective function
    cone_cons = A_primal_SOCP.add_list_of_constraints(
        [abs(Z[i]) <= mu[i] for i in range(s)])
    lin_cons = A_primal_SOCP.add_constraint(
        picos.sum([AA[i] * Z[i] for i in range(s)]) == 'I')
    A_primal_SOCP.set_objective('min', (1 | mu))

    solution = A_primal_SOCP.solve(dualize=dualize, solver=solver)
    w = mu.value
    wopt = w / sum(w)
    exp_opt = [0, 0, 2.49091e-01, 1.42474e-01,
               8.50547e-02, 1.21285e-01, 1.32472e-01, 2.69620e-01]
    return np.linalg.norm(wopt - cvx.matrix(exp_opt), np.inf)


def A_multi(solver='cvxopt', dualize=False):  # noqa
    A_multiconstraints = picos.Problem()
    AA = [picos.Constant('A[{0}]'.format(i), Ai)
          for i, Ai in enumerate(A)]  # each AA[i].T is a 3 x 5 obs matrix
    s = len(AA)
    mu = picos.RealVariable('mu', s)
    w = picos.RealVariable('w', s)
    Z = [picos.RealVariable('Z[{0}]'.format(i), AA[i].T.size)
         for i in range(s)]
    # define the constraints and objective function
    lin_cons0 = A_multiconstraints.add_constraint(
        picos.sum([AA[i] * Z[i] for i in range(s)]) == 'I')
    lin_cons1 = A_multiconstraints.add_constraint((1 | w[:4]) <= 0.5)
    lin_cons2 = A_multiconstraints.add_constraint((1 | w[4:]) <= 0.5)
    cone_cons = A_multiconstraints.add_list_of_constraints(
        [abs(Z[i]) ** 2 <= mu[i] * w[i] for i in range(s)])
    A_multiconstraints.set_objective('min', (1 | mu))

    solution = A_multiconstraints.solve(dualize=dualize, solver=solver)
    w = w.value
    wopt = w / sum(w)

    exp_opt = [0, 0, 2.97337e-01, 2.02662e-01,
               6.5387e-02, 1.19282e-01, 9.01631e-02, 2.25167e-01]

    return np.linalg.norm(wopt - cvx.matrix(exp_opt), np.inf)


def A_exact(solver='mosek'):  # noqa
    # create the problem, variables and params
    A_exact = picos.Problem()
    AA = [picos.Constant('A[{0}]'.format(i), Ai)
          for i, Ai in enumerate(A)]  # each AA[i].T is a 3 x 5 obs matrix
    s = len(AA)
    m = AA[0].size[0]
    N = picos.Constant('N', 20)  # number of trials allowed
    I = picos.Constant('I', cvx.spmatrix([1] * m, range(m), range(m), (m, m)))
    Z = [picos.RealVariable('Z[{0}]'.format(i), AA[i].T.size)
         for i in range(s)]
    n = picos.IntegerVariable('n', s)
    t = picos.RealVariable('t', s)

    # define the constraints and objective function
    cone_cons = A_exact.add_list_of_constraints(
        [abs(Z[i]) ** 2 <= n[i] * t[i] for i in range(s)])
    lin_cons = A_exact.add_constraint(
        picos.sum([AA[i] * Z[i] for i in range(s)]) == I)
    wgt_cons = A_exact.add_constraint((1 | n) <= N)
    A_exact.set_objective('min', 1 | t)

    solution = A_exact.solve(solver=solver)
    exp_opt = [0, 0, 5, 3, 2, 2, 3, 5]
    return np.linalg.norm(n.value - cvx.matrix(exp_opt), np.inf)


def D_SOCP(solver='cvxopt', dualize=False):  # noqa
    D_SOCP = picos.Problem()
    AA = [picos.Constant('A[{0}]'.format(i), Ai)
          for i, Ai in enumerate(A)]  # each AA[i].T is a 3 x 5 obs matrix
    s = len(AA)
    m = AA[0].size[0]
    mm = picos.Constant('m', m)
    L = picos.RealVariable('L', (m, m))
    V = [picos.RealVariable('V[' + str(i) + ']', AA[i].T.size)
         for i in range(s)]
    w = picos.RealVariable('w', s)
    # additional variable to handle the geometric mean in the objective function
    t = picos.RealVariable('t', 1)
    # define the constraints and objective function
    lin_cons = D_SOCP.add_constraint(picos.sum([AA[i] * V[i]
                                                for i in range(s)]) == L)
    # L is lower triangular
    lowtri_cons = D_SOCP.add_list_of_constraints([L[i, j] == 0
                                                  for i in range(m)
                                                  for j in range(i + 1, m)])
    cone_cons = D_SOCP.add_list_of_constraints([abs(V[i]) <= (mm ** 0.5) * w[i]
                                                for i in range(s)])
    wgt_cons = D_SOCP.add_constraint(1 | w <= 1)
    geomean_cons = D_SOCP.add_constraint(t <= picos.geomean(picos.maindiag(L)))
    D_SOCP.set_objective('max', t)

    solution = D_SOCP.solve(solver=solver, dualize=True)
    exp_opt = [0, 0, 2.26737e-01, 3.38338e-02, 1.65183e-02,
               5.44358e-02, 3.17624e-01, 3.50851e-01]
    return np.linalg.norm(w.value - cvx.matrix(exp_opt), np.inf)


def D_exact(solver='mosek'):  # noqa
    # create the problem, variables and params
    D_exact = picos.Problem()
    AA = [picos.Constant('A[{0}]'.format(i), Ai)
          for i, Ai in enumerate(A)]  # each AA[i].T is a 3 x 5 obs matrix
    s = len(AA)
    m = AA[0].size[0]
    mm = picos.Constant('m', m)
    L = picos.RealVariable('L', (m, m))
    V = [picos.RealVariable('V[' + str(i) + ']', AA[i].T.size)
         for i in range(s)]
    T = picos.RealVariable('T', (s, m))
    n = picos.IntegerVariable('n', s)
    N = picos.Constant('N', 20)
    # additional variable to handle the geomean inequality
    t = picos.RealVariable('t', 1)

    # define the constraints and objective function
    lin_cons = D_exact.add_constraint(
        picos.sum([AA[i] * V[i] for i in range(s)]) == L)
    # L is lower triangular
    lowtri_cons = D_exact.add_list_of_constraints([L[i, j] == 0
                                                   for i in range(m)
                                                   for j in range(i + 1, m)])
    cone_cons = D_exact.add_list_of_constraints([
        abs(V[i][:, k]) ** 2 <= n[i] / N * T[i, k]
        for i in range(s) for k in range(m)])
    lin_cons2 = D_exact.add_list_of_constraints([(1 | T[:, k]) <= 1
                                                 for k in range(m)])
    wgt_cons = D_exact.add_constraint(1 | n <= N)
    geomean_cons = D_exact.add_constraint(t <= picos.geomean(picos.maindiag(L)))
    D_exact.set_objective('max', t)

    solution = D_exact.solve(solver=solver)
    exp_opt = [0, 0, 5, 1, 0, 1, 6, 7]
    return np.linalg.norm(n.value - cvx.matrix(exp_opt), np.inf)


def D_MAXDET(solver='cvcopt', dualize=False):  # noqa
    D_MAXDET = picos.Problem()
    AA = [picos.Constant('A[{0}]'.format(i), Ai)
          for i, Ai in enumerate(A)]  # each AA[i].T is a 3 x 5 obs matrix
    s = len(AA)
    m = AA[0].size[0]
    w = picos.RealVariable('w', s, lower=0)
    t = picos.RealVariable('t', 1)
    # constraint and objective
    wgt_cons = D_MAXDET.add_constraint(1 | w <= 1)
    Mw = picos.sum([w[i] * AA[i] * AA[i].T for i in range(s)])
    detrootn_cons = D_MAXDET.add_constraint(t <= picos.DetRootN(Mw))
    D_MAXDET.set_objective('max', t)
    solution = D_MAXDET.solve(solver=solver, dualize=True)
    exp_opt = [0, 0, 2.26737e-01, 3.38338e-02, 1.65183e-02,
               5.44358e-02, 3.17624e-01, 3.50851e-01]
    return np.linalg.norm(w.value - cvx.matrix(exp_opt), np.inf)


def Pp_SDP(solver='cvcopt', dualize=False, p=0.2):  # noqa
    Pp_SDP = picos.Problem()
    AA = [picos.Constant('A[{0}]'.format(i), Ai)
          for i, Ai in enumerate(A)]  # each AA[i].T is a 3 x 5 obs matrix
    s = len(AA)
    m = AA[0].size[0]
    w = picos.RealVariable('w', s, lower=0)
    t = picos.RealVariable('t', 1)

    # constraint and objective
    wgt_cons = Pp_SDP.add_constraint(1 | w <= 1)
    Mw = picos.sum([w[i] * AA[i] * AA[i].T for i in range(s)])

    if p >= 0:
        tracep_cons = Pp_SDP.add_constraint(t <= picos.PowerTrace(Mw, p))
        Pp_SDP.set_objective('max', t)
    else:
        tracep_cons = Pp_SDP.add_constraint(t >= picos.PowerTrace(Mw, p))
        Pp_SDP.set_objective('min', t)

    solution = Pp_SDP.solve(solver=solver, dualize=True)

    if p == 0.2:
        exp_opt = [0, 0, 2.06402783e-01, 0, 0,
                   9.19905459e-03, 4.07744555e-01, 3.76653596e-01]

    elif p == -3:
        exp_opt = [0, 0, 2.47527347e-01, 1.65737084e-01, 1.07798441e-01,
                   1.41009554e-01, 7.82810752e-02, 2.59646497e-01]
    else:
        raise ValueError('unknown p')

    return np.linalg.norm(w.value - cvx.matrix(exp_opt), np.inf)


def test_cont(name, problem, tol, **kwargs):  # noqa
    test = problem(**kwargs)
    if test > tol:
        print('failure for problem ' + name)


solvers_cont = ['cvxopt', 'ecos', 'gurobi', 'cplex', 'mosek']
for solver in solvers_cont:
    for dualize in [False, True]:
        print()
        print(solver, dualize)
        test_cont('c_SOCP', c_SOCP, 1e-4, solver=solver, dualize=dualize)
        test_cont('c_LP', c_LP, 1e-4, solver=solver, dualize=dualize)
        if solver in ['cvxopt', 'mosek']:
            test_cont('c_SDP', c_SDP, 1e-4, solver=solver, dualize=dualize)
            test_cont('A_SDP', A_SDP, 1e-4, solver=solver, dualize=dualize)
            test_cont('D_MAXDET', D_MAXDET, 1e-4, solver=solver,
                      dualize=dualize)
            test_cont('P02_SDP', Pp_SDP, 1e-4, solver=solver,
                      dualize=dualize, p=0.2)
            test_cont('Pm3_SDP', Pp_SDP, 1e-4, solver=solver,
                      dualize=dualize, p=-3)

        test_cont('A_multi', A_multi, 1e-4, solver=solver, dualize=dualize)
        test_cont('D_SOCP', D_SOCP, 1e-4, solver=solver, dualize=dualize)

solvers_int = ['gurobi', 'cplex', 'mosek']

for solver in solvers_int:
    print()
    print(solver)
    test_cont('A_exact', A_exact, 1e-4, solver=solver)
    test_cont('D_exact', D_exact, 1e-4, solver=solver)
