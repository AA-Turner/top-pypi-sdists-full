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
import scipy.sparse.linalg as spl


class Laplacian1D():
    '''
    The Laplace operator.
    '''
    def __init__(self,Mesh,mu,assemble='no'):
        self.mu   = mu
        self.Mesh = Mesh
        self.g11 = self.geometric()
        if assemble == 'no':
            self.matrix=spl.LinearOperator( (self.Mesh.dof,self.Mesh.dof),\
                                            matvec=self.action_python,dtype='float')    
        #if assemble == 'yes':
    
    def geometric(self):
        w = np.zeros((self.Mesh.noe,self.Mesh.n),float)
        g11=1.0/self.Mesh.jac
        return g11
        
    def action_python(self,v_in):
        w = np.zeros((self.Mesh.noe,self.Mesh.n),float)
        u = self.Mesh.mapping_q(v_in)
        for k in range(self.Mesh.noe):
            for m in range(self.Mesh.n):
                for n in range(self.Mesh.n):
                    for alpha in range(self.Mesh.n):
                        w[k,m]=w[k,m]+self.Mesh.weights[alpha]*self.g11[k,alpha]\
                                     *self.mu[k,alpha]\
                                     *self.Mesh.D[alpha,n]*self.Mesh.D[alpha,m]*u[k,n]
        # Mapping
        v_out=self.Mesh.mapping_qt(w)
        # Mask
        v_out = self.Mesh.mask(v_out)
        return v_out
    
#    def action(self,v):
#        # Mapping from global to local
#        u = self.Mesh.mapping_Q(v)
#        # Matrix-vector product
#        w = fortrancode.action_of_laplacian(u,self.mu,self.Mesh.weights,self.Mesh.jac,self.Mesh.D)
#        # Mapping from local to global
#        w_out = self.Mesh.mapping_QT(w)
#        # Mask
#        w_out = self.Mesh.mask(w_out)
#        return w_out
        
#    def action_assemble(self):
#        print 'assemble sem...'
#        nz = self.Mesh.noe * self.Mesh.n * self.Mesh.n
#
#        weights = self.Mesh.weights
#        D   = self.Mesh.D
#        mu  = self.mu
#        g11 = self.g11
#        
#        nz_b=self.Mesh.noe * self.Mesh.n * self.Mesh.n
#        irow,jcolumn,value = fortrancode.assemble_full(weights,mu,g11,D,self.Mesh.theta,nz_b)
#        A = pysparse.spmatrix.ll_mat(self.Mesh.dof, self.Mesh.dof, nz)
#        for k in range(len(value)):
#            i=int(irow[k])
#            j=int(jcolumn[k])
#            A[i,j]=A[i,j]+value[k]
#        # Mask
#        for k in range(self.Mesh.noe_bc):
#            [i, phys, bc_type, element_edge]=self.Mesh.theta_phys_bc(k)
#            if bc_type == "Dir":
#                A[int(i),:] = 0.0
#        t2 = time.clock()
#        print '...assemble time=',t2-t1
#        print 'A.nz=',A.nnz
#        print '...assemble sem'
#        return A 

class Mass1D():
    '''
    The mass matrix.
    
    :param Mesh: An object of one of the mesh classes
    
    :attributes: *matrix* - Returns the mass matrix :math:`M\in \\mathbb R^{dof\\times dof}`. Since 
                              this matrix is diagonal it is always assembled. 
    
    Usage::
    
      import sempy
      
      B=Mass(mesh).matrix
      
    :todo: * inverse mass matrix.
      
    '''
    def __init__(self,Mesh):
        self.Mesh = Mesh
        self.matrix = spl.LinearOperator( (self.Mesh.dof,self.Mesh.dof),\
                                           matvec=self.action,dtype='float') 
        
    def action(self,u):
        w=np.zeros((self.Mesh.noe,self.Mesh.n),float)
        u_local = self.Mesh.mapping_Q(u)
        for k in range(self.Mesh.noe):
            for m in range(self.Mesh.n):
                w[k,m] = self.Mesh.weights[m] * self.Mesh.jac[k,m] * u_local[k,m]
        # Gather
        w_out = self.Mesh.mapping_qt(w)
        # Mask
        w_out = self.Mesh.mask(w_out)
        return w_out
        
    def action_of_matrix(self,f):
        '''
        Action of the mass matrix on a set of basis coefficients given in local data
        representation. 
        
        :param f: set of basis coefficients given in local data representation. 
        
        This is useful for functions in :math:`L^2(\\Omega)`
        
        Usage::
        
          import sempy
          
          f = np.ones((mesh.noe,mesh.n,mesh.n),float)
          F = Mass(mesh).action_of_matrix(f)
          
        '''
        w=np.zeros((self.Mesh.noe,self.Mesh.n),float)
        for k in range(self.Mesh.noe):
            for m in range(self.Mesh.n):
                w[k,m] = self.Mesh.weights[m] * self.Mesh.jac[k,m] * f[k,m]
        # Gather
        w_out = self.Mesh.mapping_qt(w)
        # Mask
        w_out = self.Mesh.mask(w_out)
        return w_out
