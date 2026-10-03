#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
Featrix Sphere API Client

Transform any CSV into a production-ready ML model in minutes, not months.

The Featrix Sphere API automatically builds neural embedding spaces from your data
and trains high-accuracy predictors without requiring any ML expertise.
Just upload your data, specify what you want to predict, and get a production API endpoint.

Usage:
------

    >>> from featrixsphere.api import FeatrixSphere
    >>>
    >>> featrix = FeatrixSphere("http://your-server.com")
    >>>
    >>> # Create foundational model
    >>> fm = featrix.create_foundational_model(
    ...     name="my_model",
    ...     data_file="data.csv"
    ... )
    >>> fm.wait_for_training()
    >>>
    >>> # Create predictor
    >>> predictor = fm.create_binary_classifier(
    ...     target_column="target",
    ...     name="my_predictor"
    ... )
    >>> predictor.wait_for_training()
    >>>
    >>> # Make predictions
    >>> result = predictor.predict({"feature": "value"})
    >>> print(result.predicted_class)
    >>> print(result.confidence)

For more examples, see the documentation at https://docs.featrix.com
"""

__version__ = "2.0.13148"
__author__ = "Featrix"
__email__ = "support@featrix.com"
__license__ = "MIT"

# New OO API - recommended
from .api import FeatrixSphere, FoundationalModel, Predictor, PredictionResult
from .api.exceptions import FeatrixAuthenticationError, FeatrixPredictionError, TrainingStatusUnavailableError, SessionNotFoundError
from .api.label_utils import find_similar_labels, collapse_similar_labels
from .api.null_distribution import compute_null_distribution
from .api.target_type_detection import suggest_model_type

__all__ = [
    "FeatrixAuthenticationError",
    "FeatrixPredictionError",
    "TrainingStatusUnavailableError",
    "SessionNotFoundError",
    "FeatrixSphere",
    "FoundationalModel",
    "Predictor",
    "PredictionResult",
    "find_similar_labels",
    "collapse_similar_labels",
    "compute_null_distribution",
    "suggest_model_type",
    "__version__",
]


# Deprecation shim for old API - prints once and exits
_deprecated_warning_shown = False

def _show_deprecation_and_exit(name):
    """Show deprecation warning once and exit."""
    import sys
    global _deprecated_warning_shown
    if _deprecated_warning_shown:
        sys.exit(1)
    _deprecated_warning_shown = True

    from pathlib import Path
    guide_path = Path(__file__).parent / "MIGRATION.md"
    guide_url = f"file://{guide_path.resolve()}" if guide_path.exists() else "(see featrixsphere docs)"

    print("\n" + "=" * 70, file=sys.stderr)
    print(f"ERROR: '{name}' has been removed.", file=sys.stderr)
    print(file=sys.stderr)
    print("Please upgrade to the new OO API:", file=sys.stderr)
    print(file=sys.stderr)
    print("  OLD:  from featrixsphere import FeatrixSphereClient", file=sys.stderr)
    print("        client = FeatrixSphereClient(url)", file=sys.stderr)
    print("        session = client.upload_df_and_create_session(df=df)", file=sys.stderr)
    print(file=sys.stderr)
    print("  NEW:  from featrixsphere.api import FeatrixSphere", file=sys.stderr)
    print("        featrix = FeatrixSphere(url)", file=sys.stderr)
    print("        fm = featrix.create_foundational_model(df=df)", file=sys.stderr)
    print("        fm.wait_for_training()", file=sys.stderr)
    print(file=sys.stderr)
    print(f"Full migration guide: {guide_url}", file=sys.stderr)
    print("=" * 70 + "\n", file=sys.stderr)
    sys.exit(1)

def __getattr__(name):
    """Provide helpful error for deprecated imports."""
    if name in ("FeatrixSphereClient", "SessionInfo", "PredictionBatch", "PredictionGrid"):
        _show_deprecation_and_exit(name)
    raise AttributeError(f"module 'featrixsphere' has no attribute '{name}'")
