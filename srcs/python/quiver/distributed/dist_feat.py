import torch.distributed.rpc as rpc
import quiver.partition as quiver_partition

class DistFeature:
    def __init__(self, master_node_adress, local_listen_address, rank, partition_result_path):
        self.local_listen_address = local_listen_adress
        
        