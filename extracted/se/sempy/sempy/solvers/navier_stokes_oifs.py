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

from projection import ProjectionMethod
from projection import bdf1ex1
from projection import bdf2ex2
from projection import bdf3ex3
from projection import cnab2ex2
from projection import __bc__

def erk4():
    '''
    Explicit RK method of order 4.
    '''
    ah,bh,ch =np.zeros((4,4),float),np.zeros((4),float),np.zeros((4),float)

    ah[1,0]=1.0/2.0
    ah[2,1]=1.0/2.0
    ah[3,2]=1.0

    ch[1],ch[2],ch[3]=ah[1,0],ah[2,1],ah[3,2]
    bh[0],bh[1],bh[2],bh[3]=1.0/6.0 ,1.0/3.0, 1.0/3.0, 1.0/6.0
    stages=4
    return ah,bh,ch,stages 

class PC_OIFS(ProjectionMethod):
    '''
    OIFS.
    '''
    def __init__( self, Space, SpaceGL, Time, u, p, T= None,  
                  mu = None , kappa = None, Ri = 0.0,
                  order = 1, conv_term = False,
                  bound_cond = __bc__ , force_function = None,
                  init_steps = 1, explicit_steps =1, 
                  neumann_cond = None, chi = 0.5,
                  deflation_solver = True, call_back = None,
                  hyper_filter = False,
                  isothermal = True, 
                  tol = 1e-09, file_increment =100):
        
        self.order = order
        if self.order == 1:
            method = bdf1ex1
        if self.order == 2:
            method = bdf2ex2
            #method = cnab2ex2
        
        ProjectionMethod.__init__( self, Space, SpaceGL, Time, u, p, 
                                   T= T,  
                  mu = mu , kappa = kappa, Ri = Ri,
                  method = method, conv_term = conv_term,
                  bound_cond = bound_cond, force_function = force_function,
                  init_steps = init_steps, 
                  neumann_cond = neumann_cond, chi = chi,
                  deflation_solver = deflation_solver, 
                  call_back = call_back,
                  hyper_filter = hyper_filter,
                  isothermal = isothermal, 
                  tol = tol, file_increment = file_increment)
        
        self.explicit_steps = explicit_steps
        self.u_star = sempy.VectorFunction( self.Space )
        
        # Explicit solver
        u_temp = [ ]
        for i in range(self.Space.dim):
            u_temp.append( sempy.Function( self.Space ) )
        self.erk_u = sempy.ode.PRK( u_temp, self.Time, 
                                    force_function = self.force_function_u,
                                    bound_cond = self.bound_cond_u,
                                    prk_method = 'erk4',silent=True)
        if not self.isothermal:
            T_temp = sempy.Function( self.T.Space )
            self.erk_T = sempy.ode.PRK( [T_temp], self.Time, 
                                     force_function = self.force_function_T,
                                     bound_cond = self.bound_cond_T,
                                     prk_method = 'erk4',silent=True)
        
    def bound_cond_u(self,u,t):
        T_temp = sempy.Function(self.Space,basis_coeff=0.0)
        u,T_temp = self.bound_cond(u, T_temp, t)
        return u
    
    def bound_cond_T(self,T,t):
        u_temp = sempy.VectorFunction(self.Space)
        u_temp,T[0] = self.bound_cond(u_temp, T[0], t)
        return T
    
    def force_function_u( self, u, t ):
        # Forcing term f
        T_temp = sempy.Function(self.Space,basis_coeff=0.0)
        p_temp = sempy.Function(self.SpaceGL,basis_coeff=0.0)
        s = self.force_function( u, p_temp, T_temp,t )
        
        F = np.zeros((self.Space.dim, self.Space.dof),float)
        for i in range(self.Space.dim):
            F[i][:]= self.M*s[i][:]
        
        # Convection term
        self.inter_extra_polate(t)
        # Convection operator
        if self.Space.dim ==1:
            self.conv.u_conv = [ self.u_star[0].basis_coeff ]
        if self.Space.dim ==2:
            self.conv.u_conv = [ self.u_star[0].basis_coeff,
                                 self.u_star[1].basis_coeff ]
        if self.Space.dim ==3:
            self.conv.u_conv = [ self.u_star[0].basis_coeff,
                                 self.u_star[1].basis_coeff, 
                                 self.u_star[2].basis_coeff ]
        
        q = np.zeros((self.Space.dof),float)    
        for j in range( self.Space.dim):
            q = self.conv.matrix * u[j].glob()
            F[j][:] = F[j][:] - q[:]
        return F
    
    def force_function_T( self, T, t ):
        # Forcing term f
        #T_temp = sempy.Function(self.Space,basis_coeff=0.0)
        #p_temp = sempy.Function(self.SpaceGL,basis_coeff=0.0)
        #s = self.force_function( u, p_temp, T_temp,t )
        
        F = np.zeros((self.T.Space.dof),float)
        #for i in range(self.Space.dim):
        #    F[i][:]= self.M*s[i][:]
        
        # Convection term
        self.inter_extra_polate(t)
        # Convection operator
        if self.Space.dim ==1:
            self.conv_T.u_conv = [ self.u_star[0].basis_coeff ]
        if self.Space.dim ==2:
            self.conv_T.u_conv = [ self.u_star[0].basis_coeff,
                                   self.u_star[1].basis_coeff ]
        if self.Space.dim ==3:
            self.conv_T.u_conv = [ self.u_star[0].basis_coeff,
                                   self.u_star[1].basis_coeff, 
                                   self.u_star[2].basis_coeff ]
        
        q = np.zeros((self.T.Space.dof),float)    
        #for j in range( self.Space.dim):
        q[:] = self.conv_T.matrix * T[0].glob()
        F[:] = - q[:]
        return [F]
    
    def __solve_momentum( self, u, u_tilde, p, T, T_tilde ):
        '''
        '''
        # Solve the energy equation:
        if not self.isothermal:
            # 1) Convection subproblems
            for j in range(self.levels-1):
                T_temp = self.solve_nonlinear_T( self.Time.time,j )
                T_tilde[j].basis_coeff = np.copy(T_temp[0].basis_coeff)
            #if self.Time.time > 0.2:
            #    print 'o T=',T_tilde[0].basis_coeff[1,3,4]
            #    print '1 T=',T_tilde[1].basis_coeff[1,3,4]
            #for i in range(self.Space.dim):
            #    u_tilde[j][i].basis_coeff = np.copy(u_temp[i].basis_coeff)
            # 2) Diffusion subproblems
            F = self.__rhs_T__( T, u, T_tilde )
            s, flag = self.helmholtz_solver_T.solve( self.H_T, F, 
                                            T[self.levels-1].glob() )
            T[self.levels-1].basis_coeff = self.T.Space.mapping_q( s )
            print 'T flag=',flag
            
        # Solve the momentum equations:
        # 1) Convection subproblems
        t1_ex=time.time()
        for j in range(self.levels-1):
            u_temp = self.solve_nonlinear( self.Time.time,j )
            for i in range(self.Space.dim):
                u_tilde[j][i].basis_coeff = np.copy(u_temp[i].basis_coeff)
        t2_ex=time.time()
        print 'Convection ex time=',t2_ex-t1_ex
        # 2) Diffusion subproblems
        F = self.__rhs__( u, u_tilde,p, T )
        for i in range(self.Space.dim):
            s, flag = self.helmholtz_solver.solve( 
                                            self.H, F[i], 
                                            u[self.levels-1][i].glob() )
            u[self.levels-1][i].basis_coeff = self.Space.mapping_q( s )
            print 'i=',i,'flag=',flag
        return u, T
    
    def inter_extra_polate(self,t):
        '''
        Interpolation/extrapolation of the velocity field.
        '''
        if self.order == 1:
            for i in range(self.Space.dim):
                self.u_star[i].basis_coeff = np.copy(
                            self.u_levels[self.levels-2][i].basis_coeff)
        if self.order == 2:
            for i in range(self.Space.dim):
                u_int = self.u_levels[self.levels-2][i].basis_coeff-\
                    (self.u_levels[self.levels-2][i].basis_coeff -\
                     self.u_levels[self.levels-3][i].basis_coeff)/(self.Time.h)*\
                    (self.Time.time-t-self.Time.h)
                    #(t-self.Time.time-self.Time.h)
                self.u_star[i].basis_coeff = np.copy(u_int)
                                       
    
    def solve_nonlinear(self,t_global,j):
        '''
        Solve the convection sub-problems.
        '''
        h=self.Time.h
        # Time domain
        Time_local = sempy.ode.Time(self.Time.Space,
                        start_time = t_global - np.float(self.levels-j-1)*h,
                        end_time = t_global,
                        time_steps = self.explicit_steps*(self.levels-j-1))
        self.erk_u.Time = Time_local
        # Initial condition
        for k in range(self.Space.dim):
            self.erk_u.y0[k].basis_coeff = np.copy(
                                        self.u_levels[j][k].basis_coeff)
        # Solve the problem
        y_temp = self.erk_u.solve()
        
        return y_temp
       
    def solve_nonlinear_T(self,t_global,j):
        '''
        Solve the convection sub-problems.
        '''
        h=self.Time.h
        # Time domain
        Time_local = sempy.ode.Time(self.Time.Space,
                        start_time = t_global - np.float(self.levels-j-1)*h,
                        end_time = t_global,
                        time_steps = self.explicit_steps*(self.levels-j-1))
        self.erk_T.Time = Time_local
        # Initial condition
        #for k in range(self.Space.dim):
        self.erk_T.y0[0].basis_coeff = np.copy(self.T_levels[j].basis_coeff)
        # Solve the problem
        y_temp = self.erk_T.solve()
        
        return y_temp        
    
    def __rhs__(self, u, u_tilde,p, T ):
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
                    #F[j] = F[j] - self.alpha[i] * self.M * u[i][j].glob()
                    F[j] = F[j] - self.alpha[i]*self.M*u_tilde[i][j].glob()
        
        # Contribution from the buoyancy term
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
        for j in range( self.Space.dim ) :
            for i in range( self.levels ) :
                if abs( self.eta[i] ) > 0 :
                    s = self.G[j] * p[i].glob()
                    F[j] = F[j] - self.Time.h * self.eta[i] * s
        
        
        # Forcing term
        #for i in range( self.levels ):
        #    if abs(self.gamma[i]) > 0 :
        #        local_time = self.Time.time - \
        #                     ( float( self.levels ) - 1.0 - \
        #                     float(i) ) * self.Time.h
        #        s = self.force_function( u[i], p[i], T[i],local_time )
        #        for j in range( self.Space.dim ) :
        #            F[j] = F[j] + \
        #                   self.Time.h * self.gamma[i] * self.M * s[j]
         
        return F
    
    def __rhs_T__(self, T, u, T_tilde ):
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
                #F[:] = F[:] - self.alpha[i] * self.M_T * T[i].glob()
                F[:] = F[:] - self.alpha[i] * self.M_T * T_tilde[i].glob()
                    
        # Contribution from the viscous term:
        for i in range( self.levels - 1 ) :
            if abs( self.beta[i] ) > 0 :
                s[:] = self.A_T * T[i].glob()
                F[:] = F[:] - self.Time.h * self.beta[i] * s[:]
        
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
        #if self.conv_term :
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
        #        if abs( self.gamma[i] ) > 0.0 :
        #            s[:] = self.conv_T.matrix * T[i].glob()
        #            F[:] = F[:] - self.Time.h * self.gamma[i] * s
         
        return F
        
    def solve(self):
        '''
        Solve the problem. 
        
        :returns: * **u** - Velocity
                  * **p** - Pressure
        '''
        delta = self.space_check()
        if delta > 1.0e-04:
            print 'Spaces for u and T are not compatible.'
            return self.u, self.p, self.T
        
        # Solution functions:
        self.u_levels = [ ]
        self.p_levels = [ ]
        self.T_levels = [ ]
        
        for i in range(self.levels):
            self.u_levels.append( sempy.VectorFunction( self.Space ) )
            self.p_levels.append( sempy.Function( self.SpaceGL ) )
            self.T_levels.append( sempy.Function( self.T.Space ) )
        
        # u tilde
        u_tilde = [ ]
        for i in range(self.levels-1):
            if self.Space.dim==1:
                u_tilde.append( sempy.Function( self.Space ) )
            if self.Space.dim==2:
                u_tilde.append( [sempy.Function( self.Space ),
                                sempy.Function( self.Space )] )
            if self.Space.dim==3:
                u_tilde.append( [sempy.Function( self.Space ),
                                 sempy.Function( self.Space ),
                                 sempy.Function( self.Space )] )
        T_tilde = [ ]
        for i in range(self.levels-1):
            T_tilde.append( sempy.Function( self.T.Space ) )
        # Setting initial values:
        for i in range(self.levels):
            self.p_levels[i].basis_coeff = np.copy( self.p.basis_coeff )
            for j in range(self.Space.dim) :
                self.u_levels[i][j].basis_coeff = np.copy( self.u[j].basis_coeff )
            self.T_levels[i].basis_coeff = np.copy( self.T.basis_coeff )
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
        # Callback
        if not self.call_back == None:
            self.call_back(self.u,self.p,self.T,self.Time.time,0)
        #-- Initialize
        factor = 0.0
        for i in range( 0, self.levels-2 ):
            print '--> Time step number x: ', i+1,'time=',self.Time.time
            self.Time.increment()
            factor = factor + 1.0
            u_dum, p_dum, T_dum = self.__initialize( 
                                        self.u_levels[i], 
                                        self.p_levels[i], 
                                        self.T_levels[i],
                                        ( factor - 1.0 ) * self.Time.h,
                                        factor*self.Time.h )
            self.p_levels[i+1].basis_coeff = np.copy( p_dum.basis_coeff )
            self.T_levels[i+1].basis_coeff = np.copy( T_dum.basis_coeff )
            for j in range(self.Space.dim) :
                self.u_levels[i+1][j].basis_coeff = np.copy( 
                                                u_dum[j].basis_coeff )
            del u_dum, p_dum, T_dum
            # -- Callback
            if not self.call_back == None:
                for j in range(self.Space.dim):
                    self.u[j].basis_coeff = np.copy( 
                                        self.u_levels[i+1][j].basis_coeff )
                self.p.basis_coeff = np.copy(self.p_levels[i+1].basis_coeff)
                self.T.basis_coeff = np.copy(self.T_levels[i+1].basis_coeff)
                self.call_back(self.u, self.p, self.T,self.Time.time, i+1)
            # To file
            if (i+1) in k_file:
                self.to_file(self.u_levels[i+1],self.p_levels[i+1],
                             self.T_levels[i+1])
        # Time stepping
        for k in range( self.levels-2, self.Time.time_steps ):
            self.Time.increment()
            print '--> Time step number: ', k+1,'time=',self.Time.time
            
            # Momentum equations:
            # BC
            self.u_levels[self.levels-1], self.T_levels[self.levels-1]=\
                self.bound_cond( self.u_levels[self.levels-1], 
                                 self.T_levels[self.levels-1], 
                                 self.Time.time )
            # Solve
            self.u_levels, self.T_levels = self.__solve_momentum( 
                            self.u_levels, u_tilde,
                            self.p_levels, self.T_levels, T_tilde )
            
            # Solve the pressure Poisson equation
            phi = self.solve_pressure( self.u_levels )
            
            # Update pressure and velocity
            self.p_levels, self.u_levels = self.update( 
                            self.p_levels, phi, self.u_levels )
            
            # Update solution array
            for i in range( self.levels-1 ):
                self.p_levels[i].basis_coeff = np.copy( 
                                    self.p_levels[i+1].basis_coeff )
                for j in range(self.Space.dim) :
                    self.u_levels[i][j].basis_coeff = np.copy( 
                                self.u_levels[i+1][j].basis_coeff )
                self.T_levels[i].basis_coeff = np.copy( 
                                self.T_levels[i+1].basis_coeff )
            # -- Callback
            if not self.call_back == None:
                for i in range(self.Space.dim):
                    self.u[i].basis_coeff = \
                             np.copy( self.u_levels[self.levels-1][i].basis_coeff )
                self.p.basis_coeff = \
                      np.copy(self.p_levels[self.levels-1].basis_coeff)
                self.T.basis_coeff = \
                      np.copy(self.T_levels[self.levels-1].basis_coeff)
                self.call_back(self.u,self.p,self.T,self.Time.time,k+1)
            # To file
            if (k+1) in k_file:
                print '-------->>>> to file'
                self.to_file(self.u_levels[self.levels-1],
                             self.p_levels[self.levels-1],
                             self.T_levels[self.levels-1])
                
        # Return values
        for i in range(self.Space.dim):
            self.u[i].basis_coeff = np.copy( 
                        self.u_levels[self.levels-1][i].basis_coeff )
        self.p.basis_coeff = np.copy(
                        self.p_levels[self.levels-1].basis_coeff)
        self.T.basis_coeff = np.copy(
                        self.T_levels[self.levels-1].basis_coeff)
        return self.u, self.p, self.T
    
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
        
        eul = PC_OIFS( self.Space, self.SpaceGL, t2, 
                       u_init, p_init, T=T_init,  
                       mu = self.mu , kappa = self.kappa, 
                       Ri = self.Ri, order = 1, conv_term = self.conv_term,
                       bound_cond = self.bound_cond,  
                       force_function = self.force_function,
                       explicit_steps =self.explicit_steps, 
                       neumann_cond = self.neumann_cond, chi = 1.0,
                       deflation_solver = self.deflation_solver, 
                       hyper_filter = self.hyper_filter,
                       isothermal = self.isothermal,
                       tol = self.tol, file_increment =10000)
         
        u_init, p_init, T_init = eul.solve()
        del eul
        return u_init, p_init, T_init
       
        
class ProjectionOIFS(ProjectionMethod):
    '''
    OIFS.
    '''
    def __init__( self, Space, SpaceGL, Time, u, p, T= None,  
                  mu = None , kappa = None, Ri = 0.0,
                  order = 1, conv_term = False,
                  bound_cond = __bc__ , force_function = None,
                  init_steps = 1, explicit_steps =1, 
                  neumann_cond = None, chi = 0.5,
                  deflation_solver = True, call_back = None,
                  hyper_filter = False,
                  isothermal = True, 
                  tol = 1e-09, file_increment =100):
        
        self.order = order
        if self.order == 1:
            method = bdf1ex1
        if self.order == 2:
            method = bdf2ex2
        
        ProjectionMethod.__init__( self, Space, SpaceGL, Time, u, p, 
                                   T= T,  
                  mu = mu , kappa = kappa, Ri = Ri,
                  method = method, conv_term = conv_term,
                  bound_cond = bound_cond, force_function = force_function,
                  init_steps = 1, neumann_cond = neumann_cond, chi = chi,
                  deflation_solver = deflation_solver, 
                  call_back = call_back,
                  hyper_filter = hyper_filter,
                  isothermal = isothermal, 
                  tol = tol, file_increment = file_increment)
        
        self.explicit_steps = explicit_steps
        self.u_star = sempy.VectorFunction( self.Space )
    
    def __solve_momentum( self, u, p, T ):
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
        # 1) Convection subproblems
        #self.solve_nonlinear(u[0],self.Time)
        #self.conv_sub(u)
        #self.__conv_sub()
        #self.__erk(u,p,T)
        #self.inter_extra_polate(u,self.Time.time)
        #self.u_star[0].plot_wire()
        #self.erk_timestepping(u,p,T)
        # 2) Diffusion subproblems
        F = self.__rhs__( u, p, T )
        for i in range(self.Space.dim):
            s, flag = self.helmholtz_solver.solve( 
                                            self.H, F[i], 
                                            u[self.levels-1][i].glob() )
            u[self.levels-1][i].basis_coeff = self.Space.mapping_q( s )
            print 'i=',i,'flag=',flag
        return u, T
    
    def inter_extra_polate(self,u,t):
        '''
        Interpolation/extrapolation of the velocity field.
        '''
        if self.order == 1:
            for i in range(self.Space.dim):
                self.u_star[i].basis_coeff = np.copy(
                                        u[self.levels-2][i].basis_coeff)
        if self.order == 2:
            for i in range(self.Space.dim):
                u_int = u[self.levels-2][i].basis_coeff+\
                       (u[self.levels-2][i].basis_coeff -\
                        u[self.levels-3][i].basis_coeff)/(self.Time.h)*\
                       (t-self.Time.time-self.Time.h)
                self.u_star[i].basis_coeff = np.copy(u_int)
                                       
    
    def non_linear_function(self,u_tilde,T_tilde,u,p,T,t):
        '''
        '''
        F  = np.zeros((self.Space.dim + 1,self.Space.dof),float)
        # Forcing term
        s = self.force_function( u, p, T, t )
        for j in range( self.Space.dim + 1):
            F[j][:]=self.M*s[j][:]
        # Interpolate/extrapolate velocity
        self.inter_extra_polate(u,t)
        # Convection operator
        if self.Space.dim ==1:
            self.conv.u_conv = [ self.u_star[0].basis_coeff ]
        if self.Space.dim ==2:
            self.conv.u_conv = [ self.u_star[0].basis_coeff,
                                 self.u_star[1].basis_coeff ]
        if self.Space.dim ==3:
            self.conv.u_conv = [ self.u_star[0].basis_coeff,
                                 self.u_star[1].basis_coeff, 
                                 self.u_star[2].basis_coeff ]
        #
        for j in range( self.Space.dim):
            s = self.conv.matrix * u_tilde[j].glob()
            F[j][:] = F[j][:] + s
            
        if not self.isothermal:
            if self.Space.dim ==1:
                self.conv_T.u_conv = [ self.u_star[0].basis_coeff ]
            if self.Space.dim ==2:
                self.conv_T.u_conv = [ self.u_star[0].basis_coeff, 
                                       self.u_star[1].basis_coeff ]
            if self.Space.dim ==3:
                self.conv_T.u_conv = [ self.u_star[0].basis_coeff,
                                       self.u_star[1].basis_coeff, 
                                       self.u_star[2].basis_coeff ]
            s = self.conv_T.matrix * T_tilde[j].glob()
            F[self.Space.dim][:] = F[self.Space.dim][:] + s[self.Space.dim]
            
        return F
    
    #def erk_solve(self):
        #-- Solution vector y: y[0]=y^{n+1}, y[1]=y^{n}, y[2]=y^{n-1}, 
        #u_tilde = np.zeros( (self.vector_size), float )
        #yend   = np.zeros( (self.vector_size), float )
        #ystart[:] = self.component_to_vector( self.y0 )
    
    def solve_nonlinear(self,u,Y):
        print 'hei'
        print 'self.levels=',self.levels
        # Solver
        Time_local = sempy.ode.Time(Y.Space,
                        start_time = 0.0,
                        end_time = Y.h,
                        time_steps = self.explicit_steps)
        if self.Space.dim==1:
            w=[u[0]]
        if self.Space.dim==2:
            w=[u[0],u[1]]
        if self.Space.dim==3:
            w=[u[0],u[1],u[2]]
        erk = sempy.ode.PRK( w,Time_local,
                             force_function = self.force_function, 
                             bound_cond = self.bound_cond,
                             prk_method='erk4')
        # Solve
        for j in range(self.levels-1):
            Time_local = sempy.ode.Time(Y.Space,
                start_time = Y.time - np.float(self.levels-j-1)*Y.h,
                end_time = Y.time,
                time_steps = self.explicit_steps*(self.levels-j-1))
        #    for k in range(self.Space.dim):
        #        erk.y0[k].basis_coeff = np.copy(y[j][k].basis_coeff)
                
        #    for k in range(self.number_of_eq):
        #        erk.y0[k].basis_coeff = np.copy(y[j][k].basis_coeff)
        #    #erk.y0 = y[j]
        #    erk.Time = Time_local
        #    y_temp = erk.solve()
        #    for k in range(self.number_of_eq):
        #        y_tilde[j][k].basis_coeff = np.copy(y_temp[k].basis_coeff)
        #    del y_temp 
            
    
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
        
        # Contribution from the buoyancy term
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
        
        # Forcing term
        for i in range( self.levels ):
            if abs(self.gamma[i]) > 0 :
                local_time = self.Time.time - \
                             ( float( self.levels ) - 1.0 - \
                             float(i) ) * self.Time.h
                s = self.force_function( u[i], p[i], T[i],local_time )
                for j in range( self.Space.dim ) :
                    F[j] = F[j] + \
                           self.Time.h * self.gamma[i] * self.M * s[j]
         
        return F
        
    def solve(self):
        '''
        Solve the problem. 
        
        :returns: * **u** - Velocity
                  * **p** - Pressure
        '''
        delta = self.space_check()
        if delta > 1.0e-04:
            print 'Spaces for u and T are not compatible.'
            return self.u, self.p, self.T
        print 'hei'
        
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
        
        # Time stepping
        for k in range( self.levels-2, self.Time.time_steps ):
            print '--> Time step number: ', k+1,'time=',self.Time.time
            self.Time.increment()
            
            # Solve the momentum equations:
            self.bound_cond( u[self.levels-1], T[self.levels-1], 
                             self.Time.time )
            u, T = self.__solve_momentum( u, p, T )
            
                               
            # Solve the pressure Poisson equation
            phi = self.solve_pressure( u )
            
            # Update pressure and velocity
            p, u = self.update( p, phi, u )
            
            # Hyperbolic filter
            #if self.hyper_filter:
            #    for i in range(self.Space.dim):
            #        u[self.levels-1][i].hyper_filter()
            #    if not self.isothermal:
            #        T[self.levels-1].hyper_filter()
            #    self.bound_cond( u[self.levels-1], T[self.levels-1],
            #                     self.Time.time )
            
                    
            # Update solution array
            for i in range( self.levels-1 ):
                p[i].basis_coeff = np.copy( p[i+1].basis_coeff )
                for j in range(self.Space.dim) :
                    u[i][j].basis_coeff = np.copy( u[i+1][j].basis_coeff )
                T[i].basis_coeff = np.copy( T[i+1].basis_coeff )
            # -- Callback
            #if not self.call_back == None:
            #    for i in range(self.Space.dim):
            #        self.u[i].basis_coeff = \
            #                 np.copy( u[self.levels-1][i].basis_coeff )
            #    self.p.basis_coeff = \
            #          np.copy(p[self.levels-1].basis_coeff)
            #    self.T.basis_coeff = \
            #          np.copy(T[self.levels-1].basis_coeff)
            #    self.call_back(self.u,self.p,self.T,self.Time.time,k+1)
            # Print to file
            #if (k+1) in k_file:
            #    self.to_file(u[self.levels-1], p[self.levels-1], 
            #                 T[self.levels-1])
                
        #print 'end time=',self.Time.time
        # Return values
        for i in range(self.Space.dim):
            self.u[i].basis_coeff = np.copy( u[self.levels-1][i].basis_coeff )
        self.p.basis_coeff = np.copy(p[self.levels-1].basis_coeff)
        self.T.basis_coeff = np.copy(T[self.levels-1].basis_coeff)
        return self.u, self.p, self.T
        