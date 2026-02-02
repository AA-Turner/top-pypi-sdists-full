# Copied from PyTorch's example folder.

# Original: https://raw.githubusercontent.com/pytorch/examples/master/mnist/main.py
# Retrieved: 2021-09-01
# Modified to use the giving package

from __future__ import print_function

import argparse

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
from torchvision import datasets, transforms

from giving import give, given


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output


class DataStream:
    def __init__(self, args, cursor=(0, 0)):
        self.cursor = cursor

        use_cuda = not args.no_cuda and torch.cuda.is_available()

        train_kwargs = {"batch_size": args.batch_size}
        test_kwargs = {"batch_size": args.test_batch_size}
        if use_cuda:
            cuda_kwargs = {
                "num_workers": 1,
                "pin_memory": True,
                "shuffle": True,
            }
            train_kwargs.update(cuda_kwargs)
            test_kwargs.update(cuda_kwargs)

        transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
        )

        dataset_train = datasets.MNIST(
            "../data", train=True, download=True, transform=transform
        )
        self.train_loader = torch.utils.data.DataLoader(dataset_train, **train_kwargs)

        dataset_test = datasets.MNIST("../data", train=False, transform=transform)
        self.test_loader = torch.utils.data.DataLoader(dataset_test, **test_kwargs)

    def __iter__(self):
        if self.cursor is None:
            epoch, batch = 0, 0
        else:
            epoch, batch = self.cursor

        while True:
            self.cursor = (epoch, batch)
            try:
                it = iter(self.train_loader)
                if batch > 0:
                    for _ in range(batch):
                        next(it)

                while True:
                    yield next(it)
                    batch += 1

            except StopIteration:
                batch = 0
                epoch += 1

    # def state_dict(self):
    #     return {
    #         "cursor": self.cursor
    #     }


class Trainer:
    def __init__(self, args):
        use_cuda = not args.no_cuda and torch.cuda.is_available()

        torch.manual_seed(args.seed)

        self.device = torch.device("cuda" if use_cuda else "cpu")

        self.model = Net().to(self.device)
        self.optimizer = optim.Adadelta(self.model.parameters(), lr=args.lr)
        self.scheduler = StepLR(self.optimizer, step_size=1, gamma=args.gamma)
        self.start = (0, 0)

    def step(self, data, target):
        data, target = data.to(self.device), target.to(self.device)
        self.optimizer.zero_grad()
        output = self.model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        self.optimizer.step()
        give(train_loss=loss)

    def train(self, loader):
        for step, (data, target) in iter_dataset(loader, self.start):
            with give.inherit(step=step):
                self.step(data, target)

    def save(self):
        pass

    def load(self, path):
        pass


# class SkipFirst:
#     def __init__(self, total, skip):
#         self.total = total
#         self.skip = skip

#     def __iter__(self):
#         return range(self.skip, self.total)

#     def __len__(self):
#         return self.total


def iter_dataset(loader, start=None):
    if start is None:
        start = (0, 0)
    epoch, batch = start

    while True:
        try:
            it = iter(loader)
            if batch > 0:
                for _ in range(batch):
                    next(it)

            while True:
                yield (epoch, batch), next(it)
                batch += 1

        except StopIteration:
            batch = 0
            epoch += 1


def train_step(data, target, model, device, optimizer):
    data, target = data.to(device), target.to(device)
    optimizer.zero_grad()
    output = model(data)
    loss = F.nll_loss(output, target)
    loss.backward()
    optimizer.step()
    give(train_loss=loss)


# def train(args, model, device, train_loader, optimizer, epoch):
#     model.train()
#     for batch_idx, (data, target) in enumerate(train_loader):
#         data, target = data.to(device), target.to(device)
#         optimizer.zero_grad()
#         output = model(data)
#         loss = F.nll_loss(output, target)
#         loss.backward()
#         optimizer.step()
#         give(batch_idx, train_loss=loss)


# def test(model, device, test_loader):
#     model.eval()
#     test_loss = 0
#     correct = 0
#     with torch.no_grad():
#         for batch_idx, (data, target) in enumerate(test_loader):
#             data, target = data.to(device), target.to(device)
#             output = model(data)
#             test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
#             pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
#             correct += pred.eq(target.view_as(pred)).sum().item()
#             give(batch_idx)

#     test_loss /= len(test_loader.dataset)
#     correct /= len(test_loader.dataset)
#     give(test_loss, correct)


def run(args, start):
    use_cuda = not args.no_cuda and torch.cuda.is_available()

    torch.manual_seed(args.seed)

    device = torch.device("cuda" if use_cuda else "cpu")

    train_kwargs = {"batch_size": args.batch_size}
    test_kwargs = {"batch_size": args.test_batch_size}
    if use_cuda:
        cuda_kwargs = {"num_workers": 1, "pin_memory": True, "shuffle": True}
        train_kwargs.update(cuda_kwargs)
        test_kwargs.update(cuda_kwargs)

    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    )
    dataset1 = datasets.MNIST("../data", train=True, download=True, transform=transform)
    dataset2 = datasets.MNIST("../data", train=False, transform=transform)
    train_loader = torch.utils.data.DataLoader(dataset1, **train_kwargs)
    test_loader = torch.utils.data.DataLoader(dataset2, **test_kwargs)

    model = Net().to(device)
    give()
    optimizer = optim.Adadelta(model.parameters(), lr=args.lr)

    scheduler = StepLR(optimizer, step_size=1, gamma=args.gamma)

    for step, (data, target) in iter_dataset(train_loader, start):
        with give.inherit(step=step):
            train_step(model, device, optimizer, data, target)

    # for epoch in range(1, args.epochs + 1):
    #     with give.inherit(epoch=epoch):
    #         with give.wrap_inherit("train", mode="train", batch_size=train_loader.batch_size, length=len(train_loader.dataset)):
    #             train(args, model, device, train_loader, optimizer, epoch)

    #         with give.wrap_inherit("test", mode="test", batch_size=test_loader.batch_size, length=len(test_loader.dataset)):
    #             test(model, device, test_loader)

    #     scheduler.step()

    # if args.save_model:
    #     torch.save(model.state_dict(), "mnist_cnn.pt")


def log_all(gv):
    """Log everything that is given. This is useful for debugging."""
    gv.display()


def log_simple(gv):
    """Log a few select fields."""

    # List of fields we will display
    to_display = [
        "mode",
        "batch_idx",
        "train_loss",
        "test_loss",
        "correct",
    ]

    # The | operator merges two streams, here we have
    # * The stream of train_loss entries, throttled to one every 0.5 seconds
    # * The stream of test_loss entries, not throttled
    data = gv.where("train_loss").throttle(0.5) | gv.where("test_loss")

    # Only keep the keys we want to display, and then display them
    data.keep(*to_display).display()


def log_terminal(gv):
    """Custom logging on the terminal."""

    # Install wrappers around the train and test wrap_inherits
    @gv.kwrap("train")
    @gv.kwrap("test")
    def _(mode):
        # Printed before we enter the block
        print(f"Start {mode}")
        yield
        # Printed after we exit the block
        print(f"End {mode}")

    # Take entries that contain train_loss, then every 0.5 seconds, do:
    @gv.where("train_loss").throttle(0.5).ksubscribe
    def _(batch_idx, batch_size, length, epoch, train_loss):
        # Every named argument corresponds to an entry in the dictionary
        # produced by give(). batch_idx and train_loss are given together
        # at the same time, whereas batch_size, length and epoch are also
        # given because of wrap_inherit
        n = (batch_idx + 1) * batch_size
        progress = f"{n}/{length} {n / length:.0%}"
        print(f"  Train Epoch #{epoch} [{progress}] Loss: {train_loss:.6f}")

    # Now we will do the same thing for test_loss, but differently.
    # Use whichever technique fits your brain better :)

    def _progress(batch_idx, batch_size, length):
        n = (batch_idx + 1) * batch_size
        return f"{n}/{length} {n / length:.0%}"

    # * test_loss is only provided at the end of the test
    # * augment() adds a key computed from the others
    # * print() takes a format string (but no f prefix!)
    gv.where("batch_idx", mode="test").throttle(0.5).augment(progress=_progress).print(
        "  Test Epoch #{epoch} [{progress}]"
    )

    # These are given at the end of the test block
    @gv.where("test_loss", "correct").ksubscribe
    def _(test_loss, correct):
        print(f"  Test loss: {test_loss:.6f}")
        print(f"  Accuracy:  {correct:.0%}")


def log_rich(gv):
    """Create a simple terminal dashboard using rich.

    This displays a live table of the last value for everything given,
    with a progress bar for the current task under it.
    """

    from rich.console import Group
    from rich.live import Live
    from rich.pretty import Pretty
    from rich.progress import Progress
    from rich.table import Table

    # Current rows are stored here
    rows = {}

    # First, a table with the latest value of everything that was given
    table = Table.grid(padding=(0, 3, 0, 0))
    table.add_column("key", style="bold green")
    table.add_column("value")

    # Below, a progress bar for the current task (train or test)
    progress = Progress(auto_refresh=False)
    current_task = progress.add_task("----")

    # Group them
    grp = Group(table, progress)

    # This will wrap Live around the run block (the whole main function)
    gv.wrap("run", Live(grp, refresh_per_second=4))

    # This refreshes the progress bar when we change task
    @gv.kwrap("train")
    @gv.kwrap("test")
    def _(epoch, length, mode):
        # Note: the difference between wrap and kwrap is that kwrap
        # takes a function that passes the data as keyword arguments,
        # whereas wrap passes no arguments.
        descr = f"Epoch #{epoch}" if mode == "train" else "Test"
        progress.reset(current_task, total=length, description=descr)
        yield

    # This sets the progress bar's completion meter
    @gv.where("batch_idx").ksubscribe
    def _(batch_idx, batch_size):
        progress.update(current_task, completed=batch_idx * batch_size)

    # This updates the table every time we get new values
    @gv.subscribe
    def _(values):
        for k, v in values.items():
            if isinstance(v, torch.Tensor):
                # Some special processing for torch.Tensor, we will
                # only display shape and type if it's not a scalar
                if v.shape:
                    v = (v.shape, v.dtype)
                else:
                    v = v.item()
            if k in rows:
                rows[k]._object = v
            else:
                rows[k] = Pretty(v)
                table.add_row(k, rows[k])


def log_wandb(gv, args):
    """Log data into Weights and Biases."""

    # Only import if needed :)
    import wandb

    # Initialize the project
    entity, project = args.wandb.split(":")
    wandb.init(project=project, entity=entity, config=vars(args))

    # Watch the model's weights. We only do it the first time we see the model.
    gv["?model"].first() >> wandb.watch

    # Log train_loss, test_loss and correct (see the plots in the wandb dash)
    gv.keep("train_loss", "test_loss", "correct") >> wandb.log


def log_mlflow(gv, args):
    """Log data into MLFlow."""

    import mlflow

    mlflow.log_params(vars(args))

    gv.keep("train_loss", "test_loss", "correct") >> mlflow.log_metrics


def log_comet(gv, args):
    """Log data into CometML."""

    import comet_ml

    entity, project, api_key = args.comet.split(":")

    # Create an experiment with your api key
    experiment = comet_ml.Experiment(
        api_key=api_key,
        project_name=project,
        workspace=entity,
        auto_output_logging=False,
    )

    experiment.log_parameters(vars(args))

    # CometML uses context managers, which we can conveniently plug in here
    gv.wrap("train", experiment.train)
    gv.wrap("test", experiment.test)

    # Set epoch and step whenever we give them
    gv["?epoch"] >> experiment.set_epoch
    gv["?batch_idx"] >> experiment.set_step

    gv.keep("train_loss", "test_loss", "correct") >> experiment.log_metrics


def log_plot(gv):
    from random import random

    from bokeh.client import push_session
    from bokeh.layouts import column
    from bokeh.models import Button
    from bokeh.palettes import RdYlBu3
    from bokeh.plotting import curdoc, figure

    # create a plot and style its properties
    p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
    p.border_fill_color = "black"
    p.background_fill_color = "black"
    p.outline_line_color = None
    p.grid.grid_line_color = None

    # add a text renderer to the plot (no data yet)
    r = p.text(
        x=[],
        y=[],
        text=[],
        text_color=[],
        text_font_size="26px",
        text_baseline="middle",
        text_align="center",
    )

    i = 0

    ds = r.data_source

    # create a callback that adds a number in a random location
    def callback():
        print("fuck.")
        nonlocal i

        # BEST PRACTICE --- update .data in one step with a new dict
        new_data = dict()
        new_data["x"] = ds.data["x"] + [random() * 70 + 15]
        new_data["y"] = ds.data["y"] + [random() * 70 + 15]
        new_data["text_color"] = ds.data["text_color"] + [RdYlBu3[i % 3]]
        new_data["text"] = ds.data["text"] + [str(i)]
        ds.data = new_data

        i = i + 1

    # add a button widget and configure with the call back
    button = Button(label="Press Me")
    button.on_click(callback)

    # put the button and plot in a layout and add to the document
    curdoc().add_root(column(button, p))

    session = push_session(curdoc())
    session.show()

    # import dash
    # from dash import dcc, html
    # from dash.dependencies import Input, Output
    # import plotly.express as px
    # import threading
    # import plotly.graph_objects as go

    # reference_line = go.Scatter(x=[2, 4],
    #                             y=[4, 8],
    #                             mode="lines",
    #                             line=go.scatter.Line(color="gray"),
    #                             showlegend=False)

    # fig = px.line(x=[1, 2, 3], y=[5, 10, 99])

    # app = dash.Dash(__name__)
    # hello = html.P("Hello")
    # app.layout = html.Div([
    #     hello,
    #     dcc.Graph(id="graph", figure=fig),
    #     dcc.Interval(
    #         id='interval-component',
    #         interval=1000,
    #         n_intervals=0
    #     )
    # ])
    # # hello.children = ["wow!"]

    # @gv["?train_loss"].throttle(1).subscribe
    # def _(loss):
    #     fig.add_trace(reference_line)
    #     # hello.children = [str(loss)]
    #     # print(dir(hello))

    # # @app.callback(Output('graph', 'figure'),
    # #               Input('interval-component', 'n_intervals'))
    # # def update(n_intervals):
    # #     xs = list(range(n_intervals))
    # #     ys = [x * x for x in xs]
    # #     return px.line(x=xs, y=ys)

    # th = threading.Thread(target=lambda: app.run_server(debug=False))
    # th.start()


def main():
    # Training settings
    parser = argparse.ArgumentParser(description="PyTorch MNIST Example")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        metavar="N",
        help="input batch size for training (default: 64)",
    )
    parser.add_argument(
        "--test-batch-size",
        type=int,
        default=1000,
        metavar="N",
        help="input batch size for testing (default: 1000)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=14,
        metavar="N",
        help="number of epochs to train (default: 14)",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=1.0,
        metavar="LR",
        help="learning rate (default: 1.0)",
    )
    parser.add_argument(
        "--gamma",
        type=float,
        default=0.7,
        metavar="M",
        help="Learning rate step gamma (default: 0.7)",
    )
    parser.add_argument(
        "--no-cuda",
        action="store_true",
        default=False,
        help="disables CUDA training",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="quickly check a single pass",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=1,
        metavar="S",
        help="random seed (default: 1)",
    )
    parser.add_argument(
        "--log-interval",
        type=int,
        default=10,
        metavar="N",
        help="how many batches to wait before logging training status",
    )
    parser.add_argument(
        "--save-model",
        action="store_true",
        default=False,
        help="For Saving the current Model",
    )
    parser.add_argument("--wandb", default="", help="username:project for wandb")
    parser.add_argument("--comet", default="", help="username:project for comet")
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
        "--simple",
        action="store_true",
        default=False,
        help="whether to use the simple display method",
    )
    parser.add_argument(
        "--display-all",
        action="store_true",
        default=False,
        help="whether to display all given data",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        default=False,
        help="whether to plot the loss with plotly",
    )
    args = parser.parse_args()

    with given() as gv:
        if args.display_all:
            log_all(gv)
        elif args.rich:
            log_rich(gv)
        elif args.simple:
            log_simple(gv)
        else:
            log_terminal(gv)

        if args.wandb:
            log_wandb(gv, args)

        if args.comet:
            log_comet(gv, args)

        if args.mlflow:
            log_mlflow(gv, args)

        if args.plot:
            log_plot(gv)

        give(args=vars(args))

        with give.wrap("run"):
            run(args)


if __name__ == "__main__":
    main()
