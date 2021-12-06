from concurrent import futures
import torch
import torch_quiver as torch_qv
import time

import torch
import torch.distributed.rpc as rpc

import os

MASTER_ADDR = '155.198.152.17'
os.environ['MASTER_ADDR'] = MASTER_ADDR
os.environ['MASTER_PORT'] = '12355'
os.environ['GLOO_SOCKET_IFNAME']='eth0'
os.environ['TP_SOCKET_IFNAME']='eth0'


LocalFeature = None
Global2Local = None

def collect(node_idx):
    local_idx = Global2Local[node_idx]
    return LocalFeature[local_idx]

def start_server(local_feature, global2local, worker_name, rank, world_size):
    global LocalFeature, Global2Local
    LocalFeature = local_feature
    Global2Local = global2local
    rpc.init_rpc(worker_name, rank=rank, world_size=world_size)
    rpc.shutdown()

if __name__ == "__main__":
    local_feature = torch.randint(0, 100, (230000, 600)).type(torch.float)
    global2local = torch.arange(0, local_feature.shape[0])
    start_server(local_feature, global2local)


        