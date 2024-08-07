# RUN: %PYTHON %s | FileCheck %s

import torch
import numpy as np

from mpact.mpactbackend import mpact_jit

from mpact.models.resnet import resnet_20

resnet = resnet_20()
resnet.eval()  # Switch to inference.

# Get a random input.
#   B x RGB x H x W
x = torch.rand(1, 3, 16, 16)

#
# CHECK: pytorch
# CHECK: mpact
# CHECK: passed
#

with torch.no_grad():
    # Run it with PyTorch.
    print("pytorch")
    res1 = resnet(x)
    print(res1)

    # Run it with MPACT.
    print("mpact")
    res2 = mpact_jit(resnet, x)
    print(res2)

# Completely different inputs and weights for each run,
# so we simply verify the two results are the same.
np.testing.assert_allclose(res1.numpy(), res2, rtol=1e-5, atol=0)
print("passed")
