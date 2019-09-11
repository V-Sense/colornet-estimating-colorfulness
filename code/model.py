# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
from mobile_net_v2 import mobile_net_v2
class NIMA(nn.Module):
    """Neural IMage Assessment model by Google"""
    def __init__(self, base_model, num_classes=10):
        super(NIMA, self).__init__()
        self.features = base_model.features
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.75),
            nn.Linear(in_features=25088, out_features=num_classes),
            nn.ReLU(),
            nn.Linear(in_features=num_classes, out_features=1),
#            nn.Softmax()
            )

    def forward(self, x):
        out = self.features(x)
        out = out.view(out.size(0), -1)
        out = self.classifier(out)
        return out

#    def __init__(self, base_model):
#        super(NIMA, self).__init__()
#        base_model = nn.Sequential(*list(base_model.children())[:-2])
#
#        self.features = base_model
#
#        self.classifier = nn.Sequential(
#            nn.Dropout(p=0.75),
#            nn.Linear(25088, 10),
#            nn.ReLU(),
#            nn.Linear(in_features= 10, out_features=1),
#        )
#
#    def forward(self, x):
#        x = self.features(x)
#        x = x.view(x.size(0), -1)
#        x = self.classifier(x)
#        return x

        
#    def __init__(self, pretrained_base_model=True):
#        super(NIMA, self).__init__()
#        base_model = mobile_net_v2(pretrained=pretrained_base_model)
#        base_model = nn.Sequential(*list(base_model.children())[:-1])
#
#        self.features = base_model
#
#        self.classifier = nn.Sequential(
#            nn.ReLU(inplace=True),
#            nn.Dropout(p=0.75),
#            nn.Linear(1280, 10),
#            nn.ReLU(),
#            nn.Linear(in_features= 10, out_features=1),
#        )
#
#    def forward(self, x):
#        x = self.features(x)
#        x = x.view(x.size(0), -1)
#        x = self.classifier(x)
#        return x


def single_emd_loss(p, q, r=2):
    """
    Earth Mover's Distance of one sample

    Args:
        p: true distribution of shape num_classes × 1
        q: estimated distribution of shape num_classes × 1
        r: norm parameter
    """
    assert p.shape == q.shape, "Length of the two distribution must be the same"
    length = p.shape[0]
    emd_loss = 0.0
    for i in range(1, length + 1):
        emd_loss += sum(torch.abs(p[:i] - q[:i])) ** r
    return (emd_loss / length) ** (1. / r)


def emd_loss(p, q, r=2):
    """
    Earth Mover's Distance on a batch

    Args:
        p: true distribution of shape mini_batch_size × num_classes × 1
        q: estimated distribution of shape mini_batch_size × num_classes × 1
        r: norm parameters
    """
    assert p.shape == q.shape, "Shape of the two distribution batches must be the same."
    mini_batch_size = p.shape[0]
    loss_vector = []
    for i in range(mini_batch_size):
        loss_vector.append(single_emd_loss(p[i], q[i], r=r))
    return sum(loss_vector) / mini_batch_size


