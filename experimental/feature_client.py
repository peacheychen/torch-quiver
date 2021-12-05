from __future__ import print_function

import logging
import random

"""
import grpc
import feature_server_pb2
import feature_server_pb2_grpc
import torch
import torch_quiver as torch_qv
import time
def run():
    MAX_MESSAGE_LENGTH = 900 * 1024 * 1024
    with grpc.insecure_channel(
        'localhost:50051',
        options=[
            ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
            ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
        ],
    ) as channel:
        stub = feature_server_pb2_grpc.FeatureServerStub(channel)
        nodes = torch.randint(0, 230000, (250000, )).type(torch.float)
        node_bytes = torch_qv.torch_tensor_to_bytes(nodes)
        msg = feature_server_pb2.CollectRequest(
            req_id="0",
            node_idx= node_bytes,
            node_count= nodes.shape[0]
        )

        start = time.time()
        res = stub.Collect(msg)
        feature = torch.frombuffer(res.feature, dtype=torch.float)
        #print(feature.shape)
        
        print(f"Collection Time: {time.time() - start}s ")
if __name__ == "__main__":
    run()
"""

import torch
import torch.distributed.rpc as rpc
local_feature = torch.randint(0, 100, (230000, 600)).type(torch.float)
def collect(node_idx):
    return local_feature[node_idx]

rpc.init_rpc("worker1", rank=1, world_size=2)
rpc.shutdown()



