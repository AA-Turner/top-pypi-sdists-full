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
import sempy
import sempy.space.space_f90 as space_f90

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import sempy.operators
import scipy.sparse.linalg as spl

import pysparse
from pysparse.direct import umfpack
# Compatibility with older versions
if int(pysparse.__version__[2]) >= 2:
    from pysparse.sparse.pysparseMatrix import PysparseMatrix #as pysparseMatrix
    from pysparse import direct
    
if int(pysparse.__version__[2]) <= 1:
    from pysparse.pysparseMatrix import PysparseMatrix
import time
import precond_f90



#print umfpack.factorize.__doc__


#import PyTrilinos.Epetra as Epetra
#import PyTrilinos.AztecOO as AztecOO
#import PyTrilinos.IFPACK as IFPACK

class SpaceFEM():
    '''
    Finite element space. 
    
    :param Space: A spectral element space
    :type Space: :class:`sempy.Space`
    
    **Example**::
    
      import sempy
      
      # SEM Space
      X = sempy.Space('square', n = 10, dim = 2)
      
      # FEM Space
      X_fem = sempy.precond.SpaceFEM( X )
      
      
    '''
    def __init__(self,Space):
        '''
        This is the init method.
        '''
        self.Space = Space
        self.type = 'GLL'
        
        self.n = 2
        self.dof = self.Space.dof
        self.basic = sempy.Basic()
        self.D = self.basic.derivative_matrix_gll( self.n )
        self.points, self.weights = \
                    self.basic.gauss_lobatto_legendre( self.n )
        
        if self.Space.dim == 1:
            self.noe = (self.Space.n-1)*self.Space.noe
            self.noe_bc = self.Space.noe_bc
            self.x, self.theta=self.fem_x()
            self.dim = 1
            self.jac_s = np.zeros((self.noe_bc), float)
            
        if self.Space.dim == 2:
            self.noe = (self.Space.n-1)*(self.Space.n-1)*self.Space.noe
            self.noe_bc = (self.Space.n-1)*self.Space.noe_bc
            self.x, self.y, self.theta = self.fem_xy()
            self.dim = 2
            self.jac_s = np.zeros((self.noe_bc,self.n), float)
        
        if self.Space.dim == 3:
            self.noe = (self.Space.n-1)*(self.Space.n-1)*\
                       (self.Space.n-1)*self.Space.noe
            self.noe_bc = (self.Space.n-1)*(self.Space.n-1)*\
                          self.Space.noe_bc
            self.x, self.y, self.z, self.theta = self.fem_xyz()
            self.dim = 3
            self.jac_s = np.zeros((self.noe_bc,self.n,self.n), float)
            
        self.theta_bc, self.physical_bc =  self.boundary_connectivity()
        self.jac = self._geometric()
        self.bc_type = self.Space.bc_type
        
        
    def _geometric(self):
        
        if self.Space.dim == 1:
            jac = space_f90.geometric_1d(self.x,self.D)
        if self.Space.dim == 2:
            jac = space_f90.geometric_2d(self.x,self.y,self.D)
        if self.Space.dim == 3:
            jac = space_f90.geometric_3d(self.x,self.y,self.z,self.D)
            
        return jac 
        
    def plot_mesh(self):
        '''
        Plots the numerical mesh.
        '''
        if self.dim == 1:
            u = np.zeros((self.noe,self.n),float)
            fig = plt.figure()
            for k in range(self.noe):
                plt.plot(self.x[k,:],u[k,:],'o-')
            plt.xlabel(r'$x$')
            plt.ylabel(r'$u$')
            plt.show()
            
        if self.dim == 2:
            u = np.zeros((self.noe,self.n,self.n),float)
            fig = plt.figure()
            ax = axes3d.Axes3D(fig)
            for k in range(self.noe):
                ax.plot_wireframe(self.x[k,:,:],self.y[k,:,:],u[k,:,:])
            plt.show()
    
    def plot_scalar(self,u,n_int=0):
        if n_int == 0:
            fig=plt.figure()
            ax=axes3d.Axes3D(fig)
            for k in range(self.noe):
                ax.plot_wireframe(self.x[k,:,:],self.y[k,:,:],u[k,:,:])
                #ax.plot_surface(self.x[k,:,:],self.y[k,:,:],u[k,:,:],rstride=1, cstride=1)
            ax.set_xlabel(r'$x$')
            ax.set_ylabel(r'$y$')
            ax.set_zlabel(r'$u$')
            plt.show()
        else:
            u_i = self.interpolation(u,n_int)
            x_i = self.interpolation(self.x, n_int)
            y_i = self.interpolation(self.y, n_int)
            
            fig = plt.figure()
            ax = axes3d.Axes3D(fig)
            for k in range(self.noe):
                #ax.plot_wireframe(x_i[k,:,:],y_i[k,:,:],u_i[k,:,:],rstride=1, cstride=1)
                ax.plot_surface(x_i[k,:,:],y_i[k,:,:],u_i[k,:,:],rstride=1, cstride=1)
            #ax.set_zlim3d(0, 1.0)
            ax.set_xlabel(r'$x$')
            ax.set_ylabel(r'$y$')
            ax.set_zlabel(r'$u$')
            plt.show()

    def l2_norm(self,u):
        '''
        Computes the :math:`L^2(\Omega)` - norm
           
        .. math::
           ||u||_{L^2(\\Omega)}=\\bigg(\\int_{\\Omega} u^2d\\Omega\\bigg)^{1/2}
              
        using GLL quadrature. 
           
        :param u: Basis coefficients in global data structure, i.e. 
                  :math:`u\\in\\mathbb R^{dof}` .
        :returns: The :math:`L^2` - norm as a floating number.
                   
        Usage::
           
             import sempy
             
             X = sempy.Space( filename = 'square', n = 5, dim = 2 ) 
             X_fem = sempy.SpaceFEM( X )      
             u = np.ones( ( X_fem.dof ), float )
             print 'L2-norm=',X_fem.l2_norm( u )
        '''
        if self.dim == 1:
            u_local = self.mapping_Q(u)
            norm = space_f90.l2norm_1d(self.weights,self.jac,u_local)
            
        if self.dim == 2:
            u_local = self.mapping_Q(u)
            norm = space_f90.l2norm_2d(self.weights,self.jac,u_local)
        
        if self.dim == 3:
            u_local = self.mapping_Q(u)
            print 'oobss l2 norm check mapping'
            norm = space_f90.l2norm_3d(self.weights,self.jac,u_local)
            
        return norm
    
    def quadrature(self,f):
        '''
        Computes the value :math:`\\kappa` of the integral 
        
        .. math::
           \\kappa = \\int_\\Omega f\\,d\\Omega 
           
        for :math:`f\\in L^2(\\Omega)` with GLL quadrature rules. 
        
        :param f: Basis coefficients of the function to be integrated 
                  given in local data representation 
                  (since :math:`f\\in L^2(\\Omega)`). 
        :returns: Value :math:`\\kappa` of the integral.
        
        Usage::
           
             import sempy
             X = sempy.Space( filename = 'square', n = 5, dim = 2 )
             X_fem = sempy.SpaceFEM( X )
    
             u = sempy.Function( X_fem, basis_coeff = X.x ) 
             kappa = X_fem.quadrature( u.basis_coeff )
        '''
        if self.dim == 1:
            kappa = space_f90.quadrature_1d(self.weights,self.jac,f)
        if self.dim == 2:
            kappa = space_f90.quadrature_2d(self.weights,self.jac,f)
        if self.dim == 3:
            kappa = space_f90.quadrature_3d(self.weights,self.jac,f)
        return kappa
        
    def theta_phys_bc(self, *args):
        '''
        :todo: element_edge
        '''
        
        if self.dim == 1:
            k=args[0]
            i       = self.theta_bc[k]
            phys    = self.physical_bc[k]
            #bc_type = self.Space.GTS.bc_type[phys-1]
            boundarycondtion_type = self.bc_type[phys-1]
            #element_edge = self.edge[k]
            element_edge=[0,0]
            
        if self.dim == 2:
            k=args[0]
            m=args[1]
            i       = self.theta_bc[k,m]
            phys    = self.physical_bc[k]
            #bc_type = self.Space.GTS.bc_type[phys-1]
            boundarycondtion_type = self.bc_type[phys-1]
            #element_edge = self.edge[k]
            element_edge=[0,0]
        
        if self.dim == 3:
            k=args[0]
            m=args[1]
            n=args[2]
            i       = self.theta_bc[k,m,n]
            phys    = self.physical_bc[k]
            #bc_type = self.Space.GTS.bc_type[phys-1]
            boundarycondtion_type = self.bc_type[phys-1]
            #element_edge = self.edge[k]
            element_edge=[0,0]
            
        return int(i), phys, boundarycondtion_type, element_edge

           
    def mapping_q(self,v):
        if self.dim == 1:
            w = space_f90.mapping_q_1d(v,self.theta)
        if self.dim == 2:
            w = space_f90.mapping_q_2d(v,self.theta)
        if self.dim == 3:
            w = space_f90.mapping_q_3d(v,self.theta)
        return w
        
    def mapping_qt(self,w):
        if self.dim == 1:
            v = space_f90.mapping_qt_1d(w,self.theta,self.dof)
        if self.dim == 2:
            v = space_f90.mapping_qt_2d(w,self.theta,self.dof)
        if self.dim == 3:
            v = space_f90.mapping_qt_3d(w,self.theta,self.dof)
        return v
    
    def local_to_global(self,w):
        if self.dim == 1:
            v = space_f90.local_to_global_1d(w,self.theta,self.dof)
        if self.dim == 2:
            v = space_f90.local_to_global_2d(w,self.theta,self.dof)
        if self.dim == 3:
            v = space_f90.local_to_global_3d(w,self.theta,self.dof)
        return v

    def mask(self,w):
        if self.dim == 1:
            for k in range(self.noe_bc):
                [i, name, bc_type, element_edge] = self.theta_phys_bc(k)
                if bc_type == 'Dir':
                    w[i] = 0.0
                        
        if self.dim == 2:
            for k in range(self.noe_bc):
                for m in range(self.n):
                    [i, name, bc_type, element_edge] = self.theta_phys_bc(k,m)
                    if bc_type == 'Dir':
                        w[i] = 0.0
        if self.dim == 3:
            for k in range(self.noe_bc):
                for m in range(self.n):
                    for n in range(self.n):
                        [i, name, bc_type, element_edge] = self.theta_phys_bc(k,m,n)
                        if bc_type == 'Dir':
                            w[i] = 0.0
        return w
        
    def mask_matrix(self,A):
        if self.dim == 1:
            for k in range(self.noe_bc):
                [i, phys, bc_type, element_edge]=self.theta_phys_bc(k)
                if bc_type == "Dir":
                    A[int(i),:] = 0.0
        if self.dim == 2:
            for k in range(self.noe_bc):
                for m in range(self.n):
                    [i, phys, bc_type, element_edge]=self.theta_phys_bc(k,m)
                    if bc_type == "Dir":
                        A[i,:] = 0.0
        if self.dim == 3:
            val = np.zeros((self.dof),float)
            row = np.zeros((self.dof),int)
            col = np.zeros((self.dof),int)
            col[:]=range(self.dof)
            for k in range(self.noe_bc):
                for m in range(self.n):
                    for n in range(self.n):
                        [i, phys, bc_type, element_edge]=self.theta_phys_bc(k,m,n)
                        if bc_type == "Dir":
                            #A[int(i),0:-1:1] = 0.0
                            row[:] = int(i)
                            A.put(val,row,col)
        return A
    
    def fem_x(self):
        x,theta = precond_f90.fem_coor_1d(self.Space.x,self.Space.theta, \
                                          self.n,self.noe)
        #x = np.zeros( (self.noe,self.n),float)
        #theta = np.zeros( (self.noe,self.n),int)
        
        #count=0
        #for k in range(self.Space.noe):
        #    for i in range(self.Space.n-1):
        #        x[count,0]=self.Space.x[k,i]
        #        x[count,1]=self.Space.x[k,i+1]
        #        theta[count,0]=self.Space.theta[k,i]
        #        theta[count,1]=self.Space.theta[k,i+1]
        #        count=count+1
        return x, theta
        
    def fem_xy(self):
        x,y,theta = precond_f90.fem_coor_2d( self.Space.x,
                                             self.Space.y,
                                             self.Space.theta, 
                                             self.n,self.noe )
        
        #x = np.zeros((self.noe,self.n,self.n),float)
        #y = np.zeros((self.noe,self.n,self.n),float)
        #theta = np.zeros((self.noe,self.n,self.n),int)
        
        #count=0
        #for k in range(self.Space.noe):
        #    for i in range(self.Space.n-1):
        #        for j in range(self.Space.n-1):
        #            x[count,0,0]=self.Space.x[k,i,j]
        #            x[count,1,0]=self.Space.x[k,i+1,j]
        #            x[count,0,1]=self.Space.x[k,i,j+1]
        #            x[count,1,1]=self.Space.x[k,i+1,j+1]
        #            y[count,0,0]=self.Space.y[k,i,j]
        #            y[count,1,0]=self.Space.y[k,i+1,j]
        #            y[count,0,1]=self.Space.y[k,i,j+1]
        #            y[count,1,1]=self.Space.y[k,i+1,j+1]
        #            theta[count,0,0]=self.Space.theta[k,i,j]
        #            theta[count,1,0]=self.Space.theta[k,i+1,j]
        #            theta[count,0,1]=self.Space.theta[k,i,j+1]
        #            theta[count,1,1]=self.Space.theta[k,i+1,j+1]
        #            count=count+1
        
        return x, y, theta
    
    def fem_xyz(self):
        #print precond_f90.fem_coor_3d.__doc__
        x,y,z,theta = precond_f90.fem_coor_3d( self.Space.x,
                                               self.Space.y,
                                               self.Space.z,
                                               self.Space.theta, 
                                               self.n,self.noe )
        
        #x = np.zeros((self.noe,self.n,self.n,self.n),float)
        #y = np.zeros((self.noe,self.n,self.n,self.n),float)
        #z = np.zeros((self.noe,self.n,self.n,self.n),float)
        #theta = np.zeros((self.noe,self.n,self.n,self.n),int)
        
        #count=0
        #for k in range(self.Space.noe):
        #    for m in range(self.Space.n-1):
        #        for n in range(self.Space.n-1):
        #            for o in range(self.Space.n-1):
        #                x[count,0,0,0]=self.Space.x[k,m,n,o]
        #                x[count,1,0,0]=self.Space.x[k,m+1,n,o]
        #                x[count,0,1,0]=self.Space.x[k,m,n+1,o]
        #                x[count,1,1,0]=self.Space.x[k,m+1,n+1,o]
        #                x[count,0,0,1]=self.Space.x[k,m,n,o+1]
        #                x[count,1,0,1]=self.Space.x[k,m+1,n,o+1]
        #                x[count,0,1,1]=self.Space.x[k,m,n+1,o+1]
        #                x[count,1,1,1]=self.Space.x[k,m+1,n+1,o+1]
                    
        #                y[count,0,0,0]=self.Space.y[k,m,n,o]
        #                y[count,1,0,0]=self.Space.y[k,m+1,n,o]
        #                y[count,0,1,0]=self.Space.y[k,m,n+1,o]
        #                y[count,1,1,0]=self.Space.y[k,m+1,n+1,o]
        #               y[count,0,0,1]=self.Space.y[k,m,n,o+1]
        #                y[count,1,0,1]=self.Space.y[k,m+1,n,o+1]
        #                y[count,0,1,1]=self.Space.y[k,m,n+1,o+1]
        #                y[count,1,1,1]=self.Space.y[k,m+1,n+1,o+1]
                        
        #                z[count,0,0,0]=self.Space.z[k,m,n,o]
        #                z[count,1,0,0]=self.Space.z[k,m+1,n,o]
        #                z[count,0,1,0]=self.Space.z[k,m,n+1,o]
        #                z[count,1,1,0]=self.Space.z[k,m+1,n+1,o]
        #                z[count,0,0,1]=self.Space.z[k,m,n,o+1]
        #                z[count,1,0,1]=self.Space.z[k,m+1,n,o+1]
        #                z[count,0,1,1]=self.Space.z[k,m,n+1,o+1]
        #                z[count,1,1,1]=self.Space.z[k,m+1,n+1,o+1]
                        
        #                theta[count,0,0,0]=self.Space.theta[k,m,n,o]
        #                theta[count,1,0,0]=self.Space.theta[k,m+1,n,o]
        #                theta[count,0,1,0]=self.Space.theta[k,m,n+1,o]
        #                theta[count,1,1,0]=self.Space.theta[k,m+1,n+1,o]
        #                theta[count,0,0,1]=self.Space.theta[k,m,n,o+1]
        #                theta[count,1,0,1]=self.Space.theta[k,m+1,n,o+1]
        #                theta[count,0,1,1]=self.Space.theta[k,m,n+1,o+1]
        #                theta[count,1,1,1]=self.Space.theta[k,m+1,n+1,o+1]
                        
        #                count=count+1
        
        return x, y, z, theta
        
    def boundary_connectivity(self):
        
        if self.Space.dim == 1:
            theta_bc    = np.zeros((self.noe_bc),int)
            physical_bc = np.zeros((self.noe_bc),int)
                        
            count = 0
            for k in range(self.Space.noe_bc):
                [i, phys, bc_type_gll, element_edge] = self.Space.theta_phys_bc(k)
                theta_bc[count] = self.Space.theta_bc[k]
                physical_bc[count] = phys
                count = count+1
            
        if self.Space.dim == 2:
            theta_bc    = np.zeros((self.noe_bc,self.n),int)
            physical_bc = np.zeros((self.noe_bc),int)
            #edge        = np.zeros((self.noe_bc, 2), int)
        
            count = 0
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n-1):
                    [i, phys, bc_type_gll, element_edge] = self.Space.theta_phys_bc(k,m)
                    theta_bc[count,0] = self.Space.theta_bc[k,m]
                    theta_bc[count,1] = self.Space.theta_bc[k,m+1]
                    physical_bc[count] = phys
                    #bc_type_fem.append(bc_type_gll)
                    #edge[count,0] = # internal element number
                    #edge[count,1] = element_edge[1]# edge
                    #if element_edge[1] == 0:
                    #    k_fem=element_edge[1]*
                    # k_fem=theta[k,m,0]
                    count = count+1
        
        if self.Space.dim == 3:
            theta_bc    = np.zeros((self.noe_bc,self.n,self.n),int)
            physical_bc = np.zeros((self.noe_bc),int)
            
            count = 0
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n-1):
                    for n in range(self.Space.n-1):
                        [i, phys, bc_type_gll, element_edge] = self.Space.theta_phys_bc(k,m,n)
                        theta_bc[count,0,0] = self.Space.theta_bc[k,m,n]
                        theta_bc[count,1,0] = self.Space.theta_bc[k,m+1,n]
                        theta_bc[count,0,1] = self.Space.theta_bc[k,m,n+1]
                        theta_bc[count,1,1] = self.Space.theta_bc[k,m+1,n+1]
                        
                        physical_bc[count] = phys
                        count = count+1
            
        return theta_bc, physical_bc
        
    def sem_to_fem(self,u_sem):
        '''
        A mapping from the SEM space to FEM space. 
        '''
        if self.dim == 1:
            u_fem = precond_f90.sem_to_fem_1d(u_sem,self.n,self.noe)
            #u_fem = np.zeros((self.noe,self.n),float)
            #count=0
            #for k in range(self.Space.noe):
            #    for i in range(self.Space.n-1):
            #        u_fem[count,0]=u_sem[k,i]
            #        u_fem[count,1]=u_sem[k,i+1]
            #        count=count+1
                        
        if self.dim == 2:
            u_fem = precond_f90.sem_to_fem_2d(u_sem,self.n,self.noe)
            #u_fem = np.zeros((self.noe,self.n,self.n),float)
            #count=0
            #for k in range(self.Space.noe):
            #    for i in range(self.Space.n-1):
            #        for j in range(self.Space.n-1):
            #            u_fem[count,0,0]=u_sem[k,i,j]
            #            u_fem[count,1,0]=u_sem[k,i+1,j]
            #            u_fem[count,0,1]=u_sem[k,i,j+1]
            #            u_fem[count,1,1]=u_sem[k,i+1,j+1]
            #            count=count+1
        if self.dim == 3:
            u_fem = precond_f90.sem_to_fem_3d(u_sem,self.n,self.noe)
            
        return u_fem
                                          
                                  

        
class Preconditioner:
    '''
    Preconditioner. 
        
    :param Space: Space
    :type Space: :class:`sempy.Space`
    :param Operators: A collection of operators
    :param scaling_factor: Scaling factors for operators in 
                           :literal:`Operators`.
    :param drop_tol: Drop tolerance for ILU
    :param string library: Either :literal:`superlu` or :literal:`umfpack`. 
    
    :attributes: * **matrix** - The preconditioner. A matrix that approximates the inverse of the SEM matrix.
    
    **Example**::
    
      import sempy
      
      X = sempy.Space( filename = 'square', n = 30, dim = 2 ) 
      laplace = sempy.operators.Laplacian( X, fem_assemble = 'yes' )
      
      A_fem = laplace.matrix_fem

      pre = sempy.precond.Preconditioner( X, [A_fem] , drop_tol = 0.5 )
      P = pre.matrix

     
    '''
    def __init__( self, Space, Operators, 
                  scaling_factor = 'none', drop_tol = 0.0,
                  library = 'superlu',silent = False ):
        
        
        self.Space = Space
        self.library = library
        self.silent = silent
        if scaling_factor=='none':
            self.scaling_factor = np.ones((len(Operators)),float)
        else:
            self.scaling_factor = scaling_factor
        self.drop_tol = drop_tol
        Q = sempy.operators.MultipleOperators(
                            Operators,
                            scaling_factor = self.scaling_factor,
                            assemble = 'yes',silent=self.silent ).matrix
        Q = self.__convert_to_ll_mat__(Q)
        if not self.silent:
            print ''
            print '**** Factorizing, pre         ****'
        
        if pysparse.__version__[2] >='2':
            if self.library == 'superlu':
                self.LU = direct.superlu.factorize( Q.to_csr(),
                                           drop_tol=self.drop_tol )
            if self.library == 'umfpack':
                self.LU = umfpack.factorize( Q )
                
        if pysparse.__version__[2] <='1':
            self.LU = pysparse.superlu.factorize(Q.to_csr(),
                                                 drop_tol=self.drop_tol)
        if not self.silent:
            print '**** Non-zero entries=',self.LU.nnz
        del Q
        self.matrix = spl.LinearOperator( 
                                (self.Space.dof,self.Space.dof),
                                matvec = self.__action__, 
                                dtype = 'float' )
    
    def __convert_to_ll_mat__(self,A):
        Q = pysparse.spmatrix.ll_mat( self.Space.dof, self.Space.dof )
                
        val,irow,jcol = A.find()
        Q.update_add_at(val,irow,jcol)
        del val,irow,jcol
        
        if self.Space.dim == 1:
            for k in range(self.Space.noe_bc):
                [i, phys, bc_type, element_edge] = \
                                        self.Space.theta_phys_bc(k)
                if bc_type == "Dir":
                    Q[int(i),int(i)] = 1.0
                    
        if self.Space.dim == 2:
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n):
                    [i, phys, bc_type, element_edge] = \
                                        self.Space.theta_phys_bc(k,m)
                    if bc_type == "Dir":
                        Q[int(i),int(i)] = 1.0
                        
        if self.Space.dim == 3:
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n):
                    for n in range(self.Space.n):
                        [i, phys, bc_type, element_edge] = \
                                        self.Space.theta_phys_bc(k,m,n)
                        if bc_type == "Dir":
                            Q[int(i),int(i)] = 1.0
                        
        return Q
        
    def __action__(self,v):
        w = np.zeros(self.Space.dof, float)
        self.LU.solve(v,w)
        return w

                           
#class PressurePrecond:
#    def __init__(self,Space,SpaceGL):
#        self.Space = Space
#        self.SpaceGL = SpaceGL
#        
#        # Laplacian
#        self.lap = sempy.operators.Laplacian( self.Space, 
#                                              mask = 'no',
#                                              fem_assemble = 'yes' )
#        #self.A = self.lap.matrix
#        self.A = self.lap.matrix_fem
#        self.A_pre = sempy.precond.Preconditioner( self.Space, 
#                                                   [self.A], 
#                                                   library = 'superlu',
#                                                   drop_tol = 1.0 ).matrix
#        self.poisson_solver = sempy.linsolvers.Krylov(
#                                                tol = 1.0e-16,
#                                                solver_type = 'cg')
#        #self.matrix =
#        self.x = np.zeros((self.Space.dof),float)
#        self.matrix = spl.LinearOperator( 
#                          ( self.Space.dof,self.Space.dof ),
#                            matvec = self.__action_pre__,
#                            dtype = 'float' )
#        
#    def __action_pre__(self,v):
#        t1=time.time()
#        self.x[:] = 0.0
#        #[x,flag] = self.poisson_solver.solve(self.A,v,self.x)
#        x=self.A_pre*v
#        t2=time.time()
#        print 'pre. ex time=',t2-t1#,'iter=',flag
#        
#        return x
        
 