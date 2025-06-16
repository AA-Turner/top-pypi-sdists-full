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

import fluid_f90
import fluid_operator_f90
import fluid_def_f90
import sempy
import scipy.sparse.linalg as spl
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

import sempy.operators.operators_f90 as operators_f90
import sempy.space.space_f90 as space_f90

from sempy.precond import precond_f90
import sempy.space.space_f90 as space_f90

import pysparse
from pysparse.direct import umfpack
# Compatibility with older versions
if int(pysparse.__version__[2]) >=2:
    from pysparse.sparse.pysparseMatrix import PysparseMatrix 
    from pysparse import direct
    
if int(pysparse.__version__[2]) <=1:
    from pysparse.pysparseMatrix import PysparseMatrix



import time


class PressurePoisson:
    '''
    The pressure Poisson operator.
    
    .. math::
    
       P = DM^{-1}G
    '''
    def __init__( self, SpaceGL, D, M_inv, G ):
        self.SpaceGL = SpaceGL
        self.D = D
        self.M_inv = M_inv
        self.G = G
        
        P = spl.LinearOperator( 
                          ( self.SpaceGL.dof,self.SpaceGL.dof ),
                            matvec = self.__action_poisson,
                            dtype = 'float' )
        return P
        
    
    def __action_poisson(self,q_in):
        #
        if self.SpaceGL.dim == 2:
            # 1
            s_x = self.G[0] * q_in
            s_y = self.G[1] * q_in
            # 2
            v_x = self.M_inv * s_x
            v_y = self.M_inv * s_y
            # 3
            q_out = self.D[0] * v_x + self.D[1] * v_y
            
        return q_out

#class DeflationPrecond:
#    '''
#    Precond.
#    '''
#    def __init__(self,SpaceGL):
#        self.SpaceGL = SpaceGL
#        X_gl_fem = sempy.fluid.SpaceGLFEM( self.SpaceGL )
#        A_fem = sempy.operators.Laplacian( X_gl_fem, 
#                                           assemble = 'yes' ).matrix
#        self.P = sempy.precond.Preconditioner( X_gl_fem, [A_fem] ).matrix
#        #del A_fem
#        self.matrix = spl.LinearOperator( 
#                            ( self.SpaceGL.dof,self.SpaceGL.dof ),
#                              matvec = self.__action__,
#                              dtype = 'float' )
#        
#        
#    def __action__(self,v_in):
#        # MAtrix vector product
#        v = self.P * v_in
#        # Compatibility
#        v_local = self.SpaceGL.mapping_q( v )
#        if self.SpaceGL.dim == 2:
#            v_local = fluid_def_f90.pre_compatibility_2d(v_local)
#        v_out = self.SpaceGL.mapping_qt( v_local )
#        return v_out
#        

def pcg(A,b,u,precond,tol=1e-12,max_iter=5000):
    '''
    pcg
    '''
    n = b.size
    p = np.zeros( (n), float)
    s = np.zeros( (n), float)
    r = np.zeros( (n), float)
    z = np.zeros( (n), float)

    s = A*u
    r[:] = b[:] - s[:]
    z = precond*r
    R_new = np.inner(r,z)
    for i in range(max_iter): 
        R_old = R_new
        R_new = np.inner(r,z)
        if abs(R_new) < tol*tol : 
            flag = i
            #s=A*u#r=b-s
            print 'PCG: Conv at iter.=',i,'sqrt dot(r)=',R_new #,\
                  #'real dot(r)=',np.inner(r,r)
            return [u,flag]
        beta = R_new / R_old
        p[:] = z[:] + beta * p[:]
        s = A*p
        Dd = np.inner( p, s )
        alpha = R_new/Dd
        u[:] = u[:] + alpha * p[:]
        r[:] = r[:] - alpha * s[:]
        #print 'i=',i,'sum=',z.sum()
        z = precond * r
        print 'r.sum()=',r.sum()
     
    if i == max_iter-1: 
        flag= i
        print 'pcg() did not converge. dot(r)=',np.inner(r,r)
        
    return [u,flag] 

 
def cg(A,b,u,tol=1e-10,max_iter=5000):
    '''
    cg
    '''
    n = b.size
    p, s, r = np.zeros((n),np.float), np.zeros((n),np.float), \
              np.zeros((n),np.float)

    s = A * u
    r = b - s
    R_new = np.inner(r,r)
    for i in range(max_iter): 
        R_old = R_new
        R_new = np.inner(r,r)
        if abs(R_new) < tol * tol : 
            flag = i
            print 'CG: Conv. at iter.=',i,'dot(r)=', R_new
            return [u,flag]
        beta = R_new/R_old
        p = r + beta*p
        s = A*p
        Dd = np.inner(p,s)
        alpha = R_new/Dd
        u = u + alpha*p
        r = r - alpha*s
    if i == max_iter-1: 
        flag= i
        print 'cg() did not converge. dot(r)=',np.inner(r,r)
    return [u,flag]        
        
class Deflation:
    '''
    Deflation solver.
    
    Can be applied to solve equations of type 
    
    .. math::
       Sp=b
    
    where 
    
    .. math::
       S=DB^{-1}G
       
    Here, :math:`D` is the divergence operator, :math:`G` is the gradient 
    operator and :math:`B` is either the GLL mass matrix (when used in 
    conjuction with the projection method 
    (:class:`sempy.solvers.ProjectionMethod`)   
    or a Helmholtz operator,  when used in 
    :class:`sempy.solvers.UzawaSolver`. 
    
    One way to solve the above equation is to decompose the solution 
    into coarse and fine constituents:
    
    .. math::
       p=Jp_c + p_f
    
    In short, this leads to two subproblems
    
    .. math:: 
       S_cp_c = J^T(b-Sp_f)\quad (\\text{coarse problem})
       
       S_fp_f = (I-SJS^{-1}_cJ^T)b\quad (\\text{fine problem})
    
    where 
    
    .. math::
       S_c = J^T S J
       
       S_f = (I-SJ S^{-1}_c J^T)S  
    
    The algorithm is as follows
    
      1. Solve the fine problem for :math:`p_f` using preconditioned 
         CG iterations. 
      2. Solve the coarse problem to obtain :math:`p_c`. This is done 
         by a direct method since :math:`S_c\in\mathbb R^{noe\\times noe}`. 
      3. Combine the two solution by the expression 
         :math:`p=Jp_c + p_f`.
          
    In step 1 above, a preconditioner constructed of elemetal 
    Laplacian matrices based on the GL points, with purely homogeneous 
    Neumann conditions, are used.  
               
    :param Space: Discrete space.
    :type Space: :class:`sempy.Space`
    :param SpaceGL: Discrete space.
    :type SpaceGL: :class:`sempy.fluid.SpaceGL`
    :param S: Pressure Poisson operator or the Schur complement. 
    :type S: Scipy LinearOperator
    
    :arguments: * **operator_type** (*string*) - Operator type. Either
                  :literal:`poisson` or :literal:`uzawa`. 
                * **time_step_size** (*float*) - Time step size. Used to
                  create the preconditioner for Uzawa solvers. 
    
    :attributes: * **J** (*Scipy LinearOperator*) - Mapping. 
                           
                   .. math::
                      p=Jp_c
                              
                   where :math:`p\in\mathbb R^{dof}`,
                   :math:`J\in\mathbb R^{dof\\times noe}` and 
                   :math:`p_c\in\mathbb R^{noe}`.  
                              
                 * **JT** (*Scipy LinearOperator*) - The transpose 
                   of :math:`J`.
                   
                   .. math::
                      p_c=J^Tp
                              
                   where :math:`p_c\in\mathbb R^{noe}`,
                   :math:`J^T\in\mathbb R^{noe\\times dof}` and 
                   :math:`p\in\mathbb R^{dof}`.
                     
                 * **S_c** (*Pysparse matrix*)- Coarse operator.
                 * **S_c_inv** (*Pysparse matrix*) - Inverse of the 
                   coarse operator.
                 * **S_f** (*Scipy LinearOperator*) - Fine operator.
                 * **S_f_pre** (*Scipy LinearOperator*) - Preconditioner
                 
    **Usage**::
    
       import sempy 
       
       # Spaces
       X = sempy.Space( filename = filename, n = 10, dim = 2 )
       X_gl = sempy.fluid.SpaceGL( X , zero = 'yes' )

       # Trial functions and time object
       U = sempy.VectorFunction( X )
       p = sempy.Function( X_gl )
       Y = sempy.ode.Time( )

       # Create a projection method instance:
       pro = sempy.solvers.ProjectionMethod( X, X_gl, Y, U, p )
       S = pro.poisson_operator
       
       # An instance of the deflation class:
       deflation = sempy.fluid.Deflation( X, X_gl, S )    
       
    '''
    def __init__( self, Space, SpaceGL, S , 
                  operator_type= 'poisson',
                  time_step_size = 0.1,
                  tol = 1e-10,
                  mu_gl = 'none'):
        print '*** Creating deflation solver..'
        self.Space = Space
        self.SpaceGL = SpaceGL
        self.S = S
        self.operator_type = operator_type
        self.time_step_size = time_step_size 
        self.tol = tol
        # Transport coefficient
        if mu_gl == 'none':
            self.mu_gl = sempy.Function( self.SpaceGL, basis_coeff =  1.0 )
        else:
            self.mu_gl = mu_gl
        # Mapping operator
        self.J = spl.LinearOperator( (self.SpaceGL.dof,self.SpaceGL.noe),
                                      matvec = self.__action_of_j,
                                      dtype = 'float')     
        self.JT = spl.LinearOperator( (self.SpaceGL.noe,self.SpaceGL.dof),
                                      matvec = self.__action_of_jt,
                                      dtype = 'float')     
        self.S_c = self.__coarse_operator()
        # Inverse
        self.LU_coarse = self.__inverse_coarse_operator__()
        self.S_c_inv = spl.LinearOperator( 
                                ( self.SpaceGL.noe, self.SpaceGL.noe ),
                                  matvec = self.__action_coarse_inverse__, 
                                  dtype = 'float' )
        self.S_f = spl.LinearOperator( 
                                ( self.SpaceGL.dof, self.SpaceGL.dof ),
                                  matvec = self.__action_fine__, 
                                  dtype = 'float' )
        
        # Preconditioner
        if self.operator_type == 'poisson':
            self.S_f_pre = self.preconditioner_poisson()
        if self.operator_type == 'uzawa':
            self.S_f_pre = self.preconditioner_uzawa()
            
        self.poisson_solver = sempy.linsolvers.Krylov( 
                                        pre = self.S_f_pre,
                                        tol = self.tol, 
                                        solver_type = 'cg',
                                        maxiter=1000)
        if self.operator_type == 'uzawa':
            self.poisson_solver.maxiter = 300
        print '*** Finished creating deflation solver.'
        
    
    def preconditioner_poisson(self):
        '''
        Preconditioner for the fine problem when 
        :math:`S=DM^{-1}G`.
        
        :returns: A Scipy LinearOperator. 
        '''
        X_gl_fem = sempy.fluid.SpaceGLFEM( self.SpaceGL )
        A_fem = sempy.operators.Laplacian( X_gl_fem, 
                                           assemble = 'yes' ).matrix
        self.P = sempy.precond.Preconditioner( X_gl_fem, 
                                               [A_fem],
                                               #library = 'superlu' ).matrix
                                               library = 'umfpack' ).matrix
        del A_fem
        pre_matrix = spl.LinearOperator( 
                            ( self.SpaceGL.dof,self.SpaceGL.dof ),
                              matvec = self.__action_precond__,
                              dtype = 'float' )
        return pre_matrix
    
    def preconditioner_uzawa(self):
        '''
        Preconditioner for the fine problem when 
        :math:`S=DH^{-1}G`.
        
        :returns: A LinearOperator. 
        '''
        X_gl_fem = sempy.fluid.SpaceGLFEM( self.SpaceGL )
    
        # Laplacian
        A_fem = sempy.operators.Laplacian( X_gl_fem, 
                                           assemble = 'yes' ).matrix
        #
        self.P_1 = sempy.precond.Preconditioner( 
                            X_gl_fem, 
                            [A_fem], 
                            library = 'umfpack' ).matrix
        #
        coeff = self.mu_gl.glob()
        self.P_2 = sempy.precond.Preconditioner( 
                            self.SpaceGL, 
                            [self.SpaceGL.mass_matrix],
                            #scaling_factor= [self.time_step_size*coeff[0]],
                            library = 'superlu' ).matrix
        #self.P = sempy.operators.MultipleOperators([P_2],#[P_1,P_2], 
        #                                           assemble = 'no'
        #                                           ).matrix
        
        del A_fem
        pre_matrix = spl.LinearOperator( 
                            ( self.SpaceGL.dof,self.SpaceGL.dof ),
                              matvec = self.__action_precond_uzawa__,
                              dtype = 'float' )
        return pre_matrix
    
    def __action_precond_uzawa__(self,v_in):
        co = self.mu_gl.glob()
        coeff = co[0]
        # Matrix vector product
        v_1 = self.P_1 * v_in
        v_2 = coeff*self.time_step_size * (self.P_2 * v_in)
        v = v_1 +v_2
        # Compatibility
        v_out = self.compatibility( v )
        return v_out
        
    def __action_precond__(self,v_in):
        # Matrix vector product
        v = self.P * v_in
        # Compatibility
        v_out = self.compatibility( v )
        return v_out
    
        
    def __solve_coarse__( self, b, phi_f ):
        # rhs
        b_rhs = self.JT * ( b - ( self.S * phi_f ) )
        # Compatibility condition
        #if self.SpaceGL.zero == 'yes':
        #    b_sum = b_rhs.sum()
        #    b_rhs = b_rhs - b_sum / np.float( self.SpaceGL.noe )
        #print 'coarse sum rhs=',b_rhs.sum()
        phi_c = self.S_c_inv * b_rhs
        return phi_c
    
    def solve_standard( self, b ,x ):
        '''
        Solve the pressure Poisson equation with standard CG iterations, 
        i.e. non-preconditioned.
        
        .. math::
           Sx=b
        
        This method can be used to compare the efficiency of the 
        preconditioned deflation solver. 
        
        :param b: Right hand side. For projection methods: 
                  b=D*u_hat 
        :type b: array
        :param x: Solution vector.
        :type x: array
        :returns: Solution vector and a flag.
        
        **Example**::
        
           # To solve S*phi = b:
           [phi, flag] = deflation.solve_standard( b, phi )
           
        '''
        t1 = time.clock()
        self.poisson_solver.pre = 'none'
        [ phi, flag ] = self.poisson_solver.solve( self.S, b, x )
        t2 = time.clock()
        print 'time standard=',t2-t1
        return [phi, flag]
    
    def compatibility( self, v ):
        '''
        A method to enforce a local compatibility condition when solving 
        the fine problem in the deflation solver. This is necessary since the 
        preconditioner is blockwise semi-definite. 
        '''
        v_local = self.SpaceGL.mapping_q( v )
        
        if self.SpaceGL.dim == 1:
            print 'Deflation: compatibility() not implemented for 1D.'
        
        if self.SpaceGL.dim == 2:
            v_local = fluid_def_f90.pre_compatibility_2d(v_local)
            
        if self.SpaceGL.dim == 3:
            v_local = fluid_def_f90.pre_compatibility_3d(v_local)
                
        v_out = self.SpaceGL.mapping_qt( v_local )
        
        return v_out
                
    def solve( self, b, x ):
        '''
        Solve the pressure Poisson equation with the deflation method.
        
        :param b: Right hand side. For projection methods: 
                  b=D*u_hat 
        :type b: array
        :param x: Solution vector.
        :type x: array
        :returns: Solution vector and a flag.'
        
        **Example**::
        
           # To solve S*phi = b:
           [phi, flag] = deflation.solve( b, phi )
           
        '''
        #t1 = time.clock()
        
        # Right hand side: b = D * u
        s1 = self.S * ( self.J * ( self.S_c_inv * (self.JT * b ) ) )
        b_rhs = np.zeros( ( self.SpaceGL.dof ), float )
        b_rhs[:] = b[:] - s1[:]
        b_rhs = self.compatibility( b_rhs ) 
        # Solve fine problem
        [ phi_f, flag ] = self.poisson_solver.solve( self.S_f, b_rhs, x )
        #[ phi_f, flag ] = self.pcg( self.S_f, b_rhs, x, Pre )
        #[ phi_f, flag ] = cg( self.S_f, b_rhs, x )
        #flag = 0
        #phi_f = self.S_f_pre * b_rhs
        
        # Solve coarse problem
        phi_c = self.__solve_coarse__( b, phi_f )
        
        # Combine
        phi = self.J * phi_c + phi_f
        # Test rhs
        #b_local = self.SpaceGL.mapping_q(b_rhs)
        #for k in range(self.SpaceGL.noe):
        #    alpha = 0.0
        #    for m in range(self.SpaceGL.n):
        #        for n in range(self.SpaceGL.n):
        #            alpha = alpha + b_local[k,m,n]
        #    print 'k=',k,'alpha=',alpha
        # Test phi_f
        #b_local = self.SpaceGL.mapping_q( phi_f )
        #for k in range(self.SpaceGL.noe):
        #    alpha = 0.0
        #    for m in range(self.SpaceGL.n):
        #        for n in range(self.SpaceGL.n):
        #            alpha = alpha + b_local[k,m,n]
        #    print 'k=',k,'phi alpha=',alpha
        #t2 = time.clock()
        #print 'time def=',t2-t1
        
        return [phi, flag]
    
        
    def __inverse_coarse_operator__(self):
        if pysparse.__version__[2] >='2':
            #LU_coarse = direct.superlu.factorize( self.S_c.to_csr() )
            LU_coarse = umfpack.factorize( self.S_c )
        if pysparse.__version__[2] <='1':
            #LU_coarse = pysparse.superlu.factorize( self.S_c.to_csr() )
            LU_coarse = umfpack.factorize( self.S_c )
        return LU_coarse
        
        
    def __action_coarse_inverse__(self,v):
        # v is the RHS: A*w=v
        w = np.zeros(self.SpaceGL.noe, float)
        self.LU_coarse.solve(v,w)
        #print 'coarse='
        #print w
        #if self.SpaceGL.zero == 'yes':
        #    #print '--> zero'
        #    w.sum()
        #    w=w-w.sum()/float(self.SpaceGL.noe)
            #print 'wsum=',w.sum()
        return w
    
    
    def __action_fine__(self,q):
        # 
        s1 = self.S * q
        s2 = self.S * ( self.J * ( self.S_c_inv* ( self.JT*s1 ) ) )
        s = s1 -s2
        #print 'obbs __action_fine__ compatibility()'
        s = self.compatibility( s )
        return s
        
    
    def __coarse_operator(self):
        #
        noe = self.SpaceGL.noe
        n = self.SpaceGL.n
        A = pysparse.spmatrix.ll_mat( noe, noe )
        
        if self.SpaceGL.dim == 1:
            v = np.zeros( ( noe, n ), float )
            for k in range( noe ):
                v[:,:]=0.0
                v[k,:]=1.0
                v_glob = self.SpaceGL.local_to_global( v ) 
                w = self.S * v_glob
                Ad = self.JT * w
                for i in range(noe):
                    A[i,k] = Ad[i]
                    
        if self.SpaceGL.dim == 2:
            v = np.zeros( ( noe, n, n ), float )
            for k in range( noe ):
                v[:,:,:]=0.0
                v[k,:,:]=1.0
                v_glob = self.SpaceGL.local_to_global( v ) 
                w = self.S * v_glob
                Ad = self.JT * w
                for i in range(noe):
                    A[i,k] = Ad[i]
                    
        if self.SpaceGL.dim == 3:
            v = np.zeros( ( noe, n, n, n ), float )
            for k in range( noe ):
                v[:,:,:,:]=0.0
                v[k,:,:,:]=1.0
                v_glob = self.SpaceGL.local_to_global( v ) 
                w = self.S * v_glob
                Ad = self.JT * w
                for i in range(noe):
                    A[i,k] = Ad[i]
        #print 'A='
        #print A
        # Check if singular
        s = np.zeros((noe),float)
        for i in range(noe):
            for j in range(noe):
                s[i] = s[i] + A[i,j]
        
        if abs(s.sum()) <= 1e-10:
            print '-> Coarse pressure matrix is singular:',s.sum()
        
        return A
            
    def __action_of_jt(self,v):
        #
        v_loc = self.SpaceGL.mapping_q( v )
        if self.SpaceGL.dim == 1:
            w = fluid_def_f90.action_f_jt_1d(v_loc) 
        if self.SpaceGL.dim == 2:
            w = fluid_def_f90.action_f_jt_2d(v_loc) 
        if self.SpaceGL.dim == 3:
            w = fluid_def_f90.action_f_jt_3d(v_loc) 
        return w
        
        
    def __action_of_j(self,v):
        #
        if self.SpaceGL.dim == 1:
            w = fluid_def_f90.action_f_j_1d( v, self.SpaceGL.n ) 
         
        if self.SpaceGL.dim == 2:
            w = fluid_def_f90.action_f_j_2d( v, self.SpaceGL.n ) 
        
        if self.SpaceGL.dim == 3:
            w = fluid_def_f90.action_f_j_3d( v, self.SpaceGL.n )
        
        w_out = self.SpaceGL.local_to_global(w)
        return w_out 
            
        
class SpaceGL:
    '''
    A space for pressure.
     
    :argument Space: Discrete space.
    :type Space: :class:`sempy.Space`
    
    :attributes: * **n** (*int*)- Number of nodal points in each direction 
                   of an element. 
                 * **dim** (*int*) - Dimension :math:`d` of the computational 
                   domain :math:`\Omega\in\mathbb R^d`.  
                 * **zero** (*string*) - Determines the type of space. Either 
                   :literal:`yes`, meaning
                   
                   .. math::
                   
                      \\int_\Omega p\,d\Omega=0
                   
                   or :literal:`no` (default). 
                 * **noe** (*int*)- Number of spectral elements.  
                 * **dof** (*int*)- Degrees of freedom of the GL mesh. 
                 * **points** (*array*)- GL quadrature points 
                   :math:`\\underline{\\xi}\\in\\mathbb R^{N-1},\\ -1< \\xi_j < 1`.
                 * **weights** (*array*)- GL quadrature weights 
                   :math:`\\underline{\\tilde\\rho}\\in\\mathbb R^{N+1}` 
                   corresponding to the points :math:`\\underline{\\tilde\\xi}`. 
                   Used to evaluate an integral over the reference domain, e.g.:
                 
                   .. math::
                      \\hat\\Omega\\in\\mathbb R^1: \\int_{\\hat\\Omega} f d\\hat\\Omega\\approx
                      \\sum_i\\tilde\\rho_if_i
                      
                      \\hat\\Omega\\in\\mathbb R^2: \\int_{\\hat\\Omega} f d\\hat\\Omega\\approx
                      \\sum_i\\sum_j\\tilde\\rho_i\\tilde\\rho_jf_{ij}
                 
                 * **x,y,z** (*array*)- Coordinate arrays (given in local 
                   data distribution). 
                 * **I_tilde** (*array*)- Interpolation matrix. 
                   Used to interpolate a function from GLL points to GL
                   points.
                 
                   .. math::
                      
                      w_{i}=\\sum_{m=0}^{N}\\tilde I_{im}u_{m}
                      
                 * **I_tilde_gll** (*array*)- Interpolation matrix. Used to 
                   interpolate a function from GL points to GLL points.
                 * **D_tilde** (array)- Derivative matrix (numpy array). 
                   Used to interpolate derivatives from GLL to GL.
                   
                   .. math::
                   
                      \\frac{\partial u}{\partial\\xi}\\bigg|_{\\alpha\\beta}=
                      \sum_{m=0}^N\sum_{n=0}^N\\frac{\partial\ell_m}{\partial\\xi}
                      (\\xi_\\alpha)\ell_n(\\eta_\\beta)u_{mn}=
                      \sum_{m=0}^N\sum_{n=0}^N\\tilde D_{\\alpha m}
                        \\tilde I_{\\beta n}u_{mn}
                      
                   here :math:`(\\alpha,\\beta)` denotes the GL points. 
                   
                 * **theta** (*array*)- Connectivity array.   
                 * **mass_matrix** (*Pysparse matrix*) - GL mass matrix.
                 * **mass_inv** (*Scipy LinearOperator*) - Inverse of the GL 
                   mass matrix.  
                      
    **Example**::
    
       import sempy
       
       X = sempy.Space( filename = 'square', n = 10, dim = 2 )
       
       X_gl = sempy.fluid.SpaceGL( X )
       
       X_gl.plot_mesh()
                   
    '''
    def __init__(self,Space, zero = 'no'):
        self.Space = Space
        self.n   = self.Space.n - 2 
        self.noe = self.Space.noe
        self.dim = self.Space.dim
        self.type = 'GL'
        self.zero = zero
        self.noe_bc = 0
        self.basic = sempy.Basic()
        
        if self.Space.n <= 3:
            print 'Polynomial degree to low to create interpoaltion matrix'
            print 'Remedy: increase the polynomial degree to >=3.'
        else:
            self.points, self.weights = self.basic.gauss_legendre(self.n)
            self.I_tilde = self.__interpolation_matrix()
            self.I_tilde_gll = self.__interpolation_matrix_gll()
            self.__coordinates()
            self.D_tilde = self.__derivative_matrix_tilde()
            # Connectivity
            self.theta = self.__connectivity()
            # DOF
            if self.dim == 1:
                self.dof = self.n*self.noe
            if self.dim == 2:
                self.dof = (self.n*self.n)*self.noe
            if self.dim == 3:
                self.dof = (self.n*self.n*self.n)*self.noe
            # The GL mas matrix
            self.mass_matrix = self.__mass_matrix__()
            # inverse of mass matrix gl
            self.mass_inv = self.__mass_matrix_inv__( self.mass_matrix )
           
            #self.mass_inv = spl.LinearOperator( 
            #              ( self.dof,self.dof ),
            #                matvec = self.__action_mass_matrix_inv,
            #                dtype = 'float' )
        
        self.fem = SpaceGLFEM( self )
    
    def __mass_matrix_inv__( self, M ):
        M_inv = PysparseMatrix( size = self.dof )
        #M_inv = pysparse.spmatrix.ll_mat( self.dof, self.dof )
        
        for i in range( self.dof ):
            M_inv[i,i] = 1.0/M[i,i]
            
        return M_inv
    
        
    def __mass_matrix__( self ):
        #M = pysparse.spmatrix.ll_mat( self.dof, self.dof )
        M = PysparseMatrix( size = self.dof )
        
        if self.dim == 1:
            mass_local = np.zeros( ( self.noe, self.n ), float )
            for k in range(self.noe):
                for m in range(self.n):
                        mass_local[k,m] = self.jac[k,m]*\
                                          self.weights[m]
                                           
        if self.dim == 2:
            mass_local = np.zeros( (self.noe,self.n,self.n), float )
            for k in range(self.noe):
                for m in range(self.n):
                    for n in range(self.n):
                        mass_local[k,m,n] = self.jac[k,m,n]*\
                                            self.weights[m]*\
                                            self.weights[n]
        
        if self.dim == 3:
            mass_local = np.zeros( (self.noe,self.n,self.n,self.n), float )
            for k in range(self.noe):
                for m in range(self.n):
                    for n in range(self.n):
                        for o in range(self.n):
                            mass_local[k,m,n,o] = self.jac[k,m,n,o]*\
                                                  self.weights[m]*\
                                                  self.weights[n]*\
                                                  self.weights[o]
                                               
        mass_global = self.local_to_global( mass_local )
        for i in range(self.dof):
            M[i,i] = mass_global[i]
        return M
            
    def __action_mass_matrix_inv(self,u_in):
        u = self.mapping_q(u_in)
        if self.dim == 1:
            b = fluid_operator_f90.action_mass_matrix_gl_inv_1d(u,
                                                    self.weights,self.jac)
            
        if self.dim == 2:
            b = fluid_operator_f90.action_mass_matrix_gl_inv_2d(u,
                                                    self.weights,self.jac)
            
        if self.dim == 3:
            b = fluid_operator_f90.action_mass_matrix_gl_inv_3d(u,
                                                    self.weights,self.jac)
        u_out = self.mapping_qt(b)    
        
        return u_out
        
        
    def __connectivity(self):
        '''
        Connectivity array.
        '''
        if self.dim == 1:
            i = 0
            theta = np.zeros((self.noe,self.n),int)
            for k in range(self.noe):
                for m in range(self.n):
                    theta[k,m] = i
                    i = i + 1
        if self.dim == 2:
            i = 0
            theta = np.zeros((self.noe,self.n,self.n),int)
            for k in range(self.noe):
                for m in range(self.n):
                    for n in range(self.n):
                        theta[k,m,n] = i
                        i = i + 1
        if self.dim == 3:
            i = 0
            theta = np.zeros((self.noe,self.n,self.n,self.n),int)
            for k in range(self.noe):
                for m in range(self.n):
                    for n in range(self.n):
                        for o in range(self.n):
                            theta[k,m,n,o] = i
                            i = i + 1
                        
        return theta
            
    def gradient_vector(self,u):
        '''
        Gradient vector.
        
        :param u: Basis coefficients in local data structure.
        '''
        if self.Space.dim == 1:
            u_gll = self.interpolation_gll( u )
            u_x = self.Space.gradient_vector( u_gll )
            u_x_gl = self.interpolation( u_x )
            return u_x_gl
        
        if self.Space.dim == 2:
            u_gll = self.interpolation_gll( u )
            u_x, u_y = self.Space.gradient_vector( u_gll )
            u_x_gl = self.interpolation( u_x )
            u_y_gl = self.interpolation( u_y )
            return u_x_gl, u_y_gl
        
        if self.Space.dim == 3:
            u_gll = self.interpolation_gll( u )
            u_x, u_y, u_z = self.Space.gradient_vector( u_gll )
            u_x_gl = self.interpolation( u_x )
            u_y_gl = self.interpolation( u_y )
            u_z_gl = self.interpolation( u_z )
            return u_x_gl, u_y_gl, u_z_gl
        
    def quadrature(self,f):
        """Computes the value of the integral 
        
           .. math::
              \\kappa = \\int_\\Omega f\\,d\\Omega 
           
           for :math:`f\\in L^2(\\Omega)` with GL quadrature rules. 
        
           :param f: Basis coefficients of the function to be integrated given in local
                     data representation (since f in L2). 
           :returns: Value :math:`\\kappa` of the integral.
        
        """
        if self.dim ==1:
            kappa = space_f90.quadrature_1d(self.weights,self.jac,f)
        if self.dim ==2:
            kappa = space_f90.quadrature_2d(self.weights,self.jac,f)
        if self.dim ==3:
            kappa = space_f90.quadrature_3d(self.weights,self.jac,f)
        return kappa
    
    def l2_norm(self,u):
        """Computes the :math:`L^2` - norm
           
           .. math::
              ||u||_{L^2(\\Omega)}=\\bigg(\\int_{\\Omega} u^2d\\Omega\\bigg)^{1/2}
              
           using GL quadrature. 
           
           :param u: Basis coefficients in local data structure.
           :returns: The :math:`L^2` - norm as a floating number.
           
           Usage::
           
             u  = np.ones((mesh.dof),float)
             print 'L2-norm=',mesh.l2norm(u)

        """
        if self.dim ==1:
            norm = space_f90.l2norm_1d(self.weights,self.jac,u)
        if self.dim ==2:
            norm = space_f90.l2norm_2d(self.weights,self.jac,u)
        if self.dim ==3:
            norm = space_f90.l2norm_3d(self.weights,self.jac,u)
            
        return norm
    
    def local_to_global(self,u_loc):
        '''
        Maps from local to global. Identical to 
        :class:`SpaceGL.mapping_qt`. This method only exist to make the 
        present class compatible with the :class:`sempy.Function` class.  
                
        :param array u_loc: Basis coefficients in local data 
                            representation.
        :returns: (*array*) - The mapped basis coefficients in global data
                  representation. 
                             
        '''
        if self.dim == 1:
            #u_glob = np.zeros((self.dof),float)
            #for k in range(self.noe):
            #    for m in range(self.n):
            #        i = self.theta[k,m]
            #        u_glob[i] = u_loc[k,m]
            u_glob = space_f90.local_to_global_1d(u_loc,self.theta,self.dof)
            return u_glob
        
        if self.dim == 2:
            #u_glob = np.zeros((self.dof),float)
            #for k in range(self.noe):
            #    for m in range(self.n):
            #        for n in range(self.n):
            #            i = self.theta[k,m,n]
            #            u_glob[i] = u_loc[k,m,n]
            u_glob = space_f90.local_to_global_2d(u_loc,self.theta,self.dof)
            return u_glob
        
        if self.dim == 3:
            u_glob = space_f90.local_to_global_3d(u_loc,self.theta,self.dof)
            return u_glob
        
    def mapping_qt(self,u_loc):
        '''
        Maps from local to global
        
        :param array u_loc: Basis coefficients in local data representation.
        :returns: (*array*) - The mapped basis coefficients in global data
                  representation. 
        
        '''
        if self.dim == 1:
            #u_glob = np.zeros((self.dof),float)
            #for k in range(self.noe):
            #    for m in range(self.n):
            #        i = self.theta[k,m]
            #        u_glob[i] = u_loc[k,m]
            u_glob = space_f90.local_to_global_1d(u_loc,self.theta,self.dof)
            return u_glob
        
        if self.dim == 2:
            #u_glob = np.zeros((self.dof),float)
            #for k in range(self.noe):
            #    for m in range(self.n):
            #        for n in range(self.n):
            #            i = self.theta[k,m,n]
            #            u_glob[i] = u_loc[k,m,n]
            u_glob = space_f90.local_to_global_2d(u_loc,self.theta,self.dof)
            return u_glob
        
        if self.dim == 3:
            #u_glob = np.zeros((self.dof),float)
            #for k in range(self.noe):
            #    for m in range(self.n):
            #        for n in range(self.n):
            #            for o in range(self.n):
            #                i = self.theta[k,m,n,o]
            #                u_glob[i] = u_loc[k,m,n,o]
            u_glob = space_f90.local_to_global_3d(u_loc,self.theta,self.dof)
            return u_glob
    
    def mapping_q(self,u_glob):
        '''
        Maps from global to local
        
        :param array u_glob: Basis coefficients in global data 
                             representation.
        :returns: (*array*) - The mapped basis coefficients in local data
                  representation. 
        
        '''
        if self.dim == 1:
            #u_loc = np.zeros( (self.noe,self.n), float )
            #for k in range(self.noe):
            #    for m in range(self.n):
            #        i = self.theta[k,m]
            #        u_loc[k,m] = u_glob[i]
            u_loc = space_f90.mapping_q_1d(u_glob,self.theta)
            return u_loc
        
        if self.dim == 2:
            #u_loc = np.zeros( (self.noe,self.n,self.n), float )
            #for k in range(self.noe):
            #    for m in range(self.n):
            #        for n in range(self.n):
            #            i = self.theta[k,m,n]
            #            u_loc[k,m,n] = u_glob[i]
            u_loc = space_f90.mapping_q_2d(u_glob,self.theta)
            return u_loc
        
        if self.dim == 3:
            #u_loc = np.zeros( (self.noe,self.n,self.n,self.n), float )
            #for k in range(self.noe):
            #    for m in range(self.n):
            #        for n in range(self.n):
            #            for o in range(self.n):
            #                i = self.theta[k,m,n,o]
            #                u_loc[k,m,n,o] = u_glob[i]
            u_loc = space_f90.mapping_q_3d(u_glob,self.theta)
            return u_loc
        
    def plot_mesh(self):
        '''
        Plots the GL mesh.
        '''
        if self.dim == 1:
            u = np.zeros((self.noe,self.n),float)
            for k in range(self.noe):
                plt.plot(self.x[k,:],u[k,:],'o-')
            # test interpolate
            #x_gll=self.interpolation_gll(self.x)
            #u = np.zeros((self.noe,self.n+2),float)
            #for k in range(self.noe):
            #    plt.plot(x_gll[k,:],u[k,:],'o-')
            plt.show()
            
        if self.dim == 2:
            fig = plt.figure()
            ax = axes3d.Axes3D(fig)
            u = np.zeros((self.noe,self.n,self.n),float)
            #u = self.x
            #u_glob = self.mapping_qt(self.x)
            #u = self.mapping_q(u_glob)
            for k in range(self.noe):
                ax.plot_wireframe(self.x[k,:,:],self.y[k,:,:],u[k,:,:])
            # test interpoalte
            #x_gll=self.interpolation_gll(self.x)
            #y_gll=self.interpolation_gll(self.y)
            #u = np.zeros((self.noe,self.n+2,self.n+2),float)
            #for k in range(self.noe):
            #    ax.plot_wireframe(x_gll[k,:,:],y_gll[k,:,:],u[k,:,:])
            
            ax.set_xlabel(r'$x$')
            ax.set_ylabel(r'$y$')
            plt.show()
        if self.dim == 3:
            #try:
            from enthought.mayavi import mlab
            x = self.x#interpolation_gll(self.x)
            y = self.y#interpolation_gll(self.y)
            z = self.z#interpolation_gll(self.z)
            u = z#np.zeros((self.noe,self.n,self.n,self.n),float)
        
            #s = mlab.mesh(x, y, z)
            #levels = np.arange(0, 1, 0.1)
            levels=[0.2,0.4,0.6,0.8]
            for k in range(self.noe):
                #s=mlab.contour3d( x[k,:,:,:], y[k,:,:,:], 
                #                  z[k,:,:,:], u[k,:,:,:],
                #                  contours=levels)
                s=mlab.points3d( x[k,:,:,:], y[k,:,:,:], 
                               z[k,:,:,:], u[k,:,:,:])
            mlab.show()
            #except:
                    
    def __coordinates(self):
        '''
        '''
        if self.dim == 1:
            self.x = self.interpolation(self.Space.x)
            self.y = 0.0 
            self.z = 0.0
            self.jac = self.interpolation(self.Space.jac)
            
        if self.dim == 2:
            self.x = self.interpolation(self.Space.x)
            self.y = self.interpolation(self.Space.y)
            self.z = 0.0
            self.jac = self.interpolation(self.Space.jac)
            
        if self.dim == 3:
            self.x = self.interpolation(self.Space.x)
            self.y = self.interpolation(self.Space.y)
            self.z = self.interpolation(self.Space.z)
            self.jac = self.interpolation(self.Space.jac)
        
        return    
            
        
    def interpolation(self,u_gll):
        '''
        Interpolation from GLL to GL.
        
        :param array u_gll: Basis coefficients of a GLL function given in 
                            local data representation.
        :returns: (*array*) - Basis coefficients of a GL function given in 
                  local data representation.
        '''
        if self.dim == 1:
            u_gl = fluid_f90.interpolation_1d( u_gll, self.I_tilde )
        if self.dim == 2:
            u_gl = fluid_f90.interpolation_2d( u_gll, self.I_tilde )
        if self.dim == 3:
            u_gl = fluid_f90.interpolation_3d( u_gll, self.I_tilde )
            
        return u_gl
    
    def interpolation_gll(self,u_gl):
        '''
        Interpolation from GL to GLL.
        
        :param array u_gl: Basis coefficients of a GL function given in 
                           local data representation.
        :returns: (*array*) - Basis coefficients of a GLL function given in 
                  local data representation.
                            
        '''
        if self.dim == 1:
            u_gll = fluid_f90.interpolation_gll_1d( u_gl, self.I_tilde_gll )
        if self.dim == 2:
            u_gll = fluid_f90.interpolation_gll_2d( u_gl, self.I_tilde_gll )
        if self.dim == 3:
            u_gll = fluid_f90.interpolation_gll_3d( u_gl, self.I_tilde_gll )
            
        return u_gll
                    
    def __interpolation_matrix(self):
        '''
        The interpolation matrix (GLL to GL)
        '''
        gll = self.Space.points # GLL quadrature points
        gl  = self.points # GL quadrature points
        I_tilde = fluid_f90.interpolation_matrix( gll, gl )
        return I_tilde
    
    def __derivative_matrix_tilde(self):
        '''
        The interpolation matrix (GLL to GL)
        '''
        #gll = self.Space.points # GLL quadrature points
        #gl  = self.points # GL quadrature points
        D_tilde = fluid_f90.derivative_matrix_tilde(self.I_tilde,self.Space.D)
        return D_tilde
    
    def __interpolation_matrix_gll(self):
        '''
        The interpolation matrix (GL to GLL)
        '''
        gll = self.Space.points # GLL quadrature points
        gl  = self.points # GL quadrature points
        I_tilde_gll = fluid_f90.interpolation_matrix_gll(gll,gl)
        return I_tilde_gll           


class SpaceGLFEM:
    '''
    Finite element space based on the GL points.
    
    :param SpaceGL: Discrete GL space.
    :type SpaceGL: :class:`sempy.fluid.SpaceGL` 
    '''
    def __init__(self,SpaceGL):
        self.SpaceGL = SpaceGL
        self.type    = 'GL'
        self.dim     = self.SpaceGL.dim
        self.n       = 2
        self.dof     = self.SpaceGL.dof
        self.noe_bc = 0
        self.basic = sempy.Basic()
        
        
        # Number of elements
        __n = self.SpaceGL.n-1
        __noe =self.SpaceGL.noe
        
        if self.dim == 1:
            self.noe = ( __n ) * __noe
            
        if self.dim == 2:
            self.noe = ( __n ) * ( __n ) * __noe
        
        if self.dim == 3:
            self.noe = ( __n ) * ( __n ) * ( __n ) * __noe
            #self.theta_bc = 
        # GLL points and weigts
        #self.points, self.weights = sempy.basic.gauss_legendre(self.n)
        self.points, self.weights = \
                      self.basic.gauss_lobatto_legendre( self.n )
        #print 'SpaceGLFEM p=',self.points
        #print 'SpaceGLFEM w=',self.weights
        #self.x, self.y, self.theta = 
        self.__fem_coor()
        self.D = self.basic.derivative_matrix_gll( self.n )
        #print 'D='
        #print self.D
        self.jac = self.__jacobian()
        
        #self.I_tilde = self.__interpolation_matrix()
        #self.I_tilde_gll = self.__interpolation_matrix_gll()
        #self.__coordinates()
        #self.D_tilde = self.__derivative_matrix_tilde()
            
        
        #self.D = basic.lagrange_derivative_matrix_gll(self.n)
        #self.points, self.weights = basic.gauss_lobatto_legendre(self.n)
    def mask(self,v):
        return v
        
    def __jacobian(self):
        # The jacobian.
        if self.dim == 1:
            jac = sempy.space.space_f90.geometric_1d( self.x, self.D )
        if self.dim == 2:
            jac = sempy.space.space_f90.geometric_2d( self.x, self.y, 
                                                      self.D )
        if self.dim == 3:
            jac = sempy.space.space_f90.geometric_3d( self.x, self.y, 
                                                      self.z, self.D )
        return jac
            
    def sem_to_fem(self,u_sem):
        '''
        A mapping from the SEM space to FEM space. 
        '''
        if self.dim == 1:
            u_fem = precond_f90.sem_to_fem_1d( u_sem, self.n, self.noe)
        if self.dim == 2:
            u_fem = precond_f90.sem_to_fem_2d( u_sem, self.n, self.noe)
        if self.dim == 3:
            u_fem = precond_f90.sem_to_fem_3d( u_sem, self.n, self.noe)
            
        return u_fem
        
    def local_to_global(self,w):
        if self.dim == 1:
            v = space_f90.local_to_global_1d(w,self.theta,self.dof)
        if self.dim == 2:
            v = space_f90.local_to_global_2d(w,self.theta,self.dof)
        if self.dim == 3:
            v = space_f90.local_to_global_3d(w,self.theta,self.dof)
        return v
    
    def __fem_coor(self):
        # Coordinates
        if self.dim == 1:
            self.x, self.theta = precond_f90.fem_coor_1d( 
                                               self.SpaceGL.x,
                                               self.SpaceGL.theta, 
                                               self.n,
                                               self.noe )
            return self.x, self.theta
        
        if self.dim == 2:
            self.x,self.y,self.theta = precond_f90.fem_coor_2d( 
                                               self.SpaceGL.x,
                                               self.SpaceGL.y,
                                               self.SpaceGL.theta, 
                                               self.n,
                                               self.noe )
            return self.x, self.y, self.theta
        
        if self.dim == 3:
            self.x, self.y, self.z, self.theta = \
                        precond_f90.fem_coor_3d( self.SpaceGL.x,
                                                 self.SpaceGL.y,
                                                 self.SpaceGL.z,
                                                 self.SpaceGL.theta, 
                                                 self.n,self.noe )
            return self.x, self.y, self.z, self.theta
    
    def plot_mesh(self):
        '''
        Plots the numerical mesh.
        ''' 
        if self.dim == 2:
            u = np.zeros((self.noe,self.n,self.n),float)
            fig = plt.figure()
            ax = axes3d.Axes3D(fig)
            for k in range(self.noe):
                ax.plot_wireframe(self.x[k,:,:],self.y[k,:,:],u[k,:,:])
            plt.show()
    
        

class Gradient:
    '''
    The gradient operator 
    
    .. math::
    
       \underline{\mathbf G} =[\underline{G}_x,
                   \underline{G}_y,\underline{G}_z]^T 
        
    as found in the Stokes- and Navier-Stokes equations. 
    
    .. math::
    
       \\nabla p \\Rightarrow 
       \underbrace{-\int_\Omega p\\nabla\cdot \mathbf w\,d\Omega}_{\\text{GL quadrature}}
       \Rightarrow b_N(p,\mathbf w) 
       
       b_N(p,\mathbf w)\\Rightarrow 
       \underline{\mathbf G}\,\underline{p}
    
    :argument Space: Discrete space.
    :type Space: :class:`sempy.Space`
    :argument SpaceGL: Discrete GL space.
    :type SpaceGL: :class:`sempy.fluid.SpaceGL`
        
    :attributes: * **matrix_x**, **matrix_y**, **matrix_z** 
                   (*Scipy LinearOperator*) - The components 
                   of the gradient operator
                   :math:`\underline{\mathbf G} =[\underline{G}_x\,\underline{G}_y\, \underline{G}_z]^T`. 
                 * **matrix** (*List of Scipy LinearOperators*) - The gradient 
                   operator :math:`\underline{\mathbf G}`.   
    
    **Example**::
    
       import sempy

       X = sempy.Space( filename = 'cube', n = 4, dim = 3 )
       X_gl=sempy.fluid.SpaceGL( X )
    
       grad = sempy.fluid.Gradient( X, X_gl )
    
       G_x = grad.matrix_x
       G_z = grad.matrix_y
       G_y = grad.matrix_z
    
    '''
    def __init__(self,Space,SpaceGL):#,assemble='no'):
        self.Space = Space
        self.SpaceGL = SpaceGL
        #self.assemble = assemble
        
        if self.Space.dim == 1:
            self.matrix_x = spl.LinearOperator( 
                                   ( self.Space.dof,self.SpaceGL.dof ),
                                     matvec = self.__action_1d,
                                     dtype = 'float' )
            self.matrix = [ self.matrix_x ]
            
        if self.Space.dim == 2:
            g11,g12,g21,g22=\
               operators_f90.geometric_convection_2d(self.Space.x,
                                                     self.Space.y,
                                                     self.Space.D) 
            # Interpolate to GL mesh
            self.g11 = self.SpaceGL.interpolation(g11)
            self.g12 = self.SpaceGL.interpolation(g12)
            self.g21 = self.SpaceGL.interpolation(g21)
            self.g22 = self.SpaceGL.interpolation(g22)
            
            # Matrix
            self.matrix_x = spl.LinearOperator( 
                                   ( self.Space.dof,self.SpaceGL.dof ),
                                     matvec = self.__action_x_2d,
                                     dtype = 'float' )    
            self.matrix_y = spl.LinearOperator( 
                                   ( self.Space.dof,self.SpaceGL.dof ),
                                     matvec = self.__action_y_2d,
                                     dtype = 'float' )
            self.matrix = [ self.matrix_x, self.matrix_y ]
        if self.Space.dim == 3:
            self.__geometric_3d()
            # Matrix
            self.matrix_x = spl.LinearOperator( 
                                   ( self.Space.dof,self.SpaceGL.dof ),
                                     matvec = self.__action_x_3d,
                                     dtype = 'float' ) 
            # Matrix
            self.matrix_y = spl.LinearOperator( 
                                   ( self.Space.dof,self.SpaceGL.dof ),
                                     matvec = self.__action_y_3d,
                                     dtype = 'float' ) 
            # Matrix
            self.matrix_z = spl.LinearOperator( 
                                   ( self.Space.dof,self.SpaceGL.dof ),
                                     matvec = self.__action_z_3d,
                                     dtype = 'float' ) 
            #
            self.matrix = [ self.matrix_x, self.matrix_y, self.matrix_z ]
            
              
    def __geometric_3d(self):
        # geometric 
        noe = self.Space.noe
        n = self.Space.n
        g11 = np.zeros((noe,n,n,n),float)
        g12 = np.zeros((noe,n,n,n),float)
        g13 = np.zeros((noe,n,n,n),float)
        g21 = np.zeros((noe,n,n,n),float)
        g22 = np.zeros((noe,n,n,n),float)
        g23 = np.zeros((noe,n,n,n),float)
        g31 = np.zeros((noe,n,n,n),float)
        g32 = np.zeros((noe,n,n,n),float)
        g33 = np.zeros((noe,n,n,n),float)
        for k in range(self.Space.noe):
            g11[k,:,:,:],g12[k,:,:,:],g13[k,:,:,:],\
            g21[k,:,:,:],g22[k,:,:,:],g23[k,:,:,:],\
            g31[k,:,:,:],g32[k,:,:,:],g33[k,:,:,:] =\
                operators_f90.geometric_convection_3d(
                                        self.Space.x[k,:,:,:],
                                        self.Space.y[k,:,:,:],
                                        self.Space.z[k,:,:,:],
                                        self.Space.D)
        self.g11 = self.SpaceGL.interpolation(g11)
        self.g12 = self.SpaceGL.interpolation(g12)
        self.g13 = self.SpaceGL.interpolation(g13)
        self.g21 = self.SpaceGL.interpolation(g21)
        self.g22 = self.SpaceGL.interpolation(g22)
        self.g23 = self.SpaceGL.interpolation(g23)
        self.g31 = self.SpaceGL.interpolation(g31)
        self.g32 = self.SpaceGL.interpolation(g32)
        self.g33 = self.SpaceGL.interpolation(g33)
        
    def assemble_1d(self):
        print ''
        print '**** Assemble convection      ****'
        nz_1 = self.Space.noe * self.Space.n * self.Space.n
        nz_2 = self.SpaceGL.noe * self.SpaceGL.n * self.SpaceGL.n
        #t1 = time.clock()
        irow,jcolumn,value = \
            operators_f90.assemble_convection_1d(
                                    self.u_conv,
                                    self.Space.weights,
                                    self.Space.D,
                                    self.Space.theta,nz)
        #A = PysparseMatrix(size=self.Space.dof)
        # Assign values
        #for k in range(len(value)):
        #    i = int(irow[k])
        #    j = int(jcolumn[k])
        #    A[i,j] = A[i,j] + value[k]
        # Mask
        #A = self.Space.mask_matrix(A)
        #t2 = time.clock()
        #print '**** ex time=',t2-t1,'nnz=',A.nnz
        return A
    
    def __action_1d(self,v_in):
        # Mapping
        u = self.SpaceGL.mapping_q(v_in)
        # Local matrix vector product w_L=G_L*v_L
        w = fluid_operator_f90.gradient_1d(self.SpaceGL.D_tilde, 
                                           self.SpaceGL.weights,u)
        # Mapping
        v_out = self.Space.mapping_qt(w)
        # Mask
        v_out = self.Space.mask(v_out)
        return v_out
    
                  
    def __action_x_2d(self,v_in):
        # Mapping
        u = self.SpaceGL.mapping_q(v_in)
        # Local matrix vector product w_L=G_L*v_L
        w = fluid_operator_f90.gradient_x_2d(self.SpaceGL.I_tilde,
                                             self.SpaceGL.D_tilde, 
                                             self.SpaceGL.weights,
                                             self.g11,self.g12,u)
        # Mapping
        v_out = self.Space.mapping_qt(w)
        # Mask
        v_out = self.Space.mask(v_out)
        return v_out
    
    def __action_y_2d(self,v_in):
        # Mapping
        u = self.SpaceGL.mapping_q(v_in)
        # Local matrix vector product w_L=G_L*v_L
        w = fluid_operator_f90.gradient_y_2d(self.SpaceGL.I_tilde,
                                             self.SpaceGL.D_tilde, 
                                             self.SpaceGL.weights,
                                             self.g21,self.g22,u)
        # Mapping
        v_out = self.Space.mapping_qt(w)
        # Mask
        v_out = self.Space.mask(v_out)
        return v_out
    
    def __action_x_3d(self,v_in):
        # Mapping
        u = self.SpaceGL.mapping_q(v_in)
        # Local matrix vector product w_L=G_L*v_L
        w = fluid_operator_f90.gradient_x_3d(self.SpaceGL.I_tilde,
                                             self.SpaceGL.D_tilde, 
                                             self.SpaceGL.weights,
                                             self.g11,self.g12,
                                             self.g13,u)
        # Mapping
        v_out = self.Space.mapping_qt(w)
        # Mask
        v_out = self.Space.mask(v_out)
        return v_out
    
    def __action_y_3d(self,v_in):
        # Mapping
        u = self.SpaceGL.mapping_q(v_in)
        # Local matrix vector product w_L=G_L*v_L
        w = fluid_operator_f90.gradient_x_3d(self.SpaceGL.I_tilde,
                                             self.SpaceGL.D_tilde, 
                                             self.SpaceGL.weights,
                                             self.g21,self.g22,
                                             self.g23,u)
        # Mapping
        v_out = self.Space.mapping_qt(w)
        # Mask
        v_out = self.Space.mask(v_out)
        return v_out
    
    def __action_z_3d(self,v_in):
        # Mapping
        u = self.SpaceGL.mapping_q(v_in)
        # Local matrix vector product w_L=G_L*v_L
        w = fluid_operator_f90.gradient_x_3d(self.SpaceGL.I_tilde,
                                             self.SpaceGL.D_tilde, 
                                             self.SpaceGL.weights,
                                             self.g31,self.g32,
                                             self.g33,u)
        # Mapping
        v_out = self.Space.mapping_qt(w)
        # Mask
        v_out = self.Space.mask(v_out)
        return v_out
        
    def plot(self):
        '''
        Plots the GL mesh.
        '''
            
        if self.SpaceGL.dim == 2:
            fig = plt.figure()
            ax = axes3d.Axes3D(fig)
            #u = np.zeros((self.SpaceGL.noe,self.SpaceGL.n,self.SpaceGL.n),float)
            #u = self.g11
            #for k in range(self.SpaceGL.noe):
            #    ax.plot_wireframe(self.SpaceGL.x[k,:,:],
            #                      self.SpaceGL.y[k,:,:],u[k,:,:])
            # test interpoalte
            x_gll=self.Space.x
            y_gll=self.Space.y
            u = self.w#np.zeros((self.noe,self.n+2,self.n+2),float)
            for k in range(self.Space.noe):
                ax.plot_wireframe(x_gll[k,:,:],y_gll[k,:,:],u[k,:,:])
            
            ax.set_xlabel(r'$x$')
            ax.set_ylabel(r'$y$')
            plt.show()

class Divergence:
    '''
    The divergence operator. 
    
    .. math::
    
       \underline{\mathbf D} =[\underline{D}_x\ 
                   \underline{D}_y\ \underline{D}_z] 
    
    As found in the continuity equation
    
    .. math::
    
       \\nabla\cdot\mathbf u=0\quad \Rightarrow\quad 
       \int_\Omega (\\nabla\cdot\mathbf u)q\,d\Omega=
       -b_N(q,\mathbf u)
       
       
    .. math:: 
       -b_N(q,\mathbf u)\quad \Rightarrow\quad 
       \underline{\mathbf D}\,\underline{\mathbf u}
    
    
    :argument Space: Discrete space.
    :type Space: :class:`sempy.Space` or :class:`sempy.precond.SpaceFEM`
    
    :argument SpaceGL: Discrete space.
    :type SpaceGL: :class:`sempy.fluid.SpaceGL`
    
    :attributes: * **matrix_x**, **matrix_y**, **matrix_z** 
                   (*Scipy LinearOperator*) - The 
                   components of the divergence operator 
                   :math:`\underline{\mathbf D} =[\underline{D}_x\,\underline{D}_y\, \underline{D}_z]`.
                 * **matrix** (*A list of Scipy LinearOperators*) - 
                   The divergence operator  
                   :math:`\underline{\mathbf D}`.
    
    ..               If the matrix is assembled the type is 
                   `Pysparse PysparseMatrix <http://pysparse.sourceforge.net/pysparsematrix.html#pysparse.sparse.pysparseMatrix.PysparseMatrix>`_
                   `SciPy LinearOperator <http://docs.scipy.org/doc/scipy-0.7.x/reference/sparse.linalg.html#examples>`_
                    
    **Example**::
    
       import sempy
       
       X = sempy.Space( filename = 'square', n = 6, dim = 2 )
       X_gl = sempy.fluid.SpaceGL( X )
       
       div = sempy.fluid.Divergence( X, X_gl )
       D_x = div.matrix_x
       D_y = div.matrix_y
       
    The divergence of a vector field::
    
       U = sempy.VectorFunction( X )
       D = div.matrix
       
       s = np.zeros( ( X_gl.dof ), float )
       for i in range( X.dim ):
           s = s + D[i] * U[i].glob()
                       
    '''
    def __init__(self,Space,SpaceGL):
        self.Space = Space
        self.SpaceGL = SpaceGL
        
        #if self.Space.dim == 1:
        #    self.matrix_x = spl.LinearOperator( 
        #                           ( self.SpaceGL.dof,self.Space.dof ),
        #                             matvec = self.__action_1d,
        #                             dtype = 'float' )    
        #    self.matrix = [ self.matrix_x ]
            
        if self.Space.dim == 2:
            g11,g12,g21,g22=\
               operators_f90.geometric_convection_2d(self.Space.x,
                                                     self.Space.y,
                                                     self.Space.D) 
            # Interpolate to GL mesh
            self.g11 = self.SpaceGL.interpolation(g11)
            self.g12 = self.SpaceGL.interpolation(g12)
            self.g21 = self.SpaceGL.interpolation(g21)
            self.g22 = self.SpaceGL.interpolation(g22)
            # Matrix
            self.matrix_x = spl.LinearOperator( 
                                   ( self.SpaceGL.dof,self.Space.dof ),
                                     matvec = self.__action_x_2d,
                                     dtype = 'float' )    
            self.matrix_y = spl.LinearOperator( 
                                   ( self.SpaceGL.dof,self.Space.dof ),
                                     matvec = self.__action_y_2d,
                                     dtype = 'float' )  
            self.matrix_z = 'none'
            
            self.matrix = [ self.matrix_x, self.matrix_y ]
            #spl.LinearOperator( 
            #                       ( self.SpaceGL.dof,self.Space.dof ),
            #                         matvec = self.__action_2d,
            #                         dtype = 'float' )   
            
        if self.Space.dim == 3:
            self.__geometric_3d()
            # Matrix
            self.matrix_x = spl.LinearOperator( 
                                   ( self.SpaceGL.dof,self.Space.dof ),
                                     matvec = self.__action_x_3d,
                                     dtype = 'float' )    
            # Matrix
            self.matrix_y = spl.LinearOperator( 
                                   ( self.SpaceGL.dof,self.Space.dof ),
                                     matvec = self.__action_y_3d,
                                     dtype = 'float' )   
            # Matrix
            self.matrix_z = spl.LinearOperator( 
                                   ( self.SpaceGL.dof,self.Space.dof ),
                                     matvec = self.__action_z_3d,
                                     dtype = 'float' )
            self.matrix = [ self.matrix_x, self.matrix_y, self.matrix_z ]   
            
         
              
    def __geometric_3d(self):
        # geometric 
        noe = self.Space.noe
        n = self.Space.n
        g11 = np.zeros((noe,n,n,n),float);g12 = np.zeros((noe,n,n,n),float);
        g13 = np.zeros((noe,n,n,n),float);g21 = np.zeros((noe,n,n,n),float);
        g22 = np.zeros((noe,n,n,n),float);g23 = np.zeros((noe,n,n,n),float);
        g31 = np.zeros((noe,n,n,n),float);g32 = np.zeros((noe,n,n,n),float);
        g33 = np.zeros((noe,n,n,n),float);
        for k in range(self.Space.noe):
            g11[k,:,:,:],g12[k,:,:,:],g13[k,:,:,:],\
            g21[k,:,:,:],g22[k,:,:,:],g23[k,:,:,:],\
            g31[k,:,:,:],g32[k,:,:,:],g33[k,:,:,:] =\
                operators_f90.geometric_convection_3d(
                                        self.Space.x[k,:,:,:],
                                        self.Space.y[k,:,:,:],
                                        self.Space.z[k,:,:,:],
                                        self.Space.D)
        self.g11 = self.SpaceGL.interpolation(g11)
        self.g12 = self.SpaceGL.interpolation(g12)
        self.g13 = self.SpaceGL.interpolation(g13)
        self.g21 = self.SpaceGL.interpolation(g21)
        self.g22 = self.SpaceGL.interpolation(g22)
        self.g23 = self.SpaceGL.interpolation(g23)
        self.g31 = self.SpaceGL.interpolation(g31)
        self.g32 = self.SpaceGL.interpolation(g32)
        self.g33 = self.SpaceGL.interpolation(g33)
    
    def __action_2d(self,u_in):
        # Mapping
        #u1 = self.Space.mapping_q(u_in[0].basis_coeff)
        #u2 = self.Space.mapping_q(u_in[1])
        # 
        w_x = fluid_operator_f90.divergence_x_2d(
                        self.SpaceGL.I_tilde,
                        self.SpaceGL.D_tilde,
                        self.SpaceGL.weights,
                        self.g11,self.g12,u_in[0].basis_coeff)
        w_y = fluid_operator_f90.divergence_x_2d(
                        self.SpaceGL.I_tilde,
                        self.SpaceGL.D_tilde,
                        self.SpaceGL.weights,
                        self.g21,self.g22,u_in[1].basis_coeff)
        w = w_x + w_y
        # Mapping
        v_out = self.SpaceGL.mapping_qt(w)
        return v_out
    
    #def __action_x_1d(self,u_in):
    #    # Mapping
    #    u = self.Space.mapping_q(u_in)
    #    # 
    #    w = fluid_operator_f90.divergence_1d(
    #                    self.SpaceGL.I_tilde,
    #                    self.SpaceGL.D_tilde,
    #                    self.SpaceGL.weights,
    #                    self.g11,self.g12,u)
    #    # Mapping
    #    v_out = self.SpaceGL.mapping_qt(w)
    #    return v_out
                
    def __action_x_2d(self,u_in):
        # Mapping
        u = self.Space.mapping_q(u_in)
        # 
        w = fluid_operator_f90.divergence_x_2d(
                        self.SpaceGL.I_tilde,
                        self.SpaceGL.D_tilde,
                        self.SpaceGL.weights,
                        self.g11,self.g12,u)
        # Mapping
        v_out = self.SpaceGL.mapping_qt(w)
        return v_out
    
    def __action_y_2d(self,v_in):
        # Mapping
        v = self.Space.mapping_q(v_in)
        w = fluid_operator_f90.divergence_x_2d(
                        self.SpaceGL.I_tilde,
                        self.SpaceGL.D_tilde,
                        self.SpaceGL.weights,
                        self.g21,self.g22,v)
        # Mapping
        v_out = self.SpaceGL.mapping_qt(w)
        return v_out
    
    def __action_x_3d(self,u_in):
        # Mapping
        u = self.Space.mapping_q(u_in)
        # 
        w = fluid_operator_f90.divergence_x_3d(
                        self.SpaceGL.I_tilde,
                        self.SpaceGL.D_tilde,
                        self.SpaceGL.weights,
                        self.g11,self.g12,self.g13,u)
        # Mapping
        v_out = self.SpaceGL.mapping_qt(w)
        return v_out   
    
    def __action_y_3d(self,u_in):
        # Mapping
        u = self.Space.mapping_q(u_in)
        # 
        w = fluid_operator_f90.divergence_x_3d(
                        self.SpaceGL.I_tilde,
                        self.SpaceGL.D_tilde,
                        self.SpaceGL.weights,
                        self.g21,self.g22,self.g23,u)
        # Mapping
        v_out = self.SpaceGL.mapping_qt(w)
        return v_out   
    
    def __action_z_3d(self,u_in):
        # Mapping
        u = self.Space.mapping_q(u_in)
        # 
        w = fluid_operator_f90.divergence_x_3d(
                        self.SpaceGL.I_tilde,
                        self.SpaceGL.D_tilde,
                        self.SpaceGL.weights,
                        self.g31,self.g32,self.g33,u)
        # Mapping
        v_out = self.SpaceGL.mapping_qt(w)
        return v_out   
    
    
'''
class Stokes:
    
    The Stokes operator. 
    
    The Stokes equation reads
    
    .. math::

        -\\nabla\cdot \mu\\nabla\mathbf u +\\nabla p &= f \\\\
        \\nabla\cdot\mathbf u &= 0
        
    which can be posed in discrete form as 
    
    .. math:: 
       :nowrap:
        
        \\begin{equation}
        \\begin{bmatrix}
        A & G\\\\
        D & 0
        \\end{bmatrix}
        \\begin{bmatrix}
        u\\\\
        p
        \\end{bmatrix}
        =
        \\begin{bmatrix}
        f\\\\
        0
        \\end{bmatrix}
        \\nonumber
        \\end{equation}
        
    where the Stokes operator is
    
    .. math::
       :nowrap:
    
        \\begin{equation}
        S=
        \\begin{bmatrix}
        A & G\\\\
        D & 0
        \\end{bmatrix}
        \\nonumber
        \\end{equation}
    
    
    
    def __init__(self,Space,SpaceGL):
        self.Space = Space
        self.SpaceGL = SpaceGL
'''


def uzawa_cg(A,b,u,tol=1e-10,max_iter=100):
    n=b.size
    p,s,r=np.zeros((n),np.float),np.zeros((n),np.float),np.zeros((n),np.float)

    s=A*u
    r=b-s
    R_new=np.inner(r,r)
    for i in range(max_iter): 
        R_old=R_new
        R_new=np.inner(r,r)
        if R_new<tol : 
            flag=0
            print 'CG: Conv. at iter.=',i,'dot(r)=',R_new
            return [u,flag]
        beta=R_new/R_old
        p=r+beta*p
        s=A*p
        Dd=np.inner(p,s)
        alpha=R_new/Dd
        u=u+alpha*p
        r=r-alpha*s
        print 'iter=',i,'r_new=',R_new
    if i == max_iter-1: 
        flag= i
        print 'cg() did not converge. dot(r)=',np.inner(r,r)
    return [u,flag]

class Uzawa:
    '''
    The Uzawa method. 
    
    The Stokes equation reads
    
    .. math:: 
       :nowrap:
        
        \\begin{equation}
        \\begin{bmatrix}
        A & G\\\\
        D & 0
        \\end{bmatrix}
        \\begin{bmatrix}
        u\\\\
        p
        \\end{bmatrix}
        =
        \\begin{bmatrix}
        b\\\\
        0
        \\end{bmatrix}
        \\nonumber
        \\end{equation}
    
    in discrete form. One way to solve this system is by using 
    the Uzawa method, i.e.:    
    
    1. Solve the Uzawa equation for pressure :math:`p` 
    
       .. math::
       
          DA^{-1}Gp = DA^{-1}b
    
    2. Solve the momentum equation for the velocity field :math:`u` 
    
       .. math::
       
          Au+Gp=b
    
    :param Space: Discrete space.
    :type Space: :class:`sempy.Space`
    :param u: Velocity
    :type u: :class:`sempy.Function`
    :param f: Forcing term
    :type f: :class:`sempy.Function`
    
    '''
    def __init__(self,Space,SpaceGL,u,b):
        self.Space = Space
        self.SpaceGL = SpaceGL
        self.u = u
        self.b = b
        
        # Laplacian
        X_fem = sempy.precond.SpaceFEM( self.Space)
        lap = sempy.operators.Laplacian( self.Space ,
                                         fem_assemble='yes')
        self.A = lap.matrix
        # Preconditioner
        A_fem = lap.matrix_fem
        P = sempy.precond.Preconditioner( self.Space, [A_fem], 
                                    drop_tol = 0.5 ).matrix
        # Gradient
        grad = sempy.fluid.Gradient( self.Space, self.SpaceGL )
        
        if self.Space.dim == 2:
            
            self.G_x = grad.matrix_x
            self.G_y = grad.matrix_y
            
        if self.Space.dim == 3:
            
            self.G_x = grad.matrix_x
            self.G_y = grad.matrix_y
            self.G_z = grad.matrix_z
        # Divergence
        div = sempy.fluid.Divergence( self.Space, self.SpaceGL )
        
        if self.Space.dim == 2:
            
            self.D_x = div.matrix_x
            self.D_y = div.matrix_y
            
        if self.Space.dim == 3:
            
            self.D_x = div.matrix_x
            self.D_y = div.matrix_y
            self.D_z = div.matrix_z
        # Solution vector
        #self.t_x = sempy.Function( self.Space, basis_coeff = 0.0 )
        #self.t_y = sempy.Function( self.Space, basis_coeff = 0.0 )
        #self.inner_solver = sempy.linsolvers.Direct(self.Space)
        self.inner_solver = sempy.linsolvers.Krylov( tol = 1e-15,
                                                     solver_type = 'bicgstab',
                                                     pre = P )
        self.outer_solver = sempy.linsolvers.Krylov(
                                            tol = 1e-08,
                                            solver_type = 'cg',
                                            pre = self.SpaceGL.mass_inv)  
        # Forcing term and linear form
        self.b_uz = self.__rhs()
        # Uzawa operator
        self.U = spl.LinearOperator( 
                          ( self.SpaceGL.dof,self.SpaceGL.dof ),
                            matvec = self.__action_uzawa,
                            dtype = 'float' )
        
        
    def solve(self):
        '''
        Solves the Sokes problem. 
        '''
        # Step 1: Pressure
        p_f = np.zeros((self.SpaceGL.dof),float)
        #[p, flag] = uzawa_cg( self.U, self.b, p_f )
        [p, flag] = self.outer_solver.solve( self.U, self.b_uz, p_f )
        #[p,flag] = uzawa_cg(self.U,self.b_uz,p_f)
        #print 'uzawa iter=',flag,'time=',self.outer_solver.ex_time
        # Step 2: Velocity
        if self.Space.dim == 2:
            b_x = self.G_x*p*(-1.0) + self.b[0]
            [u_x, flag] = self.inner_solver.solve( self.A, b_x, 
                                               self.u[0].glob() )
            self.u[0].basis_coeff = self.Space.mapping_q(u_x)
            #print 'flag=',flag
            b_y = self.G_y*p*(-1.0) + self.b[1]
            [u_y, flag] = self.inner_solver.solve( self.A, b_y, 
                                               self.u[1].glob() )
            self.u[1].basis_coeff = self.Space.mapping_q(u_y)
            return p,[self.u[0],self.u[1]],flag
        
        if self.Space.dim == 3:
            b_x = self.G_x*p*(-1.0) + self.b[0]
            [u_x, flag] = self.inner_solver.solve( self.A, b_x, 
                                               self.u[0].glob() )
            self.u[0].basis_coeff = self.Space.mapping_q(u_x)
            
            b_y = self.G_y*p*(-1.0) + self.b[1]
            [u_y, flag] = self.inner_solver.solve( self.A, b_y, 
                                               self.u[1].glob() )
            self.u[1].basis_coeff = self.Space.mapping_q(u_y)
            
            b_z = self.G_z*p*(-1.0) + self.b[2]
            [u_z, flag] = self.inner_solver.solve( self.A, b_z, 
                                               self.u[2].glob() )
            self.u[2].basis_coeff = self.Space.mapping_q(u_z)
            
            return p,[self.u[0],self.u[1],self.u[2]],flag
        
    def __rhs(self):
        print 'calc rhs...'
        if self.Space.dim == 2:
            # u component
            [t_x, flag] = self.inner_solver.solve( self.A, 
                                    self.b[0], self.u[0].glob())
            # v component
            [t_y, flag] = self.inner_solver.solve( self.A, 
                                    self.b[1], self.u[1].glob())
            # Divergence
            b = self.D_x*t_x + self.D_y*t_y
            
        if self.Space.dim == 3:
            # u component
            [t_x, flag] = self.inner_solver.solve( self.A, 
                                    self.b[0], self.u[0].glob())
            # v component
            [t_y, flag] = self.inner_solver.solve( self.A, 
                                    self.b[1], self.u[1].glob())
            # w component
            [t_z, flag] = self.inner_solver.solve( self.A, 
                                    self.b[2], self.u[2].glob())
            # Divergence
            b = self.D_x*t_x + self.D_y*t_y + self.D_z*t_z
        print '..rhs.'    
        return b
        
            
    def __action_uzawa(self,q_in):
        print 'action uzawa...'
        #
        if self.Space.dim == 2:
            # 1
            s_x = self.G_x*q_in
            s_y = self.G_y*q_in
            # 2
            t_x = sempy.Function( self.Space, basis_coeff = 0.0 )
            t_y = sempy.Function( self.Space, basis_coeff = 0.0 )
            [v_x, flag] = self.inner_solver.solve( self.A, s_x, t_x.glob() )
            [v_y, flag] = self.inner_solver.solve( self.A, s_y, t_y.glob() )
            # 3
            q_out = self.D_x * v_x + self.D_y * v_y
            
        if self.Space.dim == 3:
            # 1
            s_x = self.G_x*q_in
            s_y = self.G_y*q_in
            s_z = self.G_z*q_in
            # 2
            t_x = sempy.Function( self.Space, basis_coeff = 0.0 )
            t_y = sempy.Function( self.Space, basis_coeff = 0.0 )
            t_z = sempy.Function( self.Space, basis_coeff = 0.0 )
            [v_x, flag] = self.inner_solver.solve( self.A, s_x, t_x.glob() )
            [v_y, flag] = self.inner_solver.solve( self.A, s_y, t_y.glob() )
            [v_z, flag] = self.inner_solver.solve( self.A, s_z, t_z.glob() )
            # 3
            q_out = self.D_x * v_x + self.D_y * v_y + self.D_z * v_z
            
        print '.. uzawa.'        
        return q_out
         
        
if __name__=='__main__':
    #X = sempy.Space( filename = 'line', n = 10, dim = 1 )
    X = sempy.Space( filename = 'square', n = 10, dim = 2 )
    #X = sempy.Space( filename = 'cube', n = 4, dim = 3 )
    X_gl = sempy.fluid.SpaceGL( X )
    X_gl.plot_mesh()
    