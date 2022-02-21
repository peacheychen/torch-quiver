from pickle import NONE
import threading
from typing import List, Tuple, Union
import pytensorpipe as tp


class DispatchItem:
    def __init__(self, endpoint_idx, seeds) -> None:
        self.endpoint_idx_ = endpoint_idx
        self.seeds_ = seeds

    @property    
    def endpoint(self):
        return self.endpoint_idx_
    
    @property
    def task_data(self):
        return self.seeds_
    

class DistributeSageSampler:
    def __init__(self, master_node_adress, listen_adress, partition_result_path) -> None:
        self.listen_adress = listen_adress
        self.master_node_adress = master_node_adress
        self.client_context = None
        self.server_context = None
        self.local_idx = None
        self.partition_result_path = partition_result_path
        self.partition_book = None

        self.init()

    @staticmethod
    def on_server_connection():
        pass

    def load_partition_book(self):
        pass

    def init(self):
        # create client 
        self.client_context = tp.Context()
        self.client_context.register_transport(0, "tcp", tp.create_uv_transport())
        self.client_context.register_channel(0, "basic", tp.create_basic_channel())
        
        # create server
        self.server_context = tp.Context()
        self.server_context.register_transport(0, "tcp", tp.create_uv_transport())
        self.server_context.register_channel(0, "basic", tp.create_basic_channel())

    def dispatch(self, seeds):
        return None

    def data(self):
        pass

    def sample(self, seeds):
        dispatched_result:List[DispatchItem] = self.dispatch(seeds)
        local_task = None
        for dispatch_item in dispatched_result:
            if dispatch_item.endpoint != self.local_idx:
                pass
            else:
                local_task = dispatch_item