#!/usr/bin/env python3

import torch

def get_backend():
    cuda_flg = torch.cuda.is_available()
    mps_flg = torch.backends.mps.is_available()

    if cuda_flg:
        return "cuda"
    elif mps_flg:
        return "mps"
    else:
        return "cpu"
