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
from scipy import linalg
import basic_f90


class Basic():
    '''
    Fundamental SEM routines. 
    
    This class contains methods for computing the GLL and GL 
    quadrature points and weights, the GLL derivative matrix and 
    values of the Legendre interpolants. 
    '''
    def __init__(self):
        pass
    
    def legendre(self,n, xi):
        """
        Computes the value :math:`\kappa` of the :math:`n`'th Legendre polynomial 
        
        .. math::
           \kappa = l_n(\\xi)
           
        evaluated at the point :math:`\\xi`, 
        where :math:`-1\le\\xi\le 1`.
        
        :param n: Number of points. 
        :type n: int
        :param xi: A point.  
        :type xi: float
        :returns: * **kappa** (float) - The value of :math:`l_n(\\xi)`. 
        
        
        **Example:**
        
        >>> import sempy
        >>> basic = sempy.basic.Basic( )
        >>> n = 3
        >>> xi = 0.7
        >>> print basic.legendre( n, xi )
        -0.1925
        """
        if n <= 0: # Just a control structure to avoid hang-up.
            L = 0.0
            print '***: Warning from sempy.basic.legendre: '
            print '---: Input value n was given an invalid value. n=',n
            return L
        
        if n > 0:
            L = basic_f90.legendre(n,xi)
        
        return L
    
    def legendre_derivative(self,n, xi):
        """
        Computes the value of the derivative of the :math:`n`'th Legendre polynomial 
        
        .. math::
           \kappa = l_n'(\\xi)
        
        evaluated at the point :math:`\\xi`, 
        where :math:`-1\le\\xi\le 1`.
                
        :param n: Number of points. 
        :type n: int
        :param xi: A point.  
        :type xi: float
        :returns: * **kappa** (float) - The value of :math:`l_n'(\\xi)`. 
        
        **Example:**
            
        >>> import sempy
        >>> basic = sempy.basic.Basic()
        >>> n = 3
        >>> xi = 0.7
        >>> print basic.legendre_derivative( n, xi )
        2.175
        
        """
        if n <= 0: # Just a control structure to avoid hang-up.
            Ld = 0.0
            print '***: Warning from sempy.basic.legendre_derivative: '
            print '---: Input value n was given an invalid value. n=',n
            return Ld
        if n > 0:
            Ld = basic_f90.legendre_derivative(n, xi)
        
        return Ld
    
    def gauss_legendre(self,n):
        """
        Creates the Gauss-Legendre quadrature points and weights 
        based on the number of points :math:`n`. 
        
        :param n: Number of points. 
        :type n: int
        :returns: * **points** (array) - Quadrature points. 
                  * **weights** (array) - Quadrature weights. 
        
        **Example:**
        
        >>> import sempy
        >>> basic = sempy.basic.Basic()
        >>> n = 3
        >>> points , weights = basic.gauss_legendre( n )
        >>> print points
        [-0.7745966692414834, 1.720588613669501e-17, 0.77459666924148329]
        >>> print weights
        [ 0.55555556  0.88888889  0.55555556]
        
        """
        if n > 1:
            A = basic_f90.gauss_legendre_1( n )
            
            la,v = linalg.eig( A )
            p = sorted( la.real )
    
            # This routine finds the weights
            w = basic_f90.gauss_legendre_2( p )
        else:
            p = 0.0
            w = 0.0
        
        return p,w

    def gauss_lobatto_legendre(self,n):
        """
        Creates the Gauss-Lobatto-Legendre quadrature points and weights 
        based on the number of points :math:`n`. 
        
        :param n: Number of points. 
        :type n: int
        :returns: * **points** (array) - Quadrature points. 
                  * **weights** (array) - Quadrature weights. 
                  
        **Example:**
        
        >>> import sempy
        >>> basic = sempy.basic.Basic()
        >>> n=3
        >>> points , weights = basic.gauss_lobatto_legendre( n )
        >>> print points
        [-1.  0.  1.]
        >>> print weights
        [ 0.33333333  1.33333333  0.33333333]
        """
    
        # Fortran code
        if n < 2:
            p = 0.0
            w = 0.0
            print '***: Warning from sempy.basic.gauss_lobatto_legendre: '
            print '---: Input value n was given an invalid value. n=',n
        
        if n == 2:
            GLpoints = 0.0
            p, w = basic_f90.gauss_lobatto_legendre(GLpoints,n)
                
        if n > 2:
            GLpoints,GLweights = self.gauss_legendre(n-1)
            p, w = basic_f90.gauss_lobatto_legendre(GLpoints,n)
        
        return p,w
    
    def derivative_matrix_gll(self,n):
        """
        This method constructs the derivative matrix 
        of the Lagrange derivatives l'_j(x_i)
        
        Consider the function 
        
        .. math::
        
           u(\\xi)=\sum_{i=0}^{n-1}\ell_i(\\xi)u_i 
        
        Its derivative at the GLL points 
        :math:`\\xi_j` (:math:`0\le j\le n-1`)  
        can be expressed as
        
        .. math::
        
           \\frac{\partial u}{\partial\\xi}\\bigg|_j=
           \sum_{i=0}^{n-1}\ell_i'(\\xi_j)u_i=
           \sum_{i=0}^{n-1}D_{ji}u_i
            
        where :math:`D\in\mathbb R^{n\\times n}` is the derivative matrix. 
           
        :param n: Number of points. 
        :type n: int
        :returns: **D** (array) - Derivative matrix.  
                  
        **Example:**
        
        >>> import sempy
        >>> basic = sempy.basic.Basic()
        >>> n = 3
        >>> D = basic.derivative_matrix_gll( n )
        >>> print D
        [[-1.5  2.  -0.5]
         [-0.5  0.   0.5]
         [ 0.5 -2.   1.5]]

        """
        [points, weights] = self.gauss_lobatto_legendre( n )
        D = basic_f90.lagrange_derivative_matrix( points )
        return D
    
    def lagrange(self,i,xi,gll_points):
        """
        This function returns the value of the :math:`i`'th Lagrangian interpolant 
        evaluated at the point x.
        
        :param i: Index :math:`0\le i\le n-1`. 
        :type i: int
        :param xi: Point.
        :type xi: float
        :param gll_points: GLL quadrature points
                           :math:`\\underline{\\xi}\\in\\mathbb R^{N-1},\\ -1< \\xi_j < 1`. 
        :type gll_points: array
        :returns: Value. 
    
        **Example:**
        
        >>> import sempy
        >>> basic = sempy.basic.Basic()
        >>> n = 3
        >>> p , w = basic.gauss_lobatto_legendre(n)
        >>> xi = 0.3
        >>> print basic.lagrange(n-1, xi, p)
        0.195
        """
        La = basic_f90.lagrange( i+1, xi, gll_points )
        return La

#def legendre(n, x):
#    if n <= 0: # Just a control structure to avoid hang-up.
#        L = 0.0
#        print '***: Warning from sempy.basic.legendre: '
#        print '---: Input value n was given an invalid value. n=',n
#        return L
#     
#    if n > 0:
#        L = basic_f90.legendre(n,x)
#        
#    return L


#def legendre_derivative(n, x):
#    if n <= 0: # Just a control structure to avoid hang-up.
#        Ld = 0.0
#        print '***: Warning from sempy.basic.legendre_derivative: '
#        print '---: Input value n was given an invalid value. n=',n
#        return Ld
#    if n > 0:
#        Ld = basic_f90.legendre_derivative(n, x)
#        
#    return Ld



#def gauss_legendre(n):
#    if n > 1:
#        A = basic_f90.gauss_legendre_1(n)
#    
#        la,v = linalg.eig(A)
#        p = sorted(la.real)
#    
#        # This loop finds the associated weights
#        w = basic_f90.gauss_legendre_2(p)
#    else:
#        p = 0.0
#        w = 0.0
#        
#    return p,w

#def gauss_lobatto_legendre(n):
#    if n < 2:
#        p = 0.0
#        w = 0.0
#        print '***: Warning from sempy.basic.gauss_lobatto_legendre: '
#        print '---: Input value n was given an invalid value. n=',n
#        
#    if n == 2:
#        GLpoints = 0.0
#        p, w = basic_f90.gauss_lobatto_legendre(GLpoints,n)
#                
#    if n > 2:
#        GLpoints,GLweights = gauss_legendre(n-1)
#        p, w = basic_f90.gauss_lobatto_legendre(GLpoints,n)
#        
#    return p,w



#def lagrange_derivative_matrix_gll(n):
#    GLLPoints,GLLWeights = gauss_lobatto_legendre(n)
#    D = basic_f90.lagrange_derivative_matrix(GLLPoints)
#    return D



#def lagrange(i,n,x,gll_points):
#    La = basic_f90.lagrange(i+1,x,gll_points)
#    return La
 

if __name__ == "__main__":
    import doctest
    doctest.testmod()