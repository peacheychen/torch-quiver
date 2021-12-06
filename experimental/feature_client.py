from concurrent import futures
import torch
import torch_quiver as torch_qv
import time

import torch
import torch.distributed.rpc as rpc
from feature_server import collect
import os

MASTER_ADDR = '155.198.152.17'
os.environ['MASTER_ADDR'] = MASTER_ADDR
os.environ['MASTER_PORT'] = '12355'
os.environ['GLOO_SOCKET_IFNAME']='eth0'
os.environ['TP_SOCKET_IFNAME']='eth0'


class FeatureClient:
    def __init__(self, worker_name, rank, world_size, partition_book=None):
        rpc.init_rpc(worker_name, rank=rank, world_size=world_size)
        self.rank = rank
        self.world_size = world_size
        self.partititon_book = partition_book


    def collect(self, nodes):
        start = time.time()
        ret = rpc.rpc_sync(0, collect, args=(nodes, ))
        print(f"Total Data = {ret.numel() * 4 // 1024 // 1024} MB\tTotal consumed time = {time.time() - start}s\tNetwork throughput = {ret.numel() * 4 / (time.time() - start) // 1024 // 1024} MB/s")

    
    def __getitem__(self, nodes):
        start = time.time()
        ret = rpc.rpc_sync(0, collect, args=(nodes, ))
        print(f"Total Data = {ret.numel() * 4 // 1024 // 1024} MB\tTotal consumed time = {time.time() - start}s\tNetwork throughput = {ret.numel() * 4 / (time.time() - start) // 1024 // 1024} MB/s")
        return ret

    def shutdown(self):
        rpc.shutdown()
