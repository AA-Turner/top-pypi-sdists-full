'''
Sempy: A Python implementation of the spectral element method.
Copyright (C) 2011,  Stian Jensen.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
''' 


import numpy as np
import scipy.sparse.linalg as sp
import pysparse
import scipy.linalg as sc

# Compatibility with older versions
if int(pysparse.__version__[2]) >=2:
    from pysparse.sparse.pysparseMatrix import PysparseMatrix #as pysparseMatrix
    
if int(pysparse.__version__[2]) <=1:
    from pysparse.pysparseMatrix import PysparseMatrix
#import sempy.krylov
import time

class CallBack():
    def __init__(self):
        self.iterations = 0
    def it_count(self,u):
        self.iterations=self.iterations + 1
    

class Krylov:
    '''      
    Krylov methods. 
    
    :param pre: Preconditioning matrix, i.e. :math:`P\sim A^{-1}`.
    :type pre: :class:`sempy.precond.Preconditioner`  
    :param float tol: Iterative tolerance. 
    :param integer maxiter: Maximum number of iterations. 
    :param string solver_type: 'cg', 'cgs', 'bicgstab'
    
    :attribute: * **ex_time** (*float*) - Execution time.
    
    :return: The solution vector and a *flag*. 
    
    **Example**::
    
      import sempy
      
      X = sempy.Space( filename = 'square', n = 30, dim = 2 )
      
      laplace = sempy.operators.Laplacian( X )
      A = laplace.matrix

      f = sempy.Function( X, basis_coeff = 1.0 )
      b = sempy.operators.Mass( X ).action_local( f.basis_coeff )
      u = sempy.Function( X, basis_coeff = 0.0 )

      # Solve the system
      solver = sempy.linsolvers.Krylov( solver_type = 'cg' )
      [v, flag] = solver.solve( A, b, u.glob() )
      u.basis_coeff = X.mapping_q(v)
    
    '''
    def __init__(self,pre='none',tol=1e-15,maxiter=5000,solver_type='cg',
                 verbose = 'off' ):
        self.tol         = tol
        self.maxiter     = maxiter
        self.pre         = pre
        self.solver_type = solver_type
        self.cb          = CallBack()
        self.linsolver_type = 'iterative'
        self.verbose = verbose
        self.ex_time =0.0
        self.flag = 0

    def solve(self,A,b,u):
        '''
        Solves the system 
        
        .. math::
        
           Au=b
           
        :param A: System matrix. 
        :param b: Right hand side vector.
        :param u: Solution vector.
        '''
        if self.verbose == 'on':
            print ''
            print '**** Krylov solver            ****'
            print '**** Solver type   =',self.solver_type
        t1 = time.clock()
        self.cb.iterations = 0
        if self.pre == 'none':
            if self.solver_type == 'cg':
                [u, self.flag] = sp.cg( A, b, x0 = u, 
                                        tol = self.tol,
                                        maxiter = self.maxiter,
                                        callback = self.cb.it_count )
            if self.solver_type == 'cgs':
                [u, self.flag] = sp.cgs( A, b, x0 = u, 
                                         tol = self.tol,
                                         maxiter = self.maxiter,
                                         callback = self.cb.it_count )
            if self.solver_type == 'bicgstab':
                [u, self.flag] = sp.bicgstab( A, b, x0 = u, 
                                              tol = self.tol,
                                              maxiter = self.maxiter,
                                              callback = self.cb.it_count )
                
        else:
            if self.solver_type == 'cg':
                [u, self.flag] = sp.cg( A, b, x0 = u, 
                                        tol = self.tol, 
                                        maxiter = self.maxiter,
                                        callback = self.cb.it_count, 
                                        M = self.pre )
                
                #print 'cg res=',np.norm(s)
                #[u, flag] = sempy.krylov.pcg(A,b,u,self.pre,tol=self.tol/10.0,max_iter=self.maxiter)
            if self.solver_type == 'cgs':
                [u, self.flag] = sp.cgs( A, b, x0 = u, 
                                         tol = self.tol,
                                         maxiter = self.maxiter,
                                         callback = self.cb.it_count, 
                                         M = self.pre )
            if self.solver_type == 'bicgstab':
                [u, self.flag] = sp.bicgstab( A, b, x0 = u, 
                                              tol = self.tol,
                                              maxiter = self.maxiter,
                                              callback = self.cb.it_count,
                                              M = self.pre )
        t2 = time.clock()
        #self.ex_time =self.ex_time + (t2-t1)
        self.ex_time =  (t2-t1)
        self.flag = self.cb.iterations
        #s=A*u
        #r=b-s
        #print 'real dot(r)=',np.inner(r,r)
        #flag = flag
        if self.verbose == 'on':
            print '**** Iterations    =',self.flag
            print '**** Solution time =',t2-t1
        
        return u, self.flag
        

        
class Direct:
    '''
    Direct solver. 
    
    :param Space: Discrete function space. 
    :param solver_type: superlu, umfpack. 
    '''
    def __init__(self,Space,solver_type='superlu'):
        self.solver_type = solver_type
        self.Space = Space
        self.linsolver_type = 'direct'
        
    def __convert_to_ll_mat__(self,A):
        Q = pysparse.spmatrix.ll_mat(self.Space.dof, self.Space.dof)
                
        val,irow,jcol = A.find()
        Q.update_add_at(val,irow,jcol)
            
        if self.Space.dim == 1:
            for k in range(self.Space.noe_bc):
                [i, phys, bc_type, element_edge]=self.Space.theta_phys_bc(k)
                if bc_type == "Dir":
                    Q[int(i),int(i)] = 1.0
        if self.Space.dim == 2:
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n):
                    [i, phys, bc_type, element_edge]=self.Space.theta_phys_bc(k,m)
                    if bc_type == "Dir":
                        Q[int(i),int(i)] = 1.0
        if self.Space.dim == 3:
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n):
                    for n in range(self.Space.n):
                        [i, phys, bc_type, element_edge]=self.Space.theta_phys_bc(k,m,n)
                        if bc_type == "Dir":
                            Q[int(i),int(i)] = 1.0

        return Q
        
    def solve(self,A,b,u):
        '''
        Solves the system 
        
        .. math::
           Au=b
           
        :param A: System matrix. 
        :param b: Right hand side vector.
        :param u: Solution vector.
        '''
        matrix = self.__convert_to_ll_mat__(A)
        if self.solver_type == 'superlu':    
            LU = pysparse.superlu.factorize(matrix.to_csr())
        if self.solver_type == 'umfpack':
            LU = pysparse.umfpack.factorize(matrix)
        
        # Temporary array
        F_t = np.zeros((self.Space.dof),float)
        F_t[:]=b[:]
        # Add Dirichlet values to the RHS
        if self.Space.dim == 1:
            for k in range(self.Space.noe_bc):
                [i, phys, bc_type, element_edge]=self.Space.theta_phys_bc(k)
                if bc_type == "Dir":
                    F_t[i] = u[i]
        if self.Space.dim == 2:
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n):
                    [i, phys, bc_type, element_edge]=self.Space.theta_phys_bc(k,m)
                    if bc_type == "Dir":
                        F_t[i] = u[i]
        if self.Space.dim == 3:
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n):
                    for n in range(self.Space.n):
                        [i, phys, bc_type, element_edge]=self.Space.theta_phys_bc(k,m,n)
                        if bc_type == "Dir":
                            F_t[i] = u[i]
        # Solve            
        LU.solve(F_t,u)
        flag = LU.nnz
        return u, flag
        
        