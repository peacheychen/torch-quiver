import ray
import numpy as np
from ray.util.queue import Queue as DistQueue
import torch
import time
import os

class DistTensorConfig:
    """
    {
        "machine_memory_budget": xxx
        "198.xxx.xxx.xxx": {
            start_index: 0,
            end_index: 0,
        },
        "198.xxx.xxx.xxx": {
            start_index: 0,
            end_index: 0,
        },

    }
    """
    def __init__(self):
        pass

class FeatureDataset:
    def __init__(self, data_path):
        self.data_path = data_path
        self.inited = False
        self.feature = None
    
    def lazy_init(self):
        if self.inited:
            return
        data, _ = torch.load(self.data_path)
        self.feature = data.x

    def __getitem__(self, nodes):
        self.lazy_init()
        return self.feature[nodes]

data_path = "/home/dalong/data/products/ogbn_products/processed/geometric_data_processed.pt"
graph_feature = FeatureDataset(data_path)

@ray.remote
def worker(graph_feature, index_queue, result_queue, worker_index):
    while True:
        print(f"enter {os.getpid()}")
        node_idx = index_queue.get()
        print(node_idx.shape)
        data = graph_feature[node_idx]
        result_queue.put(data)
        print(f"exit {os.getpid()}")
        break

num_workers = 50

index_queue_lst = []
result_queue = DistQueue()

for worker_index in range(num_workers):
    index_queue = DistQueue()
    worker.remote(graph_feature, index_queue, result_queue, worker_index)
    index_queue_lst.append(index_queue)


total_node_num = 2000000
node_count = 250000
index =  torch.randint(0, high=total_node_num, size=(node_count,))

for worker_index in range(num_workers):
    index_queue_lst[worker_index].put(index)

start = time.time()
for worker_index in range(num_workers):
    item = result_queue.get()

end = time.time()
print(f"Average time is {(end - start) / num_workers}")

"""
node_idx = sample(seeds)

# prefetch
def prefetch(self):
    for worker_idx in range(worker_nums):
        for _ in range(prefetch_factor):
            feature, remote_idx, orders = quiver.Feature(node_idx)
            index_queue[randint()].put(remote_idx)
            msg_queue.append((idx, feature, orders))

def __next__(self):
    data, index_queue_idx = result_queue.get()
    feature[orders] = data.to(0)
    feature, remote_idx, orders = quiver.Feature(node_idx)
    index_queue[index_queue_idx].put(remote_idx)
    msg_queue.append((idx, feature, orders))
    return feature


"""









