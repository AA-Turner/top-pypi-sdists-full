
import sempy
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
from matplotlib import rcParams
rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True
rcParams['legend.fontsize']=20

from pysparse.sparse.pysparseMatrix import PysparseMatrix


class Diffusion:
    '''
    Test case for the diffusion equation
    
    .. math::
    
       y=
       
    '''
    def __init__(self,Space,mu=None):
        self.Space = Space
        self.M = sempy.operators.Mass( self.Space ).matrix
        self.mu = mu
        self.f = sempy.Function( self.Space)
        if self.mu == None:
            self.mu = sempy.Function( self.Space, basis_coeff = 1.0)
        self.error = sempy.Function( self.Space )
        self.u = sempy.Function( self.Space)
        
    def initial_condition(self,y,t):
        #
        if self.Space.dim == 1:
            y_val = np.cos(t)*np.cos(2.0*np.pi*self.Space.x)
            
        if self.Space.dim == 2:
            y_val = np.cos(t)*np.cos(2.0*np.pi*self.Space.x)*\
                              np.cos(2.0*np.pi*self.Space.y)
        y.basis_coeff = np.copy( y_val )
        return y
    
    def force_function(self,y,t):
        #
        if self.Space.dim == 1:
            dudt  = -np.sin(t)*np.cos(2.0*np.pi*self.Space.x)
            dudx2 = -4.0*np.pi*np.pi*\
                     np.cos(t)*np.cos(2.0*np.pi*self.Space.x)
            self.f.basis_coeff = dudt - self.mu.basis_coeff*( dudx2  )
            
        if self.Space.dim == 2:
            dudt  = -np.sin(t)*np.cos(2.0*np.pi*self.Space.x)*\
                               np.cos(2.0*np.pi*self.Space.y)
            dudx2 = -4.0*np.pi*np.pi*np.cos(t)*\
                     np.cos(2.0*np.pi*self.Space.x)*\
                     np.cos(2.0*np.pi*self.Space.y)
            self.f.basis_coeff = dudt - self.mu.basis_coeff*( 2.0*dudx2  )
                
        b = self.M*self.f.glob()
        return [b]
        
    def bc(self,y,t):
        if self.Space.dim == 1:
            y_val = np.cos(t)*np.cos(2.0*np.pi*self.Space.x)
                
        if self.Space.dim == 2:
            y_val = np.cos(t)*np.cos(2.0*np.pi*self.Space.x)*\
                              np.cos(2.0*np.pi*self.Space.y)
        
        self.u.basis_coeff = self.Space.mapping_q( y )
        for i in range(1,5):
            self.u.set_bc(y_val,i)
            
        return self.u.glob()
    
    def error_norms( self, y, t ):
        # Error norms.
        y_ex = sempy.Function( self.Space )
        y_ex = self.initial_condition( y_ex, t )
        
        self.error.basis_coeff = y_ex.basis_coeff - y.basis_coeff
        e_L2=self.error.l2_norm()
        e_H1=self.error.h1_norm()
        print 'L2= ',e_L2
        print 'H1= ',e_H1  
        return e_L2,e_H1
    
    def plot_error(self):
        self.error.plot_wire()


class ConvectionDiffusion1d:
    '''
    Test case for the convection-diffusion equation.
    '''
    def __init__(self,Space,mu=None):
        self.Space = Space
        self.M = sempy.operators.Mass( self.Space ).matrix
        self.mu = mu
        self.f = sempy.Function( self.Space)
        if self.mu == None:
            self.mu = sempy.Function( self.Space, basis_coeff = 1.0)
        self.error = sempy.Function( self.Space )
        self.u = sempy.Function( self.Space)
        self.C = sempy.operators.Convection( self.Space ).matrix
            
    def initial_condition(self,y,t):
        y_val = np.exp(-4.0*np.pi*np.pi*self.mu.basis_coeff*t)*\
                np.sin(2.0*np.pi*(self.Space.x-t))
        y.basis_coeff = np.copy( y_val )
        return y
    
    def force_function(self,y,t):
        #dudt  = -np.sin(t)*\
        #         np.cos(2.0*np.pi*self.Space.x)#*\
        #         #np.cos(2.0*np.pi*self.Space.y)
        #dudx2 = -4.0*np.pi*np.pi*\
        #             np.cos(t)*\
        #             np.cos(2.0*np.pi*self.Space.x)#*\
        #             #np.cos(2.0*np.pi*self.Space.y)
        #self.f.basis_coeff = dudt - self.mu.basis_coeff*( 1.0*dudx2  )
        #b = self.M*self.f.glob()
        #b=np.zeros((self.Space.dof),float)
        b =  self.C * y[0].glob()
        b = -b
        return [b]
        
    def bc(self,y,t):
        #
        y_val = np.exp(-4.0*np.pi*np.pi*self.mu.basis_coeff*t)*\
                np.sin(2.0*np.pi*(self.Space.x-t))
        #self.u.basis_coeff = self.Space.mapping_q( y )
        for i in range(0,3):
            #self.u.set_bc(y_val,i)
            y[0].set_bc(y_val,i)
        return y#y[0]#self.u.glob()
    
    def error_norms( self, y, t ):
        # Error norms.
        y_ex = sempy.Function( self.Space )
        y_ex = self.initial_condition( y_ex, t )
        
        self.error.basis_coeff = y_ex.basis_coeff - y.basis_coeff
        e_L2=self.error.l2_norm()
        e_H1=self.error.h1_norm()
        print 'L2= ',e_L2
        print 'H1= ',e_H1  
        return e_L2,e_H1
    
    def plot_error(self):
        self.error.plot_wire()

class ConvectionDiffusion2d:
    '''
    Test case for the convection-diffusion equation.
    '''
    def __init__(self,Space,mu=None):
        self.Space = Space
        self.M = sempy.operators.Mass( self.Space ).matrix
        self.mu = mu
        self.f = sempy.Function( self.Space)
        if self.mu == None:
            self.mu = sempy.Function( self.Space, basis_coeff = 1.0)
        self.error = sempy.Function( self.Space )
        self.u = sempy.Function( self.Space)
        self.C = sempy.operators.Convection( self.Space ).matrix
            
    def initial_condition(self,u,t):
        x=self.Space.x
        y=self.Space.y
        u_val = -np.sin(np.pi*x)*np.cos(np.pi*y)*np.cos(np.pi*t)
        u.basis_coeff = np.copy( u_val )
        return u
    
    def force_function(self,y,t):
        #dudt  = -np.sin(t)*\
        #         np.cos(2.0*np.pi*self.Space.x)#*\
        #         #np.cos(2.0*np.pi*self.Space.y)
        #dudx2 = -4.0*np.pi*np.pi*\
        #             np.cos(t)*\
        #             np.cos(2.0*np.pi*self.Space.x)#*\
        #             #np.cos(2.0*np.pi*self.Space.y)
        #self.f.basis_coeff = dudt - self.mu.basis_coeff*( 1.0*dudx2  )
        #b = self.M*self.f.glob()
        #b=np.zeros((self.Space.dof),float)
        b =  self.C * y
        b = -b
        return [b]
        
    def bc(self,u,t):
        #
        #y_val = np.exp(-4.0*np.pi*np.pi*self.mu.basis_coeff*t)*\
        #        np.sin(2.0*np.pi*(self.Space.x-t))
        x=self.Space.x
        y=self.Space.y
        u_val = -np.sin(np.pi*x)*np.cos(np.pi*y)*np.cos(np.pi*t)
        #self.u.basis_coeff = self.Space.mapping_q( u_val )
        for i in range(0,3):
            self.u.set_bc(u_val,i)
        return self.u.glob()
    
    def error_norms( self, y, t ):
        # Error norms.
        y_ex = sempy.Function( self.Space )
        y_ex = self.initial_condition( y_ex, t )
        
        self.error.basis_coeff = y_ex.basis_coeff - y.basis_coeff
        e_L2=self.error.l2_norm()
        e_H1=self.error.h1_norm()
        print 'L2= ',e_L2
        print 'H1= ',e_H1  
        return e_L2,e_H1
    
    def plot_error(self):
        self.error.plot_wire()   


class TwoEqTest:
    '''
    Test case for the convection-diffusion equation.
    '''
    def __init__(self,Space,mu_1=None,mu_2=None):
        self.Space = Space
        self.M = sempy.operators.Mass( self.Space ).matrix
        self.mu_1 = mu_1
        self.mu_2 = mu_2
        if self.mu_1 == None:
            self.mu_1 = sempy.Function( self.Space, basis_coeff = 1.0)
        if self.mu_2 == None:
            self.mu_2 = sempy.Function( self.Space, basis_coeff = 1.0)
        self.f = sempy.Function( self.Space)
        self.error = [sempy.Function(self.Space),sempy.Function(self.Space)]
        #self.u = sempy.Function( self.Space)
        self.C = sempy.operators.Convection( self.Space ).matrix
        
    def linear_operator(self):
        lap_1 = sempy.operators.Laplacian( self.Space,fem_assemble='yes',
                                         mu=self.mu_1 )
        A_1 = lap_1.matrix
        A_1_fem= lap_1.matrix_fem
        
        lap_2 = sempy.operators.Laplacian( self.Space,fem_assemble='yes',
                                         mu=self.mu_2 )
        A_2 = lap_2.matrix
        A_2_fem= lap_2.matrix_fem
        
        B_1 = sempy.operators.MultipleOperators([A_1], [-1.0 ]).matrix
        B_1_fem = sempy.operators.MultipleOperators([A_1_fem], 
                                           [-1.0],
                                           assemble='yes').matrix
        B_2 = sempy.operators.MultipleOperators([A_2], [-1.0 ]).matrix
        B_2_fem = sempy.operators.MultipleOperators([A_2_fem], 
                                           [-1.0],
                                           assemble='yes').matrix
        E = PysparseMatrix(size=self.Space.dof)
                                    
        S = [[B_1, E],[E,   B_2]]
        S_fem = [[B_1_fem,E],[E,B_2_fem]]
        return S,S_fem
            
    def initial_condition(self,y,t):
        # Conv-diff eq
        y_val = np.exp(-4.0*np.pi*np.pi*self.mu_1.basis_coeff*t)*\
                np.sin(2.0*np.pi*(self.Space.x-t))
        y[0].basis_coeff = np.copy( y_val )
        # Diff eq
        y_val = np.cos(t)*np.cos(2.0*np.pi*self.Space.x)
        y[1].basis_coeff = np.copy( y_val )
        return y
    
    def force_function(self,y,t):
        # First
        b_1 =  self.C * y[0].glob()
        b_1 = -b_1
        # Second
        dudt  = -np.sin(t)*np.cos(2.0*np.pi*self.Space.x)
        dudx2 = -4.0*np.pi*np.pi*\
               np.cos(t)*np.cos(2.0*np.pi*self.Space.x)
        self.f.basis_coeff = dudt - self.mu_2.basis_coeff*( dudx2  )
        b_2 = self.M*self.f.glob()
        return [b_1,b_2]
        
    def bc(self,y,t):
        # First
        y_val = np.exp(-4.0*np.pi*np.pi*self.mu_1.basis_coeff*t)*\
                np.sin(2.0*np.pi*(self.Space.x-t))
        for i in range(0,3):
            y[0].set_bc(y_val,i)
        # Second
        y_val = np.cos(t)*np.cos(2.0*np.pi*self.Space.x)
        for i in range(0,3):
            y[1].set_bc(y_val,i)
        return y
    
    def error_norms( self, y, t ):
        # Error norms.
        y_ex = [sempy.Function(self.Space),sempy.Function(self.Space)]
        y_ex = self.initial_condition( y_ex, t )
        
        self.error[0].basis_coeff = y_ex[0].basis_coeff - y[0].basis_coeff
        self.error[1].basis_coeff = y_ex[1].basis_coeff - y[1].basis_coeff

        e1_L2 = self.error[0].l2_norm()
        e1_H1 = self.error[0].h1_norm()
        e2_L2 = self.error[1].l2_norm()
        e2_H1 = self.error[1].h1_norm()
        
        return e1_L2,e1_H1,e2_L2,e2_H1
    
    def plot_error(self,i):
        self.error[i].plot_wire()


class TwoEqHeat:
    '''
    Test case for the two-equation heat transfer model.
    '''
    def __init__(self,Space,gamma=None,eta=None,Pe=1.0,Time=None):
        self.Space = Space
        self.M = sempy.operators.Mass( self.Space ).matrix
        self.gamma = gamma
        self.eta = eta
        if self.gamma == None:
            self.gamma = sempy.Function( self.Space, basis_coeff = 1.0)
        if self.eta == None:
            self.eta = 1.0
        self.f = sempy.Function( self.Space)
        self.error = [sempy.Function(self.Space),sempy.Function(self.Space)]
        self.Pe=Pe
        u_conv = sempy.Function( self.Space, basis_coeff = self.Pe)
        self.conv = sempy.operators.Convection( self.Space, 
                                             u_conv=[u_conv] )
        self.C = self.conv.matrix
        # Plot of solution
        self.Time = Time
        if not self.Time==None:
            n_t = self.Time.time_steps+1
            t = np.zeros((n_t),float)
            h = self.Time.h
            for i in range(n_t):
                t[i]=np.float(i)*h
            #v = np.zeros((n_t,u.Space.dof),float)
            x = self.Space.local_to_global(self.Space.x)
            self.X=np.zeros((n_t,self.Space.dof),float)
            self.T=np.zeros((n_t,self.Space.dof),float)
            self.y1=np.zeros((n_t,self.Space.dof),float)
            self.y2=np.zeros((n_t,self.Space.dof),float)
            for i in range(n_t):
                self.X[i,:]=x[:]
                self.T[i,:]=t[i]
            
            
    def linear_operator(self):
        '''
        Linear operator
        '''
        # L_11
        lap_1 = sempy.operators.Laplacian( self.Space,fem_assemble='yes',
                                            mu=self.gamma )
        
        A_1 = lap_1.matrix
        A_1_fem= lap_1.matrix_fem
                
        L_11 = sempy.operators.MultipleOperators([A_1,self.M], 
                                                 [-1.0,-self.eta]).matrix
        L_11_fem = sempy.operators.MultipleOperators([A_1_fem,self.M], 
                                           [-1.0,-self.eta],
                                           assemble='yes').matrix
        # L_12
        L_12 = sempy.operators.MultipleOperators([self.M], [self.eta],
                                                 assemble='yes').matrix
        # L_21
        L_21 = sempy.operators.MultipleOperators([self.M], [self.eta],
                                                 assemble='yes').matrix
        # L_22
        lap_2 = sempy.operators.Laplacian(self.Space,fem_assemble='yes')
        A_2 = lap_2.matrix
        A_2_fem= lap_2.matrix_fem
        L_22 = sempy.operators.MultipleOperators([A_2,self.M], 
                                                 [-1.0,-self.eta]).matrix
        L_22_fem = sempy.operators.MultipleOperators([A_2_fem,self.M], 
                                           [-1.0,-self.eta],
                                           assemble='yes').matrix
        #                                    
        S = [[L_11, L_12],[L_21, L_22]]
        S_fem = [[L_11_fem,L_12],[L_21,L_22_fem]]
        return S,S_fem
            
    def initial_condition(self,y,t):
        # First
        x=self.Space.x
        y_val = np.exp(-t)*np.sin(2.0*np.pi*x)
        y[0].basis_coeff[:,:] = np.copy( y_val )
        # Second
        g1=(4.0*self.gamma.basis_coeff)*np.pi*np.pi + self.eta - 1.0
        g=(1.0/self.eta)*(g1*np.sin(2.0*np.pi*x)+\
                          2.0*np.pi*self.Pe*np.cos(2.0*np.pi*x))
        y_val=np.exp(-t)*g
        y[1].basis_coeff[:,:] = np.copy( y_val )
        return y
    
    def force_function(self,y,t):
        # First
        b_1 =  self.C * y[0].glob()
        b_1 = -b_1
        # Second
        x=self.Space.x
        g1=(4.0*self.gamma.basis_coeff)*np.pi*np.pi + self.eta - 1.0
        g=(1.0/self.eta)*(g1*np.sin(2.0*np.pi*x)+\
                          2.0*np.pi*self.Pe*np.cos(2.0*np.pi*x))
        Q=(4.0*np.pi*np.pi + self.eta - 1.0)*g - self.eta*np.sin(2.0*np.pi*x)
        f_val = np.exp(-t)*Q
        
        self.f.basis_coeff[:,:] = np.copy(f_val)
        b_2 = self.M*self.f.glob()
        return [b_1,b_2]
    
    def callback(self,y,t,i):
        # First
        y_ex = [sempy.Function(self.Space),sempy.Function(self.Space)]
        y_ex = self.initial_condition( y_ex, t )
        
        self.error[0].basis_coeff = y_ex[0].basis_coeff - y[0].basis_coeff
        self.error[1].basis_coeff = y_ex[1].basis_coeff - y[1].basis_coeff
        
        #self.y1[i,:]=y[0].glob()
        #self.y2[i,:]=y[1].glob()
        self.y1[i,:]=self.error[0].glob()
        self.y2[i,:]=self.error[1].glob()
        return
    
    def plot_evo(self):
        font_size = 20
        
        fig1 = plt.figure(1)
        ax1 = axes3d.Axes3D(fig1)
        #ax1.plot_wireframe(self.X,self.T, self.y1)
        #ax1.plot_surface(self.X,self.T, self.y1,
        #                 rstride=1, cstride=1, cmap=cm.jet,
        #                 linewidth=1, antialiased=False)
        ax1.plot_surface( self.X,self.T,self.y1,
                          color='b',alpha=1.0,rstride=1, cstride=1)
        # Dirk252, oifs2
        #ax1.set_zlim3d(-0.004,0.008)
        # Strang
        #ax1.set_zlim3d(-0.015,0.015)
        for label in ax1.w_xaxis.get_ticklabels():
            label.set_fontsize(18)
        for label in ax1.w_yaxis.get_ticklabels():
            label.set_fontsize(18)
        for label in ax1.w_zaxis.get_ticklabels():
            label.set_fontsize(18)
        ax1.set_xlabel(r'$x$',fontsize=font_size)
        ax1.set_ylabel(r'$t$',fontsize=font_size)
        ax1.set_zlabel(r'$e$',fontsize=font_size)
        
        fig2 = plt.figure(2)
        ax2 = axes3d.Axes3D(fig2)
        ax2.plot_surface( self.X,self.T,self.y2,
                          color='b',alpha=1.0,rstride=1, cstride=1)
        #ax2.set_zlim3d(-0.00006,0.00006)

        for label in ax2.w_xaxis.get_ticklabels():
            label.set_fontsize(12)
        for label in ax2.w_yaxis.get_ticklabels():
            label.set_fontsize(12)
        for label in ax2.w_zaxis.get_ticklabels():
            label.set_fontsize(12)
                
        ax2.set_xlabel(r'$x$',fontsize=font_size)
        ax2.set_ylabel(r'$t$',fontsize=font_size)
        ax2.set_zlabel(r'$e$',fontsize=font_size)
        
        
        plt.show()   
        
        
        
    def bc(self,y,t):
        # First
        #y_val = np.exp(-4.0*np.pi*np.pi*self.mu_1.basis_coeff*t)*\
        #        np.sin(2.0*np.pi*(self.Space.x-t))
        self.error = self.initial_condition( self.error, t )
        #y_val=0.0
        for i in range(0,3):
            y[0].set_bc(self.error[0].basis_coeff,i)
        # Second
        #y_val = np.cos(t)*np.cos(2.0*np.pi*self.Space.x)
        #y_val=0.0
        for i in range(0,3):
            y[1].set_bc(self.error[1].basis_coeff,i)
        return y
    
    def error_norms( self, y, t ):
        # Error norms.
        y_ex = [sempy.Function(self.Space),sempy.Function(self.Space)]
        y_ex = self.initial_condition( y_ex, t )
        
        self.error[0].basis_coeff = y_ex[0].basis_coeff - y[0].basis_coeff
        self.error[1].basis_coeff = y_ex[1].basis_coeff - y[1].basis_coeff

        e1_L2 = self.error[0].l2_norm()
        e1_H1 = self.error[0].h1_norm()
        e2_L2 = self.error[1].l2_norm()
        e2_H1 = self.error[1].h1_norm()
        
        return e1_L2,e1_H1,e2_L2,e2_H1
    
    def plot_error(self):
        self.error[0].plot_wire(show=False)
        self.error[1].plot_wire(show=True)