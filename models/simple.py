import torch
from torch import Tensor
from torch.nn import functional as F

class Simple(torch.nn.Module):
    def __init__(self, activation=F.tanh):
        super(Simple, self).__init__()
        self.layers = []
        self.activation = activation
        self.fc1 = torch.nn.Linear(2, 1, bias=None)
        self.eta = torch.nn.Parameter(Tensor([0.5]))

    def forward(self, x):
        x = torch.cat((x, x**2), 1)
        x = self.fc1(x)
        return x


if __name__ == '__main__':
    test = Simple()
    input = Tensor([[2],[4]])

    a = test(input)

    print(a)
