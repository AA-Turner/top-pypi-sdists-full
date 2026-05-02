import sys

import torchvision
from torch.utils import data
from torchvision import transforms

from g2fl.common import *  # noqa
from g2fl.dldata import *  # noqa
from g2fl.plotting import *  # noqa
from g2fl.rnn import *  # noqa
from g2fl.train import *  # noqa

dl = sys.modules[__name__]


def synthetic_data(w, b, num_examples):
    """生成 y = Wx + b + 噪声。"""
    X = torch.normal(0, 1, (num_examples, len(w)))
    y = torch.matmul(X, w) + b
    y += torch.normal(0, 0.01, y.shape)
    return X, y.reshape((-1, 1))


def get_fashion_mnist_labels(labels):
    """Return text labels for the Fashion-MNIST dataset."""

    text_labels = [
        "t-shirt",
        "trouser",
        "pullover",
        "dress",
        "coat",
        "sandal",
        "shirt",
        "sneaker",
        "bag",
        "ankle boot",
    ]
    return [text_labels[int(i)] for i in labels]


def get_dataloader_workers():
    """Use 4 processes to read the data."""
    return 4


def load_data_fashion_mnist(batch_size, resize=None):
    """下载Fashion-MNIST数据集，然后将其加载到内存中"""
    trans = [transforms.ToTensor()]
    if resize:
        trans.insert(0, transforms.Resize(resize))
    trans = transforms.Compose(trans)
    mnist_train = torchvision.datasets.FashionMNIST(
        root="../data", train=True, transform=trans, download=True
    )
    mnist_test = torchvision.datasets.FashionMNIST(
        root="../data", train=False, transform=trans, download=True
    )
    return (
        data.DataLoader(
            mnist_train,
            batch_size,
            shuffle=True,
            num_workers=get_dataloader_workers(),
        ),
        data.DataLoader(
            mnist_test,
            batch_size,
            shuffle=False,
            num_workers=get_dataloader_workers(),
        ),
    )


def corr2d(X: torch.tensor, K: torch.tensor):
    h, w = K.shape
    Y = torch.zeros((X.shape[0] - h + 1, X.shape[1] - w + 1))
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            Y[i, j] = (X[i : i + h, j : j + w] * K).sum()
    return Y


def num_gpus():
    """Get the number of available GPUs."""
    return torch.cuda.device_count()


def try_gpu(i=0):
    """Return gpu(i) if exists, otherwise return cpu()."""
    if num_gpus() >= i + 1:
        return gpu(i)
    return cpu()


def cpu():
    """Get the CPU device."""

    return torch.device("cpu")


def gpu(i=0):
    """Get a GPU device."""

    return torch.device(f"cuda:{i}")
