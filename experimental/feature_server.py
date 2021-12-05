import grpc
import feature_server_pb2_grpc
from concurrent import futures
import feature_server_pb2
import torch
import torch_quiver as torch_qv
import time
"""

class FeatureServerServicer(feature_server_pb2_grpc.FeatureServerServicer):
    def __init__(self, local_feature_tensor, global2local):
        self.local_feature_tensor = local_feature_tensor
        self.global2local = global2local
    
    def Collect(self, request: feature_server_pb2.CollectRequest, context):
        node_global_ids = torch.frombuffer(request.node_idx, dtype=torch.float, count = request.node_count).type(torch.long)
        req_id = request.req_id
        start = time.time()
        node_local_ids = self.global2local[node_global_ids]
        feature = self.local_feature_tensor[node_local_ids]
        feature_bytes = torch_qv.torch_tensor_to_bytes(feature)
        print(f"result size = {len(feature_bytes) // 1024 // 1024} MB")
        response = feature_server_pb2.CollectReply()
        response.feature = feature_bytes
        response.node_count = node_local_ids.shape[0]
        response.req_id = req_id
        print(f"time consumed on server {time.time() - start}")
        return response


def serve():
    local_feature = torch.randint(0, 100, (230000, 600)).type(torch.float)
    global2local = torch.range(0, local_feature.shape[0]).type(torch.long)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    feature_server_pb2_grpc.add_FeatureServerServicer_to_server(
        FeatureServerServicer(local_feature, global2local), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
"""
import torch
import torch.distributed.rpc as rpc

local_feature = torch.randint(0, 100, (230000, 600))
def collect(node_idx):
    return local_feature[node_idx]

rpc.init_rpc("worker0", rank=0, world_size=2)
nodes = torch.randint(0, 230000, (int(250000 * 0.2), ))
ret = rpc.rpc_sync("worker1", collect, args=(nodes, ))

for _ in range(10):
    start = time.time()
    ret = rpc.rpc_sync("worker1", collect, args=(nodes, ))
    print(f"torch rpc time = {time.time() - start}s for {ret.numel() * 4 // 1024 // 1024} MB")

rpc.shutdown()


        