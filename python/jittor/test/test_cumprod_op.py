# ***************************************************************
# Copyright (c) 2020 Jittor. Authors: 
#     Guowei Yang <471184555@qq.com>
#     Dun Liang <randonlang@gmail.com>. 
# All Rights Reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# ***************************************************************
import unittest
import jittor as jt
import numpy as np
import ctypes
import sys
import torch
from torch.autograd import Variable

class TestCumprod(unittest.TestCase):
    def test_cumprod_cpu(self):
        jt.flags.use_cuda = 0

        for i in range(1,6):
            for j in range(i):
                x = np.random.rand(*((10,)*i))
                x_jt = jt.array(x)
                y_jt = jt.cumprod(x_jt, j).sqr()
                g_jt = jt.grad(y_jt.sum(), x_jt)
                x_tc = Variable(torch.from_numpy(x), requires_grad=True)
                y_tc = torch.cumprod(x_tc, j)**2
                y_tc.sum().backward()
                g_tc = x_tc.grad
                assert np.allclose(y_jt.numpy(), y_tc.data)
                assert np.allclose(g_jt.numpy(), g_tc.data)

    def test_cumprod_gpu(self):
        jt.flags.use_cuda = 1
        
        for i in range(1,6):
            for j in range(i):
                x = np.random.rand(*((10,)*i))
                x_jt = jt.array(x)
                y_jt = jt.cumprod(x_jt, j).sqr()
                g_jt = jt.grad(y_jt.sum(), x_jt)
                x_tc = Variable(torch.from_numpy(x), requires_grad=True)
                y_tc = torch.cumprod(x_tc, j)**2
                y_tc.sum().backward()
                g_tc = x_tc.grad
                assert np.allclose(y_jt.numpy(), y_tc.data)
                assert np.allclose(g_jt.numpy(), g_tc.data)

if __name__ == "__main__":
    unittest.main()