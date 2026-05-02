import torch
from torch import nn

from g2fl.common import *  # noqa
from g2fl.plotting import Animator


def evaluate_loss(net, data_iter, loss):
    """Evaluate the loss of a model on the given dataset."""

    metric = Accumulator(2)  # Sum of losses, no. of examples
    for X, y in data_iter:
        out = net(X)
        y = y.reshape(out.shape)
        ls = loss(out, y)
        metric.add(ls.sum(), ls.numel())
    return metric[0] / metric[1]


def accuracy(y_hat, y):
    if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:
        y_hat = y_hat.argmax(axis=1)
    y_type_y_hat = y_hat.type(y.dtype)
    cmp = y_type_y_hat == y
    return float(cmp.type(y.dtype).sum())


def evaluate_accuracy(net, data_iter):
    if isinstance(net, torch.nn.Module):
        net.eval()
    metric = Accumulator(2)
    with torch.no_grad():
        for X, y in data_iter:
            metric.add(accuracy(net(X), y), y.numel())
    return metric[0] / metric[1]


def evaluate_accuracy_gpu(net, data_iter, device=None):
    if isinstance(net, nn.Module):
        net.eval()
        if not device:
            device = next(iter(net.parameters())).device
    metric = Accumulator(2)
    with torch.no_grad():
        for X, y in data_iter:
            if isinstance(X, list):
                X = [x.to(device) for x in X]
            else:
                X = X.to(device)
            y = y.to(device)
            metric.add(accuracy(net(X), y), y.numel())
    return metric[0] / metric[1]


def train_epoch_reg(net, train_iter, loss, updater):
    """训练模型一个迭代周期"""
    if isinstance(net, torch.nn.Module):
        net.train()
    metric = Accumulator(3)
    for X, y in train_iter:
        y_hat = net(X)
        ls = loss(y_hat, y)
        if isinstance(updater, torch.optim.Optimizer):
            updater.zero_grad()
            ls.mean().backward()
            updater.step()
        else:
            ls.sum().backward()
            updater(X.shape[0])
        metric.add(float(ls.sum()), accuracy(y_hat, y), y.numel())
    return metric[0] / metric[2], metric[1] / metric[2]


def train_reg(net, train_iter, test_iter, loss, num_epochs, updater):
    animator = Animator(
        xlabel="epoch",
        xlim=[1, num_epochs],
        ylim=[0.3, 0.9],
        legend=["train loss", "train acc", "test acc"],
    )
    for epoch in range(num_epochs):
        train_metrics = train_epoch_reg(net, train_iter, loss, updater)
        test_acc = evaluate_accuracy(net, test_iter)
        animator.add(epoch + 1, train_metrics + (test_acc,))
    train_loss, train_acc = train_metrics
    assert train_loss < 0.5, train_loss
    assert 1 >= train_acc > 0.7, train_acc


def train_conv(net, train_iter, test_iter, num_epochs, lr, device):
    def init_weights(m):
        if type(m) is nn.Linear or type(m) is nn.Conv2d:
            nn.init.xavier_uniform_(m.weight)

    net.apply(init_weights)
    print("training on ", device)
    net.to(device)
    optimizer = torch.optim.SGD(net.parameters(), lr=lr)
    loss = nn.CrossEntropyLoss()
    animator = Animator(
        xlabel="epoch",
        xlim=[1, num_epochs],
        legend=["train loss", "train acc", "test acc"],
    )
    timer, num_batches = Timer(), len(train_iter)
    for epoch in range(num_epochs):
        metric = Accumulator(3)
        net.train()
        for i, (X, y) in enumerate(train_iter):
            timer.start()
            optimizer.zero_grad()
            X, y = X.to(device), y.to(device)
            y_hat = net(X)
            ls = loss(y_hat, y)
            ls.backward()
            optimizer.step()
            with torch.no_grad():
                metric.add(ls * X.shape[0], accuracy(y_hat, y), X.shape[0])
            timer.stop()
            train_l = metric[0] / metric[2]
            train_acc = metric[1] / metric[2]
            if (i + 1) % (num_batches // 5) == 0 or i == num_batches - 1:
                animator.add(epoch + (i + 1) / num_batches, (train_l, train_acc, None))
        test_acc = evaluate_accuracy_gpu(net, test_iter)
        animator.add(epoch + 1, (None, None, test_acc))
    print(f"loss {train_l:.3f}, train acc {train_acc:.3f}, " f"test acc {test_acc:.3f}")
    print(
        f"{metric[2] * num_epochs / timer.sum():.1f} examples/sec " f"on {str(device)}"
    )
