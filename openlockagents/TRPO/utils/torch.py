import torch
import numpy as np

use_gpu = torch.cuda.is_available()
DoubleTensor = torch.cuda.DoubleTensor if use_gpu else torch.DoubleTensor
FloatTensor = torch.cuda.FloatTensor if use_gpu else torch.FloatTensor
LongTensor = torch.cuda.LongTensor if use_gpu else torch.LongTensor
ByteTensor = torch.cuda.ByteTensor if use_gpu else torch.ByteTensor


def ones(*shape):
    return torch.ones(*shape).cuda() if use_gpu else torch.ones(*shape)


def zeros(*shape, **kwargs):
    return torch.zeros(*shape).cuda() if use_gpu else torch.zeros(*shape)


def get_flat_params_from(model):
    params = []
    for param in model.parameters():
        params.append(param.data.view(-1))

    flat_params = torch.cat(params)
    return flat_params


def set_flat_params_to(model, flat_params):
    prev_ind = 0
    for param in model.parameters():
        flat_size = int(np.prod(list(param.size())))
        param.data.copy_(
            flat_params[prev_ind : prev_ind + flat_size].view(param.size())
        )
        prev_ind += flat_size


def get_flat_grad_from(net, grad_grad=False):
    grads = []
    for param in net.parameters():
        if grad_grad:
            grads.append(param.grad.grad.view(-1))
        else:
            grads.append(param.grad.view(-1))

    flat_grad = torch.cat(grads)
    return flat_grad


def set_lr(optimizer, lr):
    s = optimizer.state_dict()
    s["param_groups"][0]["lr"] = lr
    optimizer.load_state_dict(s)
