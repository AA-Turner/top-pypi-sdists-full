import sempy
from prk import PRK
import numpy as np


def bdf1():
    # First order.
    alpha =np.zeros((2),float)
    beta =np.zeros((2),float)
    alpha[1], alpha[0] = 1.0, -1.0
    beta[1] = 1.0
    levels=2
    return alpha,beta,levels

def bdf2():
    # second order
    alpha =np.zeros((3),float)
    beta =np.zeros((3),float)
    alpha[2], alpha[1], alpha[0] = 1.5, -2.0, 0.5
    beta[2] = 1.0
    levels=3
    return alpha,beta,levels

def bdf3():
    # Third order.
    alpha =np.zeros((4),float)
    beta =np.zeros((4),float)
    alpha[3],alpha[2],alpha[1],alpha[0]=11.0/6.0,-3.0,3.0/2.0,-1.0/3.0
    beta[3]=1.0
    levels=4
    return alpha,beta,levels

def bdf4():
    # Fourth order
    alpha =np.zeros((5),float)
    beta =np.zeros((5),float)
    alpha[4],alpha[3],alpha[2],alpha[1],alpha[0]=25.0/12.0,-4.0,3.0,-4.0/3.0,1.0/4.0
    beta[4] = 1.0
    levels=5
    return alpha,beta,levels

def __bc__(y,t):
    return y

class OIFS(PRK):
    '''
    Operator integration factor splitting (OIFS) method for the solution 
    of 
    
    .. math::
       M\\frac{dy}{dt}=Ly+N(y,t)
    
    where :math:`M` is the mass matrix, :math:`L` is a linear operator 
    and :math:`N(y,t)` is a non-linear function. 
    
    :param y: Initial condition
    :type y: A collection of :class:`sempy.Function`
    :param Time: An instance of the :class:`sempy.ode.Time` class.
    :kwargs: * **L** - Linear operator
             * **L_pre** - The FEM equivalent of L. Used to create 
               preconditioner. 
             * **force_function** - A function, possibly non-linear. 
               This is the function :math:`N(y,t)` in the equation above.
             * **bound_cond** - Strong BCs.
             * **order** (*int*) - Order of the method to be used. 
             * **explicit_steps** (*int*) - Number of steps with the explicit 
               solver. 
             * **init_steps** (*int*) - Number of inital steps to kickstart 
               the solution process. 
             * **linear_solver** - The linear solver. The default is 
               CG. If L is not SPD, then one can for example use bicgstab.
             * **iter_tol** (*float*) - Iterative tolerance.
    '''
    def __init__(self, y, Time, L = None, L_pre= None,
                 force_function = None, bound_cond = __bc__,
                 order = 1, explicit_steps = 1,
                 init_steps = 1, file_increment = 1000,
                 hyper_filter = False,call_back=None,
                 linear_solver = None, iter_tol = 1e-10,maxiter=1000):
        PRK.__init__( self, y, Time, L = L, L_pre= L_pre,
                      force_function = force_function, 
                      bound_cond = bound_cond, 
                      file_increment = file_increment,
                      hyper_filter = hyper_filter,call_back=call_back,
                      linear_solver = linear_solver, iter_tol = iter_tol,
                      maxiter=maxiter)
        
        self.explicit_steps = explicit_steps
        self.init_steps = init_steps
        self.order = order
        
        if self.order==1:
            [self.alpha,self.beta,self.levels]=bdf1()
        if self.order==2:
            [self.alpha,self.beta,self.levels]=bdf2()
        if self.order==3:
            [self.alpha,self.beta,self.levels]=bdf3()
        if self.order==4:
            [self.alpha,self.beta,self.levels]=bdf4()
            
    def solve(self):
        '''
        Solve the equations. 
        '''
        #-- Solution vectors
        y_vec = np.zeros( (self.vector_size), float )
        #
        y_tilde=[]
        for i in range(self.levels-1):
            y_temp=[]
            for j in range(self.number_of_eq):
                y_temp.append( sempy.Function(self.y0[j].Space,
                                              basis_coeff=0.0) )
            y_tilde.append( y_temp )
            del y_temp
        y=[]
        for i in range(self.levels):
            y_temp=[]
            for j in range(self.number_of_eq):
                y_temp.append( sempy.Function(self.y0[j].Space,
                                              basis_coeff=0.0) )
            y.append( y_temp )
            del y_temp
        # Init value
        for i in range(self.levels-1):
            for j in range(self.number_of_eq):
                y_tilde[i][j].basis_coeff=np.copy(self.y0[j].basis_coeff)
        for i in range(self.levels):
            for j in range(self.number_of_eq):
                y[i][j].basis_coeff=np.copy(self.y0[j].basis_coeff)
        #-- Explicit solver
        Time_local = sempy.ode.Time(self.Time.Space,
                        start_time = 0.0,
                        end_time = self.Time.h,
                        time_steps = self.explicit_steps)
        y_help = self.output_vector(self.y0,adopt_filename=False)
        erk = sempy.ode.PRK( y_help,Time_local,
                             force_function = self.force_function, 
                             bound_cond = self.bound_cond,
                             prk_method='erk4',
                             hyper_filter=self.hyper_filter,
                             file_increment = 100000)
        # -- Callback
        if not self.call_back == None:
            self.call_back(y[0],self.Time.time,0)
        #-- Initialize
        factor=0.0
        for i in range(0,self.levels-2):
            self.Time.increment()
            factor = factor + 1.0
            y_temp = self.__initialize__( y[i],
                                          (factor-1.0)*self.Time.h,
                                          factor*self.Time.h )
            for k in range(self.number_of_eq):
                y[i+1][k].basis_coeff = np.copy(y_temp[k].basis_coeff)
            del y_temp
            # -- Callback
            if not self.call_back == None:
                self.call_back(y[i+1],self.Time.time,i+1)
                
           
        #-- Time-stepping
        for i in range(self.levels-2,self.Time.time_steps):
            self.Time.increment()
            time_global = self.Time.time
            h = self.Time.h
            # Solve the non-linear problem
            for j in range(self.levels-1):
                Time_local = sempy.ode.Time(self.Time.Space,
                               start_time = time_global - \
                                     np.float(self.levels-j-1)*h,
                               end_time = time_global,
                               time_steps = \
                                   self.explicit_steps*(self.levels-j-1))
                # Initial condition
                for k in range(self.number_of_eq):
                    erk.y0[k].basis_coeff = np.copy(y[j][k].basis_coeff)
                erk.Time = Time_local
                # Solve the problem
                y_temp = erk.solve()
                
                for k in range(self.number_of_eq):
                    y_tilde[j][k].basis_coeff = np.copy(y_temp[k].basis_coeff)
                del y_temp 
            # Calculate right hand side for the linear problem
            b = self.__rhs__(y_tilde)
            # Helmholtz operator
            H = sempy.operators.MultipleOperators([self.M,self.L],
                      scaling_factor=[self.alpha[self.levels-1], 
                                    -self.Time.h*self.beta[self.levels-1]],
                      assemble='no').matrix
            # Solve linear system
            # Boundary conditions
            y[self.levels-1] = self.bound_cond(y[self.levels-1],
                                               self.Time.time)
            y_vec = self.component_to_vector( y[self.levels-1] )
            [y_vec,flag] = self.linear_solver.solve(H, b, y_vec)
            y[self.levels-1] = self.vector_to_component_x(y_vec,
                                                   y[self.levels-1])
            print 'iter=',flag
            # Update solution array
            for k in range(self.levels-1):
                for j in range(self.number_of_eq):
                    y[k][j].basis_coeff=np.copy(y[k+1][j].basis_coeff)
            # -- Callback
            if not self.call_back == None:
                self.call_back(y[self.levels-1],self.Time.time,i+1)
                
        return y[self.levels-1]
    
    def __initialize__(self,y_0,start,end):
        print 'initialize...'
        
        Time_local = sempy.ode.Time( self.Time.Space,
                             start_time = start,
                             end_time = end,
                             time_steps = self.init_steps )
        print 'local h=',Time_local.h
        y_t=[]
        for j in range(self.number_of_eq):
            y_t.append( sempy.Function(y_0[j].Space,
                                       basis_coeff=0.0) )
        for k in range(self.number_of_eq):
            y_t[k].basis_coeff = np.copy(y_0[k].basis_coeff)
        euler= OIFS( y_t, Time_local, 
                     L = self.L_in, L_pre= self.L_pre,
                     force_function = self.force_function, 
                     bound_cond = self.bound_cond,
                     order = 1, 
                     explicit_steps = self.explicit_steps,
                     linear_solver = self.linear_solver, 
                     iter_tol = self.iter_tol,
                     file_increment = 10000)
        y1 = euler.solve()
        del euler
        return y1
    
    def vector_to_component_x(self,y_vec,y_comp):
        #
        dof_1 = 0
        dof_2 = 0
        for i in range(self.number_of_eq):
            dof_1 = dof_2
            dof_2 = dof_2 + y_comp[i].Space.dof
            temp = y_comp[i].Space.mapping_q( y_vec[dof_1:dof_2] )
            y_comp[i].basis_coeff = np.copy(temp)
        return y_comp
            
    def __rhs__(self,y_tilde):
        F = np.zeros((self.vector_size),float)
        #s = np.zeros((self.vector_size),float)
        # Time derivative
        #for i in range(0,self.alpha.size-1):
        for i in range(self.levels-1):
            if abs(self.alpha[i]) > 0.0:
                y_vec = self.component_to_vector( y_tilde[i] )
                F = F - self.alpha[i] * ( self.M * y_vec )
        # weak BCs
        return F
        
        