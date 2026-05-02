from processes import StochasticProcess
from libs import show


def simulation(sp: StochasticProcess, x_obs, y_obs, x_test, y_test):
    sp.observed(x_obs, y_obs)
    params = sp.find_MAP(start=[sp.get_params_current(), sp.get_params_random(sigma=0.6), sp.get_params_random(sigma=1.0)], points=1, plot=False)
    scores = sp.scores(params = params, space=x_test, hidden=y_test)
    sp.plot(params = params)
    show()
    sp.plot_model(params = params, indexs=[len(x_obs)//2, len(x_obs)//2+2])
    show()
    return params, scores