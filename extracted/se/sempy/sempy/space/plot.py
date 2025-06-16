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
#import sempy.basic as basic
#import sempy.space.space_f90 as space_f90

#import matplotlib.pyplot as plt
from matplotlib import pyplot as pl
#from mpl_toolkits.mplot3d import axes3d
#from matplotlib import cm


class Plot:
    '''
    An interface to matplotlib for easy plotting of 
    Sempy functions
    '''
    def __init__(self,Space):
        self.Space = Space
    
    def plot3d(self, u,contours=[0.01,0.02]):
        try:
            import enthought.mayavi
        except:
            print 'No mayavi python module installed.'
            print '3D plotting not possible.'
            return

        v_fem = sempy.Function(self.Space.fem, filename = 'test_data')
        v_fem.basis_coeff = self.Space.fem.sem_to_fem(u.basis_coeff)
        v_fem.to_file()

        vtkFile='test_data0.vtk'

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
            
    def plot2d( self, u, min = 0.0, max = 0.1, levels = 10,
                n_int = 10, type = 'countorf' ):
        '''
        Plot a 2D function.
        '''
        fig = pl.figure()
        x = self.Space.interpolation(self.Space.x,n_int)
        y = self.Space.interpolation(self.Space.y,n_int)
        z = self.Space.interpolation(u.basis_coeff,n_int)
        
        du=(max-min)/float(levels)
        levels = np.arange(min, max, du)
        
        if type == 'countorf':
            for k in range(self.Space.noe):
                cset1 = pl.contourf(x[k,:,:], y[k,:,:], z[k,:,:], levels)
        if type == 'countor':
            for k in range(self.Space.noe):
                cset1 = pl.contour(x[k,:,:], y[k,:,:], z[k,:,:], levels)
        pl.xlabel(r'$x$')
        pl.ylabel(r'$y$')              
        pl.axis([self.Space.x.min(), self.Space.x.max(), self.Space.y.min(), self.Space.y.max()])  
        pl.colorbar(cset1)
        pl.show()

        