from contextlib import contextmanager

from giving import give, given


def add_parser_arguments(parser):
    parser.add_argument("--wandb", default="", help="username:project for wandb")
    parser.add_argument(
        "--mlflow",
        action="store_true",
        default=False,
        help="whether to use mlflow to store logs",
    )
    parser.add_argument(
        "--rich",
        action="store_true",
        default=False,
        help="whether to show a rich display",
    )
    parser.add_argument(
        "--display-all",
        action="store_true",
        default=False,
        help="whether to display all given data",
    )


def log_wandb(gv, args):
    """Log data into Weights and Biases."""

    import wandb

    # Initialize the project
    entity, project = args.wandb.split(":")
    wandb.init(project=project, entity=entity, config=vars(args))

    # Watch the model's weights. We only do it the first time we see the model.
    gv["?model"].first() >> wandb.watch

    # Log train_loss, test_loss and correct (see the plots in the wandb dash)
    gv.keep("train_loss", "test_loss", "correct") >> wandb.log


@contextmanager
def proceed(args):
    with given() as gv:
        if args.display_all:
            log_all(gv)
        elif args.rich:
            log_rich(gv)
        else:
            log_terminal(gv)

        if args.wandb:
            log_wandb(gv, args)

        if args.mlflow:
            log_mlflow(gv, args)

        give(args=vars(args))

        with give.wrap("run"):
            yield gv
