import sempy
from prk import PRK
import numpy as np


def __bc__(y,t):
    return y

class Strang(PRK):
    '''
    Implementation of an operator splitting approach known as Strang splitting. 
    The method solves a system of ODEs 
    
    .. math::
       M\\frac{dy}{dt}=Ly+N(y,t)
    
    where :math:`L` is a linear operator and :math:`N(y,t)` is a non-linear 
    function. 
    
    The first order method consists of solving two sub-problems:
    
    .. math::
    
       \\frac{d\\tilde y}{dt}=N(y,t),\quad {\\tilde y}_0=y^{n},\quad 
       t^{n} < t \\le t^{n+1}
       
       \\frac{d\\tilde{\\tilde y}}{dt}=Ly,\quad
       {\\tilde{\\tilde{y}}}_0={\\tilde y}(t^{n+1}),\quad 
       t^{n} < t \\le t^{n+1}
       
       y^{n+1}={\\tilde{\\tilde{y}}}(t^{n+1})
    
    The second order method is similar, but here the symmetry increases 
    the accuracy:
    
    .. math::
    
       \\frac{d\\tilde y}{dt}=N(\\tilde y,t),\quad 
       {\\tilde y}_0=y^{n},\quad 
       t^{n} < t \\le t^{n+1/2}
       
       \\frac{d\\tilde{\\tilde y}}{dt}=Ly,\quad
       {\\tilde{\\tilde{y}}}_0={\\tilde y}(t^{n+1}),\quad 
       t^{n} < t \\le t^{n+1}
       
       \\frac{d\\tilde y}{dt}=N(\\tilde y,t),\quad 
       {\\tilde y}_0={\\tilde{\\tilde{y}}}(t^{n+1}),\quad 
       t^{n+1/2} < t \\le t^{n+1}
       
       y^{n+1}= \\tilde{y}(t^{n+1})
       
    :param y: Initial condition
    :type y: A collection of :class:`sempy.Function`
    :param Time: An instance of the :class:`sempy.ode.Time` class.
    :kwargs: * **L** - Linear operator
             * **L_pre** - The FEM equivalent of L. Used to create 
               preconditioner. 
             * **force_function** - A function, possibly non-linear. 
               This is the function :math:`N(y,t)` in the equation above.
             * **bound_cond** - Strong BCs.
             * **order** (*int*) - Order of the method. Either 1 or 2. 
             * **explicit_steps** (*int*) -  Number of steps used in the 
               explicit solver. 
             * **linear_solver** - The linear solver. The default is 
               CG. If L is not SPD, then one can for example use bicgstab.
             * **iter_tol** (*float*) - Iterative tolerance.
    '''
    def __init__(self, y, Time, L = None, L_pre= None,
                 force_function = None, bound_cond = __bc__,
                 order = 1, explicit_steps = 1,
                 file_increment = 1000,hyper_filter = False,
                 call_back=None,
                 linear_solver = None, iter_tol = 1e-10, maxiter = 1000):
        PRK.__init__( self, y, Time, L = L, L_pre= L_pre,
                      force_function = force_function, 
                      bound_cond = bound_cond, 
                      file_increment=file_increment,
                      hyper_filter = hyper_filter,call_back=call_back,
                      linear_solver = linear_solver, iter_tol = iter_tol,
                      maxiter = maxiter)
        self.explicit_steps = explicit_steps
        self.order = order
        
    def solve(self):
        '''
        Solves the ODE system.
        '''
        if self.order == 1:
            y = self.solve_1st()
            return y
        
        if self.order == 2:
            y = self.solve_2nd()
            return y
                    
    def solve_1st(self):
        #-- Solution vector y: y[0]=y^{n+1}, 
        ystart = self.y0
        #
        irk = sempy.ode.PRK( ystart, self.Time, 
                             L = self.L_in, L_pre = self.L_pre,
                             bound_cond = self.bound_cond,
                             prk_method = 'dirk111',
                             iter_tol = self.iter_tol,
                             maxiter=self.maxiter )
        prk = sempy.ode.PRK( ystart,self.Time,
                             force_function = self.force_function, 
                             bound_cond = self.bound_cond,
                             prk_method='erk4')
        # -- Callback
        if not self.call_back == None: 
            self.call_back(self.y0, self.Time.time,0)
        #-- Time-stepping
        for i in range(self.Time.time_steps):
            local_time = self.Time.time
            h = self.Time.h
            # Solve non-linear problem explicitly
            Time_local = sempy.ode.Time(self.Time.Space,
                           start_time = local_time,
                           end_time = local_time + h,
                           time_steps = self.explicit_steps)
            prk.y0 = ystart
            prk.Time = Time_local
            yend = prk.solve()
            # Solve linear problem implicitly
            #y_temp1 = self.component_to_vector( yend )
            #y_temp  = self.apply_bc(y_temp1,local_time)
            #self.vector_to_component(y_temp)
            
            Time_local = sempy.ode.Time(self.Time.Space,
                          start_time = local_time,
                          end_time = local_time + h,
                          time_steps = 1)
            
            irk.y0 = self.bound_cond(yend,local_time)#self.y_out
            irk.Time = Time_local
            ystart = irk.solve()
            self.Time.increment()
            print '--> Time step number: ', i+1,'time=',self.Time.time
            # -- Callback
            if not self.call_back == None:
                self.call_back(ystart,self.Time.time,i+1)
            
        return ystart
    
    def solve_2nd(self):
        #-- Solution vector y: y[0]=y^{n+1}, 
        ystart = self.y0
        # Use only one time-step for the implicit solver. Otherwise
        # implement complex BCs.
        irk = sempy.ode.IMEX( ystart, self.Time, 
                              L = self.L_in, L_pre = self.L_pre,
                              bound_cond = self.bound_cond,
                              imex_method = 'cn',
                              iter_tol = self.iter_tol,
                              maxiter=self.maxiter  )
        Time_local = sempy.ode.Time(self.Time.Space,
                           start_time = 0.0,
                           end_time = 0.5*self.Time.h,
                           time_steps = self.explicit_steps)
        erk = sempy.ode.PRK( ystart,Time_local,
                             force_function = self.force_function, 
                             bound_cond = self.bound_cond,
                             prk_method='erk4')
        # -- Callback
        if not self.call_back == None: 
            self.call_back(self.y0, self.Time.time,0)
        #-- Time-stepping
        for i in range(self.Time.time_steps):
            local_time = self.Time.time
            h = self.Time.h
            # 1) Solve non-linear problem explicitly
            Time_local = sempy.ode.Time(self.Time.Space,
                           start_time = local_time,
                           end_time = local_time + 0.5*h,
                           time_steps = self.explicit_steps)
            erk.y0 = ystart
            erk.Time = Time_local
            yend = erk.solve()
            # 2) Solve linear problem implicitly
            #--BC
            Time_local = sempy.ode.Time(self.Time.Space,
                          start_time = local_time,
                          end_time = local_time + h,
                          time_steps = 1)
            irk.y0 = self.bound_cond(yend,local_time)
            irk.Time = Time_local
            ystart = irk.solve()
            # 3) Solve non-linear problem
            Time_local = sempy.ode.Time(self.Time.Space,
                           start_time = local_time+0.5*h,
                           end_time = local_time + h,
                           time_steps = self.explicit_steps)
            erk.y0 = self.bound_cond(ystart,local_time+0.5*h)
            erk.Time = Time_local
            yend = erk.solve()
            # Time increment
            self.Time.increment()
            ystart = yend
            print '--> Time step number: ', i+1,'time=',self.Time.time
            # -- Callback
            if not self.call_back == None:
                self.call_back(ystart,self.Time.time,i+1)
            
        return ystart
    
    