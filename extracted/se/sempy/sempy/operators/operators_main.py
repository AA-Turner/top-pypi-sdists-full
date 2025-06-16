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

import scipy.sparse.linalg as spl
import scipy.sparse as sps
import numpy as np
import operators_f90
# Pysparse
import pysparse
# Compatibility with older versions
if int(pysparse.__version__[2]) >=2:
    from pysparse.sparse.pysparseMatrix import PysparseMatrix #as pysparseMatrix
    
if int(pysparse.__version__[2]) <=1:
    from pysparse.pysparseMatrix import PysparseMatrix
#from pysparse import pysparseMatrix
import time

import sempy

#import PyTrilinos.Epetra as Epetra


class Laplacian():
    '''
    The Laplace operator. 
       
    :param Space: Discrete space.
    :type Space: :class:`sempy.Space`
    :param mu: Transport coefficient, such as viscosity or thermal conductivity. 
    :type mu: :class:`sempy.Function`
    :param g_neu: Neumann boundary conditions.
    :type g_neu: :class:`sempy.BoundaryFunction`
    :param g_rob: Robin boundary conditions.
    :type g_rob: :class:`sempy.BoundaryFunction`
    :param u_infty: Robin boundary conditions.
    :type u_infty: :class:`sempy.BoundaryFunction`
    :param mask: If :literal:`mask='yes'` the matrix is masked according to 
                 strong boundary conditions. If :literal:`mask='no'` the
                 matrix is not masked (results in Neumann-Laplace matrix 
                 operator).  The mask flag has only effect on the matrix free 
                 method and the linear_form. 
    :type mask: string
    :param string assemble: If :literal:`assemble='no'` (default) the method 
                            is matrix free. For :literal:`assemble = 'yes'` 
                            the stiffness matrix is assembled and stored in 
                            the CSR format. The latter might be used with care 
                            for high values of :attr:`sempy.Space.n` 
                            and :attr:`sempy.Space.noe` as the SEM Laplacian 
                            is elementwise full. 
    :param string fem_assemble: If :literal:`assemble = 'yes'` the 
                                corresponding FEM matrix is assembled.  
    
    :attributes: * **matrix** (LinearOperator or PysparseMatrix ) - Returns 
                   the stiffness matrix  
                   :math:`A\in \\mathbb R^{\\text{dof}\\times\\text{dof}}`. 
                   Wether *matrix* holds any data at all depends on the 
                   :literal:`assemble` paramter above.
                 * **linear_form** (array) - Returns a one dimensional array 
                   of length :attr:`sempy.Space.dof`  
                   (global degrees of freedom).
                 * **matrix_fem** (LinearOperator or PysparseMatrix ) - The 
                   finite element matrix based on the same nodal points 
                   as the GLL mesh.

    This class supplies the stiffness :literal:`matrix` and 
    the :literal:`linear_form` resulting from applying SEM to the Laplace 
    operator. 
    
    .. math::
       -\\int_{\\Omega}(\\nabla\\cdot\\mu\\nabla u)v d\\Omega =
       \\int_{\\Omega} \\mu\\nabla u\\cdot \\nabla v d\\Omega -
       \\int_{\\Gamma} (\\mu\\nabla u\cdot\mathbf n )vd\\Gamma
       
    Three different boundary conditions are associated with the Laplacian, 
    the Dirichlet, the Neumann and the Robin boundary conditions, i.e.:
    
    .. math::
       u=u_\\text{dir}\quad\\text{(Dirichlet)}
       
       \\mu(\\partial u/\\partial n)|_{\\Gamma}=g_\\text{neu}
       \quad\\text{(Neumann)}
       
       \\mu(\\partial u/\\partial n)|_{\\Gamma}=g_\\text{rob}(u_{\\infty}-u)
       \quad\\text{(Robin)}
    
    which, when inserted into the above equation gives   
    
    .. math::
       -\\int_{\\Omega}(\\nabla\\cdot\\mu\\nabla u)v d\\Omega =
       \\underbrace{\\int_{\\Omega} \\mu\\nabla u\\cdot \\nabla v 
       +\\int_{\\Gamma_{rob}} g_\\text{rob}uvd\\Gamma}_{a(u,v) \\rightarrow Au}
       -\\underbrace{\\bigg(\\int_{\\Gamma_\\text{neu}} g_\\text{neu}vd\\Gamma 
       +\\int_{\\Gamma_\\text{rob}} g_\\text{rob}u_\\infty vd\\Gamma\\bigg)}_{l(v) \\rightarrow f}
       
      
    Dirichlet conditions are attached to the trial function (an instance of 
    the class :class:`sempy.Function`). Natural boundary conditions, on the 
    other hand, have to be supplied explicitly when creating an instance of 
    this class, i.e. :literal:`g_neu`, :literal:`g_rob`, 
    :literal:`u_infty`. 
    
    
                
    **Example**::
           
       import sempy
       
       X = sempy.Space( 'square.msh', n = 5, dim = 2 )
       mu = sempy.Function( X, basis_coeff = 1.0 )
       laplacian = sempy.operators.Laplacian( X, mu )
       A = laplacian.matrix
       f = laplacian.linear_form
    
    '''
    def __init__(self, Space, mu='none', g_neu='none', g_rob='none',\
                 u_infty='none', assemble='no' ,fem_assemble = 'no',
                 mask = 'yes',silent=False):
    #def __init__(self, Space, mu='none', g_neu='none', g_rob='none',\
    #             u_infty='none', assemble='no', SpaceFEM='none'):
        self.Space = Space
        self.assemble = assemble
        self.fem_assemble = fem_assemble
        #self.SpaceFEM = SpaceFEM
        self.mask = mask
        self.silent=silent
        
        if mu == 'none':
            self.mu = sempy.Function(self.Space, basis_coeff = 1.0)
        else:
            self.mu = mu
                
        if g_neu == 'none':
            self.g_neu = sempy.BoundaryFunction(self.Space)
        else:
            self.g_neu = g_neu
                
        if g_rob == 'none':
            self.g_rob = sempy.BoundaryFunction(self.Space)
        else:
            self.g_rob = g_rob
             
        if u_infty == 'none':
            self.u_infty = sempy.BoundaryFunction(self.Space)
        else:
            self.u_infty = u_infty
        
        if self.Space.dim == 1:
                       
            self.g11 = 1.0/self.Space.jac
            if self.assemble == 'no':
                self.matrix = spl.LinearOperator( (self.Space.dof,self.Space.dof),\
                                 matvec=self.__action_1d,dtype='float')    
            if self.assemble == 'yes':
                self.matrix = self.__assemble_1d()
                self.matrix.dtype='float64'
            self.linear_form = self.__rhs_1d()

        if self.Space.dim == 2:
                      
            self.g11, self.g12, \
            self.g21, self.g22   = \
                operators_f90.geometric_laplacian_2d(self.Space.x,self.Space.y,\
                                                self.Space.jac,self.Space.D)
            if self.assemble == 'no':
                self.matrix = spl.LinearOperator( (self.Space.dof,self.Space.dof),\
                                         matvec=self.__action_2d,dtype='float')    
            if self.assemble == 'yes':
                self.matrix = self.__assemble_2d()
                self.matrix.dtype='float64'
            self.linear_form = self.__rhs_2d()
            
        
        
        if self.Space.dim == 3:
            self.g11, self.g12, self.g13,\
            self.g21, self.g22, self.g23,\
            self.g31, self.g32, self.g33=\
                operators_f90.geometric_laplacian_3d(self.Space.x,self.Space.y,self.Space.z,\
                                                     self.Space.jac,self.Space.D)
            if self.assemble == 'no':
                self.matrix = spl.LinearOperator( (self.Space.dof,self.Space.dof),\
                                        matvec=self.__action_3d,dtype='float')  
            if self.assemble == 'yes':
                self.matrix = self.__assemble_3d()
                self.matrix.dtype='float64'
                
            self.linear_form = self.__rhs_3d()     
        
        # FEM matrix
        #if self.SpaceFEM == 'none':
        if self.fem_assemble == 'no':
            self.matrix_fem = 'none'
        #if not self.SpaceFEM == 'none':
        if self.fem_assemble == 'yes':
            #self.matrix_fem = 
            self.assemble_fem()
        
        # remove?
        self.matrix.Space = self.Space
        
            
    def assemble_fem(self):
        '''
        Assembles the FEM matrix used for preconditioning.
        
        Usage::
        
           import sempy 

           X = sempy.Space( filename = 'square', n = 10, dim = 2 )
           
           laplace = sempy.operators.Laplacian( X, assemble='yes',fem_assemble='yes')

           A = laplace.matrix
           A_fem = laplace.matrix_fem

           print 'Non-zero entries in A=', A.nnz
           print 'Non-zero entries in A_fem=',A_fem.nnz
            
        '''
        #basis_coeff = self.SpaceFEM.sem_to_fem( self.mu.basis_coeff )
        #mu_fem = sempy.Function( self.SpaceFEM, basis_coeff = basis_coeff )
        ##A_fem = Laplacian( self.SpaceFEM, mu = mu_fem, 
        ##                   assemble = 'yes').matrix
        #self.matrix_fem = Laplacian( self.SpaceFEM, mu = mu_fem, 
        #                   assemble = 'yes').matrix
        ##
        basis_coeff = self.Space.fem.sem_to_fem( self.mu.basis_coeff )
        mu_fem = sempy.Function( self.Space.fem, basis_coeff = basis_coeff )
        self.matrix_fem = Laplacian( self.Space.fem, mu = mu_fem, 
                           assemble = 'yes',
                           mask = self.mask).matrix                   
        #return A_fem
        
        
    def assemble_matrix(self):
        '''
        Assembles the stiffness matrix.
        
        Usage::
        
          import sempy 
      
          X = sempy.Space( filename = 'square_neumann', n = 3, dim = 2 )

          laplacian = sempy.operators.Laplacian( X )
          laplacian.assemble_matrix()
          A = laplacian.matrix 
        '''
        if self.Space.dim == 1:
                self.matrix = self.__assemble_1d()
                self.matrix.dtype='float64'
                
        if self.Space.dim == 2:
            self.matrix = self.__assemble_2d()
            self.matrix.dtype='float64'
            
        if self.Space.dim == 3:
                self.matrix = self.__assemble_3d()
                self.matrix.dtype='float64'
        return 
    
    def __action_1d(self,v_in):
        u = self.Space.mapping_q(v_in)
        # Local matrix vector product w_L=A_L*v_L
        w = operators_f90.action_of_laplacian_1d(u,self.mu.basis_coeff,\
                                                 self.Space.weights,\
                                                 self.g11,self.Space.D)
        # Mapping
        v_out = self.Space.mapping_qt(w)
        # Robin
        for k in range(self.Space.noe_bc):
            i = self.Space.theta_bc[k]
            v_out[i] = v_out[i] + self.g_rob.basis_coeff[k]*v_in[i]
        # Mask
        if self.mask == 'yes':
            v_out = self.Space.mask(v_out)
            
        return v_out
    
    def __action_2d(self,v_in):
        u = self.Space.mapping_q(v_in)
        # Local matrix vector product w_L=A_L*v_L
        w = operators_f90.action_of_laplacian_2d(u, self.mu.basis_coeff, \
                                                 self.Space.weights, self.Space.D,\
                                                 self.g11, self.g12, self.g21, self.g22)
        # Mapping
        v_out = self.Space.mapping_qt(w)
        # Robin
        v_out = operators_f90.action_of_laplacian_2d_robin(v_out,v_in,self.Space.theta_bc,\
                    self.Space.weights,self.Space.jac_s,self.g_rob.basis_coeff)
        # Mask
        if self.mask == 'yes':
            v_out = self.Space.mask(v_out)
            
        return v_out
    
    def __action_3d(self,v_in):
        u = self.Space.mapping_q(v_in)
        # Local matrix vector product w_L=A_L*v_L
        w = operators_f90.action_of_laplacian_3d(u,self.mu.basis_coeff,self.Space.weights,\
                                                 self.Space.D,\
                                                 self.g11,self.g12,self.g13,\
                                                 self.g21,self.g22,self.g23,\
                                                 self.g31,self.g32,self.g33)
        # Mapping
        v_out = self.Space.mapping_qt(w)
        # Robin
        v_out = operators_f90.action_of_laplacian_3d_robin(v_out,v_in,self.Space.theta_bc,\
                    self.Space.weights,self.Space.jac_s,self.g_rob.basis_coeff)
        # Mask
        if self.mask == 'yes':
            v_out = self.Space.mask(v_out)
            
        return v_out
        
        
    def __assemble_1d(self):
        '''
        assemble
        '''
        if not self.silent:
            print ''
            print '**** Assemble Laplacian       ****'
        nz = self.Space.noe * self.Space.n * self.Space.n
        
        #A = pysparse.spmatrix.ll_mat(self.Space.dof, self.Space.dof, nz)
        #A = sps.lil_matrix((self.Space.dof, self.Space.dof), dtype='float')
        #A = pysparseMatrix.PysparseMatrix(size=self.Space.dof)#,dtype=float)
        A = PysparseMatrix(size=self.Space.dof)#,dtype=float)
        #A = sps.lil_matrix(B)#,shape=(self.Space.dof, self.Space.dof), dtype='float')
        t1 = time.clock()
        irow,jcolumn,value = \
            operators_f90.assemble_laplacian_1d(self.Space.weights,self.mu.basis_coeff,\
                                                self.g11,self.Space.D,\
                                                self.Space.theta,nz)
        
        # Assign values
        for k in range(len(value)):
            i = int(irow[k])
            j = int(jcolumn[k])
            A[i,j] = A[i,j] + value[k]
        # Robin
        for k in range(self.Space.noe_bc):
            i = int(self.Space.theta_bc[k])
            A[i,i] = A[i,i] + self.g_rob.basis_coeff[k]
        # Mask
        A = self.Space.mask_matrix(A)
        t2 = time.clock()
        if not self.silent:
            print '**** ex. time=',t2-t1,'nnz=',A.nnz
            
        return A
        
    
        
    def __assemble_2d(self):
        
        if not self.silent:
            print ''
            print '**** Assemble Laplacian       ****'
        t1 = time.clock()
        
        # Local comnectivity array
        theta_local = np.zeros((self.Space.n, self.Space.n),int)
        count =0
        for m in range(self.Space.n):
            for n in range(self.Space.n):
                theta_local[m,n]=count
                count=count+1

        # Mask array
        
        mask   = np.zeros((self.Space.noe,self.Space.n,self.Space.n),int)
        if self.mask == 'yes':
            mask_g = np.zeros((self.Space.dof),int)
            for k in range(self.Space.noe_bc):
                for m in range(self.Space.n):
                    [i, phys, bc_type, edge] = self.Space.theta_phys_bc(k,m)
                    if bc_type == "Dir":
                        mask_g[i] = 1
                        
            for k in range(self.Space.noe):
                for m in range(self.Space.n):
                    for n in range(self.Space.n):
                        i = self.Space.theta[k,m,n]
                        mask[k,m,n] = mask_g[i]
            del mask_g
                
        # Matrix
        #A = pysparseMatrix.PysparseMatrix(size=self.Space.dof)#, sizeHint=nz)
        A = PysparseMatrix(size=self.Space.dof)#, sizeHint=nz)
                
        # Local degrees of freedom
        nz = self.Space.n*self.Space.n
        
        # Assemble stiffness matrix elementwize
        for k in range(self.Space.noe):
            val, row, col = operators_f90.assemble_laplacian_2d_new(
                                        self.Space.weights,
                                        self.mu.basis_coeff[k,:,:],
                                        self.g11[k,:,:], self.g12[k,:,:],
                                        self.g21[k,:,:], self.g22[k,:,:],
                                        self.Space.D,
                                        self.Space.theta[k,:,:],
                                        theta_local, mask[k,:,:], nz)
            val = np.reshape(val, nz*nz)
            row = np.reshape(row, nz*nz)
            col = np.reshape(col, nz*nz)
            A.addAt(val,row,col)
                
        # Add Robin contribution
        for k in range(self.Space.noe_bc):
            for m in range(self.Space.n):
                [i, phys, bc_type, element_edge]=self.Space.theta_phys_bc(k,m)
                if element_edge[1] == 0:
                    I=self.Space.theta[element_edge[0],m,0]
                if element_edge[1] == 1:
                    I=self.Space.theta[element_edge[0],m,self.Space.n-1]
                if element_edge[1] == 2:
                    I=self.Space.theta[element_edge[0],0,m]
                if element_edge[1] == 3:
                    I=self.Space.theta[element_edge[0],self.Space.n-1,m]
                J=i
                A[int(I),int(J)] = A[int(I),int(J)] + \
                                   self.Space.weights[m]*self.Space.jac_s[k,m]*\
                                   self.g_rob.basis_coeff[k,m]   
        # Mask
        #print '**** nnz=',A.nnz
        #t1_m = time.clock()    
        #A = self.Space.mask_matrix(A)
        #t2_m = time.clock()    
        t2 = time.clock()    
        #print '**** assemble time=',t2_f-t1_f
        #print '**** robin    time=',t2_r-t1_r
        #print '**** mask     time=',t2_m-t1_m
        if not self.silent:
            print '**** assemble time=',t2-t1
            print '**** nnz=',A.nnz
        return A
    
    def __assemble_3d(self):
        
        if not self.silent:
            print ''
            print '**** Assemble Laplacian       ****'
        
        # Local comnectivity array
        theta_local = np.zeros((self.Space.n, self.Space.n, self.Space.n),int)
        count =0
        for k in range(self.Space.n):
            for m in range(self.Space.n):
                for n in range(self.Space.n):
                    theta_local[k,m,n]=count
                    count=count+1
                    
        # Mask array
        mask   = np.zeros((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),int)
        mask_g = np.zeros((self.Space.dof),int)
        for k in range(self.Space.noe_bc):
            for m in range(self.Space.n):
                for n in range(self.Space.n):
                    [i, phys, bc_type, edge] = self.Space.theta_phys_bc(k,m,n)
                    if bc_type == "Dir":
                        mask_g[i] = 1
                        
        for k in range(self.Space.noe):
            for m in range(self.Space.n):
                for n in range(self.Space.n):
                    for o in range(self.Space.n):
                        i = self.Space.theta[k,m,n,o]
                        mask[k,m,n,o] = mask_g[i]
        del mask_g                
        
        # Matrix
        #A = pysparseMatrix.PysparseMatrix(size=self.Space.dof)#, sizeHint=nz)
        A = PysparseMatrix(size=self.Space.dof)#, sizeHint=nz)
        
        # Local degrees of freedom
        nz =  self.Space.n*self.Space.n*self.Space.n
        t1 = time.clock()
        
        # Assemble the stiffness matrix, elementwize.
        t1_f = time.clock()    
        for k in range(self.Space.noe):
            val,row,col = \
                operators_f90.assemble_laplacian_3d(self.Space.weights,self.mu.basis_coeff[k,:,:,:],\
                                 self.g11[k,:,:,:],self.g12[k,:,:,:],self.g13[k,:,:,:],\
                                 self.g21[k,:,:,:],self.g22[k,:,:,:],self.g23[k,:,:,:],\
                                 self.g31[k,:,:,:],self.g32[k,:,:,:],self.g33[k,:,:,:],\
                                 self.Space.D,self.Space.theta[k,:,:,:],theta_local,mask[k,:,:,:],nz)
            val = np.reshape(val, nz*nz)
            row = np.reshape(row, nz*nz)
            col = np.reshape(col, nz*nz)
            A.addAt(val,row,col)
            
        t2_f = time.clock()    
        # Add Robin contribution
        t1_r = time.clock()    
        for k in range(self.Space.noe_bc):
            for m in range(self.Space.n):
                for n in range(self.Space.n):
                    [i, phys, bc_type, element_edge] = self.Space.theta_phys_bc(k,m,n)
                    if element_edge[1] == 0:
                        I = self.Space.theta[element_edge[0],m,n,0]
                    if element_edge[1] == 1:
                        I = self.Space.theta[element_edge[0],m,n,self.Space.n-1]
                    if element_edge[1] == 2:
                        I = self.Space.theta[element_edge[0],m,0,n]
                    if element_edge[1] == 3:
                        I = self.Space.theta[element_edge[0],m,self.Space.n-1,n]
                    if element_edge[1] == 4:
                        I = self.Space.theta[element_edge[0],0,m,n]
                    if element_edge[1] == 5:
                        I = self.Space.theta[element_edge[0],self.Space.n-1,m,n]
                    J = i
                    A[int(I),int(J)] = A[int(I),int(J)] + \
                                       self.Space.weights[m]*self.Space.weights[n]*\
                                       self.Space.jac_s[k,m,n]*\
                                       self.g_rob.basis_coeff[k,m,n]
        t2_r = time.clock()    
        # Mask
        if not self.silent:
            print '**** Number of nnz=',A.nnz
        #t1_m = time.clock()    
        #A = self.Space.mask_matrix(A)
        #t2_m = time.clock()    
        t2 = time.clock()
        #print '**** post mask nnz=',A.nnz
        if not self.silent:
            print '**** assemble time=',t2_f-t1_f
            print '**** robin    time=',t2_r-t1_r
            #print '**** mask     time=',t2_m-t1_m
            print '**** total    time=',t2-t1#,'nnz=',A.nnz
        
        return A
    
            
    def __rhs_1d(self):
        f = np.zeros((self.Space.dof), float)
        # Contributions from Neumann conditions
        for k in range(self.Space.noe_bc):
            i = self.Space.theta_bc[k]
            f[i] = f[i] + self.g_neu.basis_coeff[k]
        # Contributions from Robin conditions
        for k in range(self.Space.noe_bc):
            i = self.Space.theta_bc[k]
            f[i] = f[i] + self.g_rob.basis_coeff[k]*self.u_infty.basis_coeff[k]
        # Mask Dirichlet boundary points
        if self.mask == 'yes':
            f = self.Space.mask(f)
        return f
        
    def __rhs_2d(self):
        f = np.zeros((self.Space.dof), float)
        # Contributions from Neumann conditions
        for k in range(self.Space.noe_bc):
            for m in range(self.Space.n):
                i = self.Space.theta_bc[k,m]
                f[i] = f[i] + self.Space.weights[m]*self.Space.jac_s[k,m]*\
                              self.g_neu.basis_coeff[k,m]
        # Contributions from Robin conditions
        for k in range(self.Space.noe_bc):
            for m in range(self.Space.n):
                i = self.Space.theta_bc[k,m]
                f[i] = f[i] + self.Space.weights[m]*self.Space.jac_s[k,m]*\
                              self.g_rob.basis_coeff[k,m]*\
                              self.u_infty.basis_coeff[k,m]
        # Mask Dirichlet boundary points
        if self.mask == 'yes':
            f = self.Space.mask(f)
        return f
    
    def __rhs_3d(self):
        #f = np.zeros((self.Space.dof), float)
        # Contributions from Neumann conditions
        #for k in range(self.Space.noe_bc):
        #    for m in range(self.Space.n):
        #        for n in range(self.Space.n):
        #            i = self.Space.theta_bc[k,m,n]
        #            f[i] = f[i] + self.Space.weights[m]*self.Space.weights[n]*\
        #                          self.Space.jac_s[k,m,n]*self.g_neu.basis_coeff[k,m,n]
        # Contributions from Robin conditions
        #for k in range(self.Space.noe_bc):
        #    for m in range(self.Space.n):
        #        for n in range(self.Space.n):
        #            i = self.Space.theta_bc[k,m,n]
        #            f[i] = f[i] + self.Space.weights[m]*self.Space.weights[n]*\
        #                          self.Space.jac_s[k,m,n]*\
        #                          self.g_rob.basis_coeff[k,m,n]*self.u_infty.basis_coeff[k,m,n]
        # 
        f = np.zeros(self.Space.dof, float)
        if self.Space.noe_bc > 0:
            f = operators_f90.assemble_linear_form_3d( \
                                self.Space.theta_bc,
                                self.Space.weights,\
                                self.Space.jac_s,\
                                self.g_rob.basis_coeff,\
                                self.u_infty.basis_coeff,\
                                self.g_neu.basis_coeff,self.Space.dof)
        # Mask Dirichlet boundary points
        if self.mask == 'yes':
            f = self.Space.mask(f)
        return f
        
    def assemble_linear_form(self):
        '''
        Assembles the linear form.
        '''
        
        if self.Space.dim == 1:
            f = self.__rhs_1d()
        if self.Space.dim == 2:
            f = self.__rhs_2d()
        if self.Space.dim == 3:
            f = self.__rhs_3d()
        return f
        
        
        
class Convection:
    '''
    The convection operator. 
    
    :param Space: The function space.
    :type Space: :class:`sempy.Space`
    :param u_conv: Convecting velocity field.
    :type u_conv: A list of :class:`sempy.Function` instances
    :param string assemble: A boolean argument controlling the assembly 
                            of the matrix. If :literal:`assemble = 'yes'`
                            the matrix is assembled and if 
                            :literal:`assemble = 'no'` the 
                            :literal:`matrix` only performs the action of 
                            the matrix. 
    :param string fem_assemble:  If :literal:`assemble = 'yes'` the 
                                 corresponding FEM matrix is assembled.  
             
    :attributes: * **matrix** - A matrix in the Pysparse format 
                   (:literal:`assemble = 'yes'`) or an instance of the class
                   :class:`scipy.sparse.linalg.LinearOperator` 
                   (:literal:`assemble = 'no'`). 
                 * **matrix_fem** - The corresponding FEM matrix.
    
    .. :todo: Option to controll conservative/non-conservative form.
    
    **Example**::
    
        import sempy
        
        X = sempy.Space( 'square', n = 10, dim = 2 )
        
        # Convecting velocity field
        u = sempy.Function( X, basis_coeff = 1.0 )
        v = sempy.Function( X, basis_coeff = 1.0 )
        U = [ u, v ]
        
        conv = sempy.operators.Convection( X, u_conv = U,
                                           assemble = 'yes',
                                           fem_assemble = 'yes' )
        # Convection matrix
        C = conv.matrix
        C_fem = conv.matrix_fem
    
    '''
    def __init__(self,Space,u_conv='none',assemble='no',
                 fem_assemble = 'no', silent = False ):
        self.Space = Space
        self.dim = self.Space.dim
        self.silent = silent
        
        if u_conv == 'none':
            if self.Space.dim == 1:
                _u = sempy.Function(self.Space, basis_coeff = 1.0)
                self.u_conv = [ _u.basis_coeff ]
            if self.Space.dim == 2:
                _u = sempy.Function(self.Space, basis_coeff = 1.0)
                _v = sempy.Function(self.Space, basis_coeff = 1.0)
                self.u_conv = [ _u.basis_coeff, _v.basis_coeff ]
            if self.Space.dim == 3:
                _u = sempy.Function(self.Space, basis_coeff = 1.0)
                _v = sempy.Function(self.Space, basis_coeff = 1.0)
                _w = sempy.Function(self.Space, basis_coeff = 1.0)
                self.u_conv = [ _u.basis_coeff, _v.basis_coeff, _w.basis_coeff ]
        else:
            if self.Space.dim == 1:
                self.u_conv=[ u_conv[0].basis_coeff ]
            if self.Space.dim == 2:
                self.u_conv=[ u_conv[0].basis_coeff,
                          u_conv[1].basis_coeff ]
            if self.Space.dim == 3:
                self.u_conv=[ u_conv[0].basis_coeff,
                          u_conv[1].basis_coeff,
                          u_conv[2].basis_coeff ]
             
        self.assemble = assemble
        self.fem_assemble = fem_assemble
        #self.SpaceFEM = self.Space.fem
        
        if self.dim == 1:
            if self.assemble == 'no':
                self.matrix = spl.LinearOperator( (self.Space.dof,self.Space.dof),\
                                    matvec=self.__action_1d,dtype='float')  
            if self.assemble == 'yes':
                self.matrix = self.__assemble_1d()
            
        
        if self.dim == 2:
            self.g11,self.g12,self.g21,self.g22=\
               operators_f90.geometric_convection_2d(self.Space.x,
                                                     self.Space.y,
                                                     self.Space.D)
            if self.assemble == 'no':
                self.matrix = spl.LinearOperator( (self.Space.dof,self.Space.dof),\
                                               matvec=self.__action_2d,
                                                   dtype='float')  
            if self.assemble == 'yes':
                self.matrix = self.__assemble_2d()
        
        if self.dim == 3:
            self.g11 = np.zeros((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),
                                float)
            self.g12 = np.zeros((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),
                                float)
            self.g13 = np.zeros((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),
                                float)
            self.g21 = np.zeros((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),
                                float)
            self.g22 = np.zeros((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),
                                float)
            self.g23 = np.zeros((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),
                                float)
            self.g31 = np.zeros((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),
                                float)
            self.g32 = np.zeros((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),
                                float)
            self.g33 = np.zeros((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),
                                float)
            
            for k in range(self.Space.noe):
                self.g11[k,:,:,:],self.g12[k,:,:,:],self.g13[k,:,:,:],\
                self.g21[k,:,:,:],self.g22[k,:,:,:],self.g23[k,:,:,:],\
                self.g31[k,:,:,:],self.g32[k,:,:,:],self.g33[k,:,:,:] =\
                    operators_f90.geometric_convection_3d(self.Space.x[k,:,:,:],
                                                          self.Space.y[k,:,:,:],
                                                          self.Space.z[k,:,:,:],
                                                          self.Space.D)
            # Weights array
            self.W=np.zeros((self.Space.n,self.Space.n,self.Space.n))
            for i in range(self.Space.n):
                for j in range(self.Space.n):
                    for k in range(self.Space.n):
                        self.W[i,j,k]=self.Space.weights[i]*self.Space.weights[j]*self.Space.weights[k]
                    
            if self.assemble == 'no':
                self.matrix = spl.LinearOperator( (self.Space.dof,self.Space.dof),
                                    matvec=self.__action_3d,dtype='float')  
            if self.assemble == 'yes':
                self.matrix = self.__assemble_3d()
        
        #if not self.SpaceFEM == 'none':
        if not self.fem_assemble == 'no':
            #self.matrix_fem = self.assemble_fem()
            self.assemble_fem()
        else:
            self.matrix_fem = 'none'
    
    def assemble_matrix(self):
        '''
        Assembles the stiffness matrix.
        
        Usage::
        
          import sempy 
      
          X = sempy.Space( filename = 'square', n = 3, dim = 2 )

          conv = sempy.operators.Convection( X )
          conv.assemble_matrix()
          C = conv.matrix 
        '''
        if self.Space.dim == 1:
                self.matrix = self.__assemble_1d()
                self.matrix.dtype='float64'
                
        if self.Space.dim == 2:
            self.matrix = self.__assemble_2d()
            self.matrix.dtype='float64'
            
        if self.Space.dim == 3:
                self.matrix = self.__assemble_3d()
                self.matrix.dtype='float64'
        return 
            
    def assemble_fem(self):
        '''
        Assembles the FEM matrix used for preconditioning.
        
        Usage::
        
           import sempy

           X = sempy.Space( 'square', n = 7, dim = 2 )
           conv = sempy.operators.Convection(X)
           conv.assemble_fem()
           
           C_fem = conv.matrix_fem
        '''
        if self.dim == 1:
            #u_conv[0] = self.SpaceFEM.sem_to_fem(self.u_conv[0])
            
            U = sempy.Function( self.Space.fem, 
                 basis_coeff = self.Space.fem.sem_to_fem(self.u_conv[0]) )
            u_conv = [ U ]
            
        if self.dim == 2:
            #u_conv = np.ones((2, self.SpaceFEM.noe, self.SpaceFEM.n, self.SpaceFEM.n),float)
            #u_conv[0] = self.SpaceFEM.sem_to_fem(self.u_conv[0])
            #u_conv[1] = self.SpaceFEM.sem_to_fem(self.u_conv[1])
            U = sempy.Function( self.Space.fem, 
                 basis_coeff = self.Space.fem.sem_to_fem(self.u_conv[0]) )
            V = sempy.Function( self.Space.fem, 
                 basis_coeff = self.Space.fem.sem_to_fem(self.u_conv[1]) )
            u_conv = [ U, V ]
            
        if self.dim == 3:
            #u_conv = np.ones((3, self.SpaceFEM.noe, \
            #                     self.SpaceFEM.n, self.SpaceFEM.n, self.SpaceFEM.n),float)
            #u_conv[0] = self.SpaceFEM.sem_to_fem(self.u_conv[0])
            #u_conv[1] = self.SpaceFEM.sem_to_fem(self.u_conv[1])
            #u_conv[2] = self.SpaceFEM.sem_to_fem(self.u_conv[2])
            U = sempy.Function( self.Space.fem, 
                 basis_coeff = self.Space.fem.sem_to_fem(self.u_conv[0]) )
            V = sempy.Function( self.Space.fem, 
                 basis_coeff = self.Space.fem.sem_to_fem(self.u_conv[1]) )
            W = sempy.Function( self.Space.fem, 
                 basis_coeff = self.Space.fem.sem_to_fem(self.u_conv[2]) )
            u_conv = [ U, V, W ]
        
        self.matrix_fem = Convection(self.Space.fem,
                                     u_conv,assemble='yes',
                                     silent=self.silent).matrix
        #return Convection(self.Space.fem,u_conv,assemble='yes').matrix
    
    def __action_1d(self,v_in):
        # Mapping from global to local
        v = self.Space.mapping_q(v_in)
        # Matrix-vector product
        w = operators_f90.action_of_convection_1d(v,self.u_conv,self.Space.weights,\
                                                  self.Space.D)
        # Mapping from local to global
        v_out=self.Space.mapping_qt(w)
        # Mask
        v_out = self.Space.mask(v_out)
        return v_out
        
    def __action_2d(self,v_in):
        # Mapping from global to local
        v = self.Space.mapping_q(v_in)
        # Matrix-vector product
        w = operators_f90.action_of_convection_2d(v,self.u_conv[0],\
                                                  self.u_conv[1],\
                                                  self.Space.weights,\
                                                  self.Space.D,\
                                                  self.g11,self.g12,\
                                                  self.g21,self.g22)    
        # Mapping from local to global
        v_out=self.Space.mapping_qt(w)
        # Mask
        v_out = self.Space.mask(v_out)
        return v_out
    
    def __action_3d(self,v_in):
        # Mapping from global to local
        v = self.Space.mapping_q(v_in)
        # Matrix-vector product
        #w = np.zeros((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),float)
        #for k in range(self.Space.noe):
        #    w[k,:,:,:] = operators_f90.action_of_convection_3d(v[k,:,:,:],\
        #                           self.u_conv[0][k,:,:,:],self.u_conv[1][k,:,:,:],self.u_conv[2][k,:,:,:],\
        #                           self.W,self.Space.D,\
        #                           self.g11[k,:,:,:],self.g12[k,:,:,:],self.g13[k,:,:,:],\
        #                           self.g21[k,:,:,:],self.g22[k,:,:,:],self.g23[k,:,:,:],\
        #                           self.g31[k,:,:,:],self.g32[k,:,:,:],self.g33[k,:,:,:])
        w = operators_f90.action_of_convection_3d_2(v,\
                                   self.u_conv[0],self.u_conv[1],self.u_conv[2],\
                                   self.W,self.Space.D,\
                                   self.g11,self.g12,self.g13,\
                                   self.g21,self.g22,self.g23,\
                                   self.g31,self.g32,self.g33)
        # Mapping from local to global
        v_out=self.Space.mapping_qt(w)
        # Mask
        v_out = self.Space.mask(v_out)
        return v_out
        
    def __assemble_1d(self):
        '''
        Assemble.
        '''
        if not self.silent:
            print ''
            print '**** Assemble convection      ****'
        nz = self.Space.noe * self.Space.n * self.Space.n
        t1 = time.clock()
        irow,jcolumn,value = \
            operators_f90.assemble_convection_1d(self.u_conv,self.Space.weights,self.Space.D,\
                                                self.Space.theta,nz)
        #A = pysparse.spmatrix.ll_mat(self.Space.dof, self.Space.dof, nz)
        #A = sps.lil_matrix((self.Space.dof, self.Space.dof), dtype='float')
        #A = pysparseMatrix.PysparseMatrix(size=self.Space.dof)
        A = PysparseMatrix(size=self.Space.dof)
        # Assign values
        for k in range(len(value)):
            i = int(irow[k])
            j = int(jcolumn[k])
            A[i,j] = A[i,j] + value[k]
        # Mask
        A = self.Space.mask_matrix(A)
        t2 = time.clock()
        if not self.silent:
            print '**** ex time=',t2-t1,'nnz=',A.nnz
        return A
        
    def __assemble_2d(self):
        # Local comnectivity array
        theta_local = np.zeros((self.Space.n, self.Space.n),int)
        count =0
        for m in range(self.Space.n):
            for n in range(self.Space.n):
                theta_local[m,n]=count
                count=count+1

        # Mask array
        mask   = np.zeros((self.Space.noe,self.Space.n,self.Space.n),int)
        mask_g = np.zeros((self.Space.dof),int)
        for k in range(self.Space.noe_bc):
            for m in range(self.Space.n):
                [i, phys, bc_type, edge] = self.Space.theta_phys_bc(k,m)
                if bc_type == "Dir":
                    mask_g[i] = 1
                        
        for k in range(self.Space.noe):
            for m in range(self.Space.n):
                for n in range(self.Space.n):
                    i = self.Space.theta[k,m,n]
                    mask[k,m,n] = mask_g[i]
        del mask_g
        
        if not self.silent:
            print ' '
            print '**** Assemble convection      ****'
        # Stiffness matrix
        #A  = pysparseMatrix.PysparseMatrix(size=self.Space.dof)#
        A  = PysparseMatrix(size=self.Space.dof)#
        nz = self.Space.n*self.Space.n
        t1 = time.clock()
        # Assemble the stiffness matrix elementwize.
        for k in range(self.Space.noe):
            val,row,col = \
                   operators_f90.assemble_convection_2d(self.Space.weights,\
                        self.u_conv[0][k,:,:],self.u_conv[1][k,:,:],\
                        self.g11[k,:,:],self.g12[k,:,:],\
                        self.g21[k,:,:],self.g22[k,:,:],\
                        self.Space.D,self.Space.theta[k,:,:],theta_local,mask[k,:,:],nz)
            val = np.reshape(val, nz*nz)
            row = np.reshape(row, nz*nz)
            col = np.reshape(col, nz*nz)
            A.addAt(val,row,col)
        #---
        # Mask
        #t1_m = time.clock()
        #A = self.Space.mask_matrix(A)
        #t2_m = time.clock()
               
        t2 = time.clock()
        #print '**** mask     time=',t2_m-t1_m
        if not self.silent:
            print '**** assemble time=',t2-t1
            print '**** nnz=',A.nnz
        return A
        
    def __assemble_3d(self):
        # Local comnectivity array
        theta_local = np.zeros((self.Space.n, self.Space.n, self.Space.n),int)
        count =0
        for k in range(self.Space.n):
            for m in range(self.Space.n):
                for n in range(self.Space.n):
                    theta_local[k,m,n]=count
                    count=count+1

        # Mask array
        mask   = np.zeros((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),int)
        mask_g = np.zeros((self.Space.dof),int)
        for k in range(self.Space.noe_bc):
            for m in range(self.Space.n):
                for n in range(self.Space.n):
                    [i, phys, bc_type, edge] = self.Space.theta_phys_bc(k,m,n)
                    if bc_type == "Dir":
                        mask_g[i] = 1
                        
        for k in range(self.Space.noe):
            for m in range(self.Space.n):
                for n in range(self.Space.n):
                    for o in range(self.Space.n):
                        i = self.Space.theta[k,m,n,o]
                        mask[k,m,n,o] = mask_g[i]
        del mask_g
        if not self.silent:
            print ''
            print '**** Assemble Convection      ****'
        # Matrix
        #A = pysparseMatrix.PysparseMatrix(size=self.Space.dof)#, sizeHint=nz)
        A = PysparseMatrix(size=self.Space.dof)
        
        # Local degrees of freedom
        nz =  self.Space.n*self.Space.n*self.Space.n
        t1 = time.clock()
        
        # Assemble the stiffness matrix, elementwize.
        t1_f = time.clock()    
        for k in range(self.Space.noe):
            val,row,col = \
                operators_f90.assemble_convection_3d(self.Space.weights,\
                          self.u_conv[0][k,:,:,:],self.u_conv[1][k,:,:,:],self.u_conv[2][k,:,:,:],\
                          self.g11[k,:,:,:],self.g12[k,:,:,:],self.g13[k,:,:,:],\
                          self.g21[k,:,:,:],self.g22[k,:,:,:],self.g23[k,:,:,:],\
                          self.g31[k,:,:,:],self.g32[k,:,:,:],self.g33[k,:,:,:],\
                          self.Space.D,self.Space.theta[k,:,:,:],theta_local,mask[k,:,:,:],nz)
            val = np.reshape(val, nz*nz)
            row = np.reshape(row, nz*nz)
            col = np.reshape(col, nz*nz)
            A.addAt(val,row,col)
            
        t2_f = time.clock()    
        
        t2 = time.clock()
        
        # Mask
        if not self.silent:
            print '**** Number of nnz=',A.nnz
            #print '**** post mask nnz=',A.nnz
            #print '**** assemble time=',t2_f-t1_f
            #print '**** robin    time=',t2_r-t1_r
            #print '**** mask     time=',t2_m-t1_m
            print '**** assemble time=',t2-t1#,'nnz=',A.nnz
        
        return A


class MultipleOperators:
    '''
    Combines multiple operators into one, e.g. 
    
    .. math::
    
       (A+B+C)u=b
    
    becomes 
    
    .. math::
    
       Lu=b
    
    where :math:`L=A+B+C`. 
    
    :param list Operator: A list of operators
    :param list scaling_factor: Scaling factors.
    :param assemble: A flag which determines if the combined operator should
                     be assembled (:literal:`assemble='yes'`) or not
                     (:literal:`assemble='no'`).
    :type assemble: string
    :attribute: * **matrix** (*Scipy LinearOperator/Pysparse matrix*)- The combined operator. 
           
    **Example**::
    
      import sempy
      
      X = sempy.Space( filename = 'square', n = 4, dim = 2 )
      
      lap = sempy.operators.Laplacian( X, fem_assemble = 'yes' )
      A_fem = lap.matrix_fem
      
      conv = sempy.operators.Convection( X, fem_assemble = 'yes' )
      C_fem = conv.matrix_fem

      # L = - A_fem - 2.0 * C_fem
      combined = sempy.operators.MultipleOperators( [A_fem,C_fem],
                                                    [-1,-2],
                                                    assemble = 'no' )
      L = combined.matrix
    
    '''
    def __init__(self,Operator,scaling_factor='none',assemble='no',
                 silent=False):
        self.Operator = Operator
        self.dof      = self.Operator[0].shape[0]
        self.silent = silent
        
        if scaling_factor == 'none':
            self.scaling_factor = np.ones((len(self.Operator)),float)
        else:
            self.scaling_factor = scaling_factor
        
        if assemble == 'no':
            self.matrix = spl.LinearOperator( (self.dof,self.dof),\
                                   matvec=self.__action__,dtype='float')
        if assemble == 'yes':
            if not self.silent:
                print ''
                print '**** MultipleOperators        ****'
            t1 = time.clock()
            #self.matrix = pysparseMatrix.PysparseMatrix(size=self.dof)
            self.matrix = PysparseMatrix(size=self.dof)
            for i in range(len(self.Operator)):
                val,irow,jcol = self.Operator[i].find()
                factor = float(self.scaling_factor[i])
                self.matrix.addAt(val*factor, irow, jcol)
            self.matrix.dtype='float64'
            t2 = time.clock()
            if not self.silent:
                print '**** Number of nnz=',self.matrix.nnz
                print '**** Assemble time =',t2-t1
            
    def __action__(self,v):
        w = np.zeros((self.dof))
        for i in range(len(self.Operator)):
            factor = float(self.scaling_factor[i])
            s = self.Operator[i] * v
            w = w + factor * s
            #del s
        return w   


       
class Mass:
    '''
    The mass matrix.
    
    .. math::
       \int_\Omega uv\, d\Omega\Rightarrow Mu
    
    :param Space: The discrete function space. 
    :type Space: :class:`sempy.Space`
    :param mask: If :literal:`mask='yes'` the matrix is masked according to 
                 strong boundary conditions. If :literal:`mask='no'` the
                 matrix is not masked.
    :type mask: string
    
    :attributes: * **matrix** - The mass matrix.
                 * **matrix_inv** - The inverse of the mass matrix. 
                 
    **Example**::
    
      import sempy
      
      
      X = sempy.Space( 'square', n = 7, dim = 2 )

      mass = sempy.operators.Mass(X)
      M     = mass.matrix
      M_inv = mass.matrix_inv
      
      f = sempy.Function( X, basis_coeff = 2.0 )
      b = mass.action_local( f.basis_coeff )
      
    '''
    def __init__( self, Space, mask='yes' ):
        self.Space = Space
        self.mask = mask
        self.matrix = self.__assemble_mass()
        self.matrix_inv = self.__assemble_mass_inv()
    
      
    def __assemble_mass(self):
        # The local matrix vector product w=M_L*u_L
        if self.Space.dim == 1:
            u_local = np.ones((self.Space.noe,self.Space.n),float)
            w = operators_f90.action_of_mass_1d(u_local,
                                                self.Space.jac,
                                                self.Space.weights)
        if self.Space.dim == 2:
            u_local = np.ones((self.Space.noe,self.Space.n,self.Space.n),float)
            w = operators_f90.action_of_mass_2d(u_local,
                                                self.Space.jac,
                                                self.Space.weights)
        if self.Space.dim == 3:
            u_local = np.ones((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),float)
            w = operators_f90.action_of_mass_3d(u_local,
                                                self.Space.jac,
                                                self.Space.weights)
        # Gather (local to global)
        w_out = self.Space.mapping_qt(w)
        # Mask
        if self.mask == 'yes':
            w_out = self.Space.mask(w_out)
        # Matrix
        #A = pysparseMatrix.PysparseMatrix(size = self.Space.dof)
        A = PysparseMatrix(size = self.Space.dof)
        A.putDiagonal(w_out)
        return A
    
    def __assemble_mass_inv(self):
        if self.Space.dim == 1:
            u_local = np.ones((self.Space.noe,self.Space.n),float)
            w = operators_f90.action_of_mass_1d( u_local,
                                                 self.Space.jac,
                                                 self.Space.weights)
        if self.Space.dim == 2:
            u_local = np.ones( (self.Space.noe,self.Space.n,self.Space.n),
                               float )
            w = operators_f90.action_of_mass_2d( u_local, 
                                                 self.Space.jac,
                                                 self.Space.weights)
        if self.Space.dim == 3:
            u_local = np.ones((self.Space.noe,self.Space.n,self.Space.n,self.Space.n),float)
            w = operators_f90.action_of_mass_3d(u_local,self.Space.jac,self.Space.weights)
        # Gather (local to global)
        w_out = self.Space.mapping_qt(w)
        # Inverse
        if self.Space.dim == 1:
            w_out = operators_f90.mass_inv_1d(w_out)
        if self.Space.dim == 2:
            w_out = operators_f90.mass_inv_2d(w_out)
        if self.Space.dim == 3:
            w_out = operators_f90.mass_inv_3d(w_out)
        # Mask
        if self.mask == 'yes':
            w_out = self.Space.mask(w_out)
        # Matrix
        #A = pysparseMatrix.PysparseMatrix(size = self.Space.dof)
        A = PysparseMatrix(size = self.Space.dof)
        A.putDiagonal(w_out)
        return A
        
    def action_local(self,u_L):
        '''
        Action of the mass matrix on a set of basis coefficients 
        in local data structure:
        
        .. math::
           v=Mu=Q^TM_Lu_L
           
        :param u_L: Basis coefficients in local data structure.
        :returns: A vector in :math:`\mathbb R^{dof}`
           
        '''
        # The local matrix vector product w=M_L*u_L
        if self.Space.dim == 1:
            w = operators_f90.action_of_mass_1d(u_L,self.Space.jac,self.Space.weights)
        if self.Space.dim == 2:
            w = operators_f90.action_of_mass_2d(u_L,self.Space.jac,self.Space.weights)
        if self.Space.dim == 3:
            w = operators_f90.action_of_mass_3d(u_L,self.Space.jac,self.Space.weights)
        # Gather (local to global)
        w_out = self.Space.mapping_qt(w)
        # Mask
        if self.mask == 'yes':
            w_out = self.Space.mask(w_out)
            
        return w_out
        