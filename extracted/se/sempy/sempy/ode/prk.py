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
import scipy as sp
import scipy.sparse.linalg as spl
import pickle as pickle
import scipy.io as sio
import sempy
import ode_f90
# Compatibility with older versions
import pysparse
if int(pysparse.__version__[2]) >= 2:
    from pysparse.sparse.pysparseMatrix import PysparseMatrix #as pysparseMatrix
    from pysparse import direct
    
if int(pysparse.__version__[2]) <=1:
    from pysparse.pysparseMatrix import PysparseMatrix

class Time:
    '''
    Sets up the temporal domain. 
       
    >>> import sempy
    >>> Y = sempy.ode.Time(start_time=0,end_time=10,time_steps=10)


    :param float start_time: Start time 
    :param float end_time: End time 
    :param int time_steps: Number of timesteps

    :attributes: * **h** (float)- Time step size
                 * **time** (float)- Time
    '''
    def __init__( self, Space, start_time=0, end_time=1.0, 
                  time_steps = 2):
        self.Space = Space
        self.start_time = float(start_time)
        self.end_time   = float(end_time)
        self.time_steps = time_steps
        self.h          = (self.end_time-self.start_time)/float(self.time_steps)
        self.time       = float(start_time)
        #solver = sempy.linsolvers.Krylov()
   
    def increment(self):
        """
        Increments the :literal:`time` attribute with the time step size 
        :literal:`h`. 

        Usage::
        
           import sempy
        
           Y = sempy.ode.Time( start_time=0,end_time=10,time_steps=10)
           Y.increment()

        """
        self.time += self.h
        
       
def dirk111():
    '''
    Euler method. Forward/backward.
    '''
    a,b,c    =np.zeros((2,2)),np.zeros(2),np.zeros(2)#float
    ah,bh,ch =np.zeros((2,2)),np.zeros(2),np.zeros(2)#float
    a[0,0],  a[0,1]=0.0, 0.0
    a[1,0],  a[1,1]=0.0, 1.0
    ah[0,0],ah[0,1]=0.0, 0.0
    ah[1,0],ah[1,1]=1.0, 0.0
    b[0],b[1]  =0.0,1.0 
    bh[0],bh[1]=1.0,0.0 
    c[0],c[1]  =0.0,1.0 
    ch[0],ch[1]=0.0,1.0 
    stages=2
    return a,b,c,ah,bh,ch,stages 

def dirk122():
    '''
    PRK method.
    '''
    a,b,c    =np.zeros((2,2),float),np.zeros((2),float),np.zeros((2),float)
    ah,bh,ch =np.zeros((2,2),float),np.zeros((2),float),np.zeros((2),float)
    a[0,0],  a[0,1]=0.0, 0.0
    a[1,0],  a[1,1]=0.0, 0.5
    ah[0,0],ah[0,1]=0.0, 0.0
    ah[1,0],ah[1,1]=0.5, 0.0
    b[0],b[1]  =0.0,1.0 
    bh[0],bh[1]=0.0,1.0 
    c[0],c[1]  =0.0,0.5 
    ch[0],ch[1]=0.0,0.5 
    stages=2
    return a,b,c,ah,bh,ch,stages 
    
def dirk222():
    '''
    PRK.
    '''
    a,b,c    =np.zeros((3,3),float),np.zeros((3),float),np.zeros((3),float)
    ah,bh,ch =np.zeros((3,3),float),np.zeros((3),float),np.zeros((3),float)
    gamma = (2.0 - sp.sqrt(2.0))/2.0
    delta = 1.0 - 1.0/(2.0*gamma)
    a[0,0], a[0,1], a[0,2] = 0.0, 0.0      ,0.0
    a[1,0], a[1,1], a[1,2] = 0.0, gamma    ,0.0
    a[2,0], a[2,1], a[2,2] = 0.0, 1.0-gamma,gamma

    ah[0,0], ah[0,1], ah[0,2] = 0.0,   0.0      ,0.0
    ah[1,0], ah[1,1], ah[1,2] = gamma, 0.0      ,0.0
    ah[2,0], ah[2,1], ah[2,2] = delta, 1.0-delta,0.0

    b[0], b[1], b[2]    = 0.0,1.0-gamma,gamma
    bh[0], bh[1], bh[2] = delta, 1.0-delta,0.0
    c[0], c[1], c[2]    = 0.0,gamma,1.0
    ch[0], ch[1], ch[2] = 0.0,gamma,1.0
    stages=3
    return a,b,c,ah,bh,ch,stages 

def irk2():
    a,b,c    = np.zeros((2,2),float),np.zeros((2),float),np.zeros((2),float)
    ah,bh,ch = np.zeros((2,2),float),np.zeros((2),float),np.zeros((2),float)
    gamma    = (2.0 - np.sqrt(2.0))/2.0
    #delta=1.0-1.0/(2.0*gamma)
    a[0,0],  a[0,1]= gamma    , 0.0
    a[1,0],  a[1,1]= 1.0-gamma, gamma
    b[0],b[1]      = 1.0-gamma, gamma
    c[0],c[1]      = gamma, 1.0
    stages=2
    return a,b,c,ah,bh,ch,stages 

def dirk443():
    '''
    PRK method of second order.
    '''
    a,b,c    =np.zeros((5,5)),np.zeros(5),np.zeros(5)#float
    ah,bh,ch =np.zeros((5,5)),np.zeros(5),np.zeros(5)#float
    gamma=(2.0-sp.sqrt(2.0))/2.0
    delta=1.0-1.0/(2.0*gamma)
     
    a[1,1]=1.0/2.0
    a[2,1],a[2,2]=1.0/6.0,1.0/2.0
    a[3,1],a[3,2],a[3,3]=-1.0/2.0,1.0/2.0,1.0/2.0
    a[4,1],a[4,2],a[4,3],a[4,4]=3.0/2.0,-3.0/2.0,1.0/2.0,1.0/2.0
    b[1],b[2],b[3],b[4]=3.0/2.0,-3.0/2.0,1.0/2.0,1.0/2.0
    c[1],c[2],c[3],c[4]=1.0/2.0,2.0/3.0,1.0/2.0,1.0

    ah[1,0] =1.0/2.0
    ah[2,0],ah[2,1]=11.0/18.0,1.0/18.0  
    ah[3,0],ah[3,1],ah[3,2]=5.0/6.0,-5.0/6.0,1.0/2.0
    ah[4,0],ah[4,1],ah[4,2],ah[4,3]=1.0/4.0,7.0/4.0,3.0/4.0,-7.0/4.0
    ch[1],ch[2],ch[3],ch[4]=1.0/2.0,2.0/3.0,1.0/2.0,1.0
    bh[0],bh[1],bh[2],bh[3]=ah[4,0],ah[4,1],ah[4,2],ah[4,3]

    stages=5
    return a,b,c,ah,bh,ch,stages 

def dirk252():
    '''
    PRK method of second order.
    '''
    a,b,c    =np.zeros((5,5)),np.zeros(5),np.zeros(5)#float
    ah,bh,ch =np.zeros((5,5)),np.zeros(5),np.zeros(5)#float
    gamma=(2.0-sp.sqrt(2.0))/2.0
    delta=1.0-1.0/(2.0*gamma)
     
    a[3,3]=gamma
    a[4,3]=1.0-gamma
    a[4,4]=gamma
    b[3]=1.0-gamma
    b[4]=gamma
    c[3]=gamma
    c[4]=1.0

    ah[1,0]=1.0/4.0
    ah[2,1]=1.0/3.0
    ah[3,2]=gamma
    ah[4,3]=1.0/(2.0*gamma)
    ah[4,0]=-np.sqrt(1.0/2.0)
    ch[1]=ah[1,0]
    ch[2]=ah[2,1]
    ch[3]=ah[3,2]
    ch[4]=1.0
    bh[0]=ah[4,0]
    bh[3]=ah[4,3]

    stages=5
    return a,b,c,ah,bh,ch,stages 

def erk4():
    '''
    Explicit RK method of order 4.
    '''
    a,b,c    =np.zeros((4,4),float),np.zeros((4),float),np.zeros((4),float)
    ah,bh,ch =np.zeros((4,4),float),np.zeros((4),float),np.zeros((4),float)

    ah[1,0]=1.0/2.0
    ah[2,1]=1.0/2.0
    ah[3,2]=1.0

    ch[1],ch[2],ch[3]=ah[1,0],ah[2,1],ah[3,2]
    bh[0],bh[1],bh[2],bh[3]=1.0/6.0 ,1.0/3.0, 1.0/3.0, 1.0/6.0
    stages=4
    return a,b,c,ah,bh,ch,stages 

def __emptyfunc__(y,t):
    v=np.zeros((y.size))
    return v

def __pre__(y):
    return y

def __bc__(y,t):
    return y

class PRK():
    '''
    Implementation of partitioned Runge-Kutta (PRK) method
    for the solution of ODE systems on the form:  
    
    .. math::
    
       M\\frac{dy}{dt}=Ly+N(y,t)
    
    :param y: Initial condition
    :type y: A collection of :class:`sempy.Function`
    :param Time: An instance of the time class.
    :type Time: :class:`sempy.ode.Time`
    :kwargs: * **L** - Linear operator
             * **L_pre** - The FEM equivalent of L. Used to create 
               preconditioner. 
             * **force_function** - A function, possibly non-linear. 
               This is the function :math:`N(y,t)` in the equation above. 
               Called as:: 
               
                 F=force_function(y,t)
                 
             * **bound_cond** - Strong BCs. Called as:: 
               
                 y=bound_cond(y,t)
                 
             * **prk_method** (*string*) - The PRK method to be used. 
               The options are:
                    * :literal:`dirk111`
                    * :literal:`dirk122`
                    * :literal:`dirk222`
                    * :literal:`dirk443`
             * **linear_solver** - The linear solver. The default is 
               CG. If L is not SPD, then one can for example use bicgstab.
             * **iter_tol** (*float*) - Iterative tolerance.
             * **maxiter** (*int*) - Maximum number of iterations.
    '''
    def __init__( self, y, Time, L = None, L_pre= None,
                  force_function = None, bound_cond = __bc__,
                  prk_method = None, file_increment = 1000,
                  hyper_filter = False,call_back=None,
                  linear_solver = None, iter_tol = 1e-10,
                  maxiter = 1000,silent=False):
        # Solution vector
        self.number_of_eq = len(y)
        self.y0 = self.output_vector(y,adopt_filename=True)
        self.y_help = self.output_vector(y)
        self.y_out = self.output_vector(y)
        self.hyper_filter = hyper_filter
        self.call_back = call_back 
        self.silent = silent

        self.file_increment= file_increment
        # Degrees of freedom
        dof = 0
        for i in range(self.number_of_eq):
            dof = dof + y[i].Space.dof 
        self.vector_size = dof
        # Strong BC
        self.bound_cond = bound_cond
        # Temporal domain
        self.Time = Time
        # PRK method
        self.prk_method = prk_method
        [self.a,self.b,self.c,self.ah,self.bh,self.ch,self.stages]=\
               self.runge_kutta_method(self.prk_method)
        # Linear operator
        self.L_in = L
        if self.L_in == None:
            self.L_in = []
            G=[]
            for i in range( self.number_of_eq ):
                G.append(0)
            for i in range( self.number_of_eq ):
                self.L_in.append(G) 
            del G

        self.L = spl.LinearOperator( (self.vector_size,
                                      self.vector_size),
                                      matvec = self.__action_linear_operator,
                                      dtype = 'float')   
        # Mass matrix
        self.M, self.M_inv = self.mass_matrix()
        # Preconditioner
        self.L_pre = L_pre
        if self.L_pre == None:
            self.L_pre_inv = 'none'
        else:
            self.L_pre_inv = self.__preconditioner(self.L_pre)
        # Non-linear function
        self.force_function = force_function
        # Linear solver:    
        self.linear_solver = linear_solver
        self.iter_tol = iter_tol
        self.maxiter=maxiter
        if self.linear_solver == None:
            self.linear_solver = sempy.linsolvers.Krylov(
                                                tol = self.iter_tol,
                                                solver_type = 'cg',
                                                maxiter=self.maxiter,
                                                pre=self.L_pre_inv)
    def to_file(self,y_vec):
        '''
        Print to file.
        '''
        dof_1 = 0
        dof_2 = 0
        for i in range(self.number_of_eq):
            dof_1 = dof_2
            dof_2 = dof_2 + self.y0[i].Space.dof
            temp = self.y0[i].Space.mapping_q( y_vec[dof_1:dof_2] )
            self.y0[i].basis_coeff = np.copy(temp)
            
        for i in range(self.number_of_eq):
            if not self.y0[i].filename == 'none':
                self.y0[i].to_file()
        
        
    def solve(self):
        '''
        Solves the ODE system. 
        '''
        #-- Solution vector y: y[0]=y^{n+1}, y[1]=y^{n}, y[2]=y^{n-1}, 
        # and so on
        ystart = np.zeros( (self.vector_size), float )
        yend   = np.zeros( (self.vector_size), float )
        ystart[:] = self.component_to_vector( self.y0 )
        # Timesteps to file:
        k_file = range( self.file_increment, 
                        self.Time.time_steps+self.file_increment, 
                        self.file_increment )
        #-To file
        #self.to_file(ystart)
        # -- Callback
        if not self.call_back == None:
            y_out = self.vector_to_component(ystart)  
            self.call_back(y_out ,self.Time.time,0)
        # --Checking for b_i=a_si
        alpha=0.0
        for i in range(self.stages):
            alpha = alpha + np.abs(self.b[i]-self.a[self.stages-1,i]) + \
                            np.abs(self.bh[i]-self.ah[self.stages-1,i])
        #-- Time-stepping
        for i in range(self.Time.time_steps):
            if not self.silent:
                print '--> time step no=',i+1
            yend = self.__timestepping__(ystart,alpha)
            # Hyper filter
            #if self.hyper_filter:
            #    y_out = self.vector_to_component(yend)
            #    for k in range(self.number_of_eq):
            #        y_out[k].hyper_filter()
            #    #y_out = self.bound_cond( y_out,self.Time.time +self.Time.h)
            #    yend = self.component_to_vector(y_out)
                
            self.Time.increment()
            ystart = np.copy(yend)
            # -- Callback
            if not self.call_back == None:
                y_out = self.vector_to_component(yend)  
                self.call_back(y_out ,self.Time.time,i+1)
            # To file
            #if (i+1) in k_file:
            #    self.to_file(ystart)
            if not self.silent:
                print 'time=',self.Time.time
            
        y_out = self.vector_to_component(yend)    
        return y_out
        
    def __timestepping__(self,ystart,alpha):
        '''
        Advancing the solution one time-step.
        '''
        #-- Solution vector yi
        yi = np.zeros((self.stages,self.vector_size),float)
        fi = np.zeros((self.stages,self.vector_size),float)
        F  = np.zeros((self.vector_size),float)
        b  = np.zeros((self.vector_size),float)
        
        #for i in range(self.stages):
        #    yi[i,:] = np.copy(ystart[:])
        yi[0,:] = np.copy(ystart[:])
            
        #-- Computing the y_i's
        for i in range(self.stages):
            F[:] = 0.0
            for j in range(i):
                # Explicit
                if np.abs(self.ah[i,j]) > 1.0e-10:
                    #F[:] = F[:] + self.Time.h * self.ah[i,j] * fi[j][:]
                    F[:] = ode_f90.vec_add(F[:],self.Time.h * self.ah[i,j],
                                           fi[j][:])
                # Implicit
                if np.abs(self.a[i,j]) > 1.0e-10:
                    b[:] = self.L*yi[j][:]
                    #F[:] = F[:] + self.Time.h*self.a[i,j]*b[:]
                    F[:] = ode_f90.vec_add(F[:],self.Time.h*self.a[i,j],b[:])
                    # include weak BCs in this step. 
                    
            b[:] = self.M * ystart[:] + F[:]
            if np.abs(self.a[i,i]) > 0.0:
                # System solve required. Solve the system Hy[i]=b
                local_time  = self.Time.time + self.c[i] * self.Time.h
                yi[i][:] = self.apply_bc(yi[i][:],local_time)
                H = sempy.operators.MultipleOperators([self.M,self.L],\
                       scaling_factor=[1.0, -self.Time.h*self.a[i,i]],\
                       assemble='no').matrix
                [yi[i][:],flag] = self.linear_solver.solve(H,b,yi[i][:])
                if not self.silent:
                    print 'iter=',flag
                # 1) Include optional hyperbolic filter here. 
            else:
                # System solve not required
                time  = self.Time.time + self.ch[i] * self.Time.h
                yi[i][:] = self.M_inv*b[:]
                #yi[i][:] = self.bound_cond(yi[i][:],time)
                yi[i][:] = self.apply_bc(yi[i][:],time)
            time  = self.Time.time + self.ch[i] * self.Time.h
            fi[i][:] = self.force_vec(yi[i][:],time)
        # Computing the final value yend:
        if np.abs(alpha) > 1.0e-10 :
            if not self.silent:
                print 'last step required'
            F[:] = 0.0
            for i in range(self.stages):
                if np.abs(self.bh[i]) > 0.0:
                    #F[:] = F[:] + self.Time.h * self.bh[i] * fi[i][:]
                    F[:] = ode_f90.vec_add(F[:],self.Time.h * self.bh[i],
                                           fi[i][:])
                if np.abs(self.b[i]) > 0.0:
                    b[:] = self.L * yi[i][:]
                    # include weak BCs here too.
                    F[:] = F[:] + self.Time.h * self.b[i] * b[:]
            yi[self.stages-1][:] = ystart[:] + self.M_inv * F[:]
            time = self.Time.time + self.Time.h
            return self.apply_bc(yi[self.stages-1][:],time)
        else :
            time = self.Time.time + self.Time.h
            return self.apply_bc(yi[self.stages-1][:],time)
    
    def force_vec( self, y_vec, t ):
        """force function."""
        # 0) Output vector
        v = np.zeros( ( self.vector_size ), float )
        # 1) Vector to functions
        y_comp = self.vector_to_component(y_vec)
        
        if not self.force_function == None:
            w = self.force_function(y_comp,t)
            dof_1=0
            dof_2=0
            for i in range(self.number_of_eq):
                dof_1 = dof_2
                dof_2 = dof_2 + self.y0[i].Space.dof
                v[dof_1:dof_2] = w[i][:]
        return v
        
    def apply_bc(self,y_vec,t):
        '''
        Apply BCs.
        '''
        # 1) Vector to functions
        y_comp = self.vector_to_component(y_vec)
        # 2) Apply BCs
        y_comp = self.bound_cond(y_comp,t)
        # 3) Functions to vector
        y_vec = self.component_to_vector(self.y_help)
        return y_vec
        
    def component_to_vector(self,y_comp):
        y_vec = np.zeros( self.vector_size, float )
        dof_1 = 0
        dof_2 = 0
        for i in range(self.number_of_eq):
            dof_1 = dof_2
            dof_2 = dof_2 + y_comp[i].Space.dof
            y_vec[dof_1:dof_2] = y_comp[i].glob()
        return y_vec
    
    def vector_to_component(self,y_vec):
        #
        dof_1 = 0
        dof_2 = 0
        for i in range(self.number_of_eq):
            dof_1 = dof_2
            dof_2 = dof_2 + self.y0[i].Space.dof
            temp = self.y0[i].Space.mapping_q( y_vec[dof_1:dof_2] )
            self.y_help[i].basis_coeff = np.copy(temp)
        return self.y_help
                                    
    def mass_matrix(self):
        M_glob = PysparseMatrix(size=self.vector_size)
        M_glob_inv = PysparseMatrix(size=self.vector_size)
        dof_1 = 0
        for i in range( self.number_of_eq ):
            mass = sempy.operators.Mass( self.y0[i].Space )
            # Mass matrix
            M_local = mass.matrix
            val,irow,jcol = M_local.find()
            M_glob.addAt(val, irow+dof_1, jcol+dof_1)
            # Inverse of mass matrix
            M_inv = mass.matrix_inv
            val,irow,jcol = M_inv.find()
            M_glob_inv.addAt(val, irow+dof_1, jcol+dof_1)
            dof_1 = dof_1 + self.y0[i].Space.dof
        return M_glob,M_glob_inv
            
    def runge_kutta_method(self,prk_method):
        '''
        Method.
        '''
        if prk_method == None:
            [a,b,c,ah,bh,ch,stages]= dirk111()
        if prk_method == 'dirk111':
            [a,b,c,ah,bh,ch,stages]= dirk111()
        if prk_method == 'dirk222':
            [a,b,c,ah,bh,ch,stages]= dirk222()
        if prk_method == 'dirk122':
            [a,b,c,ah,bh,ch,stages]= dirk122()
        if prk_method == 'dirk252':
            [a,b,c,ah,bh,ch,stages]= dirk252()
        if prk_method == 'dirk443':
            [a,b,c,ah,bh,ch,stages]= dirk443()
        if prk_method == 'erk4':
            [a,b,c,ah,bh,ch,stages]= erk4()
        if prk_method == 'irk2':
            [a,b,c,ah,bh,ch,stages]= irk2()
        
        return [a, b, c, ah, bh, ch, stages]
    
    def output_vector(self,y_in,adopt_filename=False):
        y_out=[]
        for j in range(self.number_of_eq):
            if adopt_filename:
                y_out.append( sempy.Function(y_in[j].Space,
                                         basis_coeff=0.0,
                                         filename=y_in[j].filename) )
            else:
                y_out.append( sempy.Function(y_in[j].Space,
                                         basis_coeff=0.0) )
        for j in range(self.number_of_eq):
            y_out[j].basis_coeff=np.copy(y_in[j].basis_coeff)    
        return y_out
    
    def __action_linear_operator(self,y):
        '''
        Action of the linear operator.
        '''
        v = [ ]
        w = [ ]
        for i in range(self.number_of_eq):
            v.append( np.zeros( self.y0[i].Space.dof, float ) )
            w.append( np.zeros( self.y0[i].Space.dof, float ) )
            
        # Convert global vector to its constituents
        dof_1=0
        dof_2=0
        for i in range(self.number_of_eq):
            dof_1 = dof_2
            dof_2 = dof_2 + self.y0[i].Space.dof
            w[i] = y[dof_1:dof_2]
            
        # Action of the linear operator
        for i in range(self.number_of_eq):
            for j in range(self.number_of_eq):
                v[i][:] = v[i][:] + self.L_in[i][j]* w[j]
        # Create the vector to be returned:
        v_out = np.zeros( self.vector_size, float )
        dof_1 = 0
        dof_2 = 0
        for i in range(self.number_of_eq):
            dof_1 = dof_2
            dof_2 = dof_2 + self.y0[i].Space.dof
            v_out[dof_1:dof_2] = v[i]
            
        return v_out
    
    def __preconditioner(self,L_pre):
        '''
        Precond.
        '''
        # Mass matrices
        M=[]
        for i in range( self.number_of_eq ):
            mass = sempy.operators.Mass( self.y0[i].Space ).matrix
            mass = self.__preconditioner_mask(mass,i)
            M.append(mass)
        # Combined
        P = PysparseMatrix(size=self.vector_size)

        # Assemble             
        dof_1 = 0
        for i in range(self.number_of_eq):
            dof_2 = 0
            for j in range(self.number_of_eq):
                # Block diagonal entries
                if j==i:
                    T = sempy.operators.MultipleOperators(
                                            [M[i],L_pre[i][j]], 
                                            [1.0,-self.Time.h],
                                            assemble='yes').matrix
                    T = self.__preconditioner_mask( T, j )
                    val,irow,jcol = T.find()
                    P.addAt(val, irow+dof_1, jcol+dof_2)
                # non-diagonal entries
                if not j==i:
                    T = sempy.operators.MultipleOperators(
                                           [L_pre[i][j]], 
                                           [-self.Time.h],
                                           assemble='yes').matrix
                    val,irow,jcol = T.find()
                    P.addAt(val, irow+dof_1, jcol+dof_2)
                dof_2 = dof_2 + self.y0[j].Space.dof
            dof_1 = dof_1 + self.y0[i].Space.dof
        # Convert to ll_mat
        Q = pysparse.spmatrix.ll_mat( self.vector_size, 
                                      self.vector_size )
                
        val,irow,jcol = P.find()
        Q.update_add_at(val,irow,jcol)
        del val,irow,jcol
        # Factorize
        #if self.library == 'superlu':
        print 'factorize'
        self.LU = direct.superlu.factorize( Q.to_csr(),
                                       drop_tol=0.5)#self.drop_tol )
        #if self.library == 'umfpack':
        #self.LU = umfpack.factorize( Q )
        #return P
        L_pre_inv = spl.LinearOperator( 
                                (self.vector_size,self.vector_size),
                                matvec = self.__action_precond, 
                                dtype = 'float' )
        return L_pre_inv
    
    def __action_precond(self,v):
        w = np.zeros(self.vector_size, float)
        self.LU.solve(v,w)
        return w
    
    def __preconditioner_mask(self,Q,j):
        # Mask
        if self.y0[0].Space.dim == 1:
            for k in range(self.y0[j].Space.noe_bc):
                [i, phys, bc_type, element_edge] = \
                                  self.y0[j].Space.theta_phys_bc(k)
                if bc_type == "Dir":
                     Q[int(i),int(i)] = 1.0
                     
        if self.y0[0].Space.dim == 2:
            for k in range(self.y0[j].Space.noe_bc):
                for m in range(self.y0[j].Space.n):
                    [i, phys, bc_type, element_edge] = \
                                  self.y0[j].Space.theta_phys_bc(k,m)
                    if bc_type == "Dir":
                        Q[int(i),int(i)] = 1.0
        
        if self.y0[0].Space.dim == 3:
            for k in range(self.y0[j].Space.noe_bc):
                for m in range(self.y0[j].Space.n):
                    for n in range(self.y0[j].Space.n):
                        [i, phys, bc_type, element_edge] = \
                                  self.y0[j].Space.theta_phys_bc(k,m,n)
                    if bc_type == "Dir":
                        Q[int(i),int(i)] = 1.0
                        
        return Q
            
class PRK_old_1():
    '''
    Implementation of partitioned Runge-Kutta (PRK) method
    for the solution of ODE systems on the form:  
    
    .. math::
    
       M\\frac{dy}{dt}=Ly+N(y,t)
    
    :param y: Initial condition
    :type y: A collection of :class:`sempy.Function`
    :param Time: An instance of the time class.
    :type Time: :class:`sempy.ode.Time`
    :kwargs: * **L** - Linear operator
             * **L_pre** - The FEM equivalent of L. Used to create 
               preconditioner. 
             * **force_function** - A function, possibly non-linear. 
               This is the function :math:`N(y,t)` in the equation above. 
               Called as:: 
               
                 F=force_function(y,t)
                 
             * **bound_cond** - Strong BCs. Called as:: 
               
                 y=bound_cond(y,t)
                 
             * **prk_method** (*string*) - The PRK method to be used. 
               The options are:
                    * :literal:`DIRK111`
                    * :literal:`DIRK122`
                    * :literal:`DIRK222`
                    * :literal:`DIRK443`
             * **linear_solver** - The linear solver. The default is 
               CG. If L is not SPD, then one can for example use bicgstab.
             * **iter_tol** (*float*) - Iterative tolerance.
             * **maxiter** (*int*) - Maximum number of iterations.
    '''
    def __init__( self, y, Time, L = None, L_pre= None,
                  force_function = None, bound_cond = __bc__,
                  prk_method = None, 
                  linear_solver = None, iter_tol = 1e-10,
                  maxiter = 1000):
        # Solution vector
        self.number_of_eq = len(y)
        self.y0 = self.output_vector(y)
        self.y_out = self.output_vector(y)
        dof = 0
        for i in range(self.number_of_eq):
            dof = dof + self.y0[i].Space.dof 
        self.vector_size = dof
        # Strong BC
        self.bound_cond = bound_cond
        # Temporal
        self.Time = Time
        # PRK method
        self.prk_method = prk_method
        if self.prk_method == None:
            [self.a,self.b,self.c,
             self.ah,self.bh,self.ch,self.stages]= dirk111()
        if self.prk_method == 'dirk111':
            [self.a,self.b,self.c,
             self.ah,self.bh,self.ch,self.stages]= dirk111()
        if self.prk_method == 'dirk222':
            [self.a,self.b,self.c,
             self.ah,self.bh,self.ch,self.stages]= dirk222()
        if self.prk_method == 'dirk122':
            [self.a,self.b,self.c,
             self.ah,self.bh,self.ch,self.stages]= dirk122()
        if self.prk_method == 'dirk252':
            [self.a,self.b,self.c,
             self.ah,self.bh,self.ch,self.stages]= dirk252()
        if self.prk_method == 'dirk443':
            [self.a,self.b,self.c,
             self.ah,self.bh,self.ch,self.stages]= dirk443()
        if self.prk_method == 'erk4':
            [self.a,self.b,self.c,
             self.ah,self.bh,self.ch,self.stages]= erk4()
        if self.prk_method == 'irk2':
            [self.a,self.b,self.c,
             self.ah,self.bh,self.ch,self.stages]= irk2()
        # Linear operator
        self.L_in = L
        if self.L_in == None:
            self.L_in = []
            G=[]
            for i in range( self.number_of_eq ):
                G.append(0)
            for i in range( self.number_of_eq ):
                self.L_in.append(G) 
            del G
        self.L = spl.LinearOperator( (self.vector_size,
                                      self.vector_size),
                                      matvec = self.__action_linear_operator,
                                      dtype = 'float')   
        # Mass matrix
        self.M = PysparseMatrix(size=self.vector_size)
        self.M_inv = PysparseMatrix(size=self.vector_size)
        dof_1 = 0
        for i in range( self.number_of_eq ):
            mass = sempy.operators.Mass( self.y0[i].Space )
            # Mass
            M = mass.matrix
            val,irow,jcol = M.find()
            self.M.addAt(val, irow+dof_1, jcol+dof_1)
            # Mass inverse
            M_inv = mass.matrix_inv
            val,irow,jcol = M_inv.find()
            self.M_inv.addAt(val, irow+dof_1, jcol+dof_1)
            dof_1 = dof_1 + self.y0[i].Space.dof
        # Preconditioner
        self.L_pre = L_pre
        if self.L_pre == None:
            self.L_pre_inv = 'none'
        else:
            self.L_pre_inv = self.__preconditioner(self.L_pre)
        # Non-linear function
        self.force_function = force_function
        # Linear solver:    
        self.linear_solver = linear_solver
        self.iter_tol = iter_tol
        self.maxiter=maxiter
        if self.linear_solver == None:
            self.linear_solver = sempy.linsolvers.Krylov(
                                                tol = self.iter_tol,
                                                solver_type = 'cg',
                                                maxiter=self.maxiter,
                                                pre=self.L_pre_inv)
    def output_vector(self,y_in):
        self.y_out=[]
        for j in range(self.number_of_eq):
            self.y_out.append( sempy.Function(y_in[j].Space,
                                              basis_coeff=0.0) )
        for j in range(self.number_of_eq):
            self.y_out[j].basis_coeff=np.copy(y_in[j].basis_coeff)    
        return self.y_out
            
    def __preconditioner_mask(self,Q,j):
        # Mask
        if self.y0[0].Space.dim == 1:
            for k in range(self.y0[j].Space.noe_bc):
                [i, phys, bc_type, element_edge] = \
                                  self.y0[j].Space.theta_phys_bc(k)
                if bc_type == "Dir":
                     Q[int(i),int(i)] = 1.0
                     
        if self.y0[0].Space.dim == 2:
            for k in range(self.y0[j].Space.noe_bc):
                for m in range(self.y0[j].Space.n):
                    [i, phys, bc_type, element_edge] = \
                                  self.y0[j].Space.theta_phys_bc(k,m)
                    if bc_type == "Dir":
                        Q[int(i),int(i)] = 1.0
        return Q
    
                                        
    def __preconditioner(self,L_pre):
        '''
        Precond.
        '''
        # Mass matrices
        M=[]
        for i in range( self.number_of_eq ):
            mass = sempy.operators.Mass( self.y0[i].Space ).matrix
            mass = self.__preconditioner_mask(mass,i)
            M.append(mass)
        # Combined
        P = PysparseMatrix(size=self.vector_size)

        # Assemble             
        dof_1 = 0
        for i in range(self.number_of_eq):
            dof_2 = 0
            for j in range(self.number_of_eq):
                # Block diagonal entries
                if j==i:
                    T = sempy.operators.MultipleOperators(
                                            [M[i],L_pre[i][j]], 
                                            [1.0,-self.Time.h],
                                            assemble='yes').matrix
                    T = self.__preconditioner_mask( T, j )
                    val,irow,jcol = T.find()
                    P.addAt(val, irow+dof_1, jcol+dof_2)
                # non-diagonal entries
                if not j==i:
                    T = sempy.operators.MultipleOperators(
                                           [L_pre[i][j]], 
                                           [-self.Time.h],
                                           assemble='yes').matrix
                    val,irow,jcol = T.find()
                    P.addAt(val, irow+dof_1, jcol+dof_2)
                dof_2 = dof_2 + self.y0[j].Space.dof
            dof_1 = dof_1 + self.y0[i].Space.dof
        # Convert to ll_mat
        Q = pysparse.spmatrix.ll_mat( self.vector_size, 
                                      self.vector_size )
                
        val,irow,jcol = P.find()
        Q.update_add_at(val,irow,jcol)
        del val,irow,jcol
        # Factorize
        #if self.library == 'superlu':
        print 'factorize'
        self.LU = direct.superlu.factorize( Q.to_csr(),
                                       drop_tol=0.5)#self.drop_tol )
        #if self.library == 'umfpack':
        #self.LU = umfpack.factorize( Q )
        #return P
        L_pre_inv = spl.LinearOperator( 
                                (self.vector_size,self.vector_size),
                                matvec = self.__action_precond, 
                                dtype = 'float' )
        return L_pre_inv
    
    def __action_precond(self,v):
        w = np.zeros(self.vector_size, float)
        self.LU.solve(v,w)
        return w
                                    
                
    def component_to_vector(self,y_comp):
        y_vec = np.zeros( self.vector_size, float )
        dof_1 = 0
        dof_2 = 0
        for i in range(self.number_of_eq):
            dof_1 = dof_2
            dof_2 = dof_2 + y_comp[i].Space.dof
            y_vec[dof_1:dof_2] = y_comp[i].glob()
        return y_vec
    
    def vector_to_component(self,y_vec):
        #
        dof_1 = 0
        dof_2 = 0
        for i in range(self.number_of_eq):
            dof_1 = dof_2
            dof_2 = dof_2 + self.y_out[i].Space.dof
            temp = self.y0[i].Space.mapping_q( y_vec[dof_1:dof_2] )
            self.y_out[i].basis_coeff = np.copy(temp)
        
    
    def __action_linear_operator(self,y):
        # Action of the linear operator.
        v = [ ]
        w = [ ]
        for i in range(self.number_of_eq):
            v.append( np.zeros( self.y0[i].Space.dof, float ) )
            w.append( np.zeros( self.y0[i].Space.dof, float ) )
        # Convert global vector to its constituents
        dof_1=0
        dof_2=0
        for i in range(self.number_of_eq):
            dof_1 = dof_2
            dof_2 = dof_2 + self.y0[i].Space.dof
            w[i] = y[dof_1:dof_2]
        # Action of the linear operator
        for i in range(self.number_of_eq):
            for j in range(self.number_of_eq):
                #if not self.L_in[i][j] == None:
                v[i][:] = v[i][:] + self.L_in[i][j]* w[j]
        # Create the vector to be returned:
        v_out = np.zeros( self.vector_size, float )
        dof_1 = 0
        dof_2 = 0
        for i in range(self.number_of_eq):
            dof_1 = dof_2
            dof_2 = dof_2 + self.y0[i].Space.dof
            v_out[dof_1:dof_2] = v[i]
            
        return v_out
             
    def force_vec( self, y, t ):
        """force function."""
        v = np.zeros( ( self.vector_size ), float )
        if not self.force_function == None:
            w = self.force_function(y,t)
            dof_1=0
            dof_2=0
            for i in range(self.number_of_eq):
                dof_1 = dof_2
                dof_2 = dof_2 + self.y_out[i].Space.dof
                v[dof_1:dof_2] = w[i]
        return v
    
    #def __bc( self, y, t ):
    #    """This is an empty function."""
    #    # 1) Vector to constituents
    #    self.vector_to_component( y )# gives self.y_out
    #    self.y_out = self.bound_cond( self.y_out, t )
    #    # w is [sempy Functions]
    #    y = self.component_to_vector( self.y_out )
    #    return y
        
    def solve(self):
        '''
        Solves the ODE system. 
        '''
        #-- Solution vector y: y[0]=y^{n+1}, y[1]=y^{n}, y[2]=y^{n-1}, 
        # and so on
        ystart = np.zeros( (self.vector_size), float )
        yend   = np.zeros( (self.vector_size), float )
        ystart[:] = self.component_to_vector( self.y0 )
        # --Checking for b_i=a_si
        alpha=0.0
        for i in range(self.stages):
            alpha = alpha + np.abs(self.b[i]-self.a[self.stages-1,i]) + \
                            np.abs(self.bh[i]-self.ah[self.stages-1,i])
        #-- Time-stepping
        for i in range(self.Time.time_steps):
            print '--> time step no=',i+1
            yend = self.__timestepping__(ystart,alpha)
            self.Time.increment()
            ystart = yend
            self.vector_to_component(yend)
            #self.y0.to_file()
            print 'time=',self.Time.time
            #self.y_out[0].plot_wire()
            
        return self.y_out


    def __timestepping__(self,ystart,alpha):
        '''
        Advancing the solution one time-step.
        '''
        #-- Solution vector yi
        yi = np.zeros((self.stages,self.vector_size),float)
        fi = np.zeros((self.stages,self.vector_size),float)
        F  = np.zeros((self.vector_size),float)
        b  = np.zeros((self.vector_size),float)
        y_temp  = np.zeros((self.vector_size),float)
        for i in range(self.stages):
            yi[i,:] = np.copy(ystart[:])
            #yi[i,:] = ystart[:]
        #-- Computing the y_i's
        for i in range(self.stages):
            F[:] = 0.0
            for j in range(i):
                # Explicit
                if np.abs(self.ah[i,j]) > 0.0:
                    F[:] = F[:] + self.Time.h * self.ah[i,j] * fi[j][:]
                # Implicit
                if np.abs(self.a[i,j]) > 0.0:
                    b[:] = self.L*yi[j][:]
                    F[:] = F[:] + self.Time.h*self.a[i,j]*b[:]
                    # include weak BCs in this step. 
                    
            b[:] = self.M*ystart[:] + F[:]
            if np.abs(self.a[i,i]) > 0.0:
                # System solve required. Solve the system Hy[i]=b
                local_time  = self.Time.time + self.c[i] * self.Time.h
                yi[i][:] = self.bound_cond(yi[i][:],local_time)
                H = sempy.operators.MultipleOperators([self.M,self.L],\
                       scaling_factor=[1.0, -self.Time.h*self.a[i,i]],\
                       assemble='no').matrix
                [yi[i][:],flag] = self.linear_solver.solve(H,b,yi[i][:])
                #yi[i][:]=np.copy(y_temp[:])
                print 'iter=',flag
                # 1) If pressure-correction: include poisson solver and
                # update equations
                # 2) Include optional hyperbolic filter here. 
            else:
                # System solve not required
                time  = self.Time.time + self.ch[i] * self.Time.h
                yi[i][:] = self.M_inv*b[:]
                yi[i][:] = self.bound_cond(yi[i][:],time)
            time  = self.Time.time + self.ch[i] * self.Time.h
            fi[i][:] = self.force_vec(yi[i][:],time)
        # Computing the final value yend:
        if np.abs(alpha) > 0.0 :
            print 'last step required'
            F[:] = 0.0
            for i in range(self.stages):
                if np.abs(self.bh[i]) > 0.0:
                    F[:] = F[:] + self.Time.h * self.bh[i] * fi[i][:]
                if np.abs(self.b[i]) > 0.0:
                    b[:] = self.L * yi[i][:]
                    # include weak BCs here too.
                    F[:] = F[:] + self.Time.h * self.b[i] * b[:]
            yi[self.stages-1][:] = ystart[:] + self.M_inv * F[:]
            time = self.Time.time + self.Time.h
            return self.bound_cond(yi[self.stages-1][:],time)
        else :
            time = self.Time.time + self.Time.h
            return self.bound_cond(yi[self.stages-1][:],time)#yi[self.stages-1]


   

class PRK_old_2():
    ''' 
    Implementation of partitioned Runge-Kutta (PRK) methods
    for the solution of ODE systems.  
    
    Solves
    
    .. math:: 
       \underline{M}\\frac{d\underline{y}}{dt}=
       \underline{L}\,\underline{y}+\underline{N}(\underline{y},t) 
       
    where :math:`\underline{M}` is the SEM mass matrix, 
    :math:`\underline{L}` is a linear operator and 
    :math:`\underline{N}` is a non-linear function.
    
    :param y: Starting value.
    :type y: :class:`sempy.Function`
    :param Mass: An instance of the Mass class. This instance supplies the 
                 mass matrix and its inverse.   
    :type Mass: :class:`sempy.operators.Mass`
    :param matrix L: Linear operator.
    :param matrix L_pre: A matrix that approximates :literal:`L`. 
                         Used for preconditioning. 
    :param function non_lin: Function to be treated explicitly. Called as 
                     :literal:`non_lin(y,t)`.
    
    :param function bound_cond: Function with (possibly) time dependent boundary 
                       conditions. Called as :literal:`bound_cond(y,t)`. 
    :param string prk_method: The PRK method can be 
                              :literal:`dirk111`, 
                              :literal:`dirk122`, 
                              :literal:`dirk222`.
    :param LinearSolver: The linear solver for system solves at 
                         each time-step. It is called as 
                         :literal:`LinearSolver.solve(A,b,u)`. The default 
                         is CG.  
    :type LinearSolver: :class:`sempy.linsolvers.Krylov`, :class:`sempy.linsolvers.Direct`
    
    '''
    def __init__( self, y, Mass , Time, L = 'none', L_pre = 'none',
                  non_lin = 'none',
                  bound_cond = 'none', prk_method = 'dirk111',
                  LinearSolver = 'none' ):
        
        self.y0 = y
        self.Space = self.y0.Space
        self.dof = self.Space.dof
        self.Time = Time
        
        #start_time = 0.0, end_time = 1.0,time_steps = 5,
        #self.start_time = float(start_time)
        #self.end_time   = float(end_time)
        #self.time_steps = time_steps
        #self.h = (self.end_time-self.start_time)/float(self.time_steps)
        
        
        
        if non_lin == 'none':
            self.exp_func =  __emptyfunc__
        else:
            self.exp_func = non_lin
        
        #if Mass == 'none':
        #    self.M     = np.ones((self.dof),float)
        #    self.M_inv = np.ones((self.dof),float)
        #    self.M     = self.L.Space.mask(self.M)
        #    self.M_inv = self.L.Space.mask(self.M_inv)
        #else:
        self.M = Mass.matrix
        self.M_inv = Mass.matrix_inv
        self.L = L
        
        
        if bound_cond == 'none':
            self.bound_cond = __emptyfunc__
        else:
            self.bound_cond = bound_cond
            
        self.prk_method = prk_method
        
        if LinearSolver == 'none':
            self.LinearSolver = sempy.linsolvers.Krylov()
        else:
            self.LinearSolver = LinearSolver
        
        #self.L_pre = L_pre
           
        try:
            if L_pre == 'none':
                print 'L_pre'
                self.L_pre = L_pre
        except:
            #pass
            self.L_pre = L_pre
            self.LinearSolver.pre = sempy.precond.Preconditioner(
                                self.y0.Space, 
                                [self.M,self.L_pre],
                                scaling_factor=[1.0, -self.Time.h]).matrix
                    
                    
                    
            #self.LinearSolver.pre = sempy.precond.Preconditioner(
            #                    self.y0.Space, 
            #                    [self.M,self.L_pre],
            #                    scaling_factor=[1.0, -self.Time.h]).matrix
        #self.LinearSolver.pre = sempy.precond.Preconditioner([self.M,self.L.fem_matrix],\
        #                                    self.L.SpaceFEM,\
        #                                    scaling_factor=[1.0, -self.Time.h ]).matrix
        
        if self.prk_method == 'dirk111':
            [self.a,self.b,self.c,self.ah,self.bh,self.ch,self.stages]= \
                                                           dirk111()
        if self.prk_method == 'dirk122':
            [self.a,self.b,self.c,self.ah,self.bh,self.ch,self.stages]= \
                                                           dirk122()
        if self.prk_method == 'dirk222':
            [self.a,self.b,self.c,self.ah,self.bh,self.ch,self.stages]= \
                                                           dirk222()
        if self.prk_method == 'dirk252':
            [self.a,self.b,self.c,self.ah,self.bh,self.ch,self.stages]= \
                                                           dirk252()
   
    def solve(self):
        '''
        Solves the ODE system. 
        '''
        #-- Solution vector y: y[0]=y^{n+1}, y[1]=y^{n}, y[2]=y^{n-1}, 
        # and so on
        ystart = np.zeros( (self.dof), float )
        yend   = np.zeros( (self.dof), float )
        #ystart[:] = self.y0[:]
        ystart[:] = self.y0.glob()
        
        # --Checking for b_i=a_si
        alpha=0.0
        for i in range(self.stages):
            alpha = alpha + np.abs(self.b[i]-self.a[self.stages-1,i]) + \
                            np.abs(self.bh[i]-self.ah[self.stages-1,i])
        #-- Output
        self.y0.to_file()
        #-- Time-stepping
        for i in range(self.Time.time_steps):
            print '--> time step no=',i+1
            yend = self.__timestepping__(ystart,alpha)
            self.Time.increment()
            ystart = yend
            self.y0.basis_coeff = self.Space.mapping_q(ystart)
            self.y0.to_file()
            print 'time=',self.Time.time
            
        return self.y0


    def __timestepping__(self,ystart,alpha):
        #-- Solution vector yi
        yi = np.zeros((self.stages,self.dof),float)
        fi = np.zeros((self.stages,self.dof),float)
        F  = np.zeros((self.dof),float)
        b  = np.zeros((self.dof),float)
        for i in range(self.stages):
            yi[i,:] = ystart[:]
        #-- Advancing the solution one time step:
        #-- Computing the y_i's
        for i in range(self.stages):
            F[:] = 0.0
            for j in range(i):
                if np.abs(self.ah[i,j]) > 0.0:
                    F = F + self.Time.h * self.ah[i,j] * fi[j]
                #if self.L != 'none' and np.abs(self.a[i,j]) > 0.0:
                if np.abs(self.a[i,j]) > 0.0:
                    b = self.L*yi[j]
                    F = F + self.Time.h*self.a[i,j]*b
                    
            b = self.M*ystart + F
            #if self.L != 'none' and np.abs(self.a[i,i]) > 0.0:
            if np.abs(self.a[i,i]) > 0.0:
                # System solve required. Solve the system Hy[i]=b
                time  = self.Time.time + self.c[i] * self.Time.h
                yi[i] = self.bound_cond(yi[i],time)
                #H  = Helmholtz(self.M,self.L,self.Time.h,1.0,\
                #               self.a[i,i]).matrix
                H = sempy.operators.MultipleOperators([self.M,self.L],\
                       scaling_factor=[1.0, -self.Time.h*self.a[i,i]],\
                       assemble='no').matrix
                # If uzawa: solve uzawa
                #p=uzawa(H,b,G,D)
                [yi[i],flag] = self.linear_solver.solve(H,b,yi[i])
                print 'iter=',flag
            else:
                # System solve not required
                time  = self.Time.time + self.ch[i] * self.Time.h
                #yi[i] = self.bound_cond(b,time)
                yi[i] = self.M_inv*b
                yi[i] = self.bound_cond(yi[i],time)
            time  = self.Time.time + self.ch[i] * self.Time.h
            fi[i] = self.exp_func(yi[i],time)
        #--- Computing the final value yend:
        if alpha > 0 :
            # print 'last step required'
            F[:] = 0.0
            for i in range(self.stages):
                if np.abs(self.bh[i]) > 0.0:
                    F = F + self.Time.h * self.bh[i] * fi[i]
                #if self.L != 'none' and np.abs(self.b[i]) > 0.0:
                if np.abs(self.b[i]) > 0.0:
                    b = self.L * yi[i]
                    F = F + self.Time.h * self.b[i] * b
            yi[self.stages-1] = ystart + self.M_inv * F
            time = self.Time.time + self.Time.h
            return self.bound_cond(yi[self.stages-1], time)
        else :
            return yi[self.stages-1]


    

