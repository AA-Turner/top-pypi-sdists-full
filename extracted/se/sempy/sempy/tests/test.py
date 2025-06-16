


if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    import sempy
    
    X = sempy.Space(filename = 'cube', n = 4, dim = 3)
    X_fem = sempy.precond.SpaceFEM(X)
    #X_fem.plot_mesh()
    #A = sempy.operators.Laplacian(X).matrix
    
    #f = sempy.Function( X, basis_coeff = 1.0 )
    #b = sempy.operators.Mass( X ).action_local( f.basis_coeff )
    #u = sempy.Function( X, basis_coeff = 0.0 )
    
    #[v, flag] = sempy.linsolvers.Krylov().solve(A, b, u.glob())
    #u.basis_coeff = X.mapping_q(v)
    #u.plot_wire()
    
