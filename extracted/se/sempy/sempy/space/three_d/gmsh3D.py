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
import sempy.operators.operators_f90 as operators_f90

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

import time 

def MeshConvert3D(filename,elem_dof=3):
    '''
    Takes as input a gmsh file (filename) and gmsh element type (elem_dof).
    Returns: x, y, physical_names, theta, physical, theta_bc, physical_bc, dof, noe
    '''
    #print 'Reading gmsh file....'
    #--- Physical names
    f=open(filename,'r')
    i=0
    for line in f:
        i=i+1
        if line == "$PhysicalNames\n":
            name_start=i+1
        if line == "$EndPhysicalNames\n":
            name_end=i
    f.close()
    
    
    f=open(filename,'r')
    f_names=open('names.txt','w')
    i=0
    for line in f:
        i=i+1
        if i > name_start and i < name_end:
            f_names.write(line)
    f.close()
    f_names.close()
    f_names=open('names.txt','r')
    physical_names = np.genfromtxt(f_names,usecols=(0,1),dtype=int)
    f_names.close()
    #print 'physical_names='
    #print physical_names
    #print '**************'
    # Determining the bc type, i.e. "dir" (strong, Dirichlet) or "Nat" 
    # (natural like Robin and Neumann)
    f_names=open('names.txt','r')
    bc_type=['0']
    for line in f_names:
        #print line
        if int(line[0]) == 2:
            bc_type.append(line[5:8])
    f_names.close()
    bc_type.remove('0')
    #print 'bc_type=',bc_type
    #print 'physical_names=',physical_names
    #print '**************'
    
    #--- Locating the nodes and elements in the  gmsh-file:
    f=open(filename,'r')
    i=0
    for line in f:
        i=i+1
        if line == "$Nodes\n":
            nodes_start=i+1
        if line == "$EndNodes\n":
            nodes_end=i        
        if line == "$Elements\n":
            elements_start=i+1
        if line == "$EndElements\n":
            elements_end=i
    f.close()

    #--- Creating temporary files of nodes and elements
    f          = open(filename,'r')
    f_nodes    = open('nodes.txt','w')
    f_elements = open('elements.txt','w')

    i=0
    for line in f:
        i=i+1
        if i > nodes_start and i < nodes_end:
            f_nodes.write(line)
        if i > elements_start and i < elements_end:
            f_elements.write(line)
    f.close()
    f_nodes.close()
    f_elements.close()

    #--- Nodal points (x,y)
    f_nodes = open('nodes.txt','r')
    A = np.genfromtxt(f_nodes,dtype=float)
    f_nodes.close()
    x=A[:,1]
    y=A[:,2]
    z=A[:,3]
    #print 'A='
    #print A   
    #print 'x shape=',x.shape
    #--- Connectivity array (theta_bc)
    # Finding internal elements
    f_elements = open('elements.txt','r')
    A = np.genfromtxt(f_elements, dtype=int,
                      usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14))
    f_elements.close()
    #print 'A.shape=',A.shape
    #print A
    # Removing the boundary elements
    #print 'elem_dof=',elem_dof
    if elem_dof == 2:
        element_type = 5 # gmsh type
    if elem_dof == 3:
        element_type = 12 # gmsh type
    for i in range(A.shape[0]):
        if A[i,1] == element_type:
            cutoff=i
            break
    #print 'cutoff=',cutoff
    
    # Boundary elements
    theta_bc=np.zeros((cutoff,elem_dof,elem_dof),int)
    physical_bc=np.zeros((cutoff),int)
    for i in range(cutoff):
        physical_bc[i]=A[i,3]
    #print 'physical_bc='
    #print physical_bc
    
    if elem_dof == 3:
        for i in range(cutoff):
            theta_bc[i,0,0] = A[i,6]-1
            theta_bc[i,1,0] = A[i,7]-1
            theta_bc[i,1,1] = A[i,8]-1
            theta_bc[i,0,1] = A[i,9]-1
            
    if elem_dof == 3:
        for i in range(cutoff):
            theta_bc[i,0,0] = A[i,6]-1
            theta_bc[i,1,0] = A[i,10]-1
            theta_bc[i,2,0] = A[i,7]-1
            theta_bc[i,2,1] = A[i,11]-1
            theta_bc[i,1,2] = A[i,12]-1
            theta_bc[i,0,1] = A[i,13]-1
            theta_bc[i,1,1] = A[i,14]-1
            theta_bc[i,2,2] = A[i,8]-1
            theta_bc[i,0,2] = A[i,9]-1
    #print 'theta_bc'
    #print theta_bc
    # Creating array of elements without boundary elements
    f_elements = open( 'elements.txt', 'r' )
    ver = np.fromstring( np.__version__, dtype = float, sep='.' )
    if ver[0] > 1.3:
        internal_elements = np.genfromtxt( f_elements, dtype = int, 
                                           skip_header = cutoff )
    else:
        internal_elements = np.genfromtxt( f_elements, dtype = int, 
                                           skiprows = cutoff )
    f_elements.close()

    #print 'internal_elements shape=',internal_elements.shape
    #print internal_elements

    k = internal_elements.shape[0]
    
    if elem_dof == 2:
        theta        = np.zeros((k,2,2,2),int)
        physical     = np.zeros((k),int)
        theta[:,0,0,0] = internal_elements[:,6]-1 # 0
        theta[:,1,0,0] = internal_elements[:,7]-1 # 1
        theta[:,1,1,0] = internal_elements[:,8]-1 # 2
        theta[:,0,1,0] = internal_elements[:,9]-1 # 3
        theta[:,0,0,1] = internal_elements[:,10]-1 # 4
        theta[:,1,0,1] = internal_elements[:,11]-1 # 5
        theta[:,1,1,1] = internal_elements[:,12]-1 # 6
        theta[:,0,1,1] = internal_elements[:,13]-1 # 7
        
        physical[:]  = internal_elements[:,3]
        
    if elem_dof == 3:
        theta        = np.zeros((k,3,3,3),int)
        physical     = np.zeros((k),int)
        theta[:,0,0,0] = internal_elements[:,6]-1 # 0
        theta[:,2,0,0] = internal_elements[:,7]-1 # 1
        theta[:,2,2,0] = internal_elements[:,8]-1 # 2
        theta[:,0,2,0] = internal_elements[:,9]-1 # 3
        
        theta[:,0,0,2] = internal_elements[:,10]-1 # 4
        theta[:,2,0,2] = internal_elements[:,11]-1 # 5
        theta[:,2,2,2] = internal_elements[:,12]-1 # 6
        theta[:,0,2,2] = internal_elements[:,13]-1 # 7
        
        theta[:,1,0,0] = internal_elements[:,14]-1 # 8
        theta[:,0,1,0] = internal_elements[:,15]-1 # 9
        theta[:,0,0,1] = internal_elements[:,16]-1 # 10
        theta[:,2,1,0] = internal_elements[:,17]-1 # 11
        
        theta[:,2,0,1] = internal_elements[:,18]-1 # 12
        theta[:,1,2,0] = internal_elements[:,19]-1 # 13
        theta[:,2,2,1] = internal_elements[:,20]-1 # 14
        theta[:,0,2,1] = internal_elements[:,21]-1 # 15
        
        theta[:,1,0,2] = internal_elements[:,22]-1 # 16
        theta[:,0,1,2] = internal_elements[:,23]-1 # 17
        theta[:,2,1,2] = internal_elements[:,24]-1 # 18
        theta[:,1,2,2] = internal_elements[:,25]-1 # 19
        
        theta[:,1,1,0] = internal_elements[:,26]-1 # 20
        theta[:,1,0,1] = internal_elements[:,27]-1 # 21
        theta[:,0,1,1] = internal_elements[:,28]-1 # 22
        theta[:,2,1,1] = internal_elements[:,29]-1 # 23
        
        theta[:,1,2,1] = internal_elements[:,30]-1 # 24
        theta[:,1,1,2] = internal_elements[:,31]-1 # 25
        theta[:,1,1,1] = internal_elements[:,32]-1 # 26
        
        physical[:]  = internal_elements[:,3]

    dof=x.shape[0]
    noe=theta.shape[0]
        
    return x, y, z, physical_names, theta, physical, \
           theta_bc, physical_bc, dof, noe, bc_type



class GmeshToSpectral3D():
    def __init__(self,filename,n=3):
        #print 'Creating Gmsh object ..'
        self.dim = 3
        self.n = n
        self.basic = sempy.Basic()
        self.D = self.basic.derivative_matrix_gll(self.n)
        x_glob, y_glob, z_glob, self.physical_names, self.theta, self.physical,\
        self.theta_bc, self.physical_bc, self.dof, self.noe, self.bc_type\
            = MeshConvert3D(filename,self.n)
        self.noe_bc      = self.theta_bc.shape[0]
        self.points, self.weights = \
                    self.basic.gauss_lobatto_legendre( self.n )
        self.x = self.mapping_q(x_glob)
        self.y = self.mapping_q(y_glob)
        self.z = self.mapping_q(z_glob)
        #print '... finished creating Gmsh object.'
        #self.jac = space_f90.geometric_3d(self.x, self.y, self.z, self.D)
        
        #print '**** noe =',self.noe
        #print '**** dof =',self.dof
        #print '**** n   =',self.n
        
    #def theta_phys_bc(self, k, m, n):
    #    i       = self.theta_bc[k,m,n]
    #    phys    = self.physical_bc[k]
    #    boundarycondtion_type = self.bc_type[phys-1]
    #    element_edge = 0#self.edge[k]
    #    return i, phys, boundarycondtion_type, element_edge
        
    #def theta_phys(self,k,m,n,o):
    #    i    = self.theta[k,m,n,o]
    #    phys = self.physical[k]
    #    return i, phys
        
    def mapping_q(self,v):
        # from global to local
        w = space_f90.mapping_q_3d(v,self.theta)
        #w=np.zeros((self.noe, self.n, self.n, self.n),float)
        #for k in range(self.noe):
        #    for m in range(self.n):
        #        for n in range(self.n):
        #            for o in range(self.n):
        #                i = self.theta[k,m,n,o]
        #                w[k,m,n,o]=v[i]
        return w
        
    #def mapping_qt(self,w):
    #    v = space_f90.mapping_qt_3d(w,self.theta,self.dof)
    #    return v
        
    #def local_to_global(self,w):
    #    v = space_f90.local_to_global_3d(w,self.theta,self.dof)
    #    return v
        
    #def quadrature(self,f):
    #    #kappa = space_f90.quadrature_3d(self.weights,self.jac,f)
    #    kappa=0.0
    #    for k in range(self.noe):
    #        for m in range(self.n):
    #            for n in range(self.n):
    #                for o in range(self.n):
    #                    kappa = kappa + self.weights[m]*self.weights[n]*self.weights[o]*\
    #                            self.jac[k,m,n,o]*f[k,m,n,o]
    #    return kappa
        
    #def l2_norm(self,u):
    #    norm = space_f90.l2norm_3d(self.weights,self.jac,u)
    #    return norm
    
    #def mask(self,w):
    #    '''
    #    This method masks nodal point values associated with a Dirichlet boundary condition.
    #    
    #    :param w: Numpy array in global data representation subject to masking.
    #    :returns: A masked numpy array in global data representation.
    #    
    #    '''
    #    for k in range(self.noe_bc):
    #        for m in range(self.n):
    #            for n in range(self.n):
    #                [i, name, bc_type, edge] = self.theta_phys_bc(k,m,n)
    #                if bc_type == 'Dir':
    #                    w[i] = 0.0
    #    return w


class SimpleMesh3D():
    def __init__(self):
        #print 'Creating Gmsh object ..'
        self.dim = 3
        self.n   = 2
        self.noe = 1
        self.noe_bc = 6
        self.dof = 8
        self.basic = sempy.Basic()
        self.D = self.basic.derivative_matrix_gll( self.n )
        self.physical = np.zeros((1),int)
        self.physical = 1
        #self.physical_names, self.theta,,\
        self.points, self.weights = \
                    self.basic.gauss_lobatto_legendre(self.n)
        
        self.x = np.zeros((self.noe, self.n, self.n, self.n),float)
        self.y = np.zeros((self.noe, self.n, self.n, self.n),float)
        self.z = np.zeros((self.noe, self.n, self.n, self.n),float)
        
        self.x[0,0,0,0]=0.3333333333333335
        self.x[0,1,0,0]=0.5000000000013294
        self.x[0,0,1,0]=0.0
        self.x[0,1,1,0]=0.0
        self.x[0,0,0,1]=0.2500000000001332
        self.x[0,1,0,1]=0.3333333333337766
        self.x[0,0,1,1]=0.0
        self.x[0,1,1,1]=0.0
        
        self.y[0,0,0,0]=0.3333333333333335
        self.y[0,1,0,0]=0.4999999999986707
        self.y[0,0,1,0]=0.5000000000013305
        self.y[0,1,1,0]=1.0
        self.y[0,0,0,1]=0.2499999999998673
        self.y[0,1,0,1]=0.3333333333328904
        self.y[0,0,1,1]=0.3333333333333337
        self.y[0,1,1,1]=0.4999999999986717
        
        self.z[0,0,0,0]=0.666666666666667
        self.z[0,1,0,0]=1.0
        self.z[0,0,1,0]=0.5000000000013305
        self.z[0,1,1,0]=1.0
        self.z[0,0,0,1]=0.7500000000001333
        self.z[0,1,0,1]=1.0
        self.z[0,0,1,1]=0.6666666666671102
        self.z[0,1,1,1]=1.0
        
        #self.x[0,0,0,0]=0.0;self.x[0,1,0,0]=1.0;self.x[0,0,1,0]=0.0;self.x[0,1,1,0]=1.0;
        #self.x[0,0,0,1]=0.0;self.x[0,1,0,1]=1.0;self.x[0,0,1,1]=0.0;self.x[0,1,1,1]=1.0;
        #self.y[0,0,0,0]=0.0;self.y[0,1,0,0]=0.0;self.y[0,0,1,0]=1.0;self.y[0,1,1,0]=1.0;
        #self.y[0,0,0,1]=0.0;self.y[0,1,0,1]=0.0;self.y[0,0,1,1]=1.0;self.y[0,1,1,1]=1.0;
        #self.z[0,0,0,0]=0.0;self.z[0,1,0,0]=0.0;self.z[0,0,1,0]=0.0;self.z[0,1,1,0]=0.0;
        #self.z[0,0,0,1]=1.0;self.z[0,1,0,1]=1.0;self.z[0,0,1,1]=1.0;self.z[0,1,1,1]=1.0;
       
        
        self.jac = space_f90.geometric_3d(self.x, self.y, self.z, self.D)
                
        self.theta=np.zeros((self.noe, self.n, self.n, self.n),int)
        
        self.theta[0,0,0,0]=0
        self.theta[0,1,0,0]=1
        self.theta[0,0,1,0]=2
        self.theta[0,1,1,0]=3
        
        self.theta[0,0,0,1]=4
        self.theta[0,1,0,1]=5
        self.theta[0,0,1,1]=6
        self.theta[0,1,1,1]=7
        
       
    #def theta_phys_bc(self,k,m,n):
    #    i    = self.theta_bc[k,m,n]
    #    phys = self.physical_bc[k]
    #    return i, phys
        
    #def theta_phys(self,k,m,n,o):
    #    i    = self.theta[k,m,n,o]
    #    phys = self.physical[k]
    #    return i, phys
        
    def mapping_q(self,v):
        # from global to local
        w = space_f90.mapping_q_3d(v,self.theta)
        return w
        
    def mapping_qt(self,w):
        v = space_f90.mapping_qt_3d(w,self.theta,self.dof)
        return v
        
    def local_to_global(self,w):
        v = space_f90.local_to_global_3d(w,self.theta,self.dof)
        return v
        
    def quadrature(self,f):
        kappa = space_f90.quadrature_3d(self.weights,self.jac,f)
        return kappa
        
           
        
class MeshObject3D():
    '''
    This class creates a sem mesh object based on a gmsh file and the chosen polynomial degree. 
    '''
    def __init__(self,filename,n,n_gmsh=3):
        print ''
        print '**** Creating Space object     ****'
        t1 = time.clock()
        self.GTS      = GmeshToSpectral3D(filename,n_gmsh)
        self.bc_type  = self.GTS.bc_type
        self.dim      = 3
        self.basic = sempy.Basic()
               
        self.physical = self.GTS.physical
        self.n        = n
        self.D        = self.basic.derivative_matrix_gll(self.n)
        self.points, self.weights = \
                    self.basic.gauss_lobatto_legendre(self.n)
        self.noe      = self.GTS.noe
        
        if self.n == n_gmsh:
            self.x = self.GTS.x
            self.y = self.GTS.y
            self.z = self.GTS.z
            self.dof = self.GTS.dof
            self.theta = self.GTS.theta
        else:
            self.x = self.interpolation(self.GTS.x,self.n)
            self.y = self.interpolation(self.GTS.y,self.n)
            self.z = self.interpolation(self.GTS.z,self.n)
            self.theta, self.dof = space_f90.connectivity_3d(self.x,self.y,self.z)
        
        self.jac = space_f90.geometric_3d(self.x, self.y, self.z, self.D)
        #self.jac = self.geometric()
                
        self.theta_bc, self.physical_bc, self.jac_s, self.edge = self.boundary_connectivity()
        self.noe_bc = self.GTS.theta_bc.shape[0]
        #self.n_x, self.n_y = self.surface_unit_normal()
        # Arrays to calculate derivatives
        self.__derivative_geometric()
        
        t2 = time.clock()
        print '**** dim =',self.dim
        print '**** noe =',self.noe
        print '**** dof =',self.dof
        print '****   n =',self.n
        print '**** ex. time=',t2-t1
        print '**** Finished creating instance.'
        
        
    #def plot_mesh(self):
    
    #def plot_scalar(self,u,n_int=0):
               
    #def plot_basis_function(self,n_g):
    def __derivative_geometric(self):
        #
        self.g11 = np.zeros((self.noe,self.n,self.n,self.n),float)
        self.g12 = np.zeros((self.noe,self.n,self.n,self.n),float)
        self.g13 = np.zeros((self.noe,self.n,self.n,self.n),float)
        self.g21 = np.zeros((self.noe,self.n,self.n,self.n),float)
        self.g22 = np.zeros((self.noe,self.n,self.n,self.n),float)
        self.g23 = np.zeros((self.noe,self.n,self.n,self.n),float)
        self.g31 = np.zeros((self.noe,self.n,self.n,self.n),float)
        self.g32 = np.zeros((self.noe,self.n,self.n,self.n),float)
        self.g33 = np.zeros((self.noe,self.n,self.n,self.n),float)
            
        for k in range(self.noe):
            self.g11[k,:,:,:],self.g12[k,:,:,:],self.g13[k,:,:,:],\
            self.g21[k,:,:,:],self.g22[k,:,:,:],self.g23[k,:,:,:],\
            self.g31[k,:,:,:],self.g32[k,:,:,:],self.g33[k,:,:,:] =\
                    operators_f90.geometric_convection_3d(self.x[k,:,:,:],
                                                          self.y[k,:,:,:],
                                                          self.z[k,:,:,:],
                                                          self.D)
    
    def __geometric(self):
        jac   =np.zeros((self.noe, self.n, self.n, self.n),np.float)
        x_xi  =np.zeros((self.noe, self.n, self.n, self.n),np.float)
        x_eta =np.zeros((self.noe, self.n, self.n, self.n),np.float)
        x_zeta=np.zeros((self.noe, self.n, self.n, self.n),np.float)
        y_xi  =np.zeros((self.noe, self.n, self.n, self.n),np.float)
        y_eta =np.zeros((self.noe, self.n, self.n, self.n),np.float)
        y_zeta=np.zeros((self.noe, self.n, self.n, self.n),np.float)
        z_xi  =np.zeros((self.noe, self.n, self.n, self.n),np.float)
        z_eta =np.zeros((self.noe, self.n, self.n, self.n),np.float)
        z_zeta=np.zeros((self.noe, self.n, self.n, self.n),np.float)
        t1    =np.zeros((self.noe, self.n, self.n, self.n),np.float)
        t2    =np.zeros((self.noe, self.n, self.n, self.n),np.float)
        t3    =np.zeros((self.noe, self.n, self.n, self.n),np.float)
        # geometric
        for k in range(self.noe):
          for alpha in range(self.n):
              for beta in range(self.n):
                  for gamma in range(self.n):
                      for i in range(self.n):
                          x_xi[k,alpha,beta,gamma] = x_xi[k,alpha,beta,gamma] + self.D[alpha,i] * self.x[k,i,beta,gamma]
                          y_xi[k,alpha,beta,gamma] = y_xi[k,alpha,beta,gamma] + self.D[alpha,i] * self.y[k,i,beta,gamma]
                          z_xi[k,alpha,beta,gamma] = z_xi[k,alpha,beta,gamma] + self.D[alpha,i] * self.z[k,i,beta,gamma]
        
                          x_eta[k,alpha,beta,gamma] = x_eta[k,alpha,beta,gamma] + self.D[beta,i]* self.x[k,alpha,i,gamma]
                          y_eta[k,alpha,beta,gamma] = y_eta[k,alpha,beta,gamma] + self.D[beta,i]* self.y[k,alpha,i,gamma]
                          z_eta[k,alpha,beta,gamma] = z_eta[k,alpha,beta,gamma] + self.D[beta,i]* self.z[k,alpha,i,gamma]
        
                          x_zeta[k,alpha,beta,gamma] = x_zeta[k,alpha,beta,gamma] + self.D[gamma,i] * self.x[k,alpha,beta,i]
                          y_zeta[k,alpha,beta,gamma] = y_zeta[k,alpha,beta,gamma] + self.D[gamma,i] * self.y[k,alpha,beta,i]
                          z_zeta[k,alpha,beta,gamma] = z_zeta[k,alpha,beta,gamma] + self.D[gamma,i] * self.z[k,alpha,beta,i]
        # Jacobian
        t1[:,:,:,:] = x_xi * ( y_eta * z_zeta - y_zeta * z_eta )
        t2[:,:,:,:] = y_xi * ( x_eta * z_zeta - x_zeta * z_eta )
        t3[:,:,:,:] = z_xi * ( x_eta * y_zeta - x_zeta * y_eta )
        jac[:,:,:,:] = t1 - t2 + t3
        return jac
    
    
    def gradient_vector(self,u):
        # grad
        #print space_f90.gradient_vector_3d.__doc__
        u_x, u_y, u_z = space_f90.gradient_vector_3d(
                                u,
                                self.jac,self.D,
                                self.g11,self.g12,self.g13,
                                self.g21,self.g22,self.g23,
                                self.g31,self.g32,self.g33 )
        return u_x,u_y,u_z
           
    def l2_norm(self,u):
        #u_local = self.mapping_q(u)
        norm = space_f90.l2norm_3d(self.weights,self.jac,u)
        return norm
    
    def quadrature(self,f):
        kappa = space_f90.quadrature_3d(self.weights,self.jac,f)
        #kappa=0.0
        #for k in range(self.noe):
        #    alpha=0.0
        #    for m in range(self.n):
        #        for n in range(self.n):
        #            for o in range(self.n):
        #                alpha = alpha + self.weights[m]*self.weights[n]*self.weights[o]*\
        #                        self.jac[k,m,n,o]*f[k,m,n,o]
        #    #print 'alpha[',k,']=',alpha
        #    kappa=kappa+alpha
        return kappa
                    
    def quadrature_surf(self):
        #kappa = space_f90.quadrature_3d(self.weights,self.jac,f)
        #print space_f90.quadrature_surf_3d.__doc__
        kappa= space_f90.quadrature_surf_3d(self.weights,self.jac_s)
        #kappa = 0.0
        #for k in range(self.noe_bc):
        #    for m in range(self.n):
        #        for n in range(self.n):
        #            #i = self.theta_bc[k,m,n]
        #            #print 'f[',i,']=',f[i]
        #            kappa = kappa + self.weights[m]*self.weights[n]*self.jac_s[k,m,n]#*f[i]
        #            #kappa = kappa + self.jac_s[k,m,n]
                    
        return kappa
        
    def theta_phys(self, k, m, n, o):
        '''Local to global connectivity method. Takes as input the local node 
           description and returns the global node number and the physical name 
           of the element. 

           :param k: Element number
           :param m: Node number in the xi direction
           :param n: Node number in the eta direction
           :type k: integer
           :type m: integer
           :type n: integer
           :returns: An integer tuple of global node number and corresponding physical name.         
           
             
           Example::
              
              for k in range(mesh.noe):
                  for m in range(mesh.n):
                      for n in range(mesh.n):
                          i, phys = mesh.theta_phys(k,m,n)
        '''
        i    = self.theta[k,m,n,o]
        phys = self.physical[k]
        return i, phys

    def theta_phys_bc(self, k, m, n):
        i       = self.theta_bc[k,m,n]
        phys    = self.physical_bc[k]
        boundarycondtion_type = self.bc_type[phys-1]
        element_edge = self.edge[k]
        
        return i, phys, boundarycondtion_type, element_edge
    
    #def gradient_vector(self,u):
    #    u_x,u_y = space_f90.gradient_vector_2d(u,self.x,self.y,self.jac,self.D)
    #    return u_x,u_y
    
    
    #def surface_flux(self,u_grad):
    #    u_bx = self.boundary_value(u_grad[0])
    #    u_by = self.boundary_value(u_grad[1])
    #    #mu_b = self.boundary_value(mu)
    #    
    #    kappa = 0.0
    #    for k in range(self.noe_bc):
    #        for m in range(self.n):
    ##            [i, phys, boundarycondtion_type, element_edge] = self.theta_phys_bc(k,m)
    #             u_n = u_bx[k,m] * self.n_x[k,m] + u_by[k,m] * self.n_y[k,m]
    #             #coeff = (self.n_x[k,m] +self.n_y[k,m])/(self.n_x[k,m]*self.n_y[k,m])
    #             #print coeff
    #             #u_n = u_bx[k,m] * self.n_x[k,m]*self.n_x[k,m] + \
    #             #      u_by[k,m] * self.n_y[k,m]*self.n_y[k,m]
    #             #print u_n
    #             kappa = kappa +self.weights[m]*self.jac_s[k,m]*u_n
    #             
    #    return kappa
    
        
    def surface_unit_normal(self):
        n_x_f, n_y_f = space_f90.surface_1_2d(self.x,self.y,self.D)
        #n_x = np.zeros((self.noe, self.n, self.n),float)
        #n_y = np.zeros((self.noe, self.n, self.n),float)
        n_x = np.zeros((self.noe_bc, self.n),float)
        n_y = np.zeros((self.noe_bc, self.n),float)
        
       
        for k in range(self.noe_bc):
            for m in range(self.n):
                [i, phys, boundarycondtion_type, element_edge] = self.theta_phys_bc(k,m)
                if element_edge[1] == 0:
                    k_e = element_edge[0]
                    #n_x[k_e,m,0]       =  n_x_f[k_e,0,m]
                    #n_y[k_e,m,0]       =  n_y_f[k_e,0,m]
                    n_x[k,m]       =  n_x_f[k_e,0,m]
                    n_y[k,m]       =  n_y_f[k_e,0,m]
                        
                if element_edge[1] == 1:
                    k_e = element_edge[0]
                    #n_x[k_e,m,self.n-1] =  n_x_f[k_e,1,m]
                    #n_y[k_e,m,self.n-1] =  n_y_f[k_e,1,m]
                    n_x[k,m] =  n_x_f[k_e,1,m]
                    n_y[k,m] =  n_y_f[k_e,1,m]
                        
                if element_edge[1] == 2:
                    k_e = element_edge[0]
                    #n_x[k_e,0,m]        =  n_x_f[k_e,2,m]
                    #n_y[k_e,0,m]        =  n_y_f[k_e,2,m]
                    n_x[k,m]        =  n_x_f[k_e,2,m]
                    n_y[k,m]        =  n_y_f[k_e,2,m]
                        
                if element_edge[1] == 3:
                    k_e = element_edge[0]
                    #n_x[k_e,self.n-1,m] = n_x_f[k_e,3,m]
                    #n_y[k_e,self.n-1,m] = n_y_f[k_e,3,m]
                    n_x[k,m] = n_x_f[k_e,3,m]
                    n_y[k,m] = n_y_f[k_e,3,m]
                
        #plt.figure()
        ##k=2
        #for k in range(self.noe):
        #    Q = plt.quiver(self.x[k,:,:],self.y[k,:,:],n_x[k,:,:],n_y[k,:,:],\
        #                   scale=25.0)#,units='dots')#,color='r',linewidths=(2,) )
        ##qk =plt.quiverkey(Q, 0.9, 0.95, 2,'asdf',coordinates='figure')
        ##plt.axis([-0.2,1.2,-0.2,1.2])
        #plt.show()
        return n_x,n_y
                
                
        
    def boundary_value(self,u):
        '''
        Creates an array of boundary values of a function u.
        
        :param u: An array in local data representation
        
        :returns: An array of boundary points.
        '''
        u_bound = np.zeros((self.noe_bc, self.n), float)
        
        for k in range(self.noe_bc):
            for m in range(self.n):
                [i, phys, bc_type, element_edge] = self.theta_phys_bc(k,m)
                k_element = element_edge[0]
                if element_edge[1] == int(0):
                    u_bound[k,m] = u[k_element,m,0]
                if element_edge[1] == int(1):
                    u_bound[k,m] = u[k_element,m,self.n-1]
                if element_edge[1] == int(2):
                    u_bound[k,m] = u[k_element,0,m]
                if element_edge[1] == int(3):
                    u_bound[k,m] = u[k_element,self.n-1,m]
                
        return u_bound
        
    def mapping_q(self,v):
        #  w[k,m,n] = v[i]
        w = space_f90.mapping_q_3d(v,self.theta)
        #w=np.zeros((self.noe, self.n, self.n, self.n),float)
        #for k in range(self.noe):
        #    for m in range(self.n):
        #        for n in range(self.n):
        #            for o in range(self.n):
        #                i = self.theta[k,m,n,o]
        #                w[k,m,n,o]=v[i]
        return w
        
    def mapping_qt(self,w):
        #  v[i] = v[i] + w[k,m,n]
        v = space_f90.mapping_qt_3d(w,self.theta,self.dof)
        #v = np.zeros((self.dof),float)
        #for k in range(self.noe):
        #    for m in range(self.n):
        #        for n in range(self.n):
        #            for o in range(self.n):
        #                i    = self.theta[k,m,n,o]
        #                v[i] = v[i] + w[k,m,n,o]
        return v

    def local_to_global(self,w):
        # v[i]=w[k,m,n]
        v = space_f90.local_to_global_3d(w,self.theta,self.dof)
        #v = np.zeros((self.dof),float)
        #for k in range(self.noe):
        #    for m in range(self.n):
        #        for n in range(self.n):
        #            for o in range(self.n):
        #                i    = self.theta[k,m,n,o]
        #                v[i] = w[k,m,n,o]
        return v
        
    def mask(self,w):
        '''
        This method masks nodal point values associated with a Dirichlet boundary condition.
        
        :param w: Numpy array in global data representation subject to masking.
        :returns: A masked numpy array in global data representation.
        
        '''
        for k in range(self.noe_bc):
            for m in range(self.n):
                for n in range(self.n):
                    [i, name, bc_type, edge] = self.theta_phys_bc(k,m,n)
                    if bc_type == 'Dir':
                        w[i] = 0.0
        return w
        
    def mask_matrix(self,A):
        '''
        This method masks nodal point values associated with a Dirichlet boundary condition.
        
        :param A: Numpy array in global data representation subject to masking.
        :type A: PysparseMatrix
        :returns: A masked PysparseMatrix.
        
        '''
        val = np.zeros((self.dof),float)
        row = np.zeros((self.dof),int)
        col = np.zeros((self.dof),int)
        col[:]=range(self.dof)
        
        for k in range(self.noe_bc):
            for m in range(self.n):
                for n in range(self.n):
                    [i, phys, bc_type, element_edge]=self.theta_phys_bc(k,m,n)
                    if bc_type == "Dir":
                        #for j in range(self.dof):
                        #    A[int(i),j] = 0.0
                        #for j in range(self.dof):
                        #    if np.abs(A[int(i),j])>0.0:
                        #        A[int(i),j] = 0.0
                        row[:] = int(i)
                        A.put(val,row,col)
                        
        return A
        
    def interpolation(self,u,m):
        n_local = u.shape[1]
        points_local, weights_local = \
                    self.basic.gauss_lobatto_legendre( n_local )
        points_int,   weights_int   = \
                    self.basic.gauss_lobatto_legendre( m )
        u_int = space_f90.interpolation_3d( points_int, u, points_local )
        return u_int
        
    def hyper_filter(self,u_tilde,alpha=0.25):
        u1 = self.interpolation(u_tilde,self.n-1)
        u2 = self.interpolation(u1,self.n)
        u_out = alpha * u2 + (1.0 - alpha) * u_tilde
        return u_out
        
    def boundary_connectivity_gmsh(self,j):
        u      = np.zeros((self.GTS.dof),float)
        noe_bc = self.GTS.theta_bc.shape[0]
        
        for k in range(noe_bc):
            for m in range(self.GTS.n):
                for n in range(self.GTS.n):
                    i = self.GTS.theta_bc[k,m,n]
                    if self.GTS.physical_bc[k] == j:
                        u[i] = self.GTS.physical_bc[k]
                    
        return self.GTS.mapping_q(u)
        
         
    def boundary_connectivity_gll(self,u_gmsh):
        #u_gll = np.zeros((self.noe,self.n,self.n),float)
        #for k in range(self.noe):
        #    for i in range(self.n):
        #        for j in range(self.n):
        #            for m in range(self.GTS.n):
        #                for n in range(self.GTS.n):
        #                    L_xi  = basic.lagrange(m,self.GTS.n,self.points[i],self.GTS.points)
        #                    L_eta = basic.lagrange(n,self.GTS.n,self.points[j],self.GTS.points)
        #                    u_gll[k,i,j] = u_gll[k,i,j]+u_gmsh[k,m,n]*L_xi*L_eta
        u_gll = self.interpolation(u_gmsh,self.n)
        return np.rint(u_gll)
        
    def boundary_connectivity_theta(self, theta_bc, physical_bc, jac_s, edge, count, u_gll, i):
    #def boundary_connectivity_theta(self, theta_bc, physical_bc, jac_s, edge, count, u_gll, i):
        #
        for k in range(self.noe):
                alpha1=0.0
                alpha2=0.0
                alpha3=0.0
                alpha4=0.0
                alpha5=0.0
                alpha6=0.0
                for m in range(self.n):
                    for n in range(self.n):
                        alpha1=alpha1 + u_gll[k,m,n,0]
                        alpha2=alpha2 + u_gll[k,m,n,self.n-1]
                        alpha3=alpha3 + u_gll[k,m,0,n]
                        alpha4=alpha4 + u_gll[k,m,self.n-1,n]
                        alpha5=alpha5 + u_gll[k,0,m,n]
                        alpha6=alpha6 + u_gll[k,self.n-1,m,n]
                # zeta planes      
                if int(np.rint(alpha1)) == self.n*self.n*i:
                    for m in range(self.n):
                        for n in range(self.n):
                            theta_bc[count,m,n] = self.theta[k,m,n,0]# edge 0
                    physical_bc[count]=i
                    jac_s[count,:,:] = space_f90.jac_surf_3d_1(self.x[k,:,:,0],\
                                                              self.y[k,:,:,0],\
                                                              self.z[k,:,:,0],self.D)
                    edge[count,0] = k # element number
                    edge[count,1] = 0 # edge number
                    count = count +1
                    
                    
                if int(np.rint(alpha2)) == self.n*self.n*i:
                    for m in range(self.n):
                        for n in range(self.n):
                            theta_bc[count,m,n]=self.theta[k,m,n,self.n-1]# edge 1
                    physical_bc[count]=i
                    jac_s[count,:,:] = space_f90.jac_surf_3d_1(self.x[k,:,:,self.n-1],\
                                                              self.y[k,:,:,self.n-1],\
                                                              self.z[k,:,:,self.n-1],self.D)
                    edge[count,0] = k # element number
                    edge[count,1] = 1 # edge number
                    count = count +1
                     
                # eta planes    
                if int(np.rint(alpha3)) == self.n*self.n*i:
                    for m in range(self.n):
                        for n in range(self.n):
                            theta_bc[count,m,n]=self.theta[k,m,0,n]# edge 2
                    physical_bc[count]=i
                    jac_s[count,:,:] = space_f90.jac_surf_3d_2(self.x[k,:,0,:],\
                                                              self.y[k,:,0,:],\
                                                              self.z[k,:,0,:],self.D)
                    edge[count,0] = k # element number
                    edge[count,1] = 2 # edge number
                    count = count +1
                
                if int(np.rint(alpha4)) == self.n*self.n*i:
                    for m in range(self.n):
                        for n in range(self.n):
                            theta_bc[count,m,n]=self.theta[k,m,self.n-1,n]# edge 3
                    physical_bc[count]=i
                    jac_s[count,:,:] = space_f90.jac_surf_3d_2(self.x[k,:,self.n-1,:],\
                                                              self.y[k,:,self.n-1,:],\
                                                              self.z[k,:,self.n-1,:],self.D)
                    edge[count,0] = k # element number
                    edge[count,1] = 3 # edge number
                    count = count +1
                
                # xi planes
                if int(np.rint(alpha5)) == self.n*self.n*i:
                    for m in range(self.n):
                        for n in range(self.n):
                            theta_bc[count,m,n]=self.theta[k,0,m,n]# edge 4
                    physical_bc[count]=i
                    jac_s[count,:,:] = space_f90.jac_surf_3d_3(self.x[k,0,:,:],\
                                                              self.y[k,0,:,:],\
                                                              self.z[k,0,:,:],self.D)
                    edge[count,0] = k # element number
                    edge[count,1] = 4 # edge number
                    count = count +1
                    
                if int(np.rint(alpha6)) == self.n*self.n*i:
                    for m in range(self.n):
                        for n in range(self.n):
                            theta_bc[count,m,n]=self.theta[k,self.n-1,m,n]# edge 5
                    physical_bc[count]=i
                    jac_s[count,:,:] = space_f90.jac_surf_3d_3(self.x[k,self.n-1,:,:],\
                                                              self.y[k,self.n-1,:,:],\
                                                              self.z[k,self.n-1,:,:],self.D)
                    edge[count,0] = k # element number
                    edge[count,1] = 5 # edge number
                    count = count +1
                    
        return theta_bc, physical_bc, count, jac_s, edge
        #return theta_bc, physical_bc, jac_s, edge, count
        
    def boundary_connectivity(self):
        noe_bc      = self.GTS.theta_bc.shape[0]
        theta_bc    = np.zeros((noe_bc,self.n,self.n), int)
        
        jac_s       = np.zeros((noe_bc,self.n,self.n), float)
        u_gll       = np.zeros((self.noe,self.n,self.n,self.n), float)
        physical_bc = np.zeros((noe_bc), int)
        edge        = np.zeros((noe_bc, 2), int)
        
        #print 'names=',self.GTS.physical_names
        #print 'shape=',self.GTS.physical_names.shape[0]
        
        # Locating boundary points
        #print 'phys'
        #print self.GTS.physical_names
        count=0
        for i in range(self.GTS.physical_names.shape[0]):
            if self.GTS.physical_names[i,0] == 2:
                j = self.GTS.physical_names[i,1]
                u_gmsh = self.boundary_connectivity_gmsh(j)
                u_gll  = self.boundary_connectivity_gll(u_gmsh)
                theta_bc, physical_bc, count, jac_s, edge = \
                     self.boundary_connectivity_theta(theta_bc, physical_bc, jac_s, edge, count, u_gll, j)
            
        return theta_bc, physical_bc, jac_s, edge
        


