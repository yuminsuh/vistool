""" Plot SN weights """

import torch
import torch.nn as nn
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
from plot import plot_mult_bar


#model_path = '/home/yumin/codes/domain_adaptation_dg/output/pacs/lr1e-2_mobilenetsn_inlnbn_init/mobilenetsn_1e-02_mul2photo_b32_trainsplit/best_mobilenetsn+None+i0_None2photo.pth'
#model_path = '/home/yumin/codes/domain_adaptation_dg/output/pacs/lr1e-2_mobilenetsn_inlnbn_init/mobilenetsn_1e-02_mul2photo_b32_trainsplit/best_mobilenetsn+None+i0_None2photo.pth'
model_path = '/home/yumin/codes/domain_adaptation_dg/output/pacs/lr1e-2_slnsn/resnet18slnsn_1e-02_mul2art_painting_b48_trainsplit/best_resnet18slnsn+None+i0_None2art_painting.pth'
state_dict = torch.load(model_path)

softmax = nn.Softmax(0)

mean_weights = OrderedDict()
var_weights = OrderedDict()
for k in state_dict['model'].keys():
    if 'mean_weight' in k:
        mean_weights[k] = softmax(state_dict['model'][k]).numpy()
    if 'var_weight' in k:
        var_weights[k]= softmax(state_dict['model'][k]).numpy()

xs = ['.'.join(k.split('.')[:2]) for k in mean_weights]
#ys = np.array([w for _,w in mean_weights.items()]).transpose()
ys = np.array([w for _,w in var_weights.items()]).transpose()
print(xs)
print(ys)
plot_mult_bar(xs, ys, ['IN', 'LN', 'BN'])

