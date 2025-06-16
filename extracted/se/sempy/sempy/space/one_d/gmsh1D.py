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


def MeshConvert1D(filename,elem_dof):
    '''
    Takes as input a gmsh file (filename) and gmsh element type (elem_dof).
    Returns: x, y, physical_names, theta, physical, theta_bc, physical_bc, dof, noe
    '''
    #print 'Reading gmsh file....'
    #--- Physical names
    f = open(filename,'r')
    i = 0
    for line in f:
        i = i+1
        if line == "$PhysicalNames\n":
            name_start = i + 1
        if line == "$EndPhysicalNames\n":
            name_end = i
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
    
    #print '**************'
    # Determining the bc type, i.e. "dir" (strong, Dirichlet) or "Nat" 
    # (natural like Robin and Neumann)
    f_names=open('names.txt','r')
    bc_type=['0']
    for line in f_names:
        #print line
        if int(line[0]) == 0:
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
    f=open(filename,'r')
    f_nodes=open('nodes.txt','w')
    f_elements=open('elements.txt','w')

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

    #--- Connectivity array (theta)
    # Finding internal elements
    f_elements = open('elements.txt','r')
    A = np.genfromtxt(f_elements, dtype=int,
                      usecols=(0,1,2,3,4,5,6))
    f_elements.close()
    #print 'A='
    #print A

    # Removing the boundary elements
    if elem_dof == 3:
        element_type = 8 # gmsh type 1D
    for i in range(A.shape[0]):
        if A[i,1] == element_type:
            cutoff=i
            break
    
    # Boundary elements
    theta_bc=np.zeros((cutoff),int)
    physical_bc=np.zeros((cutoff),int)
    for i in range(cutoff):
        theta_bc[i]=A[i,6]-1
        physical_bc[i]=A[i,3]
    
    # Creating array of elements without boundary elements
    f_elements = open( 'elements.txt', 'r' )
    ver = np.fromstring( np.__version__, dtype = float,sep='.' )
    if ver[0] > 1.3:
        internal_elements = np.genfromtxt( f_elements, dtype=int, 
                                           skip_header = cutoff )
    else:
        internal_elements = np.genfromtxt( f_elements, dtype=int, 
                                           skiprows = cutoff )
        
    f_elements.close()


    k = internal_elements.shape[0]
      
    if elem_dof == 3:
        theta       = np.zeros((k,3),int)
        physical    = np.zeros((k),int)
        theta[:,0]  = internal_elements[:,6]-1
        theta[:,1]  = internal_elements[:,8]-1
        theta[:,2]  = internal_elements[:,7]-1
        physical[:] = internal_elements[:,3]

    dof=x.shape[0]
    noe=theta.shape[0]
    #print ' number of elements=',noe
    #print ' degrees of freedom=',dof
    
    #print '... finished reading file.'
    return x, physical_names, theta, physical, theta_bc, physical_bc, dof, noe, bc_type



class GmeshToSpectral1D():
    def __init__(self,filename,n):
        #print 'Creating Gmsh object ..'
        self.n = n
        self.basic = sempy.Basic()
        self.D = self.basic.derivative_matrix_gll(self.n)
        self.points, self.weights = \
                    self.basic.gauss_lobatto_legendre(self.n)

        x_glob, self.physical_names, self.theta, self.physical,\
        self.theta_bc, self.physical_bc, self.dof, self.noe, self.bc_type\
            = MeshConvert1D(filename,self.n)
        self.x = self.mapping_q(x_glob)
        #print '... finished creating Gmsh object.'
        
    def theta_phys_bc(self,k):
        i    = self.theta_bc[k]
        phys = self.physical_bc[k]
        return i,phys
        
    def theta_phys(self,k,m):
        i    = self.theta[k,m]
        phys = self.physical[k]
        return i,phys
        
    def mapping_q(self,v):
        w = space_f90.mapping_q_1d(v,self.theta)
        return w
        
    def mapping_qt(self,w):
        v = space_f90.mapping_qt_1d(w,self.theta,self.dof)
        return v

    
        
class MeshObject1D():
    '''
    This class creates a sem mesh object based on a gmsh file and the chosen polynomial degree. 
    
    :param filename: A gmsh file with format .msh
    :param n: Number of nodal points in each direction of an element. Hence, the polynomial 
              degree of the basis functions is :math:`N=n-1`.
    :param n_gmsh (optional): Gmsh dof. n_gmsh=2 or n_gmsh=3
    
    :attributes: 
                      
                 * *points* - GLL quadrature points 
                   :math:`\\underline{\\xi}\\in\\mathbb R^{N+1},\\ -1\\le \\xi_j\\le 1`
                 * *weights* - GLL quadrature weights :math:`\\underline{\\rho}\\in\\mathbb R^{N+1}` 
                   corresponding to the points :math:`\\underline{\\xi}`. 
                   Used to evaluate an integral over the reference domain:
                 
                   .. math::
                      \\hat\\Omega\\in\\mathbb R^1: \\int_{\\hat\\Omega} f d\\hat\\Omega\\approx
                      \\sum_i\\rho_if_i
                      
                      \\hat\\Omega\\in\\mathbb R^2: \\int_{\\hat\\Omega} f d\\hat\\Omega\\approx
                      \\sum_i\\sum_j\\rho_i\\rho_jf_{ij}
                      
                 * *D* - GLL derivative matrix 
                   :math:`\\underline D\\in\\mathbb R^{(N+1)\\times (N+1)}`. For a 1D problem:
    
                   .. math::
                      u_N'(\\xi_j)=\\sum_i l_i'(\\xi_j) u_i=\\sum_i D_{ji}u_i\\Rightarrow
                      D_{ji}=l_i'(\\xi_j)
                 * *noe* - Number of elements
                 * *noe_bc* - Number of boundary elements
                 * *x* - Coordinate array (given in local data distribution). 
                 * *y* -
                 * *jac* - The Jacobian :math:`|\\underline{J}|`.
                 * *jac_s* - The surface Jacobian :math:`|\\underline{J}^s|`. jac_s[noe_bc,n]. 
                 * *dof* - Global degrees of freedom
    
    Usage::
    
       import sempy
      
       filename = 'square.msh'
       n = 6
       mesh = MeshObject2D(filename,n)
       mesh.plot()
    
    '''
    def __init__(self,filename,n,n_gmsh=3):
        '''
        This is the init method.
        '''
        print ''
        print '**** Creating Space object     ****'
        self.GTS = GmeshToSpectral1D(filename,n_gmsh)
        self.bc_type = self.GTS.bc_type
        self.basic = sempy.Basic()
        
        self.dim = 1
        
        self.physical = self.GTS.physical
        self.n = n
        self.D = self.basic.derivative_matrix_gll( self.n )
        self.points, self.weights = \
                    self.basic.gauss_lobatto_legendre( self.n )
        self.noe = self.GTS.noe
        
        self.x = self.interpolation(self.GTS.x,self.n)
        
        
        self.theta, self.dof = self.connectivity()
        self.theta_bc, self.physical_bc, self.jac_s, self.edge = self.boundary_connectivity()
        self.noe_bc = self.GTS.theta_bc.shape[0]
        self.jac = self.geometric()
        
        #self.x = self.local_to_global(self.x)
        #self.x = self.mapping_q(self.x)
        print '**** dim =',self.dim
        print '**** noe =',self.noe
        print '**** dof =',self.dof
        print '****   n =',self.n
        print '**** Finished creating instance.' 
        
    def geometric(self):
        # Jacobian
        jac = space_f90.geometric_1d(self.x,self.D)
        return jac
    
    def gradient_vector(self,u):
        # Gradient
        #print space_f90.gradient_vector_1d.__doc__
        u_x = space_f90.gradient_vector_1d(u,self.jac,self.D)
        return u_x
    
    def plot_mesh(self):
        '''
        Plot mesh.
        '''
        u = np.zeros((self.noe,self.n),float)
        for k in range(self.noe):
            plt.plot(self.x[k,:],u[k,:],'o-')
        plt.show()
                       
        
    def plot_scalar(self,u,n_int=0):
        '''
        Plot mesh.
        '''
        if n_int == 0:
            for k in range(self.noe):
                plt.plot(self.x[k,:],u[k,:],'o-')
            plt.show()
        else:
            u_int=self.interpolation(u,n_int)
            x_int=self.interpolation(self.x,n_int)
            for k in range(self.noe):
                plt.plot(x_int[k,:],u_int[k,:],'-')
            plt.show()
            
    def plot_basis_function(self,n_g,show=True,font_size=20):
        ''' Plot.'''
        n_int = 60
        u_glob = np.zeros((self.dof),float)
        u_glob[n_g] = 1.0
        u = self.mapping_q(u_glob)
        u_zero=np.zeros((self.noe,self.n),float)
        u_i = self.interpolation(u,n_int)
        x_i = self.interpolation(self.x, n_int)
            
        fig_number = np.random.randint(0,1001)
        fig = plt.figure(fig_number)
        #levels=np.arange(-0.2,1.01,0.02)
        for k in range(self.noe):
            plt.plot(x_i[k,:],u_i[k,:],'-',color='blue')
            a='k='+str(k)
            plt.plot(self.x[k,:],u_zero[k,:],'o-',label=a)
                         #color='black')
            #    plt.contourf(x_i[k,:,:],y_i[k,:,:],u_i[k,:,:],levels,\
            #                 cmap=cm.get_cmap('jet',len(levels)-1))
        plt.xlabel(r'$x$', fontsize = font_size )
        plt.ylabel(r'$\phi$', fontsize = font_size )
        plt.axis([self.x.min(),self.x.max(),-0.50,1.1])

        ax = plt.gca()
        for label in ax.xaxis.get_ticklabels():
            label.set_fontsize( font_size )
        for label in ax.yaxis.get_ticklabels():
            label.set_fontsize( font_size )
        plt.legend(loc='best')
        if show:
            plt.show()
            
                
    def l2_norm(self,u):
        """Computes the :math:`L^2` - norm
           
           .. math::
              ||u||_{L^2(\\Omega)}=\\bigg(\\int_{\\Omega} u^2d\\Omega\\bigg)^{1/2}
              
           using GLL quadrature. 
           
           :param u: Basis coefficients in global data structure, i.e. :math:`u\\in\\mathbb R^{dof}` .
           :returns: The :math:`L^2` - norm as a floating number.
           :todo: Fortran code. 
           
           Usage::
           
             u  = np.ones((mesh.dof),float)
             print 'L2-norm=',mesh.l2norm(u)

        """
        norm = space_f90.l2norm_1d(self.weights,self.jac,u)
        return norm
    
    def quadrature(self,f):
        """Computes the value of the integral 
        
           .. math::
              \\kappa = \\int_\\Omega f\\,d\\Omega 
           
           for :math:`f\\in L^2(\\Omega)` with GLL quadrature rules. 
        
           :param f: Basis coefficients of the function to be integrated given in local
                     data representation (since f in L2). 
           :returns: Value :math:`\\kappa` of the integral.
           :todo: Fortran code. 
        
        """
        kappa = space_f90.quadrature_1d(self.weights,self.jac,f)
        return kappa
                    
        
    def theta_phys(self, k, m):
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
           
           :todo: Function overloading for 1D, 2D and 3D problems,
           
           Example::
              
              for k in range(mesh.noe):
                  for m in range(mesh.n):
                      for n in range(mesh.n):
                          i, phys = mesh.theta_phys(k,m,n)
        '''
        i    = self.theta[k,m]
        phys = self.physical[k]
        return i, phys

    def theta_phys_bc(self, k):
        '''
           Local to global connectivity method for boundary points. 
           
           :param k: Element number
           :param m: Node number along the boundary element
           :type k: integer
           :type m: integer
           :returns: A tuple [i, name, bc_type, element_edge] of global node number i, corresponding 
                     physical name and type of boundary condition, either Dir or Nat. The type 
                     has to be specified in the Gmsh .geo file. 
                     element_edge: gives the internal element number and edge.
           
           
           To use this to apply boundary conditions to u::
           
              u_1 = 10.0
              u_2 =  5.0
              for k in range(mesh.noe_bc):              # Loops over the boundary elements
                  for m in range(mesh.n):               # Loops over the points along the boundary element
                      [i, name, bc_type, edge] = mesh.theta_phys_bc(k,m)
                      if name == 1:
                          u[i] = u_1                    # Assign bc
                      if name == 2:
                          u[i] = u_2                    # Assing bc 
           
        '''
        i       = self.theta_bc[k]
        phys    = self.physical_bc[k]
        boundarycondtion_type = self.bc_type[phys-1]
        element_edge = self.edge[k]
        
        return i, phys, boundarycondtion_type, element_edge
        
    def boundary_value(self,u):
        '''
        Creates an array of boundary values of a function u.
        
        :param u: An array in local data representation
        
        :returns: An array of boundary points.
        '''
        u_bound = np.zeros((self.noe_bc), float)
        
        for k in range(self.noe_bc):
            [i, phys, bc_type, element_edge] = self.theta_phys_bc(k)
            k_element = element_edge[0]
            if element_edge[1] == int(0):
                u_bound[k] = u[k_element,0]
            if element_edge[1] == int(1):
                u_bound[k] = u[k_element,self.n-1]
                              
        return u_bound
        
    def mapping_q(self,v):
        '''
        The mapping operator :math:`Q`.
        
        :param v: Numpy array in global data representation.
        :returns: Numpy array in local data representation
        
        The method maps a vector of global ordering to a local data representation. 
        This operator is used in the assembly or the action of a global matrix on a vector,
        
        .. math::
           \underline w=\underline  Q^T\underline A_L\underline Q\underline v=\underline A\,\underline v
           
        where :math:`\underline A_L` is e.g. the local Laplacian or the local mass matrix. 
        
           
        Given that a mesh object has already been created one can perform the matrix vector 
        product :math:`\underline v_{local}=\underline Q\underline v_{global}` by typing::
        
           v_local = mesh.mapping_Q(v_global)
        
        '''
        #w = np.zeros((self.noe,self.n),float)
        #for k in range(self.noe):
        #    for m in range(self.n):
        #        i = self.theta[k,m]
        #        w[k,m] = v[i]
        w = space_f90.mapping_q_1d(v,self.theta)
        return w
        
    def mapping_qt(self,w):
        '''
        The transpose :math:`Q^T` of the mapping operator :math:`Q`. This method maps an array 
        of local ordering to a global data representation. 
        
        :param w: Numpy array in local data representation.
        :returns: Numpy array in global data representation 
        
        The matrix vector product :math:`v_{global}=Q^Tv_{local}`::
        
           v_global = mesh.mapping_Q(v_local)
        
        '''
        #v = np.zeros(self.dof,float)
        #for k in range(self.noe):
        #    for m in range(self.n):
        #        i = self.theta[k,m]
        #        v[i] = v[i] + w[k,m]
        v = space_f90.mapping_qt_1d(w,self.theta,self.dof)
        return v

    def local_to_global(self,w):
        '''
        Maps a function in H1 from local to global
        '''
        #v = np.zeros(self.dof,float)
        #for k in range(self.noe):
        #    for m in range(self.n):
        #        i = self.theta[k,m]
        #        v[i] = w[k,m]
        #v=fortrancode.mapping_qt(w,self.theta,self.dof)
        v = space_f90.local_to_global_1d(w,self.theta,self.dof)
        return v
        
    def mask(self,w):
        '''
        This method masks nodal point values associated with a Dirichlet boundary condition.
        
        :param w: Numpy array in global data representation subject to masking.
        :returns: A masked numpy array in global data representation.
        
        '''
        for k in range(self.noe_bc):
            [i, name, bc_type, edge] = self.theta_phys_bc(k)
            if bc_type == 'Dir':
                w[i] = 0.0
        return w
        
    def mask_matrix(self,A):
        '''
        '''
        for k in range(self.noe_bc):
            [i, phys, bc_type, element_edge]=self.theta_phys_bc(k)
            if bc_type == "Dir":
                A[int(i),:] = 0.0
        return A
        
    def interpolation(self,u,m):
        '''
        Interpolates a function :math:`u_N\\in\\mathbb P_N(\\Omega)`
        to a function :math:`u\\in\\mathbb P_{m-1}(\\Omega)`.
        
        .. math::
           u=I_N^{m-1}u_N
        
        :param u: Basis coefficients of a function with polynomial degree N.
        :param m: Polynomial degree of the interpolated function.
        :returns: Basis coefficients of the interpolated functon :math:`u_{m-1}`. 
        '''
        n_local = u.shape[1]
        points_local, weights_local = self.basic.gauss_lobatto_legendre(n_local)
        points_int,   weights_int   = self.basic.gauss_lobatto_legendre(m)
        u_int = space_f90.interpolation_1d(points_int,u,points_local)
        return u_int
        
    def hyper_filter(self,u_tilde,alpha=0.25):
        '''
        A filter for hyperbolic problems (see Deville et al.). 
        
        .. math::
           u = F_\\alpha \\tilde u
           
        where the filter is
        
        .. math::
           F_\\alpha := \\alpha \\Pi_{N-1} + (1-\\alpha) I_N^N,\quad 
           \\Pi_{N-1} = I_{N-1}^N I_{N}^{N-1}
           
        Where :math:`\\alpha` is typically :math:`0.05<\\alpha<0.3`. 
           
        :param u_tilde: Basis coefficients of function to be filtered. 
        :param alpha: Weighting factor.
        :returns: Basis coefficients of the filtered function. 
           
        '''
        u1 = self.interpolation(u_tilde,self.n-1)
        u2 = self.interpolation(u1,self.n)
        u_out = alpha * u2 + (1.0 - alpha) * u_tilde
        return u_out
        
    def connectivity(self):
        theta, dof = space_f90.connectivity_1d(self.x)
        return theta, dof

    def boundary_connectivity_gmsh(self,j):
        u      = np.zeros((self.GTS.dof),float)
        noe_bc = self.GTS.theta_bc.shape[0]
        
        for k in range(noe_bc):
            i = self.GTS.theta_bc[k]
            if self.GTS.physical_bc[k] == j:
                u[i] = self.GTS.physical_bc[k]
                    
        return self.GTS.mapping_q(u)
        
        
    def boundary_connectivity_theta(self, theta_bc, physical_bc, jac_s, edge, count, u_gll, i):
        #
        for k in range(self.noe):
            alpha1=u_gll[k,0]
            alpha2=u_gll[k,self.n-1]
            if int(np.rint(alpha1)) == i:
                theta_bc[count]=self.theta[k,0]
                physical_bc[count]=i
                jac_s[count]=1.0
                edge[count,0] = k # element number
                edge[count,1] = 0 # edge numbe
                count = count +1
            if int(np.rint(alpha2)) == i:
                theta_bc[count]=self.theta[k,self.n-1]
                physical_bc[count]=i
                jac_s[count]=1.0
                edge[count,0] = k # element number
                edge[count,1] = 1 # edge numbe
                count = count +1
                    
        return theta_bc, physical_bc, jac_s, edge, count
        
    def boundary_connectivity(self):
        noe_bc      = self.GTS.theta_bc.shape[0]
        theta_bc    = np.zeros(noe_bc, int)
        jac_s       = np.zeros(noe_bc, float)
        u_gll       = np.zeros((self.noe,self.n), float)
        physical_bc = np.zeros(noe_bc, int)
        edge        = np.zeros((noe_bc, 2), int)
        
        # Locating boundary points
        count=0
        for i in range(self.GTS.physical_names.shape[0]):
            if self.GTS.physical_names[i,0] == 0:
                j = self.GTS.physical_names[i,1]
                u_gmsh = self.boundary_connectivity_gmsh(j)
                u_gll = self.interpolation(u_gmsh,self.n)
                theta_bc, physical_bc, jac_s, edge, count = \
                    self.boundary_connectivity_theta(theta_bc, physical_bc, jac_s,\
                                                     edge, count, u_gll, j)
        return theta_bc, physical_bc, jac_s, edge
        


