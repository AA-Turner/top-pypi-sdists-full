import sempy
import numpy as np
import scipy.sparse.linalg as spl

import scipy.linalg as sc


class NavierStokes:
    def __init__(self, Space, SpaceGL, Time, u, p, mu = 'none' , 
                  f = 'none' ):
        self.Space = Space
        self.SpaceGL = SpaceGL
        self.u = u
        self.p = p
        self.Time = Time
        
        # Forcing term
        if f == 'none':
            f_dummy = sempy.Function( Space, basis_coeff =  0.0)
            #if self.Space.dim == 1:
            #    b = f_dummy.glob()
            #    self.b = [b]
            if self.Space.dim == 2:
                #b = f_dummy.glob()
                self.f = [f_dummy,f_dummy]
                
            #if self.Space.dim == 3:
            #    b = f_dummy.glob()
            #    self.b = [b,b,b]
        #else:
        #    for i in range(self.Space.dim):
        #        mass_gll = sempy.operators.Mass( self.Space )
        #        self.b[i] = mass_gll.action_local( f[i].basis_coeff )
        # Transport coefficient
        if mu == 'none':
            mu_dummy = sempy.Function( Space, basis_coeff =  1.0 )
            self.mu = mu_dummy
        else:
            self.mu = mu
        # Laplacian
        lap = sempy.operators.Laplacian( self.Space, 
                                         mu = self.mu,
                                         fem_assemble = 'yes' )
        self.A = lap.matrix
        self.A_fem = lap.matrix_fem
        # Convection
        #conv = sempy.operators.Convection( self.Space, 
        #                                  [self.u[0], self.u[1]])
        #self.C = conv.matrix
        # Mass matrix
        mass = sempy.operators.Mass( self.Space )
        self.M = mass.matrix
        self.M_inv = mass.matrix_inv
        # Helmholtz
        self.H = sempy.operators.MultipleOperators( [self.M,self.A],
                                                    [1.0,self.Time.h],
                                                    assemble = 'no').matrix
        #self.H_fem = sempy.operators.MultipleOperators( [self.M,self.A_fem],
        #                                            [1.0,self.Time.h],
        #                                            assemble = 'yes').matrix
        # Precond.
        self.P = sempy.precond.Preconditioner( self.Space, [self.M, self.A_fem], 
                                          scaling_factor=[1.0,self.Time.h],
                                          drop_tol = 0.5 ).matrix
        # Divergence
        self.__divergence_matrix()
        # Gradient
        self.__gradient_matrix()
        # Uzawa operator
        self.U = spl.LinearOperator( 
                          ( self.SpaceGL.dof,self.SpaceGL.dof ),
                            matvec = self.__action_uzawa,
                            dtype = 'float' )
        self.U_fem = spl.LinearOperator( 
                          ( self.SpaceGL.dof,self.SpaceGL.dof ),
                            matvec = self.__action_uzawa_fem,
                            dtype = 'float' )
        self.U_pre = spl.LinearOperator( 
                          ( self.SpaceGL.dof,self.SpaceGL.dof ),
                            matvec = self.__uzawa_pre,
                            dtype = 'float' )
        #print 'U_pre'
        #print self.U_pre*self.p.glob()
        # Linear solvers
        self.inner_solver = sempy.linsolvers.Krylov(tol = 1e-10,
                                                    solver_type = 'bicgstab',
                                                    pre = self.P )
        self.outer_solver = sempy.linsolvers.Krylov(
                                            tol = 1e-08,
                                            solver_type = 'cg',
                                            pre = self.U_pre)
        self.pre_solver  = sempy.linsolvers.Krylov(tol = 1e-10,
                                         solver_type = 'bicgstab')
                                         #pre = self.P )
        
    def __mom_b(self,u,f):
        
        conv = sempy.operators.Convection( self.Space, [ u[0], u[1] ] )
        C = conv.matrix
            
        b_x = self.M*f[0].glob() - C*u[0].glob()
        b_y = self.M*f[1].glob() - C*u[1].glob()
        b = [b_x, b_y]
        
        return b    
    
    def __action_uzawa(self,q_in):
        #print 'action uzawa...'
        #
        if self.Space.dim == 2:
            # 1
            s_x = self.G_x*q_in
            s_y = self.G_y*q_in
            # 2
            t_x = sempy.Function( self.Space, basis_coeff = 0.0 )
            t_y = sempy.Function( self.Space, basis_coeff = 0.0 )
            [v_x, flag] = self.inner_solver.solve( self.H, s_x, t_x.glob() )
            #[v_x, flag] = spl.cg( self.H, s_x, x0 = t_x.glob(), 
            #                      tol = 1e-15,
            #                      maxiter = 1000,
            #                      M= self.P)
            print'v_x flag=',flag 
            #print '3 uz cg=',flag
            [v_y, flag] = self.inner_solver.solve( self.H, s_y, t_y.glob() )
            #[v_y, flag] = spl.cg( self.H, s_y, x0 = t_y.glob(), 
            #                      tol = 1e-15,
            #                      maxiter = 1000,
            #                      M= self.P)
            print'v_y flag=',flag 
            # 3
            q_out = self.D_x * v_x + self.D_y * v_y
            
        return q_out
    
    def __uzawa_pre(self,q_in):
        print 'pre uzawa...'
        s = sempy.Function( self.SpaceGL, basis_coeff = 0.0 )
        #[p_out, flag] = spl.bicgstab( self.U_fem, q_in, #x0 = s.glob(), 
        #                        tol = 1e-15,
        #                        maxiter = 2000)
        #                       #callback = self.cb.it_count )
        [p_out, flag] = self.pre_solver.solve( self.U_fem, q_in, s.glob() )
        #[p_out, flag] = sempy.linsolvers.Krylov(tol = 1e-15).
        #solve( self.U_fem, q_in, s.glob() )
        print 'pre uzawa flag=',flag
        #t = self.U_fem*p_out - q_in
        #print 'pre uzawa norm', sc.norm(t,1)
        print 'pre uzawa stop'
        return p_out
        
        
    def __action_uzawa_fem(self,q_in):
        #
        if self.Space.dim == 2:
            # 1
            s_x = self.G_x * q_in
            s_y = self.G_y * q_in
            # 2
            v_x = self.P * s_x
            v_y = self.P * s_y
            # 3
            q_out = self.D_x * v_x + self.D_y * v_y
            
        return q_out
         
    def __divergence_matrix(self):
        # Divergence
        div = sempy.fluid.Divergence( self.Space, self.SpaceGL )
        
        if self.Space.dim == 2:
            
            self.D_x = div.matrix_x
            self.D_y = div.matrix_y
            
        if self.Space.dim == 3:
            
            self.D_x = div.matrix_x
            self.D_y = div.matrix_y
            self.D_z = div.matrix_z
            
    def __gradient_matrix(self):
        grad = sempy.fluid.Gradient( self.Space, self.SpaceGL )
        
        if self.Space.dim == 2:
            
            self.G_x = grad.matrix_x
            self.G_y = grad.matrix_y
            
        if self.Space.dim == 3:
            
            self.G_x = grad.matrix_x
            self.G_y = grad.matrix_y
            self.G_z = grad.matrix_z
        
    def solve(self):
        '''
        Solve.
        '''
        
        #-- Output
        self.u.to_file()
        self.p.to_file()
        #ystart = np.zeros( (self.Space.dof), float )
        #print self.H*ystart
        #
        #ystart[:] = self.y0.glob()
        ustart = self.u
        pstart = self.p
        pend = sempy.Function( self.SpaceGL, basis_coeff = 0.0 )
        uend = sempy.VectorFunction( self.Space )
        #-- Time-stepping
        for i in range(self.Time.time_steps):
            print '--> time step no=',i+1
            uend, pend = self.__time_stepping( ustart, uend, pstart, pend )
            self.Time.increment()
            ustart = uend
            pstart = pend
            #self.u = ustart
            #self.p = pstart
            self.u[0].basis_coeff =ustart[0].basis_coeff
            self.u[1].basis_coeff =ustart[1].basis_coeff
            self.p.basis_coeff = pstart.basis_coeff
            self.u.to_file()
            self.p.to_file()
            print 'time=',self.Time.time
        return self.u, self.p
            
    def __time_stepping(self,ustart,uend, pstart,pend):
        # The b term in Navier-Stokes
        b = self.__mom_b( ustart, self.f )
        # RHS Uzawa
        b_uz = self.__rhs_uzawa(ustart, b)
        # Solve Uzawa
        print 'solving uzawa'
        [p_glob, flag] = self.outer_solver.solve( self.U, b_uz, 
                                                  pstart.glob() )
        #print 'U_pre*b=',self.U_pre*b_uz
        
        #[p_glob, flag] = spl.cg( self.U, b_uz, 
        #                         x0 = pstart.glob(), 
        #                         tol = 1e-10,
        #                         maxiter = 2000,
        #                         M = self.U_pre)
        pend.basis_coeff = self.SpaceGL.mapping_q( p_glob )
        print 'solving uzawa stop. flag=',flag
        # Momentum
        if self.Space.dim == 2:
            # u  
            b_x = self.M*ustart[0].glob() + \
                  self.Time.h*( b[0] - self.G_x*p_glob )
            #[u_x, flag] = self.inner_solver.solve( self.H, b_x, 
            #                                       ustart[0].glob() )
            [u_x, flag] = spl.cg( self.H, b_x, x0 = ustart[0].glob(), 
                                  tol = 1e-15,
                                  maxiter = 1000,
                                  M = self.P)
            print 'x mom flag=',flag
            uend[0].basis_coeff = self.Space.mapping_q(u_x)
            # v
            b_y = self.M * ustart[1].glob() + \
                  self.Time.h*( b[1] - self.G_y*p_glob )
                  
            #[u_y, flag] = self.inner_solver.solve( self.H, b_y, 
            #                                   ustart[1].glob() )
            [u_y, flag] = spl.cg( self.H, b_y, x0 = ustart[1].glob(), 
                                  tol = 1e-15,
                                  maxiter = 1000,
                                  M = self.P)
            print 'y mom flag=',flag
            uend[1].basis_coeff = self.Space.mapping_q(u_y)
        
        return uend, pend
                    
    def __rhs_uzawa(self,u, b):
        print 'rhs uzawa..'
        if self.Space.dim == 2:
            
            # u component
            b_x = self.M * u[0].glob() + self.Time.h * b[0]
            [t_x, flag] = self.inner_solver.solve( self.H, b_x, u[0].glob() )
            #[t_x, flag] = spl.cg( self.H, b_x, x0 = u[0].glob(), 
            #                      tol = 1e-15,
            #                      maxiter = 1000,
            #                      M = self.P)
            print 't_x rhs flag=',flag
            # v component
            b_y = self.M * u[1].glob() + self.Time.h * b[1]
            [t_y, flag] = self.inner_solver.solve( self.H, b_y, u[1].glob() )
            #[t_y, flag] = spl.cg( self.H, b_y, x0 = u[1].glob(), 
            #                      tol = 1e-15,
            #                      maxiter = 1000,
            #                      M = self.P)
            print 't_y rhs flag=',flag
            # Divergence
            b_uz = ( 1.0 / self.Time.h ) * ( self.D_x*t_x + self.D_y*t_y )
            #print '2 rhs cg=',flag
            
        #if self.Space.dim == 3:
        #    # u component
        #    [t_x, flag] = self.inner_solver.solve( self.A, 
        #                            self.b[0], self.u[0].glob())
        #    # v component
        #    [t_y, flag] = self.inner_solver.solve( self.A, 
        #                            self.b[1], self.u[1].glob())
        #    # w component
        #    [t_z, flag] = self.inner_solver.solve( self.A, 
        #                            self.b[2], self.u[2].glob())
        #    # Divergence
        #    b = self.D_x*t_x + self.D_y*t_y + self.D_z*t_z
        #print '..rhs.'
        print 'rhs uzawa stop.'    
        return b_uz
        
        