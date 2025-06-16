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
from prk import PRK
import numpy as np
import scipy as sp
import scipy.sparse.linalg as spl
import pickle



def euler():
     """
     Euler method 1st order.
     """
     alpha = np.zeros(2) #: time derivative
     beta  = np.zeros(2) #: implicit terms
     gamma = np.zeros(2) #: explicit terms
     alpha[1],alpha[0] = 1.0,-1.0 #: time derivative
     beta[1], beta[0] = 1.0, 0.0  #: implicit terms
     gamma[1],gamma[0] = 0.0, 1.0  #: explicit terms
     levels = 2 
     return alpha,beta,gamma,levels

def cnab2():
     """ Crank-Nicolson/Adams-Bashforth 2nd order. 
         return: alpha,beta, gamma,levels 
     """
     alpha,beta,gamma =np.zeros(3),np.zeros(3),np.zeros(3)
     alpha[2],alpha[1],alpha[0]=1.0,-1.0,0.0
     beta[2] ,beta[1], beta [0]=0.5,0.5,0.0
     gamma[2],gamma[1],gamma[0]=0.0,1.5,-0.5
     levels=3
     return alpha,beta,gamma,levels

def cn():
     """ Crank-Nicolson/Adams-Bashforth 2nd order. 
         return: alpha,beta, gamma,levels 
     """
     alpha,beta,gamma =np.zeros(2),np.zeros(2),np.zeros(2)
     alpha[1],alpha[0]=1.0,-1.0
     beta[1], beta [0]=0.5,0.5
     #gamma[2],gamma[1],gamma[0]=0.0,1.5,-0.5
     levels=2
     return alpha,beta,gamma,levels
 
def mcnab2():
     """Modified Crank-Nicolson/Adams-Bashforth 2nd order."""
     alpha,beta,gamma =np.zeros(3),np.zeros(3),np.zeros(3)
     alpha[2],alpha[1],alpha[0]=1.0,-1.0,0.0
     beta[2] ,beta[1], beta [0]=9.0/16.0,6.0/16.0,1.0/16
     gamma[2],gamma[1],gamma[0]=0.0,1.5,-0.5
     levels=3
     return alpha,beta,gamma,levels

def cnlf():
     """Crank-Nicolson/Leapfrog 2nd order"""
     alpha,beta,gamma =np.zeros(3),np.zeros(3),np.zeros(3)
     alpha[2],alpha[1],alpha[0]=1.0,0.0,-1.0
     beta[2] ,beta[1], beta [0]=1.0,0.0,1.0
     gamma[2],gamma[1],gamma[0]=0.0,2.0,0.0
     levels=3
     return alpha,beta,gamma,levels

def bdfex2():
     """Backward differentiation formula/extrapolation 2nd order"""
     alpha,beta,gamma =np.zeros(3),np.zeros(3),np.zeros(3)
     alpha[2],alpha[1],alpha[0]=1.5,-2.0,0.5
     beta[2] ,beta[1], beta [0]=1.0,0.0,0.0
     gamma[2],gamma[1],gamma[0]=0.0,2.0,-1.0
     levels=3
     return alpha,beta,gamma,levels

def bdfex3():
     """Backward differentiation formula/extrapolation 2nd order"""
     alpha, beta, gamma = np.zeros(4), np.zeros(4), np.zeros(4)
     alpha[3] =  11.0/6.0
     alpha[2] = -3.0
     alpha[1] =  3.0/2.0
     alpha[0] = -1.0/3.0
     beta[3], beta[2], beta[1], beta[0] =  1.0, 0.0, 0.0, 0.0
     gamma[3], gamma[2], gamma[1], gamma[0] = 0.0, 3.0, -3.0, 1.0
     levels = 4
     return alpha, beta, gamma, levels

def __emptyfunc__(y,t):
   """This is an empty func."""
   v = np.zeros( ( y.size ) )
   return v

def __pre__(y):
   """This is an empty preconditioner."""
   return y

def __bc__(y,t):
   """This is an empty boundary condition function. Leaves y untouched."""
   return y

class IMEX(PRK):
    '''
    This class is an implementation of implicit-explicit multistep schemes (IMEX)
    for the solution of:
    
    .. math::
    
       M\\frac{dy}{dt}=Ly+N(y,t)
    
    :param y: Initial condition
    :type y: A collection of :class:`sempy.Function`
    :param Time: An instance of the :class:`sempy.ode.Time` class.
    :kwargs: * **L** - Linear operator
             * **L_pre** - The FEM equivalent of L. Used to create 
               preconditioner. 
             * **force_function** - A function, possibly non-linear. 
               This is the function :math:`N(y,t)` in the equation above.
             * **bound_cond** - Strong BCs.
             * **imex_method** (*string*) - The IMEX method to be used. 
               The options are:
                    * First order forward/backward Euler: :literal:`euler`
                    * Crank-Nicolson/Adams-Bashforth: :literal:`cnab2`
                    * Modified Crank-Nicolson/Adams-Bashforth: 
                      :literal:`mcnab2`
                    * Second order BDF and second order extrapolatio: 
                      :literal:`bdfex2`
                    * Crank-Nicolson/leap-frog: :literal:`cnlf`
             * **init_steps** (*int*) - Number of time-steps used with a 
               first order method to kick-start the solution process. 
             * **linear_solver** - The linear solver. The default is 
               CG. If L is not SPD, then one can for example use bicgstab.
             * **iter_tol** (*float*)- Iterative tolerance.
    '''
    def __init__(self, y, Time, L = None, L_pre= None,
                  force_function = None, bound_cond = __bc__,
                  imex_method = 'euler', init_steps = 1,
                  file_increment = 1000,
                  hyper_filter = False,call_back=None,
                  linear_solver = None, iter_tol = 1e-10, maxiter = 1000):
        PRK.__init__( self, y, Time, L = L, L_pre= L_pre,
                      force_function = force_function, 
                      bound_cond = bound_cond,
                      file_increment = file_increment, 
                      hyper_filter = hyper_filter,call_back=call_back,
                      linear_solver = linear_solver, iter_tol = iter_tol,
                      maxiter=maxiter )
       
        self.init_steps = init_steps
        self.imex_method = imex_method

        if self.imex_method == 'euler':
            [self.alpha,self.beta,self.gamma,self.levels]=euler()
        if self.imex_method == 'bdfex2':
            [self.alpha,self.beta,self.gamma,self.levels]=bdfex2()
        if self.imex_method == 'bdfex3':
            [self.alpha,self.beta,self.gamma,self.levels]=bdfex3()
        if self.imex_method == 'mcnab2':
            [self.alpha,self.beta,self.gamma,self.levels]=mcnab2()
        if self.imex_method == 'cnab2':
            [self.alpha,self.beta,self.gamma,self.levels]=cnab2()
        if self.imex_method == 'cnlf':
            [self.alpha,self.beta,self.gamma,self.levels]=cnlf()
        if self.imex_method == 'cn':
            [self.alpha,self.beta,self.gamma,self.levels]=cn()
            
    def __rhs__(self,y):
        F = np.zeros((self.vector_size),float)
        s = np.zeros((self.vector_size),float)
        # Time derivative
        for i in range(0,self.alpha.size-1):   
            if abs(self.alpha[i])>0 :
                F = F - self.alpha[i] * (self.M * y[i])
        # Linear term
        for i in range(0,self.beta.size-1): 
            if abs(self.beta[i])>0 :
                s = self.L*y[i]
                F= F + self.Time.h*self.beta[i]*s
        # Explicit function
        for i in range(0,self.gamma.size):
            if abs(self.gamma[i])>0 :
                time = self.Time.time - \
                      (float(self.gamma.size)-1.0-float(i))*self.Time.h
                s = self.force_vec(y[i],time)
                F = F + self.Time.h*self.gamma[i]*s
         
        return F   
     
    def __initialize__(self,y_0,start,end):
        print 'initialize...'
        Time_local = sempy.ode.Time( self.Time.Space,start_time = start,
                             end_time = end,
                             time_steps = self.init_steps ) 
        euler= IMEX(y_0, Time_local, L = self.L_in, 
                    L_pre = self.L_pre,
                    force_function = self.force_function, 
                    bound_cond = self.bound_cond,
                    imex_method = 'euler', 
                    linear_solver = self.linear_solver, 
                    iter_tol = self.iter_tol,
                    maxiter = self.maxiter)
        y1 = euler.solve()
        del euler
        return y1
    
    def solve(self):
        '''
        Solves the ODE system
        '''
        #-- Solution vector y: y[0]=y^{n+1}, y[1]=y^{n}, y[2]=y^{n-1}, and so on
        y = np.zeros( (self.levels,self.vector_size), float )
        for i in range(self.levels):
            for j in range(self.number_of_eq):
                y[i] = self.component_to_vector( self.y0 )
        # Timesteps to file:
        k_file = range( self.file_increment, 
                        self.Time.time_steps+self.file_increment, 
                        self.file_increment )
        #--To file
        self.to_file(y[0])
        # -- Callback
        if not self.call_back == None:
            y_out = self.vector_to_component(y[0])  
            self.call_back(y_out ,self.Time.time,0)
        #-- Initialize
        factor=0.0
        for i in range(0,self.levels-2):
            self.Time.increment()
            factor = factor+1.0
            y_start = self.vector_to_component(y[i])
            y_temp = self.__initialize__( y_start,
                                          (factor-1.0)*self.Time.h,
                                          factor*self.Time.h )
            y[i+1] = self.component_to_vector( y_temp )
            # To file
            if (i+1) in k_file:
                self.to_file(y[i+1])
            # -- Callback
            if not self.call_back == None:
                y_out = self.vector_to_component(y[i+1])  
                self.call_back(y_out ,self.Time.time,i+1)
                
        #-- Time-stepping
        for i in range(self.levels-2,self.Time.time_steps):
            self.Time.increment()
            print '--> Time step number: ', i+1,'time=',self.Time.time
            # RHS
            b = self.__rhs__(y)
            # Boundary conditions
            y[self.levels-1]=self.apply_bc(y[self.levels-1],self.Time.time )
            # Helmholtz operator
            H = sempy.operators.MultipleOperators([self.M,self.L],
                      scaling_factor=[self.alpha[self.levels-1], 
                                    -self.Time.h*self.beta[self.levels-1]],
                      assemble='no').matrix
            # Solve linear system
            [y[self.levels-1],flag] = self.linear_solver.solve(
                                            H,b,y[self.levels-1])
            print 'iter=',flag
            # Update solution array
            for k in range(self.levels-1):
                y[k]=np.copy(y[k+1])
            # To file
            if (i+1) in k_file:
                self.to_file(y[self.levels-1])
            # -- Callback
            if not self.call_back == None:
                y_out = self.vector_to_component(y[self.levels-1])  
                self.call_back(y_out,self.Time.time,i+1)
        
        y_out = self.vector_to_component(y[self.levels-1])
        return y_out

class IMEX_old():
    """ 
    This is the imex multistep Solver class.
    ImpOp and ExpOp has to be square matrices or 
    LinearOperators as given by scipy.
    
       Usage
    
    :param A: Time instance.
    :param y0: Initial value. 
    :param Time: A L{blackbox.ode.basic.Time} object.
    :param ImpFunc: Function to be treated implicitly.
    :param ExpFunc: Function to be treated explicitly.
    :param ImpOp: Implicit operator.
    :param ExpOp: Explicit operator.
    :param BoundCond: Method/function with (possibly) time dependent boundary conditions.
    :param Mask:  Method/function depending on Dirichlet boundary conditions. 
    :param Method: The method can be L{imex.multistep.euler}, L{imex.multistep.cnab2}, L{imex.multistep.mcnab2}, 
           L{imex.multistep.cnlf}, L{imex.multistep.bdfex2} or a self defined one.
    :param InitSteps: For higher order methods one might need to start with small timesteps with the Euler method.
    :param LinearSolver: Sets the linear solver for system solves at each time-step. 
            Currently only: solvers.linear.cg.pcg.
    :param PreCond: Preconditioner passed to solvers.linear.cg.pcg. Has to approximately solve the linear system Hz=r.
    :param FileName: Sets the filename to store data. Every timestep solution is printed to file.
    """
    def __init__(self,y0,Time,
                 ImpFunc=__emptyfunc__,ExpFunc=__emptyfunc__,
                 ImpOp=[sp.array([0.0])],ExpOp=[sp.array([0.0])],
                 BoundCond=__bc__,Mask=__pre__,Method=euler,InitSteps=1,
                 LinearSolver=None, PreCond=__pre__,FileName=' '):
        
        self.Method       =Method 
        self.y0           =y0
        self.Time         =Time
        self.A            =ode.MultipleOperators(ImpOp,'implicit').MultiOperator# Implicit operator
        self.B            =ode.MultipleOperators(ExpOp,'explicit').MultiOperator# Explicit operator
        self.ImpFunc      =ImpFunc
        self.ExpFunc      =ExpFunc
        self.Mask         =Mask
        self.BoundCond    =BoundCond
        self.dof          =y0.size
        self.InitSteps    =InitSteps
        self.LinearSolver =LinearSolver
        self.PreCond      =PreCond
        self.FileName     =FileName
        [self.alpha,self.beta,self.gamma,self.levels]=Method()
        self.H            = ode.Helmholtz(self.A,self.Time.h,
                                      self.alpha[self.levels-1],
                                      self.beta[self.levels-1],
                                      self.dof,self.Mask).Matrix
    
    def __rhs__(self,y):
        F = np.zeros((self.dof))
        s = np.zeros((self.dof))
        for i in range(0,self.alpha.size-1):   # time derivative
            if abs(self.alpha[i])>0 :
                F = F - self.alpha[i] * y[i]
        if self.A:
            for i in range(0,self.beta.size-1): # implicit terms
                if abs(self.beta[i])>0 :
                    s = self.A*y[i]
                    F= F + self.Time.h*self.beta[i]*s
              
        for i in range(0,self.beta.size):      # implicit function
            if abs(self.beta[i])>0 :
                time = self.Time.time - \
                       (float(self.beta.size)-1.0-float(i))*self.Time.h
                s = self.ImpFunc(y[i],time)
                F = F + self.Time.h*self.beta[i]*s
         
        if self.B:
            for i in range(0,self.gamma.size):  # explicit terms
                if abs(self.gamma[i])>0 :
                    s = self.B*y[i]
                    F = F + self.Time.h*self.gamma[i]*s
            
        for i in range(0,self.gamma.size):     # explicit function
            if abs(self.gamma[i])>0 :
                time = self.Time.time - \
                      (float(self.gamma.size)-1.0-float(i))*self.Time.h
                s = self.ExpFunc(y[i],time)
                F = F + self.Time.h*self.gamma[i]*s
         
        #-- Mask boundaryconditions(F) upon exit
        return self.Mask(F)# compensate for Dirichlet conditions
     
    def __initialize__(self,y_0,start,end):
        print 'initialize...'
        t2 = ode.Time( start_time = start,
                       end_time = end,
                       time_steps = self.InitSteps ) 
        eul= Solver( y_0, t2, 
                     ImpFunc = self.ImpFunc,
                     ExpFunc = self.ExpFunc,
                     ImpOp = [self.A],ExpOp=[self.B],
                     BoundCond = self.BoundCond,
                     Mask = self.Mask,
                     Method = euler,
                     InitSteps = self.InitSteps,
                     LinearSolver = self.LinearSolver,
                     PreCond = self.PreCond )
        y1=eul.solve()
        print 'initialize stop. time=',t2.time
        return y1
    
    def solve(self):
        """ this solves the ODE problem."""
        #-- Solution vector y: y[0]=y^{n+1}, y[1]=y^{n}, y[2]=y^{n-1}, and so on
        y = np.zeros((self.levels,self.dof),float)
        for i in range(self.levels):
            y[i] = self.y0
        #--- Data to file
        FILE = file( self.FileName, 'w' )
        FILE.write( y[0].tostring() )
        #-- Initialize
        factor=0.0
        for i in range(0,self.levels-2):
            self.Time.increment()
            factor = factor+1.0
            y[i+1] = self.__initialize__( y[i],(factor-1.0)*self.Time.h,
                                        factor*self.Time.h )
            FILE.write(y[i+1].tostring())
        #-- Time-stepping
        for i in range(self.levels-2,self.Time.time_steps):
            self.Time.increment()
            print 'i=',i,'time=',self.Time.time
            b = self.__rhs__(y)
            if self.A: # System solve required
                y[self.levels-1]=self.BoundCond(
                                            y[self.levels-1],
                                            self.Time.time )
                [y[self.levels-1],flag]= self.LinearSolver(
                                            self.H,b,
                                            y[self.levels-1],
                                            precond = self.PreCond )
            else:     # System solve not required
                y[self.levels-1] = b / self.alpha[self.levels-1]
                y[self.levels-1] = self.BoundCond( y[self.levels-1],
                                                   self.Time.time )
        FILE.write(y[self.levels-1].tostring())

        for i in range(self.levels-1):# update solution array
          y[i]=y[i+1]
          
        return y[self.levels-1]
 
 
  

