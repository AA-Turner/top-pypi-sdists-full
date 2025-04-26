import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from dask.distributed import print

import coiled


# Define our model
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 1024, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(1024, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


@coiled.function(vm_type="g5.2xlarge", region="us-west-2")
def train():
    # Select hardware to run on
    device = torch.device("cuda")
    print("Running on a GPU 🔥\n")

    model = Net()
    model = model.to(device)

    # Load dataset
    print("Downloading training data...")
    trainset = torchvision.datasets.CIFAR10(
        root="./data",
        train=True,
        download=True,
        transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(
                (0.4914, 0.4822, 0.4465),
                (0.2470, 0.2435, 0.2616),
            ),  # noqa
        ]),
    )
    trainloader = torch.utils.data.DataLoader(
        trainset,
        batch_size=256,
        shuffle=True,
    )
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    print("Training...")
    for epoch in range(10):
        print(f"Epoch {epoch + 1} / 10")
        model.train()
        for batch in trainloader:
            # Move training data to device
            inputs, labels = batch[0].to(device), batch[1].to(device)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

    return model.to("cpu")


model = train()
print(model)

# Tip: Press enter to run this cell.
# When you're done, type "exit" + enter to exit IPython.
