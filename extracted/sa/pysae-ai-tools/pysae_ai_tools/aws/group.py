"""``aws`` command group — AWS tooling."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="aws",
    help="AWS tooling",
    no_args_is_help=True,
    lazy_subcommands={
        "spot-advisor": "pysae_ai_tools.aws.spot_advisor:main",
        "spot-evictions": "pysae_ai_tools.aws.spot_evictions:main",
        "spot-prices": "pysae_ai_tools.aws.spot_prices:main",
        "eks-optimize": "pysae_ai_tools.aws.eks_optimize.cli:main",
    },
)
