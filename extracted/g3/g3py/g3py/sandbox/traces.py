
def trace_to_dataframe(trace, chains=None, flat_names=None, hide_transformed_vars=True):
    # TODO: mientras pymc3 se arregla
    var_shapes = trace._straces[0].var_shapes
    if flat_names is None:
        flat_names = {v: pm.backends.tracetab.create_flat_names(v, shape)
                      for v, shape in var_shapes.items()
                      if not (hide_transformed_vars and v.endswith('_'))}

    var_dfs = []
    for varname, shape in var_shapes.items():
        if not hide_transformed_vars or not varname.endswith('_'):
            vals = trace.get_values(varname, combine=True, chains=chains)
            flat_vals = vals.reshape(vals.shape[0], -1)
            var_dfs.append(pd.DataFrame(flat_vals, columns=flat_names[varname]))
    return pd.concat(var_dfs, axis=1)


def dump_trace(name, trace, chains=None):
    # TODO: mientras pymc3 se arregla
    if not os.path.exists(name):
        os.mkdir(name)
    if chains is None:
        chains = trace.chains

    var_shapes = trace._straces[chains[0]].var_shapes
    flat_names = {v: pm.backends.tracetab.create_flat_names(v, shape)
                  for v, shape in var_shapes.items()}

    for chain in chains:
        filename = os.path.join(name, 'chain-{}.csv'.format(chain))
        df = trace_to_dataframe(trace, chains=chain, flat_names=flat_names, hide_transformed_vars=False)
        df.to_csv(filename, index=False)


def traceplot(trace, plot_transformed=True):
    pm.traceplot(trace, plot_transformed=plot_transformed)
