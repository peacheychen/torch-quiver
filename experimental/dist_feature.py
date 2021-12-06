import torch
import quiver
import torch.multiprocessing as mp
from feature_server import start_server
from feature_client import FeatureClient

local_feature = torch.randint(0, 100, (250000, 600)).type(torch.float)
global2local = torch.arange(0, local_feature.shape[0])
quiver_feature = quiver.Feature(local_feature, device_list=[0], device_cache_size="100M")

if __name__ == "__main__":
    mp.set_start_method("spawn")
    feature_server_process = mp.Process(target=start_server, args=(local_feature, global2local, "feature_server", 0, 2))
    feature_server_process.daemon = True
    feature_server_process.start()
    feature_client = FeatureClient("client1", 1, 2, None)
    nodes = torch.randint(0, local_feature.shape[0], (25000, ))
    res = feature_client[nodes]
    feature_client.shutdown()














