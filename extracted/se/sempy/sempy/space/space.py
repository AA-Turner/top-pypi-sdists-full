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
import sempy.space.one_d.gmsh1D as mesh1d
import sempy.space.two_d.gmsh2D as mesh2d
import sempy.space.three_d.gmsh3D as mesh3d

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
from matplotlib import rcParams
rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True

import os,sys
import sempy.space.mesh_lib as mesh_lib

class Space:
    '''
    
    This class represents the implementation of the discrete space :math:`X_N`
    
    .. math::
    
       X_N\subset X & = H^1(\Omega)
       
       X_N &= \{v\in H^1(\Omega)\ |\ v|_{\Omega^k}\circ\mathcal F  \in\mathbb P_N(\hat\Omega),\ 
             k=0,\ldots, \\text{NOE}-1 \}
    
    where :math:`\Omega\in\mathbb R^d` is the computational domain and 
    :math:`\hat\Omega` is the reference domain.          
    An instance is created based on a Gmsh .msh file and 
    the chosen polynomial degree, :math:`N=n-1`. 
    
     
    
    :param filename: This is typically a Gmsh file with format extension 
                     *.msh*. However, :mod:`sempy` is shipped with a few 
                     ready to use meshes such as 
                     :literal:`line` for one dimensional problems, 
                     :literal:`square` for two dimensional problems and
                     :literal:`cube` for three dimensional problems.
    :type filename: string 
    :param n: Number of nodal points in each direction of an element. 
              Hence, the polynomial degree of the basis functions 
              is :math:`N=n-1`.
    :type n: int
    :param dim: Dimension :math:`d` of the computational domain 
                :math:`\Omega\in\mathbb R^d`. 
    :type dim: int
    
                     
    :attributes: * **noe** (*int*) - Number of spectral elements. 
                 * **noe_bc** (*int*) - Number of boundary elements. 
                 * **dof** (*int*) - Global degrees of freedom. 
                 * **points** (*array*) - GLL quadrature points 
                   :math:`\\underline{\\xi}\\in\\mathbb R^{N+1},\\ -1\\le \\xi_j\\le 1`.
                 * **weights** (*array*) - GLL quadrature weights 
                   :math:`\\underline{\\rho}\\in\\mathbb R^{N+1}` 
                   corresponding to the points :math:`\\underline{\\xi}`. 
                   Used to evaluate an integral over the reference domain, 
                   e.g.:
                 
                   .. math::
                      \\hat\\Omega\\in\\mathbb R^1: \\int_{\\hat\\Omega} f d\\hat\\Omega\\approx
                      \\sum_i\\rho_if_i
                      
                      \\hat\\Omega\\in\\mathbb R^2: \\int_{\\hat\\Omega} f d\\hat\\Omega\\approx
                      \\sum_i\\sum_j\\rho_i\\rho_jf_{ij}
                      
                 * **D** (*array*) - GLL derivative matrix 
                   :math:`\\underline D\\in\\mathbb R^{(N+1)\\times (N+1)}`. For a 1D problem:
    
                   .. math::
                      u_N'(\\xi_j)=\\sum_i l_i'(\\xi_j) u_i=\\sum_i D_{ji}u_i\\Rightarrow
                      D_{ji}=l_i'(\\xi_j)
                 
                 * **x,y,z** (*array*) - Coordinate arrays (given in local 
                   data distribution). 
                 * **jac** (*array*) - The Jacobian :math:`|\\underline{J}|`.
                 * **jac_s** (*array*) - The surface Jacobian 
                   :math:`|\\underline{J}^s|`. 
                 * **n_unit** (*array*) - Surface unit normal vector.
                 
                 
    **Example**::
    
       >>> import sempy
       >>> X_N = sempy.Space( filename = 'square', n = 3, dim = 2 )
       <BLANKLINE>
       **** Creating Space object     ****
       **** dim = 2
       **** noe = 84
       **** dof = 361
       ****   n = 3
       **** Finished creating instance.

       

             
    '''
    def __init__(self,filename, n, dim = 1):
        self.n = n
        self.dim = dim
        self.type = 'GLL'
        
        if dim == 1:
            if filename == 'line':
                path = os.path.dirname(mesh_lib.__file__)
                file_line = path+'/gmsh/line.msh'
                filename = file_line
            self._MeshD = mesh1d.MeshObject1D(filename,n,n_gmsh=3)
            self.x = self._MeshD.x 
            
        if dim == 2:
            if filename == 'square':
                path = os.path.dirname(mesh_lib.__file__)
                file_square = path+'/gmsh/square.msh'
                filename = file_square
            if filename == 'square_neumann':
                path = os.path.dirname(mesh_lib.__file__)
                file_square = path+'/gmsh/square_neumann.msh'
                filename = file_square
                #print '--filename=',filename

            self._MeshD = mesh2d.MeshObject2D(filename,n,n_gmsh=3)
            self.x, self.y=self._MeshD.x, self._MeshD.y
            self.z =  np.zeros((self._MeshD.noe, self.n,self.n),int)
            self.n_x = self._MeshD.n_x 
            self.n_y = self._MeshD.n_y
            
            self.n_unit  = np.zeros( (2,self._MeshD.noe_bc, self._MeshD.n),
                                      float)
            self.n_unit[0] = self._MeshD.n_x
            self.n_unit[1] = self._MeshD.n_y
        
        if dim == 3:
            if filename == 'cube':
                path = os.path.dirname(mesh_lib.__file__)
                file_square = path+'/gmsh/cube.msh'
                filename = file_square
            self._MeshD = mesh3d.MeshObject3D(filename,n)
            self.x, self.y, self.z = self._MeshD.x, self._MeshD.y,\
                                     self._MeshD.z
            
        self.physical = self._MeshD.physical
        
        self.noe = self._MeshD.noe
        self.noe_bc = self._MeshD.noe_bc
        self.dof = self._MeshD.dof
        self.weights = self._MeshD.weights
        self.points =self._MeshD.points
        self.D = self._MeshD.D
        self.jac = self._MeshD.jac
        
        self.jac_s = self._MeshD.jac_s
        self.theta = self._MeshD.theta
        self.theta_bc = self._MeshD.theta_bc
        self.bc_type = self._MeshD.bc_type
        
        self.fem = sempy.precond.SpaceFEM( self )
    
    def plot_mesh(self):
        '''
        Plots the computational mesh including type of boundary conditions. 
        Red circles indicate Dirichlet boundary conditions and green 
        circles indicate natural boundary conditions. 
        '''
        self._MeshD.plot_mesh()
        
    def plot_domain(self,font_size=20,show=True):
        '''Plot mesh.'''
        fig_number = np.random.randint(102,201)
        fig = plt.figure(fig_number) 
        if self.dim==2:
            thickness = 0.5
            n=self.n
            for k in range(self.noe):
                #for m in range(n):
                for i in range(n):
                    plt.plot(self.x[k,:,i],self.y[k,:,i],
                             color='k',linewidth=thickness)
                    #plt.plot(self.x[k,:,n-1],self.y[k,:,n-1],
                    #   color='k',linewidth=thickness)
                    plt.plot(self.x[k,i,:],self.y[k,i,:],
                             color='k',linewidth=thickness)
                    #plt.plot(self.x[k,n-1,:],self.y[k,n-1,:],
                    #  color='k',linewidth=thickness)
            plt.xlabel(r'$x$', fontsize = font_size )
            plt.ylabel(r'$y$', fontsize = font_size )
            plt.axis([self.x.min(),self.x.max(),self.y.min(),self.y.max()])
            plt.axes().set_aspect('equal')
            ax = plt.gca()
            for label in ax.xaxis.get_ticklabels():
                label.set_fontsize( font_size )
            for label in ax.yaxis.get_ticklabels():
                label.set_fontsize( font_size )
            if show:
                plt.show()
            
    def plot_scalar(self, u, n_int = 0):
        '''
        Plots a scalar :math:`u(x)`. 
        '''
        self._MeshD.plot_scalar(u, n_int)
        
    def plot_basis_function(self,i=0,show=True,font_size=20):
        '''
        Plots the :math:`i`'th basis function. 
        
        :param i: Global node number, :math:`i\in\{0,\ldots,\\text{DOF}-1\}`. 
        '''
        print 'show=',show
        self._MeshD.plot_basis_function(i,show=show,font_size=font_size)
        
    def mapping_q(self,v):
        '''
        The action of the mapping operator :math:`Q` on a vector :math:`v`.
        
        :param array v: Basis coefficients in global data representation.
        :returns: Basis coefficients in local data representation
        
        This method maps a vector of global ordering to a local data 
        representation. This operator is used in the assembly or the action 
        of a global matrix on a vector,
        
        .. math::
           \underline w=\underline  Q^T\underline A_L\underline Q\underline v=\underline A\,\underline v
           
        where :math:`\underline A_L` is e.g. the local Laplacian or the local mass matrix. 
        
        The matrix-vector product 
        :math:`\underline v_{local}=\underline Q\underline v_{global}` 
        can be achieved as follows::
           
           import sempy
           import numpy as np
           
           X = sempy.Space( filename = 'square', n = 5, dim = 2 )      

           u_global = np.ones( ( X.dof ) , float )
           u_local = X.mapping_q( u_global )
        
        '''
        return self._MeshD.mapping_q(v)
        
    def mapping_qt(self,u):
        '''
        The action of the transpose :math:`Q^T` of the mapping operator 
        :math:`Q`. 
        
        :param array u: Basis coefficients in local data representation.
        :returns: Basis coefficients in global data representation 
        
        This method maps an array of local ordering to a global data 
        representation. Also known as the gather operation. The matrix 
        vector product :math:`v_{global}=Q^Tv_{local}` is performed 
        by typing::
        
           import sempy
           import numpy as np

           X = sempy.Space( filename = 'square', n = 5, dim = 2 )      
    
           u_local = np.ones( ( X.noe, X.n, X.n ), float )
           u_global= X.mapping_qt( u_local )
        
        '''
        return self._MeshD.mapping_qt(u)
        
    def local_to_global(self,u):
        '''
        Maps the basis coefficients of a function 
        :math:`u\in H^1(\Omega)` from local to global 
        data representation.
        
        :param array u: Basis coefficients in local data representation.
        :returns: Basis coefficients in global data representation
        
        Usage::
           
           import sempy
           
           X = sempy.Space( filename = 'square', n = 5, dim = 2 )
           
           u = sempy.Function( X, basis_coeff =1.0 )
           
           u_global = X.local_to_global( u.basis_coeff )
           
        '''
        return self._MeshD.local_to_global(u)
    
    def mask(self,w):
        '''
        This method masks nodal point values associated with Dirichlet 
        boundary conditions.
        
        :param array w: Basis coefficients in global data representation 
                  subject to masking.
        :returns: Masked basis coefficients in global data representation.
        
        '''
        return self._MeshD.mask(w)
        
    def mask_matrix(self,A):
        '''
        This method masks entries in a matrix associated with Dirichlet 
        boundary conditions.
        
        :param A: Matrix subject to masking.
        :type A: PysparseMatrix
        :returns: The masked matrix.
        
        '''
        return self._MeshD.mask_matrix(A)
        
    def boundary_value(self,u):
        return self._MeshD.boundary_value(u)
        
    def l2_norm(self,u):
        '''
        Computes the :math:`L^2(\Omega)` - norm
           
        .. math::
           ||u||_{L^2(\\Omega)}=\\bigg(\\int_{\\Omega} u^2d\\Omega\\bigg)^{1/2}
              
        using GLL quadrature. 
           
        :param array u: Basis coefficients in global data structure, i.e. 
                        :math:`u\\in\\mathbb R^{dof}` .
        :returns: The :math:`L^2` - norm as a floating number.
                   
        Usage::
           
             import sempy
             
             X = sempy.Space( filename = 'square', n = 5, dim = 2 )      
             u = np.ones( ( X.dof ), float )
             print 'L2-norm=',X.l2_norm( u )
        '''
        return self._MeshD.l2_norm(u)
        
    def quadrature(self,f):
        '''
        Computes the value :math:`\\kappa` of the integral 
        
        .. math::
           \\kappa = \\int_\\Omega f\\,d\\Omega 
           
        for :math:`f\\in L^2(\\Omega)` with GLL quadrature rules. 
        
        :param array f: Basis coefficients of the function to be integrated 
                        given in local data representation 
                        (since :math:`f\\in L^2(\\Omega)`). 
        :returns: Value :math:`\\kappa` of the integral.
        
        Usage::
           
             import sempy
             X = sempy.Space( filename = 'square', n = 5, dim = 2 )
    
             u = sempy.Function( X, basis_coeff = X.x ) 
             kappa = X.quadrature( u.basis_coeff )
        '''
        return self._MeshD.quadrature(f)
    
    def theta_phys(self, *arguments):
        '''
        Local to global connectivity method. Takes as input the local node 
        description and returns the global node number and the physical name 
        of the element. 

        :arguments: Local node number. 
        :returns: * **i** (*int*)- Global node number. 
                  * **phys** (*int*) - Physical name.         
           
             
        A two dimensional example::
        
            import sempy
            
            X = sempy.Space( filename = 'square', n = 2, dim = 2 )
    
            for k in range( X.noe ):
                for m in range( X.n ):
                    for n in range( X.n ):
                        i, phys = X.theta_phys(k,m,n)
                        print '(k,m,n)=(',k,m,n,') i=',i
           
        
        '''
        return self._MeshD.theta_phys(*arguments)
        
    def theta_phys_bc(self, *arguments):
        '''
        Local to global connectivity method for boundary points. 
        
        .. Takes as input the local node 
           description and returns the global node number and the physical 
           name of the element. 
        
        
        :arguments: Local boundary node number. For 1D (k), for 2D (k,m) and for 3D (k,m,n). (k[,m[,n]])
        :returns: * **i** (*int*) - Global node number. 
                  * **phys** (*int*) - Physical name.
                  * **bc_type** (*string*) - Type of boundary condition,
                    e.g. "Dir" or "Neu", as specified in the Gmsh .geo file. 
                  * **element_edge** (*array*) - Holds the edge number 
                    and element number. 
        
        This routine can be used to apply boundary conditions. Note however 
        that the :class:`Function` class has easier ways of 
        dealing with this issue. 
        
        For example, for a 2D problem::
        
             import sempy
             
             X = sempy.Space( filename = 'square', n = 2, dim = 2 )
             u = sempy.Function( X, basis_coeff = 0.0 )
    
             u_global = u.glob()
             u_dirichlet = 10.0
             
             for k in range( X.noe_bc ): # Loops over the boundary elements.
                for m in range( X.n ):
                   [ i, phys, bc_type, edge ] = X.theta_phys_bc( k, m )
                   if bc_type=='Dir': # Assign BC value
                      u_global[i] = u_dirichlet
                
             u.basis_coeff = X.mapping_q( u_global )
             u.plot_wire()
                          
        '''
        return self._MeshD.theta_phys_bc(*arguments)
        
    def interpolation(self,u_N,m):
        '''
        Action of the interpolation operator :math:`I_N^M`
        
        .. math::
        
           u=I_N^M u_N
           
        where :math:`M=m-1`. 
        
        :param array u_N: Basis coefficients of the function 
                          to be interpolated.
        :type u_N: array 
        :param m: Number of nodal points in each elemental direction.
        :type m: int
        :returns: Basis coefficients of the interpolated function 
                  of polynomial degree :math:`M=m-1`. 
        
        Usage::
        
           import sempy
    
           X = sempy.Space( filename = 'square', n = 5, dim = 2 )
    
           u = sempy.Function( X, basis_coeff = X.x )
           u_int = X.interpolation( u.basis_coeff, 2 )
           u_new = X.interpolation( u_int, X.n )
           u.set_value( u_new )
           u.plot_wire()
        '''
        return self._MeshD.interpolation(u_N,m)
        
    def hyper_filter(self,u_tilde,alpha=0.25):
        '''
        A filter for hyperbolic problems (see Deville et al.). 
        
        .. math::
           u = F_\\alpha \\tilde u
           
        where the filter is
        
        .. math::
           F_\\alpha := \\alpha \\Pi_{N-1} + (1-\\alpha) I_N^N,\quad 
           \\Pi_{N-1} = I_{N-1}^N I_{N}^{N-1}
           
        Here, the weighting factor :math:`\\alpha` is typically in the 
        range :math:`0.05<\\alpha<0.3`. 
           
        :param array u_tilde: Basis coefficients of the function to 
                              be filtered. 
        :param float alpha: Weighting factor.
        :returns: Filtered basis coefficients. 
        '''
        return self._MeshD.hyper_filter(u_tilde,alpha)
        
    def gradient_vector(self,u):
        '''
        Computes the gradient vector of :math:`u`, i.e
        
        
        .. math::
        
           \\text{1D}:\quad \\nabla u= \partial u/\partial x
           
           \\text{2D}:\quad \\nabla u= (\partial u/\partial x,\partial u/\partial y)^T
           
           \\text{3D}:\quad \\nabla u= (\partial u/\partial x,\partial u/\partial y,\partial u/\partial z)^T
           
        :param u: The function to be differentiated
        :returns: The components of the gradient vector. 
        
        Usage::
          
          import sempy
    
          X = sempy.Space( filename = 'square', n = 5, dim = 2 )
    
          u = sempy.Function( X, basis_coeff = X.x * X.x )          
          u_x,u_y = X.gradient_vector(u.basis_coeff)
        
        '''
        return self._MeshD.gradient_vector( u )
        
    def surface_unit_normal(self):
        return self._MeshD.surface_unit_normal()
        
    def surface_flux(self,u):
        return self._MeshD.surface_flux(u)
 


def bc_function(Space,value=[0.0], bctype=[1]):
    g = np.zeros((Space.noe_bc, Space.n),float)
        
    if len(value) < len(bctype) or len(value) > len(bctype):
        print '---> Error in bc_function. len(value) does not equal len(bctype)'
        print '---> For example: value = [1.0, 2.0], bctype = [1,2]'
        #return 
    
    val    = np.zeros((len(value),Space.noe, Space.n, Space.n),float)
    val_bc = np.zeros((len(value),Space.noe_bc, Space.n),float)
    for j in range(len(value)):
        val[j][:,:,:] = value[j]
        val_bc[j] = Space.boundary_value(val[j])
        
    for j in range(len(value)):
        for k in range(Space.noe_bc):
            for m in range(Space.n):
                i, phys, bc_type, element_edge = Space.theta_phys_bc(k,m)
                if phys == bctype[j]:
                    g[k,m] = val_bc[j][k,m]
    return g
    
'''
class BoundaryFunction:
'''
    #BC.
'''
    def __init__(self,Space,value=[0.0], bctype=[1]):
        self.Space = Space
        self.coeff = np.zeros((self.Space.noe_bc, \
                               self.Space.n),float)
        
        if len(value) < len(bctype) or len(value) > len(bctype):
            print '---> Error in bc_function. len(value) does not equal len(bctype)'
            print '---> For example: value = [1.0, 2.0], bctype = [1,2]'
            #return 
    
        val    = np.zeros((len(value),self.Space.noe, \
                          self.Space.n, self.Space.n),float)
        val_bc = np.zeros((len(value),self.Space.noe_bc, \
                           self.Space.n),float)
        for j in range(len(value)):
            val[j][:,:,:] = value[j]
            val_bc[j] = self.Space.boundary_value(val[j])
        
        for j in range(len(value)):
            for k in range(self.Space.noe_bc):
                 for m in range(self.Space.n):
                    i, phys, bc_type, element_edge = self.Space.theta_phys_bc(k,m)
                    if phys == bctype[j]:
                        self.coeff[k,m] = val_bc[j][k,m]
                        #self.__setitem__[k,m] = val_bc[j][k,m]
                        #self.__setitem([k,m],val_bc[j][k,m])
        #return self.g
    #def __setitem__(self,key,value):
    #    self[key]=value
        
        
        
    def plot(self):
        
        x_bc = self.Space.boundary_value(self.Space.x)
        y_bc = self.Space.boundary_value(self.Space.y)
        u = np.zeros((self.Space.noe, self.Space.n,self.Space.n),float)
        
        for k in range(self.Space.noe_bc):
            for m in range(self.Space.n):
                [i, phys, bc_type, element_edge] = self.Space.theta_phys_bc(k,m)
                k_element = element_edge[0]
                if element_edge[1] == int(0):
                    u[k_element,m,0] = self.coeff[k,m]
                if element_edge[1] == int(1):
                    u[k_element,m,self.n-1] = self.coeff[k,m]
                if element_edge[1] == int(2):
                    u[k_element,0,m] = self.coeff[k,m]
                if element_edge[1] == int(3):
                    u[k_element,self.n-1,m] = self.coeff[k,m]
                    
        fig = plt.figure()
        ax = axes3d.Axes3D(fig)
        for k in range(self.Space.noe):
            ax.plot_wireframe(self.Space.x[k,:,:],self.Space.y[k,:,:],u[k,:,:])
        plt.show()
'''
                

class BoundaryFunction:
    '''
    Creates a function in the discrete space restricted to the boundary 
    :math:`\Gamma` of the computational domain :math:`\Omega`. 
    
    .. .. math::
       Y_N=\{v\in L^2(\Omega)\ |\ v|_{\Omega^k}\in\mathbb P_N(\Omega^k),\ 
             k=0,\ldots, \\text{NOE}-1 \}
    
    :param Space: The function space.
    :type Space: :class:`sempy.Space`
    :param array basis_coeff: Basis coefficients
    
    This class can be used in concert with the class 
    :class:`sempy.operators.Laplacian` to set Neumann and Robin 
    boundary conditions. It can be noted that the values of the *basis_coeff* 
    associated with Dirichlet conditions are masked. 
    
    **Example**::
    
       import sempy
      
       X = sempy.Space( 'square_neumann', n = 6, dim = 2 )
       u_gamma = sempy.BoundaryFunction( X )
       u_gamma.set_value( value = 3.0, physical_boundary = 2 )
      
    '''
    def __init__(self, Space,mask='yes'):
        self.Space = Space
        self.mask = mask
        if self.Space.dim == 1:
            self.basis_coeff =  np.zeros((self.Space.noe_bc),float)
            self.basis_coeff[:] = 0.0
            
        if self.Space.dim == 2:
            self.basis_coeff =  np.zeros((self.Space.noe_bc, \
                                          self.Space.n),float)
            self.basis_coeff[:,:] = 0.0
        
        if self.Space.dim == 3:
            self.basis_coeff =  np.zeros((self.Space.noe_bc, \
                                          self.Space.n,self.Space.n),float)
            self.basis_coeff[:,:,:] = 0.0
            
    def set_value(self,value,physical_boundary):
        '''
        Asigns *value* to the basis coefficients of the :class:`BoundaryFunction`. 
        
        :param value: Value to be assigned to the given boundary.
        :type value: Numpy array or floating point
        :param physical_boundary: Index of the physical boundary.
        :type physical_boundary: Integer
        '''
        
        if self.Space.dim == 1:
            val = np.zeros((self.Space.noe, self.Space.n),float)
            val[:,:] = value
            val_global = self.Space.local_to_global(val)
            #print 'obbs: check set_value in class BoundaryFunction'
            if self.mask == 'yes':
                val_global = self.Space.mask(val_global)
    
            for k in range(self.Space.noe_bc):
                [i, phys, bc_type, element_edge] = self.Space.theta_phys_bc(k)
                if phys == physical_boundary:
                    self.basis_coeff[k] = val_global[i]
                            
        if self.Space.dim == 2:
            val = np.zeros((self.Space.noe, self.Space.n, \
                            self.Space.n),float)
            val[:,:,:] = value
            val_global = self.Space.local_to_global(val)
            if self.mask == 'yes':
                val_global = self.Space.mask(val_global)
        
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n):
                    [i, phys, bc_type, element_edge] = self.Space.theta_phys_bc(k,m)
                    #print 'phys=',phys
                    #print 'physical_boundary=',physical_boundary
                    if phys == np.int(physical_boundary):
                        self.basis_coeff[k,m] = val_global[i]
                        
        if self.Space.dim == 3:
            val = np.zeros((self.Space.noe, self.Space.n, \
                            self.Space.n, self.Space.n),float)
            val[:,:,:,:] = value
            val_global = self.Space.local_to_global(val)
            if self.mask == 'yes':
                val_global = self.Space.mask(val_global)
        
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n):
                    for n in range(self.Space.n):
                        [i, phys, bc_type, element_edge] = self.Space.theta_phys_bc(k,m,n)
                        if phys == physical_boundary:
                            self.basis_coeff[k,m,n] = val_global[i]
        
    
        
class Function:
    '''
    An instance of this class represents a function in the discrete space.  
    
    .. .. math::
       X_N=\{v\in H^1(\Omega)\ |\ v|_{\Omega^k}\in\mathbb P_N(\Omega^k),\ 
             k=0,\ldots, \\text{NOE}-1 \}
             
       Y_N =\{ q\in L^2(\Omega)\ |\ q|_{\Omega^k}\in\mathbb P_N(\Omega^k),\ 
             k=0,\ldots, \\text{NOE}-1 \}
             
          
    :param Space: The function space.
    :type Space: :class:`sempy.Space`, :class:`sempy.precond.SpaceFEM` or
                 :class:`sempy.fluid.SpaceGL` 
    :param array basis_coeff: Basis coefficients of the function in local data 
                        representation.  
    :param string filename: The name of a file to dump data. 
    
    A function :math:`v` is defined as:
            
    .. math::
    
       \\forall v\in X_N,\quad v(\mathbf x)= 
       \sum_{i=0}^{\\text{dof}-1}\phi_i(\mathbf x)v_i
       
    where :math:`v_i` are the basis coefficients in global data 
    representation and the basis functions 
    :math:`\underline\phi\in\mathbb R^{\\text{dof}}` 
    have the property:
    
    .. math::
       \phi_j(\mathbf x_i)=\delta_{ij}
       
    In a local data structure the function is represented as:
    
    .. math::
       1D:&\quad v(\\xi)|_{\Omega^k}=\sum_{m=0}^N l_m(\\xi)v_{km}
       
       2D:&\quad v(\\xi,\\eta)|_{\Omega^k}=\sum_{m=0}^N \sum_{n=0}^N
                                          l_m(\\xi) l_n(\\eta) v_{kmn}
       
       3D:&\quad v(\\xi,\\eta,\\zeta)|_{\Omega^k}=\sum_{m=0}^N \sum_{n=0}^N\sum_{o=0}^N
                                          l_m(\\xi) l_n(\\eta) l_o(\\zeta)v_{kmno}
    
    **Example**::
    
      import sempy
      
      X = sempy.Space( 'square',n = 3, dim = 2 )
      u = sempy.Function( X, basis_coeff = X.x * X.x )
      
    '''
    def __init__( self, Space, basis_coeff = 0.0, 
                  filename = None, time = 0.0 ):
        
        self.Space = Space
        self.filename = filename
        self.file_count = 0
        self.time = time
               
        if self.Space.dim == 1:
            self.basis_coeff =  np.zeros((self.Space.noe, self.Space.n),
                                          float)
            self.basis_coeff[:,:] = basis_coeff
                        
        if self.Space.dim == 2:
            self.basis_coeff =  np.zeros((self.Space.noe, self.Space.n, 
                                          self.Space.n),float)
            self.basis_coeff[:,:,:] = basis_coeff
            
        if self.Space.dim == 3:
            self.basis_coeff =  np.zeros((self.Space.noe, self.Space.n, 
                                          self.Space.n, self.Space.n),float)
            self.basis_coeff[:,:,:,:] = basis_coeff
           
    #def at_boundary(self):
    #    '''
    #    Value at the boundary.
    #    '''
    #    return self.Space.boundary_value(self.coeff)
    def increment(self,h):
        """
        Increments the :attr:`sempy.Function.time` 
        attribute with :literal:`h`.

        >>> u.increment(0.1)

        """
        self.time += h
            
    def set_bc(self,value,physical_boundary):
        '''
        Sets the values of the Dirichlet boundary condition.
        
        :param value: The value to be assigned to the boundary. If 
                      :literal:`value` is given as an array it has to be 
                      given in local data representation. 
        :type value: array or floating point
        :param physical_boundary: The part of the boundary to recieve the value. 
        :type physical_boundary: integer
        
        Usage::
        
          import sempy
      
          X = sempy.Space( 'square', n = 3, dim = 2)
          u = sempy.Function( X, basis_coeff = X.x * X.x )
    
          u.set_bc( 1.0, 1 )
          u.set_bc( 1.0, 2 )
          u.plot_wire()
        '''
        if self.Space.type == 'GL':
            print 'Warning: cannot assign strong BC to a function in SpaceGL'
            return
        
        if self.Space.dim == 1:
            val = np.zeros((self.Space.noe, self.Space.n),float)
            val[:,:] = value
            val_global = self.Space.local_to_global(val)
            coeff_global = self.Space.local_to_global(self.basis_coeff)
        
            for k in range(self.Space.noe_bc):
                [i, phys, bc_type, element_edge] = self.Space.theta_phys_bc(k)
                if phys == physical_boundary:
                    coeff_global[i] = val_global[i]
                        
        if self.Space.dim == 2:
            val = np.zeros((self.Space.noe, self.Space.n, self.Space.n),float)
            val[:,:,:] = value
            val_global = self.Space.local_to_global(val)
            coeff_global = self.Space.local_to_global(self.basis_coeff)
        
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n):
                    [i, phys, bc_type, element_edge] = self.Space.theta_phys_bc(k,m)
                    if phys == physical_boundary:
                        coeff_global[i] = val_global[i]
        
        if self.Space.dim == 3:
            val = np.zeros((self.Space.noe, self.Space.n, self.Space.n, self.Space.n),float)
            val[:,:,:,:] = value
            val_global = self.Space.local_to_global(val)
            coeff_global = self.Space.local_to_global(self.basis_coeff)
        
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n):
                    for n in range(self.Space.n):
                        [i, phys, bc_type, element_edge] = self.Space.theta_phys_bc(k,m,n)
                        if phys == physical_boundary:
                            coeff_global[i] = val_global[i]
                        
        self.basis_coeff = self.Space.mapping_q(coeff_global)
    
    def set_value(self,value,physical_domain='none'):
        '''
        Assigns values to the basis coefficients. 
        
        :param value: Value to be assigned to the basis coefficients. 
        :type value: array or a floating number
        :param physical_domain: The index number of the physical domain, as 
                                given in the Gmsh geo file, 
                                to recieve the value. 
                                The default value is *none* in which the 
                                whole domain recieves the value. 
        :type physical_domain: integer
        
        Usage::
        
           import sempy
      
           X = sempy.Space( 'square', n = 3, dim = 2 )
           u = sempy.Function( X )
    
           u.set_value( 4.0 )
           u.plot_wire()
        
        '''
        if self.Space.dim == 1:
            val = np.zeros((self.Space.noe, self.Space.n),float)
            val[:,:] = value
            if physical_domain == 'none':
                self.basis_coeff[:,:]=val[:,:]
            else:
                for k in range(self.Space.noe):
                    i,phys=self.Space.theta_phys(k,0)
                    if phys == physical_domain:
                        self.basis_coeff[k,:]=val[k,:]
                        
        if self.Space.dim == 2:
            val = np.zeros((self.Space.noe, self.Space.n, self.Space.n),float)
            val[:,:,:] = value
            if physical_domain == 'none':
                self.basis_coeff[:,:,:]=val[:,:,:]
            else:
                for k in range(self.Space.noe):
                    i,phys=self.Space.theta_phys(k,0,0)
                    if phys == physical_domain:
                        self.basis_coeff[k,:,:]=val[k,:,:]
        
        if self.Space.dim == 3:
            val = np.zeros((self.Space.noe, self.Space.n, self.Space.n, self.Space.n),float)
            val[:,:,:,:] = value
            if physical_domain == 'none':
                self.basis_coeff[:,:,:,:]=val[:,:,:,:]
            else:
                for k in range(self.Space.noe):
                    i,phys=self.Space.theta_phys(k,0,0,0)
                    if phys == physical_domain:
                        self.basis_coeff[k,:,:,:]=val[k,:,:,:]
                    
        
    def glob(self):
        '''
        A method for grabbing the basis coefficients in global data structure. 
        
        :returns: The basis coefficients in global data structure. 
        :rtype: Numpy array
        
        Usage::
        
          import sempy
      
          X = sempy.Space( 'square',n = 5, dim = 2 )
          u = sempy.Function( X )
    
          u_glob = u.glob() 
        '''
        #if self.space == 'L2':
        #    print '---> error in TrialFunction.glob()'
        #    print '---> Cannot convert a function in L2 to'
        #    print '---> global data structure.'
        #else:
        return self.Space.local_to_global(self.basis_coeff)
    
    def quadrature(self):
        '''
        Computes the value :math:`\\kappa` of the integral 
        
        .. math::
           \\kappa = \\int_\\Omega f\\,d\\Omega 
           
        for :math:`f\\in L^2(\\Omega)` with GLL or GL quadrature rules, 
        depending of the corresponding space. 
        
        :returns: Value :math:`\\kappa` of the integral.
        
        Usage::
           
             import sempy
             
             X = sempy.Space( filename = 'square', n = 5, dim = 2 )
    
             u = sempy.Function( X, basis_coeff = X.x ) 
             print 'kappa=', u.quadrature()
        '''
        return self.Space.quadrature(self.basis_coeff)
        
    def l2_norm(self):
        """Computes the :math:`L^2` - norm
           
           .. math::
              ||u||_{L^2(\\Omega)}=\\bigg(\\int_{\\Omega} u^2d\\Omega\\bigg)^{1/2}
              
           using GLL or GL quadrature depending on the space. 
           
           :returns: The :math:`L^2` - norm as a floating number.
           
           Usage::
              
              import sempy
              
              X = sempy.Space( filename = 'square', n = 11, dim = 2 )
              
              u = sempy.Function( X, basis_coeff = X.x )
              print 'L2 norm=', u.l2_norm()

        """
        return self.Space.l2_norm( self.basis_coeff )
        
    def h1_norm(self):
        '''
        Computes the :math:`H^1(\\Omega)` - norm
           
        .. math::
           ||u||_{H^1(\\Omega)}=\\bigg(\\int_{\\Omega}\\bigg( u^2 + 
           \\sum_{i=1}^d\\bigg( \\frac{\\partial u}{\\partial x_i}\\bigg)^2
           \\bigg)
           d\\Omega\\bigg)^{1/2}
              
        using GLL quadrature. 
           
        :returns: The :math:`H^1` - norm as a floating number.
           
        Usage::
              
              import sempy
              
              X = sempy.Space( filename = 'square', n = 11, dim = 2 )
              
              u = sempy.Function( X, basis_coeff = X.x )
              print 'H1 norm=', u.h1_norm()
        
        '''
        if self.Space.dim == 1:
            u_x = self.grad()
            s_1 = self.Space.quadrature( self.basis_coeff * self.basis_coeff )
            s_2 = self.Space.quadrature( u_x * u_x )
            alpha = np.sqrt( s_1 + s_2 )
            return alpha
        
        if self.Space.dim == 2:
            u_x, u_y = self.grad()
            s_1 = self.Space.quadrature( self.basis_coeff * self.basis_coeff )
            s_2 = self.Space.quadrature( u_x * u_x )
            s_3 = self.Space.quadrature( u_y * u_y )
            alpha = np.sqrt( s_1 + s_2 + s_3 )
            return alpha
        
        if self.Space.dim == 3:
            u_x, u_y, u_z = self.grad()
            s_1 = self.Space.quadrature( self.basis_coeff * self.basis_coeff )
            s_2 = self.Space.quadrature( u_x * u_x )
            s_3 = self.Space.quadrature( u_y * u_y )
            s_4 = self.Space.quadrature( u_z * u_z )
            alpha = np.sqrt( s_1 + s_2 + s_3 + s_4 )
            return alpha
            
    def h1_semi_norm(self):
        '''
        Computes the :math:`H^1(\\Omega)` - semi-norm
           
        .. math::
           ||u||_{H^1(\\Omega)}=\\bigg(\\int_{\\Omega}
           \\sum_{i=1}^d\\bigg( \\frac{\\partial u}{\\partial x_i}\\bigg)^2
           d\\Omega\\bigg)^{1/2}
              
        using GLL quadrature. 
           
        :returns: The :math:`H^1` - semi-norm as a floating number.
           
        Usage::
              
              import sempy
              
              X = sempy.Space( filename = 'square', n = 11, dim = 2 )
              
              u = sempy.Function( X, basis_coeff = X.x )
              print 'H1 semi-norm=', u.h1_semi_norm()
        
        '''
        if self.Space.dim == 1:
            u_x = self.grad()
            s_1 = self.Space.quadrature( u_x * u_x )
            alpha = np.sqrt( s_1 )
            return alpha
        
        if self.Space.dim == 2:
            u_x, u_y = self.grad()
            s_1 = self.Space.quadrature( u_x * u_x )
            s_2 = self.Space.quadrature( u_y * u_y )
            alpha = np.sqrt( s_1 + s_2 )
            return alpha
        
        if self.Space.dim == 3:
            u_x, u_y, u_z = self.grad()
            s_1 = self.Space.quadrature( u_x * u_x )
            s_2 = self.Space.quadrature( u_y * u_y )
            s_3 = self.Space.quadrature( u_z * u_z )
            alpha = np.sqrt( s_1 + s_2 + s_3 )
            return alpha
            
        
    def grad(self):
        '''
        Computes the gradient vector of :math:`u`, i.e
        
        
        .. math::
        
           \\text{1D}:\quad \\nabla u= \partial u/\partial x
           
           \\text{2D}:\quad \\nabla u= (\partial u/\partial x,\partial u/\partial y)^T
           
           \\text{3D}:\quad \\nabla u= (\partial u/\partial x,\partial u/\partial y,\partial u/\partial z)^T
           
        :returns: The components of the gradient vector. 
        
        Usage::
          
          import sempy
          
          X = sempy.Space( 'square', n = 3, dim = 2 )
          u = sempy.Function( X, basis_coeff = X.x * X.x )
    
          # Calculate the gradient vector
          u_x, u_y = u.grad()
          u.set_value( u_x )
          u.plot_wire()
        
        '''
        #if self.Space.dim == 1:
        #    if self.Space.type == 'GL':
        #        print 'Warning: The gradient method is not implemented'
        #        print 'for functions in SpaceGL.'
        #        return
        #    else:
        #        u_x = sempy.space.space_f90.gradient_vector_1d(
        #                                    self.basis_coeff,
        #                                    self.Space.jac,
        #                                    self.Space.D)
        #        return u_x
        # 
        #if self.Space.dim == 2:
        #    if self.Space.type == 'GL':
        #        print 'Warning: The gradient method is not implemented'
        #        print 'for functions in SpaceGL.'
        #        return
        #    else:
        #        u_x, u_y = sempy.space.space_f90.gradient_vector_2d(
        #                                            self.basis_coeff,
        #                                            self.Space.x,
        #                                            self.Space.y,
        #                                            self.Space.jac,
        #                                            self.Space.D)
        #        return u_x, u_y
        # 
        #if self.Space.dim == 3:
        #    if self.Space.type == 'GL':
        #        print 'Warning: The gradient method is not implemented'
        #        print 'for functions in SpaceGL.'
        #        return
        #    else:
        #        #u_x, u_y, u_z = sempy.space.space_f90.gradient_vector_3d(
        #        #                self.basis_coeff,
        #        #                self.Space.jac,self.Space.D,
        #        #                self.Space.g11,self.Space.g12,
        #        #                self.Space.g13,self.Space.g21,
        #        #                self.Space.g22,self.Space.g23,
        #        #                self.Space.g31,self.Space.g32,
        #        #                self.Space.g33 )
        #        #print u_x
        return self.Space.gradient_vector( self.basis_coeff )
        
        #if self.Space.type == 'GL':
        #    print 'Warning: The gradient method is not implemented'
        #    print 'for functions in SpaceGL.'
        #    return
        #else:
        #    return self.Space.gradient_vector( self.basis_coeff )
        
    def hyper_filter(self,alpha=0.25):
        '''
        A filter for hyperbolic problems, see e.g. Deville et al. 
        
        .. math::
           u = F_\\alpha \\tilde u
           
        where the filter is
        
        .. math::
           F_\\alpha := \\alpha \\Pi_{N-1} + (1-\\alpha) I_N^N,\quad 
           \\Pi_{N-1} = I_{N-1}^N I_{N}^{N-1}
           
        Here, the weighting factor :math:`\\alpha` is typically in the 
        range :math:`0.05<\\alpha<0.3`. 
         
        :param alpha: Weighting factor.
        
        Usage::
        
          import sempy
          
          X = sempy.Space( 'square', n = 7, dim = 2 )
          u = sempy.Function( X, basis_coeff = X.x * X.x )
          
          u.hyper_filter( alpha = 0.3 )
          
        '''
        if self.Space.type == 'GL':
            print 'Warning: hyper_filter not applicable to functions in SpaceGL.'
            return
        if self.Space.n < 3:
            #return self.basis_coeff
            return
        else:
            #return self.Space.hyper_filter(self.basis_coeff,alpha)
            self.basis_coeff = self.Space.hyper_filter( self.basis_coeff,
                                                        alpha )
            return
    def plot(self,legend=True,filled=True,resolution=20.0,
             show_elements=True,font_size=20, show = True,
             show_boundary=False,
             lower='none',upper='none' ):
        if self.Space.dim==2:
            self.__plot_2d(legend=legend,filled=filled,
                           resolution=resolution,
                           show_elements=show_elements,
                           font_size=font_size,
                           show = show,
                           show_boundary=show_boundary,
                           lower=lower,upper=upper )
                
    def __plot_2d(self,legend=True,filled=True,resolution=20.0,
             show_elements=True,font_size=20, show = True,
             show_boundary=False,
             lower='none',upper='none' ):
        '''
        Plots the trial function. 
        
        Usage::
        
          u = Function(Space)
          u.plot()
          
        '''
        #rcParams['legend.fontsize']=3
        #fig=plt.figure()
        #ax=axes3d.Axes3D(fig)
        #for k in range(self.Space.noe):
        #    ax.plot_wireframe(self.Space.x[k,:,:],self.Space.y[k,:,:],self.coeff[k,:,:])
        #    #ax.plot_surface(self.x[k,:,:],self.y[k,:,:],u[k,:,:],rstride=1, cstride=1,cmap=cm.jet)
        #ax.set_xlabel(r'$x$')
        #ax.set_ylabel(r'$y$')
        #ax.set_zlabel(r'$u$')
        #plt.show()
        
        if self.Space.type == 'GL':
            u_i = self.Space.interpolation_gll(self.basis_coeff)
            x_i = self.Space.interpolation_gll(self.Space.x)
            y_i = self.Space.interpolation_gll(self.Space.y)
        else:
            n_int = 17
            u_i = self.Space.interpolation(self.basis_coeff,  n_int)
            x_i = self.Space.interpolation(self.Space.x, n_int)
            y_i = self.Space.interpolation(self.Space.y, n_int)
        
        extent_2 = (x_i.min(),x_i.max(),y_i.min(),y_i.max())
        
        fig_number = np.random.randint(0,101)
        
        #a_x=35.0/5.0
        #b_y=20.0/5.0
        #a_x=14.0/1.5#35.0/5.0
        #b_y=7.0/1.5#20.0/5.0
        #fig = plt.figure(fig_number,figsize=[ a_x, b_y ])
        fig = plt.figure(fig_number)  
    
        ax = fig.add_subplot(111)

        #levels=np.arange(-0.2,1.01,0.02)
        #beta = (abs(self.coeff.min())+abs(self.coeff.max()))/20.0
        #low  = self.coeff.min()-abs(self.coeff.min())*0.15
        #high = self.coeff.max()+self.coeff.max()*0.15
        #beta = (abs(low)+abs(high))/40.0
        if lower == 'none':
            low = u_i.min()-abs(u_i.min())#25
        else:
            low = lower
        #print 'low=',low
        if upper == 'none':
            high = u_i.max()#+abs(u_i.max())*0.12#25
        else:
            high = upper 
        beta   = (abs(low)+abs(high))/float(resolution)#40.0
        levels = np.arange(low-beta,high+beta,beta)
        #print levels
                
        if len(levels) == 0:
            levels= np.arange(-0.1,0.11,.01)
        #levels_new=np.zeros((len(levels)+1), float)
        #levels_new[0]=-0.13625
        #for i in range(len(levels)):
        #    levels_new[i+1]=levels[i]
        #del levels
        #levels=levels_new
        # Contour plot
        for k in range(self.Space.noe):
            if filled:
                plt.contourf(x_i[k,:,:],y_i[k,:,:],u_i[k,:,:],levels,\
                         cmap=cm.get_cmap('jet',len(levels)-1))#,extent=extent_2)
            else:
                plt.contour(x_i[k,:,:],y_i[k,:,:],u_i[k,:,:],levels,
                            #cmap=cm.get_cmap('jet',len(levels)-1),
                            linewidths=1,#)#,colors='b',linestyles='solid')
                            colors='k',linestyles='solid')
        #Elements
        thickness = 0.5
        if show_elements:
            if self.Space.type=='GL':
                n = self.Space.Space.n
                for k in range(self.Space.noe):
                    #for m in range(n):
                    plt.plot( self.Space.Space.x[k,:,0],
                              self.Space.Space.y[k,:,0],
                              color = 'k', linewidth = thickness)
                    plt.plot( self.Space.Space.x[k,:,n-1],
                              self.Space.Space.y[k,:,n-1],
                              color = 'k', linewidth = thickness)
                    plt.plot( self.Space.Space.x[k,0,:],
                              self.Space.Space.y[k,0,:],
                              color = 'k', linewidth = thickness)
                    plt.plot( self.Space.Space.x[k,n-1,:],
                              self.Space.Space.y[k,n-1,:],
                              color = 'k', linewidth = thickness)
            else:
                n = self.Space.n
                for k in range(self.Space.noe):
                    #for m in range(n):
                    plt.plot(self.Space.x[k,:,0],self.Space.y[k,:,0],
                         color='k',linewidth=thickness)
                    plt.plot(self.Space.x[k,:,n-1],self.Space.y[k,:,n-1],
                         color='k',linewidth=thickness)
                    plt.plot(self.Space.x[k,0,:],self.Space.y[k,0,:],
                         color='k',linewidth=thickness)
                    plt.plot(self.Space.x[k,n-1,:],self.Space.y[k,n-1,:],
                         color='k',linewidth=thickness)
        if legend:
            #rcParams['legend.fontsize']= font_size
            cbar = plt.colorbar( shrink=0.6)#,
                                 #orientation='horizontal')
            #cb = colorbar() # grab the Colorbar instance
            for t in cbar.ax.get_yticklabels():
                t.set_fontsize(20)

        
        if show_boundary:
            X = self.Space
            xb = X.boundary_value( X.x )
            yb = X.boundary_value( X.y )
            for k in range(X.noe_bc):
                plt.plot(xb[k,:],yb[k,:],color='k')
            #for k in range(self.Space.noe_bc):
            #    plt.plot
        #ax.xaxis.set_major_locator(ticker.FixedLocator(
        #                     (0.2,0.4,0.6,0.8)))
        #ax.yaxis.set_major_locator(ticker.FixedLocator(
        #                     (0.2,0.4,0.6,0.8)))

        plt.xlabel(r'$x$', fontsize = font_size )
        plt.ylabel(r'$y$', fontsize = font_size )
        
        plt.axis([self.Space.x.min(),self.Space.x.max(),
                  self.Space.y.min(),self.Space.y.max()])
        plt.axes().set_aspect('equal')
        
        ax = plt.gca()
        for label in ax.xaxis.get_ticklabels():
            label.set_fontsize( font_size )
        for label in ax.yaxis.get_ticklabels():
            label.set_fontsize( font_size )
        
        if show:
            plt.show()
        
        
    def plot_wire( self, levels = 7, show = True ):
        '''
        Visualization of the function.
        
        :param levels: Number of levels in the contour plot (for 3D functions).
        :type levels: int
        '''
        # filename = 'none'
        if self.Space.dim == 1:
            fig = plt.figure()
            for k in range(self.Space.noe):
                plt.plot(self.Space.x[k,:],self.basis_coeff[k,:])
            plt.xlabel(r'$x$')
            plt.ylabel(r'$u$')
            #if filename != 'none':
            #    print '---> filename=',filename
            #    plt.savefig(filename)
            if show:
                plt.show()
                
        if self.Space.dim == 2:
            fig = plt.figure()
            ax = axes3d.Axes3D(fig)
            for k in range(self.Space.noe):
                ax.plot_wireframe( self.Space.x[k,:,:], self.Space.y[k,:,:],
                                   self.basis_coeff[k,:,:])
            ax.set_xlabel(r'$x$')
            ax.set_ylabel(r'$y$')
            ax.set_zlabel(r'$u$')
            #if filename != 'none':
            #    print '---> filename=',filename
            #    plt.savefig(filename)
            plt.show()
            
        if  self.Space.dim == 3:
            self.__plot_wire_3d(levels)#contours=[0.01,0.02]):
    
    def __plot_wire_3d( self, levels ):#contours=[0.2,0.4,0.6,0.8]):
        try:
            import enthought.mayavi
        except:
            print 'No mayavi python module installed.'
            print '3D plotting not possible.'
            return
        #X_fem = sempy.precond.SpaceFEM(self.Space)
        #if self.SpaceFEM == 'none':
        #    print 'Error: Supply a SpaceFEM instance to facilitate 3D plotting'
        #    return
        
        u_max = self.basis_coeff.max()
        u_min = self.basis_coeff.min()
        du = ( u_max - u_min ) / float( levels )
        cont =np.arange( u_min, u_max, du )
        contours=['asdf']
        for i in range(len(cont)):
            contours.append(cont[i])
        contours.remove('asdf') 

        v_fem = sempy.Function(self.Space,filename='temp_file')
        v_fem.basis_coeff = self.basis_coeff
        #v_fem.basis_coeff = self.SpaceFEM.sem_to_fem(u.basis_coeff)
        v_fem.to_file()

        vtkFile='temp_file0.vtk'

        # Create the MayaVi engine and start it.
        from enthought.mayavi.core.api import Engine
        engine = Engine()
        engine.start()
        scene = engine.new_scene()

        # Read in VTK file and add as source
        from enthought.mayavi.sources.vtk_file_reader import VTKFileReader
        reader = VTKFileReader()
        reader.initialize(vtkFile)
        engine.add_source(reader)

        ## Add Surface Module
        #from enthought.mayavi.modules.surface import Surface
        #surface = Surface()
        #engine.add_module(surface)

        # Axes
        from enthought.mayavi.modules.axes import Axes
        axes = Axes()
        engine.add_module(axes)

        # Outline
        from enthought.mayavi.modules.outline import Outline
        outline = Outline()
        engine.add_module(outline)

        # IsoSurface
        from enthought.mayavi.modules.api import IsoSurface
        iso = IsoSurface()
        engine.add_module(iso)
        #iso.contour.contours = [-0.4, 0.0, 0.4]
        #iso.contour.contours = [-0.9, 0.45, 0.0, 0.45, 0.9]
        iso.contour.contours = contours#[0.01, 0.02, 0.03]
         #iso.contour.filled.contours = True
        # Make them translucent.
        #iso.actor.property.opacity = 0.9
        # Show the scalar bar (legend).
        iso.module_manager.scalar_lut_manager.show_scalar_bar = True

        # Move the camera
        scene.scene.camera.elevation(-45)

        # Save scene to image file
        #scene.scene.save_png('figures/poisson_3d_plot.png')

        # Create a GUI instance and start the event loop.
        # This stops the window from closing
        from enthought.pyface.api import GUI
        gui = GUI()
        gui.start_event_loop()
        
            
    def to_file_old(self):
        # Filename
        #if self.file_count == 0:
        #    _filename = self.filename + '.vtk'
        #    self.file_count=self.file_count+1
        #else:
        _filename = self.filename + str(self.file_count) + '.vtk'
        self.file_count=self.file_count+1
        print '_filename=',_filename
        
        # open file
        f = open(_filename,'w')
        f.write('# vtk DataFile Version 3.0\n')
        f.write('Sempy data file\n')
        f.write('ASCII\n')
        f.write('DATASET UNSTRUCTURED_GRID\n')
        
        #--- Points
        f.write('\n')
        f.write('POINTS ')
        a = np.zeros(1,np.int)
        a[0] = self.Space.dof
        f.write(np.array_str(a[0]))
        f.write(' float\n')
        
        xx = self.Space.local_to_global(self.Space.x)
        yy = self.Space.local_to_global(self.Space.y)
        zz = self.Space.local_to_global(self.Space.z)

        for k in range(self.Space.dof):
            f.write(np.array_str(xx[k]))
            f.write(' ')
            f.write(np.array_str(yy[k]))
            f.write(' ')
            f.write(np.array_str(zz[k]))
            f.write(' \n')

        #--- Cells
        f.write('\n')
        f.write('CELLS ')
        a=np.zeros(1,np.int)
        a[0]=self.Space.noe
        f.write(np.array_str(a[0]))
        f.write(' ')
        a=np.zeros(1,np.int)
        a[0]=self.Space.noe*(self.Space.n*self.Space.n*self.Space.n + 1)
        f.write(np.array_str(a[0]))
        f.write('\n')
        for k in range(self.Space.noe):
            f.write('8 ')
            f.write(np.array_str(self.Space.theta[k,0,0,0]))
            f.write(' ')
            f.write(np.array_str(self.Space.theta[k,1,0,0]))
            f.write(' ')
            f.write(np.array_str(self.Space.theta[k,1,0,1]))
            f.write(' ')
            f.write(np.array_str(self.Space.theta[k,0,0,1]))
            f.write(' ')
            f.write(np.array_str(self.Space.theta[k,0,1,0]))
            f.write(' ')
            f.write(np.array_str(self.Space.theta[k,1,1,0]))
            f.write(' ')
            f.write(np.array_str(self.Space.theta[k,1,1,1]))
            f.write(' ')
            f.write(np.array_str(self.Space.theta[k,0,1,1]))
            f.write(' \n')
            
        #--- Cell types
        f.write('\n')
        f.write('CELL_TYPES ')
        a=np.zeros(1,np.int)
        a[0]=self.Space.noe
        f.write(np.array_str(a[0]))
        f.write('\n')
        a[0]=12
        for k in range(self.Space.noe):
            f.write(np.array_str(a[0]))
            f.write(' \n')
        f.write('\n')
        
        #--- Scalar
        #if self.file_count > 0:
        _u = self.Space.local_to_global(self.basis_coeff)
        
        f.write('POINT_DATA ')
        a=np.zeros(1,np.int)
        a[0]=self.Space.dof
        f.write(np.array_str(a[0]))
        f.write('\n')
        f.write('SCALARS scalars float\n')
        f.write('LOOKUP_TABLE default\n')
        #a=np.zeros(1,np.float)
        #a[0]=3.0
        for k in range(self.Space.dof):
            f.write(np.array_str(_u[k]))
            #f.write(np.array_str(a[0]))
            f.write(' \n')
    
        f.close()
    
    def to_file(self):
        '''
        This method prints the basis coefficients to a 
        file. For 2D and 3D functions, the coefficients is written 
        into a file of the vtk file format. 1D functions are written 
        into a trivial .dat file with two columns.
        '''
        if not self.filename == None:
            if self.Space.dim == 1:
                self.__to_file_1d()
            if self.Space.dim == 2:
                self.__to_file_2d()
            if self.Space.dim == 3:
                self.__to_file_3d()
            
    def __to_file_1d(self):
        '''
        Print the basis coefficients to a file in the vtk file format.
        '''
        # Filename
        #if self.file_count == 0:
        #    _filename = self.filename + '.vtk'
        #    self.file_count=self.file_count+1
        #else:
        
        _filename = self.filename + str(self.file_count) + '.dat'
        self.file_count=self.file_count+1
        print '_filename=',_filename
        
        # open file
        f = open(_filename,'w')
        
        xx = self.Space.local_to_global(self.Space.x)
        uu = self.Space.local_to_global(self.basis_coeff)
        
        # Write to file
        for k in range(self.Space.dof):
            f.write(np.array_str(xx[k]))
            f.write(' ')
            f.write(np.array_str(uu[k]))
            f.write(' \n')
            
        # Close file
        f.close()
        
    def __to_file_2d(self):
        '''
        Print the basis coefficients to a file in the vtk file format.
        '''
        # Filename
        #if self.file_count == 0:
        #    _filename = self.filename + '.vtk'
        #    self.file_count=self.file_count+1
        #else:
        
        _filename = self.filename + str(self.file_count) + '.vtk'
        self.file_count=self.file_count+1
        
        #print '_filename=',_filename
        
        # open file
        f = open(_filename,'w')
        f.write('# vtk DataFile Version 3.0\n')
        f.write('Sempy data file\n')
        f.write('ASCII\n')
        f.write('DATASET UNSTRUCTURED_GRID\n')
        
        #--- Points
        f.write('\n')
        f.write('POINTS ')
        a = np.zeros(1,np.int)
        a[0] = self.Space.dof
        f.write(np.array_str(a[0]))
        f.write(' float\n')
        
        
        xx = self.Space.fem.local_to_global(self.Space.fem.x)
        yy = self.Space.fem.local_to_global(self.Space.fem.y)
        zz = np.zeros((self.Space.dof),float)

        for k in range(self.Space.dof):
            f.write(np.array_str(xx[k]))
            f.write(' ')
            f.write(np.array_str(yy[k]))
            f.write(' ')
            f.write(np.array_str(zz[k]))
            f.write(' \n')

        #--- Cells
        f.write('\n')
        f.write('CELLS ')
        a = np.zeros(1,np.int)
        a[0] = self.Space.fem.noe
        f.write( np.array_str( a[0] ) )
        f.write( ' ' ) 
        a = np.zeros( 1, np.int )
        a[0] = self.Space.fem.noe*(self.Space.fem.n*self.Space.fem.n + 1)
        f.write( np.array_str( a[0] ) )
        f.write('\n')
        for k in range(self.Space.fem.noe):
            f.write('4 ')
            f.write(np.array_str(self.Space.fem.theta[k,0,0]))
            f.write(' ')
            f.write(np.array_str(self.Space.fem.theta[k,1,0]))
            f.write(' ')
            f.write(np.array_str(self.Space.fem.theta[k,0,1]))
            f.write(' ')
            f.write(np.array_str(self.Space.fem.theta[k,1,1]))
            f.write(' \n')
            
        #--- Cell types
        f.write( '\n' )
        f.write( 'CELL_TYPES ' )
        a = np.zeros( 1, np.int )
        a[0] = self.Space.fem.noe
        f.write( np.array_str( a[0] ) )
        f.write( '\n' )
        a[0] = 8
        for k in range(self.Space.fem.noe):
            f.write(np.array_str(a[0]))
            f.write(' \n')
        f.write('\n')
        
        #--- Scalar
        #if self.file_count > 0:
        __u = self.Space.fem.sem_to_fem(self.basis_coeff)
    
        _u = self.Space.fem.local_to_global(__u)#self.basis_coeff)
        
        f.write('POINT_DATA ')
        a = np.zeros(1,np.int)
        a[0] = self.Space.dof
        f.write( np.array_str(a[0]) )
        f.write('\n')
        f.write('SCALARS scalars float\n')
        f.write('LOOKUP_TABLE default\n')
        #a=np.zeros(1,np.float)
        #a[0]=3.0
        for k in range(self.Space.dof):
            f.write(np.array_str(_u[k]))
            #f.write(np.array_str(a[0]))
            f.write(' \n')
    
        f.close()
                
    def __to_file_3d(self):
        '''
        Print the basis coefficients to a file in the vtk file format.
        '''
        # Filename
        #if self.file_count == 0:
        #    _filename = self.filename + '.vtk'
        #    self.file_count=self.file_count+1
        #else:
        
        _filename = self.filename + str(self.file_count) + '.vtk'
        self.file_count=self.file_count+1
        #print '_filename=',_filename
        
        # open file
        f = open(_filename,'w')
        f.write('# vtk DataFile Version 3.0\n')
        f.write('Sempy data file\n')
        f.write('ASCII\n')
        f.write('DATASET UNSTRUCTURED_GRID\n')
        
        #--- Points
        f.write('\n')
        f.write('POINTS ')
        a = np.zeros(1,np.int)
        a[0] = self.Space.dof
        f.write(np.array_str(a[0]))
        f.write(' float\n')
        
        
        xx = self.Space.fem.local_to_global(self.Space.fem.x)
        yy = self.Space.fem.local_to_global(self.Space.fem.y)
        zz = self.Space.fem.local_to_global(self.Space.fem.z)

        for k in range(self.Space.dof):
            f.write(np.array_str(xx[k]))
            f.write(' ')
            f.write(np.array_str(yy[k]))
            f.write(' ')
            f.write(np.array_str(zz[k]))
            f.write(' \n')

        #--- Cells
        f.write('\n')
        f.write('CELLS ')
        a = np.zeros(1,np.int)
        a[0] = self.Space.fem.noe
        f.write( np.array_str( a[0] ) )
        f.write( ' ' ) 
        a = np.zeros( 1, np.int )
        a[0] = self.Space.fem.noe*(self.Space.fem.n*self.Space.fem.n*self.Space.fem.n + 1)
        f.write( np.array_str( a[0] ) )
        f.write('\n')
        for k in range(self.Space.fem.noe):
            f.write('8 ')
            f.write(np.array_str(self.Space.fem.theta[k,0,0,0]))
            f.write(' ')
            f.write(np.array_str(self.Space.fem.theta[k,1,0,0]))
            f.write(' ')
            f.write(np.array_str(self.Space.fem.theta[k,1,0,1]))
            f.write(' ')
            f.write(np.array_str(self.Space.fem.theta[k,0,0,1]))
            f.write(' ')
            f.write(np.array_str(self.Space.fem.theta[k,0,1,0]))
            f.write(' ')
            f.write(np.array_str(self.Space.fem.theta[k,1,1,0]))
            f.write(' ')
            f.write(np.array_str(self.Space.fem.theta[k,1,1,1]))
            f.write(' ')
            f.write(np.array_str(self.Space.fem.theta[k,0,1,1]))
            f.write(' \n')
            
        #--- Cell types
        f.write( '\n' )
        f.write( 'CELL_TYPES ' )
        a = np.zeros( 1, np.int )
        a[0] = self.Space.fem.noe
        f.write( np.array_str( a[0] ) )
        f.write( '\n' )
        a[0] = 12
        for k in range(self.Space.fem.noe):
            f.write(np.array_str(a[0]))
            f.write(' \n')
        f.write('\n')
        
        #--- Scalar
        #if self.file_count > 0:
        __u = self.Space.fem.sem_to_fem(self.basis_coeff)
    
        _u = self.Space.fem.local_to_global(__u)#self.basis_coeff)
        
        f.write('POINT_DATA ')
        a = np.zeros(1,np.int)
        a[0] = self.Space.dof
        f.write( np.array_str(a[0]) )
        f.write('\n')
        f.write('SCALARS scalars float\n')
        f.write('LOOKUP_TABLE default\n')
        #a=np.zeros(1,np.float)
        #a[0]=3.0
        for k in range(self.Space.dof):
            f.write(np.array_str(_u[k]))
            #f.write(np.array_str(a[0]))
            f.write(' \n')
    
        f.close()


if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    import sempy
      
    #X = sempy.Space('line',n = 6, dim = 1)
    #X = sempy.Space('square',n = 6, dim = 2)
    X = sempy.Space('cube',n = 4, dim = 3)
    

