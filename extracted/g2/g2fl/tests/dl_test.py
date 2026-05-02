import torch

from g2fl import dl


def test_synthetic_data():
    true_w = torch.tensor([2, -3.4])
    true_b = 4.2
    features, labels = dl.synthetic_data(true_w, true_b, 1000)
    assert len(labels) == 1000
    assert len(features) == 1000


def test_load_data_fashion_mnist():
    batch_size = 30
    train_iter, test_iter = dl.load_data_fashion_mnist(batch_size)
    for X, y in train_iter:
        assert len(X) == batch_size
        assert len(y) == batch_size
        assert list(X.shape) == [batch_size, 1, 28, 28]
        break


def test_accuracy():
    y = torch.tensor([0, 2])
    y_hat = torch.tensor([[0.1, 0.3, 0.6], [0.3, 0.2, 0.5]])
    accuracy = dl.accuracy(y_hat, y)
    assert accuracy == 1


def test_accumulator():
    metric = dl.Accumulator(2)
    metric.add(1, 2)
    metric.add(2, 3)
    assert metric[0] == 1 + 2
    assert metric[1] == 2 + 3
