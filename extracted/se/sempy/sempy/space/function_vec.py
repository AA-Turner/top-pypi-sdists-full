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
import numpy as np


class VectorFunction:
    '''
    A vector function used to represent e.g. the velocity vector field. 
    
    .. math::
    
       \\mathbf u\in (H^1(\Omega))^d
    
    :param Space: The function space.
    :type Space: :class:`sempy.Space`
    :param filename: The filename. 
    :type filename: string
    '''
    def __init__( self, Space, filename = None ):
        self.Space = Space
        self.filename = filename
        self.file_count = 0
        
        self.U= []
        if self.Space.dim == 1:
            self.U.append(sempy.Function( self.Space, basis_coeff = 0.0, 
                                      filename = 'none' ))
            self.U.append('none')
            self.U.append('none')
            
        if self.Space.dim == 2:
            self.U.append(sempy.Function( self.Space, basis_coeff = 0.0, 
                                          filename = 'none' ))
            self.U.append(sempy.Function( self.Space, basis_coeff = 0.0, 
                                          filename = 'none' ))
            self.U.append('none')
            
        if self.Space.dim == 3:
            self.U.append(sempy.Function( self.Space, basis_coeff = 0.0, 
                                          filename = 'none' ))
            self.U.append(sempy.Function( self.Space, basis_coeff = 0.0, 
                                          filename = 'none' ))
            self.U.append(sempy.Function( self.Space, basis_coeff = 0.0, 
                                          filename = 'none' ))
    #def __setitem__(self,index,value):
    #    self.U[index].basis_coeff = value
    #    return self.U[index]
    
    def __getitem__(self,index):
       return self.U[index]
    
    def vorticity(self):
        #
        if self.Space.dim ==2:
            [u_x,u_y] = self.U[0].grad()
            [v_x,v_y] = self.U[1].grad()
            #omega = sempy.Function( self.Space , basis_coeff = v_x-u_y )
            #omega.plot( legend = legend, filled = filled,
            #            resolution = resolution, 
            #            show_elements = show_elements,
            #            font_size = font_size, show = show,
            #            lower=lower, upper = upper )
            return v_x-u_y
        
    def plot_vorticity(self,legend=True,filled=True,resolution=20,
                       show_elements=True,font_size=20, show=True,
                       lower='none',upper='none'):
        '''
        Plots the vorticity :math:`\omega`:  
        
        .. math::
        
           \\omega= \\frac{\\partial v}{\\partial x}-
                    \\frac{\\partial u}{\\partial y}
        '''
        if self.Space.dim ==2:
            [u_x,u_y]=self.U[0].grad()
            [v_x,v_y]=self.U[1].grad()
            omega = sempy.Function( self.Space , basis_coeff = v_x-u_y )
            omega.plot( legend = legend, filled = filled,
                        resolution = resolution, 
                        show_elements = show_elements,
                        font_size = font_size, show = show,
                        lower=lower, upper = upper )
        else:
            print 'Vorticity plot not implemented for 1D and 2D.'
        
        
    def plot_stream_function(self, legend = True, filled = True,
                             resolution = 20, show_elements = True,
                             font_size = 20, show = False,
                             show_boundary=False,
                             lower='none',upper='none'):
        '''
        Plots the stream-function :math:`\psi`.
        
        .. math::
        
           -\\nabla^2 \psi=\\omega
        
        where the vorticity :math:`\omega` is  
        
        .. math::
        
           \\omega= \\frac{\\partial v}{\\partial x}-
                    \\frac{\\partial u}{\\partial y}
        
        and the boundary conditions are
        
        .. math::
           \\frac{\\partial\psi}{\\partial x}\\cdot\\mathbf n\\bigg|_\Gamma=
           -v
           
           \\frac{\\partial\psi}{\\partial y}\\cdot\\mathbf n\\bigg|_\Gamma=
           u
        '''
        if self.Space.dim ==1:
            print '***: Calculation of the stream-function is not'
            print '    implemented for 1D.'
        if self.Space.dim ==2:
            
            # Vorticity, omega
            [u_x,u_y]=self.U[0].grad()
            [v_x,v_y]=self.U[1].grad()
            omega = sempy.Function( self.Space , 
                                    basis_coeff = v_x-u_y )
            # Weak BC
            weak_x = sempy.BoundaryFunction( self.Space, mask = 'no' ) 
            weak_y = sempy.BoundaryFunction( self.Space, mask = 'no' ) 
            for i in range(5):
                weak_x.set_value(-self.U[1].basis_coeff,i)
                weak_y.set_value(self.U[0].basis_coeff,i)
            #print 'weak_x=',weak_x.basis_coeff*self.Space.n_unit[1]
            weak_x.basis_coeff = weak_x.basis_coeff*self.Space.n_unit[0]
            weak_y.basis_coeff = weak_y.basis_coeff*self.Space.n_unit[1]
            g_neu = sempy.BoundaryFunction( self.Space, mask = 'no' )
            g_neu.basis_coeff = weak_x.basis_coeff + weak_y.basis_coeff
            
            # Lapalcian
            lap = sempy.operators.Laplacian( self.Space, g_neu = g_neu,
                                             mask = 'no',
                                             fem_assemble = 'yes' )
            A = lap.matrix
            b_weak = lap.linear_form
            
            # RHS
            mass = sempy.operators.Mass( self.Space, mask = 'no' )
            M = mass.matrix
            b = M*omega.glob() + b_weak
            print 'sum b1=',b.sum()
            alpha=0.0
            for k in range(self.Space.dof):
                alpha=alpha+b[k]
            b=b-alpha/float(self.Space.dof)
            print 'sum b2=',b.sum()
            # Solver
            solver = sempy.linsolvers.Krylov(tol = 1e-09,
                                    solver_type = 'cg',
                                    maxiter = 2000)
                                    #pre = P_A )
            # Solve
            s = np.zeros( (self.Space.dof), float )
            psi = sempy.Function( self.Space )
            s, iter = solver.solve(A,b,s)
            psi = sempy.Function( self.Space, 
                                  basis_coeff = self.Space.mapping_q( s )  )
            print 'converged at iter=',iter
            #psi.plot_wire()
            #print psi.basis_coeff
            psi.plot( legend = legend, filled = filled, 
                      resolution = resolution, show_elements = show_elements,
                      font_size = font_size, show = show,
                      show_boundary=show_boundary,
                      lower = lower, upper = upper)
            
        if self.Space.dim ==3:
            print '***: Calculation of the stream-function is not'
            print '    implemented for 3D.'
            
    def calc_stream_function(self):
        '''
        Calculates the stream function.
        '''
        if self.Space.dim ==1:
            print '***: Calculation of the stream-function is not'
            print '    implemented for 1D.'
        if self.Space.dim ==2:
            
            # Vorticity, omega
            [u_x,u_y]=self.U[0].grad()
            [v_x,v_y]=self.U[1].grad()
            omega = sempy.Function( self.Space , 
                                    basis_coeff = v_x-u_y )
            # Weak BC
            weak_x = sempy.BoundaryFunction( self.Space, mask = 'no' ) 
            weak_y = sempy.BoundaryFunction( self.Space, mask = 'no' ) 
            for i in range(5):
                weak_x.set_value(-self.U[1].basis_coeff,i)
                weak_y.set_value(self.U[0].basis_coeff,i)
            #print 'weak_x=',weak_x.basis_coeff*self.Space.n_unit[1]
            weak_x.basis_coeff = weak_x.basis_coeff*self.Space.n_unit[0]
            weak_y.basis_coeff = weak_y.basis_coeff*self.Space.n_unit[1]
            g_neu = sempy.BoundaryFunction( self.Space, mask = 'no' )
            g_neu.basis_coeff = weak_x.basis_coeff + weak_y.basis_coeff
            
            # Lapalcian
            lap = sempy.operators.Laplacian( self.Space, g_neu = g_neu,
                                             mask = 'no',
                                             fem_assemble = 'yes',
                                             silent = True )
            A = lap.matrix
            b_weak = lap.linear_form
            
            # RHS
            mass = sempy.operators.Mass( self.Space, mask = 'no' )
            M = mass.matrix
            b = M*omega.glob() + b_weak
            print 'sum b1=',b.sum()
            alpha=0.0
            for k in range(self.Space.dof):
                alpha=alpha+b[k]
            b=b-alpha/float(self.Space.dof)
            print 'sum b2=',b.sum()
            # Solver
            solver = sempy.linsolvers.Krylov(tol = 1e-09,
                                    solver_type = 'cg',
                                    maxiter = 2000)
                                    #pre = P_A )
            # Solve
            s = np.zeros( (self.Space.dof), float )
            psi = sempy.Function( self.Space )
            s, iter = solver.solve(A,b,s)
            psi = sempy.Function( self.Space, 
                                  basis_coeff = self.Space.mapping_q( s )  )
            print 'Calc. stream func. conv. at it.=',iter
            return psi.basis_coeff
            
        if self.Space.dim ==3:
            print '***: Calculation of the stream-function is not'
            print '    implemented for 3D.'
    
                    
    def to_file(self):
        '''
        Print to file.
        '''
        if not self.filename == None:
            if self.Space.dim == 2:
                print 'to file=',self.filename
                self.__to_file_2d()
            
            if self.Space.dim == 3:
                self.__to_file_3d()
    
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
        a[0] = self.Space.fem.dof
        f.write(np.array_str(a[0]))
        f.write(' float\n')
        
        
        xx = self.Space.fem.local_to_global(self.Space.fem.x)
        yy = self.Space.fem.local_to_global(self.Space.fem.y)
        zz = np.zeros((self.Space.dof),float)

        for k in range(self.Space.fem.dof):
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
        __u = self.Space.fem.sem_to_fem(self.U[0].basis_coeff)
        __v = self.Space.fem.sem_to_fem(self.U[1].basis_coeff)
        _u = self.Space.fem.local_to_global(__u)
        _v = self.Space.fem.local_to_global(__v)
        _w = np.zeros((self.Space.dof),float)
    
        #_u = self.Space.fem.local_to_global(__u)#self.basis_coeff)
        
        f.write('POINT_DATA ')
        a = np.zeros(1,np.int)
        a[0] = self.Space.fem.dof
        f.write( np.array_str(a[0]) )
        f.write('\n')
        f.write('VECTORS stians float\n')
        #a=np.zeros(1,np.float)
        #a[0]=3.0
        for k in range(self.Space.fem.dof):
            f.write(np.array_str(_u[k]))
            f.write(' ')
            f.write(np.array_str(_v[k]))
            f.write(' ')
            f.write(np.array_str(_w[k]))
            f.write(' \n')
        f.write('\n')
    
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
        a[0] = self.Space.fem.dof
        f.write(np.array_str(a[0]))
        f.write(' float\n')
        
        
        xx = self.Space.fem.local_to_global(self.Space.fem.x)
        yy = self.Space.fem.local_to_global(self.Space.fem.y)
        zz = self.Space.fem.local_to_global(self.Space.fem.z)
        
        for k in range(self.Space.fem.dof):
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
        __u = self.Space.fem.sem_to_fem(self.U[0].basis_coeff)
        __v = self.Space.fem.sem_to_fem(self.U[1].basis_coeff)
        __w = self.Space.fem.sem_to_fem(self.U[2].basis_coeff)
        
        _u = self.Space.fem.local_to_global(__u)
        _v = self.Space.fem.local_to_global(__v)
        _w = self.Space.fem.local_to_global(__w)
        
     
        #f.write('LOOKUP_TABLE default\n')    
        f.write('POINT_DATA ')
        a = np.zeros(1,np.int)
        a[0] = self.Space.fem.dof
        f.write( np.array_str(a[0]) )
        f.write('\n')
        f.write('VECTORS stians float\n')
    
        #a=np.zeros(1,np.float)
        #a[0]=3.0
        for k in range(self.Space.fem.dof):
            f.write(np.array_str(_u[k]))
            f.write(' ')
            f.write(np.array_str(_v[k]))
            f.write(' ')
            f.write(np.array_str(_w[k]))
            #f.write(np.array_str(a[0]))
            f.write(' \n')
        f.write('\n')
    
        f.close()
       
    
            
        
        