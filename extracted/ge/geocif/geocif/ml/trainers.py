import multiprocessing as mp

import numpy as np
import pandas as pd
import optuna
from catboost import CatBoostRegressor
from geocif.progress import pbar as _pbar
from . import threads as ml_threads


class BassRegressor:
    """scikit-learn-style wrapper around pyBASS (BASS = Bayesian Adaptive
    Spline Surfaces = Bayesian MARS: adaptive hinge-spline bases + automatic
    interaction selection, MCMC-fit).

    One-hot-encodes categorical/object columns, fills NaN with the train
    median, and returns the posterior-MEAN prediction. pyBASS is a git-only
    optional dependency (``pip install git+https://github.com/lanl/pyBASS.git``)
    imported lazily so geocif installs without it. Tuned poppy defaults
    (maxInt=1 additive, npart=15) beat cubist on MIN_ESI4WK LOOCV (0.489 vs
    0.443); interactions overfit the small sample.
    """

    def __init__(self, max_int=1, npart=15, max_basis=1000,
                 nmcmc=14000, nburn=9000, thin=10):
        self.max_int = max_int
        self.npart = npart
        self.max_basis = max_basis
        self.nmcmc = nmcmc
        self.nburn = nburn
        self.thin = thin

    def get_params(self, deep=True):
        return dict(max_int=self.max_int, npart=self.npart, max_basis=self.max_basis,
                    nmcmc=self.nmcmc, nburn=self.nburn, thin=self.thin)

    def set_params(self, **p):
        for k, v in p.items():
            setattr(self, k, v)
        return self

    def _numeric(self, X):
        X = pd.DataFrame(X).copy()
        obj = list(X.select_dtypes(include=["object", "category"]).columns)
        if obj:
            X = pd.get_dummies(X, columns=obj, dummy_na=False)
        return X.apply(pd.to_numeric, errors="coerce")

    def fit(self, X, y):
        try:
            import pyBASS as pb
        except ImportError as exc:
            raise ImportError(
                "model = 'bass' requires pyBASS (Bayesian MARS), a git-only "
                "optional dependency:\n"
                "    pip install git+https://github.com/lanl/pyBASS.git"
            ) from exc
        Xn = self._numeric(X)
        self._median = Xn.median(numeric_only=True)
        Xn = Xn.fillna(self._median).fillna(0.0)
        self.columns_ = list(Xn.columns)
        self.model_ = pb.bass(
            Xn.values.astype(float), np.asarray(y, dtype=float),
            maxInt=self.max_int, npart=self.npart, maxBasis=self.max_basis,
            nmcmc=self.nmcmc, nburn=self.nburn, thin=self.thin, verbose=False,
        )
        return self

    def predict(self, X):
        Xn = self._numeric(X).reindex(columns=self.columns_, fill_value=0.0)
        Xn = Xn.fillna(self._median).fillna(0.0)
        preds = np.asarray(self.model_.predict(Xn.values.astype(float)))
        return preds.mean(axis=0)


class GeorgeGPRegressor:
    """sklearn-style wrapper around ``george`` (dfm/george, C++ GP library) —
    exact GP regression with a fitted-hyperparameter isotropic kernel.

    Routed like the existing ``gpr`` model: geocif hands it a StandardScaler-
    scaled numeric matrix (cat features dropped), so inputs arrive standardized.
    Design choices, per the george docs' production guidance:

    * isotropic ExpSquaredKernel (one shared length scale). ARD with our
      D≈50-1000 features on a few-hundred-row fold is D+ hyperparameters on a
      multimodal marginal likelihood — ill-conditioned and slow. Matern 3/2 /
      5/2 selectable via [ML] george_kernel for rougher response surfaces.
    * metric initialized to D (squared length scale): squared distances
      between standardized D-dim points concentrate around 2D, so metric=D
      keeps exp(-r²/2ℓ²) away from the all-zeros regime at init.
    * mean=mean(y) with fit_mean=True; amplitude init var(y).
    * positive-definiteness: fixed jitter via ``yerr`` (relative to std(y))
      PLUS fitted white noise — the two mechanisms the docs recommend for the
      near-duplicate rows a region-year yield table is full of.
    * BasicSolver (default). HODLR "doesn't (in general) scale well with the
      number of input dimensions" (docs) and is approximate; our n is a few
      hundred, so exact O(n³) Cholesky is trivially cheap.
    * hardened NLL optimization (L-BFGS-B, quiet=True, 1e25 on non-finite),
      verbatim pattern from the george hyperparameter tutorial. Falls back to
      the init vector if optimization lands on a non-finite optimum.

    george predict() does not store training targets — the wrapper keeps
    (X_train, y_train) and passes y every call. ``predict_std`` exposes the
    posterior std (latent var + fitted noise var) for future CI use.
    george is an OPTIONAL dep (PyPI wheels for linux x86_64/win but not
    aarch64): ``pip install geocif[george]`` or ``pixi add george``.
    """

    def __init__(self, kernel="expsquared", jitter=1e-3):
        self.kernel = kernel
        self.jitter = jitter

    def get_params(self, deep=True):
        return dict(kernel=self.kernel, jitter=self.jitter)

    def set_params(self, **p):
        for k, v in p.items():
            setattr(self, k, v)
        return self

    def _numeric(self, X):
        X = pd.DataFrame(X).copy()
        obj = list(X.select_dtypes(include=["object", "category"]).columns)
        if obj:
            X = pd.get_dummies(X, columns=obj, dummy_na=False)
        return X.apply(pd.to_numeric, errors="coerce")

    def _kernel(self, D, var_y):
        from george import kernels as gk

        metric = float(D)
        if self.kernel == "matern32":
            k = gk.Matern32Kernel(metric=metric, ndim=D)
        elif self.kernel == "matern52":
            k = gk.Matern52Kernel(metric=metric, ndim=D)
        else:
            k = gk.ExpSquaredKernel(metric=metric, ndim=D)
        return var_y * k

    def fit(self, X, y):
        try:
            import george
        except ImportError as exc:
            raise ImportError(
                "model = 'george' requires the `george` GP library, an "
                "OPTIONAL geocif extra (PyPI ships no aarch64 wheels, so it "
                "can't be a core dep). Install with:\n"
                "    pip install geocif[george]\n"
                "or on the pixi cluster env:\n"
                "    pixi add --manifest-path <geo-run>/pixi.toml george"
            ) from exc
        from scipy.optimize import minimize

        Xn = self._numeric(X)
        self._median = Xn.median(numeric_only=True)
        Xn = Xn.fillna(self._median).fillna(0.0)
        self.columns_ = list(Xn.columns)
        Xv = Xn.values.astype(float)
        yv = np.asarray(y, dtype=float).ravel()

        self._X_train = Xv
        self._y_train = yv
        D = Xv.shape[1]
        var_y = float(np.var(yv))
        if not np.isfinite(var_y) or var_y <= 0:
            var_y = 1.0
        std_y = np.sqrt(var_y)

        self._gp = george.GP(
            self._kernel(D, var_y),
            mean=float(np.mean(yv)),
            fit_mean=True,
            white_noise=np.log(var_y * 0.1),
            fit_white_noise=True,
        )
        self._gp.compute(Xv, yerr=self.jitter * std_y)

        def nll(p):
            self._gp.set_parameter_vector(p)
            ll = self._gp.log_likelihood(yv, quiet=True)
            return -ll if np.isfinite(ll) else 1e25

        def grad_nll(p):
            self._gp.set_parameter_vector(p)
            return -self._gp.grad_log_likelihood(yv, quiet=True)

        p0 = self._gp.get_parameter_vector()
        result = minimize(nll, p0, jac=grad_nll, method="L-BFGS-B")
        self._gp.set_parameter_vector(
            result.x if np.isfinite(result.fun) and result.fun < 1e25 else p0
        )
        self.fitted_params_ = dict(
            zip(self._gp.get_parameter_names(), self._gp.get_parameter_vector())
        )
        return self

    def _predict(self, X):
        Xn = self._numeric(X).reindex(columns=self.columns_, fill_value=0.0)
        Xn = Xn.fillna(self._median).fillna(0.0)
        return self._gp.predict(
            self._y_train, Xn.values.astype(float), return_var=True
        )

    def predict(self, X):
        mu, _ = self._predict(X)
        return np.asarray(mu).ravel()

    def predict_std(self, X):
        """Posterior predictive std for new observations: latent variance
        plus the fitted white-noise variance (george's return_var excludes
        observation noise at the test points)."""
        mu, var = self._predict(X)
        noise = np.exp(
            self.fitted_params_.get("white_noise:value", -np.inf)
        )
        return np.asarray(mu).ravel(), np.sqrt(np.maximum(var + noise, 0.0))


class PyGRFRegressor:
    """sklearn-style wrapper around PyGRF (geoai-lab/PyGRF, Sun et al. 2024,
    Transactions in GIS) — Geographical Random Forest: one global sklearn RF
    plus one local RF per training sample (fit on its band_width nearest
    neighbors, bisquare-distance-weighted), blended at predict time as
    ``local_weight * local + (1 - local_weight) * global``.

    Coordinates come from the ``lat``/``lon`` columns of X (present when
    [ML] include_lat_lon_as_feature = True force-includes them in
    selected_features); they are POPPED out of the feature matrix — in GRF
    they define the spatial kernel, not covariates. Because PyGRF computes
    Euclidean distances and "recommends projected coordinates", lon/lat
    degrees are locally projected (equirectangular, cos(mean lat) scaling)
    to km before use — adequate at country scale for k-NN bandwidths.

    PyGRF API quirks this wrapper absorbs (verbatim from PyGRF.py 0.0.12):
    * fit() REQUIRES a DataFrame X / Series y (uses .iloc + .columns) and a
      positional (n, 2) coords array — rows are index-reset so pairing stays
      positional after geocif's region masking.
    * predict() returns a 3-TUPLE (combined, global, local) and REQUIRES
      coords_test + local_weight — we return np.asarray(combined).
    * all features must be numeric — object/category cols are one-hot
      encoded and NaN median-imputed (mirrors BassRegressor._numeric).

    Defaults: band_width=None → adaptive heuristic (15% of n, floor 20,
    capped at n-1); local_weight=None → theory-informed global Moran's I of
    y on band_width-NN weights (the paper's recommendation), fallback 0.25.
    Both overridable via [ML] pygrf_band_width / pygrf_local_weight.

    COST: PyGRF fits ONE local RF PER TRAINING ROW — a pooled ~1700-row
    fold trains 1700 local forests (several minutes). Fine for per-region
    ('individual') clustering; budget accordingly for pooled strategies.
    """

    def __init__(self, band_width=None, local_weight=None, n_estimators=100,
                 max_features=1.0, kernel="adaptive", train_weighted=True,
                 predict_weighted=True, resampled=True, n_jobs=None, seed=0):
        self.band_width = band_width
        self.local_weight = local_weight
        self.n_estimators = n_estimators
        self.max_features = max_features
        self.kernel = kernel
        self.train_weighted = train_weighted
        self.predict_weighted = predict_weighted
        self.resampled = resampled
        self.n_jobs = n_jobs
        self.seed = seed

    def get_params(self, deep=True):
        return dict(
            band_width=self.band_width, local_weight=self.local_weight,
            n_estimators=self.n_estimators, max_features=self.max_features,
            kernel=self.kernel, train_weighted=self.train_weighted,
            predict_weighted=self.predict_weighted, resampled=self.resampled,
            n_jobs=self.n_jobs, seed=self.seed,
        )

    def set_params(self, **p):
        for k, v in p.items():
            setattr(self, k, v)
        return self

    @staticmethod
    def _require_coords(X, model_label="pygrf"):
        missing = [c for c in ("lat", "lon") if c not in X.columns]
        if missing:
            raise ValueError(
                f"model = '{model_label}' needs 'lat'/'lon' columns in X "
                f"(missing: {missing}). Set [ML] include_lat_lon_as_feature "
                "= True so geocif force-includes region centroids in the "
                "feature set."
            )

    def _project(self, lonlat):
        """Equirectangular lon/lat → km, scaled at the training-mean
        latitude (``self._lat0``, set in _split(fit=True)). Euclidean
        distance on the result approximates great-circle distance at
        country scale, which is all the (rank-based) adaptive k-NN kernel
        needs."""
        xy = np.asarray(lonlat, dtype=float)
        x_km = xy[:, 0] * 111.320 * np.cos(np.radians(self._lat0))
        y_km = xy[:, 1] * 110.574
        return np.column_stack([x_km, y_km])

    def _split(self, X, fit):
        """X → (numeric feature DataFrame, projected (n,2) coords)."""
        X = pd.DataFrame(X).reset_index(drop=True)
        if fit:
            self._require_coords(X)
        lonlat = X[["lon", "lat"]].astype(float).to_numpy()
        feats = X.drop(columns=["lat", "lon"], errors="ignore")
        obj = list(feats.select_dtypes(include=["object", "category"]).columns)
        if obj:
            feats = pd.get_dummies(feats, columns=obj, dummy_na=False)
        feats = feats.apply(pd.to_numeric, errors="coerce")
        if fit:
            self._median = feats.median(numeric_only=True)
            self._coord_mean = np.nanmean(lonlat, axis=0)
            if not np.all(np.isfinite(self._coord_mean)):
                self._coord_mean = np.zeros(2)
        else:
            feats = feats.reindex(columns=self.columns_, fill_value=0.0)
        feats = feats.fillna(self._median).fillna(0.0)
        # coords must be NaN-free for cdist: regions missing from the
        # boundary-file centroid merge fall back to the train-mean location
        # (their local blend degrades gracefully toward the global model).
        nan_rows = np.isnan(lonlat).any(axis=1)
        if nan_rows.any():
            lonlat[nan_rows] = self._coord_mean
        if fit:
            self._lat0 = float(np.mean(lonlat[:, 1]))
        coords = self._project(lonlat)
        # PyGRF's adaptive kernel divides by the band_width-th NN distance
        # (PyGRF.py:129-131 fit, 250-252 predict). geocif's lat/lon are
        # per-region centroids repeated for every training year, so that
        # distance is exactly 0 whenever a region contributes >= band_width
        # rows (ALWAYS under 'individual' clustering) -> 0/0 NaN sample
        # weights -> sklearn ValueError. Break exact ties with a
        # deterministic ~1 mm jitter (coords are in km); separate fit /
        # predict streams so a test row never lands exactly on a train row.
        rng = np.random.default_rng(self.seed if fit else self.seed + 1)
        return feats, coords + rng.normal(0.0, 1e-6, coords.shape)

    def _moran_local_weight(self, y, coords, k):
        """Theory-informed local_weight = global Moran's I of the response
        (Sun et al. 2024). Falls back to a conservative 0.25 if the weights
        build fails (e.g. degenerate/duplicate coordinate sets)."""
        try:
            from libpysal.weights import KNN
            from esda.moran import Moran

            w = KNN.from_array(coords, k=max(1, min(k, len(y) - 1)))
            mi = Moran(np.asarray(y, dtype=float), w, permutations=0)
            if np.isfinite(mi.I):
                return float(np.clip(mi.I, 0.0, 1.0))
        except Exception:
            pass
        return 0.25

    def fit(self, X, y):
        try:
            from PyGRF import PyGRFBuilder
        except ImportError as exc:
            raise ImportError(
                "model = 'pygrf' requires the PyGRF package (pure-Python, "
                "on PyPI):\n    pip install PyGRF"
            ) from exc

        feats, coords = self._split(X, fit=True)
        self.columns_ = list(feats.columns)
        y_series = pd.Series(np.asarray(y, dtype=float).ravel()).reset_index(
            drop=True
        )
        n = len(y_series)

        bw = self.band_width
        if str(self.kernel).lower() == "fixed":
            # fixed kernel: band_width is a search RADIUS in km (coords are
            # projected to km in _split), NOT a neighbor count — the
            # count clamp / 15%-of-n heuristic has no distance meaning.
            if bw is None:
                raise ValueError(
                    "pygrf kernel='fixed' needs an explicit [ML] "
                    "pygrf_band_width (search radius in km); the adaptive "
                    "count heuristic does not apply."
                )
            bw = float(bw)
            if not np.isfinite(bw) or bw <= 0:
                raise ValueError(
                    f"pygrf_band_width must be a positive radius in km for "
                    f"kernel='fixed', got {bw!r}"
                )
            # Moran's I still needs a NEIGHBOR COUNT — use the heuristic.
            moran_k = max(
                int(np.clip(round(0.15 * n), 1, max(1, n - 1))),
                min(20, max(1, n - 1)),
            )
        else:
            if bw is None:
                bw = int(round(0.15 * n))
                # floor of 2, not 1: band_width=1 makes PyGRF's train-side
                # bandwidth the row's own self-distance (distance-matrix
                # diagonal) = exactly 0, which no jitter can fix.
                bw = int(np.clip(bw, 2, max(2, n - 1)))
                bw = max(bw, min(20, max(2, n - 1)))
            else:
                bw = int(np.clip(int(bw), 2, max(2, n - 1)))
            moran_k = bw
        self.band_width_ = bw

        lw = self.local_weight
        if lw is None:
            lw = self._moran_local_weight(y_series, coords, moran_k)
        self.local_weight_ = float(np.clip(lw, 0.0, 1.0))

        self._model = PyGRFBuilder(
            band_width=bw,
            n_estimators=self.n_estimators,
            max_features=self.max_features,
            kernel=self.kernel,
            train_weighted=self.train_weighted,
            predict_weighted=self.predict_weighted,
            resampled=self.resampled,
            n_jobs=self.n_jobs,
            bootstrap=True,
            random_state=self.seed,
        )
        self._model.fit(feats, y_series, coords)
        return self

    def predict(self, X):
        feats, coords = self._split(X, fit=False)
        combined, global_, _local = self._model.predict(
            feats, coords, self.local_weight_
        )
        out = np.asarray(combined, dtype=float).ravel()
        # kernel='fixed' with a test point that has no training point inside
        # the radius yields 0/0 = NaN from PyGRF's weighted local average —
        # fall back to the global RF prediction for those rows.
        g = np.asarray(global_, dtype=float).ravel()
        nan_out = np.isnan(out)
        if nan_out.any():
            out[nan_out] = g[nan_out]
        return out


class TabPFNGSARegressor:
    """sklearn-style wrapper around TabPFN-GSA (ruid7181/TabPFN-GSA; Deng,
    Li & Wang 2026, IJGIS — GSA = Geospatial Sparse Attention). A spatial
    context-sampler around the stock TabPFNRegressor: predict-time it grids
    the study area into K cells and, per cell with test points, fits TabPFN
    in-context on the 3x3-neighborhood training rows plus a fraction ``s``
    of distant rows, ensembled over 3 samplings; a global-fallback TabPFN
    (fit on all rows at fit() time) covers empty neighborhoods.

    Spatial columns are geocif's ``lat``/``lon`` feature columns (requires
    [ML] include_lat_lon_as_feature = True). GSAModel hardcodes
    include_spatial_features=True — coords double as model features — so
    x_cols is everything EXCEPT lat/lon (overlap raises ValueError
    upstream). X stays a DataFrame end-to-end (GSA requires it; slices are
    handed straight to tabpfn, which infers category-dtype columns like
    Region on its own). K must be a perfect square — non-square configs are
    rounded to the nearest one rather than crashing mid-run.

    ignore_pretraining_limits=True mirrors geocif's plain-tabpfn branch:
    the global fallback fits on the FULL fold (>1000 rows on CPU aborts
    without it). Degenerate case: an 'individual'-cluster fold where every
    row shares one centroid collapses the grid to a single cell — GSA then
    behaves as plain tabpfn (x3 ensembles), no crash.

    tabpfn-gsa is git-only research code (v0.1.0, not on PyPI):
        pip install git+https://github.com/ruid7181/TabPFN-GSA.git
    """

    def __init__(self, K=64, s=0.1, device="auto", seed=0):
        self.K = K
        self.s = s
        self.device = device
        self.seed = seed

    def get_params(self, deep=True):
        return dict(K=self.K, s=self.s, device=self.device, seed=self.seed)

    def set_params(self, **p):
        for k, v in p.items():
            setattr(self, k, v)
        return self

    @staticmethod
    def _fill_nan_coords(X, coord_mean):
        """Coords must be NaN-free: ONE NaN lat/lon makes tabpfn_gsa's grid
        mins/spans NaN, silently collapsing EVERY row's cell index to 0 on
        that axis (grid.py floors NaN -> int-cast warning -> clip 0), i.e.
        the geospatial attention degenerates with no error. Regions missing
        from the boundary-file centroid merge fall back to the train-mean
        location, same as PyGRFRegressor."""
        nan_mask = X[["lat", "lon"]].isna()
        if nan_mask.to_numpy().any():
            X = X.copy()
            X["lat"] = X["lat"].fillna(coord_mean[0])
            X["lon"] = X["lon"].fillna(coord_mean[1])
        return X

    def fit(self, X, y):
        try:
            from tabpfn_gsa import GSAModel
        except ImportError as exc:
            raise ImportError(
                "model = 'tabpfn_gsa' requires tabpfn-gsa, a git-only "
                "optional dependency (not on PyPI):\n"
                "    pip install git+https://github.com/ruid7181/TabPFN-GSA.git"
            ) from exc

        X = pd.DataFrame(X)
        PyGRFRegressor._require_coords(X, model_label="tabpfn_gsa")
        # Fill at FIT time, not just predict: GSAModel stores X internally
        # and reuses those coords when building the predict-time grid.
        self._coord_mean = np.nanmean(
            X[["lat", "lon"]].to_numpy(dtype=float), axis=0
        )
        if not np.all(np.isfinite(self._coord_mean)):
            self._coord_mean = np.zeros(2)
        X = self._fill_nan_coords(X, self._coord_mean)
        x_cols = [c for c in X.columns if c not in ("lat", "lon")]
        # Declare categoricals to the backend TabPFN, exactly like the plain
        # `tabpfn` branch does. Without this, tabpfn ordinal-encodes string
        # columns as *suspected free text* and warns they "usually add noise
        # rather than signal" -- harmless-ish for admin_1 Region (~39 states)
        # but material at admin_2, where Region is ~919 county names. Leaving
        # it unset also made the tabpfn_gsa-vs-tabpfn comparison unfair, since
        # only plain tabpfn got the declaration.
        #
        # Index space: GSAModel builds model_columns_ = [*x_cols, *spa_cols]
        # and fits on X[model_columns_], so positions are relative to x_cols
        # (lat/lon are appended last and are numeric).
        cat_idx = [
            i for i, c in enumerate(x_cols)
            if hasattr(X[c], "cat") or pd.api.types.is_string_dtype(X[c])
        ]
        side = max(2, int(round(np.sqrt(self.K))))
        self._m = GSAModel(
            spa_cols=["lat", "lon"],
            x_cols=x_cols,
            K=side * side,
            s=float(np.clip(self.s, 0.0, 1.0)),
            random_state=int(self.seed),
            device=self.device,
            model_kwargs={
                "ignore_pretraining_limits": True,
                "categorical_features_indices": cat_idx,
            },
        )
        self._m.fit(X, np.asarray(y, dtype=float).ravel())
        return self

    def predict(self, X):
        X = self._fill_nan_coords(pd.DataFrame(X), self._coord_mean)
        return np.asarray(self._m.predict(X)).ravel()


def loocv(
    model,
    df,
    loocv_var,
    feature_names,
    target_col,
    fraction_loocv=1.0,
    cat_features=[],
    trial_id=0,
    seed=0,
):
    """
    Perform Leave-One-Out Cross Validation (LOOCV)
    :param model: CatBoostRegressor, CatBoost model
    :param df: pd.DataFrame, training data
    :param loocv_var: str, variable to perform LOOCV on
    :param feature_names: list, list of feature names
    :param target_col: str, target column name
    :param fraction_loocv: float, fraction of unique values to perform LOOCV on
    :param cat_features: list, list of categorical feature names
    :return: float, average RMSE
    """
    from sklearn.metrics import root_mean_squared_error

    rmse_values = []

    X = df[feature_names + cat_features]
    y = df[target_col]

    # Perform LOOCV based on precentage of loocv_var
    # Find unique values
    unique_values = df[loocv_var].unique()
    num_to_select = int(len(unique_values) * fraction_loocv)
    # Randomly select X% of the unique values without replacement
    selected_values = np.random.default_rng(seed).choice(unique_values, size=num_to_select, replace=False)
    pbar = _pbar(selected_values, leave=False)
    for idx, var in enumerate(pbar):
        pbar.set_description(f"Trial {trial_id}, LOOCV {var}")

        train_index = df[df[loocv_var] != var].index
        val_index = df[df[loocv_var] == var].index

        X_train, X_val = X.loc[train_index], X.loc[val_index]
        y_train, y_val = y.loc[train_index], y.loc[val_index]

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_val)

        # Calculate RMSE
        rmse = root_mean_squared_error(y_val, y_pred)
        rmse_values.append(rmse)

    # Compute average MSE
    average_rmse = np.mean(rmse_values)

    return average_rmse


def optuna_objective(model, df, feature_names, target_col, cat_features=[]):
    """

    Args:
        model:
        df:
        feature_names:
        target_col:
        cat_features:

    Returns:

    """
    from sklearn.metrics import root_mean_squared_error
    from sklearn.model_selection import train_test_split

    X = df[feature_names + cat_features]
    y = df[target_col]

    # Divide the data into training and validation sets
    train_X, val_X, train_y, val_y = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    model.fit(
        train_X,
        train_y,
        cat_features=cat_features,
        eval_set=(val_X, val_y),
        early_stopping_rounds=100,
        use_best_model=True,
        verbose=False,
    )

    # Make predictions
    val_preds = model.predict(val_X)

    # Evaluate predictions
    rmse = root_mean_squared_error(val_y, val_preds)

    return rmse


def optimized_model(
    model_name,
    df,
    use_loocv,
    loocv_var,
    feature_names,
    target_col,
    fraction_loocv,
    cat_features=[],
    seed=0,
):
    """
    Train CatBoost model using Optuna hyperparameter optimization
    :param model_name: str, 'CatBoost' or 'XGBoost'
    :param df: pd.DataFrame, training data
    :param loocv_var: str, 'Harvest Year'
    :param feature_names: list, list of feature names
    :param target_col: str, target column name
    :param fraction_loocv: float, fraction of unique values to perform LOOCV on
    :param cat_features: list, list of categorical feature names
    :param seed: int, random seed
    """
    # Define objecive function for optuna Hyperparameter tuning
    def _optuna_objective(trial):
        try:
            if model_name == "catboost":
                params = {
                    "depth": trial.suggest_int("depth", 2, 5),
                    "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1),
                    "iterations": trial.suggest_int(
                        "iterations", low=1000, high=5000, step=500
                    ),
                    "subsample": trial.suggest_float("subsample", 0.5, 1.0),
                    "bootstrap_type": "Bernoulli",
                    "random_strength": trial.suggest_float("random_strength", 0.3, 1.0),
                    "reg_lambda": trial.suggest_float("reg_lambda", 1.0, 30.0, log=True),
                    "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 3, 10),
                    "loss_function": "RMSE",
                    "early_stopping_rounds": 50,
                    "random_seed": seed,
                    "verbose": False,
                }

                # Fit the optuna model. CatBoost has its own thread pool and
                # ignores OMP_NUM_THREADS, so the per-worker budget has to be
                # passed explicitly (-1 = all cores, its own default).
                cb_params = dict(params)
                cb_params.setdefault("thread_count", ml_threads.thread_count(-1))
                optuna_model = CatBoostRegressor(**cb_params, cat_features=cat_features)
            else:
                raise NotImplementedError

            if use_loocv:
                trial_id = trial.number
                error_metric = loocv(
                    optuna_model,
                    df,
                    loocv_var,
                    feature_names,
                    target_col,
                    fraction_loocv,
                    cat_features,
                    trial_id,
                    seed,
                )
            else:
                error_metric = optuna_objective(
                    optuna_model, df, feature_names, target_col, cat_features
                )

            return error_metric
        except Exception as e:
            print(f"Trial failed with exception: {e}")
            return np.inf  # Assign a high cost to failed trials

    try:
        # Optimize hyperparameters
        n_trials = min(20, int(mp.cpu_count() * 0.9))
        optuna.logging.set_verbosity(optuna.logging.WARNING)  # Disable verbose
        sampler = optuna.samplers.TPESampler(seed=seed)
        study = optuna.create_study(sampler=sampler, direction="minimize")
        study.optimize(
            _optuna_objective, n_trials=n_trials, n_jobs=1
        )
        if study.best_trial is None:
            raise ValueError("Optimization failed to complete any trials.")
        hyperparams = study.best_trial.params

    except Exception as e:
        print(f"Optimization failed: {e}")
        hyperparams = {
            "depth": 4,
            "learning_rate": 0.01,
            "iterations": 10,
            "subsample": 1.0,
            "bootstrap_type": "Bernoulli",
            "random_strength": 0.5,
            "reg_lambda": 5.0,
            "min_data_in_leaf": 5,
            "loss_function": "RMSE",
            "early_stopping_rounds": 50,
            "random_seed": seed,
            "verbose": False,
        }

    # Model Initialization & Training
    if model_name == "catboost":
        # Copy so the per-worker thread budget (an environment detail) never
        # leaks into the hyperparameters recorded in the results DB.
        cb_params = dict(hyperparams)
        cb_params.setdefault("thread_count", ml_threads.thread_count(-1))
        model = CatBoostRegressor(**cb_params, cat_features=cat_features)
    else:
        raise NotImplementedError

    return hyperparams, model


def strip_variant_prefix(model_name: str) -> str:
    """Map a wrapper section name to the algorithm it dispatches to.

    ``curated_<algo>``, ``top<N>_<algo>``, ``auto_<algo>`` and
    ``last<N>m_<algo>`` are config-driven wrappers around the same underlying
    algorithm; the section name carries the knobs (use_cids, top_n,
    last_n_months, ...) which Geocif applies BEFORE training. Stripping the
    prefix here lets every ``model_name == "catboost"`` branch work unchanged,
    while the original section name lives on the caller side and is what shows
    up in DB rows and plot filenames, keeping variants distinguishable.

        curated_tabpfn  -> tabpfn
        top10_tabpfn    -> tabpfn
        auto_tabpfn     -> tabpfn
        last2m_catboost -> catboost

    Single source of truth on purpose: this logic was duplicated in
    ``auto_train`` and the CI wrapper, and adding ``last<N>m_`` to only one of
    them raised "Unknown model name: last2m_catboost" at fit time.
    """
    import re as _re

    if model_name.startswith(("curated_", "auto_")):
        return model_name.split("_", 1)[1]
    for pattern in (r"^top\d+_(.+)$", r"^last\d+m_(.+)$"):
        m = _re.match(pattern, model_name)
        if m:
            return m.group(1)
    return model_name


def auto_train(
    cluster_strategy: str,
    model_name: str,
    model_type: str,
    use_loocv: bool,
    loocv_var: str,
    df_train: pd.DataFrame,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    feature_names: list,
    target_col: str,
    optimize: bool = False,
    fraction_loocv: float = 1.0,
    cat_features: list = None,
    monotonic_features: list = None,
    seed: int = 0,
    cubist_params: dict = None,
    bass_params: dict = None,
    george_params: dict = None,
    pygrf_params: dict = None,
    gsa_params: dict = None,
    bnn_params: dict = None,
):
    """
    Train a model using specified parameters and optionally perform hyperparameter optimization.

    :param cluster_strategy: Clustering strategy ('individual', 'auto_detect', 'single')
    :param model_name: Name of the model ('catboost', 'xgboost', 'merf', 'oblique', 'ydf', 'linear', 'gam', etc.)
    :param model_type: Type of model ('REGRESSION' or 'CLASSIFICATION')
    :param use_loocv: Whether to use leave-one-out cross-validation
    :param loocv_var: Variable for LOOCV
    :param df_train: Training dataset
    :param X_train: Training features
    :param y_train: Training target
    :param feature_names: List of feature names
    :param target_col: Name of the target column
    :param optimize: Whether to optimize hyperparameters
    :param fraction_loocv: Fraction of unique values for LOOCV
    :param cat_features: List of categorical features (optional)
    :param monotonic_features: List of monotonic features (optional)
    :param seed: Random seed for reproducibility
    :return: Hyperparameters and trained model
    """
    # `curated_<algo>`, `top<N>_<algo>` and `auto_<algo>` are all
    # config-driven CID-selection wrappers that dispatch to the same
    # underlying algo. The section name carries the selection knobs
    # (use_cids, top_n, auto_min_count, etc.) — Geocif applies those
    # before training. Here we strip the wrapper prefix so every
    # existing `elif model_name == "tabpfn"` / "catboost" / ... branch
    # below works unchanged. Examples:
    #   curated_tabpfn → tabpfn
    #   top10_tabpfn   → tabpfn
    #   auto_tabpfn    → tabpfn
    # The original section name still lives on the caller side and is
    # what shows up in DB rows / plot filenames, keeping variants
    # distinguishable.
    model_name = strip_variant_prefix(model_name)

    if optimize:
        hyperparams, model = optimized_model(
            model_name, df_train, use_loocv, loocv_var,
            feature_names, target_col, fraction_loocv,
            cat_features, seed
        )
    else:
        hyperparams = {}

        if model_name in ["catboost", "merf", "catboost_quantile"]:
            from catboost import CatBoostRegressor, CatBoostClassifier

            # catboost_quantile trains catboost against the 0.25-quantile
            # loss instead of RMSE. Same hyperparams; useful for insurance-
            # trigger scenarios where distinguishing the LOW tail matters
            # more than mean accuracy (RMSE loss mean-reverts and rarely
            # predicts below-threshold yields on small data).
            if model_name == "catboost_quantile":
                loss_function = "Quantile:alpha=0.25"
            else:
                loss_function = "RMSE" if model_type == "REGRESSION" else "MultiClass"
            # Small-n / high-feature-count tuning (Kenya-maize regime,
            # ~300 rows × ~500 features per fold):
            #   subsample=0.7   → activate Bernoulli bagging (was 1.0 → inert)
            #   border_count=64 → coarser feature quantization (default 254
            #                     over-fits noise at small n)
            #   reg_lambda=12   → stronger L2 (was 5.0)
            hyperparams = {
                "iterations": 2500,
                "learning_rate": 0.01,
                "depth": 4,
                "subsample": 0.7,
                "bootstrap_type": "Bernoulli",
                "random_strength": 0.5,
                "reg_lambda": 12.0,
                "border_count": 64,
                "min_data_in_leaf": 5,
                "loss_function": loss_function,
                "early_stopping_rounds": 50,
                "random_seed": seed,
                "verbose": False,
            }

            # The optimize=False path is the one production actually takes
            # (usa_admin2 sets optimize = False), so the per-worker thread
            # budget has to be applied HERE too — the two sites in
            # optimized_model() only run when optimize=True.
            hyperparams.setdefault("thread_count", ml_threads.thread_count(-1))

            if model_name in ("catboost", "catboost_quantile"):
                model_cls = CatBoostRegressor if model_type == "REGRESSION" else CatBoostClassifier
                model = model_cls(**hyperparams, cat_features=cat_features)

            elif model_name == "merf":
                from merf import MERF
                hyperparams["iterations"] = 1000
                regr_cls = CatBoostRegressor if model_type == "REGRESSION" else CatBoostClassifier
                regr = regr_cls(**hyperparams, cat_features=cat_features)
                model = MERF(regr, max_iterations=10)

        elif model_name == "oblique":
            raise ValueError(
                "model = 'oblique' relies on `treeple`, which was removed from geocif "
                "(compiled backend with no aarch64/ARM wheels). Pick another model in "
                "[DEFAULT] models = [...] (e.g. catboost, tabpfn, cubist)."
            )
        elif model_name == "tabpfn":
            from tabpfn import TabPFNRegressor

            # Identify the column indices for cat_features in X_train
            if cat_features is None:
                cat_feature_indices = []
            else:
                cat_feature_indices = [X_train.columns.get_loc(col) for col in cat_features if
                    col in X_train.columns]

            # Tuning notes — see IDEAS.md at project root:
            #   * n_estimators=8: tabpfn default. A/B tested 8/16/32 on
            #     Kenya maize (0.4.787 → 0.4.790 → 0.4.791); all three
            #     produced RMSE within 0.4% of each other (0.4723 / 0.4741
            #     / 0.4760) and R² within 0.004. The ensemble is saturated
            #     at ~40 training points per region-year — bumping does
            #     nothing but burn compute (1x/1.5x/3x runtime). Kept at
            #     tabpfn's own default to avoid the illusion of tuning.
            #   * ignore_pretraining_limits=True: REQUIRED at our sample
            #     size. tabpfn 8.x enforces a CPU-only guardrail that
            #     aborts with RuntimeError "Running on CPU with more than
            #     1000 samples is not allowed by default" when the training
            #     set exceeds 1000 rows. Kenya has ~1700 rows per season,
            #     so removing the flag breaks every fit. (Learned the hard
            #     way in 0.4.789 — every prediction failed silently.)
            #   * random_state=int(seed): guarantees deterministic ensemble
            #     permutations across estimators, safe against float-seed
            #     configs.
            #   * inference_config left at None: custom PREPROCESS_TRANSFORMS
            #     / FEATURE_SHIFT_METHOD tuning (Tier 2b) is a future
            #     experiment — see IDEAS.md.
            model = TabPFNRegressor(
                device="auto",
                categorical_features_indices=cat_feature_indices,
                random_state=int(seed),
                n_estimators=8,
                ignore_pretraining_limits=True,
            )
        elif model_name == "tabpfn_phe":
            # Post-Hoc Ensembling wrapper from tabpfn_extensions — runs
            # TabPFN with multiple preprocessing configurations and
            # ensembles their predictions. In published benchmarks it's
            # typically the strongest zero-shot tabular regressor
            # available, at 3-10x the runtime of base TabPFN.
            #
            # Named "tabpfn_phe" rather than "auto_tabpfn" to avoid the
            # wrapper-prefix regex at the top of this function, which
            # strips "auto_" and would route "auto_tabpfn" back to the
            # plain "tabpfn" branch.
            #
            # max_time bounds the per-fit optimization budget; 600s = 10min
            # is a reasonable operational ceiling. Cat feature indices
            # aren't currently accepted by AutoTabPFNRegressor's ctor
            # (the underlying PHE machinery detects them itself), so we
            # don't pass them. See IDEAS.md for benchmarking notes.
            from tabpfn_extensions.post_hoc_ensembles.sklearn_interface import (
                AutoTabPFNRegressor,
            )
            # ignore_pretraining_limits=True passes through to the
            # constituent TabPFN estimators, suppressing the same
            # >1000-samples-CPU guardrail that would otherwise abort
            # every fit on our ~1700-row Kenya training sets.
            model = AutoTabPFNRegressor(
                max_time=600,
                random_state=int(seed),
                ignore_pretraining_limits=True,
            )
        elif model_name == "tabfm":
            # Google Research's TabFM (tabular foundation model) — zero-shot
            # inference like TabPFN, so no fit-time hyperparameters and no
            # Optuna. PyTorch CPU backend is the correct choice on this
            # cluster (JAX-on-CPU JIT-recompiles every call → ~130s/row vs
            # PyTorch's ~10s/row; a V100 16GB doesn't fit the ~11GB weights
            # + working memory, so GPU is deferred).
            #
            # Load is heavy (~26s cold; ~0s if HF cache is warm — cluster
            # HF_HOME lives on /gpfs so the ~13GB weights persist between
            # runs). Loading per-call mirrors the tabpfn branch above; if
            # this becomes a bottleneck on production runs, cache the
            # pretrained handle at module level.
            from tabfm import TabFMRegressor
            from tabfm import tabfm_v1_0_0_pytorch as tabfm_v1_0_1

            class _TabFMWithObjectDtype:
                """sklearn-shaped wrapper that casts pandas category
                columns back to object before fit/predict.

                Why: TabFM's tokenizer misreads CategoricalDtype as
                numeric codes — verified 10x worse RMSE on a synthetic
                fixture (1.410 vs 0.149) with the same underlying data.
                geocif casts cat_features to category at geocif.py:1270
                because catboost/tabpfn/etc. need it; we can't unwind
                that upstream cast without breaking the other models.
                So this adapter locally undoes it for TabFM only."""
                def __init__(self, pretrained):
                    self._reg = TabFMRegressor(model=pretrained)

                @staticmethod
                def _cast(X):
                    X = X.copy()
                    for c in X.columns:
                        if hasattr(X[c], "cat"):
                            X[c] = X[c].astype(object)
                    return X

                def fit(self, X, y):
                    return self._reg.fit(self._cast(X), y)

                def predict(self, X):
                    return self._reg.predict(self._cast(X))

            _pretrained = tabfm_v1_0_1.load(model_type="regression")
            model = _TabFMWithObjectDtype(_pretrained)
        elif model_name == "exaone":
            # LG AI Research EXAONE-Tabular (github.com/LGAI-Research/EXAONE-
            # Tabular) — zero-shot tabular foundation model (in-context
            # learning, no gradient updates), sklearn-style .fit/.predict.
            # ``from_pretrained`` fetches the regression checkpoint from the HF
            # Hub (cached under HF_HOME on /gpfs). CPU on this cluster (upstream
            # recommends GPU; torch 2.13 cpu here).
            #
            # Unlike TabPFN/TabFM, EXAONE.fit()/predict() hard-require a 2-D
            # *numeric* NumPy array (TypeError on a DataFrame) and run their own
            # low-cardinality categorical detection on that numeric array. So we
            # integer-encode object/category columns (Region etc.) with a
            # fit-time level->code map and cast everything to float64. Unseen
            # predict-time levels and NaN categoricals map to -1 (a distinct
            # "unknown" code EXAONE still treats categorically). NaN in numeric
            # features is fine — EXAONE's TabularPreprocessor mean-fills it;
            # only targets must be NaN-free (LOOCV training rows already are).
            from exaonetabular import EXAONETabularRegressor
            import numpy as _np
            import pandas as _pd

            class _ExaoneNumeric:
                def __init__(self):
                    self._reg = EXAONETabularRegressor.from_pretrained(device="cpu")
                    self._cat_maps = {}
                    self._columns = None

                @staticmethod
                def _is_cat(s):
                    return (
                        hasattr(s, "cat")
                        or s.dtype == object
                        or str(s.dtype).startswith("string")
                    )

                def _to_numeric(self, X, fit):
                    cols = []
                    for c in X.columns:
                        s = X[c]
                        if self._is_cat(s):
                            if fit:
                                codes, uniques = _pd.factorize(s, sort=False)  # NaN -> -1
                                self._cat_maps[c] = {v: i for i, v in enumerate(uniques)}
                                col = codes.astype("float64")
                            else:
                                col = s.map(self._cat_maps.get(c, {})).to_numpy(dtype="float64")
                                col = _np.where(_np.isnan(col), -1.0, col)  # unseen/NaN -> -1
                            cols.append(col)
                        else:
                            cols.append(
                                _pd.to_numeric(s, errors="coerce").to_numpy(dtype="float64")
                            )
                    return (
                        _np.column_stack(cols)
                        if cols
                        else _np.empty((len(X), 0), dtype="float64")
                    )

                def fit(self, X, y):
                    self._columns = list(X.columns)
                    Xn = self._to_numeric(X, fit=True)
                    yn = _np.asarray(
                        _pd.to_numeric(_pd.Series(y), errors="coerce"), dtype="float64"
                    )
                    self._reg.fit(Xn, yn)
                    return self

                def predict(self, X):
                    if self._columns is not None:
                        X = X.reindex(columns=self._columns)
                    return self._reg.predict(self._to_numeric(X, fit=False))

            model = _ExaoneNumeric()
        elif model_name == "tabpfn_ft":
            from tabpfn.finetuning import FinetunedTabPFNRegressor

            if cat_features is None:
                cat_feature_indices = []
            else:
                cat_feature_indices = [X_train.columns.get_loc(col) for col in cat_features if
                    col in X_train.columns]

            # Fine-tuned variant of TabPFN. Needs X_val/y_val (handled by
            # TabPFNFTFitter in geocif.py). Defaults from PriorLabs tutorial;
            # CPU works but expect ~5-10x slower per task than zero-shot 'tabpfn'.
            model = FinetunedTabPFNRegressor(
                device="auto",
                epochs=30,
                learning_rate=1e-5,
                n_estimators_finetune=2,
                n_estimators_validation=2,
                n_estimators_final_inference=8,
                early_stopping=True,
                early_stopping_patience=8,
                use_fixed_preprocessing_seed=False,
                random_state=seed,
                extra_regressor_kwargs={
                    "categorical_features_indices": cat_feature_indices,
                    "ignore_pretraining_limits": True,
                },
            )
        elif model_name == "tabicl":
            from tabicl import TabICLRegressor

            model = TabICLRegressor(
                n_estimators=16,
                norm_methods=["none", "power", "quantile", "robust"],
                outlier_threshold=5.0,
                random_state=seed,
            )
        elif model_name == "tabicl_ft":
            from tabicl import FinetunedTabICLRegressor

            # Fine-tuned variant of TabICL. Needs X_val/y_val for early
            # stopping — wired in the TabICLFTFitter class in geocif.py.
            # GPU-friendly; falls back to CPU when no CUDA device is
            # available — expect ~5-10x slower per task on CPU. Defaults
            # come from the tabicl tutorial.
            model = FinetunedTabICLRegressor(
                epochs=60,
                learning_rate=1e-5,
                n_estimators_finetune=2,
                n_estimators_validation=2,
                n_estimators_inference=4,
                early_stopping=True,
                patience=10,
                random_state=seed,
                verbose=False,
            )
        elif model_name == "desreg":
            raise ValueError(
                "model = 'desreg' builds a DES ensemble that includes `ydf`, which "
                "was removed from geocif (Yggdrasil/Bazel backend — no aarch64 wheels, "
                "unbuildable on ARM). Pick another model in [DEFAULT] models = [...] "
                "(e.g. catboost, tabpfn, cubist)."
            )
        elif model_name == "ngboost":
            if model_type == "REGRESSION":
                from ngboost import NGBRegressor
                from ngboost.distns import Normal
                from ngboost.scores import MLE

                # Initialize and train NGBoost regressor
                model = NGBRegressor(Dist=Normal, Score=MLE, natural_gradient=True)
            elif model_type == "CLASSIFICATION":
                from ngboost import NGBClassifier
                from ngboost.distns import k_categorical
                from ngboost.scores import LogScore

                # Initialize and train NGBoost classifier
                model = NGBClassifier(Dist=k_categorical(3), Score=LogScore, natural_gradient=True)
        elif model_name == "ydf":
            raise ValueError(
                "model = 'ydf' relies on `ydf` (Yggdrasil / Bazel build), which was "
                "removed from geocif (no aarch64/ARM wheels, unbuildable on ARM). Pick "
                "another model in [DEFAULT] models = [...] (e.g. catboost, tabpfn, cubist)."
            )

        elif model_name == "linear":
            from sklearn.linear_model import LassoCV, LogisticRegressionCV
            linear_cls = LassoCV if model_type == "REGRESSION" else LogisticRegressionCV
            model = linear_cls(cv=5, random_state=42)
        elif model_name == "logistic":
            from sklearn.linear_model import LogisticRegression
            model = LogisticRegression(multi_class='multinomial', solver='lbfgs')

        elif model_name == "extratrees":
            # sklearn Extremely Randomized Trees (axis-aligned splits, random
            # thresholds) — distinct from geocif's 'oblique' (treeple oblique
            # extra-forest). sklearn can't ingest string categoricals or NaN,
            # so wrap it: one-hot the object/category cols + median-impute
            # (mirrors BassRegressor._numeric), remembering the fit-time
            # columns so predict reindexes to the same layout. Delegates any
            # other attribute (feature_importances_ etc.) to the underlying
            # estimator like _CubistUnseenSafe.
            from sklearn.ensemble import ExtraTreesRegressor, ExtraTreesClassifier
            et_cls = ExtraTreesRegressor if model_type == "REGRESSION" else ExtraTreesClassifier

            class _ExtraTreesNumeric:
                def __init__(self, **kw):
                    self._m = et_cls(**kw)

                @staticmethod
                def _numeric(X):
                    X = pd.DataFrame(X).copy()
                    obj = list(X.select_dtypes(include=["object", "category"]).columns)
                    if obj:
                        X = pd.get_dummies(X, columns=obj, dummy_na=False)
                    return X.apply(pd.to_numeric, errors="coerce")

                def fit(self, X, y):
                    Xn = self._numeric(X)
                    self._median = Xn.median(numeric_only=True)
                    Xn = Xn.fillna(self._median).fillna(0.0)
                    self.columns_ = list(Xn.columns)
                    self._m.fit(Xn.values.astype(float), y)
                    return self

                def predict(self, X):
                    Xn = self._numeric(X).reindex(columns=self.columns_, fill_value=0.0)
                    Xn = Xn.fillna(self._median).fillna(0.0)
                    return self._m.predict(Xn.values.astype(float))

                def __getattr__(self, name):
                    return getattr(self._m, name)

            model = _ExtraTreesNumeric(
                n_estimators=500,
                n_jobs=ml_threads.thread_count(-1),
                random_state=seed,
            )

        elif model_name.startswith("gam"):
            # Placeholder — real term construction and the single gridsearch
            # fit happen in GAMFitter.fit() where the final fit-time feature
            # matrix and column order are known.  Constructing with terms here
            # would lock them to a stale X_train layout, and calling .fit()
            # here would be redundant with GAMFitter.
            from pygam import LinearGAM, LogisticGAM
            gam_cls = LogisticGAM if model_type == "CLASSIFICATION" else LinearGAM
            model = gam_cls()
        elif model_name == "geospaNN":
            try:
                import torch
                import geospaNN
            except ImportError as exc:
                raise ImportError(
                    "model = 'geospaNN' requires torch + geospaNN, an "
                    "OPTIONAL geocif extra (held out because geospaNN "
                    "depends on torch-scatter, which has a broken build "
                    "system that can't find torch under PEP-517 build "
                    "isolation). Install in this order:\n"
                    "    pip install torch\n"
                    "    pip install geocif[geospann] --no-build-isolation\n"
                    "Or pick a different model in [DEFAULT] models = [...]."
                ) from exc

            X_train = X_train.drop(columns=cat_features)
            X, Y = torch.from_numpy(X_train.to_numpy()).float(), torch.from_numpy(y_train.to_numpy().reshape(-1)).float()
            coord = torch.from_numpy(df_train[['lon', 'lat']].to_numpy()).float()
            p, n, nn = X.shape[1], X.shape[0], 5

            data = geospaNN.make_graph(X, Y, coord, nn)
            mlp = torch.nn.Sequential(
                torch.nn.Linear(p, 50), torch.nn.ReLU(),
                torch.nn.Linear(50, 20), torch.nn.ReLU(),
                torch.nn.Linear(20, 10), torch.nn.ReLU(),
                torch.nn.Linear(10, 1)
            )

            data_train, data_val, data_test = geospaNN.split_data(X, Y, coord, neighbor_size=nn, test_proportion=0.1)
            theta0 = geospaNN.theta_update(torch.tensor([1, 1.5, 0.01]), mlp(data_train.x).squeeze() - data_train.y, data_train.pos, neighbor_size=5)
            model = geospaNN.nngls(p=p, neighbor_size=nn, coord_dimensions=2, mlp=mlp, theta=torch.tensor(theta0))
            model = geospaNN.nngls_train(model, lr=0.01, min_delta=0.001)
            training_log = model.train(data_train, data_val, data_test, Update_init=10, Update_step=10)
        elif model_name == "cubist":
            from cubist import Cubist

            # n_committees=10: default 5 (R Cubist legacy) under-boosts on
            # yield data where errors correlate across regions.
            # extrapolation=0.10: default 0.05 clips predictions too tightly
            # for climate-driven yield anomalies that exceed the training range.
            # unbiased=True: yield is right-skewed; default minimizes MAE and
            # underestimates the high tail.
            # These defaults suit data-rich crops; small-n crops override them
            # via [ML] cubist_* config (e.g. poppy: n_committees=1,
            # extrapolation=0.0) — see cubist_params in geocif.py.
            cub = dict(n_committees=10, auto=True, extrapolation=0.10, unbiased=True)
            cub.update(cubist_params or {})
            # `neighbors` (composite instance-based correction) requires
            # auto=False; flip it defensively so a config that sets neighbors
            # without auto=False doesn't raise mid-run.
            if cub.get("neighbors") is not None and cub.get("auto", True):
                cub["auto"] = False

            class _CubistUnseenSafe:
                """Cubist's C engine aborts the whole predict batch if a
                *string* categorical column holds a level unseen at fit —
                e.g. predict-only regions with zero training rows (Malawi's
                no-yield city districts: `bad value of 'Blantyre City' for
                attribute 'Region' -> Error limit exceeded`). catboost/tabpfn
                tolerate this; cubist does not. Record the training levels of
                each non-numeric categorical column; at predict, any row with
                an unseen level in such a column gets NaN (region ignored for
                prediction) instead of crashing the batch. Numeric columns
                (Harvest Year, numeric Region_ID) are left alone — cubist
                treats them as continuous, so the LOOCV held-out year never
                trips this."""

                def __init__(self, **kw):
                    self._m = Cubist(**kw)
                    self._levels = {}

                @staticmethod
                def _is_numeric(s):
                    return pd.to_numeric(s, errors="coerce").notna().all()

                def fit(self, X, y):
                    self._m.fit(X, y)
                    self._levels = {}
                    if hasattr(X, "columns"):
                        for c in X.columns:
                            col = X[c]
                            # is_string_dtype catches BOTH pandas<3 object and
                            # pandas>=3 str dtype (string columns are no longer
                            # `object` in pandas 3 — `dtype == object` misses
                            # them, silently disabling this guard).
                            if hasattr(col, "cat") or pd.api.types.is_string_dtype(col):
                                s = col.astype(str)
                                if not self._is_numeric(s):
                                    self._levels[c] = set(s.unique())
                    return self

                def predict(self, X):
                    if not hasattr(X, "columns") or not self._levels:
                        return self._m.predict(X)
                    keep = pd.Series(True, index=X.index)
                    for c, lv in self._levels.items():
                        if c in X.columns:
                            keep &= X[c].astype(str).isin(lv)
                    out = np.full(len(X), np.nan, dtype=float)
                    if keep.any():
                        out[keep.to_numpy()] = self._m.predict(X.loc[keep])
                    return out

                def __getattr__(self, name):
                    # delegate anything else (e.g. feature_importances_) to Cubist
                    return getattr(self._m, name)

            model = _CubistUnseenSafe(random_state=seed, **cub)
        elif model_name == "bass":
            # BASS = Bayesian MARS (pyBASS). Tuned poppy defaults (maxInt=1
            # additive, npart=15) beat cubist on MIN_ESI4WK; interactions
            # overfit small samples. Overridable per-project via [ML] bass_*.
            bass = dict(max_int=1, npart=15, max_basis=1000,
                        nmcmc=14000, nburn=9000, thin=10)
            bass.update(bass_params or {})
            model = BassRegressor(**bass)
        elif model_name == "bnn":
            # Bayesian NN (Ma et al. 2021 RSE): two-headed mean-field
            # variational torch net -- heteroscedastic sigma head + MC-sampled
            # epistemic variance, with held-out-newest-year sigma
            # recalibration inside the wrapper (see ml/bnn.py). Regression
            # only. kl_weight defaults to 0.05, NOT the paper's 1.0: at 1.0
            # the sigma head collapses to a near-constant (marginally
            # calibrated only); 0.05 learns per-region heterogeneity and the
            # recalibration fixes its scale. Overridable via [ML] bnn_*.
            if model_type != "REGRESSION":
                raise ValueError(
                    "model = 'bnn' supports REGRESSION only; choose catboost "
                    "or logistic for CLASSIFICATION."
                )
            try:
                from .bnn import BNNYieldRegressor
            except ImportError as exc:
                raise ImportError(
                    "model = 'bnn' requires torch (normally present "
                    "transitively via the core tabpfn dep; the pixi cluster "
                    "env ships pytorch-cpu). Install with:\n"
                    "    pip install torch"
                ) from exc
            bnn = dict(
                epochs=700, batch_size=512, lr=1e-3, prior_sigma=0.1,
                kl_weight=0.05, warmup_epochs=50, n_mc=100,
                calibrate_sigma=True, device="auto",
            )
            bnn.update(bnn_params or {})
            model = BNNYieldRegressor(seed=int(seed), **bnn)
        elif model_name == "pygrf":
            # Geographical Random Forest (geoai-lab/PyGRF). Coords come from
            # the lat/lon feature columns; band_width/local_weight default to
            # the adaptive heuristic / Moran's I inside the wrapper.
            # Overridable via [ML] pygrf_* config keys. Local RFs are tiny,
            # so give the (parallel-capable) sklearn forests the per-worker
            # thread budget like catboost/extratrees.
            grf = dict(n_jobs=ml_threads.thread_count(-1))
            grf.update(pygrf_params or {})
            model = PyGRFRegressor(seed=int(seed), **grf)
        elif model_name == "tabpfn_gsa":
            # TabPFN-GSA (ruid7181) — Geospatial Sparse Attention context
            # sampler around the stock TabPFNRegressor. K (grid cells,
            # perfect square) and s (distant-sampling rate) via [ML]
            # tabpfn_gsa_* config keys.
            gsa = dict(K=64, s=0.1, device="auto")
            gsa.update(gsa_params or {})
            model = TabPFNGSARegressor(seed=int(seed), **gsa)
        elif model_name == "george":
            # george (dfm/george) — C++ exact-GP regression, routed through
            # the same scaled path as 'gpr' (GPRFitter / StandardScaler).
            # Kernel + jitter overridable via [ML] george_* config keys.
            geo = dict(kernel="expsquared", jitter=1e-3)
            geo.update(george_params or {})
            model = GeorgeGPRegressor(**geo)
        elif model_name == "gpr":
            from sklearn.gaussian_process import GaussianProcessRegressor
            from sklearn.gaussian_process.kernels import (
                RBF, WhiteKernel, ConstantKernel as C,
            )

            kernel = (
                C(1.0, (1e-3, 1e3))
                * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e2))
                + WhiteKernel(noise_level=1.0, noise_level_bounds=(1e-5, 1e1))
            )
            model = GaussianProcessRegressor(
                kernel=kernel,
                n_restarts_optimizer=5,
                normalize_y=True,
                random_state=seed,
            )
        elif model_name == "xgboost":
            raise NotImplementedError("XGBoost model not implemented yet")
        else:
            raise ValueError(f"Unknown model name: {model_name}")

    return hyperparams, model


def estimate_ci(model_type, model_name, model, alpha=0.05, ci_method="crepes"):
    """
    Wrap a fitted model for conformal prediction.

    Args:
        model_type: 'REGRESSION' or 'CLASSIFICATION'
        model_name: Model name (e.g. 'catboost', 'xgboost')
        model: The fitted model
        alpha: Significance level for confidence intervals
        ci_method: 'crepes' (default) or 'mapie'

    Returns:
        Wrapped model for confidence interval estimation
    """
    # Mirror auto_train's wrapper-prefix strip so estimate_ci treats
    # curated_/top<N>_/auto_ variants like their underlying algo.
    model_name = strip_variant_prefix(model_name)

    # bnn produces its own calibrated predictive sigma (ml/bnn.py) -- wrapping
    # it in crepes/mapie would replace heteroscedastic intervals with
    # marginal conformal ones. Its CI path is Geocif._predict_bnn_with_ci.
    if model_name in ["ngboost", "tabpfn", "tabpfn_ft", "tabicl", "tabicl_ft", "bnn"]:
        return model
    elif model_type == "CLASSIFICATION" and model_name == "catboost":
        return model
    elif model_type == "REGRESSION":
        if ci_method == "crepes":
            from crepes import WrapRegressor
            model = WrapRegressor(model)
        else:
            from mapie.regression import SplitConformalRegressor
            model = SplitConformalRegressor(estimator=model, confidence_level=1 - alpha, prefit=True)
    elif model_type == "CLASSIFICATION":
        from mapie.classification import SplitConformalClassifier
        model = SplitConformalClassifier(estimator=model, confidence_level=1 - alpha, prefit=True)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    return model

