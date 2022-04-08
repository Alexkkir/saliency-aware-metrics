import torch

x = torch.tensor([1.0], requires_grad=True)
# optimizer = torch.optim.SGD([x], lr=0.99)

def f(x):
    return (x ** 2).sum()


def step(f, x):
    r = f(x)
    r.backward()
    # optimizer.step()
    # optimizer.zero_grad()
    x.data -= 1 * x.grad
    x.grad.zero_()

for i in range(1000):
    step(f, x)

print(x)