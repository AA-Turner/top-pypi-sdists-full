"""
Class for parallelizing GridSearchCV jobs in scikit-learn
"""

from sklearn.model_selection import ParameterGrid
from sklearn.model_selection._search import _check_param_grid
from spark_sklearn.base_search import SparkBaseSearchCV


class GridSearchCV(SparkBaseSearchCV):
    """Exhaustive search over specified parameter values for an estimator.
    
    Important members are fit, predict.
    
    GridSearchCV implements a "fit" and a "score" method.
    It also implements "predict", "predict_proba", "decision_function",
    "transform" and "inverse_transform" if they are implemented in the
    estimator used.
    
    The parameters of the estimator used to apply these methods are optimized
    by cross-validated grid-search over a parameter grid.

    Parameters
    ----------
    estimator : estimator object.
        This is assumed to implement the scikit-learn estimator interface.
        Either estimator needs to provide a ``score`` function,
        or ``scoring`` must be passed.
    
    param_grid : dict or list of dictionaries
        Dictionary with parameters names (string) as keys and lists of
        parameter settings to try as values, or a list of such
        dictionaries, in which case the grids spanned by each dictionary
        in the list are explored. This enables searching over any sequence
        of parameter settings.
    
    scoring : string, callable or None, default=None
        A string (see model evaluation documentation) or
        a scorer callable object / function with signature
        ``scorer(estimator, X, y)``.
        If ``None``, the ``score`` method of the estimator is used.
    
    fit_params : dict, optional
        Parameters to pass to the fit method.
    
    n_jobs : int, default=1
        Number of jobs to run in parallel.
    
    pre_dispatch : int, or string, optional
        Not used; exists for scikit-learn compatibility.

    iid : boolean, default=True
        If True, the data is assumed to be identically distributed across
        the folds, and the loss minimized is the total loss per sample,
        and not the mean loss across the folds.
    
    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:

        - None, to use the default 3-fold cross validation,
        - integer, to specify the number of folds in a `(Stratified)KFold`,
        - An object to be used as a cross-validation generator.
        - An iterable yielding train, test splits.

        For integer/None inputs, if the estimator is a classifier and ``y`` is
        either binary or multiclass, :class:`StratifiedKFold` is used. In all
        other cases, :class:`KFold` is used.
    
    refit : boolean, default=True
        Refit the best estimator with the entire dataset.
        If "False", it is impossible to make predictions using
        this GridSearchCV instance after fitting.
    
    verbose : integer
        Controls the verbosity: the higher, the more messages.
    
    error_score : 'raise' (default) or numeric
        Value to assign to the score if an error occurs in estimator fitting.
        If set to 'raise', the error is raised. If a numeric value is given,
        FitFailedWarning is raised. This parameter does not affect the refit
        step, which will always raise the error.
    
    return_train_score : boolean, default=True
        If ``'False'``, the ``cv_results_`` attribute will not include training
        scores.
    
    Examples
    --------
    >>> from sklearn import svm, datasets
    >>> from spark_sklearn.grid_search import GridSearchCV
    >>> from spark_sklearn.util import createLocalSparkSession
    >>> sc = createLocalSparkSession().sparkContext
    >>> iris = datasets.load_iris()
    >>> parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
    >>> svr = svm.SVC(gamma='auto')
    >>> clf = GridSearchCV(sc, svr, parameters)
    >>> clf.fit(iris.data, iris.target)
    ...                             # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    GridSearchCV(cv=3, error_score=...,
           estimator=SVC(C=1.0, cache_size=..., class_weight=..., coef0=...,
                         decision_function_shape=..., degree=..., gamma=...,
                         kernel='rbf', max_iter=-1, probability=False,
                         random_state=None, shrinking=True, tol=...,
                         verbose=False),
           fit_params={}, iid=..., n_jobs=1,
           param_grid=..., pre_dispatch=..., refit=...,
           scoring=..., verbose=...)
    >>> sorted(clf.cv_results_.keys())
    ...                             # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    ['mean_fit_time', 'mean_score_time', 'mean_test_score',...
     'mean_train_score', 'param_C', 'param_kernel', 'params',...
     'rank_test_score', 'split0_test_score',...
     'split0_train_score', 'split1_test_score', 'split1_train_score',...
     'split2_test_score', 'split2_train_score',...
     'std_fit_time', 'std_score_time', 'std_test_score', 'std_train_score'...]
    
    Attributes
    ----------
    cv_results_ : dict of numpy (masked) ndarrays
        A dict with keys as column headers and values as columns, that can be
        imported into a pandas ``DataFrame``.
        For instance the below given table

        +------------+-----------+------------+-----------------+---+---------+
        |param_kernel|param_gamma|param_degree|split0_test_score|...|rank.....|
        +============+===========+============+=================+===+=========+
        |  'poly'    |     --    |      2     |        0.8      |...|    2    |
        +------------+-----------+------------+-----------------+---+---------+
        |  'poly'    |     --    |      3     |        0.7      |...|    4    |
        +------------+-----------+------------+-----------------+---+---------+
        |  'rbf'     |     0.1   |     --     |        0.8      |...|    3    |
        +------------+-----------+------------+-----------------+---+---------+
        |  'rbf'     |     0.2   |     --     |        0.9      |...|    1    |
        +------------+-----------+------------+-----------------+---+---------+

        will be represented by a ``cv_results_`` dict of::

            {
            'param_kernel': masked_array(data = ['poly', 'poly', 'rbf', 'rbf'],
                                         mask = [False False False False]...)
            'param_gamma': masked_array(data = [-- -- 0.1 0.2],
                                        mask = [ True  True False False]...),
            'param_degree': masked_array(data = [2.0 3.0 -- --],
                                         mask = [False False  True  True]...),
            'split0_test_score'  : [0.8, 0.7, 0.8, 0.9],
            'split1_test_score'  : [0.82, 0.5, 0.7, 0.78],
            'mean_test_score'    : [0.81, 0.60, 0.75, 0.82],
            'std_test_score'     : [0.02, 0.01, 0.03, 0.03],
            'rank_test_score'    : [2, 4, 3, 1],
            'split0_train_score' : [0.8, 0.9, 0.7],
            'split1_train_score' : [0.82, 0.5, 0.7],
            'mean_train_score'   : [0.81, 0.7, 0.7],
            'std_train_score'    : [0.03, 0.03, 0.04],
            'mean_fit_time'      : [0.73, 0.63, 0.43, 0.49],
            'std_fit_time'       : [0.01, 0.02, 0.01, 0.01],
            'mean_score_time'    : [0.007, 0.06, 0.04, 0.04],
            'std_score_time'     : [0.001, 0.002, 0.003, 0.005],
            'params'             : [{'kernel': 'poly', 'degree': 2}, ...],
            }

        NOTE that the key ``'params'`` is used to store a list of parameter
        settings dict for all the parameter candidates.
        The ``mean_fit_time``, ``std_fit_time``, ``mean_score_time`` and
        ``std_score_time`` are all in seconds.
    
    best_estimator_ : estimator
        Estimator that was chosen by the search, i.e. estimator
        which gave highest score (or smallest loss if specified)
        on the left out data. Not available if refit=False.
    
    best_score_ : float
        Score of best_estimator on the left out data.
    
    best_params_ : dict
        Parameter setting that gave the best results on the hold out data.
    
    best_index_ : int
        The index (of the ``cv_results_`` arrays) which corresponds to the best
        candidate parameter setting.
        The dict at ``search.cv_results_['params'][search.best_index_]`` gives
        the parameter setting for the best model, that gives the highest
        mean score (``search.best_score_``).
    
    scorer_ : function
        Scorer function used on the held out data to choose the best
        parameters for the model.
    
    n_splits_ : int
        The number of cross-validation splits (folds/iterations).

    Notes
    ------
    The parameters selected are those that maximize the score of the left out
    data, unless an explicit score is passed in which case it is used instead.
    
    See Also
    ---------
    :class:`ParameterGrid`:
        generates all the combinations of a hyperparameter grid.
    
    :func:`sklearn.model_selection.train_test_split`:
        utility function to split the data into a development set usable
        for fitting a GridSearchCV instance and an evaluation set for
        its final evaluation.
    
    :func:`sklearn.metrics.make_scorer`:
        Make a scorer from a performance metric or loss function.
    
    """

    def __init__(self, sc, estimator, param_grid, scoring=None, fit_params=None,
                 n_jobs=1, iid=True, refit=True, cv=3, verbose=0,
                 pre_dispatch='2*n_jobs', error_score='raise', return_train_score=True):
        super(GridSearchCV, self).__init__(
            estimator=estimator, scoring=scoring, n_jobs=n_jobs, iid=iid,
            refit=refit, cv=cv, verbose=verbose, pre_dispatch=pre_dispatch, error_score=error_score,
            return_train_score=return_train_score)

        self.fit_params = fit_params if fit_params is not None else {}

        self.sc = sc
        self.param_grid = param_grid

        self.cv_results_ = None
        _check_param_grid(param_grid)
    
    def fit(self, X, y=None, groups=None):
        """Run fit with all sets of parameters.
        
        Parameters
        ----------
        
        X : array-like, shape = [n_samples, n_features]
            Training vector, where n_samples is the number of samples and
            n_features is the number of features.
        
        y : array-like, shape = [n_samples] or [n_samples, n_output], optional
            Target relative to X for classification or regression;
            None for unsupervised learning.
        
        groups : array-like, with shape (n_samples,), optional
            Group labels for the samples used while splitting the dataset into
            train/test set.
        """
        return self._fit(X, y, groups, ParameterGrid(self.param_grid))

