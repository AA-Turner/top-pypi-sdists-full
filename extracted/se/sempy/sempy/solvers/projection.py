import sempy
import numpy as np
import scipy.sparse.linalg as spl

import sempy.basic.basic_f90 as basic_f90

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

from matplotlib import rcParams
rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True

import time



def bdf1ex1():
     """
     Euler method 1st order.
     """
     alpha = np.zeros(2) #: time derivative
     beta  = np.zeros(2) #: implicit terms
     gamma = np.zeros(2) #: explicit terms
     eta = np.zeros(2) #: explicit terms
     alpha[1],alpha[0] = 1.0,-1.0 #: time derivative
     beta[1], beta[0] = 1.0, 0.0  #: implicit terms
     gamma[1],gamma[0] = 0.0, 1.0  #: explicit terms
     eta[1],eta[0] = 0.0, 1.0
     levels = 2 
     return alpha,beta,gamma,eta,levels

 
def cnab2ex2():
     """Modified Crank-Nicolson/Adams-Bashforth 2nd order."""
     alpha, beta, gamma, eta = np.zeros(3), np.zeros(3), np.zeros(3), \
                               np.zeros(3)
     alpha[2], alpha[1], alpha[0] = 1.0, -1.0, 0.0
     beta[2], beta[1], beta [0] = 0.5, 0.5, 0.0
     gamma[2], gamma[1], gamma[0] = 0.0, 1.5, -0.5
     eta[2], eta[1], eta[0] = 0.0, 1.5, -0.5
     levels = 3
     return alpha, beta, gamma, eta, levels
 
def cnab2ex1():
     """Modified Crank-Nicolson/Adams-Bashforth 2nd order."""
     alpha, beta, gamma, eta = np.zeros(3), np.zeros(3), np.zeros(3), \
                               np.zeros(3)
     alpha[2], alpha[1], alpha[0] = 1.0, -1.0, 0.0
     beta[2], beta[1], beta [0] = 0.5, 0.5, 0.0
     gamma[2], gamma[1], gamma[0] = 0.0, 1.5, -0.5
     eta[2], eta[1], eta[0] = 0.0, 1.0, 0.0
     levels = 3
     return alpha, beta, gamma, eta, levels
 
def mcnab2ex2():
     """Modified Crank-Nicolson/Adams-Bashforth 2nd order."""
     alpha, beta, gamma, eta = np.zeros(3), np.zeros(3), np.zeros(3), \
                               np.zeros(3)
     alpha[2], alpha[1], alpha[0] = 1.0, -1.0, 0.0
     beta[2], beta[1], beta [0] = 9.0/16.0, 6.0/16.0, 1.0/16
     gamma[2], gamma[1], gamma[0] = 0.0, 1.5, -0.5
     eta[2], eta[1], eta[0] = 0.0, 1.5, -0.5
     levels = 3
     return alpha, beta, gamma, eta, levels
 
def cnlf():
     """Crank-Nicolson/Leapfrog 2nd order"""
     alpha,beta,gamma =np.zeros(3),np.zeros(3),np.zeros(3)
     alpha[2],alpha[1],alpha[0]=1.0,0.0,-1.0
     beta[2] ,beta[1], beta [0]=1.0,0.0,1.0
     gamma[2],gamma[1],gamma[0]=0.0,2.0,0.0
     levels=3
     return alpha,beta,gamma,levels

def bdf2ex1():
     """Backward differentiation formula/extrapolation 2nd order"""
     alpha, beta, gamma, eta = \
          np.zeros(3), np.zeros(3), np.zeros(3), np.zeros(3)
     alpha[2], alpha[1], alpha[0] = 1.5, -2.0, 0.5
     beta[2] ,beta[1], beta [0] = 1.0, 0.0, 0.0
     gamma[2], gamma[1], gamma[0] = 0.0, 2.0, -1.0
     eta[2], eta[1], eta[0] = 0.0, 1.0, 0.0
     levels = 3
     return alpha, beta, gamma, eta, levels
 
def bdf2ex2():
     """Backward differentiation formula/extrapolation 2nd order"""
     alpha, beta, gamma, eta = \
          np.zeros(3), np.zeros(3), np.zeros(3), np.zeros(3)
     alpha[2], alpha[1], alpha[0] = 1.5, -2.0, 0.5
     beta[2] ,beta[1], beta [0] = 1.0, 0.0, 0.0
     gamma[2], gamma[1], gamma[0] = 0.0, 2.0, -1.0
     eta[2], eta[1], eta[0] = 0.0, 2.0, -1.0
     levels = 3
     return alpha, beta, gamma, eta, levels

def bdf3ex2():
     """Backward differentiation formula/extrapolation 2nd order"""
     alpha, beta, gamma,eta = \
        np.zeros(4), np.zeros(4), np.zeros(4), np.zeros(4)
     alpha[3] =  11.0/6.0
     alpha[2] = -3.0
     alpha[1] =  3.0/2.0
     alpha[0] = -1.0/3.0
     beta[3], beta[2], beta[1], beta[0] =  1.0, 0.0, 0.0, 0.0
     gamma[3], gamma[2], gamma[1], gamma[0] = 0.0, 3.0, -3.0, 1.0
     eta[3], eta[2], eta[1], eta[0] = 0.0, 2.0, -1.0, 0.0
     #gamma[3], gamma[2], gamma[1], gamma[0] = 0.0, 2.0, -1.0, 0.0
     levels = 4
     return alpha, beta, gamma, eta,levels

def bdf3ex3():
     """Backward differentiation formula/extrapolation 2nd order"""
     alpha, beta, gamma,eta = \
        np.zeros(4), np.zeros(4), np.zeros(4), np.zeros(4)
     alpha[3] =  11.0/6.0
     alpha[2] = -3.0
     alpha[1] =  3.0/2.0
     alpha[0] = -1.0/3.0
     beta[3], beta[2], beta[1], beta[0] =  1.0, 0.0, 0.0, 0.0
     gamma[3], gamma[2], gamma[1], gamma[0] = 0.0, 3.0, -3.0, 1.0
     eta[3], eta[2], eta[1], eta[0] = 0.0, 3.0, -3.0, 1.0
     #gamma[3], gamma[2], gamma[1], gamma[0] = 0.0, 2.0, -1.0, 0.0
     levels = 4
     return alpha, beta, gamma, eta,levels

def bdf4ex2():
     """Backward differentiation formula/extrapolation 2nd order"""
     alpha, beta, gamma,eta = \
        np.zeros(5), np.zeros(5), np.zeros(5), np.zeros(5)
     alpha[4] =   25.0 / 12.0
     alpha[3] = - 4.0
     alpha[2] =   3.0
     alpha[1] = - 4.0 / 3.0
     alpha[0] =   1.0 / 4.0
     beta[4]  =   1.0
     gamma[4], gamma[3], gamma[2], gamma[1], gamma[0] = \
          0.0, 4.0, -6.0, 4.0, -1.0
     #eta[4], eta[3], eta[2], eta[1],eta[0] = 0.0, 3.0, -3.0, 1.0, 0.0
     eta[4], eta[3], eta[2], eta[1],eta[0] = 0.0, 2.0, -1.0, 0.0, 0.0
     levels = 5
     return alpha, beta, gamma, eta,levels
 
def bdf4ex4():
     """Backward differentiation formula/extrapolation 2nd order"""
     alpha, beta, gamma,eta = \
        np.zeros(5), np.zeros(5), np.zeros(5), np.zeros(5)
     alpha[4] =   25.0 / 12.0
     alpha[3] = - 4.0
     alpha[2] =   3.0
     alpha[1] = - 4.0 / 3.0
     alpha[0] =   1.0 / 4.0
     beta[4]  =   1.0
     gamma[4], gamma[3], gamma[2], gamma[1], gamma[0] = \
          0.0, 4.0, -6.0, 4.0, -1.0
     eta[:] = gamma[:]
     #gamma[3], gamma[2], gamma[1], gamma[0] = 0.0, 2.0, -1.0, 0.0
     levels = 5
     return alpha, beta, gamma, eta,levels

def __bc__(u,T,t):
    '''
    An empy BC function.
    '''
    return

#class LinCN
 
class ProjectionMethod:
    '''
    A projection-/pressure-correction method for the solution of the 
    Navier-Stokes equations 
    
    .. .. math::
    
       \\frac{\partial\mathbf u}{\partial t}=
         -\\nabla p +\\text{Re}^{-1}\\nabla^2\mathbf u
         -\\text{Ri}\\frac{\\mathbf g}{||\mathbf g||} 
         +\mathbf f
    
    .. math::
       \\frac{\partial\mathbf u}{\partial t}+
       \mathbf u\\cdot\\nabla\mathbf u=
         -\\nabla p +\\text{Re}^{-1}\\nabla^2\mathbf u
         -\\text{Ri}\\frac{\\mathbf g}{||\mathbf g||}T  
         +\mathbf f
         
    .. math::
       \\nabla\\cdot\mathbf u= 0
    
    .. math::
       \\frac{\partial T}{\partial t}+
       \mathbf u\\cdot\\nabla T= \\text{Pe}^{-1}\\nabla^2 T + f_T
    
    using multistep methods    
    
    .. math::
    
       \\frac{\\alpha_0 \mathbf {\hat u}^{n+1}+
       \\sum_{i=1}^s \\alpha_i \mathbf u^{n+1-i}}{h}=-
       \\nabla p^\star +
       \\sum_{i=0}^s\\beta_i\\mu\\nabla^2\mathbf {\hat u}^{n+1-i} +
       \\sum_{i=0}^s\\gamma_i \mathbf f^{n+1-i}
    
    where 
    
    .. math::
    
       p^\\star = \\sum_{i=0}^s\\eta_i p^{n+1-i}
    
    :param Space: Discrete space.
    :type Space: :class:`sempy.Space`
    :param SpaceGL: Discrete space.
    :type SpaceGL: :class:`sempy.fluid.SpaceGL`
    :param Time: Temporal space.
    :type Time: :class:`sempy.ode.Time`
    :param u: Velocity
    :type u: :class:`sempy.VectorFunction`
    :param p: Pressure
    :type p: :class:`sempy.Function`
    :kwargs: * **mu** (:class:`sempy.Function`) - Viscosity. The default is 
               None. Then, :literal:`mu` is set to 1.
             * **kappa** (:class:`sempy.Function`) - Thermal conductivity. 
               The default is None. Then, :literal:`kappa` is set to 1.  
             * **method** (*string*) - The available methods are:
                   * :literal:`euler` 
                   * :literal:`mcnab2ex2`
                   * :literal:`bdf2ex1` 
                   * :literal:`bdf2ex2`
                   * :literal:`bdf3ex2`
             * **conv_term** (*boolean*) - Either :literal:`True` or 
               :literal:`False`. 
             * **bound_cond** (*function*) - A function controlling 
               strong BCs. Called as :literal:`bound_cond(u,T,t)`. 
             * **neumann_cond** (*function*) - A function controlling 
               Neumann BCs. Default is :literal:`None`. 
             * **force_function** (*function*) - The forcing function 
               :math:`\\mathbf f` in the above equation. Default is 
               :literal:`None`. 
             * **init_steps** (*int*) - Number of steps to kick start higher 
               order methods. 
             * **chi** (*float*) - A value between 0 and 1. The default value 
               is 0.5.  
             * **hyper_filter** (boolean) - Hyperbolic filter. To apply it 
               set it to :literal:`True`.  
             * **isothermal** (boolean) - Default is True.  
             * **deflation_solver** (*boolean*) - To use the deflation 
               solver, set *deflation_solver* to :literal:`True` (default), 
               otherwise to :literal:`False`.   
             * **tol** (*float*) - Iterative tolerance.
             * **file_increment** (*int*) - The distance between time-steps 
               to be printed to file. 
             * **call_back** (*function*) - A call-back function. The 
               function is called as :literal:`call_back(u,p,T,t,i)`, 
               where u is velocoity, p is pressure, t is time and 
               i is the time-step number.  
    
    .. To solve the time-dependent iso-thermal Stokes problem. set
    
      * :literal:`conv_term` = False
      * :literal:`Re` = 1
      * :literal:`Ri` = 0

    '''
    def __init__( self, Space, SpaceGL, Time, u, p, T= None,  
                  mu = None , kappa = None, Ri = 0.0,
                  method = bdf1ex1, conv_term = False,
                  bound_cond = __bc__ , force_function = None,
                  init_steps = 1, neumann_cond = None, chi = 0.5,
                  deflation_solver = True, call_back = None,
                  hyper_filter = False,
                  isothermal = True, 
                  tol = 1e-09, file_increment =100):
        self.Space = Space
        self.SpaceGL = SpaceGL
        self.u = u
        self.p = p
        self.T = T
        self.isothermal = isothermal
        if self.T == None:
            self.T = sempy.Function( self.Space )
        if kappa == None:
            self.kappa = sempy.Function( self.T.Space, basis_coeff =  1.0 )
        else:
            self.kappa = kappa
        self.Ri = Ri
            
        self.Time = Time
        self.conv_term = conv_term
        self.method = method
        self.bound_cond = bound_cond
        self.call_back = call_back
        self.hyper_filter = hyper_filter
        self.file_increment = file_increment
        if init_steps <= 1:
            self.init_steps = 1
        else:
            self.init_steps = init_steps
        self.alpha, self.beta, self.gamma, self.eta, self.levels = \
                self.method()
        self.chi = chi
        self.deflation_solver = deflation_solver
        self.tol = tol
        if force_function == None:
            self.force_function = self.__emptyfunc__
        else:
            self.force_function = force_function
        # Neumann cond 
        if neumann_cond == None:
            self.neumann_cond = self.__empty_neumann__
        else:
            self.neumann_cond = neumann_cond
            
        
        # Transport coefficient
        if mu == None:
            mu_dummy = sempy.Function( self.Space, basis_coeff =  1.0 )
            self.mu = mu_dummy
        else:
            self.mu = mu
        # Interpolated viscosicty
        self.mu_gl =  sempy.Function( self.SpaceGL, 
            basis_coeff =  self.SpaceGL.interpolation( self.mu.basis_coeff ) )
        # Laplacian
        self.lap = sempy.operators.Laplacian( self.Space, mu = self.mu,
                                              fem_assemble = 'yes',
                                              silent = True )
        self.A = self.lap.matrix
        self.A_fem = self.lap.matrix_fem
        # Convection
        self.conv = sempy.operators.Convection( self.Space, silent = True )    
        # Mass matrix
        mass = sempy.operators.Mass( self.Space )
        self.M = mass.matrix
        self.M_inv = mass.matrix_inv
        # Divergence operator
        self.D = sempy.fluid.Divergence( self.Space, self.SpaceGL ).matrix
        # Gradient operator
        self.G = sempy.fluid.Gradient( self.Space, self.SpaceGL ).matrix
        # Helmholtz operator
        self.H = sempy.operators.MultipleOperators( 
                            [ self.M, self.A ],
                            [ self.alpha[self.levels-1],
                              self.Time.h*self.beta[self.levels-1] ],
                            assemble = 'no').matrix
        self.H_fem = sempy.operators.MultipleOperators( 
                            [self.M,self.A_fem],
                            [self.alpha[self.levels-1],
                            self.Time.h * self.beta[self.levels-1] ],
                            assemble = 'yes' ).matrix
        #del self.A_fem
        self.H_pre = sempy.precond.Preconditioner( self.Space, 
                                                   [self.H_fem], 
                                                   drop_tol = 0.0 ).matrix
        del self.H_fem
        # Consistent pressure Poisson operator
        self.poisson_operator = spl.LinearOperator( 
                          ( self.SpaceGL.dof,self.SpaceGL.dof ),
                            matvec = self.__action_poisson__,
                            dtype = 'float' )
        # Uzawa operator
        #self.uzawa_operator = spl.LinearOperator( 
        #                  ( self.SpaceGL.dof,self.SpaceGL.dof ),
        #                    matvec = self.__action_uzawa__,
        #                    dtype = 'float' )
        # Helmholtz solver
        #helmholtz_tol = self.tol / 1000.0
        self.helmholtz_solver = sempy.linsolvers.Krylov(
                                                #tol = 1e-14,#helmholtz_tol,
                                                #tol = 1e-15,
                                                tol = 1e-17,
                                                solver_type = 'bicgstab',
                                                pre = self.H_pre 
                                                )
        # Poisson solver
        self.poisson_solver = sempy.linsolvers.Krylov(
                                                tol = self.tol,
                                                solver_type = 'cg')
        if self.deflation_solver:# == 'yes':
            self.deflation = sempy.fluid.Deflation( self.Space, 
                                                self.SpaceGL, 
                                                self.poisson_operator,
                                                tol = self.tol )
        # Temperatur:
        if not self.isothermal:
            self.temperature_matrices()
            
    def space_check(self):
        '''
        '''
        X = self.Space
        X_T = self.T.Space
        if self.Space.dim == 1:
            delta = 0.0
            for k in range(X.noe):
                for m in range(X.n):
                    delta = delta + np.abs(X.x[k,m]-X_T.x[k,m])
        if self.Space.dim == 2:
            delta = 0.0
            for k in range(X.noe):
                for m in range(X.n):
                    for n in range(X.n):
                        delta = delta + np.abs(X.x[k,m,n]-X_T.x[k,m,n])
            #print 'delta =',delta
        if self.Space.dim == 3:
            delta = 0.0
            for k in range(X.noe):
                for m in range(X.n):
                    for n in range(X.n):
                        for o in range(X.n):
                            delta = delta +\
                                    np.abs(X.x[k,m,n,o]-X_T.x[k,m,n,o])
            #print 'delta =',delta
        return delta
                
    def temperature_matrices(self):
        # Mass matrix
        mass_T = sempy.operators.Mass( self.T.Space )
        self.M_T = mass_T.matrix
        self.M_inv_T = mass_T.matrix_inv
        # Conduction operator
        self.conduction = sempy.operators.Laplacian( self.T.Space, 
                                               mu = self.kappa,
                                               fem_assemble = 'yes',
                                               silent=True )
        self.A_T = self.conduction.matrix
        self.A_fem_T = self.conduction.matrix_fem
        # Convection operator
        self.conv_T = sempy.operators.Convection( self.T.Space, 
                                                  silent = True )   
        # Helmholtz operator
        self.H_T = sempy.operators.MultipleOperators( 
                            [ self.M_T, self.A_T ],
                            [ self.alpha[self.levels-1],
                              self.Time.h*self.beta[self.levels-1] ],
                            assemble = 'no').matrix
        H_fem_T = sempy.operators.MultipleOperators( 
                            [self.M_T,self.A_fem_T],
                            [self.alpha[self.levels-1],
                            self.Time.h * self.beta[self.levels-1] ],
                            assemble = 'yes' ).matrix
        #del self.A_fem
        self.H_pre_T = sempy.precond.Preconditioner( self.T.Space, 
                                                   [H_fem_T], 
                                                   drop_tol = 0.0 ).matrix
        del H_fem_T
        # Solver for the energy equation:
        self.helmholtz_solver_T = sempy.linsolvers.Krylov(
                                                tol = 1e-17,
                                                solver_type = 'bicgstab',
                                                pre = self.H_pre_T 
                                                )
            
    def solve_momentum( self, u, p, T ):
        '''
        '''
        # Solve the energy equation:
        if not self.isothermal:
            F = self.__rhs_T__( T, u )
            s, flag = self.helmholtz_solver_T.solve( 
                                            self.H_T, F, 
                                            T[self.levels-1].glob() )
            T[self.levels-1].basis_coeff = self.T.Space.mapping_q( s )
            print 'T flag=',flag
            
        # Solve the momentum equations:
        F = self.__rhs__( u, p, T )
        for i in range(self.Space.dim):
            s, flag = self.helmholtz_solver.solve( 
                                            self.H, F[i], 
                                            u[self.levels-1][i].glob() )
            u[self.levels-1][i].basis_coeff = self.Space.mapping_q( s )
            print 'i=',i,'flag=',flag
        return u, T
    
    def solve_pressure( self, u ):
        # Calculate the RHS of the pressure Poisson equation.
        
        # Divergence of the tentative velocity field:
        s = np.zeros( ( self.SpaceGL.dof ), float )
        for i in range( self.Space.dim ) :
            s = s + self.D[i] * u[self.levels-1][i].glob()
        coeff =  self.alpha[self.levels-1] / self.Time.h 
        s = coeff * s
        # Compatibility condition
        if self.SpaceGL.zero == 'yes':
            s_sum = s.sum()
            coeff = s_sum / np.float( self.SpaceGL.dof )
            s = s - coeff
        # Solve the pressure Poisson equation with the deflation solver:
        phi = np.zeros( ( self.SpaceGL.dof ), float )
        t1 = time.clock()
        if self.deflation_solver == False:
            [phi, flag] = self.poisson_solver.solve( self.poisson_operator, 
                                                     s, phi )
        else:
            [phi, flag] = self.deflation.solve( s, phi )
        
        t2 = time.clock()
        print 'Poisson cg it=',flag,'exe time=',t2-t1    
        
        return phi
    
    
    def update( self, p, phi, u ):
        # Update pressure
        
        # p_star:
        p_star = np.zeros( ( self.SpaceGL.dof ), float )
        
        if self.method == sempy.solvers.mcnab2ex2 or \
           self.method == sempy.solvers.cnab2ex2 :
            p_star = 2.0 * p[1].glob() - p[0].glob()
            
        else:
            for i in range( self.levels - 1 ):
                if abs( self.eta[i] ) > 0:
                    #p_star = p_star + self.eta[i] * p[i].glob()
                    p_star = basic_f90.vector_add( p_star,
                                                   self.eta[i],
                                                   p[i].glob() )
        
        # Divergence (only works for BDF. Otherwise: multiply with beta)
        s = np.zeros( ( self.SpaceGL.dof ), float )
        for i in range( self.Space.dim ) :
            s = s + self.D[i] * u[self.levels-1][i].glob()
        #print 'beta max=',self.beta[self.levels-1]
        #s = self.beta[self.levels-1]*self.chi * \
        #        ( self.SpaceGL.mass_inv * s )
        s = self.chi * ( self.SpaceGL.mass_inv * s )
        # account for viscosity
        s = self.mu_gl.glob()*s
        # Update pressure:
        if self.method == sempy.solvers.mcnab2ex2 or \
           self.method == sempy.solvers.cnab2ex2 :
            p[self.levels-1].basis_coeff = \
                 self.SpaceGL.mapping_q( p_star + 2.0*phi + s )
        else:
            p[self.levels-1].basis_coeff = \
                 self.SpaceGL.mapping_q( p_star + phi + s )
        
        # - Compatibility condition
        if self.SpaceGL.zero == 'yes':
            p_int = p[self.levels-1].quadrature()
            ones = sempy.Function( self.SpaceGL, basis_coeff = 1.0 )
            omega_int = self.SpaceGL.quadrature( ones.basis_coeff )
            p[self.levels-1].set_value( p[self.levels-1].basis_coeff - \
                                        p_int/omega_int )
        # Update velocity
        coeff = self.Time.h / self.alpha[self.levels-1] 
        for i in range(self.Space.dim):
            s =  self.M_inv * ( self.G[i] * phi )
            u_temp = basic_f90.vector_add(
                                  u[self.levels-1][i].glob(), -coeff, s )
            u_temp = self.Space.mapping_q( u_temp )
            u[self.levels-1][i].basis_coeff = np.copy( u_temp )
        
        # Check divergence
        #s = np.zeros( ( self.SpaceGL.dof ), float )
        #for i in range( self.Space.dim ) :
        #    s = s + self.D[i] * u[self.levels-1][i].glob()
        #print 'norm div after proj=',np.sqrt(np.dot(s,s))
             
        return p, u
    
    
    def __initialize( self, u_0, p_0, T_0, start, end ):
        #print 'initialize...'
        # Temporal domain
        t2 = sempy.ode.Time( self.Space,start_time = start,
                             end_time = end,
                             time_steps = self.init_steps )
        # Solution vectors 
        u_init = sempy.VectorFunction( self.Space )
        p_init = sempy.Function( self.SpaceGL )
        T_init = sempy.Function( self.T.Space )
    
        p_init.basis_coeff = np.copy( p_0.basis_coeff )
        T_init.basis_coeff = np.copy( T_0.basis_coeff )
        for j in range(self.Space.dim) :
            u_init[j].basis_coeff = np.copy( u_0[j].basis_coeff )
        
        eul = ProjectionMethod( self.Space, 
                                self.SpaceGL, 
                                t2, 
                                u_init, p_init, T = T_init,
                                mu = self.mu,
                                kappa = self.kappa,
                                Ri = self.Ri,
                                method = bdf1ex1, 
                                conv_term = self.conv_term,
                                bound_cond = self.bound_cond, 
                                force_function = self.force_function,
                                neumann_cond = self.neumann_cond,
                                chi = 1.0,
                                deflation_solver = self.deflation_solver, 
                                hyper_filter = self.hyper_filter,
                                isothermal = self.isothermal,
                                tol = self.tol,
                                file_increment = 1000 )
         
        u_init, p_init, T_init = eul.solve()
        del eul
        return u_init, p_init, T_init
        
    def solve(self):
        '''
        Solve the problem. 
        
        :returns: * **u** - Velocity
                  * **p** - Pressure
        '''
        #
        delta = self.space_check()
        if delta > 1.0e-04:
            print 'Spaces for u and T are not compatible.'
            return self.u, self.p, self.T
        # Solution functions:
        u = [ ]
        p = [ ]
        T = [ ]
        
        for i in range(self.levels):
            u.append( sempy.VectorFunction( self.Space ) )
            p.append( sempy.Function( self.SpaceGL ) )
            T.append( sempy.Function( self.T.Space ) )
        # Setting initial values:
        for i in range(self.levels):
            p[i].basis_coeff = np.copy( self.p.basis_coeff )
            for j in range(self.Space.dim) :
                u[i][j].basis_coeff = np.copy( self.u[j].basis_coeff )
            T[i].basis_coeff = np.copy( self.T.basis_coeff )
        # Timesteps to file:
        k_file = range( self.file_increment, 
                        self.Time.time_steps+self.file_increment, 
                        self.file_increment )
        
        # Initial value to file:        
        if not self.u.filename == 'none':
            self.u.to_file()
        if not self.p.filename == 'none':
            self.p.to_file()
        if not self.T.filename == 'none':
            self.T.to_file()
        # -- Callback
        if not self.call_back == None:
            self.call_back(self.u,self.p,self.T,self.Time.time,0)
        #-- Initialize
        factor = 0.0
                
        for i in range( 0, self.levels-2 ):
            print '--> Time step number x: ', i+1,'time=',self.Time.time
            self.Time.increment()
            factor = factor + 1.0
            u_dum, p_dum, T_dum = self.__initialize( 
                                        u[i], p[i], T[i],
                                        ( factor - 1.0 ) * self.Time.h,
                                        factor*self.Time.h )
            p[i+1].basis_coeff = np.copy( p_dum.basis_coeff )
            T[i+1].basis_coeff = np.copy( T_dum.basis_coeff )
            for j in range(self.Space.dim) :
                u[i+1][j].basis_coeff = np.copy( u_dum[j].basis_coeff )
            del u_dum, p_dum, T_dum
            # -- Callback
            if not self.call_back == None:
                for j in range(self.Space.dim):
                    self.u[j].basis_coeff = np.copy( u[i+1][j].basis_coeff )
                self.p.basis_coeff = np.copy(p[i+1].basis_coeff)
                self.T.basis_coeff = np.copy(T[i+1].basis_coeff)
                self.call_back(self.u, self.p, self.T,self.Time.time, i+1)
            # To file
            if (i+1) in k_file:
                self.to_file(u[i+1],p[i+1],T[i+1])
        #print '0 u',u[0][0].basis_coeff[5,2,2]
        #print '0 u',u[1][0].basis_coeff[5,2,2]
        #print '0 u',u[2][0].basis_coeff[5,2,2]
        # Level 1
        #print 'obs! ProjMethod: use only second order.'
        #self.Time.increment()
        #x_gl = self.SpaceGL.x
        #y_gl = self.SpaceGL.y
        #x = self.Space.x
        #y = self.Space.y
        
        # Test Guermond
        #ic = np.sin( x_gl - y_gl + self.Time.time )
        #p[1].basis_coeff = np.copy( ic )
        #ic1 = np.sin( x + self.Time.time )*np.sin( y + self.Time.time )
        #ic2 = np.cos( x + self.Time.time )*np.cos( y + self.Time.time )
        #u[1][0].basis_coeff = np.copy( ic1 )
        #u[1][1].basis_coeff = np.copy( ic2 )
        # Test Kim and Moin
        #t=self.Time.time
        #ic = -0.5*(np.sin(np.pi*x_gl) + np.sin(np.pi*y_gl))*np.cos(np.pi*t)
        #p[1].basis_coeff = np.copy( ic ) 
        #ic1 = -np.sin(np.pi*x)*np.cos(np.pi*y)*np.cos(np.pi*t)
        #ic2 =  np.cos(np.pi*x)*np.sin(np.pi*y)*np.cos(np.pi*t)
        #u[1][0].basis_coeff = np.copy( ic1 )
        #u[1][1].basis_coeff = np.copy( ic2 )

        # Level 2
        #self.Time.increment()
        #ic = np.sin( x_gl - y_gl + self.Time.time )
        #p[2].basis_coeff = np.copy( ic )      
        #ic1 = np.sin( x + self.Time.time )*np.sin( y + self.Time.time )
        #ic2 = np.cos( x + self.Time.time )*np.cos( y + self.Time.time )
        #u[2][0].basis_coeff = np.copy( ic1 )
        #u[2][1].basis_coeff = np.copy( ic2 )
        
        # Time stepping
        for k in range( self.levels-2, self.Time.time_steps ):
            print '--> Time step number: ', k+1,'time=',self.Time.time
            self.Time.increment()
            
            # Solve the momentum equations:
            self.bound_cond( u[self.levels-1], T[self.levels-1], 
                             self.Time.time )
            u, T = self.solve_momentum( u, p, T )
            
                               
            # Solve the pressure Poisson equation
            phi = self.solve_pressure( u )
            
            # Update pressure and velocity
            p, u = self.update( p, phi, u )
            
            # Hyperbolic filter
            if self.hyper_filter:
                for i in range(self.Space.dim):
                    u[self.levels-1][i].hyper_filter()
                if not self.isothermal:
                    T[self.levels-1].hyper_filter()
                self.bound_cond( u[self.levels-1], T[self.levels-1],
                                 self.Time.time )
            
            # Implicit correction
            #u = self.implicit_correction(u,p)
                    
            # Update solution array
            for i in range( self.levels-1 ):
                p[i].basis_coeff = np.copy( p[i+1].basis_coeff )
                for j in range(self.Space.dim) :
                    u[i][j].basis_coeff = np.copy( u[i+1][j].basis_coeff )
                T[i].basis_coeff = np.copy( T[i+1].basis_coeff )
            # -- Callback
            if not self.call_back == None:
                for i in range(self.Space.dim):
                    self.u[i].basis_coeff = \
                             np.copy( u[self.levels-1][i].basis_coeff )
                self.p.basis_coeff = \
                      np.copy(p[self.levels-1].basis_coeff)
                self.T.basis_coeff = \
                      np.copy(T[self.levels-1].basis_coeff)
                self.call_back(self.u,self.p,self.T,self.Time.time,k+1)
            # Print to file
            #if not self.u.filename == 'none':   
            if (k+1) in k_file:
                self.to_file(u[self.levels-1], p[self.levels-1], 
                             T[self.levels-1])
                
        print 'end time=',self.Time.time
        # Return values
        for i in range(self.Space.dim):
            self.u[i].basis_coeff = np.copy( u[self.levels-1][i].basis_coeff )
        self.p.basis_coeff = np.copy(p[self.levels-1].basis_coeff)
        self.T.basis_coeff = np.copy(T[self.levels-1].basis_coeff)
        return self.u, self.p, self.T
    
    def to_file(self,u,p,T):
        '''
        Print to file.
        '''
        for i in range(self.Space.dim):
            self.u[i].basis_coeff = \
                          np.copy( u[i].basis_coeff )
                          #np.copy( u[self.levels-1][i].basis_coeff )
        self.p.basis_coeff = \
                     np.copy(p.basis_coeff)
                     #np.copy(p[self.levels-1].basis_coeff)
        self.T.basis_coeff = \
                     np.copy(T.basis_coeff)
                     #np.copy(T[self.levels-1].basis_coeff)
        if not self.u.filename == 'none':
            self.u.to_file()
        if not self.p.filename == 'none':
            self.p.to_file()
        if not self.T.filename == 'none':
            self.T.to_file()
            
    def assemble_helmholtz_matrices(self,u):
        # Extrapolate the velocity field
        if self.Space.dim == 1:
            u_ext = np.zeros( (1,self.Space.noe, self.Space.n),
                               float )
        if self.Space.dim == 2:
            u_ext = np.zeros( (2,self.Space.noe, self.Space.n,self.Space.n),
                               float )
        if self.Space.dim == 3:
            u_ext = np.zeros( (3,self.Space.noe, self.Space.n, self.Space.n, 
                               self.Space.n),float )
        # 
        if self.levels == 2:
            for j in range( self.Space.dim ):
                u_ext[j] =  u[0][j].basis_coeff
        if self.levels == 3:
            for j in range( self.Space.dim ):
                u_ext[j] = 2.0*u[1][j].basis_coeff - u[0][j].basis_coeff
                    
        #for j in range( self.Space.dim ):
        #    for i in range( self.levels -1 ) :
        #        if abs( self.gamma[i] ) > 0.0 :
        #            u_ext[j] = u_ext[j] + self.gamma[i]*u[i][j].basis_coeff
        # Convection operator            
        if self.Space.dim ==1:
            self.conv.u_conv = [ u_ext[0] ]
            self.conv_T.u_conv = [ u_ext[0] ]
        if self.Space.dim ==2:
            self.conv.u_conv = [ u_ext[0], u_ext[1] ]
            self.conv_T.u_conv = [ u_ext[0], u_ext[1] ]
        if self.Space.dim ==3:
            self.conv.u_conv = [ u_ext[0], u_ext[1], u_ext[2] ]
            self.conv_T.u_conv = [ u_ext[0], u_ext[1], u_ext[2] ]
        
        self.conv.assemble_fem()
        C_fem = self.conv.matrix_fem
        ## Helmholtz operators
        self.H = sempy.operators.MultipleOperators( 
                            [ self.M, self.A, self.conv.matrix ],
                            [ self.alpha[self.levels-1],
                              self.Time.h*self.beta[self.levels-1],
                              self.Time.h*self.beta[self.levels-1] ],
                              assemble = 'no',
                              silent = True).matrix
        H_fem = sempy.operators.MultipleOperators( 
                            [self.M, self.A_fem, C_fem],
                            [ self.alpha[self.levels-1],
                            self.Time.h * self.beta[self.levels-1],
                            self.Time.h * self.beta[self.levels-1] ],
                            assemble = 'yes',
                            silent = True ).matrix
        del C_fem
        self.H_pre = sempy.precond.Preconditioner( self.Space, 
                                              [H_fem], 
                                              drop_tol = 0.5, 
                                              silent = True ).matrix
        del H_fem
        self.helmholtz_solver.pre = self.H_pre
        # Energy equation
        if not self.isothermal:
            self.H_T = sempy.operators.MultipleOperators( 
                            [ self.M_T, self.A_T, self.conv_T.matrix ],
                            [ self.alpha[self.levels-1],
                              self.Time.h*self.beta[self.levels-1],
                              self.Time.h*self.beta[self.levels-1] ],
                              assemble = 'no', silent = True).matrix
            self.conv_T.assemble_fem()
            C_fem_T = self.conv_T.matrix_fem
            H_fem = sempy.operators.MultipleOperators( 
                            [self.M_T, self.A_fem_T, C_fem_T],
                            [ self.alpha[self.levels-1],
                              self.Time.h * self.beta[self.levels-1],
                              self.Time.h * self.beta[self.levels-1] ],
                              assemble = 'yes', silent = True ).matrix
        del C_fem_T
        self.H_pre_T = sempy.precond.Preconditioner( self.T.Space, 
                                                     [H_fem], 
                                                     drop_tol = 0.5,
                                                     silent = True ).matrix
        del H_fem
        self.helmholtz_solver_T.pre = self.H_pre_T
        return      
    
    #def implicit_correction(self,u,p):
    #    #
    #    t1 = time.clock()        
    #    # Convection operator
    #    if self.Space.dim ==1:
    #        self.conv.u_conv = [ u[self.levels-1][0].basis_coeff ]
    #    if self.Space.dim ==2:
    #        self.conv.u_conv = [ u[self.levels-1][0].basis_coeff, 
    #                             u[self.levels-1][1].basis_coeff ]
    #    if self.Space.dim ==3:
    #        self.conv.u_conv = [ u[self.levels-1][0].basis_coeff,
    #                             u[self.levels-1][1].basis_coeff, 
    #                             u[self.levels-1][2].basis_coeff ]
    #    self.conv.assemble_fem()
    #    C_fem = self.conv.matrix_fem
    #    # Helmholtz operators
    #    H = sempy.operators.MultipleOperators( 
    #                        [ self.M, self.A, self.conv.matrix ],
    #                        [ self.alpha[self.levels-1],
    #                          self.Time.h*self.beta[self.levels-1],
    #                          self.Time.h*self.beta[self.levels-1] ],
    #                          assemble = 'no').matrix
    #    H_fem = sempy.operators.MultipleOperators( 
    #                        [self.M,self.A_fem, C_fem],
    #                        [ self.alpha[self.levels-1],
    #                          self.Time.h * self.beta[self.levels-1],
    #                          self.Time.h * self.beta[self.levels-1] ],
    #                        assemble = 'yes' ).matrix
    #    del C_fem
    #    #del self.A_fem
    #    H_pre = sempy.precond.Preconditioner( self.Space, 
    #                                          [H_fem], 
    #                                          drop_tol = 0.5 ).matrix
    #    del H_fem
    #    # Right hand side
    #    F = self.rhs_correction( u, p )
    #    # Solve the momentum equations:
    #    self.helmholtz_solver.pre = H_pre
    #    for i in range(self.Space.dim):
    #        s, flag = self.helmholtz_solver.solve(H, F[i], 
    #                                        u[self.levels-1][i].glob() )
    #        u[self.levels-1][i].basis_coeff = self.Space.mapping_q( s )
    #        print 'i=',i,'flag=',flag
    #    self.helmholtz_solver.pre = self.H_pre
    #    
    #    t2 = time.clock()
    #    print 'Correction time=',t2-t1    
    #    
    #    return u
    
    def rhs_correction(self, u, p, T ):
        '''
        The right hand side of the momentum equations.
         
        :param u: Velocity
        :param p: Pressure
        '''
        # RHS
        if self.Space.dim == 1:
            F1 = np.zeros( ( self.Space.dof ), float )
            F = [ F1 ]
        if self.Space.dim == 2:
            F1 = np.zeros( ( self.Space.dof ), float )
            F2 = np.zeros( ( self.Space.dof ), float )
            F = [ F1, F2 ]
        
        if self.Space.dim == 3:
            F1 = np.zeros( ( self.Space.dof ), float )
            F2 = np.zeros( ( self.Space.dof ), float )
            F3 = np.zeros( ( self.Space.dof ), float )
            F = [ F1, F2, F3 ]
                
        s = np.zeros( ( self.Space.dof ) )
        
        # Contribution from temporal derivative
        for j in range( self.Space.dim ) : 
            for i in range( self.levels - 1 ) :   
                if abs( self.alpha[i]) > 0 :
                    F[j] = F[j] - self.alpha[i] * self.M * u[i][j].glob()
                    
        # Contribution from the viscous term:
        for j in range( self.Space.dim ) :
            for i in range( 0, self.levels - 1 ) : 
                if abs( self.beta[i] ) > 0 :
                    s = self.A * u[i][j].glob()
                    F[j] = F[j] - self.Time.h * self.beta[i] * s
        
        # Contribution from the linear form stemming from the Laplacian
        for i in range( self.levels ) :
            if abs( self.beta[i] ) > 0 :
                local_time = self.Time.time - \
                             ( float( self.levels ) - 1.0 - \
                             float(i) ) * self.Time.h
                s1 = self.neumann_cond( local_time )
                for j in range( self.Space.dim ):
                    self.lap.g_neu = s1[j]
                    s = self.lap.assemble_linear_form()
                    #print 'j=',j,'s=',s 
                    F[j] = F[j] + self.Time.h * self.beta[i] * s
                    
        # Pressure gradient
        for j in range( self.Space.dim ) :
            for i in range( self.levels ) :
                if abs( self.beta[i] ) > 0 :
                    s = self.G[j] * p[i].glob()
                    F[j] = F[j] - self.Time.h * self.beta[i] * s
                
        # Forcing term
        for i in range( self.levels ):
            if abs(self.gamma[i]) > 0 :
                local_time = self.Time.time - \
                             ( float( self.levels ) - 1.0 - \
                             float(i) ) * self.Time.h
                s = self.force_function( u[i], p[i], local_time )
                for j in range( self.Space.dim ) :
                    F[j] = F[j] + self.Time.h * self.gamma[i] * self.M * s[j]
         
        return F    
        
    def __emptyfunc__( self, y, q, T, t ):
        """This is an empty function."""
        #v = np.zeros( ( y.size ) )
        v = sempy.VectorFunction( self.Space )
        s = np.zeros((self.T.Space.dof),float)
        if self.Space.dim == 1:
            return [ v.glob(),s ]
        if self.Space.dim == 2:
            return [ v[0].glob(), v[1].glob(),s ]
        if self.Space.dim == 3:
            return [ v[0].glob(),v[1].glob(), v[2].glob(),s ]
        
    def __empty_neumann__( self, t ):
        # Neumann
        if self.Space.dim == 1:
            bound_u = sempy.BoundaryFunction( self.Space )
            return [ bound_u ]
        
        if self.Space.dim == 2:
            bound_u = sempy.BoundaryFunction( self.Space )
            bound_v = sempy.BoundaryFunction( self.Space ) 
            return [ bound_u, bound_v ]
        
        if self.Space.dim == 3:
            bound_u = sempy.BoundaryFunction( self.Space )
            bound_v = sempy.BoundaryFunction( self.Space )
            bound_w = sempy.BoundaryFunction( self.Space )  
            return [ bound_u, bound_v, bound_w ]
        
    def __rhs__(self, u, p, T ):
        '''
        The right hand side of the momentum equations.
         
        :param u: Velocity
        :param p: Pressure
        '''
        # RHS
        if self.Space.dim == 1:
            F1 = np.zeros( ( self.Space.dof ), float )
            F = [ F1 ]
        if self.Space.dim == 2:
            F1 = np.zeros( ( self.Space.dof ), float )
            F2 = np.zeros( ( self.Space.dof ), float )
            F = [ F1, F2 ]
        
        if self.Space.dim == 3:
            F1 = np.zeros( ( self.Space.dof ), float )
            F2 = np.zeros( ( self.Space.dof ), float )
            F3 = np.zeros( ( self.Space.dof ), float )
            F = [ F1, F2, F3 ]
                
        s = np.zeros( ( self.Space.dof ), float )
        
        # Contribution from temporal derivative
        for j in range( self.Space.dim ) : 
            for i in range( self.levels - 1 ) :   
                if abs( self.alpha[i]) > 0 :
                    F[j] = F[j] - self.alpha[i] * self.M * u[i][j].glob()
        
        # Contribution from the buoyancy
        #for j in range( self.Space.dim ) :
        if np.abs(self.Ri) > 1e-15:
            for i in range( self.levels ) :
                if abs( self.beta[i]) > 0 :
                    coeff = self.Time.h * self.beta[i] * self.Ri
                    if self.Space.dim == 1:# and j == 0:
                        F[0] = F[0] + coeff * self.M * T[i].glob()
                    if self.Space.dim == 2:# and j == 1:
                        F[1] = F[1] + coeff * self.M * T[i].glob()            
                    if self.Space.dim == 3:# and j == 2:
                        F[2] = F[2] + coeff * self.M * T[i].glob()
                    
        # Contribution from the viscous term:
        for j in range( self.Space.dim ) :
            for i in range( self.levels - 1 ) : 
                if abs( self.beta[i] ) > 0 :
                    s = self.A * u[i][j].glob()
                    F[j] = F[j] - self.Time.h * self.beta[i] * s
        
        # Convection term
        #if not self.conv_term :
        #    for j in range( self.Space.dim ) :
        #        for i in range( self.levels -1 ) :
        #            if self.Space.dim ==1:
        #                self.conv.u_conv = [ u[i][0].basis_coeff ]
        #            if self.Space.dim ==2:
        #                self.conv.u_conv = [ u[i][0].basis_coeff, 
        #                                     u[i][1].basis_coeff ]
        #            if self.Space.dim ==3:
        #                self.conv.u_conv = [ u[i][0].basis_coeff,
        #                                     u[i][1].basis_coeff, 
        #                                     u[i][2].basis_coeff ]
        #            if abs( self.beta[i] ) > 0.0 :
        #                s = self.conv.matrix * u[i][j].glob()
        #                F[j] = F[j] - self.Time.h * self.beta[i] * s
        
        # Contribution from the linear form stemming from the Laplacian
        for i in range( self.levels ) :
            if abs( self.beta[i] ) > 0 :
                local_time = self.Time.time - \
                             ( float( self.levels ) - 1.0 - \
                             float(i) ) * self.Time.h
                s1 = self.neumann_cond( local_time )
                for j in range( self.Space.dim ):
                    self.lap.g_neu = s1[j]
                    s = self.lap.assemble_linear_form()
                    #print 'j=',j,'s=',s 
                    F[j] = F[j] + self.Time.h * self.beta[i] * s
                    
        # Pressure gradient
        for j in range( self.Space.dim ) :
            for i in range( self.levels ) :
                if abs( self.eta[i] ) > 0 :
                    s = self.G[j] * p[i].glob()
                    F[j] = F[j] - self.Time.h * self.eta[i] * s
                    
        # Convection term
        if self.conv_term :
            for j in range( self.Space.dim ) :
                for i in range( self.levels -1 ) :
                    if self.Space.dim ==1:
                        self.conv.u_conv = [ u[i][0].basis_coeff ]
                    if self.Space.dim ==2:
                        self.conv.u_conv = [ u[i][0].basis_coeff, 
                                             u[i][1].basis_coeff ]
                    if self.Space.dim ==3:
                        self.conv.u_conv = [ u[i][0].basis_coeff,
                                             u[i][1].basis_coeff, 
                                             u[i][2].basis_coeff ]
                    if abs( self.gamma[i] ) > 0.0 :
                        s = self.conv.matrix * u[i][j].glob()
                        F[j] = F[j] - self.Time.h * self.gamma[i] * s
        
        # Forcing term
        for i in range( self.levels ):
            if abs(self.gamma[i]) > 0 :
                local_time = self.Time.time - \
                             ( float( self.levels ) - 1.0 - \
                             float(i) ) * self.Time.h
                s = self.force_function( u[i], p[i], T[i], local_time )
                for j in range( self.Space.dim ) :
                    F[j] = F[j] + \
                           self.Time.h * self.gamma[i] * self.M * s[j]
         
        return F
    
    def __rhs_T__(self, T, u ):
        '''
        The right hand side of the momentum equations.
         
        :param T: Temperature.
        :param u: Velocity.
        '''
        # RHS
        F = np.zeros( ( self.Space.dof ), float )
        s = np.zeros( ( self.Space.dof ), float )
        
        # Contribution from temporal derivative
        for i in range( self.levels - 1 ) :
            if abs( self.alpha[i]) > 0 :
                F[:] = F[:] - self.alpha[i] * self.M_T * T[i].glob()
                    
        # Contribution from the viscous term:
        for i in range( self.levels - 1 ) :
            if abs( self.beta[i] ) > 0 :
                s[:] = self.A_T * T[i].glob()
                F[:] = F[:] - self.Time.h * self.beta[i] * s[:]
        # oobs semi-implicit        
        #if not self.conv_term :
        #    for i in range( self.levels - 1 ) :
        #        if self.Space.dim ==1:
        #            self.conv_T.u_conv = [ u[i][0].basis_coeff ]
        #        if self.Space.dim ==2:
        #            self.conv_T.u_conv = [ u[i][0].basis_coeff, 
        #                                   u[i][1].basis_coeff ]
        #        if self.Space.dim ==3:
        #            self.conv_T.u_conv = [ u[i][0].basis_coeff,
        #                                   u[i][1].basis_coeff, 
        #                                   u[i][2].basis_coeff ]
        #        if abs( self.beta[i] ) > 0.0 :
        #            s[:] = self.conv_T.matrix * T[i].glob()
        #            F[:] = F[:] - self.Time.h * self.beta[i] * s
        
        # Contribution from the linear form stemming from the Laplacian
        #for i in range( self.levels ) :
        #    if abs( self.beta[i] ) > 0 :
        #        local_time = self.Time.time - \
        #                     ( float( self.levels ) - 1.0 - \
        #                     float(i) ) * self.Time.h
        #        s1 = self.neumann_cond( local_time )
        #        for j in range( self.Space.dim ):
        #            self.lap.g_neu = s1[j]
        #            s = self.lap.assemble_linear_form()
        #            #print 'j=',j,'s=',s 
        #            F[j] = F[j] + self.Time.h * self.beta[i] * s
                    
        # Convection term
        if self.conv_term :
            for i in range( self.levels - 1 ) :
                if self.Space.dim ==1:
                    self.conv_T.u_conv = [ u[i][0].basis_coeff ]
                if self.Space.dim ==2:
                    self.conv_T.u_conv = [ u[i][0].basis_coeff, 
                                           u[i][1].basis_coeff ]
                if self.Space.dim ==3:
                    self.conv_T.u_conv = [ u[i][0].basis_coeff,
                                           u[i][1].basis_coeff, 
                                           u[i][2].basis_coeff ]
                if abs( self.gamma[i] ) > 0.0 :
                    s[:] = self.conv_T.matrix * T[i].glob()
                    F[:] = F[:] - self.Time.h * self.gamma[i] * s
        
        # Forcing term
        #for i in range( self.levels ):
        #    if abs(self.gamma[i]) > 0 :
        #        local_time = self.Time.time - \
        #                     ( float( self.levels ) - 1.0 - \
        #                     float(i) ) * self.Time.h
        #        #s = self.force_function_T( u[i], p[i], T[i], local_time )
        #        F[:] = F[:] + self.Time.h * self.gamma[i] * self.M * s[:]
         
        return F
        
    def __action_poisson__(self,q_in):
        # Action of the pressure Poisson operator.
        
        # 1: Gradient
        s = np.zeros( (self.Space.dim, self.Space.dof), float)
        for i in range( self.Space.dim ) :
            s[i] = self.G[i] * q_in
                        
        # 2: Inverse of mass matrix
        v = np.zeros( (self.Space.dim, self.Space.dof), float)
        for i in range( self.Space.dim ) :
            v[i] = self.M_inv * s[i]
        
        # 3: Divergence
        q_out = np.zeros( ( self.SpaceGL.dof ), float )
        for i in range( self.Space.dim ) :
            q_out = q_out + self.D[i] * v[i]
                
        return q_out
    
    #def __action_uzawa__(self,q_in):
    #    # Action of the pressure Poisson operator.
    #    
    #    # 1: Gradient 
    #    s = np.zeros( (self.Space.dim, self.Space.dof), float)
    #    for i in range( self.Space.dim ) :
    #        s[i] = self.G[i] * q_in
    #                    
    #    # 2: Inverse of Helmholtz
    #    v = np.zeros( (self.Space.dim, self.Space.dof), float)
    #    t = np.zeros( (self.Space.dim, self.Space.dof), float)
    #    for i in range( self.Space.dim ) :
    #        v[i], flag = self.helmholtz_solver.solve( self.H, s[i], t[i] )
    #    
    #    # 3: Divergence
    #    q_out = np.zeros( ( self.SpaceGL.dof ), float )
    #    for i in range( self.Space.dim ) :
    #        q_out = q_out + self.D[i] * v[i]
    #            
    #    return q_out
        


class Guermond3D:
    '''
    Test case. 
    '''
    def __init__( self, Space, SpaceGL, mu ):
        #
        self.Space = Space
        self.SpaceGL = SpaceGL
        self.bound_func_u = sempy.BoundaryFunction( self.Space ) 
        self.bound_func_v = sempy.BoundaryFunction( self.Space )
        self.bound_func_w = sempy.BoundaryFunction( self.Space )  
        self.mu = mu
        self.f = sempy.VectorFunction( self.Space )
        
        self.err_p = sempy.Function( self.SpaceGL )            
        
                
    def error_norms( self, u, p, t ):
        # Error norms.
        u_ex = sempy.VectorFunction( self.Space )
        p_ex = sempy.Function( self.SpaceGL )
        
        self.initial_condition( u_ex, p_ex, t )
        
        err_u = sempy.VectorFunction( self.Space )
        #err_p = sempy.Function( self.SpaceGL )
        
        err_u[0].basis_coeff = u_ex[0].basis_coeff - u[0].basis_coeff
        err_u[1].basis_coeff = u_ex[1].basis_coeff - u[1].basis_coeff
        err_u[2].basis_coeff = u_ex[2].basis_coeff - u[2].basis_coeff
        
        self.err_p.basis_coeff = p_ex.basis_coeff - p.basis_coeff
        
        print 'u l2= ',err_u[0].l2_norm()
        print 'v l2= ',err_u[1].l2_norm()
        print 'w l2= ',err_u[2].l2_norm()
        print 'p l2= ',self.err_p.l2_norm()
        print 'p h1= ',self.err_p.h1_norm()
        
        u_infty = abs(err_u[0].basis_coeff).max()
        v_infty = abs(err_u[1].basis_coeff).max()
        w_infty = abs(err_u[2].basis_coeff).max()
        p_infty = abs(self.err_p.basis_coeff).max()
        #print 'u inf= ',u_infty
        #print 'v inf= ',v_infty
        #print 'w inf= ',w_infty
        #print 'p inf= ',p_infty
        #self.err_p.plot_wire()
        #print 'theoretical rate 3/2=',1.0/(0.5**1.5)
        #print 'theoretical rate 2=',1.0/(0.5**2.0)
        #print 'theoretical rate 5/2=',1.0/(0.5**2.5)
        #print 'theoretical rate 3=',1.0/(0.5**3.0)
        
        return err_u[0].l2_norm(), err_u[1].l2_norm(),err_u[2].l2_norm(),\
               self.err_p.l2_norm(),\
               u_infty, v_infty, w_infty, p_infty, self.err_p.h1_norm()
        
    def initial_condition( self, u, p, t ):
        # Velocity
        x = self.Space.x
        y = self.Space.y
        z = self.Space.z
        
        ic1 = np.sin( x )*np.sin( y + z + t )
        ic2 = np.cos( x )*np.cos( y + z + t )
        ic3 = np.cos( x )*np.sin( y + t )
        u[0].basis_coeff = np.copy( ic1 )
        u[1].basis_coeff = np.copy( ic2 )
        u[2].basis_coeff = np.copy( ic3 )
        
        # Pressure
        x_gl = self.SpaceGL.x
        y_gl = self.SpaceGL.y
        z_gl = self.SpaceGL.z
        
        ic = np.cos( x_gl ) * np.sin( y_gl + z_gl + t )
        p.basis_coeff = np.copy( ic )
        
        if self.SpaceGL.zero == 'yes':
            p_int = p.quadrature()
            ones = sempy.Function( self.SpaceGL, basis_coeff = 1.0 )
            omega_int = self.SpaceGL.quadrature( ones.basis_coeff )
            p.set_value( p.basis_coeff - p_int/omega_int )
            #print '!!!control init 0=',p.quadrature()
            #p.plot_wire()
        return 
    
    def boundary_condition( self, u, t ):
        x = self.Space.x
        y = self.Space.y
        z = self.Space.z
        
        u_bc = np.sin( x ) * np.sin( y + z + t )
        v_bc = np.cos( x ) * np.cos( y + z + t )
        w_bc = np.cos( x ) * np.sin( y + t )
        for i in range( 1, 5 ):#1,3
            u[0].set_bc( u_bc, i ) 
            u[1].set_bc( v_bc, i )
            u[2].set_bc( w_bc, i )  
        return 
    
    def weak_bc( self, t ):
        #x = self.Space.x
        #y = self.Space.y
        #dudx =   np.cos( x + t ) * np.sin( y + t )
        #dvdx = - np.sin( x + t ) * np.cos( y + t )
        #p = np.sin( x - y + t )
        #value = - ( dudx - p )
        #self.bound_func_u.set_value(value, 4)
        #value = - ( dvdx )
        #self.bound_func_v.set_value(value, 4)
        return [ self.bound_func_u, self.bound_func_v, self.bound_func_w ]
    
    def forcing_term( self, u, p, t ):
        x = self.Space.x
        y = self.Space.y
        z = self.Space.z
        mu = self.mu.basis_coeff
        
        # u mom
        s =  np.sin( x ) * np.cos( y + z + t )   + \
             (3.0*mu - 1.0) * np.sin( x ) * np.sin( y + z + t )
        self.f[0].basis_coeff = np.copy( s )
        
        # v mom
        s = -np.cos(x) * np.sin(y+z+t)+\
            ( 3.0 * mu + 1.0 ) * np.cos( x ) * np.cos( y + z + t )
        self.f[1].basis_coeff = np.copy( s )
        
        # w mom
        s = np.cos( x ) * ( np.cos( y + t ) + \
                            np.cos( y + z + t ) + \
                            2.0*mu*np.sin( y + t ) )
        self.f[2].basis_coeff = np.copy( s )
        
        return [ self.f[0].glob(), self.f[1].glob(), self.f[2].glob()]

class KimAndMoinTest:
    '''
    Test case. 
    '''
    def __init__( self, Space, SpaceGL, mu, convection = False ):
        #
        self.Space = Space
        self.SpaceGL = SpaceGL
        self.convection = convection
        self.bound_func_u = sempy.BoundaryFunction( self.Space ) 
        self.bound_func_v = sempy.BoundaryFunction( self.Space ) 
        self.mu = mu
        self.f = sempy.VectorFunction( self.Space )
        
        
        self.err_p = sempy.Function( self.SpaceGL )
        self.err_u = sempy.VectorFunction( self.Space )
        
    def boundary_condition( self, u, T, t ):
        x = self.Space.x
        y = self.Space.y
        u_bc = -np.sin(np.pi*x)*np.cos(np.pi*y) * np.cos(np.pi*t)
        v_bc =  np.cos(np.pi*x)*np.sin(np.pi*y) * np.cos(np.pi*t)
        # set (1,4) for neumann, (1,5) for Dirichelt
        for i in range( 1, 5 ):
            u[0].set_bc( u_bc, i ) 
            u[1].set_bc( v_bc, i )
        #print 'obs: sjekk BC in kim and moin test. Har inkludert return' 
        #print 'value time=',t 
        return u,T
        
    def initial_condition( self, u, p, t ):
        # Velocity
        x = self.Space.x
        y = self.Space.y
        
        u[0].basis_coeff = -np.sin(np.pi*x)*np.cos(np.pi*y)*\
                            np.cos(np.pi*t)
        u[1].basis_coeff =  np.cos(np.pi*x)*np.sin(np.pi*y)*\
                            np.cos(np.pi*t)
        # Pressure
        x_gl = self.SpaceGL.x
        y_gl = self.SpaceGL.y
        
        p.basis_coeff = -0.5*(np.sin(np.pi*x_gl) + \
                              np.sin(np.pi*y_gl))*np.cos(np.pi*t)
        
        if self.SpaceGL.zero == 'yes':
            p_int = p.quadrature()
            ones = sempy.Function( self.SpaceGL, basis_coeff = 1.0 )
            omega_int = self.SpaceGL.quadrature(ones.basis_coeff)
            p.set_value( p.basis_coeff - p_int/omega_int )
            
        return u,p
    
    def weak_bc( self, t ):
        x = self.Space.x
        y = self.Space.y
        dudx =  -np.pi*np.cos(np.pi*x)*np.cos(np.pi*y)*np.cos(np.pi*t)
        dvdx =  -np.pi*np.sin(np.pi*x)*np.sin(np.pi*y)*np.cos(np.pi*t)
        p = -0.5*(np.sin(np.pi*x) +  np.sin(np.pi*y))*np.cos(np.pi*t)
        value = - ( dudx - p )
        self.bound_func_u.set_value(value, 4)
        value = - ( dvdx )
        self.bound_func_v.set_value(value, 4)
        return [ self.bound_func_u, self.bound_func_v ]
    
    def forcing_term( self, u, p, T,t ):
        x = self.Space.x
        y = self.Space.y
        
                                   
        # u mom
        u_t = np.pi*np.sin(np.pi*x)*np.cos(np.pi*y)*np.sin(np.pi*t)
        u_xx=(np.pi*np.pi)*np.sin(np.pi*x)*np.cos(np.pi*y)*np.cos(np.pi*t)
        p_x = -0.5*np.pi*np.cos(np.pi*x)*np.cos(np.pi*t)
        if self.convection:
            u   = -np.sin(np.pi*x)*np.cos(np.pi*y)*np.cos(np.pi*t)
            v   =  np.cos(np.pi*x)*np.sin(np.pi*y)*np.cos(np.pi*t)
            u_x = -np.pi*np.cos(np.pi*x)*np.cos(np.pi*y)*np.cos(np.pi*t)
            u_y =  np.pi*np.sin(np.pi*x)*np.sin(np.pi*y)*np.cos(np.pi*t)
            conv = u*u_x + v*u_y
        else:
            conv = 0.0
        s = u_t - 2.0*self.mu.basis_coeff * u_xx + p_x + conv
        self.f[0].basis_coeff = np.copy( s )
        
        # v mom
        v_t = -np.pi*np.cos(np.pi*x)*np.sin(np.pi*y)*np.sin(np.pi*t)
        v_xx=-(np.pi*np.pi)*np.cos(np.pi*x)*np.sin(np.pi*y)*np.cos(np.pi*t)
        p_y= -0.5*np.pi*np.cos(np.pi*y)*np.cos(np.pi*t)
        if self.convection:
            u   = -np.sin(np.pi*x)*np.cos(np.pi*y)*np.cos(np.pi*t)
            v   =  np.cos(np.pi*x)*np.sin(np.pi*y)*np.cos(np.pi*t)
            v_x = -np.pi*np.sin(np.pi*x)*np.sin(np.pi*y)*np.cos(np.pi*t)
            v_y =  np.pi*np.cos(np.pi*x)*np.cos(np.pi*y)*np.cos(np.pi*t) 
            conv = u*v_x + v*v_y
        else:
            conv = 0.0
        s=v_t - 2.0*self.mu.basis_coeff * v_xx + p_y + conv
        self.f[1].basis_coeff = np.copy( s )
       
        s = np.zeros((self.Space.dof),float)
        return [ self.f[0].glob(), self.f[1].glob(), s]
    
    def error_norms( self, u, p, t ):
        # Error norms.
        u_ex = sempy.VectorFunction( self.Space )
        p_ex = sempy.Function( self.SpaceGL )
        
        self.initial_condition( u_ex, p_ex, t )
        
        self.err_u[0].basis_coeff = u_ex[0].basis_coeff - u[0].basis_coeff
        self.err_u[1].basis_coeff = u_ex[1].basis_coeff - u[1].basis_coeff
        self.err_p.basis_coeff = p_ex.basis_coeff - p.basis_coeff
        print 'u l2= ',self.err_u[0].l2_norm()
        print 'v l2= ',self.err_u[1].l2_norm()
        print 'p l2= ',self.err_p.l2_norm()
        u_h1 = self.err_u[0].h1_norm()#abs(self.err_u[0].basis_coeff).max()
        v_h1 = self.err_u[1].h1_norm()#abs(self.err_u[1].basis_coeff).max()
        p_h1 = self.err_p.h1_norm()
        print 'u h1= ',u_h1
        print 'v h1= ',v_h1
        print 'p h1= ',p_h1
                
        return self.err_u[0].l2_norm(), self.err_u[1].l2_norm(),\
               self.err_p.l2_norm(), u_h1, v_h1, p_h1
               
    def plot( self, levels = 7 ):
        '''
        Visualization of the function.
        
        :param levels: Number of levels in the contour plot (for 3D functions).
        :type levels: int
        '''
                
        if self.Space.dim == 2:
            
            font_size = 18
            fig = plt.figure(1)
            ax = axes3d.Axes3D(fig)

            for k in range(self.Space.noe):
                ax.plot_surface( self.SpaceGL.x[k,:,:], 
                                 self.SpaceGL.y[k,:,:], 
                                 self.err_p.basis_coeff[k,:,:],
                                 color='b',
                                 alpha=0.7,
                                 rstride=1, cstride=1)
            #ax.set_xlim3d(0,1)
            #ax.set_ylim3d(0,1)
            # for PC(1,chi)
            #ax.set_zlim3d(-0.12,0.01)
            
            ax.set_xlabel(r'$x$',fontsize=20)
            ax.set_ylabel(r'$y$',fontsize=20)
            #ax.set_zlabel(r'$e_p$',fontsize=20)
            #ax.set_zticks3d((-0.02,0.0,0.01)) 
            
            for label in ax.w_xaxis.get_ticklabels():
                label.set_fontsize(font_size)
            for label in ax.w_yaxis.get_ticklabels():
                label.set_fontsize(font_size)
            for label in ax.w_zaxis.get_ticklabels():
                label.set_fontsize(font_size)
            
            plt.show()
        
class GuermondTestOne:
    '''
    Test case. 
    '''
    def __init__( self, Space, SpaceGL, mu ):
        #
        self.Space = Space
        self.SpaceGL = SpaceGL
        self.bound_func_u = sempy.BoundaryFunction( self.Space ) 
        self.bound_func_v = sempy.BoundaryFunction( self.Space ) 
        self.mu = mu
        self.f = sempy.VectorFunction( self.Space )
        
        self.err_p = sempy.Function( self.SpaceGL )
        self.err_u = sempy.VectorFunction( self.Space )
    
    def plot_gll(self):
        #
        u_gll = self.SpaceGL.interpolation_gll( self.err_p.basis_coeff )
        x_int = self.Space.interpolation( self.Space.x, 15)
        y_int = self.Space.interpolation( self.Space.y, 15)
        u_int = self.Space.interpolation( u_gll, 15)
        
        fig = plt.figure(2)
        ax = axes3d.Axes3D(fig)

        min = u_int.min()
        max = u_int.max()
        du=(max-min)/float(10)
        levels = np.arange(min, max, du)
        
        for k in range( self.Space.noe ):
            #ax.plot_wireframe( x_int[k,:,:], y_int[k,:,:], u_int[k,:,:])
            #ax.contour( x_int[k,:,:], y_int[k,:,:], u_int[k,:,:],levels)
            ax.plot_surface( x_int[k,:,:], y_int[k,:,:], u_int[k,:,:],
                             color='b',
                             alpha=0.7,
                             rstride=1, cstride=1)
        ax.set_xlim3d(0,1)
        ax.set_ylim3d(0,1)
        ax.set_zlim3d(-0.03,0.01)    
        plt.show()    
        
    def plot( self, levels = 7 ):
        '''
        Visualization of the function.
        
        :param levels: Number of levels in the contour plot (for 3D functions).
        :type levels: int
        '''
                
        if self.Space.dim == 2:
            
            font_size = 18
            fig = plt.figure(1)
            ax = axes3d.Axes3D(fig)

            for k in range(self.Space.noe):
                ax.plot_surface( self.SpaceGL.x[k,:,:], 
                                 self.SpaceGL.y[k,:,:], 
                                 self.err_p.basis_coeff[k,:,:],
                                 color='b',
                                 alpha=0.7,
                                 rstride=1, cstride=1)
            ax.set_xlim3d(0,1)
            ax.set_ylim3d(0,1)
            # for PC(1,chi)
            #ax.set_zlim3d(-0.02,0.005)
            # for PC(2,chi)
            #ax.set_zlim3d(-0.005,0.012)
            #ax.set_zlim3d(-0.04,0.015)
            #ax.w_zaxis.set_major_locator(ticker.FixedLocator(
            #                                    (-0.03,-0.02,-0.01,0.0,0.01)))
            #ax.set_fontsize(20)
            # pc22 -pc32 comparison
            #ax.set_zlim3d(-0.0011,0.0011)
            #ax.set_zlim3d(-0.0002,0.0002)
            #ax.w_zaxis.set_major_locator(ticker.FixedLocator(
            #                                    (-0.03,-0.02,-0.01,0.0,0.01)))
            
            ax.set_xlabel(r'$x$',fontsize=20)
            ax.set_ylabel(r'$y$',fontsize=20)
            #ax.set_zlabel(r'$e_p$',fontsize=20)
            #ax.set_zticks3d((-0.02,0.0,0.01)) 
            
            for label in ax.w_xaxis.get_ticklabels():
                label.set_fontsize(font_size)
            for label in ax.w_yaxis.get_ticklabels():
                label.set_fontsize(font_size)
            for label in ax.w_zaxis.get_ticklabels():
                label.set_fontsize(font_size)

            
            #ax.set_zlim3d(-0.0007,0.0009)
            #plt.axes([-0.02,-0.01,0.0,0.01])
            #plt.grid(True)
            
            #fig = plt.figure(2)
            #ax2 = axes3d.Axes3D(fig)
            #for k in range(self.Space.noe):
            #    ax2.plot_surface( self.Space.x[k,:,:], 
            #                     self.Space.y[k,:,:], 
            #                     self.err_u[0].basis_coeff[k,:,:],
            #                     color='b',
            #                     alpha=0.7,
            #                     rstride=1, cstride=1)
            #ax2.set_xlim3d(0,1)
            #ax2.set_ylim3d(0,1)
            #plt.title('U velocity')
            
            #fig = plt.figure(3)
            #ax2 = axes3d.Axes3D(fig)
            #for k in range(self.Space.noe):
            #    ax2.plot_surface( self.Space.x[k,:,:], 
            #                     self.Space.y[k,:,:], 
            #                     self.err_u[1].basis_coeff[k,:,:],
            #                     color='b',
            #                     alpha=0.7,
            #                     rstride=1, cstride=1)
            #ax2.set_xlim3d(0,1)
            #ax2.set_ylim3d(0,1)
            #plt.title('V velocity')
            
            plt.show()
            
        
                
    def error_norms( self, u, p, t ):
        # Error norms.
        u_ex = sempy.VectorFunction( self.Space )
        p_ex = sempy.Function( self.SpaceGL )
        
        self.initial_condition( u_ex, p_ex, t )
        
        #self.err_u = sempy.VectorFunction( self.Space )
        #err_p = sempy.Function( self.SpaceGL )
        
        self.err_u[0].basis_coeff = u_ex[0].basis_coeff - u[0].basis_coeff
        self.err_u[1].basis_coeff = u_ex[1].basis_coeff - u[1].basis_coeff
        self.err_p.basis_coeff = p_ex.basis_coeff - p.basis_coeff
        print 'u e= ',self.err_u[0].l2_norm()
        print 'v e= ',self.err_u[1].l2_norm()
        print 'p e= ',self.err_p.l2_norm()
        u_infty = self.err_u[0].h1_norm()#abs(self.err_u[0].basis_coeff).max()
        v_infty = self.err_u[1].h1_norm()#abs(self.err_u[1].basis_coeff).max()
        p_infty = abs(self.err_p.basis_coeff).max()
        print 'u inf= ',u_infty
        print 'v inf= ',v_infty
        print 'p inf= ',p_infty
        print 'p H1= ',self.err_p.h1_norm()
        #self.err_p.plot_wire()
        print 'theoretical rate 3/2=',1.0/(0.5**1.5)
        print 'theoretical rate 2=',1.0/(0.5**2.0)
        print 'theoretical rate 5/2=',1.0/(0.5**2.5)
        print 'theoretical rate 3=',1.0/(0.5**3.0)
        
        return self.err_u[0].l2_norm(), self.err_u[1].l2_norm(),\
               self.err_p.l2_norm(),\
               u_infty, v_infty, p_infty,self.err_p.h1_norm()
        
    def initial_condition( self, u, p, t ):
        # Velocity
        x = self.Space.x
        y = self.Space.y
        ic1 = np.sin( x + t )*np.sin( y + t )
        ic2 = np.cos( x + t )*np.cos( y + t )
        u[0].basis_coeff = np.copy( ic1 )
        u[1].basis_coeff = np.copy( ic2 )
        # Pressure
        x_gl = self.SpaceGL.x
        y_gl = self.SpaceGL.y
        ic = np.sin( x_gl - y_gl + t )
        p.basis_coeff = np.copy( ic )
        
        if self.SpaceGL.zero == 'yes':
            p_int = p.quadrature()
            ones = sempy.Function( self.SpaceGL, basis_coeff = 1.0 )
            omega_int = self.SpaceGL.quadrature(ones.basis_coeff)
            p.set_value( p.basis_coeff - p_int/omega_int )
            #print 'control init 0=',p.quadrature()
            #p.plot_wire()
        return u, p 
    
    def boundary_condition( self, u, T, t ):
        x = self.Space.x
        y = self.Space.y
        u_bc = np.sin( x + t )*np.sin( y + t )
        v_bc = np.cos( x + t )*np.cos( y + t )
        # set (1,4) for neumann, (1,5) for Dirichelt
        for i in range( 1, 5 ):
            u[0].set_bc( u_bc, i ) 
            u[1].set_bc( v_bc, i ) 
        return u,T
    
    def weak_bc( self, t ):
        x = self.Space.x
        y = self.Space.y
        dudx =   self.mu.basis_coeff * np.cos( x + t ) * np.sin( y + t )
        dvdx = - self.mu.basis_coeff * np.sin( x + t ) * np.cos( y + t )
        p = np.sin( x - y + t )
        value = - ( dudx - p )
        self.bound_func_u.set_value(value, 4)
        value = - ( dvdx )
        self.bound_func_v.set_value(value, 4)
        return [ self.bound_func_u, self.bound_func_v ]
    
    def forcing_term( self, u, p, T, t ):
        x = self.Space.x
        y = self.Space.y
        # u mom
        s = ( np.cos( x + t )*np.sin( y + t )   + \
              np.sin( x + t )*np.cos( y + t ) ) + \
              np.cos( x - y + t ) +\
              2.0*self.mu.basis_coeff*np.sin( x + t )*np.sin( y + t )
        self.f[0].basis_coeff = np.copy( s )
        # v mom
        s = - ( np.sin( x + t )*np.cos( y + t ) +   \
                np.cos( x + t )*np.sin( y + t ) ) - \
                np.cos( x - y + t ) + \
                2.0*self.mu.basis_coeff*np.cos( x + t )*np.cos( y + t )
        self.f[1].basis_coeff = np.copy( s )
        return [ self.f[0].glob(), self.f[1].glob()]
        
    
class UzawaSolver( ProjectionMethod ):
    '''
    Implementation of the Uzawa algorithm for the solution of the 
    Navier-Stokes equations consisting of the momentum equations
    
    .. math::
    
       \\frac{\\partial \\mathbf u}{\\partial t}+
       \\mathbf u\\cdot\\nabla\\mathbf u =
       -\\nabla p +\\nu\\nabla\\mathbf u + \\mathbf f
       
    and the continuity equation
    
    .. math::
    
       \\nabla\\cdot\\mathbf u=0
    
    Here, multistep methods are used for the time-stepping:
    
    .. math::
       :nowrap:
    
       \\begin{align}
       \\frac{\\alpha_0 \mathbf {u}^{n+1}+
       \\sum_{i=1}^s \\alpha_i \mathbf u^{n+1-i}}{h}&=
       \\sum_{i=0}^s\\beta_i(-\\nabla p^{n+1-i}+
       \\mu\\nabla^2\mathbf {u}^{n+1-i}) +
       \\sum_{i=0}^s\\gamma_i \mathbf f^{n+1-i}\\nonumber \\\\
       \\nabla\cdot\mathbf {u}^{n+1} &= 0\\nonumber
       \\end{align}
    
    In matrix form:
    
    .. math:: 
       :nowrap:
        
        \\begin{equation}
        \\begin{bmatrix}
        \underline{H} & \\beta_0 h\underline{G}\\\\
        \underline{D} & 0
        \\end{bmatrix}
        \\begin{bmatrix}
        \underline{u}^{n+1}\\\\
        \underline{p}^{n+1}
        \\end{bmatrix}
        =
        \\begin{bmatrix}
        \underline{b}^{n+1}\\\\
        0
        \\end{bmatrix}
        \\nonumber
        \\end{equation}
    
    Where:
    
    .. math::
       :nowrap:
    
       \\begin{align}
       H&=\\alpha_0M+\\beta_0 hA \\nonumber \\\\
       b^{n+1}&=M\\sum_{i=1}^s \\alpha_i \mathbf u^{n+1-i}
               +
               h\\sum_{i=1}^s\\beta_i(-Gp^{n+1-i}+
               A\mathbf {u}^{n+1-i}) +
               h\\sum_{i=1}^s\\gamma_i \mathbf f^{n+1-i}\\nonumber
       \\end{align}
    
    Algorithm:
    
      1. Solve the Uzawa problem
      
         .. math::
         
            DH^{-1}Gp^{n+1}=\\frac{1}{\\beta_0 h}DH^{-1}b^{n+1}
            
      2. Solve the momentum equations
      
         .. math::
         
            H u^{n+1}=b^{n+1} - \\beta_0 hGp^{n+1}
    
    :param Space: Discrete space.
    :type Space: :class:`sempy.Space`
    :param SpaceGL: Discrete space.
    :type SpaceGL: :class:`sempy.fluid.SpaceGL`
    :param Time: Temporal space.
    :type Time: :class:`sempy.ode.Time`
    :param u: Velocity
    :type u: :class:`sempy.VectorFunction`
    :param p: Pressure
    :type p: :class:`sempy.Function`   
    
    :kwargs: * **mu** (:class:`sempy.Function`) - Viscosity. The default is 
               None. Then, :literal:`mu` is set to 1. 
             * **method** (*string*) - The available methods are:
                   * :literal:`euler` 
                   * :literal:`cnab2ex2`
                   * :literal:`mcnab2ex2`
                   * :literal:`bdf2ex1` 
                   * :literal:`bdf2ex2`
                   * :literal:`bdf3ex2`
                   * :literal:`bdf3ex3`
                   * :literal:`bdf4ex4`  
             * **conv_term** (*boolean*) - Either :literal:`True` or 
               :literal:`False`. 
             * **bound_cond** (*function*) - A function controlling 
               strong BCs.
             * **neumann_cond** (*function*) - A function controlling 
               Neumann BCs. Default is :literal:`None`. 
             * **force_function** (*function*) - The forcing function 
               :math:`\\mathbf f` in the above equation. Default 
               is :literal:`None`. 
             * **init_steps** (*int*) - Number of steps to kick start 
               higher order methods. 
             * **hyper_filter** (boolean)- Hyperbolic filter. To apply it 
               set it to :literal:`True`.  
             * **deflation_solver** (*boolean*) - To use the deflation 
               solver, set *deflation_solver* to :literal:`True`, 
               otherwise to :literal:`False` (default).   
             * **tol** (*float*) - Iterative tolerance.
             * **file_increment** (*int*) - The distance between time-steps 
               to be printed to file.  
             * **call_back** (*function*) - A call-back function. The 
               function is called as :literal:`call_back(u,p,t,i)`, 
               where u is velocoity, p is pressure, t is time and 
               i is the time-step number.  
    '''
    def __init__( self, Space, SpaceGL, Time, u, p, 
                  mu = None, method = bdf1ex1, conv_term = False,
                  bound_cond = __bc__ , force_function = None,
                  init_steps = 1, neumann_cond = None,
                  deflation_solver = False,call_back=None,
                  hyper_filter = False, tol = 1e-09,file_increment =100):
        # 
        ProjectionMethod.__init__( self, Space, SpaceGL, Time, u, p,
                                   mu = mu, 
                                   method = method,
                                   conv_term = conv_term,
                                   bound_cond = bound_cond,
                                   force_function = force_function,
                                   init_steps = init_steps,
                                   neumann_cond = neumann_cond,
                                   call_back = call_back,
                                   deflation_solver = deflation_solver,
                                   hyper_filter = hyper_filter,
                                   tol = tol,
                                   file_increment = file_increment)
        
        # Uzawa operator
        self.uzawa_operator = spl.LinearOperator( 
                          ( self.SpaceGL.dof,self.SpaceGL.dof ),
                            matvec = self.__action_uzawa__,
                            dtype = 'float' )
        # Helmholtz solver
        #self.helmholtz_solver = sempy.linsolvers.Krylov(
        #                                        tol = 1e-14,
        #                                        solver_type = 'bicgstab',
        #                                        pre = self.H_pre 
        #                                        )
        # Deflation solver
        if self.deflation_solver == True:#'yes':
            self.deflation = sempy.fluid.Deflation( 
                                    self.Space, 
                                    self.SpaceGL, 
                                    self.uzawa_operator,
                                    operator_type= 'uzawa',
                                    time_step_size = self.Time.h,
                                    tol = self.tol,
                                    mu_gl = self.mu_gl ) 
        self.u_dummy = sempy.VectorFunction( self.Space )
        
    def __action_uzawa__(self, q_in):
        # Action of the pressure Poisson operator.
        #print 'Action of uzawa'
        # 1: Gradient 
        s = np.zeros( (self.Space.dim, self.Space.dof), float)
        for i in range( self.Space.dim ) :
            s[i] = self.G[i] * q_in
                        
        # 2: Inverse of Helmholtz
        v = np.zeros( (self.Space.dim, self.Space.dof), float)
        t = np.zeros( (self.Space.dim, self.Space.dof), float)
        for i in range( self.Space.dim ) :
            v[i], flag = self.helmholtz_solver.solve( self.H, s[i], t[i] )
            #print 'Action of uzawa i=',i,'flag=',flag
        
        # 3: Divergence
        q_out = np.zeros( ( self.SpaceGL.dof ), float )
        for i in range( self.Space.dim ) :
            q_out = q_out + self.D[i] * v[i]
                
        return q_out
        
    def solve(self):
        '''
        Solves the problem. 
        
        :returns: * **u** - Velocity
                  * **p** - Pressure
        '''
        
        # Solution functions:
        u = [ ]
        p = [ ]
        for i in range(self.levels):
            u.append( sempy.VectorFunction( self.Space ) )
            p.append( sempy.Function( self.SpaceGL ) )
            
        # Setting initial values:
        for i in range(self.levels):
            p[i].basis_coeff = np.copy( self.p.basis_coeff )
            for j in range(self.Space.dim) :
                u[i][j].basis_coeff = np.copy( self.u[j].basis_coeff )
                
        # Timesteps to file:
        #k_file = range( 100, self.Time.time_steps+100, 100 )
        k_file = range( self.file_increment, 
                        self.Time.time_steps+self.file_increment, 
                        self.file_increment )
        # Initial value to file:
        if not self.u.filename == 'none':
            self.u.to_file()
        if not self.p.filename == 'none':
            self.p.to_file()
        # -- Callback
        if not self.call_back == None:
            self.call_back(self.u,self.p,self.Time.time,0)    
        #-- Initialize
        factor = 0.0
        for i in range( 0, self.levels-2 ):
            print '--> Time step number x: ', i+1
            self.Time.increment()
            factor = factor + 1.0
            u_dum, p_dum = self.__initialize( 
                                        u[i], p[i],
                                        ( factor - 1.0 ) * self.Time.h,
                                        factor*self.Time.h )
            p[i+1].basis_coeff = np.copy( p_dum.basis_coeff )
            for j in range(self.Space.dim) :
                    u[i+1][j].basis_coeff = np.copy( u_dum[j].basis_coeff )
            del u_dum, p_dum
            # -- Callback
            if not self.call_back == None:
                for j in range(self.Space.dim):
                    self.u[j].basis_coeff = np.copy( u[i+1][j].basis_coeff )
                self.p.basis_coeff = np.copy(p[i+1].basis_coeff)
                self.call_back(self.u,self.p,self.Time.time,i+1)
            # To file
            if (i+1) in k_file:
                self.to_file(u,p)
        # Level 1
        #print 'obs! UzawaMethod: use only fourth order.'
        #self.Time.increment()
        #x_gl = self.SpaceGL.x
        #y_gl = self.SpaceGL.y

        #x = self.Space.x
        #y = self.Space.y
        
        # Test Guermond
        #ic = np.sin( x_gl - y_gl + self.Time.time )
        #p[1].basis_coeff = np.copy( ic )               
        #ic1 = np.sin( x + self.Time.time )*np.sin( y + self.Time.time )
        #ic2 = np.cos( x + self.Time.time )*np.cos( y + self.Time.time )
        #u[1][0].basis_coeff = np.copy( ic1 )
        #u[1][1].basis_coeff = np.copy( ic2 )
        # Test Kim and Moin
        #t=self.Time.time
        #ic = -0.5*(np.sin(np.pi*x_gl) + np.sin(np.pi*y_gl))*np.cos(np.pi*t)
        #p[1].basis_coeff = np.copy( ic ) 
        #ic1 = -np.sin(np.pi*x)*np.cos(np.pi*y)*np.cos(np.pi*t)
        #ic2 =  np.cos(np.pi*x)*np.sin(np.pi*y)*np.cos(np.pi*t)
        #u[1][0].basis_coeff = np.copy( ic1 )
        #u[1][1].basis_coeff = np.copy( ic2 )
        
        # Level 2
        #self.Time.increment()
        # Test Guermond
        #ic = np.sin( x_gl - y_gl + self.Time.time )
        #p[2].basis_coeff = np.copy( ic )      
        #ic1 = np.sin( x + self.Time.time )*np.sin( y + self.Time.time )
        #ic2 = np.cos( x + self.Time.time )*np.cos( y + self.Time.time )
        #u[2][0].basis_coeff = np.copy( ic1 )
        #u[2][1].basis_coeff = np.copy( ic2 )
        # Test Kim and Moin
        #t=self.Time.time
        #ic = -0.5*(np.sin(np.pi*x_gl) + np.sin(np.pi*y_gl))*np.cos(np.pi*t)
        #p[2].basis_coeff = np.copy( ic ) 
        #ic1 = -np.sin(np.pi*x)*np.cos(np.pi*y)*np.cos(np.pi*t)
        #ic2 =  np.cos(np.pi*x)*np.sin(np.pi*y)*np.cos(np.pi*t)
        #u[2][0].basis_coeff = np.copy( ic1 )
        #u[2][1].basis_coeff = np.copy( ic2 )
        
        # Level 3
        #self.Time.increment()
        
        # Test Guermond
        #ic = np.sin( x_gl - y_gl + self.Time.time )
        #p[3].basis_coeff = np.copy( ic )      
        #ic1 = np.sin( x + self.Time.time )*np.sin( y + self.Time.time )
        #ic2 = np.cos( x + self.Time.time )*np.cos( y + self.Time.time )
        #u[3][0].basis_coeff = np.copy( ic1 )
        #u[3][1].basis_coeff = np.copy( ic2 )
        # Test Kim and Moin
        #t=self.Time.time
        #ic = -0.5*(np.sin(np.pi*x_gl) + np.sin(np.pi*y_gl))*np.cos(np.pi*t)
        #p[3].basis_coeff = np.copy( ic ) 
        #ic1 = -np.sin(np.pi*x)*np.cos(np.pi*y)*np.cos(np.pi*t)
        #ic2 =  np.cos(np.pi*x)*np.sin(np.pi*y)*np.cos(np.pi*t)
        #u[3][0].basis_coeff = np.copy( ic1 )
        #u[3][1].basis_coeff = np.copy( ic2 )
        
        # Time stepping
        for k in range( self.levels-2, self.Time.time_steps ):
            print '--> Time step number: ', k+1
            
            # Time increment
            self.Time.increment()
            
            # BC
            self.bound_cond( u[self.levels-1], self.Time.time )
            
            # 1) The RHS
            b = self.__rhs__( u, p )
            
            # 2) The Uzawa RHS
            b_uzawa = self.__rhs_uzawa__( b )

            # 3) Solve the pressure Poisson equation
            p[self.levels-1] = self.__solve_uzawa( b_uzawa, p )
            
            # 4) Solve momentum equations
            u = self.__solve_momentum( u, p, b )
            
            # Implicit correction
            #u = self.implicit_correction(u,p)
            
            # Hyperbolic filter
            if self.hyper_filter:# == 'yes':
                for i in range(self.Space.dim):
                    u[self.levels-1][i].hyper_filter()
                self.bound_cond( u[self.levels-1], self.Time.time )
            # Update solution array
            for i in range( self.levels-1 ):
                p[i].basis_coeff = np.copy( p[i+1].basis_coeff )
                for j in range(self.Space.dim) :
                    u[i][j].basis_coeff = np.copy( u[i+1][j].basis_coeff )
            # -- Callback
            if not self.call_back == None:
                for i in range(self.Space.dim):
                    self.u[i].basis_coeff = \
                             np.copy( u[self.levels-1][i].basis_coeff )
                self.p.basis_coeff = \
                      np.copy(p[self.levels-1].basis_coeff)
                self.call_back(self.u,self.p,self.Time.time,k+1)
            # Print to file
            if (k+1) in k_file:
                self.to_file(u,p)
                #for i in range(self.Space.dim):
                #    self.u[i].basis_coeff = \
                #         np.copy( u[self.levels-1][i].basis_coeff )
                #self.p.basis_coeff = \
                #         np.copy(p[self.levels-1].basis_coeff)
                #if not self.u.filename == 'none':
                #    self.u.to_file()
                #if not self.p.filename == 'none':
                #    self.p.to_file()
        print 'end time=',self.Time.time
        # Return values
        for i in range(self.Space.dim):
            self.u[i].basis_coeff = np.copy( u[self.levels-1][i].basis_coeff )
        self.p.basis_coeff = np.copy(p[self.levels-1].basis_coeff)
        return self.u, self.p
    
    def __initialize( self, u_0, p_0, start, end ):
        #print 'initialize...'
        # Temporal domain
        t2 = sempy.ode.Time( self.Space, start_time = start,
                             end_time = end,
                             time_steps = self.init_steps )
        # Solution vectors 
        u_init = sempy.VectorFunction( self.Space )
        p_init = sempy.Function( self.SpaceGL )
    
        p_init.basis_coeff = np.copy( p_0.basis_coeff )
        for j in range(self.Space.dim) :
            u_init[j].basis_coeff = np.copy( u_0[j].basis_coeff )
        
        eul = UzawaSolver( self.Space, 
                           self.SpaceGL, 
                           t2, 
                           u_init, p_init,
                           mu = self.mu,
                           method = bdf1ex1, 
                           conv_term = self.conv_term,
                           bound_cond = self.bound_cond, 
                           force_function = self.force_function, 
                           neumann_cond = self.neumann_cond,
                           deflation_solver = False, 
                           hyper_filter = self.hyper_filter,
                           tol = self.tol,
                           file_increment =1000 )
        u_init, p_init = eul.solve()
        del eul
        return u_init, p_init
    
    def __solve_uzawa( self, b_uzawa, p ):
        '''
        Solve the Uzawa equation. 
        '''
        
        # Solution vector
        phi = np.zeros( ( self.SpaceGL.dof ), float )
        
        # Estimation of pressure at time level t^(n+1)
        for i in range(self.levels-1):
            phi = phi + self.eta[i]*p[i].glob()
            
        # Solve Uzawa equation
        t1 = time.clock()
        if self.deflation_solver == False:#'no':
            [phi, flag] = self.poisson_solver.solve( 
                                            self.uzawa_operator, 
                                            b_uzawa, 
                                            phi )
        else:
            [phi, flag] = self.deflation.solve( b_uzawa, phi )
        
        t2 = time.clock()
        print 'Uzawa cg it=',flag,'exe time=',t2-t1
        
        
        # Set the value to pressure function
        s = self.SpaceGL.mapping_q( phi )
        p[self.levels-1].basis_coeff = np.copy( s )
        
        # - Compatibility condition
        if self.SpaceGL.zero == 'yes':
            p_int = p[self.levels-1].quadrature()
            ones = sempy.Function( self.SpaceGL, basis_coeff = 1.0 )
            omega_int = self.SpaceGL.quadrature( ones.basis_coeff )
            p[self.levels-1].set_value( p[self.levels-1].basis_coeff - \
                                        p_int/omega_int )
            
        return p[self.levels-1]
    
    
    def __solve_momentum( self, u, p, b ):
        # Compute the RHS of the momentum equations:
        
        # Contribution from pressure gradient
        F = np.zeros( ( self.Space.dim, self.Space.dof ), float )
        for j in range( self.Space.dim ):
            #for i in range( self.levels ): 
            if abs( self.beta[self.levels-1] ) > 0:
                s = self.G[j] * p[self.levels-1].glob()
                F[j] = F[j] - self.Time.h * self.beta[self.levels-1] * s
                    
        for j in range( self.Space.dim ):
            F[j] = F[j] + b[j]
            
        # Solve the momentum equations:
        for i in range(self.Space.dim):
            s, flag = self.helmholtz_solver.solve( 
                                            self.H, 
                                            F[i], 
                                            u[self.levels-1][i].glob() )
            u[self.levels-1][i].basis_coeff = self.Space.mapping_q( s )
            print 'i=',i,'flag=',flag
        return u
        
    def __rhs_uzawa__(self,b ):
        # The right hand side.
        
        # Solve for the components
        self.bound_cond( self.u_dummy, self.Time.time )
        
        t = np.zeros( (self.Space.dim, self.Space.dof), float)
        for i in range(self.Space.dim):
            t[i], flag = self.helmholtz_solver.solve( 
                                        self.H, 
                                        b[i], 
                                        self.u_dummy[i].glob() )
        
        # Divergence:
        b_uzawa = np.zeros( ( self.SpaceGL.dof ), float )
        for i in range( self.Space.dim ):
            b_uzawa = b_uzawa + self.D[i] * t[i]
        
        coeff = 1.0 / ( self.Time.h * self.beta[self.levels - 1])
        b_uzawa = b_uzawa * coeff        
        
        # Compatibility
        if self.SpaceGL.zero == 'yes':
            alpha = b_uzawa.sum()
            b_uzawa = b_uzawa - alpha / np.float( self.SpaceGL.dof ) 
            
        return b_uzawa
    
    def __rhs__(self, u, p ):
        # RHS
        if self.Space.dim == 1:
            F1 = np.zeros( ( self.Space.dof ), float )
            F = [ F1 ]
            
        if self.Space.dim == 2:
            F1 = np.zeros( ( self.Space.dof ), float )
            F2 = np.zeros( ( self.Space.dof ), float )
            F = [ F1, F2 ]
        
        if self.Space.dim == 3:
            F1 = np.zeros( ( self.Space.dof ), float )
            F2 = np.zeros( ( self.Space.dof ), float )
            F3 = np.zeros( ( self.Space.dof ), float )
            F = [ F1, F2, F3 ]
                
        s = np.zeros( ( self.Space.dof ), float )
        
        # Contribution from temporal derivative
        for j in range( self.Space.dim ) : 
            for i in range( self.levels - 1 ) :   
                if abs( self.alpha[i]) > 0 :
                    F[j] = F[j] - self.alpha[i] * self.M * u[i][j].glob()
                    
        # Contribution from the viscous term:
        for j in range( self.Space.dim ) :
            for i in range( self.levels - 1 ) : 
                if abs( self.beta[i] ) > 0 :
                    s = self.A * u[i][j].glob()
                    F[j] = F[j] - self.Time.h * self.beta[i] * s
        
        # Contribution from the linear form stemming from the Laplacian
        for i in range( self.levels ) :
            if abs( self.beta[i] ) > 0 :
                local_time = self.Time.time - \
                             ( float( self.levels ) - 1.0 - \
                             float(i) ) * self.Time.h
                s1 = self.neumann_cond( local_time )
                for j in range( self.Space.dim ):
                    self.lap.g_neu = s1[j]
                    s = self.lap.assemble_linear_form()
                    F[j] = F[j] + self.Time.h * self.beta[i] * s
                    
        # Pressure gradient
        for j in range( self.Space.dim ):
            for i in range( self.levels -1 ):
                if abs( self.eta[i] ) > 0 :
                    s = self.G[j] * p[i].glob()
                    F[j] = F[j] - self.Time.h * self.beta[i] * s
                    
        # Convection term
        if self.conv_term :#== 'yes':    
            for j in range( self.Space.dim ) :
                for i in range( self.levels ) :
                    if self.Space.dim == 1:
                        self.conv.u_conv = [ u[i][0].basis_coeff ]
                    if self.Space.dim == 2:
                        self.conv.u_conv = [ u[i][0].basis_coeff, 
                                         u[i][1].basis_coeff ]
                    if self.Space.dim == 3:
                        self.conv.u_conv = [ u[i][0].basis_coeff, 
                                             u[i][1].basis_coeff,
                                             u[i][2].basis_coeff ]
                    if abs( self.gamma[i] ) > 0 :
                        s = self.conv.matrix * u[i][j].glob()
                        F[j] = F[j] - self.Time.h * self.gamma[i] * s
        
        # Forcing term
        for i in range( self.levels ):
            if abs(self.gamma[i]) > 0 :
                local_time = self.Time.time - \
                             ( float( self.levels ) - 1.0 - \
                             float(i) ) * self.Time.h
                s = self.force_function( u[i], p[i], local_time )
                for j in range( self.Space.dim ) :
                    F[j] = F[j] + \
                           self.Time.h * self.gamma[i] * self.M * s[j]
         
        return F
        
        