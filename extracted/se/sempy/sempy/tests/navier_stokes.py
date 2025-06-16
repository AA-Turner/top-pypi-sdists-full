
import sempy
import numpy as np
import matplotlib.pyplot as plt



class NStest:
    '''
    Test case. 
    '''
    def __init__( self, Space, SpaceGL, Time):
        #
        self.Space = Space
        self.SpaceGL = SpaceGL
        self.Time = Time
        self.err_p = sempy.Function( self.SpaceGL )
        self.err_u = sempy.VectorFunction( self.Space )
        
    
    def ic(self,u,p,t):
        #
        x=self.Space.x
        y=self.Space.y
        
        x_gl=self.SpaceGL.x
        y_gl=self.SpaceGL.y
        
        u[0].basis_coeff = -np.cos(x)*np.sin(y)*np.exp(-2.0*t)
        u[1].basis_coeff =  np.sin(x)*np.cos(y)*np.exp(-2.0*t)
        p.basis_coeff = -0.25*(np.cos(2.0*x_gl) + np.cos(2.0*y_gl))*\
                         np.exp(-4.0*t)
        return u
    
    def error_norms( self, u, p, t ):
        # Error norms.
        u_ex = sempy.VectorFunction( self.Space )
        p_ex = sempy.Function( self.SpaceGL )
        
        self.ic( u_ex, p_ex, t )
        #p_ex.plot_wire()
        
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
                
        #return self.err_u[0].l2_norm(), self.err_u[1].l2_norm(),\
        #       self.err_p.l2_norm(),\
        #       u_infty, v_infty, p_infty,self.err_p.h1_norm()
                   
    def bc( self, u, T, t ):
        #
        x=self.Space.x
        y=self.Space.y
        U = -np.cos(x)*np.sin(y)*np.exp(-2.0*t)
        V =  np.sin(x)*np.cos(y)*np.exp(-2.0*t)
        
        for i in range(5):
            u[0].set_bc( U, i )
            u[1].set_bc( V, i )
        
        return
    
  
 