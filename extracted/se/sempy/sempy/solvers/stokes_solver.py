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

import sempy
import scipy.sparse.linalg as spl
import numpy as np


class SteadyStokes:
    '''
    A solver for the steady Stokes problem
    
    .. math::
    
       -\\nabla\cdot\mu\\nabla \mathbf u +\\nabla p =\mathbf f
       
       \\nabla\cdot\mathbf u = 0
    
    which reads
    
    .. math:: 
       :nowrap:
        
        \\begin{equation}
        \\begin{bmatrix}
        \underline{A} & \underline{G}\\\\
        \underline{D} & 0
        \\end{bmatrix}
        \\begin{bmatrix}
        \underline{u}\\\\
        \underline{p}
        \\end{bmatrix}
        =
        \\begin{bmatrix}
        \underline{b}\\\\
        0
        \\end{bmatrix}
        \\nonumber
        \\end{equation}
    
    in discrete form. One way to solve this system is by using 
    the Uzawa method, i.e.:    
    
    1. Solve the Uzawa equation for pressure :math:`p` 
    
       .. math::
          
          \underline{D}\,\underline{A}^{-1}\underline{G}
          \,\underline{p} = 
          \underline{D}\,\underline{A}^{-1}\underline{b}
    
    2. Solve the momentum equation for the velocity field :math:`u` 
    
       .. math::
       
          \underline{A}\,\underline{u}+
          \underline{G}\,\underline{p}=\underline{b}
    
    Here, the first step involves nested iterations. 
    
    :param Space: Discrete space.
    :type Space: :class:`sempy.Space`
    :param SpaceGL: Discrete space.
    :type SpaceGL: :class:`sempy.fluid.SpaceGL`
    :param u: Velocity. A function in :math:`(H^1(\Omega))^d`.
    :type u: :class:`sempy.VectorFunction`
    :param p: Pressure. A function in :math:`L^2(\Omega)`.
    :type p: :class:`sempy.Function`
    :param mu: Viscosity. If :literal:`None` it will be set to unity. 
    :type mu: :class:`sempy.Function`
    :param f: Forcing term. If :literal:`None` it will be set to zero. 
    :type f: :class:`sempy.Function`
    
    :attribute: * **U** - The uzawa operator 
                  :math:`\underline{U}=\underline{D}\,\underline{A}^{-1}\underline{G}`
    
    **Example**::
    
       import sempy
       
       X = sempy.Space( filename = 'cube', n = 4, dim = 3 )
       X_gl = sempy.fluid.SpaceGL( X )

       U = sempy.VectorFunction( X, filename = 'vecfunc' )
       U[0].set_bc( 1.0, 1 )
       p = sempy.Function( X_gl, filename = 'pressure' )

       solver = sempy.solvers.SteadyStokes( X, X_gl, U, p )
       p, U, flag = solver.solve()
       
       print 'Number of outer iter=',flag
       U.to_file()
       
    '''
    def __init__( self, Space, SpaceGL, u, p, mu = None, 
                  f = None ):
        self.Space = Space
        self.SpaceGL = SpaceGL
        self.u = u
        self.p = p
        
        # Forcing term
        if f == None:
            f_dummy = sempy.Function( Space, basis_coeff =  0.0)
            if self.Space.dim == 1:
                b = f_dummy.glob()
                self.b = [b]
            if self.Space.dim == 2:
                b = f_dummy.glob()
                self.b = [b,b]
            if self.Space.dim == 3:
                b = f_dummy.glob()
                self.b = [b,b,b]
        else:
            mass_gll = sempy.operators.Mass( self.Space )
            #f_dummy = sempy.Function( Space, basis_coeff =  0.0)
            if self.Space.dim == 2:
                s1 = np.zeros( ( self.Space.dof ) )
                s2 = np.zeros( ( self.Space.dof ) )
                #b = f_dummy.glob()
                self.b = [ s1, s2 ]
                for i in range(self.Space.dim):
                    self.b[i] = mass_gll.action_local( f[i].basis_coeff )
                
        # Transport coefficient
        if mu == None:
            mu_dummy = sempy.Function( Space, basis_coeff =  1.0 )
            self.mu = mu_dummy
        else:
            self.mu = mu
        
        # Laplacian
        lap = sempy.operators.Laplacian( self.Space, 
                                         mu = self.mu,
                                         fem_assemble = 'yes' )
        self.A = lap.matrix
        # Preconditioner
        A_fem = lap.matrix_fem
        self.P = sempy.precond.Preconditioner( self.Space, [A_fem], 
                                          drop_tol = 0.5 ).matrix
        # Gradient
        grad = sempy.fluid.Gradient( self.Space, self.SpaceGL )
        self.G = grad.matrix

        # Divergence
        div = sempy.fluid.Divergence( self.Space, self.SpaceGL )
        self.D = div.matrix
        
        # Solution vector
        self.inner_solver = sempy.linsolvers.Krylov( tol = 1e-15,
                                                     solver_type = 'bicgstab',
                                                     pre = self.P )
        self.M_gl_inv = sempy.precond.Preconditioner( 
                                    self.SpaceGL, 
                                    [self.SpaceGL.mass_matrix] ).matrix
        self.outer_solver = sempy.linsolvers.Krylov(
                                            tol = 1e-10,
                                            solver_type = 'cg',
                                            pre = self.M_gl_inv )  
        # Forcing term and linear form
        self.b_uz = self.__rhs()
        # Uzawa operator
        self.U = spl.LinearOperator( 
                          ( self.SpaceGL.dof,self.SpaceGL.dof ),
                            matvec = self.__action_uzawa,
                            dtype = 'float' )
        
    def pcg(self,A,b,u,precond,tol=1e-10,max_iter=5000):
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
         
    def solve(self):
        '''
        Solves the Stokes problem.
        
        :returns: * **u** - Velocity
                  * **p** - Pressure
                  * **flag** - Gives the number of Uzawa iterations, if 
                    the iterative proceedure is successful.  
        '''
        print 'Solving the Stokes problem...'
        # Step 1: Pressure
        [p_glob, flag] = self.outer_solver.solve( self.U, 
                                                  self.b_uz, 
                                                  self.p.glob() )
        #[p_glob, flag] = self.pcg( self.U, self.b_uz,
        #                           self.p.glob(),
        #                           self.SpaceGL.mass_inv )
        self.p.basis_coeff = self.SpaceGL.mapping_q( p_glob )
        
        # Step 2: Velocity
        for i in range(self.SpaceGL.dim):
            b_temp = self.G[i]*p_glob*(-1.0) + self.b[i]
            [u_temp, flag] = self.inner_solver.solve( 
                                            self.A, 
                                            b_temp, 
                                            self.u[i].glob() )
            self.u[i].basis_coeff = self.Space.mapping_q(u_temp)
        print '...finished.'    
        return self.p, self.u, flag
    
        
    def __rhs(self):
        # The right hand side.
        
        # Solve for the components
        t = np.zeros( (self.Space.dim, self.Space.dof), float)
        for i in range(self.Space.dim):
            [t[i], flag] = self.inner_solver.solve( self.A, 
                                    self.b[i], self.u[i].glob())
        
        # Divergence:
        b = np.zeros( ( self.SpaceGL.dof ), float )
        for i in range( self.Space.dim ):
            b = b + self.D[i] * t[i]
                
        # Compatibility
        if self.SpaceGL.zero == 'yes':
            alpha = b.sum()
            b = b - alpha / self.SpaceGL.dof
        
        return b
        
    
    def __action_uzawa(self,q_in):
        # Action of the Uzawa operator.
        
        # 1: Gradient 
        s = np.zeros( (self.Space.dim, self.Space.dof), float)
        for i in range( self.Space.dim ) :
            s[i] = self.G[i] * q_in
                        
        # 2: Inverse of Helmholtz
        v = np.zeros( (self.Space.dim, self.Space.dof), float)
        t = np.zeros( (self.Space.dim, self.Space.dof), float)
        for i in range( self.Space.dim ) :
            v[i], flag = self.inner_solver.solve( self.A, s[i], t[i] )
        
        # 3: Divergence
        q_out = np.zeros( ( self.SpaceGL.dof ), float )
        for i in range( self.Space.dim ) :
            q_out = q_out + self.D[i] * v[i]
                
        return q_out
            
    
        
            